# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Exercise the actual Actions version handoff across offline containment."""
from pathlib import Path
import os
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('valid', [True, False])
def test_guarded_tag_step_exports_only_validated_version(tmp_path, valid):
    """The host exports a matching version; invalid tags leave no output."""
    workflow = yaml.safe_load((ROOT / '.github/workflows/release.yml').read_text())
    step = next(step for step in workflow['jobs']['qualification']['steps']
                if step.get('id') == 'version')
    version = (ROOT / 'VERSION').read_text().strip()
    output = tmp_path / 'actions-output'
    output.touch()
    environment = dict(os.environ, GITHUB_OUTPUT=str(output),
                       RELEASE_TAG='release@' + version if valid else 'invalid-tag')
    result = subprocess.run(['bash', '-euo', 'pipefail', '-c', step['run']],
                            cwd=ROOT, env=environment, capture_output=True, text=True,
                            timeout=15)
    if valid:
        assert result.returncode == 0, result.stdout + result.stderr
        assert output.read_text() == f'version={version}\n'
    else:
        assert result.returncode != 0
        assert output.read_text() == ''


def test_archive_step_rejects_empty_version_before_invoking_builders(tmp_path):
    """A missing Actions output must fail before creating any archive."""
    workflow = yaml.safe_load((ROOT / '.github/workflows/release.yml').read_text())
    step = next(step for step in workflow['jobs']['qualification']['steps']
                if step.get('name') == 'Build production ZIP and SHA-256')
    fake = tmp_path / 'python3'
    marker = tmp_path / 'builder-invoked'
    fake.write_text('#!/bin/sh\ntouch "$BUILDER_MARKER"\nexit 81\n')
    fake.chmod(0o755)
    environment = dict(os.environ, RELEASE_VERSION='', BUILDER_MARKER=str(marker),
                       PATH=str(tmp_path) + os.pathsep + os.environ['PATH'])
    result = subprocess.run(['bash', '-euo', 'pipefail', '-c', step['run']],
                            cwd=ROOT, env=environment, capture_output=True, text=True,
                            timeout=15)
    assert result.returncode != 0
    assert 'Missing validated release version' in result.stderr
    assert not marker.exists()
