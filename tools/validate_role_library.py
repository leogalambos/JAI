#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Check effective role identities, professional contracts and projections."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

from compose_role_library import compose


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
from role_context_contract import INSTRUCTION_BYTES, SECTION_BYTES, alias_key


def _impact(composition, changed):
    roles = composition.manifest['roles']
    if not changed:
        return None
    consumers = defaultdict(set)
    for slug, record in roles.items():
        effective = {slug, *composition.manifest['descendants_by_role'][slug]}
        consumers[f'{record["source_root"]}/{record["source_path"]}'].update(effective)
        consumers['.ai/' + record['projection_path']].update(effective)
        anchor = roles[record['legacy_anchor']]
        consumers['.ai/' + anchor['projection_path']].add(slug)
        for module in record['modules']:
            source = PurePosixPath('.ai/role-library') / module['source_path']
            consumers[source.as_posix()].add(slug)
            for section in module['sections']:
                name = section.get('source_reference')
                if name is not None:
                    consumers[(source.parent / name).as_posix()].add(slug)
    if not set(changed) <= consumers.keys():
        return None
    return set().union(*(consumers[path] for path in changed))


def _check(root, library, changed):
    composition = compose(root, library)
    runtime = root / '.ai/runtime'
    legacy = json.loads((runtime / 'roles.json').read_bytes())
    manifest = composition.manifest['roles']
    rows = {row['slug']: row for row in composition.registry['roles']}
    contracts_path = 'artifacts/contracts/role-deliverables.v3.json'
    contracts = json.loads((runtime / contracts_path).read_bytes())['contracts']
    by_id = {row['id']: row for row in contracts}
    findings = []
    impacted = None if library is not None else _impact(composition, changed)

    def report(rule, source, identity, message, ancestry=(), *, severity='error'):
        findings.append({
            'rule': rule, 'severity': severity, 'source': source,
            'identity': identity, 'message': message, 'ancestry': list(ancestry),
        })

    if len(by_id) != len(contracts):
        report('ROLE001', contracts_path, 'catalogue', 'Duplicate professional output contract ID')
    by_alias = defaultdict(set)
    for slug, row in sorted(rows.items()):
        record = manifest[slug]
        source = f'{record["source_root"]}/{record["source_path"]}'
        ancestry = record['ancestry']
        anchor = record['legacy_anchor']
        for alias in row['aliases']:
            key = alias_key(alias)
            if not key:
                report('ROLE007', source, slug, 'Alias has no visible lookup text', ancestry)
            elif key in rows and key != slug:
                report('ROLE007', source, slug, f'Alias shadows the exact role slug {key}', ancestry)
            else:
                by_alias[key].add(slug)
        if impacted is not None and slug not in impacted:
            continue
        if not isinstance(row.get('mission'), str) or not row['mission'].strip():
            report('ROLE002', source, slug, 'Role requires a professional mission', ancestry)
        if row.get('tool_tier') not in {'advise', 'author', 'execute', 'inspect'}:
            report('ROLE003', source, slug, 'Unknown professional tool tier', ancestry)
        for position, _ in enumerate(row['primary_deliverables'], 1):
            identifier = f'{anchor}:{position}'
            contract = by_id.get(identifier)
            if (not contract or contract.get('role_slug') != anchor
                    or contract.get('deliverable_number') != position or not contract.get('version')):
                report('ROLE004', source, slug, f'Missing or invalid professional output {identifier}', ancestry)
        instruction = composition.instructions[slug]
        if len(instruction) > INSTRUCTION_BYTES:
            report('ROLE008', source, slug,
                   f'Effective instructions have {len(instruction)} bytes; limit is {INSTRUCTION_BYTES}. Defer detail.',
                   ancestry)
        for section in record.get('context_sections', ()):
            size = section['end'] - section['start']
            if size > SECTION_BYTES:
                report('KNOW002', source, section['id'],
                       f'Initial knowledge section has {size} bytes; limit is {SECTION_BYTES}. Defer detail.', ancestry)
        projection = '.ai/' + record['projection_path']
        if (composition.files.get(projection) != instruction
                or hashlib.sha256(instruction).hexdigest() != record['instruction_sha256']):
            report('ROLE005', source, slug, 'Effective instruction projection differs from its manifest', ancestry)

    for alias, candidates in sorted(by_alias.items()):
        if len(candidates) > 1:
            report('ROLE009', '.ai/runtime/roles.json', alias,
                   f'Search alias requires disambiguation: {", ".join(sorted(candidates))}', severity='advisory')

    tier_capabilities = {
        'advise': set(), 'author': {'materialize'},
        'inspect': {'measure'}, 'execute': {'materialize', 'measure'},
    }
    for workflow in json.loads((runtime / 'workflows.json').read_bytes())['workflows']:
        for step in workflow['steps']:
            if impacted is not None and step['slug'] not in impacted:
                continue
            row = rows.get(step['slug'])
            tier = step.get('tool_tier')
            skill = step.get('skill')
            agent = step.get('operator_agent')
            if skill == 'agent':
                valid = agent == step['slug'] and (root / '.ai/agents' / f'{agent}.md').is_file()
            elif skill in {'external', 'dynamic'}:
                valid = (skill, agent, tier) in {
                    ('external', 'human', 'advise'), ('dynamic', 'role-author', 'author'),
                }
            else:
                valid = (row is not None and skill == row.get('skill') and tier in tier_capabilities
                         and row.get('tool_tier') in tier_capabilities
                         and tier_capabilities[tier] <= tier_capabilities[row['tool_tier']])
            if not valid:
                report('ROLE006', '.ai/runtime/workflows.json', workflow['key'],
                       f'Invalid role binding at step {step["step"]}: {step["slug"]}')

    sections = composition.manifest['knowledge_sections']
    unclassified = sorted(identity for identity, section in sections.items() if not section['classified'])
    for identity in unclassified:
        report('KNOW001', sections[identity]['source'], identity, 'No current section classification')

    return {
        'schema_version': 1,
        'scope': {'mode': 'full' if impacted is None else 'changed',
                  'roles': sorted(rows if impacted is None else impacted), 'changed': sorted(set(changed))},
        'inventory': {
            'distributed_roles': sorted(row['slug'] for row in legacy['roles']),
            'effective_roles': sorted(rows),
            'knowledge_modules': sorted(composition.manifest['roles_by_module']),
            'knowledge_sections': sorted(sections),
            'unclassified_sections': unclassified,
        },
        'findings': findings,
    }


def main(argv=None):
    """Validate a checkout from CLI arguments and report diagnostics.

    Args:
        argv: Optional argument sequence. Defaults to the process arguments.
    Returns:
        Zero on success, one for a policy violation, or two for an incomplete
        check due to missing, unreadable or structurally invalid inputs.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--library', type=Path, help='Validate an alternate composition source tree')
    parser.add_argument('--changed', action='append', default=[], metavar='PATH',
                        help='Check a changed repository path and its dependent roles; repeat as needed')
    parser.add_argument('--format', choices=('text', 'json'), default='text')
    args = parser.parse_args(argv)
    try:
        result = _check(args.root, args.library, args.changed)
        status = int(any(item['severity'] == 'error' for item in result['findings']))
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        result = {'schema_version': 1, 'inventory': None, 'findings': [
            {'rule': 'INPUT001', 'severity': 'error', 'source': str(args.root), 'message': str(error)}
        ]}
        status = 2
    except ValueError as error:
        result = {'schema_version': 1, 'inventory': None, 'findings': [
            {'rule': 'COMPOSE001', 'severity': 'error', 'source': '.ai/role-library', 'message': str(error)}
        ]}
        status = 1
    if args.format == 'json':
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for finding in result['findings']:
            print(f'{finding["severity"]} {finding["rule"]} {finding["source"]}: {finding["message"]}')
        if not status:
            inventory = result['inventory']
            print(f'PASS: {len(inventory["distributed_roles"])} distributed roles, '
                  f'{len(inventory["effective_roles"])} effective roles, '
                  f'{len(inventory["knowledge_modules"])} knowledge modules')
            print(f'PASS: all {len(inventory["knowledge_sections"])} knowledge sections are classified')
            scope = result['scope']
            print(f'Checked role scope ({scope["mode"]}): {len(scope["roles"])} entries')
    return status


if __name__ == '__main__':
    raise SystemExit(main())
