# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Install-time provider projections preserve canonical runtime bindings."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import agent_runtime

spec = importlib.util.spec_from_file_location('tested_installer', ROOT / '.ai/setup/installer.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerProjectionTests(unittest.TestCase):
    def test_content_profile_bindings_preserved_without_permission_expansion(self):
        registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_text())
        for name, shell in (('role-engineer', True), ('codebase-reviewer', False)):
            rendered = installer.render_claude_agent(ROOT / '.ai/agents' / (name + '.md'), registry).decode()
            tools = next(line for line in rendered.splitlines() if line.startswith('tools:'))
            self.assertEqual('Bash' in tools, shell)
        profile=json.loads((ROOT/'.ai/runtime/jai/profiles/content-profile.json').read_text())
        registry=json.loads((ROOT/'.ai/runtime/models/model-registry.json').read_text())
        for name in profile['agent_bindings']:
            contract=agent_runtime.contracts()[name]
            for provider in ('claude','codex'):
                expected=agent_runtime.provider_config(contract,provider)
                installed=installer.provider_contract_config(contract,provider,registry,profile)
                self.assertEqual(installed,expected)
                self.assertEqual(installed['content_profile_ref'],'jai/profiles/content-profile.json')
                self.assertFalse(installed['runtime_boundary']['live_verified'])
        unsafe=copy.deepcopy(profile)
        unsafe['agent_bindings']['role-author']={'workspace_write':True}
        with self.assertRaises(ValueError):
            installer.provider_contract_config(agent_runtime.contracts()['role-author'],'codex',registry,unsafe)

    def test_desired_outputs_preserve_exact_canonical_provider_contracts(self):
        contract = agent_runtime.contracts()['codebase-reviewer']
        registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            package = home / 'package'
            for section in ('runtime/agents', 'skills', 'agents', 'commands'):
                (package / '.ai' / section).mkdir(parents=True)
            (package/'.ai/runtime/schema').mkdir()
            (package/'.ai/runtime/schema/release-scope.schema.json').write_bytes((ROOT/'.ai/runtime/schema/release-scope.schema.json').read_bytes())
            (package/'RELEASE-SCOPE.json').write_bytes((ROOT/'RELEASE-SCOPE.json').read_bytes())
            (package / '.ai/runtime/agents/agent-contracts.json').write_text(json.dumps({'contracts': [contract]}))
            (package/'.ai/runtime/tools').mkdir()
            (package/'.ai/runtime/tools/runtime_service.py').write_text('raise RuntimeError("not shipped")')
            outputs, modes = installer.desired_outputs(package, {'codex', 'claude'}, home / 'house', home / 'claude', home / 'codex', registry)
            self.assertNotIn(str(home/'house/tools/runtime_service.py'),outputs)
            for provider in ('codex', 'claude'):
                path = str(home / 'house/providers' / provider / 'codebase-reviewer.json')
                expected = agent_runtime.provider_config(contract, provider)
                self.assertEqual(json.loads(outputs[path]), expected)
                self.assertEqual(modes[path], 0o644)
                self.assertFalse(Path(path).exists())
                actual = installer.provider_contract_config(contract, provider, registry)
                actual['jai']['profile'] = 'changed'
                self.assertEqual(contract['jai']['profile'], 'runtime')
            changed=json.loads((package/'RELEASE-SCOPE.json').read_text())
            name,revision=changed['scope'].rsplit('/',1)
            changed['scope']=name+'/'+str(int(revision)+1)
            (package/'RELEASE-SCOPE.json').write_text(json.dumps(changed))
            self.assertEqual(installer.provider_contract_config(contract,'codex',registry,scope_root=package)['runtime_boundary']['scope'],changed['scope'])

    def test_provider_contract_rejects_unsupported_provider_and_missing_binding(self):
        contract = copy.deepcopy(agent_runtime.contracts()['codebase-reviewer'])
        registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_text())
        with self.assertRaises(ValueError):
            installer.provider_contract_config(contract, 'unknown', registry)
        del contract['jai']
        with self.assertRaises(ValueError):
            installer.provider_contract_config(contract, 'codex', registry)


class InstallerSafetyTests(unittest.TestCase):
    def test_atomic_files_backups_and_hashes_preserve_existing_content_on_failure(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'settings.json'
            installer.atomic_write(target, b'original', 0o600)
            self.assertEqual(installer.sha_file(target), installer.sha_bytes(b'original'))
            self.assertEqual(installer.sha_bytes(b''), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
            self.assertIsNone(installer.sha_file(root / 'missing'))
            self.assertTrue(installer.backup_one(target, root / 'backup'))
            copies = list((root / 'backup').rglob('settings.json'))
            self.assertEqual([p.read_bytes() for p in copies], [b'original'])
            self.assertFalse(installer.backup_one(root / 'missing', root / 'backup'))
            with patch.object(installer.os, 'replace', side_effect=OSError('replace refused')):
                with self.assertRaises(OSError):
                    installer.atomic_write(target, b'changed')
            self.assertEqual(target.read_bytes(), b'original')
            self.assertEqual(list(root.glob('.settings.json.*')), [])
            (root / '__pycache__').mkdir()
            (root / '__pycache__/ignored.pyc').write_bytes(b'x')
            self.assertNotIn(root / '__pycache__/ignored.pyc', installer.files_under(root))
            self.assertEqual(installer.files_under(root / 'missing'), [])

    def test_frontmatter_rendering_keeps_role_tool_boundary_and_unicode(self):
        front, body = installer.split_frontmatter('---\nname: sample\ndescription: "Café"\n---\nBody')
        self.assertEqual(front, {'name': 'sample', 'description': 'Café'})
        self.assertEqual(body, 'Body')
        malformed = '---\nname: missing-close\nBody'
        self.assertEqual(installer.split_frontmatter(malformed), ({}, malformed))
        self.assertEqual(installer.split_frontmatter('Body'), ({}, 'Body'))
        rendered = installer.skill_doc('sample', 'Café', ' Body', 'skill', 'sample', 'Read').decode()
        self.assertIn('Source tool ceiling: `Read`', rendered)
        self.assertIn('Café', rendered)
        self.assertTrue(rendered.endswith('Body'))
        command = installer.skill_doc('workflow-sample', '', 'Body', 'command', 'sample').decode()
        self.assertIn('workflow command `/sample`', command)
        self.assertNotIn('Source tool ceiling', command)

    def test_deep_merge_and_placeholders_do_not_mutate_user_configuration(self):
        base = {'nested': {'keep': [1], 'change': 'old'}, 'value': 1}
        override = {'nested': {'change': 'new'}, 'value': [2]}
        merged = installer.deep_merge(base, override)
        merged['nested']['keep'].append(3)
        self.assertEqual(base['nested']['keep'], [1])
        self.assertEqual(merged['nested']['change'], 'new')
        self.assertEqual(installer.deep_merge([1], {'value': 2}), {'value': 2})
        data = {'path': '{AI_HOUSE}/bin', 'nested': ['{AI_HOUSE}', 5], 'flag': True}
        self.assertEqual(installer.render_placeholders(data, '/tmp/house'), {'path': '/tmp/house/bin', 'nested': ['/tmp/house', 5], 'flag': True})
        self.assertEqual(data['path'], '{AI_HOUSE}/bin')

    def test_registry_override_and_json_validation_fail_closed(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            model_dir = package / '.ai/runtime/models'
            model_dir.mkdir(parents=True)
            registry = {'fallback_class': 'standard', 'workload_classes': {'standard': {}},
                        'providers': {p: {'classes': {'standard': {'model_selector': 'inherit'}}} for p in ('claude', 'codex')}}
            registry_path = model_dir / 'model-registry.json'
            registry_path.write_text(json.dumps(registry))
            override = package / 'override.json'
            override.write_text(json.dumps({'providers': {'codex': {'classes': {'standard': {'model_selector': 'chosen'}}}}}))
            with patch.dict(installer.os.environ, {}, clear=True):
                loaded, source = installer.load_model_registry(package, str(override))
            self.assertEqual(source, override)
            self.assertEqual(installer.model_selector(loaded, 'codex', 'standard'), 'chosen')
            mapping = installer.model_mapping(loaded, 'claude', 'standard')
            mapping['model_selector'] = 'mutated'
            self.assertEqual(loaded['providers']['claude']['classes']['standard']['model_selector'], 'inherit')
            with self.assertRaises(SystemExit):
                installer.model_mapping(loaded, 'missing', 'standard')
            default = {'list': []}
            fallback = installer.json_load(package / 'missing.json', default)
            fallback['list'].append('changed')
            self.assertEqual(default, {'list': []})
            override.write_text('broken-json')
            with self.assertRaises(SystemExit):
                installer.json_load(override, {})
            registry['fallback_class'] = 'absent'
            registry_path.write_text(json.dumps(registry))
            with self.assertRaises(SystemExit):
                installer.load_model_registry(package, str(package / 'missing.json'))

    def test_managed_json_roundtrip_removes_only_installer_owned_additions(self):
        user_hook = {'hooks': [{'command': 'user-check'}]}
        managed_hook = {'hooks': [{'command': 'managed-check'}]}
        original = {'permissions': {'allow': ['Read'], 'deny': ['Write']}, 'hooks': {'PreToolUse': [user_hook]}, 'custom': True}
        snippet = {'permissions': {'allow': ['Read', 'Edit']}, 'hooks': {'PreToolUse': [managed_hook]}}
        merged, added = installer.merge_snippet(original, snippet)
        self.assertEqual(merged['permissions']['allow'], ['Read', 'Edit'])
        self.assertEqual(added['permissions']['allow'], ['Edit'])
        self.assertEqual(installer.hook_cmds(managed_hook), {'managed-check'})
        self.assertEqual(installer.hook_cmds({'hooks': [None, {}, {'command': ''}]}), set())
        repeated, second = installer.merge_snippet(merged, snippet)
        self.assertEqual(repeated, merged)
        self.assertEqual(second, {'permissions': {}, 'hooks': {}})
        self.assertEqual(installer.remove_recorded_json(merged, added), original)
        self.assertEqual(original['permissions']['allow'], ['Read'])
        self.assertEqual(installer.remove_recorded_json({}, {}), {})

    def test_managed_blocks_keep_user_prose_and_replace_legacy_content(self):
        begin, end = '<managed>', '</managed>'
        first = installer.managed_block('User instructions', begin, end, 'owned')
        updated = installer.managed_block(first, begin, end, 'updated')
        self.assertTrue(updated.startswith('User instructions'))
        self.assertNotIn('\nowned\n', updated)
        self.assertEqual(installer.remove_block(updated, begin, end), 'User instructions\n')
        self.assertEqual(installer.remove_block('untouched', begin, end), 'untouched')
        self.assertEqual(installer.managed_block('', begin, end, 'owned'), '<managed>\nowned\n</managed>\n')
        legacy = installer.LEGACY_MARKERS[0] + '\nold\n' + installer.LEGACY_MARKERS[1] + '\nUser prose'
        converted = installer.managed_block(legacy, begin, end, 'new', legacy=True)
        self.assertIn('User prose', converted)
        self.assertNotIn(installer.LEGACY_MARKERS[0], converted)

    def test_package_validation_checks_identity_duplicates_and_actual_compilation(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            runtime = package / '.ai/runtime'
            runtime.mkdir(parents=True)
            installer.validate_package(package)
            skill = package / '.ai/skills/first/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: first\ndescription: First role\n---\nBody')
            module = runtime / 'example.py'
            module.write_text('"""Temporary qualification fixture."""\nVALUE = 1\n')
            installer.validate_package(package)
            duplicate = package / '.ai/skills/second/SKILL.md'
            duplicate.parent.mkdir(parents=True)
            duplicate.write_text(skill.read_text())
            with self.assertRaisesRegex(SystemExit, 'duplicate skill names'):
                installer.validate_package(package)
            duplicate.write_text('Body without identity')
            with self.assertRaisesRegex(SystemExit, 'missing skill identity'):
                installer.validate_package(package)
            duplicate.write_text('---\nname: second\ndescription: Second role\n---\nBody')
            module.write_text('def invalid syntax\n')
            with self.assertRaisesRegex(SystemExit, 'python compile failed'):
                installer.validate_package(package)


def test_optional_discovery_prints_full_report_and_failure_streams(capsys):
    from unittest.mock import patch
    import subprocess
    report = {'capabilities': {'setup_notices': ['Optional renderer setup']},
              'tools': {'office': {'status': 'UNAVAILABLE', 'reason': 'TimeoutExpired'}},
              'environment': {'path': '/fixture/bin'}}
    with patch.object(installer.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(report), 'native warning')) as run:
        installer.optional_discovery(Path('/fixture/house'))
    output = capsys.readouterr().out
    assert 'TimeoutExpired' in output and '/fixture/bin' in output
    assert 'Optional renderer setup' in output and 'native warning' in output
    assert run.call_args.kwargs['timeout'] >= 125
    with patch.object(installer.subprocess, 'run', side_effect=subprocess.TimeoutExpired('configure', 150, output=b'partial JSON', stderr=b'load failure')):
        installer.optional_discovery(Path('/fixture/house'))
    output = capsys.readouterr().out
    assert 'TimeoutExpired' in output and 'partial JSON' in output and 'load failure' in output


def test_shell_installer_selects_explicit_python_and_preserves_path(tmp_path):
    import os
    import shutil
    import subprocess
    interpreter = tmp_path / 'selected python'
    interpreter.write_text('#!/bin/sh\nprintf "%s\\n" "$PATH" "$@"\nexit 23\n')
    interpreter.chmod(0o755)
    environment = dict(os.environ, JAI_PYTHON=str(interpreter), PATH='/fixture/bin:/usr/bin:/bin')
    result = subprocess.run([shutil.which('bash'), str(ROOT / 'install.sh'), '--dry-run'],
                            env=environment, capture_output=True, text=True)
    assert result.returncode == 23
    assert result.stdout.splitlines() == [environment['PATH'], str(ROOT / '.ai/setup/installer.py'), '--dry-run']


def test_bare_python_installs_without_third_party_packages_and_reports_runtime_dependency(tmp_path):
    import os
    import subprocess
    environment=dict(os.environ, HOME=str(tmp_path/'home'),
                     AI_IT_HOME=str(tmp_path/'home/.ai'),
                     AI_IT_HOUSE=str(tmp_path/'home/.ai/it-role-house'),
                     CODEX_HOME=str(tmp_path/'home/.codex'), CLAUDE_HOME=str(tmp_path/'home/.claude'),
                     PATH=os.defpath)
    command=[sys.executable,'-S',str(ROOT/'.ai/setup/installer.py'),'--codex-only']
    dry=subprocess.run([*command,'--dry-run'],env=environment,capture_output=True,text=True,timeout=30)
    assert dry.returncode==0, dry.stdout+dry.stderr
    assert 'nothing written' in dry.stdout
    assert not (tmp_path/'home').exists()
    installed=subprocess.run(command,env=environment,capture_output=True,text=True,timeout=150)
    assert installed.returncode==0, installed.stdout+installed.stderr
    assert (tmp_path/'home/.ai/it-role-house/install-state.json').is_file()
    assert 'Installation/update complete.' in installed.stdout
    assert 'installation complete; runtime dependency jsonschema>=4.26,<5 is missing' in installed.stdout
    assert '"available": false' in installed.stdout
    assert 'Traceback' not in installed.stdout+installed.stderr
    assert '"no_site": true' in installed.stdout


@pytest.mark.parametrize('platform,ready,expected',[('darwin',False,True),('darwin',True,False),('linux',False,False),('win32',False,False)])
def test_runtime_setup_completion_limits_macos_venv_commands_to_missing_dependency(tmp_path,capsys,platform,ready,expected):
    from unittest.mock import patch
    capabilities={'runtime_dependencies':{'jsonschema':{'available':ready,'compatible':ready}}}
    with patch.object(installer.sys,'platform',platform), patch.object(installer.Path,'home',return_value=tmp_path/'home with space'):
        installer.runtime_setup_instructions(tmp_path/'house with space',capabilities)
    output=capsys.readouterr().out
    assert ('-m venv' in output)==expected
    if expected:
        assert "-m pip install 'jsonschema>=4.26,<5'" in output
        assert 'operator_actions.py' in output and 'configure --refresh' in output
        assert 'PATH=' in output and 'codex' in output and 'claude' in output
        assert 'does not persist' in output
    elif not ready:
        assert 'jsonschema>=4.26,<5' in output


@pytest.mark.parametrize('discovery',['success','doctor-unavailable','timeout'])
def test_main_prints_macos_runtime_setup_after_all_diagnostics_and_codex_notice(tmp_path,monkeypatch,capsys,discovery):
    import importlib.metadata
    import subprocess
    from unittest.mock import patch
    for key,value in {'HOME':tmp_path/'home with space','AI_IT_HOME':tmp_path/'home with space/.ai','AI_IT_HOUSE':tmp_path/'home with space/.ai/it-role-house','CODEX_HOME':tmp_path/'home with space/.codex','CLAUDE_HOME':tmp_path/'home with space/.claude'}.items():
        monkeypatch.setenv(key,str(value))
    real_run=subprocess.run
    def run(command,**kwargs):
        if 'configure' not in command:return real_run(command,**kwargs)
        if discovery=='timeout':raise subprocess.TimeoutExpired(command,150,stderr=b'optional renderer timeout')
        capabilities=({'runtime_dependencies':{'jsonschema':{'available':True,'compatible':False}}}
                      if discovery=='success' else {'status':'UNAVAILABLE','reason':'doctor failed'})
        return subprocess.CompletedProcess(command,0,json.dumps({'capabilities':capabilities,'tools':{}}),'')
    with patch.object(installer.sys,'argv',['installer.py','--codex-only']), patch.object(installer.sys,'platform','darwin'), patch.object(installer.subprocess,'run',side_effect=run), patch('importlib.util.find_spec',return_value=True), patch.object(importlib.metadata,'version',return_value='4.23.0'):
        assert installer.main()==0
    output=capsys.readouterr().out
    assert (tmp_path/'home with space/.ai/it-role-house/install-state.json').is_file()
    assert output.index('Runtime setup required:')>output.index('Codex: review/approve')
    assert output.index('Runtime setup required:')>output.index('Refresh optional capabilities with:')
    assert output.rstrip().endswith('for GUI sessions, use an environment with the same PATH.')
    assert "-m pip install 'jsonschema>=4.26,<5'" in output


@pytest.mark.parametrize('state',['unknown','ready'])
def test_main_uses_independent_runtime_observation_after_doctor_failure(tmp_path,monkeypatch,capsys,state):
    import subprocess
    from unittest.mock import patch
    for key,value in {'HOME':tmp_path/'home','AI_IT_HOME':tmp_path/'home/.ai','AI_IT_HOUSE':tmp_path/'home/.ai/it-role-house','CODEX_HOME':tmp_path/'home/.codex','CLAUDE_HOME':tmp_path/'home/.claude'}.items():
        monkeypatch.setenv(key,str(value))
    real_run=subprocess.run
    def run(command,**kwargs):
        if 'configure' in command:raise subprocess.TimeoutExpired(command,150)
        return real_run(command,**kwargs)
    observed={'status':state,'available':True if state=='ready' else None,'compatible':True if state=='ready' else None}
    with patch.object(installer.sys,'argv',['installer.py','--codex-only']), patch.object(installer.sys,'platform','darwin'), patch.object(installer.subprocess,'run',side_effect=run), patch.object(installer,'jsonschema_status',return_value=observed):
        assert installer.main()==0
    output=capsys.readouterr().out
    if state=='ready':
        assert '-m venv' not in output
        assert output.rstrip().endswith('Codex: review/approve the installed hook configuration in Codex before relying on enforcement.')
    else:
        assert output.index('Runtime readiness NOT VERIFIED:')>output.index('Codex: review/approve')
        assert 'Runtime setup required:' not in output
        assert 'does not mean the package is missing' in output
        assert output.index('verify first')<output.index('-m venv')
        assert output.rstrip().endswith('for GUI sessions, use an environment with the same PATH.')
