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
import sys
import unittest
import pytest
from unittest.mock import patch
from types import SimpleNamespace as NS

_PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/commercial_runtime.py'
sys.path.insert(0, str(_PATH.parent))
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







    def test_actual_governed_binding_requires_exact_claim_hash_and_current_output(self):
        from governed_fixtures import GovernedHarness, lc
        domain = {'version_id': 'domain:1', 'type': 'DomainContract', 'data': {}}
        claim = {'version_id': 'claim:1', 'type': 'Claim', 'data': {'text': 'one claim'}}
        with tempfile.TemporaryDirectory() as directory, pytest.MonkeyPatch.context() as monkeypatch:
            host = GovernedHarness(Path(directory), monkeypatch, engagement='binding')
            host.bootstrap()
            actor, output, _ = host.qualified_answer()
            mapping = {'domain_contract_version': 'domain:1', 'domain_digest': runtime._digest(domain),
                       'claim_ids': ['claim:1'], 'claim_digests': [runtime._digest(claim)],
                       'assignment': actor['author'], 'layer': actor['owner']['layer'],
                       'outputs': [output]}
            binding, _, delivery = host.observation(actor, lc.canonical(mapping).decode(),
                                                    suffix='claim-binding')
            response = runtime.append_commercial_binding(host.store, mapping, message=host.outbound(delivery),
                                                          dispatch_proof=host.attest(delivery))
            self.assertEqual(response['status'], 'committed')
            fragment = {'version_id': 'fragment:1', 'type': 'Fragment',
                        'data': {'governed_output': output}}
            entity = {'data': {'layer': actor['owner']['layer'], 'domain_contract_version': 'domain:1',
                               'claim_ids': ['claim:1'], 'fragment_ids': ['fragment:1'],
                               'governed_assignment': actor['author'], 'governed_binding': binding}}
            snapshot = {'entities': [domain, claim, fragment]}
            resolver = runtime.fabric_binding_resolver(host.path)
            self.assertTrue(resolver(entity, snapshot))
            claim['data']['text'] = 'unrelated commitment'
            self.assertFalse(resolver(entity, snapshot))
            claim['data']['text'] = 'one claim'
            wrong = dict(mapping, domain_digest='0' * 64)
            before = host.path.read_bytes()
            with self.assertRaises(ValueError):
                runtime.append_commercial_binding(host.store, wrong, message=host.outbound(delivery),
                                                   dispatch_proof=host.attest_invalid_proposal(delivery))
            self.assertEqual(host.path.read_bytes(), before)
            invalidation = host.owner_decision(actor['owner'], {'action': 'invalidate',
                'reason': 'Required current output is no longer supported', 'subjects': [output]})
            host.commit(invalidation)
            self.assertFalse(resolver(entity, snapshot))

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
