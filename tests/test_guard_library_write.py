# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Defense-in-depth hook never treats agent-written JSON as external approval."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/hooks/guard_library_write.py'
SPEC = importlib.util.spec_from_file_location('library_guard_test', PATH)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class LibraryGuardTests(unittest.TestCase):
    def test_local_approval_files_never_authorize(self):
        with tempfile.TemporaryDirectory() as directory:
            approval = Path(directory) / 'APPROVAL.json'
            approval.write_text(json.dumps({'approver': 'human', 'scope': [directory], 'expires_epoch': 99999999999}))
            with patch.object(guard, 'APPROVAL', str(approval)):
                self.assertFalse(guard.approval_covers(directory)[0])
                approval.write_text('{')
                self.assertFalse(guard.approval_covers(directory)[0])
                approval.unlink()
                self.assertFalse(guard.approval_covers(directory)[0])

    def test_hook_target_inventory_is_defense_in_depth_only(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(guard, 'LIB', directory):
            self.assertEqual(guard.owned(), (set(), set()))
            self.assertTrue(guard.protected(directory + '/file'))
            self.assertFalse(guard.protected('/different/file'))
            for name in ('.git','policy','approvals','.fabric'):
                self.assertTrue(guard.protected('/different/'+name+'/object'))
            self.assertTrue(guard.under(directory + '/child', directory))
            self.assertFalse(guard.under(directory + '-other', directory))
            self.assertIsNone(guard.target({}))
            self.assertEqual(guard.target({'tool_input': {'path': directory}}), directory)
            self.assertEqual(guard.targets({'tool_name': 'apply_patch', 'cwd': directory,
                'tool_input': {'command': '*** Update File: file.txt'}}), [directory + '/file.txt'])
            self.assertEqual(guard.targets({}), [])


if __name__ == '__main__':
    unittest.main()
