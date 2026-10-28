# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""ExecutionRecord compatibility and tamper detection do not imply immutable storage."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import execution_record as records


class ExecutionRecordTests(unittest.TestCase):
    def test_schema_chain_order_deletion_truncation_and_selftest_contract(self):
        binding = records.jai_binding('author', [], [])
        self.assertEqual(binding['layer'], 6)
        self.assertEqual(records.canonical({'b': 1, 'a': 2}), b'{"a":2,"b":1}')
        first = records.make(agent='author')
        self.assertEqual(records.digest_record(first), first['record_hash'])
        self.assertTrue(records.validate(first))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'events.jsonl'
            for agent in ('author', 'reviewer', 'observer'):
                records.append(path, records.make(agent=agent))
            self.assertEqual(records.verify(path), 3)
            rows = path.read_text().splitlines()
            corruptions = {
                'reordered': [rows[1], rows[0], rows[2]],
                'middle-record-deleted': [rows[0], rows[2]],
                'truncated-json-record': [rows[0], rows[1], rows[2][:-1]],
            }
            for scenario, corrupted in corruptions.items():
                with self.subTest(scenario=scenario):
                    path.write_text('\n'.join(corrupted) + '\n')
                    with self.assertRaises(ValueError):
                        records.verify(path)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(records.self_test(), 0)
        self.assertIn('local storage remains mutable', output.getvalue())


if __name__ == '__main__':
    unittest.main()
