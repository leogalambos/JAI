# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Immutable format-2 lifecycle identities, replay, transactions and exact gates.

All semantic values are integer/string JSON. Signed operator wrappers have their
own serialization and are bound separately by exact canonical wrapper bytes.
No legacy ledger reader or authority credential is provided here.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import unicodedata
import uuid

VERSION_DOMAIN = b'jai.lifecycle.version.v2\0'
BLOB_DOMAIN = b'jai.lifecycle.blob.v2\0'
TRANSACTION_DOMAIN = b'jai.lifecycle.transaction.v2\0'
CATEGORIES = ('source', 'test', 'configuration', 'environment', 'contract', 'policy', 'assumptions')
OPERATIONS = {'init', 'version', 'select', 'state', 'rely', 'proof-select', 'verify-select', 'node', 'edge', 'locate', 'routine'}
ZERO = '0' * 64


class LifecycleError(ValueError):
    """Reject malformed identity, immutable history, selection or gate input."""


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
    """Return strict canonical UTF-8 bytes; raise LifecycleError for invalid JSON."""
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
    """Return domain-separated immutable identity of a canonical manifest."""
    return hashlib.sha256(VERSION_DOMAIN + canonical(value)).hexdigest()


def policy():
    """Return fresh governed obligations; callers cannot weaken these defaults.

    A contract must explicitly declare its categories and proof roles. Conclusions
    without such a governing contract remain unusable rather than receiving
    invented inapplicability reasons.
    """
    supervision = Path(__file__).resolve().parents[1] / 'fabric/supervision-policy.json'
    return {'schema': 'jai.lifecycle.policy/2', 'categories': list(CATEGORIES),
            'supervision_digest': hashlib.sha256(supervision.read_bytes()).hexdigest(),
            'required_evidence_roles': ['evidence'], 'review_roles': ['reviewer'],
            'acceptance_role': 'accept', 'contract_exclusions_require_review': True,
            'routine_profile': 'jai.layer-review/1',
            'observation_profile': 'jai.byte-observation/1',
            'top_output_profile': 'jai.intent-output/1'}


def graph_reliance(edge, scope='default'):
    """Derive the mandatory exact causal dependency of a graph edge.

    Args:
        edge: Validated typed graph edge with exact endpoint versions.
        scope: Graph's governing lifecycle scope, defaulting to default.
    Returns:
        Required reliance payload, or None for a noncausal graph relation.
    Raises:
        KeyError: A causal edge lacks its exact endpoint version fields.
    """
    label = edge['label']
    if label in {'supports', 'requests', 'derives', 'refines', 'consolidated_into'}:
        role = ('evidence' if label in {'supports', 'consolidated_into'}
                else 'contract' if label == 'requests' else 'requirement')
        return {'dependent': edge['dst_version'], 'prerequisite': edge['src_version'],
                'scope': scope, 'role': role}
    if label == 'implements':
        return {'dependent': edge['src_version'], 'prerequisite': edge['dst_version'],
                'scope': scope, 'role': 'requirement'}
    return None


def envelope(engagement, previous, sequence, operations, proof=None, transaction_id=None):
    """Build an atomic transaction envelope without granting operator authority.

    Args:
        engagement: Exact engagement identity.
        previous: Expected ledger head hash.
        sequence: One-based transaction sequence.
        operations: Complete ordered operation objects.
        proof: Optional independently verified request/receipt wrapper.
        transaction_id: Optional request UUID, otherwise a fresh UUID.
    Returns:
        Complete envelope with semantic hash and optional proof wrapper.
    Raises:
        LifecycleError: Invalid semantic data.
    """
    value = {'format': 2, 'engagement': engagement, 'sequence': sequence,
             'previous': previous, 'transaction_id': transaction_id or str(uuid.uuid4()),
             'timestamp': int(time.time() * 1000), 'operations': copy.deepcopy(operations)}
    if proof is not None:
        import operator_actions
        value['proof_digest'] = hashlib.sha256(operator_actions.canonical(proof)).hexdigest()
    value['hash'] = hashlib.sha256(TRANSACTION_DOMAIN + canonical(value)).hexdigest()
    if proof is not None:
        value['proof'] = proof
    return value


def read(path, engagement=None, proof_verifier=None):
    """Load only complete format-2 envelopes and validate replay globally.

    Args:
        path: Nonsymlink regular ledger file.
        engagement: Optional expected engagement identity.
        proof_verifier: Callback(transaction, prior transactions), required for proofs.
    Returns:
        Validated immutable transaction list.
    Raises:
        LifecycleError: Unsupported format, corrupt chain or invalid proof.
        OSError: Unreadable file.
    """
    import operator_actions
    raw = operator_actions.regular(path)
    transactions = []
    for line in raw.splitlines():
        if not line.strip():
            raise LifecycleError('blank ledger line is not a transaction')
        # Wrapper floats are parsed using their own protocol; semantic fields
        # subsequently pass strict canonical validation in replay.
        def pairs(items):
            result = {}
            for key, value in items:
                if normal(key) in result:
                    raise LifecycleError('duplicate JSON key')
                result[normal(key)] = value
            return result
        transactions.append(json.loads(line, object_pairs_hook=pairs))
    if not transactions:
        raise LifecycleError('empty ledger is not an initialized engagement')
    replay(transactions, engagement, proof_verifier)
    return transactions


def replay(transactions, engagement=None, proof_verifier=None):
    """Validate envelopes and return deterministic lifecycle indexes.

    Args:
        transactions: Format-2 envelopes; raw graph rows are never accepted.
        engagement: Optional expected engagement identity.
        proof_verifier: Independent historical proof validation callback.
    Returns:
        State containing immutable versions, selections, proofs and reliance.
    Raises:
        LifecycleError: Corrupt transaction, unsupported operation or invalid state.
    """
    state = State()
    previous, identities = ZERO, set()
    for number, tx in enumerate(transactions, 1):
        required = {'format', 'engagement', 'sequence', 'previous', 'transaction_id', 'timestamp', 'operations', 'hash'}
        if not isinstance(tx, dict) or not required <= set(tx) or set(tx) - required - {'proof', 'proof_digest'}:
            raise LifecycleError('unsupported ledger; archive and reconstruct a fresh engagement')
        if tx['format'] != 2 or tx['sequence'] != number or tx['previous'] != previous:
            raise LifecycleError('unsupported format or broken transaction chain')
        if type(tx['sequence']) is not int or type(tx['timestamp']) is not int:
            raise LifecycleError('integer sequence and millisecond timestamp required')
        try:
            if str(uuid.UUID(tx['transaction_id'])) != tx['transaction_id']:
                raise ValueError('noncanonical UUID')
        except (ValueError, TypeError, AttributeError) as exc:
            raise LifecycleError('canonical transaction UUID required') from exc
        if engagement is None:
            engagement = tx['engagement']
        if tx['engagement'] != engagement or tx['transaction_id'] in identities:
            raise LifecycleError('cross-engagement transaction or transaction replay')
        identities.add(tx['transaction_id'])
        unsigned = {key: value for key, value in tx.items() if key not in {'hash', 'proof'}}
        if hashlib.sha256(TRANSACTION_DOMAIN + canonical(unsigned)).hexdigest() != tx['hash']:
            raise LifecycleError('transaction semantic hash mismatch')
        if ('proof' in tx) != ('proof_digest' in tx):
            raise LifecycleError('missing operator proof or proof digest')
        if 'proof' in tx:
            import operator_actions
            if hashlib.sha256(operator_actions.canonical(tx['proof'])).hexdigest() != tx['proof_digest']:
                raise LifecycleError('operator proof bytes changed')
            if proof_verifier is None:
                raise LifecycleError('operator proof verifier required')
            proof_verifier(tx, transactions[:number - 1])
        if not isinstance(tx['operations'], list) or not tx['operations']:
            raise LifecycleError('empty transaction')
        for operation in tx['operations']:
            state.apply(operation, authorized='proof' in tx)
            if (operation['op'] == 'version' and 'proof' in tx and
                    tx['proof']['request']['kind'] == 'fabric-review'):
                state.accept_authorities.add(operation['data']['version_id'])
            if operation['op'] == 'version' and 'proof' in tx and tx['proof']['request']['kind'] == 'fabric-authorise':
                state.decision_authorities.add(operation['data']['version_id'])
        previous = tx['hash']
    state.check_cycles()
    return state


class State:
    """Replay-only lifecycle indexes; state changes occur through explicit events."""

    def __init__(self):
        """Create empty indexes; no selection or acceptance exists by default."""
        self.versions = {}
        self.selections = {}
        self.states = {}
        self.scoped_states = {}
        self.locators = {}
        self.reliance = []
        self.proofs = {}
        self.rows = []
        self.initialized = False
        self.accept_authorities = set()
        self.decision_authorities = set()
        self.graph_ids = set()
        self.applicability = {}
        self.verifications = {}
        self.cancelled = set()

    def apply(self, operation, authorized=False):
        """Apply one validated operation to indexes or raise LifecycleError.

        Args:
            operation: Exact op/data pair.
            authorized: Independently verified transaction proof presence.
        Returns:
            None.
        Raises:
            LifecycleError: Unknown operation, invalid selection or immutable collision.
        """
        if not isinstance(operation, dict) or set(operation) != {'op', 'data'} or operation['op'] not in OPERATIONS:
            raise LifecycleError('unknown or malformed lifecycle operation')
        op, data = operation['op'], normal(operation['data'])
        operation = {'op': op, 'data': data}
        if op == 'init':
            if self.initialized or self.rows or self.versions:
                raise LifecycleError('duplicate or late initialization')
            if set(data) != {'policy', 'scope'} or data['policy'].get('schema') != 'jai.lifecycle.policy/2':
                raise LifecycleError('fresh lifecycle policy required')
            self.initialized = True
            governing = manifest('lifecycle-policy', 'policy', data['policy'])
            identifier = version_id(governing)
            self.versions[identifier] = governing
            self.selections[(data['scope'], 'lifecycle-policy')] = identifier
            self.states[identifier] = {'validity': 'valid', 'applicable': True, 'sufficient': True, 'reviewed': True}
            self.scoped_states[(data['scope'], identifier)] = copy.deepcopy(self.states[identifier])
            self.applicability[(data['scope'], identifier)] = True
        elif not self.initialized:
            raise LifecycleError('explicit format-2 initialization required')
        elif op in {'node', 'edge'}:
            if op == 'node':
                identifier = data.get('id')
                if not isinstance(identifier, str) or not identifier.strip() or identifier in self.graph_ids:
                    raise LifecycleError('duplicate or invalid graph identity')
                if data.get('layer') == 0 and not authorized:
                    raise LifecycleError('authority node requires independent operator proof')
                version = data.get('version_id')
                if version not in self.versions or self.versions[version]['logical_id'] != identifier or data.get('object_hash') != 'sha256:' + version:
                    raise LifecycleError('graph identity must bind shared exact version')
                content = {key: value for key, value in data.items() if key not in
                           {'object_ref', 'object_hash', 'version_id', 'file', 'bindings'}}
                expected = self.versions[version]['content']
                if expected.get('blob'):
                    content['blob'] = expected['blob']
                if canonical(content) != canonical(expected) or data.get('bindings', {}) != self.versions[version]['bindings']:
                    raise LifecycleError('graph payload differs from immutable exact manifest')
                self.graph_ids.add(identifier)
            elif (set(data) != {'src', 'label', 'dst', 'src_version', 'dst_version'} or
                    data['src'] not in self.graph_ids or data['dst'] not in self.graph_ids or
                    self.versions.get(data['src_version'], {}).get('logical_id') != data['src'] or
                    self.versions.get(data['dst_version'], {}).get('logical_id') != data['dst']):
                raise LifecycleError('edge subject missing or malformed')
            if op == 'edge':
                if (not authorized and any(
                        self.versions[data[key]]['content'].get('layer') == 0
                        for key in ('src_version', 'dst_version'))):
                    raise LifecycleError('authority edge requires independent operator proof')
                required = graph_reliance(data)
                if required is not None and required not in self.reliance:
                    raise LifecycleError('actual graph edge lacks exact causal reliance')
            self.rows.append(copy.deepcopy(operation))
        elif op == 'version':
            if set(data) != {'version_id', 'manifest'} or version_id(data['manifest']) != data['version_id']:
                raise LifecycleError('version identity mismatch')
            value = data['manifest']
            if (set(value) != {'schema', 'logical_id', 'kind', 'content', 'bindings', 'members'} or
                    value['schema'] != 'jai.lifecycle.manifest/2' or not isinstance(value['content'], dict) or
                    not isinstance(value['bindings'], dict) or not isinstance(value['members'], list) or
                    not isinstance(value['logical_id'], str) or not value['logical_id'].strip() or
                    not isinstance(value['kind'], str) or not value['kind'] or 'locator' in value):
                raise LifecycleError('strict version manifest schema required')
            if canonical(manifest(value['logical_id'], value['kind'], value['content'], value['bindings'], value['members'])) != canonical(value):
                raise LifecycleError('composite manifest members must be canonical and unique')
            identifier = data['version_id']
            if identifier in self.versions and canonical(self.versions[identifier]) != canonical(data['manifest']):
                raise LifecycleError('immutable version collision')
            self.versions[identifier] = data['manifest']
            self.states.setdefault(identifier, {'validity': 'pending', 'applicable': False,
                                               'sufficient': False, 'reviewed': False})
        elif op == 'select':
            if set(data) != {'scope', 'logical_id', 'version_id', 'previous'}:
                raise LifecycleError('exact selection fields required')
            key = (data['scope'], data['logical_id'])
            old = self.selections.get(key)
            if old != data['previous'] or (old is not None and not authorized):
                raise LifecycleError('selection conflict or governed replacement required')
            if self.versions.get(data['version_id'], {}).get('logical_id') != data['logical_id']:
                raise LifecycleError('selection refers to missing or substituted version')
            self.selections[key] = data['version_id']
        elif op == 'state':
            if not authorized:
                raise LifecycleError('qualification and cancellation require governed transaction')
            if set(data) != {'version_id', 'scope', 'changes'} or data['version_id'] not in self.versions:
                raise LifecycleError('state subject missing')
            changes = data['changes']
            if not changes or set(changes) - {'validity', 'applicable', 'sufficient', 'reviewed'}:
                raise LifecycleError('unknown state predicate')
            if 'validity' in changes and changes['validity'] not in {'valid', 'invalid', 'revoked', 'pending'}:
                raise LifecycleError('unknown validity state')
            if any(type(value) is not bool for key, value in changes.items() if key != 'validity'):
                raise LifecycleError('state predicates require boolean values')
            current = self.predicates(data['version_id'], data['scope'])
            if (current['validity'] in {'invalid', 'revoked'} and changes.get('validity') == 'valid'
                    and self.versions[data['version_id']]['kind'] in {'frag', 'conclusion', 'rev', 'acceptance', 'permission'}):
                raise LifecycleError('cancelled version cannot be reactivated; fresh verification required')
            current.update(changes)
            if changes.get('validity') in {'invalid', 'revoked'}:
                self.cancelled.add((data['scope'], data['version_id']))
            self.scoped_states[(data['scope'], data['version_id'])] = current
            if data['scope'] == 'default':
                self.states[data['version_id']] = current
            if 'applicable' in changes:
                self.applicability[(data['scope'], data['version_id'])] = changes['applicable']
        elif op == 'rely':
            if (set(data) not in ({'dependent', 'prerequisite', 'scope', 'role'},
                                  {'dependent', 'prerequisite', 'scope', 'role', 'prerequisite_scope'}) or not data['role']):
                raise LifecycleError('exact scoped reliance fields required')
            if any(data[key] not in self.versions for key in ('dependent', 'prerequisite')):
                raise LifecycleError('declared prerequisite missing')
            if data not in self.reliance:
                self.reliance.append(data)
        elif op == 'proof-select':
            if not authorized:
                raise LifecycleError('new governing proof selection requires governed transaction')
            if set(data) != {'scope', 'subject', 'role', 'proof', 'previous'}:
                raise LifecycleError('exact proof selection fields required')
            key = (data['scope'], data['subject'], data['role'])
            old = self.proofs.get(key)
            if old != data['previous'] or (old is not None and not authorized):
                raise LifecycleError('ambiguous proof or governed selection required')
            if data['subject'] not in self.versions or data['proof'] not in self.versions:
                raise LifecycleError('proof selection subject missing')
            self.proofs[key] = data['proof']
        elif op == 'verify-select':
            if (not authorized or set(data) != {'scope', 'subject', 'evidence', 'path'} or
                    data['subject'] not in self.versions or not data['evidence'] or not data['path'] or
                    any(identifier not in self.versions for identifier in data['evidence'])):
                raise LifecycleError('governed exact verification proof selection required')
            self.verifications[(data['scope'], data['subject'])] = data
        elif op == 'locate':
            if set(data) != {'version_id', 'path'} or data['version_id'] not in self.versions:
                raise LifecycleError('locator subject missing')
            existing = self.locators.get(data['version_id'])
            if existing is not None and existing != data['path'] and not authorized:
                raise LifecycleError('existing locator replacement requires governed exact effects')
            self.locators[data['version_id']] = data['path']
        elif op == 'routine':
            self._routine(data)

    def _routine(self, data):
        """Reconstruct bounded first-qualification effects without authority rights.

        The event carries no effects or caller-selected predicates. Its fixed
        family validates the exact existing subject and derives only initial
        qualification. Replacement, cancellation and L0 rights stay governed.
        """
        if set(data) != {'family', 'subject', 'scope'} or data['scope'] != 'default':
            raise LifecycleError('exact routine verification event required')
        subject, scope, family = data['subject'], data['scope'], data['family']
        value = self.versions.get(subject)
        if not value or self.selections.get((scope, value['logical_id'])) != subject:
            raise LifecycleError('routine subject must be exact current selection')
        if (self.predicates(subject, scope)['validity'] != 'pending'
                or (scope, subject) in self.cancelled):
            raise LifecycleError('routine qualification requires a fresh pending subject')
        kind, content = value['kind'], value['content']
        rows = [row['data'] for row in self.rows if row['op'] == 'edge']
        node = next((row['data'] for row in self.rows if row['op'] == 'node'
                     and row['data']['version_id'] == subject), None)
        changes = {'validity': 'valid', 'applicable': True,
                   'sufficient': False, 'reviewed': False}
        if family == 'structure':
            if not node or kind not in {'intent', 'req', 'ctr', 'att'} or not content.get('text'):
                raise LifecycleError('routine structural record missing')
            parents = [edge for edge in rows if edge['dst_version'] == subject]
            if kind == 'intent':
                ready = node['layer'] == 1
            elif kind == 'req':
                ready = False
                for edge in parents:
                    parent = self.versions[edge['src_version']]
                    parent_layer = parent['content'].get('layer')
                    ready |= (
                        edge['label'] == 'derives' and parent['kind'] == 'intent'
                        and parent_layer == node['layer'] == 1) or (
                        edge['label'] == 'refines' and parent['kind'] == 'ctr'
                        and parent['content'].get('target_layer') == node['layer'] == parent_layer + 1) or (
                        edge['label'] == 'refines' and parent['kind'] == 'req'
                        and parent_layer == node['layer']) or (
                        edge['label'] == 'revises' and parent['kind'] == 'auth'
                        and edge['src_version'] in self.decision_authorities and node['layer'] == 1)
            elif kind == 'ctr':
                fields = content.get('fields', {})
                ready = (content.get('target_layer') == node['layer'] + 1
                         and all(fields.get(key) for key in (
                             'what', 'why', 'who', 'where', 'when', 'how',
                             'evidence', 'escalate_if', 'sanitise'))
                         and any(edge['label'] == 'derives'
                                 and self.versions[edge['src_version']]['kind'] == 'req'
                                 and self.versions[edge['src_version']]['content'].get('layer') == node['layer']
                                 for edge in parents))
            else:
                ready = any(edge['label'] == 'attempts'
                            and self.versions[edge['src_version']]['kind'] == 'ctr'
                            and self.versions[edge['src_version']]['content'].get('target_layer') == node['layer']
                            for edge in parents)
            if not ready:
                raise LifecycleError('structural record lacks required exact parent relation')
            for edge in parents:
                parent = self.versions[edge['src_version']]
                if (self.selections.get((scope, parent['logical_id'])) != edge['src_version']
                        or self.predicates(edge['src_version'], scope)['validity'] != 'valid'):
                    raise LifecycleError('structural parent is not current and valid')
        elif family == 'input':
            if (node or kind not in set(CATEGORIES) - {'contract', 'policy'}
                    or not content.get('blob') or subject not in self.locators
                    or content.get('capture_profile') != 'jai.byte-observation/1'):
                raise LifecycleError('initial input requires exact byte-bound source record')
        elif family == 'observation':
            if (kind not in {'evd', 'evidence'} or not content.get('blob')
                    or content.get('confidence') not in {'deterministic', 'observation'}
                    or subject not in self.locators or not value['bindings'].get('source', {}).get('refs')):
                raise LifecycleError('observation requires exact source and captured bytes')
            assessment = self._evaluate(subject, routine_subject=subject, read_content=False)
            if not assessment['eligible']:
                raise LifecycleError('observation inputs unqualified: ' + str(assessment['reasons']))
            changes['sufficient'] = True
        elif family == 'review':
            if kind != 'rev' or not node or node['layer'] < 1:
                raise LifecycleError('routine review cannot exercise human authority')
            target = content.get('subject')
            target_value = self.versions.get(target, {})
            contract = content.get('issuer_contract')
            issuer = self.versions.get(contract, {})
            profile = self.versions[self.selections[(scope, 'lifecycle-policy')]]['content'].get('routine_profile')
            target_layer = target_value.get('content', {}).get('layer')
            if (content.get('profile') != profile or not profile
                    or target_value.get('kind') != 'frag'
                    or node['layer'] != target_layer - 1
                    or issuer.get('kind') != 'ctr'
                    or issuer['content'].get('layer') != node['layer']
                    or target_value.get('content', {}).get('contract') != issuer['logical_id']
                    or target_value.get('bindings', {}).get('contract', {}).get('refs') != [contract]
                    or [edge['src_version'] for edge in rows
                        if edge['label'] == 'requests' and edge['dst_version'] == target] != [contract]
                    or self.selections.get((scope, issuer['logical_id'])) != contract
                    or content.get('state') not in {'accepts', 'accepts_with_constraints'}
                    or (content.get('state') == 'accepts_with_constraints' and not content.get('constraints'))
                    or not any(edge['label'] == 'reviewed_by' and edge['src_version'] == target
                               and edge['dst_version'] == subject for edge in rows)):
                raise LifecycleError('review lacks exact issuer, adjacency or maintained role profile')
            if self.proofs.get((scope, target, 'reviewer')) is not None:
                raise LifecycleError('routine review cannot replace a governing proof')
            if self.predicates(target, scope)['validity'] != 'pending':
                raise LifecycleError('routine review requires a fresh pending conclusion')
            assessment = self._evaluate(target, routine_subject=target, read_content=False)
            if (not assessment['eligible'] or content.get('assessed_closure') != assessment['contexts']
                    or content.get('assessed_hash') != assessment['closure_hash']):
                raise LifecycleError('review does not bind all exact qualified dependencies')
            for point in assessment['contexts']:
                relation = {'dependent': subject, 'prerequisite': point['version_id'],
                            'scope': scope, 'prerequisite_scope': point['scope'], 'role': 'assessed-input'}
                if relation not in self.reliance:
                    self.reliance.append(relation)
            self.proofs[(scope, target, 'reviewer')] = subject
            target_changes = {'validity': 'valid', 'applicable': True,
                              'sufficient': True, 'reviewed': True}
            self.scoped_states[(scope, target)] = target_changes
            self.states[target] = copy.deepcopy(target_changes)
            self.applicability[(scope, target)] = True
            changes.update(sufficient=True, reviewed=True)
        elif family == 'answer':
            contract_refs = value['bindings'].get('contract', {}).get('refs', [])
            requirement = content.get('requirement')
            requirement_version = self.selections.get((scope, requirement))
            if (kind != 'frag' or not node or node['layer'] != 1
                    or content.get('profile') != 'jai.intent-output/1'
                    or not requirement_version
                    or len(contract_refs) != 1
                    or not any(edge['label'] == 'derives'
                               and edge['src_version'] == requirement_version
                               and edge['dst_version'] == contract_refs[0] for edge in rows)
                    or not any(edge['label'] == 'requests' and edge['dst_version'] == subject
                               and edge['src_version'] == requirement_version for edge in rows)
                    or not any(edge['label'] == 'supports' and edge['dst_version'] == subject
                               and self.versions[edge['src_version']]['kind'] == 'frag'
                               and self.versions[edge['src_version']]['content'].get('layer') == 2
                               for edge in rows)):
                raise LifecycleError('intent answer requires exact requirement and reviewed child')
            assessment = self._evaluate(subject, routine_subject=subject, read_content=False)
            if not assessment['eligible']:
                raise LifecycleError('answer inputs unqualified: ' + str(assessment['reasons']))
            changes['sufficient'] = True
        else:
            raise LifecycleError('unknown routine verification family')
        self.scoped_states[(scope, subject)] = changes
        self.states[subject] = copy.deepcopy(changes)
        self.applicability[(scope, subject)] = True

    def effects(self, spec, read_content=True):
        """Derive complete governed replacement/cancellation/verification operations.

        Args:
            spec: Scope, reason, proposed versions, selections, reinstatements,
                verification events and allowed verification path.
            read_content: Validate current observation bytes during planning/apply,
                false for historical immutable-effect verification.
        Returns:
            Deterministic effect list, including cross-scope cancellations.
        Raises:
            LifecycleError: Unknown fields, missing predecessor or unsafe reinstatement.
        """
        fields = {'scope', 'reason', 'proposed', 'selections', 'reinstatements',
                  'verification', 'allowed_verification_path', 'invalidations', 'proofs'}
        if not isinstance(spec, dict) or set(spec) != fields or not spec['reason'] or not spec['allowed_verification_path']:
            raise LifecycleError('complete typed lifecycle update specification required')
        scope, result, roots, relations = spec['scope'], [], set(), []
        for identifier in spec['invalidations']:
            if identifier not in self.versions:
                raise LifecycleError('unknown invalidation subject')
            roots.add(identifier)
        proposed = {}
        for item in spec['proposed']:
            if set(item) not in ({'manifest'}, {'manifest', 'locator'}):
                raise LifecycleError('unknown proposed version fields')
            value = item['manifest']
            identifier = version_id(value)
            if identifier in proposed:
                raise LifecycleError('duplicate proposed version')
            proposed[identifier] = value
            result.append({'op': 'version', 'data': {'version_id': identifier, 'manifest': value}})
            for role, binding in value['bindings'].items():
                for prerequisite in binding.get('refs', []):
                    relations.append({'op': 'rely', 'data': {'dependent': identifier, 'prerequisite': prerequisite, 'scope': scope, 'role': role}})
            for member in value['members']:
                relations.append({'op': 'rely', 'data': {'dependent': identifier, 'prerequisite': member['version_id'], 'scope': scope, 'role': member['role']}})
            if value['kind'] in {'rev', 'review'} and value['content'].get('subject'):
                relations.append({'op': 'rely', 'data': {'dependent': identifier, 'prerequisite': value['content']['subject'], 'scope': scope, 'role': 'subject'}})
            governing = self.selections.get((scope, 'lifecycle-policy'))
            if governing and value['logical_id'] != 'lifecycle-policy':
                relations.append({'op': 'rely', 'data': {'dependent': identifier, 'prerequisite': governing, 'scope': scope, 'role': 'governing-policy'}})
            if 'locator' in item:
                result.append({'op': 'locate', 'data': {'version_id': identifier, 'path': item['locator']}})
        result.extend(relations)
        selected = set()
        for item in spec['selections']:
            if set(item) != {'logical_id', 'version_id'} or item['logical_id'] in selected:
                raise LifecycleError('duplicate or unknown governing selection fields')
            selected.add(item['logical_id'])
            old = self.selections.get((scope, item['logical_id']))
            new = item['version_id']
            value = proposed.get(new, self.versions.get(new))
            if not value or value['logical_id'] != item['logical_id'] or new == old:
                raise LifecycleError('missing, unchanged or substituted selection')
            if new in self.versions and new not in spec['reinstatements']:
                raise LifecycleError('historical selection requires explicit reinstatement')
            if old:
                roots.add(old)
            result.append({'op': 'select', 'data': {'scope': scope, 'logical_id': item['logical_id'], 'version_id': new, 'previous': old}})
        if set(spec['reinstatements']) != {item['version_id'] for item in spec['selections'] if item['version_id'] in self.versions}:
            raise LifecycleError('unused or missing reinstatement')
        affected_contexts = self.affected_contexts(roots, scope)
        affected = sorted({point['version_id'] for point in affected_contexts})
        for point in affected_contexts:
            result.append({'op': 'state', 'data': {**point,
                           'changes': {'validity': 'invalid', 'applicable': False,
                                       'sufficient': False, 'reviewed': False}}})
        for verification in spec['verification']:
            if set(verification) != {'version_id', 'evidence', 'path', 'changes'}:
                raise LifecycleError('typed fresh verification required')
            subject = verification['version_id']
            if subject in proposed or {'scope': scope, 'version_id': subject} in affected_contexts or subject not in self.versions:
                raise LifecycleError('new or cancelled replacement must await fresh verification')
            if verification['path'] != spec['allowed_verification_path'] or not verification['evidence']:
                raise LifecycleError('verification path/evidence missing')
            for evidence in verification['evidence']:
                value = self.versions.get(evidence, {})
                if value.get('kind') not in {'evd', 'evidence'}:
                    raise LifecycleError('fresh distinct observation evidence required')
                if not value.get('content', {}).get('blob'):
                    raise LifecycleError('verification evidence must bind exact observed bytes')
                try:
                    import operator_actions
                    if read_content and blob(operator_actions.regular(self.locators[evidence])) != value['content']['blob']:
                        raise LifecycleError('verification evidence content changed')
                except (OSError, KeyError) as exc:
                    raise LifecycleError('verification evidence unavailable') from exc
            result.append({'op': 'verify-select', 'data': {'scope': scope, 'subject': subject,
                           'evidence': verification['evidence'], 'path': verification['path']}})
            result.append({'op': 'state', 'data': {'version_id': subject, 'scope': scope, 'changes': verification['changes']}})
        for proof in spec['proofs']:
            if set(proof) != {'subject', 'role', 'proof'} or proof['role'] in {'accept', 'permission'}:
                raise LifecycleError('lifecycle update cannot grant human acceptance/permission')
            key = (scope, proof['subject'], proof['role'])
            result.append({'op': 'proof-select', 'data': {**proof, 'scope': scope, 'previous': self.proofs.get(key)}})
        if not result:
            raise LifecycleError('empty lifecycle update')
        return {'operations': result, 'affected': affected, 'affected_contexts': affected_contexts}

    def predicates(self, identifier, scope='default'):
        """Return a copy of exact scoped predicates, pending when not qualified.

        Args:
            identifier: Exact immutable version ID.
            scope: Applicability and qualification context.
        Returns:
            Independent validity, applicability, sufficiency and review predicates.
        Raises:
            LifecycleError: The immutable version does not exist.
        """
        if identifier not in self.versions:
            raise LifecycleError('predicate subject missing')
        return copy.deepcopy(self.scoped_states.get((scope, identifier),
            {'validity': 'pending', 'applicable': False, 'sufficient': False, 'reviewed': False}))

    def check_cycles(self):
        """Reject causal cycles in scoped nodes, including explicit cross-scope paths."""
        visiting, done = set(), set()
        def visit(point):
            if point in visiting:
                raise LifecycleError('scoped reliance cycle')
            if point in done:
                return
            visiting.add(point)
            context, identifier = point
            for edge in self.reliance:
                if edge['dependent'] == identifier and edge['scope'] == context:
                    visit((edge.get('prerequisite_scope', context), edge['prerequisite']))
            visiting.remove(point)
            done.add(point)
        for edge in self.reliance:
            visit((edge['scope'], edge['dependent']))

    def affected_contexts(self, roots, scope):
        """Return complete impacted scope/version pairs without invalidating other uses.

        Args:
            roots: Exact prerequisite versions changed in scope.
            scope: Starting governing context; cross-scope edges remain traversable.
        Returns:
            Sorted context objects naming every affected exact version.
        Raises:
            LifecycleError: Any root version is missing.
        """
        if any(identifier not in self.versions for identifier in roots):
            raise LifecycleError('impact root missing')
        result = {(scope, identifier) for identifier in roots}
        while True:
            expanded = result | {(edge['scope'], edge['dependent']) for edge in self.reliance
                if (edge.get('prerequisite_scope', edge['scope']), edge['prerequisite']) in result}
            expanded |= {(context, subject) for (context, subject), proof in self.verifications.items()
                         if any((context, evidence) in result for evidence in proof['evidence'])}
            expanded |= {(context, proof) for (context, subject, role), proof in self.proofs.items()
                         if (context, subject) in result}
            if expanded == result:
                return [{'scope': context, 'version_id': identifier} for context, identifier in sorted(result)]
            result = expanded

    def affected(self, roots, scope=None):
        """Return impacted exact versions, optionally starting from a single scope.

        Args:
            roots: Exact versions whose dependents are requested.
            scope: Explicit starting context, or all declared contexts for a global report.
        Returns:
            Sorted unique immutable version IDs; affected_contexts preserves scope detail.
        Raises:
            LifecycleError: Any root is missing.
        """
        contexts = {scope} if scope is not None else {context for context, logical in self.selections}
        contexts |= {edge.get('prerequisite_scope', edge['scope']) for edge in self.reliance
                     if scope is None and edge['prerequisite'] in roots}
        points = [point for context in contexts for point in self.affected_contexts(roots, context)]
        return sorted({point['version_id'] for point in points})

    def evaluate(self, output, scope='default', release=False):
        """Evaluate all governed slots and selected exact proofs conjunctively.

        Args:
            output: Exact output version ID.
            scope: Governing selection scope.
            release: Require separately authorized exact acceptance and permission.
        Returns:
            Eligibility, reasons, sorted preacceptance closure and closure identity.
        Raises:
            LifecycleError: Reliance cycle or malformed semantic manifests.
        """
        return self._evaluate(output, scope, release, read_content=True, historical=False)

    def _evaluate(self, output, scope='default', release=False, read_content=True, historical=False, assessment=None, routine_subject=None):
        """Reconstruct exact proof closure; archived policy evaluation never grants release."""
        if historical and release:
            raise LifecycleError('historical proof reconstruction cannot grant current release')
        if historical and assessment is None:
            raise LifecycleError('archived immutable assessment context required')
        read_content = read_content and not historical
        evaluation_time = assessment['timestamp'] / 1000 if assessment else time.time()
        self.check_cycles()
        reasons, closure, checked, contexts = [], set(), set(), set()
        def visit(identifier, require_review=True, context=None):
            context = scope if context is None else context
            if (identifier, require_review, context) in checked:
                return
            checked.add((identifier, require_review, context))
            contexts.add((context, identifier))
            closure.add(identifier)
            value = self.versions.get(identifier)
            if value is None:
                reasons.append('missing required version ' + identifier)
                return
            if version_id(value) != identifier:
                reasons.append('manifest integrity failure ' + identifier)
            if self.selections.get((context, value['logical_id'])) != identifier:
                reasons.append('missing or noncurrent governing selection ' + value['logical_id'])
            predicates = self.predicates(identifier, context)
            if identifier != routine_subject and (predicates['validity'] != 'valid' or not self.applicability.get((context, identifier), False)):
                reasons.append('invalid or inapplicable required version ' + identifier)
            context_policy = self.selections.get((context, 'lifecycle-policy'))
            if context_policy is None:
                reasons.append('missing governing policy in required scope ' + context)
            elif identifier != context_policy:
                visit(context_policy, False, context)
                if not historical and self.versions[context_policy]['content'] != policy():
                    reasons.append('governing policy changed in required scope ' + context)
            governing_rules = self.versions[context_policy]['content'] if context_policy else policy()
            kind = value['kind']
            verification = self.verifications.get((context, identifier))
            if verification is not None:
                for evidence in verification['evidence']:
                    visit(evidence, context=context)
            if identifier != routine_subject and kind in {'evd', 'evidence', 'frag', 'conclusion'} and not predicates['sufficient']:
                reasons.append('insufficient required version ' + identifier)
            content = value['content']
            if read_content and content.get('blob'):
                try:
                    import operator_actions
                    if blob(operator_actions.regular(self.locators[identifier])) != content['blob']:
                        reasons.append('required content changed ' + identifier)
                except (OSError, ValueError, KeyError):
                    reasons.append('required content unreadable ' + identifier)
            edges = [edge for edge in self.reliance if edge['dependent'] == identifier and edge['scope'] == context]
            if kind in {'frag', 'conclusion', 'evd', 'evidence'}:
                bindings = value['bindings']
                contract_refs = bindings.get('contract', {}).get('refs', [])
                governing = self.versions.get(contract_refs[0], {}) if len(contract_refs) == 1 else {}
                obligations = governing.get('content', {}).get('obligations')
                if (governing.get('kind') not in {'ctr', 'contract'} or not isinstance(obligations, dict) or
                        set(obligations) != {'categories', 'evidence_roles', 'review_roles'}):
                    reasons.append('exact governing contract obligations missing ' + identifier)
                    obligations = {'categories': {}, 'evidence_roles': [], 'review_roles': []}
                declared = obligations['categories']
                if (not isinstance(declared, dict) or not declared
                        or set(declared) - set(CATEGORIES)
                        or not {'contract', 'policy'} <= set(declared)
                        or set(bindings) != set(declared)):
                    reasons.append('complete declared category bindings required ' + identifier)
                if kind in {'evd', 'evidence'} and 'source' not in bindings:
                    reasons.append('observation source binding required ' + identifier)
                for category in declared:
                    bound = bindings.get(category, {})
                    rule = obligations['categories'].get(category)
                    if not isinstance(rule, dict) or set(rule) != {'minimum', 'allow_exclusion'}:
                        reasons.append('governing category obligation missing ' + category)
                        continue
                    refs = bound.get('refs', [])
                    if refs:
                        if set(bound) != {'refs'} or len(set(refs)) != len(refs) or len(refs) < rule['minimum']:
                            reasons.append('missing or duplicate required category ' + category)
                        for prerequisite in refs:
                            if not any(edge['prerequisite'] == prerequisite and edge['role'] == category for edge in edges):
                                reasons.append('binding lacks declared reliance ' + category)
                            matches = [edge for edge in edges if edge['prerequisite'] == prerequisite and edge['role'] == category]
                            for binding_edge in matches:
                                visit(prerequisite, category not in {'contract', 'policy'}, binding_edge.get('prerequisite_scope', context))
                    else:
                        exclusion = bound.get('exclusion', {})
                        proof = self.proofs.get((context, identifier, 'exclusion:' + category))
                        if (not rule['allow_exclusion'] or set(bound) != {'exclusion'} or
                                not exclusion.get('reason') or not proof):
                            reasons.append('unauthorized category exclusion ' + category)
                        else:
                            visit(proof, False, context)
                            review = self.versions[proof]
                            if (review['kind'] not in {'rev', 'review'} or
                                    review['content'].get('subject') != identifier or
                                    review['content'].get('state') not in {'accepts', 'accepts_with_constraints'}):
                                reasons.append('exclusion lacks independently selected exact review ' + category)
                evidence_roles = set(obligations['evidence_roles']) if kind in {'frag', 'conclusion'} else set()
                if kind in {'frag', 'conclusion'}:
                    evidence_roles.update(governing_rules['required_evidence_roles'])
                for role in sorted(evidence_roles):
                    required = [edge for edge in edges if edge['role'] == role]
                    if not required:
                        reasons.append('missing governed evidence role ' + role)
                top_answer = (kind == 'frag' and content.get('layer') == 1
                              and content.get('requirement')
                              and content.get('profile') == governing_rules.get('top_output_profile'))
                if require_review and identifier != routine_subject and kind in {'frag', 'conclusion'} and not top_answer:
                    for role in sorted(set(obligations['review_roles']) | set(governing_rules['review_roles'])):
                        proof = self.proofs.get((context, identifier, role))
                        if not proof:
                            reasons.append('missing selected review role ' + role)
                        else:
                            visit(proof, False, context)
                            review_value = self.versions[proof]
                            reviewed = review_value['content']
                            proof_edges = [edge for edge in self.reliance if edge['dependent'] == proof and edge['scope'] == context]
                            if (review_value['kind'] not in {'rev', 'review'} or reviewed.get('subject') != identifier or
                                    reviewed.get('state') not in {'accepts', 'accepts_with_constraints'} or
                                    not any(edge['prerequisite'] == identifier and edge['role'] == 'subject' for edge in proof_edges)):
                                reasons.append('selected review does not qualify exact subject')
            if content.get('contradiction'):
                reasons.append('contradiction in required closure ' + identifier)
            for edge in edges:
                visit(edge['prerequisite'], edge['role'] not in {'subject', 'contract', 'policy'}, edge.get('prerequisite_scope', context))
        governing_policy = self.selections.get((scope, 'lifecycle-policy'))
        if governing_policy is None:
            reasons.append('missing governing lifecycle policy selection')
        else:
            visit(governing_policy, False)
            if not historical and self.versions[governing_policy]['content'] != policy():
                reasons.append('governing lifecycle policy changed; fresh governed replacement required')
        visit(output)
        graph_edges = [row['data'] for row in self.rows if row['op'] == 'edge']
        def unresolved(start):
            seen, pending = set(), [start]
            while pending:
                current = pending.pop()
                if current in seen:
                    continue
                seen.add(current)
                for edge in graph_edges:
                    if edge['src_version'] != current:
                        continue
                    if edge['label'] == 'escalates':
                        pending.append(edge['dst_version'])
                    if edge['label'] == 'resolved_by' and edge['dst_version'] in self.decision_authorities:
                        decision = self.versions[edge['dst_version']]['content']
                        if decision.get('decision') == 'accept':
                            return False
                        if decision.get('decision') == 'exception' and decision.get('expires_epoch', 0) > evaluation_time:
                            return False
            return True
        for edge in graph_edges:
            if edge['label'] == 'may_create' and ('default', edge['src_version']) in contexts and unresolved(edge['dst_version']):
                reasons.append('unresolved contradiction in required closure ' + edge['dst_version'])
            if edge['label'] == 'contradicts' and ('default', edge['dst_version']) in contexts:
                contradictory = self.predicates(edge['src_version'], 'default')
                if contradictory['validity'] == 'valid' and self.applicability.get(('default', edge['src_version']), False):
                    reasons.append('applicable contradictory evidence ' + edge['src_version'])
        preacceptance = sorted(closure)
        reliance = sorted((edge for edge in self.reliance if (edge['scope'], edge['dependent']) in contexts and (edge.get('prerequisite_scope', edge['scope']), edge['prerequisite']) in contexts), key=canonical)
        selected = sorted([{'scope': item_scope, 'subject': subject, 'role': role, 'proof': proof}
                           for (item_scope, subject, role), proof in self.proofs.items()
                           if (item_scope, subject) in contexts and role not in {'accept', 'permission'}], key=canonical)
        verification = sorted([value for (item_scope, subject), value in self.verifications.items()
                               if (item_scope, subject) in contexts], key=canonical)
        context_manifest = [{'scope': context, 'version_id': identifier} for context, identifier in sorted(contexts)]
        closure_hash = hashlib.sha256(canonical({'scope': scope, 'members': preacceptance,
                                                 'reliance': reliance, 'proofs': selected,
                                                 'verification': verification, 'contexts': context_manifest, 'policy': governing_policy})).hexdigest()
        if release:
            acceptance = self.proofs.get((scope, output, 'accept'))
            if not acceptance:
                reasons.append('separate human acceptance missing')
            else:
                visit(acceptance, False)
                content = self.versions[acceptance]['content']
                if (content.get('subject') != output or content.get('closure_hash') != closure_hash or
                        content.get('state') not in {'accepts', 'accepts_with_constraints'} or
                        (content.get('state') == 'accepts_with_constraints' and not content.get('constraints')) or
                        acceptance not in self.accept_authorities):
                    reasons.append('acceptance does not bind current exact closure')
                permission = self.proofs.get((scope, output, 'permission'))
                if not permission:
                    reasons.append('release permission missing')
                else:
                    visit(permission, False)
                    permission_content = self.versions[permission]['content']
                    if permission_content.get('subject') != output or permission_content.get('acceptance') != acceptance:
                        reasons.append('permission does not depend on current exact acceptance')
        return {'eligible': not reasons, 'reasons': reasons, 'closure': preacceptance, 'contexts': context_manifest, 'closure_hash': closure_hash}


def commit(path, engagement, expected_head, operations, proof_verifier=None, proof=None, transaction_id=None, candidate_validator=None):
    """Atomically validate and replace the full ledger under an exclusive lock.

    Args:
        path: Ledger path outside protected runtime/configuration directories.
        engagement: Exact engagement identity.
        expected_head: Head observed before command planning, ZERO for init.
        operations: Complete in-memory command batch.
        proof_verifier: Historical and candidate operator proof validator.
        proof: Optional externally signed request/receipt wrapper.
        transaction_id: Optional unique signed request identity.
        candidate_validator: Optional integrated graph validator run before any replacement.
    Returns:
        Committed complete envelope.
    Raises:
        LifecycleError: Concurrent head, invalid candidate or replay.
        OSError: Lock contention or secure-file/atomic-replacement failure.
    """
    import operator_actions
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = str(path) + '.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    temporary = None
    try:
        before = read(path, engagement, proof_verifier) if path.exists() else []
        head = before[-1]['hash'] if before else ZERO
        if head != expected_head:
            raise LifecycleError('engagement changed; replan against current head')
        raw = operator_actions.regular(path) if path.exists() else b''
        transaction = envelope(engagement, head, len(before) + 1, operations, proof, transaction_id)
        replay(before + [transaction], engagement, proof_verifier)
        if candidate_validator is not None:
            candidate_validator(before + [transaction])
        encoded = json.dumps(transaction, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode() + b'\n'
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.lifecycle-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw + encoded)
            stream.flush()
            os.fsync(stream.fileno())
        current = operator_actions.regular(path) if path.exists() else b''
        if current != raw:
            raise LifecycleError('engagement changed during candidate validation')
        os.replace(temporary, path)
        temporary = None
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        return transaction
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        os.close(fd)
        os.unlink(lock)
