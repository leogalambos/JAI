# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Offline physical-call reservation, replay and exact member grant boundaries."""
import sys
from pathlib import Path
import time

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import governed_native_provider as provider
import governed_workflow
import governed_dispatch
import governed_invocations
import lifecycle as lc


def _workflow(tmp_path):
    store = lc.Store(tmp_path / 'invocations.jsonl', 'physical-invocations')
    limits = [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 600000}]
    deadline = int(time.time() * 1000) + 900000
    result = provider.bootstrap(store, b'Describe a bounded backup service.',
        b'Preserve restore-readiness requirements.', 'codex', 'backup', limits, deadline)
    workflow = governed_workflow.Workflow(store, result['config'])
    entry = workflow.entry('default', 'backup', limits, deadline)
    return workflow, entry['assignment']


def test_issue_batch_reserves_actual_bounded_call_once_and_cancel_replays(tmp_path):
    workflow, assignment = _workflow(tmp_path)
    issued = workflow.issue_batch([{'assignment': assignment, 'phase': 'selection'}], bound_ms=1000)
    state = workflow.store.read()
    invocation = state.invocations[issued['invocation_id']]
    assert invocation['state'] == 'issued'
    assert invocation['bound_ms'] == 1000
    assert len(invocation['members']) == 1
    member = invocation['members'][0]
    context = state.resolve(member['context'], 'context')
    assert state.run_details[context['run_id']]['invocation_id'] == invocation['invocation_id']
    assert state.run_details[context['run_id']]['member_key'] == member['member_key']
    assert state.usage[('default', 'elapsed_ms', 'ms')] == {'spent': 0, 'reserved': 1000}
    capture = workflow.store.put_blob(lc.canonical({'state': 'not-dispatched', 'observation': 'Offline fixture; no provider call was started.'}))
    facts = {'observed_at_ms': int(time.time() * 1000), 'capture_blob_id': capture,
             'reason': 'Issued work cancelled before any physical call.'}
    response = workflow.invocation_event(invocation['invocation_id'], 'invocation_cancelled', **facts)
    before = workflow.store.path.read_bytes()
    retry = workflow.invocation_event(invocation['invocation_id'], 'invocation_cancelled', **facts)
    assert retry['receipt'] == response['receipt']
    assert workflow.store.path.read_bytes() == before
    with pytest.raises(lc.ERROR) as failure:
        workflow.invocation_event(invocation['invocation_id'], 'invocation_cancelled', **{**facts, 'reason': 'Changed facts.'})
    assert failure.value.code == 'P_IDEMPOTENCY'
    state = workflow.store.read()
    assert state.usage[('default', 'elapsed_ms', 'ms')] == {'spent': 0, 'reserved': 0}
    assert state.run_states[context['run_id']] == 'cancelled'
    replay = lc.replay(state.transactions, engagement=workflow.store.engagement, blob_reader=workflow.store._blob)
    assert replay.invocations == state.invocations
    assert replay.usage == state.usage


def test_duplicate_member_job_rejects_atomically_and_traits_do_not_grant_work(tmp_path):
    workflow, assignment = _workflow(tmp_path)
    state = workflow.store.read()
    before = workflow.store.path.read_bytes()
    traits = state.invocation_traits(assignment, 'selection')
    assert traits['provider'] == 'codex'
    assert traits['responsibility'] == 'setter'
    assert not state.invocations
    with pytest.raises(governed_dispatch.DispatchError) as failure:
        workflow.issue_batch([{'assignment': assignment, 'phase': 'selection'},
                              {'assignment': assignment, 'phase': 'selection'}], bound_ms=1000)
    assert failure.value.code == 'P_CONFLICT'
    assert workflow.store.path.read_bytes() == before
    # The shared control handler rejects an unissued identity without effects.
    message = {'scope': 'default', 'payload': {'event': 'invocation_prepared',
               'invocation_id': 'not-issued', 'manifest_blob_id': '0' * 64}}
    with pytest.raises(lc.ERROR) as failure:
        governed_invocations.derive(state, message, {'kind': 'controller', 'id': 'test'},
                                   int(time.time() * 1000), True)
    assert failure.value.code == 'P_SCOPE'
