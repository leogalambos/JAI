#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Measure content without inventing rendered pages or minimum prose quotas."""
from __future__ import annotations
import argparse
import json
import datetime as dt
import math
import statistics
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
              'semantic_units': len(model.get('semantic_units', {})),
              'elements': len(model['elements']) if isinstance(model.get('elements'), list) else (len(model['nodes']) if isinstance(model.get('nodes'), list) else None),
              'configuration_checks': len(model['checks']) if isinstance(model.get('checks'), list) else None}
    advice = []
    for metric, budget in (spec or {}).get('blueprint', {}).get('budgets', {}).items():
        observed = counts.get(metric)
        if observed is not None and budget.get('soft_max') is not None and observed > budget['soft_max']:
            advice.append({'metric': metric, 'observed': observed, 'limit': budget['soft_max'], 'action': 'revise/justify', 'blocking': False})
        for key in ('hard_max', 'max_limit'):
            limit=budget.get(key)
            if limit is None:
                continue
            basis=budget.get('hard_limit_basis')
            valid_basis=(isinstance(basis,dict) and basis.get('kind') in ('contractual','regulatory','publication-constraint')
                         and isinstance(basis.get('source_ref'),str) and bool(basis['source_ref'].strip())
                         and isinstance(basis.get('reason'),str) and bool(basis['reason'].strip()))
            if not valid_basis:
                rule,action='SIZE_CONSTRAINT_BASIS_REQUIRED','provide the registered genuine upper-constraint source and rationale'
            elif observed is None:
                rule,action='SIZE_CONSTRAINT_UNMEASURED','measure the actual modality before accepting the declared constraint'
            elif observed>limit:
                rule,action='HARD_SIZE_CONSTRAINT','revise to meet the registered genuine upper constraint'
            else:
                continue
            advice.append({'metric':metric,'observed':observed,'limit':limit,'action':action,
                           'rule_id':rule,'category':'critical-content','blocking':False,
                           'basis':basis,'limit_kind':key})
    return {'counts': counts, 'duplication': duplicates, 'budget_advice': advice,
            'page_count_basis': 'unknown until measured by the existing renderer',
            'calibration_status': (spec or {}).get('calibration_status', 'synthetic-only')}


def trends(snapshots, root=None, trusted_executions=None, authority=None):
    """Compare replayed QA snapshots only within one exact specification/context.

    Args:
        snapshots: Ordered objects containing observed_at (aware ISO timestamp),
            semantic_model and content_qa; at least two distinct source snapshots.
        root: Trusted registry root; supplied compiled specs are never trusted.
        trusted_executions: Optional existing host dispatcher for review replay.
        authority: Optional existing JAI L0 adapter for enforcement replay.
    Returns:
        Hash-bound observations and numeric deltas; never qualification approval.
    Raises:
        ValueError: For tamper, duplicate snapshots, noncomparable policy/context,
            unordered/naive timepoints or insufficient observations.
    """
    import content_lint
    if not isinstance(snapshots,list) or len(snapshots)<2:
        raise ValueError('TREND_REQUIRES_TWO_SNAPSHOTS')
    engine=content_spec.ContentSpec(root)
    observations=[];identity=None;seen=set();previous=None
    for item in snapshots:
        model=item['semantic_model'];report=item['content_qa']
        instant=dt.datetime.fromisoformat(item['observed_at'].replace('Z','+00:00'))
        if instant.tzinfo is None or (previous is not None and instant<=previous):
            raise ValueError('TREND_TIMEPOINT_INVALID')
        previous=instant
        spec=engine.resolve(model['contract_id'],model.get('context',{}))
        if content_lint.verify_report(report,model,spec,trusted_executions,authority):
            raise ValueError('TREND_QA_REPLAY_FAILED')
        current=(model['contract_id'],model['document_kind'],spec['compiled_spec_hash'],spec['context_hash'])
        if identity is not None and current!=identity:
            raise ValueError('TREND_NONCOMPARABLE_SPEC_OR_CONTEXT')
        identity=current
        snapshot=(model['artifact_id'],content_spec.canonical_hash(model))
        if snapshot in seen:
            raise ValueError('TREND_DUPLICATE_SNAPSHOT')
        seen.add(snapshot)
        metrics=analyze(model,spec)
        observations.append({'observed_at':instant.isoformat(),'artifact_id':snapshot[0],
            'semantic_hash':snapshot[1],'report_hash':report['report_hash'],
            'gate_verdict':report['gate_verdict'],'words':metrics['counts']['words'],
            'duplicate_groups':len(metrics['duplication']),'findings':len(report['findings']),
            'critical_findings':sum(f['category']=='critical-content' for f in report['findings'])})
    result={'contract_id':identity[0],'document_kind':identity[1],'compiled_spec_hash':identity[2],
            'context_hash':identity[3],'observations':observations,
            'delta':{key:observations[-1][key]-observations[0][key] for key in ('words','duplicate_groups','findings','critical_findings')},
            'qualification_evidence':False,'production_ready':False,
            'comparison_basis':'Exact QA replay; timestamps are caller observations, not trusted execution time.'}
    result['trend_hash']=content_spec.canonical_hash(result)
    return result


def calibrate(samples, metric='words', root=None):
    """Derive an informational candidate envelope from actual semantic observations.

    Args:
        samples: Objects with project_id, complexity (simple/medium/complex),
            synthetic boolean, semantic_model, and its exact content_qa report.
            At least three distinct projects spanning all complexities are needed.
        metric: Actual observed metric; pages cannot be inferred from prose.
        root: Trusted registry root used to replay reports and bind the policy.
    Returns:
        Proposed, nonblocking size candidate with source/report hashes and actual
        observed range. No input flag grants human-gold or production activation.
    Raises:
        ValueError: For insufficient/diverse samples, tamper, mixed kinds/context,
            unmeasured metrics, nonfinite/nonpositive values or content failures.
            Context strata stay separate in provenance; cross-stratum range is
            descriptive only and cannot activate a policy or a hard limit.
    """
    import content_lint
    if not isinstance(samples,list) or len(samples)<3:
        raise ValueError('CALIBRATION_REQUIRES_THREE_PROJECTS')
    projects={};complexities=set();values=[];basis=[];identity=None;strata={}
    engine=content_spec.ContentSpec(root)
    for sample in samples:
        project=sample.get('project_id');complexity=sample.get('complexity')
        if not isinstance(project,str) or not project.strip() or complexity not in ('simple','medium','complex'):
            raise ValueError('CALIBRATION_PROJECT_METADATA_INVALID')
        if project in projects:
            raise ValueError('CALIBRATION_DISTINCT_PROJECTS_REQUIRED')
        if not isinstance(sample.get('synthetic'),bool):
            raise ValueError('CALIBRATION_SOURCE_CLASS_REQUIRED')
        projects[project]=complexity;complexities.add(complexity)
        model=sample['semantic_model'];report=sample['content_qa']
        spec=engine.resolve(model['contract_id'],model.get('context',{}))
        current=(model['contract_id'],model['document_kind'],content_spec.canonical_hash(spec['inheritance']))
        if identity is not None and current!=identity:
            raise ValueError('CALIBRATION_NONCOMPARABLE_POLICY')
        strata.setdefault(spec['context_hash'],{'context':spec['context'],'compiled_spec_hash':spec['compiled_spec_hash'],'projects':[]})['projects'].append(project)
        identity=current
        if content_lint.verify_report(report,model,spec) or report.get('deterministic_status')!='PASS':
            raise ValueError('CALIBRATION_QA_REPLAY_OR_CONTENT_FAILED')
        count=analyze(model,spec)['counts'].get(metric)
        if not isinstance(count,(int,float)) or isinstance(count,bool) or not math.isfinite(count) or count<=0:
            raise ValueError('CALIBRATION_METRIC_UNMEASURED')
        values.append(count)
        basis.append({'project_id':project,'complexity':complexity,'synthetic':sample['synthetic'],
            'semantic_hash':content_spec.canonical_hash(model),'report_hash':report['report_hash'],'observed':count,
            'context_hash':spec['context_hash'],'compiled_spec_hash':spec['compiled_spec_hash']})
    if complexities!={'simple','medium','complex'}:
        raise ValueError('CALIBRATION_COMPLEXITY_COVERAGE_REQUIRED')
    result={'document_kind':identity[1],'contract_id':identity[0],'policy_inheritance_hash':identity[2],
            'context_strata':strata,'status':'proposed','calibration_status':'synthetic-only' if any(s['synthetic'] for s in samples) else 'unapproved-enterprise',
            'size_budget':{'metric':metric,'target':[min(values),max(values)],'soft_max':max(values),
                'minimum_is_quality_gate':False,'target_is_informational':True,
                'applicability':'Descriptive envelope across explicitly listed context/complexity strata; no per-stratum quality threshold.'},
            'observed_median':statistics.median(values),'samples':basis,
            'production_ready':False,'human_approval_required':True,
            'activation_authority':'Existing JAI L0 only; this candidate is not an approval.'}
    result['calibration_hash']=content_spec.canonical_hash(result)
    return result


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
    command = sub.add_parser('trends')
    command.add_argument('snapshots')
    command.add_argument('--root')
    command = sub.add_parser('calibrate')
    command.add_argument('samples')
    command.add_argument('--metric', default='words')
    command.add_argument('--root')
    args = parser.parse_args(argv)
    try:
        if args.command == 'trends':
            result = trends(content_spec.load_json(args.snapshots), root=args.root)
        elif args.command == 'calibrate':
            result = calibrate(content_spec.load_json(args.samples), metric=args.metric, root=args.root)
        else:
            result = analyze(content_spec.load_json(args.model), content_spec.load_json(args.spec) if args.spec else None)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
