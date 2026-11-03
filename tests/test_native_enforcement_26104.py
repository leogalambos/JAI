# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Regression coverage for the active catalogue and signed governed recording."""
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
    def test_current_governed_identities_replay_and_tampering_fails(self):
        """Current native identity uses actual signed recording, not raw graph seeding."""
        import pytest
        from governed_fixtures import GovernedHarness, lc
        with tempfile.TemporaryDirectory() as directory, pytest.MonkeyPatch.context() as monkeypatch:
            host = GovernedHarness(Path(directory), monkeypatch, engagement='native-identity')
            host.bootstrap()
            actor = host.setup_author()
            product, body = host.product('native-answer', actor)
            host.commit(host.submission(actor, product, body))
            replayed = host.store.read()
            for reference in (host.input_a, product):
                value = replayed.versions[reference['version_id']]
                self.assertEqual(lc.version_id(value), reference['version_id'])
                self.assertEqual(value['content']['engagement'], 'native-identity')
                self.assertEqual(value['content']['scope'], 'default')
            lines = host.path.read_text().splitlines()
            broken = json.loads(lines[-1])
            broken['operations'][0]['data']['message']['request_id'] = 'altered-native-request'
            lines[-1] = json.dumps(broken)
            host.path.write_text('\n'.join(lines) + '\n')
            before = host.path.read_bytes()
            with self.assertRaises(ValueError):
                host.store.read()
            self.assertEqual(host.path.read_bytes(), before)

    def setUp(self):
        self.roles = json.loads((gate.R / 'roles.json').read_text())
        self.new = json.loads((gate.R / 'artifacts/contracts/role-deliverables.v3.json').read_text())
        self.layers = json.loads((gate.R / 'jai/core/layers.json').read_text())

    def validate(self):
        return gate.catalogue_problems(self.roles, self.new, self.layers, gate.R)

    def test_current_catalogue_passes(self):
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
                             'schema/contracts/artifact-v3.schema.json'):
                destination = runtime / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((gate.R / relative).read_bytes())
            self.new['contracts'].append(copy.deepcopy(self.new['contracts'][0]))
            (runtime / 'artifacts/contracts').mkdir(parents=True, exist_ok=True)
            (runtime / 'artifacts/contracts/role-deliverables.v3.json').write_text(json.dumps(self.new))
            with mock.patch.object(gate, 'R', runtime), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(gate.main(), 1)
            self.assertIn('duplicate, empty or missing authoritative contract identities', output.getvalue())
