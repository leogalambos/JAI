# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""CI partition coverage must be complete without repeating Gate A modules."""
import importlib.util
from pathlib import Path
import tempfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('ci_test_plan', ROOT / 'scripts/ci_test_plan.py')
plan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plan)


def test_full_partition_covers_every_test_exactly_once():
    supplementary = set(plan.select_tests('supplementary'))
    gate_a = {'tests/' + name for name in plan.REGRESSION_MODULES}
    all_tests = {str(path.relative_to(ROOT)) for path in (ROOT / 'tests').glob('test_*.py')}
    assert not supplementary & gate_a
    assert supplementary | gate_a == all_tests
    assert set(plan.select_tests('quick')) <= all_tests
    assert len(plan.select_tests('quick')) <= 10


def test_new_modules_are_automatically_selected_and_missing_smoke_fails():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / 'tests').mkdir()
        assert plan.select_tests('supplementary', root) == []
        (root / 'tests/test_future.py').touch()
        assert plan.select_tests('supplementary', root) == ['tests/test_future.py']
        with pytest.raises(ValueError, match='Missing smoke'):
            plan.select_tests('quick', root)
        with pytest.raises(ValueError, match='Unknown CI'):
            plan.select_tests('invalid', root)


def test_cli_prints_the_actual_partition(capsys):
    assert plan.main(['supplementary']) == 0
    assert capsys.readouterr().out.splitlines() == plan.select_tests('supplementary')
    with pytest.raises(SystemExit) as error:
        plan.main(['invalid'])
    assert error.value.code == 2
