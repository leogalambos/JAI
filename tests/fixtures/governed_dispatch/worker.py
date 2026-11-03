# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Disposable JSON-process worker exercising the real confined broker."""
import base64
import hashlib
import json
import os
from pathlib import Path
import socket
import signal
import subprocess
import sys


_sequence = 0


def _request(operation, **values):
    global _sequence
    _sequence += 1
    print(json.dumps({'id': operation + '-' + str(_sequence), 'operation': operation, **values}), flush=True)
    return json.loads(sys.stdin.readline())


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def _denied(action):
    try:
        action()
    except OSError:
        return True
    return False


packet = json.loads(sys.stdin.readline())
mode = sys.argv[1]
if mode == 'measure':
    print(json.dumps({'measured_targets': packet.get('targets', []), 'result': 'executed'}))
    raise SystemExit(0)
if mode == 'sleep':
    # A real blocked process is required to test host process-tree termination.
    signal.pause()
if mode == 'overflow':
    print('x' * 200000, flush=True)
    raise SystemExit(0)
settings = json.loads(Path('/worker/settings.json').read_text())
assignment = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['assignment'])
context = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['context'])
# Report visibility by exact reference without recursively copying prior reports.
report = {'scratch_write': False, 'manifest': [{'ref': item['ref']} for item in packet['manifest']], 'attachments': []}
catalogue = json.loads(Path('/catalogue/catalogue.json').read_text())
report['catalogue_count'] = catalogue['count']
report['unselected_instruction_readable'] = bool(Path('/catalogue/instructions/internal-it-auditor.md').read_text())
report['catalogue_readonly'] = _denied(lambda: Path('/catalogue/catalogue.json').write_text('altered'))
report['protected_task_denied'] = _denied(lambda: Path(settings['protected_file']).read_bytes())
report['selected_specialties'] = packet['execution']['specialties']
report['selected_instruction_slugs'] = [item['slug'] for item in packet['execution']['instructions']]
Path('/scratch/worker-created.txt').write_text('private scratch bytes')
report['scratch_write'] = Path('/scratch/worker-created.txt').read_text() == 'private scratch bytes'
for attachment in packet['attachments']:
    reply = _request('read', handle=attachment['handle'])
    report['attachments'].append({'blob_id': attachment['blob_id'], 'reply': reply})
if mode == 'attack':
    target = settings['protected_file']
    allowed_shell = subprocess.run(['/bin/sh', '-c', 'printf allowed > /scratch/shell-output'],
                                   capture_output=True)
    report['allowed_shell_scratch'] = (allowed_shell.returncode == 0 and
                                       Path('/scratch/shell-output').read_text() == 'allowed')
    report['denials'] = {
        'read': _denied(lambda: Path(target).read_bytes()),
        'edit': _denied(lambda: Path(target).write_text('changed')),
        'delete': _denied(lambda: Path(target).unlink()),
        'rename': _denied(lambda: Path(target).rename(target + '.renamed')),
        'replace': _denied(lambda: os.replace('/scratch/worker-created.txt', target)),
        'socket': _denied(lambda: socket.socket()),
        'socketpair': _denied(lambda: socket.socketpair()),
    }
    for name, command in {
        'shell_read': ['/bin/sh', '-c', 'cat "$1"', 'probe', target],
        'shell_edit': ['/bin/sh', '-c', 'printf changed > "$1"', 'probe', target],
        'child_socket': ['/usr/bin/python3', '-c', 'import socket; socket.socket()'],
    }.items():
        report['denials'][name] = subprocess.run(command, capture_output=True).returncode != 0
    report['environment_secret_absent'] = 'JAI_TEST_SECRET' not in os.environ
    report['inherited_fd_closed'] = _denied(lambda: os.fstat(settings['inherited_fd']))
    report['host_secret_absent'] = _denied(lambda: Path(settings['host_secret']).read_bytes())
    report['ledger_absent'] = _denied(lambda: Path(settings['ledger']).read_bytes())
    report['controller_absent'] = _denied(lambda: Path(settings['controller']).read_bytes())
    report['unknown_read'] = _request('read', handle='ungranted-handle')
    report['foreign_materialize'] = _request('materialize', subject=settings['subject'],
                                             blob_id='0' * 64, destination_handle='foreign')
if settings.get('measure'):
    report['measurement'] = _request('measure', tool_policy=settings['tool_policy'], targets=[settings['subject']])
data = _canonical(report)
proposed = _request('propose', data=base64.b64encode(data).decode())
blob_id = proposed['result']['blob_id']
if mode == 'information':
    print(json.dumps({'id': 'return', 'operation': 'return', 'value': {
        'assignment': packet['assignment'], 'context': packet['context'], 'records': [],
        'intents': [{'message_type': 'information_request',
                    'recipient': ({'kind': 'assignment', 'ref': assignment['issued_under']}
                                  if assignment['issued_under'] is not None else
                                  {'kind': 'controller', 'id': 'trusted-controller'}),
                    'payload': {'assignment': packet['assignment'], 'needed': [],
                                'question': 'Provide the missing operational constraint.',
                                'blocked_obligations': [assignment['criteria']]}}]}}), flush=True)
    raise SystemExit(0)
if settings.get('materialize'):
    report_copy = _request('materialize', subject=settings['subject'], blob_id=blob_id,
                           destination_handle='owned-output')
    if not report_copy['ok']:
        raise RuntimeError(report_copy)
product = {'owner': assignment['owner'], 'product_kind': 'answer',
           'assignment': packet['assignment'], 'profile': assignment['profile'],
           'inputs': assignment['inputs'], 'material': [blob_id], 'evidence': [],
           'related': [], 'limitations': []}
logical_id = 'worker-generated-answer'
manifest = {'schema': 'jai.lifecycle.manifest/2', 'logical_id': logical_id,
            'kind': 'delivery.product', 'content': {'engagement': packet['assignment']['engagement'],
            'scope': packet['assignment']['scope'], 'record': product}, 'bindings': {}, 'members': []}
reference = {**packet['assignment'], 'logical_id': logical_id,
             'version_id': hashlib.sha256(b'jai.lifecycle.version.v2\0' + _canonical(manifest)).hexdigest()}
returned = {'assignment': packet['assignment'], 'context': packet['context'],
            'records': [{'logical_id': logical_id, 'record_type': 'product', 'record': product}],
            'intents': [{'message_type': 'submission', 'recipient': {'kind': 'controller', 'id': 'trusted-controller'},
                         'payload': {'assignment': packet['assignment'], 'candidate': reference,
                                     'evidence': [], 'limitations': []}}]}
if mode == 'wrong-context':
    returned['context'] = packet['assignment']
if mode == 'unavailable-material':
    product['material'] = ['0' * 64]
print(json.dumps({'id': 'return', 'operation': 'return', 'value': returned}), flush=True)
