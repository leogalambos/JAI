# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise deterministic DCS rules and explicit synthetic host trust boundaries."""
import copy
import json
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
from content_spec import ContentSpec, canonical_hash, SpecError
from content_lint import evaluate, verify_report, write_report, main


def sample():
    unit = {'id': 'decision-paper.core', 'semantic_fields': ['core'], 'datatype': 'object',
            'category': 'required_information', 'applicability': True, 'acceptance_predicate': {'op': 'review'}}
    spec = {'schema_version': '1.0.0', 'spec_id': 'kind/decision-paper', 'spec_version': '1.0.0',
            'context': {}, 'context_hash': canonical_hash({}), 'status': 'proposed',
            'calibration_status': 'synthetic-only', 'blueprint': {'semantic_units': [unit], 'budgets': {}}}
    spec['compiled_spec_hash'] = canonical_hash(spec)
    spec.update(artifact_id='role:decision-paper', document_kind='decision-paper')
    model = {'artifact_id': 'case:01', 'contract_id': spec['artifact_id'], 'document_kind': 'decision-paper',
             'context': {}, 'compiled_spec_hash': spec['compiled_spec_hash'],
             'semantic_units': {'core': {'decision': 'Retain the managed platform until recovery evidence is reviewed.', 'knowledge_status': 'assumption'}}}
    return model, spec


def rules(report):
    return {item['rule_id'] for item in report['findings']}


def reviewed(model, spec, same_principal=False, declared_aliases=False):
    # This fake is a host boundary contract test, not live dispatcher qualification.
    registry = {}
    def verifier(token):
        return copy.deepcopy(registry.get(token))
    model = copy.deepcopy(model)
    model['producer'] = {'context_manifest': {'history_policy': 'fresh'}}
    if declared_aliases:
        model['producer']['name'] = 'Producer Alias'
    producer_hash = canonical_hash(model)
    registry['producer-token'] = {'principal': 'host:producer', 'reviewer': False,
        'subject_digest': producer_hash, 'snapshot_digest': producer_hash,
        'context_digest': canonical_hash(model['producer']['context_manifest'])}
    model['producer']['attestation'] = 'producer-token'
    review = {'semantic_hash': canonical_hash(model), 'compiled_spec_hash': spec['compiled_spec_hash'],
              'context_hash': spec['context_hash'], 'context_manifest': {'history_policy': 'fresh'},
              'unit_reviews': [{'unit_id': 'decision-paper.core', 'verdict': 'PASS',
                               'rationale': 'The specific platform decision has a bounded pending condition.',
                               'evidence': 'Reviewed canonical core decision at $.semantic_units.core.'}], 'findings': []}
    if declared_aliases:
        review['name'] = 'Reviewer Alias'
    registry['review-token'] = {'principal': 'host:producer' if same_principal else 'host:reviewer', 'reviewer': True,
        'subject_digest': canonical_hash(review), 'snapshot_digest': canonical_hash(model),
        'context_digest': canonical_hash(review['context_manifest'])}
    review['attestation'] = 'review-token'
    return model, review, verifier, registry


def test_complete_deterministic_material_remains_draft_without_independent_review():
    model, spec = sample()
    report = evaluate(model, spec)
    assert report['deterministic_status'] == 'PASS'
    assert report['gate_verdict'] == 'DRAFT_INCOMPLETE'
    assert report['critical_coverage_percent'] == 100
    assert report['reviewer']['required_units'] == ['decision-paper.core']


@pytest.mark.parametrize('value', [None, '', 'TBD', 'N/A', {'title': 'Only a heading'}, {'decision': 'TODO'}, [], 3, True])
def test_missing_placeholder_headings_and_wrong_types_do_not_satisfy_required_unit(value):
    model, spec = sample()
    model['semantic_units']['core'] = value
    report = evaluate(model, spec)
    assert 'decision-paper.core' in rules(report)
    assert report['critical_coverage_percent'] == 0
    assert not any(item['blocking'] for item in report['findings'])


def test_all_fields_of_a_unit_are_required():
    model, spec = sample()
    spec['blueprint']['semantic_units'][0]['semantic_fields'].append('rationale')
    spec['compiled_spec_hash'] = canonical_hash({k:v for k,v in spec.items() if k not in ('artifact_id','document_kind','compiled_spec_hash')})
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    assert 'decision-paper.core' in rules(evaluate(model, spec))


@pytest.mark.parametrize('field,value,rule', [('contract_id','wrong','CONTRACT_BINDING_MISMATCH'), ('document_kind','adr','DOCUMENT_KIND_MISMATCH'), ('compiled_spec_hash','0'*64,'COMPILED_SPEC_HASH_MISMATCH')])
def test_binding_or_hash_tamper_preserves_existing_blocks(field, value, rule):
    model, spec = sample()
    model[field] = value
    report = evaluate(model, spec)
    assert rule in rules(report)
    assert report['gate_verdict'] == 'CONTENT_FAIL'


def test_spec_tamper_is_detected_even_when_model_still_declares_original_hash():
    model, spec = sample()
    spec['blueprint']['semantic_units'] = []
    assert 'COMPILED_SPEC_HASH_MISMATCH' in rules(evaluate(model, spec))


def test_known_material_claim_requires_real_versioned_evidence():
    model, spec = sample()
    model['claims'] = [{'text': 'Recovery met the objective.', 'knowledge_status': 'known', 'evidence_refs': ['E1']}]
    model['evidence'] = [{'id': 'E1', 'version': '1', 'payload': {'recovery_minutes': 27}, 'observed_at': '2026-10-01', 'valid_until': '2026-11-01'}]
    model['evaluation_date'] = '2026-10-19'
    assert 'decision-paper.unsupported_material_claim' in rules(evaluate(model, spec))
    model['evidence'][0]['hash'] = canonical_hash(model['evidence'][0]['payload'])
    assert 'decision-paper.unsupported_material_claim' not in rules(evaluate(model, spec))
    model['evidence'][0]['version'] = None
    assert 'decision-paper.unsupported_material_claim' in rules(evaluate(model, spec))


@pytest.mark.parametrize('date', ['2026-09-30', '2026-11-02', None])
def test_stale_future_and_undated_evidence_cannot_support_known_claim(date):
    model, spec = sample()
    model['evaluation_date'] = date
    model['claims'] = [{'text': 'Recovery objective met.', 'knowledge_status': 'known', 'evidence_refs': ['E1']}]
    payload = {'minutes': 27}
    model['evidence'] = [{'id': 'E1', 'version': '1', 'payload': payload, 'hash': canonical_hash(payload), 'observed_at': '2026-10-01', 'valid_until': '2026-11-01'}]
    assert 'decision-paper.unsupported_material_claim' in rules(evaluate(model, spec))


def test_explicit_assumption_does_not_pretend_to_be_evidence():
    model, spec = sample()
    model['claims'] = [{'text': 'Recovery may meet the objective.', 'knowledge_status': 'assumption', 'evidence_refs': []}]
    report = evaluate(model, spec)
    assert report['unsupported_claims'] == []
    assert report['gate_verdict'] == 'DRAFT_INCOMPLETE'


def test_advisory_never_weakens_security_rules():
    model, spec = sample()
    unit = {'id': 'global.secret_disclosure', 'semantic_fields': ['secret_disclosure'], 'datatype': 'object', 'category': 'forbidden_information', 'rule_category': 'security-policy', 'applicability': True}
    spec['blueprint']['semantic_units'].append(unit)
    spec['compiled_spec_hash'] = canonical_hash({k:v for k,v in spec.items() if k not in ('artifact_id','document_kind','compiled_spec_hash')})
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    model['semantic_units']['secret_disclosure'] = {'restricted': 'Synthetic restricted-data example.'}
    report = evaluate(model, spec)
    assert next(x for x in report['findings'] if x['rule_id'] == unit['id'])['blocking']


def test_unverified_or_self_declared_identity_cannot_pass():
    model, spec = sample()
    report = evaluate(model, spec, reviewer={'name': 'Independent Person', 'trusted': True}, trusted_executions={'trusted': True})
    assert report['gate_verdict'] == 'CONTENT_FAIL'
    assert 'REVIEW_IDENTITY_UNVERIFIED' in rules(report)


def test_independent_host_verified_review_is_bound_to_exact_source():
    model, spec = sample()
    model, review, verifier, registry = reviewed(model, spec)
    report = evaluate(model, spec, reviewer=review, trusted_executions=verifier)
    assert report['gate_verdict'] == 'CONTENT_PASS'
    assert not verify_report(report, model, spec, trusted_executions=verifier)
    assert verify_report(report, model, spec)
    registry['review-token']['snapshot_digest'] = '0'*64
    assert evaluate(model, spec, reviewer=review, trusted_executions=verifier)['gate_verdict'] == 'CONTENT_FAIL'


def test_same_principal_rejected_even_with_different_declared_names():
    model, spec = sample()
    model, review, verifier, _ = reviewed(model, spec, same_principal=True, declared_aliases=True)
    assert 'REVIEW_IDENTITY_UNVERIFIED' in rules(evaluate(model, spec, reviewer=review, trusted_executions=verifier))


def test_different_authenticated_principals_pass_with_distinct_declared_aliases():
    model, spec = sample()
    model, review, verifier, _ = reviewed(model, spec, declared_aliases=True)
    assert evaluate(model, spec, reviewer=review, trusted_executions=verifier)['gate_verdict'] == 'CONTENT_PASS'


def test_review_without_unit_evidence_is_not_semantic_acceptance():
    model, spec = sample()
    model, review, verifier, registry = reviewed(model, spec)
    review['unit_reviews'][0]['evidence'] = ''
    registry['review-token']['subject_digest'] = canonical_hash({k:v for k,v in review.items() if k != 'attestation'})
    assert evaluate(model, spec, reviewer=review, trusted_executions=verifier)['gate_verdict'] == 'CONTENT_FAIL'


@pytest.mark.parametrize('authority', [None, {'approved': True, 'existing_jai_l0': True}])
def test_arbitrary_blocking_flag_never_activates_enforcement(authority):
    model, spec = sample()
    with pytest.raises(ValueError, match='HUMAN_L0'):
        evaluate(model, spec, mode='blocking', authority=authority)


def test_nonfinite_json_is_rejected():
    model, spec = sample()
    model['semantic_units']['core']['amount'] = float('nan')
    with pytest.raises(ValueError):
        evaluate(model, spec)


def test_immutable_report_replays_and_refuses_overwrite(tmp_path):
    model, spec = sample()
    report = evaluate(model, spec)
    path = tmp_path/'content-qa.json'
    assert write_report(path, report) == path
    assert write_report(path, report) == path
    assert verify_report(report, model, spec) == []
    model['semantic_units']['core']['decision'] = 'Choose a different managed platform.'
    assert verify_report(report, model, spec)
    with pytest.raises(ValueError, match='IMMUTABLE'):
        write_report(path, evaluate(model, spec))
    report['gate_verdict'] = 'CONTENT_PASS'
    with pytest.raises(ValueError, match='HASH_MISMATCH'):
        write_report(tmp_path/'tampered.json', report)


def test_cli_pilot_writes_report_and_rejects_activation(tmp_path):
    from content_eval import prepare_case
    root = Path(__file__).resolve().parents[1]
    fixture = json.loads((root / '.ai/runtime/evals/content_quality/decision-paper-simple.json').read_text())
    model, spec = prepare_case(fixture, ContentSpec(root))
    semantic = tmp_path/'semantic.json'; compiled = tmp_path/'compiled.json'; output = tmp_path/'qa.json'
    semantic.write_text(json.dumps(model)); compiled.write_text(json.dumps(spec))
    args = ['check', str(semantic), '--spec', str(compiled), '--output', str(output)]
    assert main(args) == 0
    assert main(args + ['--mode', 'blocking']) == 1


def test_outline_preserves_unknowns_and_exact_binding():
    engine = ContentSpec(Path(__file__).resolve().parents[1])
    contract = next(key for key,value in engine.bindings.items() if value['document_kind'] == 'decision-paper')
    outline = engine.outline(contract, {'processes_personal_data': None})
    assert outline['semantic_model']['artifact_id'] is None
    assert outline['semantic_model']['contract_id'] == contract
    assert all(value is None for value in outline['semantic_model']['semantic_units'].values())
    assert any(unit['applicability'] is None for unit in outline['blueprint'])
    with pytest.raises(SpecError):
        engine.outline('invented-role')


def test_missing_knowledge_state_cannot_be_certified_even_with_review():
    model, spec = sample()
    del model['semantic_units']['core']['knowledge_status']
    model, review, verifier, _ = reviewed(model, spec)
    report = evaluate(model, spec, reviewer=review, trusted_executions=verifier)
    assert 'decision-paper.core' in rules(report)
    assert report['gate_verdict'] == 'DRAFT_INCOMPLETE'


def test_unknown_list_item_is_visible_in_coverage():
    model, spec = sample()
    spec['blueprint']['semantic_units'][0]['datatype'] = 'array'
    spec['compiled_spec_hash'] = canonical_hash({k:v for k,v in spec.items() if k not in ('artifact_id','document_kind','compiled_spec_hash')})
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    model['semantic_units']['core'] = [{'decision': 'Investigate recovery evidence.', 'knowledge_status': 'unknown'}]
    report = evaluate(model, spec)
    assert report['semantic_unit_coverage'][0]['status'] == 'unknown'
    assert any(x['location'].endswith('[0]') for x in report['unknowns'])


def test_duplicate_evidence_identifier_preserves_existing_block():
    model, spec = sample()
    model['evidence'] = [{'id': 'E1'}, {'id': 'E1'}]
    report = evaluate(model, spec)
    assert 'EVIDENCE_ID_DUPLICATE' in rules(report)
    assert report['gate_verdict'] == 'CONTENT_FAIL'


def test_explicit_evidence_version_and_hash_pins_must_match():
    model, spec = sample()
    payload = {'recovery_minutes': 27}
    digest = canonical_hash(payload)
    model['evaluation_date'] = '2026-10-19'
    model['evidence'] = [{'id': 'E1', 'version': '2', 'payload': payload, 'hash': digest, 'observed_at': '2026-10-01', 'valid_until': '2026-11-01'}]
    model['claims'] = [{'text': 'Recovery met the objective.', 'knowledge_status': 'known', 'evidence_refs': [{'id': 'E1', 'version': '1', 'hash': digest}]}]
    assert 'decision-paper.unsupported_material_claim' in rules(evaluate(model, spec))
    model['claims'][0]['evidence_refs'][0]['version'] = '2'
    assert 'decision-paper.unsupported_material_claim' not in rules(evaluate(model, spec))


def test_scoped_host_verified_existing_authority_can_activate_only_approved_policy():
    model, spec = sample()
    spec['status'] = 'approved'; spec['calibration_status'] = 'human-approved'
    spec['compiled_spec_hash'] = canonical_hash({k:v for k,v in spec.items() if k not in ('artifact_id','document_kind','compiled_spec_hash')})
    model['compiled_spec_hash'] = spec['compiled_spec_hash']
    qualification = {'calibration_status':'human-approved', 'critical_recall':.95, 'false_positive_rate':.1,
        'sod_escapes':0,'critical_forbidden':0,'unsupported_critical_claims':0,'critical_coverage_percent':100,'corpus_hash':'a'*64}
    proof = {'authority_ref':'existing-fabric:test-only', 'existing_jai_l0':True, 'signature_verified':True,
        'fabric_verified':True, 'verification_warnings':[], 'scope':'dcs-content-enforcement',
        'compiled_spec_hash':spec['compiled_spec_hash'], 'document_kind':spec['document_kind'],
        'context_hash':spec['context_hash'], 'issued_at':'2026-10-01', 'expires_at':'2026-11-01',
        'verified_at':'2026-10-19T00:00:00Z', 'qualification':qualification}
    class SyntheticHostBoundary:
        # This test simulates verified host output, never issues a fabric act.
        def verify(self, attestation):
            return proof
    host = SyntheticHostBoundary()
    model['semantic_units']['core'] = None
    report = evaluate(model, spec, mode='blocking', authority=host)
    assert report['gate_verdict'] == 'CONTENT_FAIL'
    assert report['approval_refs'] == ['existing-fabric:test-only']
    proof['verified_at'] = '2026-11-02T00:00:00Z'
    with pytest.raises(ValueError, match='HUMAN_L0'):
        evaluate(model, spec, mode='blocking', authority=host)


def authenticated_dispatcher_review(model, spec):
    """Build test-only in-memory signed attestations verified by real runtime code."""
    import hashlib
    import hmac
    from commercial_runtime import TrustedDispatcher
    key = b'synthetic-host-key-for-unit-tests-only-000'
    dispatcher = TrustedDispatcher(key, [], executable_roots=())
    def sign(subject, snapshot, context, reviewer, sequence):
        execution = f'synthetic-test-{sequence}'
        pid = 100 + sequence
        payload = {'dispatch_id': execution, 'principal': f'uid:999:worker:{pid}:execution:{execution}',
            'worker_execution': {'pid':pid,'uid':999,'execution_id':execution,'readonly_inputs':True,'fresh_namespace':True},
            'subject_digest':canonical_hash(subject), 'snapshot_digest':snapshot, 'context_digest':canonical_hash(context),
            'reviewer':reviewer, 'enforcement':'bwrap-tested', 'exit_code':0}
        return {'payload':payload, 'signature':hmac.new(key, canonical_hash(payload).encode(), hashlib.sha256).hexdigest()}
    model=copy.deepcopy(model)
    model['producer']={'context_manifest':{'history_policy':'fresh','injected_instructions':['synthetic-test']}}
    producer_hash=canonical_hash(model)
    model['producer']['attestation']=sign(model, producer_hash, model['producer']['context_manifest'], False, 1)
    review={'semantic_hash':canonical_hash(model), 'compiled_spec_hash':spec['compiled_spec_hash'],
        'context_hash':spec['context_hash'], 'context_manifest':{'history_policy':'fresh','injected_instructions':['synthetic-review-test']},
        'unit_reviews':[{'unit_id':unit['id'], 'verdict':'PASS', 'rationale':'Reviewed the actual scoped decision and its explicit assumption.',
                         'evidence':'Canonical semantic source unit '+unit['id']} for unit in spec['blueprint']['semantic_units'] if (unit.get('applicability') is not False or unit['category'] == 'conditional_information') and unit['category'] in ('required_information','conditional_information','forbidden_information','low_value_information')],
        'findings':[]}
    review['attestation']=sign(review, canonical_hash(model), review['context_manifest'], True, 2)
    return model, review, dispatcher


def test_actual_dispatcher_hmac_verification_supports_review_and_rejects_tamper():
    model,spec=sample()
    model,review,dispatcher=authenticated_dispatcher_review(model,spec)
    report=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
    assert report['gate_verdict']=='CONTENT_PASS'
    review['attestation']['signature']='0'*64
    assert evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)['gate_verdict']=='CONTENT_FAIL'



def test_existing_fabric_adapter_reads_signed_acceptance_without_mutations(tmp_path, monkeypatch):
    import datetime as dt
    import importlib.util
    from content_lint import ExistingFabricAuthority
    from lifecycle_fixtures import accepted_graph
    path=Path(__file__).resolve().parents[1]/'.ai/runtime/fabric/fabric.py'
    module_spec=importlib.util.spec_from_file_location('content_test_readonly_fabric',path)
    module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
    fabric,fragment_id,_=accepted_graph(module,tmp_path,monkeypatch,
        json.dumps({'profile':'content-enforcement','dcs_activation':{'scope':'dcs-content-enforcement'}}))
    adapter=ExistingFabricAuthority(fabric,fragment_id,clock=lambda:dt.datetime(2026,10,19,tzinfo=dt.timezone.utc))
    original_bytes=Path(module.log_path(fabric.eng)).read_bytes()
    result=adapter.verify(adapter.proof)
    assert result['authority_ref']==next(n['id'] for n in fabric.nodes.values() if n['type']=='rev' and n['layer']==0)
    assert result['signature_verified']
    assert Path(module.log_path(fabric.eng)).read_bytes()==original_bytes
    for malformed in ('{"profile":"content-enforcement","profile":"content-enforcement","dcs_activation":{}}',
                      '{"profile":"content-enforcement","dcs_activation":{"critical_recall":Infinity}}'):
        directory=tmp_path/('malformed-'+str(len(malformed)));directory.mkdir()
        # Restore both ledger location and external trust together on scope exit.
        with monkeypatch.context() as isolated:
            signed,subject,_=accepted_graph(module,directory,isolated,malformed)
            rejected=ExistingFabricAuthority(signed,subject)
            assert signed.verify()==([],[])
            assert rejected.verify(rejected.proof) is None
    import operator_actions as op
    assert Path(module.log_path(fabric.eng)).read_bytes()==original_bytes
    fabric.transactions[-1]['proof']['receipt']['signature']='AA=='
    assert adapter.verify(adapter.proof) is None
    fabric.transactions=module.load(fabric.eng)
    monkeypatch.setattr(op,'trusted_key',lambda: (_ for _ in ()).throw(ValueError('no public pin')))
    assert adapter.verify(adapter.proof) is None


@pytest.mark.parametrize('body', [
    {'password':'FictionalUnitTestCredential123'},
    {'procedure':'Set access_token=FictionalUnitTestCredential123 before continuing.'},
    {'description':'-----BEGIN PRIVATE KEY-----\nQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo=\n-----END PRIVATE KEY-----'},
    {'description':'Use ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 to access the service.'},
])
def test_credentials_in_actual_content_always_block_with_redacted_findings(body):
    model,spec=sample()
    model['semantic_units']['core'].update(body)
    report=evaluate(model,spec)
    finding=next(item for item in report['findings'] if item['rule_id']=='global.secret_disclosure')
    assert finding['blocking']
    assert report['gate_verdict']=='CONTENT_FAIL'
    assert 'FictionalUnitTestCredential123' not in json.dumps(report)
    assert 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890' not in json.dumps(report)


@pytest.mark.parametrize('text', ['vault://production/platform/password', '${SERVICE_PASSWORD}', '<redacted>', 'Retrieve credentials from the approved secret store.'])
def test_secret_references_and_redacted_examples_do_not_trigger_credential_detector(text):
    model,spec=sample()
    model['semantic_units']['core']['password']=text
    assert 'global.secret_disclosure' not in rules(evaluate(model,spec))


@pytest.mark.parametrize('hard_constraint', [False, True])
def test_registered_approved_policy_activates_via_actual_existing_signed_fabric(tmp_path, monkeypatch, hard_constraint):
    import datetime as dt
    import hashlib
    import hmac
    import importlib.util
    from content_lint import ExistingFabricAuthority
    base=tmp_path/'.ai/runtime/content';base.mkdir(parents=True)
    registered={'id':'kind/decision-paper','version':'1.0.0','status':'approved','calibration_status':'human-approved',
        'completeness':'skeleton','inherits':[],'applies_to':{'document_kind':'decision-paper','artifact_types':['document']},
        'purpose':'Test-only qualified registered policy, never a shipped standard.',
        'required_information':[{'id':'decision-paper.core','semantic_fields':['core'],'datatype':'object','acceptance_predicate':{'op':'review'}}],
        'conditional_information':[],'optional_information':[],'forbidden_information':[],'size_budget':{'metric':'words'}}
    if hard_constraint:
        registered['size_budget'].update(hard_max=1,hard_limit_basis={'kind':'contractual','source_ref':'contract:test-upper-bound','reason':'Synthetic fixed one-word channel capacity for boundary test.'})
    registry={'schema_version':'1.0.0','specifications':[{'id':registered['id'],'version':'1.0.0','path':'policy.json','status':'approved'}],
        'document_kinds':[{'id':'decision-paper','artifact_types':['document'],'spec_ref':registered['id']}],
        'bindings':[{'artifact_id':'role:decision-paper','artifact_type':'document','document_kind':'decision-paper','content_spec_ref':registered['id']}],
        'context_fields':{}}
    (base/'policy.json').write_text(json.dumps(registered));(base/'registry.json').write_text(json.dumps(registry))
    spec=ContentSpec(tmp_path).resolve('role:decision-paper',{})
    assert spec['status']=='approved'
    assert spec['calibration_status']=='human-approved'
    assert spec['approval_status']=='pending-human-L0'
    assert spec['production_ready'] is False
    model,_=sample();model['compiled_spec_hash']=spec['compiled_spec_hash']
    model,review,dispatcher=authenticated_dispatcher_review(model,spec)
    qualification={'calibration_status':'human-approved','critical_recall':1.,'false_positive_rate':0.,'sod_escapes':0,
        'critical_forbidden':0,'unsupported_critical_claims':0,'critical_coverage_percent':100,'corpus_hash':'b'*64}
    policy={'profile':'content-enforcement','dcs_activation':{'scope':'dcs-content-enforcement',
        'compiled_spec_hash':spec['compiled_spec_hash'],'document_kind':spec['document_kind'],'context_hash':spec['context_hash'],
        'issued_at':'2026-10-01','expires_at':'2026-11-01','qualification':qualification}}
    module_path=Path(__file__).resolve().parents[1]/'.ai/runtime/fabric/fabric.py'
    loader=importlib.util.spec_from_file_location('registered_content_fabric_fixture',module_path)
    module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module)
    from lifecycle_fixtures import accepted_graph
    fabric,fragment_id,_=accepted_graph(module,tmp_path,monkeypatch,json.dumps(policy))
    authority=ExistingFabricAuthority(fabric,fragment_id,clock=lambda:dt.datetime(2026,10,19,tzinfo=dt.timezone.utc))
    report=evaluate(model,spec,mode='blocking',reviewer=review,trusted_executions=dispatcher,authority=authority)
    assert report['gate_verdict']==('CONTENT_FAIL' if hard_constraint else 'CONTENT_PASS')
    if hard_constraint:
        assert next(f for f in report['findings'] if f['rule_id']=='HARD_SIZE_CONSTRAINT')['blocking']
        advisory=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
        assert not next(f for f in advisory['findings'] if f['rule_id']=='HARD_SIZE_CONSTRAINT')['blocking']
        assert advisory['gate_verdict']=='DRAFT_INCOMPLETE'
    assert report['approval_refs']==[next(n['id'] for n in fabric.nodes.values() if n['type']=='rev' and n['layer']==0)]
    assert not verify_report(report,model,spec,trusted_executions=dispatcher,authority=authority)
    assert all(transaction['format']==2 for transaction in fabric.transactions)
    # The metadata alone never activates enforcement, even when declared approved.
    with pytest.raises(ValueError,match='HUMAN_L0'):
        evaluate(model,spec,mode='blocking',reviewer=review,trusted_executions=dispatcher)
    registered['status']='proposed';registry['specifications'][0]['status']='proposed'
    (base/'policy.json').write_text(json.dumps(registered));(base/'registry.json').write_text(json.dumps(registry))
    proposed=ContentSpec(tmp_path).resolve('role:decision-paper',{})
    assert proposed['status']=='proposed'
    with pytest.raises(ValueError,match='HUMAN_L0'):
        evaluate(model,proposed,mode='blocking',authority=authority)


@pytest.mark.parametrize('issued,expires,verified,accepted', [
    ('2026-10-19T00:00:00Z','2026-10-19T01:00:00Z','2026-10-19T23:00:00Z',False),
    ('2026-10-19T23:00:00Z','2026-10-20T01:00:00Z','2026-10-19T01:00:00Z',False),
    ('2026-10-19T00:00:00Z','2026-10-19T23:00:00Z','2026-10-19T12:00:00',False),
    ('2026-10-19T00:00:00','2026-10-19T23:00:00Z','2026-10-19T12:00:00Z',False),
    ('2026-10-19T00:00:00Z','2026-10-19T23:00:00','2026-10-19T12:00:00Z',False),
    ('2026-10-19','2026-10-19','2026-10-19T23:59:59.999999Z',True),
    ('2026-10-19T00:00:00+02:00','2026-10-19T01:00:00+02:00','2026-10-18T23:00:00Z',True),
    ('2026-10-19T01:00:00Z','2026-10-19T00:00:00Z','2026-10-19T00:30:00Z',False),
    ('2026-10-19T00:00:00Z','malformed','2026-10-19T12:00:00Z',False),
])
def test_activation_observes_exact_trusted_timestamp_and_timezone(issued,expires,verified,accepted):
    from content_lint import _activation_valid
    model,spec=sample();spec['status']='approved';spec['calibration_status']='human-approved'
    proof={'authority_ref':'test-only-existing-act','existing_jai_l0':True,'signature_verified':True,
        'fabric_verified':True,'verification_warnings':[],'scope':'dcs-content-enforcement',
        'compiled_spec_hash':spec['compiled_spec_hash'],'document_kind':spec['document_kind'],'context_hash':spec['context_hash'],
        'issued_at':issued,'expires_at':expires,'verified_at':verified,
        'qualification':{'calibration_status':'human-approved','critical_recall':1.,'false_positive_rate':0.,
            'sod_escapes':0,'critical_forbidden':0,'unsupported_critical_claims':0,'critical_coverage_percent':100,'corpus_hash':'a'*64}}
    class Host:
        def verify(self, attestation):
            return proof
    assert _activation_valid(Host(),spec,model) is accepted


@pytest.mark.parametrize('field,value', [
    ('critical_recall', True), ('critical_recall', float('inf')), ('critical_recall', float('nan')),
    ('critical_recall', 1.1), ('false_positive_rate', float('-inf')), ('false_positive_rate', -0.1),
    ('sod_escapes', False), ('sod_escapes', 0.0), ('critical_forbidden', -1),
    ('unsupported_critical_claims', False), ('critical_coverage_percent', float('inf')),
])
def test_authority_qualification_rejects_nonfinite_boolean_and_untyped_metrics(field,value):
    from content_lint import _activation_valid
    model,spec=sample();spec['status']='approved';spec['calibration_status']='human-approved'
    qualification={'calibration_status':'human-approved','critical_recall':1.,'false_positive_rate':0.,
        'sod_escapes':0,'critical_forbidden':0,'unsupported_critical_claims':0,'critical_coverage_percent':100,'corpus_hash':'a'*64}
    qualification[field]=value
    proof={'authority_ref':'test-only-existing-act','existing_jai_l0':True,'signature_verified':True,
        'fabric_verified':True,'verification_warnings':[],'scope':'dcs-content-enforcement',
        'compiled_spec_hash':spec['compiled_spec_hash'],'document_kind':spec['document_kind'],'context_hash':spec['context_hash'],
        'issued_at':'2026-10-01','expires_at':'2026-11-01','verified_at':'2026-10-19T12:00:00Z','qualification':qualification}
    class Host:
        def verify(self, attestation):
            return proof
    assert _activation_valid(Host(),spec,model) is False


def test_historical_26_10_7_report_replays_without_new_optional_modality_counts():
    model,spec=sample()
    model['nodes']=[{'id':'node-one'}]
    report=evaluate(model,spec)
    assert report['length']['elements']==1
    report['length'].pop('elements');report['length'].pop('configuration_checks')
    report.pop('report_hash')
    report['report_hash']=canonical_hash(report)
    assert verify_report(report,model,spec)==[]
    report['gate_verdict']='CONTENT_PASS'
    report['report_hash']=canonical_hash({k:v for k,v in report.items() if k!='report_hash'})
    assert verify_report(report,model,spec)


def test_current_spec_report_cannot_omit_modality_counts_and_rehash():
    model,spec=sample()
    spec['spec_version']='1.1.0'
    spec['compiled_spec_hash']=canonical_hash({k:v for k,v in spec.items() if k not in ('artifact_id','document_kind','compiled_spec_hash')})
    model['compiled_spec_hash']=spec['compiled_spec_hash']
    report=evaluate(model,spec)
    report['length'].pop('elements')
    report.pop('report_hash')
    report['report_hash']=canonical_hash(report)
    assert verify_report(report,model,spec)
