# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Isolated return projection; this collaborator proves no journal authority.

Actual signed/native histories cover admission and publication separately. This
test isolates visibility of an already captured recordless terminal return.
"""
import sys

import pytest

from governed_fixtures import lc
import governed_dispatch as dispatch


def _ref(name):
    return {'engagement': 'projection-only', 'scope': 'default', 'logical_id': name,
            'version_id': lc._hash(name)}


class _ProjectionHistory:
    """Supply explicit immutable history facts, never an accepted State or proof."""

    def __init__(self, event='run_completed'):
        self.event = event
        self.parent = _ref('coordinator')
        self.child = _ref('publisher')
        self.context = _ref('publisher-context')
        self.subject = _ref('integrated-bundle')
        self.owner = {'layer': 1, 'work_kind': 'integration', 'question': None,
                      'work_item': 'service-controls'}
        self.parent_record = {'owner': self.owner, 'use_scope': 'default'}
        self.child_record = {'issued_under': self.parent, 'owner': self.owner,
                             'responsibility': 'integrator', 'use_scope': 'default'}
        self.subject_record = {'owner': self.owner, 'product_kind': 'bundle'}
        self.context_record = {'assignment': self.child, 'execution': {'phase': 'work'},
                               'run_id': 'publisher-run'}
        self.intent = {'message_type': 'integration',
                       'recipient': {'kind': 'controller', 'id': 'fixture-controller'},
                       'payload': {'bundle': self.subject}}
        self.status, self.held, self.produced = 'valid', False, True
        self.messages = {}
        self.run_states = {'publisher-run': 'returned'}
        self.assignment_states = {self.child['version_id']: 'completed'}
        self.head = '0' * 64

    @property
    def transactions(self):
        package = {'assignment': self.child, 'context': self.context,
                   'records': [], 'intents': [self.intent]}
        raw = lc.canonical(package)
        return [{'hash': '1' * 64, 'return_artifact': {lc.blob(raw): raw.decode()},
                 'operations': [{'data': {'message': {
                     'message_type': 'control_event', 'scope': 'default',
                     'payload': {'event': self.event, **({'run_context': self.context} if self.event == 'run_completed' else
                                 {'invocation_id': 'actual-physical-invocation'})}}}}]}]

    def resolve(self, reference, kind=None):
        if reference == self.context:
            assert kind in {None, 'context'}
            return self.context_record
        if reference == self.child:
            assert kind in {None, 'assignment'}
            return self.child_record
        assert reference == self.subject and kind in {None, 'product'}
        return self.subject_record

    def _produced_under(self, subject, parent, owner):
        return self.produced and subject == self.subject and parent == self.parent and owner == self.owner

    def _status(self, subject, scope):
        assert subject == self.subject
        return {'validity': self.status if scope == 'default' else 'invalid'}

    def _point(self, subject, scope):
        return {'ref': subject, 'use_scope': scope}

    def _held(self, point):
        return self.held and point == {'ref': self.subject, 'use_scope': 'default'}


@pytest.mark.parametrize('event', ['run_completed', 'invocation_finished'])
def test_recordless_integration_is_visible_only_in_its_exact_delivered_current_basis(tmp_path, event):
    store = lc.Store(tmp_path / 'not-an-enrolled-journal.jsonl', 'projection-only')
    config = {'protocol': dispatch.HOST_PROTOCOL,
              'workers': [{'provider': 'json-process/1', 'argv': [sys.executable], 'files': []}],
              'destinations': [], 'tools': [], 'limits': {'packet_bytes': 10000, 'total_bytes': 10000}}
    dispatcher = dispatch.Dispatcher(store, config)
    history = _ProjectionHistory(event)
    token = 'record:' + history.subject['version_id'] + ':'

    def projected(basis):
        return dispatcher._owned_returns(history, history.parent, history.parent_record, basis)

    assert projected([]) == []
    assert projected([token + 'pending']) == []  # The old context cannot see future publication.
    assert projected(['record:' + _ref('different-bundle')['version_id'] + ':valid']) == []
    published = projected([token + 'valid'])
    assert len(published) == 1
    assert published[0]['assignment'] == history.child
    assert published[0]['records'] == [] and published[0]['intents'] == [history.intent]
    assert history.messages == {}, 'Visibility must not depend on a fabricated stored intent.'

    for status in ('pending', 'invalid', 'revoked'):
        history.status = status
        assert projected([token + status]) == []
    history.status, history.held = 'valid', True
    assert projected([token + 'valid:held']) == []
    history.held, history.produced = False, False
    assert projected([token + 'valid']) == []
    history.produced = True
    history.child_record['use_scope'] = 'another-scope'
    assert projected([token + 'valid']) == []
    history.child_record['use_scope'] = 'default'
    history.child_record['issued_under'] = _ref('unrelated-coordinator')
    assert projected([token + 'valid']) == []

    history.child_record['issued_under'] = history.parent
    history.child_record['responsibility'] = 'measurement'
    history.status = 'pending'
    history.subject_record['product_kind'] = 'observation'
    history.intent = {'message_type': 'observation',
                      'recipient': {'kind': 'controller', 'id': 'fixture-controller'},
                      'payload': {'observation': history.subject}}
    observed = projected([token + 'pending'])
    assert len(observed) == 1 and observed[0]['intents'] == [history.intent]
    assert history.status == 'pending', 'Projecting a terminal observation must not qualify it.'
