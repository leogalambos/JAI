#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
"""CI performance telemetry must never determine whether GA is published."""
from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class PerformanceReleaseSeparation(unittest.TestCase):
    def test_no_benchmark_in_any_release_gate(self):
        src = (ROOT/'.ai/runtime/tools/qualification_core.py').read_text()
        self.assertNotIn('"performance budget"', src)
        self.assertNotIn('performance_budget.py', src)
    def test_no_developer_baseline_or_report_in_sources(self):
        self.assertFalse((ROOT/'.ai/runtime/ci/performance-baseline.json').exists())
        self.assertFalse((ROOT/'.ai/runtime/_meta/performance-report.json').exists())
    def test_optional_benchmark_makes_no_release_claim(self):
        modpath = ROOT/'.ai/runtime/tools/performance_budget.py'
        spec = importlib.util.spec_from_file_location('perf_optional', modpath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        foreign = {'environment': {'python':'another', 'platform':'other'},'stages':[]}
        result = module.compare([{'name':'x','wall_time':1}], foreign, 20)
        self.assertEqual(result['status'], 'incomparable-environment')
        self.assertEqual(result['regressions'], [])
    def test_generated_validation_describes_actual_policy(self):
        content = (ROOT/'VALIDATION.md').read_text()
        self.assertNotIn('policy and performance.', content)
        self.assertIn('generated documentation and policy.', content)
if __name__ == '__main__':
    unittest.main()
