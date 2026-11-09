#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Run seven offline workflow protocol simulations, never professional approvals.

Local fixture identities exercise the existing host-verification interface; no
worker, provider or human signs these fixtures. Actual dispatcher cryptography
is tested separately by the workflow regression suite. These simulations make
no live-provider, runtime-isolation or professional-content qualification claim.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import content_lint
import content_spec
import content_workflow

SCENARIOS = {
    'cloud-migration': ('migration-and-cutover', 'Move a synthetic inventory service to a managed cloud region.', 'Reconcile 240 asset records; restore within two hours and reverse the cutover on any unexplained imbalance.'),
    'regulated-service': ('new-service-onboarding', 'Introduce a synthetic regulated settlement support service.', 'Retain dual control at trust boundaries; escalate missing retention authority and recovery evidence.'),
    'erp-data-migration': ('data-product-delivery', 'Reconcile a synthetic ERP order dataset with its versioned target schema.', 'Preserve order identifiers and currency totals; reject duplicate keys and unmatched ledger entries.'),
    'security-incident': ('cyber-incident-breach-to-recovery', 'Contain a fictional compromised account and restore the affected service.', 'Preserve evidence lineage; isolate the account and escalate notification decisions to human authority.'),
    'application-delivery': ('idea-to-production', 'Deliver a synthetic work-order application change.', 'Trace acceptance criteria to tests; retain rollback capability and independent release acceptance.'),
    'saas-integration': ('enterprise-release-orchestration', 'Integrate a fictional SaaS event interface with an internal order service.', 'Validate versioned event contracts, retries, reconciliation and the supplier exit boundary.'),
    'decommission': ('service-retirement-and-decommission', 'Retire a fictional reporting platform after dependency migration.', 'Prove consumer migration and retention disposition; stop destructive actions until external authority accepts.'),
}

# These are explicit protocol-fixture selections, never inferred task routing.
SCENARIO_PATHS = {
    'cloud-migration': 'cutover',
    'regulated-service': 'critical-regulated/saas-cots',
    'erp-data-migration': 'nonpersonal',
    'security-incident': 'suspected',
    'application-delivery': 'new-product',
    'saas-integration': 'coordinated',
    'decommission': 'authorised-retirement',
}


class _FixtureHost:
    def __init__(self):
        self.records = {}

    def attest(self, principal, subject, snapshot, context, reviewer):
        payload = {'principal': principal, 'subject_digest': content_spec.canonical_hash(subject),
                   'snapshot_digest': snapshot, 'context_digest': content_spec.canonical_hash(context),
                   'reviewer': reviewer}
        token = 'synthetic-fixture:' + content_spec.canonical_hash(payload)
        self.records[token] = payload
        return token

    def verify(self, token):
        return copy.deepcopy(self.records.get(token)) if isinstance(token, str) else None


def _put(target, field, value):
    parts = field.split('.')
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


def _model(spec, scenario_id, goal, criterion, step, upstream):
    model = {'artifact_id': f'synthetic-scenario:{scenario_id}:{step}',
             'contract_id': spec['artifact_id'], 'document_kind': spec['document_kind'],
             'compiled_spec_hash': spec['compiled_spec_hash'], 'context': spec['context'],
             'semantic_units': {}, 'knowledge_states': {}, 'claims': [], 'evidence': [],
             'scenario_lineage': {'previous_record_hash': upstream, 'scope': goal}}
    for unit in spec['blueprint']['semantic_units']:
        if unit['category'] not in ('required_information', 'conditional_information') or unit['applicability'] is False:
            continue
        for field in unit['semantic_fields']:
            record = {'knowledge_status': 'synthetic-assumption', 'scope': goal,
                      'acceptance_condition': criterion, 'unit_ref': unit['id'],
                      'upstream_record': upstream, 'evidence_limit': 'Fictional protocol fixture, not an observed project outcome.'}
            datatype = unit.get('datatype', 'object')
            value = ([record] if datatype == 'array' else True if datatype == 'boolean'
                     else 1 if datatype in ('integer', 'number')
                     else f'Synthetic scoped input for {unit["id"]}: {goal}' if datatype in ('string', 'reference') else record)
            _put(model['semantic_units'], field, value)
            model['knowledge_states'][field] = 'synthetic-assumption'
    return model


def _review(model, spec, host, principal):
    model = copy.deepcopy(model)
    context = {'scope': 'offline-synthetic-protocol-simulation'}
    model['producer'] = {'context_manifest': context}
    unsigned_hash = content_spec.canonical_hash(model)
    model['producer']['attestation'] = host.attest(principal, model, unsigned_hash, context, False)
    pending = content_lint.evaluate(model, spec)['reviewer']['required_units']
    review = {'semantic_hash': content_spec.canonical_hash(model),
              'compiled_spec_hash': spec['compiled_spec_hash'], 'context_hash': spec['context_hash'],
              'context_manifest': context,
              'unit_reviews': [{'unit_id': unit, 'verdict': 'PASS',
                                'rationale': 'Protocol fixture covers this registered obligation; professional correctness remains unassessed.',
                                'evidence': 'Deterministic synthetic scenario source, not actual control execution.'}
                               for unit in pending], 'findings': []}
    review['attestation'] = host.attest(principal + ':reviewer', review, content_spec.canonical_hash(model), context, True)
    return model, review


def _handoff_material(model, row, selected, context_record, scenario_id, goal, criterion, upstream):
    """Populate registered boundary fields with explicitly fictional protocol data.

    The versioned intake record is selected once per scenario and carried by
    reference. These records exercise field, selection and authenticated-review
    checks; they do not assert real execution, legal decisions or professional
    adequacy of the supplied generic synthetic values.
    """
    source_id = 'synthetic-input:' + scenario_id
    boundary_id = 'synthetic-handoff:' + row['handoff_id']
    input_record = {'id': source_id, 'version': '1', 'payload': {
        'scenario_id': scenario_id, 'scope': goal, 'criterion': criterion,
        'classification': 'synthetic protocol input; no project fact or approval'}}
    boundary_records = {}
    for unit in selected['handoff_content_contract']['units']:
        value = {field: f'Fictional {field} for {row["handover"]}; scoped scenario {scenario_id}'
                 for field in unit['required_fields']}
        value.update(knowledge_status='synthetic-assumption', evidence_refs=[boundary_id])
        model['semantic_units'][unit['semantic_field']] = value
        boundary_records[unit['semantic_field']] = copy.deepcopy(value)
    model['semantic_units']['workflow_context'].update({
        'context_ref': context_record['id'], 'route': 'continue',
        'input_refs': [source_id],
        'route_evidence': 'Synthetic current gate observation: ' + criterion})
    model['evidence'].extend([input_record, copy.deepcopy(context_record), {
        'id': boundary_id, 'version': '1', 'payload': {
            'scenario_id': scenario_id, 'handoff_id': row['handoff_id'],
            'scope': goal, 'criterion': selected['acceptance_criterion'],
            'upstream_record_hash': upstream, 'declared_records': boundary_records,
            'classification': 'Fictional boundary values; no real execution or authority evidence'}}])
    return model


def _receiver(row, model, report, catalog, host, principal, path):
    subject = {'handoff_id': row['handoff_id'], 'semantic_hash': content_spec.canonical_hash(model),
               'report_hash': report['report_hash'], 'catalog_hash': catalog['catalog_hash'],
               'criterion': row['acceptance_criterion'], 'receiving_role': row['receiving_role'],
               'path_id': path['id'],
               'handoff_content_hash': content_spec.canonical_hash(row['handoff_content_contract']),
               'verdict': 'PASS', 'evidence': 'Synthetic receiver protocol observation against this exact scoped gate.',
               'unit_reviews': [{'unit_id': unit['id'], 'verdict': 'PASS',
                   'rationale': 'Protocol fixture supplies this exact selected boundary unit; professional meaning remains unassessed.',
                   'evidence': 'Versioned fictional boundary/context records, not an actual operation or approval.'}
                   for unit in row['handoff_content_contract']['units']],
               'context_manifest': {'scope': 'offline-synthetic-protocol-simulation'}}
    subject['attestation'] = host.attest(principal, subject, content_spec.canonical_hash(model), subject['context_manifest'], True)
    return subject


def _run_case(root, engine, catalog, scenario_id):
    workflow, goal, criterion = SCENARIOS[scenario_id]
    profile = catalog['profiles'][workflow]
    path = next((path for path in profile['paths'] if path['id'] == SCENARIO_PATHS[scenario_id]), None)
    if path is None:
        raise ValueError('SCENARIO_PATH_MISSING')
    rows = sorted((row for row in catalog['bindings']
                   if row['workflow_id'] == workflow and row['step'] in path['steps']), key=lambda row: row['step'])
    if not rows:
        raise ValueError('SCENARIO_WORKFLOW_MISSING')
    trace = []
    previous = '0' * 64
    host = _FixtureHost()
    negatives = {}
    principal = f'synthetic:{scenario_id}:producer'
    context_record = {'id': 'synthetic-context:' + scenario_id, 'version': '1', 'payload': {
        'workflow_id': workflow, 'profile_hash': rows[0]['handoff_content_contract']['workflow_profile_hash'],
        'context_id': 'synthetic-intake:' + scenario_id, 'context_version': '1',
        'variant': path['variant'], 'mechanism_variant': path['mechanism'],
        'entry_inputs': {name: {'source_id': f'synthetic-intake:{scenario_id}:{index}',
                               'version': '1', 'scope': goal, 'criterion': criterion}
                         for index, name in enumerate(profile['entry_inputs'], 1)}}}
    for row in rows:
        selected = row['variant_bindings'][path['id']]
        effective = {**row, **selected}
        contract_id = effective['contract_ids'][0] if effective['contract_ids'] else 'enterprise-applications-architect:2'
        spec = engine.resolve(contract_id, {'processes_personal_data': False,
                                            'regulatory_requirement': scenario_id == 'regulated-service'})
        raw = _model(spec, scenario_id, goal, criterion, row['step'], previous)
        raw = _handoff_material(raw, row, selected, context_record, scenario_id, goal, criterion, previous)
        model, review = _review(raw, spec, host, principal)
        qa = content_lint.evaluate(model, spec, reviewer=review, trusted_executions=host)
        receiver = f'synthetic:{scenario_id}:receiver:{row["step"]}'
        acceptance = _receiver(effective, model, qa, catalog, host, receiver, path)
        kwargs = {'root': root, 'acceptance': acceptance, 'trusted_executions': host,
                  'receiving_assignments': {receiver: [effective['receiving_role']]}, 'resolver': engine}
        checked = content_workflow.check(row['handoff_id'], model, qa, **kwargs)
        human = 'EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED' in checked['findings']
        expected = 'EXPECTED_L0_ESCALATION' if human else 'ACCEPTANCE_VERIFIED'
        ok = (checked['findings'] == ['EXISTING_SIGNED_L0_ACCEPTANCE_REQUIRED'] if human
              else checked['status'] == 'ACCEPTANCE_VERIFIED')
        record = {'step': row['step'], 'handoff_id': row['handoff_id'],
                  'contract_id': contract_id, 'document_kind': spec['document_kind'],
                  'compiled_spec_hash': spec['compiled_spec_hash'], 'context_hash': spec['context_hash'],
                  'semantic_hash': content_spec.canonical_hash(model), 'content_qa_hash': qa['report_hash'],
                  'producer_principal': principal, 'receiver_principal': receiver,
                  'path_id': path['id'], 'findings': list(checked['findings']),
                  'previous_record_hash': previous, 'acceptance': expected, 'passed': ok,
                  'authority_granted': False}
        record['record_hash'] = content_spec.canonical_hash(record)
        trace.append(record)
        previous = record['record_hash']
        if row is rows[0]:
            forged = copy.deepcopy(acceptance)
            forged['attestation'] = 'unregistered-forged-receiver'
            rejected = content_workflow.check(row['handoff_id'], model, qa, **{**kwargs, 'acceptance': forged})
            negatives['forged_receiver_rejected'] = rejected['status'] != 'ACCEPTANCE_VERIFIED'
            wrong_role = content_workflow.check(row['handoff_id'], model, qa, **{**kwargs, 'receiving_assignments': {}})
            negatives['unassigned_receiver_rejected'] = 'RECEIVER_ROLE_UNASSIGNED' in wrong_role['findings']
            changed = copy.deepcopy(model)
            changed['scenario_lineage']['scope'] += ' Altered after the reviewed snapshot.'
            negatives['changed_snapshot_rejected'] = bool(content_lint.verify_report(qa, changed, spec, host))
            original_hash = content_spec.canonical_hash(model)
            rolled_back = copy.deepcopy(model)
            negatives['rollback_preserves_original'] = (content_spec.canonical_hash(rolled_back) == original_hash
                                                        and not content_lint.verify_report(qa, rolled_back, spec, host))
            empty = copy.deepcopy(raw)
            empty['semantic_units'] = {}
            negatives['empty_source_rejected'] = content_lint.evaluate(empty, spec)['deterministic_status'] == 'FAIL'
            self_review = copy.deepcopy(review)
            self_review.pop('attestation')
            self_review['attestation'] = host.attest(principal, self_review, content_spec.canonical_hash(model), self_review['context_manifest'], True)
            self_qa = content_lint.evaluate(model, spec, reviewer=self_review, trusted_executions=host)
            negatives['self_review_rejected'] = self_qa['reviewer']['status'] != 'verified-independent-review'
            try:
                content_workflow.check('nonexistent-scenario-workflow:1', model, qa, **kwargs)
            except ValueError as exc:
                negatives['orphan_handoff_rejected'] = str(exc) == 'UNKNOWN_WORKFLOW_HANDOFF'
            else:
                negatives['orphan_handoff_rejected'] = False
        if human:
            negatives['human_approval_not_fabricated'] = not checked['production_release_authorized'] and checked['status'] == 'ACCEPTANCE_PENDING'
            break
        principal = receiver
    passed = bool(trace) and trace[-1]['acceptance'] == 'EXPECTED_L0_ESCALATION' and all(row['passed'] for row in trace) and len(negatives) == 8 and all(negatives.values())
    return {'scenario_id': scenario_id, 'workflow_id': workflow, 'intent': goal,
            'acceptance_condition': criterion, 'status': 'PASS' if passed else 'FAIL',
            'trace': trace, 'negative_checks': negatives,
            'professional_content_review': 'NOT_EXECUTED', 'external_L0': 'ESCALATED_NOT_APPROVED'}


def run_scenarios(root=None, selection=None):
    """Execute selected registered synthetic workflow cases without subprocesses.

    Args:
        root: Trusted repository or installed runtime root, never an input policy.
        selection: Optional nonempty list of unique registered scenario names;
            None runs all seven. Source and evidence remain local and synthetic.
    Returns:
        Deterministic hash-bound protocol report with expected human escalations,
        rejection observations and explicit absence of professional approval.
    Raises:
        ValueError: For unknown/empty/duplicate selection or invalid registry.
        OSError: For missing required locally installed resources.
    """
    names = list(SCENARIOS) if selection is None else list(selection)
    if not names:
        raise ValueError('EMPTY_SCENARIO_SELECTION')
    if len(set(names)) != len(names) or any(name not in SCENARIOS for name in names):
        raise ValueError('UNKNOWN_SCENARIO_OR_DUPLICATE_SELECTION')
    engine = content_spec.ContentSpec(root)
    catalog = content_workflow.load_bindings(root)
    cases = [_run_case(root, engine, catalog, name) for name in names]
    report = {'schema_version': '1.0.0', 'qualification_class': 'synthetic-regression',
              'scenario_count': len(cases), 'scenarios': cases,
              'workflow_catalog_hash': catalog['catalog_hash'],
              'status': 'PASS' if all(case['status'] == 'PASS' for case in cases) else 'FAIL',
              'live_provider_calls': 0, 'professional_approval': False,
              'production_release_authorized': False, 'live_identity_isolation_qualified': False,
              'limitations': ['Fixture host identities exercise protocol checks; no live worker isolation is claimed.',
                              'Populated obligation values are synthetic protocol data, not professional document exemplars.',
                              'Human authority remains external; terminal acceptance is intentionally escalated.']}
    report['report_hash'] = content_spec.canonical_hash(report)
    return report


def verify_result(report):
    """Check report/hash-chain consistency without granting any authority.

    Args:
        report: Untrusted JSON-compatible scenario report.
    Returns:
        List of integrity diagnostics; empty means internal consistency only,
        never authentication or semantic correctness. Re-execute to reproduce.
    """
    problems = []
    if report.get('report_hash') != content_spec.canonical_hash({k: v for k, v in report.items() if k != 'report_hash'}):
        problems.append('REPORT_HASH_MISMATCH')
    for case in report.get('scenarios', []):
        previous = '0' * 64
        receiver = None
        for record in case['trace']:
            if (record['previous_record_hash'] != previous
                    or record['record_hash'] != content_spec.canonical_hash({k: v for k, v in record.items() if k != 'record_hash'})
                    or (receiver is not None and record['producer_principal'] != receiver)):
                problems.append('TRACE_CHAIN_INVALID')
                break
            previous = record['record_hash']
            receiver = record['receiver_principal']
    return sorted(set(problems))


def main(argv=None):
    """Run offline cases and optionally create a new immutable report file.

    Args:
        argv: Optional CLI argument sequence; process arguments are used by default.
    Returns:
        Zero for passing simulations, one for failed checks, invalid input or an
        existing output file. No provider, network or authority act is invoked.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['run'])
    parser.add_argument('--root', type=Path)
    parser.add_argument('--scenario', action='append', choices=sorted(SCENARIOS))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        report = run_scenarios(args.root, args.scenario)
        serialized = json.dumps(report, indent=2) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(serialized)
        print(json.dumps({key: value for key, value in report.items() if key != 'scenarios'}, indent=2))
        return 0 if report['status'] == 'PASS' else 1
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({'status': 'ERROR', 'diagnostic': 'SCENARIO_INPUT_OR_OUTPUT_INVALID'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
