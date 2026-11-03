#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Read-only Gen2 audit projection; qualification remains the existing evaluator's act.

The native command handles this internal CLI. Reports capture one Store snapshot,
assess only requested/current-selected products and never write to the engagement.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import time

import governed_delivery as wire
import lifecycle as lc


def _point_key(point):
    return point['use_scope'], point['ref']['version_id']


def _label(point):
    ref = point['ref']
    return f"{ref['logical_id']}@{ref['version_id']} [use={point['use_scope']}; origin={ref['scope']}]"


def _decision(state, point):
    record = state.resolve(point['ref'], 'decision')
    message = record['message']
    return {'point': point, 'sequence': state.provenance[point['ref']['version_id']]['sequence'],
            'message_type': message['message_type'], 'payload': copy.deepcopy(message['payload'])}


def _cancellation_index(state):
    result = {}
    for index, event in enumerate(state.events):
        if event['kind'] in {'cancellation', 'withdrawal', 'permission-cancellation'}:
            for point in event.get('subjects', event.get('outputs', [])):
                result.setdefault(_point_key(point), []).append((index, event))
    return result


def _cancellations(points, subject, index):
    required = {_point_key(point) for point in points}
    events = {order: event for key in required for order, event in index.get(key, [])}
    rows = []
    for order in sorted(events):
        event = events[order]
        affected = [point for point in event.get('subjects', event.get('outputs', []))
                    if _point_key(point) in required]
        rows.append({'kind': event['kind'], 'decision': {'ref': event['decision_ref'],
                     'use_scope': event.get('scope', event['decision_ref']['scope'])},
                     'affected': affected, 'relationship': 'direct' if subject in affected else 'dependency'})
    return rows


def _decisions(state, points):
    unique = {lc.canonical(point): point for point in points}
    return [_decision(state, unique[key]) for key in sorted(unique)]


def _proof_slots(state, closure):
    roles = {'answer': 'professional_review', 'bundle': 'integration_review',
             'handoff': 'receiving_acceptance', 'final_result': 'integration_review',
             'observation': 'professional_review'}
    rows = []
    for point in closure:
        if state.versions[point['ref']['version_id']]['kind'] != 'delivery.product':
            continue
        product = state.resolve(point['ref'], 'product')
        role = roles.get(product['product_kind'])
        profile = state.resolve(product['profile'], 'profile')
        for obligation in profile['obligations']:
            if (obligation['owner'] != product['owner'] or obligation['role'] != role
                    or obligation['subject_kind'] != product['product_kind']):
                continue
            slot = {'kind': 'proof', 'subject': point['ref'], 'role': role,
                    'slot_id': obligation['slot_id']}
            selected = state.proofs.get(lc._proof_key(point['use_scope'], slot))
            row = {'subject': point, 'slot': slot, 'status': 'missing', 'proof': None,
                   'verdict': None, 'recorded_applicability': None}
            if selected is not None:
                proof = {'ref': selected['proof'], 'use_scope': selected['proof_use_scope']}
                row.update(status='selected', proof=proof,
                           verdict=state.resolve(proof['ref'], 'assessment')['verdict'],
                           recorded_applicability=copy.deepcopy(state._status(proof)))
            rows.append(row)
    return rows


@lc._within_assessment
def _output(state, point, cancellation_index):
    # The existing assessment memo makes material display reuse the bytes just
    # checked by evaluate; the report does not introduce a second qualification.
    basis = state.evaluate(point['ref'], point['use_scope'])
    closure = basis['closure']
    material, inputs = [], []
    for dependency in closure:
        value = state.versions[dependency['ref']['version_id']]
        record = state.resolve(dependency['ref'])
        if value['kind'] == 'delivery.source':
            inputs.append({'point': dependency, 'source_role': record['source_role'],
                           'recorded_applicability': copy.deepcopy(state._status(dependency))})
        for identifier in record.get('material', []):
            item = {'point': dependency, 'blob_id': identifier, 'status': 'available', 'error': None}
            try:
                state._material_bytes(identifier, state.blob_reader)
            except (ValueError, OSError) as error:
                item.update(status='unavailable', error={'code': getattr(error, 'code', 'P_CONTEXT'),
                                                        'message': str(error)})
            material.append(item)
    cancellations = _cancellations(closure, point, cancellation_index)
    decisions = list(basis['established_by']) + list(basis['cancelled_by'])
    decisions.extend(item['decision'] for item in cancellations)
    return {'subject': point, 'recorded_applicability': copy.deepcopy(state._status(point)),
            'basis': basis, 'inputs': inputs, 'material': material,
            'required_proofs': _proof_slots(state, closure), 'cancellations': cancellations,
            'decisions': _decisions(state, decisions)}


def _select(state, subject, scope, inventory):
    if subject is None:
        return None
    if isinstance(subject, dict):
        point = copy.deepcopy(subject) if set(subject) == {'ref', 'use_scope'} else {
            'ref': copy.deepcopy(subject), 'use_scope': scope}
        wire.validate({'protocol': lc.PROTOCOL, 'subject': point['ref'],
                       'assessment_scope': point['use_scope']}, 'query.schema.json')
        if point['use_scope'] != scope:
            raise lc.ERROR('P_SCOPE', 'Exact subject use scope differs from the requested report scope')
        state.resolve(point['ref'], 'product')
        return [point]
    if not isinstance(subject, str) or not subject:
        raise ValueError('Subject must be an exact output reference or nonempty selector')
    return [item['point'] for item in inventory
            if subject in {item['point']['ref']['logical_id'], item['point']['ref']['version_id']}]


def report(store, subject=None, scope='default'):
    """Capture a read-only exact-version audit using the existing Gen2 assessment.

    Args:
        store: Existing lifecycle.Store; its warm verified prefix is reused.
        subject: Exact UsePoint/reference, version ID or unambiguous logical ID;
            None assesses current-selected outputs and inventories other versions.
        scope: Applicability scope for discovery and string/reference selectors.
    Returns:
        JSON-safe report with exact current facts, scoped cancellations and limits.
        Ambiguous selectors return candidates without choosing or assessing one.
        A successful report grants no permission, even when permissions exist.
    Raises:
        OSError: Existing journal is unavailable; no directory or journal is created.
        ValueError, ProtocolError: Scope, subject, format or verified history is invalid.
    """
    if not store.path.exists():
        raise FileNotFoundError('Engagement journal is unavailable')
    state = store.read()
    if not state.initialized:
        raise lc.ERROR('P_STATE', 'No admitted Gen2 engagement is available')
    if scope not in {key[0] for key in state.states}:
        raise lc.ERROR('P_SCOPE', 'Requested applicability scope is unavailable')
    selected = {_point_key({'ref': ref, 'use_scope': key[0]})
                for key, ref in state.selections.items() if key[0] == scope}
    inventory = []
    cancellation_index = _cancellation_index(state)
    for use_scope, identifier in sorted(state.states):
        if use_scope != scope or state.versions[identifier]['kind'] != 'delivery.product':
            continue
        point = {'ref': state._reference(identifier), 'use_scope': use_scope}
        slot_selected = _point_key(point) in selected
        current_selected = slot_selected and state._governing_input(point, live=True)
        unusable = None
        if slot_selected and not current_selected:
            cancellations = _cancellations([point], point, cancellation_index)
            unusable = {'reason': 'No current basis: the selected slot does not establish a currently applicable governed use.',
                        'cancellations': cancellations,
                        'decisions': _decisions(state, [item['decision'] for item in cancellations]),
                        'use_until_ms': state._use_changes.get(_point_key(point), {}).get('use_until_ms'),
                        'held': state._held(point)}
        inventory.append({'point': point, 'product_kind': state.resolve(point['ref'], 'product')['product_kind'],
                          'selected_slot': slot_selected,
                          'current_selected': current_selected, 'unusable_selection': unusable,
                          'recorded_applicability': copy.deepcopy(state._status(point))})
    requested = _select(state, subject, scope, inventory)
    status = 'complete'
    if requested is not None and len(requested) != 1:
        status = 'ambiguous' if requested else 'not-found'
        targets = []
    else:
        targets = requested if requested is not None else [item['point'] for item in inventory if item['current_selected']]
    return {'format': 'jai.gen2-audit/1', 'status': status, 'engagement': state.engagement,
            'journal': str(store.path), 'head': state.head, 'assessed_at_ms': int(time.time() * 1000),
            'history_verified': True, 'transaction_count': len(state.transactions),
            'scope': scope, 'available_scopes': sorted({key[0] for key in state.states}),
            'read_only': True, 'authority_granted': False,
            'limits': ['History integrity is verified through the displayed head; this is not professional correctness.',
                       'Current material, authority and justification are assessed only for the listed outputs.',
                       'Inventory applicability is recorded state, not a fresh output assessment.',
                       'Qualification, human acceptance and release permission are distinct; this report grants none.'],
            'governing_inputs': [{'ref': ref, 'use_scope': use} for (use, _), ref in state.sources.items() if use == scope],
            'inventory': inventory, 'selector_candidates': requested if status != 'complete' else [],
            'outputs': [_output(state, point, cancellation_index) for point in targets],
            'open_items': {'escalations': [{'ref': state._reference(identifier), 'state': value}
                                          for identifier, value in state.escalations.items()
                                          if value == 'open' and (scope, identifier) in state.states],
                           'runs': [{'run_id': identifier, 'state': value,
                                     'context': state.run_details[identifier]['context']}
                                    for identifier, value in state.run_states.items()
                                    if value in {'issued', 'running'} and state.run_details[identifier]['context']['scope'] == scope]}}


def format_report(value):
    """Render literal audit facts for a human without changing any verdict.

    Args:
        value: Report returned by report, including exact use scopes and reasons.
    Returns:
        English text suitable for relay to an independent native auditor.
    Raises:
        KeyError, TypeError: The input is not a report from this module.
    """
    lines = [f"Gen2 audit: {value['engagement']} / {value['scope']}",
             'Available recorded scopes (navigation only): ' + ', '.join(value['available_scopes']),
             f"History verified through head {value['head']} ({value['transaction_count']} transactions).",
             f"Status: {value['status']}. Read-only; authority granted: false."]
    lines.extend('Limit: ' + item for item in value['limits'])
    lines.append('Governing input versions:')
    lines.extend('- ' + _label(point) for point in value['governing_inputs'])
    lines.append('Output inventory (recorded state; not blanket qualification):')
    for item in value['inventory']:
        lines.append(f"- {_label(item['point'])}; slot pointer={item['selected_slot']}; current selected use={item['current_selected']}; "
                     f"recorded={json.dumps(item['recorded_applicability'], sort_keys=True)}")
        unusable = item['unusable_selection']
        if unusable is not None:
            lines.append('  ' + unusable['reason'])
            for cancellation in unusable['cancellations']:
                lines.append(f"  {cancellation['kind']}: {_label(cancellation['decision'])}")
                lines.extend('  Affected: ' + _label(point) for point in cancellation['affected'])
            for decision in unusable['decisions']:
                lines.append('  Decision effects: ' + json.dumps(decision['payload'], sort_keys=True))
    if value['status'] != 'complete':
        lines.append('No output assessed. Clarify the exact output version/use scope.')
        lines.extend('- Candidate: ' + _label(point) for point in value['selector_candidates'])
    if not value['outputs']:
        lines.append('No output assessed; no qualification, acceptance or release verdict inferred.')
    for output in value['outputs']:
        basis = output['basis']
        lines.extend(['Output: ' + _label(output['subject']),
                      f"Qualified={basis['qualified']}; accepted={basis['accepted']}; release permission={basis['release_eligible']}",
                      'Exact closure hash: ' + basis['closure_hash']])
        lines.extend(f"- Reason {item['code']}: {item['message']}" for item in basis['reasons'])
        lines.extend('- Required input: ' + _label(item['point']) for item in output['inputs'])
        for proof in output['required_proofs']:
            lines.append(f"- Proof slot {proof['slot']['slot_id']} for {_label(proof['subject'])}: "
                         f"{proof['status']}; verdict={proof['verdict']}" +
                         (f"; {_label(proof['proof'])}" if proof['proof'] is not None else ''))
        lines.extend(f"- Material {item['blob_id']} for {_label(item['point'])}: {item['status']}"
                     for item in output['material'])
        for cancellation in output['cancellations']:
            lines.append(f"- {cancellation['kind']} ({cancellation['relationship']}): {_label(cancellation['decision'])}")
            lines.extend('  Affected: ' + _label(point) for point in cancellation['affected'])
        for decision in output['decisions']:
            lines.append(f"- Decision {_label(decision['point'])}: " + json.dumps(decision['payload'], sort_keys=True))
    lines.append('Open items (not global output blockers): ' + json.dumps(value['open_items'], sort_keys=True))
    return '\n'.join(lines) + '\n'


def main(argv=None):
    """Run internal read-only audit transport; users invoke the native prompt command.

    Args:
        argv: Optional argument sequence; omission uses the process arguments.
    Returns:
        Zero for a completed audit, including unqualified outputs; two for missing,
        corrupt or ambiguous input. No report writes, selections or permissions occur.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('engagement', nargs='?')
    parser.add_argument('subject', nargs='?', help='Exact output version ID or unambiguous logical ID')
    parser.add_argument('--home', default=os.environ.get('FABRIC_HOME') or '.fabric')
    parser.add_argument('--scope', default='default')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        home = Path(args.home)
        engagement = args.engagement
        if engagement is None:
            candidates = list(home.glob('*.jsonl'))
            if not candidates:
                raise FileNotFoundError('No engagement journal is available')
            engagement = max(candidates, key=lambda path: (path.stat().st_mtime_ns, path.name)).stem
        if (not engagement or len(engagement) > 128 or engagement in {'.', '..'}
                or any(char in engagement for char in '/\\')):
            raise ValueError('Bounded nontraversing engagement identity required')
        value = report(lc.Store(home / (engagement + '.jsonl'), engagement), args.subject, args.scope)
        print(json.dumps(value, ensure_ascii=False, sort_keys=True) if args.json else format_report(value), end='\n' if args.json else '')
        return 0 if value['status'] == 'complete' else 2
    except (ValueError, OSError, KeyError, TypeError) as error:
        failure = {'status': 'unavailable', 'history_verified': False, 'authority_granted': False,
                   'read_only': True, 'outputs': [],
                   'error': {'code': getattr(error, 'code', 'P_CONTEXT'), 'message': str(error)}}
        print(json.dumps(failure, sort_keys=True) if args.json else
              'Audit unavailable; no current verdict. ' + str(error))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
