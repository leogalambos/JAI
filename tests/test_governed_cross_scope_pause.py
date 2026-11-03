# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Pause follows actual scoped dependencies, not blob equality or scope names."""
import time

import pytest

from governed_scheduling_fixtures import SchedulingHarness, workflow, local_conflict
import lifecycle as lc
from governed_dispatch import DispatchError


def _episode_affecting(host, affected, suffix):
    conflict = local_conflict(host, suffix=suffix + '-conflict')
    actor = host.setup_author(suffix=suffix, responsibility='integrator', work_kind='integration')
    reference, _ = host.product(suffix + '-package', actor, kind='escalation',
        related=[{'slot_id': 'conflicts', 'refs': [conflict]}],
        episode={'root': None, 'previous': None, 'collection_head': host._proposal_head(),
                 'unfinished': [], 'decisive': True})
    host.commit(host.message('escalation', {'assignment': actor['author'], 'package': reference,
        'conflicts': [conflict], 'affected': affected,
        'requested_decisions': ['Assess exactly the named scoped dependency.']},
        sender=actor['principal'], context=actor['author_context']))
    return reference


def _branches(directory, monkeypatch, engagement):
    host = SchedulingHarness(directory, monkeypatch, engagement=engagement,
                             use_scopes=('default', 'branch-b'))
    host.bootstrap(include_neighbor=True)
    host.enter_scope('branch-b')
    # The catalogue policy is intrinsically anchored in the bootstrap scope;
    # ordinary domain inputs intentionally retain their independent B uses.
    policy_uses = [{'at': '/routing/policy', 'use_scope': 'default'},
                   {'at': '/inherited/2', 'use_scope': 'default'},
                   {'at': '/inputs/1/refs/1', 'use_scope': 'default'}]
    existing, assigned = host.assignment('existing-branch-b-question', 'setter',
                                        owner=host.owner('what'), input_uses=policy_uses)
    dependencies = host.store.read()._dependencies(assigned)
    assert {'ref': host.routing_policy, 'use_scope': 'default'} in dependencies
    assert {'ref': host.input_a, 'use_scope': 'branch-b'} in dependencies
    host.enter_scope('default')
    return host, existing


def test_shared_policy_dependency_pauses_existing_other_scope_and_blocks_its_future_entry(tmp_path, monkeypatch):
    host, existing = _branches(tmp_path, monkeypatch, 'shared-policy-pause')
    episode = _episode_affecting(host, [host.routing_policy], 'shared-capability-episode')
    state = host.store.read()
    assert state.assignment_states[existing['version_id']] == 'paused'
    assert {'ref': existing, 'use_scope': 'branch-b'} in state._episode(episode)['members']
    host.enter_scope('branch-b')
    before = host.path.read_bytes()
    with pytest.raises(DispatchError) as blocked:
        workflow(host).entry('branch-b', 'service-controls',
            [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 1000}],
            int(time.time() * 1000) + 60000)
    assert blocked.value.code == 'P_STATE'
    assert host.path.read_bytes() == before
    assert host.store.read().assignment_states[existing['version_id']] == 'paused'


def test_independent_domain_use_remains_open_and_accepts_new_work_despite_same_input_bytes(tmp_path, monkeypatch):
    host, existing = _branches(tmp_path, monkeypatch, 'independent-domain-use')
    episode = _episode_affecting(host, [host.input_a], 'local-domain-episode')
    state = host.store.read()
    assert state.assignment_states[existing['version_id']] == 'open'
    assert {'ref': existing, 'use_scope': 'branch-b'} not in state._episode(episode)['members']
    assert state.resolve(host.input_a)['material'] == state.resolve(
        state.resolve(existing, 'assignment')['inputs'][0]['refs'][0])['material']
    host.enter_scope('branch-b')
    entry = workflow(host).entry('branch-b', 'service-controls',
        [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 1000}],
        int(time.time() * 1000) + 60000)['assignment']
    state = host.store.read()
    assigned = state.resolve(entry, 'assignment')
    assert state.assignment_states[entry['version_id']] == 'open'
    dependencies = state._dependencies(assigned)
    assert {'ref': host.input_a, 'use_scope': 'branch-b'} in dependencies
    assert {'ref': host.routing_policy, 'use_scope': 'default'} in dependencies
    context = host.context('independent-branch-start', entry, assigned, phase='selection')
    state = host.store.read()
    assert state.execution_eligible(context)
    assert state.run_states[state.resolve(context, 'context')['run_id']] == 'running'
    host.cancel_run(context)
