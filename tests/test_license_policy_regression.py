#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Verify the same licensing policy during unit tests as during Gate H."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LICENSE_CHECK = ROOT / '.ai/runtime/tools/license_check.py'


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
