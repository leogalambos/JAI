# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Trusted-runtime fixtures with optional disposable keys for explicit L0 acts.

Ordinary work uses the production local recorder without internal signing. Only
reserved human decisions substitute public test enrollment and use real Ed25519.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import lifecycle as lc
import operator_actions as op
import governed_delivery as delivery
import governed_routing as routing

QUESTIONS = ('what', 'why', 'how', 'who', 'where', 'when')
CONTROLLER = {'kind': 'controller', 'id': 'trusted-controller'}
HUMAN = {'kind': 'authority', 'id': 'human-owner'}


def _input_locators(bindings):
    result = []
    for binding in bindings:
        for reference in binding['refs']:
            if reference not in result:
                result.append(copy.deepcopy(reference))
    return result


class HumanSigner:
    """Create a disposable human identity only when a test requests an L0 act."""

    def __init__(self, directory, monkeypatch):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.keys = {}
        self.retained = {"human": []}
        for purpose, capabilities, signer in (
            ('human', ['lifecycle-update', 'accept', 'release', 'authorise'], 'human-owner'),
        ):
            private = self.directory / (purpose + '-disposable-private.pem')
            public = self.directory / (purpose + '-disposable-public.pem')
            subprocess.run(['openssl', 'genpkey', '-algorithm', 'ED25519', '-out', str(private)],
                           check=True, capture_output=True)
            subprocess.run(['openssl', 'pkey', '-in', str(private), '-pubout', '-out', str(public)],
                           check=True, capture_output=True)
            key = {'key_id': op.sha(public.read_bytes()), 'public_key': public.read_text(),
                   'signer': signer, 'capabilities': capabilities, 'state': 'active',
                   'engagements': ['*'], 'scopes': ['default'],
                   'valid_from_ms': 0, 'valid_until_ms': 9007199254740991}
            self.keys[purpose] = {'private': private, 'entry': key}
        monkeypatch.setattr(op, 'trusted_keys', self.trusted_keys)

    def trusted_keys(self, purpose=None):
        """Supply synthetic enrolled public keys, never a signature verdict."""
        if purpose not in {None, 'delivery-change', 'delivery-accept', 'delivery-release'}:
            raise ValueError('No internal origin keyring exists')
        selected = 'human'
        return {'schema_version': 3, 'policy_version': 'governed-keyring/1',
                'purpose': purpose or 'human',
                'host_policy': {'authority_policy_ids': ['host-authority'],
                                'routing_policy_ids': ['host-routing']},
                'keys': [copy.deepcopy(self.keys[selected]['entry']),
                         *copy.deepcopy(self.retained[selected])]}

    def rotate(self, identity, *, previous_state):
        """Retain the authentic old public key while enrolling a new active signer."""
        if previous_state not in {'retired', 'revoked'}:
            raise ValueError('explicit retained historical enrollment state required')
        old = copy.deepcopy(self.keys[identity]['entry'])
        old['state'] = previous_state
        self.retained[identity].append(old)
        ordinal = len(self.retained[identity])
        private = self.directory / f'{identity}-replacement-{ordinal}-private.pem'
        public = self.directory / f'{identity}-replacement-{ordinal}-public.pem'
        subprocess.run(['openssl', 'genpkey', '-algorithm', 'ED25519', '-out', str(private)],
                       check=True, capture_output=True)
        subprocess.run(['openssl', 'pkey', '-in', str(private), '-pubout', '-out', str(public)],
                       check=True, capture_output=True)
        entry = copy.deepcopy(old)
        entry.update(key_id=op.sha(public.read_bytes()), public_key=public.read_text(), state='active')
        self.keys[identity] = {'private': private, 'entry': entry}
        return old

    def wrapper(self, kind, source, target, parameters, *, now_ms=None, accepted=True):
        """Sign an exact synthetic request using the real OpenSSL implementation."""
        now_ms = int(time.time() * 1000) if now_ms is None else now_ms
        request = {'schema_version': 1, 'request_id': str(uuid.uuid4()), 'kind': kind,
                   'purpose': 'Disposable protocol regression only',
                   'source': {'path': str(Path(source).absolute()),
                              'sha256': op.sha(Path(source).read_bytes())},
                   'target': str(target), 'parameters': parameters,
                   'permissions': 'disposable test identity', 'risk': 'synthetic local data only',
                   'created_at': now_ms / 1000 - 1,
                   'expires_at': now_ms / 1000 + 120}
        request['request_hash'] = op.sha(op.canonical(request))
        if kind not in {'delivery-change', 'delivery-accept', 'delivery-release'}:
            raise ValueError('Only explicit L0 decisions are signed')
        identity = 'human'
        key = self.keys[identity]
        receipt = {'schema_version': 1, 'request_id': request['request_id'],
                   'request_hash': request['request_hash'], 'accepted': accepted,
                   'performed': False, 'issued_at': now_ms / 1000,
                   'expires_at': request['expires_at'], 'key_id': key['entry']['key_id'],
                   'assurance': op.ASSURANCE, 'outputs': []}
        body = self.directory / 'receipt-body'
        signature = self.directory / 'receipt-signature'
        body.write_bytes(op.canonical(receipt))
        subprocess.run(['openssl', 'pkeyutl', '-sign', '-inkey', str(key['private']),
                        '-rawin', '-in', str(body), '-out', str(signature)],
                       check=True, capture_output=True)
        receipt['signature'] = base64.b64encode(signature.read_bytes()).decode('ascii')
        return {'request': request, 'receipt': receipt}


class GovernedHarness:
    """Record actual typed work; reserve disposable signing for explicit L0 acts."""

    def __init__(self, directory, monkeypatch, *, engagement='governed-test', layer=1,
                 additional_layers=(), use_scopes=('default',), scenario_duration_ms=None):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._monkeypatch = monkeypatch
        self._human_signer = None
        self.use_scopes = list(use_scopes)
        self.engagement, self.scope, self.layer = engagement, 'default', layer
        self.layers = sorted(set([layer, *additional_layers]))
        self.store = lc.Store(self.directory / (engagement + '.jsonl'), engagement)
        self.path = self.directory / (engagement + '.jsonl')
        self.sequence = 0
        self.profile = None
        self.controller_context = None
        self.last_message = None
        self.pending = {}
        self.outbound_messages = {}
        self.setters = {}
        self.scope_sources = {}
        self.scope_contexts = {}
        self.task_duration_ms = scenario_duration_ms or 240000
        self.control_duration_ms = scenario_duration_ms or 300000
        self._proposal_records = {}
        self._registered_records = {}
        self._receipt_head = lc.ZERO
        self._receipt_stamp = None
        self.routing_policy = None
        self.route_executions = {}

    @property
    def signers(self):
        """Lazily enroll only a disposable human key for an explicit L0 test act."""
        if self._human_signer is None:
            self._human_signer = HumanSigner(self.directory / 'external-human-key', self._monkeypatch)
            self._human_signer.keys['human']['entry']['scopes'] = list(self.use_scopes)
        return self._human_signer

    def _ledger_stamp(self):
        try:
            info = self.path.stat(follow_symlinks=False)
        except FileNotFoundError:
            return None
        return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns

    def _remember_proposal(self, reference, family, record):
        self._proposal_records[reference['version_id']] = {
            'ref': copy.deepcopy(reference), 'family': family, 'record': lc.normal(record)}

    def _remember_registered(self, reference, family, record):
        # Mutable trust/policy, applicability, and selected slots are never
        # fixture caches. Only immutable ordinary record bodies prepare requests.
        if family not in {'source', 'assignment', 'context', 'product', 'assessment'}:
            return
        if family == 'source' and record['source_role'] == 'policy':
            return
        self._registered_records[reference['version_id']] = {
            'ref': copy.deepcopy(reference), 'family': family, 'record': copy.deepcopy(record)}

    def _observe_snapshot(self, state):
        self._receipt_head = state.head
        self._receipt_stamp = self._ledger_stamp()
        for identifier, value in state.versions.items():
            family = value['kind'].removeprefix('delivery.')
            self._remember_registered(state._reference(identifier), family, value['content']['record'])

    def _known_record(self, reference, family):
        cached = self._registered_records.get(reference['version_id'])
        if cached and cached['ref'] == reference and cached['family'] == family:
            return copy.deepcopy(cached['record'])
        state = self.store.read()
        record = state.resolve(reference, family)
        self._observe_snapshot(state)
        return copy.deepcopy(record)

    def _proposal_head(self):
        # External direct Store submissions and deliberate file mutations still
        # trigger a fresh verified read. A raced proposal remains subject to the
        # real planner/submit expected-head checks; it is never silently retried.
        if self._ledger_stamp() != self._receipt_stamp:
            self._observe_snapshot(self.store.read())
        return self._receipt_head

    def _observe_commit(self, response):
        if response['status'] != 'committed':
            return
        receipt = response['receipt']
        self._receipt_head = receipt['after_head']
        self._receipt_stamp = self._ledger_stamp()
        for reference in receipt['created_versions']:
            proposed = self._proposal_records.get(reference['version_id'])
            if proposed and lc.normal(proposed['ref']) == reference:
                self._remember_registered(reference, proposed['family'], proposed['record'])

    def owner(self, question='how', work_item='service-controls', layer=None, work_kind='question'):
        """Return a coordinate without giving the named actor any authority."""
        return {'layer': self.layer if layer is None else layer, 'work_kind': work_kind,
                'question': question if work_kind == 'question' else None, 'work_item': work_item}

    def ref(self, logical_id, record_type, record):
        """Derive an exact reference using the production record-to-manifest mapping."""
        value = lc.record_manifest(self.engagement, self.scope, logical_id, record_type, record)
        return {'engagement': self.engagement, 'scope': self.scope,
                'logical_id': logical_id, 'version_id': lc.version_id(value)}

    def material(self, text):
        """Register exact bytes without selecting, accepting, or authorizing their use."""
        return self.store.put_blob(text.encode('utf-8'))

    def _routing_source(self):
        worker = ROOT / 'tests/fixtures/governed_dispatch/worker.py'
        chooser = ROOT / 'tests/fixtures/governed_dispatch/selection_worker.py'
        default = {'provider': 'json-process/1', 'argv': ['/usr/bin/python3', '/worker/main.py', 'author'],
                   'files': [{'name': 'main.py', 'sha256': hashlib.sha256(worker.read_bytes()).hexdigest()}]}
        chooser_execution = {'provider': 'json-process/1', 'argv': ['/usr/bin/python3', '/worker/main.py'],
                             'files': [{'name': 'main.py', 'sha256': hashlib.sha256(chooser.read_bytes()).hexdigest()}]}
        models = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
        classes = {name: {'model_selector': 'local-' + name, 'execution': copy.deepcopy(default)}
                   for name in models['workload_classes']}
        responsibilities = ('chooser', 'setter', 'author', 'reviewer', 'integrator', 'integration_reviewer', 'receiver', 'measurement')
        for responsibility in responsibilities:
            workload = 'fixture-' + responsibility
            models['workload_classes'][workload] = {'complexity_order': 100 + len(classes),
                'description': 'Explicit globally available local fixture worker.', 'reasoning_profile': 'low'}
            for provider in models['providers'].values():
                provider['classes'][workload] = copy.deepcopy(provider['classes']['standard'])
            execution = chooser_execution if responsibility == 'chooser' else default
            classes[workload] = {'model_selector': workload, 'execution':
                                 copy.deepcopy(self.route_executions.get(responsibility, execution))}
        models['providers']['json-process/1'] = {'display_name': 'Disposable local process',
            'adapter': 'json-process/1', 'selection_strategy': 'explicit-per-agent',
            'strategy_scope': 'project-internal', 'classes': classes}
        catalogue = (ROOT / '.ai/runtime/roles.json').read_bytes()
        instructions = {row['slug']: (ROOT / '.ai/skills' / row['skill'] / 'references' /
                        (row['slug'] + '.md')).read_bytes() for row in json.loads(catalogue)['roles']}
        bootstrap = {'provider': 'json-process/1', 'workload_class': 'fixture-chooser',
                     'model_selector': 'fixture-chooser'}
        capabilities = {'effects': [
            {'operation': 'read', 'tool_policy': None, 'destination_handle': None},
            {'operation': 'propose', 'tool_policy': None, 'destination_handle': None},
            {'operation': 'materialize', 'tool_policy': None, 'destination_handle': 'owned-output'},
            {'operation': 'measure', 'tool_policy': self.criteria, 'destination_handle': None}],
            'limits': [{'metric': 'tokens', 'unit': 'governed-token', 'ceiling': 10000},
                       {'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 60000}]}
        material = routing.capture_policy('host-routing', catalogue, lc.canonical(models),
            instructions, bootstrap, capabilities, self.store.put_blob)
        return {'owner': HUMAN, 'source_role': 'policy', 'origin': HUMAN,
                'material': material, 'criteria': [], 'inherited': []}

    def message(self, message_type, payload, *, sender=None, context=None,
                recipient=None, expected_head=None, request_id=None):
        """Construct an unsigned request; this method cannot cause a state transition."""
        self.sequence += 1
        now = int(time.time() * 1000)
        message = {'protocol': 'jai.governed-delivery/1', 'message_type': message_type,
                   'message_id': '0' * 64,
                   'request_id': request_id or f'request-{self.sequence}',
                   'correlation_id': 'service-controls', 'engagement': self.engagement,
                   'scope': self.scope, 'sender': copy.deepcopy(sender or CONTROLLER),
                   'recipient': copy.deepcopy(recipient or CONTROLLER),
                   'context': copy.deepcopy(context if context is not None else self.controller_context),
                   'profile': copy.deepcopy(self.profile),
                   'expected_head': expected_head if expected_head is not None else self._proposal_head(),
                   'issued_at_ms': now, 'expires_at_ms': now + 60000,
                   'causes': [], 'attachments': [], 'payload': copy.deepcopy(payload)}
        message['message_id'] = delivery.message_id(message)
        return message

    def outbound(self, message):
        """Compile an actual captured provider return into its host completion record."""
        if message['sender']['kind'] != 'assignment':
            return message
        identity = message['message_id']
        if identity in self.outbound_messages:
            return self.outbound_messages[identity]
        context = self._known_record(message['context'], 'context')
        package = {'assignment': message['sender']['ref'], 'context': message['context'],
                   'records': copy.deepcopy(self.pending.get(message['context']['version_id'], [])),
                   'intents': [{'message_type': message['message_type'],
                                'recipient': message['recipient'], 'payload': message['payload']}]}
        assigned = self._known_record(context['assignment'], 'assignment')
        completed = self.message('control_event',
                                {'event': 'run_completed', 'run_context': message['context'],
                                 'run_id': context['run_id'], 'observed_at_ms': int(time.time() * 1000),
                                 'return_blob_id': self.store.put_blob(lc.canonical(package)),
                                 'usage': [{'metric': limit['metric'], 'unit': limit['unit'], 'total': 1}
                                           for limit in assigned['limits']]},
                                expected_head=message['expected_head'])
        completed['issued_at_ms'] = message['issued_at_ms']
        completed['expires_at_ms'] = message['expires_at_ms']
        completed['message_id'] = delivery.message_id(completed)
        self.outbound_messages[identity] = completed
        return completed

    def send(self, message, *, authority_proof=None):
        """Record runtime work, verifying a human proof only when one is supplied."""
        message = self.outbound(message)
        response = self.store.submit(lc.canonical(message), authority_proof=authority_proof)
        self._observe_commit(response)
        self.last_message = copy.deepcopy(message)
        return response

    def commit(self, message, **kwargs):
        """Return the receipt for a valid fixture operation, failing setup otherwise."""
        response = self.send(message, **kwargs)
        if response['status'] != 'committed':
            raise AssertionError(response)
        return response['receipt']

    def bootstrap_message(self, *, require_evidence=False, include_neighbor=False):
        """Prepare exact initial material and unsigned wire bytes without granting authority."""
        source = {'owner': HUMAN, 'source_role': 'input', 'origin': HUMAN,
                  'material': [self.material('Bounded service requirements A.\n')],
                  'criteria': [], 'inherited': []}
        self.input_a = self.ref('input-A', 'source', source)
        self._remember_proposal(self.input_a, 'source', source)
        criteria = {'owner': HUMAN, 'source_role': 'criteria', 'origin': HUMAN,
                    'material': [self.material('C1: preserve the exact inherited service requirement.\n')],
                    'criteria': [{'id': 'C1', 'requirement': self.input_a,
                                  'statement': 'The answer satisfies its exact inherited service requirement.',
                                  'evidence_slots': ([f'L{self.layer}:service-controls:how-evidence']
                                                     if require_evidence else [])}], 'inherited': [self.input_a]}
        self.criteria = self.ref('criteria', 'source', criteria)
        self._remember_proposal(self.criteria, 'source', criteria)
        routing_source = self._routing_source()
        self.routing_policy = self.ref('role-routing', 'source', routing_source)
        self._remember_proposal(self.routing_policy, 'source', routing_source)
        self.l0_sources = [self.input_a, self.criteria, self.routing_policy]
        obligations = []
        layers = sorted(set(self.layers + ([2] if include_neighbor else [])))
        for layer in layers:
            for work_item in ('service-controls', 'foreign-service'):
                for question in QUESTIONS:
                    roles = [('answer', 'product'), ('input', 'source'),
                             ('professional_review', 'assessment')]
                    if require_evidence:
                        roles.append(('evidence', 'product'))
                    for role, required_kind in roles:
                        obligations.append({'slot_id': f'L{layer}:' + work_item + ':' + question + '-' + role,
                                            'owner': self.owner(question, work_item, layer),
                                            'subject_kind': 'answer', 'role': role,
                                            'required_kind': required_kind, 'minimum': 1, 'maximum': 1,
                                            'allow_exclusion': False, 'exclusion_owner': None})
        if include_neighbor:
            for layer in (1, 2):
                for role, subject_kind in (('integration_review', 'bundle'),
                                            ('receiving_acceptance', 'handoff')):
                    obligations.append({'slot_id': f'L{layer}:service-controls:integration-' + role,
                                        'owner': self.owner(layer=layer, work_kind='integration'),
                                        'subject_kind': subject_kind, 'role': role,
                                        'required_kind': 'assessment', 'minimum': 1, 'maximum': 1,
                                        'allow_exclusion': False, 'exclusion_owner': None})
        profile = {'owner': CONTROLLER, 'profile_id': 'focused-governed-regression',
                   'protocol': 'jai.governed-delivery/1', 'source_profiles': [],
                   'obligations': obligations, 'max_clock_skew_ms': 5000,
                   'max_request_duration_ms': self.control_duration_ms,
                   'local_budget': {'iteration_ms': 600000, 'max_reworks': 3}, 'authority_policy_id': 'host-authority',
                   'routing_policy_id': 'host-routing', 'content_profile': None,
                   'scheduling': {'collection_window_ms': 60000,
                                  'control_limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 10000}],
                                  'max_search_steps': 200, 'max_escalation_rounds': 10,
                                  'initial_deadline_ms': int(time.time() * 1000) + self.task_duration_ms}}
        self.profile = self.ref('profile', 'profile', profile)
        message = self.message('bootstrap', {'controller_id': CONTROLLER['id'],
                                           'use_scopes': self.use_scopes,
                                           'profile': {'logical_id': 'profile', 'record': profile},
                                           'l0_inputs': [{'logical_id': 'input-A', 'record': source},
                                                         {'logical_id': 'criteria', 'record': criteria},
                                                         {'logical_id': 'role-routing', 'record': routing_source}]})
        message['profile'] = None
        message['context'] = None
        message['message_id'] = delivery.message_id(message)
        return message

    def bootstrap(self, *, require_evidence=False, include_neighbor=False):
        """Create the profile, attributable L0 input, and bounded controller context."""
        message = self.bootstrap_message(require_evidence=require_evidence,
                                          include_neighbor=include_neighbor)
        receipt = self.commit(message)
        self.controller_context = next(ref for ref in receipt['created_versions']
                                       if ref['logical_id'].startswith('controller-context:'))
        self.scope_sources = {scope: (copy.deepcopy(self.input_a), copy.deepcopy(self.criteria))
                              for scope in self.use_scopes}
        self.scope_contexts[self.scope] = copy.deepcopy(self.controller_context)
        return receipt

    def enter_scope(self, scope):
        """Select an independently preauthorized scope and renew its finite host context."""
        if scope not in self.use_scopes:
            raise ValueError('scope was not authorized at bootstrap')
        previous = self.controller_context
        self.scope = scope
        self.input_a, self.criteria = copy.deepcopy(self.scope_sources[scope])
        self.l0_sources = [self.input_a, self.criteria, self.routing_policy]
        if scope in self.scope_contexts:
            self.controller_context = copy.deepcopy(self.scope_contexts[scope])
            return self.controller_context
        renewal = self.message('control_event', {'event': 'renew_control',
                                                'previous_context': previous,
                                                'profile_use': {'ref': self.profile, 'use_scope': scope}})
        renewal['context'] = None
        renewal['expires_at_ms'] = renewal['issued_at_ms'] + self.control_duration_ms
        renewal['message_id'] = delivery.message_id(renewal)
        receipt = self.commit(renewal)
        self.controller_context = next(ref for ref in receipt['created_versions']
                                       if ref['logical_id'].startswith('controller-context:'))
        self.scope_contexts[scope] = copy.deepcopy(self.controller_context)
        return self.controller_context

    def assignment(self, logical_id, responsibility, *, owner=None, actor=None, inputs=None,
                   inherited=None, creator=None, creator_context=None, deadline_ms=None,
                   use_scope=None, input_uses=None, criteria_ref=None, token_limit=10000):
        """Create an assigned record through its setter or initial controller path."""
        owner = copy.deepcopy(owner or self.owner())
        use_scope = use_scope or self.scope
        root_key = (use_scope, json.dumps(owner, sort_keys=True))
        if responsibility == 'setter' and creator is None and root_key in self.setters:
            return copy.deepcopy(self.setters[root_key])
        parent = self._known_record(creator['ref'], 'assignment') if creator else None
        inputs = copy.deepcopy(inputs if inputs is not None else parent['inputs'] if parent else
                               [{'slot_id': f'L{owner["layer"]}:' + owner['work_item'] + ':' + (owner.get('question') or 'how') + '-input',
                                 'refs': [self.input_a]}])
        if responsibility == 'setter' and creator is None:
            present = [reference for binding in inputs for reference in binding['refs']]
            missing = [reference for reference in self.l0_sources if reference not in present]
            if missing:
                inputs.append({'slot_id': 'l0-additional', 'refs': copy.deepcopy(missing)})
        inherited = copy.deepcopy(inherited if inherited is not None else
                                  parent['inherited'] if parent else self.l0_sources)
        criteria_ref = copy.deepcopy(criteria_ref or (parent['criteria'] if parent else self.criteria))
        read_targets = []
        for ref in [item for binding in inputs for item in binding['refs']] + [criteria_ref]:
            if ref not in read_targets:
                read_targets.append(ref)
        now = int(time.time() * 1000)
        record = {'owner': owner, 'responsibility': responsibility,
                  'routing': {'policy': self.routing_policy},
                  'assigned_actor': actor or logical_id + '-actor', 'profile': self.profile,
                  'inherited': inherited,
                  'use_scope': use_scope, 'issued_under': copy.deepcopy(creator['ref']) if creator else None,
                  'input_uses': copy.deepcopy(input_uses if input_uses is not None else
                                              parent['input_uses'] if parent else []),
                  'inputs': inputs, 'criteria': criteria_ref,
                  'effects': [{'operation': 'read', 'owner': owner,
                               'targets': read_targets,
                               'destination_handle': None, 'tool_policy': None},
                              {'operation': 'propose', 'owner': owner, 'targets': [],
                               'destination_handle': None, 'tool_policy': None}],
                  'limits': [{'metric': 'tokens', 'ceiling': token_limit, 'unit': 'governed-token'}],
                  'deadline_ms': deadline_ms or min(now + self.task_duration_ms,
                        parent['deadline_ms'] if parent and parent['deadline_ms'] is not None else now + self.task_duration_ms)}
        if parent and parent.get('handling') is not None:
            record['handling'] = copy.deepcopy(parent['handling'])
        selected_scopes = {item['at']: item['use_scope'] for item in record['input_uses']}
        for index, reference in enumerate(inherited):
            if reference == self.routing_policy:
                policy_scope = selected_scopes.get('/inherited/' + str(index), use_scope)
                if policy_scope != use_scope and '/routing/policy' not in selected_scopes:
                    record['input_uses'].append({'at': '/routing/policy', 'use_scope': policy_scope})
                break
        ref = self.record(logical_id, 'assignment', record,
                          sender=creator, context=creator_context)
        if creator and creator['kind'] == 'assignment':
            self.commit(self.message('assignment', {'assignment': ref, 'owner': owner,
                                                   'responsibility': responsibility,
                                                   'inputs': _input_locators(inputs),
                                                   'criteria': criteria_ref},
                                     sender=creator, context=creator_context))
        if responsibility == 'setter':
            self.setters[root_key] = (copy.deepcopy(ref), copy.deepcopy(record))
        return ref, record

    def context(self, logical_id, assignment, record, *, phase='work', selection=None, start=True,
                speculation=None):
        """Issue explicit phases; unit fixtures synthesize choice, never native evidence."""
        if phase == 'work' and selection is None:
            chosen = self.context(logical_id + '-synthetic-selection', assignment, record,
                                  phase='selection', speculation=speculation)
            choice = {'action': 'select_execution', 'assignment': assignment,
                'previous': self.store.read().execution_plans.get((assignment['version_id'], self.scope)),
                'specialties': ['software-engineer'], 'provider': 'json-process/1',
                'workload_class': 'fixture-' + record['responsibility'],
                'model_selector': 'fixture-' + record['responsibility'],
                'reason': 'Explicit synthetic assigned-entity choice for Store unit preparation.',
                'authority_proof': None}
            message = self.message('decision', choice, sender={'kind': 'assignment', 'ref': assignment}, context=chosen)
            receipt = self.commit(message)
            state = self.store.read()
            selection = next(ref for ref in receipt['created_versions']
                             if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
        logical_id += '-' + str(self.sequence)
        execution = {'phase': phase}
        if phase == 'work':
            execution['selection'] = selection
        context = {'owner': record['owner'], 'assignment': assignment, 'profile': self.profile,
                   'purpose': record['responsibility'], 'run_id': logical_id + '-run',
                   'issued_to': record['assigned_actor'], 'inputs': record['inputs'],
                   'attachments': [], 'effects': record['effects'], 'execution': execution,
                   'expires_at_ms': min(record['deadline_ms'], int(time.time() * 1000) +
                       self.store.read().local_budget_status(assignment)['remaining_ms']),
                   'speculation': speculation,
                   'ready_basis': self.store.read().ready_basis(assignment)}
        reference = self.record(logical_id, 'context', context)
        if start:
            self.commit(self.message('control_event', {'event': 'run_started',
                'run_context': reference, 'run_id': context['run_id'], 'observed_at_ms': int(time.time() * 1000)}))
        return reference

    def cancel_run(self, reference):
        """Account a rejected invocation and explicitly close its physical reservation."""
        context = self._known_record(reference, 'context')
        assignment = self._known_record(context['assignment'], 'assignment')
        return self.commit(self.message('control_event', {'event': 'run_cancelled',
            'run_context': reference, 'run_id': context['run_id'],
            'observed_at_ms': int(time.time() * 1000),
            'reason': 'Synthetic host observed the rejected invocation stopping',
            'usage': [{'metric': limit['metric'], 'unit': limit['unit'], 'total': 1}
                      for limit in assignment['limits']]}))

    def setup_author(self, *, layer=None, question='how', work_item='service-controls', suffix='A',
                     responsibility='author', work_kind='question', inputs=None, input_uses=None,
                     author_token_limit=10000, start_author=True):
        """Create genuine setter and author assignments/contexts without raw state injection."""
        owner = self.owner(question, work_item, layer, work_kind)
        setter, setter_record = self.assignment('setter-' + suffix, 'setter', owner=owner)
        setter_context = self.context('setter-context-' + suffix, setter, setter_record)
        principal = {'kind': 'assignment', 'ref': setter}
        author, author_record = self.assignment('author-' + suffix, responsibility, owner=owner,
                                                creator=principal, creator_context=setter_context,
                                                inputs=inputs, input_uses=input_uses,
                                                token_limit=author_token_limit)
        author_context = self.context('author-context-' + suffix, author, author_record) if start_author else None
        return {'owner': owner, 'setter': setter, 'setter_record': setter_record,
                'setter_context': setter_context, 'author': author,
                'author_record': author_record, 'author_context': author_context,
                'principal': {'kind': 'assignment', 'ref': author}}

    def product(self, logical_id, actor, *, kind='answer', material=None, evidence=None,
                inputs=None, related=None, episode=None, outcome=None):
        """Record an actual author-owned pending result and return its exact body/ref."""
        record = {'owner': actor['owner'], 'product_kind': kind,
                  'assignment': actor['author'], 'profile': self.profile,
                  'inputs': copy.deepcopy(inputs if inputs is not None else actor['author_record']['inputs']),
                  'material': material or [self.material('Synthetic current answer ' + logical_id)],
                  'evidence': copy.deepcopy(evidence or []), 'related': copy.deepcopy(related or []),
                  'limitations': []}
        if kind == 'escalation':
            record['episode'] = copy.deepcopy(episode or {'root': None, 'previous': None,
                'collection_head': self._proposal_head(), 'unfinished': [], 'decisive': True})
        if outcome is not None:
            record['outcome'] = copy.deepcopy(outcome)
        ref = self.record(logical_id, 'product', record, sender=actor['principal'],
                          context=actor['author_context'])
        return ref, record

    def submission(self, actor, ref, record, **overrides):
        """Build the terminal delivery, which remains distinct from registration."""
        return self.message('submission', {'assignment': actor['author'], 'candidate': ref,
                                           'evidence': record['evidence'],
                                           'limitations': record['limitations']},
                            sender=actor['principal'], context=actor['author_context'], **overrides)

    def prepare_review(self, actor, subject, *, suffix='review', actor_id=None, owner=None,
                       assessment_kind='professional', verdict='supported', evidence=None):
        """Issue a real reviewer context before testing or submitting its returned record."""
        owner = copy.deepcopy(owner or actor['owner'])
        responsibility = {'professional': 'reviewer', 'integration': 'integration_reviewer',
                          'receiving': 'receiver'}[assessment_kind]
        setter, setter_record = self.assignment(suffix + '-setter', 'setter', owner=owner)
        setter_context = self.context(suffix + '-setter-context', setter, setter_record)
        assignment, assigned = self.assignment(suffix + '-assignment', responsibility,
                                               owner=owner, actor=actor_id,
                                               inputs=copy.deepcopy(actor['author_record']['inputs']) +
                                                      [{'slot_id': 'assessed-subject', 'refs': [subject]}] +
                                                      copy.deepcopy(evidence or []),
                                               creator={'kind': 'assignment', 'ref': setter},
                                               creator_context=setter_context)
        context = self.context(suffix + '-context', assignment, assigned)
        closure = self.store.read().assessment_closure(subject, assignment)
        record = {'owner': owner, 'assessment_kind': assessment_kind,
                  'assignment': assignment, 'subject': subject, 'criteria': self.criteria,
                  'profile': self.profile, 'assessed_closure': closure,
                  'assessed_hash': hashlib.sha256(lc.canonical(closure)).hexdigest(),
                  'verdict': verdict, 'findings': [], 'conditions': []}
        principal = {'kind': 'assignment', 'ref': assignment}
        return {'record': record, 'assignment': assignment, 'context': context,
                'principal': principal, 'suffix': suffix}

    def assessment_delivery(self, prepared, subject, *, logical_id=None):
        """Stage the actual returned assessment and its matching typed review intent."""
        record = prepared['record']
        reference = self.record(logical_id or prepared['suffix'], 'assessment', record,
                                sender=prepared['principal'], context=prepared['context'])
        message = self.message('review', {'assignment': prepared['assignment'],
                                          'assessment': reference, 'subject': subject,
                                          'criteria': self.criteria, 'verdict': record['verdict'],
                                          'findings': record['findings'], 'conditions': record['conditions']},
                               sender=prepared['principal'], context=prepared['context'])
        return reference, message

    def review(self, actor, subject, **kwargs):
        """Obtain an independent actual assessment of an already recorded subject."""
        prepared = self.prepare_review(actor, subject, **kwargs)
        record, assignment = prepared['record'], prepared['assignment']
        principal, context, suffix = prepared['principal'], prepared['context'], prepared['suffix']
        reference = self.record(suffix, 'assessment', record, sender=principal, context=context)
        message = self.message('review', {'assignment': assignment, 'assessment': reference,
                                          'subject': subject, 'criteria': self.criteria,
                                          'verdict': record['verdict'], 'findings': [], 'conditions': []},
                               sender=principal, context=context)
        self.commit(message)
        return reference, record

    def escalate(self, affected, *, suffix='escalation'):
        """Return an assigned aggregate escalation that pauses its actual layer."""
        actor = self.setup_author(suffix=suffix, responsibility='integrator')
        reference, record = self.product(suffix, actor, kind='escalation',
                                         related=[{'slot_id': 'conflicts', 'refs': [self.criteria]}])
        message = self.message('escalation', {'assignment': actor['author'], 'package': reference,
                                             'conflicts': [self.criteria], 'affected': affected,
                                             'requested_decisions': ['Resolve the exact inherited requirements conflict']},
                               sender=actor['principal'], context=actor['author_context'])
        self.commit(message)
        return reference

    def stage_input_transition(self, text, *, suffix='B', remove_old_material=False):
        """Stage exact replacement records, leaving them without governing acceptance."""
        old_input, old_criteria = self.input_a, self.criteria
        source = self._known_record(old_input, 'source')
        source['material'] = [self.material(text)]
        new_input = self.record('input-' + suffix, 'source', source)
        criteria = self._known_record(old_criteria, 'source')
        criteria['inherited'] = [new_input]
        for criterion in criteria['criteria']:
            if criterion['requirement'] == old_input:
                criterion['requirement'] = new_input
        new_criteria = self.record('criteria-' + suffix, 'source', criteria)
        if remove_old_material:
            for identifier in self._known_record(old_input, 'source')['material']:
                (self.store.material / identifier).unlink()
        message = self.message('decision', {'action': 'continue',
                                            'reason': 'Explicit approved governing input revision',
                                            'replacements': [{'previous': old_input, 'replacement': new_input},
                                                             {'previous': old_criteria, 'replacement': new_criteria}],
                                            'verification_path': new_criteria,
                                            'authority_proof': '0' * 64}, sender=HUMAN)
        return message, old_input, new_input, new_criteria

    def apply_input_transition(self, prepared):
        """Sign and apply the exact staged human transition, then renew bounded control."""
        message, old_input, new_input, new_criteria = prepared
        proof = self.human_proof(message, 'delivery-change')
        receipt = self.commit(message, authority_proof=proof)
        self.input_a, self.criteria = new_input, new_criteria
        self.l0_sources = [new_input, new_criteria, self.routing_policy]
        self.scope_sources[self.scope] = (copy.deepcopy(new_input), copy.deepcopy(new_criteria))
        self.setters = {key: value for key, value in self.setters.items() if key[0] != self.scope}
        previous = self.controller_context
        renewal = self.message('control_event', {'event': 'renew_control', 'previous_context': previous,
                                                'profile_use': {'ref': self.profile, 'use_scope': self.scope}})
        renewal['context'] = None
        renewal['expires_at_ms'] = renewal['issued_at_ms'] + self.control_duration_ms
        renewal['message_id'] = delivery.message_id(renewal)
        renewed = self.commit(renewal)
        self.controller_context = next(reference for reference in renewed['created_versions']
                                       if reference['logical_id'].startswith('controller-context:'))
        self.scope_contexts[self.scope] = copy.deepcopy(self.controller_context)
        return receipt, old_input, new_input

    def transition_inputs(self, text, *, suffix='B', remove_old_material=False):
        """Apply exact human-governed input replacement then renew host control."""
        return self.apply_input_transition(self.stage_input_transition(
            text, suffix=suffix, remove_old_material=remove_old_material))

    def owner_decision(self, owner, payload, *, inputs=None):
        """Return an exact local decision from a fresh authorized setter invocation."""
        setter, assigned = self.assignment('decision-setter-' + str(self.sequence), 'setter',
                                          owner=owner, inputs=inputs)
        context = self.context('decision-context-' + str(self.sequence), setter, assigned)
        return self.message('decision', payload, sender={'kind': 'assignment', 'ref': setter},
                            context=context)

    def select_proof(self, subject, proof, *, slot_id=None, role='professional_review', previous=None):
        """Select a qualified exact proof without adding a reverse causal edge."""
        body = self._known_record(subject, 'product')
        owner = body['owner']
        profile = self.store.read().resolve(body['profile'], 'profile')
        obligations = [item for item in profile['obligations'] if item['owner'] == owner
                       and item['role'] == role and item['subject_kind'] == body['product_kind']]
        assert len(obligations) == 1, obligations
        slot_id = slot_id or obligations[0]['slot_id']
        required = [{'slot_id': 'governing-source', 'refs': [self.input_a]},
                    {'slot_id': 'assessed-subject', 'refs': [subject]},
                    {'slot_id': 'assessed-proof', 'refs': [proof]}]
        message = self.owner_decision(owner, {'action': 'select',
                                             'reason': 'Select exact independently returned proof',
                                             'slot': {'kind': 'proof', 'subject': subject,
                                                      'role': role, 'slot_id': slot_id},
                                             'candidate': proof, 'previous': previous}, inputs=required)
        return self.commit(message)

    def select_basis(self, actor, subject):
        """Have the actual setter select an exact qualified output in its profile slot."""
        state = self.store.read()
        product = state.resolve(subject, 'product')
        assert product['owner'] == actor['owner']
        profile = state.resolve(product['profile'], 'profile')
        obligations = [item for item in profile['obligations']
                       if item['owner'] == product['owner'] and item['role'] == 'answer'
                       and item['required_kind'] == 'product'
                       and item['subject_kind'] == product['product_kind']]
        assert len(obligations) == 1, obligations
        slot = {'kind': 'basis', 'owner': product['owner'], 'slot_id': obligations[0]['slot_id']}
        previous = state.selections.get(lc._proof_key(self.scope, slot))
        message = self.owner_decision(product['owner'], {'action': 'select',
            'reason': 'The owning setter selects this exact independently qualified result',
            'slot': slot, 'candidate': subject, 'previous': previous})
        return self.commit(message)

    def qualified_answer(self, *, suffix='A', question='how', inputs=None, text=None,
                         select_basis=True, reviewer_actor=None):
        """Deliver and independently review a current owner-authored answer."""
        actor = self.setup_author(question=question, suffix=suffix)
        candidate, record = self.product('candidate-' + suffix, actor, inputs=inputs,
                                         material=[self.material(text)] if text is not None else None)
        self.commit(self.submission(actor, candidate, record))
        proof, _ = self.review(actor, candidate, suffix='review-' + suffix, actor_id=reviewer_actor)
        self.select_proof(candidate, proof)
        if select_basis:
            self.select_basis(actor, candidate)
        return actor, candidate, proof

    def accept(self, subject, *, release=False):
        """Apply genuine synthetic human intent after all required local checks qualify."""
        basis = self.store.evaluate(subject, scope=self.scope)
        payload = {'action': 'release' if release else 'accept',
                   'reason': 'Disposable exact-output authority regression',
                   'subject': subject, 'closure_hash': basis['closure_hash'],
                   'authority_proof': '0' * 64}
        if release:
            payload['acceptance'] = basis['acceptances'][0]
        message = self.message('decision', payload, sender=HUMAN)
        proof = self.human_proof(message, 'delivery-release' if release else 'delivery-accept')
        self.commit(message, authority_proof=proof)
        return proof

    def observation(self, actor, text, *, suffix='observation', subject=None):
        """Produce independently assigned exact observation material through delivery."""
        setter, setter_record = self.assignment(suffix + '-setter', 'setter', owner=actor['owner'])
        setter_context = self.context(suffix + '-setter-context', setter, setter_record)
        assignment, assigned = self.assignment(suffix + '-assignment', 'measurement',
                                               owner=actor['owner'],
                                               inputs=copy.deepcopy(actor['author_record']['inputs']) +
                                                      ([{'slot_id': 'measured-subject', 'refs': [subject]}] if subject else []),
                                               creator={'kind': 'assignment', 'ref': setter},
                                               creator_context=setter_context)
        context = self.context(suffix + '-context', assignment, assigned)
        principal = {'kind': 'assignment', 'ref': assignment}
        record = {'owner': actor['owner'], 'product_kind': 'observation',
                  'assignment': assignment, 'profile': self.profile, 'inputs': assigned['inputs'],
                  'material': [self.material(text)], 'evidence': [], 'related': [], 'limitations': []}
        ref = self.record(suffix, 'product', record, sender=principal, context=context)
        message = self.message('observation', {'assignment': assignment, 'observation': ref,
                                              'inputs': _input_locators(assigned['inputs']),
                                              'material': record['material']},
                               sender=principal, context=context)
        return ref, record, message


    def record(self, logical_id, record_type, record, *, sender=None, context=None):
        """Register typed pending content through its actual authorized origin."""
        reference = self.ref(logical_id, record_type, record)
        self._remember_proposal(reference, record_type, record)
        message = self.message('record_proposal', {'logical_id': logical_id,
                                                 'record_type': record_type,
                                                 'record': record}, sender=sender, context=context)
        if sender and sender['kind'] == 'assignment':
            self.pending.setdefault(context['version_id'], []).append(
                {'logical_id': logical_id, 'record_type': record_type, 'record': copy.deepcopy(record)})
        else:
            self.commit(message)
        return reference

    def human_proof(self, message, purpose):
        """Sign a proof-independent human intent, then bind its exact blob in the wire."""
        descriptor = delivery.action_descriptor(message, self.store.read().policy_digest(message))
        source = self.directory / 'human-intent.json'
        source.write_bytes(lc.canonical(descriptor))
        wrapper = self.signers.wrapper(purpose, source, self.path,
                                       {'intent': descriptor,
                                        'intent_digest': hashlib.sha256(lc.canonical(descriptor)).hexdigest()})
        message['payload']['authority_proof'] = lc.blob(op.canonical(wrapper))
        message['message_id'] = delivery.message_id(message)
        return wrapper

def accepted_store(directory, monkeypatch, text, *, engagement='accepted-governed', release=False):
    """Build a real exact-output acceptance without raw state or verifier substitution."""
    host = GovernedHarness(directory, monkeypatch, engagement=engagement)
    host.bootstrap()
    actor, subject, proof = host.qualified_answer(text=text)
    host.accept(subject)
    if release:
        host.accept(subject, release=True)
    return host, actor, subject, proof

