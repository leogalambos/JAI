# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Reference adapters retain dry-run workflows and reject forged local authority."""
import contextlib
import io
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import integration_adapters as adapters


class IntegrationAdapterBoundaryTests(unittest.TestCase):
    def test_reference_read_draft_query_validate_propose_workflows(self):
        self.assertTrue(adapters.load(adapters.REGISTRY)['adapters'])
        self.assertFalse(adapters.validate_contracts())
        adapter = adapters.ReferenceAdapter('itsm-cmdb')
        self.assertEqual(adapter.discover()['category'], 'itsm-cmdb')
        self.assertIsNone(adapter.read('missing'))
        self.assertEqual(adapter.query('all'), [])
        self.assertFalse(adapter.validate('missing'))
        with self.assertRaises(ValueError):
            adapter.propose_change('missing')
        draft = adapter.create_draft({'scope': 'service:example', 'payload': 'dry-run'})
        self.assertTrue(adapter.validate(draft['digest']))
        self.assertEqual(adapter.propose_change(draft['digest'])['status'], 'proposed')
        self.assertEqual(len(adapter.query('all')), 1)
        self.assertFalse(adapter.verify(draft['digest']))
        for approval in (None, {}, {'approver': 'human', 'digest': draft['digest'], 'scope': 'service:example'}):
            with self.assertRaises(PermissionError):
                adapter.execute_approved_change(draft['digest'], approval)
            with self.assertRaises(PermissionError):
                adapter.rollback(draft['digest'], approval)
            self.assertEqual(adapter.read(draft['digest'])['status'], 'draft')
            self.assertEqual(adapter.audit[-1]['decision'], 'DENY')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(adapters.self_test(), 0)


if __name__ == '__main__':
    unittest.main()
