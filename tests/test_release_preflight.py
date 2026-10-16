# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Regression coverage for source CI release preflight and prose width."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "human_text_width", ROOT / ".ai/runtime/tools/human_text_width.py"
)
WIDTH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WIDTH)


class ReleasePreflightTests(unittest.TestCase):
    def test_source_workflow_executes_full_release_gate_before_tagging(self):
        workflow = yaml.load(
            (ROOT / ".github/workflows/validate-library.yml").read_text(),
            Loader=yaml.BaseLoader,
        )
        self.assertIn("pull_request", workflow["on"])
        self.assertIn("main", workflow["on"]["push"]["branches"])
        job = workflow["jobs"].get("release-preflight")
        self.assertIsNotNone(job, "Source CI must exercise tag qualification")
        steps = job["steps"]
        self.assertTrue(any(s.get("uses") == "actions/checkout@v4" for s in steps))
        self.assertTrue(any(s.get("uses") == "./.github/actions/setup-qualification"
                            for s in steps))
        commands = "\n".join(s.get("run", "") for s in steps)
        self.assertIn("python3 -m mkdocs build --strict", commands)
        self.assertIn("python3 .ai/runtime/tools/release_ga.py qualify", commands)
        self.assertIn("python3 .ai/runtime/tools/release_bundle.py build --root . --dist dist", commands)
        self.assertIn("sha256sum -c", commands)
        self.assertNotIn("--through-g", commands)
        self.assertNotIn("gh release", commands)
        self.assertNotIn("contents: write", yaml.dump(job))

    def test_current_human_documentation_meets_release_width(self):
        self.assertEqual(WIDTH.check(ROOT), [])

    def test_width_accepts_empty_and_exact_boundary_and_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(WIDTH.check(root), [])
            document = root / "README.md"
            document.write_text("x" * 72 + "\n", encoding="utf-8")
            self.assertEqual(WIDTH.check(root), [])
            document.write_text("x" * 73 + "\n", encoding="utf-8")
            self.assertEqual(WIDTH.check(root), ["README.md:1: 73 characters"])


if __name__ == "__main__":
    unittest.main()
