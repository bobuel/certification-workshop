"""Regression probes for approval reuse and versioned assessment evidence."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from fixture import c, harbor, write_scores


def live_record_fixture():
    """Synthetic unit-test records exercising real-mode checks, never real evidence."""
    data = harbor()
    data['program'].update(mode='real', status='approved')
    for s in data['sources']: s['evidence_kind'] = 'real'
    for r in data['reviews']: r['evidence_kind'] = 'real'
    f = data['forms'][0]
    f.update(status='approved', release_evidence={k: 'unit-test-only' for k in ('job_analysis_report', 'pilot_report', 'standard_setting_report', 'delivery_verification')})
    data['policies'] = {k: 'unit-test-only' for k in ('passing_standard', 'eligibility', 'retakes', 'appeals', 'accommodations', 'renewal', 'data_retention', 'delivery')}
    targets = c.status(data)['decision_target_fingerprints']
    for typ, obj in [('program', data['program']), ('blueprint', data['blueprint']), ('form', f)]:
        data['decisions'].append({'id': 'DEC_' + typ, 'target_type': typ, 'target_id': obj['id'], 'revision': obj['revision'],
            'decision': 'approve', 'actor': 'unit test only', 'evidence_kind': 'real', 'evidence_ref': 'unit-test-only',
            'rationale': 'Exercise record checks only', 'target_fingerprint': targets['forms'][f['id']] if typ == 'form' else targets[typ]})
    return data


def award_fixture():
    data = harbor()
    award = {'id': 'A1', 'revision': 1, 'candidate_id': 'TEST_CANDIDATE_A', 'credential_version': 'v1',
             'decision_id': 'DA1', 'status': 'issued', 'receipt': 'synthetic://issued/1', 'action': 'issue'}
    data['awards'] = [award]
    # For the pre-fix probe the old implementation does not know or enforce the hash.
    fingerprint = c.award_fingerprint(award) if hasattr(c, 'award_fingerprint') else 'UNENFORCED'
    data['decisions'] = [{'id': 'DA1', 'target_type': 'award', 'target_id': 'A1', 'revision': 1,
        'decision': 'approve', 'actor': 'Synthetic owner', 'evidence_kind': 'synthetic', 'evidence_ref': 'synthetic-only',
        'rationale': 'Approve only this synthetic candidate/version/action', 'target_fingerprint': fingerprint}]
    return data


class EvidenceBoundaryTests(unittest.TestCase):
    def test_policy_change_invalidates_program_approval(self):
        data = live_record_fixture()
        self.assertTrue(c.check_form(data, 'PILOT1', True)['checks_pass'])
        data['policies']['passing_standard'] = 'A different passing rule'
        self.assertFalse(c.check_form(data, 'PILOT1', True)['checks_pass'], 'Old approval survived a changed passing policy')

    def test_competency_change_invalidates_blueprint_approval(self):
        data = live_record_fixture()
        data['competencies'][0]['statement'] = 'A substantially broader capability'
        self.assertFalse(c.check_form(data, 'PILOT1', True)['checks_pass'], 'Old blueprint approval survived a changed competency')

    def test_release_evidence_change_invalidates_form_approval(self):
        data = live_record_fixture()
        data['forms'][0]['release_evidence']['standard_setting_report'] = 'Different report'
        self.assertFalse(c.check_form(data, 'PILOT1', True)['checks_pass'], 'Old approval survived replacement of its evidence')

    def test_award_approval_cannot_move_to_another_candidate(self):
        data = award_fixture()
        self.assertTrue(c.reconcile_awards(data)['reconciled'])
        data['awards'][0]['candidate_id'] = 'TEST_CANDIDATE_B'
        self.assertFalse(c.reconcile_awards(data)['reconciled'], 'Award approval was reusable for another candidate')

    def test_issue_authority_does_not_authorize_revocation(self):
        data = award_fixture()
        data['awards'][0]['status'] = 'revoked'
        self.assertFalse(c.reconcile_awards(data)['reconciled'], 'Issue approval/receipt were sufficient for a revocation')

    def test_score_analysis_rejects_content_edit_with_same_revision(self):
        data = harbor()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_scores(folder, data)
            selected_id = data['forms'][0]['item_refs'][0]['item_id']
            c.index_items(data)[selected_id]['answer_key'] = 'A'
            with self.assertRaises(ValueError, msg='Score analysis accepted changed content under the old form'):
                c.analyze(data, 'PILOT1', folder / 'pilot-scores.csv')

    def test_form_identity_includes_practical_conditions(self):
        data = harbor()
        f, items = c.pinned_items(data, 'PILOT1')
        before = c.form_fingerprint(f, items)
        practical = next(i for i in items if i['type'] == 'practical')
        practical['setup'] += ' A substantially different starting state.'
        after = c.form_fingerprint(f, items)
        self.assertNotEqual(before, after, 'Form fingerprint omitted the practical setup')

    def test_legacy_form_requires_verified_pinning(self):
        data = harbor()
        for ref in data['forms'][0]['item_refs']: ref.pop('item_fingerprint', None)
        self.assertFalse(c.check_form(data, 'PILOT1')['checks_pass'])
        with self.assertRaises(ValueError): c.pinned_items(data, 'PILOT1')

    def test_revocation_requires_new_authority_and_receipt(self):
        data = award_fixture()
        award = data['awards'][0]
        award.update(action='revoke', revision=2, status='revoked', reason='Synthetic revocation exercise')
        self.assertFalse(c.reconcile_awards(data)['reconciled'])
        data['decisions'][0].update(revision=2, target_fingerprint=c.award_fingerprint(award))
        self.assertFalse(c.reconcile_awards(data)['reconciled'])
        award['revocation_receipt'] = 'synthetic://revoked/1'
        self.assertTrue(c.reconcile_awards(data)['reconciled'])

    def test_award_status_progression_preserves_intent_hash(self):
        data = award_fixture()
        award = data['awards'][0]
        original = c.award_fingerprint(award)
        award.update(status='submitted', receipt=None)
        self.assertEqual(original, c.award_fingerprint(award))
        self.assertFalse(c.reconcile_awards(data)['reconciled'])

    def test_candidate_whitespace_is_rejected_not_a_second_identity(self):
        data = award_fixture()
        data['awards'][0]['candidate_id'] += ' '
        with self.assertRaises(ValueError): c.validate(data)


if __name__ == '__main__': unittest.main()
