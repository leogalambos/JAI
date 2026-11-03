#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Parent-only native lifecycle over one warm Gen2 Store; never launch a model.

A provider's existing orchestrator supplies actual native handles and received
bodies. This foreground JSON-lines carrier retains the Store between those tool
calls. It is not an agent factory, network service or second authority store.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time

import governed_dispatch as dispatch
import governed_delivery as wire
import governed_workflow
import lifecycle as lc
import operator_actions as operator


class NativeSession:
    """Bind physical native observations to individually governed logical members."""

    def __init__(self, store, config):
        """Retain the sole warm Store and existing shared broker enrollment.

        Args:
            store: Current engagement Store; no second authoritative cache is made.
            config: Explicit existing dispatcher enrollment and finite transport limits.
        Raises:
            ValueError, OSError: Enrollment or local resources are unavailable.
        """
        self.store = store
        self.workflow = governed_workflow.Workflow(store, config)
        self._runs = {}

    def _peer(self):
        base = self.workflow.dispatcher
        peer = object.__new__(dispatch.Dispatcher)
        for name in ('store', 'config', 'packet_limit', 'total_limit', 'sensitive'):
            setattr(peer, name, getattr(base, name))
        peer._running_context = peer._journal_seen = None
        return peer

    def _invocation(self, invocation):
        state = self.store.read()
        if not isinstance(invocation, str) or invocation not in state.invocations:
            raise dispatch.DispatchError('P_ORIGIN', 'An exact issued physical invocation is required')
        return state, state.invocations[invocation]

    def _run(self, context_ref):
        key = context_ref['version_id']
        if key in self._runs:
            return self._runs[key]
        state = self.store.read()
        context = state.resolve(context_ref, 'context')
        details = state.run_details[context['run_id']]
        invocation = state.invocations[details['invocation_id']]
        peer = self._peer()
        if invocation.get('manifest_blob_id'):
            manifest = lc.loads(self.store._blob(invocation['manifest_blob_id']))
            member = next(item for item in manifest['members'] if item['context'] == context_ref)
            packet = lc.loads(self.store._blob(member['packet_blob_id']))
            peer.packet_limit = packet['transport_limits']['packet_bytes']
            peer.total_limit = packet['transport_limits']['total_bytes']
            peer.execution = state.context_execution(context, live=False)
            peer.handles = {item['handle']: lc.canonical(item['record']) for item in packet['manifest']}
            peer.delivered_handles = {item['handle']: item['blob_id'] for item in packet['attachments']}
            snapshot = peer.execution['snapshot']['descriptor']
            peer.intrinsic_handles = {'catalogue': snapshot['catalogue_blob_id'],
                **{'instruction:' + slug: blob for slug, blob in snapshot['instruction_blobs'].items()}}
            peer.allowed_blobs = {item['blob_id'] for item in packet['attachments']}
            peer.allowed_blobs.update(material['blob_id'] for returned in packet.get('owned_returns', [])
                                      for item in returned['records'] for material in item['material'])
            handling = packet.get('handling')
            if handling:
                peer.allowed_blobs.update(material['blob_id'] for item in
                    [handling['package'], *handling['conflicts'], *handling['inputs']]
                    for material in item['material'] if material['status'] == 'available')
            peer.allowed_blobs.update(details.get('broker_allowed_blobs', []))
            peer.transferred = details.get('broker_bytes', len(lc.canonical(packet)) + 1)
            peer.request_ids, peer.audit = set(), []
        else:
            _, context, _, packet, _, _ = peer._prepare_common(context_ref)
            packet['member_key'] = details['member_key']
            packet['invocation_id'] = details['invocation_id']
            packet['transport_limits'] = {'packet_bytes': peer.packet_limit, 'total_bytes': peer.total_limit}
            import hashlib
            packet['manifest_hash'] = hashlib.sha256(lc.canonical(
                {name: value for name, value in packet.items() if name != 'manifest_hash'})).hexdigest()
            peer.transferred = len(lc.canonical(packet)) + 1
        if peer.execution['model']['execution'].get('provider') not in {'codex', 'claude'}:
            raise dispatch.DispatchError('P_BACKEND', 'The physical invocation requires a native provider')
        peer.packet, peer.context_ref = packet, context_ref
        peer._running_context, peer._journal_seen = context_ref, peer._journal_hint()
        self._runs[key] = peer
        self._refresh(peer)
        return peer

    def _refresh(self, run):
        state = self.store.read()
        details = state.run_details[run.packet['run_id']]
        facts = state._native_packet_facts.get(run.packet['run_id'], {})
        run.handles.update({name: state.validation_assets[identifier]
                           for name, identifier in facts.get('presentation_handles', {}).items()})
        invocation = state.invocations[details['invocation_id']]
        if invocation.get('handle'):
            run._native_handle = invocation['handle']
        return details

    def _budget(self, state, context, assignment, details):
        invocation = state.invocations[details['invocation_id']]
        now = int(time.time() * 1000)
        elapsed = max(0, now - invocation['started_at_ms']) if 'started_at_ms' in invocation else 0
        local = state.local_budget_status(details['local_unit_id'], now)
        remaining = min(invocation['bound_ms'] - elapsed, invocation['deadline_ms'] - now,
                        context['expires_at_ms'] - now, local['remaining_ms'])
        if assignment['deadline_ms'] is not None:
            remaining = min(remaining, assignment['deadline_ms'] - now)
        return {'as_of_ms': now, 'current_elapsed_ms': elapsed, 'remaining_ms': remaining,
                'effective_deadline_ms': now + remaining, 'context_limits': copy.deepcopy(details['limits']),
                'local_budget': local}

    def local_budget_status(self, assignment):
        """Read the existing local iteration and pending physical observations.

        Args:
            assignment: Exact admitted assignment reference or explicit local unit ID.
        Returns:
            Current shared-core local budget status without starting or extending it.
        Raises:
            ProtocolError: The assignment or its local binding is unavailable.
        """
        return self.store.read().local_budget_status(assignment)

    def pause_due(self, scope='default'):
        """Record expired active local windows and expose operator notices.

        Args:
            scope: Existing engagement scope whose due windows are assessed.
        Returns:
            Shared Workflow paused/notices result; no semantic verdict is inferred.
        Raises:
            ProtocolError: Scope, current state or concurrent revision checks fail.
        """
        return self.workflow.pause_due(scope)

    def extend_local_budget(self, unit_id, expected_revision, additional_ms, operator_instruction_ref):
        """Apply an explicit operational extension through the existing controller.

        Args:
            unit_id: Exact paused local unit, never an expired execution grant.
            expected_revision: Observed revision for atomic concurrent-change checks.
            additional_ms: Positive additional local time in milliseconds.
            operator_instruction_ref: CAS digest of the actual operator instruction.
        Returns:
            Ordinary Store response; iteration/rework counts and old grants remain.
        Raises:
            ProtocolError: Missing instruction, wrong revision or nonpaused unit.
        """
        return self.workflow.extend_local_budget(unit_id, expected_revision, additional_ms, operator_instruction_ref)

    def stop_local_budget(self, unit_id, expected_revision, target, reason, operator_instruction_ref):
        """Stop future local/task processing without claiming a remote termination.

        Args:
            unit_id: Exact local unit whose operational stop is requested.
            expected_revision: Current revision for atomic concurrent-change checks.
            target: Existing unit or task operational scope.
            reason: Actual operator reason, not an invented business conclusion.
            operator_instruction_ref: CAS digest of the actual operator instruction.
        Returns:
            Ordinary Store response; physical uncertainty remains independently open.
        Raises:
            ProtocolError: Instruction, scope, revision or current unit is invalid.
        """
        return self.workflow.stop_local_budget(unit_id, expected_revision, target, reason, operator_instruction_ref)

    def _member(self, invocation, member_key, running=True):
        state, physical = self._invocation(invocation)
        if running and physical['state'] != 'running':
            raise dispatch.DispatchError('P_CONTEXT', 'Member requests require the bound running physical invocation')
        matches = [item for item in physical['members'] if item['member_key'] == member_key]
        if len(matches) != 1:
            raise dispatch.DispatchError('P_ORIGIN', 'Member was not issued in this physical invocation')
        run = self._run(matches[0]['context'])
        details = self._refresh(run)
        return run, details

    def _deadline(self, run, details):
        state, context, assignment = run._current(run.context_ref)
        remaining = self._budget(state, context, assignment, details)['remaining_ms']
        if remaining <= 0:
            raise dispatch.DispatchError('P_EXPIRED', 'Physical invocation exhausted its finite allowance')
        return time.monotonic() + remaining / 1000

    def issue_batch(self, jobs, bound_ms=None, invocation_id=None):
        """Atomically issue compatible logical members and one physical reservation.

        Args:
            jobs: Nonempty actual ready assignment/phase/selection/speculation objects.
            bound_ms: Optional positive physical elapsed-time bound within every
                member and root allowance. None uses the existing bounded policy.
            invocation_id: Optional preallocated exact identity for issuance replay.
        Returns:
            Preallocated invocation identity, exact member grants and Store receipt.
        Raises:
            ProtocolError, ValueError: Incompatible controls, disclosure, dependencies,
                authority or finite resource bounds. No provider is invoked.
        """
        return self.workflow.issue_batch(jobs, bound_ms, invocation_id)

    def status(self, invocation):
        """Read one physical invocation and its independently governed member states.

        Args:
            invocation: Exact previously issued physical identity.
        Returns:
            Durable state, native handle, member contexts and pending broker effects.
        Raises:
            ProtocolError: The invocation is unavailable in this engagement.
        """
        state, physical = self._invocation(invocation)
        members = []
        for member in physical['members']:
            context = state.resolve(member['context'], 'context')
            details = state.run_details[context['run_id']]
            members.append({**copy.deepcopy(member), 'state': state.run_states[context['run_id']],
                'pending_requests': [key for key, request in details.get('broker_requests', {}).items()
                                     if request['status'] == 'pending']})
        return {'invocation_id': invocation, 'state': physical['state'],
                'provider': physical['provider'], 'handle': physical.get('handle'), 'members': members}

    def prepare(self, invocation):
        """Durably pin the complete immutable presentation before exposing a call intent.

        Args:
            invocation: Existing physical identity, including a singleton invocation.
        Returns:
            Exact native call intent and member resources; repeated reads restore the
            pinned presentation and never rerender an uncertain historical dispatch.
        Raises:
            ProtocolError, ValueError, OSError: Current preparation or pinned material fails.
        """
        import governed_native_provider
        return governed_native_provider.prepare(self, invocation)

    def start(self, invocation, provider, handle, capture):
        """Bind one actual platform handle to the already prepared physical call.

        Args:
            invocation: Exact prepared physical identity.
            provider: Actual active native provider matching every issued member.
            handle: Actual platform handle observed by the trusted parent.
            capture: Actual provider-tool observation; no worker identity is trusted.
        Returns:
            Existing atomic physical start receipt. No provider is launched here.
        Raises:
            ProtocolError, ValueError: Presentation, origin, current rights or state fails.
        """
        _, physical = self._invocation(invocation)
        if physical['state'] not in {'prepared', 'uncertain'} or provider != physical['provider']:
            raise dispatch.DispatchError('P_ORIGIN', 'Start requires the exact prepared provider invocation')
        manifest = lc.loads(self.store._blob(physical['manifest_blob_id']))
        observed = {'provider_observation': capture, 'host_delivery': {
            'manifest_blob_id': manifest['delivery_manifest_blob_id'], 'prompt_blob_id': manifest['prompt_blob_id']}}
        result = self.workflow.invocation_event(invocation, 'invocation_started', provider=provider,
            handle=handle, capture_blob_id=self.store.put_blob(operator.canonical(observed)),
            observed_at_ms=int(time.time() * 1000))
        for member in physical['members']:
            self._refresh(self._run(member['context']))
        return result

    def request(self, invocation, member_key, request):
        """Relay one member's actual nonterminal request through its original broker.

        Args:
            invocation: Actual bound physical identity.
            member_key: Preissued logical member key, never another member's rights.
            request: Existing closed read/propose/tool/effect frame; terminal results
                use complete. Information/change/escalation requests retain this path.
        Returns:
            Actual broker response with existing durable request replay and effect ACKs.
        Raises:
            ProtocolError, ValueError: Member, current rights, framing or bounds fail.
        """
        run, details = self._member(invocation, member_key)
        wire.validate(request, 'broker-request.schema.json')
        if request['operation'] == 'return':
            raise dispatch.DispatchError('P_SCHEMA', 'Native terminal results require semantic capture completion')
        raw = lc.canonical(request)
        if len(raw) > run.packet_limit:
            raise dispatch.DispatchError('P_BUDGET', 'Member broker frame exceeds its bound')
        if request['id'] not in details.get('broker_requests', {}):
            run.transferred += len(raw) + 1
            if run.transferred > run.total_limit:
                raise dispatch.DispatchError('P_BUDGET', 'Member aggregate transport bound exceeded')
        return {'id': request['id'], 'ok': True,
                'result': run._request(request, run.context_ref, run.packet, self._deadline(run, details))}

    def complete(self, invocation, raw, capture):
        """Retain one actual semantic capture and atomically assess members independently.

        Args:
            invocation: Exact bound physical identity.
            raw: Actual UTF-8 semantic return envelope text or bytes, not encoded wire.
            capture: Actual terminal provider-tool observation and exposed usage facts.
        Returns:
            Physical completion and original receipt on identical replay. Invalid/stale
            members receive no semantic effects; no admitted member is repeated.
        Raises:
            ProtocolError, ValueError, OSError: Changed replay, origin or storage fails.
        """
        import governed_semantic
        import content_spec
        state, physical = self._invocation(invocation)
        raw = raw.encode('utf-8') if isinstance(raw, str) else bytes(raw)
        raw_id = self.store.put_blob(raw)
        capture_id = self.store.put_blob(operator.canonical(capture))
        if physical['state'] in {'returned', 'cancelled'} and physical.get('raw_return_blob_id'):
            if physical['raw_return_blob_id'] != raw_id or physical['capture_blob_id'] != capture_id:
                raise dispatch.DispatchError('P_IDEMPOTENCY', 'Completed invocation cannot receive a different capture')
            previous = next(value for key, value in state.requests.items()
                            if key[2] == 'invocation_finished:' + invocation)
            return {'status': physical['state'], 'completion': {'status': 'already_committed',
                    'receipt': copy.deepcopy(previous['receipt']), 'error': None}}
        if (physical['state'] not in {'running', 'uncertain'}
                and not (physical['state'] == 'cancelled' and 'started_at_ms' in physical)):
            raise dispatch.DispatchError('P_CONTEXT', 'Completion requires the actual bound running call')
        value, unattributable = None, None
        try:
            def reject_constant(value):
                raise ValueError('Nonfinite semantic JSON is not permitted')
            value = json.loads(raw, object_pairs_hook=content_spec._pairs, parse_constant=reject_constant)
            if not wire.validator('semantic-return.schema.json', 'attribution').is_valid(value):
                raise ValueError('An attributable semantic member envelope is required')
            keys = [item['member'] for item in value['results']]
            known = {item['member_key'] for item in physical['members']}
            if len(keys) != len(set(keys)) or not set(keys) <= known:
                raise ValueError('Semantic envelope has duplicate or unissued members')
        except (ValueError, TypeError, UnicodeError) as error:
            unattributable = str(error)
        encoded = []
        for member in physical['members']:
            entry = {'member_key': member['member_key'], 'return_blob_id': None, 'error': None}
            try:
                if unattributable:
                    raise ValueError(unattributable)
                run = self._run(member['context'])
                if len(raw) > run.total_limit:
                    raise dispatch.DispatchError('P_BUDGET', 'Semantic capture exceeds the member transport bound')
                result = governed_semantic.compile_semantic(run.packet, value, self.store.put_blob)
                entry['return_blob_id'] = self.store.put_blob(lc.canonical(result))
            except (ValueError, KeyError, TypeError) as error:
                entry['error'] = {'code': getattr(error, 'code', 'P_SCHEMA'), 'message': str(error)}
            encoded.append(entry)
        result = self.workflow.invocation_event(invocation, 'invocation_finished',
            observed_at_ms=int(time.time() * 1000), capture_blob_id=capture_id,
            raw_return_blob_id=raw_id, encoded_returns=encoded, codec=governed_semantic.CODEC)
        return {'status': self.store.read().invocations[invocation]['state'], 'completion': result}

    def stop(self, invocation, capture):
        """Record one actual physical stop/cancel observation without inventing termination.

        Args:
            invocation: Exact issued, prepared or running physical identity.
            capture: Actual platform observation, or actual host not-dispatched fact.
        Returns:
            Atomic cancellation receipt; existing unresolved effects remain uncertain.
        Raises:
            ProtocolError, ValueError: State, origin or current cancellation guards fail.
        """
        self._invocation(invocation)
        return self.workflow.invocation_event(invocation, 'invocation_cancelled',
            observed_at_ms=int(time.time() * 1000),
            capture_blob_id=self.store.put_blob(operator.canonical(capture)),
            reason='Actual host or platform cancellation observation retained')

def serve(session, source, destination, operations=None):
    """Serve closed parent-only JSON-line commands while retaining one Store.

    Args:
        session: NativeSession owned by the trusted parent controller.
        source: Binary input stream, normally stdin.
        destination: Text output stream, normally stdout.
        operations: Optional trusted additional operation-to-closed-field mapping.
            Extensions cannot replace any shared native operation.
    Returns:
        Zero after a close command or input EOF.
    Raises:
        OSError: Parent transport cannot be read or written.
    """
    fields = {'issue_batch': ('jobs',), 'status': ('invocation',), 'prepare': ('invocation',),
              'start': ('invocation', 'provider', 'handle', 'capture'),
              'request': ('invocation', 'member_key', 'request'),
              'complete': ('invocation', 'raw', 'capture'),
              'stop': ('invocation', 'capture'),
              'local_budget_status': ('assignment',), 'pause_due': ('scope',),
              'extend_local_budget': ('unit_id', 'expected_revision', 'additional_ms', 'operator_instruction_ref'),
              'stop_local_budget': ('unit_id', 'expected_revision', 'target', 'reason', 'operator_instruction_ref'),
              'close': ()}
    optional = {'issue_batch': ('bound_ms', 'invocation_id')}
    if operations:
        if set(operations) & set(fields):
            raise ValueError('Additional host operations cannot replace shared native operations')
        fields.update(operations)
    session.store.read()
    for raw in iter(lambda: source.readline(session.workflow.dispatcher.packet_limit + 1), b''):
        identifier = None
        broken_frame = len(raw) > session.workflow.dispatcher.packet_limit or not raw.endswith(b'\n')
        try:
            if broken_frame:
                raise dispatch.DispatchError('P_BUDGET', 'Parent command exceeds its complete frame bound')
            request = lc.loads(raw)
            if not isinstance(request, dict):
                raise dispatch.DispatchError('P_SCHEMA', 'Parent command must be an object')
            identifier, operation = request.get('id'), request.get('operation')
            required = {'id', 'operation', *fields.get(operation, ())}
            allowed = required | set(optional.get(operation, ()))
            if operation not in fields or not required <= set(request) or not set(request) <= allowed or not isinstance(identifier, str):
                raise dispatch.DispatchError('P_SCHEMA', 'Closed parent host command required')
            if operation == 'close':
                print(json.dumps({'id': identifier, 'ok': True, 'result': {'closed': True}}), file=destination, flush=True)
                return 0
            result = getattr(session, operation)(**{name: request[name] for name in
                (*fields[operation], *optional.get(operation, ())) if name in request})
            response = {'id': identifier, 'ok': True, 'result': result}
        except (dispatch.DispatchError, lc.ERROR, ValueError, OSError, KeyError, TypeError) as error:
            response = {'id': identifier, 'ok': False,
                        'error': {'code': getattr(error, 'code', 'P_CONTEXT'), 'message': str(error)}}
        print(json.dumps(response, ensure_ascii=False), file=destination, flush=True)
        if broken_frame:
            return 1
    return 0


def main(argv=None):
    """Open the foreground host session; this never launches a provider.

    Args:
        argv: Explicit host arguments, otherwise process arguments.
    Returns:
        Zero on clean parent transport completion.
    Raises:
        ValueError, OSError: Configuration or initial engagement history is invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True)
    parser.add_argument('--engagement', required=True)
    parser.add_argument('--config')
    parser.add_argument('--task')
    parser.add_argument('--criteria')
    parser.add_argument('--provider', choices=('codex', 'claude'))
    parser.add_argument('--work-item')
    parser.add_argument('--deadline-ms', type=int)
    parser.add_argument('--limit-ms', type=int)
    parser.add_argument('--iteration-ms', type=int)
    parser.add_argument('--max-reworks', type=int)
    parser.add_argument('--model-config')
    args = parser.parse_args(argv)
    store = lc.Store(args.store, args.engagement)
    startup = (args.task, args.criteria, args.provider, args.work_item)
    if args.config:
        if any(value is not None for value in (*startup, args.deadline_ms, args.limit_ms,
                args.iteration_ms, args.max_reworks, args.model_config)):
            parser.error('Use either an existing --config or explicit new-engagement inputs')
        session = NativeSession(store, lc.loads(operator.regular(args.config)))
    else:
        if any(value is None for value in startup):
            parser.error('New startup needs --task --criteria --provider --work-item')
        import governed_native_provider
        limits = [] if args.limit_ms is None else [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': args.limit_ms}]
        initialized = governed_native_provider.bootstrap(store, operator.regular(args.task),
            operator.regular(args.criteria), args.provider, args.work_item, limits,
            args.deadline_ms, args.model_config, local_budget={
                'iteration_ms': 600000 if args.iteration_ms is None else args.iteration_ms,
                'max_reworks': 3 if args.max_reworks is None else args.max_reworks})
        session = NativeSession(store, initialized['config'])
        entry = session.workflow.entry('default', args.work_item, limits, args.deadline_ms)
        issued = session.issue_batch([{'assignment': entry['assignment'], 'phase': 'selection'}])
        print(json.dumps({'id': 'startup', 'ok': True, 'result': {
            **initialized, 'entry': entry, 'issued': issued,
            'prepared': session.prepare(issued['invocation_id'])}}, ensure_ascii=False), flush=True)
    return serve(session, sys.stdin.buffer, sys.stdout)


if __name__ == '__main__':
    raise SystemExit(main())
