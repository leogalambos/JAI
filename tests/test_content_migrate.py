# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Check legacy compatibility without inferred classification or approval carryover."""
import copy
import json
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
from content_spec import ContentSpec,canonical_hash
from content_migrate import migrate,main


def binding():
    engine=ContentSpec(ROOT)
    contract=next(cid for cid,b in engine.bindings.items() if b['document_kind']=='decision-paper')
    spec=engine.resolve(contract,{})
    field=next(u['semantic_fields'][0] for u in spec['blueprint']['semantic_units'] if u['category']=='required_information')
    return contract,field


def test_explicit_migration_preserves_source_instance_and_pending_approval():
    contract,field=binding()
    source={'artifact_id':'legacy:01','approved':True,'details':{'value':{'answer':'Retain platform A with bounded recovery review.','knowledge_status':'pending'}}}
    before=copy.deepcopy(source)
    result=migrate(source,contract,'legacy:01',field_map={field:'details.value'},root=ROOT)
    assert result['source_hash']==canonical_hash(source)
    assert result['legacy_snapshot']==source==before
    assert result['status']=='DRAFT_INCOMPLETE'
    assert not result['legacy_approvals_transferred']
    assert not result['production_ready']
    assert result['field_provenance'][0]['value_hash']==canonical_hash(source['details']['value'])
    assert result['semantic_model']['contract_id']==contract
    assert 'producer' not in result['semantic_model']


def test_migration_rejects_reclassification_missing_fields_and_identity_change():
    contract,field=binding()
    with pytest.raises(ValueError,match='INSTANCE_ID'):
        migrate({'artifact_id':'old'},contract,'new',root=ROOT)
    with pytest.raises(ValueError,match='NOT_REGISTERED'):
        migrate({},contract,'old',field_map={'invented':'x'},root=ROOT)
    with pytest.raises(ValueError,match='SOURCE_FIELD_MISSING'):
        migrate({},contract,'old',field_map={field:'absent'},root=ROOT)
    with pytest.raises(ValueError,match='UNSUPPORTED_LEGACY'):
        migrate({},contract,'old',source_release='25.1.0',root=ROOT)


def test_migration_cli_reads_legacy_file_without_rewriting_it(tmp_path,capsys):
    contract,_=binding();path=tmp_path/'legacy.json';path.write_text('{"artifact_id":"legacy:1"}')
    before=path.read_bytes()
    assert main([str(path),'--contract-id',contract,'--artifact-id','legacy:1','--root',str(ROOT)])==0
    assert path.read_bytes()==before
    assert 'DRAFT_INCOMPLETE' in capsys.readouterr().out
    assert main([str(path),'--contract-id',contract,'--artifact-id','different','--root',str(ROOT)])==1


def test_migration_does_not_reuse_known_state_evidence_or_signed_approval():
    contract,field=binding()
    source={'artifact_id':'old:known','contract_id':contract,'old':{'decision':'Continue platform A.',
        'knowledge_status':'known','evidence_refs':['old-evidence'],'attestation':{'signed':True},'approval_refs':['old-approval']}}
    result=migrate(source,contract,'old:known',field_map={field:'old'},root=ROOT)
    current=result['semantic_model']['semantic_units']
    for part in field.split('.'):current=current[part]
    assert current['knowledge_status']=='pending'
    assert 'evidence_refs' not in current and 'approval_refs' not in current and 'attestation' not in current
    assert result['legacy_snapshot']['old']['knowledge_status']=='known'
    assert result['semantic_model']['knowledge_states'][field]=='pending'
    with pytest.raises(ValueError,match='CONTRACT_ID_MUST_BE_PRESERVED'):
        migrate(source,'chief-information-officer:1','old:known',root=ROOT)
