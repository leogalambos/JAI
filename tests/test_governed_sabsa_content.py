# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Pure structural contracts; these examples are not reviewed engagement results."""
import copy
import json
from pathlib import Path

import pytest

from governed_fixtures import delivery
import lifecycle as lc
import governed_sabsa as content


EXAMPLES = Path(__file__).resolve().parents[1] / '.ai/runtime/protocol/governed-delivery/v1/examples'
LAYERS = ('contextual', 'conceptual', 'logical', 'physical', 'component', 'management')
QUESTIONS = ('what', 'why', 'how', 'who', 'where', 'when')
DEDICATED = {'conceptual.attributes', 'management.activity', 'management.measure', 'management.observation'}
VIEWS = {'architecture', 'executive-summary', 'risk-treatment-plan', 'policy-architecture',
         'trust-model', 'information-access-model', 'security-service-catalogue',
         'component-realisation', 'assurance-plan', 'governance-register', 'current-state',
         'target-state', 'transition-architecture', 'transition-roadmap', 'lifecycle-register',
         'framework-mapping', 'compliance-gap-analysis', 'reuse-register', 'client-questions'}


def _example(name):
    return json.loads((EXAMPLES / (name + '.json')).read_text())


def _without(profile, keys):
    result = copy.deepcopy(profile)
    result['required_units'] = [item for item in result['required_units'] if item['key'] not in keys]
    removed = {item['key'] for item in result['required_relations']
               if item['from_obligation'] in keys or item['to_obligation'] in keys}
    result['required_relations'] = [item for item in result['required_relations'] if item['key'] not in removed]
    for view in result['required_views']:
        view['unit_obligations'] = [key for key in view['unit_obligations'] if key not in keys]
        view['relation_obligations'] = [key for key in view['relation_obligations'] if key not in removed]
    return result


def _unit(key, group, properties):
    return {'key': key, 'group': group, 'title': 'Fictional ' + key,
            'statements': ['A structural illustration, not execution or effectiveness evidence.'],
            'properties': properties, 'classification': 'public'}


def _payload(units):
    return {'format': 'jai-sabsa-content/1', 'units': units, 'relations': [], 'view_bindings': []}


def test_catalogue_preserves_all_six_perspectives_dedicated_information_and_view_purposes():
    catalogue = content.catalogue()
    assert catalogue['catalogue_id'] == 'jai-sabsa-minimum' and catalogue['catalogue_version'] == '1'
    expected = {layer + '.' + question for layer in LAYERS for question in QUESTIONS} | DEDICATED
    assert set(catalogue['groups']) == expected
    for index, layer in enumerate(LAYERS, 1):
        for question in QUESTIONS:
            group = catalogue['groups'][layer + '.' + question]
            assert group['layer'] == index and group['question'] == question
    assert {key: value['edition'] for key, value in catalogue['method_sources'].items()} == {
        'S1': 'TSI-R101/1.0/2018', 'S2': 'TSI-W100/1995-2009'}
    assert set(catalogue['views']) == VIEWS
    assert set(catalogue['trace_relations']) == {'justifies', 'refines', 'realizes'}
    assert {'measures', 'observes', 'feedback_for'} <= set(catalogue['relations'])
    assert set(catalogue['groups']['conceptual.attributes']['required_properties']) == {
        'business_justification', 'target', 'unit', 'measurement_method', 'accountable_owner', 'evaluation_horizon'}
    catalogue['groups'].clear()
    assert set(content.catalogue()['groups']) == expected


def test_maintained_profile_is_explicitly_scoped_and_cannot_silently_drop_its_business_profile():
    profile = _example('sabsa-content-profile')
    assert content.validate_profile(profile) == profile
    assert {item['group'] for item in profile['required_units']} == {
        layer + '.' + question for layer in LAYERS for question in QUESTIONS} | DEDICATED
    assert any(item['type'] == 'feedback_for' for item in profile['required_relations'])
    assert len(profile['required_views']) < len(VIEWS), 'Available views are not all universally mandatory'
    with pytest.raises(lc.ERROR) as missing_attribute:
        content.validate_profile(_without(profile, {'availability-attribute'}))
    assert missing_attribute.value.code == 'P_PROOF'
    unsupported = copy.deepcopy(profile)
    unsupported['method_sources'][0]['edition'] = 'unadopted-future-edition'
    with pytest.raises(lc.ERROR) as source_gap:
        content.validate_profile(unsupported)
    assert source_gap.value.code == 'P_PROOF'
    wrong_owner = copy.deepcopy(profile)
    next(item for item in wrong_owner['required_units'] if item['group'] == 'logical.what')['owner']['layer'] = 2
    with pytest.raises(lc.ERROR) as ownership:
        content.validate_profile(wrong_owner)
    assert ownership.value.code == 'P_SCOPE'


def test_business_attributes_require_their_actual_fields_and_keep_decimal_quantities_as_strings():
    payload = _example('sabsa-content')
    owner = {'layer': 2, 'work_kind': 'question', 'question': 'why', 'work_item': 'fictional-service'}
    assert content._validate_units(payload, owner) == payload
    attribute = next(unit for unit in payload['units'] if unit['group'] == 'conceptual.attributes')
    assert attribute['properties']['target'] == '99.5'
    malformed = copy.deepcopy(payload)
    properties = next(unit for unit in malformed['units'] if unit['group'] == 'conceptual.attributes')['properties']
    properties.pop('measurement_method')
    properties['decorative_score'] = '100'
    with pytest.raises(lc.ERROR) as missing_method:
        content._validate_units(malformed, owner)
    assert missing_method.value.code == 'P_PROOF'
    wrong_type = copy.deepcopy(payload)
    next(unit for unit in wrong_type['units'] if unit['group'] == 'conceptual.attributes')['properties']['target'] = 99
    with pytest.raises(lc.ERROR):
        delivery.validate(wrong_type, 'sabsa-content.schema.json')
    with pytest.raises(lc.ERROR) as wrong_layer:
        content._validate_units(payload, {**owner, 'layer': 3})
    assert wrong_layer.value.code == 'P_SCOPE'


def test_management_definitions_and_observations_have_distinct_typed_contracts():
    owner = {'layer': 6, 'work_kind': 'question', 'question': 'how', 'work_item': 'fictional-service'}
    activity = _unit('monitor-service', 'management.activity', {
        'objective': 'Detect failure of the fictional service.', 'responsible_actor': 'Fictional service operator',
        'inputs': 'Probe schedule and scoped endpoint.', 'outputs': 'Recorded probe results and incident request.',
        'scope': 'The fictional service boundary.', 'trigger': 'Scheduled probe event.', 'timing': 'Every five minutes.',
        'controls': 'Authenticated probe configuration.', 'required_evidence': 'Time-stamped probe result.'})
    measure = _unit('availability', 'management.measure', {
        'target': '99.5', 'unit': 'percent', 'method': 'Successful probes divided by scheduled probes.',
        'source': 'Authenticated probe observations.', 'frequency': 'Monthly evaluation.',
        'thresholds': 'Below the requested target.', 'action': 'Open an improvement request.', 'owner': 'Fictional service owner'})
    definitions = _payload([activity, measure])
    assert content._validate_units(definitions, owner) == definitions
    missing = copy.deepcopy(definitions)
    missing['units'][1]['properties'].pop('frequency')
    with pytest.raises(lc.ERROR) as absent_frequency:
        content._validate_units(missing, owner)
    assert absent_frequency.value.code == 'P_PROOF'
    observation = _payload([_unit('sample-observation', 'management.observation', {
        'subject': 'Fictional scoped service.', 'measure': 'Availability probe.', 'period': 'Illustrative period only.',
        'method': 'Structural example, no live probe was executed.', 'result': 'Fictional sample, not operating evidence.'})])
    observer = {**owner, 'work_kind': 'measurement', 'question': None}
    assert content._validate_units(observation, observer, 'observation') == observation
    with pytest.raises(lc.ERROR) as no_execution_claim:
        content._validate_units(definitions, owner, 'observation')
    assert no_execution_claim.value.code == 'P_SCOPE'
    with pytest.raises(lc.ERROR) as no_definition_substitute:
        content._validate_units(observation, observer, 'answer')
    assert no_definition_substitute.value.code == 'P_SCOPE'


def test_observation_endpoint_validator_requires_a_measure_definition(monkeypatch):
    """Isolate semantic validation, not execution, review, or L6 authority."""
    from types import SimpleNamespace

    foreign = {'engagement': 'semantic-unit', 'scope': 'default', 'logical_id': 'definitions',
               'version_id': 'a' * 64}
    measure = _unit('availability', 'management.measure', {
        'target': '99.5', 'unit': 'percent', 'method': 'Successful probes divided by scheduled probes.',
        'source': 'Probe records.', 'frequency': 'Monthly.', 'thresholds': 'Below target.',
        'action': 'Investigate.', 'owner': 'Fictional operator'})
    activity = _unit('operate', 'management.activity', {
        'objective': 'Operate the fictional service.', 'responsible_actor': 'Operator',
        'inputs': 'Schedule', 'outputs': 'Records', 'scope': 'Fictional service',
        'trigger': 'Schedule', 'timing': 'Daily', 'controls': 'Configuration', 'required_evidence': 'Log'})
    definition = _payload([measure, activity])
    observed = _payload([_unit('sample', 'management.observation', {
        'subject': 'Fictional service', 'measure': 'Availability', 'period': 'Illustration',
        'method': 'Structural example', 'result': 'Fictional result'})])
    observed['relations'] = [
        {'key': 'measurement', 'type': 'measures',
         'from': {'product': foreign, 'unit': 'availability'},
         'to': {'product': None, 'unit': 'sample'}, 'rationale': 'The exact measure defines this observation.'},
        {'key': 'subject', 'type': 'observes',
         'from': {'product': None, 'unit': 'sample'},
         'to': {'product': foreign, 'unit': 'operate'}, 'rationale': 'The observed fictional operation.'}]
    raw = {lc.blob(lc.canonical(definition)): lc.canonical(definition),
           lc.blob(lc.canonical(observed)): lc.canonical(observed)}
    record = {'owner': {'layer': 6, 'work_kind': 'measurement', 'question': None, 'work_item': 'fictional-service'},
              'product_kind': 'observation', 'profile': foreign,
              'material': [lc.blob(lc.canonical(observed))], 'evidence': [foreign]}
    state = SimpleNamespace(_assessment_walk=None, scope='default',
        _product_records={}, _product_content={foreign['version_id']: definition},
        _governing_input=lambda point, live: point == {'ref': foreign, 'use_scope': 'default'},
        _validation_bytes=lambda identifier, live: raw[identifier],
        _dependencies=lambda record: [{'ref': foreign, 'use_scope': 'default'}],
        _closure=lambda point: [point],
        resolve=lambda reference, family: {'material': [lc.blob(lc.canonical(definition))]})
    monkeypatch.setattr(content, '_policy', lambda *args: (foreign, {'required_units': []}, 'default'))
    assert content.validate_product(state, record) == observed
    wrong = copy.deepcopy(observed)
    wrong['relations'][0]['from']['unit'] = 'operate'
    identifier = lc.blob(lc.canonical(wrong))
    raw[identifier] = lc.canonical(wrong)
    with pytest.raises(lc.ERROR) as failure:
        content.validate_product(state, {**record, 'material': [identifier]})
    assert failure.value.code == 'P_PROOF'
    state._dependencies = lambda record: []
    with pytest.raises(lc.ERROR) as undeclared:
        content.validate_product(state, record)
    assert undeclared.value.code == 'P_SCOPE'
    state._dependencies = lambda record: [{'ref': foreign, 'use_scope': 'unaccepted'}]
    with pytest.raises(lc.ERROR) as inapplicable:
        content.validate_product(state, record)
    assert inapplicable.value.code == 'P_CONTEXT'


def test_projection_uses_exact_selected_relation_not_an_unrelated_same_key(monkeypatch):
    """Exercise rendering with assessed semantic collaborators, not Store qualification."""
    from types import SimpleNamespace

    refs = {name: {'engagement': 'projection-unit', 'scope': 'default', 'logical_id': name,
                   'version_id': digit * 64} for name, digit in [('A', 'a'), ('B', 'b')]}
    units = [_unit('driver', 'contextual.why', {'business_role': 'driver'}),
             _unit('quality', 'contextual.why', {'business_role': 'quality_attribute'})]
    products = {}
    for name, ref in refs.items():
        semantic = _payload(copy.deepcopy(units))
        semantic['relations'] = [{'key': 'quality-basis', 'type': 'justifies',
            'from': {'product': None, 'unit': 'quality'}, 'to': {'product': None, 'unit': 'driver'},
            'rationale': 'Selected B rationale' if name == 'B' else 'Unrelated A rationale'}]
        semantic['view_bindings'] = [{'view': 'architecture',
            'units': [{'product': None, 'unit': key} for key in ('driver', 'quality')],
            'relations': [{'product': None, 'relation': 'quality-basis'}]}]
        products[ref['version_id']] = ({'ref': ref, 'use_scope': 'default'}, {}, semantic)
    selected = {key: {'product': refs['B'], 'unit': key} for key in ('driver', 'quality')}
    profile = {'catalogue_id': 'jai-sabsa-minimum', 'catalogue_version': '1',
        'scope': {'classification': 'public'},
        'required_relations': [{'key': 'quality-basis', 'type': 'justifies',
            'from_obligation': 'quality', 'to_obligation': 'driver'}],
        'required_views': [{'view': 'architecture', 'unit_obligations': ['driver', 'quality'],
                            'relation_obligations': ['quality-basis']}]}
    report = {'profile': {'ref': refs['B']}, 'output': {'ref': refs['B'], 'use_scope': 'default'},
        'status': 'complete', 'structural_complete': True, 'substantive_complete': True,
        'basis': {'qualified': True, 'accepted': True, 'release_eligible': True},
        'obligations': [{'key': key, 'unit': locator, 'status': 'satisfied', 'reasons': []}
                        for key, locator in selected.items()],
        'relations': [{'key': 'quality-basis', 'status': 'satisfied', 'reasons': [],
                       'relation': {'product': refs['B'], 'relation': 'quality-basis'}}],
        'views': [{'view': 'architecture', 'status': 'satisfied', 'reasons': [],
                   'binding': {'product': refs['B'], 'view': 'architecture'}}]}
    state = SimpleNamespace(_assessment_walk=None,
        _reference=lambda identifier: next(ref for ref in refs.values() if ref['version_id'] == identifier))
    monkeypatch.setattr(content, '_assessed', lambda *args: (copy.deepcopy(report), profile, products, selected))
    for audience in ('private', 'public'):
        rendered = content.render(state, refs['B'], audience=audience)
        edges = rendered['views'][0]['json']['relations']
        assert len(edges) == 1
        assert edges[0]['rationale'] == 'Selected B rationale'
        assert 'Unrelated A rationale' not in json.dumps(rendered)
        if audience == 'private':
            assert edges[0]['from']['product'] == refs['B']
            assert edges[0]['to']['product'] == refs['B']
        else:
            assert edges[0]['id'] == 'relation-1'
            assert edges[0]['from'].startswith('unit-') and edges[0]['to'].startswith('unit-')
