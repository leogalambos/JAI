# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One-step host workflow preserves actual entity choice and captured returns."""
import json
import time

import pytest

from test_governed_dispatch import _ElapsedHarness, _worker_config, _execution
import governed_workflow
import lifecycle as lc


class _GatewayHarness(_ElapsedHarness):
    def _routing_source(self):
        config, _, _ = _worker_config(self.dispatch_directory / 'gateway-worker', self,
            {'owner': self.owner(work_kind='integration')}, mode='information')
        self.route_executions['setter'] = _execution(config['workers'][0])
        return super()._routing_source()


@pytest.fixture
def gateway(tmp_path, monkeypatch):
    host = _GatewayHarness(tmp_path / 'engagement', monkeypatch, engagement='one-step-workflow')
    host.dispatch_directory, host.dispatch_case, host.dispatch_mode = tmp_path, 'workflow-gateway', None
    host.bootstrap(include_neighbor=True)
    config, _, _ = _worker_config(tmp_path / 'gateway-worker', host,
        {'owner': host.owner(work_kind='integration')}, mode='information')
    workflow = governed_workflow.Workflow(host.store, config)
    return host, workflow


def test_layer_gateway_one_step_runs_actual_selection_then_local_work(gateway):
    host, workflow = gateway
    entry = workflow.entry(host.scope, 'service-controls',
        [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}], int(time.time() * 1000) + 240000)
    reference = entry['assignment']
    state = host.store.read()
    assignment = state.resolve(reference, 'assignment')
    assert assignment['owner'] == host.owner(work_kind='integration')
    assert assignment['routing'] == {'policy': host.routing_policy}
    assert state.capability_policy(host.profile) == {'ref': host.routing_policy, 'use_scope': host.scope}
    preview = workflow.preview(reference)
    assert 'software-engineer' in preview['specialties']
    assert 'internal-it-auditor' in preview['specialties']
    selected = workflow.run(reference, 'selection')
    assert selected['completion']['status'] == 'committed', selected
    state = host.store.read()
    choice = next(ref for ref in selected['completion']['receipt']['created_versions']
                  if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
    assert lc.version_id(state.versions[choice['version_id']]) == choice['version_id']
    result = workflow.run(reference, 'work', selection=choice)
    assert result['completion']['status'] == 'committed', result
    state = host.store.read()
    assert state.assignment_states[reference['version_id']] == 'open'
    terminal = state.transactions[-1]['return_artifact']
    assert terminal is not None
    returns = [json.loads(raw) for raw in terminal.values()]
    assert all(lc.blob(raw.encode('utf-8')) == identifier for identifier, raw in terminal.items())
    returned = next(item for item in returns if item['assignment'] == reference)
    assert state.resolve(returned['context'], 'context')['assignment'] == reference
    assert state.resolve(returned['context'], 'context')['execution'] == {'phase': 'work', 'selection': choice}
    assert any(intent['message_type'] == 'information_request' for intent in returned['intents'])
    assert not any(value['kind'] == 'delivery.product' for value in state.versions.values())


def test_issue_bounds_one_process_lease_without_launching_and_rejects_phase_confusion(gateway):
    host, workflow = gateway
    deadline = int(time.time() * 1000) + 120000
    entry = workflow.entry(host.scope, 'service-controls',
        [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}], deadline)
    issued = workflow.issue(entry['assignment'], 'selection')
    state = host.store.read()
    context = state.resolve(issued['context'], 'context')
    assert context['assignment'] == entry['assignment']
    assert context['execution'] == {'phase': 'selection'}
    assert context['expires_at_ms'] <= deadline
    assert state.run_states[context['run_id']] == 'issued'
    assert state.invocations[context['run_id']]['state'] == 'issued'
    details = state.run_details[context['run_id']]
    assert 0 < details['limits'][0]['ceiling'] <= 60000
    assert state.usage[(host.scope, 'elapsed_ms', 'ms')]['reserved'] == details['limits'][0]['ceiling']
    before = host.path.read_bytes()
    for phase, selection in [('work', None), ('selection', entry['assignment']), ('invalid', None)]:
        with pytest.raises(lc.ERROR) as failure:
            workflow.issue(entry['assignment'], phase, selection)
        assert failure.value.code == 'P_SCHEMA'
        assert host.path.read_bytes() == before


def test_process_entry_cli_omits_aggregate_bounds_but_issues_a_finite_context(tmp_path, monkeypatch, capsys):
    import json
    from test_governed_local_budget import _UncappedHarness, _workflow
    host = _UncappedHarness(tmp_path / 'entry-cli', monkeypatch)
    host.bootstrap(include_neighbor=True)
    workflow = _workflow(host)
    config = tmp_path / 'entry-host-config.json'
    config.write_text(json.dumps(workflow.dispatcher.config))
    assert governed_workflow.main(['--store', str(host.path), '--engagement', host.engagement,
        '--config', str(config), 'entry', '--scope', host.scope, '--work-item', 'service-controls']) == 0
    entered = json.loads(capsys.readouterr().out)
    record = host.store.read().resolve(entered['assignment'], 'assignment')
    assert record['limits'] == [] and record['deadline_ms'] is None
    issued = workflow.issue(entered['assignment'], 'selection')
    context = host.store.read().resolve(issued['context'], 'context')
    assert type(context['expires_at_ms']) is int
    assert context['expires_at_ms'] > int(time.time() * 1000)
    assert host.store.read().local_budget_status(entered['assignment'])['deadline_ms'] is None
    current = host.store.read().local_budget_status(entered['assignment'])
    instruction = host.store.put_blob(b'Actual fixture operator: stop only this local unit.')
    workflow.stop_local_budget(current['unit_id'], current['revision'], 'unit',
                               'Stop this one unit without claiming remote termination.', instruction)
    state = host.store.read()
    assert state.local_budget_status(entered['assignment'])['state'] == 'terminated'
    assert state.run_states[context['run_id']] == 'issued'
    assert state._status(entered['assignment'], host.scope)['validity'] == 'valid'
    assert not any(event['kind'] in {'accept', 'release'} for event in state.events)
    before = host.path.read_bytes()
    with pytest.raises(ValueError) as denied:
        workflow.issue(entered['assignment'], 'selection')
    assert denied.value.code == 'P_STATE'
    assert host.path.read_bytes() == before
    unrelated, _ = host.assignment('unrelated-cli-work', 'setter', owner=host.owner(work_item='foreign-service'))
    assert workflow.issue(unrelated, 'selection')['context'] != issued['context']
