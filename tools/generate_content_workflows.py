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


def build(root=ROOT):
    """Return proposed bindings with source hashes and exact registered contract IDs.

    Args:
        root: Repository containing canonical workflow references and contracts.
    Returns:
        JSON-compatible 24 workflow/207 handoff catalogue, never an approval.
    Raises:
        ValueError: If source rows, roles or editorial selections no longer match.
    """
    root = Path(root)
    contracts = {c['id']:c for c in json.loads((root/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']}
    rows = []
    workflows=json.loads((root/'.ai/runtime/workflows.json').read_text())['workflows']
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
    if len(rows)!=207:
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
