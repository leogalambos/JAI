# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Disposable deployment tooling refuses destinations outside its exact scratch tree."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile

import pytest

spec = importlib.util.spec_from_file_location('deployment_rehearsal',
    Path(__file__).with_name('p10_deployment_rehearsal.py'))
rehearsal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rehearsal)


def test_rehearsal_rejects_system_scratch_root_and_foreign_installation(tmp_path):
    """Neither the scratch root nor a real/foreign installation is an allowed target."""
    with pytest.raises(ValueError, match='disposable directory'):
        rehearsal.main(['--workspace', tempfile.gettempdir()])
    before = set(tmp_path.iterdir())
    with pytest.raises(ValueError, match='disposable installation'):
        rehearsal.main(['--workspace', str(tmp_path), '--installed-house', str(tmp_path / 'foreign')])
    assert set(tmp_path.iterdir()) == before


def test_prepared_presentation_keeps_exact_packet_despite_optional_duplicate_fields():
    """Decorative duplicates can vary; actual packet or prompt changes cannot."""
    initial = {'invocation_id': 'one', 'host_delivery': {'prompt_blob_id': 'prompt'},
               'members': [{'member_key': 'member', 'packet': {'task': 'Exact requirement.'},
                            'context': 'context', 'assignment': 'assignment'}]}
    restored = copy.deepcopy(initial)
    restored['members'][0].update(manifest_hash='duplicate', packet_blob_id='duplicate')
    assert rehearsal._prepared_view(initial) == rehearsal._prepared_view(restored)
    restored['members'][0]['packet']['task'] = 'Different requirement.'
    assert rehearsal._prepared_view(initial) != rehearsal._prepared_view(restored)
    restored = copy.deepcopy(initial)
    restored['host_delivery']['prompt_blob_id'] = 'different-prompt'
    assert rehearsal._prepared_view(initial) != rehearsal._prepared_view(restored)


def test_exit_zero_carrier_error_is_not_a_successful_rehearsal():
    """An acknowledged close is required and any failed frame remains fatal."""
    closed = {'id': 'deployment-close', 'ok': True, 'result': {'closed': True}}
    assert rehearsal._carrier_frames(json.dumps(closed)) == [closed]
    with pytest.raises(RuntimeError, match='failed protocol frame'):
        rehearsal._carrier_frames(json.dumps({'id': 'bad', 'ok': False, 'error': 'P_SCHEMA'}) + '\n' + json.dumps(closed))
    with pytest.raises(RuntimeError, match='acknowledge'):
        rehearsal._carrier_frames(json.dumps({'id': 'startup', 'ok': True, 'result': {}}))
