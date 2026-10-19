# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Regression tests for actual-detector pilot metrics and mutation isolation."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_eval import evaluate_corpus, prepare_case
from content_mutations import apply_variant
from content_spec import ContentSpec


class ContentEvalTests(unittest.TestCase):
    def test_detector_without_findings_cannot_pass_seeded_recall(self):
        report = evaluate_corpus(ROOT, detector=lambda model, spec: {
            'findings': [], 'gate_verdict': 'DRAFT_INCOMPLETE'})
        self.assertFalse(report['pilot_pass'])
        self.assertEqual(0, report['critical_recall'])
        self.assertGreater(report['false_negatives'], 0)
        self.assertEqual(300, len(report['cases']))

    def test_detector_false_positives_use_reference_denominator(self):
        def noisy(model, spec):
            return {'findings': [{'rule_id': 'always-fail',
                    'category': 'critical-content'}], 'gate_verdict': 'CONTENT_FAIL'}
        report = evaluate_corpus(ROOT, detector=noisy)
        self.assertEqual(30, report['counts']['reference_count'])
        self.assertEqual(1.0, report['reference_false_positive_rate'])
        self.assertFalse(report['pilot_pass'])

    def test_actual_validator_meets_synthetic_thresholds_reproducibly(self):
        first = evaluate_corpus(ROOT)
        second = evaluate_corpus(ROOT)
        self.assertEqual(first['evaluation_hash'], second['evaluation_hash'])
        self.assertTrue(first['pilot_pass'], first['counts'])
        self.assertFalse(first['human_gold'])
        self.assertFalse(first['production_ready'])
        self.assertGreaterEqual(first['critical_recall'], .95)
        self.assertGreaterEqual(first['critical_case_recall'], .95)
        self.assertEqual(0, first['segregation_of_duties_probes']['sod_escapes'])
        self.assertTrue(first['segregation_of_duties_probes']['positive_control_accepted'])
        self.assertEqual(6, first['segregation_of_duties_probes']['adversarial_count'])
        self.assertLessEqual(first['reference_false_positive_rate'], .10)

    def test_mutation_and_binding_preserve_reference(self):
        source = json.loads((ROOT / '.ai/runtime/evals/content_quality/adr-simple.json').read_text())
        original = copy.deepcopy(source)
        mutated = apply_variant(source, source['variants'][2])
        model, spec = prepare_case(mutated, ContentSpec(ROOT))
        self.assertEqual(source, original)
        self.assertNotIn('decision_context', model['semantic_units'])
        self.assertEqual(model['contract_id'], spec['artifact_id'])
        self.assertEqual(model['compiled_spec_hash'], spec['compiled_spec_hash'])
        with self.assertRaises(ValueError):
            apply_variant(source, {'operation': 'unsupported'})


if __name__ == '__main__':
    unittest.main()
