# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Application protocol/crypto checks; these do not prove host key separation."""
import base64,copy,json,subprocess,sys,time
from pathlib import Path
from unittest.mock import patch
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.ai/runtime/tools'))
import operator_actions as op


def test_capability_refresh_observes_changes_without_writing_configuration(tmp_path):
    manifest = Path(__file__).resolve().parents[1] / 'RELEASE-SCOPE.json'
    original = manifest.read_bytes()
    completed = subprocess.CompletedProcess([], 0, stdout='{"base_workflow":"READY"}', stderr='')
    with patch('shutil.which', return_value=None), patch.object(op.subprocess, 'run', return_value=completed):
        absent = op.configure()
        assert absent['tools']['browser']['status'] == 'UNAVAILABLE'
        assert absent['configuration_changed'] is False
    with patch('shutil.which', return_value='/optional/tool'), patch.object(op.subprocess, 'run', return_value=completed):
        present = op.tool_inventory()
        assert present['browser']['status'] == 'AVAILABLE'
        assert present['browser']['functional_readiness'] == 'NOT_VERIFIED'
        assert present['browser']['sandbox_access'] == 'NOT_VERIFIED'
    with patch('shutil.which', return_value='/optional/tool'), patch.object(op.subprocess, 'run', side_effect=subprocess.TimeoutExpired('probe', 2)):
        failed = op.configure()
        assert failed['capabilities']['status'] == 'UNAVAILABLE'
        assert failed['tools']['browser']['status'] == 'UNAVAILABLE'
    assert manifest.read_bytes() == original
    assert list(tmp_path.iterdir()) == []
    baseline=tmp_path/'previous.json';baseline.write_text(json.dumps(absent))
    with patch('shutil.which',return_value='/optional/tool'), patch.object(op.subprocess,'run',return_value=completed):
        assert 'browser' in op.configure(baseline)['changes']['newly_available']
    baseline.write_text(json.dumps({'schema_version':1,'tools':present}))
    with patch('shutil.which',return_value=None), patch.object(op.subprocess,'run',return_value=completed):
        assert 'browser' in op.configure(baseline)['changes']['became_unavailable']
    baseline.write_text('{}')
    with pytest.raises(ValueError):op.configure(baseline)


def test_request_exact_hash_expiry_and_no_arbitrary_command_transport(tmp_path):
    source=tmp_path/'draft.html';source.write_text('<h1>Fixture</h1>')
    req=op.request('render','fixture',source,tmp_path/'outputs',{'backend':'libreoffice'})
    assert op.validate(req)==req
    for field in ('purpose','target','kind'):
        wrong=copy.deepcopy(req);wrong[field]='shell'
        with pytest.raises(ValueError):op.validate(wrong)
    with pytest.raises(ValueError):op.request('shell','no',source,tmp_path,{'command':'arbitrary'})
    with patch.object(op.time,'time',return_value=req['expires_at']):
        with pytest.raises(ValueError):op.validate(req)
    hostile=op.request('render','fixture',source,tmp_path/'outputs',{'backend':'libreoffice','command':'arbitrary'})
    with pytest.raises(ValueError):op.perform_render(hostile,tmp_path/'request.json',tmp_path)
    assert op.verify_outputs(req,op.response(req,False))=='DENIED'
    assert op.verify_outputs(req,op.response(req,True))=='UNAVAILABLE'
    source.write_text('changed')
    with pytest.raises(ValueError):op.verify_outputs(req,op.response(req,False))


def test_no_follow_files_and_returned_output_scope(tmp_path):
    source=tmp_path/'source';source.write_text('source');link=tmp_path/'alias';link.symlink_to(source)
    with pytest.raises(OSError):op.regular(link)
    req=op.request('render','fixture',source,tmp_path/'outputs',{'backend':'libreoffice'})
    destination=tmp_path/'outputs'/req['request_id'];destination.mkdir(parents=True);output=destination/'page';output.write_text('fixture')
    result=op.response(req,True,True,[{'path':str(output),'sha256':op.sha(output.read_bytes())}])
    assert op.verify_outputs(req,result)=='COMPLETED'
    output.write_text('tamper')
    with pytest.raises(ValueError):op.verify_outputs(req,result)
    result['outputs']=[{'path':str(source),'sha256':op.sha(source.read_bytes())}]
    with pytest.raises(ValueError):op.verify_outputs(req,result)


def test_real_ed25519_verification_tamper_cross_request_and_decline(tmp_path):
    # Disposable synthetic crypto fixture ONLY; production trust is not patched
    # by the application, and this is not evidence of a real operator action.
    key=tmp_path/'synthetic-private.pem';pub=tmp_path/'synthetic-public.pem'
    subprocess.run(['openssl','genpkey','-algorithm','ED25519','-out',str(key)],check=True,capture_output=True)
    subprocess.run(['openssl','pkey','-in',str(key),'-pubout','-out',str(pub)],check=True,capture_output=True)
    source=tmp_path/'ledger';source.write_text('fixture')
    req=op.request('fabric-review','fixture',source,'frag-1',{})
    trust={'key_id':op.sha(pub.read_bytes()),'public_key':pub.read_text()}
    body=op.response(req,True);body.update(key_id=trust['key_id'],assurance=op.ASSURANCE)
    payload=tmp_path/'payload';payload.write_bytes(op.canonical(body));signature=tmp_path/'sig'
    subprocess.run(['openssl','pkeyutl','-sign','-inkey',str(key),'-rawin','-in',str(payload),'-out',str(signature)],check=True,capture_output=True)
    receipt=dict(body,signature=base64.b64encode(signature.read_bytes()).decode())
    with patch.object(op,'trusted_key',return_value=trust):
        assert op.verify_receipt(req,receipt)['accepted']
        altered=dict(receipt,accepted=False)
        with pytest.raises(ValueError):op.verify_receipt(req,altered)
        other=op.request('fabric-review','other',source,'frag-2',{})
        with pytest.raises(ValueError):op.verify_receipt(other,receipt)
    with patch.object(op,'trusted_key',side_effect=ValueError('missing protected trust')):
        with pytest.raises(ValueError):op.verify_receipt(req,receipt)
    with patch.object(op.sys.stdin,'isatty',return_value=False):
        with pytest.raises(ValueError):op.sign(req,key)


def test_protected_pin_doctor_and_incomplete_acceptance(tmp_path):
    import stat
    from types import SimpleNamespace
    assert op.trust_path().name=='jai-operator-trust.json'
    with patch.object(op.sys,'platform','win32'):
        with pytest.raises(ValueError):op.trust_path()
    pin=tmp_path/'public-trust.json';pin.write_text('{}');pin.chmod(0o666)
    with patch.object(op,'trust_path',return_value=pin):
        with pytest.raises(ValueError):op.trusted_key()
    manifest=tmp_path/'observations.json';manifest.write_text(json.dumps({'l0':[],'render':[]}))
    with pytest.raises(ValueError):op.check_acceptance(manifest)
    import importlib.metadata
    with patch.object(importlib.metadata, 'version', return_value='0.13.2'), patch('office_renderer.html_pdf') as render:
        legacy=op.doctor()
        assert legacy['html_pdf'].startswith('OPERATOR_ACTION_REQUIRED')
        assert legacy['renderer_dependencies']['pyphen']=='0.13.2'
        render.assert_not_called()
    state=op.doctor()
    assert state['privileged_external_mutation']=='NOT SUPPORTED'
    assert state['host_provider_confinement']=='NOT VERIFIED'
    with patch('shutil.which',return_value='/optional/office'), patch('office_renderer.prerequisites',return_value={'available':False}):
        assert op.doctor()['office_visual'].startswith('OPERATOR_ACTION_REQUIRED: observed local IPC')
    with patch.object(sys,'argv',['operator_actions.py','doctor']):assert op.main()==0


def test_exact_fabric_transaction_positive_decline_replay_and_tamper(tmp_path):
    import importlib.util,types,contextlib,io
    from unittest.mock import patch
    path=Path(__file__).resolve().parents[1]/'.ai/runtime/fabric/fabric.py'
    spec=importlib.util.spec_from_file_location('operator_transaction_unit',path);fabric=importlib.util.module_from_spec(spec);spec.loader.exec_module(fabric)
    fabric.FABRIC_DIR=str(tmp_path/'fabric');fabric.KEY_PATH=str(tmp_path/'unused-legacy-key')
    with contextlib.redirect_stdout(io.StringIO()):fabric.cmd_init(types.SimpleNamespace(engagement='fixture',intent='synthetic test only',owner='fixture',success='test',boundary='no external effects'))
    graph=fabric.open_fabric('fixture');fragment=graph.add_node('frag',1,'synthetic target',kind='claim')
    key=tmp_path/'synthetic-private.pem';public=tmp_path/'synthetic-public.pem'
    subprocess.run(['/usr/bin/openssl','genpkey','-algorithm','ED25519','-out',str(key)],check=True,capture_output=True)
    subprocess.run(['/usr/bin/openssl','pkey','-in',str(key),'-pubout','-out',str(public)],check=True,capture_output=True)
    trust={'public_key':public.read_text(),'key_id':op.sha(public.read_bytes())}
    with patch.object(op,'trusted_key',return_value=trust):
        for accepted in (True,False):
            request_file=tmp_path/('accept.json' if accepted else 'decline.json')
            args=types.SimpleNamespace(engagement='fixture',fragment=fragment['id'],layer=0,state='accepts',rationale='unit test only',reviewer='synthetic key',model='test',constraints=None,request_out=str(request_file))
            before=op.sha(op.regular(fabric.log_path('fixture')))
            with contextlib.redirect_stdout(io.StringIO()):assert fabric.operator_request(args,'fabric-review')==3
            assert before==op.sha(op.regular(fabric.log_path('fixture')))
            req=json.loads(request_file.read_text());body=op.response(req,accepted);body.update(key_id=trust['key_id'],assurance=op.ASSURANCE)
            payload=tmp_path/'payload';payload.write_bytes(op.canonical(body));signature=tmp_path/'signature'
            subprocess.run(['/usr/bin/openssl','pkeyutl','-sign','-inkey',str(key),'-rawin','-in',str(payload),'-out',str(signature)],check=True,capture_output=True)
            body['signature']=base64.b64encode(signature.read_bytes()).decode();receipt=tmp_path/('accept-receipt.json' if accepted else 'decline-receipt.json');receipt.write_text(json.dumps(body))
            command=types.SimpleNamespace(request=str(request_file),receipt=str(receipt))
            with contextlib.redirect_stdout(io.StringIO()):assert fabric.cmd_apply_operator(command)==(0 if accepted else 2)
            if accepted:
                graph=fabric.open_fabric('fixture');entry=next(e for e in graph.entries if 'operator_authority' in e)
                assert fabric.verify_operator_entry(entry,graph.entries)
                assert graph.authority_verified(entry['data']['id'])
                with pytest.raises(fabric.FabricError):fabric.cmd_apply_operator(command)
                altered=copy.deepcopy(entry);altered['operator_authority']['receipt']['signature']='AA=='
                with pytest.raises(ValueError):fabric.verify_operator_entry(altered,graph.entries)
            else:assert before==op.sha(op.regular(fabric.log_path('fixture')))


def test_execution_route_is_separate_from_formal_authority_and_never_executes(tmp_path):
    source=tmp_path/'page.html';source.write_text('<h1>approved project</h1>')
    before=source.read_bytes()
    plan=op.operation_plan('role-engineer','local-qa',source,tmp_path)
    assert plan['execution_route']=='A' and not plan['formal_l0_required']
    assert op.operation_plan('codebase-reviewer','workspace-edit',source,tmp_path)['state']=='DENIED'
    assert op.operation_plan('codebase-reviewer','local-qa',source,tmp_path,qa_output=tmp_path/'build/qa')['execution_route']=='A'
    assert op.operation_plan('codebase-reviewer','local-qa',source,tmp_path,qa_output=source)['state']=='DENIED'
    assert op.operation_plan('role-author','local-qa',source,tmp_path)['state']=='DENIED'
    for status,route in [('blocked','C'),('provider-requested','B')]:
        decision=op.operation_plan('role-engineer','local-qa',source,tmp_path,sandbox=status,observed_error='observed socket permission denial')
        assert decision['execution_route']==route and not decision['formal_l0_required']
        with pytest.raises(ValueError):op.operation_plan('role-engineer','local-qa',source,tmp_path,sandbox=status)
    assert op.operation_plan('role-engineer','system-install','package',tmp_path)['formal_l0_required'] is False
    assert op.operation_plan('role-engineer','formal-decision','risk',tmp_path)['formal_l0_required'] is True
    for effect in ['external-mutation','arbitrary-shell']:
        assert op.operation_plan('role-engineer',effect,source,tmp_path)['state']=='DENIED'
    assert op.operation_plan('unknown','read',source,tmp_path)['state']=='DENIED'
    assert op.operation_plan('role-engineer','workspace-edit',tmp_path/'.git/config',tmp_path)['state']=='DENIED'
    assert op.operation_plan('role-engineer','read',tmp_path.parent/'outside',tmp_path)['state']=='DENIED'
    alias=tmp_path/'alias';alias.symlink_to(source)
    assert op.operation_plan('role-engineer','local-qa',alias,tmp_path)['state']=='DENIED'
    assert op.operation_plan('role-engineer','local-qa',source,tmp_path,trust='untrusted-input')['execution_route']=='C'
    with patch('agent_runtime.contracts',side_effect=OSError('unavailable')):
        assert op.operation_plan('role-engineer','read',source,tmp_path)['state']=='DENIED'
    assert source.read_bytes()==before


def test_intervention_is_self_contained_and_command_text_is_display_only(tmp_path):
    source=tmp_path/'file with spaces.html';source.write_text('<h1>Fixture</h1>')
    req=op.request('render','Actual local screenshot/publication QA',source,tmp_path/'outputs',{'backend':'libreoffice'})
    text=op.request_message(req,tmp_path/'request.json',reason='Observed socket() failed: Operation not permitted',workdir=tmp_path)
    for label in ['CATEGORY: C','FORMAL L0: NO','PURPOSE:','WHY YOU:','COMMAND:','WORKDIR:','INPUT:','OUTPUT:','PRIVILEGES:','RISK /','AFTERWARDS:']:
        assert label in text
    assert str(source) in text and req['source']['sha256'] in text
    assert not (tmp_path/'outputs').exists()
    decision=op.request('fabric-review','Review exact decision',source,'frag-1',{})
    formal=op.request_message(decision,tmp_path/'decision.json',workdir=tmp_path)
    assert 'CATEGORY: D' in formal and 'FORMAL L0: YES' in formal and 'EXECUTION ROUTE: C' in formal
    assert 'COMMAND: NOT READY' in formal and 'private key' in formal
    arguments=dict(purpose='local QA',reason='actual provider request',workdir=str(tmp_path),inputs=str(source),outputs='image',privileges='normal user',risks='local output only, reversible; no external access',afterwards='return status and image',commands=[['printf','literal; not executed']])
    view=op.intervention_message({'execution_route':'B','formal_l0_required':False},**arguments)
    assert 'CATEGORY: B' in view and 'FORMAL L0: NO' in view and "'literal; not executed'" in view
    with pytest.raises(ValueError):op.intervention_message({'execution_route':'A'},**arguments)
    with pytest.raises(ValueError):op.intervention_message({'execution_route':'C'},**{**arguments,'commands':[]})
    with pytest.raises(ValueError):op.intervention_message({'execution_route':'C'},**{**arguments,'commands':['arbitrary shell text']})
    with pytest.raises(ValueError):op.intervention_message({'execution_route':'B','formal_l0_required':True},**arguments)
    with pytest.raises(ValueError):op.intervention_message({'execution_route':'C','formal_l0_required':True,'effect':'local-qa'},**arguments)
    changed=dict(req);changed['purpose']='tampered'
    with pytest.raises(ValueError):op.request_message(changed,tmp_path/'request.json')
