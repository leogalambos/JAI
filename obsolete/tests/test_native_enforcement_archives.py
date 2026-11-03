# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Historical native release gates reject active incompatible catalogues early."""
import importlib
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))


@pytest.mark.parametrize('module_name, archived_release', [
    ('native_enforcement_26102', '26.10.2'),
    ('native_enforcement_26103', '26.10.3'),
])
def test_archive_gate_rejects_a_different_release_before_reading_any_catalogue(
        tmp_path, monkeypatch, capsys, module_name, archived_release):
    gate = importlib.import_module(module_name)
    missing_catalogue = tmp_path / 'no-runtime-catalogue'
    monkeypatch.setattr(gate, 'R', missing_catalogue)
    monkeypatch.setattr(gate, 'RELEASE', '26.10.14')
    assert gate.main() == 1
    message = capsys.readouterr().out
    assert 'Unsupported archive-only gate' in message
    assert archived_release in message
    assert '26.10.14' in message
    assert not missing_catalogue.exists()
