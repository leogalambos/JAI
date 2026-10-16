#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Project compact commercial discovery metadata from the canonical role registry."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def project(registry, specialist_intents=()):
    """Return relative catalog paths and deterministic JSON text for a role registry.

    Args:
        registry: Canonical roles.json object with unique role slugs and valid tiers.
        specialist_intents: Explicit bounded specialist phrase routing rules.
    Returns:
        Mapping of relative catalog/shard paths to UTF-8 JSON text.
    Raises:
        ValueError: Registry counts, identifiers, skill domains or tiers are invalid.
    """
    roles = registry['roles']
    if registry.get('count') != len(roles) or len({r['slug'] for r in roles}) != len(roles):
        raise ValueError('role count or unique identifiers invalid')
    grouped = {}
    exact = {}
    for role in roles:
        domain = role['skill'].removeprefix('it-roles-')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', domain) or role['tool_tier'] not in ('advise', 'author', 'execute', 'inspect'):
            raise ValueError('invalid role domain or tier')
        row = {'role_id': role['slug'], 'name': role['name'], 'tier': role['tool_tier'],
               'operator': role['operator_agent'], 'skill': role['skill'], 'path': role['path'],
               'deliverables': role['primary_deliverables'], 'aliases': role.get('aliases', []),
               'guard': 'engagement-authorisation-guard' if domain == 'offensive-security-and-adversarial-testing' else None}
        grouped.setdefault(domain, {'purpose': role['category'], 'roles': []})['roles'].append(row)
        for name in (row['name'], row['role_id'], *row['aliases']):
            key = ' '.join(re.findall(r'\w+', name.casefold()))
            if domain not in exact.setdefault(key, []):
                exact[key].append(domain)
    outputs = {}
    domains = []
    for domain, group in grouped.items():
        path = f'domains/{domain}.json'
        payload = json.dumps({'version': '1', 'domain_id': domain, 'complete': True, 'roles': group['roles']}, indent=2, ensure_ascii=False) + '\n'
        outputs[path] = payload
        hints = sorted({word for role in group['roles'] for word in re.findall(r'\w+', ' '.join([role['name'], *role['aliases']]).casefold()) if len(word) > 2})
        domains.append({'domain_id': domain, 'purpose': group['purpose'], 'hints': hints,
                        'shard': path, 'version': '1', 'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                        'role_count': len(group['roles'])})
    if any(rule['role_id'] not in {r['slug'] for r in roles} for rule in specialist_intents):
        raise ValueError('specialist intent references unknown role')
    outputs['catalog.json'] = json.dumps({'version': '1', 'source_roles_version': registry['version'],
                                         'complete': True, 'domains': domains, 'exact_role_domains': exact, 'specialist_intents': list(specialist_intents)}, indent=2, ensure_ascii=False) + '\n'
    return outputs


def run(runtime, check=False):
    """Write or compare catalog projections beneath an explicit runtime directory.

    Args:
        runtime: Runtime directory containing canonical roles.json.
        check: Compare only when true; never modify files in this mode.
    Returns:
        Zero for matching/generated projections; one for drift in check mode.
    Raises:
        ValueError: Invalid canonical role metadata.
        OSError: Registry or projection files cannot be read or written.
    """
    runtime = Path(runtime)
    rules_path = runtime / 'commercial/specialist-routing.json'
    rules = json.loads(rules_path.read_text(encoding='utf-8'))['intents'] if rules_path.exists() else []
    outputs = project(json.loads((runtime / 'roles.json').read_text(encoding='utf-8')), rules)
    drift = []
    for relative, content in outputs.items():
        target = runtime / 'commercial' / relative
        if check:
            if not target.is_file() or target.read_text(encoding='utf-8') != content:
                drift.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
    if drift:
        print('Commercial catalog drift: ' + ', '.join(drift))
    return int(bool(drift))


def main():
    """Parse runtime/check options and exit with projection status.

    Returns:
        None; exits with zero on success or one for detected projection drift.
    Raises:
        ValueError: Invalid registry metadata.
        OSError: Input/output is unavailable.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raise SystemExit(run(args.runtime, args.check))


if __name__ == '__main__':
    main()
