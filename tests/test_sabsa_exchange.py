# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""CSV exchange and real document integration coverage."""
import csv
import contextlib
import io
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
import zipfile
import xml.etree.ElementTree as ET

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import sabsa
import sabsa_exchange as exchange


class SabsaExchangeTest(unittest.TestCase):
    def test_catalogue_schema_and_deterministic_roundtrip(self):
        entries = {'BD-001': {'id': 'BD-001', 'title': 'Café, "title"', '_dirtype': 'driver'}}
        with tempfile.TemporaryDirectory() as directory:
            exchange.export_catalogues(entries, sabsa.TYPES, directory)
            original = (Path(directory) / 'driver.csv').read_bytes()
            self.assertEqual(exchange.read_catalogues(directory, sabsa.TYPES, entries)['BD-001']['title'], 'Café, "title"')
            exchange.export_catalogues(entries, sabsa.TYPES, directory)
            self.assertEqual(original, (Path(directory) / 'driver.csv').read_bytes())
            (Path(directory) / 'driver.csv').write_text('id,title\nx,y\n')
            with self.assertRaisesRegex(ValueError, 'columns'):
                exchange.read_catalogues(directory, sabsa.TYPES, entries)

    def test_empty_catalogues_and_duplicate_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            exchange.export_catalogues({}, sabsa.TYPES, directory)
            self.assertEqual({}, exchange.read_catalogues(directory, sabsa.TYPES, {}))
            schema = exchange.catalogue_schema(sabsa.TYPES)
            self.assertEqual('1', schema['schema_version'])
            with (Path(directory) / 'driver.csv').open('a') as stream:
                stream.write('new' + ',' * (len(schema['types']['driver']) - 1) + '\n')
            with self.assertRaisesRegex(ValueError, 'nonlocal ID'):
                exchange.read_catalogues(directory, sabsa.TYPES, {})

    def test_catalogue_cli_import_validation_and_rollback_integration(self):
        with tempfile.TemporaryDirectory() as directory:
            lib = Path(directory) / 'lib'
            csvdir = Path(directory) / 'csv'
            tool = TOOLS / 'sabsa.py'
            def run(*args):
                return subprocess.run([sys.executable, str(tool), *map(str, args)], capture_output=True, text=True)
            self.assertEqual(0, run('init', lib, '--name', 'Test', '--organisation', 'Example', '--scope', 'Scope', '--owner', 'Owner').returncode)
            (lib / '00-sources/brief.md').write_text('Client statement')
            self.assertEqual(0, run('new', lib, 'driver', '--title', 'Original', '--set', 'statement=Business reason', '--set', 'owner=Owner', '--set', 'basis=stated', '--set', 'source=00-sources/brief.md').returncode)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(0, sabsa.cmd_catalogues(Namespace(lib=str(lib), action='export', directory=str(csvdir))))
            self.assertEqual(output.getvalue().strip(), f'CSV catalogue export: {csvdir}')
            path = csvdir / 'driver.csv'
            with path.open(newline='') as stream:
                reader = csv.DictReader(stream); columns = reader.fieldnames; rows = list(reader)
            rows[0]['title'] = 'Edited café title'
            with path.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=columns); writer.writeheader(); writer.writerows(rows)
            source = next((lib / '01-contextual/drivers').glob('*.md'))
            before = source.read_bytes()
            result = run('catalogues', lib, 'validate', '--directory', csvdir)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(before, source.read_bytes())
            result = run('catalogues', lib, 'import', '--directory', csvdir)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('Edited café title', source.read_text())
            original = source.read_bytes()
            rows[0]['id'] = 'BD-999'
            with path.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=columns); writer.writeheader(); writer.writerows(rows)
            self.assertNotEqual(0, run('catalogues', lib, 'import', '--directory', csvdir).returncode)
            self.assertEqual(original, source.read_bytes())

    def test_layer_documents_cover_each_matrix_level(self):
        with tempfile.TemporaryDirectory() as directory:
            lib = Path(directory) / 'lib'
            subprocess.run([sys.executable, str(TOOLS / 'sabsa.py'), 'init', str(lib), '--name', 'Test', '--organisation', 'Org', '--scope', 'Scope', '--owner', 'Owner'], check=True, capture_output=True)
            for layer in sabsa.LAYER_KEYS + ['operational']:
                out = Path(directory) / (layer + '.md')
                args = type('Args', (), dict(lib=str(lib), layer=layer, out=str(out), template=None, template_name='architecture'))()
                result = subprocess.run([sys.executable, str(TOOLS / 'sabsa.py'), 'document', str(lib), '--layer', layer, '--out', str(out)], capture_output=True)
                self.assertEqual(0, result.returncode, result.stderr)
                text = out.read_text()
                self.assertIn('Architecture specifications and design rationale', text)
                self.assertEqual(6, text.count('Status: open'))
            args.layer = 'logical'; args.template_name = 'trust-model'
            with self.assertRaises(sabsa.SabsaError): sabsa.cmd_document(args)

    @unittest.skipUnless(shutil.which('pandoc'), 'pandoc required')
    def test_document_tex_escaping_and_docx_layout_integration(self):
        with tempfile.TemporaryDirectory() as directory:
            lib = Path(directory) / 'lib'
            tool = TOOLS / 'sabsa.py'
            subprocess.run([sys.executable, str(tool), 'init', str(lib), '--name', r'Café architecture & 100% _ \ input', '--organisation', 'Example', '--scope', 'Test', '--owner', 'Owner'], check=True, capture_output=True)
            for extension in ('tex', 'docx'):
                dest = Path(directory) / ('out.' + extension)
                subprocess.run([sys.executable, str(tool), 'document', str(lib), '--out', str(dest)], check=True, capture_output=True)
                self.assertTrue(dest.is_file())
                if extension == 'tex':
                    text = dest.read_text()
                    self.assertIn('Café architecture', text)
                    self.assertIn(r'\&', text)
                    self.assertIn(r'100\%', text)
                    self.assertIn(r'\_', text)
                    self.assertIn('DRAFT / NOT APPROVED', text)
                else:
                    exchange.format_docx(dest)
                    exchange.format_narrative_docx(dest, dict(title='Example', viewpoint='Logical Security Architecture', organisation='Example Org', owner='Owner', version='1', scope='Test', approval='DRAFT'))
                    with zipfile.ZipFile(dest) as archive:
                        document = ET.fromstring(archive.read('word/document.xml'))
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    self.assertTrue(document.findall('.//w:gridCol', ns))
                    self.assertIn('Logical Security Architecture', ''.join(document.itertext()))
                    self.assertIn('Contents', ''.join(document.itertext()))
                    for table in document.findall('.//w:tbl', ns):
                        tags = [child.tag.rsplit('}', 1)[-1] for child in table]
                        self.assertLess(tags.index('tblGrid'), tags.index('tr'))
                    self.assertTrue(document.findall('.//w:pgSz[@w:orient="landscape"]', ns))


if __name__ == '__main__':
    unittest.main()
