# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Small genuine signed P06 histories with explicit elapsed-time accounting."""
import copy
import hashlib
import json
from pathlib import Path

from governed_fixtures import GovernedHarness, HUMAN, lc, op, delivery
import governed_workflow


WORKERS = Path(__file__).parent / 'fixtures/governed_dispatch'


class SchedulingHarness(GovernedHarness):
    """Use supported elapsed units without substituting any verification result."""

    def record(self, logical_id, record_type, record, **kwargs):
        """Convert fixture task limits to actual elapsed milliseconds before identity."""
        record = copy.deepcopy(record)
        if record_type == 'assignment':
            record['limits'] = [{'metric': 'elapsed_ms', 'unit': 'ms',
                                  'ceiling': record['limits'][0]['ceiling']}]
        return super().record(logical_id, record_type, record, **kwargs)

    def assignment(self, *args, **kwargs):
        """Return the exact recorded elapsed-time body, including cached setter refs."""
        reference, _ = super().assignment(*args, **kwargs)
        return reference, self._known_record(reference, 'assignment')


def worker(path, argv=None):
    """Return an actual fixture worker enrollment for path and explicit argv."""
    return {'provider': 'json-process/1',
            'argv': argv or ['/usr/bin/python3', '/worker/main.py'],
            'files': [{'path': str(path.resolve()), 'name': 'main.py',
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}


def workflow(host):
    """Bind ordinary host operations to the same real Store and disposable key."""
    config = {'protocol': 'jai.host-dispatch/1',
              'workers': [worker(WORKERS / 'worker.py', ['/usr/bin/python3', '/worker/main.py', 'author']),
                          worker(WORKERS / 'selection_worker.py')],
              'destinations': [], 'tools': [],
              'limits': {'packet_bytes': 1000000, 'total_bytes': 4000000}}
    return governed_workflow.Workflow(host.store, config)


def decision_ref(host, response, action):
    """Resolve the actual intrinsic action emitted by a committed response/receipt."""
    receipt = response.get('receipt', response)
    state = host.store.read()
    return next(reference for reference in receipt['created_versions']
                if state.versions[reference['version_id']]['kind'] == 'delivery.decision'
                and state.resolve(reference)['message']['payload']['action'] == action)


def local_conflict(host, *, suffix):
    """Publish an actual local reviewer finding about an explicitly incomplete result."""
    actor = host.setup_author(question='when', suffix=suffix + '-incomplete')
    subject, body = host.product(suffix + '-incomplete-answer', actor,
        material=[host.material(json.dumps({'requirement_satisfied': False}))])
    host.commit(host.submission(actor, subject, body))
    review = host.prepare_review(actor, subject, suffix=suffix + '-independent-review', verdict='rework_required')
    observed = json.loads(host.store._blob(host.store.read().resolve(subject)['material'][0]))
    if observed['requirement_satisfied'] is not False:
        raise AssertionError('The explicit incomplete-answer finding has no factual basis')
    reviewer = {'owner': review['record']['owner'], 'author': review['assignment'],
                'author_record': host.store.read().resolve(review['assignment'], 'assignment'),
                'author_context': review['context'], 'principal': review['principal']}
    finding, _ = host.product(suffix + '-local-finding', reviewer, kind='finding',
        material=[host.material('The returned answer explicitly reports that criterion C1 is unfulfilled.')],
        related=[{'slot_id': 'subject', 'refs': [subject]},
                 {'slot_id': 'criterion:C1', 'refs': [host.criteria]}])
    review['record']['findings'] = [finding]
    _, message = host.assessment_delivery(review, subject)
    host.commit(message)
    return finding


def open_episode(host, affected, *, suffix='episode', decisive=True):
    """Return an authentic assigned escalation, never a manually inserted episode."""
    conflict = local_conflict(host, suffix=suffix)
    actor = host.setup_author(suffix=suffix, responsibility='integrator', work_kind='integration')
    reference, _ = host.product(suffix, actor, kind='escalation',
        related=[{'slot_id': 'conflicts', 'refs': [conflict]}],
        episode={'root': None, 'previous': None, 'collection_head': host._proposal_head(),
                 'unfinished': affected, 'decisive': decisive})
    host.commit(host.message('escalation', {'assignment': actor['author'], 'package': reference,
        'conflicts': [conflict], 'affected': affected,
        'requested_decisions': ['Decide the exact scoped requirement and its affected work.']},
        sender=actor['principal'], context=actor['author_context']))
    return reference


def affected_refs(state, episode):
    """Read the complete actual reconciliation set from accepted episode and hold facts."""
    details = state._episode(episode)
    refs = {point['ref']['version_id']: point['ref'] for point in details['members']
            if state.versions[point['ref']['version_id']]['kind'] == 'delivery.assignment'}
    refs.update({identifier: state._reference(identifier) for (scope, identifier), hold in state.holds.items()
                 if scope == details['scope'] and hold['episode'] == details['root']})
    return [refs[identifier] for identifier in sorted(refs)]


def owner_resolution(host, episode, *, outcomes=None, decisions=None, package=None):
    """Sign the real L0 owner response for one exact L1 episode revision and impacts."""
    state = host.store.read()
    details = state._episode(episode)
    package = package or details['current']
    body = state.resolve(package, 'product')
    conflicts = next(binding['refs'] for binding in body['related'] if binding['slot_id'] == 'conflicts')
    impacts = [{'subject': {'ref': reference, 'use_scope': host.scope},
                'outcome': (outcomes or {}).get(reference['version_id'], 'unchanged'),
                'reason': 'The actual owner assessed this exact current scoped dependency.'}
               for reference in affected_refs(state, episode)]
    message = host.message('decision', {'action': 'resolve_escalation',
        'reason': 'Account for the complete current owner impact before resuming.',
        'escalation': details['root'], 'package': package, 'conflicts': conflicts,
        'impacts': impacts, 'decisions': decisions or [], 'authority_proof': '0' * 64}, sender=HUMAN)
    proof = host.human_proof(message, 'delivery-change')
    op.validate_human_intent_request(proof['request'])
    return decision_ref(host, host.commit(message, authority_proof=proof), 'resolve_escalation')


def reconciliation(host, episode, resolution, *, outcomes=None):
    """Describe every required disposition explicitly against its exact owner impact."""
    state = host.store.read()
    return {'action': 'resume', 'reason': 'Apply complete exact current owner impact coverage.',
            'escalation': state._episode(episode)['root'], 'resolutions': [resolution],
            'reconciliation': [{'subject': reference,
                'outcome': (outcomes or {}).get(reference['version_id'], 'retain'),
                'basis': state._closure({'ref': reference, 'use_scope': host.scope}),
                'impact': resolution} for reference in affected_refs(state, episode)]}


def signed_grant(host, episode, assignments, *, ceiling=1000, expires_at_ms=None, consumer=None):
    """Use the real human wrapper and ordinary operator ingestion for bounded risk."""
    consumer = consumer or workflow(host)
    state = host.store.read()
    inputs = [point for reference in assignments for point in state._dependencies(state.resolve(reference, 'assignment'))]
    inputs = sorted({lc.canonical(point): point for point in inputs}.values(), key=lc.canonical)
    expiry = expires_at_ms or min(state.resolve(reference)['deadline_ms'] for reference in assignments)
    payload = {'action': 'speculate', 'reason': 'Explicitly accept bounded speculative test execution.',
               'escalation': episode, 'assignments': assignments, 'inputs': inputs,
               'limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': ceiling}],
               'expires_at_ms': expiry}
    # Ordinary fixture work has no key; this reserved human intent needs enrollment.
    _ = host.signers
    prepared = consumer.prepare_decision(payload)
    proof = host.human_proof(prepared['message'], 'delivery-change')
    op.validate_human_intent_request(proof['request'])
    response = consumer.submit_decision(prepared['message'], proof)
    return decision_ref(host, response, 'speculate'), prepared['message'], proof


def captured_choice(host, actor, context):
    """Prepare a synthetic unit-fixture choice through the genuine signed return path."""
    payload = {'action': 'select_execution', 'assignment': actor['author'],
        'previous': host.store.read().execution_plans.get((actor['author']['version_id'], host.scope)),
        'specialties': ['software-engineer'], 'provider': 'json-process/1',
        'workload_class': 'fixture-' + actor['author_record']['responsibility'],
        'model_selector': 'fixture-' + actor['author_record']['responsibility'],
        'reason': 'Explicit fixture choice; native execution is tested separately.', 'authority_proof': None}
    message = host.message('decision', payload, sender=actor['principal'], context=context)
    return decision_ref(host, host.commit(message), 'select_execution')


def info_request(host, actor, context, *, recipient=None, question='State the missing local requirement.'):
    """Return an attributable information request without creating an output PASS."""
    return host.message('information_request', {'assignment': actor, 'needed': [],
        'question': question, 'blocked_obligations': [host.criteria]},
        sender={'kind': 'assignment', 'ref': actor}, context=context, recipient=recipient)
