#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Incremental, advisory execution metrics from already verified Store effects.

Analytics never decide acceptance, increase budgets or replay lifecycle logic.
Project history contains closed aggregate records, never prompts, material paths,
findings text or provider captures. Unknown token/currency observations stay absent.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import execution_profiles

_LABEL = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}$')
_OUTCOMES = {'in progress', 'completed', 'paused', 'stopped', 'accepted', 'failed', 'returned'}
_FIELDS = {'schema_version', 'run_id', 'profile', 'provider', 'task_class', 'review_scope',
           'outcome', 'transactions', 'invocations', 'rework_rounds', 'findings', 'reviews',
           'elapsed_ms', 'role_elapsed_ms', 'requested_models', 'observed_models', 'recommendation', 'config_version', 'routing_deviations', 'routing_observations'}
_ROLES = {'setter', 'author', 'reviewer', 'integration_reviewer', 'receiver', 'integrator', 'measurement', 'unknown'}


def _label(value):
    if not isinstance(value, str) or not _LABEL.fullmatch(value):
        raise ValueError('Analytics labels must be short identifiers, never prose or paths')
    return value


def _nonnegative(value):
    return type(value) is int and value >= 0


def _fingerprint(value):
    if value is not None and (not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value)):
        raise ValueError('Configuration version must be an opaque SHA-256 fingerprint or unknown')


def configuration_version(profile_snapshot, registry=None):
    """Fingerprint effective routing and context without private provenance.

    Args:
        profile_snapshot: Captured resolved execution preference, or None for legacy.
        registry: Captured registry including every available provider/workload alternative.
    Returns:
        SHA-256 fingerprint of effective provider, responsibilities, fallbacks and
        context; None when no captured configuration is available. Profile names,
        source locators and analytics labels do not influence the fingerprint.
    Raises:
        ValueError: A supplied snapshot lacks effective configuration fields.
    """
    if profile_snapshot is None:
        return None
    keys = ('provider', 'responsibilities', 'context_policy', 'context', 'configured')
    if not isinstance(profile_snapshot, dict) or any(key not in profile_snapshot for key in keys):
        raise ValueError('Effective execution snapshot required for configuration version')
    # Explicit allow-list prevents future source/provenance fields leaking into
    # comparison identity. Nested responsibility mappings contain routing only.
    effective = {key: profile_snapshot[key] for key in keys}
    effective['routing_mode'] = execution_profiles.routing_mode(profile_snapshot)
    if registry is not None:
        effective['available_models'] = registry['providers']
        effective['workload_classes'] = registry['workload_classes']
    return hashlib.sha256(json.dumps(effective, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=True).encode()).hexdigest()


class Accumulator:
    """Consume each new verified transaction once within a warm native session."""

    def __init__(self, run_id, profile='standard', provider='codex', task_class='unspecified', review_scope='unspecified', config_version=None, preferences=None):
        """Create private counters for a run without reading any filesystem.

        Args:
            run_id: Stable internal run identity, hashed before storage or display.
            profile: Selected execution profile identifier.
            provider: Active native provider, or unspecified for legacy snapshots.
            task_class: Explicit non-sensitive comparison class, or unspecified.
            review_scope: Explicit review scope label, or unspecified.
            config_version: Effective configuration fingerprint, or None when unknown.
            preferences: Pinned execution profile snapshot, or None for legacy routing.
        Raises:
            ValueError: A label is unsafe or provider unsupported.
        """
        if provider not in {'codex', 'claude', 'unspecified'} or not isinstance(run_id, str) or not run_id:
            raise ValueError('An actual run identity and native provider are required')
        self.run_id = hashlib.sha256(run_id.encode()).hexdigest()
        self.profile, self.provider = _label(profile), provider
        self.task_class, self.review_scope = _label(task_class), _label(review_scope)
        _fingerprint(config_version)
        self.config_version = config_version
        self.preferences = copy.deepcopy(preferences)
        self._routing_rows, self._routing_work, self._routing_unknown, self._deviations = {}, 0, 0, 0
        self.cursor = 0
        self._invocations, self._reworks, self._findings, self._reviews = {}, {}, set(), set()
        self._elapsed, self._rework_total, self._roles, self._models = 0, 0, {}, {}

    def update(self, state):
        """Consume only the new suffix of a warm verified State's transactions.

        Args:
            state: Existing trusted lifecycle State with transactions and invocations.
        Returns:
            Whether new transactions were consumed; duplicate calls are no-ops.
        Raises:
            ValueError: History shrank; use a new accumulator for cold recovery.
        """
        if len(state.transactions) < self.cursor:
            raise ValueError('Analytics history shrank; cold initialization is required')
        changed = len(state.transactions) != self.cursor
        for transaction in state.transactions[self.cursor:]:
            for effect in transaction['operations'][0]['data']['effects']:
                operation = effect['op']
                if operation in {'invocation', 'invocation-update'}:
                    identifier = effect['invocation_id']
                    invocation = state.invocations.get(identifier)
                    if invocation is not None:
                        previous = self._invocations.get(identifier)
                        observation = _invocation_metrics(invocation)
                        # Captured work choices are immutable; finishing the call
                        # changes time, not the already observed selection tuple.
                        observation['routing'] = (previous['routing'] if previous is not None
                            and previous['routing'] is not None else
                            _routing_metrics(state, invocation, self.preferences))
                        for direction, item in ((-1, previous), (1, observation)):
                            if item is None:
                                continue
                            self._routing_delta(item['routing'], direction)
                            elapsed, role, model = item['elapsed_ms'], item['role'], item['requested_model']
                            self._elapsed += direction * elapsed
                            self._roles[role] = self._roles.get(role, 0) + direction * elapsed
                            if model:
                                self._models[model] = self._models.get(model, 0) + direction
                        self._invocations[identifier] = observation
                elif operation == 'local-update' and 'reworks_used' in effect['value']:
                    identifier, count = effect['unit_id'], effect['value']['reworks_used']
                    self._rework_total += count - self._reworks.get(identifier, 0)
                    self._reworks[identifier] = count
                elif operation == 'register':
                    manifest = effect['manifest']
                    if manifest['kind'] == 'delivery.assessment':
                        record = manifest['content']['record']
                        identity = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
                        self._reviews.add(identity)
                        for finding in record.get('findings', []):
                            self._findings.add(finding['version_id'])
        self.cursor = len(state.transactions)
        return changed

    def _routing_delta(self, observation, direction):
        if observation is None:
            return
        rows, differs = observation
        self._routing_work += direction
        self._routing_unknown += direction * (differs is None)
        self._deviations += direction * (differs is True)
        for row in rows:
            key = json.dumps(row, sort_keys=True, separators=(',', ':'))
            existing = self._routing_rows.setdefault(key, {**row, 'occurrences': 0})
            existing['occurrences'] += direction

    def summary(self, outcome='in progress'):
        """Return a closed aggregate snapshot, with no acceptance inference.

        Args:
            outcome: Explicit caller-observed task status, never a model conclusion.
        Returns:
            JSON-serializable aggregate; unknown served models stay unobserved.
        Raises:
            ValueError: The outcome is not one of the supported status labels.
        """
        if outcome not in _OUTCOMES:
            raise ValueError('Unsupported explicit execution outcome')
        value = {'schema_version': 1, 'run_id': self.run_id, 'profile': self.profile,
                 'provider': self.provider, 'config_version': self.config_version, 'task_class': self.task_class, 'review_scope': self.review_scope,
                 'outcome': outcome, 'transactions': self.cursor, 'invocations': len(self._invocations),
                 'rework_rounds': self._rework_total, 'findings': len(self._findings),
                 'reviews': len(self._reviews), 'elapsed_ms': self._elapsed, 'role_elapsed_ms': dict(self._roles),
                 'requested_models': sorted(model for model, count in self._models.items() if count), 'observed_models': [],
                 'routing_deviations': self._deviations if self._routing_work and not self._routing_unknown else None,
                 'routing_observations': [copy.deepcopy(row) for key, row in sorted(self._routing_rows.items()) if row['occurrences']],
                 'recommendation': {'action': 'unchanged', 'confidence': 'insufficient-evidence'}}
        if any(row['differs'] for row in value['routing_observations']):
            value['recommendation'] = {'action': 'inspect-routing', 'confidence': 'high'}
        elif value['rework_rounds']:
            value['recommendation'] = {'action': 'inspect-rework-causes', 'confidence': 'low'}
        return value


def _routing_metrics(state, invocation, preferences):
    # Prepared grants are not observed model work; selection turns and workload
    # routing have no fixed responsibility preference against which to compare.
    if type(invocation.get('started_at_ms')) is not int or invocation.get('phase') == 'selection':
        return None
    if preferences is not None and execution_profiles.routing_mode(preferences) != 'profile':
        return None
    if preferences is None or invocation.get('phase') != 'work':
        return ([], None)
    rows, unknown = {}, False
    members = invocation.get('members', [])
    if not members:
        return ([], None)
    for member in members:
        try:
            context = state.resolve(member['context'], 'context')
            if context['execution']['phase'] != 'work':
                unknown = True
                continue
            selection = state.resolve(context['execution']['selection'])['message']['payload']
            model = invocation['model_controls']['model']
            row = execution_profiles.routing_observation(preferences,
                invocation['responsibility'], selection['workload_class'], model)
            _validate_routing_row({**row, 'occurrences': 1})
            if row['routing_mode'] != 'profile' or row['preference'] is None or row['differs'] is None:
                unknown = True
                continue
            key = json.dumps(row, sort_keys=True, separators=(',', ':'))
            rows[key] = row
        except (KeyError, ValueError, TypeError, AttributeError):
            # Missing/unsafe attribution is unavailable telemetry, never a match.
            unknown = True
    values = list(rows.values())
    differs = None if unknown else any(row['differs'] for row in values)
    return values, differs


def _validate_routing_row(row):
    fields = {'routing_mode', 'responsibility', 'preference', 'selected', 'differs', 'served_model', 'occurrences'}
    if (not isinstance(row, dict) or set(row) != fields or row['routing_mode'] != 'profile'
            or row['responsibility'] not in _ROLES - {'unknown'} or type(row['differs']) is not bool
            or row['served_model'] is not None or not _nonnegative(row['occurrences']) or not row['occurrences']):
        raise ValueError('Closed safe routing observation required')
    for key in ('preference', 'selected'):
        choice = row[key]
        if not isinstance(choice, dict) or set(choice) != {'provider', 'workload_class', 'model_selector', 'reasoning_effort'}:
            raise ValueError('Closed requested routing choice required')
        if choice['provider'] not in {'codex', 'claude'}:
            raise ValueError('Routing choice requires a supported native provider')
        for field in ('provider', 'workload_class', 'model_selector'):
            _label(choice[field])
        if choice['reasoning_effort'] is not None:
            _label(choice['reasoning_effort'])
    if row['differs'] != (row['preference'] != row['selected']):
        raise ValueError('Routing comparison differs from its captured choices')


def _validate_routing(summary):
    count = summary.get('routing_deviations')
    rows = summary.get('routing_observations', [])
    if count is not None and (not _nonnegative(count) or count > summary['invocations']):
        raise ValueError('Routing deviations must be an observed physical invocation count or unknown')
    if not isinstance(rows, list):
        raise ValueError('Routing observations must be a closed aggregate list')
    for row in rows:
        _validate_routing_row(row)
        if row['occurrences'] > summary['invocations']:
            raise ValueError('Routing occurrences exceed observed physical invocations')
    if count is not None and not rows:
        raise ValueError('Known routing deviations require actual work observations')
    if count == 0 and any(row['differs'] for row in rows):
        raise ValueError('Matching routing aggregate cannot contain deviations')
    if count and not any(row['differs'] for row in rows):
        raise ValueError('Routing deviation count requires an actual differing choice')


def _routing_signature(summary):
    rows = summary.get('routing_observations', [])
    if not rows or summary.get('routing_deviations') is None:
        return None
    choices = [{key: value for key, value in row.items() if key != 'occurrences'} for row in rows]
    keys = sorted({json.dumps(row, sort_keys=True, separators=(',', ':')) for row in choices})
    return hashlib.sha256(json.dumps(keys, separators=(',', ':')).encode()).hexdigest()


def _invocation_metrics(invocation):
    role = invocation.get('responsibility', 'unknown')
    role = role if role in _ROLES else 'unknown'
    start, finish = invocation.get('started_at_ms'), invocation.get('finished_at_ms')
    elapsed = max(0, finish - start) if type(start) is int and type(finish) is int else 0
    model = invocation.get('model_controls', {}).get('model_selector')
    # Model selectors are labels only; never copy arbitrary capture text.
    model = model if isinstance(model, str) and _LABEL.fullmatch(model) else None
    return {'role': role, 'elapsed_ms': elapsed, 'requested_model': model}


def _validate(summary):
    if (not isinstance(summary, dict) or set(summary) - _FIELDS
            or (_FIELDS - {'config_version', 'routing_deviations', 'routing_observations'}) - set(summary)
            or summary['schema_version'] != 1):
        raise ValueError('Closed version-one aggregate summary required')
    if not isinstance(summary['run_id'], str) or not re.fullmatch('[0-9a-f]{64}', summary['run_id']):
        raise ValueError('Opaque aggregate run identity required')
    _fingerprint(summary.get('config_version'))
    for field in ('profile', 'task_class', 'review_scope'):
        _label(summary[field])
    if summary['provider'] not in {'codex', 'claude', 'unspecified'} or summary['outcome'] not in _OUTCOMES:
        raise ValueError('Unsupported summary provider or outcome')
    if any(not _nonnegative(summary[key]) for key in ('transactions', 'invocations', 'rework_rounds', 'findings', 'reviews', 'elapsed_ms')):
        raise ValueError('Aggregate counters must be nonnegative integers')
    roles = summary['role_elapsed_ms']
    if not isinstance(roles, dict) or any(role not in _ROLES or not _nonnegative(value) for role, value in roles.items()):
        raise ValueError('Invalid responsibility time aggregate')
    for key in ('requested_models', 'observed_models'):
        if not isinstance(summary[key], list):
            raise ValueError('Model observations must be label lists')
        for model in summary[key]:
            _label(model)
    if summary['observed_models']:
        raise ValueError('This adapter has no served-model observation source')
    _validate_routing(summary)
    advice = summary['recommendation']
    if (not isinstance(advice, dict) or set(advice) != {'action', 'confidence'}
            or advice['action'] not in {'unchanged', 'inspect-rework-causes', 'inspect-routing'}
            or advice['confidence'] not in {'low', 'insufficient-evidence', 'high'}):
        raise ValueError('Unsupported advisory recommendation')


def _directory(project, create=False):
    root = Path(project).resolve()
    directory = root / '.jai' / 'stats'
    for path in (root / '.jai', directory):
        if path.is_symlink():
            raise ValueError('Analytics storage cannot follow symbolic links')
        if create:
            path.mkdir(mode=0o700, exist_ok=True)
    return directory


def record(project, summary):
    """Atomically upsert one private aggregate record without copying task content.

    Args:
        project: Existing project root; storage stays under .jai/stats.
        summary: Closed aggregate produced by Accumulator.summary.
    Returns:
        Stored path; repeated identical writes leave its modification time intact.
    Raises:
        ValueError, OSError: Invalid fields, symlink storage or filesystem failure.
    """
    _validate(summary)
    directory = _directory(project, create=True)
    path = directory / (summary['run_id'] + '.json')
    if path.is_symlink():
        raise ValueError('Analytics record cannot follow a symbolic link')
    raw = json.dumps(summary, sort_keys=True, indent=2) + '\n'
    if path.exists() and path.read_text(encoding='utf-8') == raw:
        return path
    descriptor, temporary = tempfile.mkstemp(dir=directory, prefix='.stats-')
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as target:
            target.write(raw)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path


def history(project, profile=None):
    """Read validated private aggregates ordered by latest filesystem update.

    Args:
        project: Project whose .jai/stats aggregates are requested.
        profile: Optional exact profile identifier filter.
    Returns:
        Aggregate records, oldest first; no journal or task materials are read.
    Raises:
        ValueError, OSError: Unsafe storage or invalid aggregate records.
    """
    if profile is not None:
        _label(profile)
    directory = _directory(project)
    values = []
    for path in sorted(directory.glob('*.json'), key=lambda item: item.lstat().st_mtime_ns):
        if path.is_symlink():
            raise ValueError('Analytics record cannot follow a symbolic link')
        value = json.loads(path.read_text(encoding='utf-8'))
        _validate(value)
        if path.name != value['run_id'] + '.json':
            raise ValueError('Aggregate filename differs from opaque run identity')
        if profile is None or value['profile'] == profile:
            values.append(value)
    return values


def compact_table(summary):
    """Render the single-row Markdown footer after the user's actual task output.

    Args:
        summary: Closed validated aggregate, without task material.
    Returns:
        Three-line Markdown table; model time is summed physical call time.
    Raises:
        ValueError: Aggregate schema or safe labels are invalid.
    """
    _validate(summary)
    deviated = bool(summary.get('routing_deviations')) or any(
        row['differs'] for row in summary.get('routing_observations', []))
    profile = summary['profile'] + ('*' if deviated else '')
    advice = ('Routing differs; coverage incomplete' if deviated and summary.get('routing_deviations') is None else
              'Routing differs; inspect details' if deviated else
              'Inspect rework causes (low confidence)' if summary['rework_rounds']
              else 'Unchanged (insufficient evidence)')
    return ('| Outcome | Profile | Model time | Rework rounds | Findings | Advice |\n'
            '| --- | --- | ---: | ---: | ---: | --- |\n'
            f"| {summary['outcome']} | {profile} | {summary['elapsed_ms'] / 1000:g}s | "
            f"{summary['rework_rounds']} | {summary['findings']} | {advice} |")


def compare(records, profiles):
    """Compare only explicit matching task/review/provider cohorts.

    Args:
        records: Validated aggregate history returned by history.
        profiles: Two distinct exact execution profile identifiers.
    Returns:
        Cohort counts and averages, or an honest insufficient-evidence message.
    Raises:
        ValueError: Profile selection or records are invalid.
    """
    if len(profiles) != 2 or profiles[0] == profiles[1]:
        raise ValueError('Comparison requires two distinct profiles')
    for profile in profiles:
        _label(profile)
    groups = {}
    for row in records:
        _validate(row)
        if (row['profile'] not in profiles or row['task_class'] == 'unspecified'
                or row['review_scope'] == 'unspecified' or row['outcome'] != 'accepted'):
            continue
        key = (row['provider'], row['task_class'], row['review_scope'])
        groups.setdefault(key, {}).setdefault(row['profile'], []).append(row)
    rows = []
    mixed_versions = False
    for key, grouped in sorted(groups.items()):
        if any(profile not in grouped for profile in profiles):
            continue
        versions = {profile: {row.get('config_version') for row in grouped[profile]} for profile in profiles}
        if any(None in values or len(values) != 1 for values in versions.values()):
            mixed_versions = True
            continue
        signatures = {profile: {_routing_signature(row) for row in grouped[profile]} for profile in profiles}
        if any(None in values or len(values) != 1 for values in signatures.values()):
            mixed_versions = True
            continue
        for profile in profiles:
            samples = grouped[profile]
            rows.append({'provider': key[0], 'task_class': key[1], 'review_scope': key[2],
                         'profile': profile, 'config_version': next(iter(versions[profile])),
                         'routing_signature': next(iter(signatures[profile])), 'samples': len(samples),
                         'mean_model_ms': sum(row['elapsed_ms'] for row in samples) / len(samples),
                         'mean_reworks': sum(row['rework_rounds'] for row in samples) / len(samples)})
    return {'cohorts': rows, 'recommendation': 'advisory-only',
            'limitation': 'Observational comparison; no causal or quality-equivalence claim.' if rows else
            ('Unknown or mixed effective configuration versions or actual routing signatures; select a homogeneous cohort.' if mixed_versions else
             'Insufficient comparable accepted tasks with explicit task class and review scope and known configuration versions.')}


def main(argv=None):
    """Execute the internal helper used by the native workflow-stats command.

    Args:
        argv: Optional argument list; defaults to the process command line.
    Returns:
        Zero for a valid read-only report; parser errors exit nonzero.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--profile')
    parser.add_argument('action', nargs='?', choices=('list', 'last', 'profile', 'compare'), default='list')
    parser.add_argument('profiles', nargs='*')
    args = parser.parse_args(argv)
    try:
        if args.action == 'profile':
            if len(args.profiles) != 1 or args.profile is not None:
                parser.error('profile requires one profile identifier')
            values = history(args.project, args.profiles[0])
            print('\n\n'.join(compact_table(row) for row in values) if values else 'No execution statistics recorded.')
            return 0
        values = history(args.project, args.profile)
        if args.action == 'compare':
            print(json.dumps(compare(values, args.profiles), indent=2))
        elif args.profiles:
            parser.error('Profile operands belong only to compare')
        elif args.action == 'last':
            print(compact_table(values[-1]) if values else 'No execution statistics recorded.')
        else:
            print('\n\n'.join(compact_table(row) for row in values) if values else 'No execution statistics recorded.')
    except (ValueError, OSError) as error:
        parser.error(str(error))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
