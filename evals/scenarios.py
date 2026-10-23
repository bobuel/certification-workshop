"""Offline CLI scenario evaluations. Synthetic records only; no model/API or provider calls."""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from fixture import c, harbor, write_scores, changed_source, ROOT

HELPER = ROOT / 'skills/certification-workshop/scripts/certification.py'


def run():
    results = []
    with tempfile.TemporaryDirectory(prefix='certification-scenarios-') as temporary:
        folder = Path(temporary)
        original = harbor()
        c.save_new(folder / 'original.json', original)
        write_scores(folder, original)
        original_digest = hashlib.sha256((folder / 'original.json').read_bytes()).hexdigest()

        def cli(command, program='original.json', code=0, **options):
            args = [sys.executable, str(HELPER), command]
            if command != 'init': args += ['--program', str(folder / program)]
            for key, value in options.items():
                if value is False or value is None: continue
                args.append('--' + key.replace('_', '-'))
                if value is not True: args.append(str(value))
            proc = subprocess.run(args, text=True, capture_output=True, timeout=30)
            if proc.returncode != code:
                raise AssertionError(f'{command}: expected exit {code}; got {proc.returncode}: {proc.stderr[:300]}')
            raw = proc.stderr if code == 2 else proc.stdout
            value = json.loads(raw)
            return value

        def record(name, expected, function):
            try:
                observed = function()
                results.append({'id': name, 'passed': True, 'expected': expected, 'observed': observed})
            except Exception as exc:
                results.append({'id': name, 'passed': False, 'expected': expected, 'error': f'{type(exc).__name__}: {exc}'})

        def creation():
            cli('init', directory=folder / 'fresh', id='fresh', title='Fresh certification')
            d = c.load(folder / 'fresh/program.json')
            assert d['program']['mode'] == 'real' and not d['items'] and not d['forms']
            status = cli('status', program='fresh/program.json')
            assert 'charter' in status['next_action']
            return {'created': True, 'items': 0, 'forms': 0, 'next_action': status['next_action']}
        record('from-scratch', 'Create resumable records without inventing a bank or existing certification.', creation)

        def draft_form():
            c.save_new(folder / 'draft.json', harbor(False))
            report = cli('assemble', program='draft.json', form='NEW', code=1)
            assert report['assembled'] is False and report['reason'] == 'infeasible'
            return {'assembled': False, 'reason': report['reason']}
        record('unreviewed-bank', 'Decline to assemble a form from unreviewed draft items.', draft_form)

        def conflicting_reviews():
            d = copy.deepcopy(original)
            d['reviews'].append(dict(d['reviews'][0], id='NEGATIVE', verdict='reject'))
            c.save_new(folder / 'conflict.json', d)
            report = cli('check-form', program='conflict.json', form='PILOT1', code=1)
            assert any('unresolved_negative_review' in x for x in report['issues'])
            return report['issues']
        record('review-conflict', 'Acceptance cannot conceal a current unresolved rejection.', conflicting_reviews)

        def missing_scores():
            path = folder / 'missing.csv'
            rows = list(csv.reader((folder / 'pilot-scores.csv').open(encoding='utf-8')))
            rows[1][1] = ''
            with path.open('w', encoding='utf-8', newline='') as f: csv.writer(f).writerows(rows)
            report = cli('analyze', form='PILOT1', csv=path, out=folder / 'should-not-exist.json', code=2)
            assert 'Missing score' in report['error'] and not (folder / 'should-not-exist.json').exists()
            return {'error': report['error'], 'output_created': False}
        record('missing-pilot-data', 'Reject missing scores without silently imputing or writing a report.', missing_scores)

        def column_order():
            rows = list(csv.reader((folder / 'pilot-scores.csv').open(encoding='utf-8')))
            path = folder / 'reordered.csv'
            with path.open('w', encoding='utf-8', newline='') as f: csv.writer(f).writerows([list(reversed(r)) for r in rows])
            one = cli('analyze', form='PILOT1', csv=folder / 'pilot-scores.csv')
            two = cli('analyze', form='PILOT1', csv=path)
            assert one == two
            assert 'passing_score' not in one and 'passed_candidates' not in one
            return {'reports_equal': True, 'automatic_awards_or_pass_decisions': False}
        record('matrix-identity', 'Map scores by exact item/revision headers, not column position.', column_order)

        def changed_content():
            d = copy.deepcopy(original)
            c.index_items(d)[d['forms'][0]['item_refs'][0]['item_id']]['prompt'] += ' Different conditions.'
            c.save_new(folder / 'edited.json', d)
            report = cli('analyze', program='edited.json', form='PILOT1', csv=folder / 'pilot-scores.csv', code=2)
            assert 'changed form content' in report['error']
            return report
        record('unchanged-revision-edit', 'Reject old score data when content changed without a version increment.', changed_content)

        def legacy_form():
            d = copy.deepcopy(original)
            for ref in d['forms'][0]['item_refs']: ref.pop('item_fingerprint')
            c.save_new(folder / 'legacy-import.json', d)
            before = (folder / 'legacy-import.json').read_bytes()
            assert cli('validate', program='legacy-import.json')['valid_structure']
            report = cli('analyze', program='legacy-import.json', form='PILOT1', csv=folder / 'pilot-scores.csv', code=2)
            assert (folder / 'legacy-import.json').read_bytes() == before
            return {'structure_preserved': True, 'analysis_refused': True, 'reason': report['error']}
        record('legacy-import', 'Preserve imported records; require verified historical content before pinning.', legacy_form)

        def source_change():
            c.save_new(folder / 'changed-source.json', changed_source(original))
            impact = cli('impact', program='changed-source.json', source='SEC')
            assert impact['items'] == ['S01', 'S02', 'S03']
            cli('check-form', program='changed-source.json', form='PILOT1', code=1)
            assert cli('check-form', form='PILOT1')['checks_pass']
            return {'affected_items': impact['items'], 'old_snapshot_still_usable': True}
        record('source-revision', 'Flag source dependencies and retain an interpretable historical snapshot.', source_change)

        def public_guide():
            d = copy.deepcopy(original)
            canary = 'RESTRICTED_EVAL_CANARY_482'
            d['notes'] = [canary]
            d['items'][0]['rationale'] += canary
            d['public']['private_bank'] = canary
            c.save_new(folder / 'private.json', d)
            report = cli('export', program='private.json', audience='candidate-guide')
            assert canary not in json.dumps(report) and 'items' not in report
            return {'restricted_canary_absent': True, 'classification': report['classification']}
        record('public-export', 'Keep restricted records and unrecognized public fields out of the candidate guide.', public_guide)

        def synthetic_release():
            report = cli('check-form', form='PILOT1', live=True, code=1)
            assert 'synthetic_program' in report['issues']
            return {'live_checks_pass': False, 'issues': report['issues']}
        record('synthetic-live-release', 'Do not treat the completed synthetic rehearsal as a live release.', synthetic_release)

        def unknown_award():
            d = copy.deepcopy(original)
            a = {'id': 'AWARD1', 'candidate_id': 'SYNTHETIC_001', 'credential_version': 'demo1', 'decision_id': 'DEC1', 'status': 'unknown'}
            d['awards'] = [a]
            d['decisions'] = [{'id': 'DEC1', 'target_type': 'award', 'target_id': 'AWARD1', 'revision': 1, 'decision': 'approve',
                'actor': 'Synthetic owner', 'evidence_kind': 'synthetic', 'evidence_ref': 'demo-only', 'rationale': 'Test record only',
                'target_fingerprint': c.award_fingerprint(a)}]
            c.save_new(folder / 'award.json', d)
            report = cli('reconcile-awards', program='award.json', code=1)
            assert any(x['code'] == 'readback_before_retry' for x in report['issues'])
            return {'retry_not_authorized': True, 'issues': report['issues']}
        record('unknown-issuance', 'Request provider readback rather than assuming failure or authorizing a duplicate.', unknown_award)

        def output_collision():
            path = folder / 'existing.json'
            path.write_text('DO NOT OVERWRITE', encoding='utf-8')
            cli('coverage', out=path, code=2)
            assert path.read_text(encoding='utf-8') == 'DO NOT OVERWRITE'
            return {'original_output_preserved': True}
        record('output-collision', 'Preserve existing output files on a refused overwrite.', output_collision)

        def inputs_unchanged():
            assert hashlib.sha256((folder / 'original.json').read_bytes()).hexdigest() == original_digest
            return {'original_program_unchanged': True}
        record('read-only-helpers', 'All analysis, proposal and export commands leave the input program unchanged.', inputs_unchanged)

    return {'suite': 'offline-cli-scenarios', 'version': json.loads((ROOT / 'plugin.json').read_text())['version'],
            'helper_sha256': hashlib.sha256(HELPER.read_bytes()).hexdigest(), 'passed': all(r['passed'] for r in results),
            'case_count': len(results), 'passed_count': sum(r['passed'] for r in results), 'cases': results,
            'limits': ['Synthetic CLI scenarios, not model behavioral eval scores.', 'No external delivery, issuance or psychometric claims.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', help='New report path; refuses overwrite')
    args = parser.parse_args()
    report = run()
    if args.out: c.save_new(args.out, report)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report['passed'] else 1)
