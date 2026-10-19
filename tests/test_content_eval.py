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
from content_eval import evaluate_corpus, prepare_case, catalogue_coverage
from content_mutations import apply_variant
from content_spec import ContentSpec


class ContentEvalTests(unittest.TestCase):
    def test_detector_without_findings_cannot_pass_seeded_recall(self):
        report = evaluate_corpus(ROOT, detector=lambda model, spec: {
            'findings': [], 'gate_verdict': 'DRAFT_INCOMPLETE'}, include_enterprise=False)
        self.assertFalse(report['pilot_pass'])
        self.assertEqual(0, report['critical_recall'])
        self.assertGreater(report['false_negatives'], 0)
        self.assertEqual(300, len(report['cases']))

    def test_detector_false_positives_use_reference_denominator(self):
        def noisy(model, spec):
            return {'findings': [{'rule_id': 'always-fail',
                    'category': 'critical-content'}], 'gate_verdict': 'CONTENT_FAIL'}
        report = evaluate_corpus(ROOT, detector=noisy, include_enterprise=False)
        self.assertEqual(30, report['counts']['reference_count'])
        self.assertEqual(1.0, report['reference_false_positive_rate'])
        self.assertFalse(report['pilot_pass'])

    def test_actual_validator_meets_synthetic_thresholds_reproducibly(self):
        first = evaluate_corpus(ROOT, include_enterprise=False)
        second = evaluate_corpus(ROOT, include_enterprise=False)
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

    def test_every_registered_dimension_has_actual_three_way_evaluation(self):
        report = evaluate_corpus(ROOT)
        self.assertTrue(report['pilot_pass'], report['counts'])
        coverage = report['catalogue_coverage']
        self.assertFalse(coverage['professional_acceptance'])
        self.assertTrue(coverage['all_development_dimensions_covered'])
        for dimension, expected in [('bindings', 1139), ('artifact_types', 28),
                                    ('archetypes', 13), ('sabsa_views', 19),
                                    ('domains', 6)]:
            self.assertEqual(expected, coverage['dimensions'][dimension]['covered'])
            self.assertEqual([], coverage['dimensions'][dimension]['gaps'])
        self.assertEqual(0, report['all_seeded_rule_misses'])

    def test_declarations_without_detector_observations_do_not_count_as_coverage(self):
        resolver = ContentSpec(ROOT)
        empty = catalogue_coverage(resolver, [])
        self.assertFalse(empty['all_development_dimensions_covered'])
        self.assertEqual(0, empty['dimensions']['bindings']['covered'])
        self.assertEqual(1139, len(empty['dimensions']['bindings']['gaps']))
        only_positive = [{'contract_id': cid, 'spec_ids': list(resolver.specs),
                          'positive': True, 'negative': False, 'borderline': False}
                         for cid in list(resolver.bindings)[:1]]
        declared = catalogue_coverage(resolver, only_positive)
        self.assertFalse(declared['all_development_dimensions_covered'])
        self.assertEqual(0, declared['dimensions']['artifact_types']['covered'])

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
