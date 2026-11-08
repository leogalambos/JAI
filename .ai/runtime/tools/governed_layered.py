#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Native layered front door over the existing Store, scheduler and effect broker.

Session files locate an exact host enrollment. They contain no workflow state,
permissions, acceptance or cached journal head. Semantic work belongs to the
actual local producer; this module prepares transport and structural metadata.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import time
import uuid

import governed_delivery as wire
import governed_native as native
import governed_native_provider as provider
import lifecycle as lc
import operator_actions as operator

LOCATOR = 'jai.layered-session/1'
OPERATIONS = {
    'next': ('scope', 'speculation'), 'checkpoint': ('scope',),
    'entry': ('scope', 'work_item', 'limits', 'deadline_ms'),
    'local_entry': ('handoff', 'phase', 'acceptance'),
    'handling_entry': ('episode', 'task', 'layer'),
    'output_status': ('subject',), 'human_handoff': ('episode', 'scope'),
    'prepare_human': ('payload', 'purpose', 'scope'),
    'stencil': ('context', 'record_type', 'logical_id', 'fields', 'uses'),
}


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _write_once(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open('xb') as stream:
            stream.write(raw)
    except FileExistsError:
        if operator.regular(path) != raw:
            raise ValueError('Existing session enrollment differs; use an explicit new enrollment') from None


def _save_locator(home, engagement, config, *, versioned=False):
    raw = lc.canonical(config)
    digest = _digest(raw)
    suffix = '.' + digest if versioned else ''
    host = home / (engagement + suffix + '.host.json')
    locator = home / (engagement + suffix + '.session.json')
    _write_once(host, raw)
    value = {'schema_version': LOCATOR, 'engagement': engagement,
             'journal': str(home / (engagement + '.jsonl')),
             'host_config': str(host), 'host_config_digest': digest}
    _write_once(locator, lc.canonical(value))
    return locator


class LayeredSession(native.NativeSession):
    """Drive native phases without replacing the governed workflow or its state."""

    def __init__(self, store, config, locator):
        """Keep one warm Store and a nonauthoritative enrollment locator.

        Args:
            store: Existing sole engagement Store.
            config: Explicit current host enrollment, validated by Dispatcher.
            locator: Machine-generated locator path for a later cold resume.
        Raises:
            ValueError, OSError: Enrollment or journal is unavailable or invalid.
        """
        super().__init__(store, config)
        self.locator = Path(locator).resolve()

    @classmethod
    def create(cls, home, engagement, task, provider_name, work_item, deadline_ms=None,
               limit_ms=None, criteria=None, config=None, model_config=None, local_budget=None, execution_profile=None, execution_context_policy=None):
        """Capture an actual request and create the initial L1 structural gateway.

        Args:
            home: Workspace journal/enrollment directory, normally .fabric.
            engagement: Bounded nontraversing journal identity.
            task: Exact nonempty UTF-8 operator intent bytes.
            provider_name: Active codex or claude session, never a model subprocess.
            work_item: Explicit stable outcome identity.
            deadline_ms: Explicit optional global stop in milliseconds, otherwise None.
            limit_ms: Explicit optional aggregate elapsed cap, otherwise None.
            criteria: Actual explicit criteria bytes; None reuses task verbatim.
            config: Optional existing host enrollment; None creates read/propose defaults.
            model_config: Existing model-registry override path, if supplied.
            execution_profile: Explicit operational profile for this new run only.
            execution_context_policy: Validated context from the session selection;
                captured at new entry and preserved by cold resume.
            local_budget: Optional iteration_ms/max_reworks configuration, defaulting
                to ten minutes per local iteration and three actual reworks.
        Returns:
            Warm session and exact initial recording receipt/references.
        Raises:
            ValueError, ProtocolError, OSError: Invalid inputs, existing engagement,
                enrollment collision or ordinary core admission rejection.
        """
        if (not isinstance(engagement, str) or not engagement or len(engagement) > 128
                or engagement in {'.', '..'} or any(char in engagement for char in '/\\')):
            raise ValueError('Bounded nontraversing engagement identity required')
        home = Path(home).resolve()
        store = lc.Store(home / (engagement + '.jsonl'), engagement)
        if store.read().initialized:
            raise ValueError('Existing engagement requires resume; startup never replaces history')
        limits = [] if limit_ms is None else [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': limit_ms}]
        supplied = copy.deepcopy(config) if config is not None else {
            'protocol': 'jai.host-dispatch/1', 'workers': [], 'destinations': [], 'tools': [],
            'limits': {'packet_bytes': 2097152, 'total_bytes': 8388608}}
        # Persist only enrollment before journal ingress, so interruption cannot
        # leave a committed engagement requiring a handwritten resume config.
        import governed_dispatch
        governed_dispatch.Dispatcher(store, supplied)
        locator = _save_locator(home, engagement, supplied, versioned=config is not None)
        initialized = provider.bootstrap(store, task, task if criteria is None else criteria,
            provider_name, work_item, limits, deadline_ms, model_config,
            destinations=supplied['destinations'], tools=supplied['tools'],
            packet_bytes=supplied['limits']['packet_bytes'], total_bytes=supplied['limits']['total_bytes'],
            local_budget=local_budget, project=home.parent, execution_profile=execution_profile,
            execution_context_policy=execution_context_policy)
        session = cls(store, supplied, locator)
        entry = session.workflow.entry('default', work_item, limits, deadline_ms)
        return session, {'locator': str(locator), 'inputs': initialized['sources'],
            'entry': entry, 'criteria_basis': 'same-verbatim-request' if criteria is None else 'explicit-criteria'}

    @classmethod
    def open(cls, locator, config=None):
        """Cold-load the accepted journal once using the exact pinned enrollment.

        Args:
            locator: Machine-generated session locator; never workflow authority.
            config: Explicit replacement enrollment, otherwise the pinned file.
        Returns:
            A warm session retaining the reconstructed Store across later turns.
        Raises:
            ValueError, ProtocolError, OSError: Changed/missing pinned enrollment,
                malformed locator, unavailable journal or invalid replacement.
        """
        path = Path(locator).resolve()
        value = lc.loads(operator.regular(path))
        expected = {'schema_version', 'engagement', 'journal', 'host_config', 'host_config_digest'}
        if set(value) != expected or value['schema_version'] != LOCATOR:
            raise ValueError('Current layered session locator required')
        raw = None
        if config is None:
            raw = lc.canonical(lc.loads(operator.regular(value['host_config'])))
            if _digest(raw) != value['host_config_digest']:
                raise ValueError('Pinned host enrollment changed; supply an explicit new config')
        store = lc.Store(value['journal'], value['engagement'])
        if Path(value['journal']).resolve() != path.parent / (value['engagement'] + '.jsonl'):
            raise ValueError('Locator must name the same engagement journal used by the fabric CLI')
        enrollment = lc.loads(raw) if config is None else copy.deepcopy(config)
        session = cls(store, enrollment, path)
        session.store.read()
        if config is not None:
            session.locator = _save_locator(path.parent, value['engagement'], enrollment, versioned=True)
        session._initial_entry()
        return session

    def _roots(self):
        state = self.store.read()
        return [state._reference(key) for key, value in state.versions.items()
                if value['kind'] == 'delivery.assignment'
                and value['content']['record']['issued_under'] is None
                and value['content']['record'].get('handling') is None
                and value['content']['record']['owner']['layer'] == 1]

    def _initial_entry(self):
        state = self.store.read()
        if not state.initialized:
            raise ValueError('Startup did not commit inputs; start again with the actual task')
        if not self._roots():
            message = state.transactions[0]['operations'][0]['data']['message']
            if message['message_type'] != 'bootstrap':
                raise lc.ERROR('P_CONTEXT', 'Current-format bootstrap is required for initial entry continuation')
            profile = message['payload']['profile']['record']
            self.workflow.entry(message['scope'], message['correlation_id'],
                profile['scheduling']['control_limits'], profile['scheduling']['initial_deadline_ms'])

    def next(self, scope='default', speculation=None):
        """Advance actual owner procedures, then offer one compatible physical call.

        Args:
            scope: Existing approved engagement use scope.
            speculation: Exact existing grant, or None for pessimistic escalation pause.
        Returns:
            One issued/prepared invocation, honest reconciliation for an already
            exposed uncertain call, or waiting facts. Logical author/reviewer phases
            never share a physical context and ordinary progress never replays history.
        Raises:
            ProtocolError, ValueError: Current owner procedure, grant or issuance fails.
        """
        notices = self.pause_due(scope)['notices']
        while True:
            state = self.store.read()
            pending = next((reference for (assignment_id, use), reference in sorted(state.procedures.items())
                            if use == scope
                            and state._status(reference, use) == {'validity': 'valid', 'applicable': True}
                            and state._status(state._reference(assignment_id), use) == {'validity': 'valid', 'applicable': True}
                            and 'step' in state.procedure_next(reference)), None)
            if pending is None:
                break
            before = state.head
            self.workflow.advance(pending)
            if self.store.read().head == before:
                raise lc.ERROR('P_CONTEXT', 'Ordinary procedure progress did not establish its declared step')
        state = self.store.read()
        for invocation, physical in state.invocations.items():
            if physical['scope'] != scope:
                continue
            if physical['state'] == 'issued':
                if physical['deadline_ms'] <= int(time.time() * 1000):
                    return {'status': 'reconcile', 'reason': 'issued-grant-expired-before-dispatch',
                            'invocation_id': invocation, 'members': copy.deepcopy(physical['members']),
                            'operator_notices': notices, 'authority_granted': False}
                return {'status': 'invoke', 'invocation_id': invocation,
                        'members': copy.deepcopy(physical['members']), 'prepared': self.prepare(invocation),
                        'operator_notices': notices}
            if physical['state'] in {'prepared', 'uncertain'}:
                return {'status': 'reconcile', 'reason': 'native-invocation-outcome-unconfirmed',
                        'invocation_id': invocation, 'members': copy.deepcopy(physical['members']),
                        'task_name': provider._task_name(invocation), 'operator_notices': notices, 'authority_granted': False}
        facts = self.workflow.ready(scope, speculation)
        selected = next((item for item in facts if item['ready']), None)
        if selected is None:
            return {'status': 'paused' if notices else 'waiting', 'readiness': facts,
                    'inflight': self.checkpoint(scope)['inflight'], 'operator_notices': notices}
        traits = state.invocation_traits(selected['assignment'], selected['phase'], selected['selection'])
        jobs = [{'assignment': item['assignment'], 'phase': item['phase'],
                 'selection': item['selection'], 'speculation': speculation}
                for item in facts if item['ready'] and state.invocation_traits(
                    item['assignment'], item['phase'], item['selection']) == traits]
        issued = self.issue_batch(jobs)
        return {'status': 'invoke', **issued, 'prepared': self.prepare(issued['invocation_id']),
                'operator_notices': notices}

    def prepare(self, invocation):
        """Expose the common durable physical preparation for layered processing.

        Args:
            invocation: Exact previously issued physical identity, singleton or batch.
        Returns:
            The unchanged common native descriptor, with precise member input rights
            and small semantic prompts referencing immutable materials/procedures.
        Raises:
            ProtocolError, ValueError, OSError: Existing preparation requirements fail.
        """
        return super().prepare(invocation)

    def checkpoint(self, scope='default'):
        """Describe actual resume state without granting or persisting permissions.

        Args:
            scope: Existing engagement use scope.
        Returns:
            Current journal head, exact governing input locators, ready phases,
            inflight bindings, unresolved effect ACKs, episode refs and root refs.
        Raises:
            ProtocolError: Required state or scope is unavailable.
        """
        state = self.store.read()
        inflight = []
        for run_id, details in state.run_details.items():
            if details['context']['scope'] != scope or state.run_states[run_id] not in {'issued', 'running'}:
                continue
            inflight.append({'run_id': run_id, 'context': details['context'],
                'state': state.run_states[run_id], 'native': copy.deepcopy(details.get('native')),
                'pending_effects': [identifier for identifier, request in details.get('broker_requests', {}).items()
                                    if request['status'] == 'pending']})
        return {'locator': str(self.locator), 'engagement': state.engagement,
            'journal': str(self.store.path), 'head': state.head,
            'inputs': [{'ref': ref, 'use_scope': use} for (use, _), ref in state.sources.items() if use == scope],
            'roots': self._roots(), 'readiness': self.workflow.ready(scope), 'inflight': inflight,
            'local_budgets': [state.local_budget_status(identifier) for identifier, unit in state.local_budget['units'].items()
                              if unit['scope'] == scope],
            'invocations': [self.status(identifier) for identifier, value in state.invocations.items()
                            if value['scope'] == scope and value['state'] in {'issued', 'prepared', 'running', 'uncertain'}],
            'episodes': [{'root': value['root'], 'current': value['current']}
                         for value in state.episodes.values() if value['scope'] == scope]}

    def entry(self, scope, work_item, limits, deadline_ms):
        """Enter an actual current L0 input basis through the existing structural gate.

        Args:
            scope: Existing approved use scope.
            work_item: Actual outcome identity, not a profession or changed requirement.
            limits: Explicit finite bounds within current profile capabilities.
            deadline_ms: Explicit future deadline allowed by the current mandate.
        Returns:
            Exact root assignment and receipt; old conclusions are not transferred.
        Raises:
            ProtocolError: Current input basis, profile, budget or reinstatement guards fail.
        """
        return self.workflow.entry(scope, work_item, limits, deadline_ms)

    def local_entry(self, handoff, phase, acceptance=None):
        """Forward an actual adjacent handoff into the existing local gateway API.

        Args:
            handoff: Exact published handoff UsePoint.
            phase: Existing receiver or setter responsibility.
            acceptance: Actual receiving assessment where required.
        Returns:
            Canonical structural assignment and receipt, with no local profession chosen.
        Raises:
            ProtocolError: Existing adjacency, acceptance or applicability guards fail.
        """
        return self.workflow.local_entry(handoff, phase, acceptance)

    def handling_entry(self, episode, task, layer=None):
        """Forward an actual episode to its bounded existing handling responsibility.

        Args:
            episode: Exact recorded escalation package reference.
            task: Existing collect, relay, resolve or reconcile function.
            layer: Exact entitled layer, or the core's local default.
        Returns:
            Canonical handling mandate and recording receipt.
        Raises:
            ProtocolError: Existing episode, adjacency, collection or budget guard fails.
        """
        return self.workflow.handling_entry(episode, task, layer)

    def output_status(self, subject):
        """Inspect one exact output using the existing justification predicate.

        Args:
            subject: Exact output UsePoint, not a mutable filename.
        Returns:
            Existing qualification, permissions and complete-layer facts.
        Raises:
            ProtocolError: Exact output or relevant dependencies are unavailable.
        """
        return self.workflow.status(subject)

    def human_handoff(self, episode=None, scope='default'):
        """Show actual conflicts and decision requests even without an enrolled key.

        Args:
            episode: Exact escalation reference, or None to list open scope episodes.
            scope: Existing engagement use scope.
        Returns:
            Read-only dossier with exact records, affected uses, recorded options,
            material availability and the actual L0 capability-readiness gap.
        Raises:
            ProtocolError: An explicitly requested episode belongs to another scope.
        """
        state = self.store.read()
        episodes = [state._episode(episode)] if episode is not None else [
            item for item in state.episodes.values() if item['scope'] == scope
            and state.escalations.get(item['root']['version_id']) == 'open']
        result = []
        for item in episodes:
            if item['scope'] != scope:
                raise lc.ERROR('P_SCOPE', 'Escalation dossier must preserve its exact use scope')
            record = state.resolve(item['current'], 'product')
            message = next((value for value in state.messages.values()
                if value['message_type'] == 'escalation' and value['payload']['package'] == item['current']), None)
            conflicts = next((entry['refs'] for entry in record['related'] if entry['slot_id'] == 'conflicts'), [])
            materials = []
            for reference in [item['current'], *conflicts]:
                body = state.resolve(reference)
                for identifier in body.get('material', []):
                    try:
                        raw = self.store._blob(identifier)
                        materials.append({'ref': reference, 'blob_id': identifier,
                            'status': 'available', 'text': raw.decode('utf-8', errors='replace')})
                    except (OSError, ValueError):
                        materials.append({'ref': reference, 'blob_id': identifier, 'status': 'unavailable'})
            human = item['layer'] == 1 or any(event['kind'] == 'relay'
                and event['payload'].get('episode') == item['root']
                and event['payload'].get('to_layer') == 0 for event in state.events)
            result.append({'episode': item['root'], 'package': item['current'],
                'state': state.escalations.get(item['root']['version_id']),
                'conflicts': conflicts, 'affected_uses': item['members'],
                'requested_decisions': message['payload']['requested_decisions'] if message else [],
                'material': materials, 'requires_l0': human})
        readiness = {'required_purpose': 'delivery-change', 'available': False,
                     'reason': 'No open escalation requiring L0'}
        if any(item['requires_l0'] for item in result):
            try:
                key = operator.trusted_key('delivery-change')
                wire._require_scope(key, state.engagement, scope)
                readiness.update(available=True, signer=key['signer'], reason=None)
            except (OSError, ValueError):
                readiness['reason'] = 'No current delivery-change key enrolled for this engagement and scope'
        return {'checkpoint': self.checkpoint(scope), 'episodes': result,
                'signing_readiness': readiness, 'authority_granted': False}

    def prepare_human(self, payload, purpose='delivery-change', scope='default'):
        """Prepare exact unsigned L0 change files, never sign or submit the decision.

        Args:
            payload: Actual proposed human decision, including its explicit effects.
            purpose: delivery-change; acceptance and release use their existing workflows.
            scope: Exact existing use scope.
        Returns:
            Concrete unsigned message/intent/request package if a matching public
            key is enrolled, with an exact external sign command and conventional
            private-key locator (not a private-key read). Otherwise an explicit
            readiness gap without a signer.
        Raises:
            ProtocolError, ValueError, OSError: Invalid action, conflicting proof,
                malformed proposed effects or unavailable output files.
        """
        allowed = {'continue', 'reformulate', 'reinstate', 'terminate', 'speculate',
                   'resolve_escalation', 'exclude_content'}
        if purpose != 'delivery-change' or payload.get('action') not in allowed:
            raise lc.ERROR('P_SCOPE', 'Layered handoff prepares explicit L0 changes, not acceptance or release')
        if payload.get('authority_proof') not in {None, lc.ZERO}:
            raise ValueError('Preparation cannot rewrite an existing human proof')
        state = self.store.read()
        try:
            key = operator.trusted_key(purpose)
            wire._require_scope(key, state.engagement, scope)
        except (OSError, ValueError):
            return {'status': 'unavailable', 'required_purpose': purpose,
                    'reason': 'No current public-key enrollment for the exact engagement and scope',
                    'proposed_payload': copy.deepcopy(payload), 'message': None,
                    'request': None, 'authority_granted': False}
        controller, context = self.workflow.dispatcher._controller(state, scope)
        profile_ref = state.resolve(context, 'context')['profile']
        profile = state.resolve(profile_ref, 'profile')
        now = int(time.time() * 1000)
        body = copy.deepcopy(payload)
        body['authority_proof'] = lc.ZERO
        message = {'protocol': wire.PROTOCOL, 'message_type': 'decision', 'message_id': lc.ZERO,
            'request_id': str(uuid.uuid4()), 'correlation_id': 'human:' + body['action'],
            'engagement': state.engagement, 'scope': scope,
            'sender': {'kind': 'authority', 'id': key['signer']}, 'recipient': controller,
            'context': context, 'profile': profile_ref, 'expected_head': state.head,
            'issued_at_ms': now, 'expires_at_ms': now + min(3600000, profile['max_request_duration_ms']),
            'causes': [], 'attachments': [], 'payload': body}
        message['message_id'] = wire.message_id(message)
        wire.validate(message)
        intent = wire.action_descriptor(message, lc._hash(profile))
        parameters = {'intent': intent, 'intent_digest': lc._hash(intent)}
        directory = self.store.path.parent / (state.engagement + '.human') / message['request_id']
        _write_once(directory / 'unsigned-message.json', lc.canonical(message))
        _write_once(directory / 'intent.json', lc.canonical(intent))
        request = operator.request(purpose, 'Review the exact proposed layered decision',
            directory / 'intent.json', str(self.store.path), parameters,
            ttl=max(1, min(3600, (message['expires_at_ms'] - now) // 1000)))
        _write_once(directory / 'request.json', operator.canonical(request))
        return {'status': 'prepared', 'package': str(directory), 'message': message,
            'intent': intent, 'request': request, 'authority_granted': False,
            'external_actions': {'signer_tool': str(Path(operator.__file__).resolve()),
                'request': str(directory / 'request.json'), 'workspace': str(self.store.path.parent.parent),
                'private_key': str(operator.default_private_key()),
                'sign_command': ['python3', str(Path(operator.__file__).resolve()), 'sign',
                    str(directory / 'request.json'), '--workspace', str(self.store.path.parent.parent)],
                'bind_command': ['python3', str(Path(__file__).resolve()), 'bind-human',
                    '--package', str(directory), '--receipt', '<actual-public-receipt-path>'],
                'submit_command': ['python3', str(Path(__file__).resolve().parents[1] / 'fabric/fabric.py'),
                    'submit', state.engagement, '--message', str(directory / 'message.json'),
                    '--authority-proof', str(directory / 'proof.json')],
                'submit_environment': {'FABRIC_HOME': str(self.store.path.parent)}}}

    def stencil(self, context, record_type, logical_id, fields, uses=()):
        """Fill exact packet-derived metadata around explicit producer semantic fields.

        Args:
            context: Exact issued work context, not a selection context.
            record_type: Existing source, assignment, product or assessment family.
            logical_id: Producer's explicit logical identity for its new record.
            fields: Actual semantic fields; conflicts with structural metadata reject.
            uses: Explicit scoped references for new/ambiguous dependencies, if needed.
        Returns:
            A closed proposal, without registration, qualification or inferred verdict.
        Raises:
            ProtocolError, ValueError: Missing semantics, conflicting structural fields,
                ambiguous dependency scope or unsupported proposal family.
        """
        import governed_records
        return governed_records.build_proposal(self._run(context).packet, record_type, logical_id, fields, uses)


def bind_human(package, receipt):
    """Bind an actual external public receipt without submitting an authority act.

    Args:
        package: Exact unsigned package produced by prepare_human.
        receipt: Actual public receipt path returned by the external host signer.
    Returns:
        Final message and proof paths; journal_submitted is always False.
    Raises:
        ValueError, ProtocolError, OSError: Stale intent, invalid signature, changed
            proposal or conflicting existing bound output.
    """
    directory = Path(package).resolve()
    request = json.loads(operator.regular(directory / 'request.json'))
    intent = operator.validate_human_intent_request(request)
    observed = json.loads(operator.regular(receipt))
    message = lc.loads(operator.regular(directory / 'unsigned-message.json'))
    if wire.action_descriptor(message, intent['policy_digest']) != intent:
        raise ValueError('Unsigned proposal differs from the exact externally approved intent')
    wrapper = {'request': request, 'receipt': observed}
    raw = wire.verify_proof(wrapper, request['kind'], int(time.time() * 1000))['raw']
    message['payload']['authority_proof'] = lc.blob(raw)
    message['message_id'] = wire.message_id(message)
    wire.validate(message)
    _write_once(directory / 'proof.json', raw)
    _write_once(directory / 'message.json', lc.canonical(message))
    return {'message': str(directory / 'message.json'), 'proof': str(directory / 'proof.json'),
            'journal_submitted': False}


def main(argv=None):
    """Open the ordinary foreground layered host, or bind an external public receipt.

    Args:
        argv: Explicit CLI arguments, otherwise process arguments.
    Returns:
        Zero after a bounded host close or successful receipt binding.
    Raises:
        ValueError, ProtocolError, OSError: Invalid ingress, enrollment, receipt or state.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    start = commands.add_parser('start')
    start.add_argument('--home', default='.fabric')
    start.add_argument('--engagement', required=True)
    start.add_argument('--task', required=True)
    start.add_argument('--criteria')
    start.add_argument('--provider', choices=('codex', 'claude'), required=True)
    start.add_argument('--work-item', required=True)
    start.add_argument('--deadline-ms', type=int)
    start.add_argument('--limit-ms', type=int)
    start.add_argument('--iteration-ms', type=int, default=600000)
    start.add_argument('--max-reworks', type=int, default=3)
    start.add_argument('--config')
    start.add_argument('--model-config')
    start.add_argument('--execution-profile')
    start.add_argument('--execution-context-policy', choices=sorted(provider.execution_profiles.CONTEXT_POLICIES))
    resume = commands.add_parser('resume')
    resume.add_argument('--session', required=True)
    resume.add_argument('--config')
    binding = commands.add_parser('bind-human')
    binding.add_argument('--package', required=True)
    binding.add_argument('--receipt', required=True)
    for name in ('budget-status', 'extend-budget', 'stop-budget'):
        operation = commands.add_parser(name)
        operation.add_argument('--session', required=True)
        operation.add_argument('--unit-id', required=True)
        if name != 'budget-status':
            operation.add_argument('--expected-revision', type=int, required=True)
            operation.add_argument('--operator-instruction', required=True)
        if name == 'extend-budget':
            operation.add_argument('--additional-ms', type=int, required=True)
        if name == 'stop-budget':
            operation.add_argument('--target', choices=('unit', 'task'), required=True)
            operation.add_argument('--reason', required=True)
    args = parser.parse_args(argv)
    if args.command == 'bind-human':
        print(json.dumps(bind_human(args.package, args.receipt), ensure_ascii=False))
        return 0
    if args.command in {'budget-status', 'extend-budget', 'stop-budget'}:
        session = LayeredSession.open(args.session)
        if args.command == 'budget-status':
            result = session.local_budget_status(args.unit_id)
        else:
            instruction = session.store.put_blob(operator.regular(args.operator_instruction))
            if args.command == 'extend-budget':
                result = session.extend_local_budget(args.unit_id, args.expected_revision, args.additional_ms, instruction)
            else:
                result = session.stop_local_budget(args.unit_id, args.expected_revision, args.target, args.reason, instruction)
        print(json.dumps({'operation': args.command, 'result': result}, ensure_ascii=False))
        return 0
    config = lc.loads(operator.regular(args.config)) if args.config else None
    if args.command == 'start':
        session, created = LayeredSession.create(args.home, args.engagement,
            operator.regular(args.task), args.provider, args.work_item, args.deadline_ms,
            args.limit_ms, operator.regular(args.criteria) if args.criteria else None,
            config, args.model_config, local_budget={'iteration_ms': args.iteration_ms, 'max_reworks': args.max_reworks},
            execution_profile=args.execution_profile, execution_context_policy=args.execution_context_policy)
        result = {'created': created, 'next': session.next(), 'checkpoint': session.checkpoint()}
    else:
        session = LayeredSession.open(args.session, config)
        result = {'checkpoint': session.checkpoint()}
    print(json.dumps({'id': 'startup', 'ok': True, 'result': result}, ensure_ascii=False), flush=True)
    return native.serve(session, sys.stdin.buffer, sys.stdout, OPERATIONS)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        print(json.dumps({'error': {'code': getattr(error, 'code', 'P_CONTEXT'),
                                    'message': str(error)}}), file=sys.stderr)
        raise SystemExit(2)
