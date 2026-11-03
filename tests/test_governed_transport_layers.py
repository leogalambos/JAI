# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""One real transport-only L1–L6 history, with a first-hop execution checkpoint.

Run this module in one pytest process to share its module-scoped history between
both nodes. These are interface/ownership checks, not six complete architectures.
Every chooser, producer, independent review and receiving entity executes in P04.
The first measured hop took 216.7 seconds; 80 native phases already exceed a
20-minute constant-rate projection, before journal growth. The fixture declares
a finite two-hour total allowance. Individual child phases remain bounded by
their existing one-minute limit; production timeouts are unchanged.
"""
import copy
import hashlib
import json
from pathlib import Path
import time

import pytest

from governed_fixtures import GovernedHarness, lc, delivery
from governed_stage_checkpoint import save_checkpoint
from test_governed_dispatch import _ElapsedHarness, _execution
import governed_workflow


WORKER = Path(__file__).parent / 'fixtures/governed_dispatch/transport_worker.py'
CHOOSER = WORKER.with_name('selection_worker.py')


def _enrolled(path):
    return {'provider': 'json-process/1', 'argv': ['/usr/bin/python3', '/worker/main.py'],
            'files': [{'path': str(path.resolve()), 'name': 'main.py',
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}


class _TransportHarness(_ElapsedHarness):
    """Capture real execution bytes and an explicit finite transport-only profile."""

    def _routing_source(self):
        execution = _execution(_enrolled(WORKER))
        for responsibility in ('setter', 'integrator', 'integration_reviewer', 'receiver'):
            self.route_executions[responsibility] = copy.deepcopy(execution)
        source = GovernedHarness._routing_source(self)
        descriptor = lc.loads(self.store._blob(source['material'][0]))
        for handle in ('foreign-output', 'foreign-layer-output'):
            descriptor['capabilities']['effects'].append(
                {'operation': 'materialize', 'tool_policy': None, 'destination_handle': handle})
        for limit in descriptor['capabilities']['limits']:
            if limit['metric'] == 'elapsed_ms':
                limit['ceiling'] = 2 * 60 * 60 * 1000
        source['material'][0] = self.store.put_blob(lc.canonical(descriptor))
        return source

    def bootstrap_message(self, **kwargs):
        message = super().bootstrap_message(**kwargs)
        profile = message['payload']['profile']['record']
        profile['obligations'] = []
        for layer in range(1, 7):
            for role, kind in (('integration_review', 'bundle'), ('receiving_acceptance', 'handoff')):
                profile['obligations'].append({'slot_id': f'transport-L{layer}-{role}',
                    'owner': self.owner(layer=layer, work_kind='integration'), 'subject_kind': kind,
                    'role': role, 'required_kind': 'assessment', 'minimum': 1, 'maximum': 1,
                    'allow_exclusion': False, 'exclusion_owner': None})
        self.profile = self.ref('profile', 'profile', profile)
        message['message_id'] = delivery.message_id(message)
        return message


class _Scenario:
    """Keep only immutable receipt references; every operation uses the real Store."""

    def __init__(self, directory, monkeypatch):
        self.directory = directory
        self.host = _TransportHarness(directory / 'engagement', monkeypatch,
            engagement='cumulative-layer-transport', scenario_duration_ms=2 * 60 * 60 * 1000)
        # Total-work allowance does not extend signed per-request proof windows.
        self.host.control_duration_ms = 300000
        self.host.bootstrap()
        self.current_layer = 1
        workflow = self.workflow(1)
        entry = workflow.entry('default', 'service-controls',
            [{'metric': 'elapsed_ms', 'unit': 'ms', 'ceiling': 2 * 60 * 60 * 1000}],
            int(time.time() * 1000) + 2 * 60 * 60 * 1000)
        self.coordinator = entry['assignment']
        self.layers = {}
        self.checkpoint = None
        self.native_phases = 0
        self.measured_usage = 0

    def workflow(self, layer):
        paths = {name: self.directory / ('output-L' + str(layer)) / name
                 for name in ('owned', 'foreign-same', 'foreign-layer')}
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
        owner = self.host.owner(layer=layer, work_kind='integration')
        other = self.host.owner(layer=layer % 6 + 1, work_kind='integration')
        foreign = self.host.owner(layer=layer, work_kind='integration', work_item='foreign-service')
        config = {'protocol': 'jai.host-dispatch/1', 'workers': [_enrolled(WORKER), _enrolled(CHOOSER)],
            'destinations': [{'handle': 'owned-output', 'owner': owner, 'root': str(paths['owned'])},
                             {'handle': 'foreign-output', 'owner': foreign, 'root': str(paths['foreign-same'])},
                             {'handle': 'foreign-layer-output', 'owner': other, 'root': str(paths['foreign-layer'])}],
            'tools': [], 'limits': {'packet_bytes': 1000000, 'total_bytes': 4000000}}
        return governed_workflow.Workflow(self.host.store, config)

    def step(self, reference, layer):
        workflow = self.workflow(layer)
        save_checkpoint(self.host.directory / 'stage-checkpoint.json', self.host,
            workflow, reference, stage='L' + str(layer) + ':' + reference['logical_id'],
            refs={'coordinator': self.coordinator,
                  'completed_bundles': [item['bundle'] for item in self.layers.values()]})
        selected = workflow.run(reference, 'selection')
        assert selected['completion']['status'] == 'committed', selected
        choices = [ref for ref in selected['completion']['receipt']['created_versions']
                   if ref['logical_id'].startswith('decision:')]
        assert len(choices) == 1
        result = workflow.run(reference, 'work', selection=choices[0])
        assert result['completion']['status'] == 'committed', result
        self.native_phases += 2
        self.measured_usage += selected['usage_ms'] + result['usage_ms']
        return result['completion']['receipt']['created_versions']

    @staticmethod
    def created(references, logical_id):
        result = [reference for reference in references if reference['logical_id'] == logical_id]
        assert len(result) == 1, (logical_id, references)
        return result[0]

    def advance(self, last_layer):
        while self.current_layer <= last_layer:
            layer = self.current_layer
            started = time.monotonic()
            coordinator = self.coordinator
            references = self.step(coordinator, layer)
            integrator = self.created(references, 'transport-integrator-L' + str(layer))
            bundle = self.created(self.step(integrator, layer), 'transport-bundle-L' + str(layer))
            reviewer = self.created(self.step(coordinator, layer), 'transport-integration_reviewer-L' + str(layer))
            assessment = self.created(self.step(reviewer, layer), 'transport-review-L' + str(layer) + '-integration')
            handoff = self.created(self.step(coordinator, layer), 'transport-handoff-L' + str(layer))
            state = self.host.store.read()
            product = state.resolve(bundle, 'product')
            report = json.loads(self.host.store._blob(product['material'][1]))
            assert report['layer'] == layer and report['owned']['ok']
            assert report['foreign_same_layer']['error']['code'] == 'P_SCOPE'
            assert report['foreign_layer']['error']['code'] == 'P_SCOPE'
            assert report['catalogue_count'] > 100 and report['unselected_instruction_readable']
            owned = self.directory / ('output-L' + str(layer)) / 'owned' / product['material'][0]
            assert owned.read_bytes() == self.host.store._blob(product['material'][0])
            assert not list((owned.parent.parent / 'foreign-same').iterdir())
            assert not list((owned.parent.parent / 'foreign-layer').iterdir())
            assert state.resolve(integrator, 'assignment')['assigned_actor'] != state.resolve(reviewer, 'assignment')['assigned_actor']
            assert state.provenance[bundle['version_id']]['context'] != state.provenance[assessment['version_id']]['context']
            review = state.resolve(assessment, 'assessment')
            assert review['subject'] == bundle and review['verdict'] == 'supported'
            status = self.workflow(layer).status({'ref': bundle, 'use_scope': 'default'})
            assert status['qualified'] and not status['complete_layer'] and not status['accepted']
            offered = {'ref': handoff, 'use_scope': 'default'}
            with pytest.raises(lc.ERROR) as denied:
                state.local_entry(offered, 'author')
            assert denied.value.code == 'P_SCOPE'
            if layer < 6:
                proposal = state.local_entry(offered, 'receiver')
                assert proposal['record']['owner'] == self.host.owner(layer=layer + 1, work_kind='integration')
                assert proposal['record']['routing'] == {'policy': self.host.routing_policy}
                receiving = self.workflow(layer + 1).local_entry(offered, 'receiver')['assignment']
                accepted = self.created(self.step(receiving, layer + 1),
                                       'transport-review-L' + str(layer + 1) + '-receiving')
                self.step(coordinator, layer)
                entry = self.workflow(layer + 1).local_entry(offered, 'setter', acceptance=accepted)
                self.coordinator = entry['assignment']
            else:
                with pytest.raises(lc.ERROR) as boundary:
                    state.local_entry(offered, 'receiver')
                assert boundary.value.code == 'P_SCOPE'
            self.layers[layer] = {'bundle': bundle, 'handoff': handoff, 'review': assessment,
                                  'seconds': time.monotonic() - started}
            self.current_layer += 1
            if layer == 1:
                self.checkpoint = self.host.store.read().head
                print('FIRST_HOP_SECONDS=' + str(self.layers[1]['seconds']), flush=True)


@pytest.fixture(scope='module')
def scenario(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield _Scenario(tmp_path_factory.mktemp('cumulative-layer-transport'), monkeypatch)


def test_first_genuine_hop_establishes_layer_two_local_gateway(scenario):
    """The first executed hop gates continuation of this same signed history."""
    scenario.advance(1)
    assert scenario.current_layer == 2 and scenario.checkpoint is not None
    assert set(scenario.layers) == {1}


def test_same_history_continues_through_all_six_layer_boundaries(scenario):
    """Continue the module checkpoint instead of constructing five new prefixes."""
    first_checkpoint = scenario.checkpoint
    scenario.advance(6)
    state = scenario.host.store.read()
    if first_checkpoint is not None:
        assert first_checkpoint in {transaction['hash'] for transaction in state.transactions}
    assert set(scenario.layers) == set(range(1, 7))
    assert scenario.native_phases > 12 and scenario.measured_usage > 0
    assert state.initialized
