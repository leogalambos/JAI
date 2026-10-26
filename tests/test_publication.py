# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""PDF publication routes through strict native conversion, never stale output."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import publication
import office_renderer


class PublicationPdfTests(unittest.TestCase):
    def setUp(self):
        self.model = {'title': 'Fixture <review>', 'artifact_id': 'FIXTURE-1',
            'owner': 'Fixture owner', 'audience': ['Fixture reviewer'], 'classification': 'Internal',
            'profile_id': 'fixture-profile', 'jai': {'intent_ref': 'intent:fixture',
                'semantic_snapshot_ref': 'snapshot:fixture', 'policy_ref': 'policy:fixture',
                'design_ref': 'design:fixture', 'realisation_ref': 'renderer:fixture', 'evidence_refs': []},
            'sections': [{'heading': 'Evidence', 'body': 'Substantive fixture content',
                          'bullets': ['One evidence item'], 'table': {'headers': ['Owner', 'State'],
                          'rows': [['Fixture owner', 'Pending']]}}]}
        self.theme = json.loads(publication.DEFAULT_THEME.read_text())

    def test_render_pdf_uses_actual_html_source_and_propagates_unavailable(self):
        model = {'title': 'Fixture', 'artifact_id': 'FIXTURE-1', 'owner': 'Fixture owner',
                 'audience': ['Fixture reviewer'], 'classification': 'Internal',
                 'sections': [{'heading': 'Evidence', 'body': 'Fixture content'}]}
        theme = json.loads(publication.DEFAULT_THEME.read_text())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'report.pdf'
            with patch.object(office_renderer, 'html_pdf', side_effect=office_renderer.RendererUnavailable('fixture denial')) as convert:
                with self.assertRaisesRegex(RuntimeError, 'fixture denial'):
                    publication.render_pdf(model, target, theme)
                self.assertFalse(target.exists())
                self.assertEqual(Path(convert.call_args.args[0]).suffix, '.html')

    def test_semantic_hash_and_xml_safety_preserve_meaning(self):
        first = publication.semantic_hash(self.model)
        self.assertEqual(first, publication.semantic_hash(dict(reversed(list(self.model.items())))))
        self.assertNotEqual(first, publication.semantic_hash(dict(self.model, owner='Different owner')))
        self.assertEqual(publication.clean_xml('a\x01b\t\n'), 'ab\t\n')
        self.assertEqual(publication.clean_xml(''), '')
        self.assertEqual(publication.esc('<&"'), '&lt;&amp;&quot;')
        self.assertIn(first, publication.markdown_text(self.model))
        self.assertEqual(publication.colname(0), '')
        self.assertEqual(publication.colname(26), 'Z')
        self.assertEqual(publication.colname(27), 'AA')
        self.assertNotIn('\x01', ElementTree.tostring(publication.docx_para('a\x01b', bold=True)).decode())

    def test_lineage_diagram_validation_and_real_native_outputs(self):
        self.assertEqual(publication.validate_native_jai(self.model), [])
        self.assertTrue(publication.validate_native_jai({}))
        wrong = dict(self.model, jai={'evidence_refs': 'wrong'})
        self.assertTrue(publication.validate_native_jai(wrong))
        diagram = {'title': 'Fixture flow', 'nodes': [{'id': 'one', 'label': 'Source'},
                    {'id': 'two', 'label': 'Evidence'}], 'edges': [{'from': 'one', 'to': 'two'}]}
        self.assertEqual(publication.validate_diagram(diagram), [])
        self.assertEqual(publication.diagram_lines(None),[])
        self.assertIn('one: Source',publication.diagram_lines(diagram))
        with self.assertRaises(ValueError):publication.diagram_lines({'nodes':[]})
        self.assertTrue(publication.validate_diagram({'title': 'Invalid', 'nodes': [], 'edges': [{'from': 'missing', 'to': 'missing'}]}))
        self.assertTrue(publication.validate_diagram({'title': 'Duplicate', 'nodes': [{'id': 'a', 'label': 'A'}, {'id': 'a', 'label': 'Other'}]}))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = [('html', publication.render_html), ('docx', publication.render_docx),
                       ('xlsx', publication.render_xlsx), ('svg', publication.render_svg)]
            for suffix, render in outputs:
                path = root / ('source.' + suffix)
                render(self.model, path, self.theme)
                self.assertGreater(path.stat().st_size, 100)
                self.assertEqual(publication.qa_file(path, self.theme)[0], [])
            with zipfile.ZipFile(root / 'source.docx') as archive:
                self.assertIn(publication.semantic_hash(self.model), archive.read('word/document.xml').decode())
            with zipfile.ZipFile(root / 'source.xlsx') as archive:
                self.assertTrue(any(name.startswith('xl/worksheets/') for name in archive.namelist()))
            svg = root / 'diagram.svg'
            publication.render_svg_diagram(diagram, svg, self.theme)
            ElementTree.parse(svg)
            with self.assertRaises(ValueError): publication.render_svg_diagram({}, svg, self.theme)
            ElementTree.fromstring(publication.slide_xml('Fixture title', ['One line', 'Boundary line']))
            self.assertEqual(publication.qa_file(root / 'missing.html', self.theme)[0], ['file missing'])
            broken = root / 'broken.docx'; broken.write_bytes(b'not a zip')
            self.assertTrue(publication.qa_file(broken, self.theme)[0])

    def test_verified_render_and_selftest_do_not_bypass_missing_evidence_or_renderer(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'draft.html'
            with self.assertRaises((ValueError, KeyError)):
                publication.render_verified(self.model, {}, directory, 'html', output, self.theme)
            self.assertFalse(output.exists())
        with patch.object(office_renderer, 'html_pdf', side_effect=office_renderer.RendererUnavailable('fixture unavailable')):
            with self.assertRaisesRegex(RuntimeError, 'fixture unavailable'): publication.self_test()


if __name__ == '__main__':
    unittest.main()
