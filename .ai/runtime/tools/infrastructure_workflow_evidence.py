# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate exact infrastructure evidence at the existing workflow receiving boundary."""

import copy
import re

import content_lint
import content_spec
from infrastructure_workflow_definitions import DELIVERY, EVIDENCE, PROVIDERS


def _versioned_reference(value):
    return (isinstance(value, dict) and
            all(isinstance(value.get(field), str) and value[field]
                for field in ('engagement', 'scope', 'logical_id', 'version_id')))


def _observed_paths(observations, expected):
    return isinstance(observations, list) and bool(observations) and all(
        isinstance(item, dict) and item.get('flow_id') and item.get('observation_ref')
        and isinstance(item['flow_id'], str) and item.get('expected') == expected and item.get('observed') == expected
        for item in observations)


def _transition_observed(facts):
    reversal = facts.get('reversal')
    dependencies = facts.get('mandatory_dependencies')
    return (facts.get('readiness') == 'PASS'
            and _observed_paths(facts.get('allowed_paths'), 'allow')
            and _observed_paths(facts.get('denied_paths'), 'deny')
            and isinstance(dependencies, list) and bool(dependencies)
            and all(isinstance(item, dict) and item.get('dependency_id')
                    and isinstance(item['dependency_id'], str)
                    and item.get('observation_ref') and item.get('status') == 'verified'
                    for item in dependencies)
            and isinstance(reversal, dict) and reversal.get('status') == 'restored'
            and reversal.get('observation_ref')
            and type(reversal.get('elapsed_seconds')) in (int, float)
            and type(reversal.get('limit_seconds')) in (int, float)
            and 0 <= reversal['elapsed_seconds'] <= reversal['limit_seconds'])


def _transition_scope(scope):
    if not isinstance(scope, dict) or set(scope) != {
            'allowed_flow_ids', 'denied_flow_ids', 'dependency_ids', 'reversal_limit_seconds'}:
        return False
    groups = [scope[key] for key in ('allowed_flow_ids', 'denied_flow_ids', 'dependency_ids')]
    limit = scope['reversal_limit_seconds']
    return (all(isinstance(group, list) and bool(group)
                and all(isinstance(item, str) and item.strip() for item in group)
                and len(set(group)) == len(group) for group in groups)
            and not set(groups[0]).intersection(groups[1])
            and type(limit) is int and limit > 0)


def _observation(model, observation):
    reference = observation.get('observation_ref')
    if not isinstance(reference, str):
        return False
    record = next((row for row in model.get('evidence', [])
                   if isinstance(row, dict) and row.get('id') == reference), {})
    payload = {key: value for key, value in observation.items() if key != 'observation_ref'}
    return bool(record.get('version')) and record.get('payload') == payload


def _transition_coverage(facts, model):
    scope = facts['verification_scope']
    for observed, identifier, expected in (
        ('allowed_paths', 'flow_id', 'allowed_flow_ids'),
        ('denied_paths', 'flow_id', 'denied_flow_ids'),
        ('mandatory_dependencies', 'dependency_id', 'dependency_ids'),
    ):
        observations = facts[observed]
        if sorted(item[identifier] for item in observations) != sorted(scope[expected]):
            return False
        if any(not _observation(model, item) for item in observations):
            return False
    reversal = facts['reversal']
    return reversal['limit_seconds'] == scope['reversal_limit_seconds'] and _observation(model, reversal)


def _context_record(model):
    units = model.get('semantic_units', {})
    context = units.get('workflow_context')
    if not isinstance(context, dict):
        return None
    return next((record for record in model.get('evidence', [])
                 if isinstance(record, dict) and record.get('id') == context.get('context_ref')), None)


def _applicable(model, facts, fields):
    reference = facts.get('applicability_ref')
    record = next((item for item in model.get('evidence', [])
                   if isinstance(item, dict) and item.get('id') == reference), {})
    payload = record.get('payload')
    return (isinstance(reference, str) and bool(record.get('version')) and isinstance(payload, dict)
            and all(isinstance(facts.get(key), str) and facts[key].strip()
                    and payload.get(key) == facts[key] for key in fields)
            and payload.get('supported') is True and bool(payload.get('source'))
            and (facts.get('integration') != 'cloud-source-repositories'
                 or payload.get('existing_eligibility') is True))


def _provider_evidence(path, field, facts, model):
    provider = facts.get('provider')
    mechanism = path['mechanism']
    expected = next((key for key in PROVIDERS
                     if mechanism == key or mechanism.startswith(key + '-')), None)
    if provider != expected:
        return 'INFRASTRUCTURE_PROVIDER_MISMATCH'
    applicability = {
        'handoff_cloud_scope': ('provider', 'target_id', 'region'),
        'handoff_delivery_source': ('provider', 'target_id', 'region', 'integration'),
        'handoff_delivery_promotion': ('provider', 'target_id', 'region', 'deployment_action'),
    }
    if field in applicability and not _applicable(model, facts, applicability[field]):
        return 'INFRASTRUCTURE_APPLICABILITY_UNVERIFIED'
    if field == 'handoff_cloud_readiness' and facts.get('independent_verdict') != 'PASS':
        return 'INFRASTRUCTURE_READINESS_UNVERIFIED'
    if mechanism not in DELIVERY:
        return None
    _, _, integrations, store, action = DELIVERY[mechanism]
    if ('artifact_digest' in facts and (not isinstance(facts['artifact_digest'], str)
            or not re.fullmatch(r'sha256:[0-9a-f]{64}', facts['artifact_digest']))):
        return 'DELIVERY_ARTIFACT_NOT_IMMUTABLE'
    if (field == 'handoff_delivery_source' and facts.get('integration') not in integrations
            or field == 'handoff_delivery_build' and facts.get('artifact_store') != store
            or field == 'handoff_delivery_promotion' and facts.get('deployment_action') != action):
        return 'DELIVERY_INTEGRATION_UNSUPPORTED'
    if field in ('handoff_delivery_build', 'handoff_delivery_promotion'):
        identity = facts.get('credential_scope' if field == 'handoff_delivery_build' else 'deployment_identity')
        if (not isinstance(identity, dict) or identity.get('target_id') != facts['target_id']
                or identity.get('environment') != facts['environment']
                or identity.get('short_lived') is not True or not identity.get('principal')):
            return 'DELIVERY_CREDENTIAL_SCOPE_UNVERIFIED'
    if field == 'handoff_delivery_rollout':
        rollout = facts.get('rollout_observations')
        reversal = facts.get('rollback_record')
        if (not isinstance(rollout, dict) or rollout.get('target_id') != facts['target_id']
                or rollout.get('artifact_digest') != facts['artifact_digest']
                or not _observation(model, rollout) or not isinstance(reversal, dict)
                or reversal.get('target') != facts['rollback_target'] or not _observation(model, reversal)
                or (rollout.get('status'), reversal.get('status')) not in (
                    ('healthy', 'not-needed'), ('halted', 'restored'))):
            return 'DELIVERY_ROLLOUT_OR_REVERSAL_UNVERIFIED'
    if field in ('handoff_delivery_test', 'handoff_delivery_health') and facts.get('independent_verdict') != 'PASS':
        return 'DELIVERY_INDEPENDENT_VERDICT_FAILED'
    return None


def artifact_findings(workflow, path, step, model):
    """Check the selected route's local evidence without traversing predecessor inputs."""
    rule = EVIDENCE.get((workflow, path['id'], step))
    if rule is None:
        return []
    field, keys, _ = rule
    facts = model.get('semantic_units', {}).get(field)
    if not isinstance(facts, dict):
        return ['INFRASTRUCTURE_EVIDENCE_MISSING']
    if any(not (isinstance(facts.get(key), str) and facts[key].strip()
                or _versioned_reference(facts.get(key))) for key in keys if key != 'verification_scope'):
        return ['INFRASTRUCTURE_SUBJECT_INVALID']
    if 'provider' in keys:
        finding = _provider_evidence(path, field, facts, model)
        if finding:
            return [finding]
    if 'verification_scope' in keys and not _transition_scope(facts.get('verification_scope')):
        return ['TRANSITION_VERIFICATION_SCOPE_INVALID']
    if field == 'handoff_transition_observations' and (
            not _transition_observed(facts) or not _transition_coverage(facts, model)):
        return ['TRANSITION_READINESS_OR_REVERSAL_UNVERIFIED']
    if field == 'handoff_transition_readiness' and facts.get('continuity_verdict') != 'PASS':
        return ['TRANSITION_CONTINUITY_UNVERIFIED']
    return []


def verify(workflow, path, step, model, producer, predecessor, trust):
    """Return infrastructure findings and the exact accepted input reference, if required.

    The caller supplies the host trust adapter used for receiving acceptance.
    This function checks the current evidence and the immediate governing input.
    An absent verified input fails a linked handoff.
    """
    rule = EVIDENCE.get((workflow, path['id'], step))
    if rule is None:
        return [], None
    field, keys, link = rule
    findings = artifact_findings(workflow, path, step, model)
    if findings:
        return findings, None
    facts = model['semantic_units'][field]
    if not link:
        return [], None
    lookup = getattr(trust, 'predecessor_input', None)
    prior_model = predecessor.get('model') if isinstance(predecessor, dict) else None
    if not callable(lookup) or not isinstance(prior_model, dict):
        return ['INFRASTRUCTURE_PREDECESSOR_UNVERIFIED'], None
    prior_snapshot = copy.deepcopy(prior_model)
    prior_producer = prior_snapshot.get('producer')
    if not isinstance(prior_producer, dict):
        return ['INFRASTRUCTURE_PREDECESSOR_UNVERIFIED'], None
    prior_token = prior_producer.pop('attestation', None)
    proof = content_lint._host_verify(trust, prior_token) if prior_token else None
    if not proof or proof.get('snapshot_digest') != content_spec.canonical_hash(prior_snapshot):
        return ['INFRASTRUCTURE_PREDECESSOR_UNVERIFIED'], None
    previous = path['steps'][path['steps'].index(step) - 1]
    prior_field, prior_keys, _ = EVIDENCE[workflow, path['id'], previous]
    prior_facts = prior_model.get('semantic_units', {}).get(prior_field)
    if (not isinstance(prior_facts, dict) or _context_record(model) != _context_record(prior_model)
            or any(facts[key] != prior_facts.get(key) for key in keys if key in prior_keys)):
        return ['INFRASTRUCTURE_SUBJECT_MISMATCH'], None
    reference = lookup(producer, prior_token)
    if not reference or facts.get(link) != reference:
        return ['INFRASTRUCTURE_PREDECESSOR_UNVERIFIED'], None
    return [], reference
