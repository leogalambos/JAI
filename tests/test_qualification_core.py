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
    pytest_command = next(args for args in commands if 'pytest' in args)
    assert any(str(path).endswith('test_commercial_proposal.py') for path in pytest_command)
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


def test_assembly_requires_complete_matching_gate_identities(tmp_path):
    output = tmp_path / 'summary.json'
    assert qualification.assemble(tmp_path, output) == 1
    for gate in 'ABCDEFG':
        (tmp_path / f'gate-{gate}.json').write_text(json.dumps({'release': (ROOT/'VERSION').read_text().strip(), 'gate': gate, 'pass': True, 'checks': [{'name': 'executed', 'state': 'PASS', 'ok': True}]}))
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
