# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Real isolation probe: unsupported kernels remain explicit rather than fake passes."""
import contextlib
import io
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace as NS

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/commercial_runtime.py'
_SPEC = importlib.util.spec_from_file_location('commercial_runtime', _PATH)
runtime = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(runtime)


class CommercialRuntimeTests(unittest.TestCase):







    def test_untrusted_identity_and_provider_flags_are_not_qualification(self):
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [])
        self.assertIsNone(dispatcher.verify({'principal': 'reviewer'}))
        callbacks = runtime.verification_callbacks(dispatcher, 'a' * 64, 'b' * 64)
        self.assertIsNone(callbacks['identity_verifier']({'principal': 'forged'}))
        self.assertFalse(callbacks['enforcement_verifier']('operational_recovery', {}))
        self.assertIsNone(dispatcher.verify({'payload': {}, 'signature': 'fake'}))
        for provider in ('codex', 'claude'):
            config = runtime.provider_boundary(provider)
            self.assertFalse(config['live_qualified'])
            self.assertIn('Agent', config['denied_tools'])
        with self.assertRaises(ValueError):
            runtime.provider_boundary('unknown')







    def test_actual_fabric_binding_requires_exact_claim_and_hash(self):
        spec = importlib.util.spec_from_file_location('fixture_fabric', _PATH.parents[1] / 'fabric/fabric.py')
        fabric = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fabric)
        domain = {'version_id': 'domain:1', 'type': 'DomainContract', 'data': {}}
        claim = {'version_id': 'claim:1', 'type': 'Claim', 'data': {'text': 'one claim'}}
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()) as output:
            fabric.FABRIC_DIR = directory
            fabric.KEY_PATH = str(Path(directory) / 'authority.key')
            fabric.cmd_init(NS(engagement='binding', intent='commercial test', owner='test', success=None, boundary=None))
            fabric.cmd_req(NS(engagement='binding', layer=1, text='derive meaning', label='derives', **{'from': 'intent-0001'}))
            fields = {key: 'bounded commercial test' for key in fabric.CONTRACT_FIELDS}
            fabric.cmd_contract(NS(engagement='binding', rework_of=None, **fields, **{'from': 'req-0001'}))
            fb = fabric.open_fabric('binding')
            contract = fb.nodes['ctr-0001']
            packet = {'context_digest': fabric.contract_context_packet(fb, contract)[1],
                      'fragments': [{'key': 'product', 'text': 'bounded meaning'}]}
            message = Path(directory) / 'result.json'
            message.write_text(json.dumps(packet))
            fabric.cmd_ingest(NS(engagement='binding', contract='ctr-0001', result=str(message)))
            fb = fabric.open_fabric('binding')
            product = fb.nodes['frag-0001']
            evidence = fb.add_node('evd', 2, 'observed supporting data', confidence='observation')
            fb.add_edge(evidence['id'], 'supports', product['id'])
            fabric.cmd_review(NS(engagement='binding', fragment=product['id'], layer=1, state='accepts',
                                 rationale='independent inspection', reviewer='test-reviewer', model='test', constraints=None))
            fb = fabric.open_fabric('binding')
            mapping = {'domain_contract_version': 'domain:1', 'domain_digest': runtime._digest(domain),
                       'claim_ids': ['claim:1'], 'claim_digests': [runtime._digest(claim)],
                       'target_id': contract['id'], 'target_digest': runtime._digest(contract), 'layer': 2,
                       'fragments': [{'id': product['id'], 'digest': runtime._digest(product)}]}
            binding = runtime.append_commercial_binding(fb, mapping)
            fragment = {'version_id': 'fragment:1', 'type': 'Fragment', 'data': {
                        'fabric_fragment_id': product['id'], 'fabric_fragment_digest': runtime._digest(product)}}
            entity = {'data': {'layer': 2, 'domain_contract_version': 'domain:1', 'claim_ids': ['claim:1'],
                               'fragment_ids': ['fragment:1'], 'fabric_contract_id': contract['id'],
                               'fabric_contract_digest': runtime._digest(contract),
                               'fabric_binding_id': binding['id'], 'fabric_binding_digest': runtime._digest(binding)}}
            for emitted in ('intent-0001', 'req-0001', 'ctr-0001', 'frag-0001', 'rev-0001'):
                self.assertIn(emitted, output.getvalue())
            self.assertIn('accepts', output.getvalue())
            snapshot = {'entities': [domain, claim, fragment]}
            resolver = runtime.fabric_binding_resolver(Path(directory) / 'binding.jsonl')
            self.assertTrue(resolver(entity, snapshot))
            claim['data']['text'] = 'unrelated commitment'
            self.assertFalse(resolver(entity, snapshot))
            mapping['target_digest'] = '0' * 64
            with self.assertRaises(ValueError):
                runtime.append_commercial_binding(fb, mapping)

    def test_empty_ledger_cannot_resolve_claim_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / 'log.jsonl'
            ledger.write_text('')
            resolver = runtime.fabric_binding_resolver(ledger)
            self.assertFalse(resolver({'data': {}}, {'entities': []}))


if __name__ == '__main__':
    unittest.main()
