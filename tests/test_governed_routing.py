# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Global professional availability does not dictate any layer's local staff."""
import copy

import pytest

from governed_fixtures import GovernedHarness, QUESTIONS, lc, routing
import model_router


@pytest.fixture
def captured(tmp_path, monkeypatch):
    host = GovernedHarness(tmp_path, monkeypatch)
    prepared = host.bootstrap_message()
    source = prepared['payload']['l0_inputs'][-1]['record']
    snapshot = routing.load_policy(source, host.store._blob)
    return host, source, snapshot, host.routing_policy


def _assignment(host, reference, layer=1, question='how', responsibility='author'):
    return {'owner': host.owner(question, layer=layer), 'responsibility': responsibility,
            'routing': {'policy': reference}, 'issued_under': None,
            'effects': [{'operation': name, 'tool_policy': None, 'destination_handle': None}
                        for name in ('read', 'propose')],
            'limits': [{'metric': 'tokens', 'unit': 'governed-token', 'ceiling': 10000}]}


def _choice(reference, specialties):
    return {'action': 'select_execution', 'assignment': reference, 'previous': None, 'specialties': specialties,
            'provider': 'json-process/1', 'workload_class': 'fixture-author',
            'model_selector': 'fixture-author', 'reason': 'Local functional entity chooses its own professionals.',
            'authority_proof': None}


def test_global_catalogue_allows_local_professional_choice_in_all_36_cells(captured, monkeypatch):
    host, _, snapshot, reference = captured
    monkeypatch.setenv('AI_HOUSE_MODEL_CONFIG', '/unavailable/ambient-override.json')
    assert len(snapshot['instructions']) == snapshot['catalogue']['count']
    for layer in range(1, 7):
        for question in QUESTIONS:
            assignment = _assignment(host, reference, layer, question)
            global_policy = routing.validate_assignment(assignment, snapshot, 'host-routing')
            assert 'specialties' not in global_policy
            for specialty in ('software-engineer', 'internal-it-auditor'):
                selected = routing.select_execution(assignment, snapshot, _choice(reference, [specialty]))
                selector, mapping = model_router.resolve_snapshot(snapshot['models'], 'json-process/1', 'fixture-author')
                assert selected['model_selector'] == selector
                assert selected['model'] == mapping
                assert selected['specialties'] == [specialty]
    combined = routing.select_execution(_assignment(host, reference), snapshot,
                                         _choice(reference, ['software-engineer', 'internal-it-auditor']))
    assert combined['allowed_operations'] == ['propose', 'read']


def test_capture_replay_is_deterministic_and_requires_the_full_intrinsic_catalogue(captured):
    host, source, snapshot, _ = captured
    descriptor = snapshot['descriptor']
    assert routing.capture_policy(descriptor['policy_id'],
        host.store._blob(descriptor['catalogue_blob_id']), host.store._blob(descriptor['models_blob_id']),
        {slug: host.store._blob(identifier) for slug, identifier in descriptor['instruction_blobs'].items()},
        descriptor['bootstrap'], descriptor['capabilities'], host.store.put_blob) == source['material']
    assert routing.load_policy(source, host.store._blob) == snapshot
    missing = copy.deepcopy(source)
    missing['material'].remove(descriptor['instruction_blobs']['internal-it-auditor'])
    with pytest.raises(lc.ERROR) as failure:
        routing.load_policy(missing, host.store._blob)
    assert failure.value.code == 'P_PROOF'


def test_global_bounds_and_unknown_capabilities_fail_without_staffing_whitelists(captured):
    host, _, snapshot, reference = captured
    assignment = _assignment(host, reference)
    with pytest.raises(lc.ERROR) as failure:
        routing.validate_assignment(assignment, snapshot, 'another-policy')
    assert failure.value.code == 'P_SCOPE'
    oversized = copy.deepcopy(assignment)
    oversized['limits'][0]['ceiling'] += 1
    with pytest.raises(lc.ERROR) as failure:
        routing.validate_assignment(oversized, snapshot, 'host-routing')
    assert failure.value.code == 'P_BUDGET'
    with pytest.raises(lc.ERROR) as failure:
        routing.select_execution(assignment, snapshot, _choice(reference, ['not-a-catalogue-professional']))
    assert failure.value.code == 'P_PROOF'
    unavailable = _choice(reference, ['software-engineer'])
    unavailable['model_selector'] = 'unavailable-worker'
    with pytest.raises(lc.ERROR) as failure:
        routing.select_execution(assignment, snapshot, unavailable)
    assert failure.value.code == 'P_PROOF'
