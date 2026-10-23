import copy
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from fixture import c, harbor, changed_source, write_scores


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ProgramTests(unittest.TestCase):
    def setUp(self):
        self.d = harbor()

    def test_from_scratch_is_empty_but_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'program'
            c.initialize(path, 'new-program', 'New program')
            data = c.load(path / 'program.json')
            self.assertTrue(c.validate(data)['valid_structure'])
            self.assertEqual(data['items'], [])
            self.assertIn('charter', c.status(data)['next_action'])
            self.assertTrue((path / 'working-templates.md').is_file())
            with self.assertRaises(ValueError): c.initialize(path, 'x', 'X')

    def test_invalid_schema_and_identity(self):
        for key, value in [('schema_version', 99), ('items', {})]:
            d = copy.deepcopy(self.d); d[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): c.validate(d)
        with self.assertRaises(ValueError): c.new_program('../escape', 'x')

    def test_duplicate_and_unknown_references(self):
        self.d['items'].append(copy.deepcopy(self.d['items'][0]))
        with self.assertRaises(ValueError): c.validate(self.d)
        self.d = harbor(); self.d['items'][0]['source_refs'][0]['version'] = 'missing'
        with self.assertRaises(ValueError): c.validate(self.d)

    def test_weight_and_rubric_invariants(self):
        self.d['blueprint']['domains'][0]['weight'] = 49
        with self.assertRaises(ValueError): c.validate(self.d)
        self.d = harbor(); next(i for i in self.d['items'] if i['type'] == 'practical')['max_score'] = 8
        with self.assertRaises(ValueError): c.validate(self.d)

    def test_invalid_option_key_and_competency(self):
        self.d['items'][0]['answer_key'] = 'Z'
        with self.assertRaises(ValueError): c.validate(self.d)
        self.d = harbor(); self.d['items'][0]['competency_ids'] = ['C3']
        with self.assertRaises(ValueError): c.validate(self.d)

    def test_item_count_allocation_exact_and_rounded(self):
        self.assertEqual(c.allocation(self.d), {'D': 4, 'S': 2, 'R': 2})
        self.d['blueprint']['form_length'] = 7
        self.assertEqual(c.allocation(self.d), {'D': 3, 'S': 2, 'R': 2})

    def test_zero_domain_rounding_is_visible(self):
        self.d['blueprint']['form_length'] = 1
        self.assertFalse(c.coverage(self.d)['ready_to_assemble'])
        with self.assertRaises(ValueError): c.assemble(self.d, 'NEW')

    def test_approved_label_without_review_fails(self):
        self.d['reviews'] = []
        self.assertFalse(c.assemble(self.d, 'NEW')['assembled'])

    def test_new_revision_invalidates_review(self):
        self.d['items'][0]['revision'] += 1
        self.assertIn('missing_current_content_acceptance', c.item_issues(self.d, self.d['items'][0]))
        self.assertIn('stale_item_revision:D01', c.check_form(self.d, 'PILOT1')['issues'])

    def test_content_edit_without_revision_is_detected(self):
        self.d['items'][0]['prompt'] += ' Changed condition.'
        self.assertIn('missing_current_content_acceptance', c.item_issues(self.d, self.d['items'][0]))

    def test_unresolved_negative_review_blocks_acceptance(self):
        self.d['reviews'].append(dict(self.d['reviews'][0], id='NEG', verdict='reject'))
        self.assertIn('unresolved_negative_review', c.item_issues(self.d, self.d['items'][0]))
        self.d['reviews'][-1].update(resolved=True, resolution='Resolved with source evidence.', resolved_by='Synthetic owner')
        self.assertNotIn('unresolved_negative_review', c.item_issues(self.d, self.d['items'][0]))

    def test_source_change_blocks_current_release_preserves_history(self):
        changed = changed_source(self.d)
        self.assertFalse(c.check_form(changed, 'PILOT1')['checks_pass'])
        self.assertTrue(c.check_form(self.d, 'PILOT1')['checks_pass'])
        self.assertEqual(c.impact(changed, ['SEC'])['items'], ['S01', 'S02', 'S03'])

    def test_live_never_accepts_demo(self):
        result = c.check_form(self.d, 'PILOT1', True)
        self.assertFalse(result['checks_pass'])
        self.assertIn('synthetic_program', result['issues'])
        self.assertFalse(c.assemble(self.d, 'LIVE', live=True)['assembled'])

    def test_live_record_gate_and_changed_approval_targets(self):
        # Pure test records only: no real reviews, studies or approvals are asserted.
        self.d['program'].update(mode='real', status='approved')
        for s in self.d['sources']: s['evidence_kind'] = 'real'
        for r in self.d['reviews']: r['evidence_kind'] = 'real'
        f = self.d['forms'][0]
        f.update(status='approved', release_evidence={k: 'test-fixture-only' for k in ('job_analysis_report', 'pilot_report', 'standard_setting_report', 'delivery_verification')})
        self.d['policies'] = {k: 'test-fixture-only' for k in ('passing_standard', 'eligibility', 'retakes', 'appeals', 'accommodations', 'renewal', 'data_retention', 'delivery')}
        targets = c.status(self.d)['decision_target_fingerprints']
        for typ, obj in [('program', self.d['program']), ('blueprint', self.d['blueprint']), ('form', f)]:
            self.d['decisions'].append({'id': 'DEC_' + typ, 'target_type': typ, 'target_id': obj['id'], 'revision': obj['revision'],
                'decision': 'approve', 'actor': 'test fixture', 'evidence_kind': 'real', 'evidence_ref': 'test-only', 'rationale': 'unit test only',
                'target_fingerprint': targets['forms'][f['id']] if typ == 'form' else targets[typ]})
        self.assertTrue(c.check_form(self.d, 'PILOT1', True)['checks_pass'])
        self.d['program']['claim'] += ' broader claim'
        self.assertIn('missing_real_approval:program', c.check_form(self.d, 'PILOT1', True)['issues'])

    def test_supporting_task_source_change_is_not_hidden(self):
        self.d['tasks'][0]['source_refs'].append({'source_id': 'SEC', 'version': '1.0', 'locator': 'Role definition'})
        self.d = changed_source(self.d)
        self.assertIn('outdated_source', c.item_issues(self.d, self.d['items'][0]))

    def test_form_requires_practical(self):
        self.assertTrue(c.check_form(self.d, 'PILOT1')['checks_pass'])
        for item in self.d['items']:
            if item['type'] == 'practical': item['status'] = 'retired'
        self.assertEqual(c.assemble(self.d, 'NEW')['reason'], 'infeasible')

    def test_enemy_group_constraints_and_search_limit(self):
        for item in self.d['items']:
            if item['domain_id'] == 'R':
                item['enemy_groups'] = ['one_recovery_only']
        for review in self.d['reviews']:
            review['item_fingerprint'] = c.content_fingerprint(c.index_items(self.d)[review['item_id']])
        self.assertEqual(c.assemble(self.d, 'NEW')['reason'], 'infeasible')
        self.assertEqual(c.assemble(harbor(), 'NEW', max_nodes=0)['reason'], 'search_limit')

    def test_public_export_is_allowlisted(self):
        secret = 'RESTRICTED_CANARY_8239'
        self.d['notes'].append(secret)
        self.d['items'][0]['rationale'] += secret
        self.d['public']['answer_key'] = secret
        result = json.dumps(c.export(self.d, 'candidate-guide'))
        self.assertNotIn(secret, result)
        self.assertNotIn('items', json.loads(result))

    def test_delivery_contains_exact_restricted_form(self):
        result = c.export(self.d, 'delivery', 'PILOT1')
        self.assertEqual(result['classification'], 'restricted')
        self.assertEqual(len(result['items']), 8)
        self.assertTrue(any('answer_key' in i for i in result['items']))
        self.d['items'][0]['revision'] = 2
        with self.assertRaises(ValueError): c.export(self.d, 'delivery', 'PILOT1')

    def test_unknown_impact_and_review_targets_rejected(self):
        with self.assertRaises(ValueError): c.impact(self.d, ['UNKNOWN'])
        with self.assertRaises(ValueError): c.review_packet(self.d, ['UNKNOWN'])

    def test_award_duplicate_receipt_and_unknown_outcome(self):
        self.d['awards'] = [{'id': 'A1', 'candidate_id': 'x', 'credential_version': '1', 'decision_id': 'D1', 'status': 'issued'}]
        self.assertIn('missing_provider_receipt', [x['code'] for x in c.reconcile_awards(self.d)['issues']])
        self.d['awards'][0]['status'] = 'unknown'
        self.assertIn('readback_before_retry', [x['code'] for x in c.reconcile_awards(self.d)['issues']])
        self.d['awards'].append(dict(self.d['awards'][0], id='A2'))
        self.assertIn('duplicate_credential_intent', [x['code'] for x in c.reconcile_awards(self.d)['issues']])

    def test_conflicting_award_authority_not_accepted(self):
        self.d['awards'] = [{'id': 'A1', 'candidate_id': 'x', 'credential_version': '1', 'decision_id': 'DEC1', 'status': 'issued', 'receipt': 'demo:1'}]
        base = {'id': 'DEC1', 'target_type': 'award', 'target_id': 'A1', 'revision': 1, 'decision': 'approve', 'actor': 'Synthetic', 'evidence_kind': 'synthetic', 'evidence_ref': 'demo', 'rationale': 'demo'}
        self.d['decisions'] = [base, dict(base, id='DEC2', decision='reject')]
        self.assertFalse(c.reconcile_awards(self.d)['reconciled'])


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.d = harbor()
        self.d['forms'] = [{'id': 'MATH', 'revision': 1, 'blueprint_revision': 1,
                            'item_refs': [{'item_id': key, 'revision': 1, 'item_fingerprint': c.content_fingerprint(c.index_items(self.d)[key])} for key in ('D01', 'D02')]}]
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'matrix.csv'

    def tearDown(self): self.tmp.cleanup()

    def matrix(self, content): self.path.write_text(content, encoding='utf-8')

    def test_known_arithmetic(self):
        self.matrix('candidate_id,D01@1,D02@1\na,0,0\nb,0,0\nc,1,1\nd,1,1\n')
        result = c.analyze(self.d, 'MATH', self.path)
        self.assertEqual(result['mean_total'], 1)
        self.assertAlmostEqual(result['coefficient_alpha'], 1)
        self.assertAlmostEqual(result['items'][0]['corrected_item_total_correlation'], 1)
        self.assertEqual(result['items'][0]['mean_proportion_of_max'], .5)
        self.assertAlmostEqual(result['sd_total'], (4 / 3) ** .5)

    def test_zero_variance_is_undefined(self):
        self.matrix('candidate_id,D01@1,D02@1\na,1,1\nb,1,1\n')
        result = c.analyze(self.d, 'MATH', self.path)
        self.assertIsNone(result['coefficient_alpha'])
        self.assertIsNone(result['items'][0]['corrected_item_total_correlation'])

    def test_negative_alpha_is_not_clamped(self):
        self.d['forms'][0]['item_refs'].append({'item_id': 'D03', 'revision': 1, 'item_fingerprint': c.content_fingerprint(c.index_items(self.d)['D03'])})
        self.matrix('candidate_id,D01@1,D02@1,D03@1\na,1,0,0\nb,1,1,0\nc,0,1,1\nd,1,1,1\n')
        result = c.analyze(self.d, 'MATH', self.path)
        self.assertAlmostEqual(result['coefficient_alpha'], -.375)
        self.assertAlmostEqual(result['items'][0]['corrected_item_total_correlation'], -3 / (33 ** .5))

    def test_single_observation_is_undefined(self):
        self.matrix('candidate_id,D01@1,D02@1\na,1,0\n')
        result = c.analyze(self.d, 'MATH', self.path)
        self.assertIsNone(result['sd_total'])
        self.assertIsNone(result['coefficient_alpha'])

    def test_invalid_matrices_rejected(self):
        cases = [
            'candidate_id,D01@1,D02@1\na,,1\n',
            'candidate_id,D01@1,D02@1\na,NaN,1\n',
            'candidate_id,D01@1,D02@1\na,0.5,1\n',
            'candidate_id,D01@1,D02@1\na,2,1\n',
            'candidate_id,D01@1,D02@1\na,0,1\na,1,1\n',
            'candidate_id,D01@2,D02@1\na,0,1\n',
            'candidate_id,D01@1,D01@1\na,0,1\n',
            'candidate_id,D01@1,D02@1\na,0,1,extra\n',
            'candidate_id,D01@1,D02@1\n',
        ]
        for content in cases:
            with self.subTest(content=content):
                self.matrix(content)
                with self.assertRaises(ValueError): c.analyze(self.d, 'MATH', self.path)

    def test_stale_form_analysis_refused(self):
        self.d['items'][0]['revision'] = 2
        self.matrix('candidate_id,D01@1,D02@1\na,0,1\n')
        with self.assertRaises(ValueError): c.analyze(self.d, 'MATH', self.path)

    def test_panel_summary_does_not_round_or_set_cut(self):
        self.matrix('judge_id,D01@1,D02@1\na,0.6,0.7\nb,0.8,0.5\n')
        result = c.panel_summary(self.d, 'MATH', self.path)
        self.assertAlmostEqual(result['mean_expected_total'], 1.3)
        self.assertNotIn('passing_score', result)

    def test_output_refuses_overwrite_and_nonfinite_json(self):
        c.save_new(self.path, {'a': 1})
        with self.assertRaises(FileExistsError): c.save_new(self.path, {'a': 2})
        self.matrix('{"a":NaN}')
        with self.assertRaises(ValueError): c.load(self.path)
        self.matrix('{"a":1,"a":2}')
        with self.assertRaises(ValueError): c.load(self.path)


class PackagingTests(unittest.TestCase):
    def test_manifest_and_relative_links(self):
        self.assertEqual(module('validate').validate_package()['skills'], 10)

    def test_portable_install_update_and_protected_uninstall(self):
        installer = module('install')
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'skills'
            preview = installer.install(target)
            self.assertFalse(target.exists())
            self.assertFalse(preview['applied'])
            installer.install(target, apply=True)
            copied = target / 'certification-workshop/scripts/certification.py'
            run = subprocess.run([sys.executable, str(copied), '--help'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            program = Path(tmp) / 'fresh-program'
            run = subprocess.run([sys.executable, str(copied), 'init', '--directory', str(program), '--id', 'fresh', '--title', 'Fresh'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((program / 'working-templates.md').is_file())
            installer.install(target, apply=True)
            skill = target / 'certification-setup/SKILL.md'
            original = skill.read_bytes()
            skill.write_text('local edit', encoding='utf-8')
            with self.assertRaises(ValueError): installer.install(target, apply=True, uninstall=True)
            skill.write_bytes(original)
            installer.install(target, apply=True, uninstall=True)
            self.assertFalse(skill.exists())

    def test_unowned_installation_refused(self):
        installer = module('install')
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / 'certification-setup').mkdir()
            (target / 'certification-setup/SKILL.md').write_text('existing', encoding='utf-8')
            with self.assertRaises(ValueError): installer.install(target, apply=True)

    def test_reproducible_archive_and_extracted_cli(self):
        pack = module('package')
        archive, first = pack.build()
        self.assertEqual(first, pack.build()[1])
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(archive) as z:
                self.assertFalse(any('__pycache__' in p or '/work/' in p or '/.git/' in p for p in z.namelist()))
                z.extractall(tmp)
            root = Path(tmp) / 'certification-workshop'
            result = subprocess.run([sys.executable, str(root / 'scripts/validate.py')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__': unittest.main()
