#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Verify the same licensing policy during unit tests as during Gate H."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LICENSE_CHECK = ROOT / '.ai/runtime/tools/license_check.py'


class LicensePolicyFixtures(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('jai_fixture_license_check', LICENSE_CHECK)
        self.policy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.policy)
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self._write('LICENSE', '\n'.join((
            'BSD 4-Clause License', 'Egothor team', 'Leo Galambos',
            'https://www.egothor.org', self.policy.FULL_SENTENCE)))
        self.header = f'# {self.policy.SPDX}\n# {self.policy.COPY}\n'

    def _write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_valid_published_headers_and_ai_context_exemption_pass(self):
        self._write('tools/example.py', '#!/usr/bin/env python3\n' + self.header)
        self._write('.ai/skills/example/SKILL.md', 'Professional role instructions.\n')
        self.assertEqual(self.policy.check(self.root), [])

    def test_unlicensed_published_source_fails(self):
        self._write('tests/example.py', 'print("example")\n')
        self.assertEqual(self.policy.check(self.root), [
            'tests/example.py: compact SPDX header missing',
            'tests/example.py: compact copyright header missing'])

    def test_private_inbox_is_not_traversed_but_similarly_named_source_is_checked(self):
        self._write('INBOX/private.py', 'private draft without headers\n')
        self._write('INBOX/.ai/skills/draft.md', self.policy.FULL_SENTENCE)
        self._write('INBOX-extra/example.py', 'published source without headers\n')
        problems = self.policy.check(self.root)
        self.assertEqual(len(problems), 2)
        self.assertTrue(all(problem.startswith('INBOX-extra/') for problem in problems))

    def test_generated_output_is_excluded_using_release_packaging_policy(self):
        for directory in ('build', 'out', 'dist', 'site', '.git', '.venv'):
            self._write(f'{directory}/generated.py', 'unlicensed generated output\n')
        self.assertEqual(self.policy.check(self.root), [])

    def test_shebang_must_remain_first(self):
        self._write('tools/example.py', self.header + '#!/usr/bin/env python3\n')
        self.assertEqual(self.policy.check(self.root), [
            'tools/example.py: shebang must remain the first line'])

    def test_headers_beyond_first_eight_lines_fail(self):
        self._write('tools/example.py', '\n' * 8 + self.header)
        self.assertEqual(len(self.policy.check(self.root)), 2)

    def test_ai_context_boilerplate_and_stale_internal_metadata_fail(self):
        self._write('.ai/skills/example/SKILL.md', self.policy.FULL_SENTENCE)
        self._write('.ai/agents/example.md', 'licence: internal-use\n')
        self.assertEqual(self.policy.check(self.root), [
            '.ai/agents/example.md: stale internal-use licence metadata',
            '.ai/skills/example/SKILL.md: full license boilerplate must not consume AI context'])

    def test_missing_root_license_fails(self):
        (self.root / 'LICENSE').unlink()
        self.assertEqual(self.policy.check(self.root), ['root LICENSE missing'])


class SourceLicensePolicy(unittest.TestCase):
    def test_source_licensing_matches_release_gate_h(self):
        spec = importlib.util.spec_from_file_location('jai_license_check', LICENSE_CHECK)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        problems = module.check(ROOT)
        self.assertEqual(problems, [], '\n'.join(problems))


if __name__ == '__main__':
    unittest.main()
