# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Prepare blinded content review and measure existing-host review observations.

This measurement helper reuses ContentSpec, ExpertReferences and the existing
host verifier. It creates no approval, reviewer identity or policy activation.
Synthetic seeded cases are development evidence, never human-gold calibration.
"""
from __future__ import annotations

from collections import defaultdict
import copy
import itertools
import re

from content_lint import _host_verify
from content_spec import canonical_hash, load_json
from expert_references import ExpertReferences, LEVELS, _child, _read, _root_path

RUBRIC = {
    'C1': 'Accuracy: distinguish facts, assumptions, uncertainty and unsupported conclusions.',
    'C2': 'Consistency: reconcile identifiers, values, interfaces and cross-artifact meaning.',
    'C3': 'Fitness: support the named recipient decision with a usable native work product.',
    'C4': 'Completeness: satisfy applicable information units and expose missing evidence.',
    'C5': 'Navigation: make claims, dependencies, evidence and next actions discoverable.',
    'C6': 'Ownership/currency: identify accountable owners, versions and change triggers.',
    'C7': 'Clarity/accessibility: use precise language, readable structure and accessible status.',
    'C8': 'Evidence: preserve traceability, reproducibility, independence and authority boundaries.',
    'C9': 'Professional basis: apply exact sources, editions, methods and bounded interpretations.',
}

# Authored negative conclusions exercise professional meaning, not document
# length or a universal approval phrase. They are synthetic seeds, not gold.
COUNTEREXAMPLES = {
    'decision-paper': ('C3', 'Select the cheapest option after comparing its one-year price with the alternatives\' five-year total cost; no common baseline is needed.'),
    'adr': ('C1', 'At-least-once event delivery guarantees exactly one business state transition, so consumers need no idempotency or reconciliation.'),
    'business-case': ('C2', 'Count the same staff saving in both operational efficiency and the headcount reduction, and omit transition costs from the investment total.'),
    'risk-assessment': ('C1', 'Lower the residual likelihood because a control is planned, although no implementation or effectiveness evidence exists.'),
    'assurance-report': ('C4', 'A documented control design proves operating effectiveness across the entire reporting period without sampling actual operation.'),
    'architecture-definition': ('C4', 'An inventory of application boxes establishes architecture completeness without stakeholder concerns, relationship meaning or cross-view correspondences.'),
    'hld': ('C1', 'Unlimited automatic retries guarantee availability and need neither idempotency, timeout bounds nor backpressure.'),
    'operational-handover': ('C8', 'Sending the runbook to operations establishes their service acceptance even though no receiving owner or readiness result is recorded.'),
    'runbook': ('C1', 'A successful backup command proves restoration within the recovery objective, so a restore rehearsal is unnecessary.'),
    'test-report': ('C2', 'Count blocked and unexecuted tests as passed when calculating the release pass rate.'),
    'it-digital-strategy': ('C3', 'Purchasing the target technology is itself proof of the intended business benefit; no outcome baseline or accountable benefit owner is needed.'),
    'requirements-specification': ('C4', 'The requirement that responses must be fast is measurable and testable without a latency threshold, workload or measurement window.'),
    'policy-standard': ('C9', 'A local management exception overrides every applicable legal restriction, regardless of jurisdiction or delegated authority.'),
    'implementation-specification-lld': ('C1', 'Treat the timeout value 2500 as seconds and milliseconds interchangeably because both configurations pass a string parser.'),
    'migration-cutover-plan': ('C1', 'A backup permits rollback after an irreversible external transaction without reconciliation or duplicate-effect risk.'),
    'test-strategy-plan': ('C3', 'Maximising statement coverage alone addresses every product risk, including authorisation, concurrency and recovery.'),
    'operational-readiness-assessment': ('C4', 'An untested recovery procedure and unowned alerts are sufficient evidence of operational readiness.'),
    'service-design-sla': ('C2', 'Commit to a customer recovery time shorter than any supporting supplier can provide without documenting a compensating architecture.'),
    'incident-postmortem': ('C1', 'A deployment occurred before the incident, which proves causation and removes the need to test competing timing or dependency hypotheses.'),
    'compliance-gap-analysis': ('C9', 'A control questionnaire response proves legal compliance without establishing the obligation, applicability or operating evidence.'),
    'benefits-realisation-review': ('C1', 'Attribute all revenue growth after delivery to the programme without a baseline, counterfactual or assessment of external effects.'),
    'transformation-roadmap': ('C3', 'Start every work package simultaneously despite shared capacity limits and prerequisite dependencies.'),
    'client-proposal': ('C2', 'Present a separately priced optional security service as included in the base programme total without changing the scope or price reconciliation.'),
    'executive-proposal': ('C8', 'A recommendation to explore the proposal is equivalent to an authorised funding and contractual commitment.'),
    'technical-proposal': ('C4', 'The architecture is implementation-ready while interface failure semantics and measurable quality targets remain unspecified.'),
    'delivery-proposal': ('C2', 'Treat person-days of effort as calendar duration regardless of parallel staffing, dependencies and client prerequisites.'),
    'commercial-proposal': ('C2', 'Charge client-owned and third-party expenditure as supplier fees while retaining the original supplier payment schedule and total.'),
    'statement-of-work': ('C8', 'Draft legal terms and a proposed signature date establish an executed agreement and permit starting work without the actual contracting authority.'),
    'rfp-response': ('C9', 'Mark every requirement compliant even when an answer is an assumption or an unaccepted exception.'),
    'proposal-compliance-matrix': ('C4', 'A requirement ID and a green status alone establish compliance without an answer location, evidence or exception disposition.'),
    'cybersecurity-transformation-proposal': ('C1', 'A security technology deployment eliminates residual business risk without validating control operation or organisational dependencies.'),
    'managed-security-services-proposal': ('C2', 'A supplier response-time target is the same as customer incident resolution, so both may be reported as one achieved SLA.'),
    'software-engineering-plan': ('C3', 'Schedule integration after every component is complete and omit interface, data migration and recovery risks from the plan.'),
    'api-interface-contract': ('C1', 'HTTP 200 alone proves exactly one successful business effect under retries, concurrent requests and downstream timeouts.'),
    'release-readiness-review': ('C8', 'A readiness recommendation grants production deployment permission without the named release authority.'),
    'transformation-baseline-assessment': ('C1', 'Treat an unverified owner estimate as an observed current-state measurement and use it as a precise improvement baseline.'),
    'target-operating-model': ('C4', 'An organisation chart establishes the target operating model without processes, decision rights, skills or service measures.'),
    'transformation-execution-plan': ('C3', 'Remove all intermediate acceptance and recovery checkpoints because the final target state is attractive.'),
    'security-architecture-assessment': ('C1', 'A product feature list establishes threat coverage without trust boundaries, abuse paths or source requirements.'),
    'threat-model': ('C4', 'Encryption in transit addresses all threats, so tenant isolation, privileged access and business-logic abuse need no analysis.'),
    'security-control-assessment': ('C1', 'Installing a scanner establishes the operating effectiveness of every preventive and detective control.'),
    'devsecops-pipeline-design': ('C1', 'Untrusted pull-request jobs may access production credentials because the repository is owned by the organisation.'),
    'cicd-pipeline-assurance': ('C8', 'A claimed build signature proves trusted provenance even when the signing identity, source revision and runner boundary were not verified.'),
    'appsec-verification-report': ('C4', 'A clean static scan establishes object-level authorisation and business-logic correctness without dynamic negative tests.'),
    'software-supply-chain-assessment': ('C1', 'A matching download checksum proves the publisher identity and absence of malicious code without a trusted reference or provenance chain.'),
}


def prepare_adjudication(root, contract_ids=None, complexities=None):
    """Build reviewer materials and a separate coordinator key for exact contracts.

    Args:
        root: Source checkout or installed runtime containing DCS and references.
        contract_ids: Explicit selected stable IDs; None selects all outputs.
        complexities: Explicit simple/medium/complex levels; None selects all.
    Returns:
        Reviewer packet without author identities/seed labels, plus coordinator
        seed labels. Shared reference and blueprint materials are hash-deduplicated.
    Raises:
        ValueError: A selection is empty, duplicated, unknown or has no reference.
        OSError: Registered sources cannot be read.
    """
    library = ExpertReferences(root)
    engine = library.specs
    selected = sorted(engine.bindings) if contract_ids is None else list(contract_ids)
    levels = list(LEVELS) if complexities is None else list(complexities)
    if not selected or not levels:
        raise ValueError('EMPTY_ADJUDICATION_SELECTION')
    if (not all(isinstance(cid, str) for cid in selected)
            or len(set(selected)) != len(selected) or any(cid not in engine.bindings for cid in selected)):
        raise ValueError('UNKNOWN_OR_DUPLICATE_CONTRACT')
    if (not all(isinstance(level, str) for level in levels)
            or len(set(levels)) != len(levels) or any(level not in LEVELS for level in levels)):
        raise ValueError('UNSUPPORTED_ADJUDICATION_COMPLEXITY')
    runtime = engine.base.parent
    roles = {role['slug']: role for role in load_json(runtime / 'roles.json')['roles']}
    materials, cases, answers, captured_references = {}, [], [], {}
    for cid in selected:
        binding = engine.bindings[cid]
        family = library.canonical_family(binding['semantic_family'], contract_id=cid)
        role = roles[cid.rsplit(':', 1)[0]]
        compiled = engine.resolve(cid)
        blueprint = {'compiled_spec_hash': compiled['compiled_spec_hash'],
                     'units': compiled['blueprint']['semantic_units'],
                     'delivery_form': compiled.get('delivery_form')}
        blueprint_hash = canonical_hash(blueprint)
        materials[blueprint_hash] = blueprint
        for level in levels:
            slot = (family, level)
            if slot not in captured_references:
                entry = next(entry for entry in library.entries
                             if entry['document_kind'] == family and entry['complexity'] == level)
                raw = _read(_child(_root_path(library.base), entry['path']))
                library._validate_raw(raw, family, level, bundled=True)
                captured_references[slot] = raw.decode('utf-8')
            raw = captured_references[slot]
            body = re.sub(r'\A---\n.*?\n---\n', '', raw, count=1, flags=re.S)
            counterexample = re.search(
                r'## Plausible but incorrect conclusion\s*\n\n(.*?)(?=\n\n|\Z)', body, re.S)
            bad_conclusion = (counterexample.group(1).strip() if counterexample else
                'All requirements and framework obligations are fully satisfied. '
                'The work is approved for production without further evidence or independent review.')
            expected_criterion = 'C1'
            if not counterexample:
                if family not in COUNTEREXAMPLES:
                    raise ValueError('NO_AUTHORED_PROFESSIONAL_COUNTEREXAMPLE:' + family)
                expected_criterion, bad_conclusion = COUNTEREXAMPLES[family]
            # Teaching labels are useful to authors but disclose seed answers
            # in a blinded review. Only the case information is shown here.
            body = body.split('## Plausible but incorrect conclusion', 1)[0]
            body = re.sub(r'<a id="[^"]+"></a>', '', body)
            for variant, text in (
                    ('reference', body),
                    ('seeded-defect', body + '\n## Conclusion\n\n'
                     + bad_conclusion)):
                material = {'text': text, 'classification': 'public-synthetic',
                            'truth_status': 'illustrative, not executed or approved'}
                digest = canonical_hash(material)
                materials[digest] = material
                case_id = canonical_hash({'contract': cid, 'complexity': level,
                                          'material': digest, 'blueprint': blueprint_hash})[:24]
                case = {'case_id': case_id, 'contract_id': cid,
                        'domain_index': role['category_index'], 'domain': role['category'],
                        'complexity': level, 'material_hash': digest,
                        'blueprint_hash': blueprint_hash,
                        'compiled_spec_hash': compiled['compiled_spec_hash']}
                cases.append(case)
                answers.append({'case_id': case_id, 'seed_class': variant,
                                'expected_criterion': expected_criterion if variant == 'seeded-defect' else None,
                                'seeded_defect': 'professional-conclusion-counterexample' if variant == 'seeded-defect' else None})
    cases.sort(key=lambda case: case['case_id'])
    packet = {'schema_version': '1.0.0', 'purpose': 'blinded-professional-content-adjudication',
              'seed_key_hash': canonical_hash(sorted(answers, key=lambda case: case['case_id'])),
              'rubric': RUBRIC, 'score_scale': {'0': 'absent or materially wrong',
                  '1': 'major deficiencies', '2': 'partially adequate',
                  '3': 'adequate within explicit limits', '4': 'strong and evidenced'},
              'cases': cases, 'materials': materials,
              'professional_approval': False, 'human_gold': False,
              'limitations': ['Synthetic illustrative cases and proposed specifications.',
                              'Scores do not establish professional acceptance or activate policy.']}
    packet['packet_hash'] = canonical_hash(packet)
    coordinator = {'schema_version': '1.0.0', 'packet_hash': packet['packet_hash'],
                   'cases': sorted(answers, key=lambda case: case['case_id']),
                   'ground_truth': 'synthetic-seeded-expectations-not-human-gold'}
    coordinator['coordinator_hash'] = canonical_hash(coordinator)
    return {'reviewer_packet': packet, 'coordinator': coordinator}


def assess_adjudication(bundle, reviews, trusted_executions=None,
                        reviewer_assignments=None, author_principals=None):
    """Measure authenticated independent review, never grant acceptance.

    Args:
        bundle: Exact prepared reviewer packet and privately retained coordinator.
        reviews: Review subjects carrying existing host attestations, criterion
            scores/rationales/evidence and located findings for a single case.
        trusted_executions: Existing host verifier callback/object, never JSON.
        reviewer_assignments: Host-owned principal to competent domain-index list.
        author_principals: Nonempty host-known author identities excluded from
            independent judgement. Missing authorship keeps coverage pending.
    Returns:
        Hash-bound coverage, seeded recall and reviewer agreement. Unauthenticated
        or out-of-scope reviews are rejected, not counted as evidence. Professional
        approval, human-gold classification and production activation remain false.
    Raises:
        ValueError: Packet/coordinator integrity, case identity or review shape is invalid.
    """
    if (not isinstance(bundle, dict) or not isinstance(bundle.get('reviewer_packet'), dict)
            or not isinstance(bundle.get('coordinator'), dict)):
        raise ValueError('INVALID_ADJUDICATION_BUNDLE')
    packet, coordinator = bundle['reviewer_packet'], bundle['coordinator']
    if (not isinstance(packet.get('cases'), list) or not packet['cases']
            or not isinstance(packet.get('materials'), dict)
            or any(not isinstance(material, dict) for material in packet['materials'].values())
            or not isinstance(coordinator.get('cases'), list)
            or any(not isinstance(case, dict)
                   or not all(isinstance(case.get(key), str) and case[key]
                              for key in ('case_id', 'contract_id', 'material_hash',
                                          'blueprint_hash', 'compiled_spec_hash', 'complexity'))
                   or type(case.get('domain_index')) is not int for case in packet['cases'])
            or any(not isinstance(case, dict) or not isinstance(case.get('case_id'), str)
                   or case.get('seed_class') not in ('reference', 'seeded-defect')
                   or (case.get('seed_class') == 'seeded-defect'
                       and (not isinstance(case.get('expected_criterion'), str)
                            or case['expected_criterion'] not in RUBRIC))
                   for case in coordinator['cases'])):
        raise ValueError('INVALID_ADJUDICATION_PACKET_SHAPE')
    if packet.get('packet_hash') != canonical_hash({k: v for k, v in packet.items() if k != 'packet_hash'}):
        raise ValueError('ADJUDICATION_PACKET_HASH_MISMATCH')
    if (coordinator.get('packet_hash') != packet['packet_hash']
            or canonical_hash(coordinator.get('cases')) != packet.get('seed_key_hash')
            or coordinator.get('coordinator_hash') != canonical_hash({k: v for k, v in coordinator.items() if k != 'coordinator_hash'})):
        raise ValueError('ADJUDICATION_COORDINATOR_HASH_MISMATCH')
    cases = {case['case_id']: case for case in packet['cases']}
    truth = {case['case_id']: case for case in coordinator['cases']}
    if (len(cases) != len(packet['cases']) or len(truth) != len(coordinator['cases'])
            or set(cases) != set(truth)
            or any(canonical_hash(material) != digest for digest, material in packet['materials'].items())
            or any(case['material_hash'] not in packet['materials']
                   or case['blueprint_hash'] not in packet['materials']
                   or packet['materials'][case['blueprint_hash']]['compiled_spec_hash'] != case['compiled_spec_hash']
                   for case in cases.values())):
        raise ValueError('ADJUDICATION_CASE_KEY_MISMATCH')
    if not isinstance(reviews, list):
        raise ValueError('ADJUDICATION_REVIEWS_MUST_BE_ARRAY')
    known_authors = (isinstance(author_principals, (list, tuple, set, frozenset))
                     and bool(author_principals)
                     and all(isinstance(principal, str) and principal.strip() for principal in author_principals))
    accepted, rejected, observed = defaultdict(list), [], set()
    for index, review in enumerate(reviews):
        if not isinstance(review, dict):
            rejected.append({'index': index, 'reason': 'INVALID_REVIEW_SUBJECT'})
            continue
        subject = copy.deepcopy(review)
        if not isinstance(subject.get('case_id'), str):
            rejected.append({'index': index, 'reason': ['INVALID_CASE_IDENTIFIER']})
            continue
        token = subject.pop('attestation', None)
        payload = _host_verify(trusted_executions, token)
        case = cases.get(subject.get('case_id'))
        principal = payload.get('principal') if payload else None
        failures = []
        if (not case or not isinstance(principal, str) or not principal.strip()
                or not payload.get('reviewer') is True
                or payload.get('subject_digest') != canonical_hash(subject)
                or payload.get('snapshot_digest') != case['material_hash']
                or payload.get('context_digest') != canonical_hash(subject.get('context_manifest'))):
            failures.append('UNVERIFIED_IDENTITY_OR_SUBJECT')
        if not known_authors:
            failures.append('AUTHORSHIP_UNVERIFIED')
        elif principal in author_principals:
            failures.append('SELF_REVIEW')
        assigned = (reviewer_assignments or {}).get(principal, []) if isinstance(principal, str) else []
        if case and case['domain_index'] not in assigned:
            failures.append('DOMAIN_COMPETENCE_UNASSIGNED')
        if case and (subject.get('packet_hash') != packet['packet_hash']
                     or subject.get('material_hash') != case['material_hash']
                     or subject.get('reviewed_digest') != case['material_hash']
                     or subject.get('compiled_spec_hash') != case['compiled_spec_hash']):
            failures.append('CASE_OR_SPEC_BINDING_MISMATCH')
        criteria = subject.get('criteria', [])
        if (not isinstance(criteria, list) or len(criteria) != len(RUBRIC)
                or any(not isinstance(row, dict) or not isinstance(row.get('criterion'), str)
                       or type(row.get('score')) is not int
                       or not 0 <= row['score'] <= 4
                       or not all(isinstance(row.get(key), str) and row[key].strip()
                                  for key in ('rationale', 'evidence')) for row in criteria)
                or {row['criterion'] for row in criteria} != set(RUBRIC)):
            failures.append('INCOMPLETE_CRITERION_REVIEW')
        findings = subject.get('findings', [])
        if (not isinstance(findings, list) or any(not isinstance(finding, dict)
                or finding.get('severity') not in ('critical', 'major', 'minor')
                or not isinstance(finding.get('criterion'), str) or finding['criterion'] not in RUBRIC
                or not all(isinstance(finding.get(key), str) and finding[key].strip()
                           for key in ('location', 'evidence')) for finding in findings)):
            failures.append('INVALID_LOCATED_FINDINGS')
        if subject.get('verdict') not in ('ACCEPTABLE', 'REWORK', 'INSUFFICIENT_EVIDENCE'):
            failures.append('INVALID_REVIEW_VERDICT')
        if (subject.get('verdict') == 'ACCEPTABLE'
                and isinstance(criteria, list) and isinstance(findings, list)
                and (any(isinstance(row, dict) and type(row.get('score')) is int and row['score'] < 3
                         for row in criteria)
                     or any(isinstance(finding, dict) and finding.get('severity') in ('critical', 'major')
                            for finding in findings))):
            failures.append('INCONSISTENT_ACCEPTABLE_VERDICT')
        if case and isinstance(principal, str) and (principal, case['case_id']) in observed:
            failures.append('DUPLICATE_REVIEWER_CASE')
        if failures:
            rejected.append({'index': index, 'reason': failures})
            continue
        observed.add((principal, case['case_id']))
        accepted[case['case_id']].append({'principal': principal, **subject})
    pairs, equal, seeded, detected, challenged, references = 0, 0, 0, 0, 0, 0
    dimensions = {name: {} for name in ('domains', 'outputs', 'complexities')}
    for ident, case in cases.items():
        observations = accepted[ident]
        pair_complete = len(observations) >= 2
        for left, right in itertools.combinations(observations, 2):
            pairs += 1
            equal += int(left['verdict'] == right['verdict'])
        if truth[ident]['seed_class'] == 'seeded-defect':
            seeded += len(observations)
            detected += sum(review['verdict'] == 'REWORK' and any(
                finding['severity'] == 'critical'
                and finding['criterion'] == truth[ident]['expected_criterion']
                for finding in review['findings']) for review in observations)
        else:
            references += len(observations)
            challenged += sum(review['verdict'] != 'ACCEPTABLE' for review in observations)
        for name, key in (('domains', str(case['domain_index'])),
                          ('outputs', case['contract_id']), ('complexities', case['complexity'])):
            row = dimensions[name].setdefault(key, {'expected_cases': 0, 'independently_reviewed_cases': 0})
            row['expected_cases'] += 1
            row['independently_reviewed_cases'] += int(pair_complete)
    for dimension in dimensions.values():
        for row in dimension.values():
            row['independent_pair_complete'] = row['expected_cases'] == row['independently_reviewed_cases']
    report = {'schema_version': '1.0.0', 'packet_hash': packet['packet_hash'],
              'verified_review_count': sum(map(len, accepted.values())),
              'rejected_reviews': rejected, 'coverage': dimensions,
              'seeded_critical_recall': detected / seeded if seeded else None,
              'pairwise_agreement': equal / pairs if pairs else None,
              'reference_challenge_rate': challenged / references if references else None,
              'false_positive_rate': None,
              'false_positive_limitation': 'References are not human-adjudicated gold; disagreement is not automatically a reviewer error.',
              'status': 'MEASURED' if accepted and all(row['independent_pair_complete']
                  for dimension in dimensions.values() for row in dimension.values()) else 'PENDING_INDEPENDENT_REVIEW',
              'human_gold': False, 'professional_approval': False, 'production_ready': False,
              'authority': 'Existing JAI human authority only; this report grants none.'}
    report['report_hash'] = canonical_hash(report)
    return report
