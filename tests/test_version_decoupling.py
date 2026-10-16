# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Protect product-version/material contract independence across future releases."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(rel: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


versioning = module('scripts/versioning.py', 'jai_versioning')


class VersionDecoupling(unittest.TestCase):
    def test_contracts_are_not_bound_to_product_release(self):
        root = ROOT / '.ai/runtime'
        roles = json.loads((root / 'roles.json').read_text(encoding='utf-8'))['roles']
        expected_ids = {f"{role['slug']}:{number}"
                        for role in roles
                        for number in range(1, len(role['primary_deliverables']) + 1)}
        self.assertTrue(expected_ids)
        catalogues = []
        for relative in ('artifacts/contracts/role-deliverables.v3.json',
                         'artifacts/role-deliverables.json'):
            data = json.loads((root / relative).read_text(encoding='utf-8'))
            self.assertEqual(len(data['contracts']), len(expected_ids))
            self.assertEqual({c['id'] for c in data['contracts']}, expected_ids)
            self.assertEqual(data['role_count'], len(roles))
            self.assertEqual(data['deliverable_count'], len(expected_ids))
            self.assertEqual(data['schema_version'], '3.0.0')
            self.assertEqual({c['version'] for c in data['contracts']}, {'3.0.0'})
            self.assertEqual({c['compatibility']['writes'] for c in data['contracts']},
                             {'ArtifactContract-v3'})
            catalogues.append(data['contracts'])
        tools = str(root / 'tools')
        with patch.object(sys, 'path', [tools, *sys.path]):
            artifacts = module('.ai/runtime/tools/artifacts.py', 'jai_artifacts_version_projection')
        projected = {row['id']: row for row in catalogues[1]}
        roles_by_slug = {role['slug']: role for role in roles}
        for row in catalogues[0]:
            with self.subTest(contract=row['id']):
                flattened = artifacts.flatten_v3(row)
                stored = projected[row['id']]
                self.assertEqual(flattened, {key: stored[key] for key in flattened})
                role = roles_by_slug[row['role_slug']]
                self.assertEqual(stored['role'], role['name'])
                self.assertEqual(stored['skill'], role['skill'])
        reg = json.loads((root / 'schema/schema-registry.json').read_text())
        by_name = {row['name']: row for row in reg['schemas']}
        self.assertEqual(by_name['ArtifactContract']['version'], '3.0.0')
        self.assertEqual(by_name['ArtifactContract']['path'], 'schema/contracts/artifact-v3.schema.json')

    def test_product_sync_preserves_native_and_legacy_contract_records(self):
        """A new distribution must not rewrite either kind of contract origin."""
        runtime = ROOT / '.ai/runtime'
        source = json.loads((runtime / 'artifacts/contracts/role-deliverables.v3.json').read_text())
        self.assertTrue(any('migration' in row for row in source['contracts']))
        self.assertTrue(any('native_creation' in row for row in source['contracts']))
        immutable = (
            'artifacts/contracts/role-deliverables.v3.json',
            'artifacts/role-deliverables.json',
            'artifacts/contracts/role-deliverables.v2.json',
            'artifacts/contracts/commercial-specialists.native-v3.json',
            'schema/contracts/artifact-v3.schema.json',
            'schema/26.10.4/artifact-contract.schema.json',
        )
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            (temp / 'VERSION').write_text('99.12.999\n', encoding='utf-8')
            for relative in versioning.MIRRORS[1:]:
                path = temp / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('26.10.4\n', encoding='utf-8')
            for relative in versioning.PRODUCT_CATALOGS:
                path = temp / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / relative).read_bytes())
            originals = {}
            for relative in immutable:
                path = temp / '.ai/runtime' / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                originals[path] = (runtime / relative).read_bytes()
                path.write_bytes(originals[path])
            versioning.sync(temp, generate_docs=False)
            for path, original in originals.items():
                with self.subTest(path=str(path.relative_to(temp))):
                    self.assertEqual(path.read_bytes(), original)
            for relative, key in versioning.PRODUCT_CATALOGS.items():
                self.assertEqual(json.loads((temp / relative).read_text())[key], '99.12.999')

    def test_sync_uses_only_root_version_and_preserves_history(self):
        with tempfile.TemporaryDirectory() as d:
            temp = Path(d)
            (temp / 'VERSION').write_text('26.10.5\n', encoding='utf-8')
            for rel in versioning.MIRRORS[1:]:
                p = temp / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('26.10.4\n', encoding='utf-8')
            for rel, key in versioning.PRODUCT_CATALOGS.items():
                p = temp / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps({key: '26.10.4', 'items': [{'version': '3.0.0'}]},
                                        indent=2) + '\n', encoding='utf-8')
            historical = temp / 'CHANGELOG.md'
            historical.write_text('## 26.10.4\nHistory remains\n', encoding='utf-8')
            versioning.sync(temp, generate_docs=False)
            for rel in versioning.MIRRORS:
                self.assertEqual((temp / rel).read_text(), '26.10.5\n')
            for rel, key in versioning.PRODUCT_CATALOGS.items():
                data = json.loads((temp / rel).read_text())
                self.assertEqual(data[key], '26.10.5')
                self.assertEqual(data['items'][0]['version'], '3.0.0')
            self.assertEqual(historical.read_text(), '## 26.10.4\nHistory remains\n')
            before = {p.relative_to(temp): p.read_bytes() for p in temp.rglob('*') if p.is_file()}
            versioning.sync(temp, generate_docs=False)
            self.assertEqual(before, {p.relative_to(temp): p.read_bytes() for p in temp.rglob('*') if p.is_file()})

    def test_cannot_downgrade_or_use_malformed_tag(self):
        self.assertEqual(versioning.identity_from_tag('release@26.10.5'), '26.10.5')
        for bad in ('release@26.13.0', 'release@26.10.5-rc1', 'v26.10.5',
                    'release@26.10.5/x'):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                versioning.identity_from_tag(bad)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'VERSION').write_text('26.10.5\n')
            with self.assertRaisesRegex(ValueError, 'differs from authoritative'):
                versioning.prepare(p, '26.10.4', generate_docs=False)

    def test_ai_commands_do_not_carry_product_specific_operational_headers(self):
        import re
        for path in (ROOT / '.ai/commands').glob('*.md'):
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(),
                    r'(?m)^## [0-9]{2}\.[0-9]{2}\.[0-9]+ operational specification')

    def test_active_evidence_schemas_accept_next_release(self):
        import re
        runtime = ROOT / '.ai/runtime'
        reg = json.loads((runtime / 'schema/schema-registry.json').read_text())
        names = {row['name']: row for row in reg['schemas']}
        for name in ('ExecutionRecord', 'BehavioralQualificationEvidence'):
            with self.subTest(schema=name):
                path = names[name]['path']
                self.assertTrue(path.startswith('schema/contracts/'))
                spec = json.loads((runtime / path).read_text())
                pattern = spec['properties']['release']['pattern']
                self.assertIsNotNone(re.fullmatch(pattern, '26.10.5'))
                self.assertIsNone(re.fullmatch(pattern, 'not-a-version'))

    def test_adapter_model_origin_does_not_track_package_release(self):
        tools = ROOT / '.ai/runtime/tools'
        sys.path.insert(0, str(tools))
        adapters = module('.ai/runtime/tools/integration_adapters.py',
                          'jai_integration_adapters')
        self.assertNotIn('release', adapters.build_registry())
        self.assertEqual(adapters.validate_contracts(), [])

    def test_model_router_reports_product_version_not_registry_origin(self):
        router = module('.ai/runtime/tools/model_router.py', 'jai_model_router_version')
        self.assertEqual(router.effective_payload()['release'],
                         (ROOT / 'VERSION').read_text().strip())
        self.assertEqual(router.effective_payload()['registry_origin_release'], '26.10.4')

    def test_tag_publishes_production_without_operator_approval(self):
        workflow = (ROOT / '.github/workflows/release.yml').read_text()
        self.assertIn("- 'release@*'", workflow)
        self.assertIn('scripts/versioning.py check --tag', workflow)
        self.assertIn('release_ga.py qualify', workflow)
        self.assertIn('gh release create', workflow)
        self.assertIn('--verify-tag --latest', workflow)
        self.assertNotIn('--draft', workflow)
        self.assertNotIn('gpg --', workflow.lower())
        policy = json.loads((ROOT / '.ai/runtime/release/release-policy.json').read_text())
        self.assertEqual(policy['signing']['mode'], 'automated-ci-release')
        self.assertIs(policy['signing']['publication_requires_manual_approval'], False)

    def test_frozen_26104_schema_has_original_identity(self):
        frozen = json.loads((ROOT / '.ai/runtime/schema/26.10.4/artifact-contract.schema.json').read_text())
        stable = json.loads((ROOT / '.ai/runtime/schema/contracts/artifact-v3.schema.json').read_text())
        self.assertEqual(frozen['properties']['compatibility']['properties']['writes']['const'],
                         '26.10.4/ArtifactContract-v3')
        self.assertEqual(stable['properties']['compatibility']['properties']['writes']['const'],
                         'ArtifactContract-v3')


if __name__ == '__main__':
    unittest.main()
