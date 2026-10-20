# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Public persistence admission preserves bounded reader usability at capacity."""
import json
from pathlib import Path

import pytest

from test_knowledge_retrieval import seed, knowledge, hint, options
from test_knowledge_capture import proposal


def candidate(identity='lesson', version=1):
    value = proposal()
    value.update(id=identity, version=version, supersedes=None if version == 1 else version - 1)
    return value


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}


def test_128th_version_saves_and_129th_rejects_before_any_write(tmp_path):
    for version in range(1, 128):
        seed(tmp_path, version=version)
    knowledge.capture(candidate(version=128), library=tmp_path, save_requested=True)
    assert len(knowledge.read_records(tmp_path, read_requested=True)) == 128
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.capture(candidate(version=129), library=tmp_path, save_requested=True)
    assert snapshot(tmp_path) == before
    assert knowledge.describe(tmp_path, 'lesson', 128, read_requested=True,
        confidentiality=['internal'], contexts=['Assessment'])['record']['version'] == 128
    assert hint.select_candidates(['ownership checks'], **options(tmp_path))['knowledge']
    assert knowledge.delete_record(tmp_path, 'lesson', delete_requested=True)['status'] == 'WITHDRAWN_RECOVERABLE'


def test_256th_identity_saves_and_257th_rejects_without_candidate(tmp_path):
    for number in range(255):
        seed(tmp_path, identity=f'lesson-{number}')
    knowledge.capture(candidate('last-lesson'), library=tmp_path, save_requested=True)
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.capture(candidate('overflow-lesson'), library=tmp_path, save_requested=True)
    assert snapshot(tmp_path) == before
    assert len(knowledge.read_records(tmp_path, read_requested=True)) == 256


def test_1024th_version_saves_and_next_rejects_without_disabling_read(tmp_path):
    for number in range(8):
        for version in range(1, 129 if number < 7 else 128):
            seed(tmp_path, identity=f'lesson-{number}', version=version)
    knowledge.capture(candidate('lesson-7', 128), library=tmp_path, save_requested=True)
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.capture(candidate('new-lesson'), library=tmp_path, save_requested=True)
    assert snapshot(tmp_path) == before
    assert len(knowledge.read_records(tmp_path, read_requested=True)) == 1024


def test_save_rechecks_capacity_after_candidate_was_prepared(tmp_path):
    prepared = knowledge.capture(candidate('pending-lesson'), library=tmp_path, prepare_requested=True)
    for number in range(256):
        seed(tmp_path, identity=f'lesson-{number}')
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.save(tmp_path, 'pending-lesson', 1, prepared['digest'], prepared['digest'],
                       source_root=tmp_path, save_requested=True)
    assert snapshot(tmp_path) == before
    assert len(knowledge.read_records(tmp_path, read_requested=True)) == 256


@pytest.mark.parametrize('suffix', ['123 project', '.extra project', '/other project', '_other'])
def test_commands_need_whitespace_or_end_after_complete_supported_token(tmp_path, suffix):
    value = candidate()
    value.update(record_type='custom-scenario', scenario=dict(inputs=['Architecture'], steps=[dict(
        purpose='Review', claude='/review' + suffix, codex='$workflow-review' + suffix, inspect='Findings')]))
    with pytest.raises(ValueError, match='commands'):
        knowledge.capture(value, library=tmp_path, save_requested=True)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('arguments', ['', ' project', '\tproject'])
def test_supported_commands_accept_end_or_whitespace_delimiter(tmp_path, arguments):
    value = candidate()
    value.update(record_type='custom-scenario', scenario=dict(inputs=['Architecture'], steps=[dict(
        purpose='Review', claude='/review' + arguments, codex='$workflow-review' + arguments, inspect='Findings')]))
    assert knowledge.capture(value, library=tmp_path, save_requested=True)['status'] == 'SAVED_NOT_APPROVAL'


def padded_record(identity, target_bytes):
    value = candidate(identity)
    value['owner'] = 'operator'
    value['observations'] = []
    remaining = target_bytes - len(knowledge._canonical(value))
    while remaining:
        # Each new ASCII string contributes its characters and JSON quotes/comma.
        overhead = 2 if not value['observations'] else 3
        count = min(4000, remaining - overhead)
        if count <= 0:
            value['observations'][-1] += 'x' * remaining
            break
        value['observations'].append('x' * count)
        remaining -= count + overhead
    assert len(knowledge._canonical(value)) == target_bytes
    return value


def test_exact_8mib_content_saves_and_one_byte_over_rejects_without_writes(tmp_path):
    capacity = 8 * 1024 * 1024
    record_bytes = 125000
    count = capacity // record_bytes
    for number in range(count):
        value = padded_record(f'large-{number}', record_bytes)
        seed(tmp_path, identity=value.pop('id'), **{k:v for k,v in value.items() if k != 'version'})
    final = padded_record('last-lesson', capacity - count * record_bytes)
    import copy
    over = copy.deepcopy(final)
    over['observations'][-1] += 'x'
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.capture(over, library=tmp_path, save_requested=True)
    assert snapshot(tmp_path) == before
    knowledge.capture(final, library=tmp_path, save_requested=True)
    existing = knowledge.read_records(tmp_path, read_requested=True)
    assert sum(len(knowledge._canonical(r)) for r in existing) == capacity
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.capture(candidate('overflow-lesson'), library=tmp_path, save_requested=True)
    assert snapshot(tmp_path) == before
    assert sum(len(knowledge._canonical(r)) for r in knowledge.read_records(tmp_path, read_requested=True)) == capacity


def test_concurrent_last_slot_admission_has_one_success_and_no_rejected_candidate(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    for number in range(255):
        seed(tmp_path, identity=f'lesson-{number}')
    def attempt(identity):
        try:
            return knowledge.capture(candidate(identity), library=tmp_path, save_requested=True)['status']
        except ValueError as error:
            assert 'capacity' in str(error)
            return 'REJECTED'
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(attempt, ['first-lesson', 'second-lesson']))
    assert sorted(results) == ['REJECTED', 'SAVED_NOT_APPROVAL']
    assert len(knowledge.read_records(tmp_path, read_requested=True)) == 256
    assert len(list((tmp_path / 'drafts').glob('*.json'))) == 1


def test_restore_rechecks_library_capacity_without_moving_history(tmp_path):
    seed(tmp_path, identity='withdrawn-lesson')
    withdrawn = knowledge.delete_record(tmp_path, 'withdrawn-lesson', delete_requested=True)
    for number in range(256):
        seed(tmp_path, identity=f'lesson-{number}')
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match='capacity'):
        knowledge.restore_record(tmp_path, 'withdrawn-lesson', withdrawn['trash_id'], restore_requested=True)
    assert snapshot(tmp_path) == before
    assert Path(withdrawn['recovery_path']).is_dir()
    assert len(knowledge.read_records(tmp_path, read_requested=True)) == 256
