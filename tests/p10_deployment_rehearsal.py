#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Rehearse current G09 installation in a new disposable scratch directory.

Usage: python tests/p10_deployment_rehearsal.py --workspace /tmp/jai-g09-unique
Requires the declared runtime validator. No provider client, professional LLM,
private key, active installation or historical compatibility reader is used.
The filename is retained; historical P10 requires its historical checkout.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def _run(command, environment, destination, expected=0, stdin=None):
    started = time.monotonic()
    result = subprocess.run(command, env=environment, input=stdin, capture_output=True, text=True)
    destination.write_text(result.stdout + result.stderr)
    if stdin is not None:
        _carrier_frames(result.stdout)
    if result.returncode != expected:
        raise RuntimeError(f'Command returned {result.returncode}, expected {expected}; see {destination}')
    return {'argv': command, 'seconds': time.monotonic() - started,
            'returncode': result.returncode, 'log': str(destination)}


def _carrier_frames(text):
    frames = [json.loads(line) for line in text.splitlines() if line.strip()]
    if not frames or any(not isinstance(frame, dict) or frame.get('ok') is not True for frame in frames):
        raise RuntimeError('Installed carrier returned a failed protocol frame')
    if not any(frame.get('id') == 'deployment-close' and frame.get('result') == {'closed': True}
               for frame in frames):
        raise RuntimeError('Installed carrier did not acknowledge the exact close request')
    return frames


def _prepared_view(value):
    # Only these optional duplicate presentation fields differ between initial
    # and restored prepare responses; exact packets and all other fields remain.
    return {**value, 'members': [{key: item for key, item in member.items()
                                  if key not in {'manifest_hash', 'packet_blob_id'}}
                                 for member in value['members']]}


def _hashes(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob('*')) if path.is_file() and '__pycache__' not in path.parts}


def _origins(house):
    result = {}
    for name, module in tuple(sys.modules.items()):
        location = getattr(module, '__file__', None)
        if not location:
            continue
        path = Path(location).resolve()
        if any(path.is_relative_to(ROOT / '.ai' / section) for section in ('runtime', 'setup')):
            raise RuntimeError(f'Checkout production module contaminated installed qualification: {name}: {path}')
        if path.is_relative_to(house):
            result[name] = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    return result


def _installed_smoke(workspace, house):
    sys.path.insert(0, str(house / 'tools'))
    lc = importlib.import_module('lifecycle')
    layered = importlib.import_module('governed_layered')
    dependency = importlib.import_module('runtime_dependencies').jsonschema_status()
    if dependency['status'] != 'ready':
        raise RuntimeError(f'Declared runtime prerequisite not ready: {dependency}')
    _origins(house)
    environment = dict(os.environ)
    task, criteria = workspace / 'task.txt', workspace / 'criteria.txt'
    task.write_text('Design the boundary of a fictional backup service. No deployed facts are asserted.\n')
    criteria.write_text('Identify service information and uncertainty without personal data.\n')
    cli = [sys.executable, str(house / 'tools/governed_layered.py')]
    commands = [_run(cli + ['start', '--home', str(workspace / 'engagement'), '--engagement', 'g09-installed',
        '--task', str(task), '--criteria', str(criteria), '--provider', 'codex', '--work-item', 'backup'],
        environment, workspace / 'start.log', stdin='{"id":"deployment-close","operation":"close"}\n')]
    startup = json.loads((workspace / 'start.log').read_text().splitlines()[0])['result']
    locator = startup['created']['locator']
    session = layered.LayeredSession.open(locator)
    prepared = startup['next']['prepared']
    invocation = startup['next']['invocation_id']
    before = session.store.path.read_bytes()
    pinned_id = session.store.read().invocations[invocation]['manifest_blob_id']
    pinned_bytes = session.store._blob(pinned_id)
    commands.append(_run(cli + ['resume', '--session', locator], environment,
                         workspace / 'resume.log', stdin='{"id":"deployment-close","operation":"close"}\n'))
    resumed = layered.LayeredSession.open(locator)
    assert resumed.store.path.read_bytes() == before
    restored = resumed.prepare(invocation)
    assert _prepared_view(restored) == _prepared_view(prepared)
    assert resumed.store.read().invocations[invocation]['manifest_blob_id'] == pinned_id
    assert resumed.store._blob(pinned_id) == pinned_bytes
    pinned = lc.loads(pinned_bytes)
    for member in restored['members']:
        exact = next(item for item in pinned['members'] if item['member_key'] == member['member_key'])
        assert lc.canonical(member['packet']) == resumed.store._blob(exact['packet_blob_id'])
        assert member['packet']['manifest_hash'] == exact['manifest_hash']
    session = resumed
    completed = []

    def finish(assignment, phase, result=None, existing=None):
        state = session.store.read()
        job = {'assignment': assignment, 'phase': phase}
        if phase == 'work':
            job['selection'] = state.execution_plans[(assignment['version_id'], 'default')]
        issued = session.issue_batch([job]) if existing is None else existing
        physical = issued['invocation_id']
        delivery = session.prepare(physical)
        packet = delivery['members'][0]['packet']
        if phase == 'selection':
            model = next(item for item in packet['execution']['availability']
                         if item['provider'] == 'codex' and item['workload_class'] == 'standard')
            value = {'member': packet['member_key'], 'kind': 'selection', 'specialties': ['software-engineer'],
                'provider': 'codex', 'workload_class': 'standard', 'model_selector': model['model_selector'],
                'reason': 'Deterministic installation fixture, not a live professional choice.'}
        else:
            value = dict(result, member=packet['member_key'])
        session.start(physical, 'codex', physical, {'observed': 'Synthetic installed-runtime dispatch; no model called.'})
        response = session.complete(physical, json.dumps({'format': 'jai.semantic-return/1', 'results': [value]}),
                                    {'observed': 'Deterministic professional-return fixture only.'})
        assert response['status'] == 'returned', response
        current = session.store.read()
        assert current.run_states[packet['run_id']] == 'returned'
        completed.append(physical)
        return response

    root = startup['created']['entry']['assignment']
    finish(root, 'selection', existing=startup['next'])
    state = session.store.read()
    root_body = state.resolve(root, 'assignment')
    requirement = startup['created']['inputs']['request']
    root_result = {'kind': 'setter', 'logical_id': 'installed-layer-criteria',
        'materials': [{'text': 'Synthetic local layer framing.'}],
        'criteria': [{'id': 'boundary', 'requirement': requirement,
            'statement': 'Describe the fictional backup boundary.', 'evidence_slots': []}],
        'inherited': root_body['inherited'], 'procedure': {'kind': 'layer',
            'reason': 'Synthetic ordinary owner procedure for deployment qualification.',
            'specification': {'framing': 'Refine the backup boundary.',
                'question_tasks': {question: 'Resolve ' + question + ' in this layer.'
                                   for question in ('what', 'why', 'how', 'who', 'where', 'when')},
                'integration_task': 'Integrate all six actual answers.',
                'review_task': 'Independently review the integration.', 'interface_criterion': 'boundary'}}}
    finish(root, 'work', root_result)
    state = session.store.read()
    root_procedure = state.procedures[(root['version_id'], 'default')]
    first = session.workflow.advance(root_procedure)
    state = session.store.read()
    question = next(ref for ref in first['completion']['receipt']['created_versions']
                    if state.versions[ref['version_id']]['kind'] == 'delivery.assignment')
    assert state.resolve(question, 'assignment')['owner']['question'] == 'what'
    question_body = state.resolve(question, 'assignment')
    inherited = list(question_body['inherited'])
    if question_body['criteria'] not in inherited:
        inherited.append(question_body['criteria'])

    def question_result(revision):
        return {'kind': 'setter', 'logical_id': 'installed-question-criteria-' + revision,
            'materials': [{'text': 'Synthetic ' + revision + ' local information requirement.'}],
            'criteria': [{'id': 'information', 'requirement': question_body['criteria'],
                'statement': 'Identify backup service information and ' + revision + ' uncertainty.', 'evidence_slots': []}],
            'inherited': inherited, 'procedure': {'kind': 'question',
                'reason': 'Actual fixture owner replaces its own derived local requirement.',
                'specification': {'question': 'What backup information is needed?',
                    'author_task': 'Describe backup information under the ' + revision + ' criterion.',
                    'reviewer_task': 'Independently inspect the exact answer under that criterion.'}}}

    def triad(revision):
        state = session.store.read()
        procedure = state.procedures[(question['version_id'], 'default')]
        for responsibility in ('author', 'reviewer'):
            step = state.procedure_next(procedure)
            assert step['step'] == responsibility, step
            receipt = session.workflow.advance(procedure)
            state = session.store.read()
            assignment = next(ref for ref in receipt['completion']['receipt']['created_versions']
                              if state.versions[ref['version_id']]['kind'] == 'delivery.assignment')
            finish(assignment, 'selection')
            value = ({'kind': 'author', 'logical_id': 'installed-answer-' + revision,
                'materials': [{'text': 'Synthetic backup information; ' + revision + ' uncertainties explicitly retained.'}],
                'evidence': [], 'limitations': ['Deterministic deployment fixture, not professional content qualification.']}
                if responsibility == 'author' else
                {'kind': 'reviewer', 'logical_id': 'installed-review-' + revision, 'verdict': 'supported',
                 'rationale': 'Synthetic independent-role response; no live professional judgment claimed.',
                 'findings': [], 'conditions': []})
            finish(assignment, 'work', value)
            state = session.store.read()
        for _ in range(3):
            step = state.procedure_next(procedure)
            if step.get('complete'):
                break
            assert step['step'].startswith('select:'), step
            session.workflow.advance(procedure)
            state = session.store.read()
        assert state.procedure_next(procedure).get('complete')
        answer = next(state._reference(identifier) for identifier, value in state.versions.items()
            if value['kind'] == 'delivery.product' and value['content']['record']['product_kind'] == 'answer'
            and value['logical_id'] == 'installed-answer-' + revision)
        assert state.evaluate(answer)['qualified']
        return answer

    finish(question, 'selection')
    finish(question, 'work', question_result('A'))
    old = triad('A')
    old_state = session.store.read()
    old_procedure = old_state.procedures[(question['version_id'], 'default')]
    old_proof = next(value for value in old_state.proofs.values() if value['subject'] == old)
    finish(question, 'work', question_result('B'))
    changed = session.store.read()
    assert changed.procedures[(question['version_id'], 'default')] != old_procedure
    assert not changed.evaluate(old)['qualified']
    assert changed._status(old_proof['proof'], old_proof['proof_use_scope'])['validity'] == 'invalid'
    assert changed.procedure_next(changed.procedures[(question['version_id'], 'default')])['step'] == 'author'
    assert not any(changed._governing_input(changed._point(changed._reference(identifier)), live=False)
        for identifier, value in changed.versions.items() if value['kind'] == 'delivery.product'
        and value['content']['record']['product_kind'] == 'answer'
        and value['logical_id'] == 'installed-answer-B')
    new = triad('B')
    state = session.store.read()
    assert new != old and not state.evaluate(old)['qualified']
    assessed = state.evaluate(new)
    assert assessed['qualified'] and not assessed['accepted'] and not assessed['release_eligible']
    # No other question was delegated or executed merely to qualify deployment.
    question_setters = [value['content']['record'] for value in state.versions.values()
        if value['kind'] == 'delivery.assignment' and value['content']['record']['responsibility'] == 'setter'
        and value['content']['record']['owner']['work_kind'] == 'question']
    assert len(question_setters) == 1
    cold = layered.LayeredSession.open(locator)
    assert cold.store.read().head == state.head
    assert cold.store.read().evaluate(new) == assessed
    commands.append(_run(cli + ['resume', '--session', locator], environment,
                         workspace / 'final-status.log', stdin='{"id":"deployment-close","operation":"close"}\n'))
    return {'runtime_modules': _origins(house), 'runtime_dependency': dependency,
        'locator': locator, 'journal': str(session.store.path), 'head': state.head,
        'resumed_prepared_invocation': invocation, 'completed_invocations': completed,
        'old_answer': old, 'current_answer': new, 'current_assessment': assessed,
        'commands': commands, 'external_llm': False, 'production_acceptance': False}


def main(argv=None):
    """Install and qualify current code in a fresh disposable scratch tree.

    Args:
        argv: Optional CLI arguments; workspace must be a new /tmp descendant.
    Returns:
        Zero after actual checks pass, with manifests and evidence beneath workspace.
    Raises:
        ValueError, OSError, RuntimeError: Unsafe destination, installation conflict,
            unavailable prerequisites, origin contamination or failed runtime assertions.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=Path)
    parser.add_argument('--installed-house', type=Path, help=argparse.SUPPRESS)
    arguments = parser.parse_args(argv)
    workspace = arguments.workspace.resolve()
    if not workspace.is_relative_to(Path(tempfile.gettempdir()).resolve()) or workspace == Path(tempfile.gettempdir()).resolve():
        raise ValueError('A disposable directory beneath system scratch is required')
    if arguments.installed_house:
        if arguments.installed_house.resolve() != workspace / 'ai/it-role-house':
            raise ValueError('The smoke child must use this disposable installation')
        result = _installed_smoke(workspace, arguments.installed_house.resolve())
        (workspace / 'smoke-evidence.json').write_text(json.dumps(result, indent=2) + '\n')
        return 0
    workspace.mkdir(exist_ok=False)
    house, claude, codex = workspace / 'ai/it-role-house', workspace / 'claude', workspace / 'codex'
    environment = dict(os.environ, AI_IT_HOME=str(workspace / 'ai'), AI_IT_HOUSE=str(house),
                       CLAUDE_HOME=str(claude), CODEX_HOME=str(codex))
    # These are supported installer destinations in this child environment only;
    # parent HOME/CODEX_HOME and the active installation are never changed.
    installer = [sys.executable, str(ROOT / '.ai/setup/installer.py'), '--no-claude-md', '--no-codex-agents']
    house.mkdir(parents=True)
    trust = house / 'trust/jai-operator-trust.json'
    trust.parent.mkdir()
    trust.write_text('{"qualification":"unmanaged-public-trust-sentinel","private_key":false}\n')
    claude.mkdir()
    settings = claude / 'settings.json'
    settings.write_text('{"qualification_unrelated":"preserve-me"}\n')
    trust_bytes = trust.read_bytes()
    operations = [_run(installer + ['--dry-run'], environment, workspace / 'install-dry-run.log'),
                  _run(installer, environment, workspace / 'install.log')]
    assert trust.read_bytes() == trust_bytes
    assert json.loads(settings.read_text())['qualification_unrelated'] == 'preserve-me'
    spec = importlib.util.spec_from_file_location('deployment_installer', ROOT / '.ai/setup/installer.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry, _ = module.load_model_registry(ROOT, None)
    desired, modes = module.desired_outputs(ROOT, {'claude', 'codex'}, house, claude, codex, registry)
    expected = {path: {'sha256': hashlib.sha256(raw).hexdigest(), 'mode': modes[path]} for path, raw in desired.items()}
    for path, metadata in expected.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == metadata['sha256'], path
        assert Path(path).stat().st_mode & 0o777 == metadata['mode'], path
    catalogue = json.loads((house / 'roles.json').read_text())
    assert catalogue['count'] == len(catalogue['roles']) == 286
    assert len(list((house / 'commands').glob('*.md'))) == 17
    assert len(list((claude / 'commands').glob('*.md'))) == 17
    assert len(list((codex / 'skills').glob('workflow-*/SKILL.md'))) == 17
    for row in catalogue['roles']:
        assert (house / 'skills' / row['skill'] / 'references' / (row['slug'] + '.md')).is_file()
        assert (codex / 'skills' / row['skill'] / 'references' / (row['slug'] + '.md')).is_file()
    manifest = {'source_revision': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        'delivery_delta': subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).splitlines(),
        'expected_installed_files': expected, 'role_count': 286, 'command_count': 17,
        'providers': ['claude', 'codex']}
    (workspace / 'artifact-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    operations.append(_run([sys.executable, str(Path(__file__).resolve()), '--workspace', str(workspace),
                           '--installed-house', str(house)], environment, workspace / 'smoke.log'))
    smoke = json.loads((workspace / 'smoke-evidence.json').read_text())
    journal = Path(smoke['journal'])
    journal_bytes = journal.read_bytes()
    software = {path: Path(path).read_bytes() for path in desired}
    recovery = workspace / 'reviewed-software-backup'
    for path in software:
        target = recovery / Path(path).relative_to(workspace)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    configuration = settings.read_bytes()
    (recovery / 'claude-settings.json').write_bytes(configuration)
    engagement_hashes = _hashes(journal.parent)
    guide = house / 'GUIDE.md'
    modified = b'Disposable managed-conflict probe.\n'
    guide.write_bytes(modified)
    before_conflict = _hashes(workspace)
    operations.append(_run(installer, environment, workspace / 'conflict.log', expected=2))
    after_conflict = _hashes(workspace)
    after_conflict.pop('conflict.log', None)
    assert after_conflict == before_conflict
    operations.append(_run(installer + ['--force'], environment, workspace / 'forced-replacement.log'))
    install_state = json.loads((house / 'install-state.json').read_text())
    backup = Path(install_state['backup_last'])
    backed_guide = backup / str(guide).lstrip(os.sep)
    assert backed_guide.read_bytes() == modified
    assert guide.read_bytes() == software[str(guide)]
    for path in software:
        shutil.copy2(recovery / Path(path).relative_to(workspace), path)
    shutil.copy2(recovery / 'claude-settings.json', settings)
    assert all(Path(path).read_bytes() == raw for path, raw in software.items())
    assert settings.read_bytes() == configuration and trust.read_bytes() == trust_bytes
    assert journal.read_bytes() == journal_bytes
    assert _hashes(journal.parent) == engagement_hashes
    result = {'status': 'PASS', 'package_revision': manifest['source_revision'],
        'artifact_manifest': str(workspace / 'artifact-manifest.json'), 'operations': operations,
        'managed_conflict': 'exit2-without-target-writes', 'installer_backup': str(backup),
        'software_configuration_restoration': 'exact-bytes-current-reader-only',
        'reviewed_software_backup': str(recovery),
        'journal_tail_preserved': True, 'external_llm': False, 'active_installation_changed': False,
        'scope': 'Disposable installed format9 native flow and recovery; no host activation, human acceptance or release.'}
    (workspace / 'evidence.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
