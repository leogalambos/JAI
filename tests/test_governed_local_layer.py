# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One genuine local six-question history, with a reusable first-question gate."""
import base64
import copy
import hashlib
import json
import time
from pathlib import Path

import pytest

from governed_fixtures import GovernedHarness
from governed_stage_checkpoint import save_checkpoint
import governed_workflow
import governed_dispatch
import lifecycle as lc


WORKERS = Path(__file__).parent / 'fixtures/governed_dispatch'


def _worker(path):
    return {'provider': 'json-process/1', 'argv': ['/usr/bin/python3', '/worker/main.py'],
            'files': [{'path': str(path.resolve()), 'name': 'main.py',
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}


class _LocalHarness(GovernedHarness):
    def material(self, text):
        if text == 'Bounded service requirements A.\n':
            text = json.dumps({'required_boundary': 'internal-service', 'valid_zones': ['east', 'west'],
                               'questions': ['what', 'why', 'how', 'who', 'where', 'when'],
                               'integration_rule': 'Different processing and endpoint zones require an explicit exact link.'})
        return super().material(text)

    def _routing_source(self):
        worker = _worker(WORKERS / 'layer_worker.py')
        execution = {'provider': worker['provider'], 'argv': worker['argv'],
                     'files': [{key: value[key] for key in ('name', 'sha256')} for value in worker['files']]}
        for role in ('setter', 'author', 'reviewer', 'integrator', 'integration_reviewer', 'receiver'):
            self.route_executions[role] = execution
        source = super()._routing_source()
        descriptor = lc.loads(self.store._blob(source['material'][0]))
        descriptor['capabilities'] = {'effects': [
            {'operation': name, 'tool_policy': None, 'destination_handle': None}
            for name in ('read', 'propose')],
            'limits': [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 7200000}]}
        source['material'][0] = self.store.put_blob(lc.canonical(descriptor))
        return source


class _Scenario:
    def __init__(self, host, workflow):
        self.host, self.workflow = host, workflow
        self.root = None
        self.setters, self.answers = {}, {}

    def _run(self, reference):
        save_checkpoint(self.host.directory / 'stage-checkpoint.json', self.host,
            self.workflow, reference, stage=reference['logical_id'],
            refs={'root': self.root, 'setters': self.setters, 'answers': self.answers})
        selected = self.workflow.run(reference, 'selection')
        state = self.host.store.read()
        choice = next(item for item in selected['completion']['receipt']['created_versions']
                      if state.versions[item['version_id']]['kind'] == 'delivery.decision')
        result = self.workflow.run(reference, 'work', selection=choice)
        assert result['completion']['status'] == 'committed', result
        return result

    def _created(self, result, family):
        state = self.host.store.read()
        return [(ref, state.resolve(ref)) for ref in result['completion']['receipt']['created_versions']
                if state.versions[ref['version_id']]['kind'] == 'delivery.' + family]

    def _child(self, result, responsibility):
        matches = [(ref, body) for ref, body in self._created(result, 'assignment')
                   if body['responsibility'] == responsibility and 'unapproved' not in body['assigned_actor']]
        assert len(matches) == 1, matches
        return matches[0]

    def _start(self):
        if self.root is not None:
            return
        entry = self.workflow.entry('default', 'service-controls',
            [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 7200000}], int(time.time() * 1000) + 7200000)
        self.root = entry['assignment']
        result = self._run(self.root)
        children = self._created(result, 'assignment')
        self.setters = {body['owner']['question']: reference for reference, body in children}
        assert set(self.setters) == {'what', 'why', 'how', 'who', 'where', 'when'}

    def question(self, question):
        self._start()
        if question in self.answers:
            return self.answers[question]
        setter = self.setters[question]
        author, original = self._child(self._run(setter), 'author')
        state = self.host.store.read()
        assert state.assignment_feedback(original) == []
        authored = self._run(author)
        candidate, _ = self._created(authored, 'product')[0]
        state = self.host.store.read()
        assert not state._produced_under(candidate, self.root, state.resolve(self.root, 'assignment')['owner'])
        reviewer, reviewer_body = self._child(self._run(setter), 'reviewer')
        reviewed = self._run(reviewer)
        assessment, assessment_body = self._created(reviewed, 'assessment')[0]
        if question in {'what', 'why'}:
            assert assessment_body['verdict'] == 'rework_required'
            assert assessment_body['findings']
            revised = self._run(setter)
            replacement, replacement_body = self._child(revised, 'author')
            if question == 'what':
                assert replacement_body['criteria'] == original['criteria']
            else:
                assert replacement_body['criteria'] != original['criteria']
            assert replacement_body['inherited'] == original['inherited']
            state = self.host.store.read()
            feedback = state.assignment_feedback(replacement_body)
            assert feedback and all(item['historical'] for item in feedback)
            assert feedback[-1]['findings'][0]['ref'] == assessment_body['findings'][0]
            assert not state._status(candidate)['applicable']
            if question == 'what':
                material = feedback[-1]['findings'][0]['material'][0]
                raw = base64.b64decode(material['data'])
                (self.host.store.material / material['blob_id']).unlink()
                try:
                    with pytest.raises(lc.ERROR) as failure:
                        state.assignment_feedback(replacement_body)
                    assert failure.value.code == 'P_CONTEXT'
                finally:
                    assert self.host.store.put_blob(raw) == material['blob_id']
            authored = self._run(replacement)
            candidate, _ = self._created(authored, 'product')[0]
            assert candidate['logical_id'].endswith(':2')
            issuance = self._run(setter)
            reviewer, second_reviewer = self._child(issuance, 'reviewer')
            assert second_reviewer['assigned_actor'] == reviewer_body['assigned_actor']
            if question == 'what':
                unapproved = next(ref for ref, body in self._created(issuance, 'assignment')
                                  if body['assigned_actor'] == 'what:unapproved-reviewer')
                selected = self.workflow.run(unapproved, 'selection')
                state = self.host.store.read()
                choice = next(ref for ref in selected['completion']['receipt']['created_versions']
                              if state.versions[ref['version_id']]['kind'] == 'delivery.decision')
                before = self.host.path.read_bytes()
                with pytest.raises(governed_dispatch.DispatchError) as failure:
                    self.workflow.run(unapproved, 'work', selection=choice)
                assert failure.value.code == 'P_PROOF'
                assert self.host.path.read_bytes() == before
            assert self.host.store.read().assignment_feedback(second_reviewer)
            reviewed = self._run(reviewer)
            assessment, assessment_body = self._created(reviewed, 'assessment')[0]
        assert assessment_body['verdict'] == 'supported'
        answer = self.host.store.read().resolve(candidate, 'product')
        content = json.loads(self.host.store._blob(answer['material'][0]))
        assert content['boundary'] == 'internal-service'
        self._run(setter)
        state = self.host.store.read()
        assert state.evaluate(candidate)['qualified']
        assert state._produced_under(candidate, self.root, state.resolve(self.root, 'assignment')['owner'])
        self.answers[question] = candidate
        return candidate

    def complete(self):
        for question in ('what', 'why', 'how', 'who', 'where', 'when'):
            self.question(question)
        author, _ = self._child(self._run(self.root), 'integrator')
        bundle_result = self._run(author)
        bundle, _ = self._created(bundle_result, 'product')[0]
        assert not self.workflow.status({'ref': bundle, 'use_scope': 'default'})['complete_layer']
        reviewer, prior_reviewer = self._child(self._run(self.root), 'integration_reviewer')
        reviewed = self._run(reviewer)
        negative, negative_body = self._created(reviewed, 'assessment')[0]
        assert negative_body['verdict'] == 'rework_required'
        state = self.host.store.read()
        assert all(state.evaluate(answer)['qualified'] for answer in self.answers.values())
        answer_material = {name: json.loads(self.host.store._blob(state.resolve(ref)['material'][0]))
                           for name, ref in self.answers.items()}
        assert answer_material['what']['zone'] == 'east'
        assert answer_material['where']['zone'] == 'west'
        assert json.loads(self.host.store._blob(state.resolve(bundle)['material'][0]))['mode'] == 'colocated'
        assert not self.workflow.status({'ref': bundle, 'use_scope': 'default'})['complete_layer']
        author, revised = self._child(self._run(self.root), 'integrator')
        assert self.host.store.read().assignment_feedback(revised)
        bundle, _ = self._created(self._run(author), 'product')[0]
        assert bundle['logical_id'].endswith(':2')
        repaired = json.loads(self.host.store._blob(self.host.store.read().resolve(bundle)['material'][0]))
        assert repaired['mode'] == 'explicit_link' and repaired['link'] == {'from': 'east', 'to': 'west'}
        reviewer, new_reviewer = self._child(self._run(self.root), 'integration_reviewer')
        assert new_reviewer['assigned_actor'] != prior_reviewer['assigned_actor']
        replacement_feedback = self.host.store.read().assignment_feedback(new_reviewer)
        assert any(item['replacement'] == reviewer and item['findings'] for item in replacement_feedback)
        positive, body = self._created(self._run(reviewer), 'assessment')[0]
        assert body['verdict'] == 'supported'
        self._run(self.root)
        assert self.host.store.evaluate(bundle)['qualified']
        publisher, _ = self._child(self._run(self.root), 'integrator')
        self._run(publisher)
        assert self.workflow.status({'ref': bundle, 'use_scope': 'default'})['complete_layer']
        handoff_author, _ = self._child(self._run(self.root), 'integrator')
        handoff, _ = self._created(self._run(handoff_author), 'product')[0]
        assert not self.host.store.evaluate(handoff)['qualified']
        receiver = self.workflow.local_entry({'ref': handoff, 'use_scope': 'default'}, 'receiver')['assignment']
        acceptance, accepted = self._created(self._run(receiver), 'assessment')[0]
        assert accepted['verdict'] == 'accepted'
        self._run(self.root)
        assert self.host.store.evaluate(handoff)['qualified']
        return handoff


@pytest.fixture(scope='module')
def scenario(tmp_path_factory):
    # Both nodes exercise one history; either node can independently construct
    # the required prefix, and every assertion queries the real current Store.
    directory = tmp_path_factory.mktemp('local-six-question')
    with pytest.MonkeyPatch.context() as monkeypatch:
        # About 107 native phases: 216.7s/14 measured phases gives a 27.6-minute
        # linear floor. A fourfold replay-growth margin stays below two hours.
        host = _LocalHarness(directory, monkeypatch, engagement='local-six-question',
                             scenario_duration_ms=7200000)
        host.control_duration_ms = 300000
        host.bootstrap(include_neighbor=True)
        config = {'protocol': 'jai.host-dispatch/1',
                  'workers': [_worker(WORKERS / 'selection_worker.py'), _worker(WORKERS / 'layer_worker.py')],
                  'destinations': [], 'tools': [], 'limits': {'packet_bytes': 1000000, 'total_bytes': 8000000}}
        yield _Scenario(host, governed_workflow.Workflow(host.store, config))


def test_local_question_owned_rework_preserves_findings_and_stable_reviewer(scenario):
    assert scenario.question('what')['logical_id'] == 'what:answer:2'


def test_same_local_layer_completes_six_questions_independent_integration_and_receiving(scenario):
    handoff = scenario.complete()
    assert scenario.host.store.evaluate(handoff)['qualified']
