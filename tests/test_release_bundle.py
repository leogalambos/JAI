# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Distribution privacy and deterministic packaging, using disposable sources only."""
import contextlib
import io
import json
from pathlib import Path
import os
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import release_bundle as bundle


class ReleaseBundleTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / 'source'
        self.root.mkdir()
        self.outputs = self.directory / 'outputs'
        self.outputs.mkdir()
        self.resources = {
            'VERSION': '26.10.4\n',
            'README.md': 'Maintained documentation',
            '.ai/runtime/tools/example.py': '"""Maintained runtime."""\n',
            '.ai/runtime/sabsa/publication/example.json': '{"fictional":true}',
            '.ai/runtime/sabsa/publication/profiles/logical.json': '{"layer":"logical"}',
            '.ai/runtime/templates/sabsa/latex/enterprise.tex': 'Maintained template',
            '.env.example': 'Public environment example',
            'QUALIFICATION-A-H.json': json.dumps({'all_pass': True, 'gates': dict.fromkeys('ABCDEFGH', True)})}
        for name, data in self.resources.items(): self.write(name, data)

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding='utf-8')
        return path

    def test_private_and_generated_trees_are_pruned_before_traversal(self):
        private = ('INBOX', 'build', 'out', 'dist', 'site', '.git', '.venv',
                   '.findings', '.fabric', 'docs/.findings', 'docs/.fabric',
                   '.direnv', '.secrets', '__pycache__', '.ai/runtime/_meta/gates')
        for name in private: self.write(name + '/sentinel.txt', 'PRIVATE FIXTURE MARKER')
        self.write('.ai/runtime/_meta/qualification-A-G.json', 'Excluded generated evidence')
        forbidden = {self.root / name for name in private}
        scandir = os.scandir
        def guarded_scandir(path):
            if Path(path) in forbidden:
                raise AssertionError('Private directory must never be traversed')
            return scandir(path)
        with patch.object(bundle.os, 'scandir', side_effect=guarded_scandir):
            actual = {path.relative_to(self.root).as_posix() for path in bundle.files(self.root)}
        self.assertEqual(set(self.resources), actual)

    def test_private_local_files_are_excluded_but_public_examples_remain(self):
        for name in ('.env', '.env.local', 'docs/.env.test', 'signing.pem', 'identity.key',
                     'identity.p12', 'identity.pfx', '.claude/settings.local.json', '.codex/config.local.toml'):
            self.write(name, 'PRIVATE FIXTURE MARKER')
        for name in ('.env.sample', '.env.template'): self.write(name, 'Public example')
        actual = {path.relative_to(self.root).as_posix() for path in bundle.files(self.root)}
        self.assertEqual(set(self.resources) | {'.env.sample', '.env.template'}, actual)

    def test_symlink_aliases_never_pull_private_bytes_into_zip(self):
        private = self.write('INBOX/sentinel.txt', 'PRIVATE FIXTURE MARKER')
        (self.root / 'public-alias.txt').symlink_to(private)
        (self.root / 'public-directory').symlink_to(private.parent, target_is_directory=True)
        out = self.outputs / 'safe.zip'
        bundle.build_zip(self.root, out, 'package')
        with zipfile.ZipFile(out) as archive:
            self.assertEqual({'package/' + name for name in self.resources}, set(archive.namelist()))
            self.assertFalse(any(b'PRIVATE FIXTURE MARKER' in archive.read(name) for name in archive.namelist()))

    def test_output_subtree_is_excluded_and_archives_are_byte_deterministic(self):
        generated = self.write('generated/archive-evidence.txt', 'Not an input')
        self.assertNotIn(generated, list(bundle.files(self.root, generated.parent)))
        first = self.outputs / 'one.zip'
        second = self.outputs / 'two.zip'
        bundle.build_zip(self.root, first, 'package')
        bundle.build_zip(self.root, second, 'package')
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertTrue(all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist()))
        inside = self.root / 'generated'
        bundle.build_zip(self.root, inside / 'release.zip', 'package')
        with zipfile.ZipFile(inside / 'release.zip') as archive:
            self.assertFalse(any('/generated/' in name for name in archive.namelist()))

    def test_invalid_root_output_and_existing_destination_do_not_overwrite(self):
        alias = self.directory / 'source-alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): list(bundle.files(alias))
        with self.assertRaises(ValueError): bundle.build_zip(alias, self.outputs / 'alias.zip', 'package')
        for out in (self.root / 'release.zip', self.directory / 'release.zip'):
            with self.subTest(out=out), self.assertRaises(ValueError):
                bundle.build_zip(self.root, out, 'package')
            self.assertFalse(out.exists())
        existing = self.write('docs/maintained.zip', 'Maintained content')
        with self.assertRaises(FileExistsError): bundle.build_zip(self.root, existing, 'package')
        self.assertEqual('Maintained content', existing.read_text())

    def test_release_qualification_gates_and_fixture_build_remain_enforced(self):
        with patch.object(bundle.subprocess, 'run', return_value=SimpleNamespace(returncode=1)):
            with self.assertRaisesRegex(SystemExit, 'policy'): bundle.check_ready(self.root)
        qualification = self.root / 'QUALIFICATION-A-H.json'
        original = qualification.read_text()
        qualification.write_text(json.dumps({'all_pass': True, 'gates': {'A': True}}))
        with patch.object(bundle.subprocess, 'run', return_value=SimpleNamespace(returncode=0)):
            with self.assertRaisesRegex(SystemExit, 'all PASS'): bundle.check_ready(self.root)
            qualification.write_text(original)
            self.assertIsNone(bundle.check_ready(self.root))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, bundle.build(self.root, self.outputs))
            with self.assertRaisesRegex(SystemExit, 'already exists'): bundle.build(self.root, self.outputs)
        self.assertTrue((self.outputs / 'ai-it-house-universal-26.10.4.zip').is_file())
        self.assertTrue((self.outputs / 'ai-it-house-universal-26.10.4.sha256').is_file())


if __name__ == '__main__':
    unittest.main()
