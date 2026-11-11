# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Viewer-only recorded-data projection over retained captures, with bounded facts.

The module projects recorded effects without canonical verification or authority
assessment. It never calls a source writer or project-loaded code.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
import time
import uuid

from facts_spool import _Budget, _Pool, _Spool
from recorded_projection import _RecordedProjection, _RecordedFormat, _RecordedFindings

WIRE = 'jai.fabric-explorer.canonical-reader/1'
ADAPTERS = {family: 'jai.fabric-explorer.' + family + '/1' for family in ('fabric', 'findings', 'audit')}
RECORD = 100 * 1024 * 1024
TOTAL = 1024 * 1024 * 1024
PAGE = 256 * 1024
CHUNK = 1024 * 1024
INLINE = 256 * 1024


class SemanticReadError(ValueError):
    """Redacted source failure with a bounded precise source/record locator.

    Args:
        code: Fixed viewer diagnostic category, never native exception text.
        source_id: Admitted opaque source identifier, or None before selection.
        pointer: Exact relative JSON pointer when known.
        sequence: Exact ledger-local decimal sequence when known.
    """
    def __init__(self, code, source_id=None, pointer='', sequence=None):
        super().__init__('Selected file changed or was replaced; reopen sources to admit the new file.' if code == 'source-changed' else 'Selected source could not be imported.')
        self.compatibility = []
        self.report = None
        self.diagnostic = {'code': code, 'message': str(self), 'sourceId': source_id,
                           'pointer': pointer, 'sequence': sequence}


def _tag(value, depth=0):
    if value is None: return {'type': 'null'}
    if isinstance(value, bool): return {'type': 'boolean', 'value': value}
    if isinstance(value, str): return {'type': 'string', 'value': value}
    if isinstance(value, int): return {'type': 'integer', 'value': str(value)}
    if isinstance(value, float): return {'type': 'float64', 'bits': struct.pack('>d', value).hex()}
    if depth >= 64: raise SemanticReadError('resource-limit')
    if isinstance(value, (list, tuple)):
        return {'type': 'array', 'items': [_tag(item, depth + 1) for item in value]}
    if isinstance(value, dict):
        return {'type': 'object', 'entries': [{'key': key, 'value': _tag(item, depth + 1)} for key, item in value.items()]}
    raise SemanticReadError('read-failed')


def _encoded(value):
    # Match the actual UTF-8 wire bytes; isolated surrogates remain JSON escapes.
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8', 'backslashreplace')


def _preflight(line):
    """Bound the original physical row, then scan JSON structure without outer padding."""
    if len(line.rstrip(b'\r\n')) > RECORD: raise SemanticReadError('resource-limit')
    depth = 0; quoted = False; escaped = False
    # Record parsing still receives the original bytes. Only the structural
    # scan skips outer JSON whitespace; quoted content and the raw limit stay exact.
    for char in line.strip(b' \t\r\n'):
        if quoted:
            if escaped: escaped = False
            elif char == 92: escaped = True
            elif char == 34: quoted = False
        elif char == 34: quoted = True
        elif char in (91, 123):
            depth += 1
            if depth > 64: raise SemanticReadError('resource-limit')
        elif char in (93, 125): depth -= 1


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result: raise SemanticReadError('read-failed')
        result[key] = value
    return result


def _fits_inline(value, budget=INLINE, depth=0):
    if depth > 64: raise SemanticReadError('resource-limit')
    if isinstance(value, str): return budget - len(value) * 6 - 40
    if value is None or isinstance(value, (bool, float)): return budget - 64
    if isinstance(value, int): return budget - len(str(value)) - 40
    if isinstance(value, dict):
        for key, item in value.items():
            budget = _fits_inline(item, budget - len(key) * 6 - 48, depth + 1)
            if budget < 0: return budget
        return budget - 40
    if isinstance(value, (list, tuple)):
        for item in value:
            budget = _fits_inline(item, budget - 2, depth + 1)
            if budget < 0: return budget
        return budget - 40
    raise SemanticReadError('read-failed')


class _FactList(_Spool):
    def __init__(self, limits, budget=None, pool=None):
        super().__init__(budget or _Budget(limits, SemanticReadError), _encoded, SemanticReadError, CHUNK, pool)


def _tag_size(value, maximum, depth=0):
    if depth >= 64 and isinstance(value, (list, tuple, dict)): raise SemanticReadError('resource-limit')
    if isinstance(value, str) and len(value) > maximum: return maximum + 1
    if isinstance(value, dict):
        size = len(_encoded({'type': 'object', 'entries': []}))
        for index, (key, item) in enumerate(value.items()):
            if len(key) > maximum: return maximum + 1
            size += (1 if index else 0) + len(_encoded({'key': key, 'value': {'type': 'null'}})) - len(_encoded({'type': 'null'}))
            size += _tag_size(item, max(0, maximum - size), depth + 1)
            if size > maximum: return maximum + 1
        return size
    if isinstance(value, (list, tuple)):
        size = len(_encoded({'type': 'array', 'items': []}))
        for index, item in enumerate(value):
            size += (1 if index else 0) + _tag_size(item, max(0, maximum - size), depth + 1)
            if size > maximum: return maximum + 1
        return size
    return len(_encoded(_tag(value)))


def _finding_attributes(value):
    # Reducer/history wrappers span multiple source rows. Advertising the add
    # row as a complete paged wrapper would hide later events. Keep the full
    # composite inline or fail at the named physical fact budget instead.
    if _tag_size(value, CHUNK) > CHUNK: raise SemanticReadError('resource-limit')
    return {'kind': 'inline', 'value': _tag(value)}


def _attributes(value, span):
    # A full record remains at its immutable source locator when semantic
    # expansion would exceed a physical frame; no field is silently discarded.
    if _fits_inline(value) < 0: return {'kind': 'paged', 'byteLength': span['byteLength'], 'mediaType': 'application/json'}
    tagged = _tag(value)
    if len(_encoded(tagged)) <= INLINE: return {'kind': 'inline', 'value': tagged}
    return {'kind': 'paged', 'byteLength': span['byteLength'], 'mediaType': 'application/json'}


def _origin(span, pointer, sequence):
    return {'pointer': pointer, 'sequence': sequence, 'byteOffset': str(span[0]), 'byteLength': str(span[1])}


def _walk(value, path=''):
    if isinstance(value, dict):
        yield path, value
        for key, item in value.items():
            yield from _walk(item, path + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value): yield from _walk(item, path + '/' + str(index))


class SemanticReader:
    """Recorded-data helper state isolated to explicitly admitted source groups.

    Args:
        reader: App-owned S05 Reader retaining source and excluded-storage roots.
        lifecycle: Ignored compatibility argument; no canonical runtime API is used.
        findings: Ignored compatibility argument; the viewer owns recorded reduction.
    """
    def __init__(self, reader, lifecycle=None, findings=None):
        self.reader, self.lc, self.findings = reader, _RecordedFormat, _RecordedFindings()
        self._pool = _Pool(SemanticReadError); self._building = []; self._pending_cache = {}; self._budget = None
        self.leases = {}; self.projections = {}; self.preflight = {}; self.findings_cache = {}; self.invalidated = set(); self._compatibility = []; self._current = None; self._limits = None

    def _material(self, entry, identifier):
        if not isinstance(identifier, str) or len(identifier) != 64 or any(char not in '0123456789abcdef' for char in identifier):
            raise SemanticReadError('missing-material', entry['_sourceId'])
        self.reader._check([entry['_root']])
        try:
            with entry['_root'].capture(entry['name'] + '.blobs/' + identifier, maximum=32 * 1024 * 1024) as captured:
                raw = captured.read_all()
        except (OSError, ValueError) as error:
            raise SemanticReadError('missing-material', entry['_sourceId']) from error
        self.reader._check([entry['_root']])
        return raw

    def _rows(self, raw, finite=True):
        def reject(_value): raise ValueError('Nonfinite JSON wrapper')
        options = {'parse_constant': reject} if finite else {}
        return [json.loads(line, object_pairs_hook=_pairs, **options) for line in raw.splitlines()]

    def _fabric(self, group, entry, raw, spans):
        source_id = entry['_sourceId']
        first_end = raw.find(b'\n')
        first_rows = self._rows(raw[:first_end + 1] if first_end >= 0 else raw) if raw else []
        first = first_rows[0] if first_rows else None
        if raw and not isinstance(first, dict): raise SemanticReadError('read-failed', source_id, sequence='1')
        engagement = first.get('engagement') if isinstance(first, dict) else None
        declared_format = first.get('format') if first is not None else None
        declared_protocol = first.get('protocol') if first is not None else None
        compatibility = {'sourceId': source_id, 'family': 'fabric', 'declaredFormat': str(declared_format) if type(declared_format) in {int, str, float} and len(str(declared_format)) <= 128 else None,
                         'declaredProtocol': declared_protocol if isinstance(declared_protocol, str) and len(declared_protocol) <= 128 else None,
                         'supported': first is None or declared_format == 9 and declared_protocol == self.lc.PROTOCOL, 'adapterVersion': ADAPTERS['fabric']}
        self._compatibility.append(compatibility)
        if not compatibility['supported']: raise SemanticReadError('incompatible-source', source_id, sequence='1')
        key = group, entry['token']
        prior = self.projections.get(key)
        reusable = prior is not None and raw.startswith(prior[0]) and (not prior[0] or prior[0].endswith(b'\n'))
        state = _RecordedProjection(self.lc, prior[1] if reusable else None)
        offset = len(prior[0]) if reusable else 0
        for transaction in self._rows(raw[offset:]):
            if not isinstance(transaction, dict) or transaction.get('format') != 9 or transaction.get('protocol') != self.lc.PROTOCOL:
                raise SemanticReadError('incompatible-source', source_id)
            operations = transaction.get('operations')
            if not isinstance(operations, list) or len(operations) != 1 or not isinstance(operations[0], dict) or operations[0].get('op') != 'governed':
                raise SemanticReadError('read-failed', source_id)
            data = operations[0].get('data')
            if not isinstance(data, dict) or not isinstance(data.get('message'), dict) or not isinstance(data.get('effects'), list):
                raise SemanticReadError('read-failed', source_id)
            state.append(transaction)
        self.projections[key] = (raw, state)
        origins = {}
        for row_index, transaction in enumerate(state.transactions):
            sequence = transaction['sequence']; span = spans[row_index]
            for index, effect in enumerate(transaction['operations'][0]['data']['effects']):
                if effect['op'] in {'register', 'decision-record'}:
                    identifier = self.lc.version_id(effect['manifest'])
                    origins[identifier] = _origin(span, '/operations/0/data/effects/' + str(index) + '/manifest', str(sequence))
        facts = self._new_facts()
        uses_by_version = {}
        for (scope, version), status in state.states.items(): uses_by_version.setdefault(version, []).append((scope, status))
        for identifier, manifest in state.versions.items():
            ref = state._reference(identifier); record = manifest['content']['record']; origin = origins[identifier]
            base = {'sourceId': source_id, 'origin': origin}
            facts.append({**base, 'kind': 'version', 'ref': ref, 'family': manifest['kind'].removeprefix('delivery.'),
                          'label': manifest['logical_id'], 'attributes': _attributes({'manifest': manifest, 'provenance': state.provenance[identifier]}, origin)})
            owner = record.get('owner')
            if isinstance(owner, dict) and set(owner) == {'layer', 'work_kind', 'question', 'work_item'}:
                facts.append({**base, 'kind': 'ownership', 'originRef': ref, 'owner': owner})
            for field in ('owner', 'origin', 'assigned_actor', 'issued_to'):
                participant = record.get(field)
                if isinstance(participant, dict) and participant.get('kind') in {'authority', 'controller', 'assignment'}:
                    facts.append({**base, 'kind': 'participant', 'originRef': ref, 'participant': participant, 'fieldPointer': '/' + field})
            material_entries = [(path + '/blob_id', item.get('blob_id')) for path, item in _walk(record)]
            material_entries.extend(('/material/' + str(index), identifier) for index, identifier in enumerate(record.get('material', [])))
            for path, blob_id in material_entries:
                if isinstance(blob_id, str) and len(blob_id) == 64 and all(char in '0123456789abcdef' for char in blob_id):
                    try: self._material(entry, blob_id); availability = 'available'
                    except SemanticReadError: availability = 'missing'
                    facts.append({**base, 'kind': 'material', 'originRef': ref, 'blobId': blob_id, 'availability': availability, 'fieldPointer': path})
            causal_paths = {path for path, _ in self.lc._causal_reference_paths(record)}
            references = list(self.lc._reference_paths(record))
            for occurrence, (path, target) in enumerate(references):
                facts.append({**base, 'kind': 'reference', 'originRef': ref, 'originUseScope': None, 'fieldPointer': path,
                              'occurrence': occurrence, 'targetRef': target, 'targetUseScope': None,
                              'historicalCausal': False, 'governing': False, 'dependencyBasis': 'association'})
            for scope, status in uses_by_version.get(identifier, []):
                point = {'ref': ref, 'use_scope': scope}
                facts.append({**base, 'kind': 'use', 'point': point, 'state': _tag(status)})
                governing = state._governing_dependencies(point)
                represented = []
                previous_scope = state.scope; state.scope = scope
                try:
                    for occurrence, (path, target) in enumerate(references):
                        target_point = state._dependency_point(record, path, target)
                        causal = path in causal_paths
                        if causal: represented.append(target_point)
                        facts.append({**base, 'kind': 'reference', 'originRef': ref, 'originUseScope': scope,
                                      'fieldPointer': path, 'occurrence': occurrence, 'targetRef': target,
                                      'targetUseScope': target_point['use_scope'], 'historicalCausal': causal,
                                      'governing': target_point in governing and causal, 'dependencyBasis': 'historical' if causal else 'association'})
                finally: state.scope = previous_scope
                for occurrence, prerequisite in enumerate(governing):
                    if prerequisite not in represented:
                        facts.append({**base, 'kind': 'governing-dependency', 'originPoint': point,
                                      'prerequisitePoint': prerequisite, 'occurrence': occurrence, 'dependencyBasis': 'governing'})
            if manifest['kind'] == 'delivery.decision':
                transaction = state.transactions[state.rows_by_version[identifier]]
                for occurrence, effect in enumerate(transaction['operations'][0]['data']['effects']):
                    targets = []
                    if isinstance(effect.get('subjects'), (list, tuple)): targets.extend(effect['subjects'])
                    if isinstance(effect.get('subject'), dict): targets.append(effect['subject'])
                    if isinstance(effect.get('ref'), dict): targets.append(effect['ref'])
                    exact = []
                    for target in targets:
                        if isinstance(target, dict) and set(target) == {'ref', 'use_scope'}: exact.append(target)
                        elif isinstance(target, dict) and set(target) == {'engagement', 'scope', 'logical_id', 'version_id'}:
                            exact.append({'ref': target, 'use_scope': effect.get('use_scope', effect.get('scope', transaction['operations'][0]['data']['message']['scope']))})
                    for target in exact or [None]:
                        facts.append({**base, 'kind': 'decision-effect', 'decisionRef': ref, 'effectKind': effect['op'],
                                      'targetPoint': target, 'effect': _tag(effect), 'occurrence': occurrence})
        return facts, state.head, str(state.transactions[-1]['sequence']) if state.transactions else '0', {'declaredFormat': compatibility['declaredFormat'], 'declaredProtocol': compatibility['declaredProtocol']}, {'mode': 'recorded', 'decoded': 'decoded', 'chain': 'unknown', 'replay': 'recorded', 'publicTrust': 'unknown', 'material': 'not-observed', 'recordedApplicability': None, 'authorityGranted': False, 'freshAssessment': False}

    def _findings(self, group, entry, raw, spans):
        source_id = entry['_sourceId']
        cached = self.findings_cache.get((group, entry['token']))
        self._compatibility.append({'sourceId': source_id, 'family': 'findings', 'declaredFormat': None, 'declaredProtocol': None, 'supported': True, 'adapterVersion': ADAPTERS['findings']})
        if cached is not None and cached[0] == raw and cached[1] == self.findings.MAX_ROUNDS:
            facts = cached[2][0]
            self._budget.check(facts.encoded, facts.vertices, facts.edges, facts.count, source_id)
            self._budget.add(facts.encoded, facts.vertices, facts.edges, facts.count)
            facts.acquire()
            try: self._building.append(facts)
            except BaseException:
                facts.release()
                raise
            return cached[2]
        try:
            events = self._rows(raw, finite=False)
            if any(not isinstance(event, dict) or not isinstance(event.get('data'), dict) or event['data'].get('op') not in {'add', 'resolve', 'verify', 'withdraw', 'accept-risk'} for event in events):
                raise SemanticReadError('read-failed', source_id)
            reduced = self.findings.state(events)
        except (KeyError, TypeError, ValueError) as error:
            raise SemanticReadError('read-failed', source_id) from error
        facts = self._new_facts()
        starts = {}; histories = {}
        for index, event in enumerate(events):
            data = event['data']
            identifiers = [item['id'] for item in data['findings']] if data.get('op') == 'add' else [data['id']]
            for finding_index, identifier in enumerate(identifiers):
                if data.get('op') == 'add':
                    if identifier in starts: raise SemanticReadError('read-failed', source_id, '/data/findings', str(event['seq']))
                    starts[identifier] = (index, finding_index)
                histories.setdefault(identifier, []).append(event)
        for identifier, value in reduced.items():
            index, finding_index = starts[identifier]
            event = events[index]
            origin = _origin(spans[index], '/data/findings/' + str(finding_index), str(event['seq']))
            history = histories[identifier]
            attributes = {'record': value, 'events': history, 'effectiveMaxRounds': self.findings.MAX_ROUNDS, 'historicalMaxRoundsKnown': False}
            facts.append({'sourceId': source_id, 'origin': origin, 'kind': 'finding', 'findingId': identifier,
                          'state': value['state'], 'severity': value['severity'], 'findingKind': value['kind'],
                          'rounds': str(value['rounds']), 'recordedExpiry': value.get('expires'), 'label': value['title'],
                          'target': value.get('target') if isinstance(value.get('target'), str) else None, 'location': value.get('location') if isinstance(value.get('location'), str) else None, 'attributes': _finding_attributes(attributes),
                          'effectiveMaxRounds': self.findings.MAX_ROUNDS, 'historicalMaxRoundsKnown': False})
        result = facts, events[-1]['hash'] if events else None, str(events[-1]['seq']) if events else '0', {'declaredFormat': None, 'declaredProtocol': None}, {'mode': 'recorded', 'decoded': 'decoded', 'chain': 'unknown', 'replay': 'recorded', 'publicTrust': 'unknown', 'material': 'not-observed', 'recordedApplicability': None, 'authorityGranted': False, 'freshAssessment': False}
        self._pending_cache[(group, entry['token'])] = (raw, self.findings.MAX_ROUNDS, result)
        return result

    def _release_facts(self, objects):
        # A close failure must not strand later objects held by the same owner.
        failure = None
        for facts in objects:
            try: facts.release()
            except BaseException as error:
                if failure is None: failure = error
        if failure is not None: raise failure

    def _drop_cache(self, key):
        cache = self.findings_cache.pop(key, None)
        if cache is not None: cache[2][0].release()

    def _new_facts(self):
        # Optional cache ownership must never prevent a valid second lease.
        while len(self._pool.objects) >= 385 and self.findings_cache:
            self._drop_cache(next(iter(self.findings_cache)))
        facts = _FactList(self._limits, self._budget, self._pool)
        try: self._building.append(facts)
        except BaseException:
            facts.release()
            raise
        return facts

    def _commit_cache(self):
        for key, cache in self._pending_cache.items():
            self._drop_cache(key)
            facts = cache[2][0]
            while self.findings_cache and (len(self.findings_cache) >= 128 or
                    sum(item[2][0].encoded for item in self.findings_cache.values()) + facts.encoded > 512 * 1024 * 1024 or
                    sum(item[2][0].count for item in self.findings_cache.values()) + facts.count > 600000):
                self._drop_cache(next(iter(self.findings_cache)))
            facts.acquire()
            try: self.findings_cache[key] = cache
            except BaseException:
                facts.release()
                raise
        self._pending_cache = {}

    def _cached_bytes(self, excluded):
        buffers = {}
        for key, cache in self.preflight.items():
            if key != excluded: buffers[id(cache[0])] = cache[0]
        for key, cache in self.findings_cache.items():
            if key != excluded: buffers[id(cache[0])] = cache[0]
        for key, projection in self.projections.items():
            if key != excluded: buffers[id(projection[0])] = projection[0]
        return sum(len(raw) for raw in buffers.values())

    def _begin(self, group, sources, limits):
        """Capture and project explicit admitted sources without changing source state.

        Args:
            group: Existing helper root-selection token.
            sources: Bounded admitted token/sourceId pairs selected by trusted main.
            limits: Trusted graph work limits, capped by the viewer contract.
        Returns:
            Opaque candidate lease with source revision summaries and import report.
        Raises:
            SemanticReadError: Parsing, source change or resource ceiling fails.
            OSError: Secure retained capture fails.
        """
        if len(self.leases) >= 2: raise SemanticReadError('resource-limit')
        _, admitted = self.reader.groups[group]
        if not isinstance(sources, list) or not 1 <= len(sources) <= 128: raise SemanticReadError('read-failed')
        if len({item['token'] for item in sources}) != len(sources) or len({item['sourceId'] for item in sources}) != len(sources): raise SemanticReadError('read-failed')
        rows = []; captures = {}; facts = []; total = 0; observations = []
        if set(limits) != {'maxVertices', 'maxEdges', 'maxEncodedGraphBytes'} or any(type(limits[key]) is not int or not 1 <= limits[key] <= maximum for key, maximum in [('maxVertices', 100000), ('maxEdges', 500000), ('maxEncodedGraphBytes', 512 * 1024 * 1024)]): raise SemanticReadError('resource-limit')
        self._limits = limits
        self._budget = _Budget(limits, SemanticReadError)
        for selected in sources:
            entry = next(item for item in admitted if item['token'] == selected['token'])
            entry = {**entry, '_sourceId': selected['sourceId']}
            self._current = entry['_sourceId']
            key = (group, entry['token'])
            if key in self.invalidated: raise SemanticReadError('source-changed', entry['_sourceId'])
            self.reader._check([entry['_root']]); entry['_anchor'].observe_ancestry()
            raw = None; spans = []
            try:
                with entry['_root'].capture(entry['name'], expected_identity=entry['identity']) as captured:
                    if captured.info.size > entry['_limit'] or total + captured.info.size > TOTAL or self._cached_bytes(key) + captured.info.size > TOTAL: raise SemanticReadError('resource-limit', entry['_sourceId'])
                    info = captured.info
                    raw = captured.read_all()
                observations.append((entry, info))
                total += len(raw)
                if total > TOTAL: raise SemanticReadError('resource-limit', entry['_sourceId'])
                prior = self.preflight.get(key)
                if entry['family'] != 'audit' and prior is not None and not raw.startswith(prior[0]):
                    self.invalidated.add(key)
                    self._drop_cache(key)
                    for mapping in (self.projections, self.preflight): mapping.pop(key, None)
                    raise SemanticReadError('source-changed', entry['_sourceId'])
                if prior is not None and raw == prior[0]: raw = prior[0]
                elif key in self.findings_cache: self._drop_cache(key)
                reusable = prior is not None and raw.startswith(prior[0]) and (not prior[0] or prior[0].endswith(b'\n'))
                spans = list(prior[1]) if reusable else []; offset = len(prior[0]) if reusable else 0
                for line in raw[offset:].splitlines(keepends=True):
                    try: _preflight(line)
                    except SemanticReadError as error:
                        error.diagnostic.update(sourceId=entry['_sourceId'], sequence=str(len(spans) + 1) if entry['family'] != 'audit' else None)
                        raise
                    spans.append((offset, len(line))); offset += len(line)
                if entry['family'] == 'fabric': result = self._fabric(group, entry, raw, spans)
                elif entry['family'] == 'findings': result = self._findings(group, entry, raw, spans)
                else:
                    if len(raw) > RECORD: raise SemanticReadError('resource-limit', entry['_sourceId'])
                    _preflight(raw); audit = json.loads(raw, object_pairs_hook=_pairs)
                    self._compatibility.append({'sourceId': entry['_sourceId'], 'family': 'audit', 'declaredFormat': audit.get('format') if isinstance(audit, dict) else None, 'declaredProtocol': None, 'supported': isinstance(audit, dict) and audit.get('format') == 'jai.gen2-audit/1', 'adapterVersion': ADAPTERS['audit']})
                    if not isinstance(audit, dict) or audit.get('format') != 'jai.gen2-audit/1': raise SemanticReadError('incompatible-source', entry['_sourceId'])
                    if audit.get('authority_granted') is not False or audit.get('read_only') is not True: raise SemanticReadError('incompatible-source', entry['_sourceId'])
                    origin = _origin((0, len(raw)), '', None)
                    audit_facts = self._new_facts()
                    audit_facts.append({'sourceId': entry['_sourceId'], 'origin': origin, 'kind': 'audit', 'attributes': _attributes(audit, origin)})
                    result = (audit_facts, audit.get('head'), None,
                              {'declaredFormat': 'jai.gen2-audit/1', 'declaredProtocol': None}, {'mode': 'diagnostic', 'decoded': 'decoded', 'chain': 'unknown', 'replay': 'unknown', 'publicTrust': 'unknown', 'material': 'not-observed', 'recordedApplicability': None, 'authorityGranted': False, 'freshAssessment': False})
                source_facts, head, sequence, compatibility, verification = result
                if not source_facts.sealed: source_facts.seal()
                facts.append(source_facts)
                self.preflight[(group, entry['token'])] = (raw, tuple(spans))
                digest = hashlib.sha256(raw).hexdigest(); capture = uuid.uuid4().hex
                captures[capture] = {'raw': raw, 'sourceId': entry['_sourceId']}
                rows.append({'sourceId': entry['_sourceId'], 'captureToken': capture, 'family': entry['family'], 'byteLength': str(len(raw)), 'digest': digest,
                             'head': head, 'sequence': sequence, 'observedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                             'adapterVersion': ADAPTERS[entry['family']], 'verification': verification, 'compatibility': {**compatibility, 'sourceId': entry['_sourceId'], 'family': entry['family'], 'supported': True, 'adapterVersion': ADAPTERS[entry['family']]}})
            except SemanticReadError:
                raise
            except (OSError, ValueError, KeyError, TypeError, RecursionError, OverflowError) as error:
                raise SemanticReadError('source-changed' if isinstance(error, OSError) or 'changed' in str(error).lower() else 'read-failed', entry['_sourceId']) from error
            self.reader._check([entry['_root']])
        # Capture completion is revalidated once for the entire selected set.
        # No cross-ledger atomicity is inferred, but an input changed while
        # another source was parsed cannot silently enter this candidate.
        for entry, expected in observations:
            self.reader._check([entry['_root']]); entry['_anchor'].observe_ancestry()
            try:
                with entry['_root'].capture(entry['name'], expected_identity=entry['identity']) as current:
                    if current.info != expected: raise SemanticReadError('source-changed', entry['_sourceId'])
            except (ValueError, OSError) as error:
                if isinstance(error, SemanticReadError): raise
                raise SemanticReadError('source-changed', entry['_sourceId']) from error
        token = uuid.uuid4().hex
        self._commit_cache()
        self.leases[token] = {'group': group, 'captures': captures, 'facts': facts, 'cursor': 0, 'offset': 0, 'readCount': 0, 'readEncoded': 0, 'sequence': 0, 'ended': False}
        self._building = []
        return {'format': WIRE, 'leaseId': token, 'sources': rows, 'report': {'selected': str(len(sources)), 'accepted': str(len(sources)), 'rejected': '0', 'skipped': '0', 'diagnostics': [], 'diagnosticTotal': '0'}}

    def begin(self, group, sources, limits):
        """Capture selected sources transactionally with a safe rejection report.

        Args:
            group: Existing admitted source-selection token.
            sources: Main-owned token/sourceId pairs, never pathnames.
            limits: Trusted finite graph staging ceilings.
        Returns:
            One recorded-data candidate lease only if every selected source succeeds.
        Raises:
            SemanticReadError: Source failure with bounded compatibility and outcome report.
        """
        self._compatibility = []; self._current = None
        self._building = []; self._pending_cache = {}
        try:
            return self._begin(group, sources, limits)
        except (ValueError, OSError, KeyError, TypeError, StopIteration, RecursionError, OverflowError, MemoryError) as error:
            failure = error if isinstance(error, SemanticReadError) else SemanticReadError('resource-limit' if isinstance(error, MemoryError) else 'source-changed' if isinstance(error, OSError) else 'read-failed', self._current)
            if failure.diagnostic['sourceId'] is None: failure.diagnostic['sourceId'] = self._current
            failure.compatibility = self._compatibility[:128]
            selected = len(sources) if isinstance(sources, list) else 0
            failure.report = {'selected': str(selected), 'accepted': '0', 'rejected': '1' if selected else '0', 'skipped': str(max(0, selected - 1)), 'diagnostics': [failure.diagnostic], 'diagnosticTotal': '1'}
            if failure is error: raise
            raise failure from error
        finally:
            failed = sys.exc_info()[0] is not None
            try:
                self._release_facts(self._building)
            except BaseException:
                if not failed: raise
            finally:
                self._building = []; self._pending_cache = {}; self._budget = None

    def chunk(self, group, lease, cursor):
        """Pull a finite ordered fact frame with a single-use cursor.

        Args:
            group: Owning selection token.
            lease: Existing candidate lease.
            cursor: None initially, then the exact previous next cursor.
        Returns:
            Sequence, bounded facts and next cursor or terminal None.
        Raises:
            SemanticReadError: Foreign, stale, duplicate or out-of-order pull.
        """
        state = self.leases[lease]
        expected = None if state['sequence'] == 0 else state.get('next')
        if state['group'] != group or state['ended'] or cursor != expected: raise SemanticReadError('read-failed')
        facts = []; size = 0
        while state['cursor'] < len(state['facts']):
            source = state['facts'][state['cursor']]
            if state['offset'] == source.physical:
                if state['readCount'] != source.count or state['readEncoded'] != source.encoded:
                    raise SemanticReadError('read-failed')
                state['cursor'] += 1; state['offset'] = 0; state['readCount'] = 0; state['readEncoded'] = 0
                continue
            fact, offset, length = source.read(state['offset'])
            if facts and size + length > CHUNK: break
            facts.append(fact); size += length; state['offset'] = offset
            state['readCount'] += 1; state['readEncoded'] += length
        sequence = state['sequence']; state['sequence'] += 1
        state['ended'] = state['cursor'] == len(state['facts'])
        state['next'] = None if state['ended'] else uuid.uuid4().hex
        return {'sequence': str(sequence), 'facts': facts, 'next': state['next']}

    def page(self, group, lease, capture, offset, length):
        """Read exact captured bytes independently of current source pathname content.

        Args:
            group: Owning helper selection.
            lease: Active candidate.
            capture: Source capture token belonging to that candidate.
            offset: Canonical unsigned decimal byte offset.
            length: Page bytes in 1..256 KiB.
        Returns:
            Exact raw bytes and EOF for transport base64 encoding by the bridge.
        Raises:
            SemanticReadError: Foreign token or invalid page bound.
        """
        state = self.leases[lease]
        if state['group'] != group or not isinstance(offset, str) or not offset.isascii() or not offset.isdigit() or len(offset) > 20 or (len(offset) > 1 and offset.startswith('0')) or type(length) is not int or not 1 <= length <= PAGE: raise SemanticReadError('read-failed')
        raw = state['captures'][capture]['raw']; start = int(offset)
        if start > len(raw): raise SemanticReadError('read-failed')
        data = raw[start:start + length]
        return data, start + len(data) == len(raw)

    def release(self, group, lease):
        """Release an owned helper lease; no published main-owned archive is removed.

        Args:
            group: Owning helper selection token.
            lease: Candidate token; repeated release is harmless.
        Raises:
            SemanticReadError: Lease belongs to a foreign group.
        """
        state = self.leases.get(lease)
        if state is not None:
            if state['group'] != group: raise SemanticReadError('read-failed')
            del self.leases[lease]
            self._release_facts(state['facts'])

    def release_group(self, group):
        """Drop group-local captures/indexes when source access is closed.

        Args:
            group: Existing source-selection token.
        """
        failure = None
        for token in list(self.leases):
            if self.leases[token]['group'] == group:
                try: self.release(group, token)
                except BaseException as error:
                    if failure is None: failure = error
        self.invalidated = {key for key in self.invalidated if key[0] != group}
        for key in list(self.findings_cache):
            if key[0] == group:
                try: self._drop_cache(key)
                except BaseException as error:
                    if failure is None: failure = error
        for mapping in (self.projections, self.preflight):
            for key in list(mapping):
                if key[0] == group: del mapping[key]
        if failure is not None: raise failure
