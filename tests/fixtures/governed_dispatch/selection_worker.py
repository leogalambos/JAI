# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Actual functional chooser reads the intrinsic catalogue before choosing work."""
import json
from pathlib import Path
import sys

packet = json.loads(sys.stdin.readline())
assignment = next(item['record'] for item in packet['manifest'] if item['ref'] == packet['assignment'])
catalogue = json.loads(Path('/catalogue/catalogue.json').read_text())
roles = {row['slug']: row for row in catalogue['roles']}
assert 'software-engineer' in roles and len(roles) > 100
assert Path('/catalogue/instructions/internal-it-auditor.md').read_text()
assert Path('/catalogue/instructions/software-engineer.md').read_text()
print(json.dumps({'id': 'forbidden-domain-proposal', 'operation': 'propose', 'data': 'bm90IGF1dGhvcml6ZWQ='}), flush=True)
denied = json.loads(sys.stdin.readline())
assert not denied['ok']
workload = 'fixture-' + assignment['responsibility']
available = next(item for item in packet['execution']['availability']
                 if item['provider'] == 'json-process/1' and item['workload_class'] == workload and item['supported'])
choice = {'action': 'select_execution', 'assignment': packet['assignment'],
          'previous': packet['execution']['previous'],
          'specialties': ['software-engineer'], 'provider': available['provider'],
          'workload_class': available['workload_class'], 'model_selector': available['model_selector'],
          'reason': 'Read the full intrinsic catalogue and chose a registered execution-capable professional.',
          'authority_proof': None}
if 'unsupported-model' in assignment['assigned_actor']:
    choice['model_selector'] = 'unavailable-local-model'
print(json.dumps({'id': 'return-choice', 'operation': 'return', 'value': {
    'assignment': packet['assignment'], 'context': packet['context'], 'records': [],
    'intents': [{'message_type': 'decision', 'recipient': {'kind': 'controller', 'id': 'trusted-controller'},
                'payload': choice}]}}), flush=True)
