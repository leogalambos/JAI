#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Domain assessment helpers and exact governed-store commercial bindings.

Content assessment attestations cannot authorize governed recording, acceptance,
or release. Store writes require independent external dispatch verification.
"""
from __future__ import annotations
import copy, hashlib, hmac, json, re
from pathlib import Path
import lifecycle

def _digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

class TrustedDispatcher:
    """Verify existing review attestations; privileged command dispatch is retired."""
    def __init__(self,key,allowed_commands=(),executable_roots=()):
        if not isinstance(key,bytes) or len(key)<32:
            raise ValueError('host verification key requires at least 32 bytes')
        if allowed_commands or executable_roots:
            raise ValueError('worker execution is not supported; use an operator action')
        self._key=key

    def verify(self, attestation):
        """Verify a dispatcher record and return its authenticated subject binding.

        Args:
            attestation: Untrusted mapping returned by run; no keys loaded from it.
        Returns:
            Verified payload copy, or None for altered/untrusted/failed records.
        """
        if not isinstance(attestation, dict) or set(attestation) != {'payload', 'signature'}:
            return None
        payload = attestation['payload']
        expected = hmac.new(self._key, _digest(payload).encode(), 'sha256').hexdigest()
        if not isinstance(attestation['signature'], str) or not hmac.compare_digest(expected, attestation['signature']):
            return None
        if payload.get('enforcement') != 'bwrap-tested' or payload.get('exit_code') != 0:
            return None
        worker = payload.get('worker_execution', {})
        if (not isinstance(worker, dict) or not isinstance(worker.get('pid'), int) or worker['pid'] <= 0
                or worker.get('execution_id') != payload.get('dispatch_id')
                or not worker.get('execution_id') or worker.get('readonly_inputs') is not True
                or worker.get('fresh_namespace') is not True
                or payload.get('principal') != f"uid:{worker.get('uid')}:worker:{worker['pid']}:execution:{worker['execution_id']}"):
            return None
        return copy.deepcopy(payload)


def verification_callbacks(dispatcher, snapshot_digest, context_digest):
    """Create host callbacks pinned to one exact snapshot and execution context.

    Args:
        dispatcher: TrustedDispatcher configured by the host, never agent JSON.
        snapshot_digest: Exact immutable input snapshot digest.
        context_digest: Exact host-approved context manifest digest.
    Returns:
        identity and enforcement callbacks for commercial_core.readiness; recovery
        remains unsupported and requires independent deployment qualification.
    """
    def identity(attestation):
        payload = dispatcher.verify(attestation)
        if not payload or payload.get('snapshot_digest') != snapshot_digest or payload.get('context_digest') != context_digest:
            return None
        return payload

    def enforcement(control, attestation):
        payload = identity(attestation)
        return False  # An attested claim does not independently measure host enforcement.
    return {'identity_verifier': identity, 'enforcement_verifier': enforcement}


def provider_boundary(provider):
    """Return conservative static provider configuration, never live qualification.

    Args:
        provider: codex or claude adapter identity.
    Returns:
        Configuration requiring external mount enforcement and denying delegation.
    Raises:
        ValueError: Unsupported provider.
    """
    if provider not in {'codex', 'claude'}:
        raise ValueError('unknown provider')
    return {'provider': provider, 'status': 'not_run', 'live_qualified': False,
            'history_policy': 'fresh', 'network': False, 'tools': ['Read'],
            'denied_tools': ['Agent', 'Write', 'Edit', 'Bash', 'Shell', 'WebFetch'],
            'external_readonly_mount_required': True, 'authority_capability': False}


def _binding_mapping(store, mapping):
    if not isinstance(store, lifecycle.Store):
        raise ValueError('host-opened governed Store required')
    required = {'domain_contract_version', 'domain_digest', 'claim_ids', 'claim_digests',
                'assignment', 'layer', 'outputs'}
    if (not isinstance(mapping, dict) or set(mapping) != required
            or type(mapping['layer']) is not int or mapping['layer'] not in range(1, 7)
            or not isinstance(mapping['domain_contract_version'], str) or not mapping['domain_contract_version']
            or not isinstance(mapping['claim_ids'], list) or not mapping['claim_ids']
            or any(not isinstance(value, str) or not value for value in mapping['claim_ids'])
            or not isinstance(mapping['claim_digests'], list)
            or not isinstance(mapping['outputs'], list) or not mapping['outputs']
            or len(mapping['claim_ids']) != len(mapping['claim_digests'])
            or len(set(mapping['claim_ids'])) != len(mapping['claim_ids'])
            or any(not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value)
                   for value in [mapping['domain_digest'], *mapping['claim_digests']])):
        raise ValueError('complete exact governed commercial mapping required')
    state = store.read()
    assignment = state.resolve(mapping['assignment'], 'assignment')
    if assignment['owner']['layer'] != mapping['layer']:
        raise ValueError('commercial assignment ownership mismatch')
    for reference in mapping['outputs']:
        product = state.resolve(reference, 'product')
        if (product['product_kind'] != 'answer' or product['assignment'] != mapping['assignment']
                or product['owner']['layer'] != mapping['layer']
                or not store.evaluate(reference, scope=assignment['use_scope'])['qualified']):
            raise ValueError('commercial output lacks its exact current justification')
    return state


def append_commercial_binding(store, mapping, *, message, dispatch_proof):
    """Submit a signed physical completion carrying exact commercial observation bytes.

    Args:
        store: Trusted host-selected governed Store; never a raw graph writer.
        mapping: Exact domain/claim digests, producer assignment and output refs.
        message: Host run_completed operation carrying the canonical provider return.
        dispatch_proof: Real external proof binding the complete message/effects.
    Returns:
        The governed processing response; only a committed response records delivery.
    Raises:
        ValueError: The mapping or recorded observation differs from exact content.
        OSError: Required material or the authoritative store is unavailable.
    """
    _binding_mapping(store, mapping)
    payload = message.get('payload', {})
    if message.get('message_type') != 'control_event' or payload.get('event') != 'run_completed':
        raise ValueError('commercial binding requires authenticated physical completion')
    package = lifecycle.loads(store._blob(payload['return_blob_id']))
    observations = [intent['payload']['observation'] for intent in package['intents']
                    if intent['message_type'] == 'observation']
    if len(observations) != 1:
        raise ValueError('commercial binding requires exactly one observation return')
    reference = observations[0]
    proposals = [proposal for proposal in package['records']
                 if proposal['logical_id'] == reference['logical_id']
                 and proposal['record_type'] == 'product']
    if len(proposals) != 1:
        raise ValueError('commercial observation must be returned in the exact package')
    record = proposals[0]['record']
    manifest = lifecycle.record_manifest(reference['engagement'], reference['scope'],
                                         reference['logical_id'], 'product', record)
    material = lifecycle.blob(lifecycle.canonical(mapping))
    if (lifecycle.version_id(manifest) != reference['version_id']
            or record['product_kind'] != 'observation' or material not in record['material']
            or lifecycle.loads(store._blob(material)) != mapping):
        raise ValueError('commercial mapping differs from its exact returned bytes')
    return store.submit(lifecycle.canonical(message), dispatch_proof)


def fabric_binding_resolver(ledger_path):
    """Resolve commercial claim bindings against current governed justifications.

    Args:
        ledger_path: Trusted host-selected format-3 ledger, never an agent-selected path.
    Returns:
        Callback(entity, snapshot) checking domain/claim hashes, exact typed binding,
        granular output references, and current shared-evaluator qualifications.
    Raises:
        OSError: Required store material cannot be read.
        ValueError: Empty, unsupported, corrupt, or unauthenticated ledger.
    """
    transactions = lifecycle.read(ledger_path)
    if not transactions:
        raise ValueError('nonempty governed commercial ledger required')
    store = lifecycle.Store(ledger_path, transactions[0]['engagement'])

    def resolve(entity, snapshot):
        try:
            data = entity['data']
            index = {item['version_id']: item for item in snapshot['entities']}
            domain = index[data['domain_contract_version']]
            claims = data['claim_ids']
            if domain['type'] != 'DomainContract' or any(index[claim]['type'] != 'Claim' for claim in claims):
                return False
            state = store.read()
            binding = data['governed_binding']
            record = state.resolve(binding, 'product')
            expected = {'domain_contract_version': domain['version_id'], 'domain_digest': _digest(domain),
                        'claim_ids': claims, 'claim_digests': [_digest(index[claim]) for claim in claims],
                        'assignment': data['governed_assignment'], 'layer': data['layer'], 'outputs': []}
            for fragment_id in data['fragment_ids']:
                fragment = index[fragment_id]
                if fragment['type'] != 'Fragment':
                    return False
                expected['outputs'].append(fragment['data']['governed_output'])
            _binding_mapping(store, expected)
            digest = lifecycle.blob(lifecycle.canonical(expected))
            binding_assignment = state.resolve(record['assignment'], 'assignment')
            claimed_assignment = state.resolve(data['governed_assignment'], 'assignment')
            return (bool(data['fragment_ids']) and record['product_kind'] == 'observation'
                    and binding_assignment['use_scope'] == claimed_assignment['use_scope']
                    and digest in record['material']
                    and lifecycle.loads(store._blob(digest)) == expected
                    and store.evaluate(binding, scope=binding_assignment['use_scope'])['qualified'])
        except (KeyError, TypeError, ValueError, OSError):
            return False
    return resolve
