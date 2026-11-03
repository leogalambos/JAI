# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One recorded Store engagement covers the semantic six-layer delivery closure.

The service and measurement are fictional deterministic fixture facts, not customer
telemetry. Native provider execution is qualified separately. No State is imported
or injected: even the receiving gateways use their actual protocol derivation.
"""
import copy
import hashlib
import json
import time

import pytest

from governed_fixtures import GovernedHarness, HUMAN, QUESTIONS, delivery
from test_governed_sabsa_content import _example
import governed_sabsa as content
import lifecycle as lc


LAYERS = ('contextual', 'conceptual', 'logical', 'physical', 'component', 'management')
FACTS = {
    'contextual': (
        'The fictional payment-status service holds transaction identifiers and status records.',
        'The sponsor needs dependable payment-status access to avoid customer support disruption.',
        'Customers query status; service operators reconcile failed lookups.',
        'The fictional service sponsor owns availability and the support manager owns recovery.',
        'The fictional service operates only inside its designated internal service boundary.',
        'The planning horizon is one month, with five-minute sampling and monthly evaluation.'),
    'conceptual': (
        'Payment status is a business information concept with an explicit availability objective.',
        'Availability and recoverability protect dependable access required by the sponsor.',
        'Separate status access, monitoring and recovery responsibilities.',
        'A service owner approves service objectives; an independent assessor reviews their realization.',
        'The internal service domain separates callers, status processing and monitoring.',
        'Proposed changes require review before activation and a monthly objective evaluation.'),
    'logical': (
        'Status records contain a transaction identifier, processing state and last-update time.',
        'A read service and a monitoring service jointly support dependable status access.',
        'A status lookup validates the identifier and reads the current status; a monitor records a probe.',
        'Caller, service operator and monitoring reader are separate logical responsibilities.',
        'Only the status interface crosses the caller-to-processing trust boundary.',
        'Lookup completion precedes response; failed probe evaluation precedes recovery escalation.'),
    'physical': (
        'A Python HTTP process and a relational status table implement the selected logical services.',
        'A read-only lookup endpoint limits accidental changes while fulfilling the status-access need.',
        'The HTTP process uses a read-only database connection; a separate process executes health probes.',
        'The service team maintains the HTTP process and the operations team maintains the probe schedule.',
        'The service and database run in the fictional internal service zone.',
        'A five-minute scheduled probe supplies measurements for monthly service evaluation.'),
    'component': (
        'The status handler accepts an identifier and returns a state from the status repository interface.',
        'Handler and probe specifications implement status access and observable service availability.',
        'The probe component records success or failure against the exact status endpoint specification.',
        'The component maintainer owns handler configuration; the duty operator owns probe execution.',
        'The handler package and probe configuration are deployed only in the internal service zone.',
        'The probe scheduler invokes the probe every five minutes; aggregation runs at month end.'),
    'management': (
        'The managed service inventory identifies the endpoint, status repository and availability measure.',
        'Availability review compares the recorded result with the sponsor-approved target.',
        'Operators execute the defined probe and evaluate the defined measure before proposing improvement.',
        'The duty operator records results; the service owner decides corrective work.',
        'Operational coverage includes the contextual objective through the deployed component endpoint.',
        'Five-minute observations feed monthly evaluation and an owner-directed improvement request.'),
}


def _unit(key, group, statement, properties=None):
    return {'key': key, 'group': group, 'title': key.replace('-', ' ').capitalize(),
            'statements': [statement], 'properties': properties or {}, 'classification': 'public'}


class _SemanticEngagement(GovernedHarness):
    """Use trusted-runtime fixtures with explicit L0 decisions with one explicit six-layer semantic mandate."""

    def __init__(self, directory, monkeypatch):
        super().__init__(directory, monkeypatch, engagement='six-layer-semantic-qualification',
                         additional_layers=(2, 3, 4, 5, 6), scenario_duration_ms=30 * 60 * 1000)
        self.control_duration_ms = 300000
        self.units = {}
        self.relations = {}
        self.bundles = {}
        self.handoffs = {}
        self.answers = {}
        self.coordinator = None
        self.started = time.monotonic()

    @staticmethod
    def key(layer, question):
        return LAYERS[layer - 1] + '-' + question

    def policy(self):
        result = copy.deepcopy(_example('sabsa-content-profile'))
        result['scope']['purpose'] = 'A fictional service architecture and deterministic fixture measurement.'
        result['scope']['depth'] = 'All six perspectives; execution facts are disposable fixture data.'
        result['claim'] = 'Bounded original JAI minimum; no formal SABSA conformity or customer effectiveness claim.'
        for obligation in result['required_units']:
            obligation['owner']['work_item'] = 'service-controls'
        observation = next(item for item in result['required_units'] if item['group'] == 'management.observation')
        observation['owner'] = self.owner(layer=6, work_kind='measurement')
        observation['owner']['question'] = None
        result['required_relations'] = []
        for obligation in result['required_units']:
            key, group = obligation['key'], obligation['group']
            if group == 'contextual.why':
                continue
            if group == 'conceptual.attributes':
                basis = self.key(1, 'why')
            elif group in {'management.activity', 'management.observation'}:
                basis = self.key(5, 'how')
            elif group == 'management.measure':
                basis = next(item['key'] for item in result['required_units'] if item['group'] == 'conceptual.attributes')
            else:
                layer = obligation['owner']['layer']
                basis = self.key(1, 'why') if layer == 1 else self.key(layer - 1, obligation['owner']['question'])
            result['required_relations'].append({'key': key + '-basis', 'type': 'realizes',
                'from_obligation': key, 'to_obligation': basis})
        measure_key = next(item['key'] for item in result['required_units'] if item['group'] == 'management.measure')
        result['required_relations'].extend([
            {'key': 'observed-subject', 'type': 'observes', 'from_obligation': observation['key'],
             'to_obligation': self.key(5, 'what')},
            {'key': 'measured-result', 'type': 'measures', 'from_obligation': measure_key,
             'to_obligation': observation['key']},
            {'key': 'operational-feedback', 'type': 'feedback_for', 'from_obligation': observation['key'],
             'to_obligation': self.key(3, 'how')}])
        result['required_views'] = [{'view': 'architecture',
            'unit_obligations': [item['key'] for item in result['required_units']],
            'relation_obligations': [item['key'] for item in result['required_relations']]}]
        return result

    def bootstrap_message(self, **kwargs):
        message = super().bootstrap_message(**kwargs)
        self.semantic_policy = self.policy()
        source = {'owner': HUMAN, 'source_role': 'policy', 'origin': HUMAN,
                  'material': [self.store.put_blob(lc.canonical(self.semantic_policy))],
                  'criteria': [], 'inherited': []}
        reference = self.ref('semantic-policy', 'source', source)
        self._remember_proposal(reference, 'source', source)
        self.l0_sources.append(reference)
        message['payload']['l0_inputs'].append({'logical_id': 'semantic-policy', 'record': source})
        profile = message['payload']['profile']['record']
        profile['content_profile'] = {'logical_id': 'semantic-policy', 'use_scope': self.scope}
        for layer in range(1, 7):
            owner = self.owner(layer=layer, work_kind='integration')
            for role, kind in (('integration_review', 'bundle'), ('receiving_acceptance', 'handoff')):
                profile['obligations'].append(self._obligation(owner, role, kind))
        owner = self.owner(layer=6, work_kind='measurement')
        owner['question'] = None
        for role, family in (('answer', 'product'), ('professional_review', 'assessment')):
            profile['obligations'].append(self._obligation(owner, role, 'observation', family))
        profile['obligations'].append(self._obligation(self.owner(layer=6, work_kind='integration'),
                                                      'integration_review', 'final_result'))
        self.profile = self.ref('profile', 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message

    @staticmethod
    def _obligation(owner, role, subject_kind, family='assessment'):
        return {'slot_id': 'semantic-L' + str(owner['layer']) + '-' + subject_kind + '-' + role,
                'owner': owner, 'subject_kind': subject_kind, 'role': role,
                'required_kind': family, 'minimum': 1, 'maximum': 1,
                'allow_exclusion': False, 'exclusion_owner': None}

    def _cache_setter(self, reference, record):
        # This remembers an actually committed assignment, not a derived State.
        key = (self.scope, json.dumps(record['owner'], sort_keys=True))
        self.setters[key] = (copy.deepcopy(reference), copy.deepcopy(record))

    def _issue(self, owner, responsibility, name, inputs=None):
        coordinator, record = self.coordinator
        context = self.context(name + '-issuer', coordinator, record)
        return self.assignment(name, responsibility, owner=owner,
            creator={'kind': 'assignment', 'ref': coordinator}, creator_context=context,
            inputs=inputs or record['inputs'])

    def _inputs(self, extra=()):
        return copy.deepcopy(self.coordinator[1]['inputs']) + [
            {'slot_id': 'returned-semantic-' + str(index), 'refs': [reference]}
            for index, reference in enumerate(extra)]

    def _local(self, layer, question):
        owner = self.owner(question=question, layer=layer)
        references = [] if layer > 1 or question == 'why' else [self.units[self.key(1, 'why')]['product']]
        inputs = self._inputs(references)
        slot = f'L{layer}:service-controls:{question}-input'
        if not any(binding['slot_id'] == slot for binding in inputs):
            inputs.append({'slot_id': slot, 'refs': [self.input_a]})
        setter = self._issue(owner, 'setter', f'L{layer}-{question}-setter', inputs)
        self._cache_setter(*setter)
        return self.setup_author(layer=layer, question=question, suffix=f'L{layer}-{question}')

    def payload(self, owner):
        obligations = [item for item in self.semantic_policy['required_units'] if item['owner'] == owner]
        units = []
        for item in obligations:
            group = item['group']
            if group == 'conceptual.attributes':
                statement = 'The fictional sponsor requires monthly availability of at least 99.5 percent.'
                properties = {'business_justification': 'Dependable payment-status access.', 'target': '99.5',
                    'unit': 'percent', 'measurement_method': 'Successful scheduled probes divided by all scheduled probes.',
                    'accountable_owner': 'Fictional service sponsor', 'evaluation_horizon': 'One calendar month'}
            elif group == 'management.activity':
                statement = 'The duty operator executes the scheduled fictional status probe.'
                properties = {'objective': 'Detect loss of status access.', 'responsible_actor': 'Fictional duty operator',
                    'inputs': 'Exact endpoint and probe specification.', 'outputs': 'Recorded probe result.',
                    'scope': 'Fictional internal status endpoint.', 'trigger': 'Scheduled probe event.',
                    'timing': 'Every five minutes.', 'controls': 'Approved probe configuration and operator review.',
                    'required_evidence': 'Exact probe result with measured subject, period, method and result.'}
            elif group == 'management.measure':
                statement = 'The availability measure evaluates successful scheduled fictional probes.'
                properties = {'target': '99.5', 'unit': 'percent', 'method': 'Successes divided by scheduled probes.',
                    'source': 'Exact probe observations.', 'frequency': 'Monthly', 'thresholds': 'Below 99.5 percent.',
                    'action': 'Request owner review and corrective work.', 'owner': 'Fictional service owner'}
            elif group == 'management.observation':
                statement = 'One deterministic fixture probe completed successfully; this is not customer telemetry.'
                properties = {'subject': 'Exact fictional component endpoint', 'measure': 'Exact availability measure',
                    'period': 'Fixture interval 0', 'method': 'Deterministic fixture probe', 'result': 'success'}
            else:
                statement = FACTS[LAYERS[owner['layer'] - 1]][QUESTIONS.index(owner['question'])]
                properties = {'business_role': 'driver'} if group == 'contextual.why' else {}
            units.append(_unit(item['key'], group, statement, properties))
        local = {unit['key'] for unit in units}
        relations = []
        for item in self.semantic_policy['required_relations']:
            if item['type'] == 'measures' and item['to_obligation'] not in local:
                continue
            if item['from_obligation'] not in local and not (
                    item['type'] == 'measures' and item['to_obligation'] in local):
                continue
            def locator(key):
                return {'product': None, 'unit': key} if key in local else copy.deepcopy(self.units[key])
            relations.append({'key': item['key'], 'type': item['type'],
                'from': locator(item['from_obligation']), 'to': locator(item['to_obligation']),
                'rationale': 'Explicit fictional business-to-operation trace; feedback requests a new owner revision.'})
        return {'format': 'jai-sabsa-content/1', 'units': units, 'relations': relations, 'view_bindings': []}

    def _remember_content(self, reference, payload):
        for unit in payload['units']:
            self.units[unit['key']] = {'product': reference, 'unit': unit['key']}
        for relation in payload['relations']:
            self.relations[relation['key']] = {'product': reference, 'relation': relation['key']}

    def answer(self, layer, question):
        actor = self._local(layer, question)
        if question == 'what':
            foreign = self.answers[layer, 'why']
            body = self._known_record(foreign, 'product')
            message = self.submission(actor, foreign, body)
            before = self.path.read_bytes()
            response = self.send(message)
            assert response['status'] == 'rejected' and response['error']['code'] == 'P_SCOPE', response
            assert self.path.read_bytes() == before
            self.cancel_run(actor['author_context'])
            actor['author_context'] = self.context(f'L{layer}-what-fresh-work', actor['author'], actor['author_record'])
        payload = self.payload(actor['owner'])
        subject, record = self.product(f'L{layer}-{question}-answer', actor,
            material=[self.store.put_blob(lc.canonical(payload))])
        self.commit(self.submission(actor, subject, record))
        review, _ = self.review(actor, subject, suffix=f'L{layer}-{question}-professional',
                                actor_id=f'L{layer}-{question}-independent')
        self.select_proof(subject, review)
        self.select_basis(actor, subject)
        self._remember_content(subject, payload)
        self.answers[layer, question] = subject
        return subject

    def observation(self):
        owner = self.owner(layer=6, work_kind='measurement')
        owner['question'] = None
        measure = next(item['product'] for key, item in self.units.items()
                       if key == next(unit['key'] for unit in self.semantic_policy['required_units']
                                      if unit['group'] == 'management.measure'))
        setter = self._issue(owner, 'setter', 'L6-measurement-setter', self._inputs([measure]))
        self._cache_setter(*setter)
        actor = self.setup_author(layer=6, question=None, suffix='L6-measurement',
                                  work_kind='measurement', responsibility='measurement')
        payload = self.payload(owner)
        raw = lc.canonical({'fixture': True, 'method': 'deterministic fixture probe',
                            'interval': 0, 'successful': 1, 'scheduled': 1})
        subject, record = self.product('L6-probe-observation', actor, kind='observation',
            material=[self.store.put_blob(lc.canonical(payload)), self.store.put_blob(raw)])
        self.commit(self.message('observation', {'assignment': actor['author'], 'observation': subject,
            'inputs': lc._input_locators(record['inputs']),
            'material': record['material']}, sender=actor['principal'], context=actor['author_context']))
        review, _ = self.review(actor, subject, suffix='L6-measurement-professional',
                                actor_id='L6-measurement-independent')
        self.select_proof(subject, review)
        self.select_basis(actor, subject)
        self._remember_content(subject, payload)
        return subject

    def _integration_actor(self, name, extra):
        return self.setup_author(layer=self.coordinator[1]['owner']['layer'], suffix=name,
            responsibility='integrator', work_kind='integration', inputs=self._inputs(extra))

    def integrate(self, layer, observation=None):
        answers = [self.answers[layer, question] for question in QUESTIONS]
        actor = self._integration_actor(f'L{layer}-bundle', answers + ([observation] if observation else []))
        bundle, record = self.product(f'L{layer}-bundle', actor, kind='bundle',
            related=[{'slot_id': 'answers', 'refs': answers}])
        self.commit(self.submission(actor, bundle, record))
        proof, _ = self.review(actor, bundle, suffix=f'L{layer}-integration-review',
                               assessment_kind='integration', actor_id=f'L{layer}-independent-integrator')
        self.select_proof(bundle, proof, role='integration_review')
        publisher = self._integration_actor(f'L{layer}-publish', [bundle, proof])
        self.commit(self.message('integration', {'assignment': publisher['author'], 'bundle': bundle,
            'answers': answers, 'integration_review': proof}, sender=publisher['principal'],
            context=publisher['author_context']))
        self.bundles[layer] = bundle
        return bundle

    def next_layer(self, layer, bundle):
        actor = self._integration_actor(f'L{layer}-handoff', [bundle, self.criteria])
        handoff, _ = self.product(f'L{layer}-handoff', actor, kind='handoff',
            related=[{'slot_id': 'bundle', 'refs': [bundle]}, {'slot_id': 'interface', 'refs': [self.criteria]}])
        self.commit(self.message('handoff', {'assignment': actor['author'], 'handoff': handoff,
            'bundle': bundle, 'interface': self.criteria, 'obligations': self.l0_sources},
            sender=actor['principal'], context=actor['author_context']))
        state = self.store.read()
        proposal = state.local_entry({'ref': handoff, 'use_scope': self.scope}, 'receiver')
        receiver = self.record(proposal['logical_id'], 'assignment', proposal['record'])
        context = self.context(f'L{layer + 1}-receiving', receiver, proposal['record'])
        closure = self.store.read().assessment_closure(handoff, receiver)
        assessment = {'owner': proposal['record']['owner'], 'assessment_kind': 'receiving',
            'assignment': receiver, 'subject': handoff, 'criteria': self.criteria, 'profile': self.profile,
            'assessed_closure': closure, 'assessed_hash': hashlib.sha256(lc.canonical(closure)).hexdigest(),
            'verdict': 'accepted', 'findings': [], 'conditions': []}
        principal = {'kind': 'assignment', 'ref': receiver}
        accepted = self.record(f'L{layer + 1}-receiving-proof', 'assessment', assessment,
                               sender=principal, context=context)
        self.commit(self.message('handoff_acceptance', {'assessment': accepted, 'handoff': handoff,
            'interface': self.criteria, 'verdict': 'accepted', 'findings': []}, sender=principal, context=context))
        self.select_proof(handoff, accepted, role='receiving_acceptance')
        proposal = self.store.read().local_entry({'ref': handoff, 'use_scope': self.scope}, 'setter', accepted)
        reference = self.record(proposal['logical_id'], 'assignment', proposal['record'])
        self.coordinator = reference, proposal['record']
        self._cache_setter(*self.coordinator)
        self.handoffs[layer] = handoff

    def final(self, bundle):
        actor = self._integration_actor('L6-final', [bundle, self.handoffs[5]])
        binding = {'view': 'architecture', 'units': list(self.units.values()),
                   'relations': list(self.relations.values())}
        payload = {'format': 'jai-sabsa-content/1', 'units': [], 'relations': [], 'view_bindings': [binding]}
        outcome = {'kind': 'verified_candidate', 'attempt': self.coordinator[0],
                   'evidence': [bundle, self.handoffs[5]]}
        subject, record = self.product('six-layer-current-result', actor, kind='final_result',
            material=[self.store.put_blob(lc.canonical(payload))], outcome=outcome,
            related=[{'slot_id': 'bundle', 'refs': [bundle]}, {'slot_id': 'handoff', 'refs': [self.handoffs[5]]}])
        self.commit(self.submission(actor, subject, record))
        proof, _ = self.review(actor, subject, suffix='six-layer-final-independent-review',
            assessment_kind='integration', actor_id='six-layer-final-independent')
        self.select_proof(subject, proof, role='integration_review')
        return subject


def test_one_governed_sabsa_engagement_traces_all_six_layers_and_renders_its_exact_current_output(tmp_path, monkeypatch):
    host = _SemanticEngagement(tmp_path, monkeypatch)
    host.bootstrap()
    owner = host.owner(layer=1, work_kind='integration')
    host.coordinator = host.assignment('semantic-L1-coordinator', 'setter', owner=owner)
    host._cache_setter(*host.coordinator)
    for layer in range(1, 7):
        for question in ('why', 'what', 'how', 'who', 'where', 'when'):
            host.answer(layer, question)
        observation = host.observation() if layer == 6 else None
        bundle = host.integrate(layer, observation)
        if layer == 1:
            partial = content.assess(host.store.read(), bundle)
            assert not partial['structural_complete'] and partial['status'] == 'incomplete'
            assert any(row['status'] == 'missing' for row in partial['obligations'])
        assert host.store.evaluate(bundle)['qualified']
        if layer < 6:
            host.next_layer(layer, bundle)
        print('SABSA_LAYER=' + str(layer) + ' ELAPSED_SECONDS=' + str(time.monotonic() - host.started)
              + ' TRANSACTIONS=' + str(len(host.store.read().transactions)), flush=True)
    output = host.final(bundle)
    with monkeypatch.context() as ordinary_status:
        def forbid_outcome_reassessment(*args, **kwargs):
            raise AssertionError('Ordinary outcome status must use established current facts')
        ordinary_status.setattr(lc.State, 'evaluate', forbid_outcome_reassessment)
        outcome = host.store.read().attempt_status(host.coordinator[0])['outcome']
        assert outcome['kind'] == 'verified_candidate' and outcome['record'] == output
    report = content.assess(host.store.read(), output)
    assert report['structural_complete'] and report['substantive_complete']
    assert len(report['obligations']) == 40
    assert len(host.answers) == 36 and set(host.bundles) == set(range(1, 7))
    assert len(host.handoffs) == 5
    assert all(row['status'] == 'satisfied' for row in report['obligations'] + report['relations'] + report['views'])
    assert len(report['traces']['backward']) == 40 and len(report['traces']['forward']) == 40
    assert not host.store.evaluate(output)['accepted']
    host.accept(output)
    assert not host.store.evaluate(output)['release_eligible']
    host.accept(output, release=True)
    before = host.path.read_bytes()
    rendered = content.render(host.store.read(), output, audience='public')
    assert rendered['publication']['eligible']
    assert len(rendered['views'][0]['json']['units']) == 40
    assert len(rendered['views'][0]['json']['relations']) == len(host.semantic_policy['required_relations'])
    assert rendered == content.render(host.store.read(), output, audience='public')
    assert host.path.read_bytes() == before
    subject = host.answers[5, 'what']
    material = host._known_record(subject, 'product')['material'][0]
    raw = host.store._blob(material)
    (host.store.material / material).unlink()
    try:
        assert not host.store.evaluate(output)['release_eligible']
        withheld = content.render(host.store.read(), output, audience='public')
        assert not withheld['publication']['eligible']
        assert not withheld['publication']['release_eligible']
        assert all(not view['json']['units'] for view in withheld['views'])
        assert host.path.read_bytes() == before
    finally:
        assert host.store.put_blob(raw) == material

    state = host.store.read()
    integrated = [*host.bundles.values(), *host.handoffs.values(), output]
    selected_proofs = [selection['proof'] for key, selection in state.proofs.items()
                       if key[0] == host.scope and selection['subject'] in integrated]
    assert len(selected_proofs) == 12  # Six bundle, five receiving and one final proof.
    permissions = [event for event in state.events
                   if event['kind'] in {'accept', 'release'} and event['subject'] == output]
    assert {event['kind'] for event in permissions} == {'accept', 'release'}
    preserved = {reference['version_id']: copy.deepcopy(state.resolve(reference))
                 for reference in integrated + selected_proofs}
    accepted_prefix = host.path.read_bytes()
    _, input_a, input_b = host.transition_inputs(
        'Explicit fictional sponsor revision B requires a different availability target.\n',
        remove_old_material=True)
    state = host.store.read()
    assert host.path.read_bytes().startswith(accepted_prefix)
    assert input_a['version_id'] != input_b['version_id']
    assert input_a['version_id'] in state.versions and input_b['version_id'] in state.versions
    for reference in integrated + selected_proofs:
        assert state.resolve(reference) == preserved[reference['version_id']]
        assert state._status(reference, host.scope) == {'validity': 'invalid', 'applicable': False}
    assert all(event['decision_id'] in state.decisions['cancelled'] for event in permissions)
    current = state.evaluate(output, host.scope)
    assert not current['qualified'] and not current['accepted'] and not current['release_eligible']
    assert not current['acceptances'] and current['cancelled_by']
