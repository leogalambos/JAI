# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Legacy compatibility diagnostics never confer execution authority."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import agent_runtime as runtime


class AgentRuntimeTests(unittest.TestCase):
    def test_loader_and_generated_native_restrictions(self):
        self.assertTrue(runtime.load(runtime.CONTRACTS)['contracts'])
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / 'invalid.json'
            bad.write_text('{')
            with self.assertRaises(json.JSONDecodeError):
                runtime.load(bad)
            with self.assertRaises(OSError):
                runtime.load(Path(directory) / 'missing')
            runtime.generate(directory)
            for provider in ('codex', 'claude'):
                for path in (Path(directory) / provider).glob('*.json'):
                    config = json.loads(path.read_text())
                    self.assertEqual(config['runtime_boundary'], runtime.load(runtime.ROOT/'providers'/provider/path.name)['runtime_boundary'])
                    self.assertFalse(config['runtime_boundary']['live_verified'])
                    if provider == 'codex':
                        author=runtime.contracts()[path.stem]['mutation_allowed']
                        self.assertEqual(config['sandbox_mode'], 'workspace-write' if author else 'read-only')
                        self.assertEqual(config['workspace_write'], author)
                        self.assertFalse(config['network'])
                        contract=runtime.contracts()[path.stem]
                        self.assertEqual('Bash' in config['allowed_tools'], 'Bash' in contract['allowed_tools'])
                    else:
                        self.assertEqual(config['sandbox']['workspace_write'], runtime.contracts()[path.stem]['mutation_allowed'])
                        self.assertFalse(config['sandbox']['network'])
                        contract=runtime.contracts()[path.stem]
                        self.assertEqual('Bash' in config['tools'], contract['mutation_allowed'] and 'Bash' in contract['allowed_tools'])
                        self.assertTrue(config['native_claude']['sandbox']['failIfUnavailable'])
                        self.assertFalse(config['native_claude']['sandbox']['allowUnsandboxedCommands'])
                        self.assertEqual(config['native_claude']['sandbox']['excludedCommands'], [])

    def test_registered_read_write_diagnostics_and_selftest_remain_functional(self):
        import release_bundle
        scope=runtime.release_scope()
        self.assertEqual(scope, runtime.load(TOOLS.parents[2]/'RELEASE-SCOPE.json'))
        self.assertFalse(scope['hardened_privileged']['enabled'])
        scope['hardened_privileged']['enabled']=True
        self.assertFalse(runtime.release_scope()['hardened_privileged']['enabled'])
        for name in release_bundle.HARDENED_MODULES:
            self.assertTrue(release_bundle.hardened_resource('.ai/runtime/tools/'+name))
        self.assertFalse(release_bundle.hardened_resource('.ai/runtime/tools/agent_runtime.py'))
        shipped={str(p.relative_to(TOOLS.parents[2])) for p in release_bundle.files(TOOLS.parents[2])}
        self.assertFalse(any(release_bundle.hardened_resource(p) for p in shipped))
        contracts = runtime.contracts()
        self.assertTrue(runtime.authorize(contracts['role-engineer'], 'validate', 'Bash')[0])
        self.assertTrue(runtime.authorize(contracts['codebase-reviewer'], 'validate', 'Bash')[0])
        self.assertFalse(runtime.authorize(contracts['role-author'], 'validate', 'Bash')[0])
        self.assertTrue(runtime.authorize(contracts['role-author'], 'write', 'Write')[0])
        self.assertFalse(runtime.authorize(contracts['codebase-reviewer'], 'write')[0])
        self.assertFalse(runtime.authorize(contracts['role-author'], 'unregistered')[0])
        self.assertFalse(runtime.authorize(contracts['role-author'], 'read', 'UnknownTool')[0])
        self.assertFalse(runtime.authorize({'id': 'role-author'}, 'write')[0])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runtime.self_test(), 0)
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            installed=Path(directory)/'house'; (installed/'tools').mkdir(parents=True)
            (installed/'schema').mkdir()
            (installed/'schema/release-scope.schema.json').write_bytes((runtime.ROOT/'schema/release-scope.schema.json').read_bytes())
            (installed/'RELEASE-SCOPE.json').write_text(json.dumps(runtime.release_scope()))
            with patch.object(runtime,'ROOT',installed), patch.object(release_bundle,'files',side_effect=AssertionError('must not enumerate installation parents')), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runtime.self_test(),0)

    def test_release_scope_is_canonical_validated_and_not_privileged_authority(self):
        import copy
        from unittest.mock import patch
        import jsonschema
        actor=runtime.contracts()['role-author']
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'schema').mkdir()
            (root/'schema/release-scope.schema.json').write_bytes((runtime.ROOT/'schema/release-scope.schema.json').read_bytes())
            manifest=root/'RELEASE-SCOPE.json';canonical=runtime.release_scope()
            with self.assertRaises(OSError):runtime.release_scope(root)
            manifest.write_text('{')
            with self.assertRaises(ValueError):runtime.release_scope(root)
            changed=copy.deepcopy(canonical)
            namespace,revision=changed['scope'].rsplit('/',1)
            changed['scope']=namespace+'/'+str(int(revision)+1)
            changed['enabled']=changed['enabled'][:-1]
            manifest.write_text(json.dumps(changed))
            with patch.object(runtime,'ROOT',root):
                self.assertEqual(runtime.release_scope(),changed)
                self.assertEqual(runtime.provider_config(actor,'codex')['runtime_boundary']['scope'],changed['scope'])
                self.assertFalse(runtime.authorize(actor,'privileged-execute')[0])
            for corrupt in [dict(changed,enabled=['root-shell']),dict(changed,hardened_privileged={**changed['hardened_privileged'],'enabled':True}),dict(changed,agent_git_required=True)]:
                manifest.write_text(json.dumps(corrupt))
                with self.assertRaises(ValueError):runtime.release_scope(root)
                with patch.object(runtime,'ROOT',root):self.assertFalse(runtime.authorize(actor,'write')[0])
            manifest.write_text(json.dumps(changed))
            with patch.dict(sys.modules,{'jsonschema':None}), patch.object(runtime,'jsonschema',None):
                self.assertEqual(runtime.release_scope(root),changed)
                with self.assertRaisesRegex(ValueError,'validator unavailable'):runtime.contracts()
                self.assertFalse(runtime.authorize(actor,'write')[0])
            nested=root/'nested/.ai/runtime';(nested/'schema').mkdir(parents=True)
            (nested/'schema/release-scope.schema.json').write_bytes((root/'schema/release-scope.schema.json').read_bytes())
            (nested/'RELEASE-SCOPE.json').write_text(json.dumps(changed))
            self.assertEqual(runtime.release_scope(nested),changed)
            (root/'nested/RELEASE-SCOPE.json').write_text(json.dumps(canonical))
            with self.assertRaisesRegex(ValueError,'ambiguous'):runtime.release_scope(nested)
            (nested/'RELEASE-SCOPE.json').unlink()
            with self.assertRaises(OSError):runtime.schema_resolver.release_scope(nested)
            (nested/'RELEASE-SCOPE.json').write_text(json.dumps(changed))
            (root/'nested/RELEASE-SCOPE.json').unlink()
            (root/'nested/.ai/setup').mkdir()
            (root/'nested/.ai/setup/installer.py').write_text('# source-layout fixture')
            with patch.object(runtime,'ROOT',nested):
                with self.assertRaises(OSError):runtime.release_scope()
                self.assertFalse(runtime.authorize(actor,'write')[0])
            with self.assertRaises(OSError):runtime.schema_resolver.release_scope(nested)



if __name__ == '__main__':
    unittest.main()
