# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Provider harness boundary tests use only disposable fake executables."""
import copy
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import optional_provider_eval as provider


def fake_cli(tmp_path, body):
    path = tmp_path / 'fake-provider'
    path.write_text('#!' + sys.executable + '\nimport sys, json\n' + body)
    path.chmod(0o755)
    return str(path)


def plan():
    return provider.prepare_plan(ROOT, 'codex', 'adr', 1, 'fake-model')


def test_preflight_and_plan_never_execute_cli_or_read_credentials():
    with patch.object(provider.subprocess, 'Popen', side_effect=AssertionError('no inference')):
        record = provider.preflight('codex', 'jai-nonexistent-provider')
        assert record['state'] == 'UNAVAILABLE'
        result = plan()
        assert result['invocations'] == 1
        assert result['classification'] == 'public-synthetic'
        assert not result['live_execution']
    with pytest.raises(ValueError):
        provider.preflight('unrecognized')
    for count in (0, 4, True):
        with pytest.raises(ValueError):
            provider.prepare_plan(ROOT, 'codex', 'adr', count)


def test_run_requires_consent_exact_budget_explicit_model_and_unchanged_plan():
    selected = plan()
    for consent, budget in ((False, 1), (True, 0), (True, True)):
        with pytest.raises(ValueError):
            provider.run_plan(ROOT, selected, consent, budget)
    changed = copy.deepcopy(selected)
    changed['cases'][0]['reference_hash'] = '0' * 64
    with pytest.raises(ValueError):
        provider.run_plan(ROOT, changed, True, 1)
    with pytest.raises(ValueError):
        provider.run_plan(ROOT, provider.prepare_plan(ROOT, 'codex', 'adr', 1), True, 1)
    for timeout in (0, -1, float('nan'), float('inf'), True, 3601):
        with pytest.raises(ValueError):
            provider.run_plan(ROOT, selected, True, 1, timeout=timeout)


def test_fake_process_records_metadata_without_transcripts_or_credentials(tmp_path):
    executable = fake_cli(tmp_path, """
if '--version' in sys.argv:
    print('fake codex 1.2.3')
else:
    assert sys.argv[1:5] == ['exec', '--json', '--skip-git-repo-check', '--model']
    print(json.dumps({'output':'PRIVATE RESPONSE api_key=secret-value', 'model':'actual-model',
                      'usage':{'input_tokens':7,'output_tokens':3,'private':'secret-value'}}))
""")
    result = provider.run_plan(ROOT, plan(), True, 1, executable=executable)
    assert result['state'] == 'COMPLETED'
    assert result['cli_version'] == '1.2.3'
    assert result['runs'][0]['observed_model'] == 'actual-model'
    assert result['runs'][0]['usage'] == {'input_tokens': 7, 'output_tokens': 3}
    assert 'secret-value' not in json.dumps(result)
    assert str(tmp_path) not in json.dumps(result)
    assert provider.inspect_report(result)['metrics']['state'] == 'not-measurable'
    result['runs'][0]['exit_code'] = 19
    with pytest.raises(ValueError):
        provider.inspect_report(result)


def test_fake_claude_arguments_and_unknown_model_are_reported_honestly(tmp_path):
    executable = fake_cli(tmp_path, """
if '--version' in sys.argv:
    print('unknown version')
else:
    assert sys.argv[1:6] == ['--print','--output-format','json','--model','fake-model']
    print(json.dumps({'result':'A fictional result'}))
""")
    result = provider.run_plan(ROOT, provider.prepare_plan(ROOT, 'claude', 'adr', 1, 'fake-model'),
                               True, 1, executable=executable)
    assert result['state'] == 'COMPLETED'
    assert result['cli_version'] is None
    assert result['runs'][0]['observed_model'] is None


@pytest.mark.parametrize('body,expected', [
    ("print('malformed')", 'INVALID_OUTPUT'),
    ("print(json.dumps({'output':''}))", 'INVALID_OUTPUT'),
    ("sys.stderr.write('secret'); sys.exit(2)", 'FAILED')])
def test_fake_provider_failures_never_pass_or_leak(tmp_path, body, expected):
    executable = fake_cli(tmp_path, "if '--version' in sys.argv: print('1.0.0')\nelse:\n " + body)
    result = provider.run_plan(ROOT, plan(), True, 1, executable=executable)
    assert result['state'] == expected
    assert len(result['runs']) == 1
    assert 'secret' not in json.dumps(result)


def test_timeout_cancels_real_fake_subprocess_and_does_not_retry(tmp_path):
    executable = fake_cli(tmp_path, """
if '--version' in sys.argv: print('1.0.0')
else:
    import threading
    threading.Event().wait(30)
""")
    result = provider.run_plan(ROOT, plan(), True, 1, timeout=.05, executable=executable)
    assert result['state'] == 'TIMEOUT'
    assert len(result['runs']) == 1


def test_keyboard_interrupt_terminates_process_group(tmp_path):
    executable = fake_cli(tmp_path, "import threading\nthreading.Event().wait(30)")
    original = subprocess.Popen.communicate
    calls = []
    def interrupt_once(process, *args, **kwargs):
        calls.append(process)
        if len(calls) == 1:
            raise KeyboardInterrupt
        return original(process, *args, **kwargs)
    with patch.object(provider.subprocess.Popen, 'communicate', interrupt_once):
        record = provider._capture([executable], 2, tmp_path)
    assert record['state'] == 'CANCELLED'
    assert calls[0].poll() is not None


def test_missing_cli_is_unavailable_not_pass():
    result = provider.run_plan(ROOT, plan(), True, 1, executable='jai-nonexistent-provider')
    assert result['state'] == 'UNAVAILABLE'
    assert result['runs'] == []
    assert not result['professional_approval']


def test_untrusted_observed_metadata_cannot_expose_absolute_paths():
    parsed = provider._observed(json.dumps({'output': 'result', 'model': '/private/customer/model',
                                          'usage': {'input_tokens': True, 'secret': 'hidden'}}))
    assert parsed['valid']
    assert parsed['model'] is None
    assert parsed['usage'] == {}


@pytest.mark.parametrize('family,expected', [('strategy','it-digital-strategy'), ('client-proposal','client-proposal'), ('managed-security-services-proposal','managed-security-services-proposal'), ('software-engineering-plan','software-engineering-plan'), ('api-interface-contract','api-interface-contract'), ('release-readiness-review','release-readiness-review'), ('transformation-baseline-assessment','transformation-baseline-assessment'), ('target-operating-model','target-operating-model'), ('transformation-execution-plan','transformation-execution-plan'), ('security-architecture-assessment','security-architecture-assessment'), ('threat-model','threat-model'), ('security-control-assessment','security-control-assessment'), ('devsecops-pipeline-design','devsecops-pipeline-design'), ('cicd-pipeline-assurance','cicd-pipeline-assurance'), ('appsec-verification-report','appsec-verification-report'), ('software-supply-chain-assessment','software-supply-chain-assessment')])
def test_plan_supports_mapped_and_proposed_families_without_inference(family, expected):
    """Expanded bundled families reuse actual registered specs, never guessed IDs."""
    with patch.object(provider.subprocess, 'Popen', side_effect=AssertionError('no inference')):
        record = provider.prepare_plan(ROOT, 'codex', family, 1, 'fake-model')
    assert record['family'] == expected
    assert record['classification'] == 'public-synthetic'
    assert record['invocations'] == 1
    assert record['professional_qualification'] is False
    assert len(record['cases'][0]['compiled_spec_hash']) == 64


def test_prepare_constructs_one_resolver_per_request_and_never_reuses_it():
    import content_spec
    import expert_references
    original = content_spec.ContentSpec
    constructed = []
    def construct(root):
        instance = original(root)
        constructed.append(instance)
        return instance
    with patch.object(content_spec, 'ContentSpec', side_effect=construct), patch.object(expert_references, 'ContentSpec', side_effect=construct):
        first = plan()
        assert len(constructed) == 1
        second = plan()
        assert len(constructed) == 2
    assert first == second
    assert len(constructed) == 2
    assert constructed[0] is not constructed[1]
    assert all(instance.root == ROOT for instance in constructed)


def test_registry_changes_are_observed_by_next_prepare_and_run_revalidation(tmp_path):
    import shutil
    runtime = tmp_path / 'runtime'
    shutil.copytree(ROOT / '.ai/runtime/content', runtime / 'content')
    selected = provider.prepare_plan(runtime, 'codex', 'adr', 1, 'fake-model')
    registry = runtime / 'content/registry.json'
    metadata = json.loads(registry.read_text())
    metadata['schema_version'] = 'unsupported-after-plan'
    registry.write_text(json.dumps(metadata))
    with patch.object(provider.subprocess, 'Popen', side_effect=AssertionError('changed registry must prevent provider execution')):
        with pytest.raises(ValueError):
            provider.prepare_plan(runtime, 'codex', 'adr', 1, 'fake-model')
        with pytest.raises(ValueError):
            provider.run_plan(runtime, selected, True, 1)
