# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local iteration effects and indexes within the existing lifecycle Store.

Operational windows do not grant semantic acceptance or fabricate remote stop
observations. There is no independent journal, queue or timer service.
"""
from __future__ import annotations

import copy

import lifecycle as lc


def _bind(state, reference, record):
    """Derive one immutable incoming-cell binding when an assignment is admitted.

    Args:
        state: Existing lifecycle state before this registration.
        reference: Exact newly constructed assignment reference.
        record: Schema-valid assignment whose issuer has already been checked.
    Returns:
        One derived local binding effect, without persistence or new authority.
    """
    parent = state.local_budget['bindings'].get(record['issued_under']['version_id']) if record['issued_under'] else None
    same_owner = parent is not None and state.resolve(record['issued_under'], 'assignment')['owner'] == record['owner']
    anchor = parent['anchor'] if same_owner else reference
    phase = ('question' if record['owner']['work_kind'] == 'question' else
             'planning' if record['responsibility'] == 'setter' else 'integration')
    generation = parent['root_generation'] if parent is not None else state._root_key(record)
    ancestors = list(parent['planning_ancestors']) if parent is not None else []
    task = record.get('procedure_task')
    if task is not None:
        procedure = state.resolve(task['procedure'])['message']['payload']
        if procedure['kind'] == 'layer':
            coordinator = state.local_budget['bindings'][procedure['assignment']['version_id']]
            planning = _unit_id(coordinator['anchor'], 'planning', coordinator['scope'])
            if planning not in ancestors:
                ancestors.append(planning)
    return {'op': 'local-bind', 'assignment': reference, 'anchor': anchor, 'phase': phase,
            'root_generation': generation, 'scope': record['use_scope'], 'owner': record['owner'],
            'policy': copy.deepcopy(state.resolve(record['profile'], 'profile')['local_budget']),
            'planning_ancestors': ancestors}


def _unit_id(anchor, phase, scope):
    """Identify one incoming local unit independently of its own revised criteria.

    Args:
        anchor: First incoming same-owner mandate reference.
        phase: Planning, question or integration responsibility.
        scope: Exact authorized use scope.
    Returns:
        Deterministic local unit digest, not an authorization token.
    """
    return lc._hash({'anchor': anchor, 'phase': phase, 'scope': scope})


def _status(state, assignment_ref, at_ms):
    """Project current operational time without modifying accepted history.

    Args:
        state: Existing replay-derived lifecycle state.
        assignment_ref: Exact incoming or locally descended assignment.
        at_ms: Trusted observation time for the requested projection.
    Returns:
        Local unit facts and actual unfinished physical observations, or None
        before an assignment's binding is admitted.
    """
    binding = state.local_budget['bindings'].get(assignment_ref['version_id'])
    if binding is None:
        return None
    phase = binding['phase']
    integration = _unit_id(binding['anchor'], 'integration', binding['scope'])
    if phase == 'planning' and integration in state.local_budget['units']:
        phase = 'integration'
    key = _unit_id(binding['anchor'], phase, binding['scope'])
    return _unit_status(state, key, at_ms)


def _unit_status(state, key, at_ms):
    unit = state.local_budget['units'][key]
    remaining = unit['remaining_ms'] if unit['deadline_ms'] is None else max(0, unit['deadline_ms'] - at_ms)
    applicable = any(state._status(reference, unit['scope'])['validity'] == 'valid'
                     for reference in unit['governors'])
    pending, progress = [], []
    for run_id in unit['runs']:
        details = state.run_details[run_id]
        context = state.resolve(details['context'], 'context')
        progress.append({'run_id': run_id, 'assignment': context['assignment'],
                         'responsibility': context['purpose'], 'phase': context['execution']['phase'],
                         'state': state.run_states[run_id]})
        if state.run_states.get(run_id) not in {'issued', 'running'}:
            continue
        physical = state.invocations.get(details.get('invocation_id'), {})
        pending.append({'run_id': run_id, 'context': details['context'],
                        'invocation_id': details.get('invocation_id'),
                        'physical_state': physical.get('state'), 'handle': physical.get('handle')})
    return {**copy.deepcopy({key: value for key, value in unit.items() if key not in {'runs', 'members', 'governors'}}),
            'remaining_ms': remaining, 'max_reworks': unit['policy']['max_reworks'],
            'state': unit['state'] if applicable else 'obsolete', 'applicable': applicable,
            'progress': progress, 'pending': pending,
            'due': applicable and unit['state'] == 'active' and remaining == 0}


def _activate(state, assignment_ref, at_ms, stage):
    """Derive actual-start activation; preparing a grant never starts its clock.

    Args:
        state: Existing state before the actual process/native start.
        assignment_ref: Exact current member assignment.
        at_ms: Actual trusted start observation.
        stage: Actual responsibility and phase being dispatched.
    Returns:
        Zero or one local activation effects, preserving an active deadline.
    Raises:
        ProtocolError: The local unit is paused, stopped or exhausted.
    """
    current = (_unit_status(state, assignment_ref, at_ms) if isinstance(assignment_ref, str)
               else _status(state, assignment_ref, at_ms))
    if current is None:
        raise lc.ERROR('P_STATE', 'A productive grant requires its incoming local unit')
    if current['state'] in {'paused', 'terminated', 'obsolete'} or current['remaining_ms'] <= 0:
        raise lc.ERROR('P_BUDGET', 'Local iteration is paused or stopped; an actual operator decision is required')
    downstream = stage.endswith(':work') and stage.split(':', 1)[0] in {'author', 'integrator', 'reviewer', 'integration_reviewer', 'receiver', 'measurement'}
    if current['state'] == 'active':
        if current['stage'] == stage and (not downstream or current['downstream_started']):
            return []
        return [{'op': 'local-update', 'unit_id': current['unit_id'], 'value': {
            'stage': stage, 'downstream_started': current['downstream_started'] or downstream,
            'revision': current['revision'] + 1}}]
    return [{'op': 'local-update', 'unit_id': current['unit_id'], 'value': {
        'state': 'active', 'started_at_ms': at_ms, 'deadline_ms': at_ms + current['remaining_ms'],
        'stage': stage, 'downstream_started': current['downstream_started'] or downstream,
        'revision': current['revision'] + 1}}]


def _idle(state, assignment_ref, at_ms, stage):
    """Stop completed or suspended local clock use, preserving the remaining iteration.

    Args:
        state: Existing state containing the unit's active window.
        assignment_ref: Exact mandate or pinned unit whose operational work finished.
        at_ms: Trusted completion time, not a proposed new deadline.
        stage: Recorded completed/suspended procedure stage.
    Returns:
        Zero or one effects; later owner work reuses the persisted allowance.
    """
    current = (_unit_status(state, assignment_ref, at_ms) if isinstance(assignment_ref, str)
               else _status(state, assignment_ref, at_ms))
    if current is None or current['state'] != 'active' or current['remaining_ms'] <= 0:
        return []
    return [{'op': 'local-update', 'unit_id': current['unit_id'], 'value': {
        'state': 'idle', 'remaining_ms': current['remaining_ms'], 'deadline_ms': None,
        'stage': stage, 'revision': current['revision'] + 1}}]


def _rework(state, assignment_ref):
    """Open one actual repair round after downstream work has started.

    Args:
        state: Current lifecycle state at the owner decision boundary.
        assignment_ref: Exact actual owner mandate making that decision.
    Returns:
        Zero preparation effects or one next-iteration effect with unchanged incoming anchor and rights.
    Raises:
        ProtocolError: The shared maximum rework count is already exhausted.
    """
    current = (_unit_status(state, assignment_ref, state.assessed_at_ms) if isinstance(assignment_ref, str)
               else _status(state, assignment_ref, state.assessed_at_ms))
    if current is None:
        raise lc.ERROR('P_STATE', 'A semantic repair requires its actual incoming local unit')
    if not current['downstream_started']:
        return []
    if current['reworks_used'] >= current['max_reworks']:
        raise lc.ERROR('P_STATE', 'Maximum local reworks reached; use the existing escalation path')
    return [{'op': 'local-update', 'unit_id': current['unit_id'], 'value': {
        'iteration': current['iteration'] + 1, 'reworks_used': current['reworks_used'] + 1,
        'state': 'ready', 'remaining_ms': current['policy']['iteration_ms'],
        'started_at_ms': None, 'deadline_ms': None, 'stage': 'rework', 'downstream_started': False,
        'revision': current['revision'] + 1}}]


def derive(state, message, origin, at, live):
    """Derive an exact operational pause/extension/stop in the existing Store.

    Args:
        state: Existing authoritative lifecycle state.
        message: Closed current controller event.
        origin: Previously authenticated local controller.
        at: Trusted assessment time.
        live: Read actual instruction material for new operational actions.
    Returns:
        Operational effects only; accepted results and old grants are unchanged.
    Raises:
        ProtocolError: Scope, stale revision, duration or instruction is invalid.
    """
    payload = message['payload']
    unit = state.local_budget['units'].get(payload['unit_id'])
    if unit is None or unit['scope'] != message['scope'] or unit['revision'] != payload['expected_revision']:
        raise lc.ERROR('P_CONFLICT', 'Operational decision must name the exact current local unit revision')
    event = payload['event']
    if event == 'local_budget_pause':
        if unit['state'] != 'active' or unit['deadline_ms'] is None or payload['observed_at_ms'] < unit['deadline_ms']:
            raise lc.ERROR('P_STATE', 'Only an actually elapsed local window may time out')
        if payload['observed_at_ms'] > at + state._profile(message)['max_clock_skew_ms']:
            raise lc.ERROR('P_EXPIRED', 'Timeout observation lies in the future')
        return [{'op': 'local-update', 'unit_id': unit['unit_id'], 'value': {
            'state': 'paused', 'remaining_ms': 0, 'deadline_ms': None,
            'stage': unit['stage'], 'revision': unit['revision'] + 1,
            'notice': 'Local iteration timed out; operator extension or stop is required.'}}]
    instruction = state._validation_bytes(payload['operator_instruction_ref'], live)
    if not instruction.decode('utf-8').strip():
        raise lc.ERROR('P_SCOPE', 'An actual nonempty operator instruction must be retained')
    if event == 'local_budget_extend':
        if not _unit_status(state, unit['unit_id'], at)['applicable']:
            raise lc.ERROR('P_CONTEXT', 'An obsolete incoming mandate cannot be revived by adding time')
        if unit['state'] != 'paused':
            raise lc.ERROR('P_STATE', 'Only a paused local unit may receive additional operational time')
        return [{'op': 'local-update', 'unit_id': unit['unit_id'], 'value': {
            'state': 'ready', 'remaining_ms': payload['additional_ms'], 'deadline_ms': None,
            'started_at_ms': None, 'revision': unit['revision'] + 1, 'notice': None,
            'operator_instruction_ref': payload['operator_instruction_ref']}}]
    if event == 'local_budget_stop':
        effects = [{'op': 'local-update', 'unit_id': unit['unit_id'], 'value': {
            'state': 'terminated', 'deadline_ms': None, 'revision': unit['revision'] + 1,
            'notice': payload['reason'], 'operator_instruction_ref': payload['operator_instruction_ref']}}]
        if payload['target'] == 'task':
            effects.append({'op': 'local-task-stop', 'root_generation': unit['root_generation'],
                            'scope': unit['scope'], 'reason': payload['reason']})
        return effects
    raise lc.ERROR('P_SCHEMA', 'Unknown local budget control')
