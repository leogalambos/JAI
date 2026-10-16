#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Deterministic bucket scheduler and explicit managed-service roster validation.

Priority is task order after dependency readiness, then chronological buckets.
This greedy feasibility schedule makes no optimality or response-time SLA claim.
Calendar buckets must be disjoint per physical pool across all engagements.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location('scheduler_economics', Path(__file__).with_name('commercial_economics.py'))
_economics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_economics)


def _number(value, name):
    if not isinstance(value, str):
        raise ValueError(f'{name}: decimal string required')
    result = Decimal(value)
    if not result.is_finite() or result < 0:
        raise ValueError(f'{name}: nonnegative finite hours required')
    return result


def _time(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.utcoffset() is None:
        raise ValueError('calendar timestamps require timezone')
    return result


def schedule(record):
    """Allocate task effort against real shared calendar capacity without overlap.

    Args:
        record: start timestamp, tasks and calendars. Each task has id, phase,
            engagement_id, pool_id, skill, region, effort_hours, dependencies;
            optional not_before, wait_hours and deadline. Calendars carry pool_id,
            id, start/end, capacity_hours, skills, region and external reservations.
            One pool models one interchangeable resource; split concurrent workers.
    Returns:
        Greedy schedule, exact effort/finish and blockers. Unknown/insufficient
        capacity leaves that task and its dependents unscheduled.
    Raises:
        ValueError: Dependency cycle/dangling ID, duplicate/overlapping calendars,
            invalid units, excess reservations or non-aware timestamps.
    """
    start = _time(record['start'])
    tasks = {task['id']: task for task in record['tasks']}
    if len(tasks) != len(record['tasks']):
        raise ValueError('duplicate task')
    for task in tasks.values():
        for key in ('phase', 'engagement_id', 'pool_id', 'skill', 'region'):
            if not task.get(key):
                raise ValueError(f'task requires {key}')
        if any(dep not in tasks for dep in task.get('dependencies', [])):
            raise ValueError('dangling dependency')
        _number(task['effort_hours'], 'effort_hours')
    ordered, visiting, visited = [], set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError('task dependency cycle')
        if key in visited:
            return
        visiting.add(key)
        for dependency in tasks[key].get('dependencies', []):
            visit(dependency)
        visiting.remove(key)
        visited.add(key)
        ordered.append(key)
    for key in tasks:
        visit(key)
    buckets, ids = [], set()
    for calendar in record.get('calendars', []):
        if calendar['id'] in ids:
            raise ValueError('duplicate calendar bucket')
        ids.add(calendar['id'])
        begin, end = _time(calendar['start']), _time(calendar['end'])
        hours = _number(calendar['capacity_hours'], 'capacity_hours')
        elapsed = Decimal(str((end-begin).total_seconds())) / Decimal('3600')
        if end <= begin or hours > elapsed:
            raise ValueError('calendar capacity exceeds physical elapsed window')
        reservations = calendar.get('external_reservations', [])
        reserved = sum((_number(item['hours'], 'reservation') for item in reservations), Decimal('0'))
        if reserved > hours or any(not item.get('engagement_id') for item in reservations):
            raise ValueError('external reservations exceed calendar or lack owner')
        # Aggregate reservations occupy the beginning of a bucket conservatively.
        cursor = begin + timedelta(seconds=float(reserved * Decimal('3600')))
        buckets.append({'source': calendar, 'start': begin, 'end': end,
                        'cursor': cursor, 'remaining': hours-reserved})
    buckets.sort(key=lambda bucket: (bucket['start'], bucket['source']['id']))
    for position, bucket in enumerate(buckets):
        if any(previous['source']['pool_id'] == bucket['source']['pool_id'] and previous['end'] > bucket['start'] for previous in buckets[:position]):
            raise ValueError('overlapping physical pool calendar buckets')
    results, blockers, finished = [], [], {}
    for key in ordered:
        task = tasks[key]
        if any(dep not in finished for dep in task.get('dependencies', [])):
            blockers.append({'task': key, 'reason': 'dependency_not_scheduled'})
            continue
        ready = max([start] + [finished[dep] for dep in task.get('dependencies', [])])
        if task.get('not_before'):
            ready = max(ready, _time(task['not_before']))
        ready += timedelta(seconds=float(_number(task.get('wait_hours', '0'), 'wait_hours') * Decimal('3600')))
        remaining = _number(task['effort_hours'], 'effort_hours')
        planned = []
        for bucket in buckets:
            calendar = bucket['source']
            if calendar['pool_id'] != task['pool_id'] or calendar['region'] != task['region'] or task['skill'] not in calendar['skills']:
                continue
            begin = max(ready, bucket['cursor'])
            usable = min(bucket['remaining'], max(Decimal('0'), Decimal(str((bucket['end']-begin).total_seconds()))/Decimal('3600')))
            take = min(remaining, usable)
            if take:
                end = begin + timedelta(seconds=float(take * Decimal('3600')))
                planned.append((bucket, take, begin, end))
                remaining -= take
            if not remaining:
                break
        if remaining:
            blockers.append({'task': key, 'reason': 'unknown_or_insufficient_capacity', 'missing_hours': str(remaining)})
            continue
        end = planned[-1][3] if planned else ready
        if task.get('deadline') and end > _time(task['deadline']):
            blockers.append({'task': key, 'reason': 'deadline_infeasible', 'earliest_finish': end.isoformat()})
            continue
        for bucket, take, begin, finish in planned:
            bucket['remaining'] -= take
            bucket['cursor'] = finish
        finished[key] = end
        results.append({'task': key, 'engagement_id': task['engagement_id'], 'phase': task['phase'],
                        'effort_hours': task['effort_hours'], 'earliest_finish': end.isoformat(),
                        'allocations': [{'calendar_id': bucket['source']['id'], 'hours': str(take),
                                         'start': begin.isoformat(), 'end': finish.isoformat()} for bucket,take,begin,finish in planned]})
    return {'formula_version': 'commercial-scheduler/1', 'algorithm': 'stable-topological-greedy',
            'tasks': results, 'blockers': blockers, 'feasible': not blockers,
            'optimality_proven': False, 'sla_proven': False}


def validate_service_roster(record):
    """Check explicit interval seats, staffing, backups and on-call restrictions.

    Args:
        record: sizing input accepted by commercial_economics.service_sizing and
            shifts, one record per worker per service bucket with worker_id,
            bucket_id, skill_pool, region, paid_hours, active_hours, mode, and
            backup_worker_id and coverage_windows. Every sizing bucket requires immutable
            contractual_source_version and required_windows whose duration equals
            service_window_hours. Coverage is derived from these contractual windows,
            never from caller-supplied summary intervals.
    Returns:
        Unchanged sizing minima plus roster blockers; never SLA percentile proof.
    Raises:
        ValueError: Duplicate worker assignment or unknown service bucket.
    """
    sizing = _economics.service_sizing(record['sizing'])
    buckets = {bucket['id']: bucket for bucket in record['sizing']['buckets']}
    shifts = record.get('shifts', [])
    assigned, blockers = set(), []
    for shift in shifts:
        key = (shift['worker_id'], shift['bucket_id'])
        if key in assigned or shift['bucket_id'] not in buckets:
            raise ValueError('duplicate worker assignment or unknown bucket')
        assigned.add(key)
        bucket = buckets[shift['bucket_id']]
        if shift['skill_pool'] != bucket['skill_pool'] or shift['region'] != bucket['region']:
            blockers.append({'bucket': bucket['id'], 'reason': 'skill_or_region_mismatch'})
        active = _number(shift['active_hours'], 'active_hours')
        paid = _number(shift['paid_hours'], 'paid_hours')
        if active > paid:
            raise ValueError('active hours exceed paid hours')
        if shift['mode'] not in {'active', 'on_call'}:
            raise ValueError('unknown shift mode')
        if shift['mode'] == 'on_call' and not all(field in shift for field in ('activation_hours', 'response_limit_hours', 'rest_hours', 'reachable')):
            blockers.append({'bucket': bucket['id'], 'reason': 'on_call_conditions_unverified'})
        elif shift['mode'] == 'on_call':
            if shift['reachable'] is not True or _number(shift['activation_hours'], 'activation_hours') > _number(shift['response_limit_hours'], 'response_limit_hours'):
                blockers.append({'bucket': bucket['id'], 'reason': 'on_call_activation_incompatible'})
            _number(shift['rest_hours'], 'rest_hours')
        if shift['mode'] == 'on_call' and active:
            blockers.append({'bucket': bucket['id'], 'reason': 'on_call_is_not_active_coverage'})
        if not shift.get('backup_worker_id') or shift['backup_worker_id'] == shift['worker_id']:
            blockers.append({'bucket': bucket['id'], 'reason': 'independent_backup_missing'})
    for row in sizing['buckets']:
        bucket = buckets[row['id']]
        valid = [shift for shift in shifts if shift['bucket_id'] == row['id'] and shift['mode'] == 'active' and shift['skill_pool'] == bucket['skill_pool'] and shift['region'] == bucket['region']]
        paid = sum((_number(shift['paid_hours'], 'paid_hours') for shift in valid), Decimal('0'))
        active = sum((_number(shift['active_hours'], 'active_hours') for shift in valid), Decimal('0'))
        if paid < Decimal(row['paid_roster_hours']) or active < Decimal(row['required_available_hours']):
            blockers.append({'bucket': row['id'], 'reason': 'interval_staffing_shortfall'})
        for shift in valid:
            if (shift.get('backup_worker_id'), row['id']) not in assigned:
                blockers.append({'bucket': row['id'], 'reason': 'backup_not_scheduled'})
    for position, shift in enumerate(shifts):
        for other in shifts[:position]:
            if shift['worker_id'] != other['worker_id']:
                continue
            if any(_time(left['start']) < _time(right['end']) and _time(right['start']) < _time(left['end'])
                   for left in shift.get('coverage_windows', []) for right in other.get('coverage_windows', [])):
                blockers.append({'worker': shift['worker_id'], 'reason': 'shared_worker_double_booking'})
    interval_blockers = []
    intervals = []
    contract_windows_complete = True
    for bucket_id, bucket in buckets.items():
        windows = bucket.get('required_windows', [])
        if not windows or not bucket.get('contractual_source_version'):
            contract_windows_complete = False
            interval_blockers.append({'bucket': bucket_id, 'reason': 'contractual_service_windows_missing'})
            continue
        elapsed = Decimal('0')
        ordered_windows = sorted(windows, key=lambda window: _time(window['start']))
        previous_end = None
        for number, window in enumerate(ordered_windows):
            begin, end = _time(window['start']), _time(window['end'])
            if begin >= end or (previous_end is not None and begin < previous_end):
                raise ValueError('contractual service windows overlap or are inverted')
            previous_end = end
            elapsed += Decimal(str((end-begin).total_seconds())) / Decimal('3600')
            intervals.append({'id': f'{bucket_id}:{number}', 'start': window['start'], 'end': window['end'],
                              'required_seats': bucket['concurrent_seats'], 'skill_pool': bucket['skill_pool'],
                              'region': bucket['region']})
        if elapsed != _number(bucket['service_window_hours'], 'service_window_hours'):
            contract_windows_complete = False
            interval_blockers.append({'bucket': bucket_id, 'reason': 'contractual_window_hours_mismatch'})
    for shift in shifts:
        windows = sorted(shift.get('coverage_windows', []), key=lambda window: _time(window['start']))
        actual = Decimal('0')
        previous_end = None
        for window in windows:
            begin, end = _time(window['start']), _time(window['end'])
            if begin >= end or (previous_end is not None and begin < previous_end):
                raise ValueError('shift coverage windows overlap or are inverted')
            previous_end = end
            actual += Decimal(str((end-begin).total_seconds())) / Decimal('3600')
            bucket = buckets[shift['bucket_id']]
            if not any(_time(required['start']) <= begin and _time(required['end']) >= end for required in bucket.get('required_windows', [])):
                interval_blockers.append({'worker': shift['worker_id'], 'reason': 'shift_outside_contractual_windows'})
        declared = _number(shift['active_hours'], 'active_hours')
        if actual != declared or (shift['mode'] == 'active' and declared and not windows):
            interval_blockers.append({'worker': shift['worker_id'], 'reason': 'active_hours_window_mismatch'})
    for interval in intervals:
        begin, end = _time(interval['start']), _time(interval['end'])
        if begin >= end:
            raise ValueError('invalid coverage interval')
        required_seats = _number(interval['required_seats'], 'required_seats')
        if required_seats != required_seats.to_integral_value():
            raise ValueError('coverage seats must be integral')
        points = {begin, end}
        eligible = []
        for shift in shifts:
            if shift['mode'] != 'active' or shift['skill_pool'] != interval['skill_pool'] or shift['region'] != interval['region']:
                continue
            for window in shift.get('coverage_windows', []):
                left, right = _time(window['start']), _time(window['end'])
                if left >= right:
                    raise ValueError('invalid shift coverage window')
                if left < end and right > begin:
                    eligible.append((shift['worker_id'], left, right))
                    points.update((max(begin, left), min(end, right)))
        points = sorted(points)
        for left, right in zip(points, points[1:]):
            workers = {worker for worker, first, last in eligible if first <= left and last >= right}
            if len(workers) < required_seats:
                interval_blockers.append({'interval': interval['id'], 'reason': 'concurrent_seat_shortfall',
                                          'start': left.isoformat(), 'end': right.isoformat()})
    blockers += [blocker for blocker in sizing['blockers'] if blocker['reason'] != 'roster_not_verified']
    return {'formula_version': 'commercial-service-roster/1', 'sizing': sizing,
            'blockers': blockers, 'feasible_aggregate_roster': not blockers,
            'interval_blockers': interval_blockers, 'interval_coverage_verified': contract_windows_complete and bool(intervals) and not interval_blockers,
            'roster_ready': contract_windows_complete and bool(intervals) and not interval_blockers and not blockers,
            'labour_law_verified': False, 'sla_proven': False, 'human_required': True}
