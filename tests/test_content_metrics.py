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


def corpus_samples():
    import json
    from content_eval import prepare_case
    from content_lint import evaluate
    from content_spec import ContentSpec
    root=Path(__file__).resolve().parents[1]
    engine=ContentSpec(root)
    result=[]
    for complexity in ('simple','medium','complex'):
        case=json.loads((root/f'.ai/runtime/evals/content_quality/decision-paper-{complexity}.json').read_text())
        model,spec=prepare_case(case,engine)
        result.append({'project_id':complexity,'complexity':complexity,'synthetic':True,
            'semantic_model':model,'content_qa':evaluate(model,spec)})
    return result


def test_calibration_candidate_uses_three_actual_projects_and_explicit_context_strata():
    from content_metrics import calibrate
    samples=corpus_samples()
    result=calibrate(samples)
    assert len(result['samples'])==3
    assert len(result['context_strata'])==3
    assert result['size_budget']['target']==[min(s['observed'] for s in result['samples']),max(s['observed'] for s in result['samples'])]
    assert not result['size_budget']['minimum_is_quality_gate']
    assert result['calibration_status']=='synthetic-only'
    assert not result['production_ready']


def test_calibration_rejects_duplicate_projects_unmeasured_pages_and_tampered_qa():
    from content_metrics import calibrate
    samples=corpus_samples()
    with pytest.raises(ValueError,match='THREE_PROJECTS'):
        calibrate(samples[:2])
    samples[1]['project_id']=samples[0]['project_id']
    with pytest.raises(ValueError,match='DISTINCT_PROJECTS'):
        calibrate(samples)
    samples[1]['project_id']='second'
    with pytest.raises(ValueError,match='METRIC_UNMEASURED'):
        calibrate(samples,metric='pages')
    samples[0]['content_qa']['gate_verdict']='CONTENT_PASS'
    with pytest.raises(ValueError,match='QA_REPLAY'):
        calibrate(samples)


def test_comparable_trends_replay_exact_reports_and_reject_forged_observations():
    import copy
    from content_metrics import trends
    from content_lint import evaluate
    from content_spec import ContentSpec
    sample=corpus_samples()[0]
    model=sample['semantic_model'];second=copy.deepcopy(model)
    second['artifact_id']='revised:01'
    spec=ContentSpec().resolve(second['contract_id'],second['context'])
    a={'observed_at':'2026-10-18T10:00:00Z','semantic_model':model,'content_qa':sample['content_qa']}
    b={'observed_at':'2026-10-19T10:00:00Z','semantic_model':second,'content_qa':evaluate(second,spec)}
    result=trends([a,b])
    assert result['delta']['words']==0
    assert not result['qualification_evidence']
    assert result['observations'][0]['gate_verdict']=='DRAFT_INCOMPLETE'
    with pytest.raises(ValueError,match='DUPLICATE_SNAPSHOT'):
        trends([a,{**a,'observed_at':b['observed_at']}])
    with pytest.raises(ValueError,match='TIMEPOINT_INVALID'):
        trends([b,a])
    with pytest.raises(ValueError,match='TIMEPOINT_INVALID'):
        trends([a,{**b,'observed_at':'2026-10-19T11:00:00'}])
    b['content_qa']['report_hash']='0'*64
    with pytest.raises(ValueError,match='QA_REPLAY_FAILED'):
        trends([a,b])


def test_trends_reject_context_changes_and_calibration_cannot_self_declare_gold():
    from content_metrics import trends,calibrate
    samples=corpus_samples()
    with pytest.raises(ValueError,match='NONCOMPARABLE'):
        trends([{'observed_at':f'2026-10-{18+i}T10:00:00Z',**s} for i,s in enumerate(samples[:2])])
    for s in samples:s['synthetic']=False
    result=calibrate(samples)
    assert result['calibration_status']=='unapproved-enterprise'
    assert result['human_approval_required']
    assert not result['production_ready']


def test_structured_size_metrics_count_real_elements_and_configuration_checks():
    result=analyze({'elements':[{'id':'one'},{'id':'two'}],'checks':[{'id':'check-one'}]})
    assert result['counts']['elements']==2
    assert result['counts']['configuration_checks']==1
    assert analyze({})['counts']['elements'] is None
    assert analyze({'checks':6})['counts']['configuration_checks'] is None


@pytest.mark.parametrize('count,exceeds',[(2,False),(3,False),(4,True)])
def test_genuine_hard_upper_constraint_boundary(count,exceeds):
    budget={'hard_max':3,'hard_limit_basis':{'kind':'contractual','source_ref':'contract:slide-limit',
        'reason':'The receiving board accepts at most three slides.'}}
    result=analyze({'slides':[{} for _ in range(count)]},{'blueprint':{'budgets':{'slides':budget}}})
    assert bool(result['budget_advice']) is exceeds
    if exceeds:
        assert result['budget_advice'][0]['rule_id']=='HARD_SIZE_CONSTRAINT'
        assert result['budget_advice'][0]['category']=='critical-content'
        assert not result['budget_advice'][0]['blocking']


def test_unknown_pages_and_unjustified_hard_quotas_remain_pending_not_invented():
    basis={'kind':'publication-constraint','source_ref':'brief:one-page','reason':'Single physical briefing page.'}
    result=analyze({'text':'A concise actual decision.'},{'blueprint':{'budgets':{'pages':{'max_limit':1,'hard_limit_basis':basis}}}})
    assert result['counts']['pages'] is None
    assert result['budget_advice'][0]['rule_id']=='SIZE_CONSTRAINT_UNMEASURED'
    result=analyze({'text':'A concise actual decision.'},{'blueprint':{'budgets':{'words':{'hard_max':1}}}})
    assert result['budget_advice'][0]['rule_id']=='SIZE_CONSTRAINT_BASIS_REQUIRED'
