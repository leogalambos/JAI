#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Evaluate synthetic DCS examples through the real content validator.

The mutation recipes provide expectations, never detector observations. Results
are development evidence only and cannot grant human-gold or rollout approval.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys

from content_spec import ContentSpec, canonical_hash


def _mutator(root):
    path = root / 'tools/generate_content_corpus.py'
    if path.is_file():
        sys.path.insert(0, str(path.parent))
        spec = importlib.util.spec_from_file_location('content_corpus_recipes', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.apply_variant
    # Installed packages carry the same recipes as the source checkout.
    from content_mutations import apply_variant
    return apply_variant


def prepare_case(reference, resolver):
    """Bind a synthetic reference to its explicit role contract and compiled DCS.

    Args:
        reference: JSON-compatible canonical example or applied mutation.
        resolver: ContentSpec registry resolver for the selected library root.
    Returns:
        Independent model copy and compiled specification tuple.
    Raises:
        KeyError: If the example lacks an explicit contract identifier.
        ValueError: If registry resolution or typed context validation fails.
    """
    model = copy.deepcopy(reference)
    model.pop('variants', None)
    model.pop('reference_expectation', None)
    spec = resolver.resolve(model['contract_id'], context=model['context'])
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    return model, spec


def evaluate_corpus(root, detector=None):
    """Measure actual seeded-defect recall and reference false positives.

    Args:
        root: Source checkout or installed runtime root accepted by ContentSpec.
        detector: Optional callable with the production evaluate(model, spec)
            contract; defaults to content_lint.evaluate.
    Returns:
        Reproducible JSON report containing every case hash and findings.
    Raises:
        OSError, ValueError, KeyError: For unreadable or invalid corpus inputs.
        ImportError: If the production validator is unavailable.
    """
    if detector is None:
        from content_lint import evaluate
        detector = evaluate
    root = Path(root).resolve()
    runtime = root / '.ai/runtime' if (root / '.ai/runtime').is_dir() else root
    resolver = ContentSpec(root)
    mutate = _mutator(root)
    manifest = json.loads((runtime / 'evals/content_quality/manifest.json').read_text())
    cases = []
    counts = dict(expected_critical=0, detected_critical=0,
                  reference_count=0, reference_false_positives=0,
                  critical_case_count=0, detected_critical_case_count=0,
                  expected_rules=0, detected_rules=0)
    for relative in manifest['cases']:
        reference = json.loads((runtime / relative).read_text())
        for variant in [None, *reference['variants']]:
            applied = reference if variant is None else mutate(reference, variant)
            model, spec = prepare_case(applied, resolver)
            report = detector(model, spec)
            findings = report['findings']
            observed = {finding['rule_id'] for finding in findings}
            expected = set(variant['expected_rule_ids']) if variant else set()
            matched = expected & observed
            counts['expected_rules'] += len(expected)
            counts['detected_rules'] += len(matched)
            if variant is None:
                counts['reference_count'] += 1
                if any(f.get('category') in ('critical-content', 'security-policy',
                       'existing-mandatory-gate', 'existing-gate') for f in findings):
                    counts['reference_false_positives'] += 1
            elif variant['expected_category'] in ('critical-content',
                                                 'existing-mandatory-gate'):
                counts['expected_critical'] += len(expected)
                counts['detected_critical'] += len(matched)
                counts['critical_case_count'] += 1
                counts['detected_critical_case_count'] += int(expected <= observed)
            cases.append({'case_id': model['artifact_id'] + '/' +
                          (variant['id'] if variant else 'reference'),
                          'semantic_hash': canonical_hash(model),
                          'compiled_spec_hash': spec['compiled_spec_hash'],
                          'report_hash': canonical_hash(report),
                          'expected_rule_ids': sorted(expected),
                          'observed_rule_ids': sorted(observed),
                          'missing_rule_ids': sorted(expected - observed),
                          'findings': findings,
                          'gate_verdict': report['gate_verdict']})
    recall = (counts['detected_critical'] / counts['expected_critical']
              if counts['expected_critical'] else 0.0)
    case_recall = (counts['detected_critical_case_count'] / counts['critical_case_count']
                   if counts['critical_case_count'] else 0.0)
    false_positive = (counts['reference_false_positives'] / counts['reference_count']
                      if counts['reference_count'] else 1.0)
    result = {'schema_version': '1.0.0', 'calibration_status': 'synthetic-only',
              'human_gold': False, 'production_ready': False,
              'approval_status': 'pending-existing-JAI-L0', 'counts': counts,
              'critical_recall': recall, 'critical_case_recall': case_recall,
              'reference_false_positive_rate': false_positive,
              'false_negatives': counts['expected_critical'] - counts['detected_critical'],
              'all_seeded_rule_recall': (counts['detected_rules'] / counts['expected_rules']
                                         if counts['expected_rules'] else 0.0),
              'all_seeded_rule_misses': counts['expected_rules'] - counts['detected_rules'],
              'thresholds': {'critical_recall_min': .95,
                             'reference_false_positive_rate_max': .10},
              'pilot_pass': recall >= .95 and case_recall >= .95 and false_positive <= .10,
              'limitations': ['Synthetic deterministic seeded-defect evaluation only.',
                             'Unimplemented semantic review predicates remain pending.',
                             'No human domain acceptance or enforcement activation.'],
              'cases': cases}
    if detector.__module__ == 'content_lint':
        first_reference = json.loads((runtime / manifest['cases'][0]).read_text())
        probe_model, probe_spec = prepare_case(first_reference, resolver)
        result['segregation_of_duties_probes'] = evaluate_sod_probes(probe_model, probe_spec, detector)
        result['pilot_pass'] = result['pilot_pass'] and result['segregation_of_duties_probes']['pass']
    result['evaluation_hash'] = canonical_hash(result)
    return result


def evaluate_sod_probes(model, spec, detector=None):
    """Exercise real review verification with synthetic authenticated host records.

    Args:
        model: Prepared canonical synthetic semantic source.
        spec: Matching compiled DCS.
        detector: Production evaluate callable; defaults to content_lint.evaluate.
    Returns:
        Reproducible probe records and escapes; not live identity qualification.
    Raises:
        KeyError, ValueError: For malformed model or validator report.
    """
    if detector is None:
        from content_lint import evaluate
        detector = evaluate
    model = copy.deepcopy(model)
    model['producer'] = {'context_manifest': {'runtime': 'synthetic-host'}}
    producer_hash = canonical_hash(model)
    model['producer']['attestation'] = 'synthetic-producer-token'
    semantic_hash = canonical_hash(model)
    pending = detector(model, spec)['reviewer']['required_units']
    review = {'semantic_hash': semantic_hash,
              'compiled_spec_hash': spec['compiled_spec_hash'],
              'context_hash': spec['context_hash'],
              'context_manifest': {'runtime': 'synthetic-independent-host'},
              'unit_reviews': [{'unit_id': unit, 'verdict': 'PASS',
                               'rationale': 'Synthetic probe exercises hash and identity binding only.',
                               'evidence': 'Synthetic host control record, not professional acceptance.'}
                              for unit in pending], 'findings': []}
    producer_payload = {'principal': 'host-author', 'reviewer': False,
                        'subject_digest': producer_hash, 'snapshot_digest': producer_hash,
                        'context_digest': canonical_hash(model['producer']['context_manifest'])}
    reviewer_payload = {'principal': 'host-independent-reviewer', 'reviewer': True,
                        'subject_digest': canonical_hash(review), 'snapshot_digest': semantic_hash,
                        'context_digest': canonical_hash(review['context_manifest'])}
    review['attestation'] = 'synthetic-review-token'
    records = []
    for name in ('independent-control', 'missing-review', 'untrusted-declaration',
                 'same-principal', 'relabeled-self-review', 'stale-snapshot',
                 'forged-attestation'):
        proposed = copy.deepcopy(review)
        payload = copy.deepcopy(reviewer_payload)
        if name == 'missing-review':
            proposed = None
        elif name in ('same-principal', 'relabeled-self-review'):
            payload['principal'] = producer_payload['principal']
            if name == 'relabeled-self-review':
                proposed['display_name'] = 'A different reviewer name'
                subject = copy.deepcopy(proposed)
                subject.pop('attestation')
                payload['subject_digest'] = canonical_hash(subject)
        elif name == 'stale-snapshot':
            payload['snapshot_digest'] = '0' * 64
        elif name == 'forged-attestation':
            proposed['attestation'] = 'forged-token'
        trusted = {'synthetic-producer-token': producer_payload,
                   'synthetic-review-token': payload}
        host = None if name == 'untrusted-declaration' else lambda token: trusted.get(token)
        report = detector(model, spec, reviewer=proposed, trusted_executions=host)
        accepted = report['reviewer']['status'] == 'verified-independent-review'
        records.append({'probe_id': name, 'semantic_hash': semantic_hash,
                        'report_hash': canonical_hash(report), 'findings': report['findings'],
                        'review_accepted': accepted,
                        'expected_review_accepted': name == 'independent-control'})
    escapes = sum(record['review_accepted'] for record in records
                  if not record['expected_review_accepted'])
    control = records[0]['review_accepted']
    return {'scope': 'Synthetic trusted-host API probes; not live provider identity evidence.',
            'probe_count': len(records), 'adversarial_count': len(records) - 1,
            'sod_escapes': escapes, 'positive_control_accepted': control,
            'pass': escapes == 0 and control, 'cases': records}


def main(argv=None):
    """Run the synthetic pilot CLI and return zero only when thresholds pass.

    Args:
        argv: Optional argument list; defaults to process command arguments.
    Returns:
        Exit status 0 for passing pilot thresholds, 1 for failure.
    Raises:
        SystemExit: For invalid command-line syntax.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['run'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate_corpus(args.root)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({key: value for key, value in result.items() if key not in ('cases', 'segregation_of_duties_probes')}, indent=2))
        return 0 if result['pilot_pass'] else 1
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Content pilot failed: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
