# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Pure immutable identity contracts; signed runtime cases live in governed tests."""
import sys
from pathlib import Path
import unittest
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.ai/runtime/tools'))
import lifecycle as lc


class LifecycleTests(unittest.TestCase):
    def test_canonical_unicode_collision_types_and_order(self):
        self.assertEqual(lc.normal('e\u0301'), 'é')
        self.assertEqual(lc.canonical({'é': '  A  '}), lc.canonical({'e\u0301': '  A  '}))
        self.assertNotEqual(lc.canonical([1, 2]), lc.canonical([2, 1]))
        for value in (1.5, float('nan'), {'é': 1, 'e\u0301': 2}, {1: 'bad'}):
            with self.assertRaises(lc.LifecycleError):
                lc.canonical(value)
        for raw in ('{"a":1,"a":2}', '{"é":1,"e\\u0301":2}', '1.5', 'NaN'):
            with self.assertRaises(lc.LifecycleError):
                lc.loads(raw)
        self.assertEqual(lc.loads('{}'), {})

    def test_identity_composite_and_distinct_conclusions(self):
        a = {'role': 'source', 'logical_id': 'a', 'version_id': 'v1'}
        b = {'role': 'source', 'logical_id': 'b', 'version_id': 'v2'}
        first = lc.manifest('subject', 'conclusion', {'text': 'x'}, members=[a, b])
        self.assertEqual(lc.version_id(first), lc.version_id(lc.manifest('subject', 'conclusion', {'text': 'x'}, members=[b, a])))
        self.assertNotEqual(lc.version_id(first), lc.version_id(lc.manifest('other', 'conclusion', {'text': 'x'}, members=[a, b])))
        self.assertNotEqual(lc.blob(b''), lc.blob(b' '))
        with self.assertRaises(lc.LifecycleError):
            lc.manifest('subject', 'conclusion', {}, members=[a, a])

@pytest.mark.parametrize('operations', [
    [{'op': 'version', 'data': {}}],
    [{'op': 'node', 'data': {}}],
    [{'op': 'governed', 'message': {}, 'effects': []}],
])
def test_low_level_commit_cannot_skip_signed_admission(tmp_path, operations):
    path = tmp_path / 'untrusted.jsonl'
    with pytest.raises(ValueError):
        lc.commit(path, 'untrusted', lc.ZERO, operations,
                  candidate_validator=lambda candidate: None)
    assert not path.exists()


def test_exact_manifest_identity_keeps_logical_identity_separate_from_versions():
    base = lc.manifest('claim', 'delivery.product', {'conclusion': 'supported'})
    changed = lc.manifest('claim', 'delivery.product', {'conclusion': 'contradicted'})
    assert base['logical_id'] == changed['logical_id']
    assert lc.version_id(base) != lc.version_id(changed)
    assert lc.version_id(base) == lc.version_id(lc.loads(lc.canonical(base)))
    assert lc.blob(lc.canonical(base)) != lc.version_id(base)
