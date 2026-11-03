#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Bounded host workflow; semantic work remains the local entity's captured return."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
import uuid

import governed_dispatch
import governed_delivery as wire
import lifecycle as lc
import operator_actions as operator


class Workflow:
    """Dispatch eligible phases while the existing Store owns all effective state."""

    def __init__(self, store, host_config):
        """Bind the existing Store and host execution enrollment.

        Args:
            store: Initialized current-format Store, never a second workflow database.
            host_config: Explicit enrolled P04 workers, destinations, tools and bounds.
        Raises:
            ValueError, OSError: Invalid enrollment or unavailable host resources.
        """
        self.store = store
        self.dispatcher = governed_dispatch.Dispatcher(store, host_config)

    def _record(self, scope, profile, proposal):
        state = self.store.read()
        controller, context = self.dispatcher._controller(state, scope)
        policy = state.resolve(profile, 'profile')
        now = int(time.time() * 1000)
        message = {'protocol': wire.PROTOCOL, 'message_type': 'record_proposal', 'message_id': '0' * 64,
                   'request_id': str(uuid.uuid4()), 'correlation_id': proposal['logical_id'],
                   'engagement': self.store.engagement, 'scope': scope, 'sender': controller,
                   'recipient': controller, 'context': context, 'profile': profile,
                   'expected_head': state.head, 'issued_at_ms': now,
                   'expires_at_ms': now + policy['max_request_duration_ms'],
                   'causes': [], 'attachments': [], 'payload': proposal}
        message['message_id'] = wire.message_id(message)
        response = self.dispatcher._submit(message)
        family = 'delivery.' + proposal['record_type']
        manifest = lc.record_manifest(self.store.engagement, scope, proposal['logical_id'], proposal['record_type'], proposal['record'])
        reference = next(ref for ref in response['receipt']['created_versions'] if ref['version_id'] == lc.version_id(manifest))
        if family not in {'delivery.assignment', 'delivery.context'}:
            raise governed_dispatch.DispatchError('P_SCOPE', 'Workflow creates structural assignments or contexts only')
        return reference, response['receipt']

    def preview(self, assignment_ref):
        """Show current global professional/model facts without making a choice.

        Args:
            assignment_ref: Exact existing local functional assignment.
        Returns:
            Catalogue identities, model availability and current task state.
        Raises:
            ProtocolError: Policy material, identity or current applicability fails.
        """
        state = self.store.read()
        assignment = state.resolve(assignment_ref, 'assignment')
        available = state.assignment_routing(assignment, live=True)
        snapshot = available['snapshot']
        return {'assignment': assignment_ref, 'owner': assignment['owner'],
                'state': state.assignment_states[assignment_ref['version_id']], 'policy_use': available['policy_use'],
                'catalogue_blob_id': snapshot['descriptor']['catalogue_blob_id'],
                'specialties': sorted(snapshot['instructions']),
                'models': [{'provider': provider, 'workload_class': workload, 'model_selector': mapping['model_selector'],
                            'supported': provider in {'json-process/1', 'codex', 'claude'}}
                           for provider, specification in snapshot['models']['providers'].items()
                           for workload, mapping in specification['classes'].items()]}

    def entry(self, scope, work_item, limits, deadline_ms):
        """Create only the deterministic L1 layer gateway from current L0 facts.

        Args:
            scope: Existing L0-approved engagement use scope.
            work_item: Outcome/work identity, not an internal profession or procedure.
            limits: Explicit finite resource bounds within global L0 availability.
            deadline_ms: Absolute finite deadline; contexts cannot extend it.
        Returns:
            Exact functional assignment reference and Store receipt.
        Raises:
            ProtocolError: Current L0 basis, profile gateway or resource bounds fail.
        """
        state = self.store.read()
        _, controller_context = self.dispatcher._controller(state, scope)
        profile_ref = state.resolve(controller_context, 'context')['profile']
        profile = state.resolve(profile_ref, 'profile')
        owner = {'layer': 1, 'work_kind': 'integration', 'question': None, 'work_item': work_item}
        if not any(item['owner'] == owner for item in profile['obligations']):
            raise lc.ERROR('P_SCOPE', 'The profile must declare this L1 layer gateway')
        inputs = [reference for (selected_scope, _), reference in state.sources.items()
                  if selected_scope == scope and state.resolve(reference, 'source')['source_role'] != 'policy']
        policy = state.capability_policy(profile_ref)
        inputs.append(policy['ref'])
        content = state.content_policy(profile_ref)
        if content is not None:
            inputs.append(content['ref'])
        criteria = [reference for reference in inputs if state.resolve(reference, 'source')['source_role'] == 'criteria']
        if len(criteria) != 1:
            raise lc.ERROR('P_CONTEXT', 'An entry requires its one attributable current L0 criterion source')
        identity = hashlib.sha256(lc.canonical({'scope': scope, 'owner': owner, 'inputs': inputs,
                                               'profile': profile_ref, 'policy': policy})).hexdigest()
        record = {'owner': owner, 'responsibility': 'setter', 'assigned_actor': 'layer-entry:' + identity,
                  'profile': profile_ref, 'routing': {'policy': policy['ref']}, 'inherited': inputs,
                  'inputs': [{'slot_id': 'l0:' + reference['logical_id'], 'refs': [reference]} for reference in inputs],
                  'criteria': criteria[0], 'effects': [], 'limits': copy.deepcopy(limits),
                  'deadline_ms': deadline_ms, 'use_scope': scope, 'issued_under': None, 'input_uses': []}
        for path, reference in lc._reference_paths(record):
            if path.startswith(('/inherited/', '/inputs/')) or path == '/criteria':
                record['input_uses'].append({'at': path, 'use_scope': policy['use_scope'] if reference == policy['ref'] else content['use_scope'] if content is not None and reference == content['ref'] else scope})
            elif path == '/routing/policy':
                record['input_uses'].append({'at': path, 'use_scope': policy['use_scope']})
        availability = state.assignment_routing(record, live=True)
        for template in availability['capabilities']['effects']:
            record['effects'].append({**template, 'owner': owner,
                                      'targets': [] if template['operation'] == 'propose' else list(inputs)})
        reference, receipt = self._record(scope, profile_ref, {'record_type': 'assignment',
                                          'logical_id': 'layer-entry:' + identity, 'record': record})
        return {'assignment': reference, 'receipt': receipt}

    def local_entry(self, handoff, phase, acceptance=None):
        """Instantiate a receiving layer gateway from an actual adjacent interface.

        Args:
            handoff: Exact offered handoff UsePoint, retaining its authorized scope.
            phase: Receiver or coordinating setter structural entry.
            acceptance: Actual selected receiving assessment for a setter entry.
        Returns:
            Host-derived local assignment and Store receipt.
        Raises:
            ProtocolError: Exact interface, profile, acceptance or current basis fails.
        """
        state = self.store.read()
        proposal = state.local_entry(handoff, phase, acceptance, live=True)
        record = proposal['record']
        reference, receipt = self._record(record['use_scope'], record['profile'],
                                          {'record_type': 'assignment', **proposal})
        return {'assignment': reference, 'receipt': receipt}

    def _local_event(self, unit_id, event, **payload):
        state = self.store.read()
        unit = state.local_budget['units'][unit_id]
        assigned = state.resolve(unit['anchor'], 'assignment')
        controller, context = self.dispatcher._controller(state, unit['scope'])
        body = {'event': event, 'unit_id': unit_id, **payload}
        request_id = event + ':' + hashlib.sha256(lc.canonical(body)).hexdigest()
        committed = state.requests.get((unit['scope'], lc._owner_key(controller), request_id))
        if committed is not None:
            return {'status': 'already_committed', 'receipt': copy.deepcopy(committed['receipt']), 'error': None}
        profile = state.resolve(assigned['profile'], 'profile')
        now = int(time.time() * 1000)
        message = {'protocol': wire.PROTOCOL, 'message_type': 'control_event', 'message_id': '0' * 64,
            'request_id': request_id, 'correlation_id': unit_id, 'engagement': self.store.engagement,
            'scope': unit['scope'], 'sender': controller, 'recipient': controller, 'context': context,
            'profile': assigned['profile'], 'expected_head': state.head, 'issued_at_ms': now,
            'expires_at_ms': now + profile['max_request_duration_ms'], 'causes': [], 'attachments': [],
            'payload': body}
        message['message_id'] = wire.message_id(message)
        return self.dispatcher._submit(message)

    def pause_due(self, scope='default'):
        """Persist elapsed local windows once and report actual operator notices.

        Args:
            scope: Existing engagement use scope to assess at a scheduling boundary.
        Returns:
            Paused units and paused/stopped notices, including stage and handles.
        Raises:
            ProtocolError: Concurrent unit revision or controller scope changed.
        """
        state = self.store.read()
        now = int(time.time() * 1000)
        paused = []
        for key, unit in state.local_budget['units'].items():
            if unit['scope'] != scope or not state.local_budget_status(key, now)['due']:
                continue
            self._local_event(key, 'local_budget_pause', expected_revision=unit['revision'], observed_at_ms=now)
            paused.append(key)
        state = self.store.read()
        notices = [state.local_budget_status(unit['unit_id'], now) for unit in state.local_budget['units'].values()
                   if unit['scope'] == scope and state.local_budget_status(unit['unit_id'], now)['applicable']
                   and unit['state'] in {'paused', 'terminated'}]
        return {'paused': [state.local_budget_status(key, now) for key in paused], 'notices': notices}

    def extend_local_budget(self, unit_id, expected_revision, additional_ms, operator_instruction_ref):
        """Record an actual operator extension of one exact paused local window.

        Args:
            unit_id: Paused incoming-unit identity.
            expected_revision: Exact displayed operational revision.
            additional_ms: Positive finite additional time, activated on actual start.
            operator_instruction_ref: CAS digest of the actual operator instruction.
        Returns:
            Ordinary Store response; identical replay never grants time twice.
        Raises:
            ProtocolError: Stale, unpaused, malformed or out-of-scope instruction.
        """
        return self._local_event(unit_id, 'local_budget_extend', expected_revision=expected_revision,
            additional_ms=additional_ms, operator_instruction_ref=operator_instruction_ref)

    def stop_local_budget(self, unit_id, expected_revision, target, reason, operator_instruction_ref):
        """Record operational stop intent without claiming a remote process stopped.

        Args:
            unit_id: Exact affected unit establishing the task/scope boundary.
            expected_revision: Displayed current operational revision.
            target: Unit or its task generation.
            reason: Actual operator reason for stopping future processing.
            operator_instruction_ref: CAS digest of the actual operator instruction.
        Returns:
            Store response; accepted semantic records are not rewritten or revoked.
        Raises:
            ProtocolError: Invalid target, stale revision or missing actual instruction.
        """
        return self._local_event(unit_id, 'local_budget_stop', expected_revision=expected_revision,
            target=target, reason=reason, operator_instruction_ref=operator_instruction_ref)

    def advance(self, procedure_ref):
        """Apply one deterministic ordinary step under an actual owner procedure.

        Args:
            procedure_ref: Exact current immutable owner configure_procedure decision.
        Returns:
            The recorded step receipt, or honest waiting/owner-required facts.
        Raises:
            ProtocolError: Current inputs, policy, step or concurrency checks fail.
        """
        state = self.store.read()
        expected = state.procedure_next(procedure_ref)
        if 'step' not in expected:
            return expected
        plan = state.resolve(procedure_ref)['message']['payload']
        assignment = state.resolve(plan['assignment'], 'assignment')
        controller, context = self.dispatcher._controller(state, assignment['use_scope'])
        now = int(time.time() * 1000)
        policy = state.resolve(assignment['profile'], 'profile')
        identity = hashlib.sha256(lc.canonical({'procedure': procedure_ref, 'step': expected['step'],
                                                'triggers': expected['triggers']})).hexdigest()
        message = {'protocol': wire.PROTOCOL, 'message_type': 'control_event', 'message_id': '0' * 64,
            'request_id': 'procedure:' + identity, 'correlation_id': plan['assignment']['logical_id'],
            'engagement': self.store.engagement, 'scope': assignment['use_scope'], 'sender': controller,
            'recipient': controller, 'context': context, 'profile': assignment['profile'],
            'expected_head': state.head, 'issued_at_ms': now,
            'expires_at_ms': now + policy['max_request_duration_ms'],
            'causes': [], 'attachments': [], 'payload': {'event': 'procedure_step',
                'procedure': procedure_ref, 'step': expected['step'], 'triggers': expected['triggers']}}
        message['message_id'] = wire.message_id(message)
        return {'procedure': procedure_ref, 'step': expected['step'],
                'completion': self.dispatcher._submit(message)}

    def invocation_event(self, invocation_id, event, **payload):
        """Record an exact physical event, returning an identical retry receipt.

        Args:
            invocation_id: Existing physical call, allocated before member hashes.
            event: Closed invocation event name from the maintained wire schema.
            **payload: Exact event-specific facts; changing a prior event is rejected.
        Returns:
            The ordinary Store response, without launching a provider operation.
        Raises:
            ProtocolError: Current controller, event, bound or replay conflict fails.
        """
        state = self.store.read()
        invocation = state.invocations[invocation_id]
        scope = invocation['scope']
        controller, context = self.dispatcher._controller(state, scope)
        request_id = event + ':' + invocation_id
        if event == 'invocation_cancelled':
            request_id = event + ':' + hashlib.sha256(lc.canonical(
                {'invocation_id': invocation_id, 'capture_blob_id': payload['capture_blob_id']})).hexdigest()
        body = {'event': event, 'invocation_id': invocation_id, **payload}
        committed = state.requests.get((scope, lc._owner_key(controller), request_id))
        if committed is not None:
            previous = state.messages[committed['message_id']]
            if event == 'invocation_cancelled':
                body['observed_at_ms'] = previous['payload']['observed_at_ms']
            if previous['payload'] != body:
                raise lc.ERROR('P_IDEMPOTENCY', 'Physical event retry changes its exact committed facts')
            return {'status': 'already_committed', 'receipt': copy.deepcopy(committed['receipt']), 'error': None}
        profile = state.resolve(state.resolve(context, 'context')['profile'], 'profile')
        now = int(time.time() * 1000)
        message = {'protocol': wire.PROTOCOL, 'message_type': 'control_event', 'message_id': '0' * 64,
            'request_id': request_id, 'correlation_id': invocation_id, 'engagement': self.store.engagement,
            'scope': scope, 'sender': controller, 'recipient': controller, 'context': context,
            'profile': state.resolve(context, 'context')['profile'], 'expected_head': state.head,
            'issued_at_ms': now, 'expires_at_ms': now + profile['max_request_duration_ms'],
            'causes': [], 'attachments': [], 'payload': body}
        message['message_id'] = wire.message_id(message)
        return self.dispatcher._submit(message)

    def issue_batch(self, jobs, bound_ms=None, invocation_id=None):
        """Issue one finite compatible native call and its exact logical members.

        Args:
            jobs: Explicit assignment/phase/selection/speculation job dictionaries.
            bound_ms: Requested physical elapsed ceiling, clamped by actual grants.
            invocation_id: Optional preallocated call identity for an exact retry.
        Returns:
            Invocation identity, exact issued member grants and ordinary receipt.
        Raises:
            ProtocolError: Incompatible jobs, stale inputs, choice or finite budget.
        """
        if not jobs:
            raise lc.ERROR('P_SCHEMA', 'A physical invocation requires at least one actual job')
        state = self.store.read()
        identifier = invocation_id or 'invocation:' + str(uuid.uuid4())
        existing = state.invocations.get(identifier)
        if existing is not None:
            contexts = [state.resolve(member['context'], 'context') for member in existing['members']]
            same = len(contexts) == len(jobs) and all(
                context['assignment'] == job['assignment'] and context['execution'] == (
                    {'phase': 'selection'} if job['phase'] == 'selection' else
                    {'phase': 'work', 'selection': job.get('selection')})
                and context['speculation'] == job.get('speculation')
                for context, job in zip(contexts, jobs))
            if not same or bound_ms is not None and bound_ms != existing['requested_bound_ms']:
                raise lc.ERROR('P_IDEMPOTENCY', 'Issued physical identity cannot select different jobs or bounds')
            controller, _ = self.dispatcher._controller(state, existing['scope'])
            committed = state.requests[(existing['scope'], lc._owner_key(controller), 'invocation_issued:' + identifier)]
            return {'invocation_id': identifier, 'members': copy.deepcopy(existing['members']),
                    'receipt': copy.deepcopy(committed['receipt'])}
        first = state.resolve(jobs[0]['assignment'], 'assignment')
        controller, context = self.dispatcher._controller(state, first['use_scope'])
        profile = state.resolve(first['profile'], 'profile')
        now = int(time.time() * 1000)
        remaining = min(state.local_budget_status(job['assignment'], now)['remaining_ms'] for job in jobs)
        bound = remaining if bound_ms is None else min(bound_ms, remaining)
        members = []
        for index, job in enumerate(jobs):
            assigned = state.resolve(job['assignment'], 'assignment')
            phase, selection = job['phase'], job.get('selection')
            if phase not in {'selection', 'work'} or (phase == 'selection') != (selection is None):
                raise lc.ERROR('P_SCHEMA', 'Each member requires an explicit valid execution phase')
            key = 'member:' + str(index)
            record = {'owner': assigned['owner'], 'assignment': job['assignment'], 'profile': assigned['profile'],
                'purpose': assigned['responsibility'], 'run_id': identifier + ':' + key,
                'issued_to': assigned['assigned_actor'], 'inputs': copy.deepcopy(assigned['inputs']),
                'attachments': [], 'effects': copy.deepcopy(assigned['effects']),
                'expires_at_ms': min([now + bound] + ([assigned['deadline_ms']] if assigned['deadline_ms'] is not None else [])),
                'speculation': job.get('speculation'), 'ready_basis': state.ready_basis(job['assignment']),
                'execution': {'phase': phase} if phase == 'selection' else {'phase': phase, 'selection': selection}}
            members.append({'member_key': key, 'logical_id': 'execution:' + identifier + ':' + key, 'record': record})
        body = {'event': 'invocation_issued', 'invocation_id': identifier, 'bound_ms': bound, 'members': members}
        message = {'protocol': wire.PROTOCOL, 'message_type': 'control_event', 'message_id': '0' * 64,
            'request_id': 'invocation_issued:' + identifier, 'correlation_id': identifier,
            'engagement': self.store.engagement, 'scope': first['use_scope'], 'sender': controller,
            'recipient': controller, 'context': context, 'profile': first['profile'], 'expected_head': state.head,
            'issued_at_ms': now, 'expires_at_ms': now + profile['max_request_duration_ms'],
            'causes': [], 'attachments': [], 'payload': body}
        message['message_id'] = wire.message_id(message)
        completion = self.dispatcher._submit(message)
        current = self.store.read().invocations[identifier]
        return {'invocation_id': identifier, 'members': copy.deepcopy(current['members']),
                'receipt': completion['receipt']}

    def issue(self, assignment_ref, phase, selection=None, speculation=None):
        """Issue one bounded context for the selected host execution transport.

        Args:
            assignment_ref: Existing local mandate; ownership is not caller-editable.
            phase: Explicit selection or work phase.
            selection: Actual same-entity captured choice required for work only.
            speculation: Exact existing signed grant, or null for ordinary work.
        Returns:
            The fresh exact context and its recording receipt; no worker is invoked.
        Raises:
            ProtocolError: Phase, current mandate, choice or context issuance fails.
        """
        if phase not in {'selection', 'work'} or (phase == 'selection') != (selection is None):
            raise lc.ERROR('P_SCHEMA', 'Selection has no supplied choice; work requires its captured choice')
        state = self.store.read()
        assignment = state.resolve(assignment_ref, 'assignment')
        profile = state.resolve(assignment['profile'], 'profile')
        run_id = 'run:' + str(uuid.uuid4())
        now = int(time.time() * 1000)
        local = state.local_budget_status(assignment_ref, now)
        expires = now + local['remaining_ms']
        if assignment['deadline_ms'] is not None:
            expires = min(expires, assignment['deadline_ms'])
        if speculation is not None:
            grant = state.speculations.get(speculation['version_id'])
            if grant is None or grant['ref'] != speculation:
                raise lc.ERROR('P_SCOPE', 'An existing exact speculative grant is required')
            expires = min(expires, grant['expires_at_ms'])
        record = {'owner': assignment['owner'], 'assignment': assignment_ref, 'profile': assignment['profile'],
                  'purpose': assignment['responsibility'], 'run_id': run_id, 'issued_to': assignment['assigned_actor'],
                  'inputs': copy.deepcopy(assignment['inputs']), 'attachments': [],
                  'effects': copy.deepcopy(assignment['effects']),
                  'expires_at_ms': expires, 'speculation': speculation,
                  'ready_basis': state.ready_basis(assignment_ref),
                  'execution': {'phase': phase} if phase == 'selection' else {'phase': phase, 'selection': selection}}
        context, receipt = self._record(assignment['use_scope'], assignment['profile'],
                                  {'record_type': 'context', 'logical_id': 'execution:' + run_id, 'record': record})
        return {'context': context, 'receipt': receipt}

    def run(self, assignment_ref, phase, selection=None, speculation=None):
        """Issue and synchronously dispatch the existing local process transport.

        Args:
            assignment_ref: Exact current functional assignment.
            phase: Selection or work under that assignment.
            selection: Required captured work choice, otherwise null.
            speculation: Existing exact speculation permission, otherwise null.
        Returns:
            Process outcome and its exact issued context.
        Raises:
            ProtocolError, DispatchError: Issuance or bounded execution fails.
        """
        issued = self.issue(assignment_ref, phase, selection, speculation)
        return {**self.dispatcher.dispatch(issued['context']), 'context': issued['context']}

    def handling_entry(self, episode_ref, task, layer=None):
        """Create only the structural mandate for exact episode handling.

        Args:
            episode_ref: Existing immutable escalation package reference.
            task: Collection, relay, resolution or reconciliation responsibility.
            layer: Entitled handling layer, or null for the episode's local layer.
        Returns:
            Exact assignment reference and structural recording receipt.
        Raises:
            ProtocolError: Episode, adjacency, current owner or allowance is invalid.
        """
        state = self.store.read()
        proposal = state.handling_entry(episode_ref, task, layer)
        record = proposal['record']
        reference, receipt = self._record(record['use_scope'], record['profile'],
                                          {'record_type': 'assignment', **proposal})
        return {'assignment': reference, 'receipt': receipt}

    def ready(self, scope='default', speculation=None):
        """Report exact ready phases and wait reasons without executing work.

        Args:
            scope: Existing engagement use scope.
            speculation: Optional exact operator grant to assess paused branches.
        Returns:
            Deterministically ordered State readiness facts; no authority is created.
        Raises:
            ProtocolError: The scope, mandate or supplied grant is malformed.
        """
        return self.store.read().readiness(scope, speculation)

    def step(self, scope='default', speculation=None):
        """Execute at most one currently eligible phase without retrying a waiter.

        Args:
            scope: Existing engagement use scope.
            speculation: Optional exact existing grant for the requested branches.
        Returns:
            An executed phase and host result, or waiting with authoritative reasons.
        Raises:
            ProtocolError, DispatchError: Eligibility changes or dispatch is rejected.
        """
        facts = self.ready(scope, speculation)
        selected = next((item for item in facts if item['ready']), None)
        if selected is None:
            return {'status': 'waiting', 'readiness': facts}
        result = self.run(selected['assignment'], selected['phase'], selected['selection'], speculation)
        return {'status': 'executed', 'assignment': selected['assignment'],
                'phase': selected['phase'], 'result': result}

    def drive(self, max_steps, scope='default', speculation=None):
        """Run a finite number of ready phases, stopping immediately when waiting.

        Args:
            max_steps: Positive integer call bound within the current profile limit.
            scope: Existing engagement use scope.
            speculation: Optional exact grant; it cannot enlarge the call or task bound.
        Returns:
            Actual executed steps and waiting or step_limit, not a fabricated outcome.
        Raises:
            ProtocolError, DispatchError: Invalid bound, changed eligibility or failed work.
        """
        state = self.store.read()
        _, controller_context = self.dispatcher._controller(state, scope)
        profile = state.resolve(state.resolve(controller_context, 'context')['profile'], 'profile')
        ceiling = profile['scheduling']['max_search_steps']
        if type(max_steps) is not int or not 1 <= max_steps <= ceiling:
            raise lc.ERROR('P_BUDGET', 'A finite drive call must fit the declared search-step bound')
        results = []
        for _ in range(max_steps):
            result = self.step(scope, speculation)
            if result['status'] != 'executed':
                return {**result, 'steps': results}
            results.append(result)
        return {'status': 'step_limit', 'steps': results,
                'readiness': self.ready(scope, speculation)}

    def attempt_status(self, attempt_ref):
        """Report actual attempt bounds and its recorded typed search outcome.

        Args:
            attempt_ref: Exact coordinating assignment identifying the attempt.
        Returns:
            State-derived facts; exhausted driver calls do not invent terminal results.
        Raises:
            ProtocolError: The exact attempt identity is unavailable.
        """
        return self.store.read().attempt_status(attempt_ref)

    def prepare_decision(self, payload, scope='default'):
        """Prepare an exact operator control message without signing human authority.

        Args:
            payload: Typed speculate, resume or terminate decision intent.
            scope: Existing engagement use scope.
        Returns:
            Exact message and non-self-referential human intent descriptor when reserved.
        Raises:
            ProtocolError: The payload is not a permitted operator control operation.
        """
        if payload.get('action') not in {'speculate', 'resume', 'terminate'}:
            raise lc.ERROR('P_SCOPE', 'Workflow prepares operator controls, never owner reasoning')
        state = self.store.read()
        controller, context = self.dispatcher._controller(state, scope)
        profile_ref = state.resolve(context, 'context')['profile']
        profile = state.resolve(profile_ref, 'profile')
        now = int(time.time() * 1000)
        body = copy.deepcopy(payload)
        reserved = body['action'] in {'speculate', 'terminate'}
        sender = controller
        if reserved:
            body['authority_proof'] = '0' * 64
            sender = {'kind': 'authority', 'id': operator.trusted_key('delivery-change')['signer']}
        message = {'protocol': wire.PROTOCOL, 'message_type': 'decision', 'message_id': '0' * 64,
                   'request_id': str(uuid.uuid4()), 'correlation_id': 'operator:' + body['action'],
                   'engagement': self.store.engagement, 'scope': scope, 'sender': sender,
                   'recipient': controller, 'context': context, 'profile': profile_ref,
                   'expected_head': state.head, 'issued_at_ms': now,
                   'expires_at_ms': now + profile['max_request_duration_ms'],
                   'causes': [], 'attachments': [], 'payload': body}
        message['message_id'] = wire.message_id(message)
        wire.validate(message)
        result = {'message': message}
        if reserved:
            intent = wire.action_descriptor(message, lc._hash(profile))
            result['intent'] = intent
            result['parameters'] = {'intent': intent, 'intent_digest': lc._hash(intent)}
            result['purpose'] = 'delivery-change'
            result['target'] = str(self.store.path)
        return result

    def submit_decision(self, message, authority_proof=None):
        """Ingest an exact prepared control and an independently supplied human proof.

        Args:
            message: Unmodified prepared operator message; only its proof digest is filled.
            authority_proof: Actual external signed wrapper for reserved acts, otherwise null.
        Returns:
            The ordinary Store submission and its exact recorded effects.
        Raises:
            ProtocolError, DispatchError: Authority, intent, time, head or typed effects fail.
        """
        value = copy.deepcopy(message)
        if (value.get('message_type') != 'decision'
                or value.get('payload', {}).get('action') not in {'speculate', 'resume', 'terminate'}):
            raise lc.ERROR('P_SCOPE', 'Workflow ingests only exact operator control decisions')
        state = self.store.read()
        controller, context = self.dispatcher._controller(state, value['scope'])
        reserved = value['payload']['action'] in {'speculate', 'terminate'}
        sender = ({'kind': 'authority', 'id': operator.trusted_key('delivery-change')['signer']}
                  if reserved else controller)
        if value['sender'] != sender or value['recipient'] != controller or value['context'] != context:
            raise lc.ERROR('P_ORIGIN', 'Prepared control must use the actual controller audit context')
        if authority_proof is not None:
            value['payload']['authority_proof'] = lc.blob(wire.proof_bytes(authority_proof)[0])
            value['message_id'] = wire.message_id(value)
        return self.dispatcher._submit(value, authority_proof)

    def content_status(self, subject, audience='private'):
        """Assess an exact content output without granting acceptance or release.

        Args:
            subject: Exact product UsePoint inside the current governed Store.
            audience: Private operator facts or a metadata-safe public summary.
        Returns:
            Deterministic content completeness and ordinary justification facts.
        Raises:
            ProtocolError: Output, profile, audience or exact material is invalid.
        """
        import governed_sabsa
        state = self.store.read()
        if audience == 'private':
            return governed_sabsa.assess(state, subject['ref'], subject['use_scope'])
        return governed_sabsa.render(state, subject['ref'], subject['use_scope'], audience)['report']

    def content_views(self, subject, audience='private'):
        """Render governed JSON/Markdown views with separate publication eligibility.

        Args:
            subject: Exact product UsePoint, not a mutable Markdown source.
            audience: Private operator content or explicitly entitled public content.
        Returns:
            Deterministic views and current permission facts; no authority is created.
        Raises:
            ProtocolError: The exact content basis or projection audience is invalid.
        """
        import governed_sabsa
        return governed_sabsa.render(self.store.read(), subject['ref'], subject['use_scope'], audience)

    def status(self, subject):
        """Report output justification and the same shared complete-layer predicate.

        Args:
            subject: Exact output UsePoint, not a mutable path or guessed latest record.
        Returns:
            Current qualification/permission facts and an explicit complete_layer flag.
        Raises:
            ProtocolError: Exact subject identity or supporting history is invalid.
        """
        state = self.store.read()
        result = state.evaluate(subject['ref'], subject['use_scope'], live=True)
        body = state.resolve(subject['ref'])
        complete = False
        if state.versions[subject['ref']['version_id']]['kind'] == 'delivery.product' and body['product_kind'] == 'bundle':
            prior = state.scope
            state.scope = subject['use_scope']
            try:
                state._complete_bundle(body, live=True)
                complete = result['qualified']
            except lc.ERROR:
                complete = False
            finally:
                state.scope = prior
        return {'subject': subject, 'complete_layer': complete, **result}


def main(argv=None):
    """Run bounded host operations without supplying a profession, verdict or return.

    Args:
        argv: Optional explicit host arguments, otherwise the process arguments.
    Returns:
        Zero for the requested step or one for a bounded public-safe diagnostic.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True)
    parser.add_argument('--engagement', required=True)
    parser.add_argument('--config', required=True)
    commands = parser.add_subparsers(dest='command', required=True)
    preview = commands.add_parser('preview'); preview.add_argument('assignment')
    entry = commands.add_parser('entry'); entry.add_argument('--scope', required=True); entry.add_argument('--work-item', required=True)
    entry.add_argument('--limits'); entry.add_argument('--deadline-ms', type=int)
    local = commands.add_parser('local-entry'); local.add_argument('handoff'); local.add_argument('--phase', choices=('receiver', 'setter'), required=True)
    local.add_argument('--acceptance')
    run = commands.add_parser('run'); run.add_argument('assignment'); run.add_argument('--phase', choices=('selection', 'work'), required=True)
    run.add_argument('--selection'); run.add_argument('--speculation')
    status = commands.add_parser('status'); status.add_argument('subject')
    for name in ('content-status', 'content-views'):
        command = commands.add_parser(name); command.add_argument('subject')
        command.add_argument('--audience', choices=('private', 'public'), default='private')
    handling = commands.add_parser('handling-entry'); handling.add_argument('episode')
    handling.add_argument('--task', choices=('collect', 'relay', 'resolve', 'reconcile'), required=True)
    handling.add_argument('--layer', type=int)
    for name in ('ready', 'step', 'drive'):
        command = commands.add_parser(name)
        command.add_argument('--scope', default='default'); command.add_argument('--speculation')
        if name == 'drive':
            command.add_argument('--max-steps', type=int, required=True)
    attempt = commands.add_parser('attempt-status'); attempt.add_argument('attempt')
    prepare = commands.add_parser('prepare-decision'); prepare.add_argument('payload'); prepare.add_argument('--scope', default='default')
    submit = commands.add_parser('submit-decision'); submit.add_argument('message'); submit.add_argument('--authority-proof')
    args = parser.parse_args(argv)
    def read(path):
        return lc.loads(operator.regular(path))
    try:
        workflow = Workflow(lc.Store(args.store, args.engagement), read(args.config))
        if args.command == 'preview':
            result = workflow.preview(read(args.assignment))
        elif args.command == 'entry':
            result = workflow.entry(args.scope, args.work_item, read(args.limits) if args.limits else [], args.deadline_ms)
        elif args.command == 'local-entry':
            result = workflow.local_entry(read(args.handoff), args.phase, read(args.acceptance) if args.acceptance else None)
        elif args.command == 'run':
            result = workflow.run(read(args.assignment), args.phase, read(args.selection) if args.selection else None,
                                  read(args.speculation) if args.speculation else None)
        elif args.command == 'status':
            result = workflow.status(read(args.subject))
        elif args.command == 'content-status':
            result = workflow.content_status(read(args.subject), args.audience)
        elif args.command == 'content-views':
            result = workflow.content_views(read(args.subject), args.audience)
        elif args.command == 'handling-entry':
            result = workflow.handling_entry(read(args.episode), args.task, args.layer)
        elif args.command == 'attempt-status':
            result = workflow.attempt_status(read(args.attempt))
        elif args.command == 'prepare-decision':
            result = workflow.prepare_decision(read(args.payload), args.scope)
        elif args.command == 'submit-decision':
            result = workflow.submit_decision(read(args.message), operator.regular(args.authority_proof) if args.authority_proof else None)
        else:
            speculation = read(args.speculation) if args.speculation else None
            if args.command == 'drive':
                result = workflow.drive(args.max_steps, args.scope, speculation)
            elif args.command == 'step':
                result = workflow.step(args.scope, speculation)
            else:
                result = workflow.ready(args.scope, speculation)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, OSError) as error:
        print(json.dumps({'status': 'rejected', 'code': getattr(error, 'code', 'P_CONTEXT'), 'message': str(error)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
