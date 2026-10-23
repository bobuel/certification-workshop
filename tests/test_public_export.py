import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from public_export import check, export


class PublicExportTests(unittest.TestCase):
    def test_redaction_preserves_original_and_structured_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            original = json.dumps({'source': 'C:' + '\\' + 'Users' + '\\' + 'private-person' + '\\' + 'case.md'}).encode()
            (source / 'plugin.json').write_bytes(original)
            target = Path(tmp) / 'public'
            result = export(source, target)
            self.assertEqual(result['sanitized_files'], ['plugin.json'])
            self.assertEqual((source / 'plugin.json').read_bytes(), original)
            content = (target / 'plugin.json').read_bytes()
            self.assertNotIn('private-person', json.loads(content)['source'])
            row = json.loads((target / 'PUBLIC_EXPORT.json').read_text())['files'][0]
            self.assertEqual(row['original_sha256'], hashlib.sha256(original).hexdigest())
            self.assertEqual(row['public_sha256'], hashlib.sha256(content).hexdigest())
            self.assertEqual(check(target), [])

    def test_credential_fails_before_destination_is_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            (source / 'README.md').write_text('gh' + 'p_' + 'a' * 30)
            target = Path(tmp) / 'public'
            with self.assertRaises(ValueError):
                export(source, target)
            self.assertFalse(target.exists())

    def test_existing_or_nested_destination_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            for target in (source, source / 'nested'):
                with self.assertRaises(ValueError):
                    export(source, target)

    def test_non_allowlisted_files_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            (source / '.env').write_text('private')
            (source / 'README.md').write_text('public')
            target = Path(tmp) / 'public'
            export(source, target)
            self.assertFalse((target / '.env').exists())
            self.assertEqual((target / 'README.md').read_text(), 'public')
