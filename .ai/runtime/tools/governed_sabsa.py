#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Bounded SABSA semantic content inside the existing governed Store.

Content is immutable product material; this module supplies no repository,
selection mechanism, approval, acceptance or release authority.
"""
from __future__ import annotations

import copy
from functools import lru_cache
from pathlib import Path
import time

import governed_delivery as wire
import lifecycle as lc

CATALOGUE = Path(__file__).resolve().parents[1] / 'sabsa/governed-catalogue.json'
FORMAT = 'jai-sabsa-content/1'
PROFILE_FORMAT = 'jai-sabsa-content-profile/1'


@lru_cache(maxsize=1)
def _catalogue():
    return lc.loads(CATALOGUE.read_bytes())


def catalogue():
    """Return an isolated copy of the original versioned JAI minimum catalogue.

    Returns:
        Six-layer information groups, source editions, relation types and view purposes.
    Raises:
        OSError, ValueError: The maintained catalogue is unavailable or malformed.
    """
    return copy.deepcopy(_catalogue())


def validate_profile(payload):
    """Validate a closed engagement-specific content profile against adopted sources.

    Args:
        payload: Integer/string JSON profile with exact catalogue and source editions.
    Returns:
        Isolated validated profile; this establishes no client facts or approval.
    Raises:
        ProtocolError: Unsupported source, duplicate requirement, scope or mapping.
    """
    wire.validate(payload, 'sabsa-content-profile.schema.json')
    data = _catalogue()
    sources = {item['id']: item for item in payload['method_sources']}
    if len(sources) != len(payload['method_sources']) or set(sources) != set(data['method_sources']):
        raise lc.ERROR('P_PROOF', 'The bounded profile requires its exact adopted method source set')
    if any(sources[key]['edition'] != value['edition'] for key, value in data['method_sources'].items()):
        raise lc.ERROR('P_PROOF', 'Requested method edition exceeds the adopted source basis')
    keys = [item['key'] for item in payload['required_units'] + payload['required_relations']]
    if len(keys) != len(set(keys)):
        raise lc.ERROR('P_CONFLICT', 'Content obligation keys must be unique')
    units = {item['key']: item for item in payload['required_units']}
    for item in units.values():
        _group_owner(item['group'], item['owner'])
        if item['owner']['layer'] not in payload['scope']['layers'] or item['owner']['question'] is not None and item['owner']['question'] not in payload['scope']['questions']:
            raise lc.ERROR('P_SCOPE', 'Content obligations cannot silently enlarge the adopted layer/question scope')
    if 2 in payload['scope']['layers'] and not any(item['group'] == 'conceptual.attributes' for item in units.values()):
        raise lc.ERROR('P_PROOF', 'Conceptual scope requires an identifiable tailored Business Attributes Profile')
    if 6 in payload['scope']['layers'] and not {'management.activity', 'management.measure'} <= {item['group'] for item in units.values()}:
        raise lc.ERROR('P_PROOF', 'Management scope requires activity and measure definitions')
    # Actual operating claims are represented by an observation obligation;
    # a definition never stands in for that observation or its evidence.
    for item in payload['required_relations']:
        if item['from_obligation'] not in units or item['to_obligation'] not in units:
            raise lc.ERROR('P_CONTEXT', 'Required relations must name explicit unit obligations')
    if len({item['view'] for item in payload['required_views']}) != len(payload['required_views']):
        raise lc.ERROR('P_CONFLICT', 'A required view has one unambiguous obligation set')
    relations = {item['key'] for item in payload['required_relations']}
    for item in payload['required_views']:
        if not set(item['unit_obligations']) <= set(units) or not set(item['relation_obligations']) <= relations:
            raise lc.ERROR('P_CONTEXT', 'View coverage must name the declared obligations')
    if any(not set(item['obligations']) <= set(keys) for item in payload['exclusions']):
        raise lc.ERROR('P_CONTEXT', 'Exclusions identify existing obligations rather than deleting requirements')
    return copy.deepcopy(payload)


def _group_owner(group, owner):
    specification = _catalogue()['groups'][group]
    if owner['layer'] != specification['layer'] or specification['question'] is not None and owner['question'] != specification['question']:
        raise lc.ERROR('P_SCOPE', 'Semantic units must remain in their assigned layer and question')
    if specification['question'] is None and owner['question'] is None and not (group == 'management.observation' and owner['work_kind'] == 'measurement'):
        raise lc.ERROR('P_SCOPE', 'Dedicated content groups require an owned question or actual measurement task')


def _validate_units(payload, owner, product_kind='answer'):
    wire.validate(payload, 'sabsa-content.schema.json')
    units = {unit['key']: unit for unit in payload['units']}
    if len(units) != len(payload['units']) or len({item['key'] for item in payload['relations']}) != len(payload['relations']):
        raise lc.ERROR('P_CONFLICT', 'Unit and relation keys must be unique within their exact product')
    if product_kind in {'bundle', 'final_result', 'handoff'} and units:
        raise lc.ERROR('P_SCOPE', 'Integrated views reference owned products instead of copying foreign semantic units')
    for unit in units.values():
        _group_owner(unit['group'], owner)
        required = _catalogue()['groups'][unit['group']]['required_properties']
        if not set(required) <= set(unit['properties']):
            raise lc.ERROR('P_PROOF', 'A dedicated semantic group lacks its required meaningful properties')
        if (unit['group'] == 'management.observation') != (product_kind == 'observation'):
            raise lc.ERROR('P_SCOPE', 'Activity and measure definitions are distinct from actual observation products')
    return payload


def _read(state, identifier, live):
    try:
        return state._validation_bytes(identifier, live)
    except lc.ERROR:
        raise
    except (OSError, ValueError) as error:
        raise lc.ERROR('P_CONTEXT', 'Exact semantic material is unavailable') from error


def _memo(state):
    walk = state._assessment_walk
    return walk.setdefault('sabsa_content', {}) if walk is not None else {}


def _policy(state, profile_ref, scope, live):
    profile = state.resolve(profile_ref, 'profile')
    selector = profile['content_profile']
    if selector is None:
        return None
    point = state.content_policy(profile_ref)
    reference, selected_scope = point['ref'], point['use_scope']
    if not state._governing_input(point, live):
        raise lc.ERROR('P_CONTEXT', 'The governing content policy has lost applicability')
    if reference['version_id'] not in state._content_policies:
        raise lc.ERROR('P_CONTEXT', 'Exact admitted content-policy metadata is unavailable')
    return reference, state._content_policies[reference['version_id']], selected_scope


def _payload(state, record, live):
    record_key = lc._hash(record)
    if record_key in state._product_records:
        return copy.deepcopy(state._product_content[state._product_records[record_key]])
    key = ('payload', record_key, live)
    memo = _memo(state)
    if key in memo:
        return memo[key]
    values = []
    for identifier in record['material']:
        raw = _read(state, identifier, live)
        try:
            value = lc.loads(raw)
        except ValueError:
            continue
        if isinstance(value, dict) and value.get('format') == FORMAT:
            if lc.canonical(value) != raw:
                raise lc.ERROR('P_PARSE', 'Semantic payload must be exact canonical JSON')
            values.append(value)
    if len(values) > 1:
        raise lc.ERROR('P_CONFLICT', 'A semantic product cannot contain competing typed payloads')
    result = values[0] if values else None
    memo[key] = result
    return result


def _locator_key(locator, current):
    reference = current if locator['product'] is None else locator['product']
    return reference['version_id'], locator.get('unit', locator.get('relation'))


@lc._within_assessment
def validate_product(state, record, scope='default', live=True):
    """Validate owned semantic material and exact declared cross-product dependencies.

    Args:
        state: Existing governed State; never a second semantic repository.
        record: Actual product record supplied by its assigned semantic owner.
        scope: Exact use scope under assessment.
        live: Require material for this operation; no unrelated history is loaded.
    Returns:
        Typed payload or None when the selected profile does not require this product.
        Partial owned units may remain pending; full claim assessment is separate.
    Raises:
        ProtocolError: Missing required typed material, malformed units, foreign units
            or unbound/missing semantic endpoints.
    """
    # Dependencies use the ambient scope as well as the explicit content scope.
    # Never publish a partial validation or expose the cached mutable payload.
    key = ('validated-product', lc.canonical(record), scope, state.scope, live)
    memo = _memo(state)
    if key not in memo:
        memo[key] = copy.deepcopy(_validate_product(state, record, scope, live))
    return copy.deepcopy(memo[key])


def _validate_product(state, record, scope, live):
    """Complete the uncached content check before publishing its successful result."""
    selected = _policy(state, record['profile'], scope, live)
    if selected is None:
        return None
    _, profile, _ = selected
    required = [item for item in profile['required_units'] if item['owner'] == record['owner']]
    payload = _payload(state, record, live)
    if payload is None:
        if required and record['product_kind'] in {'answer', 'observation'}:
            raise lc.ERROR('P_PROOF', 'The assigned content obligation requires typed semantic material')
        return None
    _validate_units(payload, record['owner'], record['product_kind'])
    local_units = {item['key']: item for item in payload['units']}
    local_relations = {item['key']: item for item in payload['relations']}
    dependencies = {}
    for point in state._dependencies(record):
        for item in state._closure(point):
            dependencies.setdefault(item['ref']['version_id'], []).append(item)
    for relation in payload['relations']:
        for endpoint in (relation['from'], relation['to']):
            _endpoint(state, endpoint, local_units, dependencies, live)
    for binding in payload['view_bindings']:
        for endpoint in binding['units']:
            _endpoint(state, endpoint, local_units, dependencies, live)
        for endpoint in binding['relations']:
            if endpoint['product'] is None:
                if endpoint['relation'] not in local_relations:
                    raise lc.ERROR('P_CONTEXT', 'A view names an unavailable local relationship')
            else:
                if endpoint['product']['version_id'] not in dependencies:
                    raise lc.ERROR('P_SCOPE', 'A view cannot navigate unprovided foreign material')
                foreign_record = state.resolve(endpoint['product'], 'product')
                if not any(state._governing_input(point, live) for point in dependencies[endpoint['product']['version_id']]):
                    raise lc.ERROR('P_CONTEXT', 'A view requires an applicable accepted input')
                foreign = state._product_content.get(endpoint['product']['version_id'])
                if foreign is None or endpoint['relation'] not in {item['key'] for item in foreign['relations']}:
                    raise lc.ERROR('P_CONTEXT', 'A view names an unavailable exact relationship')
    for unit in payload['units']:
        if unit['group'] == 'management.observation':
            observed = [item for item in payload['relations'] if item['type'] == 'observes' and item['from'] == {'product': None, 'unit': unit['key']}]
            measured = [item for item in payload['relations'] if item['type'] == 'measures' and item['to'] == {'product': None, 'unit': unit['key']}]
            if (not observed or not measured
                    or any(item['to'] == {'product': None, 'unit': unit['key']} for item in observed)
                    or any(_endpoint(state, item['from'], local_units, dependencies, live)['group'] != 'management.measure' for item in measured)
                    or not (record['evidence'] or len(record['material']) > 1)):
                raise lc.ERROR('P_PROOF', 'An observation needs exact subject/measure relations and execution evidence')
    return payload


def _endpoint(state, endpoint, local_units, dependencies, live):
    if endpoint['product'] is None:
        if endpoint['unit'] not in local_units:
            raise lc.ERROR('P_CONTEXT', 'An exact local semantic endpoint is unavailable')
        return local_units[endpoint['unit']]
    reference = endpoint['product']
    if reference['version_id'] not in dependencies:
        raise lc.ERROR('P_SCOPE', 'A semantic relation cannot invent a foreign causal dependency or visibility grant')
    foreign_record = state.resolve(reference, 'product')
    if not any(state._governing_input(point, live) for point in dependencies[reference['version_id']]):
        raise lc.ERROR('P_CONTEXT', 'A semantic endpoint requires an applicable accepted input')
    foreign = state._product_content.get(reference['version_id'])
    matches = [] if foreign is None else [item for item in foreign['units'] if item['key'] == endpoint['unit']]
    if len(matches) != 1:
        raise lc.ERROR('P_CONTEXT', 'An exact foreign semantic endpoint is unavailable')
    return matches[0]


def _owned_requirements(state, record, scope, live):
    selected = _policy(state, record['profile'], scope, live)
    if selected is None or record['product_kind'] not in {'answer', 'observation'}:
        return []
    key = lc._hash(record)
    payload = state._product_content[state._product_records[key]] if key in state._product_records else validate_product(state, record, scope, live)
    required = [item for item in selected[1]['required_units'] if item['owner'] == record['owner']]
    units = {} if payload is None else {item['key']: item for item in payload['units']}
    missing = {item['key'] for item in required if item['key'] not in units
               or units[item['key']]['group'] != item['group'] or _unknown_target(units[item['key']])}
    supports = {}
    excluded = _exclusions(state, selected[1], scope, live, record['profile'], missing, supports)
    if not missing <= excluded:
        raise lc.ERROR('P_PROOF', 'The owned current answer lacks required content or an established target')
    return [value for index, value in enumerate(supports.values()) if value not in list(supports.values())[:index]]


def _unknown_target(unit):
    return unit['properties'].get('target', '').strip().casefold() in {'unknown', 'tbd', 'proposed', 'not established'}


def _lineage(state, selector, previous, current):
    if previous == current:
        return True
    predecessors = {}
    for event in state.events:
        if (event['kind'] == 'selection' and event['category'] == 'source'
                and event['scope'] == selector['use_scope']
                and event['slot'] == {'logical_id': selector['logical_id']}):
            payload = state.resolve(event['decision_ref'])['message']['payload']
            for pair in payload.get('replacements', []):
                if pair['replacement'] == event['subject']:
                    predecessors[event['subject']['version_id']] = pair['previous']
    seen = set()
    while current['version_id'] not in seen:
        if current == previous:
            return True
        seen.add(current['version_id'])
        current = predecessors.get(current['version_id'])
        if current is None:
            break
    return False


def _exclusions(state, profile, scope, live, profile_ref, needed=None, supports=None):
    excluded = set()
    at = int(time.time() * 1000) if live else state.assessed_at_ms
    definitions = {item['key']: item for item in profile['required_units'] + profile['required_relations']}
    for item in profile['exclusions']:
        if needed is not None and not set(item['obligations']) & needed:
            continue
        if item['use_scope'] != scope or item['expires_at_ms'] is not None and at >= item['expires_at_ms']:
            continue
        decision = state.resolve(item['decision'])
        if (state.versions[item['decision']['version_id']]['kind'] != 'delivery.decision'
                or not state._governing_input(state._point(item['decision'], scope), live)):
            continue
        message = decision['message']
        payload = message['payload']
        if (message['profile'] != profile_ref or message['scope'] != scope or payload.get('action') != 'exclude_content'
                or payload['reason'] != item['rationale'] or message['sender']['kind'] != 'authority'
                or not set(item['obligations']) <= set(payload['obligations'])):
            continue
        delivery_profile = state.resolve(message['profile'], 'profile')
        selector = delivery_profile['content_profile']
        if selector is None:
            continue
        current = state.sources.get((selector['use_scope'], selector['logical_id']))
        if current is None or not _lineage(state, selector, payload['content_policy'], current):
            continue
        source = state.resolve(payload['content_policy'], 'source')
        original = state._content_policies[payload['content_policy']['version_id']]
        old = {value['key']: value for value in original['required_units'] + original['required_relations']}
        if any(old.get(key) != definitions.get(key) for key in item['obligations']):
            continue
        events = [event for event in state.events if event['kind'] == 'content-exclusion'
                  and event.get('message_id') == message['message_id']]
        if len(events) != 1:
            continue
        state._governing_grants({'decision_ref': item['decision'], 'scope': scope,
            'grants': [{'purpose': 'delivery-change', 'key_id': events[0]['payload']['human_key_id']}]}, live)
        excluded.update(item['obligations'])
        if supports is not None:
            for key in item['obligations']:
                if needed is None or key in needed:
                    supports.setdefault(key, {'point': state._point(item['decision'], scope),
                                              'expires_at_ms': item['expires_at_ms']})
    return excluded


def _structure(state, output, scope, live):
    memo = _memo(state)
    cache_key = ('structure', lc.canonical(output), scope, live)
    if cache_key in memo:
        return memo[cache_key]
    record = state.resolve(output, 'product')
    selected = _policy(state, record['profile'], scope, live)
    if selected is None:
        raise lc.ERROR('P_PROOF', 'General processing does not establish a SABSA-content claim')
    profile_ref, profile, _ = selected
    closure = state._closure(output, scope)
    products = {}
    for point in closure:
        if state.versions[point['ref']['version_id']]['kind'] == 'delivery.product':
            body = state.resolve(point['ref'], 'product')
            payload = state._product_content[point['ref']['version_id']]
            if payload is not None:
                products[point['ref']['version_id']] = (point, body, payload)
    excluded = set()
    rows, selected_units, nodes, relation_rows, selected_relations = [], {}, {}, [], {}
    for obligation in profile['required_units']:
        row = {'key': obligation['key'], 'status': 'missing', 'unit': None, 'reasons': []}
        candidates = []
        selected_refs = []
        for key, reference in state.selections.items():
            if key[0] != scope:
                continue
            slot = lc.loads(key[1])
            if slot.get('owner') == obligation['owner']:
                selected_refs.append(reference)
        for reference in selected_refs:
            product = products.get(reference['version_id'])
            if product is not None:
                matches = [unit for unit in product[2]['units'] if unit['key'] == obligation['key'] and unit['group'] == obligation['group']]
                candidates.extend((product, unit) for unit in matches)
        if not selected_refs:
            for product in products.values():
                if product[1]['owner'] == obligation['owner'] and state._status(product[0])['validity'] not in {'invalid', 'revoked'}:
                    candidates.extend((product, unit) for unit in product[2]['units'] if unit['key'] == obligation['key'] and unit['group'] == obligation['group'])
        if len(candidates) > 1:
            row['status'] = 'conflicting'
        elif candidates:
            product, unit = candidates[0]
            locator = {'product': product[0]['ref'], 'unit': unit['key']}
            row['unit'] = locator
            state_value = state._status(product[0])['validity']
            row['status'] = 'stale' if state_value in {'invalid', 'revoked'} else 'missing' if _unknown_target(unit) else 'satisfied'
            if not selected_refs and row['status'] == 'satisfied':
                row['status'] = 'unreviewed'
            selected_units[obligation['key']] = locator
            nodes[_locator_key(locator, output)] = (unit, product)
        rows.append(row)
    for product in products.values():
        for unit in product[2]['units']:
            nodes.setdefault((product[0]['ref']['version_id'], unit['key']), (unit, product))
    relations = []
    bindings = []
    for product in products.values():
        for relation in product[2]['relations']:
            relations.append((product[0]['ref'], relation))
        bindings.extend((product[0]['ref'], binding) for binding in product[2]['view_bindings'])
    for obligation in profile['required_relations']:
        row = {'key': obligation['key'], 'status': 'missing', 'reasons': [], 'relation': None}
        if obligation['from_obligation'] in selected_units and obligation['to_obligation'] in selected_units:
            origin = _locator_key(selected_units[obligation['from_obligation']], output)
            target = _locator_key(selected_units[obligation['to_obligation']], output)
            matches = [(reference, relation) for reference, relation in relations if relation['key'] == obligation['key'] and relation['type'] == obligation['type']
                       and _locator_key(relation['from'], reference) == origin and _locator_key(relation['to'], reference) == target]
            row['status'] = 'satisfied' if len(matches) == 1 else 'conflicting' if len(matches) > 1 else 'missing'
            if len(matches) == 1:
                selected_relations[obligation['key']] = {'product': matches[0][0], 'relation': matches[0][1]['key']}
                row['relation'] = selected_relations[obligation['key']]
        relation_rows.append(row)
    edges = {}
    for reference, relation in relations:
        if relation['type'] in _catalogue()['trace_relations']:
            edges.setdefault(_locator_key(relation['from'], reference), set()).add(_locator_key(relation['to'], reference))
    anchors = {key for key, (unit, _) in nodes.items() if unit['group'] == 'conceptual.attributes'
               or unit['group'] == 'contextual.why' and unit['properties'].get('business_role') in _catalogue()['business_roles']}
    def trace(key, active):
        if key in anchors:
            return [key]
        if key in active:
            return None
        for parent in sorted(edges.get(key, set())):
            path = trace(parent, active | {key})
            if path is not None:
                return [key, *path]
        return None
    backward = []
    for row in rows:
        if row['unit'] is None:
            continue
        path = trace(_locator_key(row['unit'], output), set())
        if path is None:
            row['reasons'].append('P_TRACE')
            if row['status'] == 'satisfied':
                row['status'] = 'missing'
        else:
            backward.append({'obligation': row['key'], 'path': [{'product': state._reference(key[0]), 'unit': key[1]} for key in path]})
    for row in rows:
        if row['unit'] is None:
            continue
        key = _locator_key(row['unit'], output)
        unit_layer = _catalogue()['groups'][nodes[key][0]['group']]['layer']
        if key in anchors and any(layer > unit_layer for layer in profile['scope']['layers']) and not any(path['path'][-1] == row['unit'] and len(path['path']) > 1 for path in backward):
            row['reasons'].append('P_FORWARD_TRACE')
            if row['status'] == 'satisfied':
                row['status'] = 'missing'
    needed = {row['key'] for row in rows + relation_rows if row['status'] not in {'satisfied', 'unreviewed'}}
    required_supports = {}
    excluded = _exclusions(state, profile, scope, live, record['profile'], needed, required_supports)
    for row in rows:
        if row['key'] in excluded and row['status'] not in {'satisfied', 'unreviewed'}:
            row.update(status='excluded', unit=None)
    for row in relation_rows:
        if row['key'] in excluded and row['status'] != 'satisfied':
            row.update(status='excluded', relation=None)
    view_rows = []
    for obligation in profile['required_views']:
        matches = []
        for reference, binding in bindings:
            if binding['view'] != obligation['view']:
                continue
            bound_units = {_locator_key(locator, reference) for locator in binding['units']}
            required = {_locator_key(selected_units[key], output) for key in obligation['unit_obligations'] if key in selected_units}
            relation_keys = {_locator_key(locator, reference) for locator in binding['relations']}
            required_links = {_locator_key(selected_relations[key], output) for key in obligation['relation_obligations'] if key in selected_relations}
            if len(required) == len(obligation['unit_obligations']) and required <= bound_units and len(required_links) == len(obligation['relation_obligations']) and required_links <= relation_keys:
                matches.append((reference, binding))
        view_rows.append({'view': obligation['view'], 'status': 'satisfied' if len(matches) == 1 else 'conflicting' if len(matches) > 1 else 'missing', 'reasons': [],
                          'binding': {'product': matches[0][0], 'view': matches[0][1]['view']} if len(matches) == 1 else None})
    report = {'profile': {'ref': profile_ref, 'catalogue_id': profile['catalogue_id'], 'catalogue_version': profile['catalogue_version'], 'claim': profile['claim']},
              'output': {'ref': output, 'use_scope': scope}, 'status': 'incomplete',
              'structural_complete': all(row['status'] in {'satisfied', 'unreviewed', 'excluded'} for row in rows + relation_rows + view_rows),
              'substantive_complete': False, 'obligations': rows, 'relations': relation_rows, 'views': view_rows,
              'traces': {'backward': backward, 'forward': [{'basis': path['path'][-1], 'realization': path['path'][0]} for path in backward]}}
    report['required_supports'] = [value for index, value in enumerate(required_supports.values())
                                   if value not in list(required_supports.values())[:index]]
    report['exclusions'] = [{**item, 'status': 'effective' if set(item['obligations']) <= excluded else 'not_effective'} for item in profile['exclusions']]
    result = report, profile, products, selected_units
    memo[cache_key] = result
    return result


@lc._within_assessment
def assess(state, output, scope='default', live=True):
    """Assess one output's selected content and ordinary current justification.

    Args:
        state: Existing governed State.
        output: Exact output product reference, never a mutable document path.
        scope: Current authorized applicability scope.
        live: Inspect current material and authority for this assessment.
    Returns:
        Deterministic private report of obligations, traces, reviews and permission facts.
    Raises:
        ProtocolError: No adopted profile, corrupt content or unavailable exact input.
    """
    report, _, _, _ = _assessed(state, output, scope, live)
    return report


def _assessed(state, output, scope, live):
    try:
        structure = _structure(state, output, scope, live)
    except (lc.ERROR, ValueError) as error:
        state.resolve(output, 'product')
        try:
            basis = state.evaluate(output, scope, live)
        except ValueError:
            basis = {'qualified': False, 'accepted': False, 'release_eligible': False}
        status = 'unsupported' if getattr(error, 'code', 'P_SCHEMA') in {'P_SCHEMA', 'P_PROOF'} else 'stale'
        report = {'profile': None, 'output': {'ref': output, 'use_scope': scope}, 'status': 'unsupported' if status == 'unsupported' else 'incomplete',
                  'structural_complete': False, 'substantive_complete': False, 'obligations': [{'key': 'content-profile', 'status': status, 'unit': None, 'reasons': [getattr(error, 'code', 'P_SCHEMA')]}],
                  'relations': [], 'views': [], 'traces': {'backward': [], 'forward': []}, 'exclusions': [], 'basis': basis}
        return report, {'scope': {'classification': 'private'}, 'required_views': []}, {}, {}
    report = structure[0]
    report['basis'] = state.evaluate(output, scope, live)
    for row in report['obligations']:
        if row['status'] == 'satisfied' and row['unit'] is not None and not state.evaluate(row['unit']['product'], scope, live)['qualified']:
            row['status'] = 'unreviewed'
    report['substantive_complete'] = report['structural_complete'] and report['basis']['qualified'] and all(row['status'] in {'satisfied', 'excluded'} for row in report['obligations'])
    report['status'] = 'complete' if report['substantive_complete'] else 'incomplete'
    return structure


def _require_final(state, record, scope, live):
    reference = next((state._reference(identifier) for identifier, value in state.versions.items()
                      if value['kind'] == 'delivery.product' and value['content']['record'] == record), None)
    if reference is None:
        return []
    report, profile, _, _ = _structure(state, reference, scope, live)
    if not report['structural_complete'] or any(row['status'] not in {'satisfied', 'excluded'} for row in report['obligations']):
        raise lc.ERROR('P_PROOF', 'The final SABSA claim lacks its exact current content basis')
    for row in report['obligations']:
        if row['unit'] is not None and not state._governing_input(state._point(row['unit']['product'], scope), live):
            raise lc.ERROR('P_PROOF', 'The final SABSA claim lacks applicable independent review')
    return copy.deepcopy(report['required_supports'])


def _public_report(report, withheld):
    rows = report['obligations'] + report['relations'] + report['views']
    counts = {status: sum(row['status'] == status for row in rows) for status in ('satisfied', 'excluded', 'missing', 'stale', 'unsupported', 'conflicting', 'unreviewed')}
    return {'audience': 'public', 'catalogue_id': 'jai-sabsa-minimum', 'catalogue_version': '1',
            'status': 'complete' if report['substantive_complete'] and not withheld else 'incomplete',
            'structural_complete': report['structural_complete'] and not withheld,
            'substantive_complete': report['substantive_complete'] and not withheld,
            'counts': counts, 'reasons': ['P_PUBLIC_CONTENT'] if withheld else [],
            'accepted': report['basis']['accepted'], 'release_eligible': report['basis']['release_eligible']}


@lc._within_assessment
def render(state, output, scope='default', audience='private'):
    """Create deterministic JSON/Markdown views without granting publication authority.

    Args:
        state: Existing governed State with exact selected content and decisions.
        output: Exact assessed product version.
        scope: Authorized current output use scope.
        audience: Private operator report or explicitly entitled public projection.
    Returns:
        Report, semantic views and separate current publication eligibility.
    Raises:
        ProtocolError: Invalid audience, unavailable content or unsupported profile.
    """
    if audience not in {'private', 'public'}:
        raise lc.ERROR('P_SCOPE', 'A projection audience must be explicit')
    report, profile, products, selected = _assessed(state, output, scope, True)
    released = report['basis']['release_eligible'] and report['substantive_complete']
    public_scope = profile['scope']['classification'] == 'public'
    units = []
    withheld = False
    for row in report['obligations']:
        if row['unit'] is None:
            continue
        product = products[row['unit']['product']['version_id']]
        unit = next(value for value in product[2]['units'] if value['key'] == row['unit']['unit'])
        if audience == 'public' and not (released and public_scope and unit['classification'] == 'public'):
            withheld = True
            continue
        units.append((row['key'], unit, row['unit']))
    public_ids = {key: 'unit-' + str(index + 1) for index, (key, _, _) in enumerate(units)}
    visible = {_locator_key(locator, output): public_ids[key] for key, _, locator in units}
    views = []
    for obligation in profile['required_views']:
        entries = []
        for key, unit, locator in units:
            if key not in obligation['unit_obligations']:
                continue
            entries.append({'id': public_ids[key] if audience == 'public' else key,
                            'group': unit['group'], 'title': unit['title'], 'statements': unit['statements'],
                            'properties': unit['properties'], **({} if audience == 'public' else {'locator': locator})})
        links = []
        view_row = next(row for row in report['views'] if row['view'] == obligation['view'])
        binding_ref = view_row['binding']
        bound_relations = set()
        if binding_ref is not None:
            binding_product = products[binding_ref['product']['version_id']]
            binding = next(item for item in binding_product[2]['view_bindings'] if item['view'] == binding_ref['view'])
            bound_relations = {_locator_key(item, binding_ref['product']) for item in binding['relations']}
        selected_relations = {_locator_key(row['relation'], output) for row in report['relations']
                              if row['key'] in obligation['relation_obligations'] and row['status'] == 'satisfied' and row['relation'] is not None}
        projected_relations = selected_relations & bound_relations
        for product in products.values():
            for relation in product[2]['relations']:
                if (product[0]['ref']['version_id'], relation['key']) not in projected_relations:
                    continue
                origin = _locator_key(relation['from'], product[0]['ref'])
                target = _locator_key(relation['to'], product[0]['ref'])
                if audience == 'public':
                    if not released or not public_scope or origin not in visible or target not in visible or any(unit['classification'] != 'public' for unit in product[2]['units']):
                        withheld = True
                        continue
                    links.append({'id': 'relation-' + str(len(links) + 1), 'type': relation['type'], 'from': visible[origin], 'to': visible[target], 'rationale': relation['rationale']})
                else:
                    links.append({'id': relation['key'], 'type': relation['type'], 'from': {'product': state._reference(origin[0]), 'unit': origin[1]}, 'to': {'product': state._reference(target[0]), 'unit': target[1]}, 'rationale': relation['rationale']})
        body = {'view': obligation['view'], 'audience': audience, 'status': 'complete' if report['substantive_complete'] and not withheld else 'incomplete',
                'claim_boundary': _catalogue()['claim_boundary'], 'units': entries, 'relations': links}
        if audience == 'private':
            body.update(output=report['output'], profile=report['profile'], gaps=[row for row in report['obligations'] + report['relations'] if row['status'] not in {'satisfied', 'excluded'}])
        lines = ['# ' + obligation['view'], '', body['claim_boundary'], '', 'Assessment: ' + body['status'], '']
        for entry in entries:
            lines.extend(['## ' + entry['title'], '', *entry['statements'], ''])
            lines.extend('- ' + key + ': ' + value for key, value in sorted(entry['properties'].items()))
            lines.append('')
        for link in links:
            lines.extend(['- ' + link['type'] + ': ' + (link['from'] if isinstance(link['from'], str) else link['from']['unit']) + ' -> ' + (link['to'] if isinstance(link['to'], str) else link['to']['unit']), '  ' + link['rationale']])
        if audience == 'private':
            lines.extend(['', 'Output version: ' + output['version_id'], 'Use scope: ' + scope, 'Profile: ' + profile['catalogue_id'] + '/' + profile['catalogue_version'], 'Accepted: ' + str(report['basis']['accepted']), 'Release eligible: ' + str(report['basis']['release_eligible'])])
        views.append({'view': obligation['view'], 'json': body, 'markdown': '\n'.join(lines).rstrip() + '\n'})
    eligible = bool(released and (audience == 'private' or public_scope and not withheld))
    return {'report': _public_report(report, withheld) if audience == 'public' else report,
            'views': views, 'publication': {'eligible': eligible, 'accepted': report['basis']['accepted'],
                                           'release_eligible': report['basis']['release_eligible'], 'authority_created': False}}
