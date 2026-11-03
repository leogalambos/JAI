#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""CI dependency drift regression: validation and release share one environment."""
from contextlib import ExitStack
import importlib.util
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from PIL import Image
import cairosvg

import yaml

ROOT = Path(__file__).resolve().parents[1]
ACTION = ROOT / '.github/actions/setup-qualification/action.yml'
MANIFEST = ROOT / 'ci/system-packages.txt'
PYTHON_REQUIREMENTS = ROOT / 'requirements-ci.txt'
SPEC = importlib.util.spec_from_file_location('ci_environment_contract', ROOT / 'scripts/check_ci_environment.py')
environment = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(environment)


class CIEnvironmentContract(unittest.TestCase):
    def test_both_qualification_workflows_share_composite_action(self):
        for filename in ('validate-library.yml', 'release.yml'):
            with self.subTest(filename=filename):
                text = (ROOT / '.github/workflows' / filename).read_text()
                self.assertIn('uses: ./.github/actions/setup-qualification', text)
                workflow = yaml.load(text, Loader=yaml.BaseLoader)
                full_job = workflow['jobs'].get('qualification', workflow['jobs'].get('release-preflight'))
                self.assertNotIn('pip install --disable-pip-version-check', yaml.dump(full_job))
                self.assertNotIn('sudo apt-get install', text)
                self.assertIn('jai-ci-environment', text)

    def test_pages_use_same_python_manifest(self):
        pages = (ROOT / '.github/workflows/pages.yml').read_text()
        self.assertIn('-r requirements-ci.txt', pages)
        self.assertIn("- 'requirements-ci.txt'", pages)

    def test_python_dependencies_are_canonical(self):
        text = PYTHON_REQUIREMENTS.read_text()
        self.assertIn('-r requirements.txt', text)
        for package in ('jsonschema', 'lxml', 'Pillow', 'CairoSVG', 'mistune'):
            self.assertRegex(text, rf'(?m)^{package}==\d')

    def test_system_dependencies_are_declared(self):
        packages = {row.strip() for row in MANIFEST.read_text().splitlines()
                    if row.strip() and not row.startswith('#')}
        self.assertTrue({'libreoffice-writer', 'libreoffice-calc',
                         'libreoffice-impress', 'poppler-utils', 'libcairo2'} <= packages)
        action = ACTION.read_text()
        self.assertIn('ci/system-packages.txt', action)
        self.assertIn('requirements-ci.txt', action)
        self.assertIn('scripts/check_ci_environment.py', action)
        self.assertIn('python3 -m pip check', action)

    def _renderer_report(self, failure=None):
        calls = []
        png = io.BytesIO()
        Image.new('RGB', (4, 4), 'black').save(png, format='PNG')
        png_bytes = png.getvalue()

        def render(command, timeout=45):
            calls.append(command)
            if '--version' in command:
                return subprocess.CompletedProcess(command, 0, stdout='LibreOffice fixture', stderr='')
            if '-v' in command:
                return subprocess.CompletedProcess(command, 0, stdout='', stderr='pdftoppm fixture')
            if command[0] == 'libreoffice':
                if failure == 'conversion':
                    raise subprocess.CalledProcessError(1, command)
                if failure == 'timeout':
                    raise subprocess.TimeoutExpired(command, timeout)
                if failure != 'missing_pdf':
                    output = Path(command[command.index('--outdir') + 1]) / 'smoke.pdf'
                    output.write_bytes(b'%PDF-' if failure == 'short_pdf' else b'%PDF-' + b'x' * 100)
            elif command[0] == 'pdftoppm':
                if failure != 'missing_png':
                    Path(command[-1] + '.png').write_bytes(b'invalid image' if failure == 'invalid_png' else png_bytes)
            else:
                raise AssertionError(command)
            return subprocess.CompletedProcess(command, 0, stdout='', stderr='')

        # These tests isolate renderer execution from package installation and host versions.
        # Raster files still cross the real filesystem and Pillow decoding boundary.
        with ExitStack() as stack:
            stack.enter_context(patch.object(environment.sys, 'version_info', (3, 12)))
            stack.enter_context(patch.object(environment, 'PYTHON_DEPENDENCIES', {}))
            stack.enter_context(patch.object(environment.shutil, 'which',
                side_effect=lambda name: None if failure == 'missing_executable' and name == 'libreoffice' else '/fixture/' + name))
            stack.enter_context(patch.object(environment, 'run', side_effect=render))
            svg = stack.enter_context(patch.object(cairosvg, 'svg2png',
                return_value=b'invalid image' if failure == 'invalid_svg_png' else png_bytes))
            result = environment.verify()
        return result, calls, svg

    def test_environment_gate_executes_each_renderer_and_decodes_outputs(self):
        result, calls, svg = self._renderer_report()
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['smoke_tests'], {
            'office_to_pdf': 'PASS', 'pdf_rasterisation': 'PASS', 'svg_rasterisation': 'PASS'})
        self.assertEqual([command[0] for command in calls],
                         ['libreoffice', 'pdftoppm', 'libreoffice', 'pdftoppm'])
        self.assertIn('--convert-to', calls[2])
        self.assertEqual(calls[2][calls[2].index('--convert-to') + 1], 'pdf')
        self.assertIn('-png', calls[3])
        svg.assert_called_once()
        self.assertIn(b'<svg', svg.call_args.kwargs['bytestring'])

    def test_environment_gate_never_promotes_missing_or_failed_rendering(self):
        cases = {
            'missing_executable': {}, 'conversion': {}, 'timeout': {},
            'missing_pdf': {}, 'short_pdf': {},
            'missing_png': {'office_to_pdf': 'PASS'},
            'invalid_png': {'office_to_pdf': 'PASS'},
            'invalid_svg_png': {'office_to_pdf': 'PASS', 'pdf_rasterisation': 'PASS'},
        }
        for failure, expected_smoke in cases.items():
            with self.subTest(failure=failure):
                result, calls, svg = self._renderer_report(failure)
                self.assertEqual(result['smoke_tests'], expected_smoke)
                self.assertEqual(len(result['errors']), 1)
                if failure == 'missing_executable':
                    self.assertEqual(result['errors'], ['System executable missing: libreoffice'])
                    self.assertEqual(calls, [])
                else:
                    self.assertTrue(result['errors'][0].startswith('Renderer smoke test: '))
                self.assertEqual(svg.call_count, int(failure == 'invalid_svg_png'))


if __name__ == '__main__':
    unittest.main()
