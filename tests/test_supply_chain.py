# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Distribution-scoped supply-chain provenance and private input regressions."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile
import hashlib

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import release_bundle
import supply_chain


class SupplyChainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        (self.root / 'VERSION').write_text('26.10.5\n')
        (self.root / 'public.md').write_text('Public documentation\n')

    def test_private_trees_are_pruned_before_descent(self):
        private = self.root / 'INBOX'
        private.mkdir()
        (private / 'private-review.md').write_text('Private\n')
        import os
        real_scandir = os.scandir
        def scan(path):
            if Path(path) == private:
                raise AssertionError('private directory traversed')
            return real_scandir(path)
        with mock.patch.object(os, 'scandir', side_effect=scan):
            paths = list(supply_chain.tree_files(self.root))
        self.assertEqual({p.name for p in paths}, {'VERSION', 'public.md'})

    def test_private_changes_do_not_change_digest_but_public_changes_do(self):
        before = supply_chain.tree_digest(self.root)
        for directory in ('INBOX', '.findings', '.fabric', 'build', 'out'):
            path = self.root / directory
            path.mkdir()
            (path / 'local.md').write_text('Private fixture')
        (self.root / '.env').write_text('Synthetic local configuration')
        self.assertEqual(supply_chain.tree_digest(self.root), before)
        (self.root / 'public.md').write_text('Modified')
        self.assertNotEqual(supply_chain.tree_digest(self.root), before)

    def test_sbom_and_provenance_verify_extracted_distribution(self):
        (self.root/'.ai/runtime/schema').mkdir(parents=True)
        (self.root/'.ai/runtime/schema/release-scope.schema.json').write_bytes((TOOLS.parent/'schema/release-scope.schema.json').read_bytes())
        (self.root/'RELEASE-SCOPE.json').write_bytes((TOOLS.parents[2]/'RELEASE-SCOPE.json').read_bytes())
        (self.root / 'INBOX').mkdir()
        (self.root / 'INBOX/private.md').write_text('Private fixture')
        meta = self.root / '.ai/runtime/_meta'
        meta.mkdir(parents=True,exist_ok=True)
        qualification = meta / 'qualification-A-G.json'
        qualification.write_text(json.dumps({'gates': dict.fromkeys('ABCDEFG', True)}))
        sbom = self.root / 'SBOM.spdx.json'
        prov = self.root / 'PROVENANCE.json'
        document = supply_chain.sbom(self.root, sbom)
        self.assertFalse(any('INBOX' in row['fileName'] for row in document['files']))
        supply_chain.provenance(self.root, sbom, qualification, prov)
        archive = Path(self.temp.name) / 'dist/release.zip'
        archive.parent.mkdir()
        release_bundle.build_zip(self.root, archive, 'package')
        extracted = Path(self.temp.name) / 'extract'
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(extracted)
        package = extracted / 'package'
        self.assertTrue(supply_chain.verify(package, package / sbom.name, package / prov.name))
        saved=(package/prov.name).read_text();bad=json.loads(saved);bad['supported_capabilities']={}
        (package/prov.name).write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError,'release scope mismatch'):
            supply_chain.verify(package,package/sbom.name,package/prov.name)
        (package/prov.name).write_text(saved)
        (package / 'public.md').write_text('Tampered')
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            supply_chain.verify(package, package / sbom.name, package / prov.name)

    def test_symlinks_and_circular_evidence_are_excluded(self):
        (self.root / 'alias.md').symlink_to(self.root / 'public.md')
        for name in supply_chain.EXCLUDE:
            (self.root / name).write_text('{}')
        self.assertEqual({p.name for p in supply_chain.tree_files(self.root)}, {'VERSION', 'public.md'})

    def test_empty_directory_and_invalid_root(self):
        empty = self.root / 'empty'
        empty.mkdir()
        self.assertEqual(list(supply_chain.tree_files(empty)), [])
        with self.assertRaises(ValueError):
            list(supply_chain.tree_files(self.root / 'absent'))

    def test_tree_files_importable_without_tools_search_path(self):
        spec = importlib.util.spec_from_file_location('isolated_supply_chain', TOOLS / 'supply_chain.py')
        isolated = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(isolated)
        with mock.patch.object(sys, 'path', [p for p in sys.path if p != str(TOOLS)]):
            self.assertEqual({p.name for p in isolated.tree_files(self.root)}, {'VERSION', 'public.md'})

    def test_relative_root_matches_absolute_digest_and_sbom(self):
        import os
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            self.assertEqual(supply_chain.tree_digest('.'), supply_chain.tree_digest(self.root))
            document = supply_chain.sbom('.', 'SBOM.spdx.json')
            self.assertEqual({row['fileName'] for row in document['files']}, {'./VERSION', './public.md'})
        finally:
            os.chdir(previous)

    def test_sbom_dependencies_follow_declared_requirements_not_stale_constants(self):
        (self.root / 'requirements.txt').write_text('jsonschema>=4.26,<5\nlxml>=6,<7\n')
        (self.root / 'requirements-ci.txt').write_text('-r requirements.txt\nlxml==6.1.3\npytest==8.4.2\n')
        document = supply_chain.sbom(self.root, self.root / 'SBOM.spdx.json')
        dependencies = [p for p in document['packages'] if p['SPDXID'] != 'SPDXRef-Package']
        self.assertEqual({p['name'] for p in dependencies}, {'jsonschema', 'lxml', 'pytest'})
        self.assertTrue(all(p['licenseDeclared'] == 'NOASSERTION' and not p['filesAnalyzed'] for p in dependencies))
        lxml = next(p for p in dependencies if p['name'] == 'lxml')
        self.assertEqual(lxml['versionInfo'], '6.1.3')
        self.assertNotIn('lxml 5.x', document['annotations'][0]['comment'])
        self.assertTrue(any(row['relationshipType'] == 'DEPENDS_ON' for row in document['relationships']))

    def test_hash_boundaries_and_existing_integrity_selftest(self):
        self.assertEqual(supply_chain.sha(b''), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        self.assertEqual(supply_chain.sha(b'abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        with self.assertRaises(TypeError): supply_chain.sha('not bytes')
        self.assertEqual(supply_chain.self_test(), 0)
