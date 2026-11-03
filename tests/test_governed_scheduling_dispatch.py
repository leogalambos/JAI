# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One actual quiet cancellation and signed speculative continuation history."""
from concurrent.futures import ThreadPoolExecutor
import json
from threading import Event
import time

import pytest

from governed_fixtures import GovernedHarness, delivery
from governed_scheduling_fixtures import (
    SchedulingHarness, WORKERS, worker, signed_grant, owner_resolution, reconciliation, local_conflict,
)
from governed_stage_checkpoint import save_checkpoint
import lifecycle as lc
import governed_dispatch
import governed_workflow


class _NativeSchedulingHarness(SchedulingHarness):
    def _routing_source(self):
        execution = worker(WORKERS / 'scheduling_worker.py')
        self.route_executions['author'] = {'provider': execution['provider'], 'argv': execution['argv'],
            'files': [{key: item[key] for key in ('name', 'sha256')} for item in execution['files']]}
        return GovernedHarness._routing_source(self)


def test_quiet_run_is_cancelled_then_exact_l0_grant_executes_real_pending_work(tmp_path, monkeypatch):
    host = _NativeSchedulingHarness(tmp_path, monkeypatch, engagement='native-pause-speculation')
    host.bootstrap(include_neighbor=True)
    actor = host.setup_author(suffix='native-author', author_token_limit=10000, start_author=False)
    conflict = local_conflict(host, suffix='native-conflict')
    escalation_actor = host.setup_author(suffix='native-escalation', responsibility='integrator', work_kind='integration')
    episode, _ = host.product('native-quiet-episode', escalation_actor, kind='escalation',
        related=[{'slot_id': 'conflicts', 'refs': [conflict]}],
        episode={'root': None, 'previous': None, 'collection_head': host._proposal_head(),
                 'unfinished': [actor['author']], 'decisive': True})
    escalation = host.message('escalation', {'assignment': escalation_actor['author'], 'package': episode,
        'conflicts': [conflict], 'affected': [actor['author']],
        'requested_decisions': ['The actual owner must assess the paused native branch.']},
        sender=escalation_actor['principal'], context=escalation_actor['author_context'])
    config = {'protocol': 'jai.host-dispatch/1',
              'workers': [worker(WORKERS / 'scheduling_worker.py'), worker(WORKERS / 'selection_worker.py')],
              'destinations': [], 'tools': [],
              'limits': {'packet_bytes': 1000000, 'total_bytes': 4000000}}
    consumer = governed_workflow.Workflow(host.store, config)
    quiet = Event()
    write = consumer.dispatcher._write

    def observe_real_handshake(process, raw, deadline):
        result = write(process, raw, deadline)
        frame = json.loads(raw)
        if frame.get('id') == 'quiet-ready' and frame.get('ok') is True:
            quiet.set()
        return result

    monkeypatch.setattr(consumer.dispatcher, '_write', observe_real_handshake)
    save_checkpoint(tmp_path / 'normal-stage.json', host, consumer, actor['author'], stage='normal-quiet-author')
    chosen = consumer.run(actor['author'], 'selection')
    state = host.store.read()
    choice = next(reference for reference in chosen['completion']['receipt']['created_versions']
                  if state.versions[reference['version_id']]['kind'] == 'delivery.decision')
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=1) as executor:
        running = executor.submit(consumer.run, actor['author'], 'work', choice)
        assert quiet.wait(timeout=10), 'The actual broker handshake was not observed'
        escalation['expected_head'] = host.store.read().head
        escalation['message_id'] = delivery.message_id(escalation)
        host.commit(escalation)
        with pytest.raises((governed_dispatch.DispatchError, lc.ERROR)) as cancelled:
            running.result(timeout=10)
    elapsed = time.monotonic() - started
    state = host.store.read()
    normal = [value['content']['record'] for value in state.versions.values()
              if value['kind'] == 'delivery.context'
              and value['content']['record']['assignment'] == actor['author']
              and value['content']['record']['execution']['phase'] == 'work'
              and value['content']['record']['speculation'] is None]
    assert len(normal) == 1
    assert state.run_states[normal[0]['run_id']] == 'cancelled'
    assert state.run_details[normal[0]['run_id']]['usage']['elapsed_ms:ms'] > 0
    assert cancelled.value.code == 'P_STATE', 'A governed pause must cancel, not wait for execution expiry'
    assert elapsed > 0
    assert state.assignment_states[actor['author']['version_id']] == 'paused'
    grant, _, _ = signed_grant(host, episode, [actor['author']], ceiling=10000, consumer=consumer)
    readiness = consumer.ready(speculation=grant)
    assert next(item for item in readiness if item['assignment'] == actor['author'])['ready']
    driven = consumer.drive(2, speculation=grant)
    assert driven['status'] == 'waiting'
    assert next(item for item in readiness if item['assignment'] == actor['author'])['phase'] == 'work'
    assert [step['phase'] for step in driven['steps']] == ['work']
    assert all(step['result']['completion']['status'] == 'committed' for step in driven['steps'])
    state = host.store.read()
    result = next(state._reference(identifier) for identifier, value in state.versions.items()
                  if value['logical_id'] == 'actual-speculative-native-answer')
    assert state.resolve(result)['assignment'] == actor['author']
    assert (host.scope, result['version_id']) in state.holds
    assert not state.evaluate(result)['qualified'] and not state.evaluate(result)['accepted']
    assert consumer.attempt_status(actor['setter'])['outcome'] is None
    resolution = owner_resolution(host, episode)
    payload = reconciliation(host, episode, resolution)
    assert consumer.submit_decision(consumer.prepare_decision(payload)['message'])['status'] == 'committed'
    state = host.store.read()
    assert not state.holds
    assert state.assignment_states[actor['author']['version_id']] == 'completed'
    assert not state.evaluate(result)['qualified'] and not state.evaluate(result)['accepted']
    assert state.usage[(host.scope, 'elapsed_ms', 'ms')]['reserved'] == 0
    assert consumer.step(speculation=grant)['status'] == 'waiting'
