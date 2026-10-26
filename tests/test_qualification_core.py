# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Release orchestration must propagate failed checks and retain actual evidence."""
import datetime
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import qualification_core as qualification


def test_timestamp_has_explicit_utc_timezone():
    assert datetime.datetime.fromisoformat(qualification.now()).utcoffset() == datetime.timedelta(0)


def test_governance_checks_actual_catalogue_and_detect_missing_required_role(monkeypatch):
    assert qualification.governance_check()['ok']
    monkeypatch.setattr(qualification, 'NEW_ROLES', {'unregistered-required-role'})
    assert not qualification.governance_check()['ok']


def test_every_gate_keeps_failed_checks_and_proposal_regressions(monkeypatch):
    def failed(name, args, timeout=120):
        return {'name': name, 'ok': False, 'state': 'FAIL', 'detail': '', 'args': args}
    monkeypatch.setattr(qualification, 'command', failed)
    monkeypatch.setattr(qualification, 'governance_check', lambda: {'ok': False})
    monkeypatch.setattr(qualification, 'publication_renderer_check', lambda: {'ok': False})
    groups = [qualification.gate_a(), qualification.gate_b(), qualification.gate_c(),
              qualification.gate_d(), qualification.gate_e(), qualification.gate_f(),
              qualification.gate_g()]
    assert all(group and not any(check['ok'] for check in group) for group in groups)
    commands = [check.get('args', []) for check in groups[0]]
    pytest_commands = [args for args in commands if 'pytest' in args]
    assert [Path(args[-1]).name for args in pytest_commands] == list(qualification.REGRESSION_MODULES)
    assert any(str(args[-1]).endswith('test_commercial_proposal.py') for args in pytest_commands)
    for level in ('simple', 'medium', 'complex'):
        assert any('proposal-validate' in args and any(str(a).endswith(f'proposal-{level}.json') for a in args)
                   for args in commands)


def test_payload_and_persisted_gate_cannot_hide_failed_check(tmp_path, monkeypatch):
    good = {'ok': True, 'name': 'executed', 'state': 'PASS'}
    bad = {'ok': False, 'name': 'unavailable', 'state': 'NOT_EXECUTED'}
    assert qualification.gate_payload('A', [good])['pass']
    assert not qualification.gate_payload('A', [good, bad])['pass']
    with pytest.raises(KeyError):
        qualification.gate_payload('A', [{}])
    monkeypatch.setitem(qualification.GATES, 'A', lambda: [bad])
    output = tmp_path / 'nested/gate-A.json'
    assert qualification.run_gate('A', output) == 1
    assert json.loads(output.read_text())['checks'] == [bad]
    monkeypatch.setitem(qualification.GATES, 'A', lambda: [good])
    assert qualification.run_gate('A', output) == 0
    with pytest.raises(KeyError):
        qualification.run_gate('Z', output)


def test_assembly_requires_complete_matching_gate_identities(tmp_path, monkeypatch):
    source = tmp_path/"build/source"; source.mkdir(parents=True)
    (source/"VERSION").write_text((ROOT/"VERSION").read_text())
    monkeypatch.setattr(qualification, "PACKAGE", source)
    output = tmp_path / 'summary.json'
    assert qualification.assemble(tmp_path, output) == 1
    for gate in 'ABCDEFG':
        (tmp_path / f'gate-{gate}.json').write_text(json.dumps({'release': (ROOT/'VERSION').read_text().strip(), 'gate': gate, 'pass': True, 'source_binding': qualification.source_binding(qualification.source_fingerprint(source), qualification.source_fingerprint(source)), 'checks': [{'name': 'executed', 'state': 'PASS', 'ok': True}]}))
    assert qualification.assemble(tmp_path, output) == 0
    (tmp_path / 'gate-G.json').write_text(json.dumps({'gate': 'F', 'pass': True}))
    assert qualification.assemble(tmp_path, output) == 1
    assert not json.loads(output.read_text())['all_pass']


@pytest.mark.parametrize('changes', [
    {'release': '26.10.8'}, {'release': None}, {'pass': 'true'},
    {'pass': 1}, {'checks': []}, {'checks': {}}, {'checks': [None]},
    {'checks': [{'name': 'unexecuted', 'state': 'NOT_EXECUTED', 'ok': True}]},
    {'checks': [{'name': 'failed', 'state': 'FAIL', 'ok': False}]},
    {'checks': [{'name': 'untyped', 'state': 'PASS', 'ok': 'true'}]},
    {'checks': [{'name': 'no execution state', 'ok': True}]},
])
def test_assembly_rejects_stale_or_contradictory_claims(tmp_path, changes):
    version = (ROOT/'VERSION').read_text().strip()
    for gate in 'ABCDEFG':
        report = {'release': version, 'gate': gate, 'pass': True,
                  'checks': [{'name': 'actual check', 'state': 'PASS', 'ok': True}]}
        if gate == 'G':
            report.update(changes)
        (tmp_path/f'gate-{gate}.json').write_text(json.dumps(report))
    assert qualification.assemble(tmp_path, tmp_path/'summary.json') == 1
    assert not json.loads((tmp_path/'summary.json').read_text())['all_pass']


def test_shared_gate_report_validation_requires_real_complete_execution():
    version = (ROOT/'VERSION').read_text().strip()
    good = {'release': version, 'gate': 'A', 'pass': True,
            'checks': [{'name': 'actual check', 'state': 'PASS', 'ok': True}]}
    assert qualification.gate_report_problems(good, 'A', version) == []
    assert qualification.gate_report_problems([], 'A', version)
    assert qualification.gate_report_problems(dict(good, gate='B'), 'A', version)


def test_run_all_stops_at_failed_gate_or_assembly(monkeypatch):
    called = []
    monkeypatch.setattr(qualification, 'run_gate', lambda gate: called.append(gate) or int(gate == 'B'))
    monkeypatch.setattr(qualification, 'assemble', lambda: pytest.fail('must not assemble failed gates'))
    assert qualification.run_all() == 1
    assert called == ['A', 'B']
    monkeypatch.setattr(qualification, 'run_gate', lambda gate: 0)
    monkeypatch.setattr(qualification, 'assemble', lambda: 1)
    assert qualification.run_all() == 1
    monkeypatch.setattr(qualification, 'assemble', lambda: 0)
    assert qualification.run_all() == 0


def test_cli_dispatch_and_invalid_syntax(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['qualification_core.py', 'qualify'])
    monkeypatch.setattr(qualification, 'run_all', lambda: 7)
    assert qualification.main() == 7
    monkeypatch.setattr(sys, 'argv', ['qualification_core.py', 'unknown'])
    with pytest.raises(SystemExit):
        qualification.main()


def test_regression_inventory_executes_each_module_once_under_its_own_bound(monkeypatch):
    calls = []
    def execute(name, args, timeout=120):
        calls.append((name, args, timeout))
        return {'name': name, 'ok': False, 'state': 'NOT_EXECUTED'}
    monkeypatch.setattr(qualification, 'command', execute)
    results = qualification.regression_checks()
    assert len(results) == len(qualification.REGRESSION_MODULES) == 22
    assert len(set(qualification.REGRESSION_MODULES)) == 22
    assert all(not check['ok'] and check['state'] == 'NOT_EXECUTED' for check in results)
    assert [Path(args[-1]).name for _, args, _ in calls] == list(qualification.REGRESSION_MODULES)
    assert all(timeout == 600 and args[:4] == [qualification.PY, '-u', '-m', 'pytest']
               and len(args) == 7 for _, args, timeout in calls)
    assert all(module in name for module, (name, _, _) in zip(qualification.REGRESSION_MODULES, calls))


def test_regression_cli_never_promotes_failed_or_unexecuted_modules(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['qualification_core.py', 'regression'])
    for state, ok, expected in [('PASS', True, 0), ('FAIL', False, 1), ('NOT_EXECUTED', False, 1)]:
        monkeypatch.setattr(qualification, 'regression_checks', lambda: [{'name': 'fixture', 'ok': ok, 'state': state}])
        assert qualification.main() == expected


def test_canonical_inventory_preserves_every_previously_mandatory_module():
    expected = (
        'test_content_lint.py test_content_metrics.py test_content_publication.py '
        'test_content_eval.py test_content_provider_parity.py test_content_workflow.py '
        'test_content_migrate.py test_content_calibration.py test_content_catalog.py '
        'test_content_spec.py test_content_integration.py test_expert_references.py '
        'test_optional_provider_eval.py test_evaluation_package.py test_content_scenarios.py '
        'test_offline_guard.py test_qualification_dependencies.py test_qualification_core.py '
        'test_release_ga.py test_release_bundle.py test_reference_bindings.py test_commercial_proposal.py'
    ).split()
    assert list(qualification.REGRESSION_MODULES) == expected
    assert all((ROOT / 'tests' / name).is_file() for name in expected)


def test_aggregate_budgets_cover_all_a_h_command_ceilings(monkeypatch, capsys):
    import release_ga
    timeouts = []
    def execute(name, args, timeout=120):
        timeouts.append(timeout)
        return {'name': name, 'ok': True, 'state': 'PASS'}
    monkeypatch.setattr(qualification, 'command', execute)
    monkeypatch.setattr(release_ga, 'command', execute)
    monkeypatch.setattr(qualification, 'governance_check', lambda: {'ok': True})
    monkeypatch.setattr(qualification, 'publication_renderer_check', lambda: execute('renderer', []))
    monkeypatch.setattr(release_ga, 'prep_check', lambda: {'ok': True})
    for gate in release_ga.GATES.values():
        gate()
    release_ga.h_checks(generate=True)
    execute('final policy', [])
    assert qualification.aggregate_budget('regression') == 22 * 600 + 120 == 13320
    assert qualification.aggregate_budget('qualification') >= sum(timeouts) + 120
    assert qualification.aggregate_budget('qualification') == 19920
    assert qualification.aggregate_budget('qualification') <= 21600
    with pytest.raises(ValueError, match='UNKNOWN_QUALIFICATION'):
        qualification.aggregate_budget('unknown')
    monkeypatch.setattr(sys, 'argv', ['qualification_core.py', 'budget', '--scope', 'regression'])
    assert qualification.main() == 0
    assert capsys.readouterr().out.strip() == '13320'


def test_streamed_failure_keeps_evidence_without_replaying_output(monkeypatch, capsys):
    """Live diagnostics appear once while the failure record retains evidence."""
    monkeypatch.setenv('JAI_OFFLINE_STREAM', '1')
    monkeypatch.setattr(qualification, 'run_offline', lambda *args, **kwargs: {
        'status': 'FAIL', 'returncode': 1, 'stdout': 'already-streamed-marker',
        'stderr': 'failure-detail',
    })
    result = qualification.command('streamed negative check', ['unused'])
    assert result['ok'] is False
    assert 'already-streamed-marker' in result['detail']
    assert 'failure-detail' in result['detail']
    output = capsys.readouterr().out
    assert 'FAIL streamed negative check' in output
    assert 'already-streamed-marker' not in output


def test_actual_gate_binds_source_before_and_after_and_rejects_drift(tmp_path, monkeypatch):
    source = tmp_path/'source'; source.mkdir(); (source/'VERSION').write_text('26.10.13')
    monkeypatch.setattr(qualification, 'PACKAGE', source)
    output = source/'.ai/runtime/_meta/gates/gate-A.json'
    good = {'name': 'actual fixture execution', 'ok': True, 'state': 'PASS'}
    monkeypatch.setitem(qualification.GATES, 'A', lambda: [good])
    assert qualification.run_gate('A', output) == 0
    report = json.loads(output.read_text())
    assert not qualification.binding_problems(report['source_binding'], qualification.source_fingerprint(source))
    def change_during_execution():
        (source/'fixture.txt').write_text('changed during actual executor')
        return [good]
    monkeypatch.setitem(qualification.GATES, 'A', change_during_execution)
    assert qualification.run_gate('A', output) == 1
    assert not json.loads(output.read_text())['source_binding']['stable']
    assert qualification.binding_problems(None, qualification.source_fingerprint(source))


def test_source_binding_tracks_archive_permission_bits(tmp_path):
    source = tmp_path/'runner.sh'; source.write_text('echo fixture\n')
    source.chmod(0o644)
    before = qualification.source_fingerprint(tmp_path)
    assert before == qualification.source_fingerprint(tmp_path)
    source.chmod(0o755)
    after = qualification.source_fingerprint(tmp_path)
    assert before != after
    assert qualification.binding_problems(qualification.source_binding(before, before), after)
