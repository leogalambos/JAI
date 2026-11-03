# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Small real-process probe for aggregate raw measurement output accounting."""
import json
import sys

packet = json.loads(sys.stdin.readline())
if sys.argv[1] == 'tool':
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    sys.stdout.write('m' * size)
    raise SystemExit(0)
assignment = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['assignment'])
grant = next(item for item in assignment['effects'] if item['operation'] == 'measure')
for index in range(3):
    print(json.dumps({'id': 'measurement-' + str(index), 'operation': 'measure',
                      'tool_policy': grant['tool_policy'], 'targets': grant['targets']}), flush=True)
    response = json.loads(sys.stdin.readline())
    if not response['ok']:
        raise RuntimeError(response)
print(json.dumps({'id': 'return', 'operation': 'return', 'value': {
    'assignment': packet['assignment'], 'context': packet['context'], 'records': [],
    'intents': [{'message_type': 'information_request',
                'recipient': {'kind': 'assignment', 'ref': assignment['issued_under']},
                'payload': {'assignment': packet['assignment'], 'needed': [],
                            'question': 'Measurement processing finished; clarify the next obligation.',
                            'blocked_obligations': [assignment['criteria']]}}]}}), flush=True)
