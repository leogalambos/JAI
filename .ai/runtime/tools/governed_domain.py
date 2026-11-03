#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Host-selected domain bindings over the existing Gen2 Store and evaluator.

Preissued context tokens identify captured authorship; they grant no authority.
Each consumer action captures one current state, reusing immutable provenance
inside that action without replaying history or synthesizing professional review.
"""
from __future__ import annotations

import contextlib
import copy
import json
from pathlib import Path

import lifecycle as lc
import content_spec
import governed_semantic


def _digest(value):
    return content_spec.canonical_hash(value)


def _point(value):
    if not isinstance(value, dict) or set(value) != {'ref', 'use_scope'}:
        raise ValueError('Exact host-selected UsePoint required')
    return copy.deepcopy(value)


class GovernedDomain:
    """Resolve actual domain producer and review facts for host-pinned products.

    Args:
        store: Existing host-owned Gen2 Store, never selected by source JSON.
        producers: Exact product UsePoints admitted by the existing return path.
    Raises:
        ValueError: A Store or exact product-use list is missing.
    """

    def __init__(self, store, producers):
        if not isinstance(store, lc.Store) or not producers:
            raise ValueError('Host-opened Store and exact producer uses required')
        self.store = store
        self.producers = [_point(value) for value in producers]
        self._state = None
        self._facts = {}
        self._basis = {}
        self._indexed = False

    @contextlib.contextmanager
    def action(self):
        """Capture current facts once for one action; nested callbacks reuse them.

        Yields:
            This adapter with an action-local snapshot. A later action refreshes
            current applicability and material while keeping the Store warm.
        Raises:
            ValueError, OSError: Existing history or supporting material is invalid.
        """
        if self._state is not None:
            yield self
            return
        self._state = self.store.read()
        self._facts, self._basis = {}, {}
        self._indexed = False
        try:
            yield self
        finally:
            self._state = None
            self._facts, self._basis = {}, {}
            self._indexed = False

    def _evaluate(self, point):
        key = lc.canonical(point)
        if key not in self._basis:
            self._basis[key] = self._state.evaluate(point['ref'], point['use_scope'])
        return self._basis[key]

    def _captured(self, point):
        state = self._state
        record = state.resolve(point['ref'], 'product')
        provenance = state.provenance[point['ref']['version_id']]
        context_ref = provenance['context']
        context = state.resolve(context_ref, 'context')
        details = state.run_details[context['run_id']]
        assignment = state.resolve(context['assignment'], 'assignment')
        if (provenance['origin'] != {'kind': 'assignment', 'ref': context['assignment']}
                or record['assignment'] != context['assignment']
                or context['execution']['phase'] != 'work'
                or state.run_states[context['run_id']] != 'returned'
                or not details.get('native')):
            raise ValueError('Material is not an actual admitted native work return')
        transaction = state.transactions[provenance['sequence'] - 1]
        packages = [lc.loads(raw) for raw in (transaction['return_artifact'] or {}).values()]
        matches = [value for value in packages if value.get('context') == context_ref]
        package = matches[0] if len(matches) == 1 else {}
        if (package.get('context') != context_ref or not any(
                item['record_type'] == 'product' and item['logical_id'] == point['ref']['logical_id']
                and item['record'] == record for item in package.get('records', []))):
            raise ValueError('Product is absent from the admitted encoded return linked to the actual capture')
        capture = details.get('semantic_capture')
        if (capture is None or capture['codec'] != governed_semantic.CODEC
                or capture['encoded_return_blob_id'] not in (transaction['return_artifact'] or {})
                or capture['packet_blob_id'] != details['native']['packet_blob_id']
                or capture['invocation_id'] != details['invocation_id']):
            raise ValueError('Material lacks its exact raw semantic capture and encoded member linkage')
        token = {'context': copy.deepcopy(context_ref), 'logical_id': point['ref']['logical_id']}
        manifest = {'context': copy.deepcopy(context_ref),
                    'manifest_hash': details['native']['manifest_hash']}
        return record, token, manifest, assignment

    def _materials(self, point):
        record, token, manifest, assignment = self._captured(point)
        result = []
        for identifier in record['material']:
            raw = self.store._blob(identifier)
            if lc.blob(raw) != identifier:
                raise ValueError('Required domain material integrity failure')
            try:
                value = json.loads(raw,object_pairs_hook=content_spec._pairs,
                    parse_constant=lambda value: (_ for _ in ()).throw(ValueError('NONFINITE: ' + value)))
            except (json.JSONDecodeError,UnicodeDecodeError):
                continue
            if isinstance(value, dict):
                result.append((value, token, manifest, assignment))
        return result

    def _records(self):
        if self._indexed:
            return self._facts
        self._indexed = True
        state = self._state
        def add(point, reviewer, row):
            value, token, _, _ = row
            body = value.get('data', value) if reviewer else value.get('producer', value.get('data', {}))
            key = 'attestation' if reviewer or 'producer' in value else 'producer_attestation'
            if body.get(key) != token:
                return
            identity = lc.canonical(token)
            candidate = (point, reviewer, row)
            if identity in self._facts:
                previous = self._facts[identity]
                if previous is not None and previous[:2] == candidate[:2] and _digest(previous[2][0]) == _digest(value):
                    return
                self._facts[identity] = None
            else:
                self._facts[identity] = candidate
        for producer in self.producers:
            if not self._evaluate(producer)['qualified']:
                continue
            product = state.resolve(producer['ref'], 'product')
            for row in self._materials(producer):
                add(producer, False, row)
            for proof in state.proofs.values():
                if proof['subject'] != producer['ref']:
                    continue
                assessment_point = {'ref': proof['proof'], 'use_scope': proof['proof_use_scope']}
                if assessment_point not in self._evaluate(producer)['closure']:
                    continue
                assessment = state.resolve(proof['proof'], 'assessment')
                if (assessment['subject'] != producer['ref']
                        or assessment['verdict'] not in {'supported', 'supported_with_conditions', 'accepted'}):
                    continue
                for index,finding in enumerate(assessment['findings']):
                    point = state._dependency_point(assessment,'/findings/' + str(index),finding)
                    finding_record = state.resolve(finding, 'product')
                    related = {item['slot_id']: item['refs'] for item in finding_record['related']}
                    finding_assignment = state.resolve(finding_record['assignment'], 'assignment')
                    criteria = [refs for key,refs in related.items() if key.startswith('criterion:')]
                    if (point not in self._evaluate(producer)['closure']
                            or finding_record['product_kind'] != 'finding'
                            or related.get('subject') != [producer['ref']]
                            or criteria != [[finding_assignment['criteria']]]
                            or finding_assignment['responsibility'] not in {'reviewer', 'integration_reviewer', 'receiver'}
                            or not state._governing_input(point, live=True)):
                        continue
                    for row in self._materials(point):
                        producer_context = state.provenance[producer['ref']['version_id']]['context']
                        author_details = state.run_details[state.resolve(producer_context, 'context')['run_id']]
                        reviewer_details = state.run_details[state.resolve(row[1]['context'], 'context')['run_id']]
                        same_physical = all(author_details['native'][field] == reviewer_details['native'][field]
                                            for field in ('provider', 'handle'))
                        if (row[3]['assigned_actor'] == state.resolve(product['assignment'], 'assignment')['assigned_actor']
                                or same_physical):
                            continue
                        add(producer, True, row)
        return self._facts

    def verify(self, token):
        """Resolve a preissued token to actual exact producer/reviewer material.

        Args:
            token: Context reference and logical ID embedded before the return.
        Returns:
            Existing content-review callback fields, or None. Invocation expiry
            does not erase historical authorship; current core proof governs use.
        """
        try:
            with self.action():
                found = self._records().get(lc.canonical(token))
                if found is None:
                    return None
                producer, reviewer, (material, actual_token, manifest, assignment) = found
                if token != actual_token:
                    return None
                payload = copy.deepcopy(material)
                if reviewer:
                    review = payload.get('data', payload)
                    if review.pop('attestation', None) != token or review.get('context_manifest') != manifest:
                        return None
                    snapshot = review.get('semantic_hash', review.get('reviewed_digest'))
                elif isinstance(payload.get('producer'), dict):
                    if (payload['producer'].pop('attestation', None) != token
                            or payload['producer'].get('context_manifest') != manifest):
                        return None
                    snapshot = _digest(payload)
                elif isinstance(payload.get('data'), dict):
                    if payload['data'].pop('producer_attestation', None) != token:
                        return None
                    snapshot = _digest(payload)
                else:
                    return None
                context = self._state.resolve(actual_token['context'], 'context')
                details = self._state.run_details[context['run_id']]
                physical = {'provider': details['native']['provider'], 'handle': details['native']['handle']}
                return {'invocation': details['invocation_id'], 'physical_context': physical,
                        'raw_capture': details['semantic_capture']['raw_return_blob_id'],
                        'principal': self.store.engagement + ':' + assignment['assigned_actor'],
                        'reviewer': reviewer, 'subject_digest': _digest(payload),
                        'snapshot_digest': snapshot, 'context_digest': _digest(manifest)}
        except (ValueError, OSError, KeyError, TypeError):
            return None

    def publication_status(self, model, audience=None, operation='draft'):
        """Assess exact publication source against current Gen2 justification.

        Args:
            model: Complete original model; transport tokens remain in its bytes.
            audience: Requested audience, which must match its explicit audience.
            operation: draft requires qualification; accepted and release require
                their respective additional existing human permissions.
        Returns:
            Exact source use, current core facts and eligibility; grants nothing.
        Raises:
            ValueError: Unknown operation or a source not exactly host-bound.
        """
        if operation not in {'draft', 'accepted', 'release'}:
            raise ValueError('Unknown publication operation')
        with self.action():
            matches = [point for point in self.producers
                       if any(_digest(row[0]) == _digest(model) for row in self._materials(point))]
            if len(matches) != 1:
                raise ValueError('Publication source must match one exact admitted producer material')
            if audience is not None and audience != model.get('audience'):
                raise ValueError('Publication audience differs from the exact source')
            basis = self._evaluate(matches[0])
            eligible = basis['qualified'] and (operation == 'draft' or basis['accepted'])
            if operation == 'release':
                eligible = eligible and basis['release_eligible']
            return {'subject': matches[0], 'head': self._state.head, 'operation': operation,
                    'eligible': bool(eligible), 'qualified': basis['qualified'],
                    'accepted': basis['accepted'], 'release_eligible': basis['release_eligible'],
                    'reasons': copy.deepcopy(basis['reasons']), 'authority_granted': False}

    def fabric_resolver(self, entity, snapshot):
        """Check a commercial execution binding using current exact Gen2 products.

        Args:
            entity: ExecutionContract with a governed_binding UsePoint.
            snapshot: Canonical commercial graph with exact domain/claim versions.
        Returns:
            True only for exact immutable mapping material and qualified outputs.
            This is not acceptance, contract signature or release permission.
        """
        try:
            with self.action():
                data = entity['data']
                index = {item['version_id']: item for item in snapshot['entities']}
                domain = index[data['domain_contract_version']]
                claims = [index[key] for key in data['claim_ids']]
                fragments = [index[key] for key in data['fragment_ids']]
                if any(item['type'] != 'Fragment' for item in fragments):
                    return False
                outputs = [_point(item['data']['governed_output']) for item in fragments]
                binding = _point(data['governed_binding'])
                if domain['type'] != 'DomainContract' or any(item['type'] != 'Claim' for item in claims):
                    return False
                assignment = self._state.resolve(data['governed_assignment'], 'assignment')
                bound_record = self._state.resolve(binding['ref'], 'product')
                expected = {'domain_contract_version': domain['version_id'], 'domain_digest': _digest(domain),
                            'claim_ids': data['claim_ids'], 'claim_digests': [_digest(item) for item in claims],
                            'assignment': data['governed_assignment'], 'layer': data['layer'], 'outputs': outputs}
                if (assignment['owner']['layer'] != data['layer'] or not outputs
                        or bound_record['owner'] != assignment['owner']
                        or binding not in self.producers or not self._evaluate(binding)['qualified']):
                    return False
                for output in outputs:
                    record = self._state.resolve(output['ref'], 'product')
                    if (record['assignment'] != data['governed_assignment']
                            or output['use_scope'] != binding['use_scope']
                            or not self._evaluate(output)['qualified']):
                        return False
                return any(_digest(row[0]) == _digest(expected) for row in self._materials(binding))
        except (ValueError, OSError, KeyError, TypeError):
            return False

    def commercial_callbacks(self):
        """Return existing host callback slots; source JSON cannot provide trust.

        Returns:
            Identity and exact binding callbacks. Physical assurance is not
            fabricated; actual explicit policy controls require their own proof.
        """
        return {'identity_verifier': self.verify, 'fabric_resolver': self.fabric_resolver}

def commercial_mapping(snapshot, contract_id, assignment, layer, outputs):
    """Build exact domain binding bytes for an ordinary actual producer return.

    Args:
        snapshot: Canonical commercial graph; this function grants no trust.
        contract_id: Exact DomainContract version identifier.
        assignment: Exact producing assignment reference.
        layer: Its declared layer, checked against the Store during resolution.
        outputs: Exact output UsePoints, later checked by the shared evaluator.
    Returns:
        Mapping to store as ordinary producer material, never a signed append.
    Raises:
        ValueError, KeyError: Domain/claim/output identifiers are incomplete.
    """
    index = {item['version_id']: item for item in snapshot['entities']}
    contract = index[contract_id]
    claims = list(snapshot.get('active_claims', []))
    if contract['type'] != 'DomainContract' or not claims or not outputs:
        raise ValueError('Exact domain, active claims and outputs required')
    return {'domain_contract_version': contract_id, 'domain_digest': _digest(contract),
            'claim_ids': claims, 'claim_digests': [_digest(index[key]) for key in claims],
            'assignment': copy.deepcopy(assignment), 'layer': layer,
            'outputs': [_point(value) for value in outputs]}


def add_arguments(parser, operations=('draft','accepted','release')):
    """Add internal host locator arguments to an existing consumer CLI parser.

    Args:
        parser: Existing argparse parser; no new user-facing workflow is created.
        operations: Modes actually implemented by this consumer; readiness and
            receiving checks do not silently accept publication/release requests.
    """
    parser.add_argument('--governed-journal', type=Path)
    parser.add_argument('--governed-engagement')
    parser.add_argument('--governed-uses', type=Path)
    parser.add_argument('--governed-operation', choices=operations, default='draft')
    parser.add_argument('--governed-authority-use', type=Path)


def from_arguments(args):
    """Open a host-selected domain adapter from existing internal CLI arguments.

    Args:
        args: Parsed arguments added by add_arguments, never source-model policy.
    Returns:
        Adapter and optional existing GovernedAuthority, or (None, None) for
        ordinary ungoverned draft work. Source fields cannot opt out of a pin.
    Raises:
        ValueError, OSError: Partial locators, missing history or invalid uses.
    """
    values = [args.governed_journal, args.governed_engagement, args.governed_uses]
    if not any(values):
        if args.governed_authority_use or args.governed_operation != 'draft':
            raise ValueError('A governed permission request requires an existing exact host pin')
        return None, None
    if not all(values) or not args.governed_journal.is_file():
        raise ValueError('Complete existing host journal, engagement and uses required')
    store = lc.Store(args.governed_journal, args.governed_engagement)
    uses = lc.loads(args.governed_uses.read_bytes())
    adapter = GovernedDomain(store, uses if isinstance(uses, list) else [uses])
    authority = None
    if args.governed_authority_use:
        from content_lint import GovernedAuthority
        point = _point(lc.loads(args.governed_authority_use.read_bytes()))
        authority = GovernedAuthority(store, point['ref'], use_scope=point['use_scope'])
    return adapter, authority
