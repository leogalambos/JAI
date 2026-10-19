#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Measure content without inventing rendered pages or minimum prose quotas."""
from __future__ import annotations
import argparse
import json
import re
from collections import defaultdict
import content_spec


def analyze(model, spec=None):
    """Return observed modality counts, located repetitions and soft budget advice.

    Args:
        model: JSON semantic or publication model, never mutated.
        spec: Optional compiled DCS containing modality budgets.
    Returns:
        JSON-compatible counts with unknown pages represented by None.
    Raises:
        ValueError: If the model contains nonfinite JSON numbers.
    """
    content_spec.canonical_hash(model)
    strings = []
    objects = defaultdict(list)
    def walk(value, path):
        if isinstance(value, str):
            strings.append((path, value))
        elif isinstance(value, dict):
            if len(value) >= 2 and any(key not in ('id', 'title', 'heading', 'label', 'status', 'knowledge_status', 'evidence_refs', 'evidence_ref', 'owner', 'version', 'hash') for key in value):
                objects[content_spec.canonical_hash(value)].append(path)
            for key, child in value.items():
                if key not in ('evidence', 'context', 'producer', 'reviewer'):
                    walk(child, f'{path}.{key}')
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f'{path}[{index}]')
    if 'semantic_units' in model:
        walk(model['semantic_units'], '$.semantic_units')
        for key in ('summary', 'sections', 'repeated_content', 'irrelevant_annex', 'annexes', 'claims', 'slides', 'rows', 'nodes', 'edges'):
            if key in model:
                walk(model[key], '$.' + key)
    else:
        walk(model, '$')
    groups = defaultdict(list)
    for path, value in strings:
        normalized = ' '.join(re.findall(r'\w+', value.casefold()))
        if len(normalized.split()) >= 8:
            groups[normalized].append(path)
    duplicates = [{'locations': paths, 'text': 'Repeated text content; inspect the canonical source locations.', 'object_hash': content_spec.canonical_hash(text)} for text, paths in sorted(groups.items()) if len(paths) > 1]
    duplicates.extend({'locations': paths, 'text': 'Repeated structured semantic content', 'object_hash': digest} for digest, paths in sorted(objects.items()) if len(paths) > 1)
    counts = {'words': sum(len(re.findall(r'\b[\w’-]+\b', value)) for _, value in strings),
              'pages': None, 'slides': len(model['slides']) if isinstance(model.get('slides'), list) else None,
              'rows': len(model['rows']) if isinstance(model.get('rows'), list) else None,
              'diagram_nodes': len(model['nodes']) if isinstance(model.get('nodes'), list) else None,
              'semantic_units': len(model.get('semantic_units', {}))}
    advice = []
    for metric, budget in (spec or {}).get('blueprint', {}).get('budgets', {}).items():
        observed = counts.get(metric)
        if observed is not None and budget.get('soft_max') is not None and observed > budget['soft_max']:
            advice.append({'metric': metric, 'observed': observed, 'limit': budget['soft_max'], 'action': 'revise/justify', 'blocking': False})
    return {'counts': counts, 'duplication': duplicates, 'budget_advice': advice,
            'page_count_basis': 'unknown until measured by the existing renderer',
            'calibration_status': (spec or {}).get('calibration_status', 'synthetic-only')}


def main(argv=None):
    """Run analyze CLI; return zero on valid input, one on invalid JSON or files.

    Args:
        argv: Optional command arguments.
    Returns:
        Process exit status.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('analyze')
    command.add_argument('model')
    command.add_argument('--spec')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(analyze(content_spec.load_json(args.model), content_spec.load_json(args.spec) if args.spec else None), indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
