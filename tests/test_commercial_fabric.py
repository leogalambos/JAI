# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Regression for typed forward impact and inverse implements dependencies."""
import importlib.util
from pathlib import Path
import unittest

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/fabric/fabric.py'
_SPEC = importlib.util.spec_from_file_location('commercial_fabric_impact', _PATH)
fabric = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fabric)


class CommercialFabricTests(unittest.TestCase):
    def test_refines_derives_and_inverse_implements_invalidate_products(self):
        entries = []
        for ident, kind in [('r1', 'req'), ('r2', 'req'), ('c1', 'ctr'), ('f1', 'frag'), ('f2', 'frag')]:
            entries.append({'op': 'node', 'seq': len(entries)+1, 'data': {'id': ident, 'type': kind, 'layer': 1}})
        for source, label, target in [('r1', 'derives', 'r2'), ('r2', 'refines', 'c1'),
                                       ('f1', 'implements', 'c1'), ('f1', 'supports', 'f2')]:
            entries.append({'op': 'edge', 'seq': len(entries)+1, 'data': {'src': source, 'label': label, 'dst': target}})
        graph = fabric.Fabric('test-readonly', entries)
        self.assertEqual(fabric.impact_dependents(graph, 'r1'), ['f1', 'f2'])
        self.assertEqual(fabric.impact_dependents(graph, 'f1'), ['f2'])

    def test_navigation_and_reviews_do_not_propagate(self):
        entries = [{'op': 'node', 'seq': 1, 'data': {'id': 'r', 'type': 'req', 'layer': 1}},
                   {'op': 'node', 'seq': 2, 'data': {'id': 'f', 'type': 'frag', 'layer': 1}},
                   {'op': 'edge', 'seq': 3, 'data': {'src': 'r', 'label': 'reviewed_by', 'dst': 'f'}}]
        self.assertEqual(fabric.impact_dependents(fabric.Fabric('test-readonly', entries), 'r'), [])


if __name__ == '__main__':
    unittest.main()
