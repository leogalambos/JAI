# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Offline release orchestration checks; no tag or publication is executed."""
from pathlib import Path
import json

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_publication_requires_release_tag_and_successful_validation_job():
    """A normal push/manual run cannot enter the release publication workflow."""
    source = (ROOT / '.github/workflows/release.yml').read_text()
    workflow = yaml.load(source, Loader=yaml.BaseLoader)
    assert workflow['on'] == {'push': {'tags': ['release@*']}}
    assert workflow['permissions']['contents'] == 'read'
    publish = workflow['jobs']['publish']
    assert publish['needs'] == 'validate'
    assert publish['permissions']['contents'] == 'write'
    validation = workflow['jobs']['validate']
    commands = '\n'.join(step.get('run', '') for step in validation['steps'])
    assert 'validate_release_tag.py --tag "$RELEASE_TAG"' in commands
    assert 'versioning.py check --tag "$RELEASE_TAG"' in commands
    assert 'git merge-base --is-ancestor HEAD refs/remotes/origin/main' in commands
    assert 'git fetch' not in commands
    checkout = next(step for step in validation['steps'] if step.get('uses') == 'actions/checkout@v4')
    assert checkout['with']['fetch-depth'] == '0'
    assert commands.count('license_check.py .') == 1
    assert commands.count('generate_output_contract_docs.py --root . --check') == 1
    assert '-m pytest' not in commands
    assert 'requirements-ci.txt' not in commands
    assert 'apt-get' not in commands
    assert 'setup-qualification' not in source
    assert 'actions/setup-python@v5' in source
    python_setup = next(step for step in validation['steps']
                        if step.get('uses') == 'actions/setup-python@v5')
    assert python_setup['with']['python-version'] == '3.12'
    # A warm runner may download nothing, so publishing must not depend on a
    # cache directory existing for an optional post-job cache-save action.
    assert 'cache' not in python_setup['with']
    assert 'cache-dependency-path' not in python_setup['with']
    assert '-r requirements.txt' in commands
    assert int(validation['timeout-minutes']) <= 10
    assert 'release_bundle.py build --root . --dist dist' in commands
    assert commands.count('tools/generate_content_workflows.py --check') == 1
    source_validation = (ROOT / '.github/workflows/validate-library.yml').read_text()
    assert source_validation.count('tools/generate_content_workflows.py --check') == 1
    assert source_validation.count('generate_output_contract_docs.py --root . --check') == 1
    reference_check = 'tools/generate_reference_completion.py --root . --role-examples --check'
    assert commands.count(reference_check) == 1
    assert source_validation.count(reference_check) == 1
    assert 'release_ga.py' not in source
    assert 'QUALIFICATION-A-H.json' not in source
    publication = '\n'.join(step.get('run', '') for step in publish['steps'])
    assert 'sha256sum -c' in publication
    assert 'gh release view' in publication
    assert '--verify-tag' in publication


def test_current_release_policy_requires_real_sources_not_archived_development_results():
    """The active policy describes the current pipeline and validates structurally."""
    policy = json.loads((ROOT / '.ai/runtime/release/release-policy.json').read_text())
    schema = json.loads((ROOT / '.ai/runtime/schema/contracts/auto-release-policy-v2.schema.json').read_text())
    jsonschema.Draft202012Validator(schema).validate(policy)
    assert set(policy['required_gates']) == {
        'source-contracts', 'local-offline-tests', 'public-documentation', 'archive-integrity'}
    assert 'VERSION' in policy['required_release_files']
    assert not set(policy['required_release_files']) & {
        'VALIDATION.md', 'QUALIFICATION-A-H.json', 'COMPATIBILITY.json', 'PROVENANCE.json'}


def test_pages_build_checks_generated_catalogues_and_runs_on_their_source_changes():
    """Either public publishing path must reject a stale canonical projection."""
    source = (ROOT / '.github/workflows/pages.yml').read_text()
    workflow = yaml.load(source, Loader=yaml.BaseLoader)
    for event in ('push', 'pull_request'):
        paths = workflow['on'][event]['paths']
        for dependency in ('tools/generate_output_contract_docs.py',
                           'tools/generate_workflow_diagrams.py',
                           'tools/content_catalog_definitions.py',
                           'tools/content_reference_definitions.py',
                           'tools/generate_content_catalog.py',
                           'tools/generate_content_workflows.py',
                           'tools/generate_role_output_guidance.py',
                           'tools/generate_reference_completion.py',
                           'tools/extended_reference_definitions.py',
                           'tools/professional_output_refinements.py',
                           'tools/workflow_professional_definitions.py',
                           '.ai/runtime/content/**',
                           '.ai/runtime/artifacts/contracts/**',
                           '.ai/runtime/tools/content_spec.py'):
            assert dependency in paths
    steps = workflow['jobs']['build']['steps']
    commands = '\n'.join(step.get('run', '') for step in steps)
    for generator in ('generate_output_contract_docs.py', 'generate_workflow_diagrams.py'):
        assert commands.count(f'python tools/{generator} --root . --check') == 1
    assert commands.count('python tools/generate_reference_completion.py --root . --role-examples --check') == 1
    assert '-r requirements.txt' in commands
    assert '-r requirements-ci.txt' not in commands
    assert '-m pytest' not in commands
    assert 'continue-on-error' not in source
    setup = next(step for step in steps if step.get('uses') == 'actions/setup-python@v5')
    assert 'cache' not in setup['with']
    assert workflow['jobs']['deploy']['needs'] == 'build'


def test_release_ancestry_uses_checkout_history_without_network_or_remote_credentials(tmp_path):
    import subprocess
    root = tmp_path / 'ancestry-checkout'
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(root)], check=True)
    def git(*args, check=True):
        return subprocess.run(['git', *args], cwd=root, check=check, capture_output=True, text=True)
    (root / 'source').write_text('baseline')
    git('add', 'source')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'main baseline')
    git('remote', 'add', 'origin', 'ssh://unusable.invalid/never-contact-this-repository')
    git('update-ref', 'refs/remotes/origin/main', 'HEAD')
    workflow = yaml.load((ROOT / '.github/workflows/release.yml').read_text(), Loader=yaml.BaseLoader)
    guard = next(step['run'] for step in workflow['jobs']['validate']['steps']
                 if step.get('name') == 'Require the tagged source on main')
    assert guard.strip().splitlines() == [
        'set -eu', 'git merge-base --is-ancestor HEAD refs/remotes/origin/main']
    def check_guard():
        return subprocess.run(['bash', '-c', guard], cwd=root, capture_output=True, text=True).returncode
    assert check_guard() == 0
    (root / 'source').write_text('unmerged candidate')
    git('add', 'source')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'unmerged candidate')
    assert check_guard() == 1
    git('update-ref', '-d', 'refs/remotes/origin/main')
    assert check_guard() != 0
