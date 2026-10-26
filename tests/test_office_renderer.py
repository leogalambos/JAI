# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Strict renderer prerequisites and isolated conversion, not host qualification."""
import errno
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import office_renderer as renderer


class OfficeRendererTests(unittest.TestCase):
    def test_svg_and_html_resources_fail_closed_without_relaxing_visual_rules(self):
        import importlib.util
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);svg=root/'diagram.svg'
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="file:///unapproved"/></svg>')
            with self.assertRaises(ValueError):renderer.validate_svg(svg)
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>Safe</text></svg>')
            self.assertTrue(renderer.validate_svg(svg))
            if importlib.util.find_spec('weasyprint') is None:return
            html=root/'source.html';html.write_text('<html><h1>Safe local PDF</h1><p>Classification: public synthetic</p></html>')
            self.assertTrue(renderer.html_pdf(html,root/'safe',backend='weasyprint').read_bytes().startswith(b'%PDF-'))
            for unsafe in ('<img src="file:///unapproved">','<img src="https://example.invalid/image.png">','<style>@font-face {font-family:x;src:url(file:///font)}</style>'):
                html.write_text('<html><h1>Resource denial</h1>'+unsafe+'</html>')
                with self.assertRaises(ValueError):renderer.html_pdf(html,root/'unsafe',backend='weasyprint')
                self.assertFalse((root/'unsafe/source.pdf').exists())

    def test_denied_unix_ipc_is_explicit_and_does_not_start_converter(self):
        with patch.object(renderer.sys, 'platform', 'linux'), patch.object(
                renderer.socket, 'socket', side_effect=PermissionError(errno.EPERM, 'denied')):
            result = renderer.prerequisites()
            self.assertFalse(result['available'])
            self.assertEqual(result['reason'], 'AF_UNIX_IPC_DENIED')
            self.assertEqual(result['errno'], errno.EPERM)
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / 'source.html'; source.write_text('<h1>Fixture</h1>')
                with patch.object(renderer.subprocess, 'run') as run, self.assertRaisesRegex(
                        renderer.RendererUnavailable, 'AF_UNIX_IPC_DENIED'):
                    renderer.convert_office(source, Path(directory) / 'out', executable='/usr/bin/libreoffice')
                run.assert_not_called()

    def test_empty_stderr_retains_exit_and_bounded_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.html'; source.write_text('<h1>Fixture</h1>')
            with patch.object(renderer, 'prerequisites', return_value={'available': True}), patch.object(
                    renderer.subprocess, 'run', return_value=subprocess.CompletedProcess([], 17, 'diagnostic\x1b', '')):
                with self.assertRaisesRegex(RuntimeError, 'exit=17') as error:
                    renderer.convert_office(source, Path(directory) / 'out', executable='/usr/bin/libreoffice')
                self.assertIn('diagnostic', str(error.exception))
                self.assertNotIn('\x1b', str(error.exception))

    def test_each_conversion_uses_private_profile_and_validates_fresh_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'source.html'; source.write_text('<h1>Fixture</h1>')
            commands = []
            def convert(command, **kwargs):
                commands.append((command, kwargs))
                out = Path(command[command.index('--outdir') + 1])
                (out / 'source.pdf').write_bytes(b'%PDF-1.4\nfixture')
                return subprocess.CompletedProcess(command, 0, '', '')
            with patch.object(renderer, 'prerequisites', return_value={'available': True}), patch.object(
                    renderer.subprocess, 'run', side_effect=convert), patch.dict(renderer.os.environ, {'TOKEN': 'fixture-only'}):
                first = renderer.convert_office(source, root / 'out', executable='/usr/bin/libreoffice')
                self.assertEqual(first.read_bytes(), b'%PDF-1.4\nfixture')
                renderer.convert_office(source, root / 'out', executable='/usr/bin/libreoffice')
            self.assertNotEqual(commands[0][0][1], commands[1][0][1])
            self.assertNotIn('TOKEN', commands[0][1]['env'])
            self.assertIn('-env:UserInstallation=file:', commands[0][0][1])
            self.assertEqual(commands[0][1]['timeout'], 90)

    def test_missing_or_invalid_result_and_timeout_never_accept_stale_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'source.html'; source.write_text('Fixture')
            out = root / 'out'; out.mkdir(); (out / 'source.pdf').write_bytes(b'%PDF-stale')
            for child in (subprocess.CompletedProcess([], 0, '', ''), subprocess.TimeoutExpired('fixture', 1)):
                with self.subTest(child=type(child).__name__), patch.object(renderer, 'prerequisites', return_value={'available': True}), patch.object(renderer.subprocess, 'run', side_effect=child if isinstance(child, Exception) else None, return_value=child):
                    with self.assertRaises((RuntimeError, subprocess.TimeoutExpired)):
                        renderer.convert_office(source, out, executable='/usr/bin/libreoffice')
                    self.assertEqual((out / 'source.pdf').read_bytes(), b'%PDF-stale')
            with self.assertRaises(ValueError): renderer.convert_office(source, out, timeout=0)


if __name__ == '__main__':
    unittest.main()
