#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Pure structural record construction shared by native semantic encoders.

The packet supplies granted identity and dependency metadata. Professional
content, criteria, subjects and verdicts remain explicit producer values.
"""
from __future__ import annotations

import copy

import governed_delivery as wire
import lifecycle as lc


def build_proposal(packet, record_type, logical_id, fields, uses=()):
    """Encode explicit semantic fields with exact immutable packet metadata.

    Args:
        packet: Existing issued work packet, including its assignment manifest.
        record_type: Source, assignment, product or assessment record family.
        logical_id: Producer-selected logical record identifier.
        fields: Actual semantic values; conflicting structural values are rejected.
        uses: Explicit use points for new or otherwise ambiguous dependencies.
    Returns:
        A schema-valid proposal; no material is written or authority granted.
    Raises:
        ProtocolError, ValueError: Unsupported phase/family, missing semantics,
            conflicting metadata, missing assignment or ambiguous dependency use.
    """
    if packet['execution']['phase'] != 'work' or record_type not in {'source', 'assignment', 'product', 'assessment'}:
        raise lc.ERROR('P_SCOPE', 'Producer stencils require an existing work responsibility')
    matches = [item['record'] for item in packet['manifest'] if item['ref'] == packet['assignment']]
    if len(matches) != 1:
        raise ValueError('Packet must identify its exact immutable assignment once')
    parent = matches[0]
    record = copy.deepcopy(fields)

    def supply(name, value):
        if name in record and record[name] != value:
            raise ValueError('Conflicting structural metadata: ' + name)
        record[name] = copy.deepcopy(value)

    if record_type == 'assignment':
        if 'owner' not in record:
            raise ValueError('The local producer must choose the child owner explicitly')
        for key in ('profile', 'routing', 'use_scope'):
            supply(key, parent[key])
        supply('issued_under', packet['assignment'])
        scopes = {}
        for item in [*packet['manifest'], *uses]:
            scopes.setdefault(lc.canonical(item['ref']), set()).add(item['use_scope'])
        selectors = []
        for path, reference in lc._causal_reference_paths(record):
            if path == '/issued_under':
                continue
            values = scopes.get(lc.canonical(reference), set())
            if len(values) != 1:
                raise ValueError('Each child dependency needs an explicit unambiguous use scope')
            selectors.append({'at': path, 'use_scope': next(iter(values))})
        supply('input_uses', selectors)
    else:
        supply('owner', parent['owner'])
        if record_type == 'source':
            supply('origin', {'kind': 'assignment', 'ref': packet['assignment']})
        else:
            supply('assignment', packet['assignment'])
            supply('profile', parent['profile'])
            if record_type == 'assessment':
                basis = packet.get('assessment_basis')
                if basis is None or record.get('subject') != basis['subject']:
                    raise ValueError('Producer must explicitly assess its exact assigned subject')
                supply('assessed_closure', basis['closure'])
                supply('assessed_hash', basis['hash'])
    result = {'record_type': record_type, 'logical_id': logical_id, 'record': record}
    if not wire.validator('record.schema.json', 'proposal').is_valid(result):
        raise lc.ERROR('P_SCHEMA', 'Complete explicit semantic fields for the existing proposal schema are required')
    return result
