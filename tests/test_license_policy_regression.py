#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Verify the same licensing policy during unit tests as during Gate H."""
from __future__ import annotations

import importlib.util
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LICENSE_CHECK = ROOT / '.ai/runtime/tools/license_check.py'
sys.path.insert(0, str(LICENSE_CHECK.parent))


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
        for directory in ('build', 'out', 'dist', 'site', '.venv'):
            self._write(f'{directory}/generated.py', 'unlicensed generated output\n')
        self.assertEqual(self.policy.check(self.root), [])

    def test_web_source_headers_are_required_and_comment_formats_are_accepted(self):
        for name, delimiters in (('assets/app.js', ('/*', '*/')),
                                 ('assets/site.css', ('/*', '*/')),
                                 ('overrides/main.html', ('{#', '#}'))):
            with self.subTest(name=name):
                self._write(name, 'unlicensed source\n')
                self.assertEqual(self.policy.check(self.root), [
                    f'{name}: compact SPDX header missing',
                    f'{name}: compact copyright header missing'])
                start, end = delimiters
                self._write(name, f'{start} {self.policy.SPDX}\n{self.policy.COPY} {end}\n')
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


class GitSourceLicensePolicy(unittest.TestCase):
    _write = LicensePolicyFixtures._write

    def setUp(self):
        LicensePolicyFixtures.setUp(self)
        self._git('init', '-q')
        self._git('add', 'LICENSE')

    def _git(self, *arguments):
        return subprocess.run(['git', *arguments], cwd=self.root, check=True,
                              capture_output=True, text=True)

    def test_untracked_ignored_generated_and_foreign_sources_are_not_read_or_checked(self):
        self._write('.gitignore', 'ignored/\n')
        unowned = ['untracked.py', 'untracked.js', 'ignored/draft.py',
                   'apps/demo/dist/assets/generated.js', 'vendor/foreign.js']
        for name in unowned:
            self._write(name, 'Foreign or generated source without project licensing.\n')
        read_text = Path.read_text
        def read(path, *args, **kwargs):
            self.assertNotIn(path.relative_to(self.root).as_posix(), unowned)
            return read_text(path, *args, **kwargs)
        with patch.object(Path, 'read_text', read):
            self.assertEqual(self.policy.check(self.root), [])
        self.assertEqual((self.root / 'vendor/foreign.js').read_text(),
                         'Foreign or generated source without project licensing.\n')

    def test_newly_tracked_unlicensed_source_and_edited_tracked_source_fail(self):
        self._write('tools/new.py', 'print("new")\n')
        self.assertEqual(self.policy.check(self.root), [])
        self._git('add', 'tools/new.py')
        self.assertEqual(self.policy.check(self.root), [
            'tools/new.py: compact SPDX header missing',
            'tools/new.py: compact copyright header missing'])
        self._write('tools/new.py', self.header)
        self._git('add', 'tools/new.py')
        self.assertEqual(self.policy.check(self.root), [])
        self._write('tools/new.py', 'edited without required header\n')
        self.assertEqual(len(self.policy.check(self.root)), 2)

    def test_tracked_private_generated_and_symlink_paths_remain_excluded(self):
        for name in ('INBOX/private.py', 'build/generated.py', 'config/.env', '.git/not-a-source.py'):
            self._write(name, 'Not a public release source.\n')
        (self.root / 'linked.py').symlink_to(self.root / 'INBOX/private.py')
        self._git('add', '-f', 'INBOX/private.py', 'build/generated.py', 'config/.env', 'linked.py')
        self.assertEqual(self.policy.check(self.root), [])

    def test_gitless_subdirectory_uses_its_own_archive_inventory_not_parent_git(self):
        self._write('archive/LICENSE', (self.root / 'LICENSE').read_text())
        self._write('archive/source.py', 'archive source without header\n')
        self.assertEqual(self.policy.check(self.root / 'archive'), [
            'source.py: compact SPDX header missing',
            'source.py: compact copyright header missing'])

    def test_git_inventory_failure_cannot_be_reported_as_pass_or_archive_fallback(self):
        self._write('untracked.py', 'would fail if silently scanned as an archive\n')
        with patch('subprocess.run', return_value=subprocess.CompletedProcess(['git'], 128, b'', b'broken index')):
            with self.assertRaises((OSError, ValueError)):
                self.policy.check(self.root)

    def test_git_index_failure_and_unsafe_inventory_fail_after_root_verification(self):
        location = subprocess.CompletedProcess(['git'], 0, (str(self.root) + '\n').encode(), b'')
        for inventory in (subprocess.CompletedProcess(['git'], 128, b'', b'broken index'),
                          subprocess.CompletedProcess(['git'], 0, b'../outside.py\0', b''),
                          subprocess.CompletedProcess(['git'], 0, b'incomplete.py', b'')):
            with self.subTest(inventory=inventory):
                with patch('subprocess.run', side_effect=[location, inventory]):
                    with self.assertRaises(ValueError):
                        self.policy.check(self.root)

    def test_enclosing_repository_identity_cannot_substitute_for_root_marker(self):
        location = subprocess.CompletedProcess(['git'], 0, (str(self.root.parent) + '\n').encode(), b'')
        with patch('subprocess.run', return_value=location):
            with self.assertRaisesRegex(ValueError, 'root could not be verified'):
                self.policy.check(self.root)

    def test_git_file_worktree_uses_its_own_tracked_inventory(self):
        self._git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                  'commit', '-qm', 'Source fixture')
        worktree = self.root.parent / (self.root.name + '-worktree')
        self._git('worktree', 'add', '--detach', str(worktree), 'HEAD')
        self.addCleanup(subprocess.run, ['git', 'worktree', 'remove', '--force', str(worktree)],
                        cwd=self.root, check=True, capture_output=True)
        self.assertTrue((worktree / '.git').is_file())
        (worktree / 'scratch.js').write_text('Untracked scratch source.\n')
        self.assertEqual(self.policy.check(worktree), [])
        (worktree / 'tracked.js').write_text('New project source without header.\n')
        subprocess.run(['git', 'add', 'tracked.js'], cwd=worktree, check=True, capture_output=True)
        self.assertEqual(len(self.policy.check(worktree)), 2)


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
