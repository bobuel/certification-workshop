"""Create a new allowlisted public derivative; never edit original evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from package import INCLUDE, ROOT

HOME = re.compile(r'(?:[A-Za-z]:[\\/]+Users[\\/]+|/' + r'Users/|/' + r'home/)[^\\/\s"<>]+', re.I)
SECRET = re.compile(r'(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_\-]{20,})')
NOTICE = '''# Public export provenance

This is a sanitized derivative of the local release source. Workstation home prefixes in historical synthetic request files and native smoke-test artifacts were replaced with <workspace-user>. No private employer materials, candidate records or credentials belong in this repository.

PUBLIC_EXPORT.json lists each distributed file's original and public SHA-256. Historical grades and receipts bind the original artifacts; they are retained as historical observations, not reissued grades of sanitized or edited content. The separate owner-review example is an unpiloted author revision. Source originals were not modified by export.

The ledger excludes itself and this notice. It is a publication snapshot, not a lockfile for future contributions. The scanner checks common credential markers and home paths; human review of provenance and content remains necessary. Run python scripts/public_export.py --check . before publication. Rebuild from the private source if sanitization needs changes; do not hand-edit historical grades.
'''


def selected(root):
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if rel.parts[0] not in INCLUDE or '__pycache__' in rel.parts or path.suffix == '.pyc':
            continue
        if path.is_symlink():
            raise ValueError(f'Symlink in distribution: {rel.as_posix()}')
        if path.is_file() and rel.as_posix() not in {'PUBLIC_EXPORT.json', 'PUBLIC_EXPORT.md'}:
            yield path, rel


def scan(data):
    text = data.decode('utf-8')
    issues = []
    if HOME.search(text):
        issues.append('personal-home-path')
    if SECRET.search(text):
        issues.append('credential-marker')
    return issues


def check(root):
    issues = []
    for path, rel in selected(root):
        try:
            categories = scan(path.read_bytes())
        except UnicodeDecodeError:
            categories = ['unreviewed-binary']
        issues.extend({'file': rel.as_posix(), 'category': c} for c in categories)
    return issues


def export(root, destination):
    root, destination = root.resolve(), destination.resolve()
    if destination.exists() or destination.is_relative_to(root) or root.is_relative_to(destination):
        raise ValueError('Destination must be new and outside the source tree')
    prepared, entries = [], []
    for path, rel in selected(root):
        original = path.read_bytes()
        content = HOME.sub('<workspace-user>', original.decode('utf-8')).encode('utf-8')
        if scan(content):
            raise ValueError(f'Publication scan failed: {rel.as_posix()}')
        if path.suffix == '.json':
            json.loads(content)  # Redaction must preserve valid structured files.
        prepared.append((rel, content))
        entries.append({'path': rel.as_posix(), 'original_sha256': hashlib.sha256(original).hexdigest(),
                        'public_sha256': hashlib.sha256(content).hexdigest(), 'sanitized': content != original})
    destination.mkdir(parents=True)
    for rel, content in prepared:
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    ledger = {'schema_version': 1, 'meaning': 'Publication derivative; historical receipts bind original_sha256.', 'files': entries}
    (destination / 'PUBLIC_EXPORT.json').write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')
    (destination / 'PUBLIC_EXPORT.md').write_text(NOTICE, encoding='utf-8')
    return {'files': len(entries), 'sanitized_files': [e['path'] for e in entries if e['sanitized']]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--destination', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    try:
        result = check(args.check) if args.check else export(args.source, args.destination)
        print(json.dumps(result, indent=2))
        if args.check and result:
            sys.exit(1)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
