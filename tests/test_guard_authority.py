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

    def test_patch_command_examples_are_data_and_protected_patch_targets_are_denied(self):
        import io
        from unittest.mock import patch
        signing = ' '.join(('python3', 'operator_actions.py', 'sign', 'synthetic-request.json'))
        acceptance = ' '.join(('python3', 'fabric.py', 'review', 'synthetic', 'frag-1', '--layer', '0'))
        applying = ' '.join(('python3', 'fabric.py', 'lifecycle-apply', '--request', 'synthetic.json'))
        for command in (signing, acceptance, applying):
            edit = '\n'.join(('*** Begin Patch', '*** Update File: docs/reference/lifecycle.md', '@@', '+' + command, '*** End Patch'))
            for payload in (edit, {'command': edit}, {'patch': edit}, {'input': edit}):
                event = {'tool_name': 'apply_patch', 'tool_input': payload}
                with patch.object(sys, 'stdin', io.StringIO(json.dumps(event))), patch.object(sys, 'stdout', io.StringIO()) as output:
                    self.assertEqual(GUARD.main(), 0)
                    self.assertEqual(output.getvalue(), '')
            self.assertEqual(self._decision('exec_command', command), 'deny')
        for path in ('.fabric/case.jsonl', '.findings/review.jsonl', '.ai/jai-operator-trust.json', '/synthetic/.ai/jai-operator-trust.json',
                     '/synthetic/.config/' + GUARD.KEY + '/key'):
            edit = '\n'.join(('*** Begin Patch', '*** Update File: ' + path, '@@', '+data', '*** End Patch'))
            event = {'tool_name': 'apply_patch', 'tool_input': {'patch': edit}}
            with patch.object(sys, 'stdin', io.StringIO(json.dumps(event))), patch.object(sys, 'stdout', io.StringIO()) as output:
                self.assertEqual(GUARD.main(), 0)
                self.assertEqual(json.loads(output.getvalue())['hookSpecificOutput']['permissionDecision'], 'deny')

    def test_relative_and_absolute_trust_pin_edit_targets_are_denied(self):
        for path in ('.ai/jai-operator-trust.json', '/synthetic/.ai/jai-operator-trust.json'):
            for tool in ('Write', 'Edit', 'MultiEdit', 'NotebookEdit'):
                self.assertEqual(self._decision(tool, path), 'deny')

    def test_malformed_patch_fails_closed_and_cmd_alias_is_guarded(self):
        import io
        from unittest.mock import patch
        events = [
            {'tool_name': 'apply_patch', 'tool_input': {'patch': 'unstructured text'}},
            {'tool_name': 'exec_command', 'tool_input': {'cmd': ' '.join(('python3', 'operator_actions.py', 'sign', 'synthetic.json'))}}]
        for event in events:
            with patch.object(sys, 'stdin', io.StringIO(json.dumps(event))), patch.object(sys, 'stdout', io.StringIO()) as output:
                self.assertEqual(GUARD.main(), 0)
                self.assertEqual(json.loads(output.getvalue())['hookSpecificOutput']['permissionDecision'], 'deny')


if __name__ == "__main__":
    unittest.main()
