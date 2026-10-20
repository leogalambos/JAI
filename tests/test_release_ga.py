# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""GA qualification cannot relabel stale evidence or bypass failed execution."""
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'.ai/runtime/tools'))
import release_ga as ga


def prepared(tmp_path, monkeypatch):
    version = (ROOT/'VERSION').read_text().strip()
    (tmp_path/'VERSION').write_text(version+'\n')
    summary = {'release': version, 'all_pass': True, 'gates': {}, 'checks': {}}
    for gate in 'ABCDEFG':
        checks = [{'name': 'executed fixture', 'ok': True, 'state': 'PASS'}]
        report = {'release': version, 'gate': gate, 'pass': True, 'checks': checks}
        (tmp_path/f'gate-{gate}.json').write_text(json.dumps(report))
        summary['gates'][gate] = True
        summary['checks'][gate] = checks
    ag = tmp_path/'summary.json'
    ag.write_text(json.dumps(summary))
    monkeypatch.setattr(ga, 'PACKAGE', tmp_path)
    monkeypatch.setattr(ga, 'AG', ag)
    for name in ('SBOM.spdx.json', 'COMPATIBILITY.json', 'PROVENANCE.json'):
        (tmp_path/name).write_text('{}')
    return summary


@pytest.mark.parametrize('changes', [
    {'release': '26.10.8'}, {'release': None}, {'pass': 'true'},
    {'pass': 1}, {'checks': []}, {'checks': [None]},
    {'checks': [{'name': 'missing', 'ok': True, 'state': 'NOT_EXECUTED'}]},
    {'checks': [{'name': 'failed', 'ok': False, 'state': 'FAIL'}]},
    {'checks': [{'name': 'untyped', 'ok': 'true', 'state': 'PASS'}]},
])
def test_ga_assembly_rejects_invalid_or_contradictory_gate_evidence(tmp_path, monkeypatch, changes):
    prepared(tmp_path, monkeypatch)
    path = tmp_path/'gate-G.json'
    report = json.loads(path.read_text()); report.update(changes)
    path.write_text(json.dumps(report))
    assert ga.assemble(tmp_path, tmp_path/'out.json') == 1
    assert not json.loads((tmp_path/'out.json').read_text())['all_pass']


def test_ga_assembly_accepts_only_complete_current_executed_evidence(tmp_path, monkeypatch):
    prepared(tmp_path, monkeypatch)
    assert ga.assemble(tmp_path, tmp_path/'out.json') == 0
    (tmp_path/'gate-G.json').unlink()
    assert ga.assemble(tmp_path, tmp_path/'out.json') == 1


def test_h_rechecks_summary_instead_of_relabelling_it(tmp_path, monkeypatch):
    summary = prepared(tmp_path, monkeypatch)
    assert ga.prep_check()['ok']
    passed = [{'name': 'actual H check', 'state': 'PASS', 'ok': True}]
    assert ga.write_final(passed)['all_pass']
    summary['release'] = '26.10.8'
    ga.AG.write_text(json.dumps(summary))
    assert not ga.prep_check()['ok']
    assert not ga.write_final(passed)['all_pass']
    summary['release'] = (tmp_path/'VERSION').read_text().strip()
    summary['checks']['A'][0]['state'] = 'NOT_EXECUTED'
    ga.AG.write_text(json.dumps(summary))
    assert not ga.write_final(passed)['all_pass']
    ga.AG.unlink()
    assert not ga.prep_check()['ok']


def test_gate_wrappers_retain_failures_and_current_identity(tmp_path, monkeypatch):
    prepared(tmp_path, monkeypatch)
    failed = {'name': 'fixture failure', 'ok': False, 'state': 'FAIL'}
    for name in 'abcdefg':
        monkeypatch.setattr(ga.core, 'gate_'+name, lambda: [dict(failed)])
    monkeypatch.setattr(ga, 'command', lambda *args, **kwargs: dict(failed))
    for checks in (ga.gate_a(), ga.gate_b(), ga.gate_c(), ga.gate_d(),
                   ga.gate_e(), ga.gate_f(), ga.gate_g()):
        assert checks and all(not item['ok'] for item in checks)
    assert not ga.gate_payload('A', [failed])['pass']
    monkeypatch.setitem(ga.GATES, 'A', lambda: [dict(failed)])
    assert ga.run_gate('A', tmp_path/'result.json') == 1
    assert not json.loads((tmp_path/'result.json').read_text())['pass']
    with pytest.raises(KeyError):
        ga.run_gate('Z')
    assert len(ga.generate_release_evidence()) == 3
    monkeypatch.setattr(ga, 'prep_check', lambda: dict(failed))
    assert all(not check['ok'] for check in ga.h_checks(generate=False))


def test_h_final_policy_failure_and_release_sequence_remain_blocking(tmp_path, monkeypatch):
    prepared(tmp_path, monkeypatch)
    passed = {'name': 'H fixture', 'ok': True, 'state': 'PASS'}
    monkeypatch.setattr(ga, 'h_checks', lambda generate: [dict(passed)])
    monkeypatch.setattr(ga, 'command', lambda *args: {'name': 'final policy', 'ok': False, 'state': 'FAIL'})
    assert ga.run_h() == 1
    called = []
    monkeypatch.setattr(ga, 'run_gate', lambda gate: called.append(gate) or int(gate == 'B'))
    assert ga.run_all() == 1
    assert called == ['A', 'B']
    monkeypatch.setattr(ga, 'run_gate', lambda gate: 0)
    monkeypatch.setattr(ga, 'assemble', lambda: 0)
    assert ga.run_all(through_g=True) == 0


def test_cli_and_command_use_existing_offline_execution(monkeypatch):
    result = ga.command('unavailable executable', ['jai-nonexistent-release-fixture'])
    assert not result['ok'] and result['state'] == 'NOT_EXECUTED'
    monkeypatch.setattr(sys, 'argv', ['release_ga.py', 'qualify', '--through-g'])
    monkeypatch.setattr(ga, 'run_all', lambda through_g: 7 if through_g else 8)
    assert ga.main() == 7
    monkeypatch.setattr(sys, 'argv', ['release_ga.py', 'unknown'])
    with pytest.raises(SystemExit):
        ga.main()
