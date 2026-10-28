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
    def setUp(self):
        # These existing tests exercise the current-Python fallback in isolation.
        cli = patch.object(renderer, '_html_pdf_cli', side_effect=renderer.RendererUnavailable('CLI absent'))
        cli.start()
        self.addCleanup(cli.stop)

    def test_auto_rechecks_backend_versions_and_preserves_explicit_selection(self):
        import importlib.metadata
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'source.html';source.write_text('<h1>Local</h1>')
            for version in ('69.0', importlib.metadata.PackageNotFoundError('weasyprint')):
                with patch.object(importlib.metadata,'version',side_effect=version if isinstance(version,Exception) else None,return_value=version), patch.object(renderer,'convert_office',return_value=root/'native.pdf') as native:
                    self.assertEqual(renderer.html_pdf(source,root/'out'),root/'native.pdf')
                    native.assert_called_once()
            with patch.object(renderer,'convert_office',return_value=root/'explicit.pdf') as native:
                self.assertEqual(renderer.html_pdf(source,root/'out',backend='libreoffice'),root/'explicit.pdf')
                native.assert_called_once()
            with patch.object(importlib.metadata,'version',return_value='70.0'), patch.dict(sys.modules,{'weasyprint':None}), patch.object(renderer,'convert_office',return_value=root/'fallback.pdf'):
                self.assertEqual(renderer.html_pdf(source,root/'out'),root/'fallback.pdf')
                with self.assertRaises(renderer.RendererUnavailable):
                    renderer.html_pdf(source,root/'out',backend='weasyprint')

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
            for unsafe in ('<img src="file:///unapproved">','<img src="relative.png">','<style>body{background:url(relative.png)}</style>','<img src="https://example.invalid/image.png">','<style>@font-face {font-family:x;src:url(file:///font)}</style>'):
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


def test_successful_local_render_does_not_require_pyphen_metadata(tmp_path):
    import importlib.metadata
    import json
    original = importlib.metadata.version
    def version(name):
        if name == 'pyphen':raise importlib.metadata.PackageNotFoundError(name)
        return original(name)
    source=tmp_path/'source.html';source.write_text('<h1>Safe local fixture</h1>')
    with patch.object(importlib.metadata,'version',side_effect=version), patch.object(renderer,'_html_pdf_cli',side_effect=renderer.RendererUnavailable('CLI absent')):
        pdf=renderer.html_pdf(source,tmp_path/'out',backend='weasyprint')
    assert pdf.read_bytes().startswith(b'%PDF-')
    assert json.loads(pdf.with_suffix('.renderer.json').read_text())['pyphen']=='metadata unavailable'


def test_cli_first_renders_without_importing_current_python_packages(tmp_path):
    import json
    source=tmp_path/'source.html';source.write_text('<h1>Safe CLI fixture</h1>')
    with patch.object(renderer,'_html_pdf_local',side_effect=AssertionError('must not import caller packages')):
        pdf=renderer.html_pdf(source,tmp_path/'out',backend='weasyprint')
    evidence=json.loads(pdf.with_suffix('.renderer.json').read_text())
    assert pdf.read_bytes().startswith(b'%PDF-')
    assert evidence['execution']=='cli'
    assert evidence['executable']
    assert evidence['python'] is None and evidence['pyphen'] is None


def test_cli_denied_resources_never_fall_back_to_python_or_office(tmp_path):
    source=tmp_path/'source.html'
    for unsafe in ('<img src="file:///unapproved">','<img src="https://example.invalid/image.png">','<img src="relative.png">','<style>body{background:url(relative.png)}</style>','<style>@import "https://example.invalid/x.css";</style>','<style>@font-face{font-family:x;src:url(file:///font)}</style>'):
        source.write_text(unsafe)
        with patch.object(renderer,'_html_pdf_local',side_effect=AssertionError('no weaker fallback')), patch.object(renderer,'convert_office',side_effect=AssertionError('no Office fallback')), unittest.TestCase().assertRaises(ValueError):
            renderer.html_pdf(source,tmp_path/'out',backend='auto')
        assert not (tmp_path/'out/source.pdf').exists()


def test_unavailable_cli_version_falls_back_to_current_python(tmp_path):
    source=tmp_path/'source.html';source.write_text('<h1>Local</h1>')
    for probe in (subprocess.TimeoutExpired('version',10), FileNotFoundError('missing'), subprocess.CompletedProcess([],1,'','startup failure'), subprocess.CompletedProcess([],0,'WeasyPrint version 69.0',''), subprocess.CompletedProcess([],0,'malformed version',''), subprocess.CompletedProcess([],0,'WeasyPrint version 700.0','')):
        with patch.object(renderer.shutil,'which',return_value='/fixture/weasyprint'), patch.object(renderer.subprocess,'run',side_effect=probe if isinstance(probe,Exception) else None,return_value=probe), patch.object(renderer,'_html_pdf_local',return_value=tmp_path/'local.pdf') as local:
            assert renderer.html_pdf(source,tmp_path/'out',backend='weasyprint')==tmp_path/'local.pdf'
            local.assert_called_once()
    with patch.object(renderer.shutil,'which',return_value=None), patch.object(renderer,'_html_pdf_local',return_value=tmp_path/'local.pdf'):
        assert renderer.html_pdf(source,tmp_path/'out')==tmp_path/'local.pdf'


def test_cli_conversion_errors_do_not_fall_back_or_accept_stale_pdf(tmp_path):
    source=tmp_path/'source.html';source.write_text('<h1>Local</h1>')
    out=tmp_path/'out';out.mkdir();pdf=out/'source.pdf';pdf.write_bytes(b'%PDF-stale')
    version=subprocess.CompletedProcess([],0,'WeasyPrint version 70.0','')
    for conversion in (subprocess.TimeoutExpired('conversion',20), subprocess.CompletedProcess([],2,'','render failure'), subprocess.CompletedProcess([],0,'','no PDF')):
        with patch.object(renderer.shutil,'which',return_value='/fixture/weasyprint'), patch.object(renderer.subprocess,'run',side_effect=[version,conversion]), patch.object(renderer,'_html_pdf_local',side_effect=AssertionError('no fallback')), unittest.TestCase().assertRaises(RuntimeError):
            renderer.html_pdf(source,out,backend='auto')
        assert pdf.read_bytes()==b'%PDF-stale'
    with patch.object(renderer,'_html_pdf_cli') as cli, patch.object(renderer,'convert_office',return_value=pdf):
        assert renderer.html_pdf(source,out,backend='libreoffice')==pdf
        cli.assert_not_called()


def test_cli_timeout_preserves_partial_output(tmp_path):
    source=tmp_path/'source.html';source.write_text('<h1>Local</h1>')
    version=subprocess.CompletedProcess([],0,'WeasyPrint version 70.0','')
    timeout=subprocess.TimeoutExpired('fixture',20,output=b'partial stdout',stderr=b'native library pending')
    for results in ([timeout],[version,timeout]):
        with patch.object(renderer.shutil,'which',return_value='/fixture/weasyprint'), patch.object(renderer.subprocess,'run',side_effect=results), unittest.TestCase().assertRaises(RuntimeError) as error:
            renderer._html_pdf_cli(source,tmp_path/'out')
        assert 'partial stdout' in str(error.exception)
        assert 'native library pending' in str(error.exception)
