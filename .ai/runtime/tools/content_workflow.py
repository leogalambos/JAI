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
import infrastructure_workflow_evidence
from infrastructure_workflow_definitions import DELIVERY, EVIDENCE


# Numbers are editorial selections of canonical role deliverables, not title matching.
SELECTIONS = {
'dast-control-assurance': ['4','1','2','3','source','2','source','2',
                           'source','4','1','2','1','1','1','1','3','2','source'],
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
'idea-to-production': ['2','1,3','1','1,4','2,4','4','1,2,4','2,4','2,4','1','3,4','1','1,2','1'],
'incident-to-problem': ['1','1,2,4','3','1,2,3','1,2','1,4','1,2,4','1','1,4','1,2','1,2','2'],
'migration-and-cutover': ['1,3','1,2,4','1,3','2,3','3','2,4','1','1,3','2,4','2,3','1,4'],
'new-service-onboarding': ['1','1,3','1,4','1,3,4','2,3','1,2,3','1','2,3','1','2','3','1'],
'organisational-change-and-adoption': ['1,3','1,2','2,4','4','4','4'],
'production-change': ['1,4','1,3','2,4','2','1,2','3,4','1,3','1,3','2'],
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



def load_bindings(root=None, *, pilot=None, specialist_policy=None):
    """Return the hash-checked registered workflow acceptance catalogue.

    Args:
        root: Repository or installed runtime root accepted by ContentSpec.
        pilot: Optional path to an explicitly staged, versioned SIEM registration.
        specialist_policy: Optional compiled profile overlays for the current catalogue.
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
        if step.get('variant_only'):
            receiver = next(iter(step['variant_bindings'].values()))['receiving_role']
        else:
            receiver = next((role(item) for item in source['steps'][index + 1:]
                             if not item.get('variant_only')), 'engagement:named-authority')
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
    if specialist_policy is not None:
        if pilot is not None:
            raise ValueError('WORKFLOW_POLICY_SOURCE_CONFLICT')
        from workflow_specialist_profiles import verify_policy

        policy = content_spec.load_json(specialist_policy)
        roles = {item['slug']: item for item in content_spec.load_json(runtime/'roles.json')['roles']}
        skills = runtime.parent/'skills' if (runtime.parent/'skills').is_dir() else runtime/'skills'
        instructions = {slug: lifecycle.blob((skills / role['path'].removeprefix('skills/')).read_bytes())
                        for slug, role in roles.items()}
        contracts = content_spec.load_json(runtime/'artifacts/contracts/role-deliverables.v3.json')['contracts']
        ancestry = content_spec.load_json(runtime/'role-composition.json')['roles']
        if any(ancestry.get(slug, {}).get('ancestry') != chain for slug, chain in policy['ancestry'].items()):
            raise ValueError('WORKFLOW_PROFILE_ANCESTRY_DRIFT')
        verify_policy(policy, roles, instructions, catalogue=catalog,
                      contracts={item['id']: item for item in contracts})
        return policy['catalogue']
    if pilot is not None:
        from workflow_role_selection import stage_siem_workflow

        registration = content_spec.load_json(pilot)
        contracts = content_spec.load_json(runtime/'artifacts/contracts/role-deliverables.v3.json')['contracts']
        try:
            expected = stage_siem_workflow(registration['source'], registration['deployments'], catalog,
                                           {item['id']: item for item in contracts})
        except (KeyError, TypeError) as error:
            raise ValueError('WORKFLOW_PILOT_REGISTRATION') from error
        if registration != expected:
            raise ValueError('WORKFLOW_PILOT_REGISTRATION')
        for row in expected['catalogue']['bindings'][len(rows):]:
            if any(cid not in known for cid in row['contract_ids']):
                raise ValueError('WORKFLOW_UNKNOWN_CONTRACT')
        return expected['catalogue']
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
          receiving_assignments=None, authority=None, resolver=None, governed=None, *, pilot=None, predecessor=None, specialist_policy=None, additional_outputs=None):
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
        pilot: Explicit staged SIEM registration for a governed offline action.
        specialist_policy: Explicit compiled policy supplied by the governed host.
        additional_outputs: Other exact model and QA report pairs in a required set.
        predecessor: Exact prior model, QA report and receiving subject for a
            linked handoff. A nested predecessor supplies the preceding link.
    Returns:
        Existing receiving status; never production acceptance or release.
    Raises:
        ValueError: Registry, exact source or current justification is invalid.
    """
    import contextlib
    if specialist_policy is not None and governed is None:
        raise ValueError('WORKFLOW_PROFILE_REQUIRES_GOVERNED_HOST')
    if pilot is not None:
        if governed is None:
            raise ValueError('WORKFLOW_PILOT_REQUIRES_GOVERNED_HOST')
        if handoff_id not in {'siem-log-source-integration:1', 'siem-log-source-integration:2'}:
            raise ValueError('WORKFLOW_PILOT_HANDOFF_SCOPE')
    with governed.action() if governed is not None else contextlib.nullcontext():
        if governed is not None:
            if not governed.publication_status(model,model.get('audience'))['eligible']:
                raise ValueError('Current Gen2 workflow source justification is unavailable')
            trusted_executions=governed
        if additional_outputs is not None:
            if governed is None or specialist_policy is None or pilot is not None:
                raise ValueError('WORKFLOW_CONJUNCTION_REQUIRES_GOVERNED_POLICY')
            if not isinstance(additional_outputs, list) or any(
                    not isinstance(item, dict) or set(item) != {'model', 'report'}
                    or any(not isinstance(value, dict) for value in item.values()) for item in additional_outputs):
                raise ValueError('WORKFLOW_CONJUNCTION_OUTPUT_SCHEMA')
            engine = resolver if resolver is not None else content_spec.ContentSpec(root)
            reviews = (acceptance or {}).get('output_reviews', {})
            evaluated = []
            for index, item in enumerate([{'model': model, 'report': report}, *additional_outputs]):
                output = item['model']
                if index and not governed.publication_status(output, output.get('audience'))['eligible']:
                    raise ValueError('Current Gen2 workflow source justification is unavailable')
                unit_reviews = reviews.get(output.get('contract_id'), []) if isinstance(reviews, dict) else []
                evaluated.append(_check(handoff_id, output, item['report'], root, {'unit_reviews': unit_reviews},
                    trusted_executions=governed, authority=authority, resolver=engine,
                    predecessor=predecessor, specialist_policy=specialist_policy, conjunction_member=True))
            return _accept_output_set(evaluated, acceptance, governed, receiving_assignments)
        return _check(handoff_id,model,report,root,acceptance,trusted_executions,
                      receiving_assignments,authority,resolver,pilot,predecessor, specialist_policy)


_MOBILE_IDENTITY = ('candidate_build_ref', 'sdk_scope', 'device_scope')
_ABAP_IDENTITY = ('candidate_ref', 'tenant_ref', 'product_release', 'transport_scope')
_EVIDENCE_PREDECESSORS = {
    ('idea-to-production', 'mobile-delivery', 14): (
        7, 'handoff_mobile_automation_evidence', 'handoff_mobile_build', 'build_evidence_ref', _MOBILE_IDENTITY),
    ('idea-to-production', 'mobile-delivery', 8): (
        14, 'handoff_mobile_test_verdict', 'handoff_mobile_automation_evidence', 'automation_evidence_ref', _MOBILE_IDENTITY),
    ('production-change', 'normal/abap-cloud', 5): (
        9, 'handoff_abap_cloud_change_record', 'handoff_abap_cloud_extension_evidence', 'extension_evidence_ref',
        _ABAP_IDENTITY),
    ('production-change', 'normal/abap-cloud', 9): (
        4, 'handoff_abap_cloud_extension_evidence', 'handoff_abap_cloud_release_provenance', 'release_manifest_ref',
        _ABAP_IDENTITY),
}


def _infrastructure_receiving_subject(catalogue, workflow, path, step, predecessor,
                                      current_producer, verifier, assignments, authority, resolver):
    """Check the preceding receiving attestation before advancing a scoped infrastructure path."""
    previous = path['steps'][path['steps'].index(step) - 1]
    previous_id = f'{workflow}:{previous}'
    binding = next(row for row in catalogue['bindings'] if row['handoff_id'] == previous_id)
    selected = binding['variant_bindings'][path['id']]
    model = predecessor['model']
    report = predecessor.get('report')
    subject = predecessor.get('acceptance')
    if not isinstance(report, dict) or not isinstance(subject, dict):
        return False
    subject = copy.deepcopy(subject)
    token = subject.pop('attestation', None)
    proof = content_lint._host_verify(verifier, token) or {}
    prior_token = model.get('producer', {}).get('attestation')
    prior_author = content_lint._host_verify(verifier, prior_token) or {}
    specialties = getattr(verifier, 'receiving_specialties', None)
    principal = proof.get('principal')
    expected = {
        'handoff_id': previous_id,
        'semantic_hash': content_spec.canonical_hash(model),
        'report_hash': report.get('report_hash'),
        'catalog_hash': catalogue['catalog_hash'],
        'criterion': selected['acceptance_criterion'],
        'receiving_role': selected['receiving_role'],
        'path_id': path['id'],
        'handoff_content_hash': content_spec.canonical_hash(selected['handoff_content_contract']),
    }
    if (model.get('contract_id') not in selected['contract_ids']
            or selected['next_step'] != step or not expected['report_hash']
            or subject.get('verdict') != 'PASS'
            or not content_lint._substantive(subject.get('evidence'))
            or any(subject.get(key) != value for key, value in expected.items())
            or not principal or principal == prior_author.get('principal')
            or principal != (current_producer or {}).get('principal')
            or proof.get('reviewer') is not True
            or proof.get('subject_digest') != content_spec.canonical_hash(subject)
            or proof.get('context_digest') != content_spec.canonical_hash(subject.get('context_manifest'))
            or proof.get('snapshot_digest') != expected['semantic_hash']
            or selected['receiving_role'] not in (assignments or {}).get(principal, [])
            or not callable(specialties)
            or specialties(prior_token, reviewer=False) != [selected['producer_role']]
            or specialties(token) != [selected['receiving_role']]):
        return False
    unit_reviews = subject.get('unit_reviews')
    if not isinstance(unit_reviews, list):
        return False
    for unit in selected['handoff_content_contract']['units']:
        reviews = [row for row in unit_reviews if isinstance(row, dict) and row.get('unit_id') == unit['id']]
        if (len(reviews) != 1 or reviews[0].get('verdict') != 'PASS'
                or not content_lint._substantive(reviews[0].get('evidence'))
                or not content_lint._substantive(reviews[0].get('rationale'))):
            return False
    if infrastructure_workflow_evidence.artifact_findings(workflow, path, previous, model):
        return False
    prior_spec = resolver.resolve(model['contract_id'], model.get('context', {}))
    if (report.get('gate_verdict') != 'CONTENT_PASS' or report.get('deterministic_status') != 'PASS'
            or content_lint.verify_report(report, model, prior_spec, verifier, authority)):
        return False
    if workflow == 'production-change' and previous == 5:
        expected['infrastructure_input'] = subject.get('infrastructure_input')
        return bool(expected['infrastructure_input']) and _human_accepted(authority, expected)
    return True


def _evidence_predecessor(model, predecessor, link, lookup):
    """Resolve a workflow evidence link against the host's exact assigned input.

    Args:
        model: Current semantic artifact.
        predecessor: Exact preceding model with its QA and receiving evidence.
        link: Declared predecessor step, semantic units and reference field.
        lookup: Host-provided lookup of the current assigned predecessor.

    Returns:
        Exact predecessor reference when the declared identity fields match.
    """
    if (not callable(lookup) or not isinstance(predecessor, dict)
            or set(predecessor) - {'model', 'report', 'acceptance', 'predecessor'}
            or any(not isinstance(predecessor.get(key), dict) for key in ('model', 'report', 'acceptance'))):
        return None
    _, current_unit, prior_unit, reference_field, identity_fields = link
    previous = predecessor['model']
    current_facts = model.get('semantic_units', {}).get(current_unit)
    prior_facts = previous.get('semantic_units', {}).get(prior_unit)
    if not isinstance(current_facts, dict) or not isinstance(prior_facts, dict):
        return None
    for field in identity_fields:
        value = current_facts.get(field)
        if not content_lint._substantive(value) or value != prior_facts.get(field):
            return None
    current_token = model.get('producer', {}).get('attestation')
    prior_token = previous.get('producer', {}).get('attestation')
    if current_token is None or prior_token is None:
        return None
    reference = lookup(current_token, prior_token)
    return reference if reference and current_facts.get(reference_field) == reference else None


def _abap_released_apis(facts, evidence):
    """Verify the release status recorded for each exact ABAP dependency.

    Args:
        facts: Extension evidence with the declared tenant and product release.
        evidence: Versioned evidence records indexed by their semantic IDs.

    Returns:
        Whether every declared dependency has an applicable released API record.
    """
    if not isinstance(facts, dict):
        return False
    apis = facts.get('released_apis')
    if not isinstance(apis, list) or not apis or any(not isinstance(ref, str) for ref in apis):
        return False
    if len(set(apis)) != len(apis):
        return False
    for ref in apis:
        record = evidence.get(ref, {})
        payload = record.get('payload')
        if (not record.get('version') or not isinstance(payload, dict)
                or payload.get('release_status') != 'released'
                or not content_lint._substantive(payload.get('api_id'))
                or any(payload.get(field) != facts.get(field) for field in ('tenant_ref', 'product_release'))):
            return False
    return True


def _accept_output_set(members, acceptance, verifier, receiving_assignments):
    """Bind independently checked outputs to one exact receiving attestation.

    Args:
        members: Producer-only checks in authoritative contract order.
        acceptance: Receiving subject and host attestation of the entire set.
        verifier: Governed verifier that resolves native proof tokens.
        receiving_assignments: Host-owned functional receiver assignments.

    Returns:
        One hash-bound acceptance result for the complete contract set.
    """
    from workflow_specialist_profiles import ALL_REQUIRED_PROTOCOL

    first = members[0]
    contract_set = first['contract_set']
    references = contract_set.get('contracts', [])
    shared = ('handoff_id', 'catalog_hash', 'criterion', 'receiving_role', 'path_id',
              'handoff_content_hash', 'producer_selection', 'predecessor', 'infrastructure_input')
    bound = {key: first[key] for key in shared if key in first}
    findings = list(dict.fromkeys(code for member in members for code in member['findings']))
    producers = [member.get('producer') or {} for member in members]
    origins = [producer.get('workflow_output') or {} for producer in producers]
    artifacts = [origin.get('artifact') or {} for origin in origins]
    artifact_refs = [point.get('ref') for point in artifacts]
    material_digests = [origin.get('material_digest') for origin in origins]
    if (contract_set.get('protocol') != ALL_REQUIRED_PROTOCOL or len(references) < 2
            or [ref['id'] for ref in references] != [member['contract_id'] for member in members]
            or any(member['human_step'] or member['contract_set'] != contract_set
                   or member['governing_subject'] != first['governing_subject']
                   or any(member.get(key) != first.get(key) for key in shared) for member in members)
            or not origins[0].get('assignment')
            or any(origin.get('assignment') != origins[0]['assignment'] for origin in origins)
            or not producers[0].get('invocation')
            or any(producer.get('invocation') != producers[0]['invocation'] for producer in producers)
            or not artifacts[0].get('use_scope')
            or any(point.get('use_scope') != artifacts[0]['use_scope'] for point in artifacts)
            or any(not ref for ref in artifact_refs)
            or any(digest != member['semantic_hash'] for digest, member in zip(material_digests, members, strict=True))
            or len(set(material_digests)) != len(members)):
        findings.append('WORKFLOW_OUTPUT_SET_MISMATCH')
    outputs = [{'contract_id': member['contract_id'], 'artifact_ref': artifact,
                'semantic_hash': member['semantic_hash'], 'report_hash': member['report_hash']}
               for member, artifact in zip(members, artifact_refs, strict=True)]
    bound.update(contract_set=contract_set, outputs=outputs,
                 semantic_hash=content_spec.canonical_hash(outputs), assignment=origins[0].get('assignment'),
                 producer_invocation=producers[0].get('invocation'), use_scope=artifacts[0].get('use_scope'),
                 governing_subject_hash=content_spec.canonical_hash(first['governing_subject']))
    subject = copy.deepcopy(acceptance) if isinstance(acceptance, dict) else {}
    token = subject.pop('attestation', None)
    proof = content_lint._host_verify(verifier, token) or {}
    principal = proof.get('principal')
    if any(subject.get(key) != value for key, value in bound.items()):
        findings.append('RECEIVER_SUBJECT_MISMATCH')
    if (proof.get('reviewer') is not True or not principal
            or any(principal == producer.get('principal') for producer in producers)
            or proof.get('subject_digest') != content_spec.canonical_hash(subject)
            or proof.get('snapshot_digest') != bound['semantic_hash']
            or proof.get('context_digest') != content_spec.canonical_hash(subject.get('context_manifest'))):
        findings.append('RECEIVER_IDENTITY_UNVERIFIED')
    receiving_role = bound['receiving_role']
    if (receiving_role not in (receiving_assignments or {}).get(principal, [])
            or (not receiving_role.startswith('engagement:')
                and verifier.receiving_specialties(token) != [receiving_role])):
        findings.append('WORKFLOW_RECEIVER_SELECTION_MISMATCH')
    if subject.get('verdict') != 'PASS' or not content_lint._substantive(subject.get('evidence')):
        findings.append('RECEIVING_GATE_EVIDENCE_REQUIRED')
    result = {'schema_version': '2.0.0', **bound, 'findings': findings, 'receiver_principal': principal,
              'status': 'ACCEPTANCE_PENDING' if findings else 'ACCEPTANCE_VERIFIED',
              'next_step': first['next_step'], 'production_release_authorized': False}
    result['result_hash'] = content_spec.canonical_hash(result)
    return result


def _check(handoff_id, model, report, root=None, acceptance=None, trusted_executions=None,
           receiving_assignments=None, authority=None, resolver=None, pilot=None, predecessor=None, specialist_policy=None,
           conjunction_member=False):
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
        pilot: Explicit staged SIEM registration path, if one was requested.
        specialist_policy: Explicit reviewed specialist profile policy for this batch.
        conjunction_member: Internal validation of one producer output of a set.
        predecessor: Host-provided preceding artifact, report and receiving evidence.
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
    pilot_path = Path(pilot).resolve() if pilot is not None else None
    specialist_path = Path(specialist_policy).resolve() if specialist_policy is not None else None
    if not hasattr(engine, '_workflow_catalog'):
        if specialist_path is None:
            engine._workflow_catalog = load_bindings(root) if pilot_path is None else load_bindings(root, pilot=pilot_path)
        else:
            engine._workflow_catalog = load_bindings(root, pilot=pilot_path, specialist_policy=specialist_path)
        engine._workflow_pilot = pilot_path
        engine._workflow_specialist_policy = specialist_path
    elif (getattr(engine, '_workflow_pilot', None) != pilot_path
          or getattr(engine, '_workflow_specialist_policy', None) != specialist_path):
        raise ValueError('WORKFLOW_PILOT_RESOLVER_MISMATCH')
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
    governing_evidence = {}
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
        elif conjunction_member:
            governing_evidence.update((ref, evidence[ref]) for ref in refs)
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
    elif selected_path is not None and row['step'] == selected_path['steps'][0]:
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
    producer_proof = (producer or {}).get('workflow_producer')
    requirement = effective.get('workflow_role_requirement')
    contract = (requirement or {}).get('contract', {})
    contract_refs = contract.get('contracts', []) if conjunction_member else [contract]
    if requirement is not None or producer_proof is not None:
        binding = (producer_proof or {}).get('binding', {})
        slug = (producer_proof or {}).get('slug')
        mapping = binding.get('mapping_hashes', {}).get(slug)
        if (not isinstance(requirement, dict)
                or requirement.get('mode') != 'compatible-specialization'
                or binding.get('mode') != 'compatible-specialization'
                or binding.get('endpoint') != 'producer'
                or binding.get('workflow_catalogue') != bound['catalog_hash']
                or binding.get('handoff') != bound['handoff_id']
                or binding.get('path') != bound['path_id']
                or binding.get('handoff_contract_hash') != bound['handoff_content_hash']
                or binding.get('bound_role') != effective['producer_role']
                or binding.get('contract') != requirement.get('contract')
                or model['contract_id'] not in {ref.get('id') for ref in contract_refs}
                or binding.get('requirement_hash') != requirement.get('requirement_hash')
                or binding.get('profile') != requirement.get('profile')
                or not mapping or not producer_proof.get('selection_ref') or not producer_proof.get('scope_ref')):
            failures.append('WORKFLOW_PRODUCER_SELECTION_MISMATCH')
        else:
            bound['producer_selection'] = {
                'slug': slug, 'mapping_hash': mapping, 'selection_ref': producer_proof['selection_ref'],
                'scope_ref': producer_proof['scope_ref'],
            }
    if pilot_path is not None and handoff_id == 'siem-log-source-integration:2':
        specialties = getattr(trusted_executions, 'receiving_specialties', None)
        producer_token = model.get('producer', {}).get('attestation')
        if not producer or not callable(specialties) or specialties(
                producer_token, reviewer=False) != [effective['producer_role']]:
            failures.append('WORKFLOW_TERMINAL_PRODUCER_ROLE_MISMATCH')
        lookup = getattr(trusted_executions, 'predecessor_input', None)
        prior = None
        if (callable(lookup) and isinstance(predecessor, dict)
                and set(predecessor) == {'model', 'report', 'acceptance'}
                and all(isinstance(value, dict) for value in predecessor.values())):
            previous_model = predecessor['model']
            previous_producer = previous_model.get('producer')
            if isinstance(previous_producer, dict):
                previous_token = previous_producer.get('attestation')
                reference = lookup(producer_token, previous_token)
                assessment = model.get('semantic_units', {}).get('independent_assessment', {})
                if reference and isinstance(assessment, dict) and assessment.get('reviewed_artifact_ref') == reference:
                    previous = _check('siem-log-source-integration:1', previous_model, predecessor['report'],
                        root, predecessor['acceptance'], trusted_executions, receiving_assignments,
                        resolver=engine, pilot=pilot_path)
                    if (previous['status'] == 'ACCEPTANCE_VERIFIED' and previous['next_step'] == 2
                            and previous['path_id'] == bound['path_id']
                            and previous['receiver_principal'] == (producer or {}).get('principal')
                            and assessment.get('receiving_principal') == previous['receiver_principal']):
                        prior = {'artifact_ref': reference, 'result_hash': previous['result_hash']}
        if prior is None:
            failures.append('WORKFLOW_TERMINAL_PREDECESSOR_UNVERIFIED')
        else:
            bound['predecessor'] = prior
    link = _EVIDENCE_PREDECESSORS.get((row['workflow_id'], bound['path_id'], row['step']))
    if (row['workflow_id'], bound['path_id'], row['step']) == ('production-change', 'normal/abap-cloud', 9):
        if not _abap_released_apis(model.get('semantic_units', {}).get('handoff_abap_cloud_extension_evidence'), evidence):
            failures.append('WORKFLOW_ABAP_RELEASED_API_EVIDENCE_REQUIRED')
    if link:
        reference = _evidence_predecessor(model, predecessor, link,
                                          getattr(trusted_executions, 'predecessor_input', None))
        prior = None
        if reference is not None:
            previous = _check(f"{row['workflow_id']}:{link[0]}", predecessor['model'],
                              predecessor['report'], root, predecessor['acceptance'],
                              trusted_executions, receiving_assignments, authority,
                              resolver=engine, predecessor=predecessor.get('predecessor'),
                              specialist_policy=specialist_path)
            if (previous['status'] == 'ACCEPTANCE_VERIFIED'
                    and previous['path_id'] == bound['path_id']
                    and previous['next_step'] == row['step']):
                prior = {'artifact_ref': reference, 'result_hash': previous['result_hash']}
        if prior is None:
            failures.append('WORKFLOW_EVIDENCE_PREDECESSOR_UNVERIFIED')
        else:
            bound['predecessor'] = prior
    infrastructure_step = (row['workflow_id'], bound['path_id'], row['step']) in EVIDENCE
    if infrastructure_step:
        specialties = getattr(trusted_executions, 'receiving_specialties', None)
        if (not callable(specialties) or not producer or specialties(
                model.get('producer', {}).get('attestation'), reviewer=False) != [effective['producer_role']]):
            failures.append('INFRASTRUCTURE_PRODUCER_SELECTION_MISMATCH')
        if not human_step and (not callable(specialties) or not payload
                               or specialties(token) != [effective['receiving_role']]):
            failures.append('INFRASTRUCTURE_RECEIVER_SELECTION_MISMATCH')
        infrastructure_findings, accepted_input = infrastructure_workflow_evidence.verify(
            row['workflow_id'], selected_path, row['step'], model,
            model.get('producer', {}).get('attestation'), predecessor, trusted_executions)
        failures.extend(infrastructure_findings)
        if accepted_input is not None:
            bound['infrastructure_input'] = accepted_input
            if not _infrastructure_receiving_subject(
                    catalog, row['workflow_id'], selected_path, row['step'], predecessor,
                    producer, trusted_executions, receiving_assignments, authority, engine):
                failures.append('INFRASTRUCTURE_PREDECESSOR_ACCEPTANCE_UNVERIFIED')
    if (selected_path is not None and row['workflow_id'] == 'production-change' and row['step'] == 5
            and selected_path['mechanism'] in DELIVERY and not _human_accepted(authority, bound)):
        failures.append('EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED')
    if conjunction_member:
        facts = model.get('semantic_units', {})
        governing_subject = {
            'context': context_record,
            'units': {unit['semantic_field']: facts.get(unit['semantic_field']) for unit in units},
            'evidence': governing_evidence,
            'inputs': {ref: evidence.get(ref) for ref in input_refs if isinstance(ref, str)}
                      if isinstance(input_refs, list) else {},
        }
        return {**bound, 'contract_id': model['contract_id'], 'contract_set': contract,
                'producer': producer, 'governing_subject': governing_subject, 'findings': failures,
                'human_step': human_step, 'next_step': selected.get('next_step') if selected else None}
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
        if 'producer_selection' in bound and payload:
            specialties = getattr(trusted_executions, 'receiving_specialties', None)
            if not callable(specialties) or specialties(token) != [effective['receiving_role']]:
                failures.append('WORKFLOW_RECEIVER_SELECTION_MISMATCH')
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
    listing = sub.add_parser('list')
    listing.add_argument('--staged-siem', type=Path)
    listing.add_argument('--specialist-policy', type=Path)
    command=sub.add_parser('check')
    command.add_argument('handoff_id');command.add_argument('model');command.add_argument('report')
    command.add_argument('--acceptance')
    command.add_argument('--staged-siem', type=Path)
    command.add_argument('--specialist-policy', type=Path)
    command.add_argument('--predecessor')
    command.add_argument('--additional-outputs', help='JSON list of other exact model and QA report pairs')
    command.add_argument('--receiving-assignments',help='Existing host principal-to-functional-role mapping')
    import governed_domain
    governed_domain.add_arguments(command,operations=('draft',))
    args=parser.parse_args(argv)
    try:
        if args.command=='list':
            result=load_bindings(args.root, pilot=args.staged_siem, specialist_policy=args.specialist_policy)
        else:
            adapter,authority=governed_domain.from_arguments(args)
            result=check(args.handoff_id,content_spec.load_json(args.model),content_spec.load_json(args.report),
                root=args.root,acceptance=content_spec.load_json(args.acceptance) if args.acceptance else None,
                receiving_assignments=content_spec.load_json(args.receiving_assignments) if args.receiving_assignments else None,
                governed=adapter,authority=authority,pilot=args.staged_siem, specialist_policy=args.specialist_policy,
                additional_outputs=content_spec.load_json(args.additional_outputs) if args.additional_outputs else None,
                predecessor=content_spec.load_json(args.predecessor) if args.predecessor else None)
        print(json.dumps(result,indent=2))
        return 0 if args.command=='list' or result.get('status')=='ACCEPTANCE_VERIFIED' else 2
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'error':str(exc)}));return 1

if __name__=='__main__':
    raise SystemExit(main())
