# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""DCS projection source fidelity and publication boundary regressions."""
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.ai/runtime/tools'))
import content_spec
import projection
import publication
import publication_integrity

ROOT=Path(__file__).resolve().parents[1]


def fixture(tmp_path):
    catalog=content_spec.ContentSpec(ROOT)
    contract=next(k for k,v in catalog.bindings.items() if v['document_kind']=='decision-paper')
    model=json.loads((ROOT/'.ai/runtime/evals/content_quality/decision-paper-simple.json').read_text())
    spec=catalog.resolve(contract,model['context'])
    model.update(contract_id=contract,compiled_spec_hash=spec['compiled_spec_hash'],owner='Service owner',classification='Internal',audience=['Board'])
    model['sections']=[{'heading':'Context','body':'Inventory service recovery within thirty minutes.'}]
    profile={'id':'test','audience':['Board'],'mandatory_sections':['Context'],'mandatory_semantic_fields':[]}
    source=tmp_path/'source.json'; source.write_text(json.dumps(model))
    pp=tmp_path/'profile.json'; pp.write_text(json.dumps(profile))
    return source,pp,tmp_path/'projection'


def test_headings_do_not_satisfy_explicit_semantic_fields():
    assert not projection.field_present({'sections':[{'heading':'Decision and risks'}]},'decisions')
    assert not projection.field_present({'decisions':[{'id':'D'}]},'decisions')
    assert projection.field_present({'decisions':[{'question':'Approve recovery?'}]},'decisions')


def test_empty_section_does_not_satisfy_profile():
    _,man=projection.select_sections({'sections':[{'heading':'Context'}]}, {'id':'test','audience':[],'mandatory_sections':['Context']})
    assert man['mandatory_coverage']==0
    assert publication.validate_model({'title':'T','artifact_id':'I','audience':['A'],'owner':'O','classification':'Internal','sections':[{'heading':'Context'}]})


def test_new_build_requires_registered_contract(tmp_path):
    source,profile,out=fixture(tmp_path)
    model=json.loads(source.read_text()); model.pop('contract_id'); source.write_text(json.dumps(model))
    probs,_,_=projection.build(source,profile,out)
    assert any('contract_id' in p for p in probs)
    assert not out.exists()


def test_qa_sidecars_and_exact_source_units_survive_projection(tmp_path):
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out)
    assert not probs,probs
    assert man['content_qa_ref']=='content-qa.json'
    assert not publication_integrity.verify_content(pub,man,out)
    assert pub['semantic_units']==json.loads(source.read_text())['semantic_units']
    assert man['semantic_unit_mappings']


def test_semantic_tamper_rejected_even_after_projection_resign(tmp_path):
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out); assert not probs,probs
    pub['semantic_units']['baseline']['problem']='Invented problem'
    man['projection_hash']=projection.sha(pub)
    assert any('fidelity' in p for p in publication_integrity.verify_content(pub,man,out))


def test_report_tamper_rejected_even_after_report_resign(tmp_path):
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out); assert not probs,probs
    path=out/'content-qa.json'; report=json.loads(path.read_text()); report['gate_verdict']='CONTENT_PASS'; path.write_text(json.dumps(report)); man['content_qa_hash']=projection.sha(report); man['content_status']='CONTENT_PASS'
    assert publication_integrity.verify_content(pub,man,out)


def test_legacy_manifest_readable_but_new_render_rejected(tmp_path):
    _,man=projection.select_sections({'artifact_id':'I','sections':[{'heading':'Context','body':'A scope'}]}, {'id':'legacy','audience':[],'mandatory_sections':['Context']})
    assert not projection.validate_manifest(man)
    assert publication_integrity.verify_content({},man,tmp_path)


def test_structured_evidence_reference_is_supported():
    pub={'evidence':[{'id':'E','version':'1'}], 'claims':[{'id':'C','evidence':[{'id':'E'}]}]}
    man={'projection_hash':projection.sha(pub),'mandatory_coverage':100,'mappings':[{'source':'evidence:E'}]}
    assert not publication_integrity.check(pub,man)


def test_omission_reason_cannot_waive_mandatory_publication_field(tmp_path):
    source,profile,out=fixture(tmp_path)
    model=json.loads(source.read_text()); model['publication_omissions']={'field:approvals':'Pilot context excludes approval'}; source.write_text(json.dumps(model))
    pp=json.loads(profile.read_text()); pp['mandatory_semantic_fields']=['approvals']; profile.write_text(json.dumps(pp))
    probs,_,_=projection.build(source,profile,out)
    assert any('cannot waive' in p for p in probs)
    assert not out.exists()


def test_context_tamper_rejected_and_sidecars_immutable(tmp_path):
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out); assert not probs,probs
    saved=json.loads((out/'semantic-source.json').read_text()); saved['context']['processes_personal_data']=True; (out/'semantic-source.json').write_text(json.dumps(saved))
    assert publication_integrity.verify_content(pub,man,out)
    import pytest
    with pytest.raises(FileExistsError): projection.build(source,profile,out)


def test_render_requires_bundle_even_with_fabricated_draft_status(tmp_path):
    import pytest
    with pytest.raises(ValueError,match='manifest and sidecars'):
        publication.render({'publication_status':'DRAFT_INCOMPLETE'},'html',tmp_path/'out.html',{})


def test_verified_render_exposes_draft_status_and_semantic_values(tmp_path):
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out); assert not probs,probs
    dest=tmp_path/'draft.html'
    publication.render(pub,'html',dest,{},man,out)
    text=dest.read_text()
    assert 'DRAFT' in text
    assert 'Synthetic rehearsal missed the recovery objective' in text


def test_symlinked_qa_sidecar_is_rejected(tmp_path):
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out); assert not probs,probs
    external=tmp_path/'external-report.json'; external.write_bytes((out/'content-qa.json').read_bytes())
    (out/'content-qa.json').unlink(); (out/'content-qa.json').symlink_to(external)
    assert any('regular local' in p for p in publication_integrity.verify_content(pub,man,out))


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


def test_mandatory_svg_content_is_visible_text(tmp_path):
    from xml.etree import ElementTree as ET
    source,profile,out=fixture(tmp_path)
    probs,pub,man=projection.build(source,profile,out); assert not probs,probs
    dest=tmp_path/'draft.svg'; publication.render(pub,'svg',dest,publication.load_json(publication.DEFAULT_THEME),man,out)
    tree=ET.parse(dest)
    visible=''.join(node.text or '' for node in tree.iter('{http://www.w3.org/2000/svg}text'))
    assert 'Synthetic rehearsal missed the recovery objective' in visible
    assert 'Approve TARGET managed recovery design' in visible


def test_pptx_long_content_is_wrapped_paginated_without_loss(tmp_path):
    import zipfile
    from xml.etree import ElementTree as ET
    text=''.join(f'word{i:04d} ' for i in range(400))
    model={'title':'Long draft','owner':'Owner','classification':'Internal','sections':[{'heading':'Mandatory detail','body':text}]}
    dest=tmp_path/'long.pptx'; publication.render_pptx(model,dest,{})
    paragraphs=[]; pages=0
    with zipfile.ZipFile(dest) as archive:
        for name in archive.namelist():
            if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                pages+=1
                tree=ET.fromstring(archive.read(name))
                lines=[node.text or '' for node in tree.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t')]
                paragraphs.extend(lines[1:])
                assert all(len(line)<=80 for line in lines[1:])
                assert len(lines)<=9
    assert pages>2
    assert ''.join(paragraphs[3:]).split()==text.split()


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
