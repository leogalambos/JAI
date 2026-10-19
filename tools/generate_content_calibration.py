#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Generate proposed synthetic size candidates and actual QA trend examples.

Usage: python3 tools/generate_content_calibration.py [--check]. Reads the
canonical priority corpus and current registry, replays the real validator,
and writes content/calibration/synthetic-development.json. Exit zero means
reproducible development evidence, never human approval or a production gate.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_eval import prepare_case
from content_lint import evaluate
from content_metrics import calibrate, trends
from content_mutations import apply_variant
from content_spec import ContentSpec, canonical_hash, load_json

TARGET = ROOT / '.ai/runtime/content/calibration/synthetic-development.json'


def build(root=ROOT):
    """Return candidates and trends derived from three scenarios per key family.

    Args:
        root: Source checkout with registered policies and canonical corpus.
    Returns:
        Synthetic-only, proposed development evidence with pinned inputs and
        ten nonblocking envelopes. No policy is changed or activated.
    Raises:
        OSError, ValueError, KeyError: For missing inputs, failed QA replay or
            noncomparable calibration/trend samples.
    """
    root = Path(root)
    runtime = root / '.ai/runtime'
    engine = ContentSpec(root)
    manifest = load_json(runtime / 'evals/content_quality/manifest.json')
    grouped = {}
    trend_examples = {}
    for relative in manifest['cases']:
        reference = load_json(runtime / relative)
        model, spec = prepare_case(reference, engine)
        report = evaluate(model, spec)
        complexity = relative.rsplit('-', 1)[1].removesuffix('.json')
        family = reference['document_kind']
        grouped.setdefault(family, []).append({
            'project_id': family + '-' + complexity, 'complexity': complexity,
            'synthetic': True, 'semantic_model': model, 'content_qa': report})
        if complexity == 'medium':
            recipe = next(item for item in reference['variants'] if item['id'] == 'missing-core')
            incomplete, incomplete_spec = prepare_case(apply_variant(reference, recipe), engine)
            before = evaluate(incomplete, incomplete_spec)
            snapshots = [
                {'observed_at': '2026-10-19T09:00:00Z',
                 'semantic_model': incomplete, 'content_qa': before},
                {'observed_at': '2026-10-19T10:00:00Z',
                 'semantic_model': model, 'content_qa': report},
            ]
            trend_examples[family] = trends(snapshots, root=root)
    result = {'schema_version': '1.0.0', 'status': 'proposed',
              'calibration_status': 'synthetic-only', 'human_gold': False,
              'production_ready': False, 'automatically_applied_to_policy': False,
              'scope': 'Descriptive word-count envelopes and QA deltas from synthetic development scenarios; not enterprise calibration.',
              'corpus_manifest_hash': canonical_hash(manifest),
              'candidates': {family: calibrate(samples, root=root)
                             for family, samples in sorted(grouped.items())},
              'trend_examples': dict(sorted(trend_examples.items()))}
    result['development_evidence_hash'] = canonical_hash(result)
    return result


def main(argv=None):
    """Write generated evidence or check exact reproducibility.

    Args:
        argv: Optional CLI arguments.
    Returns:
        Zero for a successful write/check, one for stale checked-in evidence.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    text = json.dumps(build(), indent=2) + '\n'
    if args.check:
        if not TARGET.is_file() or TARGET.read_text() != text:
            print('Synthetic calibration/trend evidence drift.')
            return 1
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(text)
    print('Synthetic calibration/trend evidence is reproducible; no production activation.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
