#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Select bounded source smoke tests or the tests not already run by Gate A."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from qualification_core import REGRESSION_MODULES

QUICK_MODULES = (
    'test_ci_test_plan.py', 'test_release_preflight.py',
    'test_ci_environment_contract.py', 'test_jai_pages_and_release.py',
    'test_version_decoupling.py', 'test_documentation_navigation.py',
    'test_license_policy_regression.py', 'test_offline_guard.py',
    'test_qualification_core.py',
)


def select_tests(scope: str, root: Path = ROOT) -> list[str]:
    """Return existing relative test paths for a named CI scope.

    Args:
        scope: ``quick`` smoke coverage or ``supplementary`` complete coverage
            outside Gate A's canonical inventory.
        root: Checkout whose tests directory is inspected without mutation.
    Returns:
        Sorted paths; supplementary selection includes new test modules
        automatically and never repeats a Gate A module.
    Raises:
        ValueError: If the scope is unknown or a smoke module is missing.
    """
    available = {p.name for p in (root / 'tests').glob('test_*.py')}
    if scope == 'quick':
        selected = set(QUICK_MODULES)
        if selected - available:
            raise ValueError('Missing smoke modules: ' + ', '.join(sorted(selected - available)))
    elif scope == 'supplementary':
        selected = available - set(REGRESSION_MODULES)
    else:
        raise ValueError('Unknown CI test scope: ' + scope)
    return ['tests/' + name for name in sorted(selected)]


def main(argv: list[str] | None = None) -> int:
    """Print one selected path per line; reject unknown scopes with exit 2.

    Args:
        argv: Optional command arguments, otherwise process arguments.
    Returns:
        Zero after printing a valid plan; argparse rejects invalid inputs.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scope', choices=('quick', 'supplementary'))
    args = parser.parse_args(argv)
    print('\n'.join(select_tests(args.scope)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
