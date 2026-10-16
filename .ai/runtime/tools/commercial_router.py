#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Opt-in domain discovery, consultation validation and provider readiness gates.

Routing metadata is not authority. This module never invokes a provider, grants
permissions, signs a contract or treats declared tool lists as isolation proof.
"""
from __future__ import annotations

import argparse
import hashlib
import fcntl
import os
import tempfile
import time
import json
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'commercial/catalog.json'
CAPABILITIES = ROOT / 'commercial/provider-capabilities.json'
LEVELS = {'public': 0, 'client': 1, 'internal': 2, 'restricted': 3}
STOPWORDS = frozenset(('and', 'or', 'it', 'the', 'of', 'in', 'to', 'for', 'a', 'an', 'engineer', 'specialist', 'manager', 'lead', 'senior', 'chief', 'head', 'analyst', 'architect'))
CRITICAL = ('fresh_context', 'tool_ceiling', 'leaf_delegation_denied',
            'readonly_product_mount', 'source_allowlist', 'authenticated_identity',
            'export_boundary')


def _load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _words(value):
    terms = set(re.findall(r'\w+', value.casefold()))
    aliases = {'nákup': 'procurement', 'nakup': 'procurement', 'procurementu': 'procurement',
               'firewallu': 'firewall', 'firewally': 'firewall', 'síť': 'network',
               'síťové': 'network', 'sit': 'network', 'nabídka': 'sales',
               'nabidky': 'sales', 'nabídky': 'sales', 'poptávka': 'procurement'}
    return terms | {aliases[term] for term in terms if term in aliases}


def _amount(value):
    if not isinstance(value, str):
        raise ValueError('budget values must be decimal strings')
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('invalid decimal budget') from exc
    if not number.is_finite() or number < 0:
        raise ValueError('budget must be finite and nonnegative')
    return number


class Catalog:
    """Read compact metadata and selected verified shards, never role bodies.

    Args:
        path: Root catalog JSON path, defaults to the shipped opt-in catalog.
    Raises:
        ValueError: Catalog is incomplete, duplicated or unsupported.
        OSError: Catalog cannot be read.
    """

    def __init__(self, path=CATALOG):
        self.path = Path(path)
        self.data = _load(path)
        self.loaded = []
        rows = self.data.get('domains', [])
        if (self.data.get('version') != '1' or self.data.get('complete') is not True
                or not rows or len({r['domain_id'] for r in rows}) != len(rows)):
            raise ValueError('discovery_failure: incomplete or unsupported catalog')

    def domains(self):
        """Return compact domain rows without opening any shard or role body."""
        return self.data['domains']

    def shard(self, domain_id):
        """Load one integrity-checked metadata shard.

        Args:
            domain_id: Exact catalog domain identifier.
        Returns:
            List of compact role metadata dictionaries.
        Raises:
            ValueError: Unknown domain, escaped path, digest mismatch or truncation.
            OSError: Shard is unavailable; callers must report discovery failure.
        """
        row = next((r for r in self.domains() if r['domain_id'] == domain_id), None)
        if row is None:
            raise ValueError('discovery_failure: unknown domain')
        path = (self.path.parent / row['shard']).resolve()
        if not path.is_relative_to(self.path.parent.resolve()):
            raise ValueError('discovery_failure: shard escapes catalog')
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != row['sha256']:
            raise ValueError('discovery_failure: shard digest changed')
        data = json.loads(payload)
        if (data.get('version') != row['version'] or data.get('domain_id') != domain_id
                or data.get('complete') is not True
                or len(data.get('roles', [])) != row['role_count']):
            raise ValueError('discovery_failure: truncated shard')
        if domain_id not in self.loaded:
            self.loaded.append(domain_id)
        return data['roles']

    def route(self, question, contract_ref, domain_ids=None, strategy='hierarchical', tier=None):
        """Rank deliverable metadata; return unresolved ties rather than authority.

        Args:
            question: Nonempty deliverable request.
            contract_ref: Existing requester contract identifier.
            domain_ids: Explicit domain candidates, or root metadata selection.
            strategy: hierarchical, flat or deterministic baseline.
            tier: Optional exact advise/author/execute filter.
        Returns:
            Decision, candidates and observable metadata footprint; no model override.
        Raises:
            ValueError: Invalid inputs or unavailable catalog data.
        """
        if not question.strip() or not contract_ref or strategy not in ('hierarchical', 'flat', 'deterministic'):
            raise ValueError('question, contract and supported strategy required')
        if tier is not None and tier not in ('advise', 'author', 'execute'):
            raise ValueError('unknown tier')
        terms = _words(question) - STOPWORDS
        normalized = ' '.join(re.findall(r'\w+', question.casefold()))
        rows = self.domains()
        specialist_ids = set()
        explicit_supplier_action = bool(re.search(
            r'^(?:supplier (?:bid|deal|selling|commercial))|\b(?:prepare|draft|create|manage|build) (?:a |the )?supplier (?:bid|deal|selling|commercial)\b', normalized))
        specialist_domain_allowed = domain_ids is None or 'commercial-sourcing-and-enablement' in domain_ids
        # Explicit supplier deliverables outrank incidental shared vocabulary.
        # Multiple requested specialisms remain tied for orchestrator decomposition.
        for rule in self.data.get('specialist_intents', []):
            if (specialist_domain_allowed
                    and any(f' {phrase} ' in f' {normalized} ' for phrase in rule['phrases'])
                    and (explicit_supplier_action or not any(f' {phrase} ' in f' {normalized} ' for phrase in rule.get('exclude', [])))):
                specialist_ids.add(rule['role_id'])
        independent_review = 'independent-commercial-assurance-reviewer'
        separate_authorship = bool(re.search(
            r'\b(?:author|create|prepare|build|produce) (?:a |the )?(?:commercial pricing|selling price|basis of estimate|effort estimate|supplier bid)\b', normalized)) and bool(set(normalized.split()) & {'and', 'then'})
        # The object of an assurance request is not a request to author that object.
        if independent_review in specialist_ids and not separate_authorship:
            specialist_ids = {independent_review}
        resource_pricing = (bool(terms & {'cloud', 'aws', 'azure', 'gcp', 'compute'})
                            and bool(terms & {'pricing', 'price'})
                            and not bool(terms & {'supplier', 'selling', 'deal', 'resale'}))
        if resource_pricing:
            specialist_ids.clear()
        if domain_ids is None:
            if strategy == 'hierarchical':
                exact_domains = self.data.get('exact_role_domains', {}).get(normalized, [])
                if specialist_ids:
                    exact_domains = list(dict.fromkeys([*exact_domains, 'commercial-sourcing-and-enablement']))
                if exact_domains:
                    domain_ids = exact_domains
                else:
                    frequencies = {term: sum(term in _words(r['purpose'] + ' ' + ' '.join(r['hints'])) for r in rows) for term in terms}
                    scored = [(sum(1 / frequencies[t] for t in terms & _words(r['purpose'] + ' ' + ' '.join(r['hints'])) if frequencies[t]), r['domain_id']) for r in rows]
                    scored.sort(key=lambda item: (-item[0], item[1]))
                    domain_ids = [domain for score, domain in scored[:3] if score > 0]
            else:
                domain_ids = [r['domain_id'] for r in rows]
        candidates = []
        for domain in domain_ids:
            for role in self.shard(domain):
                if specialist_ids and role['role_id'] not in specialist_ids:
                    continue
                if tier and role['tier'] != tier:
                    continue
                text = ' '.join([role['name'], *role['aliases'], *role['deliverables']])
                score = len(terms & (_words(text) - STOPWORDS))
                exact_names = [role['name'], role['role_id'], *role['aliases']]
                if any(normalized == ' '.join(re.findall(r'\w+', name.casefold())) for name in exact_names):
                    score = 1000
                if role['role_id'] in specialist_ids:
                    score = max(score, 200)
                if strategy == 'deterministic':
                    score = 100 if question.casefold() in [x.casefold() for x in [role['role_id'], role['name'], *role['deliverables']]] else 0
                if score:
                    candidates.append({'domain_id': domain, 'role_id': role['role_id'],
                                       'tool_tier': role['tier'], 'contract_ref': contract_ref,
                                       'skill': role['skill'], 'reference': role['path'],
                                       'required_guard': role['guard'], 'score': score,
                                       'reason': 'deliverable metadata match; scope confirmation required'})
        if resource_pricing:
            candidates = []
        candidates.sort(key=lambda r: (-r['score'], r['role_id']))
        best = [r for r in candidates if r['score'] == candidates[0]['score']] if candidates else []
        return {'status': 'candidate' if len(best) == 1 else 'unresolved',
                'candidates': candidates, 'catalog_version': self.data['version'],
                'strategy': strategy, 'loaded_domains': list(self.loaded),
                'authority_granted': False, 'model_policy_handoff': 'existing model_router',
                'root_bytes': self.path.stat().st_size,
                'shard_bytes': sum((self.path.parent / r['shard']).stat().st_size for r in rows if r['domain_id'] in self.loaded)}


def provider_readiness(provider, configuration, records=None, required=CRITICAL, now=None, max_age_seconds=86400):
    """Fail closed unless every critical control has matching local test evidence.

    Args:
        provider: codex or claude CLI adapter.
        configuration: Exact provider_version, adapter_version, configuration_digest,
            deployment, product and model being dispatched.
        records: Capability records from a trusted platform-controlled registry.
        required: Explicit required capability names; defaults to all strict controls.
        now: Optional aware verification clock.
        max_age_seconds: Maximum nonnegative evidence age allowed by deployment policy.
    Returns:
        ready/blocked and reasons. This validates evidence metadata, not authenticity;
        the platform must authenticate and protect the supplied evidence registry.
    Raises:
        ValueError: Unknown provider, malformed tested evidence or unknown capability.
    """
    if provider not in ('codex', 'claude') or any(c not in CRITICAL for c in required):
        raise ValueError('unknown provider or capability')
    records = _load(CAPABILITIES)['records'] if records is None else records
    keys = ('provider_version', 'adapter_version', 'configuration_digest', 'deployment', 'product', 'model')
    reasons = []
    for capability in required:
        matching = [r for r in records if r.get('provider') == provider and r.get('capability') == capability
                    and all(configuration.get(k) not in (None, '', 'unknown') and r.get(k) == configuration[k] for k in keys)]
        passing = []
        for record in matching:
            if record.get('local_status') == 'tested':
                if not all(record.get(k) for k in ('evidence_ref', 'observed_at', 'provenance_kind')):
                    raise ValueError('tested capability missing evidence provenance')
                try:
                    observed = datetime.fromisoformat(record['observed_at'].replace('Z', '+00:00'))
                    clock = now or datetime.now(timezone.utc)
                    if observed.tzinfo is None or clock.tzinfo is None:
                        raise ValueError('timezone required')
                    age = (clock - observed).total_seconds()
                except (ValueError, TypeError, AttributeError) as exc:
                    raise ValueError('invalid capability observation timestamp') from exc
                passing.append(record.get('test_result') == 'pass' and 0 <= age <= max_age_seconds)
        if not matching or not passing or not all(passing):
            reasons.append(capability + ': missing current passing local evidence')
    return {'provider': provider, 'status': 'blocked' if reasons else 'ready',
            'reasons': reasons, 'live_provider_invoked': False}


def consultation_request(request, context, now=None):
    """Validate an orchestrated cross-domain request without invoking a specialist.

    Args:
        request: Typed request including bounded budget, ancestry and minimal_input.
        context: Trusted orchestration scope with owner, contract, clearance, allowed
            recipients/inputs, episode IDs, depth limit and remaining budget.
        now: Aware datetime, injectable for deterministic expiry tests.
    Returns:
        Validated request copy or explicit unresolved exhaustion result.
    Raises:
        ValueError: Missing fields, altered ownership, excess disclosure or leaf use.
    """
    fields = ('consultation_id', 'purpose', 'question', 'minimal_input', 'classification',
              'evidence', 'deadline', 'budget', 'recipient', 'contracting_owner',
              'requester_contract', 'output_schema', 'ancestry')
    if any(k not in request for k in fields) or any(not request[k] for k in fields if k != 'ancestry'):
        raise ValueError('incomplete consultation')
    if context.get('actor_role') != 'orchestrator':
        raise ValueError('leaf delegation denied')
    if (request['contracting_owner'] != context['contracting_owner']
            or request['requester_contract'] != context['requester_contract']):
        raise ValueError('contract ownership mismatch')
    level = LEVELS.get(request['classification'])
    if level is None or level > LEVELS.get(context.get('clearance'), -1):
        raise ValueError('classification not permitted')
    if request['recipient'] not in context['allowed_recipients']:
        raise ValueError('recipient outside scope')
    for item in request['minimal_input']:
        if (not isinstance(item, dict) or not all(item.get(k) for k in ('ref', 'version', 'classification'))
                or (item['ref'], item['version']) not in [tuple(x) for x in context['allowed_inputs']]
                or LEVELS.get(item['classification'], 99) > level
                or context.get('input_classifications', {}).get(item['ref']) != item['classification']):
            raise ValueError('input outside minimum classified allowlist')
    ancestry = request['ancestry']
    if (not isinstance(ancestry, list) or len(set(ancestry)) != len(ancestry)
            or request['consultation_id'] in ancestry
            or request['consultation_id'] in context['episode_ids']):
        raise ValueError('consultation cycle or replay')
    deadline = datetime.fromisoformat(request['deadline'].replace('Z', '+00:00'))
    if deadline.tzinfo is None:
        raise ValueError('deadline requires timezone')
    budget, remaining = _amount(request['budget']), _amount(context['remaining_budget'])
    if deadline <= (now or datetime.now(timezone.utc)) or budget > remaining or len(ancestry) >= context['max_depth']:
        return {'status': 'unresolved', 'escalation': 'owner', 'reason': 'time, budget or depth exhausted'}
    return {'status': 'validated', 'request': request, 'authority_granted': False,
            'remaining_budget_after_reservation': str(remaining - budget),
            'requires_atomic_episode_reservation': True}


def reserve_consultation(path, request, context, expected_revision, now=None):
    """Atomically reserve episode budget and ID before consultation dispatch.

    Args:
        path: Orchestrator-owned JSON state path, outside untrusted worker mounts.
        request: Typed consultation request.
        context: Trusted episode limits; initial budget is remaining_budget.
        expected_revision: Exact state revision, zero for a new episode.
        now: Optional aware datetime for deterministic deadline validation.
    Returns:
        New revision and validated request, or unresolved without mutation.
    Raises:
        ValueError: Replay, invalid request or stale concurrent revision.
        OSError: Lock, durable state write or atomic replace fails.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(path.suffix + '.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = _load(path) if path.exists() else {
            'revision': 0, 'remaining_budget': context['remaining_budget'], 'episode_ids': [],
            'contracting_owner': context['contracting_owner'],
            'requester_contract': context['requester_contract']}
        if state['revision'] != expected_revision:
            raise ValueError('stale consultation episode revision')
        if any(state[k] != context[k] for k in ('contracting_owner', 'requester_contract')):
            raise ValueError('episode ownership mismatch')
        bound = dict(context, remaining_budget=state['remaining_budget'], episode_ids=state['episode_ids'])
        result = consultation_request(request, bound, now)
        if result['status'] != 'validated':
            return result
        state.update(revision=state['revision'] + 1,
                     remaining_budget=result['remaining_budget_after_reservation'],
                     episode_ids=[*state['episode_ids'], request['consultation_id']])
        descriptor, staging = tempfile.mkstemp(dir=path.parent, prefix='.consultation-')
        try:
            with os.fdopen(descriptor, 'w') as stream:
                json.dump(state, stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(staging, path)
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if os.path.exists(staging):
                os.unlink(staging)
        return dict(result, revision=state['revision'], requires_atomic_episode_reservation=False)


def incorporate_response(request, response, review, owner, trusted_executions):
    """Validate response binding and independent review before owner incorporation.

    Args:
        request: Previously validated typed consultation request.
        response: Scoped response with sources, assumptions, unit/state and identity.
        review: Review bound to exact response digest and independent execution ID.
        owner: Trusted contracting owner performing incorporation.
        trusted_executions: Platform-authenticated execution records keyed by ID.
    Returns:
        Incorporation record retaining ownership and no authority grant.
    Raises:
        ValueError: Evidence binding, identity, independence or ownership fails.
    """
    required = ('consultation_id', 'assumptions', 'source_passage_ids', 'applicability',
                'estimate_state', 'unit', 'interval', 'uncertainty', 'execution_id')
    if any(k not in response for k in required) or response['consultation_id'] != request['consultation_id']:
        raise ValueError('incomplete or unrelated response')
    if response['estimate_state'] not in ('missing', 'requested', 'declined', 'provisional', 'supported', 'conflicting', 'obsolete'):
        raise ValueError('unknown estimate state')
    if response['estimate_state'] == 'supported' and not response['source_passage_ids']:
        raise ValueError('supported response needs source passages')
    digest = hashlib.sha256(json.dumps(response, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    producer = trusted_executions.get(response['execution_id'], {})
    checker = trusted_executions.get(review.get('execution_id'), {})
    if (not producer.get('authenticated') or not checker.get('authenticated')
            or producer.get('principal') == checker.get('principal')
            or not producer.get('principal') or not checker.get('principal')
            or review.get('response_sha256') != digest or review.get('result') != 'accepted'
            or owner != request['contracting_owner']):
        raise ValueError('independent authenticated snapshot review required')
    return {'consultation_id': request['consultation_id'], 'response_sha256': digest,
            'contracting_owner': owner, 'authority_granted': False,
            'next_action': 'create versioned dependency through canonical DAG owner'}


def evaluate_routing(corpus, catalog_path=CATALOG):
    """Run reproducible local metadata baselines with observed wall time.

    Args:
        corpus: Versioned cases with question and expected_roles fixed before run.
        catalog_path: Compact catalog path, useful for failure fixtures.
    Returns:
        Per-case recall, top-match correctness, bytes and elapsed seconds. Invocation
        cost stays not_applicable because no LLM/provider is invoked. This small
        smoke corpus is not independent quality qualification.
    Raises:
        ValueError: Invalid corpus or discovery failure.
    """
    if corpus.get('version') != '1' or not corpus.get('cases'):
        raise ValueError('versioned nonempty routing corpus required')
    results = []
    for strategy in ('deterministic', 'flat', 'hierarchical'):
        for case in corpus['cases']:
            catalog = Catalog(catalog_path)
            start = time.perf_counter()
            decision = catalog.route(case['question'], 'eval-contract', strategy=strategy)
            elapsed = time.perf_counter() - start
            expected = set(case['expected_roles'])
            candidates = decision['candidates']
            retrieved = {row['role_id'] for row in candidates}
            top = {row['role_id'] for row in candidates if row['score'] == candidates[0]['score']} if candidates else set()
            results.append({'strategy': strategy, 'question': case['question'],
                            'recall': len(expected & retrieved) / len(expected) if expected else None,
                            'top_correct': len(top) == 1 and bool(top & expected) if expected else not candidates,
                            'tie_contains_expected': len(top) > 1 and bool(top & expected),
                            'root_bytes': decision['root_bytes'], 'shard_bytes': decision['shard_bytes'],
                            'elapsed_seconds': elapsed, 'provider_cost': 'not_applicable',
                            'provider_invocations': 0, 'status': decision['status']})
    return {'corpus_version': corpus['version'], 'corpus_sha256': hashlib.sha256(json.dumps(corpus, sort_keys=True).encode()).hexdigest(),
            'qualification': 'local-metadata-smoke-only', 'results': results}


def main(argv=None):
    """Run metadata discovery CLI; return zero, or two for invalid inputs.

    Args:
        argv: Optional CLI argument list.
    Returns:
        Process exit code; writes JSON to stdout, never invokes provider tools.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question')
    parser.add_argument('--contract', required=True)
    parser.add_argument('--domain', action='append')
    parser.add_argument('--strategy', choices=['hierarchical', 'flat', 'deterministic'], default='hierarchical')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(Catalog().route(args.question, args.contract, args.domain, args.strategy), indent=2))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(json.dumps({'status': 'discovery_failure', 'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
