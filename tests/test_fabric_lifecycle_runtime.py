# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Fresh CLI and externally signed lifecycle integration, using synthetic humans only."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import uuid

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from lifecycle_fixtures import accepted_graph
import operator_actions as op

SPEC = importlib.util.spec_from_file_location('lifecycle_runtime_fabric', ROOT / '.ai/runtime/fabric/fabric.py')
fabric = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fabric)


def update(tmp_path, signer, engagement, *, proposed=(), selections=(), verification=(), proofs=(), invalidations=()):
    """Use real planning and receipt verification; returned request is reviewable test data."""
    stem = str(uuid.uuid4())
    spec = {'scope': 'default', 'reason': 'Synthetic governed integration update',
            'proposed': list(proposed), 'selections': list(selections),
            'verification': list(verification), 'proofs': list(proofs),
            'invalidations': list(invalidations), 'reinstatements': [],
            'allowed_verification_path': 'synthetic-observation'}
    spec_path, request_path = tmp_path / (stem + '.spec.json'), tmp_path / (stem + '.request.json')
    spec_path.write_text(json.dumps(spec))
    fabric.cmd_lifecycle_plan(SimpleNamespace(engagement=engagement, spec=str(spec_path), out=str(request_path)))
    signer.apply(fabric, request_path)
    return json.loads(request_path.read_text())


def pending_plan(tmp_path, engagement, spec):
    """Prepare one unsigned exact spec without mutating ledger bytes."""
    stem = str(uuid.uuid4())
    source, output = tmp_path / (stem + '.spec.json'), tmp_path / (stem + '.plan.json')
    source.write_text(json.dumps(spec))
    fabric.cmd_lifecycle_plan(SimpleNamespace(engagement=engagement, spec=str(source), out=str(output)))
    return output, json.loads(output.read_text())


def empty_spec(**values):
    """Return complete explicit typed specification, including empty obligations."""
    return {'scope': 'default', 'reason': 'Synthetic exact update', 'proposed': [],
            'selections': [], 'verification': [], 'proofs': [], 'invalidations': [],
            'reinstatements': [], 'allowed_verification_path': 'synthetic-observation', **values}


def apply_receipt(tmp_path, request, receipt):
    """Invoke protected apply implementation with disposable real-signature data."""
    stem = str(uuid.uuid4())
    request_path, receipt_path = tmp_path / (stem + '.json'), tmp_path / (stem + '.receipt.json')
    request_path.write_text(json.dumps(request))
    receipt_path.write_text(json.dumps(receipt))
    return fabric.cmd_apply_operator(SimpleNamespace(request=str(request_path), receipt=str(receipt_path)))


def test_cli_fresh_initialization_scope_status_and_archive_only_refusal(tmp_path):
    environment = dict(os.environ, FABRIC_HOME=str(tmp_path))
    program = str(ROOT / '.ai/runtime/fabric/fabric.py')
    def invoke(*arguments):
        return subprocess.run([sys.executable, program, *arguments], env=environment,
                              text=True, capture_output=True, timeout=30)
    initialized = invoke('init', 'fresh', '--intent', 'Synthetic public specification', '--owner', 'Synthetic operator')
    assert initialized.returncode == 0, initialized.stderr
    ledger = tmp_path / 'fresh.jsonl'
    transactions = [json.loads(line) for line in ledger.read_text().splitlines()]
    assert len(transactions) == 1
    assert transactions[0]['format'] == 2
    assert any(operation['op'] == 'init' for operation in transactions[0]['operations'])
    status = invoke('lifecycle-status', 'fresh', '--scope', 'default')
    assert status.returncode == 0, status.stderr
    assert {item['logical_id'] for item in json.loads(status.stdout)} >= {'intent-0001', 'lifecycle-policy'}
    before = ledger.read_bytes()
    invalid = invoke('req', 'fresh', '--layer', '1', '--from', 'missing', '--label', 'derives', '--text', 'No orphan')
    assert invalid.returncode != 0
    assert ledger.read_bytes() == before
    (tmp_path / 'archive.jsonl').write_text(json.dumps({'op': 'node', 'data': {'id': 'old'}}) + '\n')
    rejected = invoke('verify', 'archive')
    assert rejected.returncode != 0
    assert 'archive' in rejected.stderr


def test_human_simulation_exact_acceptance_survives_unrelated_obsolete_locator_drift(tmp_path, monkeypatch):
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch, 'Synthetic qualified output')
    output = graph.nodes[fragment]['version_id']
    assert graph.lifecycle.evaluate(output, release=True)['eligible']
    obsolete = tmp_path / 'unrelated-obsolete.txt'
    obsolete.write_text('Unrelated historical observation')
    graph.add_node('evd', 1, 'Unrelated observation', confidence='observation', file=str(obsolete))
    obsolete.unlink()
    current = fabric.open_fabric(graph.eng)
    assert current.lifecycle.evaluate(output, release=True)['eligible']
    assert fabric.cmd_release(SimpleNamespace(engagement=graph.eng, fragment=fragment)) == 0
    assert fabric.cmd_lifecycle_status(SimpleNamespace(engagement=graph.eng, scope='default')) is None


def test_signed_blocked_update_cancels_complete_chain_without_reading_old_observation(tmp_path, monkeypatch):
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch, 'Synthetic accepted old output')
    lc, eng = fabric.lifecycle, graph.eng
    output = graph.nodes[fragment]['version_id']
    old_acceptance = graph.lifecycle.proofs[('default', output, 'accept')]
    old_permission = graph.lifecycle.proofs[('default', output, 'permission')]
    old_source = graph.lifecycle.selections[('default', 'fixture:source')]
    replacement = lc.manifest('fixture:source', 'source', {'fixture': 'changed-source'})
    unrelated = graph.add_node('req', 1, 'Unrelated retained branch')['version_id']
    Path(graph.lifecycle.locators[graph.nodes['evd-0001']['version_id']]).unlink()
    before = fabric.open_fabric(eng)
    assert not before.lifecycle.evaluate(output, release=True)['eligible']
    request = update(tmp_path, signer, eng, proposed=[{'manifest': replacement}],
                     selections=[{'logical_id': 'fixture:source', 'version_id': lc.version_id(replacement)}])
    current = fabric.open_fabric(eng)
    affected = request['parameters']['effects']['affected']
    assert {old_source, output, old_acceptance, old_permission} <= set(affected)
    assert unrelated not in affected
    assert current.lifecycle.states[output]['validity'] == 'invalid'
    assert current.lifecycle.states[old_acceptance]['validity'] == 'invalid'
    assert current.lifecycle.states[old_permission]['validity'] == 'invalid'
    assert current.lifecycle.states[lc.version_id(replacement)]['validity'] == 'pending'
    assert not current.lifecycle.evaluate(output, release=True)['eligible']

    bindings = copy.deepcopy(current.lifecycle.versions[output]['bindings'])
    bindings['source'] = {'refs': [lc.version_id(replacement)]}
    observed = tmp_path / 'fresh-observation.txt'
    observed.write_text('Synthetic newly observed verification bytes.\n')
    evidence = current.add_node('evd', 1, 'Fresh verification observation', confidence='observation',
                                file=str(observed), bindings=bindings)
    content = copy.deepcopy(current.lifecycle.versions[output]['content'])
    content['text'] = 'Fresh conclusion after governed source update'
    product = lc.manifest(fragment, 'frag', content, bindings,
                          [{'role': 'evidence', 'logical_id': evidence['id'], 'version_id': evidence['version_id']}])
    product_version = lc.version_id(product)
    update(tmp_path, signer, eng, proposed=[{'manifest': product}],
           selections=[{'logical_id': fragment, 'version_id': product_version}])
    reviews = [lc.manifest('fresh-review:' + identifier, 'rev', {'subject': identifier, 'state': 'accepts'})
               for identifier in (evidence['version_id'], product_version)]
    update(tmp_path, signer, eng, proposed=[{'manifest': value} for value in reviews],
           selections=[{'logical_id': value['logical_id'], 'version_id': lc.version_id(value)} for value in reviews])
    versions = [bound['refs'][0] for bound in bindings.values()]
    versions += [evidence['version_id'], product_version] + [lc.version_id(value) for value in reviews]
    update(tmp_path, signer, eng,
           verification=[{'version_id': identifier, 'evidence': [evidence['version_id']], 'path': 'synthetic-observation',
                          'changes': {'validity': 'valid', 'applicable': True, 'sufficient': True, 'reviewed': True}}
                         for identifier in versions],
           proofs=[{'subject': identifier, 'role': 'reviewer', 'proof': lc.version_id(review)}
                   for identifier, review in zip((evidence['version_id'], product_version), reviews)])
    fresh = fabric.open_fabric(eng)
    assert fresh.lifecycle.evaluate(product_version)['eligible']
    assert not fresh.lifecycle.evaluate(product_version, release=True)['eligible']
    assert fresh.lifecycle.states[old_acceptance]['validity'] == 'invalid'
    acceptance = tmp_path / 'fresh-human-acceptance.json'
    fabric.cmd_review(SimpleNamespace(engagement=eng, fragment=fragment, layer=0, state='accepts',
                                      rationale='Synthetic new acceptance, never inherited', reviewer='Synthetic human',
                                      model='human-fixture', constraints=None, request_out=str(acceptance)))
    signer.apply(fabric, acceptance)
    final = fabric.open_fabric(eng)
    assert final.lifecycle.evaluate(product_version, release=True)['eligible']
    assert final.lifecycle.states[old_acceptance]['validity'] == 'invalid'


def test_forgery_capability_effect_omission_policy_and_replay_refuse_with_unchanged_bytes(tmp_path, monkeypatch):
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch, 'Synthetic exact plan target')
    output = graph.nodes[fragment]['version_id']
    plan_path, request = pending_plan(tmp_path, graph.eng, empty_spec(invalidations=[output]))
    ledger = Path(fabric.log_path(graph.eng))
    original = ledger.read_bytes()
    receipt = signer.sign(request)
    forged = {**receipt, 'signature': 'AA=='}
    with pytest.raises(ValueError):
        apply_receipt(tmp_path, request, forged)
    assert ledger.read_bytes() == original
    signer.trust['capabilities'].remove('lifecycle-update')
    with pytest.raises(ValueError):
        apply_receipt(tmp_path, request, receipt)
    signer.trust['capabilities'].append('lifecycle-update')
    assert ledger.read_bytes() == original
    for change in ('effects', 'policy'):
        altered = copy.deepcopy(request)
        if change == 'effects':
            altered['parameters']['entries'] = []
            altered['parameters']['effects']['operations'] = []
        else:
            altered['parameters']['policy_digest'] = '0' * 64
        unsigned = {key: value for key, value in altered.items() if key != 'request_hash'}
        altered['request_hash'] = op.sha(op.canonical(unsigned))
        with pytest.raises(ValueError):
            apply_receipt(tmp_path, altered, signer.sign(altered))
        assert ledger.read_bytes() == original
    assert apply_receipt(tmp_path, request, receipt) == 0
    applied = ledger.read_bytes()
    with pytest.raises(ValueError):
        apply_receipt(tmp_path, request, receipt)
    assert ledger.read_bytes() == applied


def test_expired_and_concurrent_requests_cannot_commit(tmp_path, monkeypatch):
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch, 'Synthetic current output')
    output = graph.nodes[fragment]['version_id']
    path, request = pending_plan(tmp_path, graph.eng, empty_spec(invalidations=[output]))
    graph.add_node('req', 1, 'Concurrent ordinary authorized graph addition')
    ledger = Path(fabric.log_path(graph.eng))
    before = ledger.read_bytes()
    with pytest.raises(ValueError):
        apply_receipt(tmp_path, request, signer.sign(request))
    assert ledger.read_bytes() == before
    path, request = pending_plan(tmp_path, graph.eng, empty_spec(invalidations=[output]))
    expired = copy.deepcopy(request)
    expired['created_at'] -= 7200
    expired['expires_at'] -= 7200
    expired['request_hash'] = op.sha(op.canonical({key: value for key, value in expired.items() if key != 'request_hash'}))
    with pytest.raises(ValueError):
        apply_receipt(tmp_path, expired, signer.sign(expired))
    assert ledger.read_bytes() == before


def test_all_required_evidence_conjunctive_and_manifest_substitution_refused(tmp_path, monkeypatch):
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch, 'Synthetic complete output')
    output = graph.nodes[fragment]['version_id']
    good = graph.lifecycle.evaluate(output, release=True)
    assert good['eligible']
    extra = graph.add_node('evd', 1, 'Required evidence without governed category bindings', confidence='interpretation')
    graph.add_edge(extra['id'], 'supports', fragment)
    reopened = fabric.open_fabric(graph.eng)
    assert not reopened.justify(fragment, strict=True)[0]
    assert not reopened.lifecycle.evaluate(output, release=True)['eligible']
    assert any('required' in reason or 'governing' in reason for reason in reopened.lifecycle.evaluate(output)['reasons'])
    altered = copy.deepcopy(reopened.transactions[-1])
    altered['operations'][0]['data']['role'] = 'substituted'
    with pytest.raises(ValueError):
        fabric.lifecycle.replay(reopened.transactions[:-1] + [altered], graph.eng, fabric.verify_lifecycle_proof)


@pytest.mark.parametrize('state', ['insufficient', 'out_of_scope', 'resonates', 'correlates'])
def test_signed_nonaccepting_review_cannot_create_permission_or_release(state, tmp_path, monkeypatch):
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch,
        'Synthetic nonacceptance probe', acceptance_state=state)
    output = graph.nodes[fragment]['version_id']
    selected = graph.lifecycle.proofs[('default', output, 'accept')]
    assert graph.lifecycle.versions[selected]['content']['state'] == state
    assert ('default', output, 'permission') not in graph.lifecycle.proofs
    assert not graph.lifecycle.evaluate(output, release=True)['eligible']
    assert fabric.cmd_release(SimpleNamespace(engagement=graph.eng, fragment=fragment)) == 1


def test_nonzero_successful_failure_command_commits_attempt_conflict_and_escalation(tmp_path):
    environment = dict(os.environ, FABRIC_HOME=str(tmp_path))
    program = str(ROOT / '.ai/runtime/fabric/fabric.py')
    def invoke(*arguments):
        return subprocess.run([sys.executable, program, *arguments], env=environment,
                              text=True, capture_output=True, timeout=30)
    assert invoke('init', 'failure-case', '--intent', 'Synthetic failure transaction', '--owner', 'Synthetic').returncode == 0
    assert invoke('req', 'failure-case', '--layer', '1', '--from', 'intent-0001', '--label', 'derives', '--text', 'Requirement').returncode == 0
    arguments = ['contract', 'failure-case', '--from', 'req-0001']
    for field in fabric.CONTRACT_FIELDS:
        arguments.extend(['--' + field.replace('_', '-'), 'Synthetic ' + field])
    created = invoke(*arguments)
    assert created.returncode == 0, created.stderr
    ledger = tmp_path / 'failure-case.jsonl'
    before = ledger.read_bytes()
    failed = invoke('failure', 'failure-case', '--contract', 'ctr-0001', '--state', 'contradicted', '--reason', 'Synthetic observed contradiction')
    assert failed.returncode == 3, failed.stdout + failed.stderr
    assert ledger.read_bytes() != before
    transactions = [json.loads(line) for line in ledger.read_text().splitlines()]
    last_nodes = [operation['data']['type'] for operation in transactions[-1]['operations'] if operation['op'] == 'node']
    assert {'att', 'conf', 'esc'} <= set(last_nodes)
    status = invoke('status', 'failure-case')
    assert status.returncode == 0
    assert 'unresolved conflicts : 1' in status.stdout


def test_reference_acceptance_reads_exact_format2_receipt_and_refuses_revocation_or_mismatch(tmp_path, monkeypatch):
    """Exercise real synthetic L0 signatures; render observations are inert fixture data."""
    import visual_qa
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch, 'Synthetic reference acceptance')
    proof = graph.transactions[-1]['proof']
    accepted_request, accepted_receipt = tmp_path / 'reference-accepted.json', tmp_path / 'reference-accepted.receipt.json'
    accepted_request.write_text(json.dumps(proof['request']))
    accepted_receipt.write_text(json.dumps(proof['receipt']))
    declined_request = tmp_path / 'reference-declined.json'
    fabric.cmd_review(SimpleNamespace(engagement=graph.eng, fragment=fragment, layer=0, state='accepts',
                                      rationale='Synthetic independent refusal', reviewer='Synthetic human',
                                      model='human-fixture', constraints=None, request_out=str(declined_request)))
    declined_receipt = tmp_path / 'reference-declined.receipt.json'
    declined_receipt.write_text(json.dumps(signer.sign(json.loads(declined_request.read_text()), accepted=False)))
    renders = []
    for extension in ('.html', '.docx', '.pptx', '.xlsx'):
        source = tmp_path / ('synthetic-render-source' + extension)
        source.write_bytes(b'Synthetic nonexecuted renderer input')
        request = op.request('render', 'Synthetic format observation', source, str(tmp_path / 'render-outputs'), {'backend': 'libreoffice'})
        page = tmp_path / 'render-outputs' / request['request_id'] / 'page.png'
        page.parent.mkdir(parents=True)
        page.write_bytes(b'Synthetic nonexecuted page fixture')
        receipt = op.response(request, True, performed=True, outputs=[{'path': str(page), 'sha256': op.sha(page.read_bytes())}])
        receipt['tool_evidence'] = {'libreoffice_version': 'synthetic-renderer-observation'}
        reqpath, receiptpath = tmp_path / (extension[1:] + '.request.json'), tmp_path / (extension[1:] + '.receipt.json')
        reqpath.write_text(json.dumps(request))
        receiptpath.write_text(json.dumps(receipt))
        renders.append({'request': str(reqpath), 'receipt': str(receiptpath)})
    monkeypatch.setattr(visual_qa, 'image_findings', lambda path: [])
    manifest = {'l0': [{'request': str(accepted_request), 'receipt': str(accepted_receipt), 'accepted': True},
                       {'request': str(declined_request), 'receipt': str(declined_receipt), 'accepted': False}], 'render': renders}
    manifest_path = tmp_path / 'reference-manifest.json'
    manifest_path.write_text(json.dumps(manifest))
    assert op.check_acceptance(manifest_path)['state'] == 'PASS'
    wrong = copy.deepcopy(proof['receipt'])
    wrong['request_id'] = str(uuid.uuid4())
    accepted_receipt.write_text(json.dumps(wrong))
    with pytest.raises(ValueError):
        op.check_acceptance(manifest_path)
    accepted_receipt.write_text(json.dumps(proof['receipt']))
    update(tmp_path, signer, graph.eng, invalidations=[graph.nodes[fragment]['version_id']])
    with pytest.raises(ValueError):
        op.check_acceptance(manifest_path)


def test_direct_command_validation_is_atomic_and_unsigned_preflight_grants_nothing(tmp_path, monkeypatch):
    """Cover direct API boundaries separately from subprocess routing and signed tests."""
    monkeypatch.setattr(fabric, 'FABRIC_DIR', str(tmp_path))
    init = SimpleNamespace(engagement='direct-case', intent='Public synthetic intent',
                           owner='Synthetic owner', success='Explicit scoped evidence', boundary='Disposable only')
    fabric.cmd_init(init)
    ledger = Path(fabric.log_path(init.engagement))
    initialized = ledger.read_bytes()
    with pytest.raises(ValueError):
        fabric.cmd_init(init)
    assert ledger.read_bytes() == initialized
    boundary = SimpleNamespace(**{**vars(init), 'engagement': 'a' * 64})
    fabric.cmd_init(boundary)
    with pytest.raises(ValueError):
        fabric.cmd_init(SimpleNamespace(**{**vars(init), 'engagement': 'a' * 65}))

    req = SimpleNamespace(engagement=init.engagement, layer=1, text='Explicit requirement',
                          label='derives', **{'from': 'intent-0001'})
    fabric.cmd_req(req)
    required = ledger.read_bytes()
    for values in ({'from': 'missing'}, {'layer': 7}):
        with pytest.raises(ValueError):
            fabric.cmd_req(SimpleNamespace(**{**vars(req), **values}))
        assert ledger.read_bytes() == required

    contract_values = {field: 'Synthetic ' + field for field in fabric.CONTRACT_FIELDS}
    contract = SimpleNamespace(engagement=init.engagement, rework_of=None, change=None,
                               **{'from': 'req-0001'}, **contract_values)
    for values in ({'what': ''}, {'from': 'missing'}):
        with pytest.raises(ValueError):
            fabric.cmd_contract(SimpleNamespace(**{**vars(contract), **values}))
        assert ledger.read_bytes() == required
    fabric.cmd_contract(contract)
    graph = fabric.open_fabric(init.engagement)
    digest = fabric.contract_context_packet(graph, graph.nodes['ctr-0001'])[1]
    result_path = tmp_path / 'direct-layer-result.json'
    ingestion = SimpleNamespace(engagement=init.engagement, contract='ctr-0001', result=str(result_path))
    contracted = ledger.read_bytes()
    for result in ({'context_digest': digest},
                   {'context_digest': '0' * 64, 'fragments': [{'key': 'x', 'text': 'Wrong context'}]}):
        result_path.write_text(json.dumps(result))
        with pytest.raises(ValueError):
            fabric.cmd_ingest(ingestion)
        assert ledger.read_bytes() == contracted
    result_path.write_text(json.dumps({'context_digest': digest,
                                       'fragments': [{'key': 'x', 'text': 'Pending typed conclusion'}]}))
    fabric.cmd_ingest(ingestion)
    assert fabric.open_fabric(init.engagement).nodes['frag-0001']['text'] == 'Pending typed conclusion'

    lc = fabric.lifecycle
    proposal = lc.manifest('preflight-source', 'source', {'text': 'Maintained public specification'})
    plan_path, request = pending_plan(tmp_path, init.engagement,
        empty_spec(proposed=[{'manifest': proposal}],
                   selections=[{'logical_id': proposal['logical_id'], 'version_id': lc.version_id(proposal)}]))
    unsigned_bytes = ledger.read_bytes()
    assert fabric.validate_governed_request(request) is None
    assert ledger.read_bytes() == unsigned_bytes
    for change in ('omitted-effects', 'changed-policy'):
        altered = copy.deepcopy(request)
        if change == 'omitted-effects':
            altered['parameters']['entries'] = []
        else:
            altered['parameters']['policy_digest'] = '0' * 64
        altered['request_hash'] = op.sha(op.canonical({key: value for key, value in altered.items() if key != 'request_hash'}))
        with pytest.raises(ValueError):
            fabric.validate_governed_request(altered)
        assert ledger.read_bytes() == unsigned_bytes


def test_fresh_process_policy_evolution_replays_history_then_requires_fresh_justification(tmp_path):
    """Use copied runtime/policy bytes and real signatures in two fresh interpreters."""
    import shutil
    runtime = tmp_path / 'runtime'
    for relative in ('fabric/fabric.py', 'fabric/supervision-policy.json', 'tools/lifecycle.py',
                     'tools/operator_actions.py', 'tools/runtime_dependencies.py'):
        destination = runtime / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / '.ai/runtime' / relative, destination)
    storage = tmp_path / 'storage'
    storage.mkdir()
    script = tmp_path / 'policy-evolution.py'
    script.write_text('''import copy, importlib.util, json, sys
from pathlib import Path
from types import SimpleNamespace
import pytest
runtime, storage, tests, phase = map(Path, sys.argv[1:5])
sys.path.insert(0, str(runtime / 'tools'))
sys.path.insert(0, str(tests))
import operator_actions as op
from lifecycle_fixtures import accepted_graph, SyntheticOperator
spec = importlib.util.spec_from_file_location('isolated_policy_fabric', runtime / 'fabric/fabric.py')
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
lc = f.lifecycle
patch = pytest.MonkeyPatch()
if str(phase) == 'initial':
    graph, fragment, signer = accepted_graph(f, storage, patch, 'Synthetic policy A output')
    (storage / 'pin.json').write_text(json.dumps(signer.trust))
    output = graph.nodes[fragment]['version_id']
    pending = {'scope':'default','reason':'Synthetic stale pending request','proposed':[],
               'selections':[],'reinstatements':[],'verification':[],'proofs':[],
               'invalidations':[output],'allowed_verification_path':'synthetic-observation'}
    (storage / 'stale.spec.json').write_text(json.dumps(pending))
    f.cmd_lifecycle_plan(SimpleNamespace(engagement=graph.eng,spec=str(storage/'stale.spec.json'),out=str(storage/'stale.json')))
    assert graph.lifecycle.evaluate(output, release=True)['eligible']
    raise SystemExit(0)
trust = json.loads((storage / 'pin.json').read_text())
patch.setattr(op, 'trusted_key', lambda: trust)
patch.setattr(f, 'FABRIC_DIR', str(storage))
signer = object.__new__(SyntheticOperator)
signer.directory = storage; signer.private = storage/'synthetic-private.pem'; signer.trust = trust
assert not f._VERIFIED_PROOFS
graph = f.open_fabric('synthetic-content')
fragment = 'frag-0001'; old = graph.nodes[fragment]['version_id']
old_accept = graph.lifecycle.proofs[('default',old,'accept')]
assert not graph.lifecycle.evaluate(old, release=True)['eligible']
before = Path(f.log_path(graph.eng)).read_bytes()
try:
    signer.apply(f, storage/'stale.json')
except ValueError:
    pass
else:
    raise AssertionError('live stale-policy request accepted')
assert Path(f.log_path(graph.eng)).read_bytes() == before
counter = 0
def apply(proposed=(), verification=(), proofs=()):
    global counter
    counter += 1
    value = {'scope':'default','reason':'Synthetic policy B recovery','proposed':list(proposed),
             'selections':[{'logical_id':item['manifest']['logical_id'],'version_id':lc.version_id(item['manifest'])} for item in proposed],
             'reinstatements':[],'invalidations':[],'verification':list(verification),'proofs':list(proofs),
             'allowed_verification_path':'synthetic-observation'}
    spec_path = storage/('policy-'+str(counter)+'.spec.json')
    request_path = storage/('policy-'+str(counter)+'.json')
    spec_path.write_text(json.dumps(value))
    f.cmd_lifecycle_plan(SimpleNamespace(engagement=graph.eng,spec=str(spec_path),out=str(request_path)))
    signer.apply(f, request_path)
policy = lc.manifest('lifecycle-policy','policy',lc.policy())
apply(proposed=[{'manifest':policy}])
graph = f.open_fabric(graph.eng)
assert graph.lifecycle.states[old_accept]['validity'] == 'invalid'
old_bindings = graph.lifecycle.versions[old]['bindings']
bases = {}
for category, binding in old_bindings.items():
    previous = graph.lifecycle.versions[binding['refs'][0]]
    rebound_content = {**previous['content'], 'assessment_policy': lc.version_id(policy)}
    bases[category] = lc.manifest(previous['logical_id'], previous['kind'], rebound_content,
                                  previous['bindings'], previous['members'])
apply(proposed=[{'manifest':value} for value in bases.values()])
graph = f.open_fabric(graph.eng)
bindings = {category:{'refs':[lc.version_id(value)]} for category,value in bases.items()}
observation = storage/'policy-B-observation.txt'; observation.write_text('Fresh synthetic policy B observation')
evidence = graph.add_node('evd',1,'Fresh policy B verification',confidence='observation',file=str(observation),bindings=bindings)
content = copy.deepcopy(graph.lifecycle.versions[old]['content']); content['text'] = 'Fresh policy B conclusion'
product = lc.manifest(fragment,'frag',content,bindings,[{'role':'evidence','logical_id':evidence['id'],'version_id':evidence['version_id']}])
product_id = lc.version_id(product)
apply(proposed=[{'manifest':product}])
subjects = [evidence['version_id'],product_id]
reviews = [lc.manifest('policy-B-review:'+subject,'rev',{'subject':subject,'state':'accepts'}) for subject in subjects]
apply(proposed=[{'manifest':review} for review in reviews])
versions = [value['refs'][0] for value in bindings.values()] + [lc.version_id(policy)] + subjects + [lc.version_id(review) for review in reviews]
apply(verification=[{'version_id':identifier,'evidence':[evidence['version_id']],'path':'synthetic-observation',
                     'changes':{'validity':'valid','applicable':True,'sufficient':True,'reviewed':True}} for identifier in versions],
      proofs=[{'subject':subject,'role':'reviewer','proof':lc.version_id(review)} for subject,review in zip(subjects,reviews)])
graph = f.open_fabric(graph.eng)
fresh_gate = graph.lifecycle.evaluate(product_id)
assert fresh_gate['eligible'], fresh_gate
assert not graph.lifecycle.evaluate(product_id, release=True)['eligible']
acceptance = storage/'policy-B-acceptance.json'
f.cmd_review(SimpleNamespace(engagement=graph.eng,fragment=fragment,layer=0,state='accepts',
             rationale='Fresh synthetic policy B acceptance',reviewer='Synthetic human',model='human-fixture',
             constraints=None,request_out=str(acceptance)))
signer.apply(f, acceptance)
graph = f.open_fabric(graph.eng)
assert graph.lifecycle.evaluate(product_id, release=True)['eligible']
assert graph.lifecycle.states[old_accept]['validity'] == 'invalid'
''')
    def run(phase):
        return subprocess.run([sys.executable, str(script), str(runtime), str(storage), str(ROOT / 'tests'), phase],
                              text=True, capture_output=True, timeout=90)
    initial = run('initial')
    assert initial.returncode == 0, initial.stdout + initial.stderr
    policy_path = runtime / 'fabric/supervision-policy.json'
    changed = json.loads(policy_path.read_text())
    changed['synthetic_policy_revision'] = 2
    policy_path.write_text(json.dumps(changed))
    recovered = run('evolved')
    assert recovered.returncode == 0, recovered.stdout + recovered.stderr


def test_archived_assessment_replays_changed_budget_and_expired_exception_without_waiving_live_controls(tmp_path, monkeypatch):
    """Archive one signed assessment; later budgets and clocks govern only live decisions."""
    graph, fragment, signer = accepted_graph(fabric, tmp_path, monkeypatch,
        'Synthetic exception-bound output', acceptance_state=None)
    conflict = graph.add_node('conf', 1, 'Synthetic explicitly time-limited exception')
    graph.add_edge(fragment, 'may_create', conflict['id'])
    escalation = graph.add_node('esc', 1, 'Synthetic human exception required', code='outside_authority', effective='outside_authority')
    graph.add_edge(conflict['id'], 'escalates', escalation['id'])
    exception_request = tmp_path / 'exception-request.json'
    fabric.cmd_authorise(SimpleNamespace(engagement=graph.eng, escalation=escalation['id'],
        decision='exception', signer='Synthetic human', rationale='One-day synthetic exception',
        expires=1, adopt=None, revise_text=None, supersedes=None, beyond_round_limit=False,
        request_out=str(exception_request)))
    signer.apply(fabric, exception_request)
    acceptance = tmp_path / 'exception-acceptance.json'
    fabric.cmd_review(SimpleNamespace(engagement=graph.eng, fragment=fragment, layer=0, state='accepts',
        rationale='Synthetic acceptance within exception window', reviewer='Synthetic human',
        model='human-fixture', constraints=None, request_out=str(acceptance)))
    signer.apply(fabric, acceptance)
    graph = fabric.open_fabric(graph.eng)
    output = graph.nodes[fragment]['version_id']
    assert graph.lifecycle.evaluate(output, release=True)['eligible']
    ledger = Path(fabric.log_path(graph.eng))
    before = ledger.read_bytes()
    original_limit = fabric.MAX_STEPS
    monkeypatch.setattr(fabric, 'MAX_STEPS', 1)
    fabric._VERIFIED_PROOFS.clear()
    reopened = fabric.open_fabric(graph.eng)
    assert reopened.verify() == ([], [])
    with pytest.raises(ValueError):
        fabric.cmd_review(SimpleNamespace(engagement=graph.eng, fragment=fragment, layer=0, state='accepts',
            rationale='Must obey current spent budget', reviewer='Synthetic human', model='human-fixture',
            constraints=None, request_out=str(tmp_path / 'over-budget.json')))
    assert ledger.read_bytes() == before
    monkeypatch.setattr(fabric, 'MAX_STEPS', original_limit)
    future = fabric.time.time() + 2 * 86400
    monkeypatch.setattr(fabric.time, 'time', lambda: future)
    fabric._VERIFIED_PROOFS.clear()
    expired = fabric.open_fabric(graph.eng)
    assert expired.verify() == ([], [])
    assert not expired.lifecycle.evaluate(output, release=True)['eligible']
    fresh = fabric.lifecycle.manifest('after-expiry-source', 'source', {'text': 'Synthetic continuation input'})
    update(tmp_path, signer, graph.eng, proposed=[{'manifest': fresh}],
           selections=[{'logical_id': fresh['logical_id'], 'version_id': fabric.lifecycle.version_id(fresh)}])
    continued = fabric.open_fabric(graph.eng)
    assert continued.lifecycle.states[fabric.lifecycle.version_id(fresh)]['validity'] == 'pending'
    assert not continued.lifecycle.evaluate(output, release=True)['eligible']
