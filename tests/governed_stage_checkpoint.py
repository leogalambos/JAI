#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Resume one disposable test stage; this is not a production recovery command.

Usage: python3 tests/governed_stage_checkpoint.py /tmp/.../stage-checkpoint.json
The scratch descriptor contains no saved State or internal signing credential.
Optional human public enrollment only preserves real L0 grant checks in a fixture.
A resumed stage is not full-workflow proof.
"""
import argparse
import copy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import tempfile

from governed_fixtures import lc, op
import governed_workflow


_PURPOSES = ('delivery-change', 'delivery-accept', 'delivery-release')
_FIELDS = {'protocol', 'stage', 'journal', 'engagement', 'prefix_length',
           'prefix_sha256', 'assignment', 'governing_uses', 'refs',
           'human_enrollment', 'host_config'}


def _scratch(path):
    value = Path(path).absolute()
    if not value.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise ValueError('Disposable stage checkpoints and keys must remain in scratch storage')
    return value


def save_checkpoint(path, host, workflow, assignment, *, stage, refs=None):
    """Save a single next-step diagnostic cursor beside a genuine test history.

    Args:
        path: Explicit scratch JSON destination, never a public evidence output.
        host: Existing GovernedHarness; no new keys or authority are created.
        workflow: Existing host Workflow whose actual configuration is captured.
        assignment: Exact assignment that the next selection/work pair will run.
        stage: Human-readable diagnostic stage name, not an authorization claim.
        refs: Optional related immutable references for diagnosing the same stage.
    Returns:
        Path of the written scratch descriptor.
    Raises:
        ValueError, OSError: The fixture or scratch paths are unsupported.
        ProtocolError: Exact stage identity or current history cannot be resolved.
    """
    destination = _scratch(path)
    journal = _scratch(host.store.path)
    state = host.store.read()
    record = state.resolve(assignment, 'assignment')
    raw = op.journal_snapshot(journal)
    if state.head != (json.loads(raw.splitlines()[-1])['hash'] if raw else lc.ZERO):
        raise ValueError('Test history changed while capturing the diagnostic stage')
    descriptor = {'protocol': 'jai.disposable-stage-checkpoint/2', 'stage': stage,
        'journal': str(journal), 'engagement': host.store.engagement,
        'prefix_length': len(raw), 'prefix_sha256': hashlib.sha256(raw).hexdigest(),
        'assignment': copy.deepcopy(assignment),
        'governing_uses': state._dependencies(record), 'refs': copy.deepcopy(refs or {}),
        'human_enrollment': ({purpose: host._human_signer.trusted_keys(purpose) for purpose in _PURPOSES}
                             if host._human_signer is not None else None),
        'host_config': copy.deepcopy(workflow.dispatcher.config)}
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(op.canonical(descriptor))
    return destination


@contextmanager
def _test_enrollment(enrollment):
    if enrollment is None:
        yield
        return
    previous = op.trusted_keys

    def fixture_keys(purpose=None):
        if purpose not in enrollment:
            raise ValueError('Only the captured disposable proof purposes are available')
        return copy.deepcopy(enrollment[purpose])

    # Only actual human grants consult these captured public fixture keys.
    # Ordinary runtime recording and reads never acquire a keyring dependency.
    op.trusted_keys = fixture_keys
    try:
        yield
    finally:
        op.trusted_keys = previous


def _check_workers(config):
    workers = list(config['workers']) + [tool['worker'] for tool in config['tools']]
    for worker in workers:
        for asset in worker['files']:
            if hashlib.sha256(op.regular(Path(asset['path']))).hexdigest() != asset['sha256']:
                raise ValueError('A governed worker changed; this stage needs a fresh fixture')


def _completed_since(state, transactions, assignment):
    for transaction in transactions:
        message = transaction['operations'][0]['data']['message']
        payload = message['payload']
        if message['message_type'] != 'control_event' or payload.get('event') != 'run_completed':
            continue
        context = state.resolve(payload['run_context'], 'context')
        if context['assignment'] != assignment or context['execution']['phase'] != 'work':
            continue
        if any(effect.get('op') == 'run' and effect.get('run_id') == context['run_id']
               and effect.get('state') == 'returned'
               for effect in transaction['operations'][0]['data']['effects']):
            return True
    return False


def resume_checkpoint(path):
    """Cold-audit a disposable history, then execute its one unfinished stage.

    Args:
        path: Explicit scratch descriptor written by save_checkpoint.
    Returns:
        Actual captured completion, labeled resumed-stage-only with before/after heads.
    Raises:
        ValueError, OSError: Prefix, worker or required human public enrollment is unavailable.
        ProtocolError, DispatchError: Stage was completed, is no longer current, or execution fails.
    """
    descriptor = json.loads(op.regular(_scratch(path)))
    if set(descriptor) != _FIELDS or descriptor['protocol'] != 'jai.disposable-stage-checkpoint/2':
        raise ValueError('Closed disposable stage checkpoint required')
    journal = _scratch(descriptor['journal'])
    enrollment = descriptor['human_enrollment']
    if enrollment is not None and set(enrollment) != set(_PURPOSES):
        raise ValueError('Only captured human proof purposes are permitted')
    raw = op.journal_snapshot(journal)
    size = descriptor['prefix_length']
    if (type(size) is not int or size <= 0 or len(raw) < size
            or hashlib.sha256(raw[:size]).hexdigest() != descriptor['prefix_sha256']):
        raise ValueError('The authentic checkpoint prefix was changed or truncated')
    _check_workers(descriptor['host_config'])
    prefix_count = len(lc._parse_transactions(raw[:size]))
    with _test_enrollment(enrollment):
        store = lc.Store(journal, descriptor['engagement'])
        state = store.read()
        assignment = descriptor['assignment']
        body = state.resolve(assignment, 'assignment')
        if _completed_since(state, state.transactions[prefix_count:], assignment):
            raise lc.ERROR('P_IDEMPOTENCY', 'This exact diagnostic stage already completed')
        if state.assignment_states.get(assignment['version_id']) != 'open':
            raise lc.ERROR('P_STATE', 'The saved logical assignment is no longer open')
        if state._dependencies(body) != descriptor['governing_uses']:
            raise lc.ERROR('P_CONTEXT', 'The governing stage input identities changed')
        state._assignment_requirements(body, live=True)
        for reference in lc._references(descriptor['refs']):
            state.resolve(reference)
        before_head = state.head
        workflow = governed_workflow.Workflow(store, descriptor['host_config'])
        chosen = workflow.run(assignment, 'selection')
        selected = store.read()
        choice = next(reference for reference in chosen['completion']['receipt']['created_versions']
                      if selected.versions[reference['version_id']]['kind'] == 'delivery.decision')
        completed = workflow.run(assignment, 'work', selection=choice)
        after = store.read()
        if not _completed_since(after, after.transactions[len(state.transactions):], assignment):
            raise lc.ERROR('P_STATE', 'The resumed stage did not produce an accepted work return')
        return {'qualification': 'resumed-stage-only', 'stage': descriptor['stage'],
                'before_head': before_head, 'after_head': after.head,
                'verified_prefix_transactions': len(state.transactions),
                'new_transactions': len(after.transactions) - len(state.transactions),
                'result': completed}


def main(argv=None):
    """Run an explicitly named scratch checkpoint; exit nonzero on any refusal."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    arguments = parser.parse_args(argv)
    print(json.dumps(resume_checkpoint(arguments.checkpoint)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
