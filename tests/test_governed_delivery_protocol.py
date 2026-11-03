# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Offline P02 shape/canonicalization contracts; P03 semantic guards are not run."""
import copy
from functools import lru_cache
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import urldefrag, urlsplit

import jsonschema
import pytest
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / '.ai/runtime/protocol/governed-delivery/v1'
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
SPEC = importlib.util.spec_from_file_location('p02_existing_lifecycle', ROOT / '.ai/runtime/tools/lifecycle.py')
LIFECYCLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIFECYCLE)
MANIFEST = json.loads((PACKAGE / 'conformance/manifest.json').read_text())


def _read(relative):
    path = (PACKAGE / relative).resolve()
    if not path.is_relative_to(PACKAGE.resolve()):
        raise ValueError('Conformance resource escapes the offline package')
    return json.loads(path.read_text(encoding='utf-8'))


def _references(value):
    if isinstance(value, dict):
        if '$ref' in value:
            yield value['$ref']
        for child in value.values():
            yield from _references(child)
    elif isinstance(value, list):
        for child in value:
            yield from _references(child)


def _build_offline_validator(filename, replacement=None):
    # Preload only declared package schemas; even a mistaken reference cannot fetch.
    schemas = {path.name: _read(path.name) for path in PACKAGE.glob('*.schema.json')}
    if replacement is not None:
        schemas[filename] = replacement
    resources = []
    for name, rules in schemas.items():
        for target in _references(rules):
            location, _ = urldefrag(target)
            parsed = urlsplit(location)
            if parsed.scheme or parsed.netloc or (location and location not in schemas):
                raise ValueError('Only declared local schema references are permitted')
        jsonschema.Draft202012Validator.check_schema(rules)
        rules = {**rules, '$id': (PACKAGE / name).as_uri()}
        resources.append((rules['$id'], Resource.from_contents(rules)))
        schemas[name] = rules

    def unavailable(uri):
        raise NoSuchResource(ref=uri)

    registry = Registry(retrieve=unavailable).with_resources(resources)
    return jsonschema.Draft202012Validator(schemas[filename], registry=registry)


@lru_cache(maxsize=None)
def _cached_offline_validator(filename):
    return _build_offline_validator(filename)


def _offline_validator(filename, replacement=None):
    if replacement is not None:
        return _build_offline_validator(filename, replacement)
    return _cached_offline_validator(filename)


@pytest.mark.parametrize('case', MANIFEST['structural']['positive'], ids=lambda case: case['id'])
def test_published_positive_shapes_are_accepted_offline(case):
    errors = list(_offline_validator(case['schema']).iter_errors(_read(case['file'])))
    assert not errors, [error.message for error in errors]


@pytest.mark.parametrize('case', MANIFEST['structural']['negative'], ids=lambda case: case['id'])
def test_closed_contract_rejects_each_invalid_shape(case):
    with pytest.raises(jsonschema.ValidationError):
        _offline_validator(case['schema']).validate(_read(case['file']))


def test_catalogue_covers_every_message_action_and_control_family():
    messages = [_read(case['file']) for case in MANIFEST['structural']['positive'] if case['schema'] == 'message.schema.json']
    assert {value['message_type'] for value in messages} == {
        'bootstrap', 'record_proposal', 'assignment', 'submission', 'observation',
        'review', 'integration', 'handoff', 'handoff_acceptance', 'information_request',
        'information_response', 'change_request', 'escalation', 'decision', 'relay', 'control_event',
    }
    assert {value['payload']['action'] for value in messages if value['message_type'] == 'decision'} == {
        'rework', 'reformulate', 'select', 'continue', 'speculate', 'resume',
        'invalidate', 'reinstate', 'accept', 'release', 'terminate',
        'select_execution', 'resolve_escalation',
    }
    assert {value['payload']['record_type'] for value in messages if value['message_type'] == 'record_proposal'} == {
        'source', 'profile', 'assignment', 'context', 'product', 'assessment',
    }
    assert {value['payload']['event'] for value in messages if value['message_type'] == 'control_event'} == {
        'renew_control', 'run_started', 'run_completed', 'run_cancelled', 'usage_audit',
    }


@pytest.mark.parametrize('layer', range(1, 7))
def test_each_layer_can_encode_its_owned_assignment(layer):
    record = _read('examples/record-assignment.json')['payload']['record']
    record['owner']['layer'] = layer
    assert _offline_validator('record.schema.json').is_valid(record)


def test_exact_wire_limits_accept_boundary_values():
    value = _read('examples/submission.json')
    value.update(request_id='x' * 128, correlation_id='x' * 128,
                 issued_at_ms=9007199254740990, expires_at_ms=9007199254740991)
    assert _offline_validator('message.schema.json').is_valid(value)


@pytest.mark.parametrize('target', ['https://example.invalid/schema.json', '../escaped.schema.json', 'file:///tmp/schema.json'])
def test_offline_schema_loader_rejects_remote_and_escaping_references(target):
    with pytest.raises(ValueError, match='declared local'):
        _offline_validator('message.schema.json', {'$schema': 'https://json-schema.org/draft/2020-12/schema', '$ref': target})


@pytest.mark.parametrize('case', _read('conformance/raw-canonical.json'), ids=lambda case: case['id'])
def test_raw_canonical_vectors_use_the_existing_strict_lifecycle_parser(case):
    if case['accept']:
        assert LIFECYCLE.canonical(LIFECYCLE.loads(case['raw'])).decode('utf-8') == case['canonical']
    else:
        with pytest.raises(ValueError):
            LIFECYCLE.loads(case['raw'])


def _message_id(value):
    unsigned = {key: item for key, item in value.items() if key != 'message_id'}
    return hashlib.sha256(b'jai.delivery.message.v1\0' + LIFECYCLE.canonical(unsigned)).hexdigest()


def test_message_identities_bind_context_payload_recipient_and_order():
    original = _read('examples/submission.json')
    assert original['message_id'] == _message_id(original)
    for field, replacement in [('context', _read('examples/review.json')['payload']['assignment']),
                               ('recipient', {'kind': 'controller', 'id': 'different-controller'}),
                               ('issued_at_ms', original['issued_at_ms'] + 1)]:
        changed = copy.deepcopy(original)
        changed[field] = replacement
        assert _message_id(changed) != original['message_id']
    changed = copy.deepcopy(original)
    changed['payload']['limitations'] = ['Additional disclosed limitation']
    assert _message_id(changed) != original['message_id']
    ordered = copy.deepcopy(original)
    ordered['payload']['limitations'] = ['First limitation', 'Second limitation']
    reversed_order = copy.deepcopy(ordered)
    reversed_order['payload']['limitations'].reverse()
    assert _message_id(ordered) != _message_id(reversed_order)


def test_examples_use_actual_existing_content_identity_domains():
    fixtures = _read('conformance/fixtures.json')
    known = {LIFECYCLE.version_id(value) for value in fixtures['manifests'].values()}
    for blob_id, raw in fixtures['blobs'].items():
        assert LIFECYCLE.blob(raw.encode('utf-8')) == blob_id

    def references(value):
        if isinstance(value, dict):
            if set(value) == {'engagement', 'scope', 'logical_id', 'version_id'}:
                yield value
            for child in value.values():
                yield from references(child)
        elif isinstance(value, list):
            for child in value:
                yield from references(child)

    for case in MANIFEST['structural']['positive']:
        value = _read(case['file'])
        for ref in references(value):
            assert ref['version_id'] in known, ref
            assert LIFECYCLE.version_id(fixtures['manifests'][ref['logical_id']]) == ref['version_id']
        if case['schema'] == 'message.schema.json':
            assert value['message_id'] == _message_id(value)


def test_semantic_vectors_are_schema_valid_contract_data_not_executed_guards():
    vectors = _read(MANIFEST['semantic'])
    assert vectors['execution_status'] == 'specified-not-executed-P03'
    assert MANIFEST['semantic_execution_status'] == 'specified-not-executed-P03'
    validator = _offline_validator('message.schema.json')
    for case in vectors['cases']:
        assert {'id', 'trusted_context', 'initial_state', 'message', 'expected'} <= case.keys()
        validator.validate(case['message'])
        assert case['message']['message_id'] == _message_id(case['message'])
    # P03 must execute these guards; this test proves only portable input shape.
    assert {f'L{layer}-foreign-owner' for layer in range(1, 7)} <= {case['id'] for case in vectors['cases']}


def _fixture_manifest(ref, registry):
    value = registry[ref['logical_id']]
    assert LIFECYCLE.version_id(value) == ref['version_id']
    assert value['logical_id'] == ref['logical_id']
    return value


def test_semantic_fixture_identities_bind_actual_closed_record_bodies():
    fixtures = _read('conformance/fixtures.json')
    registry = fixtures['manifests']
    validators = {}
    for kind in {'source', 'profile', 'assignment', 'context', 'product', 'assessment'}:
        rules = _read('record.schema.json')
        rules = {**rules, 'oneOf': [{'$ref': '#/$defs/' + kind}]}
        validators[kind] = _offline_validator('record.schema.json', rules)
    for value in registry.values():
        if value['kind'] == 'decision':
            # Intrinsic decisions are existing signed message records, not a
            # seventh producer-authored record family.
            assert set(value['content']) == {'message'}
            message = value['content']['message']
            _offline_validator('message.schema.json').validate(message)
            assert message['message_type'] == 'decision'
            if message['payload']['action'] == 'select_execution':
                assert message['sender'] == {'kind': 'assignment', 'ref': message['payload']['assignment']}
                context = _fixture_manifest(message['context'], registry)['content']
                assert context['execution'] == {'phase': 'selection'}
                assert context['assignment'] == message['payload']['assignment']
            else:
                assert message['payload']['action'] == 'speculate'
                assert message['sender'] == {'kind': 'authority', 'id': 'human-owner'}
                assert message['payload']['authority_proof'] in fixtures['blobs']
                assert _fixture_manifest(message['context'], registry)['content']['assignment'] is None
            continue
        # Label-only manifests cannot stand in for issued assignments or products.
        assert value['kind'] in validators
        assert validators[value['kind']].is_valid(value['content'])
    vectors = _read('conformance/semantic-vectors.json')
    for item in vectors['shared_state_material']['available_versions']:
        assert _fixture_manifest(item['ref'], registry) == item['manifest']
    for family in validators:
        proposal = _read('examples/record-' + family + '.json')['payload']
        stored = registry[proposal['logical_id']]
        assert stored['kind'] == family == proposal['record_type']
        assert stored['content'] == proposal['record']
        assert LIFECYCLE.version_id(stored) == LIFECYCLE.version_id(
            LIFECYCLE.manifest(proposal['logical_id'], family, proposal['record']))
    for case in vectors['cases']:
        trusted = case['trusted_context']
        context = _fixture_manifest(trusted['context'], registry)['content']
        assert context['profile'] == trusted['profile']
        assert context['assignment'] == trusted['assignment']
        assert context['owner'] == trusted['owner']
        assert context['run_id'] == trusted['run_id']
        if case['id'] != 'forged-origin':
            assert context['issued_to'] == trusted['principal']
        if trusted['assignment'] is not None:
            assignment = _fixture_manifest(trusted['assignment'], registry)['content']
            assert assignment['owner'] == trusted['owner']
            assert assignment['responsibility'] == trusted['responsibility']
            assert assignment['profile'] == trusted['profile']


def test_AB_roadmap_uses_current_head_and_fresh_B_assignments_and_evidence():
    registry = _read('conformance/fixtures.json')['manifests']
    scenario = _read('conformance/semantic-vectors.json')['scenarios'][0]
    assert scenario['execution_status'] == 'roadmap-not-executable-transition-vector'
    transition = scenario['steps'][0]['message']
    assert transition['expected_head'] == scenario['initial_state']['head']
    assert transition['sender'] == {'kind': 'controller', 'id': scenario['trusted_context']['principal']}
    assert transition['context'] == scenario['trusted_context']['context']
    fresh = scenario['steps'][1]
    source_B = transition['payload']['replacements'][0]['replacement']
    for assignment_name, context_name in [('author_assignment', 'author_context'),
                                           ('measurement_assignment', 'measurement_context')]:
        assignment = _fixture_manifest(fresh[assignment_name], registry)['content']
        context = _fixture_manifest(fresh[context_name], registry)['content']
        assert context['assignment'] == fresh[assignment_name]
        assert assignment['inputs'] == [{'slot_id': 'source', 'refs': [source_B]}]
        assert context['inputs'] == assignment['inputs']
    observation = _fixture_manifest(fresh['observation'], registry)['content']
    candidate = _fixture_manifest(fresh['candidate'], registry)['content']
    assert observation['assignment'] == fresh['measurement_assignment']
    assert candidate['assignment'] == fresh['author_assignment']
    assert candidate['evidence'] == [fresh['observation']]
    assert candidate['inputs'] == observation['inputs'] == [{'slot_id': 'source', 'refs': [source_B]}]
    assert fresh['observation'] != scenario['initial_state']['observation']
    assert fresh['candidate'] != scenario['initial_state']['candidate']
