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
import pytest
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
        from lifecycle_fixtures import accepted_graph
        spec = importlib.util.spec_from_file_location('fixture_fabric', _PATH.parents[1] / 'fabric/fabric.py')
        fabric = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fabric)
        domain = {'version_id': 'domain:1', 'type': 'DomainContract', 'data': {}}
        claim = {'version_id': 'claim:1', 'type': 'Claim', 'data': {'text': 'one claim'}}
        with tempfile.TemporaryDirectory() as directory, pytest.MonkeyPatch.context() as monkeypatch, contextlib.redirect_stdout(io.StringIO()):
            fb,product_id,_=accepted_graph(fabric,Path(directory),monkeypatch,'Bounded meaning',
                engagement='binding',requirement_text='Bounded commercial requirement')
            product=fb.nodes[product_id]
            contract=next(node for node in fb.nodes.values() if node['type']=='req')
            mapping = {'domain_contract_version': 'domain:1', 'domain_digest': runtime._digest(domain),
                       'claim_ids': ['claim:1'], 'claim_digests': [runtime._digest(claim)],
                       'target_id': contract['id'], 'target_digest': runtime._digest(contract), 'layer': 1,
                       'fragments': [{'id': product['id'], 'digest': runtime._digest(product)}]}
            binding = runtime.append_commercial_binding(fb, mapping)
            fragment = {'version_id': 'fragment:1', 'type': 'Fragment', 'data': {
                        'fabric_fragment_id': product['id'], 'fabric_fragment_digest': runtime._digest(product)}}
            entity = {'data': {'layer': 1, 'domain_contract_version': 'domain:1', 'claim_ids': ['claim:1'],
                               'fragment_ids': ['fragment:1'], 'fabric_requirement_id': contract['id'],
                               'fabric_requirement_digest': runtime._digest(contract),
                               'fabric_binding_id': binding['id'], 'fabric_binding_digest': runtime._digest(binding)}}
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
            with self.assertRaises(ValueError):
                runtime.fabric_binding_resolver(ledger)

    def test_unmarked_graph_rows_are_archive_only(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / 'log.jsonl'
            ledger.write_text(json.dumps({'op': 'node', 'seq': 1, 'data': {}}) + '\n')
            with self.assertRaises(ValueError):
                runtime.fabric_binding_resolver(ledger)


if __name__ == '__main__':
    unittest.main()
