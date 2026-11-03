# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Archived internal HMAC attestation cases; not a supported execution route."""
import copy
import json
import pytest

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


@pytest.mark.parametrize('hard_constraint', [False, True])
def test_registered_approved_policy_activates_via_actual_existing_signed_fabric(tmp_path, monkeypatch, hard_constraint):
    import datetime as dt
    import hashlib
    import hmac
    import importlib.util
    from content_lint import GovernedAuthority
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
    from governed_fixtures import accepted_store
    host, _, subject, _ = accepted_store(tmp_path, monkeypatch, json.dumps(policy))
    authority = GovernedAuthority(host.store, subject, use_scope=host.scope,
                                 clock=lambda: dt.datetime(2026,10,19,tzinfo=dt.timezone.utc))
    report=evaluate(model,spec,mode='blocking',reviewer=review,trusted_executions=dispatcher,authority=authority)
    assert report['gate_verdict']==('CONTENT_FAIL' if hard_constraint else 'CONTENT_PASS')
    if hard_constraint:
        assert next(f for f in report['findings'] if f['rule_id']=='HARD_SIZE_CONSTRAINT')['blocking']
        advisory=evaluate(model,spec,reviewer=review,trusted_executions=dispatcher)
        assert not next(f for f in advisory['findings'] if f['rule_id']=='HARD_SIZE_CONSTRAINT')['blocking']
        assert advisory['gate_verdict']=='DRAFT_INCOMPLETE'
    assert report['approval_refs'] == [host.store.evaluate(subject)['acceptances'][0]['version_id']]
    assert not verify_report(report,model,spec,trusted_executions=dispatcher,authority=authority)
    assert all(transaction['format'] == 3 for transaction in host.store.read().transactions)
    # The metadata alone never activates enforcement, even when declared approved.
    with pytest.raises(ValueError,match='HUMAN_L0'):
        evaluate(model,spec,mode='blocking',reviewer=review,trusted_executions=dispatcher)
    registered['status']='proposed';registry['specifications'][0]['status']='proposed'
    (base/'policy.json').write_text(json.dumps(registered));(base/'registry.json').write_text(json.dumps(registry))
    proposed=ContentSpec(tmp_path).resolve('role:decision-paper',{})
    assert proposed['status']=='proposed'
    with pytest.raises(ValueError,match='HUMAN_L0'):
        evaluate(model,proposed,mode='blocking',authority=authority)

