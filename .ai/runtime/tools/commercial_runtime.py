#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Host-owned commercial dispatch attestations and read-only Fabric binding.

Trust starts at the embedding host: configure its key, command allowlist and
mount policy outside model-controlled workspace. Never accept these from agent
JSON. The local bwrap runner executes deterministic commands, not a live LLM
provider; Codex/Claude live isolation remains unqualified until separately tested.
"""
from __future__ import annotations

import copy
import hashlib
import hmac
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import uuid


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


class TrustedDispatcher:
    """Host-only HMAC verifier/runner; key custody is the embedding host's duty.

    Args:
        key: At least 32 random bytes held outside agent context and mounts.
        allowed_commands: Exact tuples of executable/arguments the host approved.
        executable_roots: Approved read-only system runtime paths. Logical mount
            destinations are preserved, including /lib and /lib64 on usr-merged
            hosts; their resolved sources must also be approved system paths.
            Missing approved paths are omitted; duplicates are mounted once.
    Raises:
        ValueError: Weak key or unsafe runtime roots/commands.
    """

    def __init__(self, key, allowed_commands, executable_roots=('/usr', '/lib', '/lib64')):
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError('host key requires at least 32 random bytes')
        self._key = key
        self._commands = {tuple(command) for command in allowed_commands}
        approved_roots = {'/usr', '/usr/lib', '/usr/lib64', '/lib', '/lib64'}
        mounts = set()
        for requested in executable_roots:
            target = Path(requested)
            if str(target) not in approved_roots:
                raise ValueError('runtime roots must contain executables only, never workspace/history')
            if not target.exists():
                continue
            source = target.resolve()
            if str(source) not in approved_roots:
                raise ValueError('resolved runtime roots must remain approved system paths')
            mounts.add((source, target))
        self._roots = tuple(sorted(mounts, key=lambda mount: str(mount[1])))
        for command in self._commands:
            if not command or not Path(command[0]).is_absolute() or Path(command[0]).name in {'sh', 'bash', 'dash', 'zsh', 'fish'}:
                raise ValueError('exact absolute non-shell commands required')

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

    def run(self, command, subject, snapshot_digest, context_manifest, inputs=(), writable_output=None, reviewer=True, timeout=30):
        """Run an approved command in an empty-history, networkless mount namespace.

        Args:
            command: Exact host-approved argv, never shell text.
            subject: Exact entity excluding its attestation; hashed before dispatch.
            snapshot_digest: Exact immutable snapshot digest.
            context_manifest: Exact context metadata, including provider instructions.
            inputs: Explicit readable individual files; directories are rejected.
            writable_output: Optional empty dedicated evidence directory, not product.
            reviewer: If true every input is mounted read-only, as for authors too.
            timeout: Positive bounded execution timeout seconds.
        Returns:
            Status, captured output and signed execution attestation on success.
            Principal identifies the actual child execution, not a human identity;
            its host-issued execution ID disambiguates operating-system PID reuse.
            A successful namespace launch proves local boundaries only, never live
            provider qualification or organisational independence.
            Unsupported/not_run never produce a usable attestation.
        Raises:
            ValueError: Command/mount/context policy violations before execution.
        """
        command = tuple(command)
        if command not in self._commands:
            raise ValueError('command outside host allowlist')
        if not isinstance(context_manifest, dict) or context_manifest.get('history_policy') != 'fresh' or not context_manifest.get('injected_instructions'):
            raise ValueError('exact fresh context and injected instruction inventory required')
        if not isinstance(snapshot_digest, str) or len(snapshot_digest) != 64:
            raise ValueError('snapshot digest required')
        if timeout <= 0 or timeout > 300:
            raise ValueError('timeout outside bounded dispatch policy')
        bwrap = shutil.which('bwrap')
        if not bwrap:
            return {'status': 'unsupported', 'reason': 'bwrap unavailable', 'attestation': None}
        args = [bwrap, '--unshare-all', '--die-with-parent', '--new-session', '--clearenv', '--setenv', 'PATH', '/usr/bin', '--setenv', 'HOME', '/home/worker', '--tmpfs', '/tmp', '--dir', '/home', '--dir', '/home/worker', '--proc', '/proc', '--dev', '/dev', '--dir', '/inputs', '--chdir', '/home/worker']
        for source, target in self._roots:
            args += ['--ro-bind', str(source), str(target)]
        mounted = []
        for number, source in enumerate(inputs):
            path = Path(source).resolve(strict=True)
            if not path.is_file() or path.is_symlink():
                raise ValueError('input allowlist accepts regular individual files only')
            target = f'/inputs/{number}'
            args += ['--ro-bind', str(path), target]
            mounted.append({'target': target, 'digest': hashlib.sha256(path.read_bytes()).hexdigest()})
        if writable_output is not None:
            output = Path(writable_output).resolve(strict=True)
            if not output.is_dir() or any(output.iterdir()):
                raise ValueError('evidence sink must be an empty dedicated directory')
            if any(output == Path(source).resolve().parent for source in inputs):
                raise ValueError('evidence sink must not contain product inputs')
            args += ['--bind', str(output), '/evidence']
        args += ['--', *command]
        execution_id = str(uuid.uuid4())
        process = None
        try:
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env={})
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            process.communicate()
            return {'status': 'not_run', 'reason': str(exc), 'attestation': None}
        except OSError as exc:
            return {'status': 'not_run', 'reason': str(exc), 'attestation': None}
        if process.returncode:
            return {'status': 'not_run', 'exit_code': process.returncode, 'stdout': stdout, 'stderr': stderr, 'attestation': None}
        worker = {'uid': os.getuid(), 'pid': process.pid, 'execution_id': execution_id,
                  'readonly_inputs': True, 'fresh_namespace': True}
        payload = {'principal': f"uid:{worker['uid']}:worker:{worker['pid']}:execution:{execution_id}",
                   'dispatch_id': execution_id, 'worker_execution': worker,
                   'subject_digest': _digest(subject), 'snapshot_digest': snapshot_digest,
                   'context_digest': _digest(context_manifest), 'input_manifest': mounted,
                   'command': list(command), 'reviewer': reviewer, 'enforcement': 'bwrap-tested',
                   'exit_code': 0, 'stdout_digest': hashlib.sha256(stdout.encode()).hexdigest()}
        signature = hmac.new(self._key, _digest(payload).encode(), 'sha256').hexdigest()
        return {'status': 'tested', 'stdout': stdout, 'stderr': stderr,
                'attestation': {'payload': payload, 'signature': signature}}



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
        return bool(payload and control in {'identity', 'tool_permissions', 'mount_isolation', 'context_isolation'})
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
        New evidence node containing the immutable mapping; never edits old nodes.
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
    return fabric.add_node('evd', mapping['layer'], 'commercial per-claim immutable binding',
                           confidence='interpretation', commercial_binding=copy.deepcopy(mapping))


def fabric_binding_resolver(ledger_path):
    """Build a verifier resolving each commercial binding against exact Fabric nodes.

    Args:
        ledger_path: Trusted host-selected immutable JSONL log, never agent path.
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
