# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Immutable identities and the sole local-writer format-9 lifecycle engine.

All semantic values are integer/string JSON. Explicit L0 wrappers have their own
serialization and are preserved as exact bytes in the journal.
No legacy ledger reader or authority credential is provided here.
"""
from __future__ import annotations

import copy
import base64
import hashlib
import json
import os
import re
from pathlib import Path
from functools import wraps
from contextlib import contextmanager
import tempfile
import time
import unicodedata
import uuid

VERSION_DOMAIN = b'jai.lifecycle.version.v2\0'
BLOB_DOMAIN = b'jai.lifecycle.blob.v2\0'
TRANSACTION_DOMAIN = b'jai.lifecycle.transaction.v9\0'
CATEGORIES = ('source', 'test', 'configuration', 'environment', 'contract', 'policy', 'assumptions')
OPERATIONS = {'governed'}
ZERO = '0' * 64


class LifecycleError(ValueError):
    """Reject malformed identity, immutable history, selection or gate input."""


class _FrozenDict(dict):
    """Admitted JSON object; ordinary copies remain editable proposals."""

    def _deny(self, *args, **kwargs):
        raise TypeError('Admitted history is immutable; deepcopy it to propose a change')

    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = __ior__ = _deny

    def __deepcopy__(self, memo):
        result = {}
        memo[id(self)] = result
        result.update((copy.deepcopy(key, memo), copy.deepcopy(value, memo)) for key, value in self.items())
        return result


class _FrozenList(list):
    """Admitted JSON array with the same JSON/equality semantics as a list."""

    def _deny(self, *args, **kwargs):
        raise TypeError('Admitted history is immutable; deepcopy it to propose a change')

    __setitem__ = __delitem__ = append = clear = extend = insert = pop = remove = reverse = sort = __iadd__ = __imul__ = _deny

    def __deepcopy__(self, memo):
        result = []
        memo[id(self)] = result
        result.extend(copy.deepcopy(value, memo) for value in self)
        return result


def _freeze(value):
    """Detach newly admitted JSON containers and make their descendants read-only."""
    if isinstance(value, (_FrozenDict, _FrozenList)):
        return value
    if isinstance(value, dict):
        return _FrozenDict((key, _freeze(item)) for key, item in value.items())
    if isinstance(value, list):
        return _FrozenList(_freeze(item) for item in value)
    return value


def _typed_key(value):
    """Use exact typed JSON equality without repeatedly serializing lookup keys."""
    if isinstance(value, dict):
        return ('object', tuple(sorted((key, _typed_key(item)) for key, item in value.items())))
    if isinstance(value, list):
        return ('array', tuple(_typed_key(item) for item in value))
    return (type(value).__name__, value)


def normal(value):
    """Return recursively NFC-normalized JSON; reject floats and key collisions.

    Args:
        value: JSON value containing only strings, integers, booleans and null.
    Returns:
        Normalized copy, preserving array order and text whitespace.
    Raises:
        LifecycleError: Unsupported type, nonstring key or normalized collision.
    """
    if value is None or type(value) in (bool, int):
        return value
    if isinstance(value, str):
        return unicodedata.normalize('NFC', value)
    if isinstance(value, list):
        return [normal(item) for item in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise LifecycleError('object keys must be strings')
            key = normal(key)
            if key in result:
                raise LifecycleError('normalized key collision')
            result[key] = normal(item)
        return result
    raise LifecycleError('unsupported semantic value type: ' + type(value).__name__)


def canonical(value):
    """Return strict canonical UTF-8 bytes for a semantic JSON value.

    Args:
        value: Integer-only JSON data normalized recursively to NFC.
    Returns:
        Deterministic sorted-key UTF-8 representation, preserving array order.
    Raises:
        LifecycleError: Unsupported types or normalized key collisions occur.
    """
    return json.dumps(normal(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def loads(raw):
    """Parse JSON rejecting duplicate keys, floats and nonfinite constants.

    Args:
        raw: UTF-8 bytes or JSON text.
    Returns:
        Normalized semantic JSON value.
    Raises:
        LifecycleError: Duplicate keys or disallowed numeric values.
        ValueError: Invalid JSON syntax.
    """
    def pairs(items):
        result = {}
        for key, value in items:
            key = normal(key)
            if key in result:
                raise LifecycleError('duplicate JSON key')
            result[key] = value
        return result
    def reject(value):
        raise LifecycleError('noninteger semantic number: ' + value)
    return normal(json.loads(raw, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject))


def blob(data):
    """Return domain-separated exact-byte content identity for bytes data."""
    return hashlib.sha256(BLOB_DOMAIN + data).hexdigest()


def manifest(logical_id, kind, content, bindings=None, members=None):
    """Build a canonical immutable version manifest with sorted composite members.

    Args:
        logical_id: Stable opaque identity, independent of paths.
        kind: Semantic record kind.
        content: Semantic JSON payload without locator or display metadata.
        bindings: Exact input-category bindings, when this is a conclusion.
        members: Unordered role/logical_id/version_id member objects.
    Returns:
        Normalized manifest; array order in content remains significant.
    Raises:
        LifecycleError: Empty identity, invalid members or invalid semantic data.
    """
    if not isinstance(logical_id, str) or not logical_id.strip() or not kind:
        raise LifecycleError('explicit logical identity and kind required')
    members = normal(copy.deepcopy(members or []))
    if any(set(item) != {'role', 'logical_id', 'version_id'} for item in members):
        raise LifecycleError('exact composite member fields required')
    keys = [(item['role'], item['logical_id']) for item in members]
    if len(set(keys)) != len(keys):
        raise LifecycleError('duplicate composite member')
    members.sort(key=lambda item: (item['role'], item['logical_id']))
    return normal({'schema': 'jai.lifecycle.manifest/2', 'logical_id': logical_id,
                   'kind': kind, 'content': content, 'bindings': bindings or {}, 'members': members})


def version_id(value):
    """Return the domain-separated immutable identity of a manifest.

    Args:
        value: Complete semantic version manifest, including its input bindings.
    Returns:
        Lowercase SHA-256 digest of its canonical bytes and version domain.
    Raises:
        LifecycleError: The manifest contains noncanonical semantic data.
    """
    return hashlib.sha256(VERSION_DOMAIN + canonical(value)).hexdigest()


# State transitions and permission derivation live here, never in the wire adapter.
import governed_delivery as wire
import operator_actions as operator

PROTOCOL = wire.PROTOCOL
RECORD_KINDS = {'source', 'profile', 'assignment', 'context', 'product', 'assessment'}
ERROR = wire.ProtocolError


@contextmanager
def store_lock(path):
    """Hold the journal's nonblocking process-lifetime writer lock.

    Args:
        path: Exact journal path; its persistent regular ``.lock`` inode is shared
            by recording and short physical-effect critical sections.
    Yields:
        None while this process owns the lock. Never hold it across native waits.
    Raises:
        ProtocolError: Another writer owns the lock, the inode changed, or this
            platform has no qualified native lock implementation.
        OSError: The lock file cannot be opened safely.
    """
    try:
        import fcntl
    except ImportError as error:
        raise ERROR('P_BACKEND', 'Native journal locking is unavailable on this platform') from error
    import stat
    lock_path = str(path) + '.lock'
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        actual = os.fstat(descriptor)
        if not stat.S_ISREG(actual.st_mode):
            raise ERROR('P_INTEGRITY', 'Journal lock must be a regular file')
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ERROR('P_HEAD', 'Concurrent governed operation; retry against current state') from error
        current = os.stat(lock_path, follow_symlinks=False)
        if (actual.st_dev, actual.st_ino) != (current.st_dev, current.st_ino):
            raise ERROR('P_INTEGRITY', 'Journal lock identity changed during acquisition')
        yield
    finally:
        # Closing releases the OS lock even after process failure. Unlinking would
        # let another writer lock a different inode while this one is still held.
        os.close(descriptor)


def message_id(message):
    """Return exact protocol message identity; message confers no authority."""
    return wire.message_id(message)


def record_manifest(engagement, scope, logical_id, record_type, record):
    """Build one closed record manifest with immutable scope and typed content.

    Args:
        engagement: Exact engagement owning the record.
        scope: Exact applicability scope.
        logical_id: Stable owner-assigned logical identity.
        record_type: One of the six closed protocol record families.
        record: Closed typed body, never generic lifecycle operations.
    Returns:
        Existing version-v2 manifest with a delivery-specific kind.
    Raises:
        ProtocolError: Record family or structure is invalid.
    """
    if record_type not in RECORD_KINDS:
        raise ERROR('P_SCHEMA', 'Unknown governed record family')
    if not wire.validator('record.schema.json', record_type).is_valid(record):
        raise ERROR('P_SCHEMA', 'Closed typed record required')
    return manifest(logical_id, 'delivery.' + record_type,
                    {'engagement': engagement, 'scope': scope, 'record': record})


def _hash(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def _ref(value, engagement=None, scope=None):
    content = value['content']
    return {'engagement': engagement or content['engagement'], 'scope': scope or content['scope'],
            'logical_id': value['logical_id'], 'version_id': version_id(value)}


def _references(value):
    if isinstance(value, dict):
        if set(value) == {'engagement', 'scope', 'logical_id', 'version_id'}:
            yield value
        else:
            for key in sorted(value):
                yield from _references(value[key])
    elif isinstance(value, list):
        for child in value:
            yield from _references(child)


def _reference_paths(value, path=''):
    if isinstance(value, dict):
        if set(value) == {'engagement', 'scope', 'logical_id', 'version_id'}:
            yield path, value
        else:
            for key in sorted(value):
                yield from _reference_paths(value[key], path + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _reference_paths(child, path + '/' + str(index))


def _causal_reference_paths(record):
    # Read grants locate already assigned inputs; they do not select a second
    # semantic use of those inputs. Tool policies and non-read effect targets
    # remain dependencies in their own right.
    for path, reference in _reference_paths(record):
        parts = path.split('/')
        if path.startswith('/handling/') or record.get('product_kind') == 'escalation' and (path.startswith('/episode/') or path.startswith('/related/')):
            continue
        if ('issued_under' in record and len(parts) == 5
                and parts[1] == 'effects' and parts[3] == 'targets'
                and record['effects'][int(parts[2])]['operation'] == 'read'):
            continue
        yield path, reference


def _owner_key(owner):
    return canonical(owner).decode()


def _input_locators(bindings):
    result = []
    for binding in bindings:
        for reference in binding['refs']:
            if reference not in result:
                result.append(reference)
    return result


def _proof_key(scope, slot):
    return scope, canonical(slot).decode()


def _bootstrap_scopes(message):
    if message['message_type'] != 'bootstrap':
        return
    scopes = message['payload']['use_scopes']
    if (message['scope'] not in scopes or len(scopes) != len(set(scopes))
            or not 1 <= len(scopes) <= 64 or '*' in scopes):
        raise ERROR('P_SCOPE', 'Bootstrap requires explicit finite initial semantic scopes')


def _within_assessment(method):
    """Share completed checks only through one stable recursive assessment."""
    @wraps(method)
    def assessed(self, *args, **kwargs):
        root = self._assessment_walk is None
        if root:
            self._assessment_walk = {'requirements': set(), 'evaluations': {},
                                     'closures': {}, 'material': {}}
        try:
            return method(self, *args, **kwargs)
        finally:
            if root:
                self._assessment_walk = None
    return assessed


class State:
    """Replay-derived indexes of the one governed store; never a caller trust input."""

    def __init__(self, engagement=None, blob_reader=None):
        """Create empty replay indexes for engagement and optional exact blob reader."""
        self.engagement = engagement
        self.blob_reader = blob_reader
        self.transactions = []
        self.versions = {}
        self._identities = {}
        self.provenance = {}
        self.states = {}
        self.selections = {}
        self.proofs = {}
        self.reliance = {}
        self.assignment_states = {}
        self.run_states = {}
        self.escalations = {}
        self.episodes = {}
        self.speculations = {}
        self.holds = {}
        self.consumed_basis = {}
        self.execution_plans = {}
        self.procedures = {}
        self.procedure_steps = {}
        self.invocations = {}
        self.local_budget = {'units': {}, 'bindings': {}, 'task_stops': {}}
        self.search_steps = {}
        self.requests = {}
        self.messages = {}
        self.human_uses = {}
        self.usage = {}
        self.decisions = {}
        self.events = []
        self.head = ZERO
        self.initialized = False
        self.run_details = {}
        self.native_handles = {}
        self._native_packet_facts = {}
        self._broker_frames = {}
        self.return_artifact = None
        self.validation_assets = {}
        self.validation_artifacts = []
        self.validation_replay_artifacts = None
        self._routing_snapshots = {}
        self.escalation_members = {}
        self.counters = {}
        self.sources = {}
        self.scope = 'default'
        self._assessment_walk = None
        self._selection_latest = {}
        self._point_selections = {}
        self._decision_selections = {}
        self._use_changes = {}
        self._product_content = {}
        self._product_records = {}
        self._assignment_records = {}
        self._content_policies = {}

    def _fork(self):
        """Detach mutable state while sharing admitted read-only history values.

        Every outer history/index container belongs to this snapshot. Immutable
        admitted descendants and the external reader capability may be shared;
        operational state is still independently copied with one alias memo.
        """
        shared = {'versions', '_identities', 'messages', 'transactions', 'events',
                  'provenance', 'requests', '_routing_snapshots', 'validation_assets',
                  '_selection_latest', '_point_selections', '_decision_selections',
                  '_product_content', '_product_records', '_assignment_records', '_content_policies',
                  '_native_packet_facts', '_broker_frames'}
        memo = {id(self.blob_reader): self.blob_reader}
        result = object.__new__(type(self))
        memo[id(self)] = result
        for name in shared:
            value = getattr(self, name)
            detached = value.copy()
            setattr(result, name, detached)
            memo[id(value)] = detached
            for item in value.values() if isinstance(value, dict) else value:
                if isinstance(item, (_FrozenDict, _FrozenList, tuple)):
                    memo[id(item)] = item
        for name, value in self.__dict__.items():
            if name not in shared and name != '_assessment_walk':
                setattr(result, name, copy.deepcopy(value, memo))
        # A fork may change its semantic view before applying any effects.
        result._assessment_walk = None
        return result

    def local_budget_status(self, assignment_ref, at_ms=None):
        """Report the local iteration without renewing time or semantic authority.

        Args:
            assignment_ref: Exact admitted mandate reference or explicit local unit ID.
            at_ms: Explicit trusted observation time, otherwise current UTC time.
        Returns:
            Unit identity, revision, remaining allowance, stage and pending handles.
        Raises:
            ProtocolError: The assignment identity is unavailable.
        """
        import governed_local_budget
        if isinstance(assignment_ref, str):
            if assignment_ref not in self.local_budget['units']:
                raise ERROR('P_CONTEXT', 'Exact local unit identity is unavailable')
            return governed_local_budget._unit_status(self, assignment_ref,
                int(time.time() * 1000) if at_ms is None else at_ms)
        self.resolve(assignment_ref, 'assignment')
        return governed_local_budget._status(self, assignment_ref,
            int(time.time() * 1000) if at_ms is None else at_ms)

    def _attempt_ref(self, reference):
        while True:
            record = self.resolve(reference, 'assignment')
            if record.get('handling') is not None:
                return self._episode(record['handling']['episode'])['attempt']
            parent = record['issued_under']
            if parent is None or self.resolve(parent, 'assignment')['owner']['layer'] != record['owner']['layer']:
                return reference
            reference = parent

    def _episode(self, reference):
        identifier = reference['version_id']
        if identifier in self.episodes:
            return self.episodes[identifier]
        matches = [item for item in self.episodes.values() if identifier in item['revisions']]
        if len(matches) != 1:
            raise ERROR('P_CONTEXT', 'Exact recorded escalation episode required')
        return matches[0]

    def _held(self, point):
        return self._key(point) in self.holds

    def _blocking_episodes(self, reference, record):
        scope = record['use_scope']
        dependencies = {self._key(point) for point in self._dependencies(record)}
        return [episode for episode in self.episodes.values()
                if self.escalations.get(episode['root']['version_id']) == 'open'
                and (episode['scope'] == scope and record['owner']['layer'] == episode['layer']
                     or self._key(reference, scope) in {self._key(point) for point in episode['members']}
                     or dependencies & {self._key(point) for point in episode['members']})]

    def _handling_right(self, record):
        handling = record.get('handling')
        if handling is None:
            return False
        episode = self._episode(handling['episode'])
        if (handling['package']['version_id'] not in episode['revisions']
                or self.escalations.get(episode['root']['version_id']) != 'open'
                or record['use_scope'] != episode['scope']
                or record['owner']['work_item'] != episode['work_item']):
            raise ERROR('P_SCOPE', 'Handling is bound to its exact open episode and work scope')
        if not 1 <= record['owner']['layer'] <= episode['layer']:
            raise ERROR('P_SCOPE', 'Handling cannot acquire a lower or unrelated layer')
        return True

    def _grant_right(self, reference, record, grant_ref, at, live):
        grant = self.speculations.get(grant_ref['version_id'])
        if grant is None or grant['ref'] != grant_ref or reference not in grant['assignments']:
            raise ERROR('P_SCOPE', 'Speculation must name this exact existing assignment')
        episode = self._episode(grant['escalation'])
        if (self.escalations.get(episode['root']['version_id']) != 'open'
                or at >= grant['expires_at_ms'] or record['deadline_ms'] is not None and at >= record['deadline_ms']
                or record['use_scope'] != episode['scope']):
            raise ERROR('P_EXPIRED', 'Speculative execution grant is no longer active')
        if self._status(grant_ref, episode['scope'])['validity'] != 'valid':
            raise ERROR('P_PROOF', 'Speculative execution grant was revoked')
        self._governing_grants({'decision_ref': grant_ref, 'scope': episode['scope'],
            'grants': [{'purpose': 'delivery-change', 'key_id': grant['human_key_id']}]}, live)
        if any(not self._governing_input(point, live) for point in grant['inputs']):
            raise ERROR('P_CONTEXT', 'Speculative governing inputs changed')
        for limit in grant['limits']:
            key = limit['metric'] + ':' + limit['unit']
            spent = sum(details['usage'].get(key, 0) for details in self.run_details.values()
                        if self.resolve(details['context'], 'context')['speculation'] == grant_ref)
            if spent >= limit['ceiling']:
                raise ERROR('P_BUDGET', 'Measured shared speculative allowance is exhausted')
        return grant

    def _execution_right(self, reference, record, context=None, at=None, live=True):
        at = int(time.time() * 1000) if at is None else at
        state = self.assignment_states.get(reference['version_id'])
        if state not in {'open', 'paused'}:
            return False
        attempt = self._attempt_ref(reference)
        settings = self.resolve(record['profile'], 'profile')['scheduling']
        running = context is not None and self.run_states.get(context.get('run_id')) == 'running'
        if (settings['max_search_steps'] is not None and self.search_steps.get(attempt['version_id'], 0) >= settings['max_search_steps'] and not running) or (record['deadline_ms'] is not None and at >= record['deadline_ms']):
            return False
        pinned = self.run_details.get(context.get('run_id'), {}).get('local_unit_id') if context is not None else None
        local = self.local_budget_status(pinned or reference, at)
        if local is not None and (local['state'] in {'paused', 'terminated', 'obsolete'} or local['remaining_ms'] <= 0):
            return False
        binding = self.local_budget['bindings'].get(reference['version_id'])
        if binding is not None and (binding['scope'], binding['root_generation']) in self.local_budget['task_stops']:
            return False
        if record.get('handling') is not None:
            return state == 'open' and self._handling_right(record)
        grant_ref = context.get('speculation') if context is not None else None
        if grant_ref is not None:
            self._grant_right(reference, record, grant_ref, at, live)
            return True
        return state == 'open' and not self._blocking_episodes(reference, record)

    @_within_assessment
    def execution_eligible(self, context_ref, at_ms=None, live=True):
        """Check one run's current work right without treating unrelated heads as revocation.

        Args:
            context_ref: Exact issued run context reference.
            at_ms: Assessment time in UTC milliseconds, defaulting to the current clock.
            live: Require current material and authority for an actual new effect.
        Returns:
            True when the exact run remains eligible; otherwise a typed rejection.
        Raises:
            ProtocolError: Pause, grant, time, ownership or governing inputs forbid work.
        """
        context = self.resolve(context_ref, 'context')
        record = self.resolve(context['assignment'], 'assignment')
        at = int(time.time() * 1000) if at_ms is None else at_ms
        if (self.run_states.get(context['run_id']) not in {'issued', 'running'}
                or at >= context['expires_at_ms']
                or self._status(context_ref, context_ref['scope'])['validity'] != 'valid'
                or not self._execution_right(context['assignment'], record, context, at, live)):
            raise ERROR('P_STATE', 'Run has no current productive, handling or speculative execution right')
        self._assignment_requirements(record, live)
        self._context_execution(context, live)
        if not self._current_inputs(record, live):
            raise ERROR('P_CONTEXT', 'Execution inputs no longer govern this assignment')
        return True

    def ready_basis(self, assignment_ref, at_ms=None):
        """Return deterministic relevant facts a fresh work context will actually receive.

        Args:
            assignment_ref: Exact stored assignment reference.
            at_ms: Captured UTC milliseconds for deterministic context replay; current time for queries.
        Returns:
            Sorted opaque tokens for the mandate, current owned publications and transitions.
        Raises:
            ProtocolError: Assignment or referenced immutable records are unavailable.
        """
        record = self.resolve(assignment_ref, 'assignment')
        at = int(time.time() * 1000) if at_ms is None else at_ms
        facts = {'assignment:' + assignment_ref['version_id']}
        for point in self._dependencies(record):
            facts.add('input:' + point['use_scope'] + ':' + point['ref']['version_id'])
        for identifier, value in self.versions.items():
            if value['kind'] not in {'delivery.product', 'delivery.assessment'}:
                continue
            reference = self._reference(identifier)
            if self.provenance[identifier]['origin'] == {'kind': 'assignment', 'ref': assignment_ref}:
                continue
            if self._produced_under(reference, assignment_ref, record['owner']):
                state = self._status(reference, record['use_scope'])['validity']
                facts.add('record:' + identifier + ':' + state + (':held' if self._held(self._point(reference, record['use_scope'])) else ''))
        for event in self.events:
            if event['kind'] == 'selection' and event['scope'] == record['use_scope']:
                subject = event.get('subject')
                owned = subject is not None and self.resolve(subject).get('owner') == record['owner']
                if event['category'] in {'proof', 'basis'} and (owned or subject is not None and any(token.startswith('record:' + subject['version_id'] + ':') for token in facts)):
                    facts.add('transition:' + event['decision_ref']['version_id'])
            elif event['kind'] in {'information_request', 'information_response', 'change_request', 'relay'}:
                message = self.messages.get(event.get('message_id'))
                if message is None:
                    continue
                sender = message['sender']
                direct = sender['kind'] == 'assignment' and self.resolve(sender['ref'], 'assignment')['issued_under'] == assignment_ref
                if direct or message['recipient'] == {'kind': 'assignment', 'ref': assignment_ref}:
                    facts.add('intent:' + message['message_id'])
        if record.get('handling') is not None:
            episode = self._episode(record['handling']['episode'])
            facts.add('episode:' + episode['current']['version_id'])
            if episode['decisive'] or at >= episode['collect_until_ms']:
                facts.add('collection:closed:' + episode['root']['version_id'])
        return sorted(facts)

    def readiness(self, scope='default', speculation=None):
        """Project a deterministic bounded driver's work without executing or granting it.

        Args:
            scope: Exact engagement use scope.
            speculation: Optional exact signed grant covering the queried work.
        Returns:
            Ordered assignment facts with phase, captured choice, basis and wait reason.
        Raises:
            ProtocolError: Stored mandate or exact grant identity is malformed.
        """
        result = []
        for identifier, value in self.versions.items():
            if value['kind'] != 'delivery.assignment':
                continue
            reference, record = self._reference(identifier), value['content']['record']
            if record['use_scope'] != scope:
                continue
            basis = self.ready_basis(reference)
            item = {'assignment': reference, 'ready': False, 'phase': None, 'selection': None,
                    'basis': basis, 'reason': 'waiting'}
            try:
                allowed = self._execution_right(reference, record, {'speculation': speculation}, live=False)
            except ERROR as error:
                allowed, item['reason'] = False, error.code
            inflight = any(self.resolve(details['context'], 'context')['assignment'] == reference
                           and self.run_states.get(run_id) in {'issued', 'running'} for run_id, details in self.run_details.items())
            if inflight:
                allowed, item['reason'] = False, 'inflight'
            if allowed and record['responsibility'] == 'setter':
                procedure = self.procedures.get((identifier, scope))
                if procedure is not None:
                    progress = self.procedure_next(procedure, live=True)
                    new_intents = set(basis) - set(self.consumed_basis.get(identifier, []))
                    discretionary = progress.get('waiting') == 'owner_required' or any(
                        token.startswith('intent:') for token in new_intents)
                    if not discretionary:
                        allowed, item['reason'] = False, 'owner_procedure_advances_or_waits'
            if allowed:
                selection = self.execution_plans.get((identifier, scope))
                if self.consumed_basis.get(identifier) != basis:
                    if selection is not None and self._status(selection, scope)['validity'] == 'valid':
                        item.update(ready=True, phase='work', selection=selection, reason=None)
                    else:
                        item.update(ready=True, phase='selection', reason=None)
            else:
                item['reason'] = item['reason'] if item['reason'] != 'waiting' else 'paused_or_terminal'
            result.append(item)
        return sorted(result, key=lambda item: (self.resolve(item['assignment'])['owner']['layer'],
                      self.resolve(item['assignment'])['owner']['work_item'], item['assignment']['logical_id'], item['assignment']['version_id']))

    def handling_entry(self, episode_ref, task, layer=None, live=True):
        """Derive a finite episode handling mandate without granting productive rights.

        Args:
            episode_ref: Exact recorded episode or revision reference.
            task: Collection, relay, owner resolution or reconciliation responsibility.
            layer: Local handling layer; defaults to the episode layer.
            live: Require current material for a new mandate, not historical replay.
        Returns:
            Deterministic logical_id and assignment record for normal signed ingress.
        Raises:
            ProtocolError: Episode, adjacent routing, current basis or task is invalid.
        """
        episode = self._episode(episode_ref)
        layer = (max(1, episode['layer'] - 1) if task in {'relay', 'resolve'} else episode['layer']) if layer is None else layer
        if task not in {'collect', 'relay', 'resolve', 'reconcile'} or not 1 <= layer <= episode['layer']:
            raise ERROR('P_SCOPE', 'Handling task and layer must belong to this episode')
        if layer < episode['layer'] - 1 and not any(event['kind'] == 'relay' and event['payload'].get('episode') == episode['root']
                and event['payload'].get('to_layer') == layer for event in self.events):
            raise ERROR('P_SCOPE', 'Farther handling needs the recorded adjacent relay chain')
        if task in {'collect', 'reconcile'} and layer != episode['layer']:
            raise ERROR('P_SCOPE', 'Local collection and reconciliation stay at the originating layer')
        package = self.resolve(episode['current'], 'product')
        original = self.resolve(package['assignment'], 'assignment')
        owner = {**original['owner'], 'layer': layer, 'work_kind': 'integration', 'question': None}
        policy = self.capability_policy(package['profile'])
        points = [self._point(ref, selected_scope) for (selected_scope, _), ref in self.sources.items()
                  if selected_scope == episode['scope'] and self.resolve(ref)['source_role'] != 'policy'] + [policy]
        content = self.content_policy(package['profile'])
        if content is not None:
            points.append(content)
        criteria = [point['ref'] for point in points if self.resolve(point['ref'])['source_role'] == 'criteria']
        if len(criteria) != 1:
            raise ERROR('P_CONTEXT', 'Handling needs one current attributable criteria source')
        record = {'owner': owner, 'responsibility': 'setter', 'assigned_actor': '', 'profile': package['profile'],
                  'routing': {'policy': policy['ref']}, 'inherited': [point['ref'] for point in points],
                  'inputs': [{'slot_id': 'current:' + str(index), 'refs': [point['ref']]} for index, point in enumerate(points)],
                  'criteria': criteria[0], 'effects': [], 'limits': copy.deepcopy(self.resolve(package['profile'], 'profile')['scheduling']['control_limits']),
                  'deadline_ms': int(time.time() * 1000) + self.resolve(package['profile'], 'profile')['max_request_duration_ms'],
                  'use_scope': episode['scope'], 'issued_under': None, 'input_uses': [],
                  'handling': {'episode': episode['root'], 'package': episode['current'], 'task': task}}
        # The episode's declared collection/control deadline is immutable, so a
        # replay or regenerated proposal cannot extend its resource window.
        record['deadline_ms'] = episode['control_until_ms']
        identity = _hash({'handling': record['handling'], 'owner': owner, 'inputs': points})
        record['assigned_actor'] = 'handling:' + identity
        for path, reference in _reference_paths(record):
            if path.startswith(('/inherited/', '/inputs/')) or path in {'/criteria', '/routing/policy'}:
                use = next(point['use_scope'] for point in points if point['ref'] == reference)
                record['input_uses'].append({'at': path, 'use_scope': use})
        available = self._assignment_routing(record, live)
        for template in available['capabilities']['effects']:
            if template['operation'] in {'read', 'propose'}:
                record['effects'].append({**template, 'owner': owner,
                    'targets': [] if template['operation'] == 'propose' else [point['ref'] for point in points]})
        return {'logical_id': 'handling:' + identity, 'record': record}

    def _terminal_requirements(self, record, at):
        outcome = record['outcome']
        attempt = self.resolve(outcome['attempt'], 'assignment')
        producer = self.resolve(record['assignment'], 'assignment')
        if (self._attempt_ref(record['assignment']) != outcome['attempt']
                or attempt['owner']['layer'] != producer['owner']['layer']
                or attempt['profile'] != record['profile']):
            raise ERROR('P_SCOPE', 'A terminal claim must identify its actual layer attempt and governing profile')
        for reference in outcome['evidence']:
            self.resolve(reference)
        kind = outcome['kind']
        settings = self.resolve(record['profile'], 'profile')['scheduling']
        if kind == 'demonstrated_contradiction' and len(outcome['evidence']) < 2:
            raise ERROR('P_PROOF', 'A contradiction needs explicit conflicting constraints and independently assessed argument')
        if kind == 'insufficient_information' and not outcome['evidence']:
            raise ERROR('P_PROOF', 'Missing information requires attributable unanswered requirements or evidence')
        if kind == 'search_exhausted' and ((settings['max_search_steps'] is None or self.search_steps.get(outcome['attempt']['version_id'], 0) < settings['max_search_steps'])
                and (attempt['deadline_ms'] is None or at < attempt['deadline_ms'])):
            raise ERROR('P_BUDGET', 'Search exhaustion must be supported by actual attempt limits or deadline')
        if kind == 'human_termination' and not any(self.versions[reference['version_id']]['kind'] == 'delivery.decision'
                and self.resolve(reference)['message']['payload'].get('action') == 'terminate'
                and self.resolve(reference)['message']['payload'].get('authority_proof') is not None
                and outcome['attempt'] in self.resolve(reference)['message']['payload']['subjects']
                for reference in outcome['evidence']):
            raise ERROR('P_PROOF', 'Human termination requires the actual exact signed L0 act')

    def attempt_status(self, attempt_ref):
        """Report typed outcomes and actual bounds without claiming search impossibility.

        Args:
            attempt_ref: Exact root coordinating assignment identifying the attempt.
        Returns:
            Attempt, current outcome, measured steps, bounds and governing episode facts.
        Raises:
            ProtocolError: The attempt identity is not an existing assignment.
        """
        record = self.resolve(attempt_ref, 'assignment')
        generation, root = self._generation(attempt_ref)
        settings = self.resolve(record['profile'], 'profile')['scheduling']
        attempt = self._attempt_ref(attempt_ref)
        steps = self.search_steps.get(attempt['version_id'], 0)
        candidates = [self._reference(identifier) for identifier, value in self.versions.items()
                      if value['kind'] == 'delivery.product' and value['content']['record']['product_kind'] == 'final_result'
                      and value['content']['record']['outcome']['attempt'] == attempt_ref
                      and not self._held(self._point(self._reference(identifier), record['use_scope']))
                      and any(message['message_type'] == 'submission' and message['payload']['candidate'] == self._reference(identifier) for message in self.messages.values())
                      and self._status(self._reference(identifier), record['use_scope'])['validity'] not in {'invalid', 'revoked'}]
        outcome = None
        for reference in candidates:
            product = self.resolve(reference)
            kind = product['outcome']['kind']
            if kind in {'verified_candidate', 'demonstrated_contradiction'} and not self._governing_input(self._point(reference, record['use_scope']), live=True):
                continue
            outcome = {'kind': kind, 'record': reference, 'evidence': product['outcome']['evidence']}
        if self.assignment_states.get(attempt_ref['version_id']) == 'cancelled':
            for identifier, value in self.versions.items():
                if value['kind'] == 'delivery.decision':
                    decision = value['content']['record']['message']['payload']
                    if decision.get('action') == 'terminate' and decision.get('authority_proof') is not None and attempt_ref in decision['subjects']:
                        outcome = {'kind': 'human_termination', 'record': self._reference(identifier), 'evidence': [self._reference(identifier)]}
        exhausted = (settings['max_search_steps'] is not None and steps >= settings['max_search_steps']) or (root['deadline_ms'] is not None and int(time.time() * 1000) >= root['deadline_ms'])
        if outcome is None and exhausted:
            outcome = {'kind': 'search_exhausted', 'record': None, 'evidence': []}
        return {'attempt': attempt_ref, 'outcome': outcome, 'steps': steps,
                'step_limit': settings['max_search_steps'], 'deadline_ms': root['deadline_ms']}

    def resolve(self, reference, kind=None):
        """Resolve an exact scoped immutable reference or reject missing/type-confused input.

        Args:
            reference: Exact version reference; no latest-version resolution.
            kind: Optional required protocol record family.
        Returns:
            Typed immutable record body.
        Raises:
            ProtocolError: Identity, engagement, scope or expected kind does not match.
        """
        value = self.versions.get(reference.get('version_id')) if isinstance(reference, dict) else None
        if value is None or self._reference(reference['version_id']) != reference:
            raise ERROR('P_CONTEXT', 'Exact referenced version is unavailable')
        if kind and value['kind'] != 'delivery.' + kind:
            raise ERROR('P_PROOF' if kind == 'assessment' else 'P_CONTEXT', 'Referenced record has the wrong type')
        return value['content']['record']

    def _reference(self, identifier):
        # Identities are derived once from registered immutable manifests in this
        # replay snapshot. Return a new object so callers cannot alter the index.
        engagement, scope, logical_id = self._identities[identifier]
        return {'engagement': engagement, 'scope': scope,
                'logical_id': logical_id, 'version_id': identifier}

    def _index_version(self, identifier, value):
        self.versions[identifier] = _freeze(value)
        content = value['content']
        self._identities[identifier] = (content['engagement'], content['scope'], value['logical_id'])

    def _point(self, reference, scope=None):
        if set(reference) == {'ref', 'use_scope'}:
            return copy.deepcopy(reference)
        return {'ref': copy.deepcopy(reference), 'use_scope': self.scope if scope is None else scope}

    def _key(self, reference, scope=None):
        point = self._point(reference, scope)
        return point['use_scope'], point['ref']['version_id']

    def _status(self, reference, scope=None):
        key = self._key(reference, scope)
        if key in self.holds:
            return {'validity': 'pending', 'applicable': False}
        return self.states.get(key, {'validity': 'pending', 'applicable': False})

    def _assignment_use(self, assignment, path, reference):
        selectors = {item['at']: item['use_scope'] for item in assignment['input_uses']}
        if path == '/routing/policy':
            anchor = self.transactions[0]['operations'][0]['data']['message']['scope']
            if path in selectors and selectors[path] != anchor:
                raise ERROR('P_SCOPE', 'Global capability policy cannot be remapped by a task')
            return self._point(reference, anchor)
        if path == '/issued_under':
            return self._point(reference, self.resolve(reference, 'assignment')['use_scope'])
        return self._point(reference, selectors.get(path, assignment['use_scope']))

    def _subject_use(self, subject, assignment):
        matches = [self._assignment_use(assignment, path, ref) for path, ref in _reference_paths(assignment)
                   if path.startswith('/inputs/') and ref == subject]
        scopes = {point['use_scope'] for point in matches}
        if len(scopes) > 1:
            raise ERROR('P_PROOF', 'An assessed subject must have one exact assigned use')
        return matches[0] if matches else self._point(subject, assignment['use_scope'])

    def _inspection(self, assignment, path, reference, live):
        slots = {'reviewer': {'assessed-subject'}, 'integration_reviewer': {'assessed-subject'},
                 'measurement': {'measured-subject'}, 'receiver': {'incoming_handoff'}}
        parts = path.split('/')
        if len(parts) != 5 or parts[1] != 'inputs' or parts[3] != 'refs':
            return False
        binding = assignment['inputs'][int(parts[2])]
        if binding['slot_id'] not in slots.get(assignment['responsibility'], set()) or len(binding['refs']) != 1:
            return False
        value = self.versions[reference['version_id']]
        if value['kind'] != 'delivery.product':
            return False
        subject = value['content']['record']
        if subject['owner']['work_item'] != assignment['owner']['work_item']:
            return False
        distance = abs(subject['owner']['layer'] - assignment['owner']['layer'])
        if distance != (1 if assignment['responsibility'] == 'receiver' else 0):
            return False
        point = self._assignment_use(assignment, path, reference)
        return all(self._governing_input(parent, live)
                   for parent in self._governing_dependencies(point))

    def _dependency_point(self, record, path, ref):
        assignment = record if 'issued_under' in record else (
            self.resolve(record['assignment'], 'assignment') if record.get('assignment') is not None else None)
        if path.startswith('/assessed_closure/'):
            return copy.deepcopy(record['assessed_closure'][int(path.split('/')[2])])
        if assignment is record:
            return self._assignment_use(assignment, path, ref)
        if assignment is not None:
            if path == '/assignment':
                return self._point(ref, assignment['use_scope'])
            assigned_paths = dict(_causal_reference_paths(assignment))
            if path in assigned_paths and assigned_paths[path] == ref:
                return self._assignment_use(assignment, path, ref)
            matches = [self._assignment_use(assignment, at, bound) for at, bound in assigned_paths.items()
                       if bound == ref and at != '/issued_under']
            return matches[0] if len({item['use_scope'] for item in matches}) == 1 else self._point(ref, assignment['use_scope'])
        return self._point(ref)

    def _dependencies(self, record):
        points = []
        for path, ref in _causal_reference_paths(record):
            point = self._dependency_point(record, path, ref)
            if point not in points:
                points.append(point)
        return sorted(points, key=canonical)

    def _closure(self, reference, scope=None):
        point = self._point(reference, scope)
        key = self._key(point)
        memo = self._assessment_walk
        if memo is not None and key in memo['closures']:
            return copy.deepcopy(memo['closures'][key])
        result = self._walk_closure(point)
        if memo is not None:
            memo['closures'][key] = copy.deepcopy(result)
        return result

    def _walk_closure(self, reference):
        seen, active, result = set(), set(), []
        def visit(point):
            key = self._key(point)
            if key in active:
                raise ERROR('P_CONFLICT', 'Scoped causal dependency cycle')
            if key in seen:
                return
            active.add(key)
            for parent in self.reliance.get(key, []):
                visit(parent)
            active.remove(key)
            seen.add(key)
            value = self.versions.get(key[1])
            if value is None:
                raise ERROR('P_CONTEXT', 'Required immutable prerequisite is missing')
            result.append(self._point(self._reference(key[1]), key[0]))
        visit(reference)
        return result

    def _governing_dependencies(self, point):
        """Project exact scoped governing paths, separately from historical provenance."""
        record = self.resolve(point['ref'])
        family = self.versions[point['ref']['version_id']]['kind']
        assignment = record if family == 'delivery.assignment' else (
            self.resolve(record['assignment'], 'assignment') if record.get('assignment') else None)
        inspection_slots = {'reviewer': 'assessed-subject', 'integration_reviewer': 'assessed-subject',
                            'receiver': 'incoming_handoff', 'measurement': 'measured-subject'}
        points = []
        previous = self.scope
        self.scope = point['use_scope']
        try:
            for path, reference in _causal_reference_paths(record):
                keep = False
                if family == 'delivery.source':
                    keep = path.startswith('/inherited/')
                elif family == 'delivery.profile':
                    keep = path.startswith('/source_profiles/')
                elif family == 'delivery.assignment':
                    keep = path in {'/profile', '/criteria', '/routing/policy'} or path.startswith(('/inherited/', '/inputs/', '/effects/'))
                elif family == 'delivery.context':
                    keep = path in {'/assignment', '/profile', '/execution/selection', '/speculation'} or path.startswith('/inputs/')
                elif family == 'delivery.product':
                    keep = path == '/profile' or path.startswith(('/inputs/', '/evidence/', '/related/', '/outcome/evidence/'))
                    if record['product_kind'] == 'finding' and path.startswith('/related/'):
                        keep = record['related'][int(path.split('/')[2])]['slot_id'] != 'subject'
                elif family == 'delivery.assessment':
                    keep = path in {'/profile', '/criteria'} or path.startswith(('/conditions/', '/findings/'))
                elif family == 'delivery.decision':
                    # Decision dependencies were explicitly derived at its transition.
                    return list(self.reliance.get(self._key(point), []))
                parts = path.split('/')
                if (keep and assignment is not None and len(parts) == 5
                        and parts[1] == 'inputs' and parts[3] == 'refs'):
                    binding = assignment['inputs'][int(parts[2])]
                    if binding['slot_id'] == inspection_slots.get(assignment['responsibility']):
                        keep = False
                if keep:
                    candidate = self._dependency_point(record, path, reference)
                    if candidate not in points:
                        points.append(candidate)
            if family == 'delivery.assessment':
                reviewer = self._point(record['assignment'], assignment['use_scope'])
                subject = self._subject_use(record['subject'], assignment)
                for dependency in self._governing_dependencies(reviewer) + self._governing_dependencies(subject):
                    if dependency not in points:
                        points.append(dependency)
            for requirement in self._use_changes.get(self._key(point), {}).get('requirements', []):
                if requirement['point'] not in points:
                    points.append(requirement['point'])
            return points
        finally:
            self.scope = previous

    def _use_affected(self, roots):
        """Compute scoped governing-use loss without cancelling historical truth."""
        affected = {self._key(point) for point in roots}
        while True:
            prior = set(affected)
            for key in self.states:
                point = self._point(self._reference(key[1]), key[0])
                if any(self._key(parent) in affected for parent in self._governing_dependencies(point)):
                    affected.add(key)
            for key, selected in self.proofs.items():
                if self._key(selected['proof'], selected['proof_use_scope']) in affected:
                    affected.add(self._key(selected['subject'], key[0]))
            for event in self._effective_establishments():
                if self._key(event['decision_ref'], event.get('decision_scope', event['scope'])) in affected:
                    affected.add(self._key(event['subject'], event['use_scope']))
            if prior == affected:
                return [self._point(self._reference(identifier), scope) for scope, identifier in sorted(affected)]

    def _withdrawal(self, roots):
        return {'op': 'withdraw', 'subjects': self._use_affected(roots)}

    def _affected(self, roots):
        affected = {self._key(root) for root in roots}
        while True:
            prior = set(affected)
            for dependent, prerequisites in self.reliance.items():
                if {self._key(point) for point in prerequisites} & affected:
                    affected.add(dependent)
            for dependent, history in self._use_changes.items():
                if any(self._key(item['point']) in affected for item in history.get('requirements', [])):
                    affected.add(dependent)
            for key, selection in self.proofs.items():
                if self._key(selection['proof'], selection['proof_use_scope']) in affected:
                    affected.add(self._key(selection['subject'], key[0]))
                if self._key(selection['subject'], key[0]) in affected:
                    affected.add(self._key(selection['proof'], selection['proof_use_scope']))
            for event in self._effective_establishments():
                if self._key(event['decision_ref'], event.get('decision_scope', event['scope'])) in affected:
                    affected.add(self._key(event['subject'], event['use_scope']))
            if prior == affected:
                return [self._point(self._reference(identifier), scope) for scope, identifier in sorted(affected)]

    def _validation_bytes(self, identifier, live=True):
        """Read a first-use CAS reference, checking exact historical bytes once per cold replay."""
        if live:
            if self.blob_reader is None:
                raise ERROR('P_CONTEXT', 'Current validation material is unavailable')
            try:
                raw = self._material_bytes(identifier, self.blob_reader)
            except ERROR:
                raise
            except (OSError, ValueError) as error:
                raise ERROR('P_CONTEXT', 'Current validation material is unavailable') from error
        elif identifier in self.validation_assets:
            return self.validation_assets[identifier]
        else:
            if self.validation_replay_artifacts is None or identifier not in self.validation_replay_artifacts:
                raise ERROR('P_INTEGRITY', 'Required historical validation reference is undeclared')
            if self.blob_reader is None:
                raise ERROR('P_INTEGRITY', 'Required historical validation material is unavailable')
            try:
                raw = self._material_bytes(identifier, self.blob_reader)
            except ERROR:
                raise
            except (OSError, ValueError) as error:
                raise ERROR('P_INTEGRITY', 'Required historical validation material is unavailable') from error
        if identifier not in self.validation_assets:
            size = sum(len(self.validation_assets[key]) for key in self.validation_artifacts)
            if size + len(raw) > 32 * 1024 * 1024:
                raise ERROR('P_CONTEXT', 'Transaction validation assets exceed the bounded archive contract')
            self.validation_assets[identifier] = raw
            self.validation_artifacts.append(identifier)
            self.validation_artifacts.sort()
        return raw

    def _material(self, record, live):
        if not live:
            return
        for identifier in record.get('material', []):
            try:
                if self.blob_reader is None:
                    raise ValueError('identity')
                self._material_bytes(identifier, self.blob_reader)
            except (OSError, ValueError):
                raise ERROR('P_CONTEXT', 'Required exact material is unavailable') from None

    def _material_bytes(self, identifier, reader):
        memo = self._assessment_walk
        key = (id(reader), identifier)
        if memo is not None and key in memo['material']:
            return memo['material'][key][1]
        raw = reader(identifier)
        if blob(raw) != identifier:
            raise ERROR('P_INTEGRITY', 'Material differs from its exact identity')
        if memo is not None:
            # Keep the exact reader alive: an inline archive reader must never
            # satisfy a current CAS check, even if callable identities recycle.
            memo['material'][key] = (reader, raw)
        return raw

    def _profile(self, message):
        if message['message_type'] == 'bootstrap':
            return message['payload']['profile']['record']
        return self.resolve(message['profile'], 'profile')

    def policy_digest(self, message):
        """Return the exact active profile commitment used for a message preview."""
        return _hash(self._profile(message))

    def _current_origin(self, message, origin, at, live, authority=None):
        if origin != message['sender']:
            raise ERROR('P_ORIGIN', 'Dispatch origin differs from the claimed sender')
        if message['engagement'] != self.engagement:
            raise ERROR('P_SCOPE', 'Cross-engagement mutation denied')
        if message['message_type'] == 'control_event' and message['payload']['event'] == 'renew_control':
            if not self.initialized or origin['kind'] != 'controller' or message['context'] is not None:
                raise ERROR('P_SCOPE', 'Renewal requires the current local controller')
            prior = self.resolve(message['payload']['previous_context'], 'context')
            if prior['purpose'] != 'controller' or prior['issued_to'] != origin['id']:
                raise ERROR('P_SCOPE', 'Control renewal cannot transfer controller ownership')
            return None, None
        if message['message_type'] == 'bootstrap':
            if self.initialized or origin['kind'] != 'controller' or origin['id'] != message['payload']['controller_id']:
                raise ERROR('P_SCOPE', 'Only the configured controller may bootstrap an empty engagement')
            return None, None
        context = self.resolve(message['context'], 'context')
        if message['context']['engagement'] != message['engagement'] or message['context']['scope'] != message['scope'] or message['profile']['engagement'] != message['engagement']:
            raise ERROR('P_SCOPE', 'Origin context and governing scope must exactly match')
        if message['recipient']['kind'] == 'controller' and message['recipient'] != {'kind': 'controller', 'id': context['issued_to']} and context['purpose'] == 'controller':
            raise ERROR('P_SCOPE', 'Unknown controller recipient')
        if context['profile'] != message['profile']:
            raise ERROR('P_CONTEXT', 'Issued profile differs from the request')
        if origin['kind'] == 'assignment':
            if self._status(message['context'])['validity'] in {'invalid', 'revoked'}:
                raise ERROR('P_CONTEXT', 'Producer execution context no longer applies')
            if at >= context['expires_at_ms']:
                raise ERROR('P_EXPIRED', 'Issued execution context expired')
            if origin['ref']['engagement'] != message['engagement']:
                raise ERROR('P_SCOPE', 'Assignment scope differs from request')
            assignment = self.resolve(origin['ref'], 'assignment')
            if assignment['use_scope'] != message['scope']:
                raise ERROR('P_SCOPE', 'Assignment mandate does not authorize this use scope')
            recipient = message['recipient']
            if recipient['kind'] == 'assignment':
                target_owner = self.resolve(recipient['ref'], 'assignment')['owner']
                distance = abs(target_owner['layer'] - assignment['owner']['layer'])
                if distance > 1 or (distance == 1 and message['message_type'] not in {'handoff', 'handoff_acceptance', 'relay', 'change_request', 'information_request', 'information_response', 'escalation'}):
                    raise ERROR('P_SCOPE', 'Message route exceeds local or adjacent responsibility')
            elif recipient['kind'] != 'controller':
                raise ERROR('P_SCOPE', 'Leaf authority communication requires its mediated route')
            if context['assignment'] != origin['ref'] or context['issued_to'] != assignment['assigned_actor']:
                raise ERROR('P_CONTEXT', 'Issued context is not bound to this assignment')
            if not self._execution_right(origin['ref'], assignment, context, at, live):
                raise ERROR('P_STATE', 'Assignment is not open for new results')
            for bound_index, bound in enumerate(context['inputs']):
                for ref_index, ref in enumerate(bound['refs']):
                    self.resolve(ref)
                    point = self._assignment_use(assignment, '/inputs/' + str(bound_index) + '/refs/' + str(ref_index), ref)
                    if not self._governing_input(point, live) and not self._inspection(assignment, '/inputs/' + str(bound_index) + '/refs/' + str(ref_index), ref, live):
                        raise ERROR('P_CONTEXT', 'Issued required input lost applicability')
            if self.run_states.get(context['run_id']) != 'running':
                raise ERROR('P_STATE', 'Issued run is not currently running')
            return assignment, context
        if origin['kind'] == 'controller':
            if context['purpose'] != 'controller' or context['issued_to'] != origin['id']:
                raise ERROR('P_ORIGIN', 'Controller context mismatch')
            return None, context
        # Control-plane contexts are audit bindings. Current authority comes
        # from external purpose proofs; typed target guards enforce semantics.
        if origin['kind'] == 'authority' and context['purpose'] == 'controller':
            return None, context
        raise ERROR('P_SCOPE', 'No entitled assignment or controller context')

    def _content_policy_admission(self, logical_id, record, profile, live):
        selector = profile['content_profile']
        if selector is None or logical_id != selector['logical_id']:
            return None
        if (record.get('source_role') != 'policy' or record['owner'].get('kind') != 'authority'
                or record['origin'] != record['owner'] or len(record['material']) != 1):
            raise ERROR('P_CONTEXT', 'The new content policy must be one attributable exact source')
        import governed_sabsa
        raw = self._validation_bytes(record['material'][0], live)
        value = loads(raw)
        if canonical(value) != raw:
            raise ERROR('P_PARSE', 'Content policy admission requires canonical semantic JSON')
        return governed_sabsa.validate_profile(value)

    def _registration(self, message, origin, assignment, record_type, logical_id, record, live, procedure=None):
        value = record_manifest(message['engagement'], message['scope'], logical_id, record_type, record)
        identifier = version_id(value)
        owner = record['owner']
        content = None
        if identifier in self.versions:
            raise ERROR('P_CONFLICT', 'Record already exists; use its exact immutable reference')
        for reference in _references(record):
            self.resolve(reference)
        if record_type in {'profile', 'context'}:
            if origin['kind'] != 'controller':
                raise ERROR('P_SCOPE', 'Only trusted control may register profiles or issued contexts')
            if record_type == 'profile':
                raise ERROR('P_SCOPE', 'An engagement profile is fixed by bootstrap; changed profiles require a new engagement')
        elif record_type == 'assignment':
            if procedure is None and origin['kind'] == 'controller' and record['responsibility'] != 'setter' and not (
                    record['owner']['layer'] > 1 and record['responsibility'] == 'receiver'):
                raise ERROR('P_SCOPE', 'The actual entitled setter must register non-setter assignments')
            self._assignment_mandate(message, origin, assignment, record, live, logical_id, procedure)
            if record.get('handling') is None and self._blocking_episodes(_ref(value), record):
                raise ERROR('P_STATE', 'An open episode blocks new productive mandates')
            prospective = self
            dependencies = self._dependencies(record)
            if any(self._key(point) not in self.states for point in dependencies):
                prospective = self._fork()
                for point in dependencies:
                    prospective._ensure_use(point)
            prospective._assignment_requirements(record, live)
            self.validation_assets = prospective.validation_assets
            self.validation_artifacts = prospective.validation_artifacts
            if record['deadline_ms'] is not None and record['deadline_ms'] <= message['issued_at_ms']:
                raise ERROR('P_BUDGET', 'Finite assignment allowance and deadline required')
        elif record_type == 'source':
            if owner.get('kind') == 'authority':
                if origin != owner and origin['kind'] != 'controller':
                    raise ERROR('P_SCOPE', 'Authority-owned input requires its genuine owner')
            elif not assignment or assignment['owner'] != owner or assignment['responsibility'] != 'setter':
                raise ERROR('P_SCOPE', 'Source requires its exact semantic owner')
        elif record_type == 'product':
            if not assignment or record['assignment'] != (procedure['assignment'] if procedure is not None else message['sender'].get('ref')) or assignment['owner'] != owner:
                raise ERROR('P_SCOPE', 'Product owner and assigned producer must agree')
            expected = {'observation': {'measurement'}, 'answer': {'author'},
                        'bundle': {'integrator'}, 'handoff': {'integrator', 'setter'},
                        'escalation': {'integrator'}, 'final_result': {'integrator'}, 'finding': {'reviewer', 'integration_reviewer', 'receiver'}}
            if assignment['responsibility'] not in expected[record['product_kind']]:
                raise ERROR('P_SCOPE', 'Assignment cannot produce this kind of result')
            if record['profile'] != assignment['profile'] or record['inputs'] != assignment['inputs']:
                raise ERROR('P_CONTEXT', 'Product differs from its exact input assignment')
            if self.resolve(record['profile'], 'profile')['content_profile'] is not None:
                import governed_sabsa
                content = governed_sabsa.validate_product(self, record, message['scope'], live)
            if record['product_kind'] == 'finding':
                self._finding(record, assignment)
            if record['product_kind'] == 'bundle':
                self._product_requirements(record, live)
            if record['product_kind'] == 'final_result':
                self._terminal_requirements(record, message['issued_at_ms'])
        elif record_type == 'assessment':
            if not assignment or record['assignment'] != (procedure['assignment'] if procedure is not None else message['sender'].get('ref')) or assignment['owner'] != owner:
                raise ERROR('P_SCOPE', 'Assessment requires its assigned owner')
            self._assessment(record, assignment, live, context_ref=message['context'])
        if record_type == 'context':
            if record['assignment'] is None:
                raise ERROR('P_SCOPE', 'Only bootstrap may create a controller context')
            target = self.resolve(record['assignment'], 'assignment')
            if (not self._execution_right(record['assignment'], target, record, message['issued_at_ms'], live)
                    or self._status(record['assignment'], target['use_scope'])['validity'] != 'valid'
                    or record['expires_at_ms'] <= message['issued_at_ms']):
                raise ERROR('P_STATE', 'Only a current open mandate may receive a fresh execution lease')
            self._assignment_requirements(target, live)
            if record['execution'] is None:
                raise ERROR('P_CONTEXT', 'An entity context requires an explicit execution phase')
            if record['execution']['phase'] == 'work':
                self._reviewer_support(target, live)
                selection = record['execution']['selection']
                self._context_execution(record, live)
                if self.execution_plans.get((record['assignment']['version_id'], target['use_scope'])) != selection:
                    raise ERROR('P_CONFLICT', 'New work leases require the exact current execution plan')
            if not self._current_inputs(target, live):
                raise ERROR('P_CONTEXT', 'A superseded governing input requires an owner-directed current assignment')
            if (record['owner'] != target['owner'] or record['issued_to'] != target['assigned_actor']
                    or record['purpose'] != target['responsibility'] or record['profile'] != target['profile']
                    or record['inputs'] != target['inputs'] or record['effects'] != target['effects']
                    or target['deadline_ms'] is not None and record['expires_at_ms'] > target['deadline_ms']):
                raise ERROR('P_CONTEXT', 'Context must exactly instantiate authorized assignment grants')
            if record['run_id'] in self.run_states:
                raise ERROR('P_IDEMPOTENCY', 'Issued run identity already exists')
            if record['ready_basis'] != self.ready_basis(record['assignment'], message['issued_at_ms']):
                raise ERROR('P_CONTEXT', 'Context must bind the exact ready facts delivered for this run')
            allowance = self._execution_allowance(record['assignment'], message['issued_at_ms'])
            if record['expires_at_ms'] - message['issued_at_ms'] > self.local_budget_status(record['assignment'], message['issued_at_ms'])['remaining_ms']:
                raise ERROR('P_BUDGET', 'A finite grant cannot exceed its current local iteration allowance')
            for bound in allowance:
                if bound['metric'] == 'elapsed_ms' and bound['unit'] == 'ms':
                    bound['ceiling'] = min(bound['ceiling'], record['expires_at_ms'] - message['issued_at_ms'])
            if record['speculation'] is not None:
                grant = self._grant_right(record['assignment'], target, record['speculation'], message['issued_at_ms'], live)
                for limit in allowance:
                    ceiling = next((item['ceiling'] for item in grant['limits'] if item['metric'] == limit['metric'] and item['unit'] == limit['unit']), 0)
                    used = reserved = 0
                    for details in self.run_details.values():
                        if self.resolve(details['context'], 'context')['speculation'] != record['speculation']:
                            continue
                        key = limit['metric'] + ':' + limit['unit']
                        spent = details['usage'].get(key, 0)
                        used += spent
                        if not details['reservation_released']:
                            bound = next((item['ceiling'] for item in details['limits'] if item['metric'] == limit['metric'] and item['unit'] == limit['unit']), 0)
                            reserved += max(0, bound - spent)
                    limit['ceiling'] = min(limit['ceiling'], ceiling - used - reserved)
                    if limit['ceiling'] <= 0:
                        raise ERROR('P_BUDGET', 'Shared speculative allowance is exhausted or already reserved')
        self._material(record, live)
        use_scope = record['use_scope'] if record_type == 'assignment' else message['scope']
        effects = [{'op': 'register', 'manifest': value, 'dependencies': self._dependencies(record), 'use_scope': use_scope,
                    'origin': origin, 'context': message['context']}]
        if record_type == 'product':
            effects[0]['semantic_content'] = content
        elif record_type == 'source':
            policy = self._content_policy_admission(logical_id, record, self._profile(message), live)
            if policy is not None:
                effects[0]['content_policy'] = policy
        if record_type == 'assignment':
            import governed_local_budget
            effects.append({'op': 'assignment', 'subject': identifier, 'state': 'open'})
            effects.append(governed_local_budget._bind(self, _ref(value), record))
        if record_type == 'context':
            effects.append({'op': 'run', 'run_id': record['run_id'], 'state': 'issued', 'context': _ref(value), 'issued_at_ms': message['issued_at_ms'], 'limits': allowance,
                            'local_unit_id': self.local_budget_status(record['assignment'], message['issued_at_ms'])['unit_id']})
        if assignment is not None and assignment.get('handling') is not None:
            if record_type == 'product' and record['product_kind'] not in {'finding', 'escalation'}:
                raise ERROR('P_SCOPE', 'Handling work cannot manufacture a productive result')
            if record_type == 'assignment' and record.get('handling') != assignment['handling']:
                raise ERROR('P_SCOPE', 'Local handling children must retain the exact episode relationship')
        if record_type == 'product' and record['product_kind'] == 'finding':
            effects.append({'op': 'qualify', 'subject': identifier, 'use_scope': use_scope})
        if record_type == 'profile':
            self._validate_profile(record)
        if record_type in {'profile', 'context', 'assignment'} or (record_type == 'source' and owner.get('kind') != 'authority'):
            effects.append({'op': 'qualify', 'subject': identifier, 'use_scope': use_scope})
        return effects, _ref(value)

    def _assessment(self, record, assignment, live, context_ref=None):
        subject = self.resolve(record['subject'])
        subject_use = self._subject_use(record['subject'], assignment)
        subject_paths = [path for path, ref in _reference_paths(assignment) if ref == record['subject'] and self._inspection(assignment, path, ref, live)]
        if self._status(subject_use)['validity'] in {'invalid', 'revoked'} and not subject_paths:
            raise ERROR('P_PROOF', 'Cancelled subject cannot acquire a current review')
        origin = self.provenance.get(record['subject']['version_id'], {})
        subject_assignment = subject.get('assignment')
        author = self.resolve(subject_assignment, 'assignment') if subject_assignment else None
        expected = {'professional': 'reviewer', 'integration': 'integration_reviewer', 'receiving': 'receiver'}
        if assignment['responsibility'] != expected[record['assessment_kind']]:
            raise ERROR('P_PROOF', 'Wrong assessment assignment responsibility')
        if author and author['assigned_actor'] == assignment['assigned_actor']:
            raise ERROR('P_PROOF', 'Producer cannot provide its independent review')
        if author and context_ref is not None and origin.get('context') is not None:
            author_run = self.resolve(origin['context'], 'context')['run_id']
            reviewer_run = self.resolve(context_ref, 'context')['run_id']
            author_native = self.run_details.get(author_run, {}).get('native')
            reviewer_native = self.run_details.get(reviewer_run, {}).get('native')
            if (author_native is not None and reviewer_native is not None
                    and all(author_native[field] == reviewer_native[field] for field in ('provider', 'handle'))):
                raise ERROR('P_PROOF', 'Producer and reviewer require distinct actual physical contexts')
        if record['assessment_kind'] == 'integration':
            answers = next((item['refs'] for item in subject['related'] if item['slot_id'] == 'answers'), [])
            for reference in answers:
                answer = self.resolve(reference, 'product')
                producer = self.resolve(answer['assignment'], 'assignment')
                if producer['assigned_actor'] == assignment['assigned_actor']:
                    raise ERROR('P_PROOF', 'Integration reviewer must be independent of every answer producer')
        subject_owner = subject['owner']
        if record['assessment_kind'] != 'receiving' and subject_owner != record['owner']:
            raise ERROR('P_PROOF', 'Professional review must match exact layer and work ownership')
        if record['assessment_kind'] == 'receiving' and abs(subject_owner['layer'] - record['owner']['layer']) != 1:
            raise ERROR('P_SCOPE', 'Receiving acceptance must cross one adjacent interface')
        if record['criteria'] != assignment['criteria'] or record['profile'] != assignment['profile']:
            raise ERROR('P_PROOF', 'Review criteria or profile changed')
        closure = self.assessment_closure(record['subject'], record['assignment'])
        if record['assessed_closure'] != closure or record['assessed_hash'] != _hash(closure):
            raise ERROR('P_PROOF', 'Assessment does not bind the exact current prerequisite closure')
        for parent in self._governing_dependencies(subject_use):
            if not self._governing_input(parent, live):
                raise ERROR('P_PROOF', 'Reviewed subject has a withdrawn direct governing input')
        self._material(subject, live)

    def _complete(self, message, assignment, context):
        if assignment is None or context is None:
            raise ERROR('P_SCOPE', 'Assigned producer execution required')
        return [{'op': 'assignment', 'subject': message['sender']['ref']['version_id'], 'state': 'completed'},
                {'op': 'run', 'run_id': context['run_id'], 'state': 'returned'}]

    def _delivery_origin(self, reference, message, context):
        provenance = self.provenance.get(reference['version_id'])
        if (not provenance or provenance['origin'] != message['sender']
                or provenance['context'] != message['context']):
            raise ERROR('P_ORIGIN', 'Returned record differs from its actual registered execution')

    @_within_assessment
    def derive(self, message, origin, assessed_at_ms, authority=None, live=True, _returned=False):
        """Independently derive exact effects, without persisting or granting authority.

        Args:
            message: Strict schema-valid message with verified content identity.
            origin: Runtime controller or the producer of the actual issued return.
            assessed_at_ms: Trusted assessment instant.
            authority: Independently verified human-proof description, when required.
            live: Check material availability for fresh operations, not obsolete history.
            _returned: Internal RunReturn interpretation marker; it grants no
                authenticated provenance or permission to persist effects.
        Returns:
            Complete deterministic internal effects.
        Raises:
            ProtocolError: Any ownership, prerequisite, state or budget guard fails.
        """
        self.scope = message['scope']
        profile = self._profile(message)
        if not _returned and message['sender']['kind'] == 'assignment':
            raise ERROR('P_ORIGIN', 'Entity output must arrive as its captured issued RunReturn')
        at = assessed_at_ms
        self.assessed_at_ms = at
        if not message['issued_at_ms'] < message['expires_at_ms'] or not message['issued_at_ms'] - profile['max_clock_skew_ms'] <= at < message['expires_at_ms']:
            raise ERROR('P_EXPIRED', 'Request outside its trusted finite time window')
        if message['expires_at_ms'] - message['issued_at_ms'] > profile['max_request_duration_ms']:
            raise ERROR('P_EXPIRED', 'Request exceeds governing maximum duration')
        assignment, context = self._current_origin(message, origin, at, live, authority)
        if message['expected_head'] != self.head:
            raise ERROR('P_HEAD', 'Engagement head changed; no partial application')
        kind, payload = message['message_type'], message['payload']
        if (assignment is not None and context['execution']['phase'] == 'selection'
                and (kind != 'decision' or payload.get('action') != 'select_execution')):
            raise ERROR('P_SCOPE', 'The selection phase cannot produce domain effects')
        effects = []
        if kind == 'control_event':
            return self._control(message, origin, at, live)
        if kind == 'bootstrap':
            self._validate_profile(profile)
            _bootstrap_scopes(message)
            logicals = [payload['profile']['logical_id']] + [item['logical_id'] for item in payload['l0_inputs']]
            if len(logicals) != len(set(logicals)):
                raise ERROR('P_CONFLICT', 'Bootstrap logical identities collide')
            values = []
            for item in payload['l0_inputs']:
                if item['record']['owner'].get('kind') != 'authority' or item['record']['origin'] != item['record']['owner']:
                    raise ERROR('P_SCOPE', 'Bootstrap must preserve attributable L0 input ownership')
                self._material(item['record'], live)
                values.append(record_manifest(message['engagement'], message['scope'], item['logical_id'], 'source', item['record']))
            profile_value = record_manifest(message['engagement'], message['scope'], payload['profile']['logical_id'], 'profile', profile)
            values.append(profile_value)
            context_body = {'owner': origin, 'assignment': None, 'profile': _ref(profile_value),
                            'purpose': 'controller', 'run_id': 'bootstrap:' + message['request_id'],
                            'issued_to': origin['id'], 'inputs': [{'slot_id': 'l0', 'refs': [_ref(value) for value in values[:-1]]}],
                            'speculation': None, 'ready_basis': [],
                            'attachments': [], 'effects': [], 'execution': None,
                            'expires_at_ms': at + profile['max_request_duration_ms']}
            values.append(record_manifest(message['engagement'], message['scope'], 'controller-context:' + message['scope'], 'context', context_body))
            for value in values:
                registration = {'op': 'register', 'manifest': value, 'dependencies': self._dependencies(value['content']['record']),
                                'origin': origin, 'context': None}
                if value['kind'] == 'delivery.source':
                    policy = self._content_policy_admission(value['logical_id'], value['content']['record'], profile, live)
                    if policy is not None:
                        registration['content_policy'] = policy
                effects.extend([registration, {'op': 'qualify', 'subject': version_id(value)}])
            for value in values[:-2]:
                for scope in payload['use_scopes']:
                    effects.append({'op': 'bootstrap-use', 'point': self._point(_ref(value), scope)})
                    effects.append({'op': 'initial-source', 'source': _ref(value), 'use_scope': scope})
            for scope in payload['use_scopes']:
                effects.append({'op': 'bootstrap-use', 'point': self._point(_ref(profile_value), scope)})
            effects.append({'op': 'initialize'})
        elif kind == 'record_proposal':
            effects, ref = self._registration(message, origin, assignment, payload['record_type'], payload['logical_id'], payload['record'], live)
        elif kind == 'assignment':
            target = self.resolve(payload['assignment'], 'assignment')
            flat = _input_locators(target['inputs'])
            if any(payload[key] != target[key] for key in ('owner', 'responsibility', 'criteria')) or payload['inputs'] != flat:
                raise ERROR('P_CONTEXT', 'Delivery differs from its stored assignment')
            if origin['kind'] != 'controller' and (not assignment or assignment['responsibility'] != 'setter' or target['issued_under'] != message['sender']['ref']):
                raise ERROR('P_SCOPE', 'Only the exact issuing setter may deliver the stored mandate')
            effects.append({'op': 'event', 'kind': kind, 'payload': payload})
        elif kind in {'submission', 'observation', 'review', 'handoff', 'handoff_acceptance', 'escalation'}:
            field = {'submission': 'candidate', 'observation': 'observation', 'review': 'assessment',
                     'handoff': 'handoff', 'handoff_acceptance': 'assessment', 'escalation': 'package'}[kind]
            reference = payload[field]
            record = self.resolve(reference, 'assessment' if kind in {'review', 'handoff_acceptance'} else 'product')
            if assignment is None or record['owner'] != assignment['owner']:
                raise ERROR('P_SCOPE', 'Result does not belong to this assigned work')
            self._delivery_origin(reference, message, context)
            if record['assignment'] != message['sender'].get('ref'):
                raise ERROR('P_SCOPE', 'Result belongs to a different assignment')
            match = {'submission': ['evidence', 'limitations'], 'observation': ['material'],
                     'review': ['subject', 'criteria', 'verdict', 'findings', 'conditions'],
                     'handoff_acceptance': ['verdict', 'findings'], 'handoff': [], 'escalation': []}[kind]
            if any(payload[key] != record[key] for key in match):
                raise ERROR('P_CONTEXT', 'Wire fields cannot replace the stored result')
            if kind == 'observation':
                if payload['inputs'] != _input_locators(record['inputs']):
                    raise ERROR('P_CONTEXT', 'Observation input delivery mismatch')
                requires_review = any(item['owner'] == record['owner'] and item['role'] == 'professional_review' and item['subject_kind'] == 'observation'
                                      for item in self.resolve(record['profile'], 'profile')['obligations'])
                observation_supports = self._product_requirements(record, live)
                effects.append({'op': 'qualify', 'subject': reference['version_id'], 'applicable': not requires_review,
                                'requirements': observation_supports})
            elif kind in {'review', 'handoff_acceptance'}:
                self._assessment(record, assignment, live)
                effects.append({'op': 'qualify', 'subject': reference['version_id']})
            else:
                for ref in record['evidence']:
                    self.resolve(ref)
                    if self._status(ref)['validity'] != 'valid':
                        raise ERROR('P_PROOF', 'Required current evidence is not qualified')
                if kind == 'submission':
                    self._assignment_requirements(assignment, live)
            if kind == 'handoff':
                related = {item['slot_id']: item['refs'] for item in record['related']}
                if related.get('bundle') != [payload['bundle']] or related.get('interface') != [payload['interface']]:
                    raise ERROR('P_CONTEXT', 'Handoff differs from its fixed bundle and interface')
            if kind == 'handoff_acceptance' and record['subject'] != payload['handoff']:
                raise ERROR('P_PROOF', 'Receiving assessment names another handoff')
            if kind == 'escalation':
                effects.extend(self._derive_escalation(reference, record, payload, assignment, message, at))
                effects.append({'op': 'event', 'kind': 'escalation', 'payload': payload, 'semantic_message': message})
            if kind != 'escalation':
                effects.append({'op': 'event', 'kind': kind, 'payload': payload, 'semantic_message': message})
            if not _returned:
                effects.extend(self._complete(message, assignment, context))
        elif kind == 'decision':
            effects.extend(self._decision(message, origin, assignment, authority, live))
        elif kind == 'integration':
            bundle = self.resolve(payload['bundle'], 'product')
            assessment = self.resolve(payload['integration_review'], 'assessment')
            if (bundle['product_kind'] != 'bundle' or assessment['assessment_kind'] != 'integration'
                    or assessment['subject'] != payload['bundle'] or assessment['verdict'] not in {'supported', 'supported_with_conditions'}
                    or self._status(payload['integration_review'])['validity'] != 'valid'):
                raise ERROR('P_PROOF', 'Exact independently qualified integration assessment required')
            if not assignment or assignment['owner'] != bundle['owner']:
                raise ERROR('P_SCOPE', 'Integration control is outside this assignment')
            related = {item['slot_id']: item['refs'] for item in bundle['related']}
            if related.get('answers') != payload['answers']:
                raise ERROR('P_CONTEXT', 'Integration answers differ from recorded bundle')
            self._complete_bundle(bundle, live)
            effects.append({'op': 'qualify', 'subject': payload['bundle']['version_id']})
        elif kind in {'information_request', 'information_response', 'change_request', 'relay'}:
            for reference in _references(payload):
                self.resolve(reference)
            if kind == 'relay':
                original = self.messages.get(payload['original_message'])
                if original is None or original['sender'] != payload['original_origin']:
                    raise ERROR('P_SCOPE', 'Relay cannot rewrite original provenance')
                route = self.resolve(payload['route'], 'source')
                if not assignment:
                    raise ERROR('P_SCOPE', 'Relay requires an assigned adjacent route')
                previous = original['sender']
                if previous['kind'] == 'assignment':
                    owner = self.resolve(previous['ref'], 'assignment')['owner']
                    if abs(owner['layer'] - assignment['owner']['layer']) != 1:
                        raise ERROR('P_SCOPE', 'Relay skips a layer')
            event_payload = payload
            if kind == 'relay':
                if assignment.get('handling', {}).get('task') != 'relay':
                    raise ERROR('P_SCOPE', 'Adjacent escalation relay requires its exact typed handling mandate')
                episode = self._episode(assignment['handling']['episode'])
                if original['message_type'] == 'escalation':
                    if self._episode(original['payload']['package'])['root'] != episode['root']:
                        raise ERROR('P_SCOPE', 'Relay cannot substitute another escalation episode')
                elif original['message_type'] != 'relay' or not any(event['kind'] == 'relay' and event.get('message_id') == original['message_id'] and event['payload'].get('episode') == episode['root'] for event in self.events):
                    raise ERROR('P_SCOPE', 'Relay must faithfully extend the recorded adjacent chain')
                sender_layer = assignment['owner']['layer']
                if message['recipient']['kind'] == 'assignment' and self.resolve(message['recipient']['ref'], 'assignment')['owner']['layer'] != sender_layer - 1:
                    raise ERROR('P_SCOPE', 'Escalations relay upward exactly one layer')
                event_payload = {**payload, 'episode': episode['root'], 'package': assignment['handling']['package'], 'from_layer': sender_layer, 'to_layer': sender_layer - 1}
            effects.append({'op': 'event', 'kind': kind, 'payload': event_payload, 'semantic_message': message})
        else:
            raise ERROR('P_SCHEMA', 'Unsupported typed operation')
        return effects

    def _child_owner(self, setter, child, profile):
        target = child['owner']
        if setter == target:
            return True
        if setter['layer'] != target['layer'] or setter['work_item'] != target['work_item']:
            return False
        if child['responsibility'] == 'setter':
            return (setter['work_kind'] in {'integration', 'handoff'}
                    and any(item['owner'] == setter and item['role'] in {'integration_review', 'receiving_acceptance'} for item in profile['obligations'])
                    and any(item['owner'] == target for item in profile['obligations']))
        if child['responsibility'] == 'measurement' and target['work_kind'] == 'measurement' and target['question'] is None:
            bindings = [item for item in child['inputs'] if item['slot_id'] == 'measured-subject']
            if len(bindings) != 1 or len(bindings[0]['refs']) != 1:
                return False
            subject = self.resolve(bindings[0]['refs'][0])
            return subject['owner'].get('layer') == setter['layer'] and subject['owner'].get('work_item') == setter['work_item']
        return False

    def _root_basis(self, record, scope):
        policy_use = self.capability_policy(record['profile'])
        current = [reference for (selected_scope, _), reference in self.sources.items()
                   if selected_scope == scope and self.resolve(reference, 'source')['source_role'] != 'policy']
        current.append(policy_use['ref'])
        content_use = self.content_policy(record['profile'])
        if content_use is not None and content_use['ref'] not in current:
            current.append(content_use['ref'])
        bindings = [binding for binding in record['inputs'] if binding['slot_id'] != 'root_reinstatement']
        flat = [ref for binding in bindings for ref in binding['refs']]
        profile = self.resolve(record['profile'], 'profile')
        criteria = [ref for ref in current if self.resolve(ref, 'source')['source_role'] == 'criteria']
        if (record['issued_under'] is not None or record['responsibility'] != 'setter'
                or record['owner']['layer'] != 1 or record['use_scope'] != scope
                or not any(item['owner'] == record['owner'] for item in profile['obligations'])
                or len(criteria) != 1 or record['criteria'] != criteria[0]
                or sorted(map(_hash, flat)) != sorted(map(_hash, current))
                or sorted(map(_hash, record['inherited'])) != sorted(map(_hash, current))):
            raise ERROR('P_SCOPE', 'Root requires the exact current attributable L0 mandate and bootstrap profile')
        paths = dict(_causal_reference_paths(record))
        if any(item['use_scope'] != (policy_use['use_scope'] if paths[item['at']] == policy_use['ref'] else content_use['use_scope'] if content_use is not None and paths[item['at']] == content_use['ref'] else scope)
               for item in record['input_uses']):
            raise ERROR('P_SCOPE', 'Root input versions must retain their exact domain and global capability uses')
        for reference in current:
            source = self.resolve(reference, 'source')
            use_scope = policy_use['use_scope'] if reference == policy_use['ref'] else content_use['use_scope'] if content_use is not None and reference == content_use['ref'] else scope
            if source['owner'].get('kind') != 'authority' or source['origin'] != source['owner'] or self._status(reference, use_scope)['validity'] != 'valid':
                raise ERROR('P_SCOPE', 'Root requires current attributable L0 inputs')

    def _root_key(self, record):
        return _hash({'scope': record['use_scope'], 'owner': record['owner'], 'profile': record['profile'],
                      'capabilities': self._assignment_use(record, '/routing/policy', record['routing']['policy']),
                      'criteria': self._assignment_use(record, '/criteria', record['criteria']),
                      'inherited': sorted((self._assignment_use(record, '/inherited/' + str(index), ref)
                                           for index, ref in enumerate(record['inherited'])), key=canonical)})

    def _root_versions(self, record):
        key = self._root_key(record)
        return [(identifier, value['content']['record']) for identifier, value in self.versions.items()
                if value['kind'] == 'delivery.assignment' and value['content']['record']['issued_under'] is None
                and self._root_key(value['content']['record']) == key]

    def _generation(self, reference):
        seen = set()
        while reference is not None:
            if reference['version_id'] in seen:
                raise ERROR('P_CONFLICT', 'Issuing mandate lineage is cyclic')
            seen.add(reference['version_id'])
            record = self.resolve(reference, 'assignment')
            if record['issued_under'] is None:
                if record.get('handling') is not None:
                    return _hash({'episode': record['handling']['episode'], 'layer': record['owner']['layer']}), record
                return self._root_key(record), record
            reference = record['issued_under']
        raise ERROR('P_CONTEXT', 'Assignment has no attributable root generation')

    def _execution_allowance(self, reference, at_ms=None):
        record = self.resolve(reference, 'assignment')
        generation, root = self._generation(reference)
        details_by_task, details_by_generation = [], []
        for details in self.run_details.values():
            assigned = self.resolve(details['context'], 'context')['assignment']
            if assigned == reference:
                details_by_task.append(details)
            if self._generation(assigned)[0] == generation:
                details_by_generation.append(details)
        result = []
        local = self.local_budget_status(reference, at_ms)
        effective = record['limits'] or root['limits'] or [{'metric': 'elapsed_ms', 'unit': 'ms',
            'ceiling': local['remaining_ms']}]
        for limit in effective:
            def remaining(ceiling, details):
                key = limit['metric'] + ':' + limit['unit']
                spent = sum(item['usage'].get(key, 0) for item in details)
                reserved = sum(next((bound['ceiling'] for bound in item['limits'] if bound['metric'] == limit['metric'] and bound['unit'] == limit['unit']), 0)
                               for item in details if not item['reservation_released'])
                return ceiling - spent - reserved
            details_by_generation = list({item.get('invocation_id', item['context']['version_id']): item for item in details_by_generation}.values())
            caps = [bound['ceiling'] for bound in root['limits'] if bound['metric'] == limit['metric'] and bound['unit'] == limit['unit']]
            allowance = remaining(limit['ceiling'], details_by_task) if record['limits'] else limit['ceiling']
            if caps:
                allowance = min(allowance, remaining(min(caps), details_by_generation))
            if limit['metric'] == 'elapsed_ms' and limit['unit'] == 'ms':
                allowance = min(allowance, local['remaining_ms'])
            if allowance <= 0:
                raise ERROR('P_BUDGET', 'Cumulative task or delegated root-generation allowance is exhausted')
            result.append({**limit, 'ceiling': allowance})
        return result

    def _restore_assignment(self, reference, record, assignment, authority, proofs, live):
        if proofs or self._status(reference, record['use_scope'])['validity'] not in {'invalid', 'revoked'}:
            raise ERROR('P_STATE', 'Mandate restoration requires a cancelled use and its type-specific basis')
        if record['use_scope'] != self.scope:
            raise ERROR('P_SCOPE', 'Mandate restoration cannot remap its scope')
        if record['issued_under'] is None:
            if not authority or authority['purpose'] != 'delivery-change':
                raise ERROR('P_SCOPE', 'Deterministic root restoration requires exact human authorization')
            self._root_basis(record, self.scope)
            latest = max(self._root_versions(record), key=lambda item: self.provenance[item[0]]['sequence'])
            if latest[0] != reference['version_id']:
                raise ERROR('P_STATE', 'Only the latest exact root generation instance may be restored')
        else:
            self._owned_decision(record, assignment, None)
            parent = self.resolve(record['issued_under'], 'assignment')
            if self._status(record['issued_under'], parent['use_scope'])['validity'] != 'valid':
                raise ERROR('P_CONTEXT', 'Original issuing mandate must currently apply')
        self._assignment_requirements(record, live)
        if any(point != self._point(reference) and not self._governing_input(point, live) for point in self._closure(reference)):
            raise ERROR('P_CONTEXT', 'All original mandate prerequisites must currently apply')

    def _assignment_mandate(self, message, origin, parent, record, live, logical_id, procedure=None):
        paths = dict(_causal_reference_paths(record))
        selectors = record['input_uses']
        if len({item['at'] for item in selectors}) != len(selectors) or any(
                item['at'] not in paths or item['at'] == '/issued_under' for item in selectors):
            raise ERROR('P_CONTEXT', 'Input-use selectors must uniquely identify causal reference occurrences')
        target = record['use_scope']
        if target not in {scope for scope, _ in self.sources}:
            raise ERROR('P_SCOPE', 'An assignment cannot create an unapproved semantic scope')
        if origin['kind'] == 'controller' and procedure is None:
            if record.get('handling') is not None:
                episode = self._episode(record['handling']['episode'])
                if record['handling']['task'] in {'relay', 'resolve'} and not episode['decisive'] and message['issued_at_ms'] < episode['collect_until_ms']:
                    raise ERROR('P_STATE', 'Collection closes at its finite window or an explicit decisive blocker')
                expected = self.handling_entry(record['handling']['episode'], record['handling']['task'], record['owner']['layer'], live=live)
                if logical_id != expected['logical_id'] or canonical(record) != canonical(expected['record']):
                    raise ERROR('P_SCOPE', 'Handling entry is mechanically bound to its exact episode and current owner mandate')
                return
            if record['owner']['layer'] > 1:
                bindings = {item['slot_id']: item['refs'] for item in record['inputs']}
                if len(bindings.get('incoming_handoff', [])) != 1:
                    raise ERROR('P_SCOPE', 'A local adjacent entry requires an exact offered handoff')
                handoff = bindings['incoming_handoff'][0]
                points = [self._assignment_use(record, path, ref) for path, ref in _reference_paths(record)
                          if path.startswith('/inputs/') and ref == handoff]
                if len({canonical(point) for point in points}) != 1:
                    raise ERROR('P_SCOPE', 'Incoming interface use must be unambiguous')
                acceptance = bindings.get('incoming_acceptance', [None])
                if len(acceptance) != 1:
                    raise ERROR('P_SCOPE', 'A coordinating entry requires one actual acceptance')
                expected = self.local_entry(points[0], record['responsibility'], acceptance[0], live)
                if logical_id != expected['logical_id'] or canonical(record) != canonical(expected['record']):
                    raise ERROR('P_SCOPE', 'External work addresses a layer, not its internal staff or method')
                return
            self._root_basis(record, message['scope'])
            previous = self._root_versions(record)
            receipts = [binding for binding in record['inputs'] if binding['slot_id'] == 'root_reinstatement']
            if not previous:
                if receipts:
                    raise ERROR('P_SCOPE', 'Initial root cannot claim a restoration receipt')
            else:
                identifier, prior = max(previous, key=lambda item: self.provenance[item[0]]['sequence'])
                if len(receipts) != 1 or len(receipts[0]['refs']) != 1 or self.assignment_states.get(identifier) not in {'cancelled', 'completed'} or self._status(self._reference(identifier), target)['validity'] != 'valid':
                    raise ERROR('P_STATE', 'Same-generation root requires explicit restoration of the latest terminal mandate')
                receipt = receipts[0]['refs'][0]
                decision = self.resolve(receipt)
                value = self.versions[receipt['version_id']]
                restored = decision.get('message', {})
                if (value['kind'] != 'delivery.decision' or restored.get('scope') != target
                        or restored.get('payload', {}).get('action') != 'reinstate'
                        or self._reference(identifier) not in restored['payload']['subjects']
                        or restored['payload']['authority_proof'] is None
                        or self.provenance[receipt['version_id']]['sequence'] <= self._latest_cancellation(self._point(self._reference(identifier), target))
                        or any(receipt in _input_locators(old['inputs']) for _, old in previous)):
                    raise ERROR('P_PROOF', 'Exact latest human root-restoration decision must be consumed once')
                grant = self._selection_for('applicability', target, {'kind': 'use'}, self._reference(identifier))
                if grant is None or grant['decision_ref'] != receipt:
                    raise ERROR('P_PROOF', 'Root restoration has no current exact establishing decision')
                self._governing_grants(grant, live)
                if (prior['deadline_ms'] is not None and (record['deadline_ms'] is None or record['deadline_ms'] > prior['deadline_ms'])) or any(
                        limit['ceiling'] > min((bound['ceiling'] for bound in prior['limits'] if bound['metric'] == limit['metric'] and bound['unit'] == limit['unit']), default=-1)
                        for limit in record['limits']):
                    raise ERROR('P_BUDGET', 'Root restoration cannot refresh its generation deadline or allowances')
            return
        issuer = procedure['assignment'] if procedure is not None else message['sender'].get('ref')
        if not parent or parent['responsibility'] != 'setter' or record['issued_under'] != issuer:
            raise ERROR('P_SCOPE', 'Assignment requires the exact actual upstream setter mandate')
        if self._status(record['issued_under'], parent['use_scope'])['validity'] != 'valid':
            raise ERROR('P_CONTEXT', 'Issuing mandate no longer applies')
        if parent['deadline_ms'] is not None and (record['deadline_ms'] is None or record['deadline_ms'] > parent['deadline_ms']):
            raise ERROR('P_BUDGET', 'Child cannot extend the upstream finite deadline')
        for limit in record['limits']:
            bounds = [item['ceiling'] for item in parent['limits'] if item['metric'] == limit['metric'] and item['unit'] == limit['unit']]
            if parent['limits'] and (not bounds or limit['ceiling'] > min(bounds)):
                raise ERROR('P_BUDGET', 'Child cannot expand an upstream allowance')
        allowed_reads = record['inherited'] + [ref for binding in record['inputs'] for ref in binding['refs']] + [record['criteria']]
        for effect in record['effects']:
            templates = [item for item in parent['effects'] if all(item[key] == effect[key] for key in ('operation', 'tool_policy', 'destination_handle'))]
            if effect['owner'] != record['owner'] or not templates:
                raise ERROR('P_SCOPE', 'Child cannot expand upstream operation, tool or destination rights')
            if effect['operation'] == 'read':
                if any(ref not in allowed_reads for ref in effect['targets']):
                    raise ERROR('P_SCOPE', 'Read targets must be exact authorized child inputs or criteria')
            elif not any(all(ref in template['targets'] for ref in effect['targets']) for template in templates):
                raise ERROR('P_SCOPE', 'Child cannot expand upstream effect targets')
        distance = record['owner']['layer'] - parent['owner']['layer']
        if distance == 0:
            if target != parent['use_scope'] or record['owner']['work_item'] != parent['owner']['work_item']:
                raise ERROR('P_SCOPE', 'Local child must preserve its issuing work scope')
            if not self._child_owner(parent['owner'], record, self.resolve(record['profile'], 'profile')):
                raise ERROR('P_SCOPE', 'Local assignment exceeds its exact question or profile-entitled coordinator ownership')
        else:
            raise ERROR('P_SCOPE', 'An adjacent layer receives a task through its deterministic local entry, not foreign staffing')
        inherited = [self._assignment_use(parent, path, ref) for path, ref in _reference_paths(parent)
                     if path.startswith('/inherited/') or path.startswith('/inputs/')]
        supplied = [self._assignment_use(record, path, ref) for path, ref in _reference_paths(record)
                    if path.startswith('/inherited/') or path.startswith('/inputs/')]
        if any(point not in supplied for point in inherited):
            raise ERROR('P_SCOPE', 'Child cannot omit or remap its inherited governing input manifest')
        entitled = inherited + [self._assignment_use(parent, '/criteria', parent['criteria'])]
        allowed_incoming = []
        for path, ref in _reference_paths(record):
            if not (path.startswith('/inherited/') or path.startswith('/inputs/') or path == '/criteria'):
                continue
            point = self._assignment_use(record, path, ref)
            if self._superseded_basis(point) and not self._inspection(record, path, ref, live):
                raise ERROR('P_CONTEXT', 'A superseded output cannot justify a new governing input')
            if point in entitled:
                continue
            if ref in allowed_incoming:
                if self._status(point)['validity'] in {'invalid', 'revoked'} and not self._inspection(record, path, ref, live):
                    raise ERROR('P_CONTEXT', 'Offered interface input has lost applicability')
                continue
            if point['use_scope'] != parent['use_scope'] or not self._produced_under(ref, record['issued_under'], parent['owner']):
                raise ERROR('P_SCOPE', 'Declared input is not governed by the issuing mandate or an actual owned return')
            if (self._status(point)['validity'] in {'invalid', 'revoked'} and not self._inspection(record, path, ref, live)) or self._key(point) not in self.states:
                raise ERROR('P_CONTEXT', 'Actual returned input has no current applicable use')

    def _produced_under(self, reference, setter, owner):
        value = self.versions[reference['version_id']]
        record = value['content']['record']
        if value['kind'] == 'delivery.source' and record['owner'].get('kind') == 'authority':
            return False
        if value['kind'] not in {'delivery.source', 'delivery.product', 'delivery.assessment'}:
            return False
        producer = self.provenance[reference['version_id']]['origin']
        if producer['kind'] != 'assignment':
            return False
        parent = self.resolve(setter, 'assignment')
        assigned = self.resolve(producer['ref'], 'assignment')
        if (assigned['owner']['work_item'] != owner['work_item'] or assigned['profile'] != parent['profile']
                or assigned['use_scope'] != parent['use_scope']):
            return False
        if producer['ref'] == setter:
            return assigned['owner'] == owner
        context_ref = self.provenance[reference['version_id']]['context']
        context = self.resolve(context_ref, 'context')
        if context['execution']['phase'] != 'work' or self.run_states.get(context['run_id']) != 'returned':
            return False
        distance = assigned['owner']['layer'] - owner['layer']
        if assigned['issued_under'] == setter:
            if distance == 0:
                return True
            if distance != 1:
                return False
            if value['kind'] == 'delivery.assessment' and record['assessment_kind'] == 'receiving':
                incoming = [ref for binding in assigned['inputs'] if binding['slot_id'] == 'incoming_handoff' for ref in binding['refs']]
                return incoming == [record['subject']]
            if value['kind'] == 'delivery.product' and record['product_kind'] == 'handoff':
                for transaction in self.transactions:
                    if transaction['return_artifact'] is None:
                        continue
                    for captured in transaction['return_artifact'].values():
                        package = loads(captured)
                        if package['context'] == context_ref:
                            return any(intent['message_type'] == 'handoff' and intent['payload']['handoff'] == reference
                                       for intent in package['intents'])
            return False
        if distance != 0 or assigned['issued_under'] is None:
            return False
        local = self.resolve(assigned['issued_under'], 'assignment')
        if (local['issued_under'] != setter or local['responsibility'] != 'setter'
                or local['profile'] != parent['profile']):
            return False
        if value['kind'] == 'delivery.product' and self._output_obligations(record):
            # This recognizes the admitted return. The actual input gate checks
            # its semantic deadline at the live or historical assessment instant.
            point = self._point(reference, parent['use_scope'])
            return (record['owner'] == local['owner'] and self._selected_output(reference, parent['use_scope'])
                    and self._status(point) == {'validity': 'valid', 'applicable': True})
        if value['kind'] == 'delivery.assessment':
            return any(selected['proof'] == reference and selected['proof_use_scope'] == parent['use_scope']
                       and self._selected_output(selected['subject'], parent['use_scope'])
                       and self.resolve(selected['subject'])['owner'] == local['owner']
                       for key, selected in self.proofs.items() if key[0] == parent['use_scope'])
        return False

    def _finding(self, record, assignment):
        bindings = {item['slot_id']: item['refs'] for item in record['related']}
        criteria_keys = [key for key in bindings if key.startswith('criterion:')]
        if set(bindings) != {'subject', *criteria_keys} or len(criteria_keys) != 1 or len(bindings['subject']) != 1 or len(bindings[criteria_keys[0]]) != 1:
            raise ERROR('P_PROOF', 'Finding needs one exact subject and criterion binding')
        criterion_ref = bindings[criteria_keys[0]][0]
        criteria = self.resolve(criterion_ref, 'source')
        if criterion_ref != assignment['criteria'] or not any(item['id'] == criteria_keys[0][10:] for item in criteria['criteria']):
            raise ERROR('P_PROOF', 'Finding criterion does not belong to the exact assigned criteria')
        subject = self.resolve(bindings['subject'][0])
        if assignment['responsibility'] not in {'reviewer', 'integration_reviewer', 'receiver'}:
            raise ERROR('P_SCOPE', 'Diagnostic findings require an assigned assessor')

    def _validate_profile(self, profile):
        ids, groups, selectors = set(), {}, set()
        for item in profile['obligations']:
            if item['slot_id'] in ids or item['minimum'] > item['maximum']:
                raise ERROR('P_CONFLICT', 'Duplicate or contradictory obligation slot')
            ids.add(item['slot_id'])
            owner = item['owner']
            if item['role'] == 'management_activity':
                raise ERROR('P_PROOF', 'Management-activity obligation enforcement is unsupported by this runtime')
            if item['role'] not in {'input', 'evidence'}:
                if item['minimum'] != 1 or item['maximum'] != 1:
                    raise ERROR('P_PROOF', 'Selector obligations support exactly one record per slot')
                key = (_owner_key(owner), item['subject_kind'], item['role'])
                if key in selectors:
                    raise ERROR('P_PROOF', 'Duplicate selector cells cannot encode an unsupported review quorum')
                selectors.add(key)
            if owner['work_kind'] == 'question':
                groups.setdefault((owner['layer'], owner['work_item']), set()).add(owner['question'])
            expected = {'professional_review': 'assessment', 'integration_review': 'assessment',
                        'receiving_acceptance': 'assessment', 'human_acceptance': 'decision',
                        'release_permission': 'decision', 'answer': 'product', 'evidence': 'product'}
            if item['role'] in expected and item['required_kind'] != expected[item['role']]:
                raise ERROR('P_PROOF', 'Obligation role and required record kind disagree')
        if any(questions != {'what', 'why', 'how', 'who', 'where', 'when'} for questions in groups.values()):
            raise ERROR('P_PROOF', 'Every included layer/work scope requires six question obligations')
        for layer, work_item in groups:
            for question in ('what', 'why', 'how', 'who', 'where', 'when'):
                relevant = [item for item in profile['obligations'] if item['owner'] == {
                    'layer': layer, 'work_kind': 'question', 'question': question, 'work_item': work_item}]
                if not any(item['role'] == 'professional_review' for item in relevant):
                    raise ERROR('P_PROOF', 'Independent professional review cannot be removed by a profile')

    def content_policy(self, profile):
        """Resolve the explicitly governed content-policy slot without historical fallback.

        Args:
            profile: Exact fixed delivery-profile reference containing the scoped selector.
        Returns:
            Current exact policy UsePoint, or None for general non-SABSA processing.
        Raises:
            ProtocolError: The selected slot lacks current attributable policy material.
        """
        selector = self.resolve(profile, 'profile')['content_profile']
        if selector is None:
            return None
        reference = self.sources.get((selector['use_scope'], selector['logical_id']))
        if reference is None:
            raise ERROR('P_CONTEXT', 'The governed content-policy slot has no current basis')
        source = self.resolve(reference, 'source')
        if (source['source_role'] != 'policy' or source['owner'].get('kind') != 'authority'
                or source['origin'] != source['owner']
                or self._status(reference, selector['use_scope'])['validity'] != 'valid'):
            raise ERROR('P_CONTEXT', 'The governed content-policy slot is not currently attributable')
        return self._point(reference, selector['use_scope'])

    def capability_policy(self, profile):
        """Resolve the intrinsic global capability source at the bootstrap scope.

        Args:
            profile: Existing governing profile reference; no neighbor preference.
        Returns:
            Exact current global capability UsePoint.
        Raises:
            ProtocolError: Engagement or unambiguous attributable source is missing.
        """
        self.resolve(profile, 'profile')
        if not self.transactions:
            raise ERROR('P_STATE', 'Global capabilities require an initialized engagement')
        anchor = self.transactions[0]['operations'][0]['data']['message']['scope']
        content = self.resolve(profile, 'profile')['content_profile']
        candidates = [selected for (scope, logical_id), selected in self.sources.items() if scope == anchor
                      and self.resolve(selected, 'source')['source_role'] == 'policy'
                      and (content is None or (scope, logical_id) != (content['use_scope'], content['logical_id']))]
        if len(candidates) != 1:
            raise ERROR('P_SCOPE', 'An unambiguous current intrinsic capability source is required')
        return self._point(candidates[0], anchor)

    @_within_assessment
    def local_entry(self, handoff_use, responsibility, acceptance=None, live=True):
        """Derive an adjacent layer's structural gateway without external staffing.

        Args:
            handoff_use: Exact published upstream handoff UsePoint.
            responsibility: Receiver entry or coordinating setter entry.
            acceptance: Actual selected receiving assessment, required for setter.
            live: Require current relevant material and governing support.
        Returns:
            Deterministic assignment proposal with logical_id and record.
        Raises:
            ProtocolError: Interface, acceptance, ownership or global basis is invalid.
        """
        if responsibility not in {'receiver', 'setter'}:
            raise ERROR('P_SCOPE', 'Adjacent entry is a local receiver or coordinator, never external staffing')
        point = self._point(handoff_use)
        handoff = self.resolve(point['ref'], 'product')
        if handoff['product_kind'] != 'handoff' or handoff['owner']['layer'] >= 6:
            raise ERROR('P_SCOPE', 'A next-layer gateway requires an exact adjacent offered interface')
        publisher = self.resolve(handoff['assignment'], 'assignment')
        parent_ref = handoff['assignment'] if publisher['responsibility'] == 'setter' else publisher['issued_under']
        parent = self.resolve(parent_ref, 'assignment')
        if (parent['responsibility'] != 'setter' or parent['owner']['layer'] != handoff['owner']['layer']
                or parent['owner']['work_item'] != handoff['owner']['work_item']
                or self._status(parent_ref, parent['use_scope'])['validity'] != 'valid'):
            raise ERROR('P_SCOPE', 'Handoff is not published under an entitled upstream mandate')
        interface = next((item['refs'] for item in handoff['related'] if item['slot_id'] == 'interface'), [])
        if len(interface) != 1:
            raise ERROR('P_CONTEXT', 'The offered handoff must name its fixed interface')
        interface_ref = interface[0]
        interfaces = [dependency for dependency in self.reliance.get(self._key(point), []) if dependency['ref'] == interface_ref]
        if len(interfaces) != 1:
            raise ERROR('P_CONTEXT', 'The offered interface use must be unambiguous')
        if self._status(point)['validity'] in {'invalid', 'revoked'}:
            raise ERROR('P_CONTEXT', 'A cancelled interface cannot issue new local work')
        for dependency in self._governing_dependencies(point):
            if not self._governing_input(dependency, live):
                raise ERROR('P_CONTEXT', 'An offered interface has an unavailable current prerequisite')
        owner = {'layer': handoff['owner']['layer'] + 1, 'work_kind': 'integration',
                 'question': None, 'work_item': handoff['owner']['work_item']}
        profile = self.resolve(handoff['profile'], 'profile')
        if not any(item['owner'] == owner for item in profile['obligations']):
            raise ERROR('P_PROOF', 'The governing profile lacks this local layer gateway')
        policy = self.capability_policy(handoff['profile'])
        anchor = policy['use_scope']
        axiom_uses = [dependency for dependency in self._closure(point)
                      if self.versions[dependency['ref']['version_id']]['kind'] == 'delivery.source'
                      and self.resolve(dependency['ref'])['owner'].get('kind') == 'authority'
                      and self.resolve(dependency['ref'])['source_role'] != 'policy']
        axiom_uses.append(policy)
        content = self.content_policy(handoff['profile'])
        if content is not None:
            axiom_uses.append(content)
        axiom_uses = sorted({canonical(item): item for item in axiom_uses}.values(), key=canonical)
        axioms = list({_hash(item['ref']): item['ref'] for item in axiom_uses}.values())
        inputs = [{'slot_id': 'l0:' + str(index) + ':' + item['ref']['logical_id'], 'refs': [item['ref']]}
                  for index, item in enumerate(axiom_uses)]
        inputs.extend([{'slot_id': 'incoming_handoff', 'refs': [point['ref']]},
                       {'slot_id': 'incoming_interface', 'refs': [interface_ref]}])
        if responsibility == 'setter':
            if acceptance is None:
                raise ERROR('P_PROOF', 'Local coordination follows actual qualified receiving acceptance')
            assessment = self.resolve(acceptance, 'assessment')
            receiver = self.resolve(assessment['assignment'], 'assignment')
            if (assessment['assessment_kind'] != 'receiving' or assessment['subject'] != point['ref']
                    or assessment['verdict'] != 'accepted' or assessment['criteria'] != interface_ref
                    or receiver['owner'] != owner or receiver['issued_under'] != parent_ref
                    or not any(selected['subject'] == point['ref'] and selected['proof'] == acceptance
                               and selected['proof_use_scope'] == receiver['use_scope']
                               for key, selected in self.proofs.items() if key[0] == point['use_scope'])
                    or not self._governing_input(point, live)):
                raise ERROR('P_PROOF', 'Exact independently accepted interface is required for local coordination')
            inputs.append({'slot_id': 'incoming_acceptance', 'refs': [acceptance]})
        elif acceptance is not None:
            raise ERROR('P_SCOPE', 'Receiving inspection cannot depend on its future acceptance')
        _, root = self._generation(parent_ref)
        identity = _hash({'handoff': point, 'owner': owner, 'responsibility': responsibility, 'acceptance': acceptance})
        record = {'owner': owner, 'responsibility': responsibility, 'assigned_actor': 'local-entry:' + identity,
                  'profile': handoff['profile'], 'routing': {'policy': policy['ref']}, 'inherited': axioms,
                  'inputs': inputs, 'criteria': interface_ref, 'effects': [], 'limits': copy.deepcopy(root['limits']),
                  'deadline_ms': root['deadline_ms'], 'use_scope': point['use_scope'], 'issued_under': parent_ref,
                  'input_uses': []}
        for path, reference in _reference_paths(record):
            if path.startswith(('/inherited/', '/inputs/')) or path in {'/criteria', '/routing/policy'}:
                if path.startswith('/inputs/'):
                    slot = inputs[int(path.split('/')[2])]['slot_id']
                    if slot.startswith('l0:'):
                        scope = axiom_uses[int(slot.split(':')[1])]['use_scope']
                    elif slot == 'incoming_interface':
                        scope = interfaces[0]['use_scope']
                    else:
                        scope = point['use_scope']
                elif path == '/criteria':
                    scope = interfaces[0]['use_scope']
                elif path == '/routing/policy':
                    scope = anchor
                else:
                    scope = next(item['use_scope'] for item in axiom_uses if item['ref'] == reference)
                record['input_uses'].append({'at': path, 'use_scope': scope})
        available = self._assignment_routing(record, live)
        targets = list(dict.fromkeys(_hash(reference) for reference in axioms + [point['ref'], interface_ref] + ([acceptance] if acceptance else [])))
        exact = axioms + [point['ref'], interface_ref] + ([acceptance] if acceptance else [])
        protected = [next(reference for reference in exact if _hash(reference) == digest) for digest in targets]
        for template in available['capabilities']['effects']:
            if responsibility == 'receiver' and template['operation'] not in {'read', 'propose'}:
                continue
            record['effects'].append({**template, 'owner': owner,
                                      'targets': [] if template['operation'] == 'propose' else protected})
        return {'logical_id': 'local-entry:' + identity, 'record': record}

    def assignment_routing(self, record, live=True):
        """Validate one assignment against its exact current scoped routing policy.

        Args:
            record: Immutable assignment including explicit routing and use selectors.
            live: Require current external material for new work; historical replay
                uses only exact control assets committed in this same journal.
        Returns:
            Selected route projection with its exact governing policy UsePoint.
        Raises:
            ProtocolError: Policy authority, applicability, material or capability fails.
        """
        return copy.deepcopy(self._assignment_routing(record, live))

    @_within_assessment
    def _assignment_routing(self, record, live=True):
        """Use current policy facts and once-admitted immutable routing metadata."""
        import governed_routing
        reference = record['routing']['policy']
        point = self._assignment_use(record, '/routing/policy', reference)
        if point != self.capability_policy(record['profile']):
            raise ERROR('P_SCOPE', 'A task must use the unambiguous intrinsic global capability policy')
        if (self.sources.get((point['use_scope'], reference['logical_id'])) != reference
                or not self._governing_input(point, live)):
            raise ERROR('P_CONTEXT', 'Routing requires its exact current attributable policy selection')
        source = self.resolve(reference, 'source')
        if (source['source_role'] != 'policy' or source['owner'].get('kind') != 'authority'
                or source['origin'] != source['owner']):
            raise ERROR('P_SCOPE', 'Global capabilities require their current attributable L0 source')
        cache_key = (canonical(reference), tuple(source['material']))
        if cache_key not in self._routing_snapshots:
            verified = {asset_id: self._validation_bytes(asset_id, live) for asset_id in source['material']}
            self._routing_snapshots[cache_key] = _freeze(governed_routing.load_policy(source, verified.__getitem__))
        snapshot = self._routing_snapshots[cache_key]
        profile = self.resolve(record['profile'], 'profile')
        selected = governed_routing.validate_assignment(record, snapshot, profile['routing_policy_id'])
        selected['policy_use'] = point
        selected['snapshot'] = snapshot
        return selected

    def context_execution(self, context, live=True):
        """Resolve the functional chooser or the entity's actual captured choice.

        Args:
            context: Exact selection/work context for an existing assignment.
            live: Require current policy material and unrevoked choice authority.
        Returns:
            Bounded execution capability plus host-only captured public resources.
        Raises:
            ProtocolError: Phase, provenance, assignment, actor or current choice fails.
        """
        return copy.deepcopy(self._context_execution(context, live))

    @_within_assessment
    def _context_execution(self, context, live=True):
        """Validate a phase internally without exporting private policy references."""
        import governed_routing
        assignment = self.resolve(context['assignment'], 'assignment')
        available = self._assignment_routing(assignment, live)
        execution = context['execution']
        if not isinstance(execution, dict) or execution.get('phase') not in {'selection', 'work'}:
            raise ERROR('P_CONTEXT', 'An entity requires an explicit selection or work phase')
        if execution['phase'] == 'selection':
            return {**available, 'phase': 'selection', 'instructions': [], 'allowed_operations': ['read']}
        reference = execution['selection']
        decision = self.resolve(reference)
        if self.versions[reference['version_id']]['kind'] != 'delivery.decision':
            raise ERROR('P_ORIGIN', 'Work requires an actual captured execution decision')
        message = decision['message']
        choice = message['payload']
        previous = self.resolve(message['context'], 'context')
        if (choice.get('action') != 'select_execution' or choice['assignment'] != context['assignment']
                or message['sender'] != {'kind': 'assignment', 'ref': context['assignment']}
                or previous['assignment'] != context['assignment'] or previous['issued_to'] != context['issued_to']
                or previous['execution'] != {'phase': 'selection'} or message['scope'] != assignment['use_scope']):
            raise ERROR('P_ORIGIN', 'Work choice is not from this exact local entity selection run')
        self._governing_grants(self._revision_grant(reference, assignment['use_scope']), live)
        selected = governed_routing.select_execution(assignment, available['snapshot'], choice)
        return {**selected, 'phase': 'work', 'selection': reference, 'policy_use': available['policy_use'],
                'snapshot': available['snapshot']}

    @_within_assessment
    def _assignment_requirements(self, record, live=True):
        key = (canonical(record), self.scope, live)
        memo = self._assessment_walk
        if key in memo['requirements']:
            return
        self._check_assignment_requirements(record, live)
        memo['requirements'].add(key)

    def _check_assignment_requirements(self, record, live):
        profile = self.resolve(record['profile'], 'profile')
        self._assignment_routing(record, live=live)
        content = self.content_policy(record['profile'])
        if content is not None and content not in self._dependencies(record):
            raise ERROR('P_CONTEXT', 'A mandate cannot drop or replace its exact currently governing content-policy use')
        inspections = [self._assignment_use(record, path, ref) for path, ref in _reference_paths(record)
                       if self._inspection(record, path, ref, live)]
        for point in self._dependencies(record):
            if not self._governing_input(point, live) and point not in inspections:
                raise ERROR('P_CONTEXT', 'Every direct governing input must currently apply except the exact inspection subject')
        if _hash(record) in self._assignment_records:
            # Immutable assignment structure/cardinality/traceability was checked
            # at admission. New work checks only the direct facts above.
            return
        bindings = {}
        for item in record['inputs']:
            if item['slot_id'] in bindings or len(item['refs']) != len({_hash(ref) for ref in item['refs']}):
                raise ERROR('P_CONFLICT', 'Input slots and exact references must be unique')
            bindings[item['slot_id']] = item['refs']
        for obligation in profile['obligations']:
            if obligation['owner'] != record['owner'] or obligation['role'] != 'input':
                continue
            values = bindings.get(obligation['slot_id'], [])
            if not obligation['minimum'] <= len(values) <= obligation['maximum']:
                raise ERROR('P_PROOF', 'Required assignment input cardinality is not satisfied')
            binding_index = next(index for index, binding in enumerate(record['inputs']) if binding['slot_id'] == obligation['slot_id']) if values else None
            for ref_index, ref in enumerate(values):
                body = self.resolve(ref, obligation['required_kind'])
                point = self._assignment_use(record, '/inputs/' + str(binding_index) + '/refs/' + str(ref_index), ref)
                inspect_subject = self._inspection(record, '/inputs/' + str(binding_index) + '/refs/' + str(ref_index), ref, live)
                if not self._governing_input(point, live) and not inspect_subject:
                    raise ERROR('P_CONTEXT', 'Required operational input is not current and qualified')
        criteria = self.resolve(record['criteria'], 'source')
        if criteria['source_role'] != 'criteria' or not criteria['criteria']:
            raise ERROR('P_PROOF', 'Exact nonempty criteria source is required')
        available = {ref['version_id'] for ref in record['inherited']}
        for item in record['inputs']:
            for ref in item['refs']:
                available.update(parent['ref']['version_id'] for parent in self._closure(ref, record['use_scope']))
        if any(item['requirement']['version_id'] not in available for item in criteria['criteria']):
            raise ERROR('P_PROOF', 'Criteria cannot detach inherited requirements from assigned inputs')

    @_within_assessment
    def assessment_closure(self, subject, assignment):
        """Return exact assessable subject plus assigned observation prerequisites.

        Args:
            subject: Existing pending or qualified subject reference.
            assignment: Exact assessment assignment containing named evidence slots.
        Returns:
            Ordered deduplicated causal closure, excluding its future assessment.
        Raises:
            ProtocolError: A reference or dependency is missing or cyclic.
        """
        self.resolve(assignment, 'assignment')
        use_scope = self.resolve(assignment, 'assignment')['use_scope']
        closure = self._closure(self._subject_use(subject, self.resolve(assignment, 'assignment')))
        for ref in self._closure(assignment, use_scope):
            if ref not in closure:
                closure.append(ref)
        return closure

    @_within_assessment
    def _product_requirements(self, record, live=True):
        key = ('product', canonical(record), self.scope, live)
        completed = self._assessment_walk.setdefault('product_supports', {})
        if key not in completed:
            completed[key] = self._check_product_requirements(record, live)
        return copy.deepcopy(completed[key])

    def _check_product_requirements(self, record, live):
        supports = []
        assignment = self.resolve(record['assignment'], 'assignment')
        self._assignment_requirements(assignment, live)
        profile = self.resolve(record['profile'], 'profile')
        if profile['content_profile'] is not None:
            import governed_sabsa
            supports.extend(governed_sabsa._owned_requirements(self, record, self.scope, live))
            if record['product_kind'] == 'final_result' and record['outcome']['kind'] == 'verified_candidate':
                supports.extend(governed_sabsa._require_final(self, record, self.scope, live))
        related = {item['slot_id']: item['refs'] for item in record['related']}
        if len(related) != len(record['related']):
            raise ERROR('P_CONFLICT', 'Related obligation slots must be unique')
        if record['product_kind'] == 'bundle' and self._question_work(profile, record['owner']):
            self._complete_bundle(record, live)
        evidence_bindings = dict(related)
        subject_ref = next((self._reference(identifier) for identifier, value in self.versions.items()
                            if value['kind'] == 'delivery.product' and value['content']['record'] == record), None)
        if subject_ref is not None:
            for key, selected in self.proofs.items():
                if key[0] != self.scope:
                    continue
                if selected['subject'] != subject_ref or self._status(selected['proof'], selected['proof_use_scope'])['validity'] != 'valid':
                    continue
                assessment = self.resolve(selected['proof'], 'assessment')
                reviewer_assignment = self.resolve(assessment['assignment'], 'assignment')
                for binding in reviewer_assignment['inputs']:
                    if binding['slot_id'] in evidence_bindings and evidence_bindings[binding['slot_id']] != binding['refs']:
                        raise ERROR('P_CONFLICT', 'Competing exact evidence bindings cannot silently replace each other')
                    evidence_bindings[binding['slot_id']] = binding['refs']
        criteria = self.resolve(assignment['criteria'], 'source')
        required = {slot for item in criteria['criteria'] for slot in item['evidence_slots']}
        if record['product_kind'] == 'answer':
            for slot in required:
                if not evidence_bindings.get(slot):
                    raise ERROR('P_PROOF', 'Required named criterion evidence has no current binding')
                for ref in evidence_bindings[slot]:
                    observed = self.resolve(ref, 'product')
                    if observed['product_kind'] != 'observation' or self._status(ref)['validity'] != 'valid':
                        raise ERROR('P_PROOF', 'Named criterion evidence must be a qualified exact observation')
        for item in profile['obligations']:
            if (item['owner'] != record['owner'] or item['role'] != 'evidence'
                    or item['subject_kind'] != record['product_kind']):
                continue
            values = evidence_bindings.get(item['slot_id'], [])
            if not item['minimum'] <= len(values) <= item['maximum']:
                raise ERROR('P_PROOF', 'Required named evidence cardinality is unsatisfied')
            for ref in values:
                self.resolve(ref, item['required_kind'])
                if self._status(ref)['validity'] != 'valid':
                    raise ERROR('P_PROOF', 'Required observation is not current and qualified')
        for ref in record['evidence']:
            observed = self.resolve(ref, 'product')
            if observed['product_kind'] != 'observation' or self._status(ref)['validity'] != 'valid':
                raise ERROR('P_PROOF', 'Declared evidence must be an exact qualified observation')
        if record['product_kind'] == 'final_result' and record['outcome']['kind'] == 'verified_candidate':
            if not related.get('bundle') or not related.get('handoff'):
                raise ERROR('P_PROOF', 'Final result needs integrated bundle and accepted handoff closure')
            for ref in related['bundle'] + related['handoff']:
                if not self._governing_input(self._point(ref), live):
                    raise ERROR('P_PROOF', 'Final result prerequisite is not qualified')
        return supports

    def _owned_decision(self, record, assignment, origin):
        if assignment is None:
            raise ERROR('P_SCOPE', 'Semantic ownership requires an actual assigned setter decision')
        owner = record['owner']
        if owner.get('kind') == 'assignment' and 'message' in record:
            owner = self.resolve(owner['ref'], 'assignment')['owner']
        if assignment['responsibility'] != 'setter' or assignment['owner'] != owner:
            raise ERROR('P_SCOPE', 'Decision exceeds exact assigned semantic ownership')

    def _review_generation(self, record):
        subjects = {canonical(ref) for binding in record['inputs'] if binding['slot_id'] == 'assessed-subject'
                    for ref in binding['refs']}
        governing = {}
        for path, ref in _reference_paths(record):
            if not path.startswith(('/inherited/', '/inputs/')) or canonical(ref) in subjects:
                continue
            point = self._assignment_use(record, path, ref)
            governing[canonical(point)] = point
        return _hash({'owner': record['owner'],
                      'profile': self._assignment_use(record, '/profile', record['profile']),
                      'criteria': self._assignment_use(record, '/criteria', record['criteria']),
                      'responsibility': record['responsibility'], 'use_scope': record['use_scope'],
                      'governing': [governing[key] for key in sorted(governing)]})

    def _revisions(self, scope):
        for identifier, value in self.versions.items():
            if value['kind'] != 'delivery.decision' or value['content']['scope'] != scope:
                continue
            message = value['content']['record']['message']
            payload = message['payload']
            if payload['action'] in {'rework', 'reformulate'}:
                previous = payload.get('assignment', payload.get('subject'))
                yield self._reference(identifier), previous, payload['replacement'], payload

    def _revision_grant(self, reference, scope):
        provenance = self.provenance[reference['version_id']]
        return {'decision_ref': reference, 'scope': scope,
                'grants': [copy.deepcopy(provenance['authority'])] if 'authority' in provenance else []}

    def _reviewer_support(self, record, live):
        if record['responsibility'] not in {'reviewer', 'integration_reviewer'}:
            return []
        generation = self._review_generation(record)
        members = {identifier: value['content']['record'] for identifier, value in self.versions.items()
                   if value['kind'] == 'delivery.assignment'
                   and value['content']['record']['responsibility'] in {'reviewer', 'integration_reviewer'}
                   and self._review_generation(value['content']['record']) == generation}
        if not members:
            return []
        actor = next(iter(members.values()))['assigned_actor']
        support = []
        for decision, previous, replacement, payload in self._revisions(record['use_scope']):
            if previous['version_id'] not in members or replacement['version_id'] not in members:
                continue
            old, new = members[previous['version_id']], members[replacement['version_id']]
            if old['assigned_actor'] != actor:
                raise ERROR('P_PROOF', 'Reviewer replacement must follow the entitled reviewer lineage')
            if not self._governing_input(self._point(decision, record['use_scope']), live):
                raise ERROR('P_PROOF', 'Reviewer replacement decision is no longer applicable')
            actor = new['assigned_actor']
            support.append(decision)
        if record['assigned_actor'] != actor:
            raise ERROR('P_PROOF', 'A different reviewer requires an explicit current owner replacement decision')
        return support

    def _prior_assessments(self, previous):
        old = self.resolve(previous)
        result = []
        for identifier, value in self.versions.items():
            if value['kind'] != 'delivery.assessment':
                continue
            assessment = value['content']['record']
            if assessment['owner'] != old['owner']:
                continue
            subject = self.resolve(assessment['subject'])
            if (assessment['assignment'] == previous or subject.get('assignment') == previous
                    or (self.versions[previous['version_id']]['kind'] == 'delivery.source'
                        and assessment['criteria'] == previous)):
                result.append((self._reference(identifier), assessment))
        return result

    def _preserved_findings(self, previous, payload):
        assessments = self._prior_assessments(previous)
        supplied = payload.get('findings', [])
        allowed = [reference for reference, _ in assessments]
        required = []
        for _, assessment in assessments:
            allowed.extend(assessment['findings'])
            required.extend(assessment['findings'])
        if any(reference not in allowed for reference in supplied):
            raise ERROR('P_SCOPE', 'Revision findings must come from the exact prior owned assessments')
        expanded = list(supplied)
        for reference, assessment in assessments:
            if reference in supplied:
                expanded.extend(assessment['findings'])
        if any(reference not in expanded for reference in required):
            raise ERROR('P_PROOF', 'An owner revision must explicitly preserve all prior findings')
        return assessments

    def assignment_feedback(self, record, live=True):
        """Project exact owner revision feedback without reviving old dependencies.

        Args:
            record: Current assignment, including any exact assigned review subject.
            live: Verify current revision grants and required historical material.
        Returns:
            Read-only revision reasons, prior assessments and named finding bytes.
        Raises:
            ProtocolError: Entitled revision support or required feedback is unavailable.
        """
        current = next((self._reference(identifier) for identifier, value in self.versions.items()
                        if value['kind'] == 'delivery.assignment' and value['content']['record'] == record), None)
        subjects = [ref for binding in record['inputs'] if binding['slot_id'] == 'assessed-subject' for ref in binding['refs']]
        producers = [self.resolve(ref).get('assignment') for ref in subjects]
        feedback = []
        for decision, previous, replacement, payload in self._revisions(record['use_scope']):
            if replacement not in [current, record['criteria'], *producers]:
                continue
            self._governing_grants(self._revision_grant(decision, record['use_scope']), live)
            assessments = self._preserved_findings(previous, payload)
            records = [{'ref': reference, 'record': copy.deepcopy(assessment)} for reference, assessment in assessments]
            findings = []
            for reference in dict.fromkeys(_hash(ref) for _, assessment in assessments for ref in assessment['findings']):
                exact = next(ref for _, assessment in assessments for ref in assessment['findings'] if _hash(ref) == reference)
                body = self.resolve(exact)
                material = []
                for identifier in body.get('material', []):
                    if self.blob_reader is None:
                        raise ERROR('P_CONTEXT', 'Required historical feedback bytes are unavailable')
                    try:
                        raw = self.blob_reader(identifier)
                    except (OSError, ValueError) as exc:
                        raise ERROR('P_CONTEXT', 'Required historical feedback bytes are unavailable') from exc
                    if blob(raw) != identifier:
                        raise ERROR('P_INTEGRITY', 'Historical feedback identity mismatch')
                    material.append({'blob_id': identifier, 'data': base64.b64encode(raw).decode('ascii')})
                findings.append({'ref': exact, 'record': copy.deepcopy(body), 'material': material})
            feedback.append({'historical': True, 'decision': decision, 'previous': previous,
                             'replacement': replacement, 'reason': payload['reason'],
                             'assessments': records, 'findings': findings})
        return feedback

    def _latest_cancellation(self, point):
        return max((event['sequence'] for event in self.events if event['kind'] == 'cancellation' and point in event['subjects']), default=0)

    def _admit_event(self, value):
        """Append detached immutable history and update only its selection indexes."""
        event = _freeze(value)
        self.events.append(event)
        if event['kind'] != 'selection':
            return
        key = (event['category'], event['scope'], _typed_key(event['slot']), _typed_key(event['subject']))
        self._selection_latest[key] = event
        point = (event['use_scope'], _typed_key(event['subject']))
        self._point_selections[point] = self._point_selections.get(point, ()) + (event,)
        decision = (_typed_key(event['decision_ref']), event['scope'])
        self._decision_selections[decision] = self._decision_selections.get(decision, ()) + (event,)

    def _selection_event(self, category, scope, slot, subject, use_scope, decision_ref, provenance, authority, decision_scope=None):
        grants = []
        if authority is not None:
            grants.append({'purpose': authority['purpose'], 'key_id': authority['key_id']})
        self._admit_event({'kind': 'selection', 'category': category, 'scope': scope,
                            'slot': copy.deepcopy(slot), 'subject': copy.deepcopy(subject), 'use_scope': use_scope,
                            'decision_ref': copy.deepcopy(decision_ref), 'grants': grants,
                            **({'decision_scope': decision_scope} if decision_scope is not None and decision_scope != scope else {})})

    def _selection_for(self, category, scope, slot, subject):
        return self._selection_latest.get((category, scope, _typed_key(slot), _typed_key(subject)))

    def _effective_establishment(self, event):
        category = event['category']
        # Reviewer replacement acts are cumulative supports, not one selector.
        if category != 'review-lineage' and self._selection_for(category, event['scope'], event['slot'], event['subject']) != event:
            return False
        if category == 'basis' and self.selections.get(_proof_key(event['scope'], event['slot'])) != event['subject']:
            return False
        if category in {'proof', 'review-lineage'}:
            current = self.proofs.get(_proof_key(event['scope'], event['slot']))
            if current is None or current['proof'] != event['subject'] or current['proof_use_scope'] != event['use_scope']:
                return False
        if category == 'source' and self.sources.get((event['scope'], event['slot']['logical_id'])) != event['subject']:
            return False
        return True

    def _effective_establishments(self):
        for event in self.events:
            if event['kind'] == 'selection' and self._effective_establishment(event):
                yield event

    def _point_establishments(self, point):
        events = [event for event in self._point_selections.get((point['use_scope'], _typed_key(point['ref'])), ())
                  if self._effective_establishment(event)]
        if self.versions[point['ref']['version_id']]['kind'] == 'delivery.decision':
            events.extend(event for event in self._decision_selections.get((_typed_key(point['ref']), point['use_scope']), ())
                          if event not in events)
        return events

    def _governing_grants(self, event, live):
        if self._status(event['decision_ref'], event.get('decision_scope', event['scope']))['validity'] != 'valid':
            raise ERROR('P_PROOF', 'Required governing decision has been withdrawn')
        if not live or not event['grants']:
            return
        try:
            profile = self.resolve(self.resolve(event['decision_ref'])['message']['profile'], 'profile')
            for grant in event['grants']:
                trust = operator.trusted_key(grant['purpose'], grant['key_id'], historical=True)
                wire._require_scope(trust, self.engagement, event['scope'])
                if (trust['state'] == 'revoked'
                        or profile['authority_policy_id'] not in trust['host_policy']['authority_policy_ids']
                        or profile['routing_policy_id'] not in trust['host_policy']['routing_policy_ids']):
                    raise ERROR('P_PROOF', 'Required governing decision authority is revoked or no longer permitted')
        except (ValueError, OSError) as error:
            if isinstance(error, ERROR):
                raise
            raise ERROR('P_PROOF', 'Required governing decision enrollment is unavailable') from error

    def _superseded_basis(self, point):
        return any(event['kind'] == 'selection' and event['category'] == 'basis'
                   and event['scope'] == point['use_scope'] and event['subject'] == point['ref']
                   and self.selections.get(_proof_key(event['scope'], event['slot'])) != point['ref']
                   for event in self.events)

    def _governing_input(self, point, live):
        """Read an established exact-use fact, without reassessing its history."""
        self.resolve(point['ref'])
        status = self._status(point)
        until = self._use_changes.get(self._key(point), {}).get('use_until_ms')
        at = int(time.time() * 1000) if live else getattr(self, 'assessed_at_ms', 0)
        if (until is not None and at >= until) or (self._held(point) or status['validity'] != 'valid'
                or not status['applicable']):
            return False
        value = self.versions[point['ref']['version_id']]
        record = value['content']['record']
        if value['kind'] == 'delivery.product' and record['product_kind'] in {'answer', 'bundle', 'handoff', 'final_result'}:
            return not self._output_obligations(record) or self._selected_output(point['ref'], point['use_scope'])
        return True

    @_within_assessment
    def _current_inputs(self, assignment, live):
        for bound_index, binding in enumerate(assignment['inputs']):
            for ref_index, reference in enumerate(binding['refs']):
                path = '/inputs/' + str(bound_index) + '/refs/' + str(ref_index)
                point = self._assignment_use(assignment, path, reference)
                if not self._governing_input(point, live) and not self._inspection(assignment, path, reference, live):
                    return False
        return True

    def _output_obligations(self, record):
        profile = self.resolve(record['profile'], 'profile')
        return [item for item in profile['obligations'] if item['owner'] == record['owner']
                and item['role'] == 'answer' and item['subject_kind'] == record['product_kind']]

    def _selected_output(self, reference, scope):
        value = self.versions[reference['version_id']]
        if value['kind'] != 'delivery.product':
            return False
        record = value['content']['record']
        obligations = self._output_obligations(record)
        return bool(obligations) and all(self.selections.get(_proof_key(scope, {
            'kind': 'basis', 'owner': record['owner'], 'slot_id': item['slot_id']})) == reference for item in obligations)

    def _current_positive_support(self, reference, scope, proof, proof_scope, live):
        assessed = self.resolve(proof, 'assessment')
        if (assessed['subject'] != reference
                or not self._governing_input(self._point(proof, proof_scope), live)
                or assessed['verdict'] not in {'supported', 'supported_with_conditions', 'accepted'}):
            raise ERROR('P_PROOF', 'Candidate requires an applicable positive exact review')
        if any(not self._governing_input(self._point(condition, proof_scope), live) for condition in assessed['conditions']):
            raise ERROR('P_PROOF', 'Local review conditions have lost current applicability')

    def _local_qualification(self, reference, scope, live, replacement=None):
        """Qualify one candidate against direct facts and its exact local reviews."""
        record = self.resolve(reference)
        point = self._point(reference, scope)
        if self.versions[reference['version_id']]['kind'] != 'delivery.product':
            if not self._governing_input(point, live):
                raise ERROR('P_PROOF', 'Selected input has no current governing use')
            return
        if self._status(point)['validity'] in {'invalid', 'revoked'} or self._held(point):
            raise ERROR('P_PROOF', 'Cancelled or held current use requires explicit restoration')
        for parent in self._governing_dependencies(point):
            if not self._governing_input(parent, live):
                raise ERROR('P_PROOF', 'Candidate has no current direct governing input')
        previous = self.scope
        self.scope = scope
        try:
            if record['product_kind'] in {'answer', 'bundle', 'final_result', 'observation'}:
                supports = self._product_requirements(record, live)
            else:
                supports = []
            self._material(record, live)
            role = {'answer': 'professional_review', 'bundle': 'integration_review',
                    'handoff': 'receiving_acceptance', 'final_result': 'integration_review',
                    'observation': 'professional_review'}.get(record['product_kind'])
            profile = self.resolve(record['profile'], 'profile')
            obligations = [item for item in profile['obligations']
                           if item['owner'] == record['owner'] and item['role'] == role and item['subject_kind'] == record['product_kind']]
            if record['product_kind'] in {'answer', 'bundle', 'handoff', 'final_result'} and not obligations:
                raise ERROR('P_PROOF', 'Candidate lacks its mandatory local review obligation')
            for obligation in obligations:
                slot = {'kind': 'proof', 'subject': reference, 'role': role, 'slot_id': obligation['slot_id']}
                selected = replacement if replacement is not None and replacement['slot'] == slot else self.proofs.get(_proof_key(scope, slot))
                if selected is None:
                    raise ERROR('P_PROOF', 'Candidate has no exact current local review')
                proof = selected.get('candidate', selected.get('proof'))
                proof_scope = selected['proof_use_scope']
                self._current_positive_support(reference, scope, proof, proof_scope, live)
            return supports
        finally:
            self.scope = previous

    def _retired_proof(self, scope, slot, candidate):
        previous, retired = None, []
        for event in self.events:
            if event['kind'] != 'selection' or event['category'] != 'proof' or event['scope'] != scope or event['slot'] != slot:
                continue
            if previous is not None and previous != event['subject']:
                retired.append(previous)
            previous = event['subject']
        return candidate in retired and candidate != previous

    def _permissions_using(self, roots):
        affected = {self._key(point) for point in roots}
        ids, permissions, outputs = [], [], []
        for event in self.events:
            if event['kind'] not in {'accept', 'release'} or event['decision_id'] in self.decisions.get('cancelled', []):
                continue
            if not affected.intersection(self._key(point) for point in event['closure']):
                continue
            ids.append(event['decision_id'])
            permissions.append(self._point(event['decision_ref'], event['scope']))
            point = self._point(event['subject'], event['scope'])
            if point not in outputs:
                outputs.append(point)
        return {'op': 'permission-cancel', 'decision_ids': ids, 'permissions': permissions, 'outputs': outputs}

    def _derive_escalation(self, reference, record, payload, assignment, message, at):
        related = {item['slot_id']: item['refs'] for item in record['related']}
        if related.get('conflicts') != payload['conflicts']:
            raise ERROR('P_CONTEXT', 'Escalation cannot erase recorded conflicts')
        metadata = record['episode']
        heads = {ZERO, self.head, *(transaction['hash'] for transaction in self.transactions)}
        if metadata['collection_head'] not in heads:
            raise ERROR('P_HEAD', 'Escalation collection head must identify an accepted journal prefix')
        layer, scope = assignment['owner']['layer'], message['scope']
        for conflict in payload['conflicts']:
            body = self.resolve(conflict)
            owner = body.get('owner', {})
            if owner.get('layer') != layer or owner.get('work_item') != assignment['owner']['work_item']:
                raise ERROR('P_SCOPE', 'A local package preserves attributable conflicts of this work layer')
        for unfinished in metadata['unfinished']:
            body = self.resolve(unfinished, 'assignment')
            if body['owner']['layer'] != layer or body['use_scope'] != scope:
                raise ERROR('P_SCOPE', 'Unfinished collection work must belong to this exact layer scope')
        if metadata['root'] is None:
            if metadata['previous'] is not None or any(item['scope'] == scope and item['layer'] == layer
                    and self.escalations.get(item['root']['version_id']) == 'open' for item in self.episodes.values()):
                raise ERROR('P_CONFLICT', 'One explicit open escalation episode governs a layer scope')
            root = reference
            prior_conflicts = []
            rounds = 1
        else:
            episode = self._episode(metadata['root'])
            if (self.escalations.get(episode['root']['version_id']) != 'open'
                    or episode['current'] != metadata['previous'] or episode['layer'] != layer or episode['scope'] != scope):
                raise ERROR('P_HEAD', 'Escalation revision must extend its exact current episode revision')
            root = episode['root']
            prior_conflicts = self.resolve(episode['current'])['related']
            prior_conflicts = next((item['refs'] for item in prior_conflicts if item['slot_id'] == 'conflicts'), [])
            rounds = len(episode['revisions']) + 1
        settings = self.resolve(record['profile'], 'profile')['scheduling']
        if rounds > settings['max_escalation_rounds'] or any(item not in payload['conflicts'] for item in prior_conflicts):
            raise ERROR('P_BUDGET', 'Escalation revisions must preserve conflicts within the finite round bound')
        affected = self._affected(payload['affected'])
        affected_ids = {point['ref']['version_id'] for point in affected}
        members = []
        effects = []
        for identifier, value in self.versions.items():
            if value['kind'] != 'delivery.assignment':
                continue
            body = value['content']['record']
            relevant = body['use_scope'] == scope and body['owner']['layer'] == layer or identifier in affected_ids
            if relevant and body.get('handling') is None and self.assignment_states.get(identifier) in {'open', 'paused'}:
                point = self._point(self._reference(identifier), body['use_scope'])
                members.append(point)
                if self.assignment_states[identifier] == 'open':
                    effects.append({'op': 'assignment', 'subject': identifier, 'state': 'paused'})
        import governed_local_budget
        suspended = set()
        for point in members:
            binding = self.local_budget['bindings'][point['ref']['version_id']]
            for phase in ('planning', 'question', 'integration'):
                key = governed_local_budget._unit_id(binding['anchor'], phase, binding['scope'])
                if key in self.local_budget['units'] and key not in suspended:
                    effects.extend(governed_local_budget._idle(self, key, at, 'semantic_pause'))
                    suspended.add(key)
        effects.append({'op': 'episode', 'root': root, 'revision': reference, 'scope': scope,
                        'layer': layer, 'work_item': assignment['owner']['work_item'],
                        'members': sorted({canonical(point): point for point in affected + members}.values(), key=canonical),
                        'collect_until_ms': at + settings['collection_window_ms'],
                        'control_until_ms': self._generation(record['assignment'])[1]['deadline_ms'],
                        'decisive': metadata['decisive'], 'attempt': self._attempt_ref(record['assignment'])})
        return effects

    def _resolve_episode(self, payload, origin, assignment, authority, scope):
        episode = self._episode(payload['escalation'])
        if (self.escalations.get(episode['root']['version_id']) != 'open'
                or payload['package'] != episode['current'] or scope != episode['scope']):
            raise ERROR('P_HEAD', 'Owner response must cover the exact current open package revision')
        human_reached = episode['layer'] == 1 or any(event['kind'] == 'relay' and event['payload'].get('episode') == episode['root'] and event['payload'].get('to_layer') == 0 for event in self.events)
        if origin['kind'] == 'authority' and human_reached:
            if authority is None or authority['purpose'] != 'delivery-change':
                raise ERROR('P_SCOPE', 'The L1 owner response belongs to actual signed L0 authority')
        elif (assignment is None or assignment.get('handling', {}).get('task') != 'resolve'
                or assignment['handling']['episode'] != episode['root']
                or assignment['owner']['layer'] >= episode['layer']):
            raise ERROR('P_SCOPE', 'Owner response requires an entitled upward handling mandate')
        conflicts = next((item['refs'] for item in self.resolve(episode['current'])['related'] if item['slot_id'] == 'conflicts'), [])
        if payload['conflicts'] != conflicts or not payload['impacts']:
            raise ERROR('P_PROOF', 'Owner response must explicitly cover every current conflict and impact')
        points = [canonical(item['subject']) for item in payload['impacts']]
        if len(points) != len(set(points)):
            raise ERROR('P_CONFLICT', 'Owner impact coverage cannot contain competing dispositions')
        allowed = {self._key(point) for point in episode['members']}
        allowed.update(key for key, hold in self.holds.items() if hold['episode'] == episode['root'])
        for item in payload['impacts']:
            self.resolve(item['subject']['ref'])
            if self._key(item['subject']) not in allowed:
                raise ERROR('P_SCOPE', 'Impact coverage is limited to exact affected episode uses and held records')
        for decision in payload['decisions']:
            value = self.resolve(decision)
            if self.versions[decision['version_id']]['kind'] != 'delivery.decision' or self._status(decision, scope)['validity'] != 'valid':
                raise ERROR('P_PROOF', 'Referenced owner changes must be actual current recorded decisions')
            if value['message']['scope'] != scope:
                raise ERROR('P_SCOPE', 'Owner changes must preserve their exact affected scope')
        return {'op': 'event', 'kind': 'owner-resolution', 'payload': payload}

    def _resolution_coverage(self, reference, resolutions, live=True):
        episode = self._episode(reference)
        if not resolutions:
            raise ERROR('P_PROOF', 'Complete current owner impact decisions are required')
        covered = []
        for resolution in resolutions:
            value = self.resolve(resolution)
            if (self.versions[resolution['version_id']]['kind'] != 'delivery.decision'
                    or self._status(resolution, episode['scope'])['validity'] != 'valid'):
                raise ERROR('P_PROOF', 'A withdrawn owner response cannot govern reconciliation')
            payload = value['message']['payload']
            if (payload.get('action') != 'resolve_escalation' or payload['escalation'] != episode['root']
                    or payload['package'] != episode['current']):
                raise ERROR('P_PROOF', 'New uncovered package conflicts keep the episode open')
            grants = self._revision_grant(resolution, episode['scope'])['grants']
            self._governing_grants({'decision_ref': resolution, 'scope': episode['scope'], 'grants': grants}, live)
            covered.extend((resolution, item) for item in payload['impacts'])
        return covered

    def _restore_product(self, reference, proofs, live):
        point = self._point(reference)
        latest = self._latest_cancellation(point)
        if not latest or self._status(point)['validity'] not in {'invalid', 'revoked'}:
            raise ERROR('P_STATE', 'Reinstatement requires an explicitly cancelled current use')
        accepted = []
        for proof in proofs:
            assessed = self.resolve(proof, 'assessment')
            assigned = self.resolve(assessed['assignment'], 'assignment')
            if assessed['subject'] != reference:
                continue
            if (self._subject_use(reference, assigned) != point
                    or self._status(proof, assigned['use_scope'])['validity'] != 'valid'
                    or self.provenance[proof['version_id']]['sequence'] <= latest
                    or assessed['verdict'] not in {'supported', 'supported_with_conditions', 'accepted'}):
                raise ERROR('P_PROOF', 'Reinstatement requires a fresh independent positive proof after cancellation')
            self._assessment(assessed, assigned, live)
            if any(not self._governing_input(self._point(condition, assigned['use_scope']), live) for condition in assessed['conditions']):
                raise ERROR('P_PROOF', 'Reinstatement conditions are not currently fulfilled')
            accepted.append(proof)
        if not accepted:
            raise ERROR('P_PROOF', 'Each restored product requires its exact fresh current assessment')

    def _read_return(self, blob_id, live):
        artifacts = dict(self.return_artifact or {})
        if blob_id in artifacts:
            raw = artifacts[blob_id].encode('utf-8')
        elif self.blob_reader is not None:
            raw = self.blob_reader(blob_id)
        else:
            raise ERROR('P_CONTEXT', 'Exact execution return artifact is unavailable')
        if blob(raw) != blob_id:
            raise ERROR('P_IDENTITY', 'Execution return blob differs from captured completion')
        value = loads(raw)
        if canonical(value) != raw:
            raise ERROR('P_PARSE', 'RunReturn must be exact canonical semantic JSON')
        wire.validate(value, 'run-return.schema.json')
        artifacts[blob_id] = raw.decode('utf-8')
        self.return_artifact = artifacts
        return value

    def _usage_effect(self, payload, details, final):
        totals = payload['usage']
        units = [(item['metric'], item['unit']) for item in totals]
        if payload['observed_at_ms'] < details.get('last_observed_at_ms', 0):
            raise ERROR('P_EXPIRED', 'Usage observation time cannot move backwards')
        if len(units) != len(set(units)):
            raise ERROR('P_BUDGET', 'Cumulative usage units must be unique')
        reserved = {(item['metric'], item['unit']): item['ceiling'] for item in details['limits']}
        if final and set(units) != set(reserved):
            raise ERROR('P_BUDGET', 'Every reserved metric must be accounted before release')
        if any(unit not in reserved for unit in units):
            raise ERROR('P_BUDGET', 'Usage must retain issued metric and units')
        previous = details['usage']
        for item in totals:
            key = item['metric'] + ':' + item['unit']
            if item['total'] < previous.get(key, 0):
                raise ERROR('P_BUDGET', 'Measured cumulative usage cannot decrease')
        return {'op': 'usage', 'run_id': payload['run_id'], 'totals': totals, 'final': final, 'observed_at_ms': payload['observed_at_ms']}

    def _apply_usage(self, effect):
        details = self.run_details[effect['run_id']]
        scope = details['context']['scope']
        details['last_observed_at_ms'] = effect['observed_at_ms']
        for item in effect['totals']:
            key = item['metric'] + ':' + item['unit']
            prior = details['usage'].get(key, 0)
            delta = item['total'] - prior
            usage = self.usage.setdefault((scope, item['metric'], item['unit']), {'spent': 0, 'reserved': 0})
            invocation = self.invocations.get(details.get('invocation_id'))
            if invocation is not None:
                physical_prior = invocation['usage'].get(key, 0)
                usage['spent'] += max(0, item['total'] - physical_prior)
                invocation['usage'][key] = max(physical_prior, item['total'])
            else:
                usage['spent'] += delta
            details['usage'][key] = item['total']
            limit = next(limit for limit in details['limits'] if limit['metric'] == item['metric'] and limit['unit'] == item['unit'])
            if item['total'] > limit['ceiling']:
                self._admit_event({'kind': 'budget-overrun', 'run_id': effect['run_id'], 'metric': item['metric'], 'unit': item['unit'], 'total': item['total'], 'ceiling': limit['ceiling']})
        if effect['final'] and not details['reservation_released']:
            invocation = self.invocations.get(details.get('invocation_id'))
            if invocation is None or not invocation['reservation_released']:
                for limit in details['limits']:
                    usage = self.usage.setdefault((scope, limit['metric'], limit['unit']), {'spent': 0, 'reserved': 0})
                    usage['reserved'] -= limit['ceiling']
                if invocation is not None:
                    invocation['reservation_released'] = True
            details['reservation_released'] = True

    def _native_packet(self, context_ref, context, binding, execution, delivery, live):
        """Validate immutable member packet and disclosed resources before dispatch."""
        raw = self._validation_bytes(binding['packet_blob_id'], live)
        packet = loads(raw)
        if (not isinstance(packet, dict) or canonical(packet) != raw or packet.get('protocol') != 'jai.process/1'
                or packet.get('operation') != 'input' or packet.get('context') != context_ref
                or packet.get('assignment') != context['assignment'] or packet.get('run_id') != context['run_id']
                or packet.get('manifest_hash') != binding['manifest_hash']
                or _hash({name: value for name, value in packet.items() if name != 'manifest_hash'}) != binding['manifest_hash']):
            raise ERROR('P_ORIGIN', 'Native packet does not bind the exact issued execution')
        if (binding['packet_bytes'] > binding['total_bytes'] or len(raw) > binding['packet_bytes']
                or not len(raw) <= binding['transferred_bytes'] <= binding['total_bytes']):
            raise ERROR('P_BUDGET', 'Native initial packet exceeds its exact transport allowance')
        handles = {}
        for item in packet['manifest']:
            if _typed_key(item['record']) != _typed_key(self.resolve(item['ref'])):
                raise ERROR('P_IDENTITY', 'Native record handle differs from its admitted immutable record')
            handles[item['handle']] = blob(canonical(item['record']))
        allowed = set()
        for item in packet['attachments']:
            prior = handles.get(item['handle'])
            if prior is not None and prior != item['blob_id']:
                raise ERROR('P_CONFLICT', 'Native packet contains competing read-handle identities')
            handles[item['handle']] = item['blob_id']
            allowed.add(item['blob_id'])
        allowed.update(material['blob_id'] for returned in packet.get('owned_returns', [])
                       for item in returned['records'] for material in item['material'])
        handling = packet.get('handling')
        if handling is not None:
            allowed.update(material['blob_id'] for item in [handling['package'], *handling['conflicts'], *handling['inputs']]
                           for material in item['material'] if material['status'] == 'available')
        catalogue = packet.get('catalogue')
        descriptor = execution['snapshot']['descriptor']
        if catalogue != {'handle': 'catalogue', 'blob_id': descriptor['catalogue_blob_id'],
                         'instruction_prefix': 'instruction:'}:
            raise ERROR('P_SCOPE', 'Native catalogue must expose the complete intrinsic captured catalogue')
        handles['catalogue'] = descriptor['catalogue_blob_id']
        facts = {'handles': handles, 'allowed_blobs': sorted(allowed),
                 'instruction_blobs': descriptor['instruction_blobs']}
        if delivery is not None:
            if (not isinstance(delivery, dict) or set(delivery) != {'manifest_blob_id', 'prompt_blob_id'}):
                raise ERROR('P_SCHEMA', 'Host delivery must identify its exact captured manifest and prompt')
            manifest = loads(self._validation_bytes(delivery['manifest_blob_id'], live))
            prompt = loads(self._validation_bytes(delivery['prompt_blob_id'], live))
            if (not isinstance(manifest, dict) or not isinstance(prompt, dict)
                    or set(manifest) != {'context', 'manifest_hash', 'resources'}
                    or not isinstance(manifest['resources'], list)
                    or manifest['context'] != context_ref
                    or manifest['manifest_hash'] != binding['manifest_hash']
                    or prompt.get('context') != context_ref
                    or prompt.get('canonical_manifest_hash') != binding['manifest_hash']
                    or prompt.get('delivery_manifest') != 'resource:' + delivery['manifest_blob_id']
                    or prompt.get('active_provider') != binding['provider']):
                raise ERROR('P_ORIGIN', 'Host delivery differs from its exact canonical input packet')
            entitled = set(handles) | {'instruction:' + slug for slug in descriptor['instruction_blobs']}
            presentation = {'resource:' + delivery['manifest_blob_id']: delivery['manifest_blob_id']}
            for item in manifest['resources']:
                if (not isinstance(item, dict) or set(item) != {'handle', 'blob_id', 'label', 'kind',
                        'source_handles', 'runtime', 'path', 'byte_length'}
                        or not isinstance(item['blob_id'], str)
                        or not isinstance(item['source_handles'], list)
                        or any(not isinstance(source, str) for source in item['source_handles'])
                        or item['handle'] != 'resource:' + item['blob_id']
                        or item['handle'] in handles or item['handle'] in presentation):
                    raise ERROR('P_CONFLICT', 'Captured presentation handles must be distinct content identities')
                if item['kind'] == 'data':
                    if not item['source_handles'] or not set(item['source_handles']).issubset(entitled) or item['runtime'] is not None:
                        raise ERROR('P_SCOPE', 'Presentation data requires already entitled exact source handles')
                elif item['kind'] == 'procedure':
                    if item['runtime'] != 'jai.governed-native' or item['source_handles']:
                        raise ERROR('P_SCOPE', 'Procedural delivery is runtime guidance, not a new business input')
                else:
                    raise ERROR('P_SCHEMA', 'Unknown host presentation provenance')
                raw_resource = self._validation_bytes(item['blob_id'], live)
                if type(item['byte_length']) is not int or item['byte_length'] != len(raw_resource):
                    raise ERROR('P_IDENTITY', 'Captured presentation resource length differs from its bytes')
                presentation[item['handle']] = item['blob_id']
            facts['presentation_handles'] = presentation
            facts['host_delivery'] = delivery
            handles.update(presentation)
        return facts

    def _native_binding(self, payload, context, details, execution, live, invocation=None):
        """Bind an actual physical observation to already pinned member resources."""
        binding = payload['native']
        if invocation is None or details.get('invocation_id') != invocation['invocation_id']:
            raise ERROR('P_ORIGIN', 'Native work requires its exact physical invocation')
        prepared = details.get('prepared_packet')
        if (prepared is None or prepared['packet_blob_id'] != binding['packet_blob_id']
                or prepared['manifest_hash'] != binding['manifest_hash']):
            raise ERROR('P_ORIGIN', 'Actual start differs from the immutable prepared member packet')
        identity = {'assignment': context['assignment'], 'scope': payload['run_context']['scope'],
                    'actor': context['issued_to'], 'owner': context['owner']}
        return {'op': 'native-bind', 'run_id': payload['run_id'], 'binding': binding,
                'identity': identity, 'packet_facts': prepared['facts']}

    def _broker_request(self, identifier, live):
        """Decode and validate one newly observed broker frame, preserving exact bytes."""
        if identifier in self._broker_frames:
            return self._broker_frames[identifier], self.validation_assets[identifier]
        raw = self._validation_bytes(identifier, live)
        value = loads(raw)
        if canonical(value) != raw:
            raise ERROR('P_PARSE', 'Broker frame must contain exact canonical JSON')
        wire.validate(value, 'broker-request.schema.json')
        if value['operation'] == 'return':
            raise ERROR('P_SCOPE', 'A terminal return requires the ordinary run-completion event')
        self._broker_frames[identifier] = _freeze(value)
        return self._broker_frames[identifier], raw

    def _broker_right(self, context, request, at, live):
        """Authorize a new broker effect against current run facts and exact grants."""
        details = self.run_details[context['run_id']]
        if (details.get('broker_frame_overrun') or details.get('broker_bytes', 0)
                > details.get('broker_limits', {}).get('total_bytes', 33554432)):
            raise ERROR('P_BUDGET', 'The run has exhausted its finite broker transport budget')
        assignment = self.resolve(context['assignment'], 'assignment')
        if (self.run_states.get(context['run_id']) != 'running' or at >= context['expires_at_ms']
                or not self._execution_right(context['assignment'], assignment, context, at, live)
                or not self._current_inputs(assignment, live)):
            raise ERROR('P_STATE', 'New broker work requires a current running assignment')
        if request['operation'] == 'reference':
            return
        execution = self._context_execution(context, live)
        operation = request['operation']
        if operation not in execution['allowed_operations']:
            raise ERROR('P_SCOPE', 'Captured professional cannot perform this broker operation')
        if operation == 'read':
            return
        grants = [grant for grant in context['effects']
                  if grant['operation'] == operation and grant['owner'] == assignment['owner']]
        if operation == 'propose' and grants:
            return
        if operation == 'materialize':
            valid = any(grant['destination_handle'] == request['destination_handle']
                        and request['subject'] in grant['targets'] for grant in grants)
        elif operation == 'measure':
            valid = bool(request['targets']) and any(grant['tool_policy'] == request['tool_policy']
                        and all(target in grant['targets'] for target in request['targets']) for grant in grants)
        else:
            valid = False
        if not valid:
            raise ERROR('P_SCOPE', 'Broker effect differs from the exact assigned owner grant')

    def _broker_result(self, context, details, request, response, live):
        """Check an acknowledgement and derive only genuinely captured material IDs."""
        if not isinstance(response, dict) or response.get('id') != request['id'] or type(response.get('ok')) is not bool:
            raise ERROR('P_IDENTITY', 'Broker acknowledgement differs from its exact request')
        if not response['ok']:
            error = response.get('error')
            if (set(response) != {'id', 'ok', 'error'} or not isinstance(error, dict)
                    or set(error) != {'code', 'message'} or any(not isinstance(value, str) or not value for value in error.values())):
                raise ERROR('P_SCHEMA', 'Broker denial requires its closed exact diagnostic')
            return []
        if set(response) != {'id', 'ok', 'result'} or not isinstance(response['result'], dict):
            raise ERROR('P_SCHEMA', 'Broker acknowledgement requires a closed successful result')
        result, operation = response['result'], request['operation']
        shapes = {'read': {'data'}, 'propose': {'blob_id', 'size'}, 'reference': {'ref'},
                  'materialize': {'blob_id'}, 'measure': {'blob_id', 'status'}}
        if set(result) != shapes[operation]:
            raise ERROR('P_SCHEMA', 'Broker result fields differ from the exact operation')
        if operation == 'read':
            try:
                raw = base64.b64decode(result['data'], validate=True)
            except (TypeError, ValueError) as error:
                raise ERROR('P_PARSE', 'Exact base64 read bytes are required') from error
            facts = self._native_packet_facts.get(context['run_id'])
            if facts is not None:
                handle = request['handle']
                identifier = (facts['instruction_blobs'].get(handle[len('instruction:'):])
                              if handle.startswith('instruction:') else facts['handles'].get(handle))
                if identifier is None or blob(raw) != identifier:
                    raise ERROR('P_SCOPE', 'Read response is outside the bound native packet or intrinsic catalogue')
        elif operation == 'propose':
            try:
                raw = base64.b64decode(request['data'], validate=True)
            except (TypeError, ValueError) as error:
                raise ERROR('P_PARSE', 'Exact proposed bytes are required') from error
            if (type(result['size']) is not int or result['size'] != len(raw)
                    or result['blob_id'] != blob(raw) or len(raw) > details['broker_limits']['packet_bytes']):
                raise ERROR('P_IDENTITY', 'Proposed material identity must derive from the actual request bytes')
            if self._validation_bytes(result['blob_id'], live) != raw:
                raise ERROR('P_IDENTITY', 'Captured proposed material differs from its acknowledgement')
            return [result['blob_id']]
        elif operation == 'reference':
            expected = _ref(record_manifest(self.engagement, details['context']['scope'],
                                            request['logical_id'], request['record_type'], request['record']))
            if result['ref'] != expected:
                raise ERROR('P_IDENTITY', 'Reference acknowledgement differs from deterministic record identity')
        elif operation == 'materialize':
            if result['blob_id'] != request['blob_id']:
                raise ERROR('P_IDENTITY', 'Materialization acknowledgement changes the exact bytes')
            facts = self._native_packet_facts.get(context['run_id'])
            if facts is not None and result['blob_id'] not in set(facts['allowed_blobs']) | set(details.get('broker_allowed_blobs', [])):
                raise ERROR('P_SCOPE', 'Materialized bytes were not delivered or captured for this run')
        else:
            if type(result['status']) is not int:
                raise ERROR('P_SCHEMA', 'Measurement acknowledgement requires its actual integer status')
            raw = self._validation_bytes(result['blob_id'], live)
            if len(raw) > details['broker_limits']['total_bytes']:
                raise ERROR('P_BUDGET', 'Measured capture exceeds the transport bound')
            return [result['blob_id']]
        return []

    def _broker_control(self, payload, context, details, at, live):
        """Derive durable request/ack facts without repeating a possibly completed effect."""
        request, request_raw = self._broker_request(payload['request_blob_id'], live)
        operation, identifier = request['operation'], request['id']
        limits = {name: payload[name] for name in ('packet_bytes', 'total_bytes')}
        if limits['packet_bytes'] > limits['total_bytes'] or len(request_raw) > limits['packet_bytes']:
            raise ERROR('P_BUDGET', 'Broker frame exceeds its declared finite transport limits')
        established = details.get('broker_limits')
        if established is not None and established != limits:
            raise ERROR('P_BUDGET', 'A later broker frame cannot reset the run transport bounds')
        previous = details.get('broker_requests', {}).get(identifier)
        if previous is not None and previous['request_blob_id'] != payload['request_blob_id']:
            raise ERROR('P_IDEMPOTENCY', 'Broker request identity was reused for changed content')
        if payload['event'] == 'broker_requested':
            if previous is not None and previous['status'] == 'pending':
                raise ERROR('P_UNCERTAIN', 'The physical effect has an unacknowledged committed intent')
            if operation not in {'materialize', 'measure'} or previous is not None:
                raise ERROR('P_STATE', 'Only a new physical effect receives a durable intent')
            self._broker_right(context, request, at, live)
            if any(item['status'] == 'pending' for item in details.get('broker_requests', {}).values()):
                raise ERROR('P_UNCERTAIN', 'An unacknowledged physical request must be reconciled before new work')
            minimum = details.get('broker_bytes', 0) + len(request_raw)
            effect = {'op': 'broker-intent', 'run_id': payload['run_id'], 'request_id': identifier,
                      'request_blob_id': payload['request_blob_id'], 'operation': operation}
        else:
            if previous is not None and previous['status'] == 'ack':
                if previous['result_blob_id'] != payload['result_blob_id'] or payload['transferred_bytes'] != details['broker_bytes']:
                    raise ERROR('P_IDEMPOTENCY', 'Broker acknowledgement changed after it was committed')
                return []
            result_raw = self._validation_bytes(payload['result_blob_id'], live)
            frame_overrun = len(result_raw) > limits['packet_bytes']
            if frame_overrun and previous is None:
                raise ERROR('P_BUDGET', 'Broker acknowledgement exceeds the finite frame bound')
            response = loads(result_raw)
            if not isinstance(response, dict) or canonical(response) != result_raw:
                raise ERROR('P_PARSE', 'Broker acknowledgement must contain exact canonical JSON')
            if operation in {'materialize', 'measure'} and response.get('ok') is True and previous is None:
                raise ERROR('P_STATE', 'A successful physical effect requires its previously committed intent')
            if previous is None and response.get('ok') is True:
                if any(item['status'] == 'pending' for item in details.get('broker_requests', {}).values()):
                    raise ERROR('P_UNCERTAIN', 'An unacknowledged physical request prevents new broker work')
                self._broker_right(context, request, at, live)
            metadata = dict(details, broker_limits=limits)
            captured = self._broker_result(context, metadata, request, response, live)
            minimum = details.get('broker_bytes', 0) + len(result_raw) + (len(request_raw) if previous is None else 0)
            effect = {'op': 'broker-ack', 'run_id': payload['run_id'], 'request_id': identifier,
                      'request_blob_id': payload['request_blob_id'], 'result_blob_id': payload['result_blob_id'],
                      'operation': operation, 'allowed_blobs': captured, 'frame_overrun': frame_overrun}
        if payload['transferred_bytes'] < minimum:
            raise ERROR('P_BUDGET', 'Cumulative broker byte observations cannot decrease or omit the current frame')
        return [{**effect, 'limits': limits, 'transferred_bytes': payload['transferred_bytes']}]

    def invocation_traits(self, assignment_ref, phase, selection=None):
        """Describe actual compatible physical controls without issuing work.

        Args:
            assignment_ref: Exact current local job assignment.
            phase: Selection or work phase.
            selection: Current local execution plan for work; null for selection.
        Returns:
            Canonical physical compatibility fields derived from enrolled controls.
        Raises:
            ProtocolError: The exact local choice or current policy is unavailable.
        """
        import governed_invocations
        assignment = self.resolve(assignment_ref, 'assignment')
        context = {'assignment': assignment_ref, 'issued_to': assignment['assigned_actor'],
                   'effects': assignment['effects'], 'execution': {'phase': phase} if phase == 'selection'
                   else {'phase': phase, 'selection': selection}}
        return governed_invocations._controls(self, context)

    def procedure_next(self, procedure_ref, live=True):
        """Derive one ordinary owner-policy step from actual local deliveries.

        Args:
            procedure_ref: Exact current immutable configure_procedure decision.
            live: Require current dependencies for a newly executed step.
        Returns:
            A deterministic step descriptor, or waiting/owner-required facts.
        Raises:
            ProtocolError: The procedure is stale or its owner inputs no longer apply.
        """
        decision = self.resolve(procedure_ref)['message']
        plan = decision['payload']
        if plan.get('action') != 'configure_procedure':
            raise ERROR('P_SCOPE', 'Ordinary advancement requires an actual owner procedure')
        parent = self.resolve(plan['assignment'], 'assignment')
        scope = parent['use_scope']
        if (self.procedures.get((plan['assignment']['version_id'], scope)) != procedure_ref
                or self._status(procedure_ref, scope)['validity'] != 'valid'
                or not self._current_inputs(parent, live)):
            raise ERROR('P_CONTEXT', 'Only the current applicable owner procedure may advance')
        self._assignment_requirements(parent, live)
        steps = self.procedure_steps.get(procedure_ref['version_id'], {})
        children = [(self._reference(key), value['content']['record']) for key, value in self.versions.items()
                    if value['kind'] == 'delivery.assignment'
                    and value['content']['record'].get('procedure_task', {}).get('procedure') == procedure_ref]
        specification = plan['specification']
        if plan['kind'] == 'layer':
            missing = [question for question in ('what', 'why', 'how', 'who', 'where', 'when')
                       if not any(record['responsibility'] == 'setter' and record['owner']['question'] == question
                                  for _, record in children)]
            if missing:
                question = missing[0]
                return {'step': 'question:' + question, 'triggers': [procedure_ref],
                        'assignment': self._procedure_child(procedure_ref, 'setter', '/question_tasks/' + question,
                            owner={**parent['owner'], 'work_kind': 'question', 'question': question})}
            return self._procedure_layer(procedure_ref, parent, children, steps, live)
        authors = [(ref, record) for ref, record in children if record['responsibility'] == 'author']
        if not authors:
            return {'step': 'author', 'triggers': [procedure_ref],
                    'assignment': self._procedure_child(procedure_ref, 'author', '/author_task')}
        author_ref, _ = authors[0]
        deliveries = [event['payload']['candidate'] for event in self.events if event['kind'] == 'submission'
                      and self.resolve(event['payload']['candidate'], 'product')['assignment'] == author_ref]
        if len(deliveries) != 1:
            return {'waiting': 'author_result' if not deliveries else 'owner_required', 'procedure': procedure_ref}
        candidate = deliveries[0]
        reviewers = [(ref, record) for ref, record in children if record['responsibility'] == 'reviewer']
        if not reviewers:
            return {'step': 'reviewer', 'triggers': [procedure_ref, candidate],
                    'assignment': self._procedure_child(procedure_ref, 'reviewer', '/reviewer_task', candidate=candidate)}
        reviewer_ref, _ = reviewers[0]
        reviews = [event['payload']['assessment'] for event in self.events if event['kind'] == 'review'
                   and self.resolve(event['payload']['assessment'], 'assessment')['assignment'] == reviewer_ref]
        if len(reviews) != 1:
            return {'waiting': 'review_result' if not reviews else 'owner_required', 'procedure': procedure_ref}
        review = self.resolve(reviews[0], 'assessment')
        if review['verdict'] not in {'supported', 'accepted'} or review['conditions']:
            return {'waiting': 'owner_required', 'procedure': procedure_ref}
        profile = self.resolve(parent['profile'], 'profile')
        obligations = [item for item in profile['obligations'] if item['owner'] == parent['owner']
                       and item['subject_kind'] == 'answer']
        pending = []
        for item in obligations:
            if item['role'] == 'professional_review':
                slot = {'kind': 'proof', 'slot_id': item['slot_id'], 'subject': candidate, 'role': item['role']}
                previous = self.proofs.get(_proof_key(scope, slot), {}).get('proof')
                selected = reviews[0]
            elif item['role'] == 'answer' and item['required_kind'] == 'product':
                slot = {'kind': 'basis', 'slot_id': item['slot_id'], 'owner': parent['owner']}
                previous = self.selections.get(_proof_key(scope, slot))
                selected = candidate
            else:
                continue
            step = 'select:' + item['slot_id']
            if step not in steps:
                pending.append({'step': step, 'triggers': [procedure_ref, candidate, reviews[0]],
                    'decision': {'action': 'select', 'reason': 'Recorded unconditional owner procedure.',
                                 'slot': slot, 'candidate': selected, 'previous': previous}})
        pending.sort(key=lambda item: item['decision']['slot']['kind'] == 'basis')
        return pending[0] if pending else {'complete': True, 'procedure': procedure_ref}

    def _procedure_layer(self, procedure_ref, parent, children, steps, live):
        plan = self.resolve(procedure_ref)['message']['payload']
        scope = parent['use_scope']
        profile = self.resolve(parent['profile'], 'profile')
        answers = []
        for question in ('what', 'why', 'how', 'who', 'where', 'when'):
            owner = {**parent['owner'], 'work_kind': 'question', 'question': question}
            selected = [ref for (use, _), ref in self.selections.items() if use == scope
                        and self.versions[ref['version_id']]['kind'] == 'delivery.product'
                        and self.resolve(ref)['product_kind'] == 'answer' and self.resolve(ref)['owner'] == owner
                        and self._governing_input(self._point(ref, scope), live)]
            selected = list({ref['version_id']: ref for ref in selected}.values())
            if len(selected) != 1:
                return {'waiting': 'question_results' if not selected else 'owner_required', 'procedure': procedure_ref}
            answers.extend(selected)
        integrators = [ref for ref, record in children if record['responsibility'] == 'integrator']
        if not integrators:
            return {'step': 'integrator', 'triggers': [procedure_ref, *answers],
                'assignment': self._procedure_child(procedure_ref, 'integrator', '/integration_task',
                    bindings=[{'slot_id': 'reviewed_answers', 'refs': answers}])}
        bundles = [event['payload']['candidate'] for event in self.events if event['kind'] == 'submission'
                   and self.resolve(event['payload']['candidate'])['assignment'] == integrators[0]]
        if len(bundles) != 1:
            return {'waiting': 'integration_result' if not bundles else 'owner_required', 'procedure': procedure_ref}
        bundle = bundles[0]
        reviewers = [ref for ref, record in children if record['responsibility'] == 'integration_reviewer']
        if not reviewers:
            return {'step': 'integration_reviewer', 'triggers': [procedure_ref, bundle],
                'assignment': self._procedure_child(procedure_ref, 'integration_reviewer', '/review_task', candidate=bundle)}
        reviews = [event['payload']['assessment'] for event in self.events if event['kind'] == 'review'
                   and self.resolve(event['payload']['assessment'])['assignment'] == reviewers[0]]
        if len(reviews) != 1:
            return {'waiting': 'integration_review' if not reviews else 'owner_required', 'procedure': procedure_ref}
        review_ref = reviews[0]
        review = self.resolve(review_ref, 'assessment')
        if review['verdict'] not in {'supported', 'accepted'} or review['conditions']:
            return {'waiting': 'owner_required', 'procedure': procedure_ref}
        obligation = [item for item in profile['obligations'] if item['owner'] == parent['owner']
                      and item['role'] == 'integration_review' and item['subject_kind'] == 'bundle']
        if len(obligation) != 1:
            return {'waiting': 'owner_required', 'procedure': procedure_ref}
        if 'integration_proof' not in steps:
            slot = {'kind': 'proof', 'slot_id': obligation[0]['slot_id'], 'subject': bundle, 'role': 'integration_review'}
            previous = self.proofs.get(_proof_key(scope, slot), {}).get('proof')
            return {'step': 'integration_proof', 'triggers': [procedure_ref, bundle, review_ref],
                'decision': {'action': 'select', 'slot': slot, 'candidate': review_ref, 'previous': previous,
                             'reason': 'Recorded unconditional owner integration procedure.'}}
        if 'integrate' not in steps:
            return {'step': 'integrate', 'triggers': [procedure_ref, bundle, review_ref],
                    'integration': {'bundle': bundle, 'integration_review': review_ref, 'answers': answers}}
        if parent['owner']['layer'] == 6:
            return {'complete': True, 'procedure': procedure_ref, 'output': bundle}
        if 'handoff' not in steps:
            record = {'owner': parent['owner'], 'product_kind': 'handoff', 'assignment': plan['assignment'],
                'profile': parent['profile'], 'inputs': parent['inputs'],
                'material': self.resolve(bundle, 'product')['material'], 'evidence': [],
                'related': [{'slot_id': 'bundle', 'refs': [bundle]},
                            {'slot_id': 'interface', 'refs': [plan['criteria']]}],
                'limitations': self.resolve(bundle, 'product')['limitations']}
            return {'step': 'handoff', 'triggers': [procedure_ref, bundle, review_ref],
                    'handoff': {'logical_id': 'procedure-handoff:' + procedure_ref['version_id'], 'record': record}}
        handoff = steps['handoff']['resolved'][0]
        if 'receiver_entry' not in steps:
            return {'step': 'receiver_entry', 'triggers': [procedure_ref, handoff],
                    'local_entry': self.local_entry(self._point(handoff, scope), 'receiver', live=live)}
        receiver = steps['receiver_entry']['resolved'][0]
        acceptances = [event['payload']['assessment'] for event in self.events if event['kind'] == 'handoff_acceptance'
                       and self.resolve(event['payload']['assessment'])['assignment'] == receiver]
        if len(acceptances) != 1:
            return {'waiting': 'receiving_review' if not acceptances else 'owner_required', 'procedure': procedure_ref}
        acceptance = acceptances[0]
        assessment = self.resolve(acceptance, 'assessment')
        if assessment['verdict'] != 'accepted' or assessment['conditions']:
            return {'waiting': 'owner_required', 'procedure': procedure_ref}
        obligation = [item for item in profile['obligations'] if item['owner'] == parent['owner']
                      and item['role'] == 'receiving_acceptance' and item['subject_kind'] == 'handoff']
        if len(obligation) != 1:
            return {'waiting': 'owner_required', 'procedure': procedure_ref}
        if 'receiving_proof' not in steps:
            slot = {'kind': 'proof', 'slot_id': obligation[0]['slot_id'], 'subject': handoff, 'role': 'receiving_acceptance'}
            previous = self.proofs.get(_proof_key(scope, slot), {}).get('proof')
            return {'step': 'receiving_proof', 'triggers': [procedure_ref, handoff, acceptance],
                'decision': {'action': 'select', 'slot': slot, 'candidate': acceptance, 'previous': previous,
                             'reason': 'Recorded unconditional adjacent interface procedure.'}}
        if 'next_layer' not in steps:
            return {'step': 'next_layer', 'triggers': [procedure_ref, handoff, acceptance],
                    'local_entry': self.local_entry(self._point(handoff, scope), 'setter', acceptance, live)}
        return {'complete': True, 'procedure': procedure_ref, 'output': bundle}

    def _procedure_child(self, procedure_ref, responsibility, task_path, owner=None, candidate=None, bindings=()):
        plan = self.resolve(procedure_ref)['message']['payload']
        parent = self.resolve(plan['assignment'], 'assignment')
        record = copy.deepcopy(parent)
        record.update(owner=copy.deepcopy(owner or parent['owner']), responsibility=responsibility,
            assigned_actor='procedure:' + procedure_ref['version_id'] + ':' + task_path,
            issued_under=plan['assignment'], criteria=plan['criteria'],
            procedure_task={'procedure': procedure_ref, 'path': task_path})
        record.pop('handling', None)
        record['inputs'].extend(copy.deepcopy(bindings))
        profile = self.resolve(parent['profile'], 'profile')
        for obligation in profile['obligations']:
            if (obligation['owner'] == record['owner'] and obligation['role'] == 'input'
                    and not any(item['slot_id'] == obligation['slot_id'] for item in record['inputs'])):
                if obligation['required_kind'] != 'source' or not obligation['minimum'] <= 1 <= obligation['maximum']:
                    raise ERROR('P_PROOF', 'Nonstandard input mapping requires an actual owner assignment')
                record['inputs'].append({'slot_id': obligation['slot_id'], 'refs': [plan['criteria']]})
        if candidate is not None:
            record['inputs'].append({'slot_id': 'assessed-subject', 'refs': [candidate]})
        read_targets = list(dict((canonical(ref), ref) for ref in [record['criteria']] + record['inherited']
                        + [ref for binding in record['inputs'] for ref in binding['refs']]).values())
        for effect in record['effects']:
            effect['owner'] = copy.deepcopy(record['owner'])
            if effect['operation'] == 'read':
                effect['targets'] = copy.deepcopy(read_targets)
        old_paths = {item['at']: item['use_scope'] for item in parent['input_uses']}
        record['input_uses'] = [{'at': path, 'use_scope': old_paths.get(path, parent['use_scope'])}
                                for path, ref in _causal_reference_paths(record) if path != '/issued_under']
        return {'logical_id': 'procedure:' + procedure_ref['version_id'] + ':' + task_path, 'record': record}

    def _procedure_step(self, message, origin, live):
        payload = message['payload']
        expected = self.procedure_next(payload['procedure'], live)
        if payload['step'] != expected.get('step') or payload['triggers'] != expected.get('triggers'):
            raise ERROR('P_CONFLICT', 'Procedure step must match its exact current rule and actual triggers')
        plan = self.resolve(payload['procedure'])['message']['payload']
        parent = self.resolve(plan['assignment'], 'assignment')
        if 'local_entry' in expected:
            proposal = expected['local_entry']
            effects, reference = self._registration(message, origin, None, 'assignment',
                proposal['logical_id'], proposal['record'], live)
            resolved = [reference]
        elif 'integration' in expected:
            product = self.resolve(expected['integration']['bundle'], 'product')
            review = self.resolve(expected['integration']['integration_review'], 'assessment')
            if review['subject'] != expected['integration']['bundle'] or review['verdict'] not in {'supported', 'accepted'}:
                raise ERROR('P_PROOF', 'Ordinary integration requires exact unconditional actual review')
            self._complete_bundle(product, live)
            reference = expected['integration']['bundle']
            effects = [{'op': 'qualify', 'subject': reference['version_id'], 'use_scope': parent['use_scope'],
                        'decision_ref': payload['procedure']}]
            resolved = [reference]
        elif 'handoff' in expected:
            proposal = expected['handoff']
            effects, reference = self._registration(message, origin, parent, 'product',
                proposal['logical_id'], proposal['record'], live, procedure=plan)
            effects.append({'op': 'event', 'kind': 'handoff', 'payload': {'handoff': reference,
                'bundle': expected['triggers'][1], 'interface': plan['criteria']}})
            resolved = [reference]
        elif 'assignment' in expected:
            proposal = expected['assignment']
            wire.validator('record.schema.json', 'assignment').validate(proposal['record'])
            effects, reference = self._registration(message, origin, parent, 'assignment',
                proposal['logical_id'], proposal['record'], live, procedure=plan)
            resolved = [reference]
        else:
            nested = {**message, 'message_type': 'decision', 'payload': expected['decision']}
            nested['message_id'] = message_id(nested)
            effects = self._decision(nested, origin, parent, None, live)
            resolved = [self._decision_ref(nested)]
        import governed_local_budget
        if ('decision' in expected and expected['decision']['slot']['kind'] == 'basis'
                or payload['step'] in {'integrate', 'next_layer'}):
            effects.extend(governed_local_budget._idle(self, plan['assignment'], self.assessed_at_ms,
                                                      'supported:' + payload['step']))
        effects.append({'op': 'procedure-step', 'procedure': payload['procedure'], 'step': payload['step'],
                        'triggers': payload['triggers'], 'resolved': resolved, 'controller': origin})
        return effects

    def _control(self, message, origin, at, live, invocation=None):
        payload = message['payload']
        event = payload['event']
        if origin['kind'] != 'controller' or message['recipient'] != origin:
            raise ERROR('P_SCOPE', 'Host controls require the exact local controller context')
        if event.startswith('local_budget_'):
            import governed_local_budget
            return governed_local_budget.derive(self, message, origin, at, live)
        if event.startswith('invocation_'):
            import governed_invocations
            return governed_invocations.derive(self, message, origin, at, live)
        if event == 'procedure_step':
            return self._procedure_step(message, origin, live)
        if event == 'renew_control':
            profile = self.resolve(message['profile'], 'profile')
            inputs = []
            for key, reference in self.sources.items():
                if key[0] == message['scope'] and self._status(reference)['validity'] == 'valid':
                    inputs.append(reference)
            if not inputs:
                raise ERROR('P_CONTEXT', 'Renewal requires a qualified current source basis')
            body = {'owner': origin, 'assignment': None, 'profile': message['profile'], 'purpose': 'controller',
                    'run_id': 'control:' + message['request_id'], 'issued_to': origin['id'],
                    'inputs': [{'slot_id': 'current-sources', 'refs': inputs}], 'attachments': [], 'effects': [], 'execution': None,
                    'speculation': None, 'ready_basis': [],
                    'expires_at_ms': min(message['expires_at_ms'], at + profile['max_request_duration_ms'])}
            value = record_manifest(self.engagement, message['scope'], 'controller-context:' + message['scope'], 'context', body)
            if payload['profile_use'] != self._point(message['profile']) or self._status(message['profile'])['validity'] != 'valid':
                raise ERROR('P_CONTEXT', 'Renewal cannot create a new semantic profile use')
            return [{'op': 'register', 'manifest': value, 'dependencies': [self._point(ref) for ref in [message['profile']] + inputs], 'origin': origin, 'context': None}, {'op': 'qualify', 'subject': version_id(value)}]
        context = self.resolve(payload['run_context'], 'context')
        if context['assignment'] is None or payload['run_id'] != context['run_id'] or payload['run_context']['scope'] != message['scope']:
            raise ERROR('P_SCOPE', 'Control event does not identify an exact owned execution run')
        details = self.run_details.get(payload['run_id'])
        if details is None or details['context'] != payload['run_context']:
            raise ERROR('P_STATE', 'Execution context has not been issued')
        if (details.get('invocation_id') in self.invocations
                and self.invocations[details['invocation_id']]['provider'] in {'codex', 'claude'} and invocation is None
                and event in {'run_started', 'run_completed', 'run_cancelled'}):
            raise ERROR('P_SCOPE', 'Physical native members advance only through their exact invocation')
        profile = self._profile(message)
        observed = payload['observed_at_ms']
        lower = details.get('started_at_ms', details['issued_at_ms'])
        if observed < lower or observed > at + profile['max_clock_skew_ms']:
            raise ERROR('P_EXPIRED', 'Host observation lies outside the exact execution interval')
        status = self.run_states[payload['run_id']]
        if event != 'run_started':
            binding = details.get('native')
            if (binding is not None and payload.get('native_handle') != binding['handle']
                    or binding is None and 'native_handle' in payload):
                raise ERROR('P_ORIGIN', 'Host observation differs from its established native handle')
        if event in {'broker_requested', 'broker_observed'}:
            return self._broker_control(payload, context, details, at, live)
        if event == 'run_started':
            execution = self._context_execution(context, live)
            if not set(context['ready_basis']).issubset(self.ready_basis(context['assignment'], at)):
                raise ERROR('P_CONTEXT', 'A captured ready fact changed before actual delivery')
            assigned = self.resolve(context['assignment'], 'assignment')
            attempt = self._attempt_ref(context['assignment'])
            if profile['scheduling']['max_search_steps'] is not None and self.search_steps.get(attempt['version_id'], 0) >= profile['scheduling']['max_search_steps']:
                raise ERROR('P_BUDGET', 'Finite attempt search-step allowance is exhausted')
            if status != 'issued' or at >= context['expires_at_ms'] or not self._execution_right(context['assignment'], assigned, context, at, live) or not self._current_inputs(assigned, live):
                raise ERROR('P_STATE', 'Only an open issued run may actually start')
            effects = [{'op': 'run', 'run_id': payload['run_id'], 'state': 'running', 'started_at_ms': observed},
                       {'op': 'search-step', 'attempt': attempt}]
            import governed_local_budget
            effects.extend(governed_local_budget._activate(self, details['local_unit_id'], observed,
                assigned['responsibility'] + ':' + context['execution']['phase']))
            if context['execution']['phase'] == 'work':
                for planning_id in self.local_budget['bindings'][context['assignment']['version_id']]['planning_ancestors']:
                    planning = self.local_budget['units'][planning_id]
                    if not planning['downstream_started']:
                        effects.append({'op': 'local-update', 'unit_id': planning_id, 'value': {
                            'downstream_started': True, 'revision': planning['revision'] + 1}})
            if 'native' in payload:
                effects.append(self._native_binding(payload, context, details, execution, live, invocation))
            return effects
        if event == 'usage_audit':
            return [self._usage_effect(payload, details, False)]
        if event == 'run_cancelled':
            if status not in {'issued', 'running'}:
                raise ERROR('P_STATE', 'Terminal run cannot be cancelled again')
            return [self._usage_effect(payload, details, True), {'op': 'run', 'run_id': payload['run_id'], 'state': 'cancelled'}]
        if event != 'run_completed':
            raise ERROR('P_SCHEMA', 'Unsupported host control event')
        if status in {'returned', 'quarantined'}:
            raise ERROR('P_STATE', 'Execution run already has a terminal completion')
        if status == 'issued':
            raise ERROR('P_STATE', 'An execution must actually start before completion')
        usage = self._usage_effect(payload, details, True)
        target = self.resolve(context['assignment'], 'assignment')
        try:
            right = self._execution_right(context['assignment'], target, context, at, live=False)
        except ERROR:
            right = False
        current = (status == 'running' and right
                   and at < context['expires_at_ms']
                   and self._status(payload['run_context'], message['scope'])['validity'] == 'valid'
                   and self._current_inputs(target, live=False))
        if current:
            try:
                self._context_execution(context, live=False)
            except ERROR:
                current = False
        overrun = any(item['total'] > next(limit['ceiling'] for limit in details['limits'] if limit['metric'] == item['metric'] and limit['unit'] == item['unit']) for item in payload['usage'])
        transport_overrun = (details.get('broker_frame_overrun', False) or details.get('broker_bytes', 0)
                             > details.get('broker_limits', {}).get('total_bytes', 33554432))
        if not current or payload['return_blob_id'] is None or overrun or transport_overrun:
            effects = [usage, {'op': 'quarantine', 'run_id': payload['run_id'], 'return_blob_id': payload['return_blob_id'], 'reason': 'No current admissible semantic result'}]
            if status == 'running':
                effects.append({'op': 'run', 'run_id': payload['run_id'], 'state': 'quarantined'})
            if overrun and self.assignment_states.get(context['assignment']['version_id']) == 'open':
                effects.append({'op': 'assignment', 'subject': context['assignment']['version_id'], 'state': 'paused'})
            return effects
        if any(item['status'] == 'pending' for item in details.get('broker_requests', {}).values()):
            raise ERROR('P_UNCERTAIN', 'An unacknowledged physical request prevents semantic completion')
        # Transient live material/enrollment failures cannot become durable
        # quarantine facts that historical replay would derive differently.
        if live:
            if not self._execution_right(context['assignment'], target, context, at, live=True) or not self._current_inputs(target, live=True):
                raise ERROR('P_CONTEXT', 'Current required input material or authority is unavailable')
            self._context_execution(context, live=True)
        package = self._read_return(payload['return_blob_id'], live)
        if package['assignment'] != context['assignment'] or package['context'] != payload['run_context']:
            raise ERROR('P_ORIGIN', 'RunReturn differs from the actual issued assignment and context')
        if context['execution']['phase'] == 'selection':
            if (package['records'] or len(package['intents']) != 1
                    or package['intents'][0]['message_type'] != 'decision'
                    or package['intents'][0]['payload'].get('action') != 'select_execution'):
                raise ERROR('P_SCOPE', 'A selection return contains one local choice and no domain records')
            intent = package['intents'][0]
            origin_producer = {'kind': 'assignment', 'ref': context['assignment']}
            nested = {**message, 'sender': origin_producer, 'context': payload['run_context'],
                      'message_type': 'decision', 'recipient': intent['recipient'], 'payload': intent['payload'],
                      'request_id': message['request_id'] + ':intent:0'}
            nested['message_id'] = message_id(nested)
            wire.validate(nested)
            selected = self.derive(nested, origin_producer, at, None, live=live, _returned=True)
            return selected + [usage, {'op': 'run', 'run_id': payload['run_id'], 'state': 'returned'}]
        allowed_records = {'setter': {'source', 'assignment', 'product'}, 'author': {'product'},
            'reviewer': {'assessment', 'product'}, 'integration_reviewer': {'assessment', 'product'},
            'integrator': {'product'}, 'receiver': {'assessment', 'product'}, 'measurement': {'product'}}
        allowed_intents = {'setter': {'assignment', 'decision', 'handoff', 'relay'}, 'author': {'submission'},
            'reviewer': {'review'}, 'integration_reviewer': {'review'}, 'integrator': {'submission', 'integration', 'handoff', 'escalation', 'relay'},
            'receiver': {'handoff_acceptance'}, 'measurement': {'observation'}}
        role = target['responsibility']
        common = {'information_request', 'information_response', 'change_request'}
        intents = package['intents']
        if role != 'setter' and len(intents) != 1 or any(intent['message_type'] not in {'assignment', 'decision'} for intent in intents[:-1]):
            raise ERROR('P_SCOPE', 'Only an actual setter may prefix typed local assignments or decisions')
        shadow = self._fork()
        origin_producer = {'kind': 'assignment', 'ref': context['assignment']}
        base = {**message, 'sender': origin_producer, 'context': payload['run_context']}
        effects = []
        for proposal in package['records']:
            family, record = proposal['record_type'], proposal['record']
            if family not in allowed_records[role]:
                raise ERROR('P_SCOPE', 'Run responsibility cannot produce this record family')
            if family == 'source' and (role != 'setter' or record['source_role'] != 'criteria' or record['owner'] != target['owner']):
                raise ERROR('P_SCOPE', 'A returned source must be local setter criteria')
            if family == 'product':
                allowed_products = {'setter': {'handoff'}, 'author': {'answer'}, 'reviewer': {'finding'},
                    'integration_reviewer': {'finding'}, 'integrator': {'bundle', 'handoff', 'escalation', 'final_result'},
                    'receiver': {'finding'}, 'measurement': {'observation'}}
                if record['product_kind'] not in allowed_products[role]:
                    raise ERROR('P_SCOPE', 'Returned product exceeds issued responsibility')
            nested = {**base, 'message_type': 'record_proposal', 'payload': proposal}
            candidate, _ = shadow._registration(nested, origin_producer, target, family, proposal['logical_id'], record, live)
            shadow._apply(candidate, nested, {}, None)
            effects.extend(candidate)
        terminal = None
        for index, intent in enumerate(intents):
            kind = intent['message_type']
            if kind not in allowed_intents[role] | common:
                raise ERROR('P_SCOPE', 'Returned intent exceeds original producer responsibility')
            if kind == 'decision' and intent['payload']['action'] not in {'configure_procedure', 'rework', 'reformulate', 'select', 'invalidate', 'reinstate', 'terminate', 'resolve_escalation'}:
                raise ERROR('P_SCOPE', 'Leaf return cannot authorize reserved human or operator actions')
            nested = {**base, 'message_type': kind, 'recipient': intent['recipient'], 'payload': intent['payload'],
                      'request_id': message['request_id'] + ':intent:' + str(index)}
            nested['message_id'] = message_id(nested)
            wire.validate(nested)
            candidate = shadow.derive(nested, origin_producer, at, None, live=live, _returned=True)
            candidate = [item for item in candidate if item['op'] not in {'run'}]
            shadow._apply(candidate, nested, {}, None)
            effects.extend(candidate)
            terminal = kind
        if role != 'setter' and terminal not in {'information_request', 'change_request', 'escalation'}:
            final_state = shadow.assignment_states.get(context['assignment']['version_id'])
            if final_state == 'open' or final_state == 'paused' and context['speculation'] is not None:
                effects.append({'op': 'assignment', 'subject': context['assignment']['version_id'], 'state': 'completed'})
                if role == 'receiver':
                    # Terminal receiving work ends its standalone operational
                    # window for any verdict; it does not accept the handoff.
                    import governed_local_budget
                    effects.extend(governed_local_budget._idle(shadow,
                        shadow.run_details[context['run_id']]['local_unit_id'], at, 'receiver_complete'))
        if context['speculation'] is not None:
            grant = self.speculations[context['speculation']['version_id']]
            for effect in list(effects):
                if effect['op'] == 'register' and effect['manifest']['kind'] in {'delivery.source', 'delivery.assignment', 'delivery.product', 'delivery.assessment'}:
                    effects.append({'op': 'hold', 'subject': self._point(_ref(effect['manifest']), message['scope']),
                                    'episode': grant['escalation'], 'grant': context['speculation']})
        effects.append({'op': 'consumed-basis', 'assignment': context['assignment'], 'basis': context['ready_basis']})
        effects.extend([usage, {'op': 'run', 'run_id': payload['run_id'], 'state': 'returned'}])
        self.validation_assets = shadow.validation_assets
        self.validation_artifacts = shadow.validation_artifacts
        return effects

    def _question_work(self, profile, owner):
        return {item['owner']['question'] for item in profile['obligations']
                if item['owner'].get('work_kind') == 'question'
                and item['owner']['layer'] == owner['layer']
                and item['owner']['work_item'] == owner['work_item']}

    @_within_assessment
    def _complete_bundle(self, bundle, live):
        profile = self.resolve(bundle['profile'], 'profile')
        if self._question_work(profile, bundle['owner']) != {'what', 'why', 'how', 'who', 'where', 'when'}:
            raise ERROR('P_PROOF', 'A transport-only profile cannot claim complete-layer integration')
        answers = next((item['refs'] for item in bundle['related'] if item['slot_id'] == 'answers'), [])
        if len(answers) != 6 or len({_hash(reference) for reference in answers}) != 6:
            raise ERROR('P_PROOF', 'A complete bundle requires exactly six distinct question answers')
        questions = set()
        dependencies = self._dependencies(bundle)
        for reference in answers:
            record = self.resolve(reference, 'product')
            points = [point for point in dependencies if point['ref'] == reference]
            if (record['product_kind'] != 'answer' or record['profile'] != bundle['profile']
                    or record['owner']['work_kind'] != 'question'
                    or any(record['owner'][key] != bundle['owner'][key] for key in ('layer', 'work_item'))
                    or len(points) != 1 or not self._governing_input(points[0], live)):
                raise ERROR('P_PROOF', 'Every bundled answer must be current, selected and in the exact work scope')
            questions.add(record['owner']['question'])
        if questions != {'what', 'why', 'how', 'who', 'where', 'when'}:
            raise ERROR('P_PROOF', 'All six exact question answers are required for integration')

    def _decision(self, message, origin, assignment, authority, live):
        payload, scope = message['payload'], message['scope']
        action = payload['action']
        effects = []
        execution_context = self.resolve(message['context'], 'context') if message['context'] is not None else None
        if execution_context is not None and execution_context['speculation'] is not None and action != 'select_execution':
            raise ERROR('P_SCOPE', 'Speculative execution records pending work, not effective governing decisions')
        for reference in _references(payload):
            self.resolve(reference)
        if action in {'continue', 'accept', 'release'} or payload.get('authority_proof') is not None:
            purpose = {'continue': 'delivery-change', 'accept': 'delivery-accept', 'release': 'delivery-release'}.get(action, 'delivery-change')
            if not authority or authority['purpose'] != purpose:
                raise ERROR('P_SCOPE', 'Separate exact human capability is required')
            human_id = authority['identity']
            used = self.human_uses.get(human_id)
            if used and used != (scope, message['request_id']):
                raise ERROR('P_IDEMPOTENCY', 'Signed human act already consumed by another request')
            effects.append({'op': 'human-use', 'identity': human_id, 'scope': scope, 'request_id': message['request_id']})
        elif action not in {'speculate', 'resume', 'select_execution', 'resolve_escalation'} and (not assignment or assignment['responsibility'] != 'setter'):
            raise ERROR('P_SCOPE', 'Owned semantic decision requires its assigned setter')
        if action == 'speculate' and (authority is None or authority['purpose'] != 'delivery-change'):
            raise ERROR('P_SCOPE', 'Speculation requires exact explicit signed L0 acceptance of bounded wasted-work risk')
        if action == 'exclude_content':
            import governed_sabsa
            point = self.content_policy(message['profile'])
            source = self.resolve(payload['content_policy'], 'source')
            if (authority is None or authority['purpose'] != 'delivery-change'
                    or origin != source['owner'] or authority['signer'] != source['owner'].get('id')
                    or point is None or point['ref'] != payload['content_policy']):
                raise ERROR('P_SCOPE', 'Content exclusion requires its exact current policy owner and explicit signed L0 act')
            selected = governed_sabsa._policy(self, message['profile'], scope, live)
            keys = {item['key'] for item in selected[1]['required_units'] + selected[1]['required_relations']}
            if not set(payload['obligations']) <= keys:
                raise ERROR('P_SCOPE', 'Content exclusion cannot authorize undeclared obligations')
            effects.append({'op': 'event', 'kind': 'content-exclusion',
                            'payload': {**payload, 'human_key_id': authority['key_id']}})
        elif action == 'select_execution':
            import governed_routing
            context = self.resolve(message['context'], 'context')
            if (not assignment or payload['assignment'] != message['sender'].get('ref')
                    or context['execution'] != {'phase': 'selection'}):
                raise ERROR('P_SCOPE', 'Only the actual local selection run may choose its own execution')
            available = self._assignment_routing(assignment, live)
            governed_routing.select_execution(assignment, available['snapshot'], payload)
            if payload['previous'] != self.execution_plans.get((payload['assignment']['version_id'], scope)):
                raise ERROR('P_CONFLICT', 'Execution plan must replace its exact current predecessor')
            effects.append({'op': 'execution-plan', 'assignment': payload['assignment'],
                            'scope': scope, 'decision_ref': self._decision_ref(message)})
            effects.append({'op': 'event', 'kind': 'execution-choice', 'payload': payload})
        elif action == 'configure_procedure':
            if payload['assignment'] != message['sender'].get('ref'):
                raise ERROR('P_SCOPE', 'Only the assigned owner may configure its own procedure')
            criteria = self.resolve(payload['criteria'], 'source')
            expected_kind = 'question' if assignment['owner']['work_kind'] == 'question' else 'layer'
            if (payload['kind'] != expected_kind or criteria['source_role'] != 'criteria'
                    or criteria['owner'] != assignment['owner']
                    or criteria.get('origin') != {'kind': 'assignment', 'ref': payload['assignment']}):
                raise ERROR('P_SCOPE', 'Procedure requires actual locally authored criteria and its exact owner kind')
            if not wire.validator('decision.schema.json', expected_kind + '_procedure').is_valid(payload['specification']):
                raise ERROR('P_SCHEMA', 'Procedure specification must match its exact owner kind')
            if payload['previous'] != self.procedures.get((payload['assignment']['version_id'], scope)):
                raise ERROR('P_CONFLICT', 'Procedure must replace its exact current predecessor')
            if payload['previous'] is not None:
                import governed_local_budget
                effects.extend(governed_local_budget._rework(self, self.run_details[execution_context['run_id']]['local_unit_id']))
                effects.append({'op': 'cancel', 'subjects': self._affected([self._point(payload['previous'], scope)]),
                                'decision': message_id(message)})
            effects.append({'op': 'procedure', 'assignment': payload['assignment'], 'scope': scope,
                            'criteria': payload['criteria']})
            if payload['kind'] == 'layer' and payload['previous'] is None:
                import governed_local_budget
                effects.extend(governed_local_budget._idle(self, self.run_details[execution_context['run_id']]['local_unit_id'],
                    at_ms=self.assessed_at_ms, stage='planning_complete'))
        elif action in {'continue', 'reformulate', 'rework'}:
            if action in {'rework', 'reformulate'} and assignment is not None:
                import governed_local_budget
                effects.extend(governed_local_budget._rework(self, self.run_details[execution_context['run_id']]['local_unit_id']))
            replacements = payload.get('replacements', [{'previous': payload.get('subject', payload.get('assignment')), 'replacement': payload.get('replacement')}])
            for pair in replacements:
                old, new = self.resolve(pair['previous']), self.resolve(pair['replacement'])
                if old['owner'] != new['owner']:
                    raise ERROR('P_SCOPE', 'Replacement cannot transfer semantic ownership')
                if action == 'continue' and any(self.versions[ref['version_id']]['kind'] != 'delivery.source' for ref in pair.values()):
                    raise ERROR('P_SCOPE', 'Continuation cannot manufacture derived answers or reviews')
                if action == 'continue' and pair['previous'] not in [reference for (selected_scope, _), reference in self.sources.items() if selected_scope == scope]:
                    raise ERROR('P_CONFLICT', 'Continuation must replace the exact currently governing source')
                if action == 'continue' and self._status(pair['replacement'])['validity'] in {'invalid', 'revoked'}:
                    raise ERROR('P_STATE', 'An invalidated predecessor requires explicit reinstatement before selection')
                if old['owner'].get('kind') == 'authority':
                    if not authority or authority['signer'] != old['owner']['id']:
                        raise ERROR('P_SCOPE', 'L0-reserved meaning requires its actual owner')
                elif assignment and assignment['owner'] != old['owner']:
                    raise ERROR('P_SCOPE', 'Foreign-owner change must use adjacent owner routing')
                elif origin['kind'] == 'controller' and action != 'continue':
                    # A controller can record an owner act, but cannot invent its semantic approval.
                    if self.provenance[pair['replacement']['version_id']]['origin']['kind'] != 'assignment':
                        raise ERROR('P_SCOPE', 'Replacement lacks actual entitled owner authorship')
                if action in {'rework', 'reformulate'}:
                    if canonical(old) == canonical(new):
                        raise ERROR('P_CONFLICT', 'Reformulation/rework must create a genuinely distinct record')
                if action == 'rework':
                    if self.versions[pair['previous']['version_id']]['kind'] != 'delivery.assignment':
                        raise ERROR('P_CONTEXT', 'Rework targets an assignment')
                    for key in ('inherited', 'criteria', 'profile'):
                        if old[key] != new[key]:
                            raise ERROR('P_SCOPE', 'Rework cannot change governing meaning')
                if action in {'rework', 'reformulate'}:
                    self._preserved_findings(pair['previous'], payload)
                    if self.versions[pair['previous']['version_id']]['kind'] == 'delivery.assignment':
                        if old['use_scope'] != scope or new.get('use_scope') != scope:
                            raise ERROR('P_SCOPE', 'Assignment revision must preserve its exact authorized use scope')
                        self._reviewer_support(old, live)
                        if self._status(pair['replacement'], scope)['validity'] != 'valid':
                            raise ERROR('P_STATE', 'A revision cannot implicitly restore a cancelled replacement')
                        effects.append({'op': 'event', 'kind': 'revision-lineage',
                                        'payload': {'previous': pair['previous'], 'replacement': pair['replacement']}})
                affected = self._affected([pair['previous']])
                effects.append({'op': 'cancel', 'subjects': affected, 'decision': message_id(message)})
                if action == 'continue':
                    self._material(new, live)
                    effects.append({'op': 'qualify', 'subject': pair['replacement']['version_id']})
                    effects.append({'op': 'source-select', 'previous': pair['previous'], 'replacement': pair['replacement']})
            effects.append({'op': 'event', 'kind': 'decision', 'payload': payload})
        elif action == 'select':
            candidate = payload['candidate']
            if self._held(self._point(candidate, scope)):
                raise ERROR('P_PROOF', 'Unreconciled speculative work cannot justify current selection')
            record = self.resolve(candidate)
            slot = payload['slot']
            governing = self._profile(message)
            obligations = [item for item in governing['obligations'] if item['slot_id'] == slot['slot_id']]
            if not obligations:
                raise ERROR('P_PROOF', 'Selection slot does not exist in governing profile')
            key = _proof_key(scope, slot)
            table = self.selections if slot['kind'] == 'basis' else self.proofs
            old = table.get(key)
            old_ref = old if slot['kind'] == 'basis' else (old['proof'] if old else None)
            if old_ref != payload['previous']:
                raise ERROR('P_CONFLICT', 'Governing slot changed or has a competing selection')
            if slot['kind'] == 'basis':
                family = self.versions[candidate['version_id']]['kind'].removeprefix('delivery.')
                if any(item['required_kind'] != family or (family == 'product' and item['subject_kind'] != record['product_kind']) for item in obligations):
                    raise ERROR('P_PROOF', 'Selected record cannot satisfy this exact obligation kind')
                if slot['owner'] != record['owner'] or any(item['owner'] != slot['owner'] for item in obligations):
                    raise ERROR('P_SCOPE', 'Basis selector does not own this exact slot')
                qualification_supports = self._local_qualification(candidate, scope, live)
            else:
                if self.versions[candidate['version_id']]['kind'] != 'delivery.assessment':
                    raise ERROR('P_PROOF', 'Review slot requires an actual assessment')
                assessor = self.resolve(record['assignment'], 'assignment')
                proof_scope = assessor['use_scope']
                subject_use = self._subject_use(record['subject'], assessor)
                role = {'professional': 'professional_review', 'integration': 'integration_review', 'receiving': 'receiving_acceptance'}[record['assessment_kind']]
                if (slot['role'] != role or record['subject'] != slot['subject'] or subject_use['use_scope'] != scope
                        or self._status(candidate, proof_scope)['validity'] != 'valid'):
                    raise ERROR('P_PROOF', 'Proof role or subject does not qualify this slot')
                if self._status(slot['subject'], scope)['validity'] in {'invalid', 'revoked'}:
                    raise ERROR('P_PROOF', 'Cancelled subject must be explicitly reinstated before selecting its fresh proof')
                if self._retired_proof(scope, slot, candidate):
                    raise ERROR('P_PROOF', 'A superseded review disposition cannot be reused as the current proof')
                if record['verdict'] in {'supported', 'supported_with_conditions', 'accepted'} and any(not self._governing_input(self._point(condition, proof_scope), live) for condition in record['conditions']):
                    raise ERROR('P_PROOF', 'Selected assessment conditions must currently hold')
                reviewer_support = self._reviewer_support(assessor, live)
            if assignment and assignment['owner'] != obligations[0]['owner']:
                raise ERROR('P_SCOPE', 'Assigned selector does not own this profile slot')
            effect = {'op': 'select' if slot['kind'] == 'basis' else 'proof', 'scope': scope, 'slot': slot, 'candidate': candidate}
            if slot['kind'] == 'proof':
                effect['proof_use_scope'] = proof_scope
                effect['reviewer_support'] = reviewer_support
            establish = slot['kind'] == 'basis'
            if slot['kind'] == 'proof' and record['verdict'] in {'supported', 'supported_with_conditions', 'accepted'}:
                self._current_positive_support(slot['subject'], scope, candidate, proof_scope, live)
                if not self._output_obligations(self.resolve(slot['subject'])):
                    qualification_supports = self._local_qualification(slot['subject'], scope, live, effect)
                    establish = True
            if old_ref is not None and old_ref != candidate:
                roots = [self._point(old_ref, old['proof_use_scope'] if slot['kind'] == 'proof' else scope)]
                withdrawal = self._withdrawal(roots)
                lost = {self._key(point) for point in withdrawal['subjects']}
                if slot['kind'] == 'proof':
                    required = [self._point(candidate, proof_scope)]
                else:
                    required = self._governing_dependencies(self._point(candidate, scope))
                    required.extend(self._point(selected['proof'], selected['proof_use_scope'])
                                    for proof_key, selected in self.proofs.items()
                                    if proof_key[0] == scope and selected['subject'] == candidate)
                if any(self._key(point) in lost for point in required):
                    raise ERROR('P_PROOF', 'Replacement would withdraw its own required governing support')
                effects.append(withdrawal)
            elif slot['kind'] == 'proof' and record['verdict'] not in {'supported', 'supported_with_conditions', 'accepted'}:
                effects.append(self._withdrawal([self._point(slot['subject'], scope)]))
            effects.append(effect)
            if establish:
                subject = candidate if slot['kind'] == 'basis' else slot['subject']
                effects.append({'op': 'qualify', 'subject': subject['version_id'], 'use_scope': scope,
                                'requirements': qualification_supports or []})
        elif action == 'invalidate':
            for reference in payload['subjects']:
                record = self.resolve(reference)
                self._owned_decision(record, assignment, origin)
            effects.append({'op': 'cancel', 'subjects': self._affected(payload['subjects']), 'decision': message_id(message)})
        elif action == 'reinstate':
            for reference in payload['subjects']:
                record = self.resolve(reference)
                family = self.versions[reference['version_id']]['kind']
                if family == 'delivery.product':
                    self._owned_decision(record, assignment, origin)
                    self._restore_product(reference, payload['fresh_proofs'], live)
                elif family == 'delivery.source':
                    if payload['fresh_proofs']:
                        raise ERROR('P_PROOF', 'Primitive source restoration uses its actual owner and exact supporting material')
                    if record['owner'].get('kind') == 'authority':
                        if not authority or authority['purpose'] != 'delivery-change' or authority['signer'] != record['owner']['id']:
                            raise ERROR('P_SCOPE', 'Reserved source restoration requires its exact human owner')
                    else:
                        self._owned_decision(record, assignment, origin)
                    if not self._latest_cancellation(self._point(reference)):
                        raise ERROR('P_STATE', 'Source use has no explicit cancellation to restore')
                    self._material(record, live)
                    if any(parent != self._point(reference) and not self._governing_input(parent, live) for parent in self._closure(reference)):
                        raise ERROR('P_CONTEXT', 'Source prerequisites must be restored before its use')
                elif family == 'delivery.assignment':
                    self._restore_assignment(reference, record, assignment, authority, payload['fresh_proofs'], live)
                else:
                    raise ERROR('P_PROOF', 'This record type requires a fresh record rather than reviving historical proof')
                effects.append({'op': 'qualify', 'subject': reference['version_id'], 'applicable': family != 'delivery.product'})
            effects.append({'op': 'event', 'kind': 'decision', 'payload': payload})
        elif action in {'accept', 'release'}:
            result = self.assess_output_decision(payload, scope, live=live)
            effects.append({'op': action, 'subject': payload['subject'], 'closure_hash': payload['closure_hash'], 'closure': result['closure'],
                            'decision_id': message_id(message), 'authority': authority['identity']})
        elif action == 'speculate':
            if origin['kind'] not in {'controller', 'authority'} or authority is None or authority['purpose'] != 'delivery-change':
                raise ERROR('P_SCOPE', 'Explicit signed L0 control is required for speculative risk')
            episode = self._episode(payload['escalation'])
            if (self.escalations.get(episode['root']['version_id']) != 'open'
                    or episode['scope'] != scope or payload['expires_at_ms'] <= message['issued_at_ms']):
                raise ERROR('P_EXPIRED', 'Speculation requires an open exact episode and finite future expiry')
            units = [(limit['metric'], limit['unit']) for limit in payload['limits']]
            if len(units) != len(set(units)) or units != [('elapsed_ms', 'ms')]:
                raise ERROR('P_BUDGET', 'The supported speculative adapter enforces only elapsed_ms in ms')
            inputs = []
            for target in payload['assignments']:
                assigned = self.resolve(target, 'assignment')
                if (assigned['use_scope'] != scope or self.assignment_states.get(target['version_id']) != 'paused'
                        or self._point(target, scope) not in episode['members'] or assigned.get('handling') is not None
                        or assigned['deadline_ms'] is not None and payload['expires_at_ms'] > assigned['deadline_ms']):
                    raise ERROR('P_SCOPE', 'Grant coverage is exact existing paused work, not new delegated children')
                if payload['limits'][0]['ceiling'] > next((item['ceiling'] for item in assigned['limits']
                        if item['metric'] == 'elapsed_ms' and item['unit'] == 'ms'), 0):
                    raise ERROR('P_BUDGET', 'Speculation cannot enlarge the original task allowance')
                inputs.extend(self._dependencies(assigned))
            expected = sorted({canonical(point): point for point in inputs}.values(), key=canonical)
            if payload['inputs'] != expected or any(not self._governing_input(point, live) for point in expected):
                raise ERROR('P_CONTEXT', 'Signed speculation must bind every exact current governing input use')
            effects.append({'op': 'speculation', 'payload': payload, 'human_key_id': authority['key_id']})
        elif action == 'resolve_escalation':
            effects.append(self._resolve_episode(payload, origin, assignment, authority, scope))
        elif action == 'resume':
            if origin['kind'] != 'controller':
                raise ERROR('P_SCOPE', 'Only accountable host control may apply complete owner reconciliation')
            episode = self._episode(payload['escalation'])
            if self.escalations.get(episode['root']['version_id']) != 'open' or episode['scope'] != scope:
                raise ERROR('P_STATE', 'Reconciliation requires the exact open episode scope')
            coverage = self._resolution_coverage(episode['root'], payload['resolutions'], live)
            required_points = {point['ref']['version_id']: point for point in episode['members']
                               if self.versions[point['ref']['version_id']]['kind'] == 'delivery.assignment'}
            required_points.update({key[1]: self._point(self._reference(key[1]), key[0])
                                    for key, hold in self.holds.items() if hold['episode'] == episode['root']})
            affected = set(required_points)
            actual = [item['subject']['version_id'] for item in payload['reconciliation']]
            if len(actual) != len(set(actual)) or set(actual) != affected:
                raise ERROR('P_STATE', 'Reconciliation must disposition every affected assignment and held record')
            cancellation_roots = [required_points[item['subject']['version_id']]
                                  for item in payload['reconciliation'] if item['outcome'] != 'retain']
            planned_cancellations = {self._key(point) for point in self._affected(cancellation_roots)}
            retained_view = self._fork()
            for item in payload['reconciliation']:
                if item['outcome'] == 'retain':
                    retained_view.holds.pop(retained_view._key(required_points[item['subject']['version_id']]), None)
            for item in payload['reconciliation']:
                reference = item['subject']
                record = self.resolve(reference)
                point = required_points[reference['version_id']]
                impact = [value for decision, value in coverage if decision == item['impact'] and value['subject'] == point]
                if len(impact) != 1:
                    raise ERROR('P_PROOF', 'Each disposition needs exact current owner impact coverage')
                if item['outcome'] == 'retain':
                    if impact[0]['outcome'] != 'unchanged' or self.states.get(self._key(point), {}).get('validity') in {'invalid', 'revoked'}:
                        raise ERROR('P_CONTEXT', 'Changed or uncertain work cannot silently inherit acceptance')
                    closure = self._closure(point)
                    if planned_cancellations & {self._key(dependency) for dependency in closure}:
                        raise ERROR('P_CONTEXT', 'Retained work cannot depend on a use cancelled by this reconciliation')
                    if item['basis'] != closure:
                        raise ERROR('P_PROOF', 'Retention must bind the exact scoped governing closure')
                    for dependency in closure:
                        if dependency == point:
                            continue
                        if retained_view._held(dependency) or retained_view._status(dependency)['validity'] in {'invalid', 'revoked'}:
                            raise ERROR('P_CONTEXT', 'A retained result cannot depend on cancelled input versions')
                        self._material(self.resolve(dependency['ref']), live)
                    if self.versions[reference['version_id']]['kind'] == 'delivery.assignment':
                        previous_scope = retained_view.scope
                        retained_view.scope = point['use_scope']
                        try:
                            retained_view._assignment_requirements(record, live)
                        finally:
                            retained_view.scope = previous_scope
                        if self.assignment_states.get(reference['version_id']) == 'paused':
                            effects.append({'op': 'assignment', 'subject': reference['version_id'], 'state': 'open'})
                    if self._held(point):
                        effects.append({'op': 'unhold', 'subject': point})
                else:
                    effects.append({'op': 'cancel', 'subjects': self._affected([point]), 'decision': message_id(message)})
                    if self._held(point):
                        effects.append({'op': 'unhold', 'subject': point})
            effects.append({'op': 'escalation', 'subject': episode['root']['version_id'], 'state': 'resolved'})
        elif action == 'terminate':
            if authority is None:
                for reference in payload['subjects']:
                    self._owned_decision(self.resolve(reference), assignment, origin)
            else:
                for reference in payload['subjects']:
                    target = self.resolve(reference)
                    if target['owner'].get('kind') == 'authority' and authority['signer'] != target['owner']['id']:
                        raise ERROR('P_SCOPE', 'Only the exact human owner may cancel a reserved source')
            effects.append({'op': 'cancel', 'subjects': self._affected(payload['subjects']), 'decision': message_id(message)})
            for ref in payload['subjects']:
                if ref['version_id'] in self.escalations:
                    effects.append({'op': 'escalation', 'subject': ref['version_id'], 'state': 'terminated'})
        else:
            raise ERROR('P_SCHEMA', 'Unsupported decision action')
        self.scope = scope
        decision_value = self._decision_manifest(message)
        decision_ref = _ref(decision_value)
        for effect in effects:
            effect['decision_ref'] = decision_ref
            if effect['op'] == 'event':
                effect['semantic_message'] = message
        # Signed decision targets preserve provenance; their former applicability
        # is not a prerequisite of the authority act establishing a new state.
        dependencies = []
        if action == 'resolve_escalation':
            dependencies = [self._point(reference, selected_scope) for (selected_scope, _), reference in self.sources.items() if selected_scope == scope]
        elif action == 'resume':
            dependencies = [self._point(reference, scope) for reference in payload['resolutions']]
        elif action == 'speculate':
            dependencies = payload['inputs']
        elif action == 'configure_procedure':
            dependencies = [self._point(payload['criteria'], scope), self._point(payload['assignment'], scope)]
        effects.append({'op': 'decision-record', 'manifest': decision_value, 'dependencies': dependencies})
        return effects

    @_within_assessment
    def assess_output_decision(self, decision, scope, live=True):
        """Check the common output basis for signing and applying a human decision.

        Args:
            decision: Validated accept/release payload naming the exact subject,
                closure hash and, for release, current acceptance reference.
            scope: Applicability scope governed by the decision.
            live: Check current material and revocation; false only during replay.
        Returns:
            Qualified current assessment without recording or authorizing an act.
        Raises:
            ProtocolError: The action, product applicability, exact closure or
                required release acceptance does not satisfy the current basis.
        """
        if decision['action'] not in {'accept', 'release'}:
            raise ERROR('P_SCOPE', 'An output decision must accept or release')
        subject = decision['subject']
        self.resolve(subject)
        if (self.versions[subject['version_id']]['kind'] != 'delivery.product'
                or not self._governing_input(self._point(subject, scope), live)):
            raise ERROR('P_PROOF', 'Human acceptance and release require an applicable exact current output')
        result = self.evaluate(subject, scope, live=live)
        if decision['closure_hash'] != result['closure_hash'] or not result['qualified']:
            raise ERROR('P_PROOF', 'Exact current preacceptance closure is not qualified')
        if decision['action'] == 'release' and (not result['accepted']
                or decision['acceptance'] not in result['acceptances']):
            raise ERROR('P_PROOF', 'Current exact human acceptance required before release permission')
        return result

    @_within_assessment
    def evaluate(self, subject, scope='default', live=True):
        """Assess a registered pending root or established use without granting permission.

        Args:
            subject: Exact output version reference.
            scope: Requested applicability scope.
            live: Inspect current protected revocation/material; false for historical replay.
        Returns:
            Internal assessment with exact closure, proofs, separate eligibility and reasons.
        Raises:
            ProtocolError: Subject identity is unavailable or dependency history is corrupt.
        """
        self.scope = scope
        self.resolve(subject)
        key = (self._key(subject, scope), live)
        memo = self._assessment_walk
        if key in memo['evaluations']:
            return copy.deepcopy(memo['evaluations'][key])
        result = self._evaluate(subject, scope, live)
        if result['qualified']:
            memo['evaluations'][key] = copy.deepcopy(result)
        return result

    def _evaluate(self, subject, scope, live):
        self.resolve(subject)
        reasons, evidence, proofs, established, dispositions = [], [], [], [], []
        context_refs, assessed, active, checked_grants = [], set(), set(), set()
        producers = set()

        def issue(code, text):
            item = {'code': code, 'message': text}
            if item not in reasons:
                reasons.append(item)

        def governing(event, current):
            decision = self._point(event['decision_ref'], event.get('decision_scope', event['scope']))
            if decision not in established:
                established.append(decision)
            key = self._key(decision)
            if key not in checked_grants:
                checked_grants.add(key)
                try:
                    actual = self.provenance.get(event['decision_ref']['version_id'], {}).get('authority')
                    required = {**event, 'grants': [actual]} if actual is not None else event
                    self._governing_grants(required, live)
                except ERROR as error:
                    issue(error.code, str(error))
            if decision != current:
                visit(decision)

        def visit(point):
            key = self._key(point)
            if key in assessed:
                return
            if key in active:
                raise ERROR('P_CONFLICT', 'Current governing-use dependency cycle')
            active.add(key)
            reference = point['ref']
            value = self.versions[reference['version_id']]
            record = self.resolve(reference)
            if not self._governing_input(point, live):
                changes = self._use_changes.get(key, {})
                until = changes.get('use_until_ms')
                at = int(time.time() * 1000) if live else getattr(self, 'assessed_at_ms', 0)
                # A pending root is a candidate for assessment, not an established input.
                pending_root = (point == self._point(subject, scope)
                    and value['kind'] == 'delivery.product' and key in self.states
                    and self._status(point)['validity'] == 'pending' and not self._held(point)
                    and not self._latest_cancellation(point) and not self._superseded_basis(point)
                    and 'withdrawn_at' not in changes and (until is None or at < until))
                if pending_root:
                    try:
                        self._local_qualification(reference, point['use_scope'], live)
                    except (ValueError, OSError) as error:
                        issue(getattr(error, 'code', 'P_PROOF'), str(error))
                else:
                    issue('P_PROOF', 'Required exact governing use is not currently applicable')
            if live:
                try:
                    self._material(record, True)
                except (ValueError, OSError):
                    issue('P_PROOF', 'Required current material is unavailable')
            for parent in self._governing_dependencies(point):
                visit(parent)
            for event in self._point_establishments(point):
                governing(event, point)
            actual_authority = self.provenance.get(reference['version_id'], {}).get('authority')
            if actual_authority is not None and key not in checked_grants:
                checked_grants.add(key)
                try:
                    self._governing_grants({'decision_ref': reference, 'scope': point['use_scope'], 'grants': [actual_authority]}, live)
                except ERROR as error:
                    issue(error.code, str(error))
            if record.get('assignment') is not None:
                producers.add(record['assignment']['version_id'])
            if value['kind'] == 'delivery.product':
                if record['product_kind'] == 'observation':
                    evidence.append(point)
                role = {'answer': 'professional_review', 'bundle': 'integration_review',
                        'handoff': 'receiving_acceptance', 'final_result': 'integration_review',
                        'observation': 'professional_review'}.get(record['product_kind'])
                profile = self.resolve(record['profile'], 'profile')
                obligations = [item for item in profile['obligations']
                               if item['owner'] == record['owner'] and item['role'] == role
                               and item['subject_kind'] == record['product_kind']]
                if record['product_kind'] in {'answer', 'bundle', 'handoff', 'final_result'} and not obligations:
                    issue('P_PROOF', 'Profile does not define the required local review')
                for obligation in obligations:
                    slot = {'kind': 'proof', 'subject': reference, 'role': role, 'slot_id': obligation['slot_id']}
                    selected = self.proofs.get(_proof_key(point['use_scope'], slot))
                    if selected is None:
                        issue('P_PROOF', 'Required exact proof slot has no current basis')
                        continue
                    proof_point = self._point(selected['proof'], selected['proof_use_scope'])
                    assessment = self.resolve(selected['proof'], 'assessment')
                    dispositions.append({'subject': point, 'assessment': proof_point, 'verdict': assessment['verdict']})
                    visit(proof_point)
                    if assessment['subject'] != reference or assessment['verdict'] not in {'supported', 'supported_with_conditions', 'accepted'}:
                        issue('P_PROOF', 'Current exact local review does not support this subject')
                    else:
                        proofs.append(proof_point)
            active.remove(key)
            assessed.add(key)
            context_refs.append(point)

        visit(self._point(subject, scope))
        closure_hash = _hash(context_refs)
        accepts = [event for event in self.events if event.get('kind') == 'accept' and event['subject'] == subject and event['scope'] == scope
                   and event['closure_hash'] == closure_hash and event['decision_id'] not in self.decisions.get('cancelled', [])]
        release = [event for event in self.events if event.get('kind') == 'release' and event['subject'] == subject and event['scope'] == scope
                   and event['closure_hash'] == closure_hash and event['decision_id'] not in self.decisions.get('cancelled', [])]
        if live:
            def current_permission(event):
                try:
                    self._governing_grants({'decision_ref': event['decision_ref'], 'scope': scope,
                        'grants': [{'purpose': event['purpose'], 'key_id': event['human_key_id']}]}, True)
                    return True
                except (ValueError, OSError):
                    return False
            accepts = [event for event in accepts if current_permission(event)]
            release = [event for event in release if current_permission(event)]
        conflicts = []
        for event in self.events:
            if event.get('kind') == 'budget-overrun':
                run = self.run_details[event['run_id']]
                assigned = self.resolve(run['context'], 'context')['assignment']
                if assigned['version_id'] in producers or self._point(assigned, self.resolve(assigned, 'assignment')['use_scope']) in context_refs:
                    issue('P_BUDGET', 'An unresolved measured execution budget incident affects this output')
        required = {self._key(point) for point in context_refs}
        required.update((self.resolve(self._reference(identifier), 'assignment')['use_scope'], identifier) for identifier in producers)
        for escalation, status in self.escalations.items():
            if status == 'open' and required & {self._key(point) for point in self.escalation_members.get(escalation, [])}:
                conflicts.append(self._point(self._reference(escalation), scope))
                issue('P_CONFLICT', 'An unresolved escalation affects this required closure')
        qualified = not reasons
        return {'qualified': qualified, 'accepted': qualified and bool(accepts),
                'release_eligible': qualified and bool(accepts) and bool(release),
                'reasons': reasons, 'closure': context_refs, 'closure_hash': closure_hash,
                'evidence': evidence, 'proofs': proofs, 'review_dispositions': dispositions,
                'acceptances': [event['decision_ref'] for event in accepts],
                'established_by': established + [self._point(event['decision_ref'], event['scope']) for event in accepts + release],
                'cancelled_by': [self._point(event['decision_ref'], event.get('scope', event['decision_ref']['scope'])) for event in self.events
                                 if (event['kind'] in {'cancellation', 'withdrawal'} and self._point(subject, scope) in event['subjects'])
                                 or (event['kind'] == 'permission-cancellation' and self._point(subject, scope) in event['outputs'])], 'conflicts': conflicts}

    def _ensure_use(self, point, active=None):
        key = self._key(point)
        if key in self.states:
            # A typed reassessment may inspect a cancelled prerequisite. Preserve
            # its tombstone; qualification and execution guards decide its use.
            return
        self._assessment_walk = None
        active = set() if active is None else active
        if key in active:
            raise ERROR('P_CONFLICT', 'Scoped causal dependency cycle')
        active.add(key)
        record = self.resolve(point['ref'])
        value = self.versions[key[1]]
        if value['kind'] in {'delivery.assignment', 'delivery.context'}:
            fixed_scope = record.get('use_scope', value['content']['scope'])
            if point['use_scope'] != fixed_scope:
                raise ERROR('P_SCOPE', 'Execution mandate cannot be imported into a different scope')
        previous = self.scope
        self.scope = point['use_scope']
        try:
            dependencies = self._dependencies(record)
        finally:
            self.scope = previous
        for dependency in dependencies:
            self._ensure_use(dependency, active)
        self.reliance[key] = dependencies
        primitive = value['kind'] in {'delivery.source', 'delivery.profile'}
        if value['kind'] == 'delivery.source' and record['owner'].get('kind') == 'authority' and self.initialized:
            if point['ref'] not in [ref for (scope, _), ref in self.sources.items() if scope == point['use_scope']]:
                primitive = False
        self.states[key] = {'validity': 'valid' if primitive else 'pending', 'applicable': primitive}
        active.remove(key)

    def _apply(self, effects, message, provenance, authority):
        self._assessment_walk = None
        self.scope = message['scope']
        for effect in effects:
            op = effect['op']
            if op == 'register':
                value = effect['manifest']
                identifier = version_id(value)
                if identifier in self.versions:
                    raise ERROR('P_INTEGRITY', 'Duplicate immutable registration')
                # New causal edges point only to previously admitted identities.
                # Scoped imports retain their own recursive active-cycle guard.
                for dependency in effect['dependencies']:
                    self.resolve(dependency['ref'])
                self._index_version(identifier, value)
                if value['kind'] == 'delivery.assignment':
                    self._assignment_records[_hash(value['content']['record'])] = identifier
                if 'content_policy' in effect:
                    self._content_policies[identifier] = _freeze(effect['content_policy'])
                if value['kind'] == 'delivery.product':
                    self._product_content[identifier] = _freeze(effect['semantic_content'])
                    self._product_records[_hash(value['content']['record'])] = identifier
                self.provenance[identifier] = _freeze({**copy.deepcopy(provenance), 'origin': effect['origin'], 'context': effect['context'], 'sequence': len(self.transactions) + 1})
                key = effect.get('use_scope', message['scope']), identifier
                for dependency in effect['dependencies']:
                    self._ensure_use(dependency)
                self.reliance[key] = effect['dependencies']
                self.states[key] = {'validity': 'pending', 'applicable': False}
            elif op == 'withdraw':
                loss = self._permissions_using(effect['subjects'])
                self.decisions.setdefault('cancelled', []).extend(loss['decision_ids'])
                for point in effect['subjects']:
                    key = self._key(point)
                    status = self.states.get(key)
                    if status is not None:
                        self.states[key] = {**status, 'applicable': False}
                    self._use_changes[key] = {**self._use_changes.get(key, {}),
                        'withdrawn_at': len(self.transactions) + 1, 'decision_ref': effect['decision_ref']}
                self._admit_event({'kind': 'withdrawal', 'subjects': effect['subjects'],
                    'decision_ref': effect['decision_ref'], 'scope': message['scope'],
                    'sequence': len(self.transactions) + 1})
            elif op == 'qualify':
                key = effect.get('use_scope', message['scope']), effect['subject']
                if key not in self.states:
                    self._ensure_use(self._point(self._reference(key[1]), key[0]))
                self.states[key] = {'validity': 'valid', 'applicable': effect.get('applicable', True)}
                if 'requirements' in effect:
                    self._use_changes[key] = {**self._use_changes.get(key, {}), 'requirements': copy.deepcopy(effect['requirements'])}
                if effect.get('applicable', True):
                    deadlines = [item['expires_at_ms'] for item in self._use_changes.get(key, {}).get('requirements', [])
                                 if item['expires_at_ms'] is not None]
                    governing = self._governing_dependencies(self._point(self._reference(key[1]), key[0]))
                    record = self.resolve(self._reference(key[1]))
                    if self.versions[key[1]]['kind'] == 'delivery.product':
                        role = {'answer': 'professional_review', 'bundle': 'integration_review',
                                'handoff': 'receiving_acceptance', 'final_result': 'integration_review',
                                'observation': 'professional_review'}.get(record['product_kind'])
                        governing.extend(self._point(selected['proof'], selected['proof_use_scope'])
                                         for proof_key, selected in self.proofs.items()
                                         if proof_key[0] == key[0] and selected['subject'] == self._reference(key[1])
                                         and loads(proof_key[1]).get('role') == role)
                    deadlines.extend(self._use_changes.get(self._key(parent), {}).get('use_until_ms')
                                     for parent in governing
                                     if self._use_changes.get(self._key(parent), {}).get('use_until_ms') is not None)
                    self._use_changes[key] = {**self._use_changes.get(key, {}), 'use_until_ms': min(deadlines) if deadlines else None}
                    self._use_changes[key] = {**self._use_changes.get(key, {}), 'established_at': len(self.transactions) + 1}
                if 'decision_ref' in effect and effect.get('applicable', True):
                    self._selection_event('applicability', key[0], {'kind': 'use'}, self._reference(key[1]), key[0], effect['decision_ref'], provenance, authority)
            elif op == 'initialize':
                self.initialized = True
            elif op == 'assignment':
                prior = self.assignment_states.get(effect['subject'])
                legal = {None: {'open'}, 'open': {'paused', 'completed', 'cancelled'}, 'paused': {'open', 'completed', 'cancelled'}}
                if effect['state'] not in legal.get(prior, set()):
                    raise ERROR('P_STATE', 'Forbidden assignment state transition')
                self.assignment_states[effect['subject']] = effect['state']
                if prior == 'paused' and effect['state'] == 'open' and 'decision_ref' in effect:
                    reference = self._reference(effect['subject'])
                    use_scope = self.resolve(reference, 'assignment')['use_scope']
                    self._selection_event('applicability', use_scope, {'kind': 'use'}, reference, use_scope,
                                          effect['decision_ref'], provenance, authority, decision_scope=message['scope'])
            elif op == 'run':
                prior = self.run_states.get(effect['run_id'])
                legal = {None: {'issued'}, 'issued': {'running', 'cancelled'}, 'running': {'returned', 'quarantined', 'cancelled'}}
                if effect['state'] not in legal.get(prior, set()):
                    raise ERROR('P_STATE', 'Forbidden run state transition')
                self.run_states[effect['run_id']] = effect['state']
                details = self.run_details.setdefault(effect['run_id'], {'usage': {}, 'reservation_released': False})
                details.update({key: copy.deepcopy(value) for key, value in effect.items() if key not in {'op', 'run_id', 'state'}})
                if prior is None and details.get('local_unit_id') is not None:
                    self.local_budget['units'][details['local_unit_id']]['runs'].append(effect['run_id'])
                if prior is None and 'invocation_id' not in details:
                    details['invocation_id'] = effect['run_id']
                    assigned = self.resolve(self.resolve(details['context'], 'context')['assignment'], 'assignment')
                    self.invocations[effect['run_id']] = {'invocation_id': effect['run_id'],
                        'provider': 'json-process/1', 'state': 'issued', 'scope': assigned['use_scope'],
                        'members': [{'member_key': 'singleton', 'context': details['context'],
                                     'assignment': self.resolve(details['context'], 'context')['assignment']}],
                        'limits': copy.deepcopy(details['limits']), 'usage': {}, 'reservation_released': False}
                    for limit in details['limits']:
                        usage = self.usage.setdefault((details['context']['scope'], limit['metric'], limit['unit']), {'spent': 0, 'reserved': 0})
                        usage['reserved'] += limit['ceiling']
                physical = self.invocations.get(details['invocation_id'])
                if physical is not None and physical['provider'] == 'json-process/1':
                    physical['state'] = effect['state']
                    physical.update({key: value for key, value in effect.items() if key in {'started_at_ms', 'issued_at_ms'}})
            elif op == 'native-bind':
                details = self.run_details[effect['run_id']]
                details['native'] = copy.deepcopy(effect['binding'])
                details['broker_limits'] = {name: effect['binding'][name] for name in ('packet_bytes', 'total_bytes')}
                details['broker_bytes'] = effect['binding']['transferred_bytes']
                self.native_handles[(effect['binding']['provider'], effect['binding']['handle'])] = {
                    'run_id': effect['run_id'], 'identity': copy.deepcopy(effect['identity'])}
                self._native_packet_facts[effect['run_id']] = _freeze(effect['packet_facts'])
            elif op in {'broker-intent', 'broker-ack'}:
                details = self.run_details[effect['run_id']]
                details['broker_limits'] = copy.deepcopy(effect['limits'])
                details['broker_bytes'] = effect['transferred_bytes']
                entry = {'request_blob_id': effect['request_blob_id'], 'operation': effect['operation'],
                         'status': 'pending' if op == 'broker-intent' else 'ack'}
                if op == 'broker-ack':
                    entry['result_blob_id'] = effect['result_blob_id']
                    if effect['frame_overrun']:
                        details['broker_frame_overrun'] = True
                    known = details.setdefault('broker_allowed_blobs', [])
                    known.extend(identifier for identifier in effect['allowed_blobs'] if identifier not in known)
                details.setdefault('broker_requests', {})[effect['request_id']] = entry
            elif op == 'select':
                self.selections[_proof_key(effect['scope'], effect['slot'])] = effect['candidate']
                self._selection_event('basis', effect['scope'], effect['slot'], effect['candidate'], effect['scope'], effect['decision_ref'], provenance, authority)
            elif op == 'proof':
                self.proofs[_proof_key(effect['scope'], effect['slot'])] = {'subject': effect['slot']['subject'], 'proof': effect['candidate'], 'proof_use_scope': effect['proof_use_scope']}
                self._selection_event('proof', effect['scope'], effect['slot'], effect['candidate'], effect['proof_use_scope'], effect['decision_ref'], provenance, authority)
                for decision in effect['reviewer_support']:
                    issuer = self.provenance[decision['version_id']]
                    self._selection_event('review-lineage', effect['scope'], effect['slot'], effect['candidate'],
                                          effect['proof_use_scope'], decision, issuer, None)
            elif op == 'cancel':
                loss = self._permissions_using(effect['subjects'])
                self.decisions.setdefault('cancelled', []).extend(loss['decision_ids'])
                for point in effect['subjects']:
                    self.states[self._key(point)] = {'validity': 'invalid', 'applicable': False}
                    self._use_changes[self._key(point)] = {**self._use_changes.get(self._key(point), {}),
                        'withdrawn_at': len(self.transactions) + 1, 'decision_ref': effect['decision_ref']}
                    identifier = point['ref']['version_id']
                    if self.versions[identifier]['kind'] == 'delivery.assignment' and self.assignment_states.get(identifier) in {'open', 'paused'}:
                        self.assignment_states[identifier] = 'cancelled'
                cancelled = self.decisions.setdefault('cancelled', [])
                for event in self.events:
                    if event.get('subject') and self._point(event['subject'], event.get('scope', message['scope'])) in effect['subjects'] and event.get('decision_id'):
                        cancelled.append(event['decision_id'])
                self._admit_event({'kind': 'cancellation', 'subjects': effect['subjects'], 'decision_ref': effect['decision_ref'], 'decision_id': effect['decision'], 'sequence': len(self.transactions) + 1})
            elif op == 'initial-source':
                self.sources[(effect['use_scope'], effect['source']['logical_id'])] = effect['source']
            elif op == 'bootstrap-use':
                if message['message_type'] != 'bootstrap' or self.initialized:
                    raise ERROR('P_SCOPE', 'Semantic scope initialization is restricted to the initial bootstrap')
                self._ensure_use(effect['point'])
            elif op == 'source-select':
                old = effect['previous']
                for key, reference in list(self.sources.items()):
                    if key[0] == message['scope'] and reference == old:
                        self.sources[key] = effect['replacement']
                        self._selection_event('source', key[0], {'logical_id': key[1]}, effect['replacement'], key[0], effect['decision_ref'], provenance, authority)
                for key, reference in list(self.selections.items()):
                    if key[0] == message['scope'] and reference == old:
                        self.selections[key] = effect['replacement']
            elif op == 'human-use':
                self.human_uses[effect['identity']] = (effect['scope'], effect['request_id'])
            elif op in {'accept', 'release'}:
                self._admit_event({'kind': op, 'subject': effect['subject'], 'scope': message['scope'], 'closure_hash': effect['closure_hash'], 'closure': effect['closure'],
                                    'decision_id': effect['decision_id'], 'decision_ref': self._decision_ref(message),
                                    'purpose': authority['purpose'], 'human_key_id': authority['key_id']})
            elif op == 'permission-cancel':
                cancelled = self.decisions.setdefault('cancelled', [])
                cancelled.extend(identifier for identifier in effect['decision_ids'] if identifier not in cancelled)
                self._admit_event({'kind': 'permission-cancellation', 'outputs': effect['outputs'], 'decision_ref': effect['decision_ref']})
            elif op == 'escalation':
                if effect.get('affected') is not None:
                    self.escalation_members[effect['subject']] = effect['affected']
                prior = self.escalations.get(effect['subject'])
                if not (prior is None and effect['state'] == 'open' or prior == 'open' and effect['state'] in {'resolved', 'terminated'}):
                    raise ERROR('P_STATE', 'Forbidden escalation state transition')
                self.escalations[effect['subject']] = effect['state']
            elif op == 'episode':
                identifier = effect['root']['version_id']
                current = self.episodes.get(identifier)
                if current is None:
                    current = {key: copy.deepcopy(effect[key]) for key in ('root', 'scope', 'layer', 'work_item', 'collect_until_ms', 'control_until_ms', 'attempt')}
                    current['revisions'] = []
                    current['members'] = []
                    self.episodes[identifier] = current
                    self.escalations[identifier] = 'open'
                current['current'] = effect['revision']
                current['revisions'].append(effect['revision']['version_id'])
                current['decisive'] = effect['decisive']
                current['members'] = sorted({canonical(point): point for point in current['members'] + effect['members']}.values(), key=canonical)
                self.escalation_members[identifier] = copy.deepcopy(current['members'])
            elif op == 'speculation':
                reference = effect['decision_ref']
                self.speculations[reference['version_id']] = {**copy.deepcopy(effect['payload']),
                    'ref': reference, 'human_key_id': effect['human_key_id']}
            elif op == 'hold':
                self.holds[self._key(effect['subject'])] = {key: copy.deepcopy(effect[key]) for key in ('episode', 'grant')}
            elif op == 'unhold':
                self.holds.pop(self._key(effect['subject']), None)
                self._selection_event('applicability', effect['subject']['use_scope'], {'kind': 'use'}, effect['subject']['ref'],
                                      effect['subject']['use_scope'], effect['decision_ref'], provenance, authority,
                                      decision_scope=message['scope'])
            elif op == 'local-bind':
                import governed_local_budget
                binding = {key: copy.deepcopy(effect[key]) for key in ('anchor', 'phase', 'scope', 'root_generation', 'planning_ancestors')}
                self.local_budget['bindings'][effect['assignment']['version_id']] = binding
                key = governed_local_budget._unit_id(effect['anchor'], effect['phase'], effect['scope'])
                unit = self.local_budget['units'].setdefault(key, {
                    'unit_id': key, 'anchor': copy.deepcopy(effect['anchor']), 'phase': effect['phase'],
                    'scope': effect['scope'], 'root_generation': effect['root_generation'],
                    'owner': copy.deepcopy(effect['owner']), 'policy': copy.deepcopy(effect['policy']),
                    'iteration': 0, 'reworks_used': 0, 'downstream_started': False, 'revision': 0, 'state': 'ready',
                    'remaining_ms': effect['policy']['iteration_ms'], 'deadline_ms': None,
                    'started_at_ms': None, 'stage': 'ready', 'notice': None, 'members': [], 'runs': [],
                    'governors': [copy.deepcopy(effect['anchor'])]})
                unit['members'].append(copy.deepcopy(effect['assignment']))
                if self.resolve(effect['assignment'], 'assignment')['responsibility'] == 'setter':
                    for phase in ('planning', 'question', 'integration'):
                        sibling = self.local_budget['units'].get(governed_local_budget._unit_id(effect['anchor'], phase, effect['scope']))
                        if sibling is not None and effect['assignment'] not in sibling['governors']:
                            sibling['governors'].append(copy.deepcopy(effect['assignment']))
            elif op == 'local-update':
                self.local_budget['units'][effect['unit_id']].update(copy.deepcopy(effect['value']))
            elif op == 'local-task-stop':
                self.local_budget['task_stops'][(effect['scope'], effect['root_generation'])] = effect['reason']
            elif op == 'invocation':
                self.invocations[effect['invocation_id']] = copy.deepcopy(effect['value'])
                for limit in effect['value']['limits']:
                    usage = self.usage.setdefault((effect['value']['scope'], limit['metric'], limit['unit']), {'spent': 0, 'reserved': 0})
                    usage['reserved'] += limit['ceiling']
            elif op == 'invocation-update':
                self.invocations[effect['invocation_id']].update(copy.deepcopy(effect['value']))
            elif op == 'prepared-packet':
                self.run_details[effect['run_id']]['prepared_packet'] = copy.deepcopy(effect['value'])
            elif op == 'semantic-capture':
                self.run_details[effect['run_id']]['semantic_capture'] = copy.deepcopy(effect['value'])
            elif op == 'procedure-step':
                self.procedure_steps.setdefault(effect['procedure']['version_id'], {})[effect['step']] = copy.deepcopy(effect)
                self._admit_event({'kind': 'procedure-step', **{key: value for key, value in effect.items() if key != 'op'}})
            elif op == 'procedure':
                self.procedures[(effect['assignment']['version_id'], effect['scope'])] = copy.deepcopy(effect['decision_ref'])
            elif op == 'execution-plan':
                self.execution_plans[(effect['assignment']['version_id'], effect['scope'])] = copy.deepcopy(effect['decision_ref'])
            elif op == 'consumed-basis':
                self.consumed_basis[effect['assignment']['version_id']] = copy.deepcopy(effect['basis'])
            elif op == 'search-step':
                key = effect['attempt']['version_id']
                self.search_steps[key] = self.search_steps.get(key, 0) + 1
            elif op == 'counter':
                self.counters[effect['key']] = effect['count']
            elif op == 'decision-record':
                value = effect['manifest']
                identifier = version_id(value)
                if identifier in self.versions:
                    raise ERROR('P_INTEGRITY', 'Duplicate immutable registration')
                for dependency in effect['dependencies']:
                    self.resolve(dependency['ref'])
                self._index_version(identifier, value)
                self.provenance[identifier] = {**copy.deepcopy(provenance), 'origin': message['sender'], 'context': message['context'], 'sequence': len(self.transactions) + 1}
                if authority is not None:
                    self.provenance[identifier]['authority'] = {
                        'purpose': authority['purpose'], 'key_id': authority['key_id']}
                self.provenance[identifier] = _freeze(self.provenance[identifier])
                key = message['scope'], identifier
                for dependency in effect['dependencies']:
                    self._ensure_use(dependency)
                self.states[key] = {'validity': 'valid', 'applicable': True}
                self.reliance[key] = effect['dependencies']
                nested = value['content']['record']['message']
                self.messages[message_id(nested)] = _freeze(nested)
            elif op == 'usage':
                self._apply_usage(effect)
            elif op == 'quarantine':
                self._admit_event({'kind': 'quarantine', **{key: value for key, value in effect.items() if key != 'op'}})
            elif op == 'event':
                semantic = effect.get('semantic_message', message)
                identifier = message_id(semantic)
                self.messages[identifier] = _freeze(semantic)
                self._admit_event({'kind': effect['kind'], 'payload': effect['payload'], 'message_id': identifier})
                if effect['kind'] == 'revision-lineage':
                    replacement = effect['payload']['replacement']
                    scope = self.resolve(replacement, 'assignment')['use_scope']
                    self._selection_event('applicability', scope, {'kind': 'use'}, replacement, scope,
                                          effect['decision_ref'], provenance, authority)
            else:
                raise ERROR('P_INTEGRITY', 'Unknown internally derived effect')

    def _decision_manifest(self, message):
        return manifest('decision:' + message['request_id'], 'delivery.decision', {'engagement': message['engagement'], 'scope': message['scope'], 'record': {'owner': message['sender'], 'message': message}})

    def _decision_ref(self, message):
        return _ref(self._decision_manifest(message))


def _parse_message(raw):
    try:
        value = loads(raw) if isinstance(raw, (str, bytes)) else normal(raw)
    except (ValueError, TypeError) as error:
        raise ERROR('P_PARSE', 'Strict semantic JSON required') from error
    wire.validate(value)
    if message_id(value) != value['message_id']:
        raise ERROR('P_IDENTITY', 'Protocol message identity mismatch')
    return value


def _verify_human(message, proof, profile, at, live, target=None):
    required = message.get('message_type') == 'decision' and message['payload'].get('authority_proof') is not None
    if not required:
        if proof is not None:
            raise ERROR('P_SCOPE', 'Unexpected human authority material')
        return None
    if proof is None:
        raise ERROR('P_SCOPE', 'Independent human authority proof is required')
    action = message['payload']['action']
    purpose = {'accept': 'delivery-accept', 'release': 'delivery-release'}.get(action, 'delivery-change')
    verified = wire.verify_proof(proof, purpose, at, live=live)
    wire._require_scope(verified['trust'], message['engagement'], message['scope'])
    if live:
        policy = verified['trust']['host_policy']
        # A new L0 act uses current policy entitlements; historical signatures
        # remain facts when those current entitlements later change.
        if (profile['authority_policy_id'] not in policy['authority_policy_ids']
                or profile['routing_policy_id'] not in policy['routing_policy_ids']):
            raise ERROR('P_SCOPE', 'Human authority does not permit the governing profile')
    if blob(verified['raw']) != message['payload']['authority_proof']:
        raise ERROR('P_IDENTITY', 'Exact human proof bytes differ from the approved message')
    descriptor = wire.action_descriptor(message, _hash(profile))
    request = verified['wrapper']['request']
    if (request['source']['sha256'] != operator.sha(canonical(descriptor))
            or target is not None and request['target'] != target):
        raise ERROR('P_SCOPE', 'Human approval does not bind the exact intent bytes and requested store')
    parameters = request['parameters']
    if set(parameters) != {'intent', 'intent_digest'}:
        raise ERROR('P_SCOPE', 'Human approval requires a closed exact intent commitment')
    try:
        same_intent = canonical(parameters['intent']) == canonical(descriptor)
    except LifecycleError as error:
        raise ERROR('P_SCOPE', 'Human approval intent is not canonical semantic JSON') from error
    if not same_intent or parameters['intent_digest'] != _hash(descriptor):
        raise ERROR('P_SCOPE', 'Human approval does not bind this exact decision intent')
    allowed = {'delivery-accept': {'accept'}, 'delivery-release': {'release'},
               'delivery-change': {'continue', 'reformulate', 'reinstate', 'terminate', 'speculate', 'resolve_escalation', 'exclude_content'}}
    if action not in allowed[purpose]:
        raise ERROR('P_SCOPE', 'Human purpose cannot authorize this action')
    return {'purpose': purpose, 'signer': verified['trust']['signer'], 'key_id': verified['trust']['key_id'],
            'identity': verified['wrapper']['request']['request_id'], 'proof_blob': blob(verified['raw'])}


def _transaction_hash(value):
    return hashlib.sha256(TRANSACTION_DOMAIN + canonical({key: item for key, item in value.items()
                       if key != 'hash'})).hexdigest()


def _receipt(transaction):
    message = transaction['operations'][0]['data']['message']
    effects = transaction['operations'][0]['data']['effects']
    references = {reference['version_id']: reference for reference in _references(effects)}
    references.update({reference['version_id']: reference for reference in _references(message)})
    for effect in effects:
        if 'manifest' in effect:
            reference = _ref(effect['manifest'])
            references[reference['version_id']] = reference
    affected = []
    for effect in effects:
        if effect['op'] in {'cancel', 'withdraw'}:
            points = effect['subjects']
        elif effect['op'] == 'permission-cancel':
            points = effect['permissions'] + effect['outputs']
        elif effect['op'] == 'bootstrap-use':
            points = [effect['point']]
        else:
            identifier = effect.get('subject') if isinstance(effect.get('subject'), str) else None
            if effect['op'] in {'register', 'decision-record'}:
                identifier = version_id(effect['manifest'])
            reference = references.get(identifier) if identifier else effect.get('candidate', effect.get('subject'))
            points = [{'ref': reference, 'use_scope': effect.get('use_scope', effect.get('scope', message['scope']))}] if isinstance(reference, dict) and 'version_id' in reference else []
        for point in points:
            if point not in affected:
                affected.append(point)
    return {'protocol': PROTOCOL, 'message_id': message['message_id'], 'request_id': message['request_id'],
            'origin_binding': _hash({'origin': message['sender'], 'context': message['context'],
                                     'run_context': message['payload'].get('run_context')}),
            'assessed_at_ms': transaction['timestamp'],
            'before_head': transaction['previous'], 'after_head': transaction['hash'],
            'transaction_id': transaction['transaction_id'],
            'created_versions': [_ref(effect['manifest']) for effect in effects if effect['op'] in {'register', 'decision-record'}],
            'affected_uses': affected,
            'effect_digest': _hash(effects)}


def _transaction_shape(state, transaction):
    """Check the exact serialized row without deriving or applying its effects."""
    keys = {'format', 'protocol', 'engagement', 'sequence', 'previous', 'transaction_id',
            'timestamp', 'operations', 'authority_proof', 'return_artifact', 'validation_artifacts', 'hash'}
    if isinstance(transaction, dict) and transaction.get('format') != 9:
        raise ERROR('P_SCHEMA', 'Unsupported historical journal format; create a fresh governed engagement')
    if not isinstance(transaction, dict) or set(transaction) != keys or transaction['protocol'] != PROTOCOL:
        raise ERROR('P_INTEGRITY', 'Closed governed transaction required')
    if (transaction['engagement'] != state.engagement or transaction['previous'] != state.head
            or type(transaction['sequence']) is not int
            or transaction['sequence'] != len(state.transactions) + 1
            or type(transaction['timestamp']) is not int):
        raise ERROR('P_INTEGRITY', 'Broken governed transaction predecessor or sequence')
    try:
        if str(uuid.UUID(transaction['transaction_id'])) != transaction['transaction_id']:
            raise ValueError('transaction identity')
    except (ValueError, AttributeError) as error:
        raise ERROR('P_INTEGRITY', 'Canonical transaction identity required') from error
    if any(item['transaction_id'] == transaction['transaction_id'] for item in state.transactions):
        raise ERROR('P_INTEGRITY', 'Repeated transaction identity')
    try:
        actual_hash = _transaction_hash(transaction)
    except (LifecycleError, TypeError) as error:
        raise ERROR('P_INTEGRITY', 'Transaction contains noncanonical semantic values') from error
    if transaction['hash'] != actual_hash:
        raise ERROR('P_INTEGRITY', 'Governed transaction hash mismatch')
    operations = transaction['operations']
    if (not isinstance(operations, list) or len(operations) != 1 or set(operations[0]) != {'op', 'data'}
            or operations[0]['op'] != 'governed' or set(operations[0]['data']) != {'message', 'effects'}
            or not isinstance(operations[0]['data']['effects'], list)
            or not isinstance(transaction['validation_artifacts'], list)
            or any(not isinstance(identifier, str) or re.fullmatch(r'[0-9a-f]{64}', identifier) is None
                   for identifier in transaction['validation_artifacts'])
            or transaction['validation_artifacts'] != sorted(set(transaction['validation_artifacts']))
            or transaction['return_artifact'] is not None and (not isinstance(transaction['return_artifact'], dict)
                or any(not isinstance(key, str) or not isinstance(value, str) or blob(value.encode('utf-8')) != key
                       for key, value in transaction['return_artifact'].items()))):
        raise ERROR('P_INTEGRITY', 'One closed governed operation and exact artifacts required')
    raw_message = operations[0]['data']['message']
    payload = raw_message.get('payload', {}) if isinstance(raw_message, dict) else {}
    if (isinstance(payload, dict) and payload.get('event') == 'invocation_finished'):
        import governed_semantic
        if payload.get('codec') != governed_semantic.CODEC:
            raise ERROR('P_SCHEMA', 'Unsupported historical semantic encoder version; preserve this archive and create a fresh governed engagement')
    return _parse_message(raw_message)


def _local_origin(message, authority):
    """Bind outer operations to the local writer or an actual signed L0 act."""
    sender = message['sender']
    if sender['kind'] == 'controller' and authority is None:
        return sender
    if (sender['kind'] == 'authority' and message['message_type'] == 'decision'
            and authority is not None and sender['id'] == authority['signer']):
        return sender
    raise ERROR('P_ORIGIN', 'Outer ingestion requires the local controller or an actual signed L0 decision')


def _decode_authority(transaction):
    encoded = transaction['authority_proof']
    if encoded is None:
        return None
    try:
        if not isinstance(encoded, str):
            raise ValueError('proof type')
        raw = base64.b64decode(encoded, validate=True)
        if base64.b64encode(raw).decode('ascii') != encoded:
            raise ValueError('proof encoding')
        return raw
    except (ValueError, TypeError) as error:
        raise ERROR('P_INTEGRITY', 'Exact base64 L0 proof bytes required') from error


def _append_transaction(state, transaction, message, effects, authority):
    key = (message['scope'], _owner_key(message['sender']), message['request_id'])
    if key in state.requests:
        raise ERROR('P_IDEMPOTENCY', 'Committed request cannot be applied twice')
    state._apply(effects, message, {}, authority)
    state.messages[message['message_id']] = _freeze(message)
    state.head = transaction['hash']
    state.transactions.append(_freeze(transaction))
    state.requests[key] = _freeze({'message_id': message['message_id'], 'receipt': _receipt(transaction)})


def _verify_transaction(state, transaction, live=False):
    """Cold-verify one transition, including only an actual L0 signature if present."""
    message = _transaction_shape(state, transaction)
    if message['sender']['kind'] == 'assignment':
        raise ERROR('P_ORIGIN', 'Direct entity ingestion is unsupported; use its captured issued RunReturn')
    authority = _verify_human(message, _decode_authority(transaction), state._profile(message),
                              transaction['timestamp'], live)
    origin = _local_origin(message, authority)
    if any(key in state.validation_assets for key in transaction['validation_artifacts']):
        raise ERROR('P_INTEGRITY', 'Validation assets must be captured once at first use')
    state.return_artifact = transaction['return_artifact']
    state.validation_artifacts = []
    state.validation_replay_artifacts = transaction['validation_artifacts']
    effects = state.derive(message, origin, transaction['timestamp'], authority, live=live)
    if canonical(state.validation_artifacts) != canonical(transaction['validation_artifacts']):
        raise ERROR('P_INTEGRITY', 'Validation journal contains unused or mismatched assets')
    state.validation_replay_artifacts = None
    if canonical(effects) != canonical(transaction['operations'][0]['data']['effects']):
        raise ERROR('P_INTEGRITY', 'Persisted effects differ from the exact derived transition')
    _append_transaction(state, transaction, message, effects, authority)


def replay(transactions, engagement=None, proof_verifier=None, blob_reader=None):
    """Reconstruct the sole local-writer journal and genuine L0 decisions.

    Args:
        transactions: Exact format-9 transaction sequence.
        engagement: Required engagement, inferred only from a nonempty first transaction.
        proof_verifier: Retired callback contract; any supplied callback is rejected.
        blob_reader: Internal exact material reader, never a provenance provider.
    Returns:
        Independently verified State using the sole effect derivation engine.
    Raises:
        ProtocolError: Any archived format, signature, origin, effect or chain is invalid.
    """
    if proof_verifier is not None:
        raise ERROR('P_ORIGIN', 'Caller-supplied authority validators are not supported')
    state = State(engagement or (transactions[0]['engagement'] if transactions else None), blob_reader)
    for transaction in transactions:
        _verify_transaction(state, transaction, live=False)
    return state


def _parse_transactions(raw):
    """Parse captured ledger bytes; callers must independently replay them."""
    transactions = []
    for line in raw.splitlines():
        if not line.strip():
            raise ERROR('P_INTEGRITY', 'Blank governed transaction')
        # Signed wrappers retain their separate finite-float representation.
        def pairs(items):
            result = {}
            for key, value in items:
                key = normal(key)
                if key in result:
                    raise ValueError('duplicate transaction member')
                result[key] = value
            return result
        try:
            transaction = json.loads(line, object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite wrapper')))
        except ValueError as error:
            raise ERROR('P_INTEGRITY', 'Invalid governed transaction JSON') from error
        transactions.append(transaction)
    return transactions


def read(path, engagement=None, proof_verifier=None):
    """Read and verify one format-9 ledger; unsupported history remains an archive.

    Args:
        path: Exact nonsymlink governed ledger path.
        engagement: Expected engagement identity.
        proof_verifier: Retired callback; cannot override mandatory verification.
    Returns:
        Validated transaction list.
    Raises:
        ProtocolError: Parsing, archive, chain or independent proof verification fails.
        OSError: Secure ledger material is unavailable.
    """
    transactions = _parse_transactions(operator.journal_snapshot(path))
    replay(transactions, engagement, proof_verifier)
    return transactions


def commit(path, engagement, expected_head, operations, proof_verifier=None, proof=None,
           transaction_id=None, candidate_validator=None):
    """Deny retired raw-operation persistence; use Store.submit with external proofs.

    Args:
        path: Historical caller target, not written.
        engagement: Claimed engagement, not authority.
        expected_head: Claimed predecessor, not authority.
        operations: Retired raw operation input, always rejected.
        proof_verifier: Retired injectable callback, always rejected.
        proof: Retired wrapper field, not a governed ingress credential.
        transaction_id: Historical transaction argument, not consumed.
        candidate_validator: Optional validators cannot exempt mandatory guards.
    Raises:
        ProtocolError: Always; raw persistence is not an active entry point.
    """
    raise ERROR('P_ORIGIN', 'Raw lifecycle operations are unsupported; use local governed ingestion')


class Store:
    """One governed ledger with separate immutable material, not another authority store."""

    def __init__(self, path, engagement):
        """Bind path and exact engagement; no actor, key or caller policy is accepted."""
        self.path, self.engagement = Path(path).absolute(), engagement
        self.material = self.path.parent / (self.path.name + '.blobs')
        self._checkpoint = None

    def _clone(self, state):
        return state._fork()

    def _verified(self, raw):
        """Advance an exact verified prefix; ordinary reads need no keyring."""
        if self._checkpoint is not None:
            accepted, state = self._checkpoint
            if raw.startswith(accepted) and (raw == accepted or not accepted or accepted.endswith(b'\n')):
                suffix = raw[len(accepted):]
                if suffix:
                    state = self._clone(state)
                    for transaction in _parse_transactions(suffix):
                        _verify_transaction(state, transaction, live=False)
                self._checkpoint = (raw, state)
                return state
            self._checkpoint = None
        state = replay(_parse_transactions(raw), self.engagement, blob_reader=self._blob)
        self._checkpoint = (raw, state)
        return state

    def put_blob(self, raw):
        """Register immutable bytes without selecting content or granting access.

        Args:
            raw: Exact bounded bytes from controlled input/output transport.
        Returns:
            Existing domain-separated blob digest.
        Raises:
            ValueError: Input is not bounded bytes or material identity conflicts.
            OSError: Secure immutable storage cannot be established.
        """
        if not isinstance(raw, bytes) or len(raw) > 32 * 1024 * 1024:
            raise ValueError('bounded exact material bytes required')
        self.material.mkdir(parents=True, exist_ok=True)
        if self.material.is_symlink():
            raise ValueError('material directory must not be a symlink')
        identifier = blob(raw)
        target = self.material / identifier
        try:
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            if operator.regular(target) != raw:
                raise ValueError('immutable material identity conflict')
        else:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        return identifier

    def _blob(self, identifier):
        if not isinstance(identifier, str) or len(identifier) != 64 or any(char not in '0123456789abcdef' for char in identifier):
            raise ValueError('exact blob identity required')
        raw = operator.regular(self.material / identifier)
        if blob(raw) != identifier:
            raise ERROR('P_INTEGRITY', 'Immutable material bytes are corrupted')
        return raw

    def read(self):
        """Return a detached snapshot with read-only admitted historical records.

        Returns:
            State derived from the verified prefix and any newly verified suffix;
            admitted JSON descendants reject mutation (deepcopy creates proposals),
            and entity visibility is enforced by its dispatcher packet. A new Store
            verifies the full history, while unchanged prefixes are reused only
            while exact accepted bytes remain unchanged.
        Raises:
            ProtocolError: History or its externally enrolled proofs fail verification.
        """
        raw = operator.journal_snapshot(self.path) if self.path.exists() else b''
        return self._clone(self._verified(raw))

    def submit(self, raw_message, authority_proof=None):
        """Record one local-runtime transition atomically, deriving it once.

        Args:
            raw_message: Closed host message; direct assignment senders are refused.
            authority_proof: Actual external L0 wrapper bytes or object for a reserved act.
        Returns:
            Closed response; exact retries return the original receipt without a new event.
            Rejection never changes the accepted journal or private checkpoint.
        """
        message = None
        try:
            message = _parse_message(raw_message)
            if message['sender']['kind'] == 'assignment':
                raise ERROR('P_ORIGIN', 'Direct entity ingestion is unsupported; use its captured issued RunReturn')
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            with store_lock(self.path):
                try:
                    raw_before = operator.journal_snapshot(self.path) if self.path.exists() else b''
                    accepted = self._verified(raw_before)
                    key = (message['scope'], _owner_key(message['sender']), message['request_id'])
                    committed = accepted.requests.get(key)
                    if committed is not None:
                        if committed['message_id'] != message['message_id']:
                            raise ERROR('P_IDEMPOTENCY', 'Committed request key reused for different content')
                        return {'status': 'already_committed', 'receipt': copy.deepcopy(committed['receipt']), 'error': None}
                    state = self._clone(accepted)
                    at = int(time.time() * 1000)
                    proof_raw = None if authority_proof is None else wire.proof_bytes(authority_proof)[0]
                    human = _verify_human(message, proof_raw, state._profile(message), at, live=True,
                                          target=str(self.path))
                    origin = _local_origin(message, human)
                    state.return_artifact = None
                    state.validation_artifacts = []
                    state.validation_replay_artifacts = None
                    effects = state.derive(message, origin, at, human, live=True)
                    transaction = {'format': 9, 'protocol': PROTOCOL, 'engagement': self.engagement,
                        'sequence': len(state.transactions) + 1, 'previous': state.head,
                        'transaction_id': str(uuid.uuid4()), 'timestamp': at,
                        'operations': [{'op': 'governed', 'data': {'message': message, 'effects': effects}}],
                        'authority_proof': None if proof_raw is None else base64.b64encode(proof_raw).decode('ascii'),
                        'return_artifact': state.return_artifact, 'validation_artifacts': state.validation_artifacts}
                    transaction['hash'] = _transaction_hash(transaction)
                    encoded = operator.canonical(transaction) + b'\n'
                    # Serialization is checked at its boundary; rederiving an already
                    # validated local transition would not establish another authority.
                    serialized = _parse_transactions(encoded)[0]
                    _transaction_shape(accepted, serialized)
                    if canonical(serialized) != canonical(transaction):
                        raise ERROR('P_INTEGRITY', 'Serialized transition differs from its exact validated representation')
                    _append_transaction(state, serialized, message, effects, human)
                    candidate_bytes = raw_before + encoded
                    with tempfile.NamedTemporaryFile(dir=self.path.parent, prefix='.governed-', delete=False) as stream:
                        temporary = Path(stream.name)
                        stream.write(candidate_bytes)
                        stream.flush()
                        os.fsync(stream.fileno())
                    if (operator.journal_snapshot(self.path) if self.path.exists() else b'') != raw_before:
                        raise ERROR('P_HEAD', 'Ledger changed during transition preparation')
                    os.replace(temporary, self.path)
                    temporary = None
                    directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                    try:
                        os.fsync(directory)
                    finally:
                        os.close(directory)
                    self._checkpoint = (candidate_bytes, state)
                    return {'status': 'committed', 'receipt': _receipt(serialized), 'error': None}
                finally:
                    if temporary is not None:
                        temporary.unlink(missing_ok=True)
        except ERROR as error:
            return {'status': 'rejected', 'receipt': None, 'error': {'code': error.code, 'message': str(error),
                'message_id': message.get('message_id') if message else None,
                'request_id': message.get('request_id') if message else None, 'field': error.field}}
        except FileExistsError:
            return {'status': 'rejected', 'receipt': None, 'error': {'code': 'P_HEAD',
                'message': 'Concurrent governed operation; retry against current state',
                'message_id': None, 'request_id': None, 'field': None}}
        except (ValueError, OSError, KeyError, TypeError):
            return {'status': 'rejected', 'receipt': None, 'error': {'code': 'P_INTEGRITY',
                'message': 'Governed history, L0 authority or exact material unavailable',
                'message_id': None, 'request_id': None, 'field': None}}

    def evaluate(self, subject, scope='default'):
        """Return internal exact-version assessment; for the local operator; this grants no permission.

        Args:
            subject: Exact stored output reference.
            scope: Authorized applicability scope.
        Returns:
            Shared qualification, acceptance, release and dependency assessment.
        """
        return self.read().evaluate(subject, scope)

    def current_basis(self, query):
        """Assess an exact output for the local operator without a read credential.

        Args:
            query: Closed protocol query with exact subject and assessment scope.
        Returns:
            Current-basis response, never an acceptance or release permission.
        Raises:
            ProtocolError: Query shape, engagement or exact subject is invalid.
        """
        wire.validate(query, 'query.schema.json')
        if set(query) != {'protocol', 'subject', 'assessment_scope'}:
            raise ERROR('P_SCHEMA', 'Current-basis request required')
        state = self.read()
        if query['subject']['engagement'] != self.engagement:
            raise ERROR('P_SCOPE', 'Requested subject belongs to another engagement')
        result = state.evaluate(query['subject'], query['assessment_scope'])
        return {'protocol': PROTOCOL, 'subject': query['subject'], 'assessment_scope': query['assessment_scope'],
                'assessed_at_ms': int(time.time() * 1000), 'head': state.head,
                'selected': [{'slot': json.loads(key[1]), 'version': reference, 'use_scope': key[0]} for key, reference in state.selections.items()
                             if key[0] == query['assessment_scope'] and state._point(reference, key[0]) in result['closure']],
                'closure': result['closure'], 'evidence': result['evidence'], 'proofs': result['proofs'],
                'review_dispositions': result['review_dispositions'],
                'established_by': result['established_by'], 'cancelled_by': result['cancelled_by'],
                'conflicts': result['conflicts'], 'eligibility': {key: result[key] for key in ('qualified', 'accepted', 'release_eligible', 'reasons')}}
