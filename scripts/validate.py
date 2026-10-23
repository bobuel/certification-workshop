"""Validate package identity, skill references and bundled program examples."""
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate_package(root=ROOT):
    manifest = json.loads((root / 'plugin.json').read_text(encoding='utf-8'))
    assert manifest['name'] == 'certification-workshop'
    for file in ('.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
        overlay = json.loads((root / file).read_text(encoding='utf-8'))
        assert all(overlay[k] == manifest[k] for k in ('name', 'version', 'description'))
    interface = manifest['extensions']['com.openai']['interface']
    assert interface == json.loads((root / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))['interface']
    assert (root / manifest['extensions']['com.openai']['onboardingSkill']).is_file()
    for key in ('composerIcon', 'logo'):
        assert (root / interface[key]).is_file()
    skills = sorted((root / 'skills').glob('*/SKILL.md'))
    assert len(skills) == 10
    for path in skills:
        content = path.read_text(encoding='utf-8')
        assert content.startswith('---\n') and '\n---\n' in content[4:]
        assert f'name: {path.parent.name}\n' in content and 'description: ' in content
        metadata = (path.parent / 'agents/openai.yaml').read_text(encoding='utf-8')
        assert '$' + path.parent.name in metadata
    for path in (root / 'skills').rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#'):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            assert target.is_relative_to((root / 'skills').resolve()) and target.exists(), f'Broken portable reference: {path} -> {link}'
    script = root / 'skills/certification-workshop/scripts/certification.py'
    spec = importlib.util.spec_from_file_location('package_certification', script)
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    examples = list((root / 'examples').rglob('*program.json'))
    for example in examples:
        c.validate(c.load(example))
    return {'valid': True, 'skills': len(skills), 'program_examples': len(examples), 'version': manifest['version']}


if __name__ == '__main__':
    try:
        print(json.dumps(validate_package(), indent=2))
    except (AssertionError, ValueError, OSError, KeyError) as e:
        print(f'Package validation failed: {e}', file=sys.stderr)
        sys.exit(1)
