# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Regression for typed forward impact and inverse implements dependencies."""
import importlib.util
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/fabric/fabric.py'
_SPEC = importlib.util.spec_from_file_location('commercial_fabric_impact', _PATH)
fabric = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fabric)


class CommercialFabricTests(unittest.TestCase):
    def test_refines_derives_and_inverse_implements_invalidate_products(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric, 'FABRIC_DIR', directory):
            graph = fabric.Fabric('impact', [])
            r1 = graph.add_node('req', 1, 'Parent requirement')['id']
            r2 = graph.add_node('req', 1, 'Refined requirement')['id']
            c1 = graph.add_node('ctr', 1, 'Derived contract')['id']
            f1 = graph.add_node('frag', 2, 'Implementation')['id']
            f2 = graph.add_node('frag', 1, 'Supported conclusion')['id']
            for source, label, target in [(r1, 'refines', r2), (r2, 'derives', c1),
                                           (f1, 'implements', c1), (f1, 'supports', f2)]:
                graph.add_edge(source, label, target)
            graph = fabric.Fabric('impact', fabric.load('impact'))
            self.assertEqual(fabric.impact_dependents(graph, r1), [f1, f2])
            self.assertEqual(fabric.impact_dependents(graph, f1), [f2])

    def test_navigation_and_reviews_do_not_propagate(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric, 'FABRIC_DIR', directory):
            graph = fabric.Fabric('navigation', [])
            fragment = graph.add_node('frag', 2, 'Reviewed subject')['id']
            review = graph.add_node('rev', 1, 'Independent review', state='accepts')['id']
            graph.add_edge(fragment, 'reviewed_by', review)
            graph = fabric.Fabric('navigation', fabric.load('navigation'))
            self.assertEqual(fabric.impact_dependents(graph, fragment), [])


if __name__ == '__main__':
    unittest.main()
