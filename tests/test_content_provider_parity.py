# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Behavioral provider parity across the shared deterministic content CLI."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_eval import prepare_case
from content_spec import ContentSpec


class ContentProviderParityTests(unittest.TestCase):
    def test_both_provider_paths_produce_identical_content_reports(self):
        source = json.loads((ROOT / '.ai/runtime/evals/content_quality/adr-simple.json').read_text())
        model, spec = prepare_case(source, ContentSpec(ROOT))
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            semantic = directory / 'semantic.json'
            compiled = directory / 'compiled.json'
            semantic.write_text(json.dumps(model))
            compiled.write_text(json.dumps(spec))
            reports = []
            for provider in ('claude', 'codex'):
                output = directory / (provider + '.json')
                run = subprocess.run([sys.executable,
                    str(ROOT / '.ai/runtime/tools/content_lint.py'), 'check',
                    str(semantic), '--spec', str(compiled), '--output', str(output),
                    '--provider', provider], capture_output=True, text=True)
                self.assertEqual(0, run.returncode, run.stdout + run.stderr)
                reports.append(json.loads(output.read_text()))
            self.assertEqual(reports[0], reports[1])
            self.assertEqual(spec['compiled_spec_hash'], reports[0]['compiled_spec_hash'])
            self.assertFalse(reports[0]['production_ready'])


if __name__ == '__main__':
    unittest.main()
