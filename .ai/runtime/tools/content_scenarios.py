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


def _receiver(row, model, report, catalog, host, principal):
    subject = {'handoff_id': row['handoff_id'], 'semantic_hash': content_spec.canonical_hash(model),
               'report_hash': report['report_hash'], 'catalog_hash': catalog['catalog_hash'],
               'criterion': row['acceptance_criterion'], 'receiving_role': row['receiving_role'],
               'verdict': 'PASS', 'evidence': 'Synthetic receiver protocol observation against this exact scoped gate.',
               'context_manifest': {'scope': 'offline-synthetic-protocol-simulation'}}
    subject['attestation'] = host.attest(principal, subject, content_spec.canonical_hash(model), subject['context_manifest'], True)
    return subject


def _run_case(root, engine, catalog, scenario_id):
    workflow, goal, criterion = SCENARIOS[scenario_id]
    rows = sorted((row for row in catalog['bindings'] if row['workflow_id'] == workflow), key=lambda row: row['step'])
    if not rows:
        raise ValueError('SCENARIO_WORKFLOW_MISSING')
    trace = []
    previous = '0' * 64
    host = _FixtureHost()
    negatives = {}
    principal = f'synthetic:{scenario_id}:producer'
    for row in rows:
        contract_id = row['contract_ids'][0] if row['contract_ids'] else 'enterprise-applications-architect:2'
        spec = engine.resolve(contract_id, {'processes_personal_data': False, 'regulatory_requirement': False})
        raw = _model(spec, scenario_id, goal, criterion, row['step'], previous)
        model, review = _review(raw, spec, host, principal)
        qa = content_lint.evaluate(model, spec, reviewer=review, trusted_executions=host)
        receiver = f'synthetic:{scenario_id}:receiver:{row["step"]}'
        acceptance = _receiver(row, model, qa, catalog, host, receiver)
        kwargs = {'root': root, 'acceptance': acceptance, 'trusted_executions': host,
                  'receiving_assignments': {receiver: [row['receiving_role']]}, 'resolver': engine}
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
