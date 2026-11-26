# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Validate and select scoped methods for offline technical security evidence."""

from dataclasses import dataclass
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path


_TUPLE_FIELDS = ('product', 'edition', 'version', 'deployment')
_STATES = {'conforming', 'deviation'}


def _nonempty_fields(record, fields):
    return all(isinstance(record.get(field), str) and record[field].strip() for field in fields)


def _index(rows, label):
    result = {}
    for row in rows:
        if not isinstance(row, dict) or not _nonempty_fields(row, ('id',)) or row['id'] in result:
            raise ValueError(f'Duplicate or invalid {label} identifier')
        result[row['id']] = row
    return result


def _scope_tuple(record, aliases):
    if not _nonempty_fields(record, _TUPLE_FIELDS):
        return None
    return (aliases.get(record['product'].casefold(), record['product']),
            *(record[field] for field in _TUPLE_FIELDS[1:]))


@dataclass(frozen=True)
class MethodManifest:
    """Validated method indexes for an immutable, digest-bound input snapshot.

    Attributes:
        revision: Version declared by the manifest author.
        digest: SHA-256 of exact loaded bytes.
        formats: Indexed normalized evidence definitions.
        criteria: Indexed examination criteria and applicability.
        methods: Indexed method declarations.
        products: Map from exact product scope to method ID.
        aliases: Map from case-insensitive product labels to canonical IDs.
    """

    revision: str
    digest: str
    formats: dict
    criteria: dict
    methods: dict
    products: dict
    aliases: dict

    def assess(self, assets, claims, observations, interfaces=()):
        """Resolve methods and evidence sufficiency without performing a test.

        Args:
            assets: Inventory rows keyed by ID, with exact product identity.
            claims: Planned questions with criterion, asset IDs and receiving
                duty. Protocol-dependent questions also identify an interface.
            observations: Already interpreted observations, each bound to a
                criterion, exact subject set, format and source revision.
            interfaces: Attributable protocol assertions per named interface.

        Returns:
            Manifest references, per-asset selection, per-question disposition
            and mandatory questions omitted from the assessment plan.
        Raises:
            ValueError: Invalid or duplicate record identifiers or malformed
                scope.
        """
        inventory = _index(assets, 'asset')
        questions = _index(claims, 'claim')
        observations = _index(observations, 'observation')
        observations_by_subject = {}
        for row in observations.values():
            if not _nonempty_fields(row, ('criterion',)):
                raise ValueError('An observation requires a criterion')
            observations_by_subject.setdefault((_subject(row), row['criterion']), []).append(row)
        interfaces = list(interfaces)
        selections = {
            key: self.products.get(_scope_tuple(row, self.aliases))
            for key, row in inventory.items()
            if _nonempty_fields(row, ('source', 'revision'))
        }
        required = {
            (asset, criterion)
            for asset, method in selections.items() if method
            for criterion in self.methods[method]['criteria']
            if self.criteria[criterion]['mandatory'] and not self.criteria[criterion].get('joint')
        }
        pending = required.copy()
        results = {}
        for key, question in questions.items():
            subject = _subject(question)
            if not _nonempty_fields(question, ('criterion', 'receiving_duty')):
                raise ValueError('A claim requires a criterion and receiving duty')
            criterion = question['criterion']
            if len(subject) == 1:
                pending.discard((next(iter(subject)), criterion))
            scoped_observations = observations_by_subject.get((subject, criterion), [])
            revisions = {asset: inventory[asset]['revision'] for asset in subject if asset in selections}
            result = self._assess_claim(question, subject, selections, scoped_observations,
                                        interfaces, revisions)
            definition = self.criteria.get(criterion, {})
            results[key] = {'assets': sorted(subject), 'criterion': criterion,
                            'criterion_revision': definition.get('revision'),
                            'assessment_question': definition.get('question'),
                            'attack_context': definition.get('attack_context'),
                            'receiving_duty': question['receiving_duty'], **result}
            scope_field = definition.get('scope_field')
            if scope_field:
                results[key][scope_field] = question.get(scope_field)
            if definition.get('evidence_routes'):
                results[key]['policy_revision'] = question.get('policy_revision')
            if _nonempty_fields(question, ('interface',)):
                results[key]['interface'] = question['interface']
        return {'manifest_revision': self.revision, 'manifest_sha256': self.digest,
                'asset_methods': {asset: selections.get(asset) for asset in inventory},
                'claims': results,
                'missing_mandatory_questions': [
                    {'asset': asset, 'criterion': criterion}
                    for asset, criterion in sorted(pending)
                ]}

    def _assess_claim(self, claim, subject, selections, observations, interfaces, revisions):
        criterion = self.criteria.get(claim['criterion'])
        selected = {selections.get(asset) for asset in subject}
        if (criterion is None or None in selected
                or any(claim['criterion'] not in self.methods[method]['criteria'] for method in selected)):
            return {'status': 'pending', 'reason': 'unsupported-scope'}
        if criterion.get('joint') and (len(subject) < 2 or len(selected) < 2):
            return {'status': 'pending', 'reason': 'shared-scope-required'}
        if not criterion.get('joint') and len(subject) != 1:
            return {'status': 'pending', 'reason': 'single-asset-scope-required'}
        interface = _resolve_interface(claim, subject, criterion, interfaces)
        if interface is False:
            return {'status': 'pending', 'reason': 'unknown-or-conflicting-interface'}

        scope_field = criterion.get('scope_field')
        if scope_field and not _nonempty_fields(claim, (scope_field,)):
            return {'status': 'pending', 'reason': 'claim-scope-required'}
        evidence = [
            row for row in observations
            if row.get('format') in criterion['formats']
            and row.get('format_revision') == self.formats[row['format']]['revision']
            and _nonempty_fields(row, ('source', 'revision'))
            and row.get('asset_revisions') == revisions
            and row.get('criterion_revision') == criterion['revision']
            and (not scope_field or row.get(scope_field) == claim[scope_field])
            and (interface is None or (row.get('interface') == claim.get('interface')
                                       and row.get('interface_evidence') == interface))
        ]
        routes = criterion.get('evidence_routes')
        if routes:
            if not _nonempty_fields(claim, ('policy_revision',)):
                return {'status': 'pending', 'reason': 'policy-revision-required'}
            known_roles = {role for route in routes for role in route['inputs']}
            evidence = [row for row in evidence
                        if row.get('policy_revision') == claim['policy_revision']
                        and isinstance(row.get('evidence_role'), str)
                        and row['evidence_role'] in known_roles]
            policy_digests = set()
            if criterion.get('runtime_policy_binding'):
                policy_digests = {row.get('expected_roles_sha256') for row in evidence
                                  if row['evidence_role'] == 'policy'
                                  and isinstance(row.get('expected_roles_sha256'), str)
                                  and len(row['expected_roles_sha256']) == 64
                                  and all(char in '0123456789abcdef' for char in row['expected_roles_sha256'])
                                  and row.get('status') == 'conforming'}
                evidence = [row for row in evidence if row['evidence_role'] != 'runtime'
                            or (len(policy_digests) == 1
                                and isinstance(row.get('expected_roles_sha256'), str)
                                and row['expected_roles_sha256'] in policy_digests)]
            mapping_digests = {row['membership_scope_sha256'] for row in evidence
                               if row['evidence_role'] == 'mapping'
                               and _sha256_value(row.get('membership_scope_sha256'))}
            if mapping_digests or any('membership_scope_sha256' in row for row in evidence):
                evidence = [row for row in evidence if row['evidence_role'] != 'identity'
                            or (len(mapping_digests) == 1
                                and _sha256_value(row.get('membership_scope_sha256'))
                                and row['membership_scope_sha256'] in mapping_digests)]
            baseline_roles = set(criterion.get('baseline_roles', []))
            accepted_baselines = {row['evidence_role'] for row in evidence
                                  if row['evidence_role'] in baseline_roles and row.get('status') == 'conforming'}
            rejected_baselines = {row['evidence_role'] for row in evidence
                                  if row['evidence_role'] in baseline_roles and row.get('status') != 'conforming'}
            available = (accepted_baselines - rejected_baselines) | {
                row['evidence_role'] for row in evidence
                if row['evidence_role'] not in baseline_roles
                and isinstance(row.get('status'), str) and row['status'] in _STATES}
            route_options = [{'id': route['id'], 'missing': {
                role: action for role, action in route['inputs'].items() if role not in available}}
                             for route in routes]
            if all(option['missing'] for option in route_options):
                return {'status': 'pending', 'reason': 'evidence-route-incomplete',
                        'evidence_routes': route_options,
                        **({'policy_roles_sha256': next(iter(policy_digests))}
                           if len(policy_digests) == 1 else {}),
                        **({'mapping_membership_sha256': next(iter(mapping_digests))}
                           if len(mapping_digests) == 1 else {})}
        if any(not isinstance(row.get('status'), str) for row in evidence):
            return {'status': 'pending', 'reason': 'missing-or-conflicting-evidence'}
        states = {row['status'] for row in evidence
                  if not routes or row['evidence_role'] not in baseline_roles}
        if len(states) > 1 and states <= _STATES:
            return {'status': 'pending', 'reason': 'conflicting-evidence'}
        if len(states) != 1 or not states <= _STATES:
            return {'status': 'pending', 'reason': 'missing-or-conflicting-evidence'}
        return {'status': states.pop(), 'methods': sorted(selected),
                **({'completed_evidence_routes': [option['id'] for option in route_options
                                                  if not option['missing']]} if routes else {}),
                'evidence': [{'id': row['id'], 'source': row['source'], 'revision': row['revision'],
                              **({'evidence_role': row['evidence_role']} if routes else {})}
                             for row in evidence],
                'interface_evidence': interface or []}


def _sha256_value(value):
    return (isinstance(value, str) and len(value) == 64
            and all(char in '0123456789abcdef' for char in value))


def _subject(row, field='assets'):
    values = row.get(field)
    if not isinstance(values, list) or not values or not all(isinstance(v, str) and v for v in values):
        raise ValueError(f'Invalid subject field: {field}')
    if len(values) != len(set(values)):
        raise ValueError(f'Duplicate subject in field: {field}')
    return frozenset(values)


def _resolve_interface(claim, subject, criterion, interfaces):
    supported = criterion.get('protocols')
    if not supported:
        return None
    if not _nonempty_fields(claim, ('interface',)):
        return False
    assertions = [row for row in interfaces if row.get('interface') == claim['interface']]
    if not assertions or any(
        not _nonempty_fields(row, ('interface', 'protocol', 'profile', 'source', 'revision'))
        or not isinstance(row.get('endpoints'), list)
        or sorted(row['endpoints'], key=str) != sorted(subject)
        for row in assertions
    ):
        return False
    identities = {(row['protocol'], row['profile']) for row in assertions}
    if len(identities) != 1 or next(iter(identities)) not in {
        (row['protocol'], row['profile']) for row in supported
    }:
        return False
    return [{'source': source, 'revision': revision} for source, revision in
            sorted({(row['source'], row['revision']) for row in assertions})]


def load_method_manifest(path):
    """Load JSON declarations and reject inconsistent availability claims.

    Args:
        path: Path to the method manifest or previously bounded manifest bytes.
    Returns:
        A digest-bound MethodManifest for offline selection.
    Raises:
        OSError: The manifest cannot be read.
        ValueError: JSON or schema, identifier, alias, or reference validation
            fails.
    """
    raw = path if isinstance(path, bytes) else Path(path).read_bytes()
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get('schema') != 'jai.technical-security-evidence-methods/v1':
        raise ValueError('Invalid technical security evidence manifest schema')
    if not _nonempty_fields(data, ('revision',)):
        raise ValueError('Missing method-manifest revision')
    try:
        formats = _index(data['evidence_formats'], 'evidence format')
        criteria = _index(data['criteria'], 'criterion')
        methods = _index(data['methods'], 'method')
        products = _load_products(data['products'], methods)
        aliases = _load_aliases(data['aliases'], products)
        for row in formats.values():
            if not _nonempty_fields(row, ('revision', 'description')):
                raise ValueError('Invalid evidence format declaration')
        for row in criteria.values():
            _validate_criterion(row, formats)
        for row in methods.values():
            if not (_nonempty_fields(row, ('family', 'revision', 'qualification'))
                    and row['criteria'] and set(row['criteria']) <= criteria.keys()):
                raise ValueError('Invalid method declaration')
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Malformed method manifest declaration') from exc
    return MethodManifest(data['revision'], hashlib.sha256(raw).hexdigest(),
                          formats, criteria, methods, products, aliases)


def _validate_criterion(row, formats):
    if not (_nonempty_fields(row, ('revision', 'question'))
            and isinstance(row['mandatory'], bool)
            and row.get('scope_field') in (None, 'channel', 'role_mapping', 'identity_scope')
            and ('evidence_request' not in row or _nonempty_fields(row, ('evidence_request',)))
            and row['formats'] and set(row['formats']) <= formats.keys()
            and all(_nonempty_fields(identity, ('protocol', 'profile'))
                    for identity in row.get('protocols', []))):
        raise ValueError('Invalid criterion declaration')
    if 'evidence_routes' in row:
        routes = row['evidence_routes']
        if (not isinstance(routes, list) or not routes or not row.get('scope_field')
                or any(not isinstance(route, dict) or not _nonempty_fields(route, ('id',))
                       or not isinstance(route.get('inputs'), dict) or not route['inputs']
                       or any(not isinstance(role, str) or not role.strip()
                              or not isinstance(action, str) or not action.strip()
                              for role, action in route['inputs'].items())
                       for route in routes)
                or len({route['id'] for route in routes}) != len(routes)):
            raise ValueError('Invalid evidence route declaration')
        if 'baseline_roles' in row:
            baselines = row['baseline_roles']
            if (not isinstance(baselines, list) or any(not isinstance(role, str) for role in baselines)
                    or len(set(baselines)) != len(baselines)
                    or any(not set(baselines) < route['inputs'].keys() for route in routes)):
                raise ValueError('Invalid baseline evidence roles')
    elif 'baseline_roles' in row:
        raise ValueError('Baseline evidence roles require declared routes')
    if 'runtime_policy_binding' in row:
        runtime = [route['inputs'] for route in row.get('evidence_routes', [])
                   if 'runtime' in route['inputs']]
        if (row['runtime_policy_binding'] is not True or row.get('baseline_roles') != ['policy']
                or not runtime or any('policy' not in roles for roles in runtime)):
            raise ValueError('Invalid runtime policy binding')



def _load_products(rows, methods):
    products = {}
    for row in rows:
        key = _scope_tuple(row, {})
        if (key is None or key in products or row['method'] not in methods
                or methods[row['method']]['qualification'] != row['qualification']):
            raise ValueError('Invalid or duplicate product method scope')
        products[key] = row['method']
    return products


def _load_aliases(rows, products):
    product_names = {scope[0] for scope in products}
    canonical = {name.casefold(): name for name in product_names}
    if len(canonical) != len(product_names):
        raise ValueError('Ambiguous canonical product names')
    aliases = canonical.copy()
    for row in rows:
        if not _nonempty_fields(row, ('label', 'product')):
            raise ValueError('Invalid product alias')
        label = row['label'].casefold()
        if label in aliases or row['product'] not in product_names:
            raise ValueError('Duplicate, ambiguous or unknown product alias')
        aliases[label] = row['product']
    return aliases


def evaluate_referral_precondition(referral, permissions, *, now):
    """Check exact scope and validity of an externally verified permission.

    Args:
        referral: Exact report digest, finding, recipient, scope, purpose and
            permission identifier.
        permissions: Permission records already verified by the caller's
            authority boundary, with the same binding and an expiry.
        now: Timezone-aware comparison instant, supplied by the caller.
    Returns:
        Eligibility or a held disposition. Eligibility is context evidence for
        the caller's transfer boundary and does not issue permission.
    Raises:
        ValueError: The comparison clock is missing timezone information.
    """
    if now.utcoffset() is None:
        raise ValueError('Referral clock requires a timezone')
    binding = ('report_sha256', 'finding', 'recipient', 'scope', 'purpose')
    if not _nonempty_fields(referral, (*binding, 'permission')):
        return 'held-invalid-referral-binding'
    candidates = [row for row in permissions if row.get('id') == referral['permission']]
    if len(candidates) != 1:
        return 'held-missing-or-ambiguous-permission'
    permission = candidates[0]
    if any(permission.get(field) != referral[field] for field in binding):
        return 'held-out-of-scope'
    if permission.get('status') != 'active':
        return 'held-inactive-permission'
    try:
        expiry = datetime.fromisoformat(permission.get('expires_at', ''))
        if expiry.utcoffset() is None:
            return 'held-invalid-expiry'
    except (TypeError, ValueError):
        return 'held-invalid-expiry'
    return 'eligible' if now < expiry else 'held-expired-permission'


def main(argv=None):
    """Write an offline evidence disposition as JSON.

    Args:
        argv: Optional arguments with manifest and supplied intake files.
    Returns:
        Zero after producing the disposition.
    Raises:
        OSError, ValueError: The manifest or intake cannot be read or validated.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('intake', type=Path)
    args = parser.parse_args(argv)
    manifest = load_method_manifest(args.manifest)
    raw = args.intake.read_bytes()
    data = json.loads(raw)
    result = manifest.assess(data['assets'], data['claims'], data['observations'],
                             data.get('interfaces', []))
    result['intake_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
