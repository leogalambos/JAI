#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Legacy host-attestation verification and Fabric bindings, without execution.

TrustedDispatcher is retained as a compatibility name for the existing verifier.
It cannot launch tools or prove human L0 identity. Keys belong to an independently
trusted review integration; caller-created signatures do not establish independence.
"""
from __future__ import annotations
import copy, hashlib, hmac, importlib.util, json
from pathlib import Path

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


def append_commercial_binding(fabric, mapping):
    """Append a non-authority binding through Fabric's supported mutation API.

    Args:
        fabric: Trusted host-opened Fabric instance; its CLI/API owns ledger writes.
        mapping: Exact domain/claim digests, contract or L1 requirement ID/digest,
            and fragment IDs/digests to bind. Independent review is still required.
    Returns:
        New evidence node containing the content-hashed mapping; never edits old nodes.
    Raises:
        ValueError: Missing fields or a node hash/layer/type mismatch.
    """
    required = {'domain_contract_version', 'domain_digest', 'claim_ids', 'claim_digests',
                'target_id', 'target_digest', 'layer', 'fragments'}
    if not isinstance(mapping, dict) or set(mapping) != required or not mapping['claim_ids'] or len(mapping['claim_ids']) != len(mapping['claim_digests']):
        raise ValueError('complete typed binding mapping required')
    top = mapping['layer'] == 1
    target = fabric.nodes.get(mapping['target_id'], {})
    if target.get('type') != ('req' if top else 'ctr') or target.get('layer') != (1 if top else mapping['layer'] - 1) or _digest(target) != mapping['target_digest']:
        raise ValueError('target type/layer/digest mismatch')
    if not mapping['fragments']:
        raise ValueError('binding needs granular fragments')
    for fragment in mapping['fragments']:
        node = fabric.nodes.get(fragment['id'], {})
        if node.get('type') != 'frag' or node.get('layer') != mapping['layer'] or _digest(node) != fragment['digest'] or (target['id'], 'requests', node['id']) not in fabric.edges:
            raise ValueError('fragment must answer the exact target with matching hash')
    return fabric.add_node('evd', mapping['layer'], 'commercial per-claim content-hashed binding',
                           confidence='interpretation', commercial_binding=copy.deepcopy(mapping))


def fabric_binding_resolver(ledger_path):
    """Build a verifier resolving each commercial binding against exact Fabric nodes.

    Args:
        ledger_path: Trusted host-selected hash-checked local JSONL log, never agent path.
    Returns:
        Callback(entity, snapshot) validating actual ledger and append-only binding
        created by append_commercial_binding. Historical nodes are never modified.
    Raises:
        OSError: Log or Fabric implementation cannot be read.
    """
    module_path = Path(__file__).resolve().parents[1] / 'fabric/fabric.py'
    spec = importlib.util.spec_from_file_location('commercial_fabric_reader', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entries = [json.loads(line) for line in Path(ledger_path).read_text().splitlines() if line.strip()]
    fabric = module.Fabric('commercial-binding-readonly', entries)

    def resolve(entity, snapshot):
        try:
            problems, warnings = fabric.verify()
            if problems or warnings:
                return False
            data = entity['data']
            index = {item['version_id']: item for item in snapshot['entities']}
            domain = index[data['domain_contract_version']]
            claims = data['claim_ids']
            top = data['layer'] == 1
            contract = fabric.nodes[data['fabric_requirement_id'] if top else data['fabric_contract_id']]
            expected_digest = data['fabric_requirement_digest'] if top else data['fabric_contract_digest']
            if contract['type'] != ('req' if top else 'ctr') or contract['layer'] != (1 if top else data['layer'] - 1) or _digest(contract) != expected_digest:
                return False
            if domain['type'] != 'DomainContract' or any(index[claim]['type'] != 'Claim' for claim in claims):
                return False
            binding_node = fabric.nodes[data['fabric_binding_id']]
            if binding_node['type'] != 'evd' or _digest(binding_node) != data['fabric_binding_digest']:
                return False
            expected = {'domain_contract_version': domain['version_id'], 'domain_digest': _digest(domain),
                        'claim_ids': claims, 'claim_digests': [_digest(index[claim]) for claim in claims],
                        'target_id': contract['id'], 'target_digest': expected_digest, 'layer': data['layer'], 'fragments': []}
            for fragment_id in data['fragment_ids']:
                fragment = index[fragment_id]
                fd = fragment['data']
                node = fabric.nodes[fd['fabric_fragment_id']]
                if fragment['type'] != 'Fragment' or node['type'] != 'frag' or node['layer'] != data['layer'] or _digest(node) != fd['fabric_fragment_digest']:
                    return False
                if (contract['id'], 'requests', node['id']) not in fabric.edges:
                    return False
                expected['fragments'].append({'id': node['id'], 'digest': fd['fabric_fragment_digest']})
                if top:
                    if not fabric._evidence_path(node['id'], {}):
                        return False
                elif not fabric.justify(node['id'], strict=True)[0]:
                    return False
            return bool(data['fragment_ids']) and binding_node.get('commercial_binding') == expected
        except (KeyError, TypeError, ValueError, OSError, module.FabricError):
            return False
    return resolve
