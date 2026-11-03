# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Archived internal HMAC attestation cases; not a supported execution route."""
import copy
import json
import pytest

def test_authenticated_dispatcher_review_replays_at_render(tmp_path):
    from test_content_lint import authenticated_dispatcher_review
    source,profile,out=fixture(tmp_path)
    model=json.loads(source.read_text())
    spec=content_spec.ContentSpec(ROOT).resolve(model['contract_id'],model['context'])
    model,review,dispatcher=authenticated_dispatcher_review(model,spec)
    source.write_text(json.dumps(model))
    probs,pub,man=projection.build(source,profile,out,reviewer=review,trusted_executions=dispatcher)
    assert not probs,probs
    assert man['content_status']=='CONTENT_PASS'
    assert not publication_integrity.verify_content(pub,man,out,trusted_executions=dispatcher)
    assert publication_integrity.verify_content(pub,man,out)
    dest=tmp_path/'authenticated-draft.html'
    publication.render(pub,'html',dest,{},man,out,trusted_executions=dispatcher)
    assert 'DRAFT' in dest.read_text()
    from commercial_runtime import TrustedDispatcher
    wrong=TrustedDispatcher(b'wrong-test-only-key-0000000000000000',[],executable_roots=())
    assert publication_integrity.verify_content(pub,man,out,trusted_executions=wrong)


def test_authenticated_review_rejects_self_review_and_wrong_snapshot(tmp_path):
    import hashlib
    import hmac
    from test_content_lint import authenticated_dispatcher_review
    source,profile,out=fixture(tmp_path)
    model=json.loads(source.read_text()); spec=content_spec.ContentSpec(ROOT).resolve(model['contract_id'],model['context'])
    model,review,dispatcher=authenticated_dispatcher_review(model,spec)
    source.write_text(json.dumps(model))
    for attack in ('same-principal','wrong-snapshot'):
        forged=copy.deepcopy(review)
        payload=forged['attestation']['payload']
        if attack=='same-principal': payload['principal']=model['producer']['attestation']['payload']['principal']
        else: payload['snapshot_digest']='0'*64
        forged['attestation']['signature']=hmac.new(b'synthetic-host-key-for-unit-tests-only-000',content_spec.canonical_hash(payload).encode(),hashlib.sha256).hexdigest()
        probs,_,man=projection.build(source,profile,out/attack,reviewer=forged,trusted_executions=dispatcher)
        assert 'blocking content QA findings' in probs
        assert man['content_status']=='CONTENT_FAIL'
        assert not (out/attack).exists()

