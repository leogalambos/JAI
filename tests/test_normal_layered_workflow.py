# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise ordinary layered CLI progression without generic graph fixtures."""
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from lifecycle_fixtures import SyntheticOperator

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'normal_workflow_fabric', ROOT / '.ai/runtime/fabric/fabric.py')
fabric = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fabric)


@pytest.mark.parametrize('label,role,reverse', [
    ('supports', 'evidence', False), ('requests', 'contract', False),
    ('derives', 'requirement', False), ('refines', 'requirement', False),
    ('consolidated_into', 'evidence', False), ('implements', 'requirement', True)])
def test_graph_reliance_derives_every_causal_direction(label, role, reverse):
    relation = fabric.lifecycle.graph_reliance({
        'label': label, 'src_version': 'source', 'dst_version': 'target'})
    assert relation == {'scope': 'default', 'role': role,
        'dependent': 'source' if reverse else 'target',
        'prerequisite': 'target' if reverse else 'source'}


def test_graph_reliance_noncausal_boundary_and_missing_endpoint_failure():
    assert fabric.lifecycle.graph_reliance({'label': 'reviewed_by'}) is None
    with pytest.raises(KeyError):
        fabric.lifecycle.graph_reliance({'label': 'supports', 'src_version': 'source'})


def test_routine_intent_answer_rejects_same_layer_support():
    lifecycle = fabric.lifecycle
    state = lifecycle.State()
    state.apply({'op': 'init', 'data': {'scope': 'default', 'policy': lifecycle.policy()}})

    def node(identifier, kind, **extra):
        content = {'id': identifier, 'type': kind, 'layer': 1, 'text': identifier, **extra}
        bindings = content.pop('bindings', {})
        value = lifecycle.manifest(identifier, kind, content, bindings)
        version = lifecycle.version_id(value)
        state.apply({'op': 'version', 'data': {'version_id': version, 'manifest': value}})
        state.apply({'op': 'select', 'data': {'scope': 'default', 'logical_id': identifier,
                                            'version_id': version, 'previous': None}})
        graph_node = {**content, 'bindings': bindings, 'version_id': version,
                      'object_hash': 'sha256:' + version}
        state.apply({'op': 'node', 'data': graph_node})
        return graph_node

    def edge(source, label, target):
        value = {'src': source['id'], 'dst': target['id'], 'label': label,
                 'src_version': source['version_id'], 'dst_version': target['version_id']}
        required = lifecycle.graph_reliance(value)
        state.apply({'op': 'rely', 'data': required})
        state.apply({'op': 'edge', 'data': value})

    requirement = node('req-0001', 'req')
    contract = node('ctr-0001', 'ctr')
    sibling = node('frag-0001', 'frag')
    answer = node('frag-0002', 'frag', requirement=requirement['id'],
                  profile='jai.intent-output/1', bindings={
                      'contract': {'refs': [contract['version_id']]}})
    edge(requirement, 'derives', contract)
    edge(requirement, 'requests', answer)
    edge(sibling, 'supports', answer)
    with pytest.raises(ValueError, match='reviewed child'):
        state.apply({'op': 'routine', 'data': {
            'family': 'answer', 'scope': 'default', 'subject': answer['version_id']}})
    assert state.predicates(answer['version_id'])['validity'] == 'pending'
    assert not state.proofs


@pytest.mark.parametrize('payload', [b'', b'Public specification bytes.\n'])
def test_record_input_binds_exact_initial_bytes(tmp_path, monkeypatch, payload):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path / 'ledger'))
    fabric.cmd_init(SimpleNamespace(engagement='input', intent='Check input',
        owner='Synthetic owner', success=None, boundary=None))
    path = tmp_path / 'source.txt'
    path.write_bytes(payload)
    fabric.cmd_record_input(SimpleNamespace(engagement='input',
        logical_id='public-source', kind='source', file=str(path)))
    state = fabric.open_fabric('input').lifecycle
    identifier = state.selections[('default', 'public-source')]
    assert state.versions[identifier]['content']['blob'] == fabric.lifecycle.blob(payload)
    assert state.predicates(identifier)['validity'] == 'valid'
    assert not state.predicates(identifier)['sufficient']
    assert not state.accept_authorities


def test_record_input_rejects_replacement_and_missing_bytes_atomically(tmp_path, monkeypatch):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path / 'ledger'))
    fabric.cmd_init(SimpleNamespace(engagement='input', intent='Check input',
        owner='Synthetic owner', success=None, boundary=None))
    path = tmp_path / 'source.txt'
    path.write_bytes(b'First source')
    args = SimpleNamespace(engagement='input', logical_id='public-source',
                           kind='source', file=str(path))
    fabric.cmd_record_input(args)
    ledger = Path(fabric.log_path('input'))
    before = ledger.read_bytes()
    path.write_bytes(b'Replacement source')
    with pytest.raises(ValueError, match='governed'):
        fabric.cmd_record_input(args)
    assert ledger.read_bytes() == before
    args.logical_id = 'new-source'
    args.file = str(tmp_path / 'missing.txt')
    with pytest.raises(OSError):
        fabric.cmd_record_input(args)
    assert ledger.read_bytes() == before


@pytest.mark.parametrize('cancelled_state', ['invalid', 'revoked'])
def test_routine_input_cannot_reactivate_a_previously_cancelled_version(cancelled_state):
    lifecycle = fabric.lifecycle
    state = lifecycle.State()
    state.apply({'op': 'init', 'data': {'scope': 'default', 'policy': lifecycle.policy()}})
    value = lifecycle.manifest('cancelled-source', 'source', {
        'blob': lifecycle.blob(b'Original source'),
        'capture_profile': 'jai.byte-observation/1'})
    identifier = lifecycle.version_id(value)
    state.apply({'op': 'version', 'data': {'version_id': identifier, 'manifest': value}})
    state.apply({'op': 'select', 'data': {'scope': 'default',
        'logical_id': 'cancelled-source', 'version_id': identifier, 'previous': None}})
    state.apply({'op': 'locate', 'data': {'version_id': identifier, 'path': '/unused/source'}})
    for validity in (cancelled_state, 'pending'):
        state.apply({'op': 'state', 'data': {'scope': 'default',
            'version_id': identifier, 'changes': {'validity': validity}}}, authorized=True)
    with pytest.raises(ValueError, match='fresh pending'):
        state.apply({'op': 'routine', 'data': {'scope': 'default',
            'family': 'input', 'subject': identifier}})
    assert not state.proofs
    assert not state.accept_authorities


@pytest.mark.parametrize('forgery', ['omitted', 'wrong-role', 'wrong-subject'])
def test_forged_actual_support_edge_cannot_omit_exact_dependency(tmp_path, monkeypatch, forgery):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path / 'ledger'))
    fabric.cmd_init(SimpleNamespace(engagement='forged-edge', intent='Check causal closure',
        owner='Synthetic owner', success=None, boundary=None))
    graph = fabric.open_fabric('forged-edge')
    evidence = graph.add_node('evd', 6, 'Actual captured observation', confidence='observation')
    fragment = graph.add_node('frag', 6, 'Claim requiring actual observation')
    edge = {'op': 'edge', 'data': {
        'src': evidence['id'], 'dst': fragment['id'], 'label': 'supports',
        'src_version': evidence['version_id'], 'dst_version': fragment['version_id']}}
    operations = []
    if forgery != 'omitted':
        relation = {'dependent': fragment['version_id'],
                    'prerequisite': evidence['version_id'], 'scope': 'default',
                    'role': 'source' if forgery == 'wrong-role' else 'evidence'}
        if forgery == 'wrong-subject':
            relation['dependent'], relation['prerequisite'] = (
                relation['prerequisite'], relation['dependent'])
        operations.append({'op': 'rely', 'data': relation})
    operations.append(edge)
    lifecycle = fabric.lifecycle
    head = graph.transactions[-1]['hash']
    forged = lifecycle.envelope('forged-edge', head,
        len(graph.transactions) + 1, operations)
    with pytest.raises(ValueError, match='causal reliance'):
        lifecycle.replay(graph.transactions + [forged], 'forged-edge',
                         fabric.verify_lifecycle_proof)
    path = Path(fabric.log_path('forged-edge'))
    before = path.read_bytes()
    with pytest.raises(ValueError, match='causal reliance'):
        lifecycle.commit(path, 'forged-edge', head, operations,
                         fabric.verify_lifecycle_proof)
    assert path.read_bytes() == before
    assert not fabric.open_fabric('forged-edge').lifecycle.evaluate(
        fragment['version_id'], release=True)['eligible']


def test_existing_locator_overwrite_requires_governed_exact_effects(tmp_path, monkeypatch):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path / 'ledger'))
    fabric.cmd_init(SimpleNamespace(engagement='locator', intent='Check locator custody',
        owner='Synthetic owner', success=None, boundary=None))
    source, moved = tmp_path / 'source.txt', tmp_path / 'moved.txt'
    source.write_bytes(b'Maintained public specification')
    moved.write_bytes(source.read_bytes())
    fabric.cmd_record_input(SimpleNamespace(engagement='locator', logical_id='public-source',
                                            kind='source', file=str(source)))
    graph = fabric.open_fabric('locator')
    lifecycle = fabric.lifecycle
    identifier = graph.lifecycle.selections[('default', 'public-source')]
    path = Path(fabric.log_path('locator'))
    before, head = path.read_bytes(), graph.transactions[-1]['hash']
    overwrite = {'op': 'locate', 'data': {'version_id': identifier, 'path': str(moved)}}
    forged = lifecycle.envelope('locator', head, len(graph.transactions) + 1, [overwrite])
    with pytest.raises(ValueError, match='locator replacement'):
        lifecycle.replay(graph.transactions + [forged], 'locator', fabric.verify_lifecycle_proof)
    with pytest.raises(ValueError, match='locator replacement'):
        lifecycle.commit(path, 'locator', head, [overwrite], fabric.verify_lifecycle_proof)
    assert path.read_bytes() == before
    same = {'op': 'locate', 'data': {'version_id': identifier, 'path': str(source)}}
    lifecycle.commit(path, 'locator', head, [same], fabric.verify_lifecycle_proof)
    signer = SyntheticOperator(tmp_path, monkeypatch)
    spec = {'scope': 'default', 'reason': 'Move unchanged public source locator',
        'proposed': [{'manifest': graph.lifecycle.versions[identifier], 'locator': str(moved)}],
        'selections': [], 'reinstatements': [], 'verification': [],
        'invalidations': [], 'proofs': [],
        'allowed_verification_path': 'jai.byte-observation/1'}
    spec_path, request_path = tmp_path / 'move-spec.json', tmp_path / 'move-request.json'
    spec_path.write_text(json.dumps(spec))
    fabric.cmd_lifecycle_plan(SimpleNamespace(engagement='locator',
        spec=str(spec_path), out=str(request_path)))
    signer.apply(fabric, request_path)
    assert fabric.open_fabric('locator').lifecycle.locators[identifier] == str(moved)


@pytest.mark.parametrize('direction', ['incoming', 'outgoing'])
def test_unsigned_edge_cannot_reuse_real_signed_authority_topology(tmp_path, monkeypatch, direction):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path / 'ledger'))
    signer = SyntheticOperator(tmp_path, monkeypatch)
    fabric.cmd_init(SimpleNamespace(engagement='authority-topology',
        intent='Keep authority effects exact', owner='Synthetic owner',
        success=None, boundary=None))
    graph = fabric.open_fabric('authority-topology')
    conflict = graph.add_node('conf', 1, 'Original scoped conflict')
    escalation = graph.add_node('esc', 1, 'Original scoped escalation',
        code='outside_authority', effective='outside_authority')
    graph.add_edge(conflict['id'], 'escalates', escalation['id'])
    request = tmp_path / 'scoped-authority.json'
    fabric.cmd_authorise(SimpleNamespace(engagement=graph.eng, escalation=escalation['id'],
        decision='accept', signer='Synthetic human', rationale='Accept original scope only',
        expires=None, adopt=None, revise_text=None, supersedes=None,
        beyond_round_limit=False, request_out=str(request)))
    signer.apply(fabric, request)
    graph = fabric.open_fabric(graph.eng)
    authority = graph.nodes['auth-0001']
    assert authority['version_id'] in graph.lifecycle.decision_authorities
    if direction == 'incoming':
        source = graph.add_node('esc', 1, 'New unsigned escalation',
            code='outside_authority', effective='outside_authority')
        target, label = authority, 'resolved_by'
    else:
        source = authority
        target = graph.add_node('req', 1, 'New unsigned authority revision')
        label = 'revises'
    operation = {'op': 'edge', 'data': {
        'src': source['id'], 'dst': target['id'], 'label': label,
        'src_version': source['version_id'], 'dst_version': target['version_id']}}
    lifecycle = fabric.lifecycle
    head = graph.transactions[-1]['hash']
    forged = lifecycle.envelope(graph.eng, head, len(graph.transactions) + 1, [operation])
    with pytest.raises(ValueError, match='authority edge'):
        lifecycle.replay(graph.transactions + [forged], graph.eng,
                         fabric.verify_lifecycle_proof)
    path = Path(fabric.log_path(graph.eng))
    before = path.read_bytes()
    with pytest.raises(ValueError, match='authority edge'):
        lifecycle.commit(path, graph.eng, head, [operation], fabric.verify_lifecycle_proof)
    assert path.read_bytes() == before
    assert fabric.open_fabric(graph.eng).lifecycle.decision_authorities == {
        authority['version_id']}


def test_normal_six_layer_cli_reaches_exact_human_release(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path / 'ledger'))
    monkeypatch.setattr(fabric, 'MAX_STEPS', 120)
    signer = SyntheticOperator(tmp_path, monkeypatch)
    engagement = 'ordinary-six-layer'

    def invoke(*arguments, pending=False):
        monkeypatch.setattr(sys, 'argv', ['fabric.py', *arguments])
        result = fabric.main()
        output = capsys.readouterr().out
        assert result in ((3,) if pending else (None, 0)), output
        return output

    def write(name, value):
        path = tmp_path / name
        path.write_text(json.dumps(value), encoding='utf-8')
        return str(path)

    invoke('init', engagement, '--intent', 'Check the maintained public source',
           '--owner', 'Synthetic project owner')
    source = tmp_path / 'maintained-public-source.txt'
    source.write_text('The supported invariant is exactly 42.\n')
    invoke('record-input', engagement, '--logical-id', 'public-spec',
           '--kind', 'source', '--file', str(source))
    graph = fabric.open_fabric(engagement)
    source_version = graph.lifecycle.selections[('default', 'public-spec')]
    policy_version = graph.lifecycle.selections[('default', 'lifecycle-policy')]
    obligations = {'categories': {key: {'minimum': 1, 'allow_exclusion': False}
                                  for key in ('source', 'contract', 'policy')},
                   'evidence_roles': ['evidence'], 'review_roles': ['reviewer']}
    fields = dict(what='Check the exact supported invariant',
                  why='Establish a reproducible ordinary workflow',
                  who='Assigned layer role', where='Disposable workspace',
                  when='Before acceptance', how='Compare exact observation',
                  evidence='Deterministic captured observation',
                  escalate_if='The invariant cannot be established',
                  sanitise='Synthetic public data only')
    invoke('req', engagement, '--layer', '1', '--from', 'intent-0001',
           '--label', 'derives', '--text', fields['what'])
    arguments = [item for key, value in fields.items()
                 for item in ('--' + key.replace('_', '-'), value)]
    invoke('contract', engagement, '--from', 'req-0001', *arguments,
           '--obligations', write('obligations.json', obligations))

    def bindings(contract):
        graph = fabric.open_fabric(engagement)
        return {key: {'refs': [value]} for key, value in {
            'source': source_version, 'policy': policy_version,
            'contract': graph.nodes[contract]['version_id']}.items()}

    def ingest(contract, **values):
        packet = json.loads(invoke('context-packet', engagement, contract))
        return invoke('ingest', engagement, '--contract', contract,
                      write('reply.json', {'context_digest': packet['context_digest'],
                                           **values}))

    for index in range(1, 5):
        ingest(f'ctr-{index:04}', derived_requirements=[{
            'key': 'child', 'text': fields['what'],
            'contract': {**fields, 'obligations': obligations}}])
    observation = tmp_path / 'observed-invariant.txt'
    observation.write_text('Observed supported invariant: 42; PASS.\n')
    ingest('ctr-0005', fragments=[{'key': 'measured', 'text': 'The invariant is 42',
                                  'bindings': bindings('ctr-0005')}],
           evidence=[{'supports': ['measured'], 'source': 'Measured source invariant',
                      'confidence': 'deterministic', 'file': str(observation),
                      'bindings': bindings('ctr-0005')}])
    child = 'frag-0001'
    for layer in range(5, 0, -1):
        invoke('ingest-reviews', engagement, '--layer', str(layer),
               '--reviewer', f'Independent layer {layer} worker',
               '--model', 'synthetic-review', write('review.json', {'reviews': [{
                   'fragment': child, 'state': 'accepts',
                   'rationale': 'Exact observed source and all dependencies checked'}]}))
        if layer > 1:
            parent = f'ctr-{layer - 1:04}'
            ingest(parent, fragments=[{'key': 'upward',
                'text': 'The invariant follows from the reviewed child',
                'supported_by': [child], 'bindings': bindings(parent)}])
            child = f'frag-{7 - layer:04}'
    ledger_before_answer = Path(fabric.log_path(engagement)).read_bytes()
    with pytest.raises(ValueError, match='exact requirement'):
        fabric.cmd_answer(SimpleNamespace(engagement=engagement,
            requirement='req-0001', text='Incorrect issuer contract',
            supported_by=[child],
            bindings=write('wrong-issuer.json', bindings('ctr-0002'))))
    assert Path(fabric.log_path(engagement)).read_bytes() == ledger_before_answer
    invoke('answer', engagement, '--requirement', 'req-0001',
           '--text', 'The exact public source invariant is established',
           '--supported-by', child, '--bindings', write('bindings.json', bindings('ctr-0001')))
    output = 'frag-0006'
    graph = fabric.open_fabric(engagement)
    assert graph.steps_this_round() < 120
    assert graph.lifecycle.evaluate(graph.nodes[output]['version_id'])['eligible']
    assert not graph.lifecycle.evaluate(graph.nodes[output]['version_id'], release=True)['eligible']
    request = tmp_path / 'acceptance.json'
    invoke('review', engagement, output, '--layer', '0', '--state', 'accepts',
           '--rationale', 'Exact final closure checked', '--reviewer', 'Synthetic human',
           '--model', 'human', '--request-out', str(request), pending=True)
    signer.apply(fabric, request)
    assert 'RELEASABLE' in invoke('release', engagement, output)
    source.write_text('The supported invariant is now 43.\n')
    assert not fabric.open_fabric(engagement).lifecycle.evaluate(
        graph.nodes[output]['version_id'], release=True)['eligible']
    lifecycle = fabric.lifecycle
    replacement = lifecycle.manifest('public-spec', 'source', {
        'blob': lifecycle.blob(source.read_bytes()),
        'capture_profile': 'jai.byte-observation/1'})
    replacement_id = lifecycle.version_id(replacement)
    change = {'scope': 'default', 'reason': 'Maintained public source changed',
        'proposed': [{'manifest': replacement, 'locator': str(source)}],
        'selections': [{'logical_id': 'public-spec', 'version_id': replacement_id}],
        'reinstatements': [], 'verification': [], 'invalidations': [], 'proofs': [],
        'allowed_verification_path': 'jai.byte-observation/1'}
    update_request = tmp_path / 'source-update.json'
    invoke('lifecycle-plan', engagement, '--spec', write('change.json', change),
           '--out', str(update_request))
    signer.apply(fabric, update_request)
    changed = fabric.open_fabric(engagement)
    assert changed.lifecycle.predicates(source_version)['validity'] == 'invalid'
    assert changed.lifecycle.predicates(graph.nodes[output]['version_id'])['validity'] == 'invalid'
    assert changed.lifecycle.predicates(replacement_id)['validity'] == 'pending'
    source_ledger = Path(fabric.log_path(engagement))
    pending_bytes = source_ledger.read_bytes()
    other_locator = tmp_path / 'same-bytes-other-locator.txt'
    other_locator.write_bytes(source.read_bytes())
    with pytest.raises(ValueError, match='locator'):
        fabric.cmd_record_input(SimpleNamespace(engagement=engagement,
            logical_id='public-spec', kind='source', file=str(other_locator)))
    assert source_ledger.read_bytes() == pending_bytes
    invoke('record-input', engagement, '--logical-id', 'public-spec',
           '--kind', 'source', '--file', str(source))
    source_version = replacement_id
    fresh_capture = tmp_path / 'fresh-observed-invariant.txt'
    fresh_capture.write_text('Observed supported invariant: 43; PASS.\n')
    ingest('ctr-0005', fragments=[{'key': 'fresh', 'text': 'The invariant is now 43',
                                  'bindings': bindings('ctr-0005')}],
           evidence=[{'supports': ['fresh'], 'source': 'Fresh source measurement',
                      'confidence': 'deterministic', 'file': str(fresh_capture),
                      'bindings': bindings('ctr-0005')}])
    child = 'frag-0007'
    for layer in range(5, 0, -1):
        invoke('review', engagement, child, '--layer', str(layer),
               '--state', 'accepts', '--reviewer', f'Independent layer {layer}',
               '--model', 'synthetic-review', '--rationale',
               'Fresh exact source and dependency closure independently checked')
        if layer > 1:
            parent = f'ctr-{layer - 1:04}'
            ingest(parent, fragments=[{'key': 'fresh-upward',
                'text': 'Fresh reviewed child establishes the changed invariant',
                'supported_by': [child], 'bindings': bindings(parent)}])
            child = f'frag-{13 - layer:04}'
    invoke('answer', engagement, '--requirement', 'req-0001',
           '--text', 'The changed public source invariant is established',
           '--supported-by', child,
           '--bindings', write('fresh-bindings.json', bindings('ctr-0001')))
    fresh_output = 'frag-0012'
    fresh = fabric.open_fabric(engagement)
    assert fresh.steps_this_round() < 120
    fresh_version = fresh.nodes[fresh_output]['version_id']
    assert fresh.lifecycle.evaluate(fresh_version)['eligible']
    assert not fresh.lifecycle.evaluate(fresh_version, release=True)['eligible']
    fresh_acceptance = tmp_path / 'fresh-acceptance.json'
    invoke('review', engagement, fresh_output, '--layer', '0', '--state', 'accepts',
           '--rationale', 'Fresh exact closure checked after source replacement',
           '--reviewer', 'Synthetic human', '--model', 'human',
           '--request-out', str(fresh_acceptance), pending=True)
    signer.apply(fabric, fresh_acceptance)
    assert 'RELEASABLE' in invoke('release', engagement, fresh_output)
    final = fabric.open_fabric(engagement)
    assert final.steps_this_round() < 120
    assert not final.lifecycle.evaluate(graph.nodes[output]['version_id'], release=True)['eligible']
