# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Canonical discovery projection and drift detection regression tests."""
import copy
import contextlib
import io
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generate_commercial_catalog', ROOT / '.ai/runtime/tools/generate_commercial_catalog.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class GenerateCommercialCatalogTests(unittest.TestCase):
    def fixture(self):
        source = json.loads((ROOT / '.ai/runtime/roles.json').read_text())
        row = copy.deepcopy(source['roles'][0])
        return {'version': source['version'], 'count': 1, 'roles': [row]}

    def test_project_keeps_exact_alias_domain_and_readonly_operator(self):
        registry = self.fixture()
        row = registry['roles'][0]
        result = g.project(registry)
        catalog = json.loads(result['catalog.json'])
        shard = json.loads(result[catalog['domains'][0]['shard']])
        self.assertEqual(shard['roles'][0]['operator'], 'role-advisor')
        self.assertEqual(shard['roles'][0]['tier'], 'advise')
        self.assertEqual(shard['roles'][0]['role_id'], row['slug'])
        self.assertIn('chief information officer', catalog['exact_role_domains'])
        self.assertEqual(result, g.project(registry))

    def test_project_empty_boundary_and_invalid_count_duplicate_unknown_specialist(self):
        self.assertEqual(json.loads(g.project({'version': '1', 'count': 0, 'roles': []})['catalog.json'])['domains'], [])
        for change in ('count', 'duplicate', 'tier'):
            source = self.fixture()
            if change == 'count': source['count'] = 2
            if change == 'duplicate': source['roles'] *= 2; source['count'] = 2
            if change == 'tier': source['roles'][0]['tool_tier'] = 'approve'
            with self.assertRaises(ValueError): g.project(source)
        with self.assertRaises(ValueError): g.project(self.fixture(), [{'role_id': 'missing'}])

    def test_run_integration_check_never_writes_and_detects_changed_shard(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory)
            (runtime / 'roles.json').write_text(json.dumps(self.fixture()))
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(g.run(runtime, check=True), 1)
            self.assertIn('Commercial catalog drift:', output.getvalue())
            self.assertFalse((runtime / 'commercial').exists())
            self.assertEqual(g.run(runtime), 0)
            self.assertEqual(g.run(runtime, check=True), 0)
            catalog = json.loads((runtime / 'commercial/catalog.json').read_text())
            shard = runtime / 'commercial' / catalog['domains'][0]['shard']
            shard.write_text('{}')
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(g.run(runtime, check=True), 1)
            self.assertEqual(output.getvalue().strip(), 'Commercial catalog drift: ' + catalog['domains'][0]['shard'])
            self.assertEqual(shard.read_text(), '{}')


    def test_main_cli_exits_with_real_projection_status(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory)
            (runtime / 'roles.json').write_text(json.dumps(self.fixture()))
            with patch('sys.argv', ['generate_commercial_catalog', '--runtime', directory]):
                with self.assertRaises(SystemExit) as outcome:
                    g.main()
            self.assertEqual(outcome.exception.code, 0)
            self.assertTrue((runtime / 'commercial/catalog.json').is_file())
