#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Evaluate typed semantic material, preserving existing gates and JAI authority.

This deterministic pilot cannot certify professional meaning. Review predicates
remain pending without independently attributable runtime evidence. Blocking
rollout requires the existing human authority boundary, unavailable to this CLI.
"""
from __future__ import annotations
import argparse
import copy
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import tempfile
import jsonschema
import content_spec
import content_metrics

SCHEMA = Path(__file__).resolve().parents[1] / 'content/schema/content-evaluation.schema.json'
_PLACEHOLDERS = {'', 'tbd', 'todo', 'unknown', 'pending', 'n/a', 'na', 'not applicable', 'placeholder', '...', 'to be determined'}
_METADATA = {'id', 'title', 'heading', 'label', 'status', 'knowledge_status', 'evidence_refs', 'evidence_ref', 'owner', 'version', 'hash'}


def _field(model, field):
    current = model.get('semantic_units', model)
    for part in field.split('.'):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _substantive(value):
    if value is None:
        return False
    if isinstance(value, str):
        stripped = value.strip().casefold()
        return stripped not in _PLACEHOLDERS and not stripped.startswith('#') and not re.fullmatch(r'\[.*\]|<.*>', stripped)
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(value)
    if isinstance(value, list):
        return bool(value) and all(_substantive(child) for child in value)
    if isinstance(value, dict):
        return any(_substantive(child) for key, child in value.items() if key not in _METADATA)
    return False


def _typed(value, kind):
    kinds = {'string': str, 'reference': str, 'number': (int, float), 'integer': int, 'boolean': bool, 'array': list, 'object': dict}
    return kind == 'any' or (kind in kinds and isinstance(value, kinds[kind]) and not (kind in ('number', 'integer') and isinstance(value, bool)))


def _credential_locations(model):
    locations = set()
    credential_key = re.compile(r'^(password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret|private[_-]?key)$', re.I)
    assignment = re.compile(r"\b(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"']?([^\s\"';,}]+)", re.I)
    token = re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b')
    private_key = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\s+[A-Za-z0-9+/=]{16,}')
    def literal(value):
        text = value.strip()
        lower = text.casefold()
        return (len(text) >= 8 and not any(char.isspace() for char in text) and lower not in _PLACEHOLDERS
                and not any(marker in lower for marker in ('redacted', 'placeholder', 'example', 'changeme', 'your_', 'your-', 'vault://', 'secret://', 'secretsmanager:', 'env:', '${', '{{', '<'))
                and lower not in ('required', 'prohibited', 'forbidden', 'retrieved', 'not-stored', 'reference', 'secret-ref'))
    def walk(value, path):
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f'{path}.{key}'
                if credential_key.fullmatch(key) and isinstance(child, str) and literal(child):
                    locations.add(child_path)
                walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f'{path}[{index}]')
        elif isinstance(value, str):
            if token.search(value) or private_key.search(value) or any(literal(match.group(1)) for match in assignment.finditer(value)):
                locations.add(path)
    walk(model, '$')
    return sorted(locations)


def _compiled_hash(spec):
    body = copy.deepcopy(spec)
    for key in ('compiled_spec_hash', 'artifact_id', 'document_kind', 'spec_selection_reason', 'decision_supported', 'resolution_hash'):
        body.pop(key, None)
    return content_spec.canonical_hash(body)


class ExistingFabricAuthority:
    """Read an existing signed L0 acceptance without creating authority acts.

    Args:
        fabric: Host-opened existing Fabric instance; key custody and its ledger
            path are host configuration, never supplied by semantic JSON.
        fragment_id: Existing L1 product whose text is strict JSON with profile
            content-enforcement and a dcs_activation scope payload. This text is
            created through the existing answer/ingest path and signed L0 review.
        clock: Host clock returning an aware datetime; defaults to UTC now.
    """

    def __init__(self, fabric, fragment_id, clock=None):
        self.fabric = fabric
        self.fragment_id = fragment_id
        self.clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))
        fragment = fabric.nodes.get(fragment_id, {})
        self.proof = {'fragment_id': fragment_id, 'fragment_hash': content_spec.canonical_hash(fragment)}

    def verify(self, proof):
        """Return qualified signed scope payload or None for absent/stale evidence.

        Args:
            proof: Exact host-pinned fragment ID and hash.
        Returns:
            Verified existing L0 acceptance metadata, without issuing approval.
        """
        if proof != self.proof:
            return None
        try:
            problems, warnings = self.fabric.verify()
            if problems or warnings:
                return None
            fragment = self.fabric.nodes[self.fragment_id]
            if content_spec.canonical_hash(fragment) != proof['fragment_hash'] or fragment.get('type') != 'frag' or fragment.get('layer') != 1:
                return None
            accepted, reasons = self.fabric.justify(self.fragment_id, strict=True)
            acceptance = self.fabric.lifecycle.evaluate(fragment['version_id'], release=True)
            acceptance_version = self.fabric.lifecycle.proofs.get(
                ('default', fragment['version_id'], 'accept'))
            review_id = next((identifier for identifier, node in self.fabric.nodes.items()
                              if node['version_id'] == acceptance_version), None)
            review = self.fabric.nodes.get(review_id, {})
            if not accepted or reasons or not acceptance['eligible'] or review.get('layer') != 0 or review.get('state') != 'accepts' or not review.get('reviewer'):
                return None
            policy = json.loads(fragment.get('text', ''), object_pairs_hook=content_spec._pairs,
                                parse_constant=lambda value: (_ for _ in ()).throw(ValueError('NONFINITE')))
            if not isinstance(policy, dict) or policy.get('profile') != 'content-enforcement':
                return None
            payload = copy.deepcopy(policy.get('dcs_activation'))
            if not isinstance(payload, dict):
                return None
            payload.update(authority_ref=review_id, existing_jai_l0=True,
                           signature_verified=True, fabric_verified=True,
                           verification_warnings=[], verified_at=self.clock().isoformat())
            return payload
        except (ValueError, TypeError, KeyError, OSError):
            return None


def _host_verify(host, attestation):
    verifier = host if callable(host) else getattr(host, 'verify', None)
    if not callable(verifier):
        return None
    try:
        payload = verifier(attestation)
        return payload if isinstance(payload, dict) else None
    except (ValueError, TypeError, KeyError):
        return None


def _review_valid(review, model, spec, semantic_hash, required_units, host):
    if not isinstance(review, dict) or not isinstance(model.get('producer'), dict):
        return False
    subject = copy.deepcopy(review)
    attestation = subject.pop('attestation', None)
    payload = _host_verify(host, attestation)
    producer = copy.deepcopy(model)
    producer_attestation = producer['producer'].pop('attestation', None)
    producer_payload = _host_verify(host, producer_attestation)
    if not payload or not producer_payload:
        return False
    producer_hash = content_spec.canonical_hash(producer)
    principal = payload.get('principal')
    producer_principal = producer_payload.get('principal')
    if not principal or not producer_principal or principal == producer_principal:
        return False
    if payload.get('reviewer') is not True or producer_payload.get('reviewer') is not False:
        return False
    if (payload.get('subject_digest') != content_spec.canonical_hash(subject)
            or payload.get('snapshot_digest') != semantic_hash
            or payload.get('context_digest') != content_spec.canonical_hash(review.get('context_manifest'))
            or producer_payload.get('subject_digest') != producer_hash
            or producer_payload.get('snapshot_digest') != producer_hash
            or producer_payload.get('context_digest') != content_spec.canonical_hash(model['producer'].get('context_manifest'))):
        return False
    if (review.get('semantic_hash') != semantic_hash or review.get('compiled_spec_hash') != spec.get('compiled_spec_hash')
            or review.get('context_hash') != spec.get('context_hash')):
        return False
    units = review.get('unit_reviews', [])
    if not isinstance(units, list) or len({item.get('unit_id') for item in units if isinstance(item, dict)}) != len(units):
        return False
    accepted = {item.get('unit_id') for item in units if isinstance(item, dict) and item.get('verdict') == 'PASS'
                and _substantive(item.get('rationale')) and _substantive(item.get('evidence'))}
    if not set(required_units) <= accepted:
        return False
    for item in review.get('findings', []):
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str) and item[key].strip() for key in ('rule_id', 'location', 'evidence', 'remediation')):
            return False
        if item.get('category') not in ('security-policy', 'existing-gate', 'critical-content', 'material-content', 'editorial') or item.get('severity') not in ('blocker', 'critical', 'major', 'minor'):
            return False
    return True


def _authority_time(value, *, date_end=False, allow_date=True):
    # Date-only policy bounds deliberately mean the whole UTC day. Host
    # verification time is always an aware instant, never an author-supplied date.
    if allow_date and isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        day = dt.date.fromisoformat(value)
        return dt.datetime.combine(day, dt.time.max if date_end else dt.time.min, dt.timezone.utc)
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', value):
        raise ValueError('Authority timestamps require an explicit timezone.')
    instant = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError('Naive authority timestamp.')
    return instant.astimezone(dt.timezone.utc)


def _activation_valid(authority, spec, model):
    # Only a trusted host can verify an existing signed fabric authority act.
    payload = _host_verify(authority, getattr(authority, 'proof', None))
    if not payload or spec.get('status') != 'approved' or spec.get('calibration_status') != 'human-approved':
        return False
    try:
        now = _authority_time(payload['verified_at'], allow_date=False)
        expires = _authority_time(payload['expires_at'], date_end=True)
        issued = _authority_time(payload['issued_at'])
    except (KeyError, TypeError, ValueError):
        return False
    qualification = payload.get('qualification', {})
    if not isinstance(qualification, dict):
        return False
    for name, maximum in (('critical_recall', 1), ('false_positive_rate', 1), ('critical_coverage_percent', 100)):
        value = qualification.get(name)
        if type(value) not in (int, float) or not 0 <= value <= maximum or not math.isfinite(value):
            return False
    for name in ('sod_escapes', 'critical_forbidden', 'unsupported_critical_claims'):
        value = qualification.get(name)
        if type(value) is not int or value < 0:
            return False
    return bool(payload.get('authority_ref') and payload.get('existing_jai_l0') is True
                and payload.get('signature_verified') is True and payload.get('fabric_verified') is True
                and not payload.get('verification_warnings') and payload.get('scope') == 'dcs-content-enforcement'
                and payload.get('compiled_spec_hash') == spec.get('compiled_spec_hash')
                and payload.get('document_kind') == spec.get('document_kind')
                and payload.get('context_hash') == spec.get('context_hash') and issued <= now <= expires
                and qualification.get('calibration_status') == 'human-approved'
                and qualification.get('critical_recall', 0) >= .95
                and qualification.get('false_positive_rate', 1) <= .1
                and qualification.get('sod_escapes') == 0
                and qualification.get('critical_forbidden') == 0
                and qualification.get('unsupported_critical_claims') == 0
                and qualification.get('critical_coverage_percent') == 100
                and re.fullmatch(r'[0-9a-f]{64}', str(qualification.get('corpus_hash', ''))))


def evaluate(model, spec, mode='advisory', reviewer=None, trusted_executions=None, authority=None):
    """Produce a deterministic hash-bound draft QA report without granting authority.

    Args:
        model: Semantic JSON with explicit instance artifact_id and contract_id.
        spec: Trusted resolved compiled DCS with explicit contract binding. The
            embedding host must resolve this from its registry; this pure API
            also accepts synthetic test specifications. CLI resolves independently.
        mode: advisory or warning; blocking is denied without existing L0 proof.
        reviewer: Hash-bound review, authenticated only by a host verifier.
        trusted_executions: Host callable or object.verify accepting an attestation
            and returning the existing TrustedDispatcher verified payload or None.
        authority: Host object.verify activation proof from the existing signed
            JAI fabric; mappings and model-supplied booleans grant nothing.
    Returns:
        Strict schema-valid content QA report with located findings and stable hash.
    Raises:
        ValueError: For invalid JSON, unsupported mode, or unverifiable activation.
        jsonschema.ValidationError: If the generated report violates its schema.
    """
    jsonschema.Draft202012Validator(content_spec.load_json(SCHEMA.with_name('semantic-content.schema.json'))).validate(model)
    if mode not in ('advisory', 'warning', 'blocking'):
        raise ValueError('INVALID_MODE')
    if mode == 'blocking' and not _activation_valid(authority, spec, model):
        raise ValueError('HUMAN_L0_ACTIVATION_REQUIRED: verified scoped qualification and existing fabric authority proof required')
    activation = _host_verify(authority, getattr(authority, 'proof', None)) if mode == 'blocking' else None
    semantic_hash = content_spec.canonical_hash(model)
    content_spec.canonical_hash(spec)
    findings, coverage, forbidden, unknowns, unsupported, review_pending = [], [], [], [], [], []
    def finding(rule, location, evidence, category='critical-content', severity='critical', remediation='Provide substantive, typed and evidenced information.'):
        if category == 'existing-mandatory-gate':
            category = 'existing-gate'
        findings.append({'rule_id': rule, 'location': location, 'category': category, 'severity': severity,
                         'evidence': evidence, 'remediation': remediation,
                         'blocking': category in ('security-policy', 'existing-gate') or (category == 'critical-content' and mode == 'blocking')})
    for location in _credential_locations(model):
        finding('global.secret_disclosure', location, 'High-confidence credential-like literal detected; value redacted.', 'security-policy', 'critical', 'Remove credential material and use an authorised secret-store reference.')
    if not isinstance(model.get('artifact_id'), str) or not model.get('artifact_id'):
        finding('INSTANCE_ID_REQUIRED', '$.artifact_id', 'Missing explicit artifact instance identifier.', 'existing-gate')
    if model.get('contract_id') != spec.get('artifact_id') or not spec.get('artifact_id'):
        finding('CONTRACT_BINDING_MISMATCH', '$.contract_id', 'Instance contract does not match the resolved stable role binding.', 'existing-gate')
    if model.get('document_kind') != spec.get('document_kind'):
        finding('DOCUMENT_KIND_MISMATCH', '$.document_kind', 'Explicit document kind differs from the resolved binding.', 'existing-gate')
    if spec.get('compiled_spec_hash') != _compiled_hash(spec) or model.get('compiled_spec_hash') != spec.get('compiled_spec_hash'):
        finding('COMPILED_SPEC_HASH_MISMATCH', '$.compiled_spec_hash', 'Compiled content specification is stale or tampered.', 'existing-gate')
    if model.get('context', {}) != spec.get('context', {}) or spec.get('context_hash') != content_spec.canonical_hash(spec.get('context', {})):
        finding('CONTEXT_MISMATCH', '$.context', 'Applicability context differs from the compiled context.')
    for unit in spec.get('blueprint', {}).get('semantic_units', []):
        ident, category = unit['id'], unit.get('category')
        values = [(field, _field(model, field)) for field in unit.get('semantic_fields', [])]
        applicability = unit.get('applicability')
        if unit.get('when'):
            field = unit['when']['field'].removeprefix('context.')
            context_value = model.get('context', {}).get(field)
            if context_value is None:
                applicability = None
        if category in ('forbidden_information', 'low_value_information'):
            if applicability is False:
                continue
            if applicability is None:
                unknowns.append({'unit_id': ident, 'location': '$.context', 'reason': 'Prohibition applicability remains unresolved.'})
                finding(ident, '$.context', 'Prohibition applicability requires explicit context evidence.', unit.get('rule_category', 'critical-content'))
                continue
            if unit.get('acceptance_predicate', {}).get('op') in ('review', 'evidence'):
                review_pending.append(ident)
            for field, value in values:
                if _substantive(value):
                    record = {'unit_id': ident, 'location': '$.semantic_units.' + field}
                    forbidden.append(record)
                    finding(ident, record['location'], 'Content occupies an explicitly prohibited or discouraged semantic field.',
                            unit.get('rule_category', 'critical-content' if category == 'forbidden_information' else 'editorial'), unit.get('severity', 'critical'))
            continue
        if category == 'optional_information':
            continue
        state = 'complete'
        if applicability is None:
            state = 'unknown-applicability'
            unknowns.append({'unit_id': ident, 'location': '$.context', 'reason': 'Applicability requires explicit context evidence.'})
            finding(ident, '$.context', f'{ident}: applicability remains unknown.')
        elif applicability is False:
            state = 'not-applicable'
            if category == 'conditional_information':
                review_pending.append(ident)
            for field, value in values:
                if isinstance(value, dict) and value.get('status') == 'not_applicable':
                    refs = value.get('evidence_refs', [])
                    sources = [source for source in model.get('evidence', []) if isinstance(source, dict)]
                    if isinstance(model.get('applicability_evidence'), dict):
                        sources.append(model['applicability_evidence'])
                    matched = [source for source in sources if source.get('id') in refs]
                    if not _substantive(value.get('reason')) or not matched or any(not _substantive(source.get('description', source.get('payload'))) for source in matched):
                        finding('NA_APPLICABILITY_EVIDENCE', '$.semantic_units.' + field, 'Conditional N/A requires an explicit reason and an actual context-evidence reference.', 'material-content', 'major', 'Supply context evidence and retain independent applicability review.')
        else:
            for field, value in values:
                location = '$.semantic_units.' + field
                if not _typed(value, unit.get('datatype', 'any')) or not _substantive(value):
                    state = 'missing-or-invalid'
                    finding(ident, location, f'{ident}: missing, placeholder, headings-only or wrong datatype.')
                records = value if isinstance(value, list) else [value]
                for index, record in enumerate(records):
                    knowledge = record.get('knowledge_status') if isinstance(record, dict) else model.get('knowledge_states', {}).get(field)
                    if knowledge in ('unknown', 'pending'):
                        state = 'unknown'
                        unknowns.append({'unit_id': ident, 'location': location + (f'[{index}]' if isinstance(value, list) else ''), 'reason': knowledge})
                        finding('UNKNOWN_REQUIRED_INFORMATION', location, f'{ident}: knowledge is explicitly {knowledge}.', 'material-content', 'major')
                    if knowledge not in ('known', 'assumption', 'synthetic-assumption', 'unknown', 'pending') and _substantive(record):
                        state = 'unknown'
                        finding(ident, location + (f'[{index}]' if isinstance(value, list) else ''), f'{ident}: required information has no explicit knowledge state.')
                if isinstance(value, dict) and value.get('status') in ('not_applicable', 'waived'):
                    state = 'missing-or-invalid'
                    finding(ident, location, f'{ident}: unconditional or applicable obligation cannot be waived by the author.')
                    if value.get('status') == 'waived':
                        finding('global.authority_bypass', location, 'Author-declared exception cannot waive an applicable obligation.', 'existing-gate')
            if unit.get('acceptance_predicate', {}).get('op') in ('review', 'evidence'):
                review_pending.append(ident)
        coverage.append({'unit_id': ident, 'fields': [field for field, _ in values], 'status': state, 'critical': unit.get('severity', 'critical') == 'critical'})
    evidence = {}
    ambiguous = set()
    for index, item in enumerate(model.get('evidence', [])):
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item.get('id'):
            finding('EVIDENCE_ID_INVALID', f'$.evidence[{index}]', 'Evidence requires an explicit unique identifier.', 'existing-gate')
            continue
        if item['id'] in evidence:
            ambiguous.add(item['id'])
            finding('EVIDENCE_ID_DUPLICATE', f'$.evidence[{index}]', 'Duplicate evidence IDs make claim references ambiguous.', 'existing-gate')
        evidence[item['id']] = item
    now_text = model.get('evaluation_date')
    # Freshness is relative to the artifact's explicit evaluation date, never a hidden clock.
    def evidence_valid(ref):
        ident = ref.get('id') if isinstance(ref, dict) else ref
        if not isinstance(ident, str) or ident in ambiguous:
            return False
        source = evidence.get(ident)
        if isinstance(ref, dict) and source and (ref.get('version') != source.get('version') or ref.get('hash') != source.get('hash')):
            return False
        if not source or not source.get('version') or 'payload' not in source:
            return False
        if source.get('hash') != content_spec.canonical_hash(source['payload']):
            return False
        try:
            observed = dt.date.fromisoformat(source['observed_at'][:10])
            until = dt.date.fromisoformat(source['valid_until'][:10])
            now = dt.date.fromisoformat(now_text)
            return observed <= now <= until
        except (KeyError, TypeError, ValueError):
            return False
    claims = []
    def walk(value, path):
        if isinstance(value, dict):
            if 'knowledge_status' in value or (path.startswith('$.claims[') and path.count('.') == 1):
                claims.append((path, value))
            for key, child in value.items():
                if key != 'evidence':
                    walk(child, f'{path}.{key}')
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f'{path}[{index}]')
    walk(model.get('semantic_units', {}), '$.semantic_units')
    walk(model.get('claims', []), '$.claims')
    for location, claim in claims:
        status = claim.get('knowledge_status')
        refs = claim.get('evidence_refs', [claim['evidence_ref']] if claim.get('evidence_ref') else [])
        if status not in ('known', 'assumption', 'synthetic-assumption', 'unknown', 'pending'):
            unsupported.append({'location': location, 'evidence_refs': refs})
            finding(model.get('document_kind', '') + '.unsupported_material_claim', location, 'Material claim has no recognised knowledge state or supporting evidence.')
        elif status == 'known' and (not isinstance(refs, list) or not refs or not all(evidence_valid(ref) for ref in refs)):
            unsupported.append({'location': location, 'evidence_refs': refs})
            finding(model.get('document_kind', '') + '.unsupported_material_claim', location, 'Known claim lacks versioned hash-verified evidence valid on the evaluation date.', 'existing-gate')
        elif status in ('unknown', 'pending'):
            unknowns.append({'unit_id': claim.get('id', ''), 'location': location, 'reason': status})
        if claim.get('contradicts'):
            finding('MATERIAL_CONTRADICTION', location, 'An explicit contradiction remains unresolved: ' + str(claim['contradicts']))
    review_status = 'pending-independent-review'
    verified_review = _review_valid(reviewer, model, spec, semantic_hash, review_pending, trusted_executions)
    if verified_review:
        review_status = 'verified-independent-review'
        for review_finding in reviewer.get('findings', []):
            finding(review_finding['rule_id'], review_finding['location'], review_finding['evidence'],
                    review_finding['category'], review_finding['severity'], review_finding['remediation'])
    elif reviewer is not None:
        finding('REVIEW_IDENTITY_UNVERIFIED', '$.reviewer', 'Review is not independently authenticated and bound to this exact source, specification and context.', 'existing-gate', remediation='Obtain an independent review through the existing attributable JAI runtime.')
    for key in ('irrelevant_annex', 'annexes'):
        if _substantive(model.get(key)):
            finding(model.get('document_kind', '') + '.irrelevant_detail', '$.' + key, 'Annex content has no registered semantic unit or decision-purpose reference; relevance requires independent review.', 'editorial', 'minor', 'Link annex information to a required unit and audience decision, or remove it.')
    metrics = content_metrics.analyze(model, spec)
    for item in metrics['budget_advice']:
        if item.get('category') == 'critical-content':
            finding(item['rule_id'], '$', str(item), 'critical-content', 'critical', item['action'])
        else:
            finding('SOFT_SIZE_BUDGET', '$', str(item), 'editorial', 'minor', 'Reduce or justify length against audience needs.')
    for item in metrics['duplication']:
        finding(model.get('document_kind', '') + '.duplicate_claim', item['locations'][0], str(item['locations']), 'editorial', 'minor', 'Reference canonical information instead of repeating it.')
    required = [item for item in coverage if item['status'] != 'not-applicable']
    blocked = any(item['blocking'] for item in findings)
    report = {'schema_version': '1.1.0', 'artifact_id': model.get('artifact_id', ''), 'contract_id': model.get('contract_id', ''),
              'document_kind': model.get('document_kind', ''), 'semantic_hash': semantic_hash,
              'source_hash': model.get('source_hash', semantic_hash), 'spec_id': spec.get('spec_id', ''), 'spec_version': spec.get('spec_version', ''),
              'compiled_spec_hash': spec.get('compiled_spec_hash', ''), 'context_hash': content_spec.canonical_hash(model.get('context', {})),
              'section_coverage': [{'section_id': item.get('id', str(index)), 'substantive': _substantive(item.get('content'))} for index, item in enumerate(model.get('sections', [])) if isinstance(item, dict)],
              'semantic_unit_coverage': coverage, 'critical_coverage_percent': 100.0 * sum(item['status'] == 'complete' for item in required) / len(required) if required else 100.0,
              'forbidden_violations': forbidden, 'unknowns': unknowns, 'unsupported_claims': unsupported,
              'length': metrics['counts'], 'duplication': metrics['duplication'], 'findings': findings,
              'reviewer': {'status': review_status, 'required_units': sorted(set(review_pending)), 'claimed_review': reviewer},
              'waivers': [], 'approval_refs': [activation['authority_ref']] if activation else [], 'mode': mode, 'gate_verdict': 'CONTENT_FAIL' if blocked else ('CONTENT_PASS' if verified_review and not any(item['category'] in ('critical-content', 'material-content') for item in findings) else 'DRAFT_INCOMPLETE'),
              'deterministic_status': 'FAIL' if any(item['category'] in ('security-policy', 'existing-gate', 'critical-content') for item in findings) else 'PASS',
              'calibration_status': spec.get('calibration_status', 'synthetic-only'), 'production_ready': False,
              'limitations': ['Deterministic pilot only; independent semantic review and human professional approval remain pending.']}
    report['report_hash'] = content_spec.canonical_hash(report)
    jsonschema.Draft202012Validator(content_spec.load_json(SCHEMA)).validate(report)
    return report


def verify_report(report, model, spec, trusted_executions=None, authority=None):
    """Return integrity errors by schema validation and complete deterministic replay.

    Args:
        report: Candidate immutable content QA report.
        model: Original semantic source snapshot.
        spec: Original resolved compiled specification.
        trusted_executions: Optional host runtime attestation verifier.
        authority: Optional existing JAI L0 activation verifier.
    Returns:
        Error strings; empty only for an exact replay of the supported pilot report.
    """
    try:
        jsonschema.Draft202012Validator(content_spec.load_json(SCHEMA)).validate(report)
        expected = evaluate(model, spec, mode=report['mode'], reviewer=report['reviewer'].get('claimed_review'), trusted_executions=trusted_executions, authority=authority)
        # Optional modality counters were added in .8. Historical .7 reports
        # retain their original immutable bytes/hash while all gate findings replay.
        for metric in ('elements', 'configuration_checks'):
            if spec.get('spec_version') == '1.0.0' and metric not in report.get('length', {}):
                expected['length'].pop(metric, None)
        expected.pop('report_hash', None)
        expected['report_hash'] = content_spec.canonical_hash(expected)
        return [] if expected == report else ['CONTENT_QA_REPLAY_MISMATCH']
    except (ValueError, TypeError, KeyError, jsonschema.ValidationError) as exc:
        return ['CONTENT_QA_INVALID: ' + str(exc)]


def write_report(path, report):
    """Atomically create a QA record; never replace a different existing record.

    Args:
        path: Output JSON path; parent directories are created as needed.
        report: Schema-valid report whose self hash is verified before writing.
    Returns:
        Path to the immutable record, including identical idempotent writes.
    Raises:
        ValueError: If the hash is wrong or another record already occupies path.
        OSError: On filesystem failures.
    """
    jsonschema.Draft202012Validator(content_spec.load_json(SCHEMA)).validate(report)
    body = dict(report)
    digest = body.pop('report_hash')
    if digest != content_spec.canonical_hash(body):
        raise ValueError('CONTENT_QA_HASH_MISMATCH')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if content_spec.load_json(path) == report:
            return path
        raise ValueError('IMMUTABLE_CONTENT_QA_EXISTS')
    fd, temporary = tempfile.mkstemp(prefix='.content-qa-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            if content_spec.load_json(path) != report:
                raise ValueError('IMMUTABLE_CONTENT_QA_EXISTS') from exc
    finally:
        os.unlink(temporary)
    return path


def _provider_profile(provider):
    runtime = Path(__file__).resolve().parents[1]
    profiles = []
    for name in ('artifact-author', 'evidence-rationale-reviewer'):
        adapter = content_spec.load_json(runtime / 'providers' / provider / (name + '.json'))
        reference = adapter.get('content_profile_ref')
        if reference != 'jai/profiles/content-profile.json':
            raise ValueError('PROVIDER_CONTENT_PROFILE_MISMATCH')
        profiles.append(reference)
    profile = content_spec.load_json(runtime / profiles[0])
    if profile.get('registry_ref') != 'content/registry.json' or profile.get('resolver') != 'tools/content_spec.py' or profile.get('validator') != 'tools/content_lint.py':
        raise ValueError('PROVIDER_CONTENT_ENGINE_MISMATCH')


def main(argv=None):
    """Run check CLI without accepting model-declared approval or trusted identity.

    Args:
        argv: Optional command arguments.
    Returns:
        Zero for nonblocking pilot result; one for blocking findings or bad input.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('check')
    command.add_argument('semantic')
    command.add_argument('--spec', required=True)
    command.add_argument('--root')
    command.add_argument('--output', required=True)
    command.add_argument('--provider', choices=('codex', 'claude'), default='codex')
    command.add_argument('--mode', choices=('advisory', 'warning', 'blocking'), default='advisory')
    args = parser.parse_args(argv)
    try:
        _provider_profile(args.provider)
        model, spec = content_spec.load_json(args.semantic), content_spec.load_json(args.spec)
        resolved = content_spec.ContentSpec(args.root).resolve(model['contract_id'], model.get('context', {}))
        if resolved != spec:
            raise ValueError('UNTRUSTED_COMPILED_SPEC: supplied profile differs from registered resolution')
        report = evaluate(model, spec, mode=args.mode)
        write_report(args.output, report)
        print(json.dumps({'report_hash': report['report_hash'], 'gate_verdict': report['gate_verdict']}))
        return int(any(item['blocking'] for item in report['findings']))
    except (OSError, ValueError, TypeError, KeyError, jsonschema.ValidationError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
