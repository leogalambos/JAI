# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Viewer indexes of recorded effects, without canonical replay or adjudication.

Only visualization state is projected: immutable manifests, origin fields,
recorded use transitions and structural dependency selectors. No signature,
chain, permission, deadline or decision-validity predicate is evaluated.
"""
import base64
import json
import hashlib
import unicodedata


class _RecordedFormat:
    """Pure format-9 identity serialization and structural reference scanning."""
    PROTOCOL = 'jai.governed-delivery/1'

    @staticmethod
    def normal(value):
        """Normalize immutable identity JSON without evaluating any journal claim."""
        if value is None or type(value) in (bool, int): return value
        if isinstance(value, str): return unicodedata.normalize('NFC', value)
        if isinstance(value, list): return [_RecordedFormat.normal(item) for item in value]
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if not isinstance(key, str): raise ValueError('Invalid identity key')
                key = _RecordedFormat.normal(key)
                if key in result: raise ValueError('Duplicate normalized identity key')
                result[key] = _RecordedFormat.normal(item)
            return result
        raise ValueError('Unsupported immutable identity value')

    @staticmethod
    def canonical(value):
        """Serialize the published integer-only immutable identifier format."""
        return json.dumps(_RecordedFormat.normal(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

    @staticmethod
    def version_id(value):
        """Compute the manifest's display identity, without verifying a chain."""
        return hashlib.sha256(b'jai.lifecycle.version.v2\0' + _RecordedFormat.canonical(value)).hexdigest()

    @staticmethod
    def _reference_paths(value, path=''):
        if isinstance(value, dict):
            if set(value) == {'engagement', 'scope', 'logical_id', 'version_id'}: yield path, value
            else:
                for key in sorted(value):
                    yield from _RecordedFormat._reference_paths(value[key], path + '/' + key.replace('~', '~0').replace('/', '~1'))
        elif isinstance(value, list):
            for index, child in enumerate(value): yield from _RecordedFormat._reference_paths(child, path + '/' + str(index))

    @staticmethod
    def _causal_reference_paths(record):
        for path, reference in _RecordedFormat._reference_paths(record):
            parts = path.split('/')
            if path.startswith('/handling/') or record.get('product_kind') == 'escalation' and path.startswith(('/episode/', '/related/')): continue
            if ('issued_under' in record and len(parts) == 5 and parts[1] == 'effects' and parts[3] == 'targets'
                    and record['effects'][int(parts[2])].get('operation') == 'read'): continue
            yield path, reference


class _RecordedFindings:
    """Pure recorded Findings operation reduction with an explicit display policy."""
    MAX_ROUNDS = 3

    def state(self, events):
        """Project recorded event state without verifying its chain or actors."""
        result = {}
        for event in events:
            data = event['data']; operation = data['op']
            if operation == 'add':
                for value in data['findings']:
                    result[value['id']] = dict(value, state='open', rounds=0, resolver=None, history=[], reviewer=data['reviewer'], target=data.get('target'))
                continue
            value = result[data['id']]
            value['history'].append({'op': operation, 'by': data.get('by'), 'note': data.get('note') or data.get('rationale'), 'ts': event['ts']})
            if operation == 'resolve': value['state'], value['resolver'] = 'resolved', data['by']
            elif operation == 'verify':
                if data['ok']: value['state'] = 'verified'
                else:
                    value['rounds'] += 1
                    value['state'] = 'stuck' if value['rounds'] >= self.MAX_ROUNDS else 'open'
            elif operation == 'withdraw': value['state'] = 'withdrawn'
            elif operation == 'accept-risk': value['state'], value['expires'] = 'accepted', data.get('expires')
        return result


def _proof_fields(transaction):
    # These are displayed claims from a recorded envelope, never a trust lookup.
    encoded = transaction.get('authority_proof')
    if not isinstance(encoded, str): return None
    try:
        wrapper = json.loads(base64.b64decode(encoded, validate=True))
        purpose = wrapper['request']['kind']; key = wrapper['receipt']['key_id']
        if isinstance(purpose, str) and isinstance(key, str): return {'purpose': purpose, 'key_id': key}
    except (ValueError, KeyError, TypeError): pass
    return None


class _RecordedProjection:
    """Minimal ordered record index; statuses are recorded/projection values only."""
    def __init__(self, lifecycle, previous=None):
        self.lc = _RecordedFormat
        self.transactions = list(previous.transactions) if previous else []
        for name in ('versions', 'provenance', 'states', 'reliance', 'requirements', 'sources', 'rows_by_version'):
            setattr(self, name, dict(getattr(previous, name)) if previous else {})
        self.scope = previous.scope if previous else 'default'
        self.initialized = previous.initialized if previous else False
        self.head = previous.head if previous else '0' * 64

    def _reference(self, identifier):
        value = self.versions[identifier]
        return {'engagement': value['content']['engagement'], 'scope': value['content']['scope'],
                'logical_id': value['logical_id'], 'version_id': identifier}

    def _point(self, reference, scope=None):
        return {'ref': reference, 'use_scope': self.scope if scope is None else scope}

    def _record(self, reference):
        if not isinstance(reference, dict): raise ValueError('Unreadable recorded reference')
        value = self.versions.get(reference.get('version_id'))
        return value['content']['record'] if value is not None else None

    def _assignment_use(self, assignment, path, reference):
        selectors = {item['at']: item['use_scope'] for item in assignment.get('input_uses', [])}
        if path == '/routing/policy':
            return self._point(reference, self.transactions[0]['operations'][0]['data']['message']['scope'] if self.transactions else self.scope)
        if path == '/issued_under':
            parent = self._record(reference)
            return self._point(reference, parent.get('use_scope', self.scope) if parent else self.scope)
        return self._point(reference, selectors.get(path, assignment.get('use_scope', self.scope)))

    def _subject_use(self, subject, assignment):
        matches = [self._assignment_use(assignment, path, ref) for path, ref in self.lc._reference_paths(assignment)
                   if path.startswith('/inputs/') and ref == subject]
        return matches[0] if matches else self._point(subject, assignment.get('use_scope', self.scope))

    def _dependency_point(self, record, path, reference):
        assignment = record if 'issued_under' in record else self._record(record['assignment']) if record.get('assignment') else None
        if path.startswith('/assessed_closure/'):
            return record['assessed_closure'][int(path.split('/')[2])]
        if assignment is record: return self._assignment_use(assignment, path, reference)
        if assignment is not None:
            if path == '/assignment': return self._point(reference, assignment.get('use_scope', self.scope))
            paths = dict(self.lc._causal_reference_paths(assignment))
            if path in paths and paths[path] == reference: return self._assignment_use(assignment, path, reference)
            matches = [self._assignment_use(assignment, at, bound) for at, bound in paths.items() if bound == reference and at != '/issued_under']
            return matches[0] if len({item['use_scope'] for item in matches}) == 1 else self._point(reference, assignment.get('use_scope', self.scope))
        return self._point(reference)

    def _dependencies(self, record):
        points = []
        for path, reference in self.lc._causal_reference_paths(record):
            point = self._dependency_point(record, path, reference)
            if point not in points: points.append(point)
        return sorted(points, key=self.lc.canonical)

    def _governing_dependencies(self, point, active=None):
        key = point['use_scope'], point['ref']['version_id']
        active = set() if active is None else active
        if key in active: return []
        active.add(key)
        try:
            record = self._record(point['ref'])
            if record is None: return []
            family = self.versions[key[1]]['kind']
            if family == 'delivery.decision': return list(self.reliance.get(key, []))
            assignment = record if family == 'delivery.assignment' else self._record(record['assignment']) if record.get('assignment') else None
            inspection = {'reviewer': 'assessed-subject', 'integration_reviewer': 'assessed-subject', 'receiver': 'incoming_handoff', 'measurement': 'measured-subject'}
            points = []; previous = self.scope; self.scope = point['use_scope']
            try:
                for path, reference in self.lc._causal_reference_paths(record):
                    keep = False
                    if family == 'delivery.source': keep = path.startswith('/inherited/')
                    elif family == 'delivery.profile': keep = path.startswith('/source_profiles/')
                    elif family == 'delivery.assignment': keep = path in {'/profile', '/criteria', '/routing/policy'} or path.startswith(('/inherited/', '/inputs/', '/effects/'))
                    elif family == 'delivery.context': keep = path in {'/assignment', '/profile', '/execution/selection', '/speculation'} or path.startswith('/inputs/')
                    elif family == 'delivery.product':
                        keep = path == '/profile' or path.startswith(('/inputs/', '/evidence/', '/related/', '/outcome/evidence/'))
                        if record.get('product_kind') == 'finding' and path.startswith('/related/'):
                            keep = record['related'][int(path.split('/')[2])]['slot_id'] != 'subject'
                    elif family == 'delivery.assessment': keep = path in {'/profile', '/criteria'} or path.startswith(('/conditions/', '/findings/'))
                    parts = path.split('/')
                    if keep and assignment is not None and len(parts) == 5 and parts[1] == 'inputs' and parts[3] == 'refs':
                        keep = assignment['inputs'][int(parts[2])]['slot_id'] != inspection.get(assignment.get('responsibility'))
                    if keep:
                        dependency = self._dependency_point(record, path, reference)
                        if dependency not in points: points.append(dependency)
                if family == 'delivery.assessment' and assignment is not None:
                    reviewer = self._point(record['assignment'], assignment.get('use_scope', self.scope))
                    subject = self._subject_use(record['subject'], assignment)
                    for dependency in self._governing_dependencies(reviewer, active) + self._governing_dependencies(subject, active):
                        if dependency not in points: points.append(dependency)
                for requirement in self.requirements.get(key, []):
                    if requirement['point'] not in points: points.append(requirement['point'])
                return points
            finally: self.scope = previous
        finally: active.remove(key)

    def _ensure_use(self, point, active=None):
        key = point['use_scope'], point['ref']['version_id']
        active = set() if active is None else active
        if key in self.states or key in active or key[1] not in self.versions: return
        active.add(key); previous = self.scope; self.scope = point['use_scope']
        try:
            value = self.versions[key[1]]; record = value['content']['record']
            dependencies = self._dependencies(record)
            for dependency in dependencies: self._ensure_use(dependency, active)
            self.reliance[key] = dependencies
            primitive = value['kind'] in {'delivery.source', 'delivery.profile'}
            if value['kind'] == 'delivery.source' and record.get('owner', {}).get('kind') == 'authority' and self.initialized:
                primitive = point['ref'] in [ref for (scope, _), ref in self.sources.items() if scope == point['use_scope']]
            # This is the format's implicit display state, not a new validity
            # judgment; the source summary always identifies recorded projection.
            self.states[key] = {'validity': 'valid' if primitive else 'pending', 'applicable': primitive}
        finally: self.scope = previous; active.remove(key)

    def append(self, transaction):
        """Index one structurally readable transaction's recorded effects.

        No chain, signature, authorization or allowed-transition predicate is
        checked. Other effect fields remain in the original captured record.
        """
        data = transaction['operations'][0]['data']; message = data['message']
        if (not isinstance(message.get('scope'), str) or type(transaction.get('sequence')) is not int
                or transaction['sequence'] < 0 or not isinstance(transaction.get('hash'), str)):
            raise ValueError('Unreadable recorded transaction fields')
        self.scope = message['scope']
        ordinal = len(self.transactions)
        sequence = transaction['sequence']
        for effect in data['effects']:
            if not isinstance(effect, dict) or not isinstance(effect.get('op'), str): raise ValueError('Unreadable recorded effect')
            operation = effect['op']
            if operation in {'register', 'decision-record'}:
                value = effect['manifest']
                if (not isinstance(value, dict) or value.get('schema') != 'jai.lifecycle.manifest/2'
                        or value.get('kind') not in {'delivery.source', 'delivery.profile', 'delivery.assignment', 'delivery.context', 'delivery.product', 'delivery.assessment', 'delivery.decision'}
                        or not isinstance(value.get('logical_id'), str) or not isinstance(value.get('content'), dict)
                        or not isinstance(value['content'].get('record'), dict)
                        or not all(isinstance(value['content'].get(field), str) for field in ('engagement', 'scope'))
                        or not isinstance(effect.get('dependencies'), list)):
                    raise ValueError('Unreadable recorded manifest')
                identifier = self.lc.version_id(value)
                self.versions[identifier] = value; self.rows_by_version[identifier] = ordinal
                origin = effect['origin'] if operation == 'register' else message['sender']
                context = effect['context'] if operation == 'register' else message['context']
                provenance = {'origin': origin, 'context': context, 'sequence': sequence}
                authority = _proof_fields(transaction) if operation == 'decision-record' else None
                if authority is not None: provenance['authority'] = authority
                self.provenance[identifier] = provenance
                key = effect.get('use_scope', message['scope']), identifier
                for dependency in effect['dependencies']: self._ensure_use(dependency)
                self.reliance[key] = effect['dependencies']
                self.states[key] = {'validity': 'valid' if operation == 'decision-record' else 'pending', 'applicable': operation == 'decision-record'}
            elif operation == 'qualify':
                key = effect.get('use_scope', message['scope']), effect['subject']
                if key not in self.states and key[1] in self.versions: self._ensure_use(self._point(self._reference(key[1]), key[0]))
                self.states[key] = {'validity': 'valid', 'applicable': effect.get('applicable', True)}
                if 'requirements' in effect: self.requirements[key] = effect['requirements']
            elif operation in {'cancel', 'withdraw'}:
                for point in effect['subjects']:
                    key = point['use_scope'], point['ref']['version_id']
                    if operation == 'cancel': self.states[key] = {'validity': 'invalid', 'applicable': False}
                    elif key in self.states: self.states[key] = {**self.states[key], 'applicable': False}
            elif operation == 'bootstrap-use': self._ensure_use(effect['point'])
            elif operation == 'initialize': self.initialized = True
            elif operation == 'initial-source': self.sources[(effect['use_scope'], effect['source']['logical_id'])] = effect['source']
            elif operation == 'source-select':
                for key, reference in list(self.sources.items()):
                    if key[0] == message['scope'] and reference == effect['previous']: self.sources[key] = effect['replacement']
        self.transactions.append(transaction); self.head = transaction['hash']
