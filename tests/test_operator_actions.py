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


def test_real_ed25519_verification_tamper_cross_request_and_decline(tmp_path,monkeypatch):
    # Disposable synthetic crypto fixture ONLY; production trust is not patched
    # by the application, and this is not evidence of a real operator action.
    from lifecycle_fixtures import SyntheticOperator
    signer=SyntheticOperator(tmp_path,monkeypatch)
    source=tmp_path/'ledger';source.write_text('fixture')
    req=op.request('fabric-review','fixture',source,'frag-1',{})
    receipt=signer.sign(req)
    assert op.verify_receipt(req,receipt)['accepted']
    assert not op.verify_receipt(req,signer.sign(req,accepted=False))['accepted']
    altered=dict(receipt,accepted=False)
    with pytest.raises(ValueError):op.verify_receipt(req,altered)
    other=op.request('fabric-review','other',source,'frag-2',{})
    with pytest.raises(ValueError):op.verify_receipt(other,receipt)
    signer.trust['capabilities']=['lifecycle-update']
    with pytest.raises(ValueError,match='capability'):op.verify_receipt(req,receipt)
    with patch.object(op,'trusted_key',side_effect=ValueError('missing protected trust')):
        with pytest.raises(ValueError):op.verify_receipt(req,receipt)
    with patch.object(op.sys.stdin,'isatty',return_value=False):
        with pytest.raises(ValueError):op.sign(req,signer.private)


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
    with patch.object(importlib.metadata, 'version', return_value='0.13.2'), patch('importlib.util.find_spec', return_value=True), patch('office_renderer.html_pdf', side_effect=RuntimeError('fixture rendering failure')) as render:
        legacy=op.doctor()
        assert legacy['html_pdf'].startswith('UNAVAILABLE: actual HTML conversion failed')
        assert legacy['renderer_dependencies']['pyphen']=='0.13.2'
        render.assert_called_once()
    state=op.doctor()
    assert state['privileged_external_mutation']=='NOT SUPPORTED'
    assert state['host_provider_confinement']=='NOT VERIFIED'
    with patch('shutil.which',return_value='/optional/office'), patch('office_renderer.prerequisites',return_value={'available':False}):
        assert op.doctor()['office_visual'].startswith('OPERATOR_ACTION_REQUIRED: observed local IPC')
    with patch.object(sys,'argv',['operator_actions.py','doctor']):assert op.main()==0


def test_exact_fabric_transaction_positive_decline_replay_and_tamper(tmp_path,monkeypatch):
    import importlib.util,types,contextlib,io
    from lifecycle_fixtures import accepted_graph
    path=Path(__file__).resolve().parents[1]/'.ai/runtime/fabric/fabric.py'
    spec=importlib.util.spec_from_file_location('operator_transaction_unit',path);fabric=importlib.util.module_from_spec(spec);spec.loader.exec_module(fabric)
    with contextlib.redirect_stdout(io.StringIO()):
        graph,fragment_id,signer=accepted_graph(fabric,tmp_path,monkeypatch,'Synthetic exact target',
            engagement='fixture',acceptance_state=None)
    fragment=graph.nodes[fragment_id]
    assert graph.lifecycle.evaluate(fragment['version_id'])['eligible']
    assert not graph.lifecycle.evaluate(fragment['version_id'],release=True)['eligible']
    for accepted in (False,True):
        request_file=tmp_path/('accept.json' if accepted else 'decline.json')
        args=types.SimpleNamespace(engagement='fixture',fragment=fragment['id'],layer=0,state='accepts',rationale='unit test only',reviewer='synthetic key',model='test',constraints=None,request_out=str(request_file))
        before=op.sha(op.regular(fabric.log_path('fixture')))
        with contextlib.redirect_stdout(io.StringIO()):assert fabric.operator_request(args,'fabric-review')==3
        assert before==op.sha(op.regular(fabric.log_path('fixture')))
        req=json.loads(request_file.read_text())
        receipt=tmp_path/('accept-receipt.json' if accepted else 'decline-receipt.json')
        receipt.write_text(json.dumps(signer.sign(req,accepted=accepted)))
        command=types.SimpleNamespace(request=str(request_file),receipt=str(receipt))
        with contextlib.redirect_stdout(io.StringIO()):assert fabric.cmd_apply_operator(command)==(0 if accepted else 2)
        if accepted:
            graph=fabric.open_fabric('fixture');transaction=graph.transactions[-1]
            assert fabric.verify_lifecycle_proof(transaction,graph.transactions[:-1])
            review=next(node for node in graph.nodes.values() if node['layer']==0)
            assert graph.authority_verified(review['id'])
            assert graph.lifecycle.evaluate(fragment['version_id'],release=True)['eligible']
            with pytest.raises(fabric.FabricError):fabric.cmd_apply_operator(command)
            altered=copy.deepcopy(transaction);altered['proof']['receipt']['signature']='AA=='
            with pytest.raises(ValueError):fabric.verify_lifecycle_proof(altered,graph.transactions[:-1])
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


def test_inventory_reports_probe_diagnostics_and_ten_second_budget():
    failed = subprocess.CompletedProcess([], 7, stdout='partial version', stderr='startup failed')
    with patch('shutil.which', return_value='/optional/tool'), patch.object(op.subprocess, 'run', return_value=failed) as run:
        item = op.tool_inventory()['office']
    assert item['command'] == ['/optional/tool', '--version']
    assert item['timeout_seconds'] == 10
    assert item['returncode'] == 7
    assert item['stdout'] == 'partial version'
    assert item['stderr'] == 'startup failed'
    assert item['duration_seconds'] >= 0
    assert item['reason'] == 'Probe exited with code 7'
    assert all(call.kwargs['timeout'] == 10 for call in run.call_args_list)
    with patch('shutil.which', return_value='/optional/tool'), patch.object(op.subprocess, 'run', side_effect=subprocess.TimeoutExpired('probe', 10, output=b'partial', stderr=b'pending')):
        item = op.tool_inventory()['office']
    assert item['reason'] == 'TimeoutExpired'
    assert item['stdout'] == 'partial'
    assert item['stderr'] == 'pending'
    assert item['returncode'] is None


def test_configure_preserves_environment_and_doctor_failure_diagnostics():
    failed = subprocess.CompletedProcess([], 2, stdout='partial doctor', stderr='native library missing')
    with patch('shutil.which', return_value=None), patch.object(op.subprocess, 'run', return_value=failed), patch.dict(op.os.environ, {'PATH': '/fixture/bin', 'SECRET_FIXTURE': 'must-not-report'}):
        report = op.configure()
    assert report['environment']['path'] == '/fixture/bin'
    assert report['environment']['python_prefix'] == sys.prefix
    assert 'SECRET_FIXTURE' not in json.dumps(report)
    assert report['doctor_probe']['stderr'] == 'native library missing'
    assert report['doctor_probe']['returncode'] == 2


def test_doctor_reports_underlying_html_error_and_optional_setup():
    import importlib.metadata
    with patch.object(importlib.metadata, 'version', return_value='0.17.2'), patch('importlib.util.find_spec', return_value=True), patch('office_renderer.html_pdf', side_effect=RuntimeError('native renderer failed')):
        state = op.doctor()
    assert state['html_pdf_diagnostic']['type'] == 'RuntimeError'
    assert state['html_pdf_diagnostic']['message'] == 'native renderer failed'
    assert any('optional' in notice.lower() for notice in state['setup_notices'])


def test_inventory_real_executable_preserves_both_output_streams(tmp_path):
    executable = tmp_path / 'claude'
    executable.write_text('#!/bin/sh\nprintf "fixture version\\n"\nprintf "fixture warning\\n" >&2\nexit 4\n')
    executable.chmod(0o755)
    with patch.dict(op.os.environ, {'PATH': str(tmp_path)}):
        report = op.tool_inventory()
    item = report['claude']
    assert item['executable'] == str(executable)
    assert item['stdout'] == 'fixture version\n'
    assert item['stderr'] == 'fixture warning\n'
    assert item['returncode'] == 4
    assert item['status'] == 'UNAVAILABLE'
    assert report['office']['executable'] is None
    assert report['office']['searched_names'] == ['libreoffice', 'soffice']


def test_configure_parses_complete_doctor_json_before_bounding_diagnostics():
    payload = {'base_workflow': 'READY', 'html_pdf_diagnostic': {'message': 'x' * 8000}}
    completed = subprocess.CompletedProcess([], 0, json.dumps(payload), '')
    with patch('shutil.which', return_value=None), patch.object(op.subprocess, 'run', return_value=completed):
        report = op.configure()
    assert report['capabilities'] == payload
    assert len(report['doctor_probe']['stdout']) == 8000
    assert report['doctor_probe']['output_truncated'] is True


def test_doctor_preserves_chained_native_renderer_failure():
    import importlib.metadata
    def failed_renderer(*args, **kwargs):
        try:
            raise ImportError('cannot load /fixture/native.dylib')
        except ImportError as exc:
            raise RuntimeError('WeasyPrint dependencies unavailable in this interpreter') from exc
    with patch.object(importlib.metadata, 'version', return_value='0.17.2'), patch('importlib.util.find_spec', return_value=True), patch('office_renderer.html_pdf', side_effect=failed_renderer):
        report = op.doctor()
    assert report['html_pdf_diagnostic']['chain'][1]['type'] == 'ImportError'
    assert '/fixture/native.dylib' in report['html_pdf_diagnostic']['chain'][1]['message']


@pytest.mark.parametrize('pyphen', ['0.13.2', '0.17.2', None])
def test_doctor_uses_conversion_not_pyphen_version_as_readiness_gate(pyphen):
    import importlib.metadata
    def version(name):
        if name == 'pyphen':
            if pyphen is None:
                raise importlib.metadata.PackageNotFoundError(name)
            return pyphen
        return '70.0'
    def render(source, directory, backend):
        result = Path(directory) / 'fixture.pdf'
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_bytes(b'%PDF-fixture')
        return result
    with patch.object(importlib.metadata, 'version', side_effect=version), patch('importlib.util.find_spec', return_value=True), patch('office_renderer.html_pdf', side_effect=render):
        report = op.doctor()
    assert report['html_pdf'].startswith('READY: actual WeasyPrint')
    assert report['renderer_dependencies']['pyphen'] == (pyphen or 'not installed')
    assert report['setup_notices'] == []


def test_doctor_distinguishes_weasyprint_cli_from_python_module():
    with patch('importlib.util.find_spec', return_value=None), patch('shutil.which', side_effect=lambda name: '/fixture/weasyprint' if name == 'weasyprint' else None):
        report = op.doctor()
    assert report['renderer_dependencies']['weasyprint_executable'] == '/fixture/weasyprint'
    assert any('CLI found' in notice for notice in report['setup_notices'])
    assert not report['html_pdf'].startswith('READY')


def _controlled_weasyprint_cli(tmp_path, version='70.0', render_exit=0):
    # This executable is a synthetic edge collaborator, never native renderer evidence.
    executable = tmp_path / 'weasyprint'
    executable.write_text(
        '#!' + sys.executable + '\n'
        'import pathlib, sys\n'
        'if sys.argv[1:] == ["--version"]:\n'
        f'    print("WeasyPrint version {version}")\n'
        '    raise SystemExit(0)\n'
        'assert sys.argv[1:3] == ["--allowed-protocols", ""]\n'
        'assert "--no-http-redirects" in sys.argv\n'
        'assert "--fail-on-http-errors" in sys.argv\n'
        'assert "JAI renderer capability check" in sys.stdin.read()\n'
        f'if {render_exit}: raise SystemExit({render_exit})\n'
        'pathlib.Path(sys.argv[-1]).write_bytes(b"%PDF-synthetic-fixture")\n'
    )
    executable.chmod(0o755)
    return str(executable)


@pytest.mark.parametrize('platform_label', ['linux', 'darwin', 'win32'])
def test_doctor_controlled_cli_selection_provenance_for_simulated_platform_labels(tmp_path, platform_label):
    executable = _controlled_weasyprint_cli(tmp_path)
    with patch.object(op.sys, 'platform', platform_label), patch('importlib.util.find_spec', return_value=None), patch('shutil.which', side_effect=lambda name: executable if name == 'weasyprint' else None):
        report = op.doctor()
    assert report['html_pdf'].startswith('READY: actual WeasyPrint')
    selected = report['renderer_dependencies']['selected_renderer']
    assert selected['execution'] == 'cli'
    assert selected['executable'] == executable
    assert selected['version'] == '70.0'
    assert selected['python'] is None and selected['pyphen'] is None


@pytest.mark.parametrize('state', ['absent', 'unqualified', 'conversion-failed'])
def test_doctor_controlled_cli_rejects_missing_unqualified_and_failed_rendering(tmp_path, state):
    executable = None if state == 'absent' else _controlled_weasyprint_cli(
        tmp_path, version='69.0' if state == 'unqualified' else '70.0',
        render_exit=7 if state == 'conversion-failed' else 0)
    with patch('importlib.util.find_spec', return_value=None), patch('shutil.which', side_effect=lambda name: executable if name == 'weasyprint' else None):
        report = op.doctor()
    assert not report['html_pdf'].startswith('READY')
    assert 'selected_renderer' not in report['renderer_dependencies']
    if state != 'absent':
        assert report['html_pdf'].startswith('UNAVAILABLE: actual HTML conversion failed')
        diagnostic = report['html_pdf_diagnostic']['message']
        assert ('version not qualified' if state == 'unqualified' else 'exit=7') in diagnostic


def test_real_qualified_weasyprint_cli_integration_reports_conversion_provenance():
    import re
    import shutil
    executable = shutil.which('weasyprint')
    if executable is None:
        pytest.skip('Core-only environment: optional WeasyPrint CLI absent; full qualification requires real renderer checks')
    probe = subprocess.run([executable, '--version'], capture_output=True, text=True, timeout=10)
    if probe.returncode or re.fullmatch(r'WeasyPrint(?: version)?\s+(70(?:\.[0-9]+)*)', probe.stdout.strip()) is None:
        pytest.skip('Core-only environment: optional CLI is not qualified WeasyPrint 70; full qualification requires real renderer checks')
    # A qualified available renderer must really convert; failure is never skipped.
    report = op.doctor()
    assert report['html_pdf'].startswith('READY: actual WeasyPrint')
    selected = report['renderer_dependencies']['selected_renderer']
    assert selected['execution'] == 'cli'
    assert selected['executable'] == executable
    assert selected['version'].split('.')[0] == '70'
    assert selected['python'] is None and selected['pyphen'] is None


def test_macos_setup_notice_explains_uniform_cli_first_selection():
    with patch.object(op.sys,'platform','darwin'), patch('importlib.util.find_spec',return_value=None), patch('office_renderer.html_pdf',side_effect=RuntimeError('fixture conversion error')):
        report=op.doctor()
    notice=next(item for item in report['setup_notices'] if item.startswith('macOS:'))
    assert 'CLI' in notice and 'automatically' in notice
    assert 'brew install weasyprint' in notice
    assert 'optional' in notice and 'no venv' in notice


def test_doctor_exception_chain_retains_timeout_streams():
    timeout=subprocess.TimeoutExpired('fixture',20,output=b'partial render',stderr=b'native loading')
    error=RuntimeError('CLI timeout');error.__cause__=timeout
    with patch('shutil.which',return_value='/fixture/weasyprint'), patch('office_renderer.html_pdf',side_effect=error):
        report=op.doctor()
    cause=report['html_pdf_diagnostic']['chain'][1]
    assert cause['stdout']=='partial render'
    assert cause['stderr']=='native loading'


@pytest.mark.parametrize('version,compatible',[('4.23.0',False),('4.26.0',True),('4.99.0',True),('5.0.0',False),('invalid',None)])
def test_doctor_reports_runtime_validator_version_compatibility(version,compatible):
    with patch('importlib.util.find_spec',side_effect=lambda name:True if name=='jsonschema' else None), patch('importlib.metadata.version',return_value=version), patch('shutil.which',return_value=None):
        report=op.doctor()
    dependency=report['runtime_dependencies']['jsonschema']
    assert dependency['available'] is True
    assert dependency['compatible'] is compatible
    assert dependency['version']==version
    if not compatible:
        assert 'OPERATOR_ACTION_REQUIRED' in report['base_workflow']
        assert 'installation complete' in report['base_workflow']
