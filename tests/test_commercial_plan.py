# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Executable approved task-DAG regression fixtures."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('commercial_plan',ROOT/'.ai/runtime/tools/commercial_plan.py')
p=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
class CommercialPlanTests(unittest.TestCase):
    def test_approved_plan_and_negative_fixtures(self):
        plan=p.load_plan(ROOT/'.ai/runtime/commercial/implementation-plan.json',fixture=True)
        self.assertEqual(len(p.validate_plan(plan)),22)
        for field,value in [('depends_on',['T22']),('depends_on',['T99']),('reviewer',plan['tasks'][0]['producer']),('acceptance',[])]:
            invalid=copy.deepcopy(plan)
            invalid['tasks'][0][field]=value
            with self.assertRaises(ValueError):p.validate_plan(invalid)
    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'fixture.json';path.write_text('{"a":1,"a":2}')
            with self.assertRaises(ValueError):p.load_plan(path,fixture=True)
