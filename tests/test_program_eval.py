"""Negative controls for the longitudinal evaluator, not tests of generated prose."""
import copy
import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
import program as evaluation
from fixture import harbor


class ProgramEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.result = self.workspace / 'result'
        self.result.mkdir()
        self.data = harbor(False)
        for n in range(4, 7):
            task = copy.deepcopy(self.data['tasks'][0])
            task['id'] = f'T{n}'
            self.data['tasks'].append(task)
        for source in self.data['sources']:
            path = self.result / source['location']
            path.parent.mkdir(exist_ok=True)
            path.write_text('Synthetic source', encoding='utf-8')
        (self.result / 'public').mkdir()
        (self.result / 'public/guide.md').write_text('Draft candidate guide.', encoding='utf-8')

    def check(self):
        (self.result / 'program.json').write_text(json.dumps(self.data), encoding='utf-8')
        return evaluation.checks(self.workspace, 1)

    def test_good_structure_still_requires_substantive_review(self):
        # Duplicated tasks and placeholder sources pass structural checks by design.
        # A reviewer must reject this as a real deliverable.
        self.assertEqual(self.check(), [])

    def test_missing_local_evidence_fails(self):
        (self.result / self.data['sources'][0]['location']).unlink()
        self.assertTrue(any('not portable' in x for x in self.check()))

    def test_absolute_source_reference_fails(self):
        self.data['sources'][0]['location'] = str(self.result / 'sources/data.md')
        self.assertTrue(any('not portable' in x for x in self.check()))

    def test_public_bank_disclosure_fails(self):
        (self.result / 'public/guide.md').write_text(self.data['items'][0]['prompt'], encoding='utf-8')
        self.assertTrue(any('leaked' in x for x in self.check()))

    def test_invented_approval_fails(self):
        self.data['items'][0]['status'] = 'approved'
        self.assertTrue(any('falsely approved' in x for x in self.check()))

    def test_fictional_source_cannot_become_real(self):
        self.data['sources'][0]['evidence_kind'] = 'real'
        self.assertTrue(any('relabeled as real' in x for x in self.check()))

    def test_review_cannot_accept_failed_grade(self):
        phase = self.workspace / 'phase-1'
        output = phase / 'workspace/result'
        output.mkdir(parents=True)
        evaluation.write(phase / 'grade.json', {'mechanical_passed': False, 'output_hashes': {}})
        findings = {k: 'Concrete finding' for k in ('source_correctness', 'owner_usefulness',
            'measurement_judgment', 'privacy', 'continuity')}
        path = self.workspace / 'review-input.json'
        evaluation.write(path, {'accepted': True, 'reviewer': 'Test reviewer', 'reviewer_type': 'model', 'findings': findings})
        with self.assertRaisesRegex(ValueError, 'mechanical failure'):
            evaluation.review(self.workspace, 1, path)

    def test_review_cannot_accept_changed_outputs(self):
        phase = self.workspace / 'phase-1'
        output = phase / 'workspace/result'
        output.mkdir(parents=True)
        evaluation.write(phase / 'grade.json', {'mechanical_passed': True, 'output_hashes': {}})
        (output / 'changed.txt').write_text('Changed after grading', encoding='utf-8')
        findings = {k: 'Concrete finding' for k in ('source_correctness', 'owner_usefulness',
            'measurement_judgment', 'privacy', 'continuity')}
        path = self.workspace / 'review-input.json'
        evaluation.write(path, {'accepted': True, 'reviewer': 'Test reviewer', 'reviewer_type': 'model', 'findings': findings})
        with self.assertRaisesRegex(ValueError, 'changed after grading'):
            evaluation.review(self.workspace, 1, path)

    def test_two_phase_receipts_and_wrong_analysis_negative_control(self):
        # End-to-end runner control. This authored fixture is not a model success.
        run = self.workspace / 'run'
        evaluation.prepare(run, 1)
        self.check()
        shutil.copytree(self.result, run / 'phase-1/workspace/result')
        grade = evaluation.grade(run, 1)
        self.assertTrue(grade['mechanical_passed'])
        review_file = self.workspace / 'review.json'
        evaluation.write(review_file, {'accepted': True, 'reviewer': 'Synthetic test control',
            'reviewer_type': 'model', 'findings': {k: 'Authored control, no acceptance claim'
            for k in ('source_correctness', 'owner_usefulness', 'measurement_judgment', 'privacy', 'continuity')}})
        evaluation.review(run, 1, review_file)
        evaluation.prepare(run, 2)
        workspace = run / 'phase-2/workspace'
        inputs, result = workspace / 'inputs', workspace / 'result'
        historical = evaluation.c.load(inputs / 'pilot-snapshot.json')
        current = copy.deepcopy(historical)
        current['items'][0]['revision'] += 1
        current['items'][0]['status'] = 'draft'
        current['items'][0]['prompt'] += ' Revised.'
        (result / 'program.json').write_text(json.dumps(current), encoding='utf-8')
        evidence = result / 'pilot-evidence'
        evidence.mkdir()
        for path in inputs.glob('*'):
            if path.is_file():
                shutil.copy2(path, evidence / path.name)
        with (inputs / 'pilot-scores.csv').open(encoding='utf-8', newline='') as stream:
            rows = list(csv.reader(stream))
        complete = result / 'complete.csv'
        with complete.open('w', encoding='utf-8', newline='') as stream:
            csv.writer(stream).writerows([rows[0], *[r for r in rows[1:] if '' not in r]])
        analysis = evaluation.c.analyze(historical, 'PILOT1', complete)
        evaluation.write(result / 'pilot-analysis.json', analysis)
        evaluation.write(result / 'panel-summary.json', evaluation.c.panel_summary(
            historical, 'PILOT1', inputs / 'panel-judgments.csv'))
        for name in ('summary.md', 'release-recommendation.md'):
            (result / name).write_text('Synthetic runner control.', encoding='utf-8')
        self.assertEqual(evaluation.checks(workspace, 2), [])
        analysis['mean_total'] = -100
        (result / 'pilot-analysis.json').write_text(json.dumps(analysis), encoding='utf-8')
        self.assertTrue(any('23 complete historical' in x for x in evaluation.checks(workspace, 2)))
        (inputs / 'access-v2.md').write_text('Tampered input', encoding='utf-8')
        grade = evaluation.grade(run, 2)
        self.assertFalse(grade['mechanical_passed'])
        self.assertIn('inputs changed during evaluation.', grade['failures'])
        with self.assertRaises(FileExistsError):
            evaluation.grade(run, 2)


if __name__ == '__main__':
    unittest.main()
