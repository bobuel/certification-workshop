"""Independent synthetic regressions for local evidence, scoring and public text.

No fixture represents human review, production source evidence or a credential.
"""
import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from fixture import c, harbor


class IntegrityAndScoringTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='cert-integrity-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'project'
        self.root.mkdir()
        self.data = harbor(reviewed=False)
        for source in self.data['sources']:
            path = self.root / source['location']
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(('Synthetic test evidence only: ' + source['id'] + '\n').encode())
            source['sha256'] = self.digest(path)

    @staticmethod
    def digest(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def reviewed(self, data=None):
        data = copy.deepcopy(self.data if data is None else data)
        receipt = self.root / 'synthetic-review.txt'
        receipt.write_text('Synthetic test acceptance, not a person or expert decision.\n')
        data['reviews'] = []
        data['forms'] = []
        for item in data['items']:
            item['status'] = 'approved'
            data['reviews'].append({'id': 'SYN_' + item['id'], 'item_id': item['id'],
                'revision': item['revision'], 'reviewer': 'Synthetic regression fixture',
                'role': 'content', 'verdict': 'accept', 'evidence_kind': 'synthetic',
                'evidence_ref': receipt.name, 'evidence_sha256': self.digest(receipt),
                'item_fingerprint': c.content_fingerprint(item),
                'source_fingerprints': c.source_fingerprints(data, [item])})
        return data

    def with_form(self, data=None):
        data = self.reviewed(data)
        result = c.assemble(data, 'SYN_FORM', evidence_root=self.root)
        self.assertTrue(result['assembled'], result)
        data['forms'] = [result['form']]
        return data

    def test_matching_local_sources_pass_and_are_not_mutated(self):
        before = copy.deepcopy(self.data)
        result = c.audit_evidence(self.data, self.root)
        self.assertTrue(result['checks_pass'], result)
        self.assertEqual(len(result['checks']), 3)
        self.assertTrue(all(row['verified'] for row in result['checks']))
        self.assertEqual(self.data, before)
        self.assertIn('not authorship', result['note'])

    def test_tampered_source_bytes_fail(self):
        (self.root / self.data['sources'][0]['location']).write_text('Different synthetic bytes.')
        result = c.audit_evidence(self.data, self.root)
        self.assertFalse(result['checks_pass'])
        self.assertIn('evidence_digest_mismatch:source:DATA@1.0', result['issues'])

    def test_missing_source_file_fails(self):
        (self.root / self.data['sources'][0]['location']).unlink()
        result = c.audit_evidence(self.data, self.root)
        self.assertIn('missing_evidence_file:source:DATA@1.0', result['issues'])

    def test_missing_or_invalid_digest_is_not_verification(self):
        for value in (None, 'not-a-digest', 7):
            with self.subTest(digest=value):
                data = copy.deepcopy(self.data)
                if value is None:
                    data['sources'][0].pop('sha256')
                else:
                    data['sources'][0]['sha256'] = value
                result = c.audit_evidence(data, self.root)
                self.assertIn('missing_or_invalid_digest:source:DATA@1.0', result['issues'])

    def test_parent_absolute_and_windows_style_paths_are_rejected(self):
        for location in ('../outside.txt', str(self.root / 'sources/data.md'), 'sources\\data.md'):
            with self.subTest(location=location):
                data = copy.deepcopy(self.data)
                data['sources'][0]['location'] = location
                result = c.audit_evidence(data, self.root)
                self.assertIn('unsafe_or_oversized_evidence_path:source:DATA@1.0', result['issues'])

    def test_external_evidence_is_not_fetched_or_marked_verified(self):
        self.data['sources'][0]['location'] = 'https://example.invalid/private-source'
        result = c.audit_evidence(self.data, self.root)
        self.assertIn('external_evidence_unverified:source:DATA@1.0', result['issues'])
        self.assertFalse(result['checks'][0]['verified'])

    def test_symlink_cannot_escape_project_root(self):
        outside = self.root.parent / 'outside.txt'
        outside.write_text('Synthetic outside-root file.')
        link = self.root / 'escape.txt'
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as error:
            self.skipTest('Symlink creation unavailable: ' + str(error))
        self.data['sources'][0].update(location=link.name, sha256=self.digest(outside))
        result = c.audit_evidence(self.data, self.root)
        self.assertIn('unsafe_or_oversized_evidence_path:source:DATA@1.0', result['issues'])

    def test_oversized_source_is_rejected_without_large_fixture(self):
        with patch.object(c, 'MAX_EVIDENCE_BYTES', 8):
            result = c.audit_evidence(self.data, self.root)
        self.assertIn('evidence_file_too_large:source:DATA@1.0', result['issues'])

    def test_required_policy_requires_review_digest(self):
        data = self.reviewed()
        data['validation_policy'] = {'evidence_integrity': 'required'}
        self.assertTrue(c.audit_evidence(data, self.root)['checks_pass'])
        data['reviews'][0].pop('evidence_sha256')
        result = c.assemble(data, 'MISSING_REVIEW_HASH', evidence_root=self.root)
        self.assertFalse(result['assembled'])
        self.assertEqual(result['reason'], 'evidence_integrity')
        self.assertIn('missing_or_invalid_digest:review:SYN_D01', result['issues'])

    def test_required_policy_rejects_missing_and_changed_review_receipts(self):
        for missing in (False, True):
            with self.subTest(missing=missing):
                data = self.reviewed()
                data['validation_policy'] = {'evidence_integrity': 'required'}
                path = self.root / data['reviews'][0]['evidence_ref']
                if missing:
                    path.unlink()
                    issue = 'missing_evidence_file:review:SYN_D01'
                else:
                    path.write_text('Changed synthetic receipt.')
                    issue = 'evidence_digest_mismatch:review:SYN_D01'
                self.assertIn(issue, c.audit_evidence(data, self.root)['issues'])

    def test_legacy_unhashed_fixture_keeps_default_behavior(self):
        data = harbor()
        self.assertEqual(c.evidence_gate(data), [])
        self.assertTrue(c.check_form(data, 'PILOT1')['checks_pass'])
        self.assertTrue(c.assemble(data, 'LEGACY_SECOND')['assembled'])
        self.assertEqual(c.source_fingerprints(data, data['items']), {})

    def test_declared_digest_requires_explicit_evidence_root(self):
        data = self.reviewed()
        result = c.assemble(data, 'NO_ROOT')
        self.assertFalse(result['assembled'])
        self.assertEqual(result['issues'], ['evidence_root_required'])

    def test_source_bindings_include_direct_and_task_only_dependencies(self):
        data = copy.deepcopy(self.data)
        data['tasks'][0]['source_refs'].append({'source_id': 'SEC', 'version': '1.0', 'locator': 'Synthetic task-only dependency'})
        data = self.with_form(data)
        item = next(i for i in data['items'] if i['id'] == 'D01')
        bindings = c.source_fingerprints(data, [item])
        self.assertEqual(set(bindings), {'DATA@1.0', 'SEC@1.0'})
        self.assertEqual(c.review_packet(data, ['D01'])['source_fingerprints']['D01'], bindings)
        self.assertEqual(set(data['forms'][0]['source_fingerprints']), {'DATA@1.0', 'SEC@1.0', 'REC@1.0'})
        source = next(s for s in data['sources'] if s['id'] == 'SEC')
        path = self.root / source['location']
        path.write_text('Changed task-only supporting source.')
        source['sha256'] = self.digest(path)
        self.assertIn('missing_current_content_acceptance', c.item_issues(data, item))

    def test_hashed_source_review_requires_its_source_bindings(self):
        data = self.with_form()
        review = next(r for r in data['reviews'] if r['item_id'] == 'D01')
        review.pop('source_fingerprints')
        item = next(i for i in data['items'] if i['id'] == 'D01')
        self.assertIn('missing_current_content_acceptance', c.item_issues(data, item))

    def test_rehashing_changed_source_same_version_rejects_old_review_and_form(self):
        data = self.with_form()
        source = data['sources'][0]
        path = self.root / source['location']
        path.write_text('Changed evidence, deceptively retaining version 1.0.')
        source['sha256'] = self.digest(path)
        self.assertTrue(c.audit_evidence(data, self.root)['checks_pass'])
        result = c.check_form(data, 'SYN_FORM', evidence_root=self.root)
        self.assertIn('missing_current_content_acceptance:D01', result['issues'])
        self.assertIn('unpinned_or_changed_source_content', result['issues'])
        with self.assertRaisesRegex(ValueError, 'source content'):
            c.pinned_items(data, 'SYN_FORM')

    def test_removing_digest_cannot_downgrade_existing_source_pins(self):
        data = self.with_form()
        for source in data['sources']:
            source.pop('sha256')
        result = c.check_form(data, 'SYN_FORM', evidence_root=self.root)
        self.assertIn('unpinned_or_changed_source_content', result['issues'])
        self.assertIn('missing_current_content_acceptance:D01', result['issues'])
        self.assertFalse(c.assemble(data, 'NO_DOWNGRADE', evidence_root=self.root)['assembled'])
        with self.assertRaisesRegex(ValueError, 'source content'):
            c.pinned_items(data, 'SYN_FORM')

    def test_raw_point_reconciliation_does_not_relabel_item_weights(self):
        result = c.score_weighting(self.data)
        rows = {r['domain_id']: r for r in result['domains']}
        self.assertEqual(result['max_score'], 21)
        self.assertEqual({k: r['max_score'] for k, r in rows.items()}, {'D': 9, 'S': 6, 'R': 6})
        self.assertAlmostEqual(rows['D']['score_weight_percent'], 100 * 9 / 21)
        self.assertEqual(rows['D']['item_weight_percent'], 50)
        self.assertIn('item_and_raw_point_weights_differ:D', result['warnings'])
        self.assertIn('score_weight_targets_not_declared', result['warnings'])
        self.assertEqual(result['target_issues'], [])

    def test_explicit_raw_point_targets_match_selected_form(self):
        data = self.with_form()
        _, selected = c.pinned_items(data, 'SYN_FORM')
        weights = c.score_weighting(data, selected)
        data['blueprint']['score_weight_policy'] = {'basis': 'raw_points',
            'target_percent': {r['domain_id']: r['score_weight_percent'] for r in weights['domains']},
            'tolerance_percentage_points': 0.001}
        self.assertEqual(c.score_weighting(data, selected)['target_issues'], [])
        self.assertTrue(c.check_form(data, 'SYN_FORM', evidence_root=self.root)['checks_pass'])
        self.assertTrue(c.assemble(data, 'MATCHING_TARGETS', evidence_root=self.root)['assembled'])

    def test_invalid_score_policies_are_rejected(self):
        policies = [
            {'basis': 'normalized_domains'},
            {'basis': 'raw_points', 'target_percent': {'D': 50, 'S': 50}},
            {'basis': 'raw_points', 'target_percent': {'D': 60, 'S': 25, 'R': 25}},
            {'basis': 'raw_points', 'tolerance_percentage_points': -1},
            {'basis': 'raw_points', 'tolerance_percentage_points': float('nan')}]
        for policy in policies:
            with self.subTest(policy=policy):
                data = copy.deepcopy(self.data)
                data['blueprint']['score_weight_policy'] = policy
                with self.assertRaises(ValueError):
                    c.validate(data)

    def test_impossible_score_targets_fail_form_and_assembly(self):
        data = self.with_form()
        data['blueprint']['score_weight_policy'] = {'basis': 'raw_points',
            'target_percent': {'D': 99, 'S': 0.5, 'R': 0.5}, 'tolerance_percentage_points': 0}
        self.assertFalse(c.check_form(data, 'SYN_FORM', evidence_root=self.root)['checks_pass'])
        result = c.assemble(data, 'IMPOSSIBLE_SCORE_TARGET', evidence_root=self.root)
        self.assertFalse(result['assembled'])
        self.assertEqual(result['reason'], 'infeasible')

    def test_domain_minimum_rejects_form_even_when_global_minimum_passes(self):
        data = self.with_form()
        _, selected = c.pinned_items(data, 'SYN_FORM')
        self.assertGreaterEqual(sum(i['type'] == 'practical' for i in selected), 1)
        self.assertEqual(sum(i['type'] == 'practical' and i['domain_id'] == 'R' for i in selected), 0)
        data['blueprint']['required_methods_by_domain'] = {'R': {'practical': 1}}
        result = c.check_form(data, 'SYN_FORM', evidence_root=self.root)
        self.assertFalse(result['checks_pass'])
        self.assertIn('domain_method_coverage:R:practical', result['issues'])
        self.assertNotIn('method_coverage:practical', result['issues'])

    def test_solver_finds_domain_method_alternative_without_relaxing_constraints(self):
        data = self.reviewed()
        data['blueprint']['required_methods_by_domain'] = {
            'D': {'practical': 1}, 'S': {'practical': 1}, 'R': {'practical': 1}}
        result = c.assemble(data, 'DOMAIN_METHODS', evidence_root=self.root)
        self.assertTrue(result['assembled'], result)
        data['forms'] = [result['form']]
        _, selected = c.pinned_items(data, 'DOMAIN_METHODS')
        self.assertEqual({d: sum(i['domain_id'] == d and i['type'] == 'practical' for i in selected)
                          for d in ('D', 'S', 'R')}, {'D': 1, 'S': 1, 'R': 1})
        self.assertTrue(c.check_form(data, 'DOMAIN_METHODS', evidence_root=self.root)['checks_pass'])
        data['blueprint']['required_methods_by_domain']['R']['practical'] = 3
        impossible = c.assemble(data, 'IMPOSSIBLE_DOMAIN_METHODS', evidence_root=self.root)
        self.assertFalse(impossible['assembled'])
        self.assertEqual(impossible['reason'], 'infeasible')

    def test_invalid_domain_method_fields_are_rejected(self):
        values = [
            {'UNKNOWN': {'practical': 1}}, {'R': {'essay': 1}},
            {'R': {'practical': -1}}, {'R': {'practical': True}},
            {'R': {'practical': 0.5}}, {'R': None}, 'not-a-mapping']
        for value in values:
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data['blueprint']['required_methods_by_domain'] = value
                with self.assertRaises(ValueError):
                    c.validate(data)

    def test_normal_guide_passes_and_unknown_fields_stay_excluded(self):
        data = harbor(reviewed=False)
        data['public']['unrecognized'] = 'SYNTHETIC_RESTRICTED_CANARY'
        data['notes'].append('SYNTHETIC_RESTRICTED_CANARY')
        result = c.export(data, 'candidate-guide')
        self.assertEqual(result['classification'], 'public-draft')
        self.assertNotIn('SYNTHETIC_RESTRICTED_CANARY', str(result))
        self.assertIn('not semantic redaction', result['note'])
        # The documented minimum phrase length avoids blocking common short text;
        # this is an explicit detector limit, not a claim that the text is safe.
        short = next(i for i in data['items'] if i['id'] == 'D02')['options']['B']
        self.assertLess(len(short), 12)
        data['public']['overview'] = short
        self.assertEqual(c.export(data, 'candidate-guide')['guide']['overview'], short)

    def test_exact_prompt_and_long_keyed_option_copies_are_blocked(self):
        data = harbor(reviewed=False)
        item = data['items'][0]
        for phrase in (item['prompt'], item['options'][item['answer_key']]):
            with self.subTest(phrase=phrase):
                data['public']['overview'] = 'Prefix ' + '  '.join(phrase.upper().split())
                with self.assertRaisesRegex(ValueError, 'known_restricted_text:overview:item.D01'):
                    c.export(data, 'candidate-guide')

    def test_exact_private_note_copy_is_blocked(self):
        data = harbor(reviewed=False)
        data['notes'].append('Private synthetic reviewer disposition text.')
        data['public']['support'] = 'Contact note: ' + data['notes'][-1]
        with self.assertRaisesRegex(ValueError, 'known_restricted_text:support:note'):
            c.export(data, 'candidate-guide')

    def test_rubric_anchor_and_restricted_record_markers_are_blocked(self):
        data = harbor(reviewed=False)
        anchor = next(i for i in data['items'] if i['type'] == 'practical')['rubric'][0]['anchor']
        values = [anchor, '{"rubric": []}', "{'answer_key': 'A'}", '{"item_fingerprint": "synthetic"}']
        for value in values:
            with self.subTest(value=value):
                data['public']['format'] = value
                with self.assertRaisesRegex(ValueError, 'Candidate export blocked'):
                    c.export(data, 'candidate-guide')

    def test_program_and_domain_titles_cannot_bypass_known_text_check(self):
        for field in ('program', 'domain'):
            with self.subTest(field=field):
                data = harbor(reviewed=False)
                if field == 'program':
                    data['program']['title'] = data['items'][0]['prompt']
                else:
                    data['blueprint']['domains'][0]['title'] = data['items'][0]['prompt']
                with self.assertRaisesRegex(ValueError, 'Candidate export blocked'):
                    c.export(data, 'candidate-guide')


if __name__ == '__main__':
    unittest.main()
