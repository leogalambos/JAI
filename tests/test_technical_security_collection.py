# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise the operator-facing collection path for approved local copies."""

import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
from technical_security_collection import collect_jboss_audit, prepare_collection
from technical_security_evidence import load_method_manifest

MANIFEST = ROOT / '.ai/skills/it-role-workflows/references/technical-security-evidence-methods.v1.json'
ASSET = {'id': 'server', 'product': 'JBoss EAP', 'edition': 'eap', 'version': '7.4.0',
         'deployment': 'standalone', 'source': 'inventory', 'revision': 'i1'}
XML = ('<server xmlns="urn:jboss:domain:16.0"><management><audit-log>'
       '<logger enabled="true" log-boot="false" log-read-only="${expression}"/>'
       '</audit-log><unrelated password="fixture-secret"/></management></server>')


def test_prepare_collection_uses_exact_inventory():
    manifest = load_method_manifest(MANIFEST)
    request = prepare_collection(manifest, ASSET)
    assert request['collector'] == 'jboss-standalone-management-audit'
    assert request['questions'][0]['criterion'] == 'application-server-management-account-scope'
    assert prepare_collection(manifest, {**ASSET, 'version': 'unknown'})['collector'] is None
    with pytest.raises(ValueError, match='inventory revision'):
        prepare_collection(manifest, {**ASSET, 'revision': ''})


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('field', ['raw_output', 'nested_value', 'artifacts'])
def test_operator_publication_blocks_unapproved_data(tmp_path, capsys, shared, field):
    from technical_security_collection import _normalize_collection, _publish_operator_result

    destination = tmp_path / 'result.json'
    asset = {**ASSET, 'approved_result_path': str(destination)} if shared else ASSET
    manifest = load_method_manifest(MANIFEST)
    request = prepare_collection(manifest, asset)
    result = {'request': request, 'export_sha256': 'a' * 64,
              'audit_logger_present': True,
              'audit_settings': {'enabled': True, 'log-boot': False, 'log-read-only': None}}
    if field == 'nested_value':
        result['audit_settings']['enabled'] = 'fixture-secret'
    else:
        result[field] = 'fixture-secret'
    assert _publish_operator_result(request, result, 0) == 1
    captured = capsys.readouterr()
    assert 'Evidence withheld' in captured.err
    assert repr(request['asset']) in captured.err
    assert repr(request['collector']) in captured.err
    assert 'publication-contract-violation' in captured.err
    assert 'fixture-secret' not in captured.err
    assert list(tmp_path.iterdir()) == ([destination] if shared else [])
    if shared:
        assert captured.out == ''
        assert f'Result available at {str(destination)!r}' in captured.err
        assert 'Tell JAI the run has finished as usual' in captured.err
    else:
        assert 'normal standalone result handoff' in captured.err
    returned = destination.read_bytes() if shared else captured.out.encode()
    assert b'fixture-secret' not in returned
    diagnostic = json.loads(returned)
    settings = {'log-boot': False}
    if field != 'nested_value':
        settings['enabled'] = True
    partial = {'audit_logger_present': True, 'audit_settings': settings}
    assert diagnostic == {'request': request, 'phase': 'publish-result',
                          'code': 'publication-contract-violation',
                          'schema': 'jai.technical-security-collection-diagnostic/v1',
                          'safe_partial_result': partial}
    observations, review = _normalize_collection(manifest, asset, [], diagnostic, returned)
    assert observations == []
    assert review['status'] == 'collection-failed'
    assert review['code'] == diagnostic['code']
    assert review['safe_partial_result'] == partial
    assert 'fresh result path' in review['next_action']
    diagnostic['safe_partial_result']['audit_logger_present'] = 1
    with pytest.raises(ValueError, match='Invalid partial publication result'):
        _normalize_collection(manifest, asset, [], diagnostic, json.dumps(diagnostic).encode())


def test_operator_does_not_announce_diagnostic_handoff_when_write_fails(tmp_path, capsys):
    from technical_security_collection import _publish_operator_result

    destination = tmp_path / 'existing.json'
    destination.write_text('existing result')
    asset = {**ASSET, 'approved_result_path': str(destination)}
    request = prepare_collection(load_method_manifest(MANIFEST), asset)
    assert _publish_operator_result(request, {'request': request}, 0) == 2
    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'Could not publish the result' in captured.err
    assert 'Tell JAI' not in captured.err
    assert destination.read_text() == 'existing result'


def test_collect_jboss_audit_minimizes_and_attributes_evidence(tmp_path):
    manifest = load_method_manifest(MANIFEST)
    export = tmp_path / 'standalone.xml'
    export.write_text(XML)
    result = collect_jboss_audit(manifest, ASSET, export)
    assert result['request'] == prepare_collection(manifest, ASSET)
    assert result['audit_logger_present'] is True
    assert result['audit_settings'] == {'enabled': True, 'log-boot': False, 'log-read-only': None}
    assert 'fixture-secret' not in json.dumps(result)
    with pytest.raises(ValueError, match='registered'):
        collect_jboss_audit(manifest, {**ASSET, 'version': 'unknown'}, export)
    export.write_text('<server xmlns="urn:jboss:domain:16.0"/>')
    assert not collect_jboss_audit(manifest, ASSET, export)['audit_logger_present']


@pytest.mark.parametrize('xml', [
    '<!DOCTYPE server SYSTEM "file:///unapproved"><server/>',
    '<domain/>',
    '<server xmlns="urn:jboss:domain:16.0"><management><audit-log><logger/><logger/></audit-log></management></server>',
    '<server><management><audit-log><logger enabled="true"/></audit-log></management></server>',
])
def test_operator_collection_rejects_unsafe_or_ambiguous_export(tmp_path, xml):
    source = tmp_path / 'standalone.xml'
    source.write_text(xml)
    with pytest.raises(ValueError):
        collect_jboss_audit(load_method_manifest(MANIFEST), ASSET, source)


def test_operator_cli_round_trip(tmp_path):
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(ASSET))
    export = tmp_path / 'standalone.xml'
    export.write_text(XML)
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(MANIFEST), str(inventory)]
    prepared = json.loads(subprocess.check_output(command))
    collected = json.loads(subprocess.check_output([*command, '--export', str(export)]))
    assert collected['request'] == prepared
    answer = tmp_path / 'collection.json'
    answer.write_text(json.dumps(collected))
    intake = tmp_path / 'intake.json'
    supplied = {'assets': [ASSET], 'claims': [], 'observations': []}
    intake.write_text(json.dumps(supplied))
    assess = [*command, '--intake', str(intake), '--collection', str(answer)]
    result = json.loads(subprocess.check_output(assess, timeout=10))
    assert result['collection_review']['status'] == 'requires-assessor-review'
    assert result['report_preparation']['recommendation'] == 'collect-or-reconcile-evidence'
    answer.write_text(json.dumps({**collected, 'request': {**prepared, 'asset_revision': 'stale'}}))
    stale = subprocess.run(assess, capture_output=True, text=True, timeout=10)
    assert stale.returncode != 0 and 'current request' in stale.stderr
    supplied['assets'] = [{**ASSET, 'revision': 'stale'}]
    intake.write_text(json.dumps(supplied))
    wrong_intake = subprocess.run(assess, capture_output=True, text=True, timeout=10)
    assert wrong_intake.returncode != 0 and 'exact inventory row' in wrong_intake.stderr


def test_report_preparation_requires_evidence_for_scoped_questions():
    from technical_security_collection import report_preparation

    manifest = load_method_manifest(MANIFEST)
    criterion = 'application-server-management-account-scope'
    claim = {'id': 'account', 'criterion': criterion, 'assets': ['server'],
             'receiving_duty': 'platform-owner'}
    observation = {'id': 'observation', 'criterion': criterion, 'criterion_revision': '1',
                   'assets': ['server'], 'asset_revisions': {'server': 'i1'},
                   'format': 'configuration-observation', 'format_revision': '1',
                   'source': 'reviewed configuration', 'revision': 'o1', 'status': 'deviation'}
    pending = report_preparation(manifest.assess([ASSET], [claim], []))
    assert pending['recommendation'] == 'collect-or-reconcile-evidence'
    assert pending['pending_claims'][0]['claim'] == 'account'
    assert report_preparation(manifest.assess([ASSET], [claim], [observation]))[
        'recommendation'] == 'draft-report'
    assert report_preparation(manifest.assess([], [], []))['empty_plan']



def test_local_collection_input_rejects_oversize_and_nonregular(tmp_path):
    manifest = load_method_manifest(MANIFEST)
    source = tmp_path / 'huge.xml'
    with source.open('wb') as output:
        output.truncate(4 * 1024 * 1024 + 1)
    with pytest.raises(ValueError, match='size limit'):
        collect_jboss_audit(manifest, ASSET, source)
    with pytest.raises(ValueError, match='regular local file'):
        collect_jboss_audit(manifest, ASSET, tmp_path)


def test_operator_collector_is_packaged_for_both_providers(tmp_path):
    installer = runpy.run_path(str(ROOT / 'tests/test_installer.py'))['installer']
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_text())
    house, claude, codex = [tmp_path / directory for directory in ('house', 'claude', 'codex')]
    outputs, _ = installer.desired_outputs(ROOT, ['claude', 'codex'], house, claude, codex, registry)
    assert str(house / 'tools/technical_security_collection.py') in outputs
    for provider in (claude, codex):
        reference = provider / 'skills/it-role-workflows/references/technical-security-evidence-assessment.md'
        assert b'technical_security_collection.py' in outputs[str(reference)]


@pytest.mark.skipif(os.name != "posix", reason="The standalone collector targets a POSIX host")
def test_build_operator_package_runs_with_one_file_on_host(tmp_path):
    from technical_security_collection import build_operator_package

    export = tmp_path / 'standalone.xml'
    export.write_text(XML)
    asset = {**ASSET, 'approved_configuration_path': str(export), 'private_note': 'omit-me'}
    package = tmp_path / 'operator.pyz'
    inventory = tmp_path / 'asset.json'
    inventory.write_text(json.dumps(asset))
    prepared = json.loads(subprocess.check_output([
        sys.executable, str(TOOLS / 'technical_security_collection.py'),
        str(MANIFEST), str(inventory), '--emit-script', str(package),
    ], timeout=10))
    proc = subprocess.run([sys.executable, str(package)], cwd=tmp_path, capture_output=True,
                          text=True, timeout=10, check=True)
    collected = json.loads(proc.stdout)
    assert collected['request'] == prepared['request']
    assert collected['audit_settings']['enabled'] is True
    assert 'omit-me' not in proc.stdout
    with zipfile.ZipFile(package) as archive:
        assert 'private_note' not in json.loads(archive.read('asset.json'))
    with pytest.raises(ValueError, match='network share'):
        build_operator_package(MANIFEST.read_bytes(), asset, '//remote/share/operator.pyz')
    with pytest.raises(FileExistsError):
        build_operator_package(MANIFEST.read_bytes(), asset, package)
    for path in ('relative.xml', '//remote/share/file', '/var/../file'):
        with pytest.raises(ValueError, match='local POSIX'):
            build_operator_package(MANIFEST.read_bytes(),
                                   {**asset, 'approved_configuration_path': path}, package)
    with pytest.raises(ValueError, match='registered collector'):
        build_operator_package(MANIFEST.read_bytes(), ASSET, package)


@pytest.mark.skipif(os.name != "posix", reason="The standalone collector targets a POSIX host")
def test_run_operator_package_rejects_override_and_missing_local_input(tmp_path, monkeypatch, capsys):
    from technical_security_collection import build_operator_package, run_operator_package

    export = tmp_path / 'standalone.xml'
    package = tmp_path / 'operator.pyz'
    build_operator_package(MANIFEST.read_bytes(),
                           {**ASSET, 'approved_configuration_path': str(export)}, package)
    monkeypatch.setattr(sys, 'argv', [str(package), str(tmp_path / 'other.xml')])
    with pytest.raises(SystemExit, match='without arguments'):
        run_operator_package()
    monkeypatch.setattr(sys, 'argv', [str(package)])
    assert run_operator_package() == 1
    failure = json.loads(capsys.readouterr().out)
    assert failure['phase'] == 'read-source' and failure['code'] == 'source-missing'
    assert 'export_sha256' not in failure
    export.write_text(XML)
    assert run_operator_package() == 0
    assert json.loads(capsys.readouterr().out)['audit_logger_present']


@pytest.mark.parametrize('value,conflict,changed_revision,expected', [
    ('true', False, None, 'conforming'),
    ('false', False, None, 'deviation'),
    ('${unresolved}', False, None, 'pending'),
    ('true', True, None, 'pending'),
    ('true', False, 'criterion', 'pending'),
    ('true', False, 'format', 'pending'),
])
def test_returned_audit_summary_answers_only_the_planned_configuration_question(
        tmp_path, value, conflict, changed_revision, expected):
    criterion = 'jboss-management-audit-explicitly-enabled'
    method_path = MANIFEST
    if changed_revision is not None:
        definitions = json.loads(MANIFEST.read_bytes())
        collection_key, record_key = (('criteria', criterion) if changed_revision == 'criterion'
                                      else ('evidence_formats', 'configuration-observation'))
        next(row for row in definitions[collection_key] if row['id'] == record_key)['revision'] = '2'
        method_path = tmp_path / 'method.json'
        method_path.write_text(json.dumps(definitions))
    manifest = load_method_manifest(method_path)
    source = tmp_path / 'standalone.xml'
    source.write_text(XML.replace('enabled="true"', f'enabled="{value}"'))
    collection = tmp_path / 'collection.json'
    collection.write_text(json.dumps(collect_jboss_audit(manifest, ASSET, source)))
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(ASSET))
    intake = tmp_path / 'intake.json'
    claim = {'id': 'audit', 'criterion': criterion, 'assets': ['server'],
             'receiving_duty': 'platform-owner'}
    observations = [{
        'id': 'second-source', 'criterion': criterion, 'criterion_revision': '1',
        'assets': ['server'], 'asset_revisions': {'server': 'i1'},
        'format': 'configuration-observation', 'format_revision': '1',
        'source': 'reviewed second source', 'revision': 'r1', 'status': 'deviation',
    }] if conflict else []
    intake.write_text(json.dumps({'assets': [ASSET], 'claims': [claim],
                                  'observations': observations}))
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(method_path), str(inventory), '--intake', str(intake),
               '--collection', str(collection)]
    report = json.loads(subprocess.check_output(command, timeout=10))
    assert report['claims']['audit']['status'] == expected
    assert report['collection_review']['status'] == 'requires-assessor-review'
    if changed_revision is not None:
        assert report['collection_review']['normalization_gap'] == 'unsupported-criterion-or-format-revision'
    assert report['report_preparation']['missing_mandatory_questions'] == [
        {'asset': 'server', 'criterion': 'application-server-management-account-scope'},
    ]
    if expected != 'pending':
        assert report['claims']['audit']['evidence'][0]['revision'] == report['collection_review']['collection_sha256']
    if expected == 'pending':
        persisted = json.loads(intake.read_text())
        persisted['assessment_window'] = report['assessment_window']
        intake.write_text(json.dumps(persisted))
        package = tmp_path / 'must-not-reissue.pyz'
        follow_up = json.loads(subprocess.check_output([
            *command, '--emit-follow-up', str(package), '--follow-up-result', str(tmp_path / 'new-result.json'),
        ], timeout=10))['follow_up']
        expected_action = ('resolve-method' if changed_revision is not None else
                           'ask-in-conversation' if conflict else 'request-different-evidence')
        assert follow_up['status'] == expected_action
        assert not package.exists()



@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
def test_collection_failure_is_actionable_without_becoming_evidence(tmp_path):
    from technical_security_collection import build_operator_package

    export = tmp_path / 'standalone.xml'
    package = tmp_path / 'collect-audit.pyz'
    asset = {**ASSET, 'approved_configuration_path': str(export)}
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    failed = subprocess.run([sys.executable, str(package)], capture_output=True, timeout=10)
    assert failed.returncode == 1 and not failed.stderr
    returned = tmp_path / 'returned.json'
    returned.write_bytes(failed.stdout)
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': [{
        'id': 'audit', 'criterion': 'jboss-management-audit-explicitly-enabled',
        'assets': ['server'], 'receiving_duty': 'platform-owner',
    }]}))
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(MANIFEST), str(inventory), '--intake', str(intake),
               '--collection', str(returned)]
    report = json.loads(subprocess.check_output(command, timeout=10))
    assert report['collection_review']['status'] == 'collection-failed'
    assert report['collection_review']['code'] == 'source-missing'
    assert 'configuration path' in report['collection_review']['next_action']
    assert report['claims']['audit']['status'] == 'pending'
    export.write_text(XML)
    succeeded = subprocess.run([sys.executable, str(package)], capture_output=True,
                               timeout=10, check=True)
    returned.write_bytes(succeeded.stdout)
    report = json.loads(subprocess.check_output(command, timeout=10))
    assert report['claims']['audit']['status'] == 'conforming'


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('source_available', [True, False])
def test_shared_result_is_published_once_and_ingested_in_place(tmp_path, source_available):
    from technical_security_collection import build_operator_package

    export = tmp_path / 'standalone.xml'
    if source_available:
        export.write_text(XML)
    shared = tmp_path / 'shared'
    shared.mkdir()
    destination = shared / 'attempt-1.json'
    asset = {**ASSET, 'approved_configuration_path': str(export),
             'approved_result_path': str(destination)}
    package = tmp_path / 'collect-audit.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    command = [sys.executable, str(package)]
    execution = subprocess.run(command, capture_output=True, timeout=10)
    assert execution.returncode == (0 if source_available else 1)
    assert not execution.stdout
    assert b'Tell JAI the run has finished as usual' in execution.stderr
    assert list(shared.iterdir()) == [destination]
    original = destination.read_bytes()
    assert destination.stat().st_mode & 0o777 == 0o600
    retry = subprocess.run(command, capture_output=True, timeout=10)
    assert retry.returncode == 2 and destination.read_bytes() == original
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': [{
        'id': 'audit', 'criterion': 'jboss-management-audit-explicitly-enabled',
        'assets': ['server'], 'receiving_duty': 'platform-owner',
    }]}))
    report = json.loads(subprocess.check_output([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(inventory), '--intake', str(intake), '--use-shared-result',
    ], timeout=10))
    assert report['claims']['audit']['status'] == ('conforming' if source_available else 'pending')
    assert report['collection_review']['status'] == (
        'requires-assessor-review' if source_available else 'collection-failed'
    )


def test_shared_result_rejects_configuration_overwrite():
    manifest = load_method_manifest(MANIFEST)
    asset = {**ASSET, 'approved_configuration_path': '/tmp/standalone.xml',
             'approved_result_path': '/tmp/standalone.xml'}
    with pytest.raises(ValueError, match='must differ'):
        prepare_collection(manifest, asset)


@pytest.mark.parametrize('case', ['valid', 'digest-mismatch', 'traversal', 'symlink', 'result-collision'])
def test_native_outputs_are_verified_in_the_result_directory(tmp_path, case):
    manifest = load_method_manifest(MANIFEST)
    export = tmp_path / 'standalone.xml'
    export.write_text(XML)
    directory = tmp_path / 'shared'
    directory.mkdir()
    result_path = directory / 'result.json'
    asset = {**ASSET, 'approved_result_path': str(result_path)}
    payload = b'\x00\xffnative fixture\n'
    capture = directory / 'capture.pcap'
    if case == 'symlink':
        original = tmp_path / 'outside.pcap'
        original.write_bytes(payload)
        try:
            capture.symlink_to(original)
        except OSError:
            pytest.skip('This test filesystem does not support symlinks')
    else:
        capture.write_bytes(payload)
    summary = collect_jboss_audit(manifest, asset, export)
    names = {'traversal': '../capture.pcap', 'result-collision': 'RESULT.JSON'}
    summary['artifacts'] = [{
        'filename': names.get(case, capture.name),
        'media_type': 'application/vnd.tcpdump.pcap', 'bytes': len(payload),
        'sha256': '0' * 64 if case == 'digest-mismatch' else hashlib.sha256(payload).hexdigest(),
    }]
    result_path.write_text(json.dumps(summary))
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': []}))
    run = subprocess.run([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(inventory), '--intake', str(intake), '--use-shared-result',
    ], capture_output=True, text=True, timeout=10)
    if case == 'valid':
        assert run.returncode == 0, run.stderr
        assert json.loads(run.stdout)['collection_review']['native_artifacts'] == summary['artifacts']
        assert capture.read_bytes() == payload
    else:
        assert run.returncode != 0 and not run.stdout


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('case,expected', [
    ('required', 'conforming'), ('optional', 'deviation'), ('wrong-channel', 'pending'),
    ('wrong-fingerprint', 'pending'), ('malformed', 'pending'),
])
def test_ibm_mq_operator_package_runs_only_pinned_local_inquiry(tmp_path, case, expected):
    from technical_security_collection import build_operator_package

    tool = tmp_path / 'runmqsc'
    mode = 'OPTIONAL' if case == 'optional' else 'REQUIRED'
    answer = f'CHANNEL(APP.CHANNEL) CHLTYPE(SVRCONN) SSLCIPH(CIPHER) SSLCAUTH({mode})'
    if case == 'malformed':
        answer = 'unrecognized fixture output'
    tool.write_text(
        '#!/bin/sh\n'
        '[ "$#" -eq 1 ] && [ "$1" = QM1 ] || exit 1\n'
        'IFS= read -r query && IFS= read -r end || exit 1\n'
        '[ "$query" = "DISPLAY CHANNEL(APP.CHANNEL) CHLTYPE(SVRCONN) SSLCIPH SSLCAUTH" ] '
        '&& [ "$end" = END ] || exit 1\n'
        '[ "$PWD" = "$TMPDIR" ] || exit 1\n'
        'printf %s fixture-secret > raw-sidecar\n'
        'printf %s fixture-secret > "$TMPDIR/raw-temp"\n'
        f"printf '%s\\n' '{answer}'\n"
    )
    tool.chmod(0o700)
    digest = ('0' * 64 if case == 'wrong-fingerprint' else hashlib.sha256(tool.read_bytes()).hexdigest())
    shared = tmp_path / 'handoff'
    shared.mkdir()
    result = shared / 'result.json'
    asset = {'id': 'mq', 'product': 'IBM MQ', 'edition': 'lts', 'version': '9.4.0.0',
             'deployment': 'distributed-queue-manager', 'source': 'inventory', 'revision': 'i1',
             'approved_mqsc_path': str(tool), 'approved_mqsc_sha256': digest,
             'queue_manager': 'QM1', 'channel': 'APP.CHANNEL', 'approved_result_path': str(result)}
    package = tmp_path / 'operator.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    run = subprocess.run([sys.executable, str(package)], capture_output=True, timeout=10,
                         cwd=shared, env={**os.environ, 'TMPDIR': str(shared)})
    assert run.returncode == (1 if case in {'wrong-fingerprint', 'malformed'} else 0)
    assert list(shared.iterdir()) == [result]
    assert b'fixture-secret' not in result.read_bytes() + run.stdout + run.stderr
    intake = tmp_path / 'intake.json'
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    claim = {'id': 'tls', 'criterion': 'ibm-mq-channel-client-certificate-required',
             'assets': ['mq'], 'receiving_duty': 'platform-owner',
             'channel': 'OTHER.CHANNEL' if case == 'wrong-channel' else 'APP.CHANNEL'}
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': [claim]}))
    report = json.loads(subprocess.check_output([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(inventory), '--intake', str(intake), '--use-shared-result',
    ], timeout=10))
    assert report['claims']['tls']['status'] == expected
    assert 'CIPHER' not in result.read_text()
    assert report['report_preparation']['missing_mandatory_questions'] == [
        {'asset': 'mq', 'criterion': 'messaging-channel-authorization'},
    ]


def test_ibm_mq_operator_package_rejects_command_injection_in_channel(tmp_path):
    from technical_security_collection import build_operator_package

    asset = {**ASSET, 'product': 'IBM MQ', 'edition': 'lts', 'version': '9.4.0.0',
             'deployment': 'distributed-queue-manager', 'approved_mqsc_path': '/opt/mq/bin/runmqsc',
             'approved_mqsc_sha256': '0' * 64, 'queue_manager': 'QM1', 'channel': 'BAD)\nEND'}
    with pytest.raises(ValueError, match='exact channel'):
        build_operator_package(MANIFEST.read_bytes(), asset, tmp_path / 'must-not-create.pyz')
    assert not (tmp_path / 'must-not-create.pyz').exists()


def test_intake_points_to_remaining_evidence_then_recommends_draft(tmp_path):
    manifest = load_method_manifest(MANIFEST)
    source = tmp_path / 'standalone.xml'
    source.write_text(XML)
    collection = tmp_path / 'result.json'
    collection.write_text(json.dumps(collect_jboss_audit(manifest, ASSET, source)))
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(ASSET))
    intake = tmp_path / 'intake.json'
    audit = {'id': 'audit', 'criterion': 'jboss-management-audit-explicitly-enabled',
             'assets': ['server'], 'receiving_duty': 'platform-owner'}
    account = {**audit, 'id': 'account', 'criterion': 'application-server-management-account-scope'}
    input_data = {'assets': [ASSET], 'observations': [], 'claims': [audit]}
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(MANIFEST), str(inventory), '--intake', str(intake),
               '--collection', str(collection)]
    intake.write_text(json.dumps(input_data))
    result = json.loads(subprocess.check_output(command, timeout=10))
    advice = result['report_preparation']
    assert advice['recommendation'] == 'collect-or-reconcile-evidence'
    assert advice['next_evidence_requests'][0]['receiving_duty'] == 'assessment-plan-owner'
    assert 'management accounts' in advice['next_evidence_requests'][0]['evidence_request']
    input_data['claims'].append(account)
    input_data['observations'].append({
        'id': 'reviewed-role-map', 'criterion': account['criterion'], 'criterion_revision': '1',
        'assets': ['server'], 'asset_revisions': {'server': ASSET['revision']},
        'format': 'configuration-observation', 'format_revision': '1',
        'source': 'reviewed-inventory', 'revision': 'map-1', 'status': 'conforming',
    })
    intake.write_text(json.dumps(input_data))
    result = json.loads(subprocess.check_output(command, timeout=10))
    assert result['report_preparation']['recommendation'] == 'draft-report'
    assert not result['report_preparation']['next_evidence_requests']
    assert result['collection_review']['status'] == 'requires-assessor-review'


def test_follow_up_points_to_unsupported_asset_and_exact_interface():
    from technical_security_collection import _next_evidence_requests

    manifest = load_method_manifest(MANIFEST)
    unknown = {**ASSET, 'version': 'unknown'}
    advice = _next_evidence_requests(manifest.assess([unknown], [], []), manifest)
    assert [(row['reason'], row['receiving_duty']) for row in advice] == [
        ('unsupported-scope', 'assessment-plan-owner'),
        ('no-planned-questions', 'assessment-plan-owner'),
    ]
    assert advice[0]['asset'] == 'server'

    mq = {**ASSET, 'id': 'mq', 'product': 'IBM MQ', 'edition': 'lts',
          'version': '9.4.0.0', 'deployment': 'distributed-queue-manager'}
    claim = {'id': 'joint', 'criterion': 'shared-interface-identity',
             'assets': ['server', 'mq'], 'receiving_duty': 'application-owner', 'interface': 'link-2'}
    advice = _next_evidence_requests(manifest.assess([ASSET, mq], [claim], []), manifest)
    pending = next(row for row in advice if row.get('claim') == 'joint')
    assert pending['interface'] == 'link-2'
    assert pending['receiving_duty'] == 'application-owner'


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('answer,exit_code', [
    ('available\nROLE-REVIEW-7\nHeld by the platform team\n', 0),
    ('available\n\n\n', 1),
])
def test_optional_operator_form_returns_scoped_intake_without_resolving_claim(tmp_path, answer, exit_code):
    asset = {**ASSET, 'approved_result_path': str(tmp_path / 'form-result.json')}
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    criterion = 'application-server-management-account-scope'
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(MANIFEST), str(inventory)]
    package = tmp_path / 'form.pyz'
    subprocess.check_output([*command, '--emit-script', str(package),
                             '--form-criterion', criterion], timeout=10)
    execution = subprocess.run([sys.executable, str(package)], input=answer,
                               text=True, capture_output=True, timeout=10)
    assert execution.returncode == exit_code
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': [{
        'id': 'account', 'criterion': criterion, 'assets': ['server'],
        'receiving_duty': 'platform-owner',
    }]}))
    report = json.loads(subprocess.check_output(
        [*command, '--intake', str(intake), '--use-shared-result'], timeout=10))
    assert report['claims']['account']['status'] == 'pending'
    review = report['collection_review']
    if exit_code == 0:
        assert review['operator_response']['evidence_reference'] == 'ROLE-REVIEW-7'
        assert review['status'] == 'requires-assessor-review'
    else:
        assert review['code'] == 'form-incomplete'
        assert review['status'] == 'collection-failed'


def test_operator_form_rejects_unrelated_criterion_and_requires_result_path(tmp_path):
    from technical_security_collection import build_operator_package

    path = tmp_path / 'form.pyz'
    with pytest.raises(ValueError, match='approved result path'):
        build_operator_package(MANIFEST.read_bytes(), ASSET, path,
                               form_criterion='application-server-management-account-scope')
    with pytest.raises(ValueError, match='outside the current request'):
        build_operator_package(MANIFEST.read_bytes(),
                               {**ASSET, 'approved_result_path': str(tmp_path / 'result.json')},
                               path, form_criterion='messaging-channel-authorization')
    assert not path.exists()


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
def test_failed_attempt_issues_new_package_after_correction_and_retains_prior_evidence(tmp_path):
    from technical_security_collection import build_operator_package

    source = tmp_path / 'standalone.xml'
    prior = tmp_path / 'attempt-1.json'
    next_result = tmp_path / 'attempt-2.json'
    asset = {**ASSET, 'approved_configuration_path': str(source),
             'approved_result_path': str(prior)}
    first = tmp_path / 'first.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, first)
    assert subprocess.run([sys.executable, str(first)], timeout=10).returncode == 1
    prior_bytes = prior.read_bytes()

    audit = {'id': 'audit', 'criterion': 'jboss-management-audit-explicitly-enabled',
             'assets': ['server'], 'receiving_duty': 'platform-owner'}
    account = {**audit, 'id': 'account', 'criterion': 'application-server-management-account-scope'}
    account_evidence = {'id': 'reviewed-roles', 'criterion': account['criterion'],
                        'criterion_revision': '1', 'assets': ['server'],
                        'asset_revisions': {'server': ASSET['revision']},
                        'format': 'configuration-observation', 'format_revision': '1',
                        'source': 'reviewed-role-inventory', 'revision': 'role-1',
                        'status': 'conforming'}
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'assets': [asset], 'observations': [account_evidence],
                                  'claims': [audit, account]}))
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(MANIFEST), str(inventory), '--intake', str(intake), '--use-shared-result']
    next_package = tmp_path / 'next.pyz'
    options = ['--emit-follow-up', str(next_package), '--follow-up-result', str(next_result)]
    initialized = json.loads(subprocess.check_output([*command, *options], timeout=10))
    assert initialized['follow_up']['status'] == 'persist-assessment-window'
    assert not next_package.exists()
    persisted = json.loads(intake.read_text())
    persisted['assessment_window'] = initialized['assessment_window']
    intake.write_text(json.dumps(persisted))
    blocked = json.loads(subprocess.check_output([*command, *options], timeout=10))
    assert blocked['follow_up']['status'] == 'confirm-correction'
    assert not next_package.exists()

    source.write_text(XML)
    prepared = json.loads(subprocess.check_output(
        [*command, *options, '--retry-after-correction'], timeout=10))['follow_up']
    assert prepared['status'] == 'package-issued'
    assert prepared['prior_collection_sha256'] == hashlib.sha256(prior_bytes).hexdigest()
    assert prepared['next_intake']['observations'] == [account_evidence]
    assert prepared['next_asset']['approved_result_path'] == str(next_result)
    subprocess.run([sys.executable, str(next_package)], timeout=10, check=True)
    assert prior.read_bytes() == prior_bytes
    inventory.write_text(json.dumps(prepared['next_asset']))
    intake.write_text(json.dumps(prepared['next_intake']))
    report = json.loads(subprocess.check_output(command, timeout=10))
    assert report['report_preparation']['recommendation'] == 'draft-report'
    assert report['claims']['account']['evidence'][0]['id'] == 'reviewed-roles'


def test_follow_up_does_not_repeat_collection_for_conflicting_observations():
    manifest = load_method_manifest(MANIFEST)
    criterion = 'jboss-management-audit-explicitly-enabled'
    claim = {'id': 'audit', 'criterion': criterion,
             'assets': ['server'], 'receiving_duty': 'platform-owner'}
    observation = {'id': 'first', 'criterion': criterion, 'criterion_revision': '1',
                   'assets': ['server'], 'asset_revisions': {'server': ASSET['revision']},
                   'format': 'configuration-observation', 'format_revision': '1',
                   'source': 'configuration', 'revision': 'f1', 'status': 'conforming'}
    result = manifest.assess([ASSET], [claim], [
        observation, {**observation, 'id': 'second', 'revision': 'f2', 'status': 'deviation'},
    ])
    assert result['claims']['audit']['reason'] == 'conflicting-evidence'


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('provider,entries,claim_scope,expected', [
    ('rbac', '<include><user name="account-a"/></include>', 'scope-1', 'conforming'),
    ('rbac', '<include><group name="team"/></include>', 'scope-1', 'deviation'),
    ('rbac', '<include><user name="account-a" realm="other"/></include>', 'scope-1', 'pending'),
    ('rbac', '<exclude><user name="account-a"/></exclude>', 'scope-1', 'pending'),
    ('simple', '<include><user name="account-a"/></include>', 'scope-1', 'pending'),
    ('rbac', '<include><user name="account-a"/></include>', 'other-scope', 'pending'),
    ('rbac', '</role><role xmlns="urn:other" name="Monitor">', 'scope-1', 'pending'),
])
def test_jboss_direct_role_mapping_collects_exact_account_without_resolving_effective_scope(
        tmp_path, provider, entries, claim_scope, expected):
    from technical_security_collection import build_operator_package

    source = tmp_path / 'standalone.xml'
    source.write_text(
        '<server xmlns="urn:jboss:domain:16.0"><management>'
        f'<access-control provider="{provider}"><role-mapping><role name="Monitor">'
        f'{entries}</role></role-mapping></access-control></management></server>'
    )
    output = tmp_path / 'output.json'
    asset = {**ASSET, 'approved_configuration_path': str(source),
             'approved_result_path': str(output),
             'jboss_role_mapping': {'id': 'scope-1', 'account': 'account-a', 'role': 'Monitor'}}
    package = tmp_path / 'role.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    subprocess.run([sys.executable, str(package)], check=True, timeout=10)
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    criterion = 'jboss-management-direct-role-inclusion'
    intake.write_text(json.dumps({'assets': [asset], 'claims': [{
        'id': 'role', 'criterion': criterion, 'role_mapping': claim_scope,
        'assets': ['server'], 'receiving_duty': 'platform-owner',
    }], 'observations': []}))
    report = json.loads(subprocess.check_output([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(inventory), '--intake', str(intake), '--use-shared-result',
    ], timeout=10))
    assert report['claims']['role']['status'] == expected
    assert report['report_preparation']['missing_mandatory_questions'] == [
        {'asset': 'server', 'criterion': 'application-server-management-account-scope'},
    ]
    assert 'team' not in output.read_text()


@pytest.mark.parametrize('roles,wrong_policy,expected,route', [
    (['policy', 'runtime'], False, 'conforming', 'runtime-and-policy'),
    (['policy', 'mapping', 'identity'], False, 'conforming', 'configuration-identity-and-policy'),
    (['policy', 'mapping', 'mapping'], False, 'pending', None),
    (['policy', 'runtime'], True, 'pending', None),
])
def test_effective_management_role_preserves_scope_and_exposes_alternative_evidence_routes(
        roles, wrong_policy, expected, route):
    from technical_security_collection import _next_evidence_requests

    manifest = load_method_manifest(MANIFEST)
    criterion = 'jboss-management-effective-role-policy'
    claim = {'id': 'managed-role', 'criterion': criterion, 'assets': ['server'],
             'identity_scope': 'approved-id-1', 'policy_revision': 'policy-2',
             'receiving_duty': 'platform-owner'}
    observations = [{
        'id': f'evidence-{index}', 'criterion': criterion, 'criterion_revision': '2',
        'assets': ['server'], 'asset_revisions': {'server': ASSET['revision']},
        'format': 'configuration-observation', 'format_revision': '1',
        'source': f'approved-{role}', 'revision': f'r-{index}',
        'evidence_role': role, 'identity_scope': 'approved-id-1',
        'expected_roles_sha256': '1' * 64,
        'policy_revision': 'policy-1' if wrong_policy and role == 'runtime' else 'policy-2',
        'status': 'conforming',
    } for index, role in enumerate(roles)]
    assessment = manifest.assess([ASSET], [claim], observations)
    entry = assessment['claims']['managed-role']
    assert entry['status'] == expected
    if route is not None:
        assert entry['completed_evidence_routes'] == [route]
        assert {row['evidence_role'] for row in entry['evidence']} == set(roles)
    else:
        requests = _next_evidence_requests(assessment, manifest)
        request = next(row for row in requests if row.get('claim') == 'managed-role')
        assert request['identity_scope'] == 'approved-id-1'
        assert set(request['evidence_routes'][0]['missing']) == {'runtime'}
        assert 'identity' in request['evidence_routes'][1]['missing']


def test_assessment_window_defaults_expires_and_extends_at_controlled_time():
    from datetime import datetime, timedelta, timezone
    from technical_security_collection import _assessment_window

    start = datetime(2026, 11, 25, 10, tzinfo=timezone.utc)
    initial, opened = _assessment_window(None, start, None)
    assert opened
    assert datetime.fromisoformat(initial['deadline']) == start + timedelta(minutes=30)
    boundary = start + timedelta(minutes=30)
    assert _assessment_window(initial, boundary, None) == (initial, False)
    extended, opened = _assessment_window(initial, boundary + timedelta(minutes=5), 12)
    assert opened
    assert extended['started_at'] == initial['started_at']
    assert datetime.fromisoformat(extended['deadline']) == start + timedelta(minutes=47)
    with pytest.raises(ValueError, match='positive'):
        _assessment_window(initial, boundary, 0)


def test_elapsed_window_blocks_follow_up_until_operator_extends(tmp_path):
    from datetime import datetime, timedelta, timezone

    asset = {**ASSET, 'approved_configuration_path': str(tmp_path / 'standalone.xml')}
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    now = datetime.now(timezone.utc)
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': [{
        'id': 'audit', 'criterion': 'jboss-management-audit-explicitly-enabled',
        'assets': ['server'], 'receiving_duty': 'platform-owner',
    }], 'assessment_window': {'started_at': (now - timedelta(hours=2)).isoformat(),
                             'deadline': (now - timedelta(hours=1)).isoformat()}}))
    package = tmp_path / 'next.pyz'
    command = [sys.executable, str(TOOLS / 'technical_security_collection.py'),
               str(MANIFEST), str(inventory), '--intake', str(intake),
               '--emit-follow-up', str(package), '--follow-up-result', str(tmp_path / 'next.json')]
    blocked = json.loads(subprocess.check_output(command, timeout=10))
    assert blocked['follow_up']['status'] == 'assessment-window-elapsed'
    assert not package.exists()
    resumed = json.loads(subprocess.check_output([*command, '--extend-minutes', '12'], timeout=10))
    assert resumed['follow_up']['status'] == 'package-issued'
    assert resumed['follow_up']['next_intake']['assessment_window'] == resumed['assessment_window']


def test_window_is_rechecked_after_evaluation_before_package_emission(tmp_path, monkeypatch, capsys):
    from datetime import datetime, timedelta, timezone
    import technical_security_collection as collection

    start = datetime(2026, 11, 25, 10, tzinfo=timezone.utc)
    deadline = start + timedelta(minutes=30)
    times = iter([deadline - timedelta(seconds=1), deadline])

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return next(times)

    monkeypatch.setattr(collection, 'datetime', Clock)
    asset = {**ASSET, 'approved_configuration_path': str(tmp_path / 'standalone.xml')}
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'assets': [asset], 'observations': [], 'claims': [{
        'id': 'audit', 'criterion': 'jboss-management-audit-explicitly-enabled',
        'assets': ['server'], 'receiving_duty': 'platform-owner',
    }], 'assessment_window': {'started_at': start.isoformat(), 'deadline': deadline.isoformat()}}))
    package = tmp_path / 'next.pyz'
    assert collection.main([str(MANIFEST), str(inventory), '--intake', str(intake),
                            '--emit-follow-up', str(package), '--follow-up-result',
                            str(tmp_path / 'next.json')]) == 0
    assert json.loads(capsys.readouterr().out)['follow_up']['status'] == 'assessment-window-elapsed'
    assert not package.exists()


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('case,expected', [
    ('matches-policy', 'conforming'), ('extra-role', 'deviation'),
    ('wrong-identity', 'pending'), ('wrong-digest', 'pending'), ('no-policy', 'pending'),
    ('different-policy-roles', 'pending'),
])
def test_jboss_runtime_inquiry_is_local_exact_and_requires_policy_evidence(tmp_path, case, expected):
    from technical_security_collection import build_operator_package

    tool = tmp_path / 'jboss-cli.sh'
    roles = ['Monitor', 'Operator'] if case == 'extra-role' else ['Monitor']
    identity = 'other' if case == 'wrong-identity' else 'account-a'
    response = json.dumps({'outcome': 'success', 'result': {
        'identity': {'username': identity, 'realm': 'ManagementRealm'},
        'mapped-roles': roles,
    }})
    tool.write_text(
        '#!/bin/sh\n'
        '[ "$#" -eq 4 ] && [ "$1" = --connect ] && '
        '[ "$2" = --controller=127.0.0.1:9990 ] && [ "$3" = --output-json ] '
        '&& [ "$4" = "--command=:whoami(verbose=true)" ] || exit 1\n'
        f"printf '%s\\n' '{response}'\n"
    )
    tool.chmod(0o700)
    digest = '0' * 64 if case == 'wrong-digest' else hashlib.sha256(tool.read_bytes()).hexdigest()
    result = tmp_path / 'result.json'
    asset = {**ASSET, 'approved_result_path': str(result), 'jboss_runtime_identity': {
        'cli_path': str(tool), 'cli_sha256': digest, 'port': 9990, 'username': 'account-a',
        'realm': 'ManagementRealm', 'identity_scope': 'identity-1', 'policy_revision': 'policy-3',
        'expected_roles': ['Monitor'],
    }}
    package = tmp_path / 'runtime.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    process = subprocess.run([sys.executable, str(package)], capture_output=True, timeout=10)
    assert process.returncode == (1 if case in {'wrong-identity', 'wrong-digest'} else 0)
    input_data = json.loads(result.read_text())
    assert 'mapped-roles' not in input_data
    if case == 'wrong-identity':
        assert input_data['code'] == 'jboss-identity-mismatch'
    criterion = 'jboss-management-effective-role-policy'
    claim = {'id': 'management-roles', 'criterion': criterion, 'assets': ['server'],
             'identity_scope': 'identity-1', 'policy_revision': 'policy-3',
             'receiving_duty': 'platform-owner'}
    policy = {'id': 'approved-policy', 'criterion': criterion, 'criterion_revision': '2',
              'assets': ['server'], 'asset_revisions': {'server': 'i1'},
              'format': 'configuration-observation', 'format_revision': '1',
              'identity_scope': 'identity-1', 'policy_revision': 'policy-3',
              'evidence_role': 'policy', 'source': 'reviewed-policy', 'revision': '3',
              'expected_roles_sha256': hashlib.sha256(
                  b'["Operator"]' if case == 'different-policy-roles' else b'["Monitor"]'
              ).hexdigest(),
              'status': 'conforming'}
    intake = tmp_path / 'intake.json'
    inventory = tmp_path / 'inventory.json'
    inventory.write_text(json.dumps(asset))
    intake.write_text(json.dumps({'assets': [asset], 'claims': [claim],
                                  'observations': [] if case == 'no-policy' else [policy]}))
    report = json.loads(subprocess.check_output([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(inventory), '--intake', str(intake), '--use-shared-result',
    ], timeout=10))
    assert report['claims']['management-roles']['status'] == expected
    if expected != 'pending':
        assert report['claims']['management-roles']['completed_evidence_routes'] == ['runtime-and-policy']
    if case == 'different-policy-roles':
        stored = json.loads(intake.read_text())
        stored['assessment_window'] = report['assessment_window']
        intake.write_text(json.dumps(stored))
        follow_up = tmp_path / 'must-not-reissue.pyz'
        decision = json.loads(subprocess.check_output([
            sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
            str(inventory), '--intake', str(intake), '--use-shared-result',
            '--emit-follow-up', str(follow_up), '--follow-up-result', str(tmp_path / 'next.json'),
        ], timeout=10))
        assert decision['follow_up']['status'] == 'ask-in-conversation'
        assert not follow_up.exists()



@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('case,expected', [
    ('direct', 'conforming'), ('absent', 'pending'), ('wrong-mapping', 'pending'),
    ('change-record', 'pending'), ('encoded-member', 'pending'),
    ('invalid-separator', 'pending'),
])
def test_directory_snapshot_is_bound_to_the_reviewed_configuration_mapping(tmp_path, case, expected):
    from technical_security_collection import build_operator_package

    group = 'cn=administrators,dc=example,dc=invalid'
    member = 'uid=account-a,dc=example,dc=invalid'
    source = tmp_path / 'group.ldif'
    content = f'dn: {group}\nobjectClass: groupOfNames\n'
    if case == 'change-record':
        content += 'changetype: add\n'
    if case == 'encoded-member':
        content += 'member:: ignored-fixture\n'
    elif case == 'invalid-separator':
        content += f'description: text\u2028member: {member}\n'
    elif case != 'absent':
        content += f'member: {member}\n'
    source.write_text(
        content + 'description: unrelated-fixture\n\n'
        f'dn: {member}\nuserPassword: private-fixture\n'
        'userPassword:: cHJpdmF0ZQ==\n IGZvbGRlZA==\n'
        'nThAsH;binary:: Zml4dHVyZQ==\n'
    )
    handoff = tmp_path / 'handoff'
    handoff.mkdir()
    output = handoff / 'out.json'
    asset = {**ASSET, 'approved_result_path': str(output), 'jboss_directory_membership': {
        'ldif_path': str(source), 'group_dn': group, 'member_dn': member,
        'identity_scope': 'identity-7', 'policy_revision': 'policy-2', 'source': 'approved-directory',
    }}
    package = tmp_path / 'directory.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    run = subprocess.run([sys.executable, str(package)], check=True, timeout=10,
                         capture_output=True)
    assert run.stdout == b''
    notice = run.stderr.decode()
    assert str(source) in notice
    assert str(output) in notice
    assert 'Recognized sensitive fields omitted: NThash, userPassword.' in notice
    assert list(handoff.iterdir()) == [output]
    result = json.loads(output.read_text())
    assert result.keys() == {'request', 'directory_membership_observed'}
    for value in ('unrelated-fixture', 'private-fixture', 'cHJpdmF0ZQ==', 'IGZvbGRlZA==',
                  'Zml4dHVyZQ=='):
        assert value not in output.read_text()
        assert value not in notice

    inventory = tmp_path / 'asset.json'
    inventory.write_text(json.dumps(asset))
    criterion = 'jboss-management-effective-role-policy'
    claim = {'id': 'role', 'criterion': criterion, 'assets': ['server'],
             'identity_scope': 'identity-7', 'policy_revision': 'policy-2',
             'receiving_duty': 'platform-owner'}
    normalized = {'criterion': criterion, 'criterion_revision': '2', 'assets': ['server'],
                  'asset_revisions': {'server': ASSET['revision']},
                  'format': 'configuration-observation', 'format_revision': '1',
                  'identity_scope': claim['identity_scope'], 'policy_revision': claim['policy_revision'],
                  'status': 'conforming'}
    membership = hashlib.sha256(json.dumps(
        ['approved-directory', group, member], separators=(',', ':')).encode('ascii')).hexdigest()
    observations = [
        {**normalized, 'id': 'policy', 'source': 'policy', 'revision': 'p2', 'evidence_role': 'policy'},
        {**normalized, 'id': 'rbac', 'source': 'configuration', 'revision': 'c1', 'evidence_role': 'mapping',
         'membership_scope_sha256': '0' * 64 if case == 'wrong-mapping' else membership},
    ]
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({'claims': [claim], 'assets': [asset], 'observations': observations}))
    report = json.loads(subprocess.check_output([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(inventory), '--intake', str(intake), '--use-shared-result',
    ], timeout=10))
    assert report['claims']['role']['status'] == expected
    if expected == 'conforming':
        assert report['claims']['role']['completed_evidence_routes'] == ['configuration-identity-and-policy']


@pytest.mark.skipif(os.name != 'posix', reason='The standalone collector targets a POSIX host')
@pytest.mark.parametrize('aliased', [False, True])
def test_directory_package_rejects_raw_source_inside_handoff(tmp_path, aliased):
    from technical_security_collection import build_operator_package

    shared = tmp_path / 'shared'
    shared.mkdir()
    result = shared / 'result.json'
    source_dir = shared / 'nested'
    source_dir.mkdir()
    source = source_dir / 'group.ldif'
    source.write_text('userPassword: fixture-secret\n')
    alias = tmp_path / 'alias'
    if aliased:
        alias.symlink_to(source_dir, target_is_directory=True)
    asset = {**ASSET, 'approved_result_path': str(result), 'jboss_directory_membership': {
        'ldif_path': str(alias / source.name if aliased else source),
        'group_dn': 'cn=admins,dc=invalid', 'member_dn': 'uid=operator,dc=invalid',
        'identity_scope': 'identity-1', 'policy_revision': 'policy-1', 'source': 'approved-directory',
    }}
    package = tmp_path / 'directory.pyz'
    build_operator_package(MANIFEST.read_bytes(), asset, package)
    run = subprocess.run([sys.executable, str(package)], timeout=10, capture_output=True)
    assert run.returncode == 1
    assert json.loads(result.read_bytes())['code'] == 'source-in-handoff'
    assert b'fixture-secret' not in run.stdout + run.stderr + result.read_bytes()
    assert source.read_text() == 'userPassword: fixture-secret\n'


@pytest.mark.parametrize('case', ['valid', 'empty-alerts', 'wrong-site', 'mixed-sites', 'wrong-digest', 'wrong-scope'])
def test_zap_report_intake_binds_application_release_without_resolving_platform_claims(tmp_path, case):
    report = tmp_path / 'zap.json'
    site = 'https://app.example.invalid'
    alerts = [{'pluginid': '12345', 'riskcode': '2',
               'instances': [{'attack': 'fixture-not-for-output'}]}] if case != 'empty-alerts' else []
    sites = [{'@name': 'https://other.example.invalid' if case == 'wrong-site' else site,
              'alerts': alerts}]
    if case == 'mixed-sites':
        sites.append({'@name': 'https://other.example.invalid', 'alerts': []})
    native = json.dumps({'site': sites}).encode()
    report.write_bytes(native)
    digest = '0' * 64 if case == 'wrong-digest' else hashlib.sha256(native).hexdigest()
    asset = tmp_path / 'asset.json'
    asset.write_text(json.dumps(ASSET))
    intake = tmp_path / 'intake.json'
    intake.write_text(json.dumps({
        'assets': [ASSET], 'claims': [], 'observations': [],
        'zap_report_scope': {'application': 'customer-portal', 'release': 'rc-7',
                             'assessment_ref': 'review-1', 'scope_ref': 'scope-8',
                             'asset': ASSET['id'],
                             'asset_revision': 'stale' if case == 'wrong-scope' else ASSET['revision'],
                             'site': site, 'sha256': digest},
    }))
    result = subprocess.run([
        sys.executable, str(TOOLS / 'technical_security_collection.py'), str(MANIFEST),
        str(asset), '--intake', str(intake), '--zap-report', str(report),
    ], capture_output=True, text=True, timeout=10)
    if case in ('valid', 'empty-alerts'):
        assert result.returncode == 0, result.stderr
        output = json.loads(result.stdout)
        evidence = output['application_evidence']
        assert evidence['release'] == 'rc-7'
        assert evidence['status'] == 'requires-assessor-review'
        assert evidence['alerts'] == (
            [{'plugin_id': '12345', 'risk_code': '2', 'entries': 1}] if alerts else [])
        assert output['report_preparation']['recommendation'] == 'collect-or-reconcile-evidence'
        assert 'fixture-not-for-output' not in result.stdout
        assert report.read_bytes() == native
    else:
        assert result.returncode != 0 and not result.stdout
