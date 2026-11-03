#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Build explicit proposed workflow acceptance bindings from editorial mappings."""
from pathlib import Path
import argparse
import json
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_spec import canonical_hash

from content_workflow import SELECTIONS


# Explicit source-owned publication contracts; these stages intentionally have no
# professional role-deliverable ID. Their requirements remain canonical here.
SOURCE_HANDOFF_CONTENT = {
    'ai-system-approval:6': {
        'required': [
            'Identify the named human authority, exact candidate version, intended use, deployment scope and reviewed risk and assurance evidence.',
            'Record the actual approval, rejection or conditional decision before the corresponding production effects; an agent recommendation is not authority.',
            'Identify conditions, unresolved evidence, monitoring obligations, validity and change triggers; reference verified external approval where the governing profile requires it.'],
        'conditional': [{'when': 'Evidence requires a bounded pilot before final approval.', 'requirement': 'Reference prior authority for that exact pilot scope, safeguards and stop conditions; pilot evidence does not authorise broader production use.'}],
        'optional': ['Decision communication within the authorised scope.']},
    'semantic-to-enterprise-publication:1': {
        'required': [
            'Identify the exact semantic model version, intended audience, purpose, scope and requested publication formats.',
            'State claims, decisions, alternatives and rationale; link material claims to evidence and distinguish facts, assumptions and unresolved questions.',
            'Identify acceptance criteria, source references, classification, disclosure limits and the owners of unresolved items.'],
        'conditional': [{'when': 'The publication requests a consequential decision.', 'requirement': 'Identify the accountable decision authority, exact decision requested and residual risks requiring disposition.'}],
        'optional': ['Supporting calculations and detailed source annexes referenced by material claims.']},
    'semantic-to-enterprise-publication:2': {
        'required': [
            'Identify reviewer, independence, exact source version and the criteria and evidence actually assessed.',
            'Locate each finding against a claim or criterion; record significance, evidence limits and required resolution.',
            'State a bounded semantic verdict, unresolved findings and any explicit waiver reference without treating missing evidence as a pass.'],
        'conditional': [{'when': 'The governing policy permits a waiver and one is relied upon.', 'requirement': 'Reference prior explicit authority for that exact criterion, scope, rationale, limits and expiry where specified; a reviewer cannot create permission to waive a mandatory gate.'}],
        'optional': ['Comparative recommendations that do not alter the underlying decision.']},
    'semantic-to-enterprise-publication:3': {
        'required': [
            'Identify the approved semantic input version and digest, selected publication archetype, audience and requested formats.',
            'Supply the actual rendered files with a manifest linking every rendition to the same semantic source; preserve claims, caveats and decisions.',
            'Record document identity, classification, references, generation limitations and dependencies needed to reproduce the projection.'],
        'conditional': [{'when': 'A required renderer or format is unavailable.', 'requirement': 'Identify the missing rendition and blocking limitation; do not claim it was produced or inspected.'}],
        'optional': ['Additional audience projections whose semantic equivalence is established.']},
    'semantic-to-enterprise-publication:4': {
        'required': [
            'Identify reviewer, exact rendered files, source binding, inspected formats and actual viewing or rendering method.',
            'Record located findings for legibility, hierarchy, density, tables, diagrams, document control and package integrity.',
            'State the publication verdict and limitations, defect disposition, and any explicit waiver; distinguish static checks from observed visual inspection.'],
        'conditional': [{'when': 'An output format or part of the package could not be inspected.', 'requirement': 'Record the missing inspection and its impact; retain the blocked state unless the governing policy permits and the exact authority explicitly approves a scoped disposition before release.'}],
        'optional': ['Annotated previews and presentation recommendations supporting the findings.']},
    'semantic-to-enterprise-publication:5': {
        'required': [
            'Identify the actual accountable authority, exact publication version and files, permitted audience and release scope.',
            'Reference the applicable semantic and publication reviews, unresolved risks and any authorised conditions or waivers.',
            'Record the explicit decision and its effective conditions using the existing authority mechanism; a drafted request or agent assertion is not approval.'],
        'conditional': [{'when': 'The governing decision requires an L0 signature.', 'requirement': 'Reference the actual operator-signed decision bound to these effects; do not manufacture a signature or inherit another output approval.'}],
        'optional': ['Communication instructions that stay within the approved audience and scope.']},
}


def build(root=ROOT):
    """Return proposed bindings with source hashes and exact registered contract IDs.

    Args:
        root: Repository containing canonical workflow references and contracts.
    Returns:
        JSON-compatible 24-workflow catalogue covering every explicit selected
        stage exactly once; the handoff total follows the canonical chains.
    Raises:
        ValueError: If source rows, roles or editorial selections no longer match.
    """
    root = Path(root)
    contracts = {c['id']:c for c in json.loads((root/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']}
    rows = []
    workflows=json.loads((root/'.ai/runtime/workflows.json').read_text())['workflows']
    source_keys = [source['key'] for source in workflows]
    if len(source_keys) != 24 or len(set(source_keys)) != 24 or set(source_keys) != set(SELECTIONS):
        raise ValueError('WORKFLOW_KEY_COVERAGE: canonical chains and explicit selections must cover the same 24 workflows')
    for source in sorted(workflows,key=lambda item:item['key']):
        workflow=source['key']
        selections=SELECTIONS[workflow]
        path=root/'.ai/runtime/workflows.json'
        chain=[]
        for step in source['steps']:
            role=step['slug']
            if step['skill']=='agent':
                role='agent:'+role
            elif step['skill'] in ('dynamic','external'):
                role='engagement:'+role
            cells=[str(step['step']),step['role'],step['does'],step['hands_over'],step['gate']]
            chain.append((cells,role))
        if len(chain)!=len(selections):
            raise ValueError(f'WORKFLOW_SOURCE_CHANGED: {workflow}')
        for index,((cells,role),choice) in enumerate(zip(chain,selections)):
            contract_role = {'agent:architecture-repository-engineer':'architecture-repository-and-modelling-lead',
                             'agent:model-consistency-reviewer':'architecture-repository-and-modelling-lead'}.get(role,role)
            ids=[] if choice=='source' else [f'{contract_role}:{n}' for n in choice.split(',')]
            if any(c not in contracts for c in ids):
                raise ValueError(f'UNKNOWN_CONTRACT: {workflow}:{index+1}')
            rows.append({'handoff_id':f'{workflow}:{index+1}','workflow_id':workflow,'step':index+1,
                'producer_role':role,'receiving_role':chain[index+1][1] if index+1<len(chain) else 'engagement:named-authority',
                'handover':cells[3],'acceptance_criterion':cells[4], 'contract_ids':ids,
                'contract_selection':'explicit-source-contract' if choice=='source' else 'registered-contracts',
                'artifact_types':sorted({contracts[c]['jai']['semantics']['artifact_type'] for c in ids}),
                'source_ref':str(path.relative_to(root)), 'source_hash':canonical_hash(source),
                'obligation_basis':'Existing workflow handover/gate and explicit professional contract mapping; proposed, pending domain approval.',
                'receiver_checks':['exact-contract-binding','content-qa-replay','existing-gates-preserved','independent-receiver-attestation','specific-gate-evidence']})
    for row in rows:
        if row['contract_selection'] == 'explicit-source-contract':
            row['source_content_contract'] = {
                'id': row['handoff_id'], 'version': '1.0.0',
                'basis': 'JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.',
                **SOURCE_HANDOFF_CONTENT[row['handoff_id']]}
    expected_handoffs = sum(len(SELECTIONS[key]) for key in source_keys)
    if len(rows) != expected_handoffs or len({row['handoff_id'] for row in rows}) != expected_handoffs:
        raise ValueError(f'WORKFLOW_COUNT_CHANGED: {len(rows)}')
    result={'schema_version':'1.0.0','status':'proposed','workflow_count':len(SELECTIONS),'handoff_count':len(rows),'bindings':rows}
    result['catalog_hash']=canonical_hash(result)
    return result


def main(argv=None):
    """Write/check the generated catalogue; return one on drift or invalid source.

    Args:
        argv: Optional command arguments.
    Returns:
        Zero on success, one on source/catalogue mismatch.
    """
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args(argv)
    path=ROOT/'.ai/runtime/content/workflow-acceptance.json'
    payload=json.dumps(build(),indent=2,ensure_ascii=False)+'\n'
    if args.check:
        return 0 if path.exists() and path.read_text()==payload else 1
    path.write_text(payload)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
