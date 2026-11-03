#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Read legacy content and create an explicit, review-pending DCS migration draft."""
from __future__ import annotations
import argparse
import copy
import json
import content_spec


def migrate(source, contract_id, artifact_id, source_release='26.10.5', field_map=None,
            context=None, root=None):
    """Map only explicitly selected legacy fields into the current registered kind.

    Args:
        source: Original JSON object; never mutated or silently reclassified.
        contract_id: Explicit existing role contract, never inferred from title.
        artifact_id: Stable instance ID retained from the source where present.
        source_release: Supported historical content release .5, .6 or .7.
        field_map: Target semantic field to explicit source dotted-path mapping.
        context: Explicit engagement context; omitted applicability stays unknown.
        root: Trusted current registry root.
    Returns:
        Draft migration envelope with exact original snapshot/hash and field-level
        provenance. Knowledge is pending; old approval/signatures never migrate.
    Raises:
        ValueError: For invalid release, identity change, unknown target or absent
            source field. Existing legacy bytes and canonical contracts stay intact.
    """
    if source_release not in ('26.10.5','26.10.6','26.10.7') or not isinstance(source,dict):
        raise ValueError('UNSUPPORTED_LEGACY_SOURCE')
    if field_map is not None and not isinstance(field_map,dict):
        raise ValueError('MIGRATION_FIELD_MAP_MUST_BE_OBJECT')
    content_spec.canonical_hash(source)
    if not isinstance(artifact_id,str) or not artifact_id.strip() or (source.get('artifact_id') and source['artifact_id']!=artifact_id):
        raise ValueError('MIGRATION_INSTANCE_ID_MUST_BE_PRESERVED')
    if source.get('contract_id') and source['contract_id']!=contract_id:
        raise ValueError('MIGRATION_CONTRACT_ID_MUST_BE_PRESERVED')
    engine=content_spec.ContentSpec(root)
    outline=engine.outline(contract_id,context or {})
    model=copy.deepcopy(outline['semantic_model'])
    model['artifact_id']=artifact_id
    spec=engine.resolve(contract_id,context or {})
    allowed={field for unit in spec['blueprint']['semantic_units'] for field in unit.get('semantic_fields',[])
             if unit['category'] in ('required_information','conditional_information','optional_information')}
    provenance=[]
    def pending(value):
        if isinstance(value,dict):
            result={key:pending(child) for key,child in value.items()
                    if key not in ('attestation','producer','reviewer','approval_refs','evidence_refs','evidence_ref','signature')}
            result['knowledge_status']='pending'
            return result
        if isinstance(value,list):
            return [pending(child) for child in value]
        return copy.deepcopy(value)

    for target,path in (field_map or {}).items():
        if target not in allowed or not isinstance(path,str) or not path:
            raise ValueError('MIGRATION_FIELD_NOT_REGISTERED')
        value=source
        for part in path.split('.'):
            if not isinstance(value,dict) or part not in value:
                raise ValueError('MIGRATION_SOURCE_FIELD_MISSING')
            value=value[part]
        current=model['semantic_units']
        parts=target.split('.')
        for part in parts[:-1]:
            if not isinstance(current.get(part),dict):
                current[part]={}
            current=current[part]
        current[parts[-1]]=pending(value)
        model.setdefault('knowledge_states',{})[target]='pending'
        provenance.append({'target_field':target,'source_path':path,'value_hash':content_spec.canonical_hash(value)})
    # Prior claims and approvals do not establish new semantic evidence or review.
    model.pop('producer',None);model.pop('reviewer',None)
    result={'schema_version':'1.0.0','source_release':source_release,
        'source_hash':content_spec.canonical_hash(source),'legacy_snapshot':copy.deepcopy(source),
        'contract_id':contract_id,'artifact_id':artifact_id,'document_kind':spec['document_kind'],
        'semantic_model':model,'field_provenance':provenance,'status':'DRAFT_INCOMPLETE',
        'professional_review_required':True,'legacy_approvals_transferred':False,
        'decision_purpose':'Requires explicit correction/domain review; legacy acceptance text is not reused.',
        'production_ready':False}
    result['migration_hash']=content_spec.canonical_hash(result)
    return result


def main(argv=None):
    """Print a migration draft; never overwrite the original historical input.

    Args:
        argv: Optional CLI arguments with explicit contract/instance IDs.
    Returns:
        Zero on a valid draft, one for an invalid source, map or registry.
    """
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('--contract-id',required=True)
    parser.add_argument('--artifact-id',required=True);parser.add_argument('--source-release',default='26.10.5')
    parser.add_argument('--field-map');parser.add_argument('--context');parser.add_argument('--root')
    args=parser.parse_args(argv)
    try:
        result=migrate(content_spec.load_json(args.source),args.contract_id,args.artifact_id,
            source_release=args.source_release,field_map=content_spec.load_json(args.field_map) if args.field_map else None,
            context=content_spec.load_json(args.context) if args.context else None,root=args.root)
        print(json.dumps(result,indent=2));return 0
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'error':str(exc)}));return 1

if __name__=='__main__':
    raise SystemExit(main())
