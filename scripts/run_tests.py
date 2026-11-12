#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Run bounded interface controls, impacted development tests, or complete suites.

Usage: python3 scripts/run_tests.py --profile control|development|full [--list]
Inputs: maintained catalog and explicit changed paths or Git baseline.
Outputs: selected commands and subprocess test output. Exit status preserves any
failed test invocation; selection/configuration errors return 2.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

try:
    from . import test_selection
except ImportError:
    import test_selection


def python_selection(root, catalog, profile, changed):
    """Return (selectors, reason) for maintained Python tests in ``root``.

    ``catalog`` supplies explicit classifications and control nodes; ``profile``
    is control, development or full. ``changed`` contains root-relative changed
    resources used only by development. Full includes every catalogued module.
    Invalid changed paths raise ValueError through impact selection.
    """
    if profile == 'control':
        return sorted(catalog['control']), 'Curated semantic interface controls (positive and negative cases)'
    if profile == 'full':
        return sorted(catalog['modules']), 'Complete maintained Python suite, including slow and six-layer progression'
    return test_selection.select_impacted(root, catalog, changed)


def main(argv=None):
    """Select and run suites; return their exit status, or 2 for invalid selection/configuration.

    ``argv`` is an optional CLI argument list. ``--list`` prints the plan without
    executing tests. Categories combine with OR and intersect profile selection.
    Native and Python suites run sequentially; no pass receipt is manufactured.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--profile', choices=('control', 'development', 'full'), default='control')
    parser.add_argument('--scope', choices=('python', 'native', 'all'), default='all')
    parser.add_argument('--changed', action='append', default=[])
    parser.add_argument('--base')
    parser.add_argument('--category', choices=sorted(test_selection.TAGS), action='append', default=[])
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.base and args.changed:
            raise ValueError('--base and --changed are mutually exclusive')
        if args.profile != 'development' and (args.base or args.changed):
            raise ValueError('--base/--changed require --profile development')
        changed = (args.changed or test_selection.changed_paths(root, args.base)) if args.profile == 'development' else []
        catalog = test_selection.load_catalog(root)
        missing = set(test_selection.maintained_modules(root)) - set(catalog['modules'])
        stale = {name for name in catalog['modules'] if not (root / name).is_file()}
        if missing or stale:
            raise ValueError(f'Test catalog mismatch; add {sorted(missing)}, remove {sorted(stale)}')
        commands = []
        if args.scope in ('python', 'all'):
            selectors, reason = python_selection(root, catalog, args.profile, changed)
            print(f'Python: {reason}; {len(selectors)} selectors', flush=True)
            if selectors:
                command = [sys.executable, '-u', '-m', 'pytest', '-q', '--strict-markers', '--durations=10']
                if args.category:
                    command += ['-m', ' or '.join(args.category)]
                command += selectors
                commands.append(command)
        if args.scope in ('native', 'all') and (args.profile != 'development' or changed):
            command = ['node', 'apps/fabric-explorer/tools/test-selection.mjs', '--profile', args.profile]
            for path in changed:
                command += ['--changed', path]
            for tag in args.category:
                command += ['--category', tag]
            if args.list:
                command += ['--list']
            commands.append(command)
        for command in commands:
            print(json.dumps(command), flush=True)
            if args.list and command[0] != 'node':
                continue
            status = subprocess.run(command, cwd=root).returncode
            if status:
                return status
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'Test selection error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
