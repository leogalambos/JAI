# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise all explicit workflow handoffs and the existing host identity boundary."""
import copy
import json
from pathlib import Path
import re
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


def test_effectful_workflows_require_prior_authority_and_independent_validation():
    workflows = {w['key']: w for w in json.loads((ROOT/'.ai/runtime/workflows.json').read_text())['workflows']}
    ai = workflows['ai-system-approval']['steps']
    roles = [s['slug'] for s in ai]
    assert roles.index('named-authority') < roles.index('machine-learning-engineer')
    assert 'candidate' in ai[2]['does']
    assert 'no production or pilot' in ai[2]['gate']
    assert 'periodic' in ai[-1]['does']
    retirement = workflows['service-retirement-and-decommission']['steps']
    roles = [s['slug'] for s in retirement]
    assert roles.index('change-manager') < roles.index('identity-and-access-management-engineer')
    assert roles.index('change-manager') < roles.index('site-reliability-engineer') < roles.index('it-asset-manager')
    access = retirement[roles.index('identity-and-access-management-engineer')]
    shutdown = retirement[roles.index('site-reliability-engineer')]
    assert 'bounded shutdown credentials' in access['gate']
    assert 'final credential revocation' in shutdown['hands_over']
    assert 'before asset reconciliation' in shutdown['gate']
    for key, executor, validator in [('incident-to-problem', 'software-engineer', 'test-analyst'),
                                      ('migration-and-cutover', 'data-engineer', 'test-analyst')]:
        steps = workflows[key]['steps']
        approval = next(i for i, s in enumerate(steps) if s['slug'] == 'change-manager')
        execution = next(i for i, s in enumerate(steps) if i > approval and s['slug'] == executor)
        validation = next(i for i, s in enumerate(steps) if i > execution and s['slug'] == validator)
        assert approval < execution < validation
        assert 'prior' in steps[execution]['gate'].lower()
        assert 'independent' in steps[validation]['does']
        assert 'rehearsal' in steps[approval]['gate'].lower() or 'candidate' in steps[approval]['gate'].lower()
        if key == 'migration-and-cutover':
            assessment = next(i for i, s in enumerate(steps) if i > validation and s['slug'] == 'test-manager')
            acceptance = next(i for i, s in enumerate(steps) if s['slug'] == 'it-service-owner')
            assert validation < assessment < acceptance
            assert steps[validation]['tool_tier'] == 'execute'
            assert steps[assessment]['tool_tier'] == 'author'
            assert 'validation effects' in steps[approval]['gate']
        if key == 'incident-to-problem':
            preparation = next(i for i, s in enumerate(steps) if s['slug'] == executor)
            assert preparation < approval
            assert 'pre-production' in steps[preparation]['does']
            assert 'test evidence' in steps[preparation]['hands_over']


def test_publication_source_approval_precedes_editor_and_release_is_separate():
    workflows = json.loads((ROOT/'.ai/runtime/workflows.json').read_text())['workflows']
    steps = next(w['steps'] for w in workflows if w['key'] == 'semantic-to-enterprise-publication')
    assert 'source approval' in steps[1]['gate']
    assert 'external human proof where required' in steps[1]['gate']
    assert 'before the editor acts' in steps[1]['gate']
    assert 'approved semantic snapshot' in steps[2]['does']
    assert 'actual visual evidence' in steps[4]['does']
    assert 'precedes release' in steps[4]['gate']
    assert 'mandatory controls remain blocking' in steps[3]['gate']


def test_repaired_workflow_references_and_contract_selections_match_registry():
    workflows = json.loads((ROOT/'.ai/runtime/workflows.json').read_text())['workflows']
    from content_workflow import SELECTIONS
    for w in workflows:
        if w['key'] not in {'ai-system-approval', 'incident-to-problem', 'migration-and-cutover',
                            'service-retirement-and-decommission', 'semantic-to-enterprise-publication'}:
            continue
        assert len(SELECTIONS[w['key']]) == len(w['steps'])
        assert [s['step'] for s in w['steps']] == list(range(1, len(w['steps']) + 1))
        reference = ROOT/'.ai/skills/it-role-workflows/references'/f"{w['key']}.md"
        rows = []
        for line in reference.read_text().splitlines():
            if re.match(r'\| \d+ \|', line):
                cells = [cell.strip() for cell in line.strip('|').split('|')]
                cells[1] = re.sub(r'^\[([^]]+)\]\([^)]*\)$', r'\1', cells[1])
                rows.append(cells)
        expected = [[str(s['step']), s['role'], s['does'], s['hands_over'], s['gate']] for s in w['steps']]
        assert rows == expected
        public = ROOT/'docs/workflow-library'/f"{w['key']}.md"
        public_rows = [[cell.strip() for cell in line.strip('|').split('|')]
                       for line in public.read_text().splitlines() if re.match(r'\| \d+ \|', line)]
        assert public_rows == expected


def test_vulnerability_remediation_authorises_production_before_deployment():
    workflows = json.loads((ROOT/'.ai/runtime/workflows.json').read_text())['workflows']
    workflow = next(row for row in workflows if row['key'] == 'vulnerability-to-remediation')
    steps = workflow['steps']
    roles = [step['slug'] for step in steps]
    assert roles.index('change-manager') < roles.index('software-engineer')
    candidate = steps[roles.index('container-platform-engineer')]
    assert 'candidate' in candidate['does']
    assert 'not deploy' in candidate['gate']
    authority = steps[roles.index('change-manager')]
    assert 'emergency' in authority['gate']
    deployment = steps[roles.index('software-engineer')]
    assert 'authorisation' in deployment['gate']
    handoffs = {row['step']: row for row in load_bindings(ROOT)['bindings']
                if row['workflow_id'] == workflow['key']}
    assert handoffs[5]['producer_role'] == 'change-manager'
    assert handoffs[5]['contract_ids'] == ['change-manager:1']
    assert handoffs[5]['receiving_role'] == 'software-engineer'
    assert handoffs[6]['contract_ids'] == ['software-engineer:1']


def test_vulnerability_remediation_reference_registry_and_public_table_agree():
    reference = ROOT/'.ai/skills/it-role-workflows/references/vulnerability-to-remediation.md'
    source_rows = []
    for line in reference.read_text().splitlines():
        if re.match(r'\| \d+ \|', line):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            cells[1] = re.match(r'\[([^]]+)\]', cells[1]).group(1)
            source_rows.append(cells)
    registry = json.loads((ROOT/'.ai/runtime/workflows.json').read_text())['workflows']
    workflow = next(row for row in registry if row['key'] == 'vulnerability-to-remediation')
    registry_rows = [[str(step['step']), step['role'], step['does'], step['hands_over'], step['gate']]
                     for step in workflow['steps']]
    assert len(source_rows) == 8
    assert source_rows == registry_rows
    page = (ROOT/'docs/workflow-library/vulnerability-to-remediation.md').read_text()
    public_rows = [[cell.strip() for cell in line.strip('|').split('|')]
                   for line in page.splitlines() if re.match(r'\| \d+ \|', line)]
    assert public_rows == source_rows


def case():
    fixture=json.loads((ROOT/'.ai/runtime/evals/content_quality/decision-paper-simple.json').read_text())
    return prepare_case(fixture,ContentSpec(ROOT))


def test_all_215_canonical_handoffs_have_explicit_sources_receivers_and_contracts():
    catalog=load_bindings(ROOT)
    assert catalog==build(ROOT)
    assert catalog['handoff_count']==215
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
    assert '215' in capsys.readouterr().out


def test_wrong_contract_and_forged_rehashed_qa_are_not_accepted():
    model,spec=case();report=evaluate(model,spec)
    report['gate_verdict']='CONTENT_PASS'
    report['report_hash']=canonical_hash({k:v for k,v in report.items() if k!='report_hash'})
    result=check('access-request-to-review:1',model,report,ROOT)
    assert 'HANDOFF_CONTRACT_MISMATCH' in result['findings']
    assert 'CONTENT_QA_INVALID' in result['findings']
    with pytest.raises(ValueError,match='UNKNOWN_WORKFLOW'):
        check('made-up:1',model,report,ROOT)


def _host_reviewed_workflow(model, spec):
    # This ordinary host-boundary fake proves no actual dispatch or L0 authority.
    from test_content_lint import reviewed
    required = evaluate(model,spec)['reviewer']['required_units']
    model,review,verifier,registry = reviewed(model,spec)
    review['unit_reviews'] = [{'unit_id':ident,'verdict':'PASS',
        'rationale':'Controlled fixture review of the applicable semantic obligation.',
        'evidence':f'Reviewed exact synthetic source against compiled unit {ident}.'}
        for ident in required]
    registry['review-token']['subject_digest'] = canonical_hash(
        {key:value for key,value in review.items() if key != 'attestation'})
    return model,review,verifier,registry


def _current_workflow_fixture(model, spec):
    """Supply explicit synthetic facts for newly selected foundation units.

    Args:
        model: Mutable synthetic semantic fixture from the historical corpus.
        spec: Current compiled contract; its obligations are never removed.
    Returns:
        The fixture with missing current foundation fields populated. These
        invented local test facts are not production evidence or authority.
    """
    facts = {
        'delivery_accountability': {'owner': 'Synthetic delivery owner', 'outcome': 'Reviewed local candidate', 'milestone': 'Candidate review before any release', 'acceptance': 'Independent test evidence'},
        'delivery_dependencies': {'dependency': 'Synthetic approved design revision 1', 'owner': 'Synthetic design owner', 'risk': 'Changed input requires a new review'},
        'document_scope': {'purpose': model['title'], 'audience': 'Synthetic receiving specialist', 'boundary': 'Local fictional workflow fixture', 'source_version': 'synthetic-input-v1'},
        'document_analysis': {'finding': 'Synthetic candidate addresses the stated local requirement', 'basis': 'Synthetic input revision 1', 'limitation': 'No production observation or authority is claimed'},
        'document_actions': {'recipient': 'Synthetic receiving specialist', 'action': 'Review the exact candidate and unresolved limits', 'acceptance': 'Record the independent review result'},
        'data_accountability': {'owner': 'Synthetic demand owner', 'classification': 'Fictional internal demand records', 'use': 'Qualification only', 'retention': 'Disposable test duration'},
        'data_lineage_quality': {'source': 'Synthetic demand input v1', 'transformation': 'Copy business outcome into demand register', 'reconciliation': 'One synthetic input reconciles to one record'},
        'register_schema': {'fields': [{'name': 'demand_id', 'datatype': 'text', 'constraint': 'Unique and nonempty'}, {'name': 'status', 'datatype': 'enum', 'allowed_values': ['pending', 'qualified']}, {'name': 'sponsor', 'datatype': 'text', 'constraint': 'Accountable fictional sponsor required'}]},
        'register_records': {'id': 'synthetic-demand-1', 'status': 'pending', 'owner': 'Synthetic sponsor', 'outcome': 'Assess local service improvement'},
        'register_integrity': {'check': 'Unique demand ID, allowed status and accountable sponsor', 'source_version': 'synthetic-demand-v1', 'change': 'Qualification updates preserve record identity'},
        'architecture_change_impact': {'change': 'Synthetic candidate topology revision 1', 'affected_owner': 'Synthetic platform owner', 'compatibility': 'Existing interface contract retained'},
        'architecture_source_trace': {'element': 'synthetic-component-1', 'source_version': 'synthetic-design-v1', 'requirement': 'Reject unauthorised external requests'},
        'component_design': {'component': 'synthetic-service-1', 'responsibility': 'Validate scoped requests', 'topology': 'One isolated test service with no production connectivity'},
        'interface_contracts': {'interface': 'synthetic-interface-v1', 'input': 'Typed test request', 'output': 'Accepted or rejected result', 'failure': 'Reject malformed or unauthorised input'},
        'design_verification': {'requirement': 'Reject unauthorised requests', 'method': 'Positive and negative isolated test cases', 'acceptance': 'Each case produces the expected result'},
        'security_boundary': {'protected_outcome': 'Integrity of the fictional test service', 'trust_boundary': 'Local test input only', 'handling': 'No real credentials or personal data'},
        'security_control_trace': {'risk': 'Unauthorised test request', 'objective': 'Permit only scoped access', 'control': 'Local validation', 'effectiveness': 'Negative request rejected in synthetic observations'},
        'assurance_criteria': {'obligation': 'Synthetic test requirement v1', 'period': 'Disposable fixture run', 'sample': 'One authorised and one unauthorised request', 'exclusions': 'All real deployments'},
        'assurance_observations': {'procedure': 'Compare synthetic outcomes with declared expected results', 'result': 'Expected local observations recorded', 'evidence': 'Synthetic test transcript v1', 'deviations': []},
        'bounded_conclusion': {'scope': 'Synthetic local test observations only', 'conclusion': 'Declared fictional criteria are met', 'limitations': 'No production, legal or release conclusion'},
        'requirement_sources': {'requirement': 'synthetic-requirement-1', 'source_version': 'synthetic-brief-v1', 'scope': 'Isolated fixture', 'assumptions': 'No external effects'},
        'verifiable_requirements': {'id': 'synthetic-requirement-1', 'statement': 'Reject requests without the declared test identity', 'priority': 'mandatory', 'acceptance': 'Unauthorised test request is rejected'},
        'requirements_consistency': {'requirement': 'synthetic-requirement-1', 'dependency': 'Synthetic identity contract v1', 'conflicts': [], 'change_owner': 'Synthetic requirement owner'},
        'operational_ownership': {'service_owner': 'Synthetic service owner', 'support': 'Local fixture operator', 'boundary': 'Disposable test service', 'escalation': 'Stop and report unexpected state'},
        'operational_recoverability': {'failure': 'Synthetic service stops responding', 'monitor': 'Local test health check', 'recovery': 'Restore the known synthetic baseline', 'evidence': 'Fictional rehearsal transcript v1'},
        'test_evidence_limits': {'sample': 'Synthetic positive and negative cases', 'environment': 'Isolated fixture', 'untested': 'Every real deployment', 'acceptance_owner': 'Independent synthetic receiver'},
        'test_requirement_trace': {'requirement': 'synthetic-requirement-1', 'procedure': 'Submit authorised and unauthorised local requests', 'expected': 'Accept first; reject second', 'evidence': 'Synthetic test transcript v1'},
        'change_behaviour': {'source_revision': 'synthetic-instrumentation-v1', 'requirement': 'Emit one event per accepted synthetic request', 'implementation': 'Versioned local event-emission library', 'interface': 'Synthetic event schema v1'},
        'change_verification': {'invocation': 'Run the local synthetic event-emission test', 'expected': 'One event for one accepted request; zero for a rejected request', 'observed': 'Fictional transcript records the expected counts', 'limits': 'No production or performance claim'},
        'change_recovery': {'compatibility': 'Synthetic event schema v1 remains unchanged', 'telemetry': 'Count local event emission failures', 'failure_detection': 'Mismatched event count fails the test', 'recovery': 'Restore the prior versioned local library'},
    }
    for unit in spec['blueprint']['semantic_units']:
        if unit['category'] != 'required_information':
            continue
        for field in unit.get('semantic_fields', []):
            if field not in model['semantic_units'] and field in facts:
                value = copy.deepcopy(facts[field])
                value['knowledge_status'] = 'synthetic-assumption'
                value['evidence_refs'] = ['SYN-01']
                model['semantic_units'][field] = [value] if unit['datatype'] == 'array' else value
    return model


def test_signed_independent_receiver_requires_host_role_assignment():
    model,spec=case()
    model,review,dispatcher,registry=_host_reviewed_workflow(model,spec)
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
        'reviewer':True,'exit_code':0}
    registry['receiver-token'] = payload
    subject['attestation'] = 'receiver-token'
    kwargs={'acceptance':subject,'trusted_executions':dispatcher}
    result=check(row['handoff_id'],model,report,ROOT,**kwargs)
    assert 'RECEIVER_ROLE_UNASSIGNED' in result['findings']
    kwargs['receiving_assignments']={principal:[row['receiving_role']]}
    assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_VERIFIED'
    subject['evidence']=''
    assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_PENDING'


def test_current_workflow_fixture_does_not_waive_new_required_content():
    engine = ContentSpec(ROOT)
    manifest = json.loads((ROOT/'.ai/runtime/evals/content_quality/manifest.json').read_text())
    fixture = next(json.loads((ROOT/'.ai/runtime'/path).read_text())
                   for path in [*manifest['cases'], *manifest['enterprise_cases']]
                   if json.loads((ROOT/'.ai/runtime'/path).read_text())['contract_id'] == 'data-scientist:1')
    model, spec = prepare_case(fixture, engine)
    model = _current_workflow_fixture(model, spec)
    assert model['semantic_units']['delivery_accountability']
    model, review, dispatcher, _ = _host_reviewed_workflow(model, spec)
    baseline = evaluate(model, spec, reviewer=review, trusted_executions=dispatcher)
    assert baseline['gate_verdict'] == 'CONTENT_PASS'
    del model['semantic_units']['delivery_accountability']
    model, review, dispatcher, _ = _host_reviewed_workflow(model, spec)
    report = evaluate(model, spec, reviewer=review, trusted_executions=dispatcher)
    assert report['gate_verdict'] != 'CONTENT_PASS'
    assert any(f['rule_id'] == 'domain/delivery.delivery_accountability'
               for f in report['findings'])


def test_human_authority_step_cannot_be_approved_by_receiver_json():
    model,spec=case();report=evaluate(model,spec)
    for handoff in ('semantic-to-enterprise-publication:4','semantic-to-enterprise-publication:5'):
        result=check(handoff,model,report,ROOT,acceptance={'verdict':'PASS','existing_jai_l0':True},authority={'approved':True})
        assert 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in result['findings']


def signed_governed_acceptance(bound, tmp_path, monkeypatch):
    """Use actual governed qualification and disposable exact-output human signatures."""
    import hashlib
    from types import SimpleNamespace
    from governed_fixtures import accepted_store
    directory = tmp_path / hashlib.sha256(json.dumps(bound, sort_keys=True).encode()).hexdigest()
    host, _, subject, _ = accepted_store(directory, monkeypatch,
        json.dumps({'profile': 'workflow-acceptance', 'acceptance': bound}))
    return SimpleNamespace(store=host.store, subject=subject, use_scope=host.scope), host


def test_every_handoff_executes_positive_and_missing_receiver_or_authority_checks(tmp_path,monkeypatch):
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
        model = _current_workflow_fixture(model, spec)
        model,review,dispatcher,registry=_host_reviewed_workflow(model,spec)
        report=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
        assert report['gate_verdict']=='CONTENT_PASS',row['handoff_id']
        bound={'handoff_id':row['handoff_id'],'semantic_hash':canonical_hash(model),'report_hash':report['report_hash'],
            'catalog_hash':catalog['catalog_hash'],'criterion':row['acceptance_criterion'],'receiving_role':row['receiving_role']}
        human=row['producer_role']=='engagement:named-authority' or row['receiving_role'] in ('engagement:named-authority','engagement:named-acceptance-authority')
        kwargs={'trusted_executions':dispatcher,'resolver':engine}
        if human:
            authority,host=signed_governed_acceptance(bound,tmp_path,monkeypatch)
            kwargs['authority']=authority
            assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_VERIFIED',row['handoff_id']
            kwargs['authority']=None
            assert 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in check(row['handoff_id'],model,report,ROOT,**kwargs)['findings']
        else:
            subject={**bound,'verdict':'PASS','evidence':'Reviewed the exact scoped workflow gate and evidence in the canonical source.',
                'context_manifest':{'history_policy':'fresh'}}
            execution='synthetic-receiver';pid=103
            principal=f'uid:999:worker:{pid}:execution:{execution}'
            payload={'dispatch_id':execution,'principal':principal,'worker_execution':{'pid':pid,'uid':999,'execution_id':execution,'readonly_inputs':True,'fresh_namespace':True},
                'subject_digest':canonical_hash(subject),'snapshot_digest':canonical_hash(model),'context_digest':canonical_hash(subject['context_manifest']),
                'reviewer':True,'exit_code':0}
            registry['receiver-token'] = payload
            subject['attestation'] = 'receiver-token'
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
