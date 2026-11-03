# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real local-writer journal admission and immutable routing-artifact replay."""
import copy
import json
import time

import pytest

from governed_fixtures import GovernedHarness, CONTROLLER, delivery, _input_locators
import lifecycle as lc


@pytest.fixture
def host(tmp_path, monkeypatch):
    fixture = GovernedHarness(tmp_path, monkeypatch, engagement='routing-admission')
    fixture.bootstrap()
    return fixture


def test_local_writer_assignment_routing_is_causal_and_replayed_from_exact_captured_assets(host):
    actor = host.setup_author()
    state = host.store.read()
    selected = state.assignment_routing(actor['author_record'])
    assert len(selected['snapshot']['instructions']) == selected['snapshot']['catalogue']['count']
    assert 'specialties' not in selected
    assert selected['policy_use'] == {'ref': host.routing_policy, 'use_scope': host.scope}
    assert {'ref': host.routing_policy, 'use_scope': host.scope} in state._dependencies(actor['author_record'])
    transactions = [json.loads(line) for line in host.path.read_text().splitlines()]
    assert all(item['format'] == 9 for item in transactions)
    source = state.resolve(host.routing_policy, 'source')
    captured = [identifier for item in transactions for identifier in item['validation_artifacts']]
    assert set(source['material']) <= set(captured)
    assert all(host.store._blob(identifier) == state.validation_assets[identifier]
               and lc.blob(state.validation_assets[identifier]) == identifier for identifier in captured)
    assert len(captured) == len(set(captured)), 'Each exact compiler input is captured only once'
    assert host.store.read().assignment_routing(actor['author_record'], live=False) == selected
    malformed = copy.deepcopy(actor['author_record'])
    malformed['routing']['policy'] = host.input_a
    with pytest.raises(lc.ERROR) as failure:
        state.assignment_routing(malformed)
    assert failure.value.code == 'P_SCOPE'


@pytest.mark.parametrize('fault', ['missing-binding', 'foreign-policy'])
def test_local_writer_setter_return_cannot_bypass_required_governing_routing(host, fault):
    actor = host.setup_author()
    host.cancel_run(actor['author_context'])
    context = host.context('invalid-routing-setter', actor['setter'], actor['setter_record'])
    record = copy.deepcopy(actor['author_record'])
    record['assigned_actor'] = 'invalid-route-instance'
    if fault == 'missing-binding':
        del record['routing']
    else:
        record['routing']['policy'] = host.input_a
    identifier = 'invalid-routing-assignment'
    manifest = lc.manifest(identifier, 'delivery.assignment',
                           {'engagement': host.engagement, 'scope': host.scope, 'record': record})
    reference = {'engagement': host.engagement, 'scope': host.scope,
                 'logical_id': identifier, 'version_id': lc.version_id(manifest)}
    returned = {'assignment': actor['setter'], 'context': context,
                'records': [{'logical_id': identifier, 'record_type': 'assignment', 'record': record}],
                'intents': [{'message_type': 'assignment', 'recipient': CONTROLLER,
                             'payload': {'assignment': reference, 'owner': record['owner'],
                                         'responsibility': record['responsibility'],
                                         'inputs': _input_locators(record['inputs']), 'criteria': record['criteria']}}]}
    issued = host.store.read().resolve(context, 'context')
    message = host.message('control_event', {'event': 'run_completed', 'run_context': context,
        'run_id': issued['run_id'], 'observed_at_ms': int(time.time() * 1000),
        'return_blob_id': host.store.put_blob(lc.canonical(returned)),
        'usage': [{'metric': 'tokens', 'unit': 'governed-token', 'total': 1}]})
    before = host.path.read_bytes()
    result = host.send(message)
    assert result['status'] == 'rejected', result
    assert result['error']['code'] == ('P_SCHEMA' if fault == 'missing-binding' else 'P_SCOPE'), result
    assert host.path.read_bytes() == before
    assert reference['version_id'] not in host.store.read().versions
