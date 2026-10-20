# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Conversational capture coordination against real temporary libraries."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def tool(path=None):
    spec = importlib.util.spec_from_file_location('knowledge_capture', path or ROOT / '.ai/runtime/tools/knowledge.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def proposal():
    return dict(schema_version=1, id='selected-lesson', record_type='experience', version=1,
        created='2026-10-20', updated='2026-10-20', language='en', confidentiality='internal',
        applicability=dict(contexts=['Assessment'], preconditions=[], exclusions=['No approval']),
        provenance=[], evidence_availability='NOT_CHECKED',
        review=dict(status='AI_EDITORIAL', reported_by='active provider', authority_claim='', authority_verification='NOT_VERIFIED'),
        limitations=['Only selected visible context; results not independently verified'], supersedes=None,
        observations=['The operator requested ownership checks'], interpretation=[], recommendations=[], scenario=None,
        reliability='user-reported', conversation_selection=dict(excerpt='Remember the ownership checks.',
        scope='user-selected-visible-context', completeness='partial'))


def test_missing_metadata_and_destination_ask_without_writing(tmp_path):
    value = proposal()
    del value['reliability']
    del value['confidentiality']
    result = tool().capture(value, library=tmp_path, save_requested=True)
    assert result['status'] == 'NEEDS_INPUT'
    assert {q['field'] for q in result['questions']} == {'reliability', 'confidentiality'}
    assert list(tmp_path.iterdir()) == []
    assert tool().capture(proposal(), save_requested=True)['status'] == 'NEEDS_INPUT'


def test_original_save_intent_completes_after_answers_without_review_claim(tmp_path):
    mod = tool()
    value = proposal()
    del value['reliability']
    assert mod.capture(value, library=tmp_path, save_requested=True)['status'] == 'NEEDS_INPUT'
    value['reliability'] = 'user-reported'
    result = mod.capture(value, library=tmp_path, save_requested=True)
    assert result['status'] == 'SAVED_NOT_APPROVAL'
    record = json.loads(Path(result['destination']).read_text())
    assert record['owner'] == 'operator'
    assert record['review']['status'] == 'AI_EDITORIAL'
    assert result['preview']['record'] == record
    with pytest.raises(ValueError, match='exists'):
        mod.capture(value, library=tmp_path, save_requested=True)


def test_prepare_only_and_no_intent_are_distinct(tmp_path):
    mod = tool()
    assert mod.capture(proposal(), library=tmp_path)['status'] == 'READY_NOT_SAVED'
    assert list(tmp_path.iterdir()) == []
    result = mod.capture(proposal(), library=tmp_path, prepare_requested=True)
    assert result['status'] == 'PREPARED_NOT_SAVED'
    assert not (tmp_path / 'records').exists()


@pytest.mark.parametrize('field,value', [('reliability','guaranteed'), ('provenance',[{'path':'history.json'}]),
    ('review',dict(status='HUMAN_REVIEW_REPORTED',reported_by='operator',authority_claim='',authority_verification='NOT_VERIFIED'))])
def test_invalid_claims_are_rejected_before_writes(tmp_path, field, value):
    item = proposal()
    item[field] = value
    with pytest.raises(ValueError):
        tool().capture(item, library=tmp_path, save_requested=True)
    assert list(tmp_path.iterdir()) == []


def test_symlink_library_is_rejected(tmp_path):
    actual = tmp_path / 'actual'
    actual.mkdir()
    link = tmp_path / 'link'
    link.symlink_to(actual, target_is_directory=True)
    with pytest.raises(OSError):
        tool().capture(proposal(), library=link, save_requested=True)
    assert list(actual.iterdir()) == []


def test_cli_capture_reads_internal_payload_from_stdin(tmp_path, monkeypatch, capsys):
    import io
    mod = tool()
    monkeypatch.setattr('sys.stdin', io.TextIOWrapper(io.BytesIO(json.dumps(proposal()).encode())))
    assert mod.main(['capture', '--library', str(tmp_path), '--save-requested']) == 0
    result = json.loads(capsys.readouterr().out)
    assert result['status'] == 'SAVED_NOT_APPROVAL'
    assert Path(result['destination']).is_file()


def test_installed_runtime_capture_has_no_documentation_dependency(tmp_path):
    import shutil
    installed = tmp_path / 'installed'
    (installed / 'tools').mkdir(parents=True)
    shutil.copytree(ROOT / '.ai/runtime/knowledge', installed / 'knowledge')
    shutil.copyfile(ROOT / '.ai/runtime/tools/knowledge.py', installed / 'tools/knowledge.py')
    library = tmp_path / 'library'
    library.mkdir()
    result = tool(installed / 'tools/knowledge.py').capture(proposal(), library=library, save_requested=True)
    assert result['status'] == 'SAVED_NOT_APPROVAL'
    assert not (installed / 'docs').exists()
    assert json.loads(Path(result['destination']).read_text())['conversation_selection']['completeness'] == 'partial'


def test_capture_rejects_invalid_excerpts_and_protected_targets_before_writes(tmp_path):
    mod = tool()
    value = proposal()
    value['conversation_selection']['scope'] = 'complete-history'
    with pytest.raises(ValueError):
        mod.capture(value, library=tmp_path, save_requested=True)
    assert list(tmp_path.iterdir()) == []
    with pytest.raises(ValueError):
        mod.capture(proposal(), library=tmp_path / '.fabric', save_requested=True)
    assert list(tmp_path.iterdir()) == []


def test_prepared_selection_can_later_be_saved_without_replacing_candidate(tmp_path):
    mod = tool()
    prepared = mod.capture(proposal(), library=tmp_path, prepare_requested=True)
    candidates = list((tmp_path / 'drafts').iterdir())
    original = candidates[0].read_bytes()
    saved = mod.capture(proposal(), library=tmp_path, save_requested=True)
    assert saved['status'] == 'SAVED_NOT_APPROVAL'
    assert saved['digest'] == prepared['digest']
    assert candidates[0].read_bytes() == original


def test_unclear_owner_is_asked_then_original_intent_saves_answer(tmp_path):
    mod = tool()
    value = proposal()
    value['owner'] = None
    result = mod.capture(value, library=tmp_path, save_requested=True)
    assert result['status'] == 'NEEDS_INPUT'
    assert result['questions'][0]['field'] == 'owner'
    assert list(tmp_path.iterdir()) == []
    value['owner'] = 'Assessment owner'
    saved = mod.capture(value, library=tmp_path, save_requested=True)
    assert saved['preview']['record']['owner'] == 'Assessment owner'
