# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Real isolation probe: unsupported kernels remain explicit rather than fake passes."""
import importlib.util
import hashlib
import json
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
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [('/usr/bin/true',)])
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

    def test_host_rejects_shell_unknown_commands_and_history(self):
        with self.assertRaises(ValueError):
            runtime.TrustedDispatcher(b'x' * 32, [('/usr/bin/bash', '-c', 'true')])
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [('/usr/bin/true',)])
        with self.assertRaisesRegex(ValueError, 'allowlist'):
            dispatcher.run(('/usr/bin/false',), {}, 'a' * 64, {})
        with self.assertRaisesRegex(ValueError, 'fresh'):
            dispatcher.run(('/usr/bin/true',), {}, 'a' * 64, {'history_policy': 'fork'})

    def test_real_runner_reports_enforcement_or_explicit_not_run(self):
        command = ('/usr/bin/true',)
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [command])
        result = dispatcher.run(command, {'id': 'subject'}, 'a' * 64,
                                {'history_policy': 'fresh', 'injected_instructions': ['host-policy:1']})
        self.assertIn(result['status'], ('tested', 'unsupported', 'not_run'))
        if result['status'] != 'tested':
            self.assertIsNone(result['attestation'])
            self.assertIsNone(dispatcher.verify(result['attestation']))
            print('bwrap isolation qualification:', result['status'], result.get('stderr', result.get('reason')))
            return
        payload = dispatcher.verify(result['attestation'])
        self.assertEqual(payload['snapshot_digest'], 'a' * 64)
        result['attestation']['payload']['subject_digest'] = 'b' * 64
        self.assertIsNone(dispatcher.verify(result['attestation']))

    def test_real_runner_negative_mount_context_and_write_boundaries(self):
        # The host-approved diagnostic is deterministic; it never receives host directories.
        code = ('import os,pathlib; p=pathlib.Path("/inputs/0"); '
                'assert p.read_text()=="public"; '
                'assert not pathlib.Path("/home/sibling-marker").exists(); '
                'assert "INHERITED_MARKER" not in os.environ; '
                '\ntry: p.write_text("changed")\nexcept OSError: pass\nelse: raise AssertionError("writable reviewer mount")')
        command = ('/usr/bin/python3', '-c', code)
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [command])
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'product.txt'
            source.write_text('public')
            result = dispatcher.run(command, {}, 'a' * 64,
                                    {'history_policy': 'fresh', 'injected_instructions': ['policy:1']}, inputs=[source])
            self.assertIn(result['status'], ('tested', 'not_run', 'unsupported'))
            self.assertEqual(source.read_text(), 'public')
            if result['status'] == 'tested':
                self.assertIsNotNone(dispatcher.verify(result['attestation']))
            else:
                self.assertIsNone(result['attestation'])

    def test_two_host_dispatches_bind_distinct_real_worker_launches(self):
        command = ('/usr/bin/true',)
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [command])
        context = {'history_policy': 'fresh', 'injected_instructions': ['policy:1']}
        class Worker:
            def __init__(self, pid):
                self.pid, self.returncode = pid, 0
            def communicate(self, timeout=None):
                return '', ''
        with patch.object(runtime.shutil, 'which', return_value='/usr/bin/bwrap'), patch.object(runtime.subprocess, 'Popen', side_effect=[Worker(1001), Worker(1002)]):
            maker = dispatcher.run(command, {'kind': 'maker'}, 'a' * 64, context, reviewer=False)
            checker = dispatcher.run(command, {'kind': 'review'}, 'a' * 64, context)
        first, second = [dispatcher.verify(item['attestation']) for item in (maker, checker)]
        self.assertNotEqual(first['principal'], second['principal'])
        self.assertEqual(first['worker_execution']['pid'], 1001)
        self.assertEqual(second['worker_execution']['pid'], 1002)
        self.assertTrue(second['worker_execution']['readonly_inputs'])
        callbacks = runtime.verification_callbacks(dispatcher, 'a' * 64, runtime._digest(context))
        self.assertEqual(callbacks['identity_verifier'](checker['attestation'])['principal'], second['principal'])
        self.assertFalse(callbacks['enforcement_verifier']('operational_recovery', checker['attestation']))
        checker['attestation']['payload']['worker_execution']['pid'] = 9999
        self.assertIsNone(dispatcher.verify(checker['attestation']))

    def test_signed_worker_executions_satisfy_core_independence_without_granting_authority(self):
        from test_commercial_core import complete_snapshot, core
        data, _ = complete_snapshot()
        index = {item['version_id']: item for item in data['entities']}
        claim, review = index['claim@1'], index['review@1']
        del claim['data']['producer_attestation']
        del review['data']['attestation']
        command = ('/usr/bin/true',)
        context = {'history_policy': 'fresh', 'injected_instructions': ['policy:1']}
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [command])
        class Worker:
            def __init__(self, pid):
                self.pid, self.returncode = pid, 0
            def communicate(self, timeout=None):
                return '', ''
        # This is a process-boundary fake, not deployment/provider qualification.
        with patch.object(runtime.shutil, 'which', return_value='/usr/bin/bwrap'), patch.object(runtime.subprocess, 'Popen', side_effect=[Worker(1001), Worker(1002)]):
            claim['data']['producer_attestation'] = dispatcher.run(command, claim, 'a' * 64, context, reviewer=False)['attestation']
            review['data']['reviewed_digest'] = core.digest(claim)
            review['data']['attestation'] = dispatcher.run(command, review, 'a' * 64, context)['attestation']
        callbacks = runtime.verification_callbacks(dispatcher, 'a' * 64, runtime._digest(context))
        result = core.readiness(data, identity_verifier=callbacks['identity_verifier'],
                                fabric_resolver=lambda entity, snapshot: True,
                                enforcement_verifier=lambda control, record: True)
        self.assertTrue(result['ready'], result['blockers'])
        self.assertFalse(result['authority_granted'])
        review['data']['attestation'] = claim['data']['producer_attestation']
        self.assertFalse(core.readiness(data, identity_verifier=callbacks['identity_verifier'],
                         fabric_resolver=lambda entity, snapshot: True,
                         enforcement_verifier=lambda control, record: True)['ready'])

    def test_worker_launch_timeout_and_failure_never_attest(self):
        from unittest.mock import Mock
        command = ('/usr/bin/true',)
        context = {'history_policy': 'fresh', 'injected_instructions': ['policy:1']}
        dispatcher = runtime.TrustedDispatcher(b'x' * 32, [command])
        with patch.object(runtime.shutil, 'which', return_value=None):
            self.assertIsNone(dispatcher.run(command, {}, 'a' * 64, context)['attestation'])
        with patch.object(runtime.shutil, 'which', return_value='/usr/bin/bwrap'):
            with patch.object(runtime.subprocess, 'Popen', side_effect=OSError('launch refused')):
                self.assertEqual(dispatcher.run(command, {}, 'a' * 64, context)['status'], 'not_run')
            worker = Mock(pid=1001, returncode=-9)
            worker.communicate.side_effect = [runtime.subprocess.TimeoutExpired(command, 1), ('', '')]
            with patch.object(runtime.subprocess, 'Popen', return_value=worker):
                result = dispatcher.run(command, {}, 'a' * 64, context, timeout=1)
            self.assertIsNone(result['attestation'])
            worker.kill.assert_called_once_with()
            failed = Mock(pid=1002, returncode=1)
            failed.communicate.return_value = ('', 'namespace denied')
            with patch.object(runtime.subprocess, 'Popen', return_value=failed):
                result = dispatcher.run(command, {}, 'a' * 64, context)
            self.assertEqual(result['status'], 'not_run')
            self.assertIsNone(result['attestation'])

    def test_actual_fabric_binding_requires_exact_claim_and_hash(self):
        spec = importlib.util.spec_from_file_location('fixture_fabric', _PATH.parents[1] / 'fabric/fabric.py')
        fabric = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fabric)
        domain = {'version_id': 'domain:1', 'type': 'DomainContract', 'data': {}}
        claim = {'version_id': 'claim:1', 'type': 'Claim', 'data': {'text': 'one claim'}}
        with tempfile.TemporaryDirectory() as directory:
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
