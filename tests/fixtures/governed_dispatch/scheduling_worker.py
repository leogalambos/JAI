# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""A quiet normal process; an exact speculative context produces pending facts."""
import base64
import hashlib
import json
import signal
import sys


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def _return_package(packet, assignment, identifier):
    body = {'owner': assignment['owner'], 'product_kind': 'answer',
            'assignment': packet['assignment'], 'profile': assignment['profile'],
            'inputs': assignment['inputs'], 'material': [identifier],
            'evidence': [], 'related': [], 'limitations': []}
    logical_id = 'actual-speculative-native-answer'
    manifest = {'schema': 'jai.lifecycle.manifest/2', 'logical_id': logical_id,
                'kind': 'delivery.product', 'content': {
                    'engagement': packet['assignment']['engagement'],
                    'scope': packet['assignment']['scope'], 'record': body},
                'bindings': {}, 'members': []}
    reference = {**packet['assignment'], 'logical_id': logical_id,
        'version_id': hashlib.sha256(b'jai.lifecycle.version.v2\0' + _canonical(manifest)).hexdigest()}
    return {'assignment': packet['assignment'], 'context': packet['context'],
            'records': [{'logical_id': logical_id, 'record_type': 'product', 'record': body}],
            'intents': [{'message_type': 'submission',
                'recipient': {'kind': 'controller', 'id': 'trusted-controller'},
                'payload': {'assignment': packet['assignment'], 'candidate': reference,
                            'evidence': [], 'limitations': []}}]}


def _request(identifier, operation, **fields):
    print(json.dumps({'id': identifier, 'operation': operation, **fields}), flush=True)
    response = json.loads(sys.stdin.readline())
    if not response['ok']:
        raise RuntimeError(response)
    return response['result']


def main():
    """Read one actual packet and return only under its exact speculative context."""
    packet = json.loads(sys.stdin.readline())
    assignment = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['assignment'])
    context = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['context'])
    attachment = packet['attachments'][0]
    read = _request('quiet-ready', 'read', handle=attachment['handle'])
    if context['speculation'] is None:
        signal.pause()
        return 1
    observation = _canonical({'input_blob_id': attachment['blob_id'],
                              'read_bytes': len(base64.b64decode(read['data'])),
                              'speculation': context['speculation']})
    proposed = _request('actual-observation', 'propose', data=base64.b64encode(observation).decode())
    print(json.dumps({'id': 'return', 'operation': 'return',
                      'value': _return_package(packet, assignment, proposed['blob_id'])}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
