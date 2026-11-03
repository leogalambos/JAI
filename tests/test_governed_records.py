# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Pure producer record encoding contracts, without a Store or authority grant."""
import copy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import governed_records


def _packet():
    ref = {'engagement': 'encoding', 'scope': 'default', 'logical_id': 'setter', 'version_id': 'a' * 64}
    owner = {'layer': 1, 'work_kind': 'question', 'question': 'what', 'work_item': 'service'}
    return {'execution': {'phase': 'work'}, 'assignment': ref,
            'manifest': [{'ref': ref, 'use_scope': 'default', 'record': {
                'owner': owner, 'profile': ref, 'routing': {'policy': ref}, 'use_scope': 'default'}}]}


def _criteria(packet):
    return {'source_role': 'criteria', 'material': ['b' * 64], 'inherited': [packet['assignment']],
            'criteria': [{'id': 'scope', 'requirement': packet['assignment'],
                          'statement': 'Describe the service boundary.', 'evidence_slots': []}]}


def _author(packet):
    return {'owner': packet['manifest'][0]['record']['owner'],
            'responsibility': 'author', 'assigned_actor': 'author',
            'inherited': [], 'inputs': [], 'criteria': packet['assignment'],
            'effects': [], 'limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 1000}],
            'deadline_ms': 10000}


def test_build_proposal_preserves_semantics_and_binds_exact_source_identity():
    packet = _packet()
    fields = _criteria(packet)
    original = copy.deepcopy(fields)
    result = governed_records.build_proposal(packet, 'source', 'criteria', fields)
    assert result['record_type'] == 'source'
    assert result['logical_id'] == 'criteria'
    assert result['record']['criteria'] == original['criteria']
    assert result['record']['material'] == original['material']
    assert result['record']['owner'] == packet['manifest'][0]['record']['owner']
    assert result['record']['origin'] == {'kind': 'assignment', 'ref': packet['assignment']}
    assert fields == original
    child = governed_records.build_proposal(packet, 'assignment', 'author', _author(packet))
    assert child['record']['issued_under'] == packet['assignment']
    assert {item['at'] for item in child['record']['input_uses']} == {'/profile', '/routing/policy', '/criteria'}
    assert {item['use_scope'] for item in child['record']['input_uses']} == {'default'}


def test_build_proposal_rejects_missing_semantics_conflicts_and_ambiguous_uses():
    packet = _packet()
    with pytest.raises(ValueError, match='structural metadata'):
        governed_records.build_proposal(packet, 'source', 'criteria', {
            **_criteria(packet), 'owner': {'layer': 6}})
    with pytest.raises(ValueError, match='semantic fields'):
        governed_records.build_proposal(packet, 'source', 'criteria', {**_criteria(packet), 'criteria': []})
    missing = {**packet, 'manifest': []}
    with pytest.raises(ValueError, match='exact immutable assignment'):
        governed_records.build_proposal(missing, 'source', 'criteria', _criteria(packet))
    # A single record appears at two effective uses; encoding must not guess one.
    with pytest.raises(ValueError, match='unambiguous use scope'):
        governed_records.build_proposal(packet, 'assignment', 'author', _author(packet),
            uses=[{'ref': packet['assignment'], 'use_scope': 'other'}])
    with pytest.raises(ValueError, match='work responsibility'):
        governed_records.build_proposal({**packet, 'execution': {'phase': 'selection'}},
                                       'source', 'criteria', _criteria(packet))
