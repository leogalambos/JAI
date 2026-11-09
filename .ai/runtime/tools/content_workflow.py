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
import lifecycle


# Numbers are editorial selections of canonical role deliverables, not title matching.
SELECTIONS = {
'access-request-to-review': ['1','2','2,3','1,2','1','3'],
'ai-system-approval': ['1','2','1,2','1,4','1,2,3','source','1,2','2,4','3'],
'architecture-model-to-repository-governance': ['1,4','1,3','3','4','1,4','1,2,3'],
'business-case-to-benefits': ['1,2','1','1,2,3','1','2,3','1,2','4'],
'codebase-takeover': ['1','1,3','1,2','2','1','1,2','4','1,4'],
'cyber-incident-breach-to-recovery': ['1,2,3','2','1,2','1,2,3','2','4','1,2','2','1,4','2,3','1','4','4'],
'data-product-delivery': ['1,2','2','1,3','1,3','1,3','1','1,2','3,4'],
'demand-to-portfolio-to-funding': ['1','2','1','1,2','1','2','1','1,4','1,2','2'],
'design-to-operational-readiness': ['1,4','1,4','1,2,4','1','1,3','1','1'],
'enterprise-release-orchestration': ['1','3,4','3','2,3','4','2,4','3','1,2','3','3,4','1,3','1'],
'idea-to-production': ['2','1,3','1','1,4','2,4','4','1,2,4','2,4','2,4','1','3,4','1','1,2'],
'incident-to-problem': ['1','1,2,4','3','1,2,3','1,2','1,4','1,2,4','1','1,4','1,2','1,2','2'],
'migration-and-cutover': ['1,3','1,2,4','1,3','2,3','3','2,4','1','1,3','2,4','2,3','1,4'],
'new-service-onboarding': ['1','1,3','1,4','1,3,4','2,3','1,2,3','1','2,3','1','2','3','1'],
'organisational-change-and-adoption': ['1,3','1,2','2,4','4','4','4'],
'production-change': ['1,4','1,3','2,4','2','1,2','3,4','1,3','1,3'],
'regulatory-change-to-assurance': ['1','2','1,3','1','1,3','1','1,2','2','3','2'],
'resilience-validation': ['1,4','2','2,3','1,3','1','1,2','3','4','2','1'],
'semantic-to-enterprise-publication': ['source','source','source','source','source'],
'service-retirement-and-decommission': ['1','1,2','1,2','1','3','3','1,3','3,4','4'],
'siam-multi-supplier': ['1','1,4','3','1','1','1','3','1'],
'source-to-contract-to-service': ['1','1,2','1','1,3','2,4','2,3','1','1,3','3,4','1,2'],
'supplier-onboarding': ['1,2,3','1','4','1','1,2','1,4','2,3'],
'vulnerability-to-remediation': [
    '1,2', '2', '3', '1,4',
    '1',  # Change Manager: change authorisation precedes deployment.
    '1',  # Software Engineer: deploy the authorised remediation.
    '4', '4']}
ALIASES = {'Demand & Intake Manager':'demand-and-intake-manager',
'IT Financial Management / TBM Manager':'it-financial-management-tbm-manager',
'Architecture Repository Engineer':'agent:architecture-repository-engineer',
'Model Consistency Reviewer':'agent:model-consistency-reviewer',
'Owning specialist':'engagement:owning-specialist',
'Evidence & Rationale Reviewer':'agent:evidence-rationale-reviewer',
'Enterprise Publication Editor':'agent:enterprise-publication-editor',
'Visual Quality Reviewer':'agent:visual-quality-reviewer'}

# These source-owned deltas supplement role contracts at the named boundary.
# They reuse semantic_units and the existing authenticated receiving review;
# a policy or published picture is not the individual decision/repository itself.
HANDOFF_CONTENT_CONTRACTS = {
    'access-request-to-review:2': {
        'id': 'handoff/access-request-to-review:2', 'version': '1.0.0',
        'basis': 'JAI-authored individual access-decision practice; professional qualification pending.',
        'units': [{
            'id': 'handoff/access-request-to-review:2.individual_access_decision',
            'semantic_field': 'individual_access_decision',
            'required_fields': ['subject', 'entitlement', 'purpose', 'decision', 'authority', 'validity', 'policy_ref'],
            'acceptance_criterion': 'Record the specific access subject, requested entitlement, justified purpose, actual grant/refusal decision, accountable authority, validity/review condition and applicable versioned policy; policy text alone is insufficient.'}]},
    'architecture-model-to-repository-governance:3': {
        'id': 'handoff/architecture-model-to-repository-governance:3', 'version': '1.0.0',
        'basis': 'JAI-authored repository/interchange handoff practice; professional qualification pending.',
        'units': [{
            'id': 'handoff/architecture-model-to-repository-governance:3.repository_revision',
            'semantic_field': 'repository_revision',
            'required_fields': ['repository_id', 'revision', 'source_revision', 'identity_preservation', 'validation_evidence'],
            'acceptance_criterion': 'Identify the exact canonical repository revision, imported source revision, stable-identity/lifecycle preservation and structural validation evidence; a view set alone is insufficient.'}, {
            'id': 'handoff/architecture-model-to-repository-governance:3.interchange_manifest',
            'semantic_field': 'interchange_manifest',
            'required_fields': ['repository_revision', 'files', 'format_profile', 'loss_disposition'],
            'acceptance_criterion': 'Identify actual interchange files and their source repository revision, exact language/exchange profile and observed loss disposition; do not claim target-tool qualification from a generated file.'}]},
}



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
    if catalog.get('profiles') != {key: workflow.get('operating_profile') for key, workflow in workflows.items()}:
        raise ValueError('WORKFLOW_PROFILE_SCOPE_MISMATCH')
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
        if (not step.get('handoff_content_contract')
                or row.get('handoff_content_contract') != step['handoff_content_contract']
                or row['handoff_content_contract'].get('workflow_profile_hash') != content_spec.canonical_hash(source['operating_profile'])):
            raise ValueError('WORKFLOW_HANDOFF_CONTENT_SCOPE_MISMATCH')
        if (row.get('variant_bindings') != step.get('variant_bindings')
                or not isinstance(row.get('variant_bindings'), dict)
                or any(cid not in known for selected in row['variant_bindings'].values()
                       for cid in selected['contract_ids'])):
            raise ValueError('WORKFLOW_VARIANT_BINDING_SCOPE_MISMATCH')
    return catalog


def _human_accepted(authority, bound):
    store = getattr(authority, 'store', None)
    subject = getattr(authority, 'subject', None)
    use_scope = getattr(authority, 'use_scope', None)
    if not isinstance(store, lifecycle.Store) or not isinstance(subject, dict) or not isinstance(use_scope, str) or not use_scope:
        return False
    try:
        product = store.read().resolve(subject, 'product')
        accepted = store.evaluate(subject, scope=use_scope)
        if not accepted['qualified'] or not accepted['accepted'] or len(product['material']) != 1:
            return False
        policy = json.loads(store._blob(product['material'][0]),
                            object_pairs_hook=content_spec._pairs,
                            parse_constant=lambda value: (_ for _ in ()).throw(ValueError('NONFINITE')))
        return (policy.get('profile') == 'workflow-acceptance'
                and policy.get('acceptance') == bound and bool(accepted['acceptances']))
    except (ValueError, TypeError, KeyError, OSError):
        return False


def check(handoff_id, model, report, root=None, acceptance=None, trusted_executions=None,
          receiving_assignments=None, authority=None, resolver=None, governed=None):
    """Check existing workflow acceptance with optional exact Gen2 provenance.

    Args:
        handoff_id: Exact registered workflow step.
        model: Complete canonical semantic source.
        report: Existing immutable QA report.
        root: Optional shared runtime root.
        acceptance: Actual receiving body; no PASS is supplied by this adapter.
        trusted_executions: Host verifier for ordinary workflow checks.
        receiving_assignments: Host-owned role assignments for ordinary checks.
        authority: Existing L0 acceptance adapter.
        resolver: Optional already-pinned ContentSpec resolver for this exact
            runtime root. Its workflow catalogue is pinned on first use; a new
            source/profile version requires a new host-opened resolver/batch.
        governed: Host-pinned Gen2 adapter; actual captured identity does not
            replace the host's existing functional receiving designation.
    Returns:
        Existing receiving status; never production acceptance or release.
    Raises:
        ValueError: Registry, exact source or current justification is invalid.
    """
    import contextlib
    with governed.action() if governed is not None else contextlib.nullcontext():
        if governed is not None:
            if not governed.publication_status(model,model.get('audience'))['eligible']:
                raise ValueError('Current Gen2 workflow source justification is unavailable')
            trusted_executions=governed
        return _check(handoff_id,model,report,root,acceptance,trusted_executions,
                      receiving_assignments,authority,resolver)


def _check(handoff_id, model, report, root=None, acceptance=None, trusted_executions=None,
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
            registry/workflow snapshot; never constructed from model-controlled
            policy. New input versions use a new resolver, without rewriting
            accepted historical work or silently refreshing this pinned batch.
    Returns:
        ACCEPTANCE_VERIFIED only after exact QA replay, independent assigned
        receiver and specific gate evidence. This is not a release authority act.
    Raises:
        ValueError: For unknown handoff or invalid registry/semantic JSON.
    """
    engine=resolver if resolver is not None else content_spec.ContentSpec(root)
    requested_root=Path(root).resolve() if root is not None else Path(__file__).resolve().parents[1]
    runtime=requested_root/'.ai/runtime' if (requested_root/'.ai/runtime').is_dir() else requested_root
    if resolver is not None and (not isinstance(resolver, content_spec.ContentSpec)
                                 or resolver.base.parent.resolve() != runtime):
        raise ValueError('WORKFLOW_RESOLVER_ROOT_MISMATCH')
    if not hasattr(engine, '_workflow_catalog'):
        engine._workflow_catalog=load_bindings(root)
    catalog=engine._workflow_catalog
    row=next((r for r in catalog['bindings'] if r['handoff_id']==handoff_id),None)
    if row is None:
        raise ValueError('UNKNOWN_WORKFLOW_HANDOFF')
    spec=engine.resolve(model['contract_id'],model.get('context',{}))
    failures=[]
    if content_lint.verify_report(report,model,spec,trusted_executions,authority):
        failures.append('CONTENT_QA_INVALID')
    if report.get('gate_verdict')!='CONTENT_PASS' or report.get('deterministic_status')!='PASS':
        failures.append('CONTENT_GATE_PENDING_OR_FAILED')
    subject=copy.deepcopy(acceptance) if isinstance(acceptance,dict) else {}
    evidence = {item.get('id'): item for item in model.get('evidence', []) if isinstance(item, dict)}
    context = model.get('semantic_units', {}).get('workflow_context', {})
    context = context if isinstance(context, dict) else {}
    context_ref = context.get('context_ref')
    context_record = evidence.get(context_ref) if isinstance(context_ref, str) else None
    context_payload = context_record.get('payload') if isinstance(context_record, dict) else None
    profile = catalog['profiles'][row['workflow_id']]
    selected_path = None
    if isinstance(context_payload, dict):
        for path in profile['paths']:
            if path['variant'] != context_payload.get('variant'):
                continue
            if path['id'] == path['variant'] or path['mechanism'] == context_payload.get('mechanism_variant'):
                selected_path = path
                break
    selected = row.get('variant_bindings', {}).get(selected_path['id']) if selected_path else None
    if selected_path is None:
        failures.append('WORKFLOW_PATH_UNRESOLVED')
    elif selected is None:
        failures.append('WORKFLOW_STAGE_OUTSIDE_SELECTED_PATH')
    effective = selected if selected is not None else row
    if row['contract_selection']=='registered-contracts' and model['contract_id'] not in effective['contract_ids']:
        failures.append('HANDOFF_CONTRACT_MISMATCH')
    human_step=(effective['producer_role']=='engagement:named-authority' or effective['receiving_role'] in ('engagement:named-authority','engagement:named-acceptance-authority'))
    units = effective.get('handoff_content_contract', {}).get('units', []) if selected is not None or selected_path is None else []
    unit_reviews = subject.get('unit_reviews', [])
    unit_reviews = unit_reviews if isinstance(unit_reviews, list) else []
    for unit in units:
        value = model.get('semantic_units', {}).get(unit['semantic_field'])
        valid = (isinstance(value, dict)
                 and value.get('knowledge_status') in ('known', 'synthetic-assumption')
                 and all(content_lint._substantive(value.get(field)) for field in unit['required_fields']))
        refs = value.get('evidence_refs') if isinstance(value, dict) else None
        if (not valid or not isinstance(refs, list) or not refs
                or any(not isinstance(ref, str) or ref not in evidence
                       or not evidence[ref].get('version') or 'payload' not in evidence[ref] for ref in refs)):
            if 'HANDOFF_CONTENT_MISSING_OR_INVALID' not in failures:
                failures.append('HANDOFF_CONTENT_MISSING_OR_INVALID')
        reviews = [review for review in unit_reviews if isinstance(review, dict) and review.get('unit_id') == unit['id']]
        if not human_step and (len(reviews) != 1 or reviews[0].get('verdict') != 'PASS'
                or not content_lint._substantive(reviews[0].get('rationale'))
                or not content_lint._substantive(reviews[0].get('evidence'))):
            if 'RECEIVING_CONTENT_REVIEW_REQUIRED' not in failures:
                failures.append('RECEIVING_CONTENT_REVIEW_REQUIRED')
    input_refs = context.get('input_refs')
    if (not isinstance(context_payload, dict)
            or not context_record.get('version')
            or not isinstance(input_refs, list) or not input_refs
            or any(not isinstance(ref, str) or ref not in evidence
                   or not evidence[ref].get('version') or 'payload' not in evidence[ref] for ref in input_refs)
            or context_payload.get('workflow_id') != row['workflow_id']
            or context_payload.get('profile_hash') != row['handoff_content_contract']['workflow_profile_hash']
            or not content_lint._substantive(context_payload.get('context_id'))
            or not content_lint._substantive(context_payload.get('context_version'))
            or not isinstance(context_payload.get('variant'), str)
            or context_payload.get('variant') not in {variant['id'] for variant in profile['variants']}
            or not isinstance(context.get('route'), str)
            or context.get('route') not in {route['id'] for route in profile['routes']}):
        failures.append('WORKFLOW_CONTEXT_UNRESOLVED')
    elif row['step'] == 1:
        intake = context_payload.get('entry_inputs')
        if (not isinstance(intake, dict) or set(intake) != set(profile['entry_inputs'])
                or any(not content_lint._substantive(value) for value in intake.values())):
            failures.append('WORKFLOW_INTAKE_INCOMPLETE')
    if isinstance(context_payload, dict):
        selected_variant = next((variant for variant in profile['variants']
                                 if variant['id'] == context_payload.get('variant')), {})
        if selected_variant.get('when') and engine._condition(selected_variant['when'], model.get('context', {})) is not True:
            failures.append('WORKFLOW_VARIANT_CONDITION_PENDING_OR_FALSE')
    # Non-entry steps carry the already-reviewed context by reference; source
    # content and route evidence remain covered by the existing receiver digest.
    if context.get('route') == 'stop':
        failures.append('WORKFLOW_STOP_DISPOSITION')
    elif context.get('route') == 'rework':
        failures.append('WORKFLOW_REWORK_REQUIRED')
    elif context.get('route') == 'exit' and (selected_path is None or row['step'] != selected_path['terminal_step']):
        failures.append('WORKFLOW_EXIT_DISPOSITION')
    token=subject.pop('attestation',None)
    payload=content_lint._host_verify(trusted_executions,token)
    producer=content_lint._host_verify(trusted_executions,model.get('producer',{}).get('attestation'))
    bound={'handoff_id':handoff_id,'semantic_hash':content_spec.canonical_hash(model),
           'report_hash':report.get('report_hash'),'catalog_hash':catalog['catalog_hash'],
           'criterion':effective['acceptance_criterion'],'receiving_role':effective['receiving_role'],
           'path_id': selected_path['id'] if selected_path else None,
           'handoff_content_hash': content_spec.canonical_hash(effective['handoff_content_contract'])}
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
        if effective['receiving_role'] not in roles:
            failures.append('RECEIVER_ROLE_UNASSIGNED')
        evidence=subject.get('evidence')
        if subject.get('verdict')!='PASS' or not isinstance(evidence,str) or not evidence.strip():
            failures.append('RECEIVING_GATE_EVIDENCE_REQUIRED')
    result={'schema_version':'1.0.0',**bound,'contract_id':model['contract_id'],
            'status':'ACCEPTANCE_VERIFIED' if not failures else 'ACCEPTANCE_PENDING',
            'findings':failures,'receiver_principal':principal,
            'disposition': context.get('route'),
            'next_step': selected.get('next_step') if selected else None,
            'production_release_authorized':False,'calibration_status':spec.get('calibration_status','synthetic-only')}
    result['result_hash']=content_spec.canonical_hash(result)
    return result


def main(argv=None):
    """List bindings or check a draft with optional host-pinned Gen2 evidence.

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
    command.add_argument('--acceptance')
    command.add_argument('--receiving-assignments',help='Existing host principal-to-functional-role mapping')
    import governed_domain
    governed_domain.add_arguments(command,operations=('draft',))
    args=parser.parse_args(argv)
    try:
        if args.command=='list':
            result=load_bindings(args.root)
        else:
            adapter,authority=governed_domain.from_arguments(args)
            result=check(args.handoff_id,content_spec.load_json(args.model),content_spec.load_json(args.report),
                root=args.root,acceptance=content_spec.load_json(args.acceptance) if args.acceptance else None,
                receiving_assignments=content_spec.load_json(args.receiving_assignments) if args.receiving_assignments else None,
                governed=adapter,authority=authority)
        print(json.dumps(result,indent=2))
        return 0 if args.command=='list' or result.get('status')=='ACCEPTANCE_VERIFIED' else 2
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'error':str(exc)}));return 1

if __name__=='__main__':
    raise SystemExit(main())
