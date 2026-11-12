# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Categories, selection safety and real CLI/pytest marker integration."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('tested_test_selection', ROOT / 'scripts/test_selection.py')
selection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(selection)
RUNNER_SPEC = importlib.util.spec_from_file_location('tested_run_tests', ROOT / 'scripts/run_tests.py')
runner = importlib.util.module_from_spec(RUNNER_SPEC)
sys.path.insert(0, str(ROOT / 'scripts'))
RUNNER_SPEC.loader.exec_module(runner)


@pytest.mark.unit
def test_node_tags_preserve_parameterized_control_and_node_category_overrides():
    catalog = {'modules': {'tests/test_x.py': {'category': 'integration', 'tags': ['slow']}},
               'node_tags': {'tests/test_x.py::test_contract': {'category': 'contract', 'tags': ['control']}}}
    assert selection.tags_for_node(catalog, 'tests/test_x.py::test_contract[negative]') == {'contract', 'control', 'slow'}
    assert selection.tags_for_node(catalog, 'tests/test_x.py::test_contract_else') == {'integration', 'slow'}
    with pytest.raises(ValueError, match='Unclassified'):
        selection.tags_for_node(catalog, 'tests/test_new.py::test_x')


@pytest.mark.integration
def test_catalog_covers_maintained_modules_and_retains_single_full_transport_history():
    catalog = selection.load_catalog(ROOT)
    assert set(selection.maintained_modules(ROOT)) == set(catalog['modules'])
    transport = 'tests/test_governed_transport_layers.py'
    assert catalog['modules'][transport]['category'] == 'e2e'
    assert 'slow' in catalog['modules'][transport]['tags']
    assert not any(node.startswith(transport) for node in catalog['control'])
    selectors, _ = runner.python_selection(ROOT, catalog, 'full', [])
    assert selectors.count(transport) == 1
    assert any(path.startswith('apps/') for path in selectors)
    assert any('expired_new_request' in node for node in catalog['control'])


@pytest.mark.integration
def test_impact_follows_transitive_imports_and_fixture_consumers_and_unknown_falls_back(tmp_path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'scripts/core.py').write_text('VALUE = 1\n')
    (tmp_path / 'scripts/consumer.py').write_text('import core\n')
    (tmp_path / 'tests/shared.py').write_text('import consumer\n')
    (tmp_path / 'tests/test_a.py').write_text('from shared import fixture\n')
    (tmp_path / 'tests/test_b.py').write_text('def test_b(): assert True\n')
    catalog = {'modules': {'tests/test_a.py': {}, 'tests/test_b.py': {}}, 'impact_rules': []}
    assert selection.select_impacted(tmp_path, catalog, ['scripts/core.py'])[0] == ['tests/test_a.py']
    assert selection.select_impacted(tmp_path, catalog, ['tests/shared.py'])[0] == ['tests/test_a.py']
    assert selection.select_impacted(tmp_path, catalog, ['tests/test_b.py'])[0] == ['tests/test_b.py']
    for changed in ('scripts/deleted_unknown.py', 'docs/new.md', 'tests/test_new.py'):
        selected, reason = selection.select_impacted(tmp_path, catalog, [changed])
        assert set(selected) == set(catalog['modules'])
        assert 'Unknown impact' in reason
    assert selection.select_impacted(tmp_path, catalog, [])[0] == []
    with pytest.raises(ValueError, match='escapes'):
        selection.select_impacted(tmp_path, catalog, ['../outside.py'])


@pytest.mark.integration
def test_impact_explicit_resource_rules_add_to_import_consumers(tmp_path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests/test_a.py').write_text('def test_a(): assert True\n')
    catalog = {'modules': {'tests/test_a.py': {}}, 'impact_rules': [
        {'paths': ['schema/**'], 'tests': ['tests/test_a.py']}]}
    selected, reason = selection.select_impacted(tmp_path, catalog, ['schema/deleted.json'])
    assert selected == ['tests/test_a.py']
    assert 'Explicit' in reason


@pytest.mark.integration
def test_changed_paths_capture_staged_unstaged_untracked_and_bad_revision(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    (tmp_path / 'first.py').write_text('before')
    subprocess.run(['git', 'add', '.'], cwd=tmp_path, check=True)
    subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                    'commit', '-qm', 'baseline'], cwd=tmp_path, check=True)
    assert selection.changed_paths(tmp_path) == []
    (tmp_path / 'first.py').write_text('after')
    (tmp_path / 'untracked.py').write_text('new')
    assert selection.changed_paths(tmp_path) == ['first.py', 'untracked.py']
    subprocess.run(['git', 'add', 'first.py'], cwd=tmp_path, check=True)
    assert selection.changed_paths(tmp_path, 'HEAD') == ['first.py', 'untracked.py']
    with pytest.raises(ValueError, match='baseline'):
        selection.changed_paths(tmp_path, 'revision-does-not-exist')


@pytest.mark.integration
def test_real_cli_dry_plan_is_bounded_and_rejects_invalid_combinations():
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_tests.py'), '--profile', 'control',
                             '--scope', 'python', '--list'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    command = json.loads(result.stdout.splitlines()[-1])
    assert command[:4] == [sys.executable, '-u', '-m', 'pytest']
    assert all('::' in token for token in command if token.startswith(('tests/', 'apps/')))
    assert len(command) < 60
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/run_tests.py'), '--scope', 'python',
                             '--changed', 'tests/test_prepublish.py'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 2
    assert 'require --profile development' in result.stderr


@pytest.mark.integration
def test_native_pytest_marker_selection_and_explicit_decorator_override():
    command = [sys.executable, '-m', 'pytest', '--collect-only', '-q', '-m', 'control',
               'apps/fabric-explorer/reader/test/test_wire_json.py']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'test_fact_budget_counts_exact_utf8_bytes_at_boundary' in result.stdout
    assert 'test_fact_json_uses_utf8_without_changing_cross_language_values[' not in result.stdout
    result = subprocess.run([sys.executable, '-m', 'pytest', '--collect-only', '-q', '-m', 'unit',
                             'tests/test_test_selection.py'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'test_node_tags_preserve_parameterized_control' in result.stdout
    assert 'test_impact_follows_transitive' not in result.stdout


@pytest.mark.unit
@pytest.mark.parametrize('status', [0, 1, 5])
def test_runner_preserves_failed_and_empty_selection_status(monkeypatch, status):
    observed = []
    def run(command, *, cwd):
        observed.append(command)
        return subprocess.CompletedProcess(command, status)
    monkeypatch.setattr(runner.subprocess, 'run', run)
    assert runner.main(['--scope', 'python', '--profile', 'control']) == status
    assert len(observed) == 1


@pytest.mark.integration
def test_invalid_catalog_rejects_unknown_category_and_escaping_path(tmp_path):
    (tmp_path / 'ci').mkdir()
    baseline = {'version': 1, 'modules': {'tests/test_a.py': {'category': 'unit'}}}
    for path, category in [('tests/test_a.py', 'unknown'), ('../test_a.py', 'unit')]:
        data = copy.deepcopy(baseline)
        data['modules'] = {path: {'category': category}}
        (tmp_path / 'ci/test-catalog.json').write_text(json.dumps(data))
        with pytest.raises(ValueError):
            selection.load_catalog(tmp_path)


@pytest.mark.unit
def test_development_without_changed_inputs_executes_no_test_subprocess(monkeypatch):
    monkeypatch.setattr(runner.test_selection, 'changed_paths', lambda root, base: [])
    monkeypatch.setattr(runner.subprocess, 'run', lambda *args, **kwargs: pytest.fail('No tests should execute'))
    assert runner.main(['--profile', 'development']) == 0


@pytest.mark.integration
def test_catalog_rejects_unmapped_impact_consumers(tmp_path):
    (tmp_path / 'ci').mkdir()
    (tmp_path / 'ci/test-catalog.json').write_text(json.dumps({
        'version': 1, 'modules': {'tests/test_a.py': {'category': 'unit'}},
        'impact_rules': [{'paths': ['schema/**'], 'tests': ['tests/test_missing.py']}]}))
    with pytest.raises(ValueError, match='Invalid impact rule'):
        selection.load_catalog(tmp_path)


@pytest.mark.unit
def test_pytest_collection_modifyitems_preserves_override_and_rejects_conflicting_categories():
    spec = importlib.util.spec_from_file_location('tested_pytest_hook', ROOT / 'conftest.py')
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    class Item:
        path = ROOT / 'tests/test_runtime_dependencies.py'
        nodeid = 'tests/test_runtime_dependencies.py::test_case'
        def __init__(self, marks):
            self.marks = marks
            self.added = []
        def iter_markers(self):
            return iter(self.marks)
        def add_marker(self, mark):
            self.added.append(mark)
    overridden = Item([pytest.mark.contract.mark])
    plugin.pytest_collection_modifyitems(None, [overridden])
    assert not ({mark.name for mark in overridden.added} & selection.CATEGORIES)
    plain = Item([])
    plugin.pytest_collection_modifyitems(None, [plain])
    assert 'unit' in {mark.name for mark in plain.added}
    plugin.pytest_collection_modifyitems(None, [])
    conflicting = Item([pytest.mark.contract.mark, pytest.mark.unit.mark])
    with pytest.raises(pytest.UsageError, match='conflicting category'):
        plugin.pytest_collection_modifyitems(None, [conflicting])
    unknown = Item([])
    unknown.path = ROOT / 'tests/test_not_catalogued.py'
    unknown.nodeid = 'tests/test_not_catalogued.py::test_case'
    with pytest.raises(pytest.UsageError, match='Unclassified maintained test'):
        plugin.pytest_collection_modifyitems(None, [unknown])
    outside = Item([])
    outside.path = Path('/tmp/not-this-checkout.py')
    plugin.pytest_collection_modifyitems(None, [outside])
    assert outside.added == []


@pytest.mark.integration
def test_runtime_impact_includes_app_example_corpus_and_qualification_consumers():
    catalog = selection.load_catalog(ROOT)
    lifecycle_tests, _ = selection.select_impacted(ROOT, catalog, ['.ai/runtime/tools/lifecycle.py'])
    assert {
        'apps/fabric-explorer/benchmarks/test/test_corpus.py',
        'apps/fabric-explorer/examples/test_public_workflows.py',
    } <= set(lifecycle_tests)
    findings_tests, _ = selection.select_impacted(ROOT, catalog, ['.ai/runtime/tools/findings.py'])
    assert 'apps/fabric-explorer/benchmarks/test/test_corpus.py' in findings_tests
    qualification_tests, _ = selection.select_impacted(ROOT, catalog, ['apps/fabric-explorer/qualification/trace.py'])
    assert 'apps/fabric-explorer/qualification/test/test_trace.py' in qualification_tests
    assert len(qualification_tests) < len(catalog['modules'])


@pytest.mark.integration
def test_app_impact_graph_excludes_dependency_build_and_private_trees(tmp_path):
    (tmp_path / 'apps/demo/test').mkdir(parents=True)
    (tmp_path / 'apps/demo/source.py').write_text('VALUE = 1\n')
    (tmp_path / 'apps/demo/test/test_source.py').write_text('import source\n')
    for excluded in ('node_modules', 'build', 'INBOX'):
        directory = tmp_path / 'apps/demo' / excluded
        directory.mkdir()
        (directory / 'test_secret.py').write_text('import source\n')
    graph = selection._source_graph(tmp_path)
    assert 'apps/demo/source.py' in graph
    assert 'apps/demo/test/test_source.py' in graph
    assert not any(part in path.split('/') for path in graph for part in ('node_modules', 'build', 'INBOX'))


@pytest.mark.integration
def test_observed_expensive_cases_are_slow_and_controls_remain_bounded():
    catalog = selection.load_catalog(ROOT)
    nodes = [
        'tests/test_governed_native_batches.py::test_layered_complete_local_triads_and_adjacent_receiving_without_bookkeeping_models',
        'tests/test_governed_sabsa_integrated.py::test_one_governed_sabsa_engagement_traces_all_six_layers_and_renders_its_exact_current_output',
        'tests/test_content_eval.py::ContentEvalTests::test_every_registered_dimension_has_actual_three_way_evaluation',
        'tests/test_content_workflow.py::test_every_handoff_executes_positive_and_missing_receiver_or_authority_checks',
        'tests/test_governed_local_layer.py::test_same_local_layer_completes_six_questions_independent_integration_and_receiving',
        'tests/test_governed_transport_layers.py::test_same_history_continues_through_all_six_layer_boundaries',
        'tests/test_governed_domain.py::test_prepared_proposal_handoff_uses_actual_component_provenance_and_current_gates[0]',
        'tests/test_content_calibration.py::test_candidates_derive_three_complexities_per_priority_family',
        'tests/test_governed_dispatch.py::test_real_blocked_or_excessive_process_is_terminated_without_result[sleep]',
        'tests/test_commercial_proposal.py::test_existing_trusted_host_can_project_exact_draft_without_granting_authority',
    ]
    for node in nodes:
        assert 'slow' in selection.tags_for_node(catalog, node), node
    for node in nodes[:2]:
        assert 'e2e' in selection.tags_for_node(catalog, node), node
    for node in catalog['control']:
        assert not selection.tags_for_node(catalog, node) & {'slow', 'e2e'}, node
