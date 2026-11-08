# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Read-only SABSA pair diagnostics and immutable professional review prerequisites."""
import copy
import json
import subprocess
import sys

import pytest

from governed_fixtures import ROOT
import lifecycle as lc
import model_router
import professional_review as review


def _pair(model, effort='medium', provider='codex'):
    return {'provider': provider, 'model_selector': model, 'reasoning_effort': effort}


def _cli(project, provider='codex', author='same-model', reviewer='same-model', extra=()):
    return subprocess.run([sys.executable, str(ROOT / '.ai/runtime/tools/professional_review.py'),
        '--project', str(project), '--author-provider', provider, '--author-model', author,
        '--author-effort', 'medium', '--reviewer-provider', provider, '--reviewer-model', reviewer,
        '--reviewer-effort', 'high', *extra], capture_output=True, text=True)


@pytest.mark.parametrize('provider', ['codex', 'claude'])
def test_actual_cli_reports_same_model_effort_change_blocked_and_distinct_passed(tmp_path, provider):
    blocked = _cli(tmp_path, provider)
    assert blocked.returncode == 2
    report = json.loads(blocked.stdout)
    assert report['status'] == 'blocked'
    assert report['served_model'] is None
    assert 'different effort' in report['help'].lower()
    assert 'pending reviewer' in report['help']
    assert 'native model' in report['help'] and 'shared pair check before dispatch' in report['help']
    assert 'select_execution' not in report['help'] and 'current previous' not in report['help']
    assert 'registry-declared only' in report['help'] and 'not observed' in report['help']
    assert 'Preserve the task and context' in report['help']
    for invented_state in ('pinned run', 'journal', 'bootstrap', 'governing owner'):
        assert invented_state not in report['help']
    passed = _cli(tmp_path, provider, author='actual-author', reviewer='actual-reviewer')
    assert passed.returncode == 0
    assert json.loads(passed.stdout)['status'] == 'passed'
    assert not (tmp_path / '.jai').exists()


@pytest.mark.parametrize('unknown', ['inherit', 'inherit-session', 'default', 'unknown', 'auto', 'unspecified', ''])
def test_unknown_author_or_reviewer_identity_cannot_prove_diversity(unknown):
    for author, reviewer in [(_pair(unknown), _pair('distinct')), (_pair('distinct'), _pair(unknown))]:
        result = review.check_pair(author, reviewer, [_pair('other')])
        assert result['status'] == 'blocked'
        assert result['served_model'] is None
    assert review.check_pair(_pair(unknown), _pair('distinct'), [_pair('other')])['alternatives'] == []


def test_pair_comparison_uses_provider_and_selector_not_effort_or_class():
    assert review.check_pair(_pair('same', 'medium'), _pair('same', 'high'), [])['status'] == 'blocked'
    assert review.check_pair(_pair('same'), _pair('same', provider='claude'), [])['status'] == 'passed'
    result = review.check_pair(_pair('same'), _pair('same'), [], assignment={'version_id': 'pending'})
    assert 'No compatible captured alternative' in result['help']
    assert 'deployment administrator' in result['help']
    assert 'governing owner' in result['help'] and 'no in-place registry replacement API' in result['help']
    assert 'pending' in result['help']


def test_cli_alternatives_apply_captured_role_preferences_before_excluding_same_model(tmp_path):
    models = model_router.load(model_router.BASE)
    for entry in models['providers']['claude']['classes'].values():
        entry['model_selector'] = 'same-model'
    models['providers']['claude']['classes']['standard']['model_selector'] = 'raw-unused-standard'
    registry_path = tmp_path / 'models.json'
    registry_path.write_text(json.dumps(models))
    (tmp_path / '.jai').mkdir()
    (tmp_path / '.jai' / 'config.json').write_text(json.dumps({'schema_version': 1,
        'execution_profile': 'standard', 'overrides': {'providers': {'claude': {'reviewer': {
            'model_selector': 'same-model', 'reasoning_effort': 'high'}}}}}))
    blocked = _cli(tmp_path, 'claude', extra=('--model-config', str(registry_path)))
    assert blocked.returncode == 2
    report = json.loads(blocked.stdout)
    assert report['alternatives'] == []
    assert 'raw-unused-standard' not in report['help']
    assert 'No compatible registry-declared alternative' in report['help']
    assert 'register a distinct model' in report['help']
    assert 'shared pair check before dispatch' in report['help']
    assert 'governing owner' not in report['help'] and 'journal' not in report['help']


def test_constraints_metadata_is_closed_and_legacy_absence_preserves_retained_rule():
    assert review.constraints_problems(None)
    assert review.constraints_problems([]) == []
    assert review.constraints_problems([copy.deepcopy(review._RETAINED)]) == []
    for change in ({'kind': 'same-model'}, {'extra': True}, {'author_categories': 4},
                   {'source_contract': 'arbitrary'}, {'author_categories': [], 'author_operators': []}):
        rule = {**copy.deepcopy(review._RETAINED), **change}
        assert review.constraints_problems([rule])
    assert review.constraints_problems('not-a-list')
    assert review.constraints_problems([review._RETAINED, review._RETAINED])
    snapshot = {'models': {'professional_review_constraints': []}}
    assert review._RETAINED in review._rules(snapshot)


class _State:
    """Owned in-memory state collaborator with immutable record lookups."""

    def __init__(self, snapshot, author_choice):
        self.policy = {'version_id': 'policy'}
        source = {'material': ['captured-asset']}
        self._routing_snapshots = {(lc.canonical(self.policy), ('captured-asset',)): snapshot}
        self.provenance = {'candidate': {'context': {'version_id': 'author-context'}}}
        self.records = {'policy': source,
            'author-assignment': {'responsibility': 'author', 'routing': {'policy': self.policy}},
            'candidate': {'assignment': {'version_id': 'author-assignment'}},
            'author-context': {'assignment': {'version_id': 'author-assignment'},
                'execution': {'phase': 'work', 'selection': {'version_id': 'author-selection'}}},
            'author-selection': {'message': {'payload': author_choice}}}

    def resolve(self, reference, kind=None):
        return self.records[reference['version_id']]

    def _validation_bytes(self, identifier, live):
        raise AssertionError('Captured snapshot must be reused rather than reloaded')


def _state_and_review(sabsa=True, same_model=False):
    models = model_router.load(model_router.BASE)
    models.pop('execution_profile', None)
    models['professional_review_constraints'] = []
    models['providers']['codex']['classes']['standard'].update(model_selector='author-model', reasoning_effort='medium')
    models['providers']['codex']['classes']['heavy'].update(model_selector='reviewer-model', reasoning_effort='high')
    snapshot = {'models': models, 'descriptor': {'catalogue_blob_id': 'catalogue'},
        'catalogue': {'roles': [{'slug': 'specialty', 'category': 'SABSA Security Architecture' if sabsa else 'Software',
                                'operator_agent': 'role-author'}]}}
    author_choice = {'assignment': {'version_id': 'author-assignment'}, 'specialties': ['specialty'],
                     'provider': 'codex', 'workload_class': 'standard', 'model_selector': 'author-model'}
    state = _State(snapshot, author_choice)
    assignment = {'responsibility': 'reviewer', 'routing': {'policy': state.policy},
                  'inputs': [{'slot_id': 'assessed-subject', 'refs': [{'version_id': 'candidate'}]}]}
    choice = {'assignment': {'version_id': 'pending-reviewer'}, 'specialties': ['specialty'], 'provider': 'codex',
              'workload_class': 'standard' if same_model else 'heavy',
              'model_selector': 'author-model' if same_model else 'reviewer-model'}
    return state, assignment, snapshot, choice


def test_enforce_uses_immutable_author_context_and_caches_valid_pair_not_acceptance():
    state, assignment, snapshot, choice = _state_and_review()
    state.execution_plans = {'not-the-author-context': 'mutable-irrelevant-plan'}
    report = review.enforce(state, assignment, snapshot, choice)
    assert report['status'] == 'passed'
    assert report['author']['model_selector'] == 'author-model'
    assert report['reviewer']['model_selector'] == 'reviewer-model'
    # Changing mutable model maps cannot affect an already checked immutable
    # candidate/selection/policy identity in this owned collaborator.
    snapshot['models']['providers']['codex']['classes'].clear()
    assert review.enforce(state, assignment, snapshot, choice) == report
    assert len(state._professional_review_checks) == 1


def test_retained_rule_blocks_live_same_model_but_never_rewrites_accepted_prefix():
    state, assignment, snapshot, choice = _state_and_review(same_model=True)
    with pytest.raises(ValueError, match='[Dd]ifferent effort'):
        review.enforce(state, assignment, snapshot, choice)
    assert review.enforce(state, assignment, snapshot, choice, live=False) is None
    assert not state._professional_review_checks
    generic, assignment, snapshot, choice = _state_and_review(sabsa=False, same_model=True)
    assert review.enforce(generic, assignment, snapshot, choice) is None


def test_missing_exact_author_origin_blocks_known_sabsa_but_not_unrelated_generic_review():
    state, assignment, snapshot, choice = _state_and_review()
    state.provenance.clear()
    with pytest.raises(ValueError, match='immutable author context/selection'):
        review.enforce(state, assignment, snapshot, choice)
    generic, assignment, snapshot, choice = _state_and_review(sabsa=False)
    generic.provenance.clear()
    assert review.enforce(generic, assignment, snapshot, choice) is None


@pytest.mark.parametrize('marker', ['semantic', 'profile', 'adopted-profile'])
def test_authoritative_sabsa_subject_marker_cannot_be_evaded_with_generic_specialty(marker):
    state, assignment, snapshot, choice = _state_and_review(sabsa=False, same_model=True)
    if marker == 'semantic':
        state._product_content = {'candidate': {'format': 'jai-sabsa-content/1'}}
    else:
        state.records['candidate']['profile'] = {'version_id': 'profile'}
        selector = {'version_id': 'content-policy'} if marker == 'profile' else {'logical_id': 'policy', 'use_scope': 'default'}
        state.records['profile'] = {'content_profile': selector}
        state._content_policies = {'content-policy': {'format': 'jai-sabsa-content-profile/1'}}
        state.content_policy = lambda reference: {'ref': {'version_id': 'content-policy'}}
    with pytest.raises(ValueError, match='[Dd]ifferent effort'):
        review.enforce(state, assignment, snapshot, choice)
    state.provenance.clear()
    with pytest.raises(ValueError, match='immutable author context/selection'):
        review.enforce(state, assignment, snapshot, choice)


def test_arbitrary_subject_names_or_untyped_prose_do_not_create_sabsa_scope():
    state, assignment, snapshot, choice = _state_and_review(sabsa=False, same_model=True)
    state.records['candidate']['name'] = 'SABSA-labelled generic document'
    state._product_content = {'candidate': {'text': 'jai-sabsa-content/1', 'format': 'other-format'}}
    assert review.enforce(state, assignment, snapshot, choice) is None


def test_known_sabsa_reviewer_without_exact_subject_is_blocked_before_work():
    state, assignment, snapshot, choice = _state_and_review()
    assignment['inputs'] = []
    with pytest.raises(ValueError, match='exactly one canonical'):
        review.enforce(state, assignment, snapshot, choice)


def test_adopted_sabsa_domain_without_subject_cannot_be_hidden_with_generic_profession():
    state, assignment, snapshot, choice = _state_and_review(sabsa=False)
    assignment['inputs'] = []
    assignment['profile'] = {'version_id': 'profile'}
    state.records['profile'] = {'content_profile': {'version_id': 'content-policy'}}
    state._content_policies = {'content-policy': {'format': 'jai-sabsa-content-profile/1'}}
    with pytest.raises(ValueError, match='same pending reviewer assignment'):
        review.enforce(state, assignment, snapshot, choice)


def test_ambiguous_sabsa_subjects_are_not_guessed_even_with_explicit_assessment_subject():
    state, assignment, snapshot, choice = _state_and_review()
    assignment['inputs'][0]['refs'].append({'version_id': 'another-candidate'})
    with pytest.raises(ValueError, match='missing or ambiguous'):
        review.enforce(state, assignment, snapshot, choice, subject={'version_id': 'candidate'})


def test_generic_missing_domain_and_genuine_human_review_preserve_existing_route():
    state, assignment, snapshot, choice = _state_and_review(sabsa=False)
    assignment['inputs'] = []
    assert review.enforce(state, assignment, snapshot, choice) is None
    state, assignment, snapshot, choice = _state_and_review()
    state.records['candidate'] = {'owner': {'kind': 'authority', 'id': 'human'}}
    assert review.enforce(state, assignment, snapshot, choice) is None
    result = review.check_pair(_pair('same'), _pair('same'), [_pair('other')])
    assert 'Ask JAI to reselect this same pending reviewer' in result['help']


def test_governed_pair_help_preserves_exact_pending_assignment_reselection_route():
    result = review.check_pair(_pair('same'), _pair('same', 'high'),
                             [{**_pair('other'), 'workload_class': 'heavy'}],
                             assignment={'version_id': 'actual-pending-review'})
    assert result['status'] == 'blocked'
    for guidance in ('same pending reviewer assignment', 'actual-pending-review', 'select_execution',
                     'current previous selection', 'pinned run', 'do not reset its journal'):
        assert guidance in result['help']
    assert 'rerun this shared pair check before dispatch' not in result['help']


def _process_author(kind=None, backend=None):
    state, assignment, snapshot, choice = _state_and_review()
    classes = {}
    for workload in snapshot['models']['workload_classes']:
        classes[workload] = {'model_selector': 'process-resource-label',
            'execution': {'provider': 'json-process/1', 'argv': ['/usr/bin/true'], 'files': []}}
        if kind is not None:
            classes[workload]['model_kind'] = kind
        if backend is not None:
            classes[workload].update(model_provider='codex', model_identity=backend)
    snapshot['models']['providers']['json-process/1'] = {'strategy_scope': 'project-internal', 'classes': classes}
    author = state.records['author-selection']['message']['payload']
    author.update(provider='json-process/1', model_selector='process-resource-label')
    return state, assignment, snapshot, choice


@pytest.mark.parametrize('review_provider', ['codex', 'json-process/1'])
def test_declared_deterministic_process_author_has_no_ai_model_pair_to_diversify(review_provider):
    state, assignment, snapshot, choice = _process_author('deterministic')
    if review_provider == 'json-process/1':
        choice.update(provider='json-process/1', model_selector='process-resource-label', workload_class='standard')
    assert review.enforce(state, assignment, snapshot, choice) is None
    assert len(state._professional_review_checks) == 1
    assert review.enforce(state, assignment, snapshot, choice) is None


def test_declared_wrapped_ai_compares_backend_identity_not_process_resource_label():
    state, assignment, snapshot, choice = _process_author('ai', 'reviewer-model')
    with pytest.raises(ValueError, match='different effort') as blocked:
        review.enforce(state, assignment, snapshot, choice)
    assert 'author codex/reviewer-model' in str(blocked.value)
    assert 'process-resource-label' not in str(blocked.value)
    state, assignment, snapshot, choice = _process_author('ai', 'distinct-backend')
    result = review.enforce(state, assignment, snapshot, choice)
    assert result['status'] == 'passed'
    assert result['author']['provider'] == 'codex'
    assert result['author']['model_selector'] == 'distinct-backend'
    assert result['served_model'] is None


def test_undeclared_process_is_unknown_not_assumed_non_ai_execution():
    state, assignment, snapshot, choice = _process_author()
    with pytest.raises(ValueError, match='declare model_kind') as blocked:
        review.enforce(state, assignment, snapshot, choice)
    assert 'same pending reviewer assignment' in str(blocked.value)
    assert 'pinned policy cannot be edited in place' in str(blocked.value)
    assert review.enforce(state, assignment, snapshot, choice, live=False) is None


def test_pure_pair_does_not_accept_nominal_process_resource_as_ai_model():
    result = review.check_pair(_pair('resource', provider='json-process/1'), _pair('native'), [_pair('another')])
    assert result['status'] == 'blocked'
    assert result['alternatives'] == []
    # Even malformed native relabeling cannot make the pair checker assume that
    # a positively native model is a deterministic tool.
    assert review._model_pair({'model_selector': 'native', 'model_kind': 'deterministic'}, 'codex') == _pair('native', None)


def test_substantive_sabsa_help_lists_declared_standard_before_light(tmp_path):
    response = _cli(tmp_path)
    assert response.returncode == 2
    report = json.loads(response.stdout)
    assert [item['workload_class'] for item in report['alternatives']] == ['standard', 'heavy', 'research', 'light']
    assert report['help'].index('standard:') < report['help'].index('light:')
    assert 'registry-declared only' in report['help']


def test_deterministic_tool_cannot_substitute_professional_review_of_sabsa_ai_author():
    state, assignment, snapshot, choice = _process_author('deterministic')
    # Restore native AI author and select the captured deterministic process as reviewer.
    state.records['author-selection']['message']['payload'].update(provider='codex', model_selector='author-model')
    choice.update(provider='json-process/1', model_selector='process-resource-label', workload_class='standard')
    with pytest.raises(ValueError, match='different AI reviewer model') as blocked:
        review.enforce(state, assignment, snapshot, choice)
    assert 'structural measurements' in str(blocked.value)
    assert 'same pending reviewer assignment' in str(blocked.value)
    # The professional constraint is domain-scoped; a generic formal tool check
    # keeps its existing route rather than acquiring a fabricated AI model pair.
    snapshot['catalogue']['roles'][0]['category'] = 'Software'
    state._professional_review_catalogues.clear()
    assert review.enforce(state, assignment, snapshot, choice) is None


def test_wrapped_ai_alternative_retains_an_executable_captured_process_route():
    state, assignment, snapshot, choice = _process_author('ai', 'author-backend')
    classes = snapshot['models']['providers']['json-process/1']['classes']
    classes['heavy'].update(model_selector='review-wrapper', model_identity='custom-review-backend')
    alternatives = review._alternatives(snapshot, 'json-process/1', 'reviewer')
    report = review.check_pair(_pair('author-backend'), _pair('author-backend'), alternatives,
                             assignment={'version_id': 'pending-reviewer'})
    assert report['status'] == 'blocked'
    suggestion = next(item for item in report['alternatives'] if item['workload_class'] == 'heavy')
    assert suggestion['provider'] == 'codex'
    assert suggestion['model_selector'] == 'custom-review-backend'
    assert suggestion['routing_provider'] == 'json-process/1'
    assert suggestion['routing_model_selector'] == 'review-wrapper'
    assert 'route provider=json-process/1, model_selector=review-wrapper' in report['help']
    assert 'backend codex/custom-review-backend' in report['help']
    # Use the actual advertised routing tuple at the production capture boundary;
    # copying backend identity into the process-resource selector would not resolve.
    corrected_choice = {'provider': suggestion['routing_provider'],
                        'workload_class': suggestion['workload_class'],
                        'model_selector': suggestion['routing_model_selector']}
    selector, selected = review.routing._execution(snapshot['models'], corrected_choice, 'reviewer')
    assert selector == 'review-wrapper'
    assert selected['execution']['provider'] == 'json-process/1'
    assert review.check_pair(_pair('author-backend'), review._model_pair(selected, corrected_choice['provider']), [])['status'] == 'passed'
    with pytest.raises(ValueError, match='Exact captured model choice'):
        review.routing._execution(snapshot['models'], {'provider': suggestion['provider'],
            'workload_class': suggestion['workload_class'], 'model_selector': suggestion['model_selector']}, 'reviewer')


def test_unknown_executed_author_requires_authentic_control_recovery_or_new_candidate():
    result = review.check_pair(_pair('inherit'), _pair('explicit-reviewer'), [_pair('alternative')],
                              assignment={'version_id': 'pending-reviewer'})
    assert result['status'] == 'blocked' and result['alternatives'] == []
    for guidance in ('reviewer-only reselection cannot', 'do not backfill or edit its capture',
                     'actual recorded author execution', 'governing owner', 'reissue/rework the author',
                     'new candidate', 'retain the old journal and budgets', 'served identity'):
        assert guidance in result['help']
    assert 'submit actual select_execution' not in result['help']


def test_ordinary_unknown_author_help_distinguishes_planned_call_from_existing_candidate():
    result = review.check_pair(_pair('unknown'), _pair('reviewer'), [_pair('another')])
    for guidance in ('before the author call', 'If a candidate already exists', 'authentic original controls',
                     'rework the author', 'new candidate', 'do not guess', 'served backend identity remains unobserved'):
        assert guidance in result['help']
    for invented_state in ('journal', 'select_execution', 'governing owner', 'bootstrap'):
        assert invented_state not in result['help']


def test_unknown_reviewer_can_be_reselected_without_reworking_known_author():
    result = review.check_pair(_pair('known-author'), _pair('inherit'),
                              [{**_pair('different-reviewer'), 'workload_class': 'heavy'}],
                              assignment={'version_id': 'pending-reviewer'})
    assert result['status'] == 'blocked'
    assert 'Ask JAI to reselect this same pending reviewer' in result['help']
    assert 'select_execution' in result['help']
    assert 'reissue/rework the author' not in result['help']


def test_reviewer_uses_assessed_subject_not_inherited_receiver_handoff():
    state, assignment, snapshot, choice = _state_and_review()
    assignment['inputs'].append({'slot_id': 'incoming_handoff', 'refs': [{'version_id': 'earlier-input'}]})
    assert review.enforce(state, assignment, snapshot, choice)['status'] == 'passed'
