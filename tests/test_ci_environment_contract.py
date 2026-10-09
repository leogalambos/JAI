#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""CI dependency drift regression: validation and release share one environment."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ACTION = ROOT / '.github/actions/setup-qualification/action.yml'
MANIFEST = ROOT / 'ci/system-packages.txt'
PYTHON_REQUIREMENTS = ROOT / 'requirements-ci.txt'


class CIEnvironmentContract(unittest.TestCase):
    def test_both_qualification_workflows_share_composite_action(self):
        for filename in ('validate-library.yml', 'release.yml'):
            with self.subTest(filename=filename):
                text = (ROOT / '.github/workflows' / filename).read_text()
                self.assertIn('uses: ./.github/actions/setup-qualification', text)
                self.assertNotIn('pip install --disable-pip-version-check', text)
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

    def test_environment_gate_checks_actual_renderers(self):
        script = (ROOT / 'scripts/check_ci_environment.py').read_text()
        for dependency in ('libreoffice', 'pdftoppm', 'cairosvg.svg2png',
                           'Image.open', 'smoke.pdf', 'page.png'):
            self.assertIn(dependency, script)


if __name__ == '__main__':
    unittest.main()
