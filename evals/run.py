"""Rehearse a full synthetic lifecycle using real helper executions, without services."""
from pathlib import Path
import copy
import json
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixture import c, harbor, write_scores, changed_source, ROOT


def run(output=None):
    with tempfile.TemporaryDirectory(prefix='certification-eval-') as temporary:
        folder = Path(temporary)
        c.initialize(folder / 'new-program', 'harbor-admin', 'Harbor Administrator', 'demo')
        blank = c.load(folder / 'new-program/program.json')
        assert not blank['items'] and not blank['tasks']
        assert 'charter' in c.status(blank)['next_action']
        draft = harbor(reviewed=False)
        c.validate(draft)
        assert not c.coverage(draft)['ready_to_assemble']
        reviewed = harbor()
        check = c.check_form(reviewed, 'PILOT1')
        assert check['checks_pass'], check
        form = reviewed['forms'][0]
        selected = [c.index_items(reviewed)[r['item_id']] for r in form['item_refs']]
        assert {key: sum(i['domain_id'] == key for i in selected) for key in 'DSR'} == {'D': 4, 'S': 2, 'R': 2}
        assert sum(i['type'] == 'practical' for i in selected) >= 1
        write_scores(folder, reviewed)
        pilot = c.analyze(reviewed, 'PILOT1', folder / 'pilot-scores.csv')
        panel = c.panel_summary(reviewed, 'PILOT1', folder / 'panel-judgments.csv')
        assert pilot['n'] == 12 and panel['judges'] == 3
        assert abs(panel['mean_expected_total'] - 0.6 * sum(i['max_score'] for i in selected)) < 1e-9
        packet = c.review_packet(reviewed)
        assert len(packet['items']) == 12
        guide = c.export(reviewed, 'candidate-guide')
        delivery = c.export(reviewed, 'delivery', 'PILOT1')
        assert 'items' not in guide and 'items' in delivery
        live = c.check_form(reviewed, 'PILOT1', live=True)
        assert not live['checks_pass'] and 'synthetic_program' in live['issues']
        changed = changed_source(reviewed)
        affected = c.impact(changed, ['SEC'])
        changed_check = c.check_form(changed, 'PILOT1')
        assert set(affected['items']) == {'S01', 'S02', 'S03'} and affected['forms'] == ['PILOT1']
        assert not changed_check['checks_pass']
        assert c.check_form(reviewed, 'PILOT1')['checks_pass']  # retained historical snapshot
        operations = copy.deepcopy(reviewed)
        operations['awards'] = [{'id': 'AWARD1', 'candidate_id': 'SYNTHETIC_01', 'credential_version': 'demo-v1',
                                  'decision_id': 'DEC_AWARD1', 'status': 'issued', 'receipt': 'synthetic://receipt/1'}]
        operations['decisions'] = [{'id': 'DEC_AWARD1', 'target_type': 'award', 'target_id': 'AWARD1', 'revision': 1,
                                     'decision': 'approve', 'actor': 'Synthetic owner', 'evidence_kind': 'synthetic',
                                     'target_fingerprint': c.award_fingerprint(operations['awards'][0]),
                                     'evidence_ref': 'synthetic-demo-only', 'rationale': 'Rehearse award record reconciliation, not an actual award.'}]
        assert c.reconcile_awards(operations)['reconciled']
        duplicate = copy.deepcopy(operations)
        duplicate['awards'].append(dict(duplicate['awards'][0], id='AWARD2'))
        assert not c.reconcile_awards(duplicate)['reconciled']
        result = {'suite': 'synthetic lifecycle', 'passed': True,
                  'phases': ['empty program initialization', 'document-derived charter/tasks/competencies',
                             'draft blueprint and bank', 'synthetic content review', 'exact mixed-method form',
                             'scored pilot analysis', 'expected-score panel arithmetic', 'audience-separated launch handoff',
                             'award record reconciliation', 'changed-source impact and historical retention'],
                  'form_check': check, 'pilot': pilot, 'panel': panel,
                  'live_readiness_correctly_blocked': live, 'source_change': affected,
                  'source_change_form_check': changed_check,
                  'limits': ['Synthetic fixtures and helper execution, not an unassisted model benchmark.',
                             'No real SMEs/candidates, psychometric validation, live provider, issued credential or owner acceptance.']}
        if output:
            output = Path(output)
            output.mkdir(parents=True, exist_ok=True)
            for name, value in [('program.json', reviewed), ('draft-program.json', draft), ('changed-program.json', changed),
                                ('operations-program.json', operations), ('review-packet.json', packet),
                                ('candidate-guide.json', guide), ('restricted-delivery.json', delivery), ('journey-report.json', result)]:
                # Only explicitly requested synthetic example folder is refreshed, never a user program.
                (output / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
            write_scores(output, reviewed)
        return result


if __name__ == '__main__':
    # --write-example refreshes only the repository's known synthetic example artifacts.
    output = ROOT / 'examples/harbor' if sys.argv[1:] == ['--write-example'] else None
    result = run(output)
    print(json.dumps({'passed': result['passed'], 'phases': len(result['phases']), 'limits': result['limits']}, indent=2))
    sys.exit(0 if result['passed'] else 1)
