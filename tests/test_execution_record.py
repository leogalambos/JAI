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
    def test_schema_hash_chain_and_local_tamper_detection(self):
        binding = records.jai_binding('author', [], [])
        self.assertEqual(binding['layer'], 6)
        self.assertEqual(records.canonical({'b': 1, 'a': 2}), b'{"a":2,"b":1}')
        first = records.make(agent='author')
        self.assertEqual(records.digest_record(first), first['record_hash'])
        self.assertTrue(records.validate(first))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'events.jsonl'
            records.append(path, first)
            records.append(path, records.make(agent='reviewer'))
            self.assertEqual(records.verify(path), 2)
            rows = path.read_text().splitlines()
            modified = json.loads(rows[0])
            modified['agent'] = 'tampered'
            rows[0] = json.dumps(modified)
            path.write_text('\n'.join(rows) + '\n')
            with self.assertRaises(ValueError):
                records.verify(path)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(records.self_test(), 0)
        self.assertIn('local storage remains mutable', output.getvalue())


if __name__ == '__main__':
    unittest.main()
