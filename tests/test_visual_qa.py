# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Transparent SVGs are judged as visible paper pixels without relaxed thresholds."""
from pathlib import Path
import sys
import tempfile
import unittest
import io
import contextlib
from unittest.mock import patch
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import visual_qa


class VisualQaTests(unittest.TestCase):
    def test_transparent_paper_canvas_does_not_create_false_edge_clipping(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rectangle((40, 100, 760, 550), outline='black', width=3)
            draw.text((40, 60), 'Architecture evidence', fill='black')
            path = Path(directory) / 'transparent.png'; image.save(path)
            self.assertFalse(any(severity == 'critical' for _, severity, _ in visual_qa.image_findings(path)))

    def test_transparent_blank_is_blank_and_real_opaque_clipping_stays_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'blank.png'
            Image.new('RGBA', (800, 600), (0, 0, 0, 0)).save(path)
            self.assertIn('blank', {code for code, _, _ in visual_qa.image_findings(path)})
            visual_qa.make_seed(path, 'edge-clipping', False)
            self.assertIn('edge-clipping', {code for code, _, _ in visual_qa.image_findings(path)})

    def test_explicit_renderer_command_reports_success_and_failure(self):
        result = visual_qa.run([sys.executable, '-c', 'print("fixture")'])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), 'fixture')
        self.assertEqual(visual_qa.run([sys.executable, '-c', 'raise SystemExit(7)']).returncode, 7)
        with self.assertRaises(OSError): visual_qa.run(['/missing/fixture-renderer'])

    def test_source_checks_native_svg_and_failed_pdf_are_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            svg = root / 'good.svg'
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><text x="40" y="70">Architecture</text><rect x="40" y="100" width="700" height="450" fill="none" stroke="black"/></svg>')
            self.assertEqual(visual_qa.source_findings(svg), [])
            pages = visual_qa.render_to_images(svg, root / 'pages')
            self.assertTrue(pages[0].is_file())
            self.assertFalse(any(severity == 'critical' for _, severity, _ in visual_qa.qa(svg, root / 'kept')))
            html = root / 'bad.html'; html.write_text('<p>Missing controls</p>')
            self.assertIn('document-control', {code for code, _, _ in visual_qa.source_findings(html)})
            text = root / 'unsupported.txt'; text.write_text('fixture')
            with self.assertRaises(ValueError): visual_qa.render_to_images(text, root / 'unsupported')
            self.assertIn('render-failed', {code for code, _, _ in visual_qa.qa(text)})
            with self.assertRaises(RuntimeError): visual_qa.pdf_pages(root / 'missing.pdf', root / 'missing-pages')

    def test_native_render_failure_keeps_selftest_nonpassing(self):
        from office_renderer import RendererUnavailable
        sources=[]
        def unavailable(source,*args,**kwargs):
            sources.append(Path(source).read_text())
            raise RendererUnavailable('fixture prerequisite denied')
        with patch.object(visual_qa, 'html_pdf', side_effect=unavailable), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(visual_qa.self_test(), 1)
        self.assertEqual(len(sources),1)
        self.assertIn('Decision scope',sources[0])
        self.assertIn('Options and evidence',sources[0])
        self.assertIn('<table',sources[0])
        self.assertIn('FAIL html-render', output.getvalue())
        self.assertIn('PASS svg-render', output.getvalue())


if __name__ == '__main__':
    unittest.main()
