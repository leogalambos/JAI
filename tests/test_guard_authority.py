# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Synthetic subprocess regressions for signing-directory recognition; no keys are accessed."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


HOOK = Path(__file__).resolve().parents[1] / ".ai/runtime/hooks/guard_authority.py"
SPEC = importlib.util.spec_from_file_location("guard_authority", HOOK)
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class GuardAuthorityTests(unittest.TestCase):
    """Exercise the hook process using synthetic paths rather than filesystem access."""

    def _decision(self, tool, value):
        field = "command" if tool in ("Bash", "PowerShell", "exec_command") else "file_path"
        result = subprocess.run(
            [sys.executable, str(HOOK), "--provider", "codex"],
            input=json.dumps({"tool_name": tool, "tool_input": {field: value}}),
            text=True, capture_output=True, check=True,
        )
        return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] if result.stdout else "allow"

    def test_documentation_and_component_lookalikes_are_allowed(self):
        for path in (f"docs/capabilities/{GUARD.KEY}.md", f"docs/{GUARD.KEY}/index.md",
                     f"/synthetic/.config/{GUARD.KEY}-backup/entry", f"/synthetic/my.config/{GUARD.KEY}/entry"):
            for tool in ("Bash", "PowerShell", "exec_command", "Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
                with self.subTest(path=path, tool=tool):
                    self.assertEqual("allow", self._decision(tool, path))

    def test_protected_directory_and_descendants_are_denied(self):
        for path in (f"~/.config/{GUARD.KEY}", f"/synthetic/.config/{GUARD.KEY}/entry",
                     f"C:\\synthetic\\.config\\{GUARD.KEY}\\entry", f".config/{GUARD.KEY}/"):
            for tool in ("Bash", "PowerShell", "exec_command", "Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
                with self.subTest(path=path, tool=tool):
                    self.assertEqual("deny", self._decision(tool, path))

    def test_shell_argument_boundaries_are_protected(self):
        for command in (f'cat "~/.config/{GUARD.KEY}"', f"cat ~/.config/{GUARD.KEY}; true",
                        f"cat ~/.config/{GUARD.KEY}|cat", f"KEY=~/.config/{GUARD.KEY}"):
            with self.subTest(command=command):
                self.assertEqual("deny", self._decision("Bash", command))


if __name__ == "__main__":
    unittest.main()
