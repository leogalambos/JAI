#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Host-only json-process dispatcher; the existing Store owns all decisions.

The closed host configuration uses protocol ``jai.host-dispatch/1``, workers,
destinations, tools and limits. A worker has provider ``json-process/1``, argv
and files [{path,name,sha256}]. Destination entries are {handle,owner,root}; tool
entries are {policy,worker}. Limits are packet_bytes and total_bytes.

Workers exchange newline-delimited ``jai.process/1`` JSON with the host. The
initial input contains run_id, assignment/context references, exact manifest
records, attachment handles and manifest_hash. Requests have id and operation:
read(handle), propose(data:base64), materialize(subject,blob_id,destination_handle),
measure(tool_policy,targets), or return(value:RunReturn). Responses contain id,
ok and result, or error {code,message}. No request accepts an executable or host
path. A measurement executable receives the same bounded input packet and emits
bounded raw stdout, not another semantic protocol.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import copy
import ctypes
import ctypes.util
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import shutil
import subprocess
import tempfile
import time
import uuid

import governed_delivery as wire
import lifecycle as lc
import operator_actions as operator

HOST_PROTOCOL = 'jai.host-dispatch/1'
PROCESS_PROTOCOL = 'jai.process/1'
_RUNTIME = (Path('/usr'), Path('/lib'), Path('/lib64'))


class DispatchError(ValueError):
    """Expose a bounded diagnostic without treating execution as acceptance."""

    def __init__(self, code, message):
        """Retain public-safe protocol code and diagnostic text."""
        super().__init__(message)
        self.code = code


def _closed(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise DispatchError('P_SCHEMA', 'Closed dispatcher shape required')
    return value


def _integer(value, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise DispatchError('P_BUDGET', 'Bounded positive dispatcher limit required')
    return value


def _bytes(value):
    if not isinstance(value, str):
        raise DispatchError('P_SCHEMA', 'Base64 byte string required')
    try:
        return base64.b64decode(value, validate=True)
    except ValueError as error:
        raise DispatchError('P_SCHEMA', 'Canonical base64 bytes required') from error


def _seccomp(path):
    name = ctypes.util.find_library('seccomp')
    if not name:
        raise DispatchError('P_BACKEND', 'Native libseccomp is unavailable')
    library = ctypes.CDLL(name, use_errno=True)
    library.seccomp_init.argtypes = [ctypes.c_uint32]
    library.seccomp_init.restype = ctypes.c_void_p
    library.seccomp_release.argtypes = [ctypes.c_void_p]
    library.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    library.seccomp_syscall_resolve_name.restype = ctypes.c_int
    library.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    library.seccomp_export_bpf.argtypes = [ctypes.c_void_p, ctypes.c_int]
    context = library.seccomp_init(0x7fff0000)  # Native architecture only; bad ABI defaults to kill.
    if not context:
        raise DispatchError('P_BACKEND', 'Native seccomp initialization failed')
    try:
        for syscall in ('socket', 'socketpair', 'io_uring_setup', 'io_uring_enter', 'io_uring_register'):
            number = library.seccomp_syscall_resolve_name(syscall.encode())
            if number < 0 or library.seccomp_rule_add(context, 0x50000 | 1, number, 0) != 0:
                raise DispatchError('P_BACKEND', 'Native socket isolation is unsupported')
        with open(path, 'xb') as stream:
            if library.seccomp_export_bpf(context, stream.fileno()) != 0:
                raise DispatchError('P_BACKEND', 'Native seccomp export failed')
    finally:
        library.seccomp_release(context)


def _terminate(process):
    if process.poll() is None:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
    with contextlib.suppress(subprocess.TimeoutExpired):
        process.wait(timeout=2)


class Dispatcher:
    """Execute one issued assignment inside an isolated host-enrolled process."""

    def __init__(self, store, config):
        """Bind the local Store and closed execution configuration.

        Args:
            store: Existing lifecycle.Store; no caller-selected producer is used.
            config: Host configuration described in the module protocol contract.
        Raises:
            DispatchError: Configuration, provider or sensitive path is unsupported.
            OSError: Host configuration assets cannot be read.
        """
        self.store = store
        self.config = copy.deepcopy(config)
        self._running_context = None
        self._journal_seen = None
        _closed(config, ('protocol', 'workers', 'destinations', 'tools', 'limits'))
        if config['protocol'] != HOST_PROTOCOL:
            raise DispatchError('P_SCHEMA', 'Unsupported dispatcher configuration')
        _closed(config['limits'], ('packet_bytes', 'total_bytes'))
        self.packet_limit = _integer(config['limits']['packet_bytes'], 256, 8 * 1024 * 1024)
        self.total_limit = _integer(config['limits']['total_bytes'], self.packet_limit, 32 * 1024 * 1024)
        self.sensitive = [store.path.resolve(), store.material.resolve(), Path(__file__).resolve(),
                          Path(lc.__file__).resolve(), Path(operator.__file__).resolve()]
        self.sensitive.extend(operator.trust_path(purpose).resolve() for purpose in
                              ('delivery-change', 'delivery-accept', 'delivery-release'))
        for runtime in _RUNTIME:
            if runtime.exists():
                actual = runtime.resolve()
                if any(path == actual or path.is_relative_to(actual) for path in self.sensitive):
                    raise DispatchError('P_SCOPE', 'Public runtime overlaps a private host capability')
        if not isinstance(config['workers'], list):
            raise DispatchError('P_SCHEMA', 'Explicit process implementation list required')
        for worker in config['workers']:
            self._worker(worker)
        if not isinstance(config['destinations'], list) or not isinstance(config['tools'], list):
            raise DispatchError('P_SCHEMA', 'Explicit destination and tool lists required')
        handles = set()
        for destination in config['destinations']:
            _closed(destination, ('handle', 'owner', 'root'))
            if not isinstance(destination['handle'], str) or not destination['handle'] or destination['handle'] in handles:
                raise DispatchError('P_SCOPE', 'Unique enrolled destination handle required')
            handles.add(destination['handle'])
            root = Path(destination['root'])
            if not root.is_absolute() or root.is_symlink() or not root.is_dir():
                raise DispatchError('P_SCOPE', 'Existing real destination root required')
            if any(root.resolve() == path or root.resolve().is_relative_to(path) or path.is_relative_to(root.resolve())
                   for path in self.sensitive):
                raise DispatchError('P_SCOPE', 'Destination overlaps a private host capability')
        policies = []
        for tool in config['tools']:
            _closed(tool, ('policy', 'worker'))
            if tool['policy'] in policies:
                raise DispatchError('P_SCOPE', 'Unique exact measurement policy required')
            policies.append(tool['policy'])
            self._worker(tool['worker'])

    def _worker(self, worker):
        _closed(worker, ('provider', 'argv', 'files'))
        if worker['provider'] != 'json-process/1':
            raise DispatchError('P_BACKEND', 'Only json-process/1 is implemented')
        if (not isinstance(worker['argv'], list) or not worker['argv']
                or any(not isinstance(arg, str) or '\x00' in arg for arg in worker['argv'])
                or not worker['argv'][0].startswith('/') or not isinstance(worker['files'], list)):
            raise DispatchError('P_SCHEMA', 'Explicit worker executable and enrolled assets required')
        names = set()
        for asset in worker['files']:
            _closed(asset, ('path', 'name', 'sha256'))
            name = asset['name']
            if not isinstance(name, str) or name in {'', '.', '..'} or '/' in name or '\\' in name or name in names:
                raise DispatchError('P_SCOPE', 'Unique flat worker asset name required')
            names.add(name)
            path = Path(asset['path']).resolve(strict=True)
            if any(path == secret or path.is_relative_to(secret) for secret in self.sensitive):
                raise DispatchError('P_SCOPE', 'Worker asset overlaps a private host capability')
            if hashlib.sha256(operator.regular(asset['path'])).hexdigest() != asset['sha256']:
                raise DispatchError('P_INTEGRITY', 'Enrolled worker bytes changed')

    def _controller(self, state, scope):
        candidates = [(state._reference(identifier), value['content']['record'])
                      for identifier, value in state.versions.items() if value['kind'] == 'delivery.context'
                      and value['content']['scope'] == scope and value['content']['record']['assignment'] is None]
        if not candidates:
            raise DispatchError('P_CONTEXT', 'Engagement has no exact controller audit context')
        reference, context = candidates[0]
        return {'kind': 'controller', 'id': context['issued_to']}, reference

    def _control(self, context_ref, event, total=0, result_blob=None, observed=None, audit=None, observation=None, request_id=None):
        state = self.store.read()
        context = state.resolve(context_ref, 'context')
        controller, controller_context = self._controller(state, context_ref['scope'])
        now = int(time.time() * 1000)
        profile = state.resolve(context['profile'], 'profile')
        message = {'protocol': wire.PROTOCOL, 'message_type': 'control_event', 'message_id': '0' * 64,
                   'request_id': request_id or str(uuid.uuid4()), 'correlation_id': context['run_id'],
                   'engagement': self.store.engagement, 'scope': context_ref['scope'],
                   'sender': controller, 'recipient': controller, 'context': controller_context,
                   'profile': context['profile'], 'expected_head': state.head, 'issued_at_ms': now,
                   'expires_at_ms': now + profile['max_request_duration_ms'], 'causes': [], 'attachments': [],
                   'payload': {'event': event, 'run_context': context_ref, 'run_id': context['run_id'],
                               'observed_at_ms': now if observed is None else observed,
                               'return_blob_id': result_blob,
                               'usage': [{'metric': 'elapsed_ms', 'unit': 'ms', 'total': total}]}}
        if audit is not None:
            message['attachments'] = [{'blob_id': audit[0], 'byte_length': audit[1], 'media_type': 'application/json',
                                       'classification': 'internal', 'access_handle': 'dispatch-audit'}]
        if getattr(self, '_native_handle', None) is not None and event != 'run_started':
            message['payload']['native_handle'] = self._native_handle
        if observation is not None:
            if set(observation) & set(message['payload']):
                raise DispatchError('P_SCOPE', 'Host observation cannot replace its exact run binding')
            message['payload'].update(observation)
        if event in {'run_started', 'broker_requested', 'broker_observed'}:
            message['payload'].pop('usage')
            message['payload'].pop('return_blob_id')
        elif event == 'run_cancelled':
            message['payload'].pop('return_blob_id')
            message['payload']['reason'] = 'Host execution ended without an admissible captured return'
        message['message_id'] = wire.message_id(message)
        return self._submit(message)

    def _submit(self, message, authority_proof=None):
        # The local runtime records its actual control flow; only an explicit
        # L0 decision carries an external signature.
        response = self.store.submit(lc.canonical(message), authority_proof=authority_proof)
        if response['status'] not in {'committed', 'already_committed'}:
            error = response['error']
            raise DispatchError(error['code'], 'Host operation was rejected: ' + error['message'])
        return response

    def _current(self, context_ref, issued=False):
        state = self.store.read()
        context = state.resolve(context_ref, 'context')
        if context['assignment'] is None:
            raise DispatchError('P_SCOPE', 'Only an issued leaf context can execute')
        assignment = state.resolve(context['assignment'], 'assignment')
        if state.run_states.get(context['run_id']) != ('issued' if issued else 'running'):
            raise DispatchError('P_CONTEXT', 'Execution context is not current and runnable')
        previous = state.scope
        state.scope = context_ref['scope']
        try:
            # A journal head is a concurrency boundary, not a run's permission.
            # The Store assesses this exact context against any relevant changes.
            state.execution_eligible(context_ref, live=True)
        finally:
            state.scope = previous
        limits = state.run_details[context['run_id']]['limits']
        if not limits or any(item['metric'] != 'elapsed_ms' or item['unit'] != 'ms' for item in limits):
            raise DispatchError('P_BUDGET', 'This route measures only elapsed_ms in ms')
        return state, context, assignment

    def _journal_hint(self):
        info = self.store.path.stat(follow_symlinks=False)
        return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns

    def _watch_run(self):
        if self._running_context is None:
            return
        observed = self._journal_hint()
        if observed != self._journal_seen:
            self._current(self._running_context)
            # Retain the pre-check hint: a concurrent later write is checked on
            # the next observation rather than stamped as already assessed.
            self._journal_seen = observed

    def _assemble(self, state, context_ref, context, assignment):
        execution = state.context_execution(context, live=True)
        policy_ref = execution['policy_use']['ref']
        references = [(context_ref, context_ref['scope']), (context['assignment'], assignment['use_scope'])]
        references.extend((ref, state._assignment_use(assignment, path, ref)['use_scope'])
                          for path, ref in lc._reference_paths(assignment)
                          if path in {'/profile', '/criteria', '/procedure_task/procedure'} or path.startswith(('/inputs/', '/inherited/')))
        references.extend((effect['tool_policy'], assignment['use_scope']) for effect in context['effects'] if effect['tool_policy'] is not None)
        readable = [ref for effect in context['effects'] if effect['operation'] == 'read' for ref in effect['targets']]
        manifest, attachments, handles = [], [], {}
        for reference, use_scope in references:
            if any(item['ref'] == reference and item['use_scope'] == use_scope for item in manifest):
                continue
            record = state.resolve(reference)
            handle = 'record:' + use_scope + ':' + reference['version_id']
            manifest.append({'handle': handle, 'ref': reference, 'use_scope': use_scope, 'record': copy.deepcopy(record)})
            handles[handle] = lc.canonical(record)
            for identifier in record.get('material', []):
                try:
                    raw = self.store._blob(identifier)
                except OSError as error:
                    raise DispatchError('P_CONTEXT', 'Required exact material is unavailable') from error
                if reference not in readable or reference == policy_ref:
                    continue
                handle = 'blob:' + identifier
                if handle not in handles:
                    handles[handle] = raw
                    attachments.append({'handle': handle, 'blob_id': identifier, 'size': len(raw)})
        for attachment in context['attachments']:
            if attachment['blob_id'] not in {item['blob_id'] for item in attachments}:
                raise DispatchError('P_SCOPE', 'Attachment is not exact material from an authorized readable input')
            try:
                raw = self.store._blob(attachment['blob_id'])
            except OSError as error:
                raise DispatchError('P_CONTEXT', 'Required exact material is unavailable') from error
            if len(raw) != attachment['byte_length']:
                raise DispatchError('P_INTEGRITY', 'Declared attachment length differs from exact bytes')
            handle = attachment['access_handle']
            if handle in handles and handles[handle] != raw:
                raise DispatchError('P_CONFLICT', 'Attachment handle is ambiguous')
            handles[handle] = raw
            attachments.append({'handle': handle, 'blob_id': attachment['blob_id'], 'size': len(raw)})
        packet = {'protocol': PROCESS_PROTOCOL, 'operation': 'input', 'run_id': context['run_id'],
                  'assignment': context['assignment'], 'context': context_ref,
                  'manifest': manifest, 'attachments': attachments,
                  'ready_basis': copy.deepcopy(context['ready_basis'])}
        snapshot = execution['snapshot']
        self.intrinsic_handles = {'catalogue': snapshot['descriptor']['catalogue_blob_id']}
        self.intrinsic_handles.update({'instruction:' + slug: identifier
                                      for slug, identifier in snapshot['descriptor']['instruction_blobs'].items()})
        packet['catalogue'] = {'handle': 'catalogue', 'blob_id': snapshot['descriptor']['catalogue_blob_id'],
                               'instruction_prefix': 'instruction:'}
        packet['execution'] = {'phase': execution['phase'], 'policy_use': execution['policy_use'],
                               'model_selector': execution['model_selector'],
                               'specialties': execution.get('specialties', []),
                               'instructions': execution['instructions']}
        if execution['phase'] == 'selection':
            packet['execution']['previous'] = copy.deepcopy(state.execution_plans.get((context['assignment']['version_id'], assignment['use_scope'])))
            packet['execution']['availability'] = [
                {'provider': provider, 'workload_class': workload, 'model_selector': model['model_selector'],
                 'supported': provider in {'json-process/1', 'codex', 'claude'}}
                for provider, details in snapshot['models']['providers'].items()
                for workload, model in details['classes'].items()]
        else:
            packet['execution']['selection'] = execution['selection']
        feedback = state.assignment_feedback(assignment, live=True)
        if feedback:
            packet['historical_feedback'] = feedback
        if execution['phase'] == 'work' and assignment['responsibility'] in {'reviewer', 'integration_reviewer', 'receiver'}:
            slot = 'incoming_handoff' if assignment['responsibility'] == 'receiver' else 'assessed-subject'
            subjects = [ref for binding in assignment['inputs'] if binding['slot_id'] == slot for ref in binding['refs']]
            if len(subjects) != 1:
                raise DispatchError('P_CONTEXT', 'A review requires its one exact assigned subject')
            closure = state.assessment_closure(subjects[0], context['assignment'])
            packet['assessment_basis'] = {'subject': subjects[0], 'closure': closure,
                                          'hash': hashlib.sha256(lc.canonical(closure)).hexdigest()}
        if execution['phase'] == 'work' and assignment['responsibility'] == 'setter':
            packet['current_procedure'] = copy.deepcopy(state.procedures.get((context['assignment']['version_id'], assignment['use_scope'])))
            packet['owned_returns'] = self._owned_returns(state, context['assignment'], assignment, context['ready_basis'])
            packet['current_slots'] = self._current_slots(state, context['assignment'], assignment,
                                                           packet['owned_returns'], context['ready_basis'])
        if assignment.get('handling') is not None:
            packet['handling'] = self._handling_facts(state, assignment['handling'])
        packet['manifest_hash'] = hashlib.sha256(lc.canonical(packet)).hexdigest()
        if len(lc.canonical(packet)) > self.packet_limit or sum(map(len, handles.values())) > self.total_limit:
            raise DispatchError('P_BUDGET', 'Declared inputs exceed the bounded process transport')
        return packet, handles

    def _historical_record(self, state, reference):
        body = copy.deepcopy(state.resolve(reference))
        material = []
        for identifier in body.get('material', []):
            if body.get('source_role') == 'policy':
                material.append({'blob_id': identifier, 'status': 'control_only'})
                continue
            try:
                raw = self.store._blob(identifier)
            except OSError:
                material.append({'blob_id': identifier, 'status': 'unavailable'})
            except lc.ERROR as error:
                if error.code != 'P_INTEGRITY':
                    raise
                material.append({'blob_id': identifier, 'status': 'integrity_failure'})
            except ValueError:
                material.append({'blob_id': identifier, 'status': 'integrity_failure'})
            else:
                material.append({'blob_id': identifier, 'status': 'available',
                                 'data': base64.b64encode(raw).decode('ascii')})
        return {'ref': reference, 'record': body, 'historical': True, 'material': material}

    def _handling_facts(self, state, handling):
        package = state.resolve(handling['package'], 'product')
        facts = {'episode': handling['episode'], 'task': handling['task'],
                 'package': self._historical_record(state, handling['package']),
                 'conflicts': [], 'inputs': []}
        seen = set()
        conflicts = next((item['refs'] for item in package['related'] if item['slot_id'] == 'conflicts'), [])
        inputs = list(lc._references(package.get('inputs', [])))
        for reference in conflicts:
            if reference['version_id'] not in seen:
                seen.add(reference['version_id'])
                facts['conflicts'].append(self._historical_record(state, reference))
                body = state.resolve(reference)
                inputs.extend(lc._references(body.get('inputs', [])))
                inputs.extend(body.get('evidence', []))
        for reference in inputs:
            if reference['version_id'] not in seen:
                seen.add(reference['version_id'])
                facts['inputs'].append(self._historical_record(state, reference))
        return facts

    def _ready_record(self, state, reference, scope, basis):
        status = state._status(reference, scope)['validity']
        point = state._point(reference, scope)
        token = 'record:' + reference['version_id'] + ':' + status + (':held' if state._held(point) else '')
        return token in basis

    def _intent_key(self, context, intent):
        return lc._hash({'context': context['version_id'], 'message_type': intent['message_type'],
                         'payload': intent['payload']})

    def _ready_returned_intent(self, state, reference, assignment, child, intent, basis):
        """Project a committed terminal return through its delivered subject fact.

        Recordless publication can change an existing subject's applicability;
        it need not create another record or a separately stored message.
        """
        subjects = {'submission': 'candidate', 'observation': 'observation',
                    'review': 'assessment', 'integration': 'bundle',
                    'handoff': 'handoff', 'handoff_acceptance': 'assessment'}
        field = subjects.get(intent['message_type'])
        if field is None:
            return False
        subject = intent['payload'][field]
        scope = child['use_scope']
        if (not state._produced_under(subject, reference, assignment['owner'])
                or not self._ready_record(state, subject, scope, basis)):
            return False
        if intent['message_type'] == 'integration':
            body = state.resolve(subject, 'product')
            return (body['product_kind'] == 'bundle'
                    and state._status(subject, scope)['validity'] == 'valid'
                    and not state._held(state._point(subject, scope)))
        return True

    def _published_record(self, state, reference):
        body = copy.deepcopy(state.resolve(reference))
        material = [{'blob_id': identifier, 'data': base64.b64encode(self.store._blob(identifier)).decode('ascii')}
                    for identifier in body.get('material', [])]
        return {'ref': reference, 'record': body, 'material': material}

    def _current_slots(self, state, reference, assignment, returns, basis):
        scope = assignment['use_scope']
        profile = state.resolve(assignment['profile'], 'profile')
        records = {item['ref']['version_id']: item for returned in returns for item in returned['records']}
        for identifier, value in state.versions.items():
            if (value['kind'] == 'delivery.product'
                    and state.provenance[identifier]['origin'] == {'kind': 'assignment', 'ref': reference}):
                records[identifier] = {'ref': state._reference(identifier), 'record': value['content']['record']}
        requested = {}
        for key, selected in state.selections.items():
            if key[0] != scope:
                continue
            slot = json.loads(key[1])
            if slot['owner'] == assignment['owner'] or state._produced_under(selected, reference, assignment['owner']):
                requested[key] = slot
        for key, selected in state.proofs.items():
            if key[0] != scope:
                continue
            subject = selected['subject']
            if (state.resolve(subject)['owner'] == assignment['owner']
                    or state._produced_under(subject, reference, assignment['owner'])):
                requested[key] = json.loads(key[1])
        for obligation in profile['obligations']:
            if obligation['role'] == 'answer' and obligation['owner'] == assignment['owner']:
                slot = {'kind': 'basis', 'owner': assignment['owner'], 'slot_id': obligation['slot_id']}
                requested[lc._proof_key(scope, slot)] = slot
            if obligation['role'] not in {'professional_review', 'integration_review', 'receiving_acceptance'}:
                continue
            for item in records.values():
                body = item['record']
                if body.get('product_kind') != obligation['subject_kind'] or body['owner'] != obligation['owner']:
                    continue
                slot = {'kind': 'proof', 'subject': item['ref'], 'role': obligation['role'], 'slot_id': obligation['slot_id']}
                requested[lc._proof_key(scope, slot)] = slot
        facts = []
        for key, slot in sorted(requested.items()):
            category = 'basis' if slot['kind'] == 'basis' else 'proof'
            selected = (state.selections if category == 'basis' else state.proofs).get(key)
            chosen = selected if category == 'basis' else (selected['proof'] if selected else None)
            chosen_scope = scope if chosen is not None and category == 'basis' else (selected['proof_use_scope'] if selected else None)
            event = state._selection_for(category, scope, slot, chosen) if chosen is not None else None
            own = (slot.get('owner') == assignment['owner'] if category == 'basis'
                   else state.resolve(slot['subject']).get('owner') == assignment['owner'])
            if chosen is not None and not own:
                if (not self._ready_record(state, chosen, chosen_scope, basis) or event is None
                        or 'transition:' + event['decision_ref']['version_id'] not in basis):
                    continue
            established = [state._point(event['decision_ref'], event['scope'])] if event else []
            applicable = False
            if chosen is not None and event is not None:
                applicable = (state._governing_input(state._point(chosen, chosen_scope), live=True)
                              and state._governing_input(state._point(event['decision_ref'],
                                  event.get('decision_scope', event['scope'])), live=True))
            facts.append({'slot': slot, 'use_scope': scope, 'selected_ref': chosen,
                          'selection_use_scope': chosen_scope, 'applicable': applicable,
                          'established_by': established})
        return facts

    def _owned_returns(self, state, reference, assignment, basis):
        results = []
        delivered_intents = set()
        for message in state.messages.values():
            if message['context'] is None:
                continue
            allowed = 'intent:' + message['message_id'] in basis
            if not allowed and message['message_type'] == 'decision':
                allowed = 'transition:' + state._decision_ref(message)['version_id'] in basis
            if allowed:
                delivered_intents.add(self._intent_key(message['context'], message))
        for transaction in state.transactions:
            message = transaction['operations'][0]['data']['message']
            payload = message['payload']
            if (message['message_type'] != 'control_event'
                    or payload.get('event') not in {'run_completed', 'invocation_finished'}):
                continue
            for captured in (transaction['return_artifact'] or {}).values():
                value = lc.loads(captured)
                context = state.resolve(value['context'], 'context')
                if context['assignment'] is None or context['execution']['phase'] != 'work':
                    continue
                child = state.resolve(context['assignment'], 'assignment')
                if (child['issued_under'] != reference or child['owner']['work_item'] != assignment['owner']['work_item']
                        or state.run_states.get(context['run_id']) != 'returned'):
                    continue
                distance = child['owner']['layer'] - assignment['owner']['layer']
                records = []
                intents = []
                for intent in value['intents']:
                    if distance and intent['message_type'] not in {'handoff', 'handoff_acceptance', 'information_request', 'information_response', 'change_request'}:
                        continue
                    if child['responsibility'] == 'setter' and intent['message_type'] == 'assignment':
                        continue
                    if child['responsibility'] == 'setter' and intent['message_type'] == 'decision':
                        choice = intent['payload']
                        if choice['action'] != 'select' or not state._produced_under(choice['candidate'], reference, assignment['owner']):
                            continue
                    if (self._intent_key(value['context'], intent) in delivered_intents
                            or self._ready_returned_intent(state, reference, assignment, child, intent, basis)):
                        intents.append(copy.deepcopy(intent))
                if not distance and child['responsibility'] == 'setter':
                    published = [intent['payload']['candidate'] for intent in intents
                                 if intent['message_type'] == 'decision' and intent['payload']['action'] == 'select'
                                 and intent['payload']['slot']['kind'] == 'basis'
                                 and state.selections.get(lc._proof_key(child['use_scope'], intent['payload']['slot'])) == intent['payload']['candidate']]
                    for candidate in published:
                        if state._produced_under(candidate, reference, assignment['owner']):
                            if not self._ready_record(state, candidate, child['use_scope'], basis):
                                continue
                            records.append(self._published_record(state, candidate))
                            for key, selected in state.proofs.items():
                                proof = selected['proof']
                                if (key[0] == child['use_scope'] and selected['subject'] == candidate
                                        and state._produced_under(proof, reference, assignment['owner'])
                                        and self._ready_record(state, proof, child['use_scope'], basis)):
                                    records.append(self._published_record(state, proof))
                else:
                    for proposal in value['records']:
                        body = proposal['record']
                        if distance and not ((proposal['record_type'] == 'assessment' and body['assessment_kind'] == 'receiving')
                                             or (proposal['record_type'] == 'product' and body['product_kind'] == 'handoff')):
                            continue
                        manifest = lc.record_manifest(state.engagement, message['scope'], proposal['logical_id'], proposal['record_type'], body)
                        candidate = state._reference(lc.version_id(manifest))
                        if (state._produced_under(candidate, reference, assignment['owner'])
                                and self._ready_record(state, candidate, child['use_scope'], basis)):
                            records.append(self._published_record(state, candidate))
                if records or intents:
                    published = {'assignment': context['assignment'], 'run_id': context['run_id'],
                                 'state': state.assignment_states.get(context['assignment']['version_id']),
                                 'head': state.head, 'committed_at': transaction['hash'],
                                 'records': records, 'intents': intents}
                    if distance == 0:
                        published['mandate'] = copy.deepcopy(child)
                    results.append(published)
        return results

    def _launch(self, worker, folder, packet):
        self._worker(worker)
        backend = shutil.which('bwrap')
        if backend is None:
            raise DispatchError('P_BACKEND', 'Host bwrap executable is unavailable on the inherited PATH')
        backend = os.path.abspath(backend)
        assets = folder / 'worker'
        assets.mkdir()
        scratch = folder / 'scratch'
        scratch.mkdir()
        for asset in worker['files']:
            raw = operator.regular(asset['path'])
            if hashlib.sha256(raw).hexdigest() != asset['sha256']:
                raise DispatchError('P_INTEGRITY', 'Worker asset changed before launch')
            (assets / asset['name']).write_bytes(raw)
            (assets / asset['name']).chmod(0o555)
        input_path = folder / 'input.json'
        input_path.write_bytes(lc.canonical(packet) + b'\n')
        catalogue = folder / 'catalogue'
        (catalogue / 'instructions').mkdir(parents=True)
        snapshot = self.execution['snapshot']
        (catalogue / 'catalogue.json').write_bytes(self.store._blob(snapshot['descriptor']['catalogue_blob_id']))
        for slug, instruction in snapshot['instructions'].items():
            (catalogue / 'instructions' / (slug + '.md')).write_bytes(self.store._blob(instruction['blob_id']))
        filter_path = folder / 'filter.bpf'
        _seccomp(filter_path)
        command = [backend, '--die-with-parent', '--new-session', '--unshare-user', '--unshare-pid',
                   '--unshare-ipc', '--unshare-uts', '--cap-drop', 'ALL', '--clearenv',
                   '--setenv', 'PATH', '/usr/bin:/bin', '--setenv', 'HOME', '/nonexistent', '--tmpfs', '/tmp']
        for runtime in _RUNTIME:
            if runtime.exists():
                command += ['--ro-bind', str(runtime), str(runtime)]
        command += ['--symlink', 'usr/bin', '/bin', '--symlink', 'usr/sbin', '/sbin',
                    '--proc', '/proc', '--dev', '/dev', '--ro-bind', str(assets), '/worker',
                    '--ro-bind', str(catalogue), '/catalogue',
                    '--ro-bind', str(input_path), '/input.json', '--bind', str(scratch), '/scratch', '--chdir', '/scratch']
        with filter_path.open('rb') as stream:
            command += ['--seccomp', str(stream.fileno()), '--', *worker['argv']]
            try:
                return subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        pass_fds=(stream.fileno(),), close_fds=True, start_new_session=True,
                                        env={'PATH': '/usr/bin:/bin'})
            except OSError as error:
                raise DispatchError('P_BACKEND', 'Confined json-process backend is unavailable') from error

    def _grant(self, context, assignment, request):
        operation = request['operation']
        if operation in {'return', 'reference'}:
            return
        if operation not in self.execution['allowed_operations']:
            raise DispatchError('P_SCOPE', 'Execution phase or selected professional cannot perform this broker effect')
        grants = [grant for grant in context['effects'] if grant['operation'] == operation and grant['owner'] == assignment['owner']]
        if operation == 'read':
            if (request['handle'] not in self.handles and request['handle'] not in self.intrinsic_handles
                    and request['handle'] not in getattr(self, 'delivered_handles', {})):
                raise DispatchError('P_SCOPE', 'Read handle is outside the exact input manifest')
            return
        if operation == 'propose' and grants:
            return
        if operation == 'materialize':
            matches = [grant for grant in grants if grant['destination_handle'] == request['destination_handle']
                       and request['subject'] in grant['targets']]
        elif operation == 'measure':
            matches = [grant for grant in grants if grant['tool_policy'] == request['tool_policy']
                       and request['targets'] and all(target in grant['targets'] for target in request['targets'])]
        else:
            matches = []
        if not matches:
            raise DispatchError('P_SCOPE', 'Operation differs from the exact assigned effect grant')

    def _materialize(self, assignment, request):
        identifier = request['blob_id']
        if identifier not in self.allowed_blobs:
            raise DispatchError('P_SCOPE', 'Materialization bytes were not delivered or captured from this run')
        destination = next((item for item in self.config['destinations'] if item['handle'] == request['destination_handle']
                            and item['owner'] == assignment['owner']), None)
        if destination is None:
            raise DispatchError('P_SCOPE', 'Destination does not belong to this exact assignment owner')
        raw = self.store._blob(identifier)
        root = Path(destination['root'])
        fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            try:
                output = os.open(identifier, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
            except FileExistsError:
                existing = os.open(identifier, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
                with os.fdopen(existing, 'rb') as stream:
                    if stream.read(self.total_limit + 1) != raw:
                        raise DispatchError('P_INTEGRITY', 'Existing artifact conflicts with immutable captured bytes')
            else:
                with os.fdopen(output, 'wb') as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.fsync(fd)
        finally:
            os.close(fd)
        return {'blob_id': identifier}

    def _measure(self, request, packet, deadline):
        tool = next((tool for tool in self.config['tools'] if tool['policy'] == request['tool_policy']), None)
        if tool is None:
            raise DispatchError('P_SCOPE', 'Exact tool-policy version is not enrolled')
        refs = request['targets'] + [request['tool_policy']]
        reduced = copy.deepcopy(packet)
        reduced['manifest'] = [item for item in packet['manifest'] if item['ref'] in refs]
        ids = {identifier for item in reduced['manifest'] for identifier in item['record'].get('material', [])}
        reduced['attachments'] = [item for item in packet['attachments'] if item['blob_id'] in ids]
        for attachment in reduced['attachments']:
            attachment['data'] = base64.b64encode(self.store._blob(attachment['blob_id'])).decode()
        reduced['manifest_hash'] = hashlib.sha256(lc.canonical({key: value for key, value in reduced.items() if key != 'manifest_hash'})).hexdigest()
        with tempfile.TemporaryDirectory(prefix='jai-measure-') as directory:
            process = self._launch(tool['worker'], Path(directory), reduced)
            try:
                output = self._communicate(process, lc.canonical(reduced) + b'\n', deadline)
                identifier = self.store.put_blob(output)
                self.allowed_blobs.add(identifier)
                return {'blob_id': identifier, 'status': process.returncode}
            finally:
                _terminate(process)

    def _write(self, process, raw, deadline):
        fd = process.stdin.fileno()
        os.set_blocking(fd, False)
        offset = 0
        with selectors.DefaultSelector() as selector:
            selector.register(fd, selectors.EVENT_WRITE)
            while offset < len(raw):
                self._watch_run()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise DispatchError('P_EXPIRED', 'Process input exceeded its finite execution window')
                if selector.select(min(remaining, 0.1)):
                    try:
                        offset += os.write(fd, raw[offset:offset + 65536])
                    except BlockingIOError:
                        continue

    def _communicate(self, process, input_bytes, deadline):
        self._write(process, input_bytes, deadline)
        process.stdin.close()
        result = bytearray()
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, 'out')
            selector.register(process.stderr, selectors.EVENT_READ, 'err')
            while selector.get_map():
                self._watch_run()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise DispatchError('P_EXPIRED', 'Measured process exceeded its finite execution window')
                for key, _ in selector.select(min(remaining, 0.1)):
                    raw = os.read(key.fileobj.fileno(), 65536)
                    if not raw:
                        selector.unregister(key.fileobj)
                        continue
                    self.transferred += len(raw)
                    if self.transferred > self.total_limit:
                        raise DispatchError('P_BUDGET', 'Process output exceeded its aggregate bound')
                    if key.data == 'out':
                        result.extend(raw)
                        if len(result) > self.packet_limit:
                            raise DispatchError('P_BUDGET', 'Measurement output exceeded its bound')
        process.wait(timeout=max(0.01, deadline - time.monotonic()))
        return bytes(result)

    def _broker_observation(self, context_ref, event, request_blob, result_blob=None):
        data = {'request_blob_id': request_blob, 'packet_bytes': self.packet_limit,
                'total_bytes': self.total_limit, 'transferred_bytes': self.transferred}
        if result_blob is not None:
            data['result_blob_id'] = result_blob
        return self._control(context_ref, event, observation=data)

    def _reference(self, request, context_ref):
        proposal = {key: request[key] for key in ('logical_id', 'record_type', 'record')}
        if not wire.validator('record.schema.json', 'proposal').is_valid(proposal):
            raise DispatchError('P_SCHEMA', 'Reference construction requires a closed typed proposal')
        value = lc.record_manifest(self.store.engagement, context_ref['scope'],
                                  request['logical_id'], request['record_type'], request['record'])
        return {'ref': {'engagement': self.store.engagement, 'scope': context_ref['scope'],
                        'logical_id': request['logical_id'], 'version_id': lc.version_id(value)}}

    def _perform_request(self, request, context_ref, packet, assignment=None):
        operation = request['operation']
        if operation == 'read':
            handle = request['handle']
            if handle in self.handles:
                raw = self.handles[handle]
            else:
                identifier = getattr(self, 'delivered_handles', {}).get(handle, self.intrinsic_handles.get(handle))
                raw = self.store._blob(identifier)
            return {'data': base64.b64encode(raw).decode()}
        if operation == 'propose':
            raw = _bytes(request['data'])
            if len(raw) > self.packet_limit:
                raise DispatchError('P_BUDGET', 'Proposed material exceeds its bound')
            identifier = self.store.put_blob(raw)
            self.allowed_blobs.add(identifier)
            return {'blob_id': identifier, 'size': len(raw)}
        if operation == 'materialize':
            return self._materialize(assignment, request)
        if operation == 'reference':
            return self._reference(request, context_ref)
        value = request['value']
        wire.validate(value, 'run-return.schema.json')
        if value['assignment'] != packet['assignment'] or value['context'] != context_ref:
            raise DispatchError('P_ORIGIN', 'Captured return differs from the issued assignment and context')
        if any(identifier not in self.allowed_blobs for proposal in value['records']
               for identifier in proposal['record'].get('material', [])):
            raise DispatchError('P_ORIGIN', 'Returned material was not captured or explicitly delivered')
        return {'return': value}

    def _request(self, request, context_ref, packet, deadline):
        self._last_response_charged = False
        wire.validate(request, 'broker-request.schema.json')
        self._current(context_ref)
        operation = request['operation']
        state = self.store.read()
        details = state.run_details[packet['run_id']]
        previous = details.get('broker_requests', {}).get(request['id'])
        raw_request = lc.canonical(request)
        request_blob = lc.blob(raw_request)
        if previous is not None:
            if previous['request_blob_id'] != request_blob:
                raise DispatchError('P_IDEMPOTENCY', 'Broker identifier reused for different content')
            if previous['status'] != 'ack':
                raise DispatchError('P_UNCERTAIN', 'Physical effect has no recorded outcome; reconcile before retry')
            response = lc.loads(state.validation_assets[previous['result_blob_id']])
            self.transferred = max(self.transferred, details.get('broker_bytes', 0))
            self.allowed_blobs.update(details.get('broker_allowed_blobs', []))
            if not response['ok']:
                raise DispatchError(response['error']['code'], response['error']['message'])
            self._last_response_charged = True
            return response['result']
        if request['id'] in self.request_ids:
            raise DispatchError('P_IDEMPOTENCY', 'Unique terminal request identifier required')
        with lc.store_lock(self.store.path):
            _, context, assignment = self._current(context_ref)
            self._grant(context, assignment, request)
        self.request_ids.add(request['id'])
        if operation == 'return':
            return self._perform_request(request, context_ref, packet)
        self.store.put_blob(raw_request)
        physical = operation in {'materialize', 'measure'}
        if physical:
            self._broker_observation(context_ref, 'broker_requested', request_blob)
        try:
            with lc.store_lock(self.store.path):
                _, context, assignment = self._current(context_ref)
                self._grant(context, assignment, request)
                result = None if operation == 'measure' else self._perform_request(request, context_ref, packet, assignment)
            if operation == 'measure':
                result = self._measure(request, packet, deadline)
            response = {'id': request['id'], 'ok': True, 'result': result}
        except (DispatchError, lc.ERROR) as error:
            response = {'id': request['id'], 'ok': False,
                        'error': {'code': error.code, 'message': str(error)}}
        raw_response = lc.canonical(response)
        self.transferred += len(raw_response) + 1
        self._last_response_charged = True
        result_blob = self.store.put_blob(raw_response)
        self._broker_observation(context_ref, 'broker_observed', request_blob, result_blob)
        event = {'request': request, 'result': response.get('result')} if response['ok'] else {'request': request, 'error': response['error']}
        self.audit.append(event)
        if not response['ok']:
            raise DispatchError(response['error']['code'], response['error']['message'])
        if self.transferred > self.total_limit or len(raw_response) > self.packet_limit:
            raise DispatchError('P_BUDGET', 'Broker response exceeded its aggregate bound')
        return result

    def _conversation(self, process, packet, context_ref, deadline):
        self._write(process, lc.canonical(packet) + b'\n', deadline)
        pending = bytearray()
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, 'out')
            selector.register(process.stderr, selectors.EVENT_READ, 'err')
            while selector.get_map():
                self._watch_run()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise DispatchError('P_EXPIRED', 'Worker exceeded its finite execution window')
                for key, _ in selector.select(min(remaining, 0.1)):
                    raw = os.read(key.fileobj.fileno(), 65536)
                    if not raw:
                        selector.unregister(key.fileobj)
                        continue
                    self.transferred += len(raw)
                    if self.transferred > self.total_limit:
                        raise DispatchError('P_BUDGET', 'Worker exceeded its total output bound')
                    if key.data == 'err':
                        continue
                    pending.extend(raw)
                    if len(pending) > self.packet_limit:
                        raise DispatchError('P_BUDGET', 'Worker frame exceeded its byte bound')
                    while b'\n' in pending:
                        line, _, remainder = pending.partition(b'\n')
                        pending[:] = remainder
                        request = lc.loads(line)
                        try:
                            result = self._request(request, context_ref, packet, deadline)
                        except (DispatchError, lc.ERROR) as error:
                            if request.get('operation') == 'return':
                                raise
                            response = {'id': request.get('id'), 'ok': False,
                                        'error': {'code': error.code, 'message': str(error)}}
                            self.audit.append({'request': request, 'error': response['error']})
                        else:
                            if 'return' in result:
                                return result['return']
                            response = {'id': request['id'], 'ok': True, 'result': result}
                        encoded = lc.canonical(response) + b'\n'
                        if not getattr(self, '_last_response_charged', False):
                            self.transferred += len(encoded)
                        if self.transferred > self.total_limit or len(encoded) > self.packet_limit:
                            raise DispatchError('P_BUDGET', 'Broker response exceeded its byte bound')
                        self._write(process, encoded, deadline)
        raise DispatchError('P_BACKEND', 'Confined worker exited without a captured RunReturn')

    def _prepare_common(self, context_ref):
        state, context, assignment = self._current(context_ref, issued=True)
        if not set(context['ready_basis']) <= set(state.ready_basis(context['assignment'])):
            raise DispatchError('P_CONTEXT', 'Captured ready facts changed before delivery')
        self.execution = state.context_execution(context, live=True)
        packet, self.handles = self._assemble(state, context_ref, context, assignment)
        self.allowed_blobs = {item['blob_id'] for item in packet['attachments']}
        self.allowed_blobs.update(material['blob_id'] for returned in packet.get('owned_returns', [])
                                  for item in returned['records'] for material in item['material'])
        handling = packet.get('handling')
        if handling is not None:
            historical = [handling['package'], *handling['conflicts'], *handling['inputs']]
            self.allowed_blobs.update(material['blob_id'] for item in historical for material in item['material']
                                      if material['status'] == 'available')
        self.request_ids, self.audit = set(), []
        self.transferred = len(lc.canonical(packet)) + 1
        if self.transferred > self.total_limit:
            raise DispatchError('P_BUDGET', 'Initial delivered facts exceed the aggregate transport bound')
        ceiling = min(limit['ceiling'] for limit in state.run_details[context['run_id']]['limits'])
        usage = state.run_details[context['run_id']]['usage'].get('elapsed_ms:ms', 0)
        remaining = ceiling - usage
        if remaining <= 0:
            raise DispatchError('P_BUDGET', 'No measured execution allowance remains')
        return state, context, assignment, packet, usage, remaining

    def _prepare(self, context_ref):
        state, context, assignment, packet, usage, remaining = self._prepare_common(context_ref)
        expected = self.execution['model']['execution']
        if expected.get('provider') != 'json-process/1':
            raise DispatchError('P_BACKEND', 'Native subagents require the host session boundary')
        def identity(worker):
            return {'provider': worker['provider'], 'argv': worker['argv'],
                    'files': sorted(({'name': item['name'], 'sha256': item['sha256']} for item in worker['files']),
                                    key=lambda item: item['name'])}
        descriptor = {**expected, 'files': sorted(expected['files'], key=lambda item: item['name'])}
        workers = [worker for worker in self.config['workers'] if identity(worker) == descriptor]
        if not workers:
            raise DispatchError('P_PROOF', 'Chosen execution has no exactly matching host-enrolled worker')
        worker = workers[0]
        # Validate all host assets/filter support before recording actual execution.
        self._worker(worker)
        return state, context, assignment, worker, packet, usage, remaining

    def _cancel_issued(self, context_ref):
        state = self.store.read()
        if context_ref['version_id'] not in state.versions:
            return
        context = state.resolve(context_ref, 'context')
        run_id = context['run_id']
        if context['assignment'] is not None and state.run_states.get(run_id) == 'issued':
            total = state.run_details[run_id]['usage'].get('elapsed_ms:ms', 0)
            self._control(context_ref, 'run_cancelled', total)

    def dispatch(self, context_ref):
        """Launch and account one exact issued context without accepting its result.

        Args:
            context_ref: Exact already-issued leaf VersionRef, not a new assignment.
        Returns:
            Host outcome with completion receipt, elapsed usage and audit blob.
        Raises:
            DispatchError: Unsupported backend, failed input assembly or bounded
                execution failure. Issued or started failures cancel their physical run.
            OSError, ValueError: Host resources or existing Store checks fail closed.
        """
        try:
            state, context, assignment, worker, packet, usage, remaining = self._prepare(context_ref)
        except Exception:
            self._cancel_issued(context_ref)
            raise
        started = None
        with tempfile.TemporaryDirectory(prefix='jai-dispatch-') as directory:
            folder = Path(directory)
            try:
                self._control(context_ref, 'run_started')
            except Exception:
                self._cancel_issued(context_ref)
                raise
            started = time.monotonic()
            self._running_context = context_ref
            self._journal_seen = self._journal_hint()
            lease_expires = context['expires_at_ms']
            if assignment['deadline_ms'] is not None:
                lease_expires = min(lease_expires, assignment['deadline_ms'])
            if context['speculation'] is not None:
                lease_expires = min(lease_expires, state.speculations[context['speculation']['version_id']]['expires_at_ms'])
            deadline = min(started + remaining / 1000,
                           started + max(0, lease_expires - int(time.time() * 1000)) / 1000)
            try:
                process = self._launch(worker, folder, packet)
                try:
                    value = self._conversation(process, packet, context_ref, deadline)
                finally:
                    _terminate(process)
                total = usage + max(1, math.ceil((time.monotonic() - started) * 1000))
                observed = int(time.time() * 1000)
                raw_audit = lc.canonical({'protocol': HOST_PROTOCOL, 'manifest_hash': packet['manifest_hash'],
                                          'events': self.audit, 'usage_ms': total, 'outcome': 'captured'})
                audit = self.store.put_blob(raw_audit)
                completion = self._control(context_ref, 'run_completed', total, self.store.put_blob(lc.canonical(value)),
                                           observed, (audit, len(raw_audit)))
                return {'status': 'completed', 'completion': completion, 'usage_ms': total, 'audit_blob_id': audit}
            except Exception as error:
                total = usage + max(1, math.ceil((time.monotonic() - started) * 1000))
                raw_audit = lc.canonical({'protocol': HOST_PROTOCOL, 'manifest_hash': packet['manifest_hash'],
                                          'events': self.audit, 'usage_ms': total, 'outcome': 'failed',
                                          'error_code': getattr(error, 'code', 'P_BACKEND')})
                audit = self.store.put_blob(raw_audit)
                self._control(context_ref, 'run_cancelled', total, audit=(audit, len(raw_audit)))
                raise
            finally:
                self._running_context = None
                self._journal_seen = None


def main(argv=None):
    """Run the local dispatcher CLI; host configuration never enters transport.

    Args:
        argv: Optional host argument list; defaults to process arguments.
    Returns:
        Zero for a captured completion and one for a safe diagnostic.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True)
    parser.add_argument('--engagement', required=True)
    parser.add_argument('--context', required=True, help='File containing an exact issued VersionRef')
    parser.add_argument('--config', required=True, help='Host-owned dispatcher configuration JSON')
    args = parser.parse_args(argv)
    try:
        config = lc.loads(operator.regular(args.config))
        context = lc.loads(operator.regular(args.context))
        result = Dispatcher(lc.Store(args.store, args.engagement), config).dispatch(context)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, OSError) as error:
        print(json.dumps({'status': 'rejected', 'code': getattr(error, 'code', 'P_BACKEND'), 'message': str(error)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
