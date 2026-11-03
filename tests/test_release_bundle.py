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
import unittest
from unittest.mock import patch
import zipfile
import hashlib

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
            '.env.example': 'Public environment example'}
        for name, data in self.resources.items(): self.write(name, data)

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding='utf-8')
        return path

    def test_release_rejects_missing_current_source_without_creating_output(self):
        destination = self.directory / 'unavailable-release'
        with self.assertRaises(OSError):
            bundle.check_ready(self.root)
        with self.assertRaises(OSError):
            bundle.build(self.root, destination)
        self.assertFalse(destination.exists())
        self.assertEqual(list(self.outputs.iterdir()), [])

    def test_current_source_contracts_are_checked_without_importing_old_pass(self):
        policy = {'signing': {'mode': 'automated-ci-release'},
                  'required_release_files': ['VERSION', 'README.md']}
        self.write('.ai/runtime/release/release-policy.json', json.dumps(policy))
        self.write('QUALIFICATION-A-H.json', json.dumps({'all_pass': True}))
        success = bundle.subprocess.CompletedProcess([], 0, 'PASS', '')
        with patch.object(bundle.subprocess, 'run', return_value=success) as execute:
            self.assertEqual(bundle.check_ready(self.root), '26.10.4')
        self.assertEqual(execute.call_count, 2)
        failed = bundle.subprocess.CompletedProcess([], 1, '', 'stale version')
        with patch.object(bundle.subprocess, 'run', return_value=failed):
            with self.assertRaisesRegex(ValueError, 'source contract failed'):
                bundle.check_ready(self.root)
        (self.root / 'README.md').unlink()
        with self.assertRaisesRegex(ValueError, 'required release source missing'):
            bundle.check_ready(self.root)

    def test_build_produces_versioned_archive_checksum_and_preserves_existing_output(self):
        for name in bundle.INTERNAL_RELEASE_RECORDS:
            self.write(name, 'PRIVATE HISTORICAL DEVELOPMENT RESULT')
        with patch.object(bundle, 'check_ready', return_value='26.10.4'):
            result = bundle.build(self.root, self.outputs)
            archive, checksum = Path(result['archive']), Path(result['checksum'])
            self.assertEqual(archive.name, 'ai-it-house-universal-26.10.4.zip')
            self.assertEqual(checksum.read_text(), hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
            with zipfile.ZipFile(archive) as package:
                self.assertFalse(any(Path(name).name in bundle.INTERNAL_RELEASE_RECORDS for name in package.namelist()))
                self.assertIn('ai-it-house-universal-26.10.4/README.md', package.namelist())
            before = archive.read_bytes()
            with self.assertRaises(FileExistsError):
                bundle.build(self.root, self.outputs)
            self.assertEqual(archive.read_bytes(), before)

    def test_dependency_closure_rejects_retired_imports_but_ships_supported_verifier(self):
        self.assertTrue(bundle.dependency_closure(self.root))
        broken=self.write('.ai/runtime/tools/broken.py','import runtime_service\n')
        with self.assertRaisesRegex(ValueError,'dependency closure'):bundle.dependency_closure(self.root)
        broken.unlink()
        self.write('.ai/runtime/tools/maintained_fixture_tool.py','def report(): return {}\n')
        self.assertIn(self.root/'.ai/runtime/tools/maintained_fixture_tool.py',list(bundle.files(self.root)))
        self.assertTrue(bundle.dependency_closure(self.root))

    def test_private_and_generated_trees_are_pruned_before_traversal(self):
        private = ('INBOX', 'build', 'out', 'dist', 'site', 'obsolete', '.git', '.venv',
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

    def test_git_pointer_and_credential_names_are_never_read_or_packaged(self):
        for name in ('.git', 'auth.json', 'id_rsa', 'id_ed25519', '.npmrc', '.pypirc', '.netrc',
                     'settings-security.xml', 'nested/auth.json'):
            self.write(name, 'PRIVATE FIXTURE MARKER')
        actual = {p.relative_to(self.root).as_posix() for p in bundle.files(self.root)}
        self.assertEqual(actual, set(self.resources))
        target = self.outputs / 'private-name-safe.zip'
        bundle.build_zip(self.root, target, 'package')
        with zipfile.ZipFile(target) as archive:
            self.assertEqual(set(archive.namelist()), {'package/' + name for name in self.resources})

    def test_personal_credential_trees_are_pruned_but_generated_skills_remain(self):
        directories = ('.aws', '.ssh', '.gnupg', '.kube', '.docker', '.config', '.local')
        for name in directories: self.write(name + '/sentinel', 'PRIVATE FIXTURE MARKER')
        for name in ('.claude.json', '.claude/settings.json', '.codex/config.toml'):
            self.write(name, 'PRIVATE FIXTURE MARKER')
        maintained = self.write('.codex/skills/example/SKILL.md', 'Maintained generated skill')
        scandir = os.scandir
        def no_private_scan(path):
            if Path(path) in {self.root / name for name in directories}:
                raise AssertionError('credential directory traversed')
            return scandir(path)
        with patch.object(bundle.os, 'scandir', side_effect=no_private_scan):
            actual = set(bundle.files(self.root))
        self.assertIn(maintained, actual)
        self.assertEqual({p.relative_to(self.root).as_posix() for p in actual},
                         set(self.resources) | {'.codex/skills/example/SKILL.md'})

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

    def test_unsafe_archive_prefix_or_member_never_creates_output(self):
        for prefix in ('', None, '.', '..', '../escape', '/absolute', 'nested/name', 'back\\slash', 'drive:name', 'line\nname', 'AUX', 'trailing.', 'COM1.txt'):
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                bundle.build_zip(self.root, self.outputs / 'unsafe.zip', prefix)
            self.assertFalse((self.outputs / 'unsafe.zip').exists())
        self.write('bad\\name.txt', 'unsafe extraction name')
        with self.assertRaises(ValueError):
            bundle.build_zip(self.root, self.outputs / 'unsafe.zip', 'package')
        self.assertFalse((self.outputs / 'unsafe.zip').exists())

    def test_portable_member_collision_is_rejected(self):
        self.write('Case.txt', 'one')
        self.write('case.txt', 'two')
        with self.assertRaises(ValueError):
            bundle.build_zip(self.root, self.outputs / 'collision.zip', 'package')
        self.assertFalse((self.outputs / 'collision.zip').exists())

    def test_source_mutation_during_build_does_not_publish_archive(self):
        original = zipfile.ZipFile.writestr
        changed = False
        def changing_write(archive, *args, **kwargs):
            nonlocal changed
            result = original(archive, *args, **kwargs)
            if not changed:
                self.write('README.md', 'changed while packaging')
                changed = True
            return result
        with patch.object(zipfile.ZipFile, 'writestr', changing_write), self.assertRaises(ValueError):
            bundle.build_zip(self.root, self.outputs / 'race.zip', 'package')
        self.assertFalse((self.outputs / 'race.zip').exists())

    def test_archive_validation_rejects_duplicates_traversal_links_and_bad_hash(self):
        good = self.outputs / 'good.zip'
        bundle.build_zip(self.root, good, 'package')
        with zipfile.ZipFile(good) as archive:
            expected = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist()}
        self.assertEqual(bundle.verify_zip(good, expected)['member_count'], len(expected))
        with self.assertRaises(ValueError): bundle.verify_zip(good, {'package/VERSION': '0' * 64})
        for kind in ('duplicate', 'traversal', 'symlink'):
            target = self.outputs / (kind + '.zip')
            with zipfile.ZipFile(target, 'w') as archive:
                if kind == 'duplicate':
                    archive.writestr('package/a', 'one')
                    with __import__('warnings').catch_warnings():
                        __import__('warnings').simplefilter('ignore', UserWarning)
                        archive.writestr('package/a', 'two')
                elif kind == 'traversal': archive.writestr('../escape', 'bad')
                else:
                    info = zipfile.ZipInfo('package/link'); info.create_system = 3
                    info.external_attr = 0o120777 << 16
                    archive.writestr(info, 'target')
            with self.subTest(kind=kind), self.assertRaises(ValueError): bundle.verify_zip(target)

    def test_archive_validation_empty_and_exact_size_boundaries(self):
        empty = self.outputs / 'empty.zip'
        with zipfile.ZipFile(empty, 'w'): pass
        with self.assertRaises(ValueError): bundle.verify_zip(empty)
        target = self.outputs / 'bounded.zip'
        with zipfile.ZipFile(target, 'w') as archive: archive.writestr('package/file', b'1234')
        self.assertEqual(bundle.verify_zip(target, maximum_uncompressed_bytes=4)['member_count'], 1)
        for limit in (3, 0, -1, True):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                bundle.verify_zip(target, maximum_uncompressed_bytes=limit)








if __name__ == '__main__':
    unittest.main()
