# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Regression coverage for SABSA-owned file resource lifetimes."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


_PROBE = '''
import gc
import importlib
from pathlib import Path
import sys
import tempfile
import warnings
sys.path.insert(0, sys.argv[1])
tempfile.tempdir = sys.argv[2]
with warnings.catch_warnings(record=True) as observed:
    warnings.simplefilter("always", ResourceWarning)
    module = importlib.import_module("sabsa")
    if sys.argv[3] == "selftest":
        assert module.cmd_selftest(None) == 0, "SABSA selftest failed"
    else:
        workspace = Path(sys.argv[2])
        entry = workspace / "entry.md"
        entry.write_text("---\\nname: Příliš\\n---\\n\\nBusiness intent.\\n", encoding="utf-8")
        parsed = module.parse(str(entry))
        assert parsed == {"name": "Příliš", "_body": "Business intent."}, parsed
        entry.write_text("", encoding="utf-8")
        try:
            module.parse(str(entry))
        except module.SabsaError as exc:
            assert "no front matter" in str(exc), str(exc)
        else:
            raise AssertionError("Empty input accepted")
        entry.write_text("---\\nname: unfinished", encoding="utf-8")
        try:
            module.parse(str(entry))
        except module.SabsaError as exc:
            assert "front matter not closed" in str(exc), str(exc)
        else:
            raise AssertionError("Unterminated front matter accepted")
        missing = workspace / "missing.md"
        try:
            module.parse(str(missing))
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Missing input accepted")
        config, problems = module.load_reuse_config(str(workspace))
        assert config == {"schema": 1, "libraries": []} and not problems
        (workspace / module.REUSE_FILE).write_text("{", encoding="utf-8")
        config, problems = module.load_reuse_config(str(workspace))
        assert config == {"schema": 1, "libraries": []}, config
        assert len(problems) == 1 and "cannot parse" in problems[0], problems
        target = workspace / "missing-directory" / "matrix.md"
        original = module.cell_path
        module.cell_path = lambda *args: str(target)
        try:
            module.scaffold_cell(str(workspace), "contextual", "what")
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Missing output directory silently accepted")
        finally:
            module.cell_path = original
    gc.collect()
resource_warnings = [str(item.message) for item in observed
                     if issubclass(item.category, ResourceWarning)]
assert not resource_warnings, "Unclosed owned files: " + repr(resource_warnings)
'''


class SabsaResourcesTest(unittest.TestCase):
    """Exercise import and real operations in isolated interpreters."""

    def _probe(self, scenario):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as workspace:
            return subprocess.run(
                [sys.executable, '-c', _PROBE,
                 str(root / '.ai/runtime/tools'), workspace, scenario],
                cwd=root, capture_output=True, text=True, timeout=180)

    def test_import_and_selftest_close_owned_files(self):
        """Capture warnings rather than turning finalizer warnings into errors."""
        completed = self._probe('selftest')
        self.assertEqual(completed.returncode, 0,
                         completed.stdout + completed.stderr)

    def test_parse_and_file_failure_paths_close_owned_files(self):
        """Keep UTF-8 content and existing parse, JSON and filesystem errors."""
        completed = self._probe('boundaries')
        self.assertEqual(completed.returncode, 0,
                         completed.stdout + completed.stderr)


if __name__ == '__main__':
    unittest.main()
