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


def test_all_canonical_handoffs_have_explicit_sources_receivers_and_contracts():
    catalog=load_bindings(ROOT)
    assert catalog==build(ROOT)
    assert catalog['handoff_count']==236
    assert catalog['workflow_count']==25
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
    assert '236' in capsys.readouterr().out


def test_wrong_contract_and_forged_rehashed_qa_are_not_accepted():
    model,spec=case();report=evaluate(model,spec)
    report['gate_verdict']='CONTENT_PASS'
    report['report_hash']=canonical_hash({k:v for k,v in report.items() if k!='report_hash'})
    result=check('access-request-to-review:1',model,report,ROOT)
    assert 'HANDOFF_CONTRACT_MISMATCH' in result['findings']
    assert 'CONTENT_QA_INVALID' in result['findings']
    with pytest.raises(ValueError,match='UNKNOWN_WORKFLOW'):
        check('made-up:1',model,report,ROOT)


@pytest.mark.parametrize('handoff_id', ['access-request-to-review:2', 'architecture-model-to-repository-governance:3'])
def test_related_general_deliverable_cannot_replace_exact_handoff_content(handoff_id):
    model, spec = case()
    report = evaluate(model, spec)
    result = check(handoff_id, model, report, ROOT)
    assert 'HANDOFF_CONTENT_MISSING_OR_INVALID' in result['findings']
    assert 'RECEIVING_CONTENT_REVIEW_REQUIRED' in result['findings']


@pytest.mark.parametrize('mutation,expected', [
    ('unknown-variant', 'WORKFLOW_CONTEXT_UNRESOLVED'),
    ('malformed-variant', 'WORKFLOW_CONTEXT_UNRESOLVED'),
    ('malformed-route', 'WORKFLOW_CONTEXT_UNRESOLVED'),
    ('stale-profile', 'WORKFLOW_CONTEXT_UNRESOLVED'),
    ('unversioned-context', 'WORKFLOW_CONTEXT_UNRESOLVED'),
    ('missing-input-ref', 'WORKFLOW_CONTEXT_UNRESOLVED'),
    ('missing-intake', 'WORKFLOW_INTAKE_INCOMPLETE'),
    ('stop', 'WORKFLOW_STOP_DISPOSITION'),
    ('rework', 'WORKFLOW_REWORK_REQUIRED'),
    ('exit', 'WORKFLOW_EXIT_DISPOSITION'),
])
def test_workflow_context_and_route_are_consumed_at_the_receiving_boundary(mutation, expected):
    row = next(row for row in load_bindings(ROOT)['bindings'] if row['handoff_id'] == 'access-request-to-review:1')
    model, spec = case()
    model = _handoff_content_fixture(row, model)
    context = next(item for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    if mutation == 'unknown-variant':
        context['payload']['variant'] = 'invented-permission'
    elif mutation == 'malformed-variant':
        context['payload']['variant'] = []
    elif mutation == 'malformed-route':
        model['semantic_units']['workflow_context']['route'] = {}
    elif mutation == 'stale-profile':
        context['payload']['profile_hash'] = '0' * 64
    elif mutation == 'unversioned-context':
        context.pop('version')
    elif mutation == 'missing-input-ref':
        model['semantic_units']['workflow_context']['input_refs'] = ['missing-versioned-input']
    elif mutation == 'missing-intake':
        context['payload']['entry_inputs'].clear()
    else:
        model['semantic_units']['workflow_context']['route'] = mutation
    result = check(row['handoff_id'], model, evaluate(model, spec), ROOT)
    assert expected in result['findings']
    assert result['status'] == 'ACCEPTANCE_PENDING'


def test_later_boundary_reuses_context_without_reconstructing_entry_inputs():
    row = next(row for row in load_bindings(ROOT)['bindings'] if row['handoff_id'] == 'access-request-to-review:2')
    model, spec = case()
    model = _handoff_content_fixture(row, model)
    context = next(item for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context['payload'].pop('entry_inputs')
    result = check(row['handoff_id'], model, evaluate(model, spec), ROOT)
    assert 'WORKFLOW_INTAKE_INCOMPLETE' not in result['findings']
    assert 'WORKFLOW_CONTEXT_UNRESOLVED' not in result['findings']
    assert 'RECEIVER_IDENTITY_UNVERIFIED' in result['findings']


@pytest.mark.parametrize('handoff_id,variant,field', [
    ('data-product-delivery:1', 'nonpersonal', 'processes_personal_data'),
    ('regulatory-change-to-assurance:1', 'not-applicable', 'regulatory_requirement'),
])
def test_context_variant_cannot_contradict_known_applicability(handoff_id, variant, field):
    row = next(row for row in load_bindings(ROOT)['bindings'] if row['handoff_id'] == handoff_id)
    model, spec = case()
    model = _handoff_content_fixture(row, model)
    context = next(item for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context['payload']['variant'] = variant
    model['context'][field] = True
    result = check(row['handoff_id'], model, evaluate(model, spec), ROOT)
    assert 'WORKFLOW_VARIANT_CONDITION_PENDING_OR_FALSE' in result['findings']


def test_handoff_catalogue_defines_individual_decision_and_interchange_revision():
    rows = {row['handoff_id']: row for row in build(ROOT)['bindings']}
    decision = rows['access-request-to-review:2']['handoff_content_contract']
    assert decision['units'][0]['semantic_field'] == 'individual_access_decision'
    assert {'subject', 'entitlement', 'purpose', 'decision', 'authority', 'validity', 'policy_ref'} <= set(decision['units'][0]['required_fields'])
    revision = rows['architecture-model-to-repository-governance:3']['handoff_content_contract']
    assert {'repository_revision', 'interchange_manifest', 'workflow_context'} == {unit['semantic_field'] for unit in revision['units']}


@pytest.mark.parametrize('mutation', ['none', 'missing-purpose', 'unknown', 'missing-evidence', 'missing-review', 'duplicate-review'])
def test_exact_handoff_content_and_each_receiving_unit_review_are_required(mutation):
    row = next(row for row in load_bindings(ROOT)['bindings'] if row['handoff_id'] == 'access-request-to-review:2')
    model, spec = case()
    model = _handoff_content_fixture(row, model)
    record = model['semantic_units']['individual_access_decision']
    if mutation == 'missing-purpose':
        record.pop('purpose')
    elif mutation == 'unknown':
        record['knowledge_status'] = 'unknown'
    elif mutation == 'missing-evidence':
        record['evidence_refs'] = ['nonexistent-source']
    review = {'unit_id': row['handoff_content_contract']['units'][0]['id'], 'verdict': 'PASS',
              'rationale': 'Reviewed the specific fictional access decision against the requested purpose and bounds.',
              'evidence': 'Synthetic individual decision record and versioned SYN-01 source.'}
    reviews = [{'unit_id': unit['id'], 'verdict': 'PASS',
                'rationale': 'Reviewed this synthetic boundary and context reference.',
                'evidence': 'Fictional populated record and versioned source.'}
               for unit in row['handoff_content_contract']['units']]
    reviews[0] = review
    if mutation == 'missing-review':
        reviews = reviews[1:]
    if mutation == 'duplicate-review':
        reviews.append(copy.deepcopy(review))
    findings = check(row['handoff_id'], model, evaluate(model, spec), ROOT,
                     acceptance={'unit_reviews': reviews})['findings']
    assert ('HANDOFF_CONTENT_MISSING_OR_INVALID' in findings) == (mutation in ('missing-purpose', 'unknown', 'missing-evidence'))
    assert ('RECEIVING_CONTENT_REVIEW_REQUIRED' in findings) == (mutation in ('missing-review', 'duplicate-review'))
    assert 'RECEIVER_IDENTITY_UNVERIFIED' in findings


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


@pytest.mark.parametrize('context_version', ['1', '2'])
def test_signed_independent_receiver_requires_host_role_assignment(context_version):
    model,spec=case()
    row=next(r for r in load_bindings(ROOT)['bindings'] if r['handoff_id']=='semantic-to-enterprise-publication:1')
    model = _handoff_content_fixture(row, model)
    context = next(item for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context['version'] = context_version
    context['payload']['context_version'] = context_version
    model,review,dispatcher,registry=_host_reviewed_workflow(model,spec)
    report=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
    assert report['gate_verdict']=='CONTENT_PASS'
    catalog=load_bindings(ROOT)
    row=next(r for r in catalog['bindings'] if r['handoff_id']=='semantic-to-enterprise-publication:1')
    selected = _selected_handoff_fixture(row, model)
    subject={'handoff_id':row['handoff_id'],'semantic_hash':canonical_hash(model),'report_hash':report['report_hash'],
        'catalog_hash':catalog['catalog_hash'],'criterion':selected['acceptance_criterion'],'receiving_role':selected['receiving_role'],
        'path_id': 'draft', 'handoff_content_hash': canonical_hash(selected['handoff_content_contract']),
        'verdict':'PASS','evidence':'Reviewed exact semantic source and traced each required unit to its basis.',
        'unit_reviews': [{'unit_id': unit['id'], 'verdict': 'PASS',
                          'rationale': 'Reviewed the exact synthetic semantic handoff and intake reference.',
                          'evidence': 'Versioned fictional handoff content and synthetic context record.'}
                         for unit in selected['handoff_content_contract']['units']],
        'context_manifest':{'history_policy':'fresh'}}
    execution='synthetic-receiver';pid=103
    principal=f'uid:999:worker:{pid}:execution:{execution}'
    payload={'dispatch_id':execution,'principal':principal,'worker_execution':{'pid':pid,'uid':999,'execution_id':execution,'readonly_inputs':True,'fresh_namespace':True},
        'subject_digest':canonical_hash(subject),'snapshot_digest':canonical_hash(model),'context_digest':canonical_hash(subject['context_manifest']),
        'reviewer':True,'exit_code':0}
    registry['receiver-token'] = payload
    subject['attestation'] = 'receiver-token'
    kwargs={'acceptance':subject,'trusted_executions':dispatcher,'resolver':ContentSpec(ROOT)}
    result=check(row['handoff_id'],model,report,ROOT,**kwargs)
    assert 'RECEIVER_ROLE_UNASSIGNED' in result['findings']
    kwargs['receiving_assignments']={principal:[selected['receiving_role']]}
    assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_VERIFIED'
    subject['evidence']=''
    assert check(row['handoff_id'],model,report,ROOT,**kwargs)['status']=='ACCEPTANCE_PENDING'


def test_host_pinned_resolver_loads_workflow_policy_once_and_new_batch_reloads(monkeypatch):
    import content_workflow
    original = content_workflow.load_bindings
    calls = []
    def recorded(root=None):
        calls.append(root)
        return original(root)
    monkeypatch.setattr(content_workflow, 'load_bindings', recorded)
    model, spec = case()
    report = evaluate(model, spec)
    prefix = canonical_hash(model)
    engine = ContentSpec(ROOT)
    check('access-request-to-review:1', model, report, ROOT, resolver=engine)
    check('access-request-to-review:2', model, report, ROOT, resolver=engine)
    assert len(calls) == 1
    check('access-request-to-review:1', model, report, ROOT, resolver=ContentSpec(ROOT))
    assert len(calls) == 2
    assert canonical_hash(model) == prefix


def test_host_resolver_cannot_select_another_runtime_root(tmp_path):
    model, spec = case()
    with pytest.raises(ValueError, match='RESOLVER_ROOT_MISMATCH'):
        check('access-request-to-review:1', model, evaluate(model, spec), tmp_path,
              resolver=ContentSpec(ROOT))


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


def _selected_handoff_fixture(row, model):
    payload = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    return row['variant_bindings'][payload['selected_path']]


def _variant_case(handoff_id, path_id, contract_id=None):
    engine = ContentSpec(ROOT)
    catalog = load_bindings(ROOT)
    row = next(row for row in catalog['bindings'] if row['handoff_id'] == handoff_id)
    cid = contract_id or row['variant_bindings'][path_id]['contract_ids'][0]
    manifest = json.loads((ROOT/'.ai/runtime/evals/content_quality/manifest.json').read_text())
    reference = next(reference for path in [*manifest['cases'], *manifest['enterprise_cases']]
                     if (reference := json.loads((ROOT/'.ai/runtime'/path).read_text()))['contract_id'] == cid
                     and not reference.get('evaluation_selection', {}).get('overlays'))
    model, spec = prepare_case(reference, engine)
    model = _current_workflow_fixture(model, spec)
    model = _handoff_content_fixture(row, model, path_id)
    return row, model, spec, engine


def _reviewed_variant_result(row, model, spec, engine, authority_factory=None, *,
                             producer_proof=None, receiver_selection=None, receiver_role=None):
    model, review, dispatcher, registry = _host_reviewed_workflow(model, spec)
    if producer_proof is not None:
        registry['producer-token']['workflow_producer'] = producer_proof
    report = evaluate(model, spec, reviewer=review, trusted_executions=dispatcher)
    selected = _selected_handoff_fixture(row, model)
    payload = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    bound = {'handoff_id': row['handoff_id'], 'semantic_hash': canonical_hash(model),
        'report_hash': report['report_hash'], 'catalog_hash': load_bindings(ROOT)['catalog_hash'],
        'criterion': selected['acceptance_criterion'], 'receiving_role': selected['receiving_role'],
        'path_id': payload['selected_path'], 'handoff_content_hash': canonical_hash(selected['handoff_content_contract'])}
    if receiver_selection is not None:
        bound['producer_selection'] = receiver_selection
        dispatcher.receiving_specialties = lambda token: [receiver_role or selected['receiving_role']]
    subject = {**bound,
        'verdict': 'PASS', 'evidence': 'Exact synthetic mechanism, invariant, input and scope evidence reviewed.',
        'unit_reviews': [{'unit_id': unit['id'], 'verdict': 'PASS',
                          'rationale': 'Synthetic result satisfies the selected exact mechanism and invariant.',
                          'evidence': 'Fictional versioned source and context; no real execution or approval claimed.'}
                         for unit in selected['handoff_content_contract']['units']],
        'context_manifest': {'history_policy': 'fresh'}}
    pid = 103
    principal = 'uid:999:worker:103:execution:synthetic-receiver'
    registry['receiver-token'] = {'dispatch_id': 'synthetic-receiver', 'principal': principal,
        'worker_execution': {'pid': pid, 'uid': 999, 'execution_id': 'synthetic-receiver', 'readonly_inputs': True, 'fresh_namespace': True},
        'subject_digest': canonical_hash(subject), 'snapshot_digest': canonical_hash(model),
        'context_digest': canonical_hash(subject['context_manifest']), 'reviewer': True, 'exit_code': 0}
    subject['attestation'] = 'receiver-token'
    result = check(row['handoff_id'], model, report, ROOT, acceptance=subject,
                   trusted_executions=dispatcher, receiving_assignments={principal: [selected['receiving_role']]}, resolver=engine,
                   authority=authority_factory(bound) if authority_factory else None)
    return result, report


@pytest.mark.parametrize('case,change,expected', [
    ('saas', 'matching', None),
    ('saas', 'missing', 'WORKFLOW_PRODUCER_SELECTION_MISMATCH'),
    ('saas', 'path', 'WORKFLOW_PRODUCER_SELECTION_MISMATCH'),
    ('saas', 'version', 'WORKFLOW_PRODUCER_SELECTION_MISMATCH'),
    ('saas', 'receiver', 'RECEIVER_SUBJECT_MISMATCH'),
    ('saas', 'receiver-role', 'WORKFLOW_RECEIVER_SELECTION_MISMATCH'),
    ('java', 'matching', None),
    ('java', 'receiver-role', 'WORKFLOW_RECEIVER_SELECTION_MISMATCH'),
])
def test_compatible_handoff_requires_exact_producer_choice_and_receiver_subject(case, change, expected, monkeypatch):
    if case == 'java':
        handoff, path = 'vulnerability-to-remediation:6', 'planned/application-dependency'
        slug = 'java-software-engineering-specialist'
    else:
        handoff, path = 'new-service-onboarding:1', 'saas-cots'
        slug = 'fixture-specialist'
    row, model, spec, engine = _variant_case(handoff, path)
    catalog = load_bindings(ROOT)
    staged_row = next(item for item in catalog['bindings'] if item['handoff_id'] == row['handoff_id'])
    effective = staged_row['variant_bindings'][path]
    contract = {'id': model['contract_id'], 'version': '3.0.0'}
    effective['workflow_role_requirement'] = {
        'mode': 'compatible-specialization', 'contract': contract,
        'requirement_hash': canonical_hash({'fixture': 'reviewed-exact-output'}),
    }
    catalog['catalog_hash'] = canonical_hash({key: value for key, value in catalog.items() if key != 'catalog_hash'})
    engine._workflow_catalog = catalog
    monkeypatch.setattr(sys.modules[__name__], 'load_bindings', lambda root: catalog)
    mapping = canonical_hash({'fixture': 'reviewed-product-mapping'})
    producer = {
        'slug': slug, 'selection_ref': {'fixture': 'exact-choice'}, 'scope_ref': {'fixture': 'product-scope'},
        'binding': {
            'mode': 'compatible-specialization', 'endpoint': 'producer',
            'workflow_catalogue': catalog['catalog_hash'], 'handoff': row['handoff_id'],
            'path': path, 'bound_role': effective['producer_role'],
            'handoff_contract_hash': canonical_hash(effective['handoff_content_contract']),
            'contract': dict(contract), 'requirement_hash': effective['workflow_role_requirement']['requirement_hash'],
            'mapping_hashes': {slug: mapping},
        },
    }
    receiver = {key: producer[key] for key in ('slug', 'selection_ref', 'scope_ref')}
    receiver['mapping_hash'] = mapping
    if change == 'missing':
        producer = None
    elif change == 'path':
        producer['binding']['path'] = 'other-path'
    elif change == 'version':
        producer['binding']['contract']['version'] = '2.0.0'
    elif change == 'receiver':
        receiver['selection_ref'] = {'fixture': 'previous-choice'}
    result, _ = _reviewed_variant_result(staged_row, model, spec, engine,
                                         producer_proof=producer, receiver_selection=receiver,
                                         receiver_role='different-reviewer' if change == 'receiver-role' else None)
    if expected is None:
        assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
        assert result['producer_selection'] == receiver
    else:
        assert result['status'] == 'ACCEPTANCE_PENDING'
        assert expected in result['findings']


@pytest.mark.parametrize('stage', [1, 2, 3, 4, 5, 6, 7])
def test_saas_onboarding_uses_real_service_evidence_without_iac_images_or_pipeline(stage):
    row, model, spec, engine = _variant_case('new-service-onboarding:' + str(stage), 'saas-cots')
    result, report = _reviewed_variant_result(row, model, spec, engine)
    assert report['gate_verdict'] == 'CONTENT_PASS', report['findings']
    assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
    selected = _selected_handoff_fixture(row, model)
    fields = {field for unit in selected['handoff_content_contract']['units'] for field in unit['required_fields']}
    assert not {'state_locking', 'clean_apply_evidence', 'image_digests', 'base_lineage', 'sbom'} & fields


@pytest.mark.parametrize('stage', [2, 3])
def test_cloud_native_cannot_substitute_saas_evidence_for_actual_iac_or_images(stage):
    row, model, spec, engine = _variant_case('new-service-onboarding:' + str(stage), 'cloud-native')
    model = _handoff_content_fixture(row, model, 'saas-cots')
    context = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context.update(variant='cloud-native', mechanism_variant='cloud-native', selected_path='cloud-native')
    for unit in row['handoff_content_contract']['units']:
        if unit['semantic_field'] != 'workflow_context':
            model['semantic_units'].pop(unit['semantic_field'], None)
    result, report = _reviewed_variant_result(row, model, spec, engine)
    assert report['gate_verdict'] == 'CONTENT_PASS', report['findings']
    assert 'HANDOFF_CONTENT_MISSING_OR_INVALID' in result['findings']
    assert result['status'] == 'ACCEPTANCE_PENDING'


def test_nonpersonal_data_path_requires_classification_not_a_fabricated_dpia():
    row, model, spec, engine = _variant_case('data-product-delivery:2', 'nonpersonal')
    model['context']['processes_personal_data'] = False
    spec = engine.resolve(model['contract_id'], model['context'])
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    result, report = _reviewed_variant_result(row, model, spec, engine)
    assert report['gate_verdict'] == 'CONTENT_PASS', report['findings']
    assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
    fields = {field for unit in _selected_handoff_fixture(row, model)['handoff_content_contract']['units'] for field in unit['required_fields']}
    assert 'classification_evidence' in fields
    assert not {'impact_assessment', 'lawful_basis'} & fields


def test_approval_variant_without_actual_change_mechanism_stays_pending():
    row, model, spec, engine = _variant_case('production-change:2', 'normal/configuration')
    context = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context.pop('mechanism_variant')
    result, _ = _reviewed_variant_result(row, model, spec, engine)
    assert 'WORKFLOW_PATH_UNRESOLVED' in result['findings']
    assert result['status'] == 'ACCEPTANCE_PENDING'


@pytest.mark.parametrize('handoff_id,path_id,field', [
    ('new-service-onboarding:6', 'data-ai/saas-cots', 'handoff_data_model_validation'),
    ('new-service-onboarding:10', 'critical-regulated/saas-cots', 'handoff_critical_service_handover'),
])
def test_overlay_selection_keeps_its_actual_validation_and_readiness_obligations(handoff_id, path_id, field):
    row, model, spec, engine = _variant_case(handoff_id, path_id)
    assert field in model['semantic_units']
    model['semantic_units'].pop(field)
    result, _ = _reviewed_variant_result(row, model, spec, engine)
    assert 'HANDOFF_CONTENT_MISSING_OR_INVALID' in result['findings']
    assert result['status'] == 'ACCEPTANCE_PENDING'


def test_regulatory_nonapplicability_closes_at_actual_decision_without_control_facts(tmp_path, monkeypatch):
    row, model, spec, engine = _variant_case('regulatory-change-to-assurance:2', 'not-applicable')
    model['context']['regulatory_requirement'] = False
    spec = engine.resolve(model['contract_id'], model['context'])
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    model['semantic_units']['workflow_context']['route'] = 'exit'
    result, report = _reviewed_variant_result(row, model, spec, engine,
        authority_factory=lambda bound: signed_governed_acceptance(bound, tmp_path, monkeypatch)[0])
    assert report['gate_verdict'] == 'CONTENT_PASS', report['findings']
    assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
    assert result['next_step'] is None
    assert result['disposition'] == 'exit'
    assert not any('implemented_control' in name for name in model['semantic_units'])
    assert not result['production_release_authorized']


def test_regulatory_excluded_scope_cannot_continue_to_control_implementation():
    row, model, spec, engine = _variant_case('regulatory-change-to-assurance:8', 'applicable')
    context = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context.update(variant='not-applicable', mechanism_variant='not-applicable', selected_path='not-applicable')
    model['context']['regulatory_requirement'] = False
    spec = engine.resolve(model['contract_id'], model['context'])
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    result = check(row['handoff_id'], model, evaluate(model, spec), ROOT, resolver=engine)
    assert 'WORKFLOW_STAGE_OUTSIDE_SELECTED_PATH' in result['findings']
    assert result['status'] == 'ACCEPTANCE_PENDING'
    assert result['next_step'] is None


def _handoff_content_fixture(row, model, path_id=None):
    facts = {
        'individual_access_decision': {
            'subject': 'Fictional analyst identity SYN-ANALYST-1',
            'entitlement': 'Read synthetic demand records',
            'purpose': 'Perform the bounded local demand-qualification exercise',
            'decision': 'Grant synthetic read access only',
            'authority': 'Fictional accountable data owner',
            'validity': 'Disposable test run; revoke when the exercise ends',
            'policy_ref': 'Synthetic use/access policy revision 1'},
        'repository_revision': {
            'repository_id': 'synthetic-ea-repository', 'revision': 'synthetic-revision-2',
            'source_revision': 'synthetic-model-1',
            'identity_preservation': 'Existing fictional element identities retained',
            'validation_evidence': 'Fictional validation transcript for revision 2'},
        'interchange_manifest': {
            'repository_revision': 'synthetic-revision-2',
            'files': ['synthetic-model.xml'],
            'format_profile': 'Explicit synthetic interchange fixture profile',
            'loss_disposition': 'No tool compatibility claim; synthetic comparison only'},
    }
    profile = load_bindings(ROOT)['profiles'][row['workflow_id']]
    candidates = [path for path in profile['paths'] if row['step'] in path['steps']]
    if path_id is not None:
        path = next(path for path in candidates if path['id'] == path_id)
    else:
        compatible = [path for path in candidates
                      if not row['variant_bindings'][path['id']]['contract_ids']
                      or model['contract_id'] in row['variant_bindings'][path['id']]['contract_ids']]
        paths = compatible or candidates
        path = next(path for path in paths if not next(variant for variant in profile['variants'] if variant['id'] == path['variant']).get('when')
                    or model.get('context', {}).get(next(variant for variant in profile['variants'] if variant['id'] == path['variant'])['when']['field'])
                    == next(variant for variant in profile['variants'] if variant['id'] == path['variant'])['when']['value'])
    selected = row['variant_bindings'][path['id']]
    for unit in selected['handoff_content_contract']['units']:
        if unit['semantic_field'] not in facts:
            facts[unit['semantic_field']] = {field: 'Synthetic ' + field.replace('_', ' ') + ' for ' + row['handover']
                                           for field in unit['required_fields']}
        model['semantic_units'][unit['semantic_field']] = {
            **copy.deepcopy(facts[unit['semantic_field']]),
            'knowledge_status': 'synthetic-assumption', 'evidence_refs': ['SYN-01']}
        source = next(item for item in model['evidence'] if item['id'] == 'SYN-01')
        source['payload'] = {'classification': 'synthetic', 'records': copy.deepcopy(facts)}
    model['evidence'] = [item for item in model['evidence'] if item['id'] != 'SYN-CONTEXT']
    model['evidence'].append({
        'id': 'SYN-CONTEXT', 'version': '1', 'payload': {
            'workflow_id': row['workflow_id'], 'profile_hash': row['handoff_content_contract']['workflow_profile_hash'],
            'context_id': 'synthetic-context-' + row['workflow_id'], 'context_version': '1',
            'variant': path['variant'], 'mechanism_variant': path['mechanism'], 'selected_path': path['id'],
            'entry_inputs': {name: 'Synthetic reviewed input: ' + name for name in profile['entry_inputs']}}})
    model['semantic_units']['workflow_context'].update({
        'context_ref': 'SYN-CONTEXT', 'route': 'continue',
        'input_refs': ['SYN-01'], 'route_evidence': 'Synthetic current criterion and reference review.'})
    return model


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
        if row['handoff_id'] in {'idea-to-production:14', 'production-change:9'}:
            # The linked evidence regressions cover these with their exact inputs.
            continue
        contract=row['contract_ids'][0] if row['contract_ids'] else fallback
        model,spec=prepare_case(references[contract],engine)
        model = _current_workflow_fixture(model, spec)
        model = _handoff_content_fixture(row, model)
        model,review,dispatcher,registry=_host_reviewed_workflow(model,spec)
        report=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
        assert report['gate_verdict']=='CONTENT_PASS',row['handoff_id']
        selected = _selected_handoff_fixture(row, model)
        context_payload = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
        bound={'handoff_id':row['handoff_id'],'semantic_hash':canonical_hash(model),'report_hash':report['report_hash'],
            'catalog_hash':catalog['catalog_hash'],'criterion':selected['acceptance_criterion'],'receiving_role':selected['receiving_role'],
            'path_id': context_payload['selected_path'], 'handoff_content_hash': canonical_hash(selected['handoff_content_contract'])}
        human=selected['producer_role']=='engagement:named-authority' or selected['receiving_role'] in ('engagement:named-authority','engagement:named-acceptance-authority')
        kwargs={'trusted_executions':dispatcher,'resolver':engine}
        if human:
            authority,host=signed_governed_acceptance(bound,tmp_path,monkeypatch)
            kwargs['authority']=authority
            result = check(row['handoff_id'], model, report, ROOT, **kwargs)
            assert result['status'] == 'ACCEPTANCE_VERIFIED', (row['handoff_id'], result['findings'])
            kwargs['authority']=None
            assert 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in check(row['handoff_id'],model,report,ROOT,**kwargs)['findings']
        else:
            subject={**bound,'verdict':'PASS','evidence':'Reviewed the exact scoped workflow gate and evidence in the canonical source.',
                'context_manifest':{'history_policy':'fresh'}}
            if 'handoff_content_contract' in row:
                subject['unit_reviews'] = [{'unit_id': unit['id'], 'verdict': 'PASS',
                    'rationale': 'The exact fictional decision/revision content matches the registered handoff obligation.',
                    'evidence': 'Reviewed the populated synthetic semantic record and its SYN-01 evidence; no actual access or tool qualification.'}
                    for unit in selected['handoff_content_contract']['units']]
            execution='synthetic-receiver';pid=103
            principal=f'uid:999:worker:{pid}:execution:{execution}'
            payload={'dispatch_id':execution,'principal':principal,'worker_execution':{'pid':pid,'uid':999,'execution_id':execution,'readonly_inputs':True,'fresh_namespace':True},
                'subject_digest':canonical_hash(subject),'snapshot_digest':canonical_hash(model),'context_digest':canonical_hash(subject['context_manifest']),
                'reviewer':True,'exit_code':0}
            registry['receiver-token'] = payload
            subject['attestation'] = 'receiver-token'
            kwargs.update(acceptance=subject,receiving_assignments={principal:[selected['receiving_role']]})
            result = check(row['handoff_id'], model, report, ROOT, **kwargs)
            assert result['status'] == 'ACCEPTANCE_VERIFIED', (row['handoff_id'], result['findings'])
            kwargs['receiving_assignments']={}
            assert 'RECEIVER_ROLE_UNASSIGNED' in check(row['handoff_id'],model,report,ROOT,**kwargs)['findings']


@pytest.mark.parametrize(('case', 'mismatch'), [
    ('mobile', None), ('mobile', 'candidate_build_ref'), ('mobile', 'device_scope'),
    ('mobile', 'automation_evidence_ref'), ('abap', None), ('abap', 'tenant_ref'),
    ('abap', 'transport_scope'), ('abap', 'unreleased_api'),
])
def test_workflow_evidence_chain_binds_the_exact_reviewed_input(case, mismatch):
    if case == 'mobile':
        workflow, path = 'idea-to-production', 'mobile-delivery'
        steps = ((7, 'mobile_build', None, None),
                 (14, 'mobile_automation_evidence', 'build_evidence_ref', None),
                 (8, 'mobile_test_verdict', 'automation_evidence_ref', 'test-analyst:4'))
        identity = {'candidate_build_ref': 'immutable-build-a', 'sdk_scope': 'SDK fixture',
                    'device_scope': 'Device fixture'}
    else:
        workflow, path = 'production-change', 'normal/abap-cloud'
        steps = ((4, 'abap_cloud_release_provenance', None, None),
                 (9, 'abap_cloud_extension_evidence', 'release_manifest_ref', None),
                 (5, 'abap_cloud_change_record', 'extension_evidence_ref', None))
        identity = {'candidate_ref': 'immutable-extension-a', 'tenant_ref': 'Tenant fixture',
                    'product_release': 'Release fixture', 'transport_scope': 'Transport fixture'}
    engine = ContentSpec(ROOT)
    catalog = load_bindings(ROOT)
    trusted = {}
    roles = {}
    links = {}
    predecessor = None
    prior = None

    def dispatcher(token):
        return copy.deepcopy(trusted.get(token))

    dispatcher.predecessor_input = lambda current, previous: links.get((current, previous))
    for index, (step, name, field, contract_id) in enumerate(steps):
        handoff = f'{workflow}:{step}'
        row, model, spec, _ = _variant_case(handoff, path, contract_id)
        selected = row['variant_bindings'][path]
        facts = model['semantic_units']['handoff_' + name]
        facts.update(identity)
        producer_token = f'producer-{step}'
        receiver_token = f'receiver-{step}'
        if prior is not None:
            reference = {'logical_id': prior['handoff_id'], 'version_id': 'admitted-version'}
            links[producer_token, predecessor['model']['producer']['attestation']] = reference
            facts[field] = reference
        api_failure = name == 'abap_cloud_extension_evidence' and mismatch == 'unreleased_api'
        identity_failure = index == 2 and mismatch is not None and mismatch != 'unreleased_api'
        if name == 'abap_cloud_extension_evidence':
            facts['released_apis'] = ['SYN-ABAP-API']
            model['evidence'].append({'id': 'SYN-ABAP-API', 'version': '1', 'payload': {
                'api_id': 'Synthetic API', 'release_status': 'unreleased' if api_failure else 'released',
                'tenant_ref': identity['tenant_ref'], 'product_release': identity['product_release']}})
        if identity_failure:
            facts[mismatch] = 'different fixture input'
        model, review, _, local = _host_reviewed_workflow(model, spec)
        model['producer']['attestation'] = producer_token
        review['semantic_hash'] = canonical_hash(model)
        review_token = f'review-{step}'
        review['attestation'] = review_token
        trusted[producer_token] = local['producer-token']
        trusted[review_token] = {
            **local['review-token'], 'snapshot_digest': canonical_hash(model),
            'subject_digest': canonical_hash({key: value for key, value in review.items() if key != 'attestation'}),
        }
        report = evaluate(model, spec, reviewer=review, trusted_executions=dispatcher)
        subject = {'handoff_id': handoff, 'path_id': path, 'semantic_hash': canonical_hash(model),
                   'report_hash': report['report_hash'], 'catalog_hash': catalog['catalog_hash'],
                   'criterion': selected['acceptance_criterion'], 'receiving_role': selected['receiving_role'],
                   'handoff_content_hash': canonical_hash(selected['handoff_content_contract']),
                   'verdict': 'PASS', 'evidence': 'Reviewed exact synthetic mobile evidence.',
                   'context_manifest': {'history_policy': 'fresh'},
                   'unit_reviews': [{'unit_id': unit['id'], 'verdict': 'PASS',
                                     'rationale': 'The exact synthetic obligation was reviewed.',
                                     'evidence': 'Reviewed the synthetic artifact and its bound input.'}
                                    for unit in selected['handoff_content_contract']['units']]}
        if prior is not None and not identity_failure:
            subject['predecessor'] = {'artifact_ref': reference, 'result_hash': prior['result_hash']}
        principal = f'fixture-receiver-{step}'
        roles[principal] = [selected['receiving_role']]
        trusted[receiver_token] = {'principal': principal, 'reviewer': True,
                                   'subject_digest': canonical_hash(subject), 'snapshot_digest': canonical_hash(model),
                                   'context_digest': canonical_hash(subject['context_manifest'])}
        subject['attestation'] = receiver_token
        result = check(handoff, model, report, ROOT, acceptance=subject, trusted_executions=dispatcher,
                       receiving_assignments=roles, resolver=engine, predecessor=predecessor)
        if api_failure:
            assert 'WORKFLOW_ABAP_RELEASED_API_EVIDENCE_REQUIRED' in result['findings']
            assert result['status'] == 'ACCEPTANCE_PENDING'
            break
        if identity_failure:
            assert 'WORKFLOW_EVIDENCE_PREDECESSOR_UNVERIFIED' in result['findings']
            assert result['status'] == 'ACCEPTANCE_PENDING'
        else:
            assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
            if index == 1 and mismatch is None:
                missing_receiver = check(handoff, model, report, ROOT, acceptance=subject,
                    trusted_executions=dispatcher, receiving_assignments={}, resolver=engine, predecessor=predecessor)
                assert 'RECEIVER_ROLE_UNASSIGNED' in missing_receiver['findings']
        predecessor = {'model': model, 'report': report, 'acceptance': subject, 'predecessor': predecessor}
        if predecessor['predecessor'] is None:
            del predecessor['predecessor']
        prior = result


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


@pytest.mark.parametrize('mutation', [
    None, 'functional-receiver', 'partial', 'duplicate', 'assignment', 'invocation', 'context', 'receiver',
])
def test_all_required_output_set_binds_one_independent_receipt(mutation):
    import content_workflow
    from workflow_specialist_profiles import ALL_REQUIRED_PROTOCOL

    contracts = {'protocol': ALL_REQUIRED_PROTOCOL, 'contracts': [
        {'id': f'software-engineer:{number}', 'version': '3.0.0', 'digest': str(number) * 64}
        for number in (1, 4)]}
    receiver = 'engagement:change-impact-owner' if mutation == 'functional-receiver' else 'configuration-manager'
    common = {'handoff_id': 'production-change:1', 'catalog_hash': 'catalogue',
              'criterion': 'Exact change evidence', 'receiving_role': receiver,
              'path_id': 'normal/application', 'handoff_content_hash': 'handoff',
              'producer_selection': {'selection_ref': 'selection'}, 'contract_set': contracts,
              'governing_subject': {'context': 'context-a', 'source_revision': 'candidate-a'},
              'findings': [], 'human_step': False, 'next_step': 2}
    members = []
    for ref in contracts['contracts']:
        identity = ref['id']
        members.append({**common, 'contract_id': identity, 'semantic_hash': identity, 'report_hash': identity,
                        'producer': {'principal': 'author', 'invocation': 'native-invocation', 'workflow_output': {
                            'assignment': 'exact-author-assignment',
                            'material_digest': identity,
                            'artifact': {'ref': {'version_id': 'same-product'}, 'use_scope': 'engagement'}}}})
    registry = {}

    def verifier(token):
        return registry.get(token)

    verifier.receiving_specialties = lambda token: ['configuration-manager'] if token == 'receipt' else []
    assignments = {'independent': [receiver]}
    prepared = content_workflow._accept_output_set(members, None, verifier, assignments)
    subject = {key: value for key, value in prepared.items()
               if key not in {'findings', 'receiver_principal', 'status', 'result_hash'}}
    subject.update(verdict='PASS', evidence='Reviewed both exact fixture outputs.',
                   context_manifest={'version': 'review'})
    registry['receipt'] = {'principal': 'independent', 'reviewer': True,
                          'subject_digest': canonical_hash(subject), 'snapshot_digest': subject['semantic_hash'],
                          'context_digest': canonical_hash(subject['context_manifest'])}
    subject['attestation'] = 'receipt'
    if mutation == 'partial':
        members.pop()
    elif mutation == 'duplicate':
        members[1]['producer'] = members[0]['producer']
    elif mutation == 'assignment':
        members[1]['producer']['workflow_output']['assignment'] = 'different-assignment'
    elif mutation == 'invocation':
        members[1]['producer']['invocation'] = 'different-invocation'
    elif mutation == 'context':
        members[1]['governing_subject'] = {'context': 'context-a', 'source_revision': 'candidate-b'}
    elif mutation == 'receiver':
        assignments = {}
    result = content_workflow._accept_output_set(members, subject, verifier, assignments)
    if mutation in (None, 'functional-receiver'):
        assert result['status'] == 'ACCEPTANCE_VERIFIED', result['findings']
        assert len(result['outputs']) == 2
    else:
        assert result['status'] == 'ACCEPTANCE_PENDING'
        assert ('WORKFLOW_RECEIVER_SELECTION_MISMATCH' if mutation == 'receiver'
                else 'WORKFLOW_OUTPUT_SET_MISMATCH') in result['findings']
    assert not result['production_release_authorized']


@pytest.mark.parametrize('mutation',['selection','contracts','handoff-content'])
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
    elif mutation == 'contracts':
        data['bindings'][0]['contract_ids']=['chief-information-officer:1']
    else:
        data['bindings'][0]['handoff_content_contract'] = {'units': []}
    data['catalog_hash']=canonical_hash({k:v for k,v in data.items() if k!='catalog_hash'})
    (runtime/'workflow-acceptance.json').write_text(json.dumps(data))
    with pytest.raises(ValueError,match='HANDOFF_CONTENT_SCOPE' if mutation == 'handoff-content' else 'CONTRACT_SCOPE'):
        load_bindings(tmp_path)


@pytest.mark.parametrize('specialty, predecessor_case', [
    ('security-assurance-and-measurement-architect', 'missing'),
    ('software-engineer', 'missing'),
    ('security-assurance-and-measurement-architect', 'matching'),
    ('security-assurance-and-measurement-architect', 'foreign'),
    ('security-assurance-and-measurement-architect', 'pending'),
])
def test_staged_siem_terminal_keeps_recorded_role_and_signed_authority(
        tmp_path, monkeypatch, specialty, predecessor_case):
    import content_workflow
    from generate_content_workflows import stage_siem_pilot

    scopes = tmp_path / 'scopes.json'
    facts = [{'edition': 'synthetic', 'version': 'fixture', 'deployment': 'offline'}]
    scopes.write_text(json.dumps({product: facts for product in
        ('splunk-enterprise-security', 'ibm-qradar-siem')}))
    pilot = tmp_path / 'registration.json'
    pilot.write_text(json.dumps(stage_siem_pilot(ROOT, scopes)))
    catalogue = content_workflow.load_bindings(ROOT, pilot=pilot)
    terminal = catalogue['bindings'][-1]
    engine = ContentSpec(ROOT)
    fixture = ROOT / '.ai/runtime/evals/content_quality/enterprise/security-assurance-and-measurement-architect-2-medium.json'
    model, spec = prepare_case(json.loads(fixture.read_bytes()), engine)
    model['semantic_units'].setdefault('workflow_context', {})
    with monkeypatch.context() as scoped:
        scoped.setattr(sys.modules[__name__], 'load_bindings', lambda root: catalogue)
        model = _handoff_content_fixture(terminal, model, 'bounded-validation')
    model['producer'] = {'attestation': 'synthetic-terminal-producer'}

    def verifier(token):
        return {'reviewer': False, 'principal': 'assessor'} if token == 'synthetic-terminal-producer' else None

    verifier.receiving_specialties = lambda token, *, reviewer: [specialty] if not reviewer else []
    predecessor = None
    if predecessor_case != 'missing':
        reference = {'logical_id': 'integration', 'version_id': 'admitted-version'}
        model['semantic_units']['independent_assessment'].update(
            reviewed_artifact_ref=reference, receiving_principal='assessor')
        verifier.predecessor_input = lambda terminal_token, previous_token: (
            reference if predecessor_case != 'foreign' else {**reference, 'version_id': 'foreign'})
        predecessor = {'model': {'producer': {'attestation': 'integration-producer'}},
                       'report': {}, 'acceptance': {}}

    def replay_prior(handoff, *args, **kwargs):
        assert handoff == 'siem-log-source-integration:1'
        status = 'ACCEPTANCE_PENDING' if predecessor_case == 'pending' else 'ACCEPTANCE_VERIFIED'
        return {'status': status, 'next_step': 2, 'path_id': 'bounded-validation',
                'receiver_principal': 'assessor', 'result_hash': 'fixture-bound-result'}

    check_terminal = content_workflow._check
    monkeypatch.setattr(content_workflow, '_check', replay_prior)
    result = check_terminal(terminal['handoff_id'], model, evaluate(model, spec), ROOT,
                            trusted_executions=verifier, resolver=engine, pilot=pilot, predecessor=predecessor)
    assert ('WORKFLOW_TERMINAL_PREDECESSOR_UNVERIFIED' in result['findings']) == (predecessor_case != 'matching')
    if predecessor_case == 'matching':
        assert result['predecessor'] == {'artifact_ref': reference, 'result_hash': 'fixture-bound-result'}
    assert result['status'] == 'ACCEPTANCE_PENDING'
    assert 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in result['findings']
    assert ('WORKFLOW_TERMINAL_PRODUCER_ROLE_MISMATCH' in result['findings']) == (specialty == 'software-engineer')


def test_zero_trust_rehearsal_rejects_failed_readiness_dependency_and_reversal():
    from infrastructure_workflow_evidence import _transition_coverage, _transition_observed

    observations = {
        'readiness': 'PASS',
        'allowed_paths': [{'flow_id': 'office-to-inventory', 'expected': 'allow',
                           'observed': 'allow', 'observation_ref': 'run:1'}],
        'denied_paths': [{'flow_id': 'guest-to-inventory', 'expected': 'deny',
                          'observed': 'deny', 'observation_ref': 'run:2'}],
        'mandatory_dependencies': [{'dependency_id': 'name-resolution',
                                    'status': 'verified', 'observation_ref': 'run:3'}],
        'reversal': {'status': 'restored', 'observation_ref': 'run:4',
                     'elapsed_seconds': 38, 'limit_seconds': 60},
    }
    observations['verification_scope'] = {
        'allowed_flow_ids': ['office-to-inventory'], 'denied_flow_ids': ['guest-to-inventory'],
        'dependency_ids': ['name-resolution'], 'reversal_limit_seconds': 60,
    }
    records = [*observations['allowed_paths'], *observations['denied_paths'],
               *observations['mandatory_dependencies'], observations['reversal']]
    observed_model = {'evidence': [_synthetic_observation(record) for record in records]}
    assert _transition_observed(observations)
    assert _transition_coverage(observations, observed_model)
    changed_scope = {**observations['verification_scope'], 'dependency_ids': ['name-resolution', 'time-sync']}
    assert not _transition_coverage({**observations, 'verification_scope': changed_scope}, observed_model)
    assert not _transition_coverage(observations, {'evidence': observed_model['evidence'][1:]})
    assert not _transition_observed({**observations, 'readiness': 'FAIL'})
    assert not _transition_observed({**observations, 'mandatory_dependencies': [
        {'dependency_id': 'name-resolution', 'status': 'unknown', 'observation_ref': 'run:3'}]})
    assert not _transition_observed({**observations, 'reversal': {
        **observations['reversal'], 'elapsed_seconds': 61}})


def _synthetic_observation(record):
    return {'id': record['observation_ref'], 'version': '1',
            'payload': {key: value for key, value in record.items() if key != 'observation_ref'}}


@pytest.mark.parametrize('provider,integration,store,action', [
    ('aws', 'codeconnections', 'ecr', 'ecs-rolling'),
    ('azure', 'azure-repos', 'acr', 'container-apps-revisions'),
    ('google-cloud', 'secure-source-manager', 'artifact-registry', 'cloud-run'),
])
def test_cloud_delivery_chain_binds_previous_artifact_and_target(provider, integration, store, action):
    from infrastructure_workflow_definitions import EVIDENCE
    from infrastructure_workflow_evidence import verify

    workflow = 'production-change'
    path = {'id': 'normal/' + provider, 'mechanism': provider, 'steps': list(range(1, 9))}
    models = {}
    hints = {'target_id': 'service-A', 'environment': 'stage', 'provider': provider,
             'artifact_digest': 'sha256:' + '1' * 64, 'source_revision': 'commit-1',
             'release_id': 'release-1', 'rollback_target': 'previous-revision'}
    identity = {'target_id': hints['target_id'], 'environment': hints['environment'],
                'short_lived': True, 'principal': 'pipeline-stage'}
    hints.update(integration=integration, region='synthetic-region', artifact_store=store,
                 deployment_action=action, credential_scope=identity,
                 deployment_identity=identity, independent_verdict='PASS',
                 applicability_ref='APP')
    hints['rollout_observations'] = {'target_id': hints['target_id'], 'artifact_digest': hints['artifact_digest'],
                                    'status': 'healthy', 'observation_ref': 'synthetic-rollout'}
    hints['rollback_record'] = {'target': hints['rollback_target'], 'status': 'not-needed',
                                'observation_ref': 'synthetic-recovery'}
    application = {key: hints[key] for key in (
        'provider', 'target_id', 'region', 'integration', 'deployment_action')}
    application.update(supported=True, source='Synthetic provider evidence')
    context = {'id': 'CTX', 'version': '1', 'payload': {'workflow_id': workflow,
                'mechanism_variant': provider}}

    class Trust:
        def verify(self, token):
            return {'snapshot_digest': canonical_hash(models[token])}

        def predecessor_input(self, current, previous):
            assert current == previous + 1
            return {'engagement': 'synthetic', 'scope': 'stage', 'logical_id': f'step-{previous}',
                    'version_id': str(previous) * 64}

    host = Trust()
    predecessor = None
    for number in path['steps']:
        field, _, link = EVIDENCE[workflow, path['id'], number]
        facts = dict(hints)
        if link:
            facts[link] = host.predecessor_input(number, number - 1)
        snapshot = {'producer': {}, 'semantic_units': {
            field: facts, 'workflow_context': {'context_ref': 'CTX'}},
            'evidence': [context, {'id': 'APP', 'version': '1', 'payload': application},
                         _synthetic_observation(hints['rollout_observations']),
                         _synthetic_observation(hints['rollback_record'])]}
        model = {**snapshot, 'producer': {'attestation': number}}
        models[number] = snapshot
        findings, actual = verify(workflow, path, number, model, number, predecessor, host)
        assert findings == []
        assert actual == facts.get(link)
        if number == 1:
            unsupported = {**model, 'evidence': [context, {'id': 'APP', 'version': '1',
                           'payload': {**application, 'supported': False}}]}
            assert verify(workflow, path, number, unsupported, number, predecessor, host)[0] == [
                'INFRASTRUCTURE_APPLICABILITY_UNVERIFIED']
        if number == 6:
            for key, wrong in [('artifact_digest', 'sha256:' + '2' * 64), ('environment', 'production')]:
                changed = copy.deepcopy(model)
                changed['semantic_units'][field][key] = wrong
                if key == 'artifact_digest':
                    changed['semantic_units'][field]['rollout_observations'][key] = wrong
                    changed['evidence'][-2]['payload'][key] = wrong
                assert verify(workflow, path, number, changed, number, predecessor, host)[0] == [
                    'INFRASTRUCTURE_SUBJECT_MISMATCH']
            assert verify(workflow, path, number, model, number, None, host)[0] == [
                'INFRASTRUCTURE_PREDECESSOR_UNVERIFIED']
        predecessor = {'model': model}


def test_zero_trust_transition_rejects_changed_baseline_and_scope():
    from infrastructure_workflow_evidence import verify

    workflow = 'design-to-operational-readiness'
    path = {'id': 'zero-trust-migration', 'mechanism': 'zero-trust-migration',
            'steps': list(range(1, 8))}
    scope = {'allowed_flow_ids': ['business'], 'denied_flow_ids': ['guest'],
             'dependency_ids': ['dns'], 'reversal_limit_seconds': 60}
    baseline = {'engagement': 'synthetic', 'scope': 'default', 'logical_id': 'baseline',
                'version_id': 'a' * 64}
    design = {**baseline, 'logical_id': 'design', 'version_id': 'b' * 64}
    context = {'id': 'context', 'version': '1', 'payload': {'workflow_id': workflow}}
    common = {'estate_id': 'network-1', 'baseline_ref': baseline, 'verification_scope': scope}
    earlier = {'producer': {}, 'evidence': [context], 'semantic_units': {
        'workflow_context': {'context_ref': 'context'}, 'handoff_zero_trust_target': common}}
    predecessor = {'model': {**earlier, 'producer': {'attestation': 'prior'}}}
    candidate = {'evidence': [context], 'semantic_units': {'workflow_context': {'context_ref': 'context'},
                 'handoff_transition_candidate': {**common, 'design_ref': design}}}

    class Trust:
        def verify(self, token):
            assert token == 'prior'
            return {'snapshot_digest': canonical_hash(earlier)}

        def predecessor_input(self, current, previous):
            assert (current, previous) == ('current', 'prior')
            return design

    host = Trust()
    assert verify(workflow, path, 3, candidate, 'current', predecessor, host) == ([], design)
    for field, value in [('baseline_ref', {**baseline, 'version_id': 'c' * 64}),
                         ('verification_scope', {**scope, 'reversal_limit_seconds': 90})]:
        altered = copy.deepcopy(candidate)
        altered['semantic_units']['handoff_transition_candidate'][field] = value
        assert verify(workflow, path, 3, altered, 'current', predecessor, host) == (
            ['INFRASTRUCTURE_SUBJECT_MISMATCH'], None)


@pytest.mark.parametrize('provider', ['aws', 'azure', 'google-cloud'])
def test_cloud_rollout_rechecks_exact_signed_prior_approval(tmp_path, monkeypatch, provider):
    from content_workflow import _infrastructure_receiving_subject

    workflow, path_id = 'production-change', f'normal/{provider}'
    row, model, spec, engine = _variant_case(workflow + ':5', path_id)
    model['semantic_units']['handoff_delivery_authority'].update(
        provider=provider, artifact_digest='sha256:' + '1' * 64)
    selected = row['variant_bindings'][path_id]
    catalogue = load_bindings(ROOT)
    path = next(path for path in catalogue['profiles'][workflow]['paths'] if path['id'] == path_id)
    model, reviewer, dispatcher, registry = _host_reviewed_workflow(model, spec)
    report = evaluate(model, spec, reviewer=reviewer, trusted_executions=dispatcher)
    assert report['gate_verdict'] == 'CONTENT_PASS'
    receiver, producer = selected['receiving_role'], selected['producer_role']
    receiving = 'uid:999:worker:103:execution:synthetic-receiver'
    assignments = {receiving: [receiver]}
    current_producer = {'principal': receiving}
    reference = {'engagement': 'synthetic', 'scope': 'default', 'logical_id': 'promotion',
                 'version_id': 'a' * 64}
    bound = {'handoff_id': row['handoff_id'], 'semantic_hash': canonical_hash(model),
             'report_hash': report['report_hash'], 'catalog_hash': catalogue['catalog_hash'],
             'criterion': selected['acceptance_criterion'], 'receiving_role': receiver,
             'path_id': path_id, 'handoff_content_hash': canonical_hash(selected['handoff_content_contract']),
             'infrastructure_input': reference}
    acceptance = {**bound, 'verdict': 'PASS', 'evidence': 'Synthetic exact scoped promotion reviewed.',
                  'context_manifest': {'history_policy': 'fresh'},
                  'unit_reviews': [{'unit_id': unit['id'], 'verdict': 'PASS',
                                    'rationale': 'Synthetic scoped criterion reviewed.',
                                    'evidence': 'Exact synthetic accepted promotion.'}
                                   for unit in selected['handoff_content_contract']['units']]}
    registry['receiver-token'] = {
        'dispatch_id': 'synthetic-receiver', 'principal': receiving, 'reviewer': True, 'exit_code': 0,
        'worker_execution': {'pid': 103, 'uid': 999, 'execution_id': 'synthetic-receiver',
                             'readonly_inputs': True, 'fresh_namespace': True},
        'subject_digest': canonical_hash(acceptance), 'snapshot_digest': bound['semantic_hash'],
        'context_digest': canonical_hash(acceptance['context_manifest']),
    }
    expected_receiver = [receiver]
    dispatcher.receiving_specialties = lambda _token, reviewer=True: expected_receiver if reviewer else [producer]
    predecessor = {'model': model, 'report': report,
                   'acceptance': {**acceptance, 'attestation': 'receiver-token'}}

    def authorized(record, authority=None):
        return _infrastructure_receiving_subject(
            catalogue, workflow, path, 6, record, current_producer, dispatcher, assignments, authority, engine)

    assert not authorized(predecessor)
    authority, _ = signed_governed_acceptance(bound, tmp_path, monkeypatch)
    assert authorized(predecessor, authority)
    changed = copy.deepcopy(predecessor)
    changed['report']['report_hash'] = '0' * 64
    assert not authorized(changed, authority)
    changed = copy.deepcopy(predecessor)
    changed['model']['semantic_units']['handoff_delivery_authority']['environment'] = 'different-environment'
    assert not authorized(changed, authority)
    expected_receiver[:] = ['release-engineer']
    assert not authorized(predecessor, authority)


@pytest.mark.parametrize('defect, finding', [
    ('missing-evidence', 'HANDOFF_CONTENT_MISSING_OR_INVALID'),
    ('wrong-path', 'WORKFLOW_STAGE_OUTSIDE_SELECTED_PATH'),
    ('missing-authority', 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED'),
])
def test_dast_release_authority_rejects_incomplete_or_incompatible_handoff(defect, finding):
    """Reject a release boundary with absent evidence, outside its path or unsigned."""
    row = next(item for item in load_bindings(ROOT)['bindings']
               if item['handoff_id'] == 'dast-control-assurance:7')
    model, spec = case()
    model = _handoff_content_fixture(row, _current_workflow_fixture(model, spec), 'release-evidence')
    if defect == 'missing-evidence':
        del model['semantic_units']['handoff_dast_release_decision']['evidence_ref']
    elif defect == 'wrong-path':
        scope = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
        scope.update(variant='qualification', mechanism_variant='qualification', selected_path='qualification')
    model, review, dispatcher, _ = _host_reviewed_workflow(model, spec)
    report = evaluate(model, spec, reviewer=review, trusted_executions=dispatcher)
    result = check(row['handoff_id'], model, report, ROOT, trusted_executions=dispatcher)
    assert result['status'] == 'ACCEPTANCE_PENDING'
    assert finding in result['findings']


@pytest.mark.parametrize('step, path', [(6, 'release-evidence'), (8, 'continuous-assurance')])
def test_dast_intake_is_required_at_the_first_selected_stage(step, path):
    """Require scoped intake for paths whose first stage has a later number."""
    row, model, spec, _ = _variant_case(f'dast-control-assurance:{step}', path)
    context = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
    context.pop('entry_inputs')
    result = check(row['handoff_id'], model, evaluate(model, spec), ROOT)
    assert 'WORKFLOW_INTAKE_INCOMPLETE' in result['findings']


@pytest.mark.parametrize('defect, finding', [
    ('missing-workstreams', 'HANDOFF_CONTENT_MISSING_OR_INVALID'),
    ('qualification-only', 'WORKFLOW_STAGE_OUTSIDE_SELECTED_PATH'),
])
def test_dast_integration_qualification_requires_workstream_evidence_and_path(defect, finding):
    """Fail closed on an incomplete join or a qualification-only scope."""
    row, model, spec, _ = _variant_case('dast-control-assurance:18', 'integration')
    if defect == 'missing-workstreams':
        del model['semantic_units']['handoff_dast_system_qualification']['workstream_refs']
    else:
        scope = next(item['payload'] for item in model['evidence'] if item['id'] == 'SYN-CONTEXT')
        scope.update(variant='qualification', mechanism_variant='qualification', selected_path='qualification')
    model, review, dispatcher, _ = _host_reviewed_workflow(model, spec)
    report = evaluate(model, spec, reviewer=review, trusted_executions=dispatcher)
    result = check(row['handoff_id'], model, report, ROOT, trusted_executions=dispatcher)
    assert result['status'] == 'ACCEPTANCE_PENDING'
    assert finding in result['findings']
