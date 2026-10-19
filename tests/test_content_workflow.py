# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise all explicit workflow handoffs and the existing host identity boundary."""
import copy
import json
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
sys.path.insert(0,str(ROOT/'tools'))
from content_spec import ContentSpec, canonical_hash
from content_lint import evaluate
from content_eval import prepare_case
from content_workflow import load_bindings, check, main
from generate_content_workflows import build


def case():
    fixture=json.loads((ROOT/'.ai/runtime/evals/content_quality/decision-paper-simple.json').read_text())
    return prepare_case(fixture,ContentSpec(ROOT))


def test_all_207_canonical_handoffs_have_explicit_sources_receivers_and_contracts():
    catalog=load_bindings(ROOT)
    assert catalog==build(ROOT)
    assert catalog['handoff_count']==207
    assert catalog['workflow_count']==24
    workflows={w['key']:w for w in json.loads((ROOT/'.ai/runtime/workflows.json').read_text())['workflows']}
    for row in catalog['bindings']:
        source=workflows[row['workflow_id']]
        step=source['steps'][row['step']-1]
        assert row['handover']==step['hands_over']
        assert row['acceptance_criterion']==step['gate']
        assert row['source_hash']==canonical_hash(source)
        assert row['receiving_role']
        assert row['contract_ids'] or row['contract_selection']=='explicit-source-contract'
        assert len(row['receiver_checks'])==5


def test_draft_receiving_cli_cannot_claim_acceptance(tmp_path,capsys):
    model,spec=case();report=evaluate(model,spec)
    result=check('semantic-to-enterprise-publication:1',model,report,ROOT)
    assert result['status']=='ACCEPTANCE_PENDING'
    assert 'CONTENT_GATE_PENDING_OR_FAILED' in result['findings']
    assert not result['production_release_authorized']
    a=tmp_path/'semantic.json';b=tmp_path/'qa.json'
    a.write_text(json.dumps(model));b.write_text(json.dumps(report))
    assert main(['--root',str(ROOT),'check','semantic-to-enterprise-publication:1',str(a),str(b)])==2
    assert main(['--root',str(ROOT),'list'])==0
    assert '207' in capsys.readouterr().out


def test_wrong_contract_and_forged_rehashed_qa_are_not_accepted():
    model,spec=case();report=evaluate(model,spec)
    report['gate_verdict']='CONTENT_PASS'
    report['report_hash']=canonical_hash({k:v for k,v in report.items() if k!='report_hash'})
    result=check('access-request-to-review:1',model,report,ROOT)
    assert 'HANDOFF_CONTRACT_MISMATCH' in result['findings']
    assert 'CONTENT_QA_INVALID' in result['findings']
    with pytest.raises(ValueError,match='UNKNOWN_WORKFLOW'):
        check('made-up:1',model,report,ROOT)


def test_signed_independent_receiver_requires_host_role_assignment():
    from test_content_lint import authenticated_dispatcher_review
    import hashlib,hmac
    model,spec=case()
    model,review,dispatcher=authenticated_dispatcher_review(model,spec)
    report=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
    assert report['gate_verdict']=='CONTENT_PASS'
    catalog=load_bindings(ROOT)
    row=next(r for r in catalog['bindings'] if r['handoff_id']=='semantic-to-enterprise-publication:1')
    subject={'handoff_id':row['handoff_id'],'semantic_hash':canonical_hash(model),'report_hash':report['report_hash'],
        'catalog_hash':catalog['catalog_hash'],'criterion':row['acceptance_criterion'],'receiving_role':row['receiving_role'],
        'verdict':'PASS','evidence':'Reviewed exact semantic source and traced each required unit to its basis.',
        'context_manifest':{'history_policy':'fresh'}}
    execution='synthetic-receiver';pid=103
    principal=f'uid:999:worker:{pid}:execution:{execution}'
    payload={'dispatch_id':execution,'principal':principal,'worker_execution':{'pid':pid,'uid':999,'execution_id':execution,'readonly_inputs':True,'fresh_namespace':True},
        'subject_digest':canonical_hash(subject),'snapshot_digest':canonical_hash(model),'context_digest':canonical_hash(subject['context_manifest']),
        'reviewer':True,'enforcement':'bwrap-tested','exit_code':0}
    key=b'synthetic-host-key-for-unit-tests-only-000'
    subject['attestation']={'payload':payload,'signature':hmac.new(key,canonical_hash(payload).encode(),hashlib.sha256).hexdigest()}
    kwargs={'acceptance':subject,'trusted_executions':dispatcher}
    result=check(row['handoff_id'],model,report,ROOT,**kwargs)
    assert 'RECEIVER_ROLE_UNASSIGNED' in result['findings']
    kwargs['receiving_assignments']={principal:[row['receiving_role']]}
    assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_VERIFIED'
    subject['evidence']=''
    assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_PENDING'


def test_human_authority_step_cannot_be_approved_by_receiver_json():
    model,spec=case();report=evaluate(model,spec)
    for handoff in ('semantic-to-enterprise-publication:4','semantic-to-enterprise-publication:5'):
        result=check(handoff,model,report,ROOT,acceptance={'verdict':'PASS','existing_jai_l0':True},authority={'approved':True})
        assert 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in result['findings']


def signed_fabric_acceptance(bound,tmp_path,monkeypatch):
    """Use real read-only Fabric hash-chain/signature verification on synthetic data."""
    import hashlib,hmac,importlib.util
    from types import SimpleNamespace
    loader=importlib.util.spec_from_file_location('workflow_content_fabric_fixture',ROOT/'.ai/runtime/fabric/fabric.py')
    module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module)
    key=b'synthetic-workflow-L0-test-key-only-000000000'
    key_path=tmp_path/'synthetic-workflow-verification-key';key_path.write_bytes(key)
    monkeypatch.setattr(module,'KEY_PATH',str(key_path))
    entries=[]
    def entry(op,data,sign=False):
        previous=entries[-1]['hash'] if entries else '0'*64
        sequence=len(entries)+1
        digest=hashlib.sha256((previous+module.canonical(data)+str(sequence)).encode()).hexdigest()
        item={'op':op,'data':data,'seq':sequence,'prev':previous,'hash':digest}
        if sign:item['sig']=hmac.new(key,digest.encode(),hashlib.sha256).hexdigest()
        entries.append(item)
    entry('node',{'id':'frag-acceptance','type':'frag','layer':1,'text':json.dumps({'profile':'workflow-acceptance','acceptance':bound})})
    entry('node',{'id':'evd-workflow','type':'evd','layer':1,'text':'Synthetic gate evidence fixture','confidence':'deterministic'})
    entry('node',{'id':'rev-l0','type':'rev','layer':0,'state':'accepts','reviewer':'Synthetic workflow authority'},True)
    entry('edge',{'src':'evd-workflow','label':'supports','dst':'frag-acceptance'})
    entry('edge',{'src':'frag-acceptance','label':'reviewed_by','dst':'rev-l0'})
    return SimpleNamespace(fabric=module.Fabric('synthetic-workflow-test',entries),fragment_id='frag-acceptance'),entries


def test_every_handoff_executes_positive_and_missing_receiver_or_authority_checks(tmp_path,monkeypatch):
    import hashlib,hmac
    from test_content_lint import authenticated_dispatcher_review
    engine=ContentSpec(ROOT)
    catalog=load_bindings(ROOT)
    manifest=json.loads((ROOT/'.ai/runtime/evals/content_quality/manifest.json').read_text())
    references={}
    for path in [*manifest['cases'],*manifest['enterprise_cases']]:
        reference=json.loads((ROOT/'.ai/runtime'/path).read_text())
        if not reference.get('evaluation_selection',{}).get('overlays'):
            references.setdefault(reference['contract_id'],reference)
    fallback=next(iter(references))
    for row in catalog['bindings']:
        contract=row['contract_ids'][0] if row['contract_ids'] else fallback
        model,spec=prepare_case(references[contract],engine)
        model,review,dispatcher=authenticated_dispatcher_review(model,spec)
        report=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
        assert report['gate_verdict']=='CONTENT_PASS',row['handoff_id']
        bound={'handoff_id':row['handoff_id'],'semantic_hash':canonical_hash(model),'report_hash':report['report_hash'],
            'catalog_hash':catalog['catalog_hash'],'criterion':row['acceptance_criterion'],'receiving_role':row['receiving_role']}
        human=row['producer_role']=='engagement:named-authority' or row['receiving_role']=='engagement:named-authority'
        kwargs={'trusted_executions':dispatcher,'resolver':engine}
        if human:
            authority,entries=signed_fabric_acceptance(bound,tmp_path,monkeypatch)
            kwargs['authority']=authority
            assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_VERIFIED',row['handoff_id']
            entries[2]['sig']='0'*64
            assert 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in check(row['handoff_id'],model,report,ROOT,**kwargs)['findings']
        else:
            subject={**bound,'verdict':'PASS','evidence':'Reviewed the exact scoped workflow gate and evidence in the canonical source.',
                'context_manifest':{'history_policy':'fresh'}}
            execution='synthetic-receiver';pid=103
            principal=f'uid:999:worker:{pid}:execution:{execution}'
            payload={'dispatch_id':execution,'principal':principal,'worker_execution':{'pid':pid,'uid':999,'execution_id':execution,'readonly_inputs':True,'fresh_namespace':True},
                'subject_digest':canonical_hash(subject),'snapshot_digest':canonical_hash(model),'context_digest':canonical_hash(subject['context_manifest']),
                'reviewer':True,'enforcement':'bwrap-tested','exit_code':0}
            key=b'synthetic-host-key-for-unit-tests-only-000'
            subject['attestation']={'payload':payload,'signature':hmac.new(key,canonical_hash(payload).encode(),hashlib.sha256).hexdigest()}
            kwargs.update(acceptance=subject,receiving_assignments={principal:[row['receiving_role']]})
            assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_VERIFIED',row['handoff_id']
            kwargs['receiving_assignments']={}
            assert 'RECEIVER_ROLE_UNASSIGNED' in check(row['handoff_id'],model,report,ROOT,**kwargs)['findings']


def test_rehashed_catalog_cannot_replace_real_workflow_source(tmp_path):
    runtime=tmp_path/'content';runtime.mkdir()
    for name in ('registry.json','workflow-acceptance.json'):
        (runtime/name).write_bytes((ROOT/'.ai/runtime/content'/name).read_bytes())
    (runtime/'migrations').mkdir()
    (runtime/'migrations/26.10.5-binding-map.json').write_bytes((ROOT/'.ai/runtime/content/migrations/26.10.5-binding-map.json').read_bytes())
    (tmp_path/'workflows.json').write_bytes((ROOT/'.ai/runtime/workflows.json').read_bytes())
    data=json.loads((runtime/'workflow-acceptance.json').read_text())
    data['bindings'][0]['acceptance_criterion']='All gates waived by author'
    data['catalog_hash']=canonical_hash({k:v for k,v in data.items() if k!='catalog_hash'})
    (runtime/'workflow-acceptance.json').write_text(json.dumps(data))
    with pytest.raises(ValueError,match='SOURCE_PROVENANCE'):
        load_bindings(tmp_path)


@pytest.mark.parametrize('mutation',['selection','contracts'])
def test_rehashed_catalog_cannot_bypass_registered_contract_scope(tmp_path,mutation):
    runtime=tmp_path/'content';runtime.mkdir()
    for name in ('registry.json','workflow-acceptance.json'):
        (runtime/name).write_bytes((ROOT/'.ai/runtime/content'/name).read_bytes())
    (runtime/'migrations').mkdir()
    (runtime/'migrations/26.10.5-binding-map.json').write_bytes((ROOT/'.ai/runtime/content/migrations/26.10.5-binding-map.json').read_bytes())
    (tmp_path/'workflows.json').write_bytes((ROOT/'.ai/runtime/workflows.json').read_bytes())
    data=json.loads((runtime/'workflow-acceptance.json').read_text())
    if mutation=='selection':
        data['bindings'][0]['contract_selection']='explicit-source-contract'
        data['bindings'][0]['contract_ids']=[]
    else:
        data['bindings'][0]['contract_ids']=['chief-information-officer:1']
    data['catalog_hash']=canonical_hash({k:v for k,v in data.items() if k!='catalog_hash'})
    (runtime/'workflow-acceptance.json').write_text(json.dumps(data))
    with pytest.raises(ValueError,match='CONTRACT_SCOPE'):
        load_bindings(tmp_path)
