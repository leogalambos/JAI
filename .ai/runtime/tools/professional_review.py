#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Live professional review prerequisites over exact captured producer choices.

A different requested provider/model is a prerequisite for SABSA independent
review. This does not prove served backend identity or replace professional
review, human authority, model availability or ordinary admission controls.
"""
from __future__ import annotations

import argparse
import copy
from functools import lru_cache
import json
from pathlib import Path
import re

import execution_profiles
import governed_routing as routing
import lifecycle as lc
import model_router

_RULE_FIELDS = {'id', 'kind', 'author_categories', 'author_operators', 'source_contract'}
_RETAINED = {'id': 'sabsa-independent-review-model', 'kind': 'different-model',
             'author_categories': ['SABSA Security Architecture'],
             'author_operators': ['sabsa-architect'], 'source_contract': 'agent:sabsa-architect'}
_UNKNOWN = {'inherit', 'inherit-session', 'default', 'unknown', 'unspecified', 'auto', ''}
_REVIEW_ROLES = {'reviewer', 'integration_reviewer', 'receiver'}
_IDENTIFIER = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,159}$')


def constraints_problems(rules):
    """Validate optional professional rule metadata without changing authority.

    Args:
        rules: List of closed different-model constraint declarations; absent metadata
            is handled by the caller, whereas an explicit null is invalid.
    Returns:
        Located structural problems; an empty list preserves legacy metadata absence.
    """
    if not isinstance(rules, list):
        return ['professional_review_constraints must be a list']
    problems, identifiers = [], set()
    for index, rule in enumerate(rules):
        label = f'professional_review_constraints[{index}]'
        if not isinstance(rule, dict) or set(rule) != _RULE_FIELDS:
            problems.append(label + ': closed constraint fields required')
            continue
        if not isinstance(rule['id'], str) or not re.fullmatch('[a-z][a-z0-9-]{0,79}', rule['id']):
            problems.append(label + ': invalid id')
        elif rule['id'] in identifiers:
            problems.append(label + ': duplicate id')
        else:
            identifiers.add(rule['id'])
        if rule['kind'] != 'different-model':
            problems.append(label + ': unknown constraint kind')
        for field in ('author_categories', 'author_operators'):
            values = rule[field]
            if (not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values)
                    or len(values) != len(set(value for value in values if isinstance(value, str)))):
                problems.append(label + ': ' + field + ' must contain distinct nonempty labels')
        if not rule['author_categories'] and not rule['author_operators']:
            problems.append(label + ': author applicability is required')
        if not isinstance(rule['source_contract'], str) or not re.fullmatch('agent:[a-z][a-z0-9-]{0,79}', rule['source_contract']):
            problems.append(label + ': source_contract must identify a canonical agent')
    return problems


def _known(pair):
    return (isinstance(pair, dict) and pair.get('provider') in {'codex', 'claude'}
            and isinstance(pair.get('model_selector'), str) and pair['model_selector'].strip().lower() not in _UNKNOWN
            and _IDENTIFIER.fullmatch(pair['model_selector']) is not None)


def _safe_pair(pair):
    pair = pair if isinstance(pair, dict) else {}
    return {key: pair.get(key) for key in ('provider', 'model_selector', 'reasoning_effort')}


def _describe(pair):
    return f"{pair.get('provider') or 'unknown'}/{pair.get('model_selector') or 'unknown'} (effort {pair.get('reasoning_effort') or 'unspecified'})"


def _describe_alternative(item):
    route_provider = item['routing_provider']
    route_model = item['routing_model_selector']
    workload = item['workload_class'] or 'declared-class'
    if (route_provider, route_model) == (item['provider'], item['model_selector']):
        return f"{workload}: {_describe(item)}"
    return (f"{workload}: route provider={route_provider}, model_selector={route_model}; "
            f"backend {_describe(item)}")


def check_pair(author, reviewer, alternatives, assignment=None):
    """Check an explicit author/reviewer requested-model pair for SABSA review.

    Args:
        author: Captured provider, model_selector and optional reasoning_effort.
        reviewer: Selected provider, model_selector and optional reasoning_effort.
        alternatives: Registry-declared backend reviewer identities with optional
            workload_class and exact routing_provider/routing_model_selector fields.
            Process resource routing stays distinct from its declared AI backend.
        assignment: Optional exact pending assignment reference for corrective help.
    Returns:
        Passed/blocked diagnostic, safe pair facts, compatible declared alternatives
        and inline corrective help. Served backend identity is always unknown.
    """
    author, reviewer = _safe_pair(author), _safe_pair(reviewer)
    compatible = []
    for alternative in alternatives:
        if not _known(author) or not _known(alternative):
            continue
        candidate = {**_safe_pair(alternative), 'workload_class': alternative.get('workload_class'),
                     'routing_provider': alternative.get('routing_provider', alternative['provider']),
                     'routing_model_selector': alternative.get('routing_model_selector', alternative['model_selector'])}
        if _known(author) and (candidate['provider'], candidate['model_selector']) == (author['provider'], author['model_selector']):
            continue
        if candidate not in compatible:
            compatible.append(candidate)
    valid = (_known(author) and _known(reviewer)
             and (author['provider'], author['model_selector']) != (reviewer['provider'], reviewer['model_selector']))
    intro = f'SABSA independent review: author {_describe(author)}; reviewer {_describe(reviewer)}. '
    if valid:
        help_text = intro + 'Different requested model prerequisite satisfied; served backend identity is unobserved.'
    elif not _known(author):
        help_text = intro + ('Review is blocked because the author requested-model control is unknown. '
            'Different effort or reviewer-only reselection cannot establish the missing author control. ')
        if assignment is not None:
            help_text += ('Keep the same pending reviewer assignment ' + json.dumps(assignment, sort_keys=True) + '. '
                'The actual recorded author execution does not establish an explicit model; do not backfill or edit its capture. '
                'Ask the governing owner to reissue/rework the author with an explicit captured model and produce a new candidate '
                'only through an allowed existing procedure and its remaining allowances. If no such captured choice or '
                'procedure is available, correct configuration and start a separately authorized new engagement. '
                'In either case retain the old journal and budgets. Do not guess the author model or treat '
                'selected controls as observed served identity. Changing a profile does not repair this pinned run. ')
        else:
            help_text += ('For a planned author call, choose explicit author model controls before the author call. '
                'If a candidate already exists, recover its authentic original controls if available or rework the author '
                'with an explicit model to produce a new candidate before reviewer dispatch. Preserve the task and context; '
                'do not guess the executed author model. Rerun this shared pair check with the authentic selected controls. ')
        help_text += 'Model identity here concerns selected/requested controls; served backend identity remains unobserved.'
    else:
        help_text = (intro + 'Review is blocked: different effort on the same provider/model is insufficient; '
            'select an explicit different requested model. ')
        if assignment is not None:
            help_text += 'Keep the same pending reviewer assignment ' + json.dumps(assignment, sort_keys=True) + '. '
            if compatible:
                help_text += ('Ask JAI to reselect this same pending reviewer with a compatible captured model. '
                    'Read its current previous selection and submit actual select_execution for this assignment with one '
                    'compatible captured choice: ' + '; '.join(
                        _describe_alternative(item) for item in compatible) + '. ')
            else:
                help_text += ('No compatible captured alternative exists. Hold the assignment pending; ask the deployment administrator '
                    'to configure a distinct model for a future capture. This pinned run has no in-place registry replacement API; '
                    'the governing owner must start a separately authorized new engagement with corrected configuration. '
                    'Retain the existing journal and do not assume output reuse or fresh allowances are authorized. ')
            help_text += ('Alternatives are registry-declared only, not observed host/account availability. Changing a profile does not '
                          'repair this pinned run; do not reset its journal, budgets or acceptance.')
        else:
            if compatible:
                help_text += ('Ask JAI to reselect this same pending reviewer with an explicit different native model from these '
                    'compatible declared choices: ' + '; '.join(
                        _describe_alternative(item) for item in compatible) + '. ')
            else:
                help_text += ('No compatible registry-declared alternative exists. Keep the native reviewer pending and ask the '
                    'deployment administrator or host operator to register a distinct model. ')
            help_text += ('Preserve the task and context, then rerun this shared pair check before dispatch. '
                'Alternatives are registry-declared only, not observed host/account availability.')
    return {'status': 'passed' if valid else 'blocked', 'help': help_text, 'author': author, 'reviewer': reviewer,
            'alternatives': compatible, 'served_model': None}


@lru_cache(maxsize=1)
def _canonical_rules():
    registry = json.loads(model_router.BASE.read_text(encoding='utf-8'))
    declared = registry.get('professional_review_constraints', [])
    problems = constraints_problems(declared)
    if problems:
        raise lc.ERROR('P_PROOF', '; '.join(problems))
    # The retained canonical contract cannot be waived by deleting or narrowing
    # captured/admin metadata. This is a live prerequisite, never prefix replay.
    return tuple([copy.deepcopy(_RETAINED), *copy.deepcopy(declared)])


def _rules(snapshot):
    captured = snapshot['models'].get('professional_review_constraints', [])
    problems = constraints_problems(captured)
    if problems:
        raise lc.ERROR('P_PROOF', '; '.join(problems))
    unique = {lc.canonical(rule): rule for rule in [*_canonical_rules(), *captured]}
    return list(unique.values())


def _snapshot(state, assignment):
    reference = assignment['routing']['policy']
    source = state.resolve(reference, 'source')
    key = (lc.canonical(reference), tuple(source['material']))
    if key not in state._routing_snapshots:
        snapshot = routing.load_policy(source, lambda identifier: state._validation_bytes(identifier, False))
        state._routing_snapshots[key] = lc._freeze(snapshot)
    return state._routing_snapshots[key]


def _affected(state, rules, snapshot, specialties):
    cache = state.__dict__.setdefault('_professional_review_catalogues', {})
    key = snapshot.get('descriptor', {}).get('catalogue_blob_id', id(snapshot))
    if key not in cache:
        cache[key] = {row['slug']: row for row in snapshot['catalogue']['roles']}
    rows = cache[key]
    selected = [rows[slug] for slug in specialties if slug in rows]
    return any(row.get('category') in rule['author_categories'] or row.get('operator_agent') in rule['author_operators']
               for row in selected for rule in rules)


def _model_pair(mapping, provider):
    transport = mapping.get('execution', {}).get('provider', provider)
    if transport in {'codex', 'claude'}:
        # Native model execution is positively AI regardless of a conflicting
        # administrator label; registry validation also rejects such relabeling.
        return {'provider': transport, 'model_selector': mapping['model_selector'],
                'reasoning_effort': mapping.get('reasoning_effort')}
    if transport != 'json-process/1':
        raise ValueError('Execution model transport is unavailable')
    kind = mapping.get('model_kind')
    if kind == 'deterministic':
        return None
    if kind == 'ai':
        pair = {'provider': mapping.get('model_provider'), 'model_selector': mapping.get('model_identity'),
                'reasoning_effort': mapping.get('reasoning_effort')}
        if _known(pair):
            return pair
    raise lc.ERROR('P_PROOF', 'SABSA review prerequisite cannot identify this process execution as deterministic or AI with '
        'an explicit backend provider/model identity. Hold the same pending reviewer assignment. Ask the deployment '
        'administrator to declare model_kind and, for AI, model_provider/model_identity in the governing capability '
        'configuration for a future capture. A pinned policy cannot be edited in place; its governing owner must use a '
        'separately authorized new engagement if the captured prerequisite is unavailable. Preserve the old journal. '
        'Do not infer model kind from process names or '
        'arguments, assume non-AI execution, change effort, or reset journal/acceptance.')


def _alternatives(snapshot, provider, responsibility):
    models = snapshot['models']
    result = []
    classes = models.get('providers', {}).get(provider, {}).get('classes', {})
    preference_order = {'standard': 0, 'heavy': 1, 'research': 2, 'light': 3}
    for workload in sorted(classes, key=lambda name: (preference_order.get(name, 4), name)):
        preference = models.get('execution_profile')
        if preference and preference.get('provider') == provider:
            _, mapping = execution_profiles.mapping(preference, responsibility, workload, models)
        else:
            mapping = copy.deepcopy(models['providers'][provider]['classes'][workload])
        try:
            pair = _model_pair(mapping, provider)
        except ValueError:
            continue
        if pair is not None:
            result.append({**pair, 'workload_class': workload, 'routing_provider': provider,
                           'routing_model_selector': mapping['model_selector']})
    return result


def _domain_subject(state, reference, candidate):
    semantic = getattr(state, '_product_content', {}).get(reference['version_id']) or {}
    if semantic.get('format') == 'jai-sabsa-content/1':
        return True
    profile_ref = candidate.get('profile')
    if profile_ref is None:
        return False
    try:
        profile = state.resolve(profile_ref, 'profile')
        selector = profile.get('content_profile')
        if not isinstance(selector, dict):
            return False
        # Current profiles name an adopted policy UsePoint; older/external
        # captured contracts may already contain its exact version reference.
        policy_ref = selector if 'version_id' in selector else state.content_policy(profile_ref)['ref']
        admitted = getattr(state, '_content_policies', {}).get(policy_ref['version_id']) or {}
        return admitted.get('format') == 'jai-sabsa-content-profile/1'
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def _producer(state, reference, candidate):
    assigned = state.resolve(candidate['assignment'], 'assignment')
    snapshot = _snapshot(state, assigned)
    provenance = state.provenance[reference['version_id']]
    context = state.resolve(provenance['context'], 'context')
    if context['assignment'] != candidate['assignment'] or context['execution']['phase'] != 'work':
        raise ValueError('No exact author work context')
    choice = state.resolve(context['execution']['selection'])['message']['payload']
    if choice['assignment'] != candidate['assignment']:
        raise ValueError('No exact author selection')
    return assigned, snapshot, provenance, context, choice


def _subject_error():
    return lc.ERROR('P_PROOF', 'SABSA review prerequisite requires exactly one canonical assessed-subject or incoming_handoff '
        'binding for the same pending reviewer assignment; the subject is missing or ambiguous. Ask JAI to hold this reviewer '
        'pending and have its governing owner restore/reissue the exact subject binding. Do not guess the reviewed input, '
        'invent an author model, reset the journal or manufacture acceptance.')


def enforce(state, assignment, snapshot, choice, live=True, subject=None):
    """Enforce live retained review prerequisites using immutable author provenance.

    Args:
        state: Existing trusted lifecycle State; no journal or acceptance is written.
        assignment: Actual reviewer/integration reviewer/receiver assignment record.
        snapshot: Captured reviewer routing snapshot already admitted by the State.
        choice: Actual reviewer select_execution payload being admitted or used.
        live: False skips this new-action prerequisite during historical replay.
        subject: Optional exact candidate reference, otherwise assigned input subject.
    Returns:
        Pair diagnostic for affected work; None for unaffected responsibilities or replay.
    Raises:
        ProtocolError: Affected work lacks exact provenance or distinct requested models.
    """
    if not live or assignment.get('responsibility') not in _REVIEW_ROLES:
        return None
    rules = _rules(snapshot)
    subject_slot = 'incoming_handoff' if assignment['responsibility'] == 'receiver' else 'assessed-subject'
    canonical_subjects = [reference for binding in assignment['inputs']
        if binding['slot_id'] == subject_slot for reference in binding['refs']]
    binding_exact = len(canonical_subjects) == 1 and (subject is None or canonical_subjects[0] == subject)
    if not binding_exact and (_affected(state, rules, snapshot, choice.get('specialties', []))
            or _domain_subject(state, {'version_id': ''}, assignment)):
        raise _subject_error()
    subjects = [subject] if subject is not None else canonical_subjects
    reports = []
    cache = state.__dict__.setdefault('_professional_review_checks', {})
    for candidate_ref in subjects:
        candidate = state.resolve(candidate_ref)
        domain_affected = _domain_subject(state, candidate_ref, candidate)
        if not candidate.get('assignment'):
            # A genuine human/non-AI input has no author-model pair to invent.
            continue
        try:
            author_assignment, author_snapshot, provenance, context, author_choice = _producer(
                state, candidate_ref, candidate)
        except (KeyError, TypeError, ValueError) as error:
            known_affected = domain_affected or _affected(state, rules, snapshot, choice.get('specialties', []))
            if not known_affected:
                continue
            raise lc.ERROR('P_PROOF', 'SABSA review prerequisite lacks exact immutable author context/selection provenance; '
                'hold the same pending reviewer assignment and restore the captured producer evidence through its governing owner. '
                'Do not guess the author model, change effort or reset journal/acceptance.') from error
        if not domain_affected and not _affected(state, rules, author_snapshot, author_choice.get('specialties', [])):
            continue
        if not binding_exact:
            raise _subject_error()
        cache_key = (candidate_ref['version_id'], lc.canonical(provenance['context']),
            lc.canonical(context['execution']['selection']), lc.canonical(choice),
            lc.canonical(assignment['routing']['policy']), lc.canonical(rules))
        if cache_key in cache:
            reports.append(copy.deepcopy(cache[cache_key]))
            continue
        _, author_model = routing._execution(author_snapshot['models'], author_choice, author_assignment['responsibility'])
        author_pair = _model_pair(author_model, author_choice['provider'])
        if author_pair is None:
            if len(cache) >= 256:
                cache.pop(next(iter(cache)))
            cache[cache_key] = None
            continue
        _, reviewer_model = routing._execution(snapshot['models'], choice, assignment['responsibility'])
        reviewer_pair = _model_pair(reviewer_model, choice['provider'])
        if reviewer_pair is None:
            report = check_pair(author_pair, {'provider': choice['provider'],
                'model_selector': None, 'reasoning_effort': None},
                _alternatives(snapshot, choice['provider'], assignment['responsibility']), choice.get('assignment'))
            raise lc.ERROR('P_PROOF', 'A deterministic reviewer may provide structural measurements but cannot satisfy '
                'SABSA professional AI review on a different model. Choose an explicit different AI reviewer model. '
                + report['help'])
        # Candidate availability is diagnostic work needed only after a failed
        # immutable pair check; ordinary valid work does not rebuild alternatives.
        report = check_pair(author_pair, reviewer_pair, [], choice.get('assignment'))
        if report['status'] != 'passed':
            report = check_pair(author_pair, reviewer_pair,
                _alternatives(snapshot, choice['provider'], assignment['responsibility']), choice.get('assignment'))
        if report['status'] != 'passed':
            raise lc.ERROR('P_PROOF', report['help'])
        if len(cache) >= 256:
            cache.pop(next(iter(cache)))
        cache[cache_key] = copy.deepcopy(report)
        reports.append(report)
    return reports[-1] if reports else None


def main(argv=None):
    """Run a read-only ordinary-workflow model-pair prerequisite diagnostic.

    Args:
        argv: Explicit arguments or process argv; no provider is launched.
    Returns:
        Zero for a different explicit model, two for blocked/invalid input.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-provider', choices=('codex', 'claude'), required=True)
    parser.add_argument('--author-model', required=True)
    parser.add_argument('--author-effort')
    parser.add_argument('--reviewer-provider', choices=('codex', 'claude'), required=True)
    parser.add_argument('--reviewer-model', required=True)
    parser.add_argument('--reviewer-effort')
    parser.add_argument('--project', default='.')
    parser.add_argument('--profile')
    parser.add_argument('--model-config')
    args = parser.parse_args(argv)
    try:
        models, _ = model_router.effective_registry(args.model_config)
        problems = model_router.validate_registry(models)
        if problems:
            raise ValueError('; '.join(problems))
        preferences = execution_profiles.resolve(args.project, models, args.reviewer_provider, args.profile)
        models['execution_profile'] = preferences
        alternatives = _alternatives({'models': models}, args.reviewer_provider, 'reviewer')
        report = check_pair({'provider': args.author_provider, 'model_selector': args.author_model,
                             'reasoning_effort': args.author_effort},
                            {'provider': args.reviewer_provider, 'model_selector': args.reviewer_model,
                             'reasoning_effort': args.reviewer_effort}, alternatives)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['status'] == 'passed' else 2


if __name__ == '__main__':
    raise SystemExit(main())
