"""Filesystem regressions for offline scenario exercises."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / '.ai/runtime/demo/scenario_demo.py'


def engine():
    spec = importlib.util.spec_from_file_location('scenario_demo', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def catalog(tmp_path, **changes):
    entry = dict(id='proposal', title='ACME proposal', guide='examples/proposal.md',
                 project_name='acme-proposal', inputs=[dict(path='inputs/request.md', content='Fictional ACME request')],
                 steps=[dict(title='Understand', why='Establish scope', claude='/analyse .',
                             codex='$workflow-analyse .', inspect='Review scope and missing evidence')])
    entry.update(changes)
    path = tmp_path / 'catalog.json'
    path.write_text(json.dumps(dict(schema_version=1, entries=[entry])))
    return path


def test_creates_inputs_and_paired_unexecuted_guidance_without_overwrite(tmp_path):
    mod = engine()
    entries = mod.load_catalog(catalog(tmp_path))
    dst = tmp_path / 'exercise'
    mod.create_scenario(entries, 'proposal', dst)
    assert (dst / 'inputs/request.md').read_text() == 'Fictional ACME request'
    start = (dst / 'START.md').read_text()
    assert '/analyse .' in start and '$workflow-analyse .' in start
    assert 'NOT_EXECUTED' in start and 'fictional' in start
    with pytest.raises(ValueError, match='exists'):
        mod.create_scenario(entries, 'proposal', dst)
    assert not (dst / '.fabric').exists()


@pytest.mark.parametrize('bad', ['../escape.md', '/tmp/escape.md', 'inputs/../escape.md', 'inputs\\escape.md', 'START.md'])
def test_invalid_catalog_paths_fail_before_creation(tmp_path, bad):
    with pytest.raises(ValueError):
        engine().load_catalog(catalog(tmp_path, inputs=[dict(path=bad, content='bad')]))


def test_reset_preserves_all_prior_work_and_rejects_wrong_marker(tmp_path):
    mod = engine()
    entries = mod.load_catalog(catalog(tmp_path))
    dst = tmp_path / 'exercise'
    mod.create_scenario(entries, 'proposal', dst)
    (dst / 'my-work.md').write_text('Keep my work')
    backup = mod.reset_scenario(entries, 'proposal', dst)
    assert (backup / 'my-work.md').read_text() == 'Keep my work'
    assert not (dst / 'my-work.md').exists()
    (dst / '.jai-scenario.json').write_text('{}')
    with pytest.raises(ValueError, match='marker'):
        mod.reset_scenario(entries, 'proposal', dst)
    assert dst.exists()


def test_symlink_destination_or_ancestor_is_rejected(tmp_path):
    mod = engine()
    entries = mod.load_catalog(catalog(tmp_path))
    real = tmp_path / 'real'
    real.mkdir()
    link = tmp_path / 'link'
    link.symlink_to(real, target_is_directory=True)
    for dst in (link, link / 'exercise'):
        with pytest.raises(ValueError, match='symlink'):
            mod.create_scenario(entries, 'proposal', dst)
    assert not (real / 'exercise').exists()


def test_unknown_id_and_step_fail_read_only(tmp_path):
    mod = engine()
    entries = mod.load_catalog(catalog(tmp_path))
    with pytest.raises(ValueError, match='Unknown'):
        mod.describe_scenario(entries, 'unknown')
    with pytest.raises(ValueError, match='step'):
        mod.describe_scenario(entries, 'proposal', 2)
    assert 'Understand' in mod.describe_scenario(entries, 'proposal', 1)


def test_installed_runtime_works_without_docs_and_legacy_list_remains(tmp_path):
    runtime = tmp_path / 'runtime'
    shutil.copytree(ROOT / '.ai/runtime/demo', runtime / 'demo')
    script = runtime / 'demo/demo.py'
    result = subprocess.run([sys.executable, str(script), 'check-scenarios'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert '29' in result.stdout
    result = subprocess.run([sys.executable, str(script), 'list'], capture_output=True, text=True)
    assert result.returncode == 0
    assert all(name in result.stdout for name in ('invoice-service', 'policy-docs', 'acme-pay'))


def legacy():
    spec = importlib.util.spec_from_file_location('legacy_demo', ROOT / '.ai/runtime/demo/demo.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_legacy_setup_list_reset_and_git_history(tmp_path, capsys):
    from argparse import Namespace
    mod = legacy()
    args = Namespace(to=str(tmp_path), force=False)
    mod.cmd_list(args)
    assert 'invoice-service' in capsys.readouterr().out
    mod.cmd_setup(args)
    assert (tmp_path / 'invoice-service/app/invoices.py').is_file()
    assert mod.git(str(tmp_path / 'invoice-service'), 'log', '--oneline').returncode == 0
    with pytest.raises(SystemExit):
        mod.cmd_setup(args)
    (tmp_path / 'policy-docs/temporary.md').write_text('temporary exercise')
    mod.cmd_reset(Namespace(to=str(tmp_path), name='policy-docs'))
    assert not (tmp_path / 'policy-docs/temporary.md').exists()
    assert Path(mod.copy_project('policy-docs', str(tmp_path))).is_dir()
    mod.history(str(tmp_path / 'invoice-service'))
    assert mod.git(str(tmp_path / 'invoice-service'), 'status', '--porcelain').returncode == 0
    assert mod.run_tool('-c', 'print("offline")').stdout.strip() == 'offline'
    assert mod.cmd_check(Namespace()) == 0


@pytest.mark.parametrize('change', [dict(id='Bad ID'), dict(guide='../outside.md'),
                                  dict(project_name='../outside'), dict(steps=[]),
                                  dict(inputs=[dict(path='inputs/a', content='x'),
                                               dict(path='inputs/a/b', content='y')])])
def test_invalid_catalog_metadata_is_rejected(tmp_path, change):
    with pytest.raises(ValueError):
        engine().load_catalog(catalog(tmp_path, **change))


def test_cli_dispatch_errors_and_step_inspection_are_read_only(tmp_path):
    script = ROOT / '.ai/runtime/demo/demo.py'
    entries = engine().load_catalog()
    entry = entries[0]
    result = subprocess.run([sys.executable, str(script), 'describe', entry['id'], '--step', '1'],
                            capture_output=True, text=True)
    assert result.returncode == 0 and entry['steps'][0]['title'] in result.stdout
    assert 'NOT_EXECUTED' in result.stdout
    result = subprocess.run([sys.executable, str(script), 'scenario', 'unknown', '--to', str(tmp_path / 'new')],
                            capture_output=True, text=True)
    assert result.returncode == 2 and 'Unknown' in result.stdout
    assert not (tmp_path / 'new').exists()


@pytest.mark.parametrize('reserved', ['.git', '.fabric', '.findings'])
def test_reserved_destination_is_rejected_before_write(tmp_path, reserved):
    mod = engine()
    entries = mod.load_catalog(catalog(tmp_path))
    with pytest.raises(ValueError, match='Unsafe'):
        mod.create_scenario(entries, 'proposal', tmp_path / reserved)
    assert not (tmp_path / reserved).exists()


def test_symlink_catalog_is_rejected(tmp_path):
    mod = engine()
    link = tmp_path / 'link.json'
    link.symlink_to(catalog(tmp_path))
    with pytest.raises(ValueError, match='symlink'):
        mod.load_catalog(link)


def test_reset_rejects_boolean_marker_version_without_mutation(tmp_path):
    mod = engine()
    entries = mod.load_catalog(catalog(tmp_path))
    dst = tmp_path / 'exercise'
    mod.create_scenario(entries, 'proposal', dst)
    marker = dst / '.jai-scenario.json'
    data = json.loads(marker.read_text())
    data['schema_version'] = True
    marker.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='marker'):
        mod.reset_scenario(entries, 'proposal', dst)
    assert marker.exists()
    assert not list(tmp_path.glob('exercise.backup-*'))


@pytest.mark.parametrize('label', ['bad', "'bad'"])
def test_git_first_bad_commit_output_compatibility(label):
    spec = importlib.util.spec_from_file_location('defect_demo_compat', ROOT / '.ai/runtime/tools/defect.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sha = 'a' * 40
    assert module._first_bad_commit(f"{sha} is the first {label} commit\ncommit {sha}\n") == sha
    assert module._first_bad_commit('Bisecting: 1 revision left') is None


def test_all_29_catalog_exercises_materialize_exact_inputs_and_steps(tmp_path):
    mod = engine()
    entries = mod.load_catalog()
    assert len(entries) == 29
    assert len({entry['id'] for entry in entries}) == 29
    for entry in entries:
        dst = mod.create_scenario(entries, entry['id'], tmp_path / entry['id'])
        for item in entry['inputs']:
            assert (dst / item['path']).read_text(encoding='utf-8') == item['content']
        start = (dst / 'START.md').read_text(encoding='utf-8')
        assert entry['guide'] in start
        for step in entry['steps']:
            assert step['claude'] in start and step['codex'] in start
        assert 'NOT_EXECUTED' in start
