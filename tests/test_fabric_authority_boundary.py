# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Local environment, terminals and hook names cannot create L0 authority."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/fabric/fabric.py'
SPEC = importlib.util.spec_from_file_location('fabric_authority_test', PATH)
fabric = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fabric)


class FabricAuthorityBoundaryTests(unittest.TestCase):
    def test_unavailable_authority_verification_key_is_blocking_not_a_warning(self):
        import hashlib
        authority = {'id': 'review-1', 'type': 'rev', 'layer': 0}
        previous = '0' * 64
        checksum = hashlib.sha256((previous + fabric.canonical(authority) + '1').encode()).hexdigest()
        entries = [{'seq': 1, 'op': 'node', 'data': authority, 'prev': previous,
                    'hash': checksum, 'sig': 'synthetic-untrusted-signature'}]
        model = fabric.Fabric('synthetic-test', entries)
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric, 'KEY_PATH', str(Path(directory) / 'absent.key')):
            problems, warnings = model.verify()
        self.assertTrue(any('key unavailable' in problem for problem in problems), (problems, warnings))
        self.assertFalse(any('key unavailable' in warning for warning in warnings))

    def test_agent_environment_tty_hook_and_json_never_authorize(self):
        with patch.dict(os.environ, {'FABRIC_TEST_AUTHORITY': '1'}), patch.object(
                fabric, 'confirmation_gate_active', return_value=True), patch.object(
                sys.stdin, 'isatty', return_value=True), patch.object(sys.stdout, 'isatty', return_value=True):
            with self.assertRaises(fabric.FabricError):
                fabric.require_human('test authority act')

    def test_caller_chosen_legacy_hmac_is_not_independent_l0(self):
        import hashlib,hmac
        with tempfile.TemporaryDirectory() as directory:
            key=Path(directory)/'synthetic-legacy-key';key.write_bytes(b'synthetic-test-key-not-human-authority')
            entries=[]
            def node(op,data,sign=False):
                previous=entries[-1]['hash'] if entries else '0'*64;seq=len(entries)+1
                digest=hashlib.sha256((previous+fabric.canonical(data)+str(seq)).encode()).hexdigest()
                item={'op':op,'data':data,'seq':seq,'prev':previous,'hash':digest}
                if sign:item['sig']=hmac.new(key.read_bytes(),digest.encode(),'sha256').hexdigest()
                entries.append(item)
            node('node',{'id':'f','type':'frag','layer':1,'kind':'product','text':'Synthetic target'})
            node('node',{'id':'e','type':'evd','layer':1,'confidence':'observation','text':'Synthetic observed evidence'})
            node('node',{'id':'r','type':'rev','layer':0,'state':'accepts','text':'Untrusted HMAC assertion'},True)
            node('edge',{'src':'e','label':'supports','dst':'f'})
            node('edge',{'src':'f','label':'reviewed_by','dst':'r'})
            with patch.object(fabric,'KEY_PATH',str(key)):
                graph=fabric.Fabric('synthetic',entries);problems,warnings=graph.verify()
                self.assertEqual(problems,[])
                self.assertTrue(any('HMAC integrity only' in w for w in warnings))
                self.assertFalse(graph.authority_verified('r'))
                accepted,reasons=graph.justify('f',strict=True)
                self.assertFalse(accepted)
                self.assertTrue(any('independent operator attestation' in reason for reason in reasons))

    def test_fabric_selftest_cannot_export_authority_to_later_calls(self):
        program = '''import importlib.util, os, sys
s=importlib.util.spec_from_file_location('f',sys.argv[1]); f=importlib.util.module_from_spec(s); s.loader.exec_module(f)
before=(f.FABRIC_DIR,f.KEY_PATH,dict(os.environ))
assert f.cmd_selftest(None)==0
assert before==(f.FABRIC_DIR,f.KEY_PATH,dict(os.environ))
try: f.require_human('after selftest')
except f.FabricError: pass
else: raise AssertionError('selftest exported authority')
'''
        result = subprocess.run([sys.executable, '-c', program, str(PATH)], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
