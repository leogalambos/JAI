# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Check observed modality counts, soft budgets and located semantic repetition."""
from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
from content_metrics import analyze, main


def test_empty_content_does_not_invent_pages_or_word_floor():
    result = analyze({})
    assert result['counts']['words'] == 0
    assert result['counts']['pages'] is None
    assert result['budget_advice'] == []


def test_known_modalities_count_actual_entities():
    result = analyze({'slides': [{},{}], 'rows': [{},{},{}], 'nodes': [{}]})
    assert result['counts']['slides'] == 2
    assert result['counts']['rows'] == 3
    assert result['counts']['diagram_nodes'] == 1


def test_soft_budget_never_blocks_length():
    result = analyze({'text': 'one two three'}, {'blueprint': {'budgets': {'words': {'soft_max': 2, 'target': [5,10]}}}})
    assert result['budget_advice'][0]['action'] == 'revise/justify'
    assert not result['budget_advice'][0]['blocking']


def test_repeated_prose_and_structured_content_are_located():
    body = {'decision': 'Keep platform A', 'deadline': '2026-12-01'}
    result = analyze({'semantic_units': {'first': body}, 'repeated_content': [body, body]})
    assert any(len(item['locations']) == 3 for item in result['duplication'])
    text = 'Recovery tests must preserve the full ledger transaction history during transition.'
    result = analyze({'semantic_units': {'first': text, 'second': text}})
    assert result['duplication'][0]['locations'] == ['$.semantic_units.first', '$.semantic_units.second']


def test_nonfinite_numbers_fail_closed():
    with pytest.raises(ValueError):
        analyze({'amount': float('inf')})


def test_metrics_cli_handles_real_file_and_invalid_file(tmp_path, capsys):
    path=tmp_path/'model.json';path.write_text('{"text":"Recovery steps"}')
    assert main(['analyze',str(path)]) == 0
    assert 'words' in capsys.readouterr().out
    assert main(['analyze',str(tmp_path/'missing.json')]) == 1
