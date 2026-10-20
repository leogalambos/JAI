#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Proposal authoring inside commercial-delivery/1, never an approval engine.

Working inputs are not a new canonical store. Existing commercial snapshots,
DCS, publication projection and JAI authority remain the controlled handoff.
Reference documents supply structure only; no reference scenario is copied into
an actual proposal. Missing project information is retained explicitly as OPEN.
"""
from __future__ import annotations

import copy
from decimal import Decimal, InvalidOperation
import json
import hashlib
import os
from pathlib import Path
import re

import commercial_core as core
import commercial_economics as economics

CORE_KINDS = ('client-proposal', 'executive-proposal', 'technical-proposal',
              'delivery-proposal', 'commercial-proposal', 'statement-of-work',
              'rfp-response', 'proposal-compliance-matrix')
OPTIONAL_KINDS = ('cybersecurity-transformation-proposal', 'managed-security-services-proposal')
ROOT = Path(__file__).resolve().parents[1]
TITLES = {kind: kind.replace('-', ' ').title() for kind in CORE_KINDS + OPTIONAL_KINDS}


def _decimal(value):
    if not isinstance(value, str):
        raise ValueError('decimal string required')
    try:
        number = Decimal(value)
    except InvalidOperation:
        raise ValueError('decimal string required') from None
    if not number.is_finite() or number < 0:
        raise ValueError('finite nonnegative decimal required')
    return number


def _digest(value):
    return core.digest(value)


def _text(value):
    if value is None or value == '' or value == []:
        return 'OPEN — authorized project input and accountable owner required.'
    if isinstance(value, dict):
        body = value.get('text', value.get('description', value.get('summary', '')))
        status = value.get('knowledge_status', 'pending')
        return (str(body) if body else 'OPEN — project input required.') + ' [Knowledge: ' + status + ']'
    if isinstance(value, list):
        return '; '.join(_text(item) for item in value)
    return str(value).replace('\x00', '')


def _findings():
    return []


def _add(findings, rule, location, severity='critical', message=None):
    findings.append({'rule_id': rule, 'location': location, 'severity': severity,
                     'blocking': severity == 'critical',
                     'message': message or 'Resolve the inconsistent or missing proposal input.'})


def _index(records, findings, location):
    result = {}
    for index, record in enumerate(records):
        identifier = record.get('id') if isinstance(record, dict) else None
        if not isinstance(identifier, str) or not identifier or identifier in result:
            _add(findings, 'proposal.identity.invalid_or_duplicate', f'{location}[{index}]')
        else:
            result[identifier] = record
    return result


def validate_package(data, evidence_verifier=None):
    """Check cross-document obligations and exact decimal commercial reconciliation.

    Args:
        data: proposal-authoring-input/1 JSON object; customer statements remain
            reported inputs, never implicitly verified facts or approval.
        evidence_verifier: Optional trusted host callback taking an evidence
            record; COMPLY requires verified observation through this callback.
            JSON flags cannot replace the callback or JAI approval.
    Returns:
        Sanitized located findings and consistency status, separate from always
        false authority/release flags. Missing material inputs are non-passing.
    Raises:
        ValueError: If the input is not a supported JSON authoring object.
    """
    if not isinstance(data, dict) or data.get('package_kind') != 'proposal-authoring-input/1':
        raise ValueError('proposal-authoring-input/1 object required')
    import jsonschema
    schema = json.loads((ROOT / 'commercial/schema/proposal-authoring.schema.json').read_text())
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(data))
    findings = _findings()
    for error in errors:
        location = '.'.join(str(part) if isinstance(part, int) else str(part) if part in schema.get('properties', {}) else 'field' for part in error.absolute_path)
        _add(findings, 'proposal.input.schema', location or 'input', message='Authoring input does not satisfy the registered working-input schema.')
    if errors:
        return _report(findings)
    from content_spec import ContentSpec
    from content_lint import evaluate
    spec = ContentSpec(ROOT).resolve('kind/client-proposal', data.get('dcs_context', {}))
    policy_probe = {'compiled_spec_hash': spec['compiled_spec_hash'],
                    'context': data.get('dcs_context', {}), 'semantic_units': {},
                    'proposal_authoring_input': data}
    if any(item['rule_id'] == 'global.secret_disclosure' and item.get('blocking') for item in evaluate(policy_probe, spec)['findings']):
        _add(findings, 'global.secret_disclosure', 'input', message='Existing security policy detected credential-like material; values and identifying locations are redacted.')
    sources = _index(data['sources'], findings, 'sources')
    deliverables = _index(data['deliverables'], findings, 'deliverables')
    acceptance = _index(data['acceptance'], findings, 'acceptance')
    dependencies = _index(data['dependencies'], findings, 'dependencies')
    requirements = _index(data['rfp_requirements'], findings, 'rfp_requirements')
    evidence = _index(data['evidence'], findings, 'evidence')
    milestones = _index(data['milestones'], findings, 'milestones')
    for field in ('sources', 'deliverables', 'acceptance', 'milestones', 'assumptions', 'exclusions', 'responsibilities'):
        if not data[field]:
            _add(findings, 'proposal.material_input.missing', field)
    for field in ('situation', 'objectives', 'technical_approach', 'delivery_approach', 'decision_request', 'risks'):
        entry = data['narrative'].get(field)
        if not entry or not entry.get('text') or entry.get('knowledge_status') in ('unknown', 'pending'):
            _add(findings, 'proposal.narrative.open', 'narrative.' + field)
    def refs(values, known, location):
        if not values or any(value not in known for value in values):
            _add(findings, 'proposal.traceability.missing_or_unknown', location)
    if data['classification'] == 'public-synthetic' and any(item['classification'] != 'public-synthetic' or item['provenance'] != 'synthetic' for item in data['sources']):
        _add(findings, 'proposal.classification.synthetic_source_conflict', 'sources')
    for field, item in data['narrative'].items():
        if item.get('text') and item.get('knowledge_status') not in ('unknown', 'pending'):
            refs(item['source_ids'], sources, 'narrative.' + field + '.source_ids')
        if re.search(r'\b(certified|guaranteed|fully compliant|tested and passed)\b', item.get('text', ''), re.I) and not re.search(r'\b(not|unverified|pending|proposed|hypothetical)\b', item.get('text', ''), re.I):
            _add(findings, 'proposal.claim.unsupported_assurance', 'narrative.' + field)
    for group in ('dependencies', 'evidence'):
        for index, item in enumerate(data[group]):
            refs(item['source_ids'], sources, f'{group}[{index}].source_ids')
    refs(data['pricing']['source_ids'], sources, 'pricing.source_ids')
    for index, item in enumerate(data['deliverables']):
        refs(item['source_ids'], sources, f'deliverables[{index}].source_ids')
        if item['acceptance_id'] not in acceptance or item['id'] not in acceptance.get(item['acceptance_id'], {}).get('deliverable_ids', []):
            _add(findings, 'proposal.acceptance.missing', f'deliverables[{index}].acceptance_id')
    declared_scope = data['scope']['deliverable_ids']
    if set(declared_scope) != set(deliverables) or len(declared_scope) != len(set(declared_scope)):
        _add(findings, 'proposal.scope.deliverables_mismatch', 'scope.deliverable_ids')
    for group in ('technical_commitments', 'delivery_commitments'):
        if not data[group]:
            _add(findings, 'proposal.commitment.missing', group)
        _index(data[group], findings, group)
        for index, item in enumerate(data[group]):
            refs(item['deliverable_ids'], deliverables, f'{group}[{index}].deliverable_ids')
            refs(item['source_ids'], sources, f'{group}[{index}].source_ids')
            if item['knowledge_status'] in ('unknown', 'pending'):
                _add(findings, 'proposal.commitment.open', f'{group}[{index}]')
    for index, item in enumerate(data['acceptance']):
        refs(item['deliverable_ids'], deliverables, f'acceptance[{index}].deliverable_ids')
        if item['status'] not in ('PROPOSED', 'NOT_EXECUTED'):
            _add(findings, 'proposal.acceptance.unverified_execution', f'acceptance[{index}].status')
    for index, item in enumerate(data['milestones']):
        refs(item['deliverable_ids'], deliverables, f'milestones[{index}].deliverable_ids')
        refs(item['acceptance_ids'], acceptance, f'milestones[{index}].acceptance_ids')
        accepted_deliverables = {key for aid in item['acceptance_ids'] for key in acceptance.get(aid, {}).get('deliverable_ids', [])}
        if not set(item['deliverable_ids']) <= accepted_deliverables:
            _add(findings, 'proposal.acceptance.milestone_mismatch', f'milestones[{index}].acceptance_ids')
        if item['end_day'] < item['start_day']:
            _add(findings, 'proposal.schedule.inverted', f'milestones[{index}]')
        for dependency in item['dependency_ids']:
            if dependency not in dependencies or dependencies[dependency]['required_by_day'] > item['start_day']:
                _add(findings, 'proposal.schedule.dependency_after_start', f'milestones[{index}].dependency_ids')
        for predecessor in item.get('predecessor_ids', []):
            if predecessor not in milestones or milestones[predecessor]['end_day'] > item['start_day']:
                _add(findings, 'proposal.schedule.predecessor_not_complete', f'milestones[{index}].predecessor_ids')
    covered = {item for milestone in data['milestones'] for item in milestone['deliverable_ids']}
    if covered != set(deliverables):
        _add(findings, 'proposal.schedule.deliverable_coverage', 'milestones')
    for group in ('assumptions', 'responsibilities'):
        for index, item in enumerate(data[group]):
            refs(item['source_ids'], sources, f'{group}[{index}].source_ids')
    if {key for item in data['responsibilities'] for key in item['deliverable_ids']} != set(deliverables):
        _add(findings, 'proposal.responsibility.deliverable_coverage', 'responsibilities')
    for index, item in enumerate(data['responsibilities']):
        refs(item['deliverable_ids'], deliverables, f'responsibilities[{index}].deliverable_ids')
    answers = {}
    for index, answer in enumerate(data['rfp_answers']):
        identifier = answer['requirement_id']
        if identifier in answers or identifier not in requirements:
            _add(findings, 'proposal.rfp.unknown_or_duplicate', f'rfp_answers[{index}]')
        answers[identifier] = answer
        refs(answer['deliverable_ids'], deliverables, f'rfp_answers[{index}].deliverable_ids')
        if answer['status'] == 'CONDITIONAL' and not answer['conditions']:
            _add(findings, 'proposal.rfp.condition_missing', f'rfp_answers[{index}]')
        if answer['status'] == 'COMPLY':
            observed = [evidence.get(identifier) for identifier in answer['evidence_ids']]
            if not observed or any(record is None or record['status'] != 'OBSERVED' or evidence_verifier is None or evidence_verifier(record) is not True for record in observed):
                _add(findings, 'proposal.rfp.unverified_comply', f'rfp_answers[{index}]')
        if any(identifier not in evidence for identifier in answer['evidence_ids']):
            _add(findings, 'proposal.rfp.evidence_missing', f'rfp_answers[{index}].evidence_ids')
    for index, requirement in enumerate(data['rfp_requirements']):
        refs(requirement['source_ids'], sources, f'rfp_requirements[{index}].source_ids')
        if requirement['id'] not in answers:
            _add(findings, 'proposal.rfp.unanswered', f'rfp_requirements[{index}]')
        elif requirement['mandatory'] and answers[requirement['id']]['status'] in ('DEVIATION', 'NOT_EVIDENCED'):
            _add(findings, 'proposal.rfp.mandatory_unresolved', f'rfp_requirements[{index}]')
    price = data['pricing']
    try:
        currency = price['currency']
        if any(line['currency'] != currency for line in price['labour']):
            _add(findings, 'proposal.pricing.currency_mismatch', 'pricing.labour')
        totals = []
        for index, line in enumerate(price['labour']):
            refs(line['deliverable_ids'], deliverables, f'pricing.labour[{index}].deliverable_ids')
            expected = _decimal(line['days']) * _decimal(line['day_rate'])
            if expected != _decimal(line['line_total']):
                _add(findings, 'proposal.pricing.day_rate_mismatch', f'pricing.labour[{index}]')
            totals.append(expected)
        # The existing calculator controls currency/rounding and invoice-line
        # aggregation. Selling day rates are not relabelled as internal cost rates.
        quote = economics.price_quote({'currency': currency, 'input_versions': ['proposal-working-input'],
            'valid_until': price['valid_until'], 'author': 'draft-pricing-author',
            'reviewer': 'unverified-independent-review-required', 'target_margin': '0',
            'invoice_lines': [{'list_price': str(amount)} for amount in totals]})
        if _decimal(quote['net_price']) != _decimal(price['supplier_fee']):
            _add(findings, 'proposal.pricing.supplier_fee_mismatch', 'pricing.supplier_fee')
        programme = _decimal(price['supplier_fee']) + _decimal(price['third_party']) + _decimal(price['customer_internal'])
        if programme != _decimal(price['programme_total']):
            _add(findings, 'proposal.pricing.programme_total_mismatch', 'pricing.programme_total')
        percentages = sum((_decimal(item['payment_percent']) for item in data['milestones']), Decimal('0'))
        payments = sum((_decimal(item['payment_amount']) for item in data['milestones']), Decimal('0'))
        if percentages != Decimal('100') or payments != _decimal(price['supplier_fee']):
            _add(findings, 'proposal.pricing.milestone_total_mismatch', 'milestones')
        for index, milestone in enumerate(data['milestones']):
            if _decimal(milestone['payment_amount']) != (_decimal(price['supplier_fee']) * _decimal(milestone['payment_percent']) / Decimal('100')).quantize(Decimal('.01')):
                _add(findings, 'proposal.pricing.milestone_amount_mismatch', f'milestones[{index}]')
        for index, offering in enumerate(data['optional_offerings']):
            if offering['kind'] not in OPTIONAL_KINDS or offering['included_in_base'] is not False:
                _add(findings, 'proposal.optional.base_scope_conflict', f'optional_offerings[{index}]')
            _decimal(offering['fee'])
            refs(offering['source_ids'], sources, f'optional_offerings[{index}].source_ids')
            if offering['selected'] and any(not offering.get(field) for field in ('service_boundary', 'service_hours', 'response_clock', 'decision_rights', 'acceptance_criteria', 'exclusions')):
                _add(findings, 'proposal.optional.own_boundaries_open', f'optional_offerings[{index}]')
            if offering['currency'] != currency:
                _add(findings, 'proposal.optional.currency_mismatch', f'optional_offerings[{index}]')
    except (ValueError, KeyError, TypeError):
        _add(findings, 'proposal.pricing.invalid_decimal_or_policy', 'pricing')
    supplied_documents = data.get('documents', {})
    if supplied_documents and set(supplied_documents) != set(_selection(data)):
        _add(findings, 'proposal.document.package_membership', 'documents')
    for index, (kind, document) in enumerate(supplied_documents.items()):
        document = dict(document, kind=kind)
        if document['kind'] not in CORE_KINDS + OPTIONAL_KINDS:
            _add(findings, 'proposal.document.unknown_kind', f'document_assertions[{index}]')
        for field, expected in _claims(data).items():
            observed = document.get(field)
            if field == 'deliverable_ids' and isinstance(observed, list):
                observed = sorted(observed)
            if field not in document or observed != expected:
                _add(findings, 'proposal.document.inconsistent_' + field, f'documents[{index}].{field}')
    return _report(findings)


def _report(findings):
    return {'profile': core.PROFILE, 'capability': 'proposal-authoring',
            'consistency_pass': not any(item['blocking'] for item in findings),
            'status': 'CONSISTENT_DRAFT' if not findings else 'OPEN_OR_INCONSISTENT_DRAFT',
            'findings': findings, 'professional_acceptance': 'NOT_APPROVED',
            'authority_granted': False, 'release_ready': False,
            'execution_evidence': 'NOT_EXECUTED',
            'limitations': ['Consistency is not professional, legal, contractual or JAI approval.',
                           'Supplied inputs remain reported or assumed until independently verified.']}


def _selection(data):
    kinds = list(CORE_KINDS)
    kinds.extend(item['kind'] for item in data.get('optional_offerings', []) if item.get('selected'))
    if len(kinds) != len(set(kinds)):
        raise ValueError('duplicate optional offering selection')
    return kinds


def plan_package(data, root=ROOT, user_root=None, organisation_root=None, engagement_root=None):
    """Resolve the linked package references deterministically without copying their facts.

    Args:
        data: Working authoring input.
        root: Existing DCS/runtime root.
        user_root, organisation_root, engagement_root: Optional existing reference
            override roots with unchanged fail-closed precedence.
    Returns:
        Sanitized reference selection and consistency results; no private paths.
    Raises:
        ValueError: For invalid inputs, ambiguous or invalid selected references.
    """
    from expert_references import ExpertReferences
    report = validate_package(data)
    resolver = ExpertReferences(root)
    selections = []
    for kind in _selection(data):
        _, selection = resolver.resolve(kind, data['complexity'], user_root=user_root,
            organisation_root=organisation_root, engagement_root=engagement_root,
            context=data.get('selection_context', {}), audience=data['audience'])
        selections.append({'kind': kind, 'complexity': data['complexity'], 'selection': selection})
    return {'profile': core.PROFILE, 'capability': 'proposal-authoring', 'documents': selections,
            'consistency': report, 'authority_granted': False, 'release_ready': False}


def _money(value, currency):
    if value is None:
        return 'OPEN — price input required'
    number = _decimal(value)
    result = format(number, ',f')
    if '.' not in result:
        result += '.00'
    elif len(result.rsplit('.', 1)[1]) < 2:
        result += '0'
    return currency + ' ' + result


def _table(headers, rows):
    def cell(value):
        return _text(value).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |',
                      *['| ' + ' | '.join(cell(value) for value in row) + ' |' for row in rows]])


def _sections(data, kind):
    narrative = data['narrative']
    price = data['pricing']
    scope = _text(data['scope']['description'])
    deliverables = _table(['ID', 'Deliverable and scope', 'Owner', 'Acceptance'],
        [(item['id'], item['title'] + ': ' + item['description'], item['owner'], item['acceptance_id']) for item in data['deliverables']])
    schedule = _table(['Milestone', 'Days', 'Deliverables', 'Dependencies', 'Acceptance'],
        [(item['id'], str(item['start_day']) + '–' + str(item['end_day']), ', '.join(item['deliverable_ids']), ', '.join(item['dependency_ids']), ', '.join(item['acceptance_ids'])) for item in data['milestones']])
    pricing = _table(['Workstream', 'Person-days', 'Sell rate/day', 'Supplier fee'],
        [(line['id'], line['days'], _money(line['day_rate'], price['currency']), _money(line['line_total'], price['currency'])) for line in price['labour']])
    totals = (f"Supplier services {_money(price['supplier_fee'], price['currency'])}; third-party estimate {_money(price['third_party'], price['currency'])}; "
        f"customer internal estimate {_money(price['customer_internal'], price['currency'])}; programme envelope {_money(price['programme_total'], price['currency'])} over {price['period_months']} months. "
        f"Third-party and customer costs are not supplier invoices. Taxes: {price['taxes'].rstrip('.')}. Quote basis valid until {price['valid_until']}, subject to authorized review.")
    payments = _table(['Milestone', 'Percent of supplier services', 'Amount', 'Acceptance prerequisite'],
        [(item['id'], item['payment_percent'], _money(item['payment_amount'], price['currency']), ', '.join(item['acceptance_ids'])) for item in data['milestones']])
    acceptance = _table(['ID', 'Deliverables', 'Acceptance evidence', 'Recipient', 'Rejection path', 'Status'],
        [(item['id'], ', '.join(item['deliverable_ids']), item['criteria'] + '; evidence: ' + item['evidence_expected'], item['recipient'], item['rejection_path'], item['status']) for item in data['acceptance']])
    assumptions = _table(['ID', 'Assumption', 'Owner', 'Validation gate'], [(item['id'], item['text'], item['owner'], item['validation_gate']) for item in data['assumptions']])
    responsibilities = _table(['Party', 'Responsibility', 'Deliverables'], [(item['party'], item['description'], ', '.join(item['deliverable_ids'])) for item in data['responsibilities']])
    exclusions = '\n'.join('- ' + item for item in data['exclusions']) or 'OPEN — exclusions require agreement.'
    technical = '\n'.join('- ' + item['description'] + ' [Deliverables: ' + ', '.join(item['deliverable_ids']) + '; ' + item['knowledge_status'] + ']' for item in data['technical_commitments'])
    delivery = '\n'.join('- ' + item['description'] + ' [Deliverables: ' + ', '.join(item['deliverable_ids']) + '; ' + item['knowledge_status'] + ']' for item in data['delivery_commitments'])
    dependency = _table(['ID', 'Prerequisite', 'Owner', 'Required by day'], [(item['id'], item['description'], item['owner'], item['required_by_day']) for item in data['dependencies']])
    answers = {item['requirement_id']: item for item in data['rfp_answers']}
    rfp = _table(['Requirement', 'Customer question', 'Response', 'Status', 'Evidence', 'Conditions', 'Deliverables'],
        [(item['id'], item['text'], answers.get(item['id'], {}).get('response', 'OPEN — unanswered'), answers.get(item['id'], {}).get('status', 'NOT_EVIDENCED'),
          ', '.join(answers.get(item['id'], {}).get('evidence_ids', [])) or 'NOT_EXECUTED', '; '.join(answers.get(item['id'], {}).get('conditions', [])) or 'None recorded',
          ', '.join(answers.get(item['id'], {}).get('deliverable_ids', []))) for item in data['rfp_requirements']])
    optionals = '\n'.join(f"- {TITLES[item['kind']]}: {_money(item['fee'], item['currency'])} ({item['period']}); separate optional scope, excluded from every base total. {_text(item['scope'])}" for item in data['optional_offerings'])
    common = {'Decision and next authorization': _text(narrative.get('decision_request')),
      'Customer situation and evidence limits': _text(narrative.get('situation')),
      'Objectives and value hypothesis': _text(narrative.get('objectives')) + '\n\n' + _text(narrative.get('value_hypothesis')),
      'Scope and deliverables': scope + '\n\n' + deliverables,
      'Technical approach and commitments': _text(narrative.get('technical_approach')) + '\n\n' + technical,
      'Security, privacy and compliance constraints': _text(narrative.get('security_constraints')),
      'Delivery approach and commitments': _text(narrative.get('delivery_approach')) + '\n\n' + delivery,
      'Schedule and prerequisites': schedule + '\n\n' + dependency,
      'Effort and supplier fee': pricing,
      'Programme cost and commercial basis': totals,
      'Payment milestones': payments,
      'Acceptance and receiving authority': acceptance,
      'Assumptions and validation gates': assumptions,
      'Exclusions': exclusions, 'Responsibilities': responsibilities,
      'Risks, alternatives and unresolved decisions': _text(narrative.get('risks')) + '\n\n' + _text(narrative.get('alternatives')),
      'RFP response and compliance traceability': rfp,
      'Separate optional offerings': optionals or 'No optional offerings selected; none included in the base programme.',
      'Contractual and legal boundary': 'Negotiation draft only. ' + _text(narrative.get('contract_terms')) + '\n\nOPEN — competent legal and commercial owners must review change control, liability, IP/data, validity, exit and signatures. No binding guarantee, execution result or approval is granted.'}
    selected = {
      'client-proposal': ['Decision and next authorization','Customer situation and evidence limits','Objectives and value hypothesis','Scope and deliverables','Technical approach and commitments','Schedule and prerequisites','Programme cost and commercial basis','Assumptions and validation gates','Risks, alternatives and unresolved decisions','Separate optional offerings'],
      'executive-proposal': ['Decision and next authorization','Customer situation and evidence limits','Objectives and value hypothesis','Programme cost and commercial basis','Risks, alternatives and unresolved decisions','Assumptions and validation gates'],
      'technical-proposal': ['Customer situation and evidence limits','Technical approach and commitments','Scope and deliverables','Security, privacy and compliance constraints','Schedule and prerequisites','Acceptance and receiving authority','Risks, alternatives and unresolved decisions'],
      'delivery-proposal': ['Scope and deliverables','Delivery approach and commitments','Effort and supplier fee','Schedule and prerequisites','Responsibilities','Acceptance and receiving authority','Assumptions and validation gates','Exclusions'],
      'commercial-proposal': ['Programme cost and commercial basis','Effort and supplier fee','Payment milestones','Assumptions and validation gates','Exclusions','Separate optional offerings','Contractual and legal boundary'],
      'statement-of-work': ['Scope and deliverables','Delivery approach and commitments','Schedule and prerequisites','Responsibilities','Acceptance and receiving authority','Programme cost and commercial basis','Payment milestones','Assumptions and validation gates','Exclusions','Contractual and legal boundary'],
      'rfp-response': ['Customer situation and evidence limits','RFP response and compliance traceability','Technical approach and commitments','Assumptions and validation gates','Exclusions'],
      'proposal-compliance-matrix': ['RFP response and compliance traceability','Scope and deliverables','Acceptance and receiving authority','Security, privacy and compliance constraints','Risks, alternatives and unresolved decisions']}
    if kind in OPTIONAL_KINDS:
        offering = next(item for item in data['optional_offerings'] if item['kind'] == kind)
        return [{'heading': 'Separate optional offering and authorization boundary', 'body': _text(offering['scope']) + f"\n\n{_money(offering['fee'], offering['currency'])} ({offering['period']}); excluded from base supplier services and programme totals. Separate authorized scope change and acceptance are required."},
                {'heading': 'Own service and control boundary', 'body': _text(offering.get('service_boundary'))},
                {'heading': 'Hours, response clock and decision rights', 'body': _text(offering.get('service_hours')) + '\n\n' + _text(offering.get('response_clock')) + '\n\n' + _text(offering.get('decision_rights'))},
                {'heading': 'Separate acceptance and exclusions', 'body': _text(offering.get('acceptance_criteria')) + '\n\n' + _text(offering.get('exclusions')) + '\n\nBase-programme acceptance records do not accept this separate optional offering.'},
                {'heading': 'Contractual and legal boundary', 'body': common['Contractual and legal boundary']} ]
    return [{'heading': heading, 'body': common[heading]} for heading in selected[kind]]


def _claims(data):
    result = {key: copy.deepcopy(data[key]) for key in ('technical_commitments',
        'delivery_commitments', 'milestones', 'dependencies', 'acceptance',
        'assumptions', 'exclusions', 'responsibilities', 'rfp_requirements', 'rfp_answers')}
    result.update({key: data['pricing'][key] for key in ('supplier_fee', 'programme_total', 'currency')})
    result['deliverable_ids'] = sorted(item['id'] for item in data['deliverables'])
    result['scope'] = copy.deepcopy(data['scope'])
    result['deliverables'] = copy.deepcopy(data['deliverables'])
    result['pricing'] = copy.deepcopy(data['pricing'])
    result['source_versions'] = {item['id']: item['version'] for item in data['sources']}
    result['optional_offerings'] = [{key: copy.deepcopy(value) for key, value in item.items() if key != 'selected'} for item in data['optional_offerings']]
    return result


def _unit_value(field, datatype, data, sections):
    material = {'scope': data['scope'], 'deliverables': data['deliverables'], 'pricing': data['pricing'],
        'cost_breakdown': data['pricing'], 'price_basis': data['pricing'], 'payment_terms': data['milestones'],
        'schedule_dependencies': data['milestones'], 'work_packages': data['deliverables'],
        'resources_governance': data['responsibilities'], 'delivery_scope': data['scope'],
        'assumptions_exclusions': {'assumptions': data['assumptions'], 'exclusions': data['exclusions']},
        'acceptance': data['acceptance'], 'requirements': data['rfp_requirements'],
        'rfp_responses': data['rfp_answers']}
    narrative = data['narrative']
    def note(name):
        value = narrative.get(name, {})
        return {'text': _text(value), 'source_ids': value.get('source_ids', []),
                'knowledge_status': 'unknown' if value.get('knowledge_status') in (None, 'unknown', 'pending') else 'assumption'}
    material.update({'customer_need': note('situation'), 'proposed_solution': note('technical_approach'),
      'scope_deliverables': data['deliverables'], 'delivery_plan': {'milestones': data['milestones'], 'approach': note('delivery_approach')},
      'commercial_overview': data['pricing'], 'decision_request': note('decision_request'),
      'executive_ask': note('decision_request'), 'business_case': note('value_hypothesis'),
      'solution_value': note('objectives'), 'alternatives': note('alternatives'),
      'risk_dependencies': {'risks': note('risks'), 'dependencies': data['dependencies']}, 'next_decision': note('decision_request'),
      'architecture_context': note('situation'), 'solution_design': note('technical_approach'),
      'interfaces_security': note('security_constraints'), 'nonfunctional_requirements': data['technical_commitments'],
      'verification_strategy': data['acceptance'], 'technical_assumptions': data['assumptions'],
      'cost_breakdown': data['pricing']['labour'], 'commercial_risks': note('risks'),
      'approval_boundary': {'text': 'OPEN — independent commercial, legal and existing JAI authority approval required; no approval or signature supplied.'},
      'quality_acceptance': data['acceptance'], 'transition_controls': note('delivery_approach'),
      'parties_scope': data['scope'], 'responsibilities': data['responsibilities'],
      'milestones_acceptance': data['milestones'], 'commercial_change': data['pricing'],
      'legal_reservations': note('contract_terms'), 'response_context': note('situation'),
      'requirement_mapping': data['rfp_answers'], 'solution_response': note('technical_approach'),
      'compliance_qualification': {'text': 'Responses remain proposed/conditional; no implied certification, executed testing or independent approval.'},
      'commercial_schedules': data['milestones'], 'clarifications': data['assumptions'],
      'requirement_source': {'requirements': data['rfp_requirements'], 'sources': data['sources']},
      'response_classification': data['rfp_answers'], 'evidence_mapping': data['evidence'],
      'exceptions_dependencies': data['dependencies'], 'closure_governance': data['responsibilities'],
      'identity': {'id': data['package_id'], 'classification': data['classification'], 'status': 'DRAFT_NOT_FOR_SUBMISSION'}})
    if field in material:
        value = copy.deepcopy(material[field])
        if datatype == 'array':
            values = value if isinstance(value, list) else [value]
            return [dict(item, knowledge_status=item.get('knowledge_status') if item.get('knowledge_status') in ('unknown', 'pending') else 'assumption') if isinstance(item, dict) else {'text': str(item), 'knowledge_status': 'assumption'} for item in values]
        if datatype == 'object':
            return dict(value, knowledge_status=value.get('knowledge_status') if value.get('knowledge_status') in ('unknown', 'pending') else 'assumption') if isinstance(value, dict) else {'items': value, 'knowledge_status': 'assumption'}
        if datatype == 'string':
            return _text(value)
    unknown = {'knowledge_status': 'unknown', 'text': 'OPEN — this required DCS unit needs authorized project input and independent review.', 'owner': 'Unassigned; contracting owner must nominate.'}
    return [unknown] if datatype == 'array' else unknown if datatype == 'object' else 'OPEN — authorized project input required.' if datatype == 'string' else None


def _semantic_model(data, kind, resolver):
    contract_id = 'kind/' + kind
    spec = resolver.resolve(contract_id, data.get('dcs_context', {}))
    sections = _sections(data, kind)
    semantic = {'artifact_id': data['package_id'] + ':' + kind, 'contract_id': contract_id,
        'document_kind': kind, 'compiled_spec_hash': spec['compiled_spec_hash'], 'context': data.get('dcs_context', {}),
        'title': TITLES[kind], 'owner': data.get('proposed_owner', 'OPEN — contracting owner must nominate accountable owner'),
        'classification': data['classification'], 'status': 'DRAFT_NOT_FOR_SUBMISSION',
        'summary': 'Draft from explicitly supplied inputs; not verified customer evidence or an offer.',
        'semantic_units': {}, 'sections': sections,
        'claims': [{'id': 'reported-proposal-input', 'statement': _text(data['narrative'].get('situation')),
                    'knowledge_status': 'assumption', 'evidence': [item['id'] for item in data['sources']]}],
        'evidence': [{'id': item['id'], 'version': item['version'], 'payload': copy.deepcopy(item),
                      'hash': _digest(item), 'status': 'REPORTED_INPUT_NOT_EXECUTION'} for item in data['sources']],
        'proposal_claims': _claims(data),
        'risks': [{'description': _text(data['narrative'].get('risks')), 'knowledge_status': 'assumption'}],
        'decisions': [{'description': _text(data['narrative'].get('decision_request')), 'knowledge_status': 'pending'}],
        'approvals': [{'status': 'PENDING_EXISTING_JAI_AUTHORITY'}]}
    for unit in spec['blueprint']['semantic_units']:
        if unit.get('category') not in ('required_information', 'conditional_information', 'optional_information') or unit.get('applicability') is False:
            continue
        for field in unit.get('semantic_fields', []):
            if '.' not in field:
                semantic['semantic_units'][field] = _unit_value(field, unit['datatype'], data, sections)
    aliases = {
        'Decision required': _text(data['narrative'].get('decision_request')),
        'Context': _text(data['narrative'].get('situation')),
        'Options considered': _text(data['narrative'].get('alternatives')),
        'Recommendation and rationale': _text(data['narrative'].get('technical_approach')),
        'Risks and mitigations': _text(data['narrative'].get('risks')),
        'Decision record': 'DRAFT — authorization pending; no approval recorded.'}
    semantic['sections'] = [{'heading': name, 'body': body} for name, body in aliases.items()] + copy.deepcopy(sections)
    semantic['publication_profile'] = 'decision-paper'
    return semantic, spec, sections


def _markdown(data, kind, sections):
    markdown = '# ' + TITLES[kind] + '\n\n**DRAFT — NOT FOR SUBMISSION. NOT AN OFFER. NO PROFESSIONAL OR JAI APPROVAL.**\n\n'
    markdown += '**Document control:** Package `' + data['package_id'] + '` · Revision `' + data.get('revision', 'working-draft-1') + '` · Audience: ' + data['audience'] + ' · Classification: ' + data['classification'] + ' · Proposed owner: ' + data.get('proposed_owner', 'OPEN — nomination required') + '.\n\n'
    markdown += ('**PUBLIC SYNTHETIC EXAMPLE — no customer facts or executed tests are established.**\n\n' if data['classification'] == 'public-synthetic' else '**PRIVATE WORKING DRAFT — authorized local use only.**\n\n')
    markdown += '\n\n'.join('## ' + section['heading'] + '\n\n' + section['body'] for section in sections)
    markdown += '\n\n## Reported input basis\n\n' + _table(['Source', 'Version', 'Provenance', 'Limitation'], [(item['id'], item['version'], item['provenance'], item['summary']) for item in data['sources']])
    markdown += '\n\n## Evidence and approval limitations\n\nAll inputs remain reported or assumed. Evidence status is NOT_EXECUTED unless separately verified by the trusted host. Open DCS units require authoring and independent review. Existing security, legal, commercial and JAI authority gates remain mandatory.\n'
    return markdown


def prepare_package(data, output, root=ROOT, **overrides):
    """Write a linked draft Markdown/semantic pack from explicit working inputs.

    Args:
        data: Validly shaped working input; unresolved material issues remain OPEN.
        output: New empty output directory. Existing files are never overwritten.
        root: Registered shared DCS and reference runtime root.
        **overrides: Existing reference resolver root keyword arguments.
    Returns:
        Sanitized drafting result with document counts and separate consistency
        status. No output is approved, released or offered as executed evidence.
    Raises:
        ValueError, OSError: For invalid references, unsafe IDs or output collisions.
    """
    from content_spec import ContentSpec
    from content_lint import evaluate
    plan = plan_package(data, root, **overrides)
    if any(item['rule_id'] == 'proposal.input.schema' for item in plan['consistency']['findings']):
        raise ValueError('validly shaped working inputs required for draft preparation')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', data['package_id']):
        raise ValueError('safe package identifier required')
    target = Path(output)
    if target.is_symlink() or (target.exists() and any(target.iterdir())):
        raise ValueError('new empty draft output directory required')
    resolver = ContentSpec(root)
    payloads = {'proposal-authoring-input.json': copy.deepcopy(data), 'proposal-consistency.json': plan['consistency']}
    records = []
    for kind in _selection(data):
        semantic, spec, sections = _semantic_model(data, kind, resolver)
        contract_id = semantic['contract_id']
        qa = evaluate(semantic, spec)
        if any(finding.get('blocking') for finding in qa['findings']):
            raise ValueError('existing security or governance content blocker; draft output forbidden')
        markdown = _markdown(data, kind, sections)
        payloads[kind + '.md'] = markdown
        payloads[kind + '.semantic.json'] = semantic
        payloads[kind + '.content-qa.json'] = qa
        records.append({'kind': kind, 'contract_id': contract_id, 'semantic_ref': kind + '.semantic.json',
                        'markdown_ref': kind + '.md', 'content_status': qa['gate_verdict'],
                        'semantic_hash': _digest(semantic), 'markdown_hash': hashlib.sha256(markdown.encode()).hexdigest()})
    payloads['proposal-package.json'] = {'package_kind': 'proposal-prepared-draft/1', 'profile': core.PROFILE, 'status': 'DRAFT_NOT_FOR_SUBMISSION',
        'documents': records, 'authority_granted': False, 'release_ready': False,
        'input_ref': 'proposal-authoring-input.json', 'input_hash': _digest(data)}
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name, payload in payloads.items():
        with (target / name).open('x', encoding='utf-8') as stream:
            os.chmod(target / name, 0o600)
            stream.write(payload if isinstance(payload, str) else json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    return {'profile': core.PROFILE, 'prepared_documents': len(records), 'document_kinds': [record['kind'] for record in records],
            'consistency': plan['consistency'], 'status': 'DRAFT_NOT_FOR_SUBMISSION',
            'authority_granted': False, 'release_ready': False}


def _load_prepared(manifest_path, root):
    from content_spec import ContentSpec
    path = Path(manifest_path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('regular prepared draft manifest required')
    manifest = json.loads(path.read_text())
    if manifest.get('package_kind') != 'proposal-prepared-draft/1' or manifest.get('input_ref') != 'proposal-authoring-input.json':
        raise ValueError('prepared draft manifest required')
    input_path = path.parent / 'proposal-authoring-input.json'
    if input_path.is_symlink():
        raise ValueError('symlink prepared input forbidden')
    data = json.loads(input_path.read_text())
    if manifest.get('input_hash') != _digest(data):
        raise ValueError('prepared input changed; prepare the draft again')
    resolver = ContentSpec(root)
    documents = {}
    contents = {}
    selected = _selection(data)
    if [item.get('kind') for item in manifest.get('documents', [])] != selected:
        raise ValueError('prepared component membership changed')
    for record in manifest['documents']:
        kind = record['kind']
        if kind not in CORE_KINDS + OPTIONAL_KINDS or record['semantic_ref'] != kind + '.semantic.json' or record['markdown_ref'] != kind + '.md':
            raise ValueError('unsafe prepared component reference')
        model_path, markdown_path = path.parent / record['semantic_ref'], path.parent / record['markdown_ref']
        if model_path.is_symlink() or markdown_path.is_symlink():
            raise ValueError('symlink prepared component forbidden')
        model, markdown = json.loads(model_path.read_text()), markdown_path.read_text()
        expected, _, sections = _semantic_model(data, kind, resolver)
        if (record['semantic_hash'] != _digest(model) or model != expected
                or record['markdown_hash'] != hashlib.sha256(markdown.encode()).hexdigest()
                or markdown != _markdown(data, kind, sections)):
            raise ValueError('prepared component changed or is stale; prepare again')
        documents[kind] = model['proposal_claims']
        contents[kind] = (model_path, markdown)
    candidate = copy.deepcopy(data)
    candidate['documents'] = documents
    return candidate, contents


def validate_prepared(manifest_path, root=ROOT):
    """Replay exact prepared drafts and cross-check independently stored component claims.

    Args:
        manifest_path: Local proposal-package.json created by prepare_package.
        root: Current shared DCS runtime root; stale specifications fail replay.
    Returns:
        Sanitized consistency and exact-byte integrity status. Edited prose is
        rejected rather than pretending to understand arbitrary free-text changes.
    """
    try:
        candidate, _ = _load_prepared(manifest_path, root)
        report = validate_package(candidate)
        report['draft_integrity'] = 'PASS'
        return report
    except (OSError, ValueError, KeyError, TypeError):
        report = _report([{'rule_id': 'proposal.draft.edited_missing_or_stale', 'location': 'prepared_draft',
                          'severity': 'critical', 'blocking': True,
                          'message': 'Prepared draft bytes or dependencies changed; regenerate from authorized working inputs.'}])
        report['draft_integrity'] = 'FAIL'
        return report


def publication_handoff(manifest_path, kind, output, root=ROOT, reviewer=None,
                        trusted_executions=None, authority=None, readiness_verifiers=None, producer=None):
    """Enter existing commercial disclosure/readiness and publication gates.

    Args:
        manifest_path: Exact prepared draft manifest, not an arbitrary Markdown file.
        kind: Selected registered proposal kind.
        output: New existing-projection bundle destination.
        root: Shared runtime root.
        reviewer, trusted_executions, authority: Existing publication host verifier
            objects; JSON declarations cannot create these trusted capabilities.
        producer: Optional existing host producer execution record. Its signed
            identity is verified through trusted_executions, never a JSON claim.
        readiness_verifiers: Existing commercial readiness callbacks injected by
            the host: identity_verifier, fabric_resolver, enforcement_verifier.
    Returns:
        BLOCKED when required gates cannot pass. If the existing host authorizes
        a projection, returns DRAFT_PROJECTED; never contract or release approval.
    """
    report = validate_prepared(manifest_path, root)
    blockers = []
    if not report['consistency_pass']:
        blockers.append('Prepared draft integrity or consistency checks are not passing.')
        return {'status': 'BLOCKED', 'blockers': blockers, 'authority_granted': False, 'release_ready': False}
    data, contents = _load_prepared(manifest_path, root)
    if kind not in contents:
        raise ValueError('requested component is not selected')
    snapshot, policy = data.get('canonical_snapshot'), data.get('disclosure_policy')
    if not snapshot or not policy:
        blockers.append('Existing canonical commercial snapshot and reviewed client disclosure policy are required.')
    else:
        try:
            projected = core.project(snapshot, 'client', policy)
            if not any(entity['data'].get('proposal_markdown') == contents[kind][1] for entity in projected['entities']):
                blockers.append('Exact draft content is not bound to the existing authorized client projection.')
            if readiness_verifiers is None:
                blockers.append('Existing trusted commercial readiness verifiers are required.')
            elif not core.readiness(snapshot, **readiness_verifiers).get('ready'):
                blockers.append('Existing commercial readiness gates are not passing.')
        except (ValueError, KeyError, TypeError):
            blockers.append('Existing commercial canonical/disclosure/readiness gates rejected the handoff.')
    if reviewer is None or trusted_executions is None:
        blockers.append('Existing host-authenticated independent content review is required; JSON cannot approve publication.')
    if blockers:
        return {'profile': core.PROFILE, 'status': 'BLOCKED', 'blockers': blockers,
                'authority_granted': False, 'release_ready': False}
    import projection
    import tempfile
    model = json.loads(contents[kind][0].read_text())
    if producer is not None:
        model['producer'] = copy.deepcopy(producer)
    profile_path = Path(root) / 'publication/archetypes/decision-paper.json'
    if not profile_path.is_file():
        profile_path = Path(root) / '.ai/runtime/publication/archetypes/decision-paper.json'
    profile = json.loads(profile_path.read_text())
    from content_spec import ContentSpec
    from content_lint import evaluate
    spec = ContentSpec(root).resolve(model['contract_id'], model['context'])
    content_report = evaluate(model, spec, reviewer=reviewer,
        trusted_executions=trusted_executions, authority=authority)
    if (content_report['reviewer']['status'] != 'verified-independent-review'
            or any(item.get('blocking') for item in content_report['findings'])):
        return {'profile': core.PROFILE, 'status': 'BLOCKED',
                'blockers': ['Existing independent content review or mandatory content gates rejected the exact source.'],
                'authority_granted': False, 'release_ready': False}
    with tempfile.TemporaryDirectory(prefix='jai-proposal-handoff-') as directory:
        source = Path(directory) / 'semantic-source.json'
        source.write_text(json.dumps(model))
        problems, _, manifest = projection.build(source, profile_path, output,
            reviewer=reviewer, trusted_executions=trusted_executions, authority=authority)
    return {'profile': core.PROFILE, 'status': 'BLOCKED' if problems else 'DRAFT_PROJECTED',
            'blockers': ['Existing projection/content gates rejected the handoff.'] if problems else [],
            'content_status': manifest.get('content_status'), 'authority_granted': False, 'release_ready': False}
