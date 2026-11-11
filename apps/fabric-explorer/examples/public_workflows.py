#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Capture public workflow definitions as source observations through the canonical Fabric CLI.

This records documentation, not workflow execution, review, approval or a risk decision.
Run with an absolute new/empty output directory; original public files remain unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS = ('idea-to-production', 'vulnerability-to-remediation')


def collect_workflows(root=ROOT):
    """Read exact public workflow stage tables with bounded, complete row provenance.

    Args:
        root: Repository containing the maintained public workflow library.
    Returns:
        Workflow title, relative source path/hash and ordered role/activity/handover/gate rows.
    Raises:
        ValueError: A table is missing, malformed or not contiguous from step one.
        OSError: A maintained public source cannot be read.
    """
    result = []
    for slug in WORKFLOWS:
        relative = f'docs/workflow-library/{slug}.md'
        raw = (root / relative).read_bytes(); text = raw.decode('utf-8')
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')), None)
        rows = []
        for number, line in enumerate(text.splitlines(), 1):
            if not re.match(r'^\| \d+ \|', line): continue
            fields = [field.strip() for field in line.strip('|').split('|')]
            if len(fields) != 5 or any(not value for value in fields): raise ValueError('Complete five-column stage row required')
            step, role, activity, handover, gate = fields
            rows.append({'step': int(step), 'role': role, 'activity': activity, 'handover': handover, 'gate': gate, 'line': number})
        if not title or not rows or [row['step'] for row in rows] != list(range(1, len(rows) + 1)):
            raise ValueError('Contiguous public workflow stage table required')
        result.append({'title': title, 'path': relative, 'sha256': hashlib.sha256(raw).hexdigest(), 'stages': rows})
    return result


def generate(destination, root=ROOT):
    """Create a source-only canonical showcase with public-documentation provenance.

    Args:
        destination: Explicit absolute new or empty owned output directory.
        root: Repository whose public sources and maintained canonical CLI are used.
    Returns:
        Public provenance/count manifest written outside the canonical journal directory.
    Raises:
        ValueError: Output is relative, linked or nonempty, or a public stage table is invalid.
        OSError: Output, material storage or subprocess setup fails.
        subprocess.CalledProcessError: The canonical writer rejects the request; no fallback mutation occurs.
    """
    destination = Path(destination)
    if not destination.is_absolute() or destination.is_symlink() or destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError('Explicit absolute new or empty showcase directory required')
    workflows = collect_workflows(root)
    destination.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(root / '.ai/runtime/tools'))
    import lifecycle
    import governed_delivery as delivery
    engagement = 'public-workflow-reference'
    ledger = destination / '.fabric' / f'{engagement}.jsonl'
    store = lifecycle.Store(ledger, engagement)
    owner = {'kind': 'authority', 'id': 'JAI public documentation maintainers'}
    controller = {'kind': 'controller', 'id': 'Public documentation capture'}
    sources = []
    roles = {}
    for workflow in workflows:
        for row in workflow['stages']:
            roles.setdefault(row['role'], []).append({'workflow': workflow['title'], 'stage': row['step'], 'source': workflow['path'], 'source_sha256': workflow['sha256'], 'line': row['line']})
    role_refs = {}
    role_observations = []
    for role, occurrences in sorted(roles.items()):
        label = f'Role · {role}'
        material = {'observation': 'Accountable role quoted from public workflow definitions; not an assignment or performed work', 'role': role, 'occurrences': occurrences}
        record = {'owner': owner, 'source_role': 'input', 'origin': owner, 'material': [store.put_blob((json.dumps(material, ensure_ascii=False, indent=2) + '\n').encode())], 'criteria': [], 'inherited': []}
        manifest = lifecycle.record_manifest(engagement, 'documentation', label, 'source', record)
        role_refs[role] = {'engagement': engagement, 'scope': 'documentation', 'logical_id': label, 'version_id': lifecycle.version_id(manifest)}
        sources.append({'logical_id': label, 'record': record})
        role_observations.append({'role': role, 'occurrences': occurrences, 'ref': role_refs[role]})
    for workflow in workflows:
        previous = None
        for row in [None, *workflow['stages']]:
            cluster = 'Delivery' if workflow['title'] == 'Idea to production' else 'Remediation'
            label = workflow['title'] if row is None else f"{cluster} {row['step']:02d} · {row['role']}"
            material = {'observation': 'Public workflow definition, not evidence of performed work or approval', 'source': workflow['path'], 'source_sha256': workflow['sha256'], 'workflow': workflow['title'], **({'stage': row} if row else {'stage_count': len(workflow['stages'])})}
            # A stage description depends on the quoted role definition as well
            # as the published predecessor. Shared roles connect real workflows.
            inherited = ([previous] if previous else []) + ([role_refs[row['role']]] if row else [])
            record = {'owner': owner, 'source_role': 'input', 'origin': owner, 'material': [store.put_blob((json.dumps(material, ensure_ascii=False, indent=2) + '\n').encode())], 'criteria': [], 'inherited': inherited}
            manifest = lifecycle.record_manifest(engagement, 'documentation', label, 'source', record)
            previous = {'engagement': engagement, 'scope': 'documentation', 'logical_id': label, 'version_id': lifecycle.version_id(manifest)}
            sources.append({'logical_id': label, 'record': record})
    now = int(time.time() * 1000)
    profile = {'owner': controller, 'profile_id': 'Public source capture only', 'protocol': 'jai.governed-delivery/1', 'source_profiles': [], 'obligations': [], 'max_clock_skew_ms': 5000, 'max_request_duration_ms': 60000, 'local_budget': {'iteration_ms': 60000, 'max_reworks': 0}, 'authority_policy_id': 'No execution or approval recorded', 'routing_policy_id': 'No worker routing', 'content_profile': None, 'scheduling': {'collection_window_ms': 1000, 'control_limits': [], 'max_search_steps': 1, 'max_escalation_rounds': 1, 'initial_deadline_ms': now + 60000}}
    message = {'protocol': delivery.PROTOCOL, 'message_type': 'bootstrap', 'message_id': '0' * 64, 'request_id': 'public-documentation-capture', 'correlation_id': 'public-workflow-reference', 'engagement': engagement, 'scope': 'documentation', 'sender': controller, 'recipient': controller, 'profile': None, 'context': None, 'expected_head': lifecycle.ZERO, 'issued_at_ms': now, 'expires_at_ms': now + 60000, 'causes': [], 'attachments': [], 'payload': {'controller_id': controller['id'], 'use_scopes': ['documentation'], 'profile': {'logical_id': 'Public documentation capture profile', 'record': profile}, 'l0_inputs': sources}}
    message['message_id'] = delivery.message_id(message)
    request = destination / 'capture-request.json'; request.write_text(json.dumps(message, ensure_ascii=False), encoding='utf-8')
    completed = subprocess.run([sys.executable, '-I', '-B', str(root / '.ai/runtime/fabric/fabric.py'), 'submit', engagement, '--message', str(request)], env={**os.environ, 'FABRIC_HOME': str(ledger.parent)}, check=True, capture_output=True, text=True)
    receipt = json.loads(completed.stdout)
    (destination / 'capture-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    provenance = {'format': 'jai.public-workflow-showcase/1', 'journal': '.fabric/' + ledger.name, 'source_records': len(sources), 'workflows': workflows, 'roles': role_observations, 'scope': 'Source-only documentation observations; no executed workflow, assessment, approval, authority grant or finding is recorded. Stage inheritance represents published stage ordering and quoted role dependencies, not observed causal execution. A role shared by two workflows is one reference source, not a live role assignment.'}
    (destination / 'showcase.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    return provenance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('destination', type=Path)
    print(json.dumps(generate(parser.parse_args().destination), ensure_ascii=False))
