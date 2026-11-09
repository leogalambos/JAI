#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Project effective professional output contracts without rewriting v3 identities.

Usage: python3 tools/generate_role_output_guidance.py [--check] [--root PATH].
Inputs are exact role IDs, frozen v3 identities and authored semantic-family
assignments. Output is the exhaustive effective-output inventory, section 6
delivery rows and a marker-owned section 14 framework-applicability instruction.
Unconditional ArchiMate scope/review phrasing is qualified without removing its
reference entry. Inputs, gates, authority and worked examples remain unchanged.
Exit zero means generated/current, never professional or human approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from content_catalog_definitions import (ADDITIONAL_FAMILIES, SEMANTIC_FAMILIES,
    SEMANTIC_REFINEMENTS, TYPE_ACCEPTANCE_DETAILS, TYPE_REQUIREMENTS)
from generate_content_catalog import BINDINGS, FAMILIES
from professional_output_refinements import delivery_form_for

ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = '.ai/runtime/content/role-output-guidance.json'
GENERIC = 'Reviewed by a competent second party; complete, dated and attributable'
ROW = re.compile(r'^\|\s*(\d+)\s*\|.*$')
FRAMEWORK_START = '<!-- JAI:FRAMEWORK-APPLICABILITY:START -->'
FRAMEWORK_END = '<!-- JAI:FRAMEWORK-APPLICABILITY:END -->'


def _hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def _fingerprint(delivery):
    return _hash({'deliverable': delivery['name'], 'format': delivery['format'],
                  'acceptance': delivery['acceptance_criterion']})


def build_guidance(root):
    """Return effective source records for every canonical role output.

    Args:
        root: Checkout containing canonical roles and immutable v3 contracts.
    Returns:
        Proposed exhaustive inventory with source and projected fingerprints.
    Raises:
        ValueError: Frozen source reconstruction or exact family coverage fails.
        OSError, KeyError: Required registry data is absent or malformed.
    """
    root = Path(root)
    roles = json.loads((root / '.ai/runtime/roles.json').read_text())['roles']
    contracts = json.loads((root / '.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']
    by_id = {entry['id']: entry for entry in contracts}
    outputs = []
    for role in roles:
        for number, name in enumerate(role['primary_deliverables'], 1):
            cid = role['slug'] + ':' + str(number)
            contract = by_id[cid]
            original = {'name': name, 'format': contract['jai']['realisation']['output_formats'][0],
                        'acceptance_criterion': contract['jai']['intent']['decision_supported']}
            if _fingerprint(original) != contract['source_fingerprint']:
                raise ValueError('Frozen source reconstruction differs: ' + cid)
            family = BINDINGS.get(cid, SEMANTIC_REFINEMENTS.get(cid,
                SEMANTIC_FAMILIES[contract['jai']['semantics']['artifact_type']]))
            obligations = ADDITIONAL_FAMILIES.get(family, FAMILIES.get(family,
                TYPE_REQUIREMENTS.get(family)))
            if obligations is None:
                raise ValueError('Uncovered semantic family: ' + family)
            criteria = TYPE_ACCEPTANCE_DETAILS.get(family, [row[2] for row in obligations])
            criteria = list(criteria)
            if len(criteria) < 3:
                raise ValueError('Insufficient professional acceptance: ' + family)
            form = delivery_form_for(family, cid)
            required = ' '.join(criteria[:3])
            if original['acceptance_criterion'] != GENERIC:
                required += ' Existing source requirement: ' + original['acceptance_criterion'].rstrip('.') + '.'
            effective = {'name': name, 'format': form['representation'],
                         'acceptance_criterion': required}
            outputs.append({'id': cid, 'role_slug': role['slug'], 'domain_index': role['category_index'],
                'role_path': role['path'], 'deliverable_number': number,
                'semantic_family': family, 'legacy_artifact_type': contract['jai']['semantics']['artifact_type'],
                'legacy_source_fingerprint': contract['source_fingerprint'],
                'source_contract_hash': _hash(contract), 'legacy_deliverable': original,
                'effective_deliverable': effective, 'effective_fingerprint': _fingerprint(effective),
                'delivery_form': form, 'acceptance_criteria': criteria,
                'authority': 'Authored content contract; source gates, execution permissions and human acceptance remain unchanged.'})
    if len(outputs) != len(contracts) or {row['id'] for row in outputs} != set(by_id):
        raise ValueError('Incomplete or duplicate effective output inventory')
    document = {'schema_version': '1.0.0', 'status': 'proposed', 'professional_approval': 'pending',
        'role_count': len(roles), 'domain_count': len({role['category_index'] for role in roles}),
        'output_count': len(outputs), 'source': 'artifacts/contracts/role-deliverables.v3.json',
        'purpose': 'Exact forward source projection; immutable storage classification is not the primary work-product modality.',
        'outputs': outputs}
    document['guidance_hash'] = _hash(document)
    return document


def project_framework_guidance(text):
    """Project concise framework selection and conditional ArchiMate instructions.

    Args:
        text: Role Markdown containing one section 14 reference-framework list.
    Returns:
        Idempotent marker-owned applicability guidance with every reference and
        manual example retained. ArchiMate-specific guidance appears only where
        the original reference list names it; role/tool boundaries stay intact.
    Raises:
        ValueError: Section 14 or its marker ownership is missing/ambiguous.
    """
    sections = list(re.finditer(r'^## 14\.[^\n]*\n(?P<body>.*?)(?=^## \d+\.|\Z)', text, re.MULTILINE | re.DOTALL))
    if len(sections) != 1:
        raise ValueError('Expected one section 14 reference framework list')
    section = sections[0]
    body = section.group('body')
    starts, ends = text.count(FRAMEWORK_START), text.count(FRAMEWORK_END)
    if starts or ends:
        if starts != 1 or ends != 1 or body.count(FRAMEWORK_START) != 1 or body.count(FRAMEWORK_END) != 1:
            raise ValueError('Ambiguous framework applicability marker ownership')
        start, end = body.index(FRAMEWORK_START), body.index(FRAMEWORK_END)
        if end < start:
            raise ValueError('Reversed framework applicability marker ownership')
        body = body[:start] + body[end + len(FRAMEWORK_END):]
    instruction = ('Treat the reference list as professional source candidates: resolve the exact source/edition, '
        'applicability, adopted method and evidence against the selected DCS output contract. '
        'Applicable law, binding contracts and adopted organisational policies remain mandatory; '
        'a candidate reference alone does not establish conformance.')
    if re.search(r'\bArchiMate\b', body, re.IGNORECASE):
        instruction += ('\n\nArchiMate 3.2 is opt-in for an explicit operator request or an explicit project profile '
            'with relevant audience/concerns, governed source facts and independent semantic/visual QA; '
            'preserve role boundaries and report the actual qualification scope. '
            'No external EA application is required, and a generic repository graph must not be called verified ArchiMate notation.')
    projected = '\n' + FRAMEWORK_START + '\n' + instruction + '\n' + FRAMEWORK_END + '\n\n' + body.lstrip('\n')
    text = text[:section.start('body')] + projected + text[section.end('body'):]
    lines = []
    current = None
    for line in text.splitlines():
        header = re.match(r'^## (\d+)\.', line)
        if header:
            current = int(header.group(1))
        if current in (1, 4) and 'ArchiMate' in line:
            line = line.replace('- Working within ', '- Working with the applicable selected methods in ')
            line = line.replace('architecture review under ', 'architecture review against the selected applicable methods in ')
        lines.append(line)
    return '\n'.join(lines) + '\n'


def project_role(text, records):
    """Project exact delivery rows and owned framework-applicability guidance.

    Args:
        text: Existing role Markdown; inputs, gates, authority and examples stay intact.
        records: Explicit effective records belonging to this role.
    Returns:
        Deterministic Markdown with professionally specified delivery rows.
    Raises:
        ValueError: A supplied output is missing or a duplicate row is found.
    """
    by_number = {row['deliverable_number']: row for row in records}
    found = set()
    result = []
    section = None
    for line in text.splitlines():
        header = re.match(r'^## (\d+)\.', line)
        if header:
            section = int(header.group(1))
        match = ROW.match(line) if section == 6 else None
        if match and int(match.group(1)) in by_number:
            number = int(match.group(1))
            if number in found:
                raise ValueError('Duplicate section 6 row')
            found.add(number)
            delivery = by_number[number]['effective_deliverable']
            cells = [str(number), delivery['name'], delivery['format'], delivery['acceptance_criterion']]
            line = '| ' + ' | '.join(value.replace('|', ' / ') for value in cells) + ' |'
        result.append(line)
    if found != set(by_number):
        raise ValueError('Effective output row missing from role')
    return project_framework_guidance('\n'.join(result) + '\n')


def generate(root=ROOT, check=False):
    """Write the inventory/role projections or report drift without writes.

    Args:
        root: Canonical repository root.
        check: If true, return one for source drift and leave files unchanged.
    Returns:
        Zero for successfully generated/current output, one for check-mode drift.
    Raises:
        OSError, ValueError: Missing/unsafe sources or invalid projection records.
    """
    root = Path(root)
    document = build_guidance(root)
    updates = {root / GUIDANCE: json.dumps(document, indent=2, ensure_ascii=False) + '\n'}
    grouped = {}
    for record in document['outputs']:
        grouped.setdefault(record['role_path'], []).append(record)
    for relative, records in grouped.items():
        path = root / '.ai' / relative
        if path.is_symlink() or not path.resolve().is_relative_to((root / '.ai/skills').resolve()):
            raise ValueError('Unsafe role projection path')
        updates[path] = project_role(path.read_text(), records)
    differences = [path for path, content in updates.items() if not path.exists() or path.read_text() != content]
    if not check:
        for path in differences:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(updates[path], encoding='utf-8')
    print(('Drift' if check and differences else 'PASS') + ': effective output inventory '
          + str(document['output_count']) + ', role projections ' + str(document['role_count'])
          + ', changed ' + str(len(differences)))
    return int(check and bool(differences))


def main(argv=None):
    """Parse CLI options and return generation status without granting approval.

    Args:
        argv: Optional explicit argument list; None uses process arguments.
    Returns:
        Exit status from generate.
    Raises:
        SystemExit: CLI arguments are invalid.
        OSError, ValueError: Projection sources or destinations are invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    return generate(args.root, args.check)


if __name__ == '__main__':
    raise SystemExit(main())
