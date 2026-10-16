# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Commercial calculator acceptance and boundary tests; run by independent verifier."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/commercial_economics.py'
_SPEC = importlib.util.spec_from_file_location('commercial_economics', _PATH)
econ = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(econ)


def quote():
    return {'currency': 'EUR', 'input_versions': ['estimate:1', 'rate:1'], 'valid_until': '2026-12-31',
            'author': 'pricing-author', 'reviewer': 'pricing-checker', 'target_margin': '0.20',
            'labour': [{'effort_hours': '100', 'cost_rate': '80'}], 'non_labour': '1000',
            'explicit_overhead': '1000', 'reserves': [
                {'risk_id': 'risk-1', 'kind': 'contingency', 'amount': '2000', 'decision_ref': 'r1'},
                {'risk_id': 'risk-2', 'kind': 'management', 'amount': '500', 'decision_ref': 'r2'}],
            'invoice_lines': [{'list_price': '20000', 'volume_discount': '0.10',
                               'strategic_discount': '0.05', 'fixed_rebate': '100'}]}


def estimate(state='supported'):
    result = {'id': 'est-1', 'state': state, 'unit': 'h', 'owner': 'delivery', 'method': 'expert',
              'gate_deadline': '2026-11-01', 'as_of': '2026-10-16', 'input_versions': ['source:1']}
    if state in {'supported', 'provisional', 'conflicting', 'obsolete'}:
        result.update(interval={'low': '80', 'high': '120'}, source_ids=['src'], passage_ids=['pass'],
                      applicability={'technology': 'same platform'}, assumptions=['same scope'],
                      valid_until='2026-12-31', input_role='expert')
    return result


def bucket():
    return {'id': 'week', 'period': '2026-W42', 'skill_pool': 'support', 'region': 'CZ',
            'interchangeable': True, 'utilization_limit': '0.70', 'shrinkage': '0.20',
            'service_window_hours': '40', 'concurrent_seats': '1', 'cost_rate': '40',
            'currency': 'EUR', 'classes': [{'volume': '20', 'handle_hours': '0.5'}]}


class CommercialEconomicsTests(unittest.TestCase):
    def test_synthetic_quote_and_management_scenario(self):
        request = quote()
        result = econ.price_quote(request)
        for key, expected in {'direct_labour_cost': '8000', 'base_cost': '10000',
                              'risk_adjusted_cost': '12000', 'required_net_revenue': '15000',
                              'net_price': '17000.00', 'gross_profit': '5000.00'}.items():
            self.assertEqual(econ.Decimal(result[key]), econ.Decimal(expected))
        self.assertEqual(econ.Decimal(result['margin']).quantize(econ.Decimal('.0001')), econ.Decimal('.2941'))
        self.assertFalse(result['authorisation_granted'])
        self.assertEqual(request, quote())
        request['include_management_scenario'] = True
        self.assertEqual(econ.price_quote(request)['required_net_revenue'], '15625')

    def test_price_rejects_float_nonfinite_target_one_and_double_costs(self):
        for field, value in [('target_margin', 0.2), ('non_labour', 'NaN'), ('target_margin', '1')]:
            request = quote()
            request[field] = value
            with self.assertRaises(ValueError):
                econ.price_quote(request)
        request = quote()
        request['labour'][0]['loaded_components'] = ['overhead']
        with self.assertRaisesRegex(ValueError, 'overhead'):
            econ.price_quote(request)
        request = quote()
        request['reserves'][1]['risk_id'] = 'risk-1'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            econ.price_quote(request)

    def test_round_half_even_per_line_and_negative_price(self):
        request = quote()
        request['invoice_lines'] = [{'list_price': '1.005'}, {'list_price': '1.005'}]
        self.assertEqual(econ.price_quote(request)['net_price'], '2.00')
        request['invoice_lines'] = [{'list_price': '1', 'fixed_rebate': '2'}]
        with self.assertRaises(ValueError):
            econ.price_quote(request)

    def test_missing_and_refused_estimates_do_not_gain_numbers(self):
        for state in ['missing', 'requested', 'declined']:
            request = estimate(state)
            self.assertFalse(econ.validate_estimate(request)['fixed_price_eligible'])
            request['interval'] = {'low': '0', 'high': '10'}
            with self.assertRaises(ValueError):
                econ.validate_estimate(request)

    def test_supported_estimate_requires_passage_and_calibration_for_quantile(self):
        request = estimate()
        self.assertTrue(econ.validate_estimate(request)['fixed_price_eligible'])
        request['passage_ids'] = []
        with self.assertRaises(ValueError):
            econ.validate_estimate(request)
        request = estimate()
        request['quantile'] = '0.9'
        with self.assertRaises(ValueError):
            econ.validate_estimate(request)
        request = estimate()
        request['as_of'] = '2027-01-01'
        self.assertIn('estimate_expired', econ.validate_estimate(request)['blockers'])

    def test_supported_estimate_cannot_omit_assessment_date(self):
        request = estimate()
        request['valid_until'] = '2000-01-01'
        del request['as_of']
        with self.assertRaisesRegex(ValueError, 'as_of'):
            econ.validate_estimate(request)

    def test_invoice_cannot_reverse_more_than_its_amount(self):
        request = {'baseline_id': 'b', 'forecast_id': 'f', 'currency': 'EUR', 'approved_budget': '1000', 'etc': '0',
                   'actuals': [{'id': 'i', 'amount': '1', 'currency': 'EUR', 'period': 'm', 'evidence_id': 'e'}],
                   'accruals': [{'id': 'a', 'amount': '1000', 'currency': 'EUR', 'period': 'm', 'evidence_id': 'e'}],
                   'reversals': [{'id': 'r', 'accrual_id': 'a', 'actual_id': 'i', 'amount': '1000'}]}
        with self.assertRaisesRegex(ValueError, 'invoice'):
            econ.forecast(request)
        request['actuals'][0]['amount'] = '100'
        request['reversals'] = [{'id': 'r1', 'accrual_id': 'a', 'actual_id': 'i', 'amount': '60'},
                                {'id': 'r2', 'accrual_id': 'a', 'actual_id': 'i', 'amount': '60'}]
        with self.assertRaisesRegex(ValueError, 'aggregate'):
            econ.forecast(request)

    def test_learning_preserves_baseline_and_requires_accepted_stage(self):
        request = {'baseline_id': 'baseline-1', 'previous_forecast_id': 'f1', 'forecast_id': 'f2',
                   'stage_acceptance_id': 'a1', 'actual_id': 'actual1', 'actual_effort': '90',
                   'next_estimate': estimate(), 'decision_gate': 'pilot-exit', 'learning_cost': '300'}
        result = econ.learning_update(request)
        self.assertEqual(result['baseline_id'], 'baseline-1')
        self.assertTrue(result['human_required'])
        self.assertEqual(len(result['alternatives']), 5)
        request['forecast_id'] = 'f1'
        with self.assertRaises(ValueError):
            econ.learning_update(request)

    def test_shared_pool_detects_cross_engagement_conflict(self):
        request = {'pools': [{'pool_id': 'person1', 'period': 'week1', 'calendar_source': 'calendar:1',
                              'calendar_work_hours': '40', 'leave': '8'}], 'allocations': []}
        for engagement in ['project-a', 'project-b']:
            request['allocations'].append({'pool_id': 'person1', 'period': 'week1', 'engagement_id': engagement,
                'role': 'engineer', 'seniority': 'senior', 'sourcing': 'internal', 'work_package_id': 'wp',
                'effort_hours': '20', 'mix_rationale': 'critical review capacity'})
        result = econ.capacity_plan(request)
        self.assertFalse(result['feasible'])
        self.assertEqual(result['conflicts'][0]['available_hours'], '32')
        self.assertFalse(result['duration_proven'])
        request['pools'][0]['utilization'] = '.8'
        with self.assertRaises(ValueError):
            econ.capacity_plan(request)

    def test_service_synthetic_and_peak_bucket(self):
        request = {'buckets': [bucket()]}
        result = econ.service_sizing(request)
        self.assertEqual(result['buckets'][0]['paid_roster_hours'], '5E+1')
        self.assertEqual(econ.Decimal(result['buckets'][0]['roster_cost']), econ.Decimal('2000'))
        self.assertFalse(result['sla_proven'])
        peak = bucket()
        peak.update(id='peak', service_window_hours='1', shrinkage='0', utilization_limit='1', roster_paid_hours='1')
        result = econ.service_sizing({'buckets': [peak]})
        self.assertEqual(result['blockers'][0]['reason'], 'insufficient_roster')
        request['buckets'][0]['calendar_losses_already_deducted'] = True
        with self.assertRaises(ValueError):
            econ.service_sizing(request)

    def test_service_utilization_shrinkage_boundaries(self):
        for field, value in [('utilization_limit', '0'), ('shrinkage', '1'), ('shrinkage', '-.1')]:
            request = bucket()
            request[field] = value
            with self.assertRaises(ValueError):
                econ.service_sizing({'buckets': [request]})

    def test_allocation_reconciles_without_invented_taxonomy(self):
        request = {'quantity': '100', 'unit': 'h', 'period': 'week', 'source_id': 'wp1',
                   'dimension': 'CTB_RTB', 'allocation_basis': 'approved work split',
                   'allocations': [{'target': 'CTB', 'weight': '.6'}, {'target': 'RTB', 'weight': '.4'}]}
        result = econ.classify_quantity(request)
        self.assertEqual([econ.Decimal(item['quantity']) for item in result['targets']], [60, 40])
        request['allocations'][0]['weight'] = '.5'
        with self.assertRaises(ValueError):
            econ.classify_quantity(request)
        mapping = {'source_dimension': 'CTB_RTB', 'target_dimension': 'Run_Grow_Transform',
                   'source_value': 'CTB', 'target_value': 'Grow', 'rule_id': 'rule1', 'rule_version': '1',
                   'state': 'exact', 'reason': 'assumed', 'quantity': '100', 'unit': 'h', 'evidence_ids': ['e1']}
        with self.assertRaises(ValueError):
            econ.map_classification(mapping)
        mapping['state'] = 'ambiguous'
        self.assertEqual(econ.map_classification(mapping)['unmapped_quantity'], '100')

    def test_accrual_reversal_does_not_duplicate_invoice(self):
        request = {'baseline_id': 'b1', 'forecast_id': 'f1', 'currency': 'EUR',
                   'approved_budget': '1000', 'etc': '400',
                   'actuals': [{'id': 'i1', 'amount': '200', 'currency': 'EUR', 'period': 'month1', 'evidence_id': 'invoice1'}],
                   'accruals': [{'id': 'a1', 'amount': '200', 'currency': 'EUR', 'period': 'month1', 'evidence_id': 'service1'}],
                   'reversals': [{'id': 'r1', 'accrual_id': 'a1', 'actual_id': 'i1', 'amount': '200'}]}
        result = econ.forecast(request)
        self.assertEqual(result['eac'], '600')
        self.assertEqual(result['vac'], '400')
        self.assertTrue(result['baseline_unchanged'])
        request['reversals'][0]['amount'] = '201'
        with self.assertRaises(ValueError):
            econ.forecast(request)

    def test_cashflow_can_need_finance_despite_future_receipt_and_fx(self):
        request = {'currency': 'EUR', 'opening_cash': '0', 'events': [
            {'id': 'cost', 'amount': '100', 'currency': 'EUR', 'direction': 'out', 'expected_date': '2026-11-01', 'invoice_ref': 'i1'},
            {'id': 'revenue', 'amount': '200', 'currency': 'USD', 'direction': 'in', 'expected_date': '2026-12-01', 'invoice_ref': 'i2',
             'fx': {'rate': '.9', 'source': 'treasury1', 'as_of': '2026-10-16', 'from_currency': 'USD', 'to_currency': 'EUR', 'risk_owner': 'finance', 'rounding_policy': 'finance-policy1'}}]}
        result = econ.cashflow(request)
        self.assertEqual(result['financing_required'], '100')
        self.assertEqual(result['closing_cash'], '80.0')
        del request['events'][1]['fx']
        with self.assertRaises(ValueError):
            econ.cashflow(request)

    def test_contract_terms_unknown_block_and_review_is_not_signature(self):
        self.assertFalse(econ.validate_terms({})['binding_gate_ready'])
        terms = {field: {'owner': 'legal', 'deadline': '2026-11-01', 'state': 'agreed',
                          'reason': 'reviewed clause', 'human_review_ref': 'review1'} for field in econ._TERM_FIELDS}
        result = econ.validate_terms(terms)
        self.assertTrue(result['binding_gate_ready'])
        self.assertFalse(result['contractual_authorisation'])
        terms['payment']['state'] = 'unknown'
        self.assertIn('payment:unresolved', econ.validate_terms(terms)['blockers'])

    def test_uncertainty_reports_calibration_and_rejects_p90(self):
        request = {'scenarios': [{'name': 'stress', 'drivers': {'scope': 'high', 'delay': 'high'},
                     'correlation_groups': [['scope', 'delay']], 'cost': '120', 'revenue': '100'}],
                   'history': [{'forecast': '80', 'actual': '100', 'low': '70', 'high': '90',
                                'comparability': 'same scope', 'source_id': 'project1', 'outcome': 'failed'}]}
        result = econ.uncertainty_analysis(request)
        self.assertEqual(result['directional_bias'], '-20')
        self.assertEqual(result['interval_coverage'], '0')
        self.assertEqual(result['scenarios'][0]['profit'], '-20')
        request['quantiles'] = ['P90']
        with self.assertRaises(ValueError):
            econ.uncertainty_analysis(request)

    def test_monitor_thresholds_inclusive_and_human_stop_loss(self):
        values = {'eac': '100', 'margin': '.2', 'overdue_days': '0', 'capacity_shortfall_hours': '0',
                  'acceptance_failures': '0', 'sla_breaches': '0'}
        request = {'baseline_id': 'b1', 'previous_forecast_id': 'f1', 'threshold_owner': 'finance',
                   'threshold_decision_ref': 'human1', 'owner': 'delivery', 'deadline': '2026-11-01',
                   'thresholds': values, 'metrics': dict(values)}
        self.assertFalse(econ.monitor(request)['block_automatic_commitment'])
        request['metrics']['eac'] = '101'
        result = econ.monitor(request)
        self.assertTrue(result['human_required'])
        self.assertFalse(result['stop_loss_decided'])
        self.assertFalse(result['client_notice_authorised'])

    def test_cli_json_file_integration_and_error_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'quote.json'
            path.write_text(json.dumps(quote()))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(econ.main(['price', str(path)]), 0)
            self.assertEqual(json.loads(output.getvalue())['net_price'], '17000.00')
            path.write_text('{')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(econ.main(['price', str(path)]), 2)


if __name__ == '__main__':
    unittest.main()
