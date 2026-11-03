# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""The canonical CLI parses proposals; the sole trusted runtime recorder writes."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

from governed_fixtures import GovernedHarness, CONTROLLER, delivery, lc

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('governed_cli_tests', ROOT / '.ai/runtime/fabric/fabric.py')
fabric = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fabric)


def test_log_path_bounds_and_store_factory_do_not_grant_authority(tmp_path, monkeypatch):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path))
    assert fabric.log_path('a' * 128) == str(tmp_path / ('a' * 128 + '.jsonl'))
    for invalid in ('', '.', '..', '../escape', 'a/b', 'a\\b', 'a' * 129):
        with pytest.raises(ValueError):
            fabric.log_path(invalid)
    store = fabric.open_fabric('proposal')
    assert isinstance(store, lc.Store)
    assert not (tmp_path / 'proposal.jsonl').exists()


def test_validate_checks_identity_without_recording_or_granting_authority(tmp_path, capsys):
    message = json.loads((delivery.PACKAGE / 'examples/bootstrap.json').read_text())
    message['message_id'] = delivery.message_id(message)
    source = tmp_path / 'proposal.json'; source.write_bytes(lc.canonical(message))
    before = sorted(tmp_path.iterdir())
    assert fabric.main(['validate', '--message', str(source)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result['message_id'] == message['message_id']
    assert result['structurally_valid'] is True
    assert result['authority_granted'] is False
    assert sorted(tmp_path.iterdir()) == before
    message['payload']['controller_id'] = 'substituted-controller'
    source.write_bytes(lc.canonical(message))
    assert fabric.main(['validate', '--message', str(source)]) == 2
    assert 'rejected' in capsys.readouterr().err.lower()


def test_retired_mutation_commands_have_no_effect_or_signing_route(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path))
    for command in ('init', 'ingest', 'review', 'authorise', 'release', 'lifecycle-apply', 'keygen', 'selftest'):
        assert fabric.main([command, 'legacy']) == 2
        assert 'Unsupported archive workflow' in capsys.readouterr().err
    assert not list(tmp_path.iterdir())


def test_cli_submit_records_runtime_message_without_any_internal_proof(tmp_path, monkeypatch, capsys):
    harness = GovernedHarness(tmp_path, monkeypatch)
    harness.bootstrap()
    message = harness.message('control_event', {
        'event': 'renew_control', 'previous_context': harness.controller_context,
        'profile_use': {'ref': harness.profile, 'use_scope': harness.scope}})
    message['context'] = None
    message['message_id'] = delivery.message_id(message)
    source = tmp_path / 'renew.json'
    source.write_bytes(lc.canonical(message))
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path))
    assert fabric.main(['submit', harness.engagement, '--message', str(source)]) == 0
    response = json.loads(capsys.readouterr().out)
    assert response['status'] == 'committed'
    assert response['receipt']['message_id'] == message['message_id']
    assert response['receipt']['after_head'] == harness.store.read().head
    recorded = harness.path.read_bytes()
    assert fabric.main(['submit', harness.engagement, '--message', str(source)]) == 0
    assert json.loads(capsys.readouterr().out)['status'] == 'already_committed'
    assert harness.path.read_bytes() == recorded
    assert harness._human_signer is None


def test_cli_current_basis_is_local_read_and_grants_no_permission(tmp_path, monkeypatch, capsys):
    harness = GovernedHarness(tmp_path, monkeypatch)
    harness.bootstrap()
    query = {'protocol': delivery.PROTOCOL, 'subject': harness.input_a,
             'assessment_scope': harness.scope}
    source = tmp_path / 'query.json'
    source.write_bytes(lc.canonical(query))
    before = harness.path.read_bytes()
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path))
    assert fabric.main(['current-basis', harness.engagement, '--query', str(source)]) == 0
    response = json.loads(capsys.readouterr().out)
    assert response['subject'] == harness.input_a
    assert response['assessment_scope'] == harness.scope
    assert {'ref': harness.input_a, 'use_scope': harness.scope} in response['closure']
    assert not response['eligibility']['accepted'] and not response['eligibility']['release_eligible']
    assert harness.path.read_bytes() == before
    assert harness._human_signer is None


def test_cli_rejects_duplicate_human_proof_members_before_any_effect(tmp_path, monkeypatch, capsys):
    harness = GovernedHarness(tmp_path, monkeypatch)
    harness.bootstrap()
    _, subject, _ = harness.qualified_answer()
    basis = harness.store.evaluate(subject)
    message = harness.message('decision', {'action': 'accept', 'reason': 'Malformed human proof rejection.',
        'subject': subject, 'closure_hash': basis['closure_hash'], 'authority_proof': '0' * 64},
        sender={'kind': 'authority', 'id': 'human-owner'})
    source, proof = tmp_path / 'acceptance.json', tmp_path / 'ambiguous-human-proof.json'
    source.write_bytes(lc.canonical(message))
    proof.write_bytes(b'{"request":{},"receipt":{},"request":{"substituted":true}}')
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path))
    before = harness.path.read_bytes()
    assert fabric.main(['submit', harness.engagement, '--message', str(source),
                        '--authority-proof', str(proof)]) == 2
    capsys.readouterr()
    assert harness.path.read_bytes() == before
