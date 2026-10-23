"""Synthetic Harbor certification fixture; not a real job study or item bank."""
import importlib.util
from pathlib import Path
import copy
import csv

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('certification', ROOT / 'skills/certification-workshop/scripts/certification.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def harbor(reviewed=True):
    d = c.new_program('harbor-admin', 'Harbor Data Platform Administrator', 'demo')
    d['program'].update(owner='Synthetic program owner', audience='Implementation administrators',
                        claim='Perform defined ingestion, access and recovery tasks in the fictional Harbor environment.',
                        purpose='Demonstrate the complete certification development workflow.')
    for sid, name in [('DATA', 'Ingestion'), ('SEC', 'Access'), ('REC', 'Recovery')]:
        d['sources'].append({'id': sid, 'version': '1.0', 'title': f'Harbor {name} Guide',
                             'location': f'sources/{sid.lower()}.md', 'evidence_kind': 'synthetic', 'current': True})
    tasks = [
        ('T1', 'Import a UTF-8 dataset and verify row counts and rejected-row evidence before making it available.', 'DATA'),
        ('T2', 'Grant a service account dataset-specific read access and remove leaked credentials.', 'SEC'),
        ('T3', 'Recover a dataset from an immutable snapshot into a new namespace and reconcile it before cutover.', 'REC')]
    for n, (tid, statement, source) in enumerate(tasks, 1):
        d['tasks'].append({'id': tid, 'statement': statement, 'source_refs': [{'source_id': source, 'version': '1.0', 'locator': 'Rules 1-4'}],
                           'study_status': 'synthetic-workshop-example'})
        d['competencies'].append({'id': f'C{n}', 'statement': statement, 'task_ids': [tid]})
    d['blueprint'].update(status='approved' if reviewed else 'draft', form_length=8,
        domains=[{'id': 'D', 'title': 'Data ingestion', 'weight': 50, 'competency_ids': ['C1']},
                 {'id': 'S', 'title': 'Access control', 'weight': 25, 'competency_ids': ['C2']},
                 {'id': 'R', 'title': 'Recovery', 'weight': 25, 'competency_ids': ['C3']}], required_methods={'practical': 1})

    def single(iid, domain, source, prompt, options, key, reason, section):
        comp = {'D': 'C1', 'S': 'C2', 'R': 'C3'}[domain]
        d['items'].append({'id': iid, 'revision': 1, 'domain_id': domain, 'competency_ids': [comp],
            'type': 'single_choice', 'status': 'approved' if reviewed else 'draft', 'prompt': prompt,
            'options': dict(zip('ABCD', options)), 'answer_key': key, 'rationale': reason, 'max_score': 1,
            'source_refs': [{'source_id': source, 'version': '1.0', 'locator': section}], 'enemy_groups': []})

    single('D01', 'D', 'DATA', 'A Harbor import reports 980 accepted and 20 rejected rows from a 1,000-row source. What should the administrator do before publishing?',
           ['Publish because most rows succeeded.', 'Inspect the rejection report and reconcile all source rows.', 'Delete the rejection report.', 'Retry until the accepted count increases.'], 'B',
           'Rule 2 requires reconciling accepted plus rejected counts and reviewing rejections; a majority accepted is insufficient.', 'Rule 2')
    single('D02', 'D', 'DATA', 'A CSV has a first row containing field names. Which Harbor import setting preserves that row as column names?',
           ['header=false', 'header=true', 'overwrite=true', 'skip_errors=true'], 'B',
           'Rule 1 defines header=true. The other settings do not select header interpretation.', 'Rule 1')
    single('D03', 'D', 'DATA', 'An import contains an empty required customer_id. Under Harbor v1, what happens to that row?',
           ['It receives a generated customer ID.', 'It replaces the previous row.', 'It is rejected with a reason in the rejection report.', 'It is accepted as a null key.'], 'C',
           'Rule 3 requires rejection of a missing required identifier; Harbor does not generate one.', 'Rule 3')
    single('D05', 'D', 'DATA', 'An administrator wants to inspect the first ten accepted rows without altering the dataset. Which documented action fits?',
           ['preview --limit 10', 'publish --force', 'delete --limit 10', 'retry --overwrite'], 'A',
           'Rule 4 defines a read-only preview command. Publishing, deleting and retrying have other effects.', 'Rule 4')
    single('D06', 'D', 'DATA', 'The accepted count plus rejected count does not equal the source row count. What is the appropriate publication decision?',
           ['Publish if the sample looks correct.', 'Publish and remove the source.', 'Assume duplicate rows account for the difference.', 'Hold publication and investigate the reconciliation gap.'], 'D',
           'Rule 2 requires complete reconciliation before publication; no automatic duplicate explanation is supported.', 'Rule 2')
    single('S01', 'S', 'SEC', 'A service account needs to read dataset orders and must not edit it. Which grant meets the documented requirement?',
           ['Workspace administrator', 'Dataset orders reader', 'Dataset orders writer', 'Workspace owner'], 'B',
           'Rule 1 specifies a dataset-specific reader role. The other roles grant excess authority.', 'Rule 1')
    single('S02', 'S', 'SEC', 'A service-account token was disclosed. Which action immediately invalidates that token under Harbor v1?',
           ['Rename the service account.', 'Change its description.', 'Revoke the token and create a replacement through the credential workflow.', 'Create a second token without revoking the first.'], 'C',
           'Rule 2 requires revocation; account metadata changes and creating another token do not revoke it.', 'Rule 2')
    single('R01', 'R', 'REC', 'A recovery operator wants to modify an existing Harbor snapshot before restoring it. What does the documented snapshot behavior permit?',
           ['Edit snapshot rows in place.', 'Overwrite the snapshot with a live dataset.', 'Modify its contents after approval.', 'Restore its immutable contents to a new namespace.'], 'D',
           'Rule 1 defines snapshots as immutable, and rule 2 defines restoration to a new namespace.', 'Rules 1-2')
    single('R02', 'R', 'REC', 'A restored dataset has been created in a new namespace. What must happen before clients are cut over?',
           ['Reconcile counts and verify access using the recovery checklist.', 'Delete the original immediately.', 'Skip verification because the restore completed.', 'Grant all users administrator access.'], 'A',
           'Rule 3 requires reconciliation and access verification before cutover; restore completion is insufficient.', 'Rule 3')

    for iid, domain, source, prompt, setup, deliverable, criteria in [
        ('D04', 'D', 'DATA', 'Prepare a publication decision for the supplied import report.',
         'Synthetic source: 1,000 rows; accepted: 980; rejected: 20 with missing customer_id. No live system.',
         'A short reconciliation and publication recommendation.',
         [('Reconcile counts', '2: explicitly accounts for all 1,000 rows; 1: identifies accepted/rejected counts without reconciliation; 0: ignores the gap.'),
          ('Resolve rejection decision', '2: holds publication and requests source correction/review of missing IDs; 1: notes errors but no publication decision; 0: publishes without review.')]),
        ('S03', 'S', 'SEC', 'Prepare a least-privilege service-account access plan for dataset orders.',
         'Synthetic role matrix only. Account has no current grants; no credentials are required.',
         'Grant choice and verification plan.',
         [('Select grant', '2: dataset orders reader only; 1: reader plus unnecessary read grants; 0: grants write/admin.'),
          ('Verify boundaries', '2: plans successful read and denied write checks; 1: only a successful read check; 0: no verification.')]),
        ('R03', 'R', 'REC', 'Prepare a recovery and cutover checklist for an immutable snapshot.',
         'Synthetic snapshot of 1,000 rows and an empty new namespace. No live system.',
         'Ordered restore, verification and cutover steps.',
         [('Restore safely', '2: restore into new namespace while preserving original; 1: new namespace with unclear preservation; 0: destructive overwrite.'),
          ('Verify before cutover', '2: reconcile counts and verify access before cutover; 1: only one check; 0: immediate cutover.')])]:
        d['items'].append({'id': iid, 'revision': 1, 'domain_id': domain,
            'competency_ids': [{'D': 'C1', 'S': 'C2', 'R': 'C3'}[domain]], 'type': 'practical',
            'status': 'approved' if reviewed else 'draft', 'prompt': prompt, 'setup': setup, 'deliverable': deliverable,
            'rubric': [{'criterion': title, 'points': 2, 'anchor': anchor} for title, anchor in criteria],
            'rationale': 'The rubric observes the relevant documented action and verification behavior.', 'max_score': 4,
            'source_refs': [{'source_id': source, 'version': '1.0', 'locator': 'Rules 1-4'}], 'enemy_groups': []})
    d['items'].sort(key=lambda i: i['id'])
    if reviewed:
        for item in d['items']:
            d['reviews'].append({'id': 'REV_' + item['id'], 'item_id': item['id'], 'revision': 1,
                'reviewer': 'Synthetic content reviewer', 'role': 'content', 'verdict': 'accept',
                'evidence_kind': 'synthetic', 'evidence_ref': 'review-register.md', 'item_fingerprint': c.content_fingerprint(item)})
        result = c.assemble(d, 'PILOT1')
        assert result['assembled']
        d['forms'].append(result['form'])
    d['public'] = {'overview': 'Illustrative Harbor administrator certification. This is a synthetic demonstration, not an offered credential.',
                   'audience': 'Implementation administrators working within the stated Harbor role scope.',
                   'eligibility': 'Proposed for owner review; no actual enrollment.',
                   'format': 'Demo: eight tasks/questions including a scored practical exercise.',
                   'permitted_resources': 'Synthetic product reference supplied for this demonstration.',
                   'accommodations': 'A real program must publish an accessible request and decision process.',
                   'retakes': 'Owner decision pending for a real program.', 'appeals': 'Owner decision pending for a real program.',
                   'renewal': 'Owner decision pending for a real program.', 'support': 'No live service; demonstration only.'}
    return d


def write_scores(folder, data):
    form, items = c.pinned_items(data, 'PILOT1')
    headers = [f"{i['id']}@{i['revision']}" for i in items]
    with (folder / 'pilot-scores.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['candidate_id', *headers])
        for candidate in range(12):
            scores = []
            for col, item in enumerate(items):
                correct = (candidate + col * 3) % 12 >= col % 5
                scores.append((candidate + col) % 5 if item['type'] == 'practical' else int(correct))
            writer.writerow([f'SYNTHETIC_{candidate + 1:02}', *scores])
    with (folder / 'panel-judgments.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['judge_id', *headers])
        for judge, proportion in enumerate((0.55, 0.6, 0.65), 1):
            writer.writerow([f'SYNTHETIC_JUDGE_{judge}', *[round(i['max_score'] * proportion, 2) for i in items]])


def changed_source(data):
    d = copy.deepcopy(data)
    old = next(s for s in d['sources'] if s['id'] == 'SEC')
    old['current'] = False
    new = dict(old, version='2.0', current=True, location='sources/sec-v2.md')
    d['sources'].append(new)
    return d
