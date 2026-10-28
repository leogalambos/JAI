#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Check explicit workflow handoffs using replayed QA and host-bound receivers.

The CLI validates a draft handoff without granting acceptance. The embedding host
supplies its existing TrustedDispatcher and trusted principal-role assignments;
JSON role declarations, renderer success and advisory findings grant no authority.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import content_spec
import content_lint


# Numbers are editorial selections of canonical role deliverables, not title matching.
SELECTIONS = {
'access-request-to-review': ['1','2','2,3','1,2','1','3'],
'ai-system-approval': ['1','2','1,2','1,4','1,2,3','1,2','2,4','3'],
'architecture-model-to-repository-governance': ['1,4','1,3','3','4','1,4','1,2,3'],
'business-case-to-benefits': ['1,2','1','1,2,3','1','2,3','1,2','4'],
'codebase-takeover': ['1','1,3','1,2','2','1','1,2','4','1,4'],
'cyber-incident-breach-to-recovery': ['1,2,3','2','1,2','1,2,3','2','4','1,2','2','1,4','2,3','1','4','4'],
'data-product-delivery': ['1,2','2','1,3','1,3','1,3','1','1,2','3,4'],
'demand-to-portfolio-to-funding': ['1','2','1','1,2','1','2','1','1,4','1,2','2'],
'design-to-operational-readiness': ['1,4','1,4','1,2,4','1','1,3','1','1'],
'enterprise-release-orchestration': ['1','3,4','3','2,3','4','2,4','3','1,2','3','3,4','1,3','1'],
'idea-to-production': ['2','1,3','1','1,4','2,4','4','1,2,4','2,4','2,4','1','3,4','1','1,2'],
'incident-to-problem': ['1','1,2,4','3','1,2,3','1,2','1,4','1','1,2','2'],
'migration-and-cutover': ['1,3','1,2,4','1,3','2,3','3','2,4','1','1,4'],
'new-service-onboarding': ['1','1,3','1,4','1,3,4','2,3','1,2,3','1','2,3','1','2','3','1'],
'organisational-change-and-adoption': ['1,3','1,2','2,4','4','4','4'],
'production-change': ['1,4','1,3','2,4','2','1,2','3,4','1,3','1,3'],
'regulatory-change-to-assurance': ['1','2','1,3','1','1,3','1','1,2','2','3','2'],
'resilience-validation': ['1,4','2','2,3','1,3','1','1,2','3','4','2','1'],
'semantic-to-enterprise-publication': ['source','source','source','source','source'],
'service-retirement-and-decommission': ['1','1,2','1,2','3','1','1,3','3,4','4'],
'siam-multi-supplier': ['1','1,4','3','1','1','1','3','1'],
'source-to-contract-to-service': ['1','1,2','1','1,3','2,4','2,3','1','1,3','3,4','1,2'],
'supplier-onboarding': ['1,2,3','1','4','1','1,2','1,4','2,3'],
'vulnerability-to-remediation': ['1,2','2','3','1,4','1','1','4','4']}
ALIASES = {'Demand & Intake Manager':'demand-and-intake-manager',
'IT Financial Management / TBM Manager':'it-financial-management-tbm-manager',
'Architecture Repository Engineer':'agent:architecture-repository-engineer',
'Model Consistency Reviewer':'agent:model-consistency-reviewer',
'Owning specialist':'engagement:owning-specialist',
'Evidence & Rationale Reviewer':'agent:evidence-rationale-reviewer',
'Enterprise Publication Editor':'agent:enterprise-publication-editor',
'Visual Quality Reviewer':'agent:visual-quality-reviewer'}



def load_bindings(root=None):
    """Return the hash-checked registered workflow acceptance catalogue.

    Args:
        root: Repository or installed runtime root accepted by ContentSpec.
    Returns:
        Catalogue with unique handoff identities and exact role contracts.
    Raises:
        ValueError: For hash, count, identity or contract-reference corruption.
        OSError: For unavailable local registry data.
    """
    root_path=Path(root).resolve() if root is not None else Path(__file__).resolve().parents[1]
    runtime=root_path/'.ai/runtime' if (root_path/'.ai/runtime').is_dir() else root_path
    catalog=content_spec.load_json(runtime/'content/workflow-acceptance.json')
    registry=content_spec.load_json(runtime/'content/registry.json')
    binding_rows=registry.get('bindings',[])
    if isinstance(binding_rows,str):
        binding_rows=content_spec.load_json(runtime/'content'/binding_rows)['bindings']
    if not binding_rows:
        binding_rows=content_spec.load_json(runtime/'content/migrations/26.10.5-binding-map.json')['bindings']
    known={r['artifact_id']:r for r in binding_rows}
    body=copy.deepcopy(catalog)
    digest=body.pop('catalog_hash',None)
    rows=catalog['bindings']
    if digest!=content_spec.canonical_hash(body) or len({r['handoff_id'] for r in rows})!=len(rows):
        raise ValueError('WORKFLOW_CATALOG_INTEGRITY')
    workflows={w['key']:w for w in content_spec.load_json(runtime/'workflows.json')['workflows']}
    if len(rows)!=catalog['handoff_count'] or len(workflows)!=catalog['workflow_count']:
        raise ValueError('WORKFLOW_CATALOG_COUNT')
    if {r['handoff_id'] for r in rows}!={f"{key}:{step['step']}" for key,w in workflows.items() for step in w['steps']}:
        raise ValueError('WORKFLOW_CATALOG_COVERAGE')
    def role(step):
        prefix='agent:' if step['skill']=='agent' else ('engagement:' if step['skill'] in ('dynamic','external') else '')
        return prefix+step['slug']
    for row in rows:
        if row['handoff_id']!=f"{row['workflow_id']}:{row['step']}":
            raise ValueError('WORKFLOW_HANDOFF_ID_MISMATCH')
        source=workflows[row['workflow_id']]
        index=row['step']-1
        step=source['steps'][index]
        receiver=role(source['steps'][index+1]) if index+1<len(source['steps']) else 'engagement:named-authority'
        if (row['source_hash']!=content_spec.canonical_hash(source) or row['acceptance_criterion']!=step['gate']
                or row['handover']!=step['hands_over'] or row['producer_role']!=role(step) or row['receiving_role']!=receiver):
            raise ValueError('WORKFLOW_SOURCE_PROVENANCE_MISMATCH')
        choice=SELECTIONS[row['workflow_id']][index]
        contract_role={'agent:architecture-repository-engineer':'architecture-repository-and-modelling-lead',
                       'agent:model-consistency-reviewer':'architecture-repository-and-modelling-lead'}.get(role(step),role(step))
        expected_ids=[] if choice=='source' else [f'{contract_role}:{number}' for number in choice.split(',')]
        expected_selection='explicit-source-contract' if choice=='source' else 'registered-contracts'
        if row['contract_ids']!=expected_ids or row['contract_selection']!=expected_selection:
            raise ValueError('WORKFLOW_CONTRACT_SCOPE_MISMATCH')
        if any(cid not in known for cid in row['contract_ids']):
            raise ValueError('WORKFLOW_UNKNOWN_CONTRACT')
        expected_types=sorted({known[cid]['artifact_type'] for cid in expected_ids})
        expected_checks=['exact-contract-binding','content-qa-replay','existing-gates-preserved','independent-receiver-attestation','specific-gate-evidence']
        if (row['artifact_types']!=expected_types or row['receiver_checks']!=expected_checks
                or row['source_ref']!='.ai/runtime/workflows.json'):
            raise ValueError('WORKFLOW_OBLIGATION_METADATA_MISMATCH')
    return catalog


def _human_accepted(authority, bound):
    fabric=getattr(authority,'fabric',None)
    fragment_id=getattr(authority,'fragment_id',None)
    if fabric is None or not fragment_id:
        return False
    try:
        problems,warnings=fabric.verify()
        if problems or warnings:
            return False
        fragment=fabric.nodes[fragment_id]
        justified,reasons=fabric.justify(fragment_id,strict=True)
        accepted=fabric.lifecycle.evaluate(fragment['version_id'],release=True)
        acceptance_version=fabric.lifecycle.proofs.get(('default',fragment['version_id'],'accept'))
        review=next((node for node in fabric.nodes.values() if node['version_id']==acceptance_version),{})
        policy=json.loads(fragment.get('text',''),object_pairs_hook=content_spec._pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError('NONFINITE')))
        return (fragment.get('type')=='frag' and fragment.get('layer')==1 and justified and not reasons and accepted['eligible']
                and review.get('layer')==0 and review.get('state')=='accepts' and bool(review.get('reviewer'))
                and policy.get('profile')=='workflow-acceptance' and policy.get('acceptance')==bound)
    except (ValueError,TypeError,KeyError,OSError):
        return False


def check(handoff_id, model, report, root=None, acceptance=None, trusted_executions=None,
          receiving_assignments=None, authority=None, resolver=None):
    """Return a hash-bound receiving acceptance result without granting release.

    Args:
        handoff_id: Exact registered workflow:step ID, never inferred from title.
        model: Canonical semantic source with explicit contract_id.
        report: Immutable content QA report for that exact source.
        root: Repository or installed runtime root.
        acceptance: Receiver subject with handoff_id, semantic_hash, report_hash,
            catalog_hash, criterion, verdict, evidence and dispatcher attestation.
        trusted_executions: Existing host TrustedDispatcher verifier.
        receiving_assignments: Host-owned principal-to-role-list mapping; never
            read from model, report or acceptance. Callers keep this host-trusted.
        authority: Existing signed JAI L0 activation adapter for QA replay.
        resolver: Optional host-opened ContentSpec for a batch against one pinned
            registry snapshot; never constructed from model-controlled policy.
    Returns:
        ACCEPTANCE_VERIFIED only after exact QA replay, independent assigned
        receiver and specific gate evidence. This is not a release authority act.
    Raises:
        ValueError: For unknown handoff or invalid registry/semantic JSON.
    """
    catalog=load_bindings(root)
    row=next((r for r in catalog['bindings'] if r['handoff_id']==handoff_id),None)
    if row is None:
        raise ValueError('UNKNOWN_WORKFLOW_HANDOFF')
    engine=resolver if resolver is not None else content_spec.ContentSpec(root)
    spec=engine.resolve(model['contract_id'],model.get('context',{}))
    failures=[]
    if row['contract_selection']=='registered-contracts' and model['contract_id'] not in row['contract_ids']:
        failures.append('HANDOFF_CONTRACT_MISMATCH')
    if content_lint.verify_report(report,model,spec,trusted_executions,authority):
        failures.append('CONTENT_QA_INVALID')
    if report.get('gate_verdict')!='CONTENT_PASS' or report.get('deterministic_status')!='PASS':
        failures.append('CONTENT_GATE_PENDING_OR_FAILED')
    subject=copy.deepcopy(acceptance) if isinstance(acceptance,dict) else {}
    token=subject.pop('attestation',None)
    payload=content_lint._host_verify(trusted_executions,token)
    producer=content_lint._host_verify(trusted_executions,model.get('producer',{}).get('attestation'))
    bound={'handoff_id':handoff_id,'semantic_hash':content_spec.canonical_hash(model),
           'report_hash':report.get('report_hash'),'catalog_hash':catalog['catalog_hash'],
           'criterion':row['acceptance_criterion'],'receiving_role':row['receiving_role']}
    human_step=(row['producer_role']=='engagement:named-authority' or row['receiving_role'] in ('engagement:named-authority','engagement:named-acceptance-authority'))
    if human_step:
        if not _human_accepted(authority,bound):
            failures.append('EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED')
        principal=None
    else:
        if any(subject.get(k)!=v for k,v in bound.items()):
            failures.append('RECEIVER_SUBJECT_MISMATCH')
        if (not payload or not producer or payload.get('reviewer') is not True
                or payload.get('principal')==producer.get('principal')
                or payload.get('subject_digest')!=content_spec.canonical_hash(subject)
                or payload.get('snapshot_digest')!=bound['semantic_hash']
                or payload.get('context_digest')!=content_spec.canonical_hash(subject.get('context_manifest'))):
            failures.append('RECEIVER_IDENTITY_UNVERIFIED')
        principal=payload.get('principal') if payload else None
        roles=(receiving_assignments or {}).get(principal,[])
        if row['receiving_role'] not in roles:
            failures.append('RECEIVER_ROLE_UNASSIGNED')
        evidence=subject.get('evidence')
        if subject.get('verdict')!='PASS' or not isinstance(evidence,str) or not evidence.strip():
            failures.append('RECEIVING_GATE_EVIDENCE_REQUIRED')
    result={'schema_version':'1.0.0',**bound,'contract_id':model['contract_id'],
            'status':'ACCEPTANCE_VERIFIED' if not failures else 'ACCEPTANCE_PENDING',
            'findings':failures,'receiver_principal':principal,
            'production_release_authorized':False,'calibration_status':spec.get('calibration_status','synthetic-only')}
    result['result_hash']=content_spec.canonical_hash(result)
    return result


def main(argv=None):
    """List bindings or check a draft; the CLI cannot authenticate receiver JSON.

    Args:
        argv: Optional CLI arguments.
    Returns:
        Zero for valid listing, two for pending acceptance, one for invalid inputs.
    """
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('list')
    command=sub.add_parser('check')
    command.add_argument('handoff_id');command.add_argument('model');command.add_argument('report')
    args=parser.parse_args(argv)
    try:
        result=load_bindings(args.root) if args.command=='list' else check(args.handoff_id,content_spec.load_json(args.model),content_spec.load_json(args.report),root=args.root)
        print(json.dumps(result,indent=2))
        return 0 if args.command=='list' else 2
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'error':str(exc)}));return 1

if __name__=='__main__':
    raise SystemExit(main())
