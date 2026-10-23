"""Build an allowlisted reproducible archive and SHA-256 digest."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = {'plugin.json', '.codex-plugin', '.claude-plugin', '.agents', '.github', 'skills', 'assets', 'docs', 'examples',
           'scripts', 'tests', 'evals', 'README.md', 'LICENSE', 'NOTICE.md', 'PRIVACY.md', 'AGENTS.md',
           'requirements.txt', '.gitignore', '.gitattributes', 'SECURITY.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
           'PUBLIC_EXPORT.md', 'PUBLIC_EXPORT.json'}


def build(root=ROOT):
    manifest = json.loads((root / 'plugin.json').read_text(encoding='utf-8'))
    output = root / 'dist' / f"{manifest['name']}-{manifest['version']}.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob('*'), key=lambda p: p.relative_to(root).as_posix()):
            relative = path.relative_to(root)
            if relative.parts[0] not in INCLUDE or '__pycache__' in relative.parts or path.suffix == '.pyc':
                continue
            if not path.is_file() or path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root.parent):
                continue
            info = zipfile.ZipInfo('certification-workshop/' + relative.as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    sha = hashlib.sha256(output.read_bytes()).hexdigest()
    (output.parent / 'SHA256SUMS').write_text(f'{sha}  {output.name}\n', encoding='utf-8')
    return output, sha


if __name__ == '__main__':
    output, sha = build()
    print(json.dumps({'archive': str(output), 'sha256': sha}, indent=2))
