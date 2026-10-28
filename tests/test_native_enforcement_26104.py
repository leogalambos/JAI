# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Regression coverage for active and immutable native release cohorts."""
import copy
import contextlib
import io
import tempfile
from unittest import mock
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location('native_gate', TOOLS / 'native_enforcement_26104.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class NativeEnforcementTests(unittest.TestCase):
    def test_current_fabric_identities_replay_with_the_shared_manifest_formula(self):
        """Native probes must bind exact versions, not former semantic aliases."""
        fabric = gate.module_from(gate.R / 'fabric/fabric.py', 'native_identity_fixture')
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(fabric, 'FABRIC_DIR', directory):
            graph = fabric.Fabric('native-identity', [])
            fragment = graph.add_node('frag', 3, 'Material claim', kind='claim', contract='ctr-0001')
            evidence = graph.add_node('evd', 3, 'Source record', confidence='observation', contract='ctr-0001')
            replayed = fabric.Fabric('native-identity', fabric.load('native-identity'))
            for node in (fragment, evidence):
                with self.subTest(kind=node['type']):
                    manifest = replayed.lifecycle.versions[node['version_id']]
                    self.assertEqual(fabric.lifecycle.version_id(manifest), node['version_id'])
                    self.assertEqual(node['object_ref'], 'lifecycle:' + node['id'])
                    self.assertEqual(node['object_hash'], 'sha256:' + node['version_id'])
                    self.assertEqual(manifest['content']['context_digest'], node['context_digest'])
                    self.assertEqual(manifest['content']['contract_ref'], 'ctr-0001')
                    self.assertEqual(replayed.nodes[node['id']], node)
            broken = copy.deepcopy(graph.transactions)
            broken[-1]['operations'][-1]['data']['object_hash'] = 'sha256:' + '0' * 64
            with self.assertRaises(ValueError):
                fabric.Fabric('native-identity', broken)

    def setUp(self):
        self.roles = json.loads((gate.R / 'roles.json').read_text())
        self.old = json.loads((gate.R / 'artifacts/contracts/role-deliverables.v2.json').read_text())
        self.new = json.loads((gate.R / 'artifacts/contracts/role-deliverables.v3.json').read_text())
        self.layers = json.loads((gate.R / 'jai/core/layers.json').read_text())

    def validate(self):
        return gate.catalogue_problems(self.roles, self.old, self.new, self.layers, gate.R)

    def test_current_native_additions_and_immutable_legacy_pass(self):
        self.assertEqual(self.validate(), [])

    def test_missing_extra_duplicate_and_empty_contracts_fail_cleanly(self):
        for kind in ('missing', 'extra', 'duplicate', 'empty'):
            with self.subTest(kind=kind):
                original = copy.deepcopy(self.new)
                if kind == 'missing': self.new['contracts'].pop(0)
                elif kind == 'duplicate': self.new['contracts'].append(copy.deepcopy(self.new['contracts'][0]))
                elif kind == 'empty': self.new['contracts'] = []
                else:
                    row = copy.deepcopy(self.new['contracts'][-1]); row['id'] = 'unknown:999'; self.new['contracts'].append(row)
                self.assertTrue(self.validate())
                self.new = original

    def test_layer_count_and_duplicate_role_tampering_fail(self):
        for kind in ('layer', 'count', 'duplicate'):
            with self.subTest(kind=kind):
                original = copy.deepcopy(self.roles)
                if kind == 'layer': self.roles['roles'][0]['layer'] = 999
                elif kind == 'count': self.roles['count'] += 1
                else: self.roles['roles'].append(copy.deepcopy(self.roles['roles'][0]))
                self.assertTrue(self.validate())
                self.roles = original

    def test_native_provenance_tampering_and_legacy_relabelling_fail(self):
        row = self.new['contracts'][-1]
        row['native_creation']['evidence_hash'] = '0' * 64
        self.assertTrue(self.validate())
        self.setUp()
        row = self.new['contracts'][0]
        row['native_creation'] = copy.deepcopy(self.new['contracts'][-1]['native_creation'])
        self.assertTrue(self.validate())

    def test_missing_legacy_source_and_material_drift_fail(self):
        self.old['contracts'].pop()
        self.assertTrue(self.validate())
        self.setUp()
        self.new['contracts'][0]['jai']['intent']['purpose'] += ' tampered'
        self.assertTrue(self.validate())

    def test_native_identity_missing_despite_adjusted_count_is_rejected(self):
        self.new['contracts'].pop()
        self.new['deliverable_count'] -= 1
        self.assertIn('canonical role deliverable identity coverage mismatch', self.validate())

    def test_native_binding_schema_and_unknown_role_are_rejected(self):
        for field in ('binding', 'role'):
            with self.subTest(field=field):
                original = copy.deepcopy(self.new)
                row = self.new['contracts'][-1]
                if field == 'binding': del row['jai']['evidence']
                else: row['role_slug'] = 'unknown'
                self.assertTrue(self.validate())
                self.new = original

    def test_main_rejects_duplicate_catalogue_without_traceback(self):
        with tempfile.TemporaryDirectory() as td:
            runtime = Path(td)
            for relative in ('roles.json', 'workflows.json', 'jai/core/layers.json',
                             'jai/core/native-write-policy.json',
                             'artifacts/contracts/role-deliverables.v2.json',
                             'schema/contracts/artifact-v3.schema.json'):
                destination = runtime / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((gate.R / relative).read_bytes())
            self.new['contracts'].append(copy.deepcopy(self.new['contracts'][0]))
            (runtime / 'artifacts/contracts/role-deliverables.v3.json').write_text(json.dumps(self.new))
            with mock.patch.object(gate, 'R', runtime), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(gate.main(), 1)
            self.assertIn('duplicate, empty or missing authoritative contract identities', output.getvalue())
