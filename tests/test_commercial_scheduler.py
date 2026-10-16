# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Dependency/calendar scheduling and service roster acceptance tests."""
import copy
import importlib.util
from pathlib import Path
import unittest

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/commercial_scheduler.py'
_SPEC = importlib.util.spec_from_file_location('commercial_scheduler', _PATH)
scheduler = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(scheduler)


def task(ident='design', pool='engineer', effort='2', dependencies=None):
    return {'id': ident, 'phase': 'design', 'engagement_id': 'e1', 'pool_id': pool,
            'skill': 'design', 'region': 'CZ', 'effort_hours': effort, 'dependencies': dependencies or []}


def calendar(ident='mon', pool='engineer', day='19', capacity='8'):
    return {'id': ident, 'pool_id': pool, 'start': f'2026-10-{day}T09:00:00+00:00',
            'end': f'2026-10-{day}T17:00:00+00:00', 'capacity_hours': capacity,
            'skills': ['design'], 'region': 'CZ', 'external_reservations': []}


def request():
    return {'start': '2026-10-19T09:00:00+00:00', 'tasks': [task()], 'calendars': [calendar()]}


class CommercialSchedulerTests(unittest.TestCase):
    def test_dependency_schedule_waits_for_calendar_and_review_bottleneck(self):
        value = request()
        value['tasks'] = [task(effort='8'), task('review', 'reviewer', '2', ['design']), task('deliver', 'engineer', '1', ['review'])]
        value['calendars'] += [calendar('review-next', 'reviewer', '20'), calendar('eng-next', 'engineer', '20')]
        result = scheduler.schedule(value)
        self.assertTrue(result['feasible'])
        self.assertEqual(result['tasks'][-1]['earliest_finish'], '2026-10-20T12:00:00+00:00')
        self.assertEqual(result['tasks'][1]['allocations'][0]['start'], '2026-10-20T09:00:00+00:00')
        self.assertFalse(result['optimality_proven'])

    def test_external_reservation_shared_engagement_and_no_doublebooking(self):
        value = request()
        value['calendars'][0]['external_reservations'] = [{'engagement_id': 'external', 'hours': '4'}]
        value['tasks'] = [task(effort='3'), task('other-project', effort='2')]
        value['tasks'][1]['engagement_id'] = 'e2'
        result = scheduler.schedule(value)
        self.assertFalse(result['feasible'])
        self.assertEqual(result['tasks'][0]['allocations'][0]['start'], '2026-10-19T13:00:00+00:00')
        self.assertEqual(result['blockers'][0]['missing_hours'], '1')

    def test_parallel_pool_and_explicit_window_wait(self):
        value = request()
        second = task('other', 'otherpool', '2')
        second['not_before'] = '2026-10-19T12:00:00+00:00'
        second['wait_hours'] = '1'
        value['tasks'].append(second)
        value['calendars'].append(calendar('otherpool-day', 'otherpool'))
        result = scheduler.schedule(value)
        self.assertEqual(result['tasks'][1]['allocations'][0]['start'], '2026-10-19T13:00:00+00:00')
        self.assertEqual(result['tasks'][0]['earliest_finish'], '2026-10-19T11:00:00+00:00')

    def test_cycles_dangling_and_overlapping_calendars_rejected(self):
        value = request()
        value['tasks'][0]['dependencies'] = ['design']
        with self.assertRaisesRegex(ValueError, 'cycle'):
            scheduler.schedule(value)
        value['tasks'][0]['dependencies'] = ['missing']
        with self.assertRaisesRegex(ValueError, 'dangling'):
            scheduler.schedule(value)
        value = request()
        value['calendars'].append(calendar('overlap'))
        with self.assertRaisesRegex(ValueError, 'overlapping'):
            scheduler.schedule(value)

    def test_missing_skill_deadline_and_dependency_are_blockers(self):
        value = request()
        value['calendars'][0]['skills'] = ['different']
        value['tasks'].append(task('dependent', dependencies=['design']))
        result = scheduler.schedule(value)
        self.assertEqual([item['reason'] for item in result['blockers']], ['unknown_or_insufficient_capacity', 'dependency_not_scheduled'])
        value = request()
        value['tasks'][0]['deadline'] = value['start']
        self.assertEqual(scheduler.schedule(value)['blockers'][0]['reason'], 'deadline_infeasible')

    def test_zero_effort_empty_plan_and_timezone_boundary(self):
        value = request()
        value['tasks'][0]['effort_hours'] = '0'
        self.assertTrue(scheduler.schedule(value)['feasible'])
        value['tasks'] = []
        self.assertEqual(scheduler.schedule(value)['tasks'], [])
        value['start'] = '2026-10-19T09:00:00'
        with self.assertRaisesRegex(ValueError, 'timezone'):
            scheduler.schedule(value)

    def test_service_minimum_no_duplicate_workload_and_backup(self):
        bucket = {'id': 'week', 'period': '2026-W42', 'skill_pool': 'support', 'region': 'CZ',
                  'interchangeable': True, 'utilization_limit': '.70', 'shrinkage': '.20',
                  'service_window_hours': '40', 'concurrent_seats': '1', 'cost_rate': '40', 'currency': 'EUR',
                  'classes': [{'volume': '20', 'handle_hours': '.5'}]}
        value = {'sizing': {'buckets': [bucket]}, 'shifts': [
            {'worker_id': 'primary', 'bucket_id': 'week', 'skill_pool': 'support', 'region': 'CZ',
             'paid_hours': '50', 'active_hours': '40', 'mode': 'active', 'backup_worker_id': 'backup'},
            {'worker_id': 'backup', 'bucket_id': 'week', 'skill_pool': 'support', 'region': 'CZ',
             'paid_hours': '0', 'active_hours': '0', 'mode': 'on_call', 'backup_worker_id': 'primary',
             'activation_hours': '.1', 'response_limit_hours': '.25', 'rest_hours': '11', 'reachable': True}]}
        result = scheduler.validate_service_roster(value)
        self.assertEqual(scheduler.Decimal(result['sizing']['buckets'][0]['roster_cost']), 2000)
        self.assertTrue(result['feasible_aggregate_roster'])
        self.assertFalse(result['sla_proven'])
        value['shifts'][0]['mode'] = 'on_call'
        result = scheduler.validate_service_roster(value)
        self.assertFalse(result['feasible_aggregate_roster'])
        self.assertIn('on_call_is_not_active_coverage', [item['reason'] for item in result['blockers']])

    def test_contractual_five_day_windows_reconcile_actual_roster_hours(self):
        windows = [{'start': f'2026-10-{day}T09:00:00+02:00', 'end': f'2026-10-{day}T17:00:00+02:00'} for day in range(19, 24)]
        bucket = {'id': 'week', 'period': 'week', 'skill_pool': 'support', 'region': 'CZ',
                  'interchangeable': True, 'utilization_limit': '.7', 'shrinkage': '.2',
                  'service_window_hours': '40', 'concurrent_seats': '1', 'cost_rate': '40', 'currency': 'EUR',
                  'classes': [{'volume': '20', 'handle_hours': '.5'}],
                  'required_windows': windows, 'contractual_source_version': 'signed-contract:1'}
        primary = {'worker_id': 'primary', 'bucket_id': 'week', 'skill_pool': 'support', 'region': 'CZ',
                   'paid_hours': '50', 'active_hours': '40', 'mode': 'active', 'backup_worker_id': 'backup',
                   'coverage_windows': copy.deepcopy(windows)}
        backup = {'worker_id': 'backup', 'bucket_id': 'week', 'skill_pool': 'support', 'region': 'CZ',
                  'paid_hours': '0', 'active_hours': '0', 'mode': 'on_call', 'backup_worker_id': 'primary',
                  'activation_hours': '.1', 'response_limit_hours': '.25', 'rest_hours': '11', 'reachable': True}
        value = {'sizing': {'buckets': [bucket]}, 'shifts': [primary, backup]}
        result = scheduler.validate_service_roster(value)
        self.assertTrue(result['roster_ready'])
        self.assertTrue(result['interval_coverage_verified'])
        primary['coverage_windows'] = [{'start': windows[0]['start'], 'end': '2026-10-19T09:01:00+02:00'}]
        value['coverage_intervals'] = [{'id': 'forged', 'start': windows[0]['start'], 'end': '2026-10-19T09:01:00+02:00',
                                        'required_seats': '1', 'skill_pool': 'support', 'region': 'CZ'}]
        result = scheduler.validate_service_roster(value)
        self.assertFalse(result['roster_ready'])
        self.assertIn('active_hours_window_mismatch', [item['reason'] for item in result['interval_blockers']])
        primary['coverage_windows'] = copy.deepcopy(windows[:-1])
        primary['active_hours'] = '32'
        self.assertFalse(scheduler.validate_service_roster(value)['roster_ready'])
        primary['coverage_windows'] = copy.deepcopy(windows)
        primary['active_hours'] = '40'
        del bucket['required_windows']
        self.assertFalse(scheduler.validate_service_roster(value)['roster_ready'])

    def test_overnight_timezone_and_seat_capacity_reconciliation(self):
        windows = [{'start': '2026-10-19T22:00:00+02:00', 'end': '2026-10-20T06:00:00+02:00'}]
        bucket = {'id': 'night', 'period': 'night', 'skill_pool': 'support', 'region': 'CZ',
                  'interchangeable': True, 'utilization_limit': '1', 'shrinkage': '0',
                  'service_window_hours': '8', 'concurrent_seats': '1', 'cost_rate': '40', 'currency': 'EUR',
                  'required_windows': windows, 'contractual_source_version': 'contract:2'}
        shift = {'worker_id': 'primary', 'bucket_id': 'night', 'skill_pool': 'support', 'region': 'CZ',
                 'paid_hours': '8', 'active_hours': '8', 'mode': 'active', 'backup_worker_id': 'backup',
                 'coverage_windows': [{'start': '2026-10-19T20:00:00+00:00', 'end': '2026-10-20T04:00:00+00:00'}]}
        backup = dict(shift, worker_id='backup', mode='on_call', paid_hours='0', active_hours='0',
                      backup_worker_id='primary', coverage_windows=[], activation_hours='.1', response_limit_hours='.2', rest_hours='11', reachable=True)
        value = {'sizing': {'buckets': [bucket]}, 'shifts': [shift, backup]}
        self.assertTrue(scheduler.validate_service_roster(value)['roster_ready'])
        bucket['concurrent_seats'] = '2'
        self.assertFalse(scheduler.validate_service_roster(value)['roster_ready'])
        bucket['concurrent_seats'] = '1'
        bucket['service_window_hours'] = '40'
        reasons = [item['reason'] for item in scheduler.validate_service_roster(value)['interval_blockers']]
        self.assertIn('contractual_window_hours_mismatch', reasons)

    def test_roster_peak_and_skill_mismatch_block(self):
        bucket = {'id': 'peak', 'period': 'peak', 'skill_pool': 'support', 'region': 'CZ',
                  'interchangeable': True, 'utilization_limit': '1', 'shrinkage': '0',
                  'service_window_hours': '1', 'concurrent_seats': '2', 'cost_rate': '40', 'currency': 'EUR',
                  'classes': [{'volume': '4', 'handle_hours': '.5'}]}
        value = {'sizing': {'buckets': [bucket]}, 'shifts': [
            {'worker_id': 'primary', 'bucket_id': 'peak', 'skill_pool': 'other', 'region': 'CZ',
             'paid_hours': '1', 'active_hours': '1', 'mode': 'active', 'backup_worker_id': 'backup'}]}
        reasons = [item['reason'] for item in scheduler.validate_service_roster(value)['blockers']]
        self.assertIn('skill_or_region_mismatch', reasons)
        self.assertIn('interval_staffing_shortfall', reasons)
        bucket['contractual_source_version'] = 'contract:1'
        bucket['required_windows'] = [{'start': '2026-10-19T09:00:00+00:00', 'end': '2026-10-19T10:00:00+00:00'}]
        value['coverage_intervals'] = [{'id': 'peak-hour', 'start': '2026-10-19T09:00:00+00:00',
            'end': '2026-10-19T10:00:00+00:00', 'required_seats': '2', 'skill_pool': 'support', 'region': 'CZ'}]
        result = scheduler.validate_service_roster(value)
        self.assertFalse(result['roster_ready'])
        self.assertIn('concurrent_seat_shortfall', [item['reason'] for item in result['interval_blockers']])


if __name__ == '__main__':
    unittest.main()
