"""Offline certification record and assessment helpers. Python 3.10+, no network."""
import argparse
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import sys

SCHEMA = 1
ID = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,63}$')
COLLECTIONS = ('sources', 'tasks', 'competencies', 'items', 'reviews', 'decisions', 'forms', 'awards')
KINDS = {'single_choice', 'practical'}
STATUSES = {'draft', 'in_review', 'approved', 'retired'}
BASE = Path(__file__).resolve().parents[1]
SHA256 = re.compile(r'^[0-9a-fA-F]{64}$')
MAX_EVIDENCE_BYTES = 10 * 1024 * 1024
PUBLIC_FIELDS = ('overview', 'audience', 'eligibility', 'format', 'permitted_resources',
                 'accommodations', 'retakes', 'appeals', 'renewal', 'support')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def text(value):
    return isinstance(value, str) and bool(value.strip())


def identifier(value):
    return isinstance(value, str) and ID.fullmatch(value) is not None


def load(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, f'Duplicate JSON key: {key}')
            obj[key] = value
        return obj
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Non-finite JSON number')))


def save_new(path, value):
    path = Path(path)
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(json.dumps(value, indent=2, allow_nan=False) + '\n')


def new_program(program_id, title, mode='real'):
    require(identifier(program_id), 'Program ID must be a short letter-led identifier')
    require(text(title), 'Program title is required')
    require(mode in {'real', 'demo'}, 'mode must be real or demo')
    return {'schema_version': SCHEMA,
            'program': {'id': program_id, 'title': title, 'mode': mode, 'revision': 1,
                        'owner': '', 'audience': '', 'claim': '', 'purpose': '', 'status': 'draft'},
            'blueprint': {'id': 'BP1', 'revision': 1, 'status': 'draft', 'weight_basis': 'items',
                          'form_length': 0, 'domains': [], 'required_methods': {}},
            **{key: [] for key in COLLECTIONS}, 'public': {}, 'policies': {}, 'notes': []}


def initialize(destination, program_id, title, mode='real'):
    data = new_program(program_id, title, mode)
    destination = Path(destination)
    require(not destination.exists(), 'Program folder already exists; choose a new folder or resume it')
    destination.mkdir(parents=True, exist_ok=False)
    save_new(destination / 'program.json', data)
    (destination / 'working-templates.md').write_text((BASE / 'assets/templates.md').read_text(encoding='utf-8'), encoding='utf-8')
    (destination / 'summary.md').write_text(
        f'# {title}\n\nMode: {mode}. New program; no job study, review, pilot or approval has occurred.\n\n'
        'Next: draft the charter and source inventory from supplied material; record owner decisions.\n'
        'Use working-templates.md for real development artifacts. Keep restricted records in this folder.\n', encoding='utf-8')
    return {'created': str(destination), 'program': str(destination / 'program.json'), 'mode': mode}


def validate(data):
    """Validate structure and relationships, not certification validity or human decisions."""
    require(isinstance(data, dict) and type(data.get('schema_version')) is int and data['schema_version'] == SCHEMA, 'Unsupported program schema_version')
    p = data.get('program')
    require(isinstance(p, dict) and identifier(p.get('id')) and text(p.get('title')), 'Invalid program identity')
    require(p.get('mode') in {'real', 'demo'} and integer(p.get('revision')), 'Invalid program mode/revision')
    for key in COLLECTIONS:
        require(isinstance(data.get(key), list), f'{key} must be an array')
        seen = set()
        for row in data[key]:
            require(isinstance(row, dict) and identifier(row.get('id')), f'{key}: invalid record ID')
            uid = (row['id'], row.get('version')) if key == 'sources' else row['id']
            require(uid not in seen, f'{key}: duplicate identity')
            seen.add(uid)
    require(isinstance(data.get('public', {}), dict), 'public must be an object')
    for key, value in data.get('public', {}).items():
        require(isinstance(value, str), 'Public fields must be text reviewed for their audience')
    require(isinstance(data.get('policies', {}), dict), 'policies must be an object')
    policy = data.get('validation_policy', {})
    require(isinstance(policy, dict) and policy.get('evidence_integrity', 'if_declared') in
            {'if_declared', 'required'}, 'Invalid validation_policy.evidence_integrity')
    sources = {}
    current = set()
    for s in data['sources']:
        require(text(s.get('version')) and text(s.get('location')), 'Source version and location required')
        require(s.get('evidence_kind') in {'real', 'synthetic'}, 'Source evidence_kind required')
        require(isinstance(s.get('current'), bool), 'Source current must be boolean')
        if s['current']:
            require(s['id'] not in current, 'Only one current version per source ID')
            current.add(s['id'])
        sources[s['id'], s['version']] = s

    def refs(row, required=False):
        values = row.get('source_refs', [])
        require(isinstance(values, list) and (bool(values) or not required), 'source_refs must contain supporting locations')
        for ref in values:
            require(isinstance(ref, dict) and text(ref.get('locator')), 'Source locator required')
            require((ref.get('source_id'), ref.get('version')) in sources, 'Unknown source ID/version')

    task_ids = {t['id'] for t in data['tasks']}
    comp_ids = {c['id'] for c in data['competencies']}
    for t in data['tasks']:
        require(text(t.get('statement')), 'Task statement required')
        refs(t)
    for c in data['competencies']:
        require(text(c.get('statement')), 'Competency statement required')
        require(isinstance(c.get('task_ids'), list) and c['task_ids'] and all(t in task_ids for t in c['task_ids']), 'Competency task mapping invalid')
    bp = data.get('blueprint')
    require(isinstance(bp, dict) and identifier(bp.get('id')) and integer(bp.get('revision')), 'Invalid blueprint identity')
    require(bp.get('weight_basis') == 'items', 'Helper supports item-count weights only')
    require(bp.get('status') in STATUSES, 'Invalid blueprint status')
    require(isinstance(bp.get('domains'), list), 'Blueprint domains must be an array')
    require(isinstance(bp.get('form_length'), int) and not isinstance(bp['form_length'], bool) and bp['form_length'] >= 0, 'Invalid form length')
    domain_ids = set()
    domains = {}
    for d in bp['domains']:
        require(isinstance(d, dict) and identifier(d.get('id')) and d['id'] not in domain_ids, 'Invalid/duplicate domain ID')
        domain_ids.add(d['id'])
        domains[d['id']] = d
        require(text(d.get('title')) and number(d.get('weight')) and 0 < d['weight'] <= 100, 'Invalid domain title/weight')
        require(isinstance(d.get('competency_ids'), list) and d['competency_ids'] and all(c in comp_ids for c in d['competency_ids']), 'Domain competency mapping invalid')
    if bp['domains']:
        require(math.isclose(sum(d['weight'] for d in bp['domains']), 100, abs_tol=1e-7), 'Blueprint weights must sum to 100')
        require(bp['form_length'] > 0, 'Populated blueprint needs positive form_length')
    score_policy = bp.get('score_weight_policy')
    if score_policy is not None:
        require(isinstance(score_policy, dict) and score_policy.get('basis') == 'raw_points',
                'score_weight_policy currently supports raw_points only; no automatic domain normalization')
        tolerance = score_policy.get('tolerance_percentage_points', 0.01)
        require(number(tolerance) and 0 <= tolerance <= 100, 'Invalid score-weight tolerance')
        if 'target_percent' in score_policy:
            target = score_policy['target_percent']
            require(isinstance(target, dict) and set(target) == domain_ids and
                    all(number(v) and 0 < v <= 100 for v in target.values()) and
                    math.isclose(sum(target.values()), 100, abs_tol=1e-7),
                    'Score-weight targets must cover every domain and sum to 100')
    methods = bp.get('required_methods', {})
    require(isinstance(methods, dict), 'required_methods must be an object')
    for k, v in methods.items():
        require(k in KINDS and isinstance(v, int) and not isinstance(v, bool) and v >= 0, 'Invalid required method count')
    domain_methods = bp.get('required_methods_by_domain', {})
    require(isinstance(domain_methods, dict) and set(domain_methods) <= domain_ids,
            'Invalid per-domain method mapping')
    for values in domain_methods.values():
        require(isinstance(values, dict) and all(k in KINDS and isinstance(v, int) and not isinstance(v, bool)
                and v >= 0 for k, v in values.items()), 'Invalid per-domain method count')
    for item in data['items']:
        require(integer(item.get('revision')), 'Item revision must be a positive integer')
        require(item.get('domain_id') in domains and item.get('type') in KINDS, 'Invalid item domain/type')
        require(item.get('status') in STATUSES and text(item.get('prompt')), 'Invalid item status/prompt')
        require(isinstance(item.get('competency_ids'), list) and item['competency_ids'] and all(c in domains[item['domain_id']]['competency_ids'] for c in item['competency_ids']), 'Item competency outside domain')
        require(number(item.get('max_score')) and item['max_score'] > 0, 'Invalid maximum score')
        require(text(item.get('rationale')), 'Item rationale required')
        refs(item, required=True)
        require(isinstance(item.get('enemy_groups', []), list) and all(identifier(g) for g in item.get('enemy_groups', [])), 'Invalid enemy group')
        if item['type'] == 'single_choice':
            options = item.get('options')
            require(isinstance(options, dict) and len(options) >= 2 and all(text(k) and text(v) for k, v in options.items()), 'At least two labeled options required')
            require(len(set(options.values())) == len(options), 'Duplicate option text')
            require(item.get('answer_key') in options and item['max_score'] == 1, 'Single-choice key/max_score invalid')
        else:
            rubric = item.get('rubric')
            require(isinstance(rubric, list) and rubric, 'Practical task rubric required')
            require(text(item.get('setup')) and text(item.get('deliverable')), 'Practical setup and deliverable required')
            for criterion in rubric:
                require(isinstance(criterion, dict) and text(criterion.get('criterion')) and text(criterion.get('anchor')) and number(criterion.get('points')) and criterion['points'] > 0, 'Invalid rubric criterion')
            require(math.isclose(sum(c['points'] for c in rubric), item['max_score']), 'Rubric points must sum to max_score')
    item_ids = {i['id'] for i in data['items']}
    for r in data['reviews']:
        require(r.get('item_id') in item_ids and integer(r.get('revision')), 'Review target invalid')
        require(r.get('verdict') in {'accept', 'revise', 'reject'} and r.get('evidence_kind') in {'real', 'synthetic'}, 'Invalid review verdict/evidence')
        require(text(r.get('reviewer')) and text(r.get('role')) and text(r.get('evidence_ref')), 'Review attribution/evidence required')
        require(isinstance(r.get('resolved', False), bool), 'Review resolved must be boolean')
        if r.get('resolved'):
            require(text(r.get('resolution')) and text(r.get('resolved_by')), 'Review resolution needs reason and authority')
    for d in data['decisions']:
        require(d.get('target_type') in {'program', 'blueprint', 'form', 'award'}, 'Invalid decision target type')
        require(identifier(d.get('target_id')) and integer(d.get('revision')), 'Decision target/revision invalid')
        require(d.get('decision') in {'approve', 'reject'} and d.get('evidence_kind') in {'real', 'synthetic'}, 'Invalid decision')
        require(text(d.get('actor')) and text(d.get('evidence_ref')) and text(d.get('rationale')), 'Decision authority/evidence/rationale required')
    for f in data['forms']:
        require(integer(f.get('revision')) and integer(f.get('blueprint_revision')), 'Invalid form revision')
        require(isinstance(f.get('item_refs'), list) and f['item_refs'], 'Form item_refs required')
        seen = set()
        for ref in f['item_refs']:
            require(isinstance(ref, dict) and ref.get('item_id') in item_ids and integer(ref.get('revision')), 'Invalid form item reference')
            require(ref['item_id'] not in seen, 'Duplicate item in form')
            seen.add(ref['item_id'])
    for a in data['awards']:
        require(text(a.get('candidate_id')) and text(a.get('credential_version')) and identifier(a.get('decision_id')), 'Award identity/decision required')
        require(a['candidate_id'] == a['candidate_id'].strip() and a['credential_version'] == a['credential_version'].strip(), 'Award identity/version must not contain surrounding whitespace')
        require(integer(a.get('revision', 1)), 'Award revision must be a positive integer')
        require(a.get('action', 'issue') in {'issue', 'revoke'}, 'Award action must be issue or revoke')
        require(a.get('status') in {'draft', 'authorized', 'submitted', 'unknown', 'issued', 'revoked'}, 'Invalid award status')
    return {'valid_structure': True, 'program_id': p['id'], 'mode': p['mode'], 'items': len(data['items'])}


def audit_evidence(data, root):
    """Check declared local bytes, never authenticate authors or fetch external evidence."""
    validate(data)
    root = Path(root).resolve()
    rows, issues = [], []

    def inspect(label, location, expected):
        row = {'record': label, 'location': location, 'sha256': expected, 'verified': False, 'issues': []}
        def issue(code):
            row['issues'].append(code)
            issues.append(code + ':' + label)
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            issue('missing_or_invalid_digest')
        if not text(location):
            issue('missing_evidence_location')
        elif '://' in location or location.startswith(('mailto:', 'data:')):
            issue('external_evidence_unverified')
        else:
            path = Path(location)
            try:
                # Neither a record nor a symlink may grant access outside the supplied project root.
                require(not path.is_absolute() and '..' not in path.parts and '\\' not in location,
                        'unsafe evidence path')
                resolved = (root / path).resolve()
                require(resolved.is_relative_to(root), 'unsafe evidence path')
                if not resolved.is_file():
                    issue('missing_evidence_file')
                elif resolved.stat().st_size > MAX_EVIDENCE_BYTES:
                    issue('evidence_file_too_large')
                else:
                    digest, size = hashlib.sha256(), 0
                    with resolved.open('rb') as stream:
                        while chunk := stream.read(64 * 1024):
                            size += len(chunk)
                            require(size <= MAX_EVIDENCE_BYTES, 'evidence file grew beyond limit')
                            digest.update(chunk)
                    row['actual_sha256'] = digest.hexdigest()
                    row['size_bytes'] = size
                    if isinstance(expected, str) and SHA256.fullmatch(expected) and digest.hexdigest() != expected.lower():
                        issue('evidence_digest_mismatch')
            except ValueError:
                issue('unsafe_or_oversized_evidence_path')
            except OSError:
                issue('evidence_file_unreadable')
        row['verified'] = not row['issues']
        rows.append(row)

    for source in data['sources']:
        inspect('source:' + source['id'] + '@' + source['version'], source.get('location'), source.get('sha256'))
    for review in data['reviews']:
        inspect('review:' + review['id'], review.get('evidence_ref'), review.get('evidence_sha256'))
    for decision in data['decisions']:
        inspect('decision:' + decision['id'], decision.get('evidence_ref'), decision.get('evidence_sha256'))
    for form in data['forms']:
        evidence = form.get('release_evidence', {})
        digests = form.get('release_evidence_sha256', {})
        if isinstance(evidence, dict):
            for key in sorted(set(evidence) | (set(digests) if isinstance(digests, dict) else set())):
                inspect('release:' + form['id'] + ':' + key, evidence.get(key),
                        digests.get(key) if isinstance(digests, dict) else None)
    return {'checks_pass': not issues, 'scope': 'local_evidence_integrity', 'checks': rows,
            'issues': sorted(set(issues)),
            'note': 'Matching bytes prove consistency with a declared digest, not authorship, reviewer identity, truth, authority or validity. No network request was made.'}


def evidence_gate(data, root=None):
    required = data.get('validation_policy', {}).get('evidence_integrity') == 'required'
    declared = {('source:' + s['id'] + '@' + s['version']) for s in data['sources'] if 'sha256' in s}
    declared.update('review:' + r['id'] for r in data['reviews'] if 'evidence_sha256' in r)
    declared.update('decision:' + d['id'] for d in data['decisions'] if 'evidence_sha256' in d)
    declared.update('release:' + f['id'] + ':' + key for f in data['forms']
                    if isinstance(f.get('release_evidence_sha256'), dict) for key in f['release_evidence_sha256'])
    if not required and not declared:
        return []
    if root is None:
        return ['evidence_root_required']
    audit = audit_evidence(data, root)
    return sorted({code + ':' + row['record'] for row in audit['checks']
                   if required or row['record'] in declared for code in row['issues']})


def score_weighting(data, items=None):
    """Reconcile raw points; item allocation is not a score-weight policy."""
    chosen = data['items'] if items is None else items
    total = sum(i['max_score'] for i in chosen)
    policy = data['blueprint'].get('score_weight_policy', {})
    targets = policy.get('target_percent', {})
    tolerance = policy.get('tolerance_percentage_points', 0.01)
    rows, warnings, mismatches = [], [], []
    for domain in data['blueprint']['domains']:
        points = sum(i['max_score'] for i in chosen if i['domain_id'] == domain['id'])
        percent = 100 * points / total if total else None
        row = {'domain_id': domain['id'], 'item_weight_percent': domain['weight'],
               'max_score': points, 'score_weight_percent': percent}
        if percent is not None and not math.isclose(percent, domain['weight'], abs_tol=0.01):
            warnings.append('item_and_raw_point_weights_differ:' + domain['id'])
        if domain['id'] in targets:
            row['target_score_weight_percent'] = targets[domain['id']]
            if percent is None or abs(percent - targets[domain['id']]) > tolerance + 1e-9:
                mismatches.append('score_weight_target_mismatch:' + domain['id'])
        rows.append(row)
    if not targets:
        warnings.append('score_weight_targets_not_declared')
    return {'scope': 'bank_diagnostic' if items is None else 'selected_form', 'basis': 'raw_points',
            'max_score': total, 'domains': rows, 'warnings': warnings, 'target_issues': mismatches,
            'note': 'This is raw-point arithmetic, not a passing standard or psychometric recommendation. Bank totals are not a proposed form.'}


def public_export_issues(data):
    """Conservative known-content check, not arbitrary secret detection or semantic review."""
    def norm(value):
        return ' '.join(value.casefold().split())
    restricted = []
    for item in data['items']:
        for key in ('prompt', 'rationale', 'setup', 'deliverable'):
            if text(item.get(key)):
                restricted.append(('item.' + item['id'] + '.' + key, norm(item[key])))
        for index, row in enumerate(item.get('rubric', [])):
            restricted.append(('item.' + item['id'] + '.rubric.' + str(index), norm(row['anchor'])))
        for label, option in item.get('options', {}).items():
            restricted.append(('item.' + item['id'] + '.option.' + label, norm(option)))
    for index, note in enumerate(data.get('notes', [])):
        if text(note):
            restricted.append(('note.' + str(index), norm(note)))
    issues = []
    exported = {field: data.get('public', {}).get(field, '') for field in PUBLIC_FIELDS}
    exported['program_title'] = data['program']['title']
    exported.update({'domain_title.' + d['id']: d['title'] for d in data['blueprint']['domains']})
    for field, value in exported.items():
        value = norm(value)
        for label, phrase in restricted:
            if len(phrase) >= 12 and phrase in value:
                issues.append('known_restricted_text:' + field + ':' + label)
        if re.search(r'["\'](?:answer_key|item_fingerprint|rubric)["\']\s*:', value):
            issues.append('restricted_record_marker:' + field)
    return sorted(set(issues))


def index_items(data):
    return {i['id']: i for i in data['items']}


def content_fingerprint(obj):
    content = {k: v for k, v in obj.items() if k not in {'status', 'release_evidence'}}
    return hashlib.sha256(json.dumps(content, sort_keys=True, allow_nan=False).encode()).hexdigest()


def program_approval_fingerprint(data):
    payload = {'program': {k: v for k, v in data['program'].items() if k != 'status'},
               'policies': data.get('policies', {}), 'public': data.get('public', {})}
    if 'validation_policy' in data:
        payload['validation_policy'] = data['validation_policy']
    return content_fingerprint(payload)


def blueprint_approval_fingerprint(data):
    return content_fingerprint({'blueprint': {k: v for k, v in data['blueprint'].items() if k != 'status'},
                                'tasks': data['tasks'], 'competencies': data['competencies'], 'sources': data['sources']})


def award_fingerprint(award):
    # State and provider receipts change after the authorized effect; identity/effect/evidence do not.
    return content_fingerprint({'id': award['id'], 'revision': award.get('revision', 1),
        'candidate_id': award['candidate_id'], 'credential_version': award['credential_version'],
        'action': award.get('action', 'issue'), 'eligibility_evidence': award.get('eligibility_evidence'),
        'result_evidence': award.get('result_evidence'), 'reason': award.get('reason')})


def decision_ok(data, target_type, target_id, revision, live=False, fingerprint=None):
    matches = [d for d in data['decisions'] if d['target_type'] == target_type and d['target_id'] == target_id and d['revision'] == revision]
    # Conflicting decisions require an explicit new version, not an arbitrary list-order winner.
    return bool(matches) and all(d['decision'] == 'approve' and (not live or d['evidence_kind'] == 'real')
                                 and (fingerprint is None or d.get('target_fingerprint') == fingerprint) for d in matches)


def source_fingerprints(data, items):
    """Digest declarations for direct and task-derived support; bytes are checked separately."""
    sources = {(s['id'], s['version']): s for s in data['sources']}
    comp_ids = {cid for item in items for cid in item['competency_ids']}
    task_ids = {tid for comp in data['competencies'] if comp['id'] in comp_ids for tid in comp['task_ids']}
    refs = [ref for item in items for ref in item['source_refs']]
    refs += [ref for task in data['tasks'] if task['id'] in task_ids for ref in task.get('source_refs', [])]
    return {ref['source_id'] + '@' + ref['version']: sources[ref['source_id'], ref['version']]['sha256'].lower()
            for ref in refs if isinstance(sources[ref['source_id'], ref['version']].get('sha256'), str)}


def item_issues(data, item, live=False):
    issues = []
    if item['status'] != 'approved':
        issues.append('item_not_approved')
    reviews = [r for r in data['reviews'] if r['item_id'] == item['id'] and r['revision'] == item['revision']]
    support = source_fingerprints(data, [item])
    if not any(r['verdict'] == 'accept' and r['role'] == 'content' and r.get('item_fingerprint') == content_fingerprint(item)
               and r.get('source_fingerprints', {}) == support
               and (not live or r['evidence_kind'] == 'real') for r in reviews):
        issues.append('missing_current_content_acceptance')
    if any(r['verdict'] in {'revise', 'reject'} and not r.get('resolved') for r in reviews):
        issues.append('unresolved_negative_review')
    sources = {(s['id'], s['version']): s for s in data['sources']}
    task_ids = {t for c in data['competencies'] if c['id'] in item['competency_ids'] for t in c['task_ids']}
    supporting_refs = item['source_refs'] + [r for t in data['tasks'] if t['id'] in task_ids for r in t.get('source_refs', [])]
    for ref in supporting_refs:
        s = sources[ref['source_id'], ref['version']]
        if not s['current']:
            issues.append('outdated_source')
        if live and s['evidence_kind'] != 'real':
            issues.append('synthetic_source')
    return sorted(set(issues))


def allocation(data):
    validate(data)
    bp = data['blueprint']
    require(bp['domains'] and bp['form_length'] > 0, 'Define a blueprint before allocation')
    exact = {d['id']: d['weight'] * bp['form_length'] / 100 for d in bp['domains']}
    counts = {k: math.floor(v) for k, v in exact.items()}
    remainder = bp['form_length'] - sum(counts.values())
    for key in sorted(exact, key=lambda k: (-(exact[k] - counts[k]), k))[:remainder]:
        counts[key] += 1
    return counts


def coverage(data, live=False):
    validate(data)
    if not data['blueprint']['domains']:
        return {'domains': [], 'issues': ['blueprint_not_defined'], 'ready_to_assemble': False}
    targets = allocation(data)
    rows = []
    for d in data['blueprint']['domains']:
        items = [i for i in data['items'] if i['domain_id'] == d['id']]
        eligible = [i for i in items if not item_issues(data, i, live)]
        rows.append({'domain_id': d['id'], 'target_items': targets[d['id']], 'eligible_items': len(eligible),
                     'shortfall': max(0, targets[d['id']] - len(eligible)),
                     'eligible_by_method': {k: sum(i['type'] == k for i in eligible) for k in sorted(KINDS)}})
    issues = ['domain_rounds_to_zero:' + d for d, n in targets.items() if n == 0]
    return {'domains': rows, 'issues': issues,
            'ready_to_assemble': not issues and not any(r['shortfall'] for r in rows),
            'note': 'Count coverage only; method/enemy-group feasibility is checked by assemble.'}


def assemble(data, form_id, live=False, max_nodes=100000, evidence_root=None):
    validate(data)
    require(identifier(form_id) and form_id not in {f['id'] for f in data['forms']}, 'Use a new form ID')
    evidence_issues = evidence_gate(data, evidence_root)
    if evidence_issues:
        return {'assembled': False, 'reason': 'evidence_integrity', 'issues': evidence_issues}
    targets = allocation(data)
    require(all(n > 0 for n in targets.values()), 'A domain rounds to zero; revise blueprint length/weights')
    eligible = sorted((i for i in data['items'] if not item_issues(data, i, live)), key=lambda i: i['id'])
    length = data['blueprint']['form_length']
    # Exact search, bounded; never confuse a search limit with a proof of infeasibility.
    nodes = 0
    hit_limit = False
    answer = None

    def visit(start, chosen, counts, groups):
        nonlocal nodes, hit_limit, answer
        nodes += 1
        if nodes > max_nodes:
            hit_limit = True
            return False
        if len(chosen) == length:
            if all(sum(i['type'] == k for i in chosen) >= n for k, n in data['blueprint'].get('required_methods', {}).items()):
                per_domain = data['blueprint'].get('required_methods_by_domain', {})
                methods_ok = all(sum(i['type'] == kind and i['domain_id'] == domain for i in chosen) >= minimum
                                 for domain, methods in per_domain.items() for kind, minimum in methods.items())
                if methods_ok and not score_weighting(data, chosen)['target_issues']:
                    answer = list(chosen)
                    return True
            return False
        for domain, target in targets.items():
            available = sum(i['domain_id'] == domain and not (set(i.get('enemy_groups', [])) & groups) for i in eligible[start:])
            if counts.get(domain, 0) + available < target:
                return False
        for pos in range(start, len(eligible)):
            i = eligible[pos]
            domain = i['domain_id']
            enemies = set(i.get('enemy_groups', []))
            if counts.get(domain, 0) >= targets[domain] or enemies & groups:
                continue
            new_counts = dict(counts)
            new_counts[domain] = new_counts.get(domain, 0) + 1
            if visit(pos + 1, chosen + [i], new_counts, groups | enemies):
                return True
            if hit_limit:
                return False
        return False

    visit(0, [], {}, set())
    if answer is None:
        return {'assembled': False, 'reason': 'search_limit' if hit_limit else 'infeasible', 'coverage': coverage(data, live), 'nodes': nodes}
    form = {'id': form_id, 'revision': 1, 'blueprint_revision': data['blueprint']['revision'], 'status': 'draft',
            'item_refs': [{'item_id': i['id'], 'revision': i['revision'], 'item_fingerprint': content_fingerprint(i)} for i in answer]}
    support = source_fingerprints(data, answer)
    if support:
        form['source_fingerprints'] = support
    return {'assembled': True, 'form': form, 'target_counts': targets, 'max_score': sum(i['max_score'] for i in answer),
            'score_weighting': score_weighting(data, answer),
            'note': 'Proposal only. Store in forms after review; no launch or approval occurred.'}


def get_form(data, form_id):
    require(identifier(form_id), 'Invalid form ID')
    found = [f for f in data['forms'] if f['id'] == form_id]
    require(len(found) == 1, 'Form ID not found')
    return found[0]


def check_form(data, form_id, live=False, evidence_root=None):
    validate(data)
    f = get_form(data, form_id)
    items = index_items(data)
    issues = evidence_gate(data, evidence_root)
    targets = allocation(data)
    if f['blueprint_revision'] != data['blueprint']['revision']:
        issues.append('stale_blueprint_revision')
    if len(f['item_refs']) != data['blueprint']['form_length']:
        issues.append('wrong_form_length')
    selected = []
    groups = set()
    for ref in f['item_refs']:
        i = items[ref['item_id']]
        if i['revision'] != ref['revision']:
            issues.append('stale_item_revision:' + i['id'])
        if ref.get('item_fingerprint') != content_fingerprint(i):
            issues.append('unpinned_or_changed_item_content:' + i['id'])
        issues.extend(code + ':' + i['id'] for code in item_issues(data, i, live))
        overlap = groups & set(i.get('enemy_groups', []))
        if overlap:
            issues.append('enemy_group_conflict')
        groups.update(i.get('enemy_groups', []))
        selected.append(i)
    for d, n in targets.items():
        if n == 0 or sum(i['domain_id'] == d for i in selected) != n:
            issues.append('domain_coverage:' + d)
    for k, n in data['blueprint'].get('required_methods', {}).items():
        if sum(i['type'] == k for i in selected) < n:
            issues.append('method_coverage:' + k)
    for domain, methods in data['blueprint'].get('required_methods_by_domain', {}).items():
        for kind, minimum in methods.items():
            if sum(i['domain_id'] == domain and i['type'] == kind for i in selected) < minimum:
                issues.append('domain_method_coverage:' + domain + ':' + kind)
    weights = score_weighting(data, selected)
    issues.extend(weights['target_issues'])
    support = source_fingerprints(data, selected)
    if f.get('source_fingerprints', {}) != support:
        issues.append('unpinned_or_changed_source_content')
    if live:
        if data['program']['mode'] != 'real':
            issues.append('synthetic_program')
        for field in ('owner', 'audience', 'claim', 'purpose'):
            if not text(data['program'].get(field)):
                issues.append('missing_program_field:' + field)
        for typ, obj in [('program', data['program']), ('blueprint', data['blueprint']), ('form', f)]:
            if obj.get('status') != 'approved':
                issues.append('not_approved:' + typ)
            fingerprint = (form_approval_fingerprint(f, selected) if typ == 'form' else
                           program_approval_fingerprint(data) if typ == 'program' else blueprint_approval_fingerprint(data))
            if not decision_ok(data, typ, obj['id'], obj['revision'], True, fingerprint):
                issues.append('missing_real_approval:' + typ)
        policy = data.get('policies', {})
        for key in ('passing_standard', 'eligibility', 'retakes', 'appeals', 'accommodations', 'renewal', 'data_retention', 'delivery'):
            if not text(policy.get(key)):
                issues.append('missing_policy:' + key)
        # The owner records these external evidence locations; this helper cannot authenticate them.
        evidence = f.get('release_evidence', {})
        for key in ('job_analysis_report', 'pilot_report', 'standard_setting_report', 'delivery_verification'):
            if not isinstance(evidence, dict) or not text(evidence.get(key)):
                issues.append('missing_release_evidence:' + key)
    return {'form_id': form_id, 'checks_pass': not issues, 'scope': 'live_record_checks' if live else 'development_record_checks',
            'score_weighting': weights,
            'issues': sorted(set(issues)), 'note': 'Record checks do not authenticate evidence, authorize launch, or establish validity.'}


def review_packet(data, ids=None):
    validate(data)
    chosen = ids or [i['id'] for i in data['items']]
    require(len(chosen) == len(set(chosen)) and set(chosen) <= set(index_items(data)), 'Unknown/duplicate review item')
    return {'classification': 'restricted', 'program_id': data['program']['id'], 'items': [copy.deepcopy(index_items(data)[k]) for k in chosen],
            'item_fingerprints': {k: content_fingerprint(index_items(data)[k]) for k in chosen},
            'source_fingerprints': {k: source_fingerprints(data, [index_items(data)[k]]) for k in chosen},
            'review_questions': ['Does it assess the mapped work at the intended level?', 'Is the key/rubric supported and unambiguous?',
                                 'Are irrelevant language, accessibility or bias barriers present?', 'Accept, revise or reject this exact revision, with evidence.'],
            'note': 'Prepared packet; no reviewer was contacted and no human review occurred.'}


def pinned_items(data, form_id):
    validate(data)
    f = get_form(data, form_id)
    items = index_items(data)
    require(all(items[r['item_id']]['revision'] == r['revision'] for r in f['item_refs']), 'Stale form: use the historical program snapshot for these data')
    require(all(r.get('item_fingerprint') == content_fingerprint(items[r['item_id']]) for r in f['item_refs']),
            'Unpinned or changed form content: recover the verified historical snapshot; do not attach old scores to current items')
    support = source_fingerprints(data, [items[r['item_id']] for r in f['item_refs']])
    require(f.get('source_fingerprints', {}) == support,
            'Unpinned or changed source content: recover the verified historical snapshot')
    return f, [items[r['item_id']] for r in f['item_refs']]


def form_fingerprint(form, items):
    payload = {'form': form['id'], 'revision': form['revision'], 'blueprint_revision': form['blueprint_revision'],
               'items': [{'id': i['id'], 'revision': i['revision'], 'content': content_fingerprint(i)} for i in items]}
    if form.get('source_fingerprints'):
        payload['source_fingerprints'] = form['source_fingerprints']
    return hashlib.sha256(json.dumps(payload, sort_keys=True, allow_nan=False).encode()).hexdigest()


def form_approval_fingerprint(form, items):
    # Approval binds study/readback evidence without changing the scored-form identity when those links are added.
    return content_fingerprint({'assessment': form_fingerprint(form, items), 'evidence': form.get('release_evidence', {})})


def score_matrix(path, items, id_column='candidate_id'):
    expected = [f"{i['id']}@{i['revision']}" for i in items]
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames is not None and len(reader.fieldnames) == len(set(reader.fieldnames)), 'Missing/duplicate CSV headers')
        require(set(reader.fieldnames) == {id_column, *expected}, 'CSV columns must match exact item revisions and ID column')
        seen = set()
        matrix = []
        for line, row in enumerate(reader, 2):
            require(None not in row and all(v is not None for v in row.values()), f'CSV shape mismatch at row {line}')
            who = row[id_column].strip()
            require(who and who not in seen, f'Missing/duplicate ID at row {line}')
            seen.add(who)
            values = []
            for column, item in zip(expected, items):
                require(row[column].strip() != '', f'Missing score at row {line}; supply an explicit scoring policy')
                try:
                    value = float(row[column])
                except ValueError:
                    raise ValueError(f'Non-numeric score at row {line}') from None
                require(number(value) and 0 <= value <= item['max_score'], f'Score outside permitted range at row {line}')
                if id_column == 'candidate_id' and item['type'] == 'single_choice':
                    require(value in (0, 1), f'Single-choice scores must be 0 or 1 at row {line}')
                values.append(value)
            matrix.append(values)
    require(matrix, 'No scored records')
    return matrix


def correlation(a, b):
    if len(a) < 2 or statistics.pvariance(a) == 0 or statistics.pvariance(b) == 0:
        return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    numerator = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    denominator = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return numerator / denominator


def analyze(data, form_id, path, evidence_root=None):
    validate(data)
    require(not evidence_gate(data, evidence_root), 'Evidence integrity failed before analysis')
    form, items = pinned_items(data, form_id)
    matrix = score_matrix(path, items)
    totals = [sum(row) for row in matrix]
    columns = list(zip(*matrix))
    n, k = len(matrix), len(items)
    variance = statistics.variance(totals) if n > 1 else None
    alpha = k / (k - 1) * (1 - sum(statistics.variance(c) for c in columns) / variance) if n > 1 and k > 1 and variance and variance > 0 else None
    rows = []
    for index, (item, column) in enumerate(zip(items, columns)):
        rest = [total - row[index] for total, row in zip(totals, matrix)]
        rows.append({'item_id': item['id'], 'revision': item['revision'], 'mean_score': statistics.mean(column),
                     'mean_proportion_of_max': statistics.mean(column) / item['max_score'],
                     'corrected_item_total_correlation': correlation(column, rest)})
    return {'classification': 'restricted', 'form_id': form_id, 'form_fingerprint': form_fingerprint(form, items),
            'n': n, 'max_score': sum(i['max_score'] for i in items), 'mean_total': statistics.mean(totals),
            'sd_total': math.sqrt(variance) if variance is not None else None, 'coefficient_alpha': alpha, 'items': rows,
            'limitations': ['Descriptive statistics for this supplied complete-case scored matrix only.',
                            'Null correlation/alpha means insufficient observations or zero variance; not zero.',
                            'No automatic pass decisions, item deletion, fairness, validity, equating or representativeness conclusion.',
                            'For practical tasks these are recorded scores, not independent rater-agreement evidence.']}


def panel_summary(data, form_id, path, evidence_root=None):
    validate(data)
    require(not evidence_gate(data, evidence_root), 'Evidence integrity failed before panel summary')
    form, items = pinned_items(data, form_id)
    matrix = score_matrix(path, items, 'judge_id')
    totals = [sum(row) for row in matrix]
    return {'classification': 'restricted', 'form_id': form_id, 'form_fingerprint': form_fingerprint(form, items),
            'judges': len(matrix), 'mean_expected_total': statistics.mean(totals),
            'min_expected_total': min(totals), 'max_expected_total': max(totals),
            'item_mean_expected_scores': {i['id']: statistics.mean(c) for i, c in zip(items, zip(*matrix))},
            'note': 'Arithmetic summary of supplied expected-score judgments, not an approved cut score. Do not invent judges, choose a rounding rule, or issue credentials from this value.'}


def impact(data, source_ids):
    validate(data)
    require(source_ids and set(source_ids) <= {s['id'] for s in data['sources']}, 'Unknown/empty source IDs')
    sources = set(source_ids)
    task_ids = {t['id'] for t in data['tasks'] if any(r['source_id'] in sources for r in t.get('source_refs', []))}
    comp_ids = {c['id'] for c in data['competencies'] if set(c['task_ids']) & task_ids}
    domain_ids = {d['id'] for d in data['blueprint']['domains'] if set(d['competency_ids']) & comp_ids}
    item_ids = {i['id'] for i in data['items'] if any(r['source_id'] in sources for r in i['source_refs']) or set(i['competency_ids']) & comp_ids}
    form_ids = {f['id'] for f in data['forms'] if any(r['item_id'] in item_ids for r in f['item_refs'])}
    return {'source_ids': sorted(sources), 'tasks': sorted(task_ids), 'competencies': sorted(comp_ids), 'domains': sorted(domain_ids),
            'items': sorted(item_ids), 'forms': sorted(form_ids), 'note': 'Conservative dependency impact. Inspect semantic changes; no records were modified.'}


def export(data, audience, form_id=None, evidence_root=None):
    validate(data)
    if audience == 'candidate-guide':
        # Explicit allowlist: never serialize items, prompts, keys, rubrics, reviews, notes or candidate records here.
        issues = public_export_issues(data)
        require(not issues, 'Candidate export blocked: ' + ', '.join(issues))
        return {'classification': 'public-draft', 'program_title': data['program']['title'],
                'guide': {k: data.get('public', {}).get(k, '') for k in PUBLIC_FIELDS},
                'domains': [{'title': d['title'], 'weight_percent_of_items': d['weight']} for d in data['blueprint']['domains']],
                'note': 'Known restricted-text check passed, not semantic redaction or arbitrary secret detection. Review public text before sharing; this is a guide, not an exam.'}
    require(audience == 'delivery', 'Unknown export audience')
    require(form_id is not None, 'Delivery export requires --form')
    result = check_form(data, form_id, evidence_root=evidence_root)
    require(result['checks_pass'], 'Form checks failed: ' + ', '.join(result['issues']))
    form, items = pinned_items(data, form_id)
    return {'classification': 'restricted', 'schema': 'certification-workshop-neutral-form-v1',
            'program_id': data['program']['id'], 'mode': data['program']['mode'], 'form': copy.deepcopy(form),
            'form_fingerprint': form_fingerprint(form, items), 'items': copy.deepcopy(items),
            'note': 'Neutral authoring handoff including keys/rubrics. Not a candidate-facing exam or verified provider import.'}


def reconcile_awards(data):
    validate(data)
    issues = []
    seen, receipts = {}, set()
    decisions = {d['id']: d for d in data['decisions']}
    for a in data['awards']:
        key = (a['candidate_id'], data['program']['id'], a['credential_version'])
        if key in seen:
            issues.append({'award_id': a['id'], 'code': 'duplicate_credential_intent'})
        seen[key] = a['id']
        decision = decisions.get(a['decision_id'])
        if not decision or decision['target_type'] != 'award' or decision['target_id'] != a['id'] or decision['revision'] != a.get('revision', 1) or decision['decision'] != 'approve' or decision.get('target_fingerprint') != award_fingerprint(a) or not decision_ok(data, 'award', a['id'], a.get('revision', 1), data['program']['mode'] == 'real', award_fingerprint(a)):
            issues.append({'award_id': a['id'], 'code': 'missing_award_authority'})
        action = a.get('action', 'issue')
        receipt = a.get('revocation_receipt') if action == 'revoke' else a.get('receipt')
        if (a['status'] == 'revoked' and action != 'revoke') or (a['status'] == 'issued' and action != 'issue'):
            issues.append({'award_id': a['id'], 'code': 'action_status_mismatch'})
        if data['program']['mode'] == 'real':
            needed = ('reason',) if action == 'revoke' else ('eligibility_evidence', 'result_evidence')
            if any(not text(a.get(key)) for key in needed):
                issues.append({'award_id': a['id'], 'code': 'missing_award_evidence'})
        if a['status'] in {'issued', 'revoked'} and not text(receipt):
            issues.append({'award_id': a['id'], 'code': 'missing_provider_receipt'})
        if a['status'] in {'submitted', 'unknown'}:
            issues.append({'award_id': a['id'], 'code': 'readback_before_retry'})
        if text(receipt):
            if receipt in receipts:
                issues.append({'award_id': a['id'], 'code': 'duplicate_receipt'})
            receipts.add(receipt)
    return {'reconciled': not issues, 'issues': issues, 'record_count': len(data['awards']),
            'note': 'Local reconciliation only; no provider queried, no credential issued, no retry authorized.'}


def status(data, evidence_root=None):
    validate(data)
    cov = coverage(data)
    issues = [{'item_id': i['id'], 'issues': item_issues(data, i)} for i in data['items'] if item_issues(data, i)]
    if not data['tasks']:
        next_action = 'Develop the charter, task hypotheses and SME instruments from the available sources.'
    elif not data['blueprint']['domains']:
        next_action = 'Map competencies into a proposed assessment blueprint with rationale.'
    elif not cov['ready_to_assemble']:
        next_action = 'Develop or review items to close the reported blueprint coverage gaps.'
    elif not data['forms']:
        next_action = 'Propose a form, review its constraints, and prepare the pilot protocol.'
    else:
        next_action = 'Review form checks and study evidence, then prepare the next authorized pilot, release or maintenance action.'
    gate_issues = evidence_gate(data, evidence_root)
    if gate_issues:
        next_action = 'Repair the local evidence-integrity gaps before assembly, restricted delivery or analysis; retain historical snapshots.'
    targets = {'program': program_approval_fingerprint(data), 'blueprint': blueprint_approval_fingerprint(data),
               'forms': {}, 'awards': {a['id']: award_fingerprint(a) for a in data['awards']}}
    for form in data['forms']:
        try:
            f, selected = pinned_items(data, form['id'])
            targets['forms'][form['id']] = form_approval_fingerprint(f, selected)
        except ValueError:
            targets['forms'][form['id']] = None
    return {'program_id': data['program']['id'], 'mode': data['program']['mode'], 'coverage': cov, 'item_issues': issues,
            'score_weighting': score_weighting(data),
            'evidence_gate_issues': gate_issues,
            'evidence_integrity': audit_evidence(data, evidence_root) if evidence_root is not None else
                {'checks_pass': None, 'issues': ['evidence_root_not_supplied'], 'note': 'No filesystem evidence was verified.'},
            'decision_target_fingerprints': targets,
            'forms': [check_form(data, f['id'], evidence_root=evidence_root) for f in data['forms']], 'next_action': next_action,
            'note': 'This summary is derived from records; read the decision register and owner context before acting.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--directory', required=True)
    init.add_argument('--id', required=True)
    init.add_argument('--title', required=True)
    init.add_argument('--mode', choices=['real', 'demo'], default='real')
    for cmd in ('validate', 'audit-evidence', 'audit-public', 'score-weights', 'status', 'coverage', 'assemble', 'check-form', 'review-packet', 'analyze', 'panel-summary', 'impact', 'export', 'reconcile-awards'):
        p = sub.add_parser(cmd)
        p.add_argument('--program', required=True)
        p.add_argument('--out', help='Write a new JSON output file; refuses overwrite')
        p.add_argument('--evidence-root', help='Project root for local evidence; defaults to the program file directory. No network access.')
        if cmd in {'assemble', 'check-form', 'analyze', 'panel-summary'}:
            p.add_argument('--form', required=True)
        elif cmd == 'score-weights':
            p.add_argument('--form', help='Inspect this exact pinned form instead of the whole bank')
        if cmd in {'coverage', 'assemble', 'check-form'}:
            p.add_argument('--live', action='store_true')
        if cmd in {'analyze', 'panel-summary'}:
            p.add_argument('--csv', required=True)
        if cmd == 'impact':
            p.add_argument('--source', action='append', required=True)
        if cmd == 'review-packet':
            p.add_argument('--item', action='append')
        if cmd == 'export':
            p.add_argument('--audience', choices=['candidate-guide', 'delivery'], required=True)
            p.add_argument('--form')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            result = initialize(args.directory, args.id, args.title, args.mode)
        else:
            d = load(args.program)
            c = args.command
            root = Path(args.evidence_root).resolve() if args.evidence_root else Path(args.program).resolve().parent
            if c == 'validate':
                result = validate(d)
                result['evidence_integrity'] = audit_evidence(d, root)
            elif c == 'audit-evidence': result = audit_evidence(d, root)
            elif c == 'audit-public':
                validate(d)
                issues = public_export_issues(d)
                result = {'checks_pass': not issues, 'issues': issues,
                          'note': 'Known restricted content only; no complete semantic or secret-detection guarantee.'}
            elif c == 'score-weights':
                validate(d)
                result = score_weighting(d, pinned_items(d, args.form)[1] if args.form else None)
            elif c == 'status': result = status(d, evidence_root=root)
            elif c == 'coverage': result = coverage(d, args.live)
            elif c == 'assemble': result = assemble(d, args.form, args.live, evidence_root=root)
            elif c == 'check-form': result = check_form(d, args.form, args.live, evidence_root=root)
            elif c == 'review-packet': result = review_packet(d, args.item)
            elif c == 'analyze': result = analyze(d, args.form, args.csv, evidence_root=root)
            elif c == 'panel-summary': result = panel_summary(d, args.form, args.csv, evidence_root=root)
            elif c == 'impact': result = impact(d, args.source)
            elif c == 'export': result = export(d, args.audience, args.form, evidence_root=root)
            elif c == 'reconcile-awards': result = reconcile_awards(d)
            if args.out:
                save_new(args.out, result)
        print(json.dumps(result, indent=2, allow_nan=False))
        if result.get('checks_pass') is False or result.get('assembled') is False or result.get('reconciled') is False:
            return 1
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
