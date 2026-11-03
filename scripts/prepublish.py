#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Run the complete maintained regression suite locally before publication.

This command does not publish, create approval receipts or invoke a live model.
The operator owns this local prerequisite; the tag workflow performs separate
bounded source, documentation and archive checks.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def pytest_command(root):
    """Construct an unfiltered, fail-fast local regression command.

    Args:
        root: Checkout containing the maintained tests directory.
    Returns:
        Argument list using this interpreter, verbose unbuffered output and the
        complete tests directory. No test selectors or aggregate timeout apply.
    Raises:
        ValueError: The maintained test directory is unavailable.
    """
    if not (Path(root) / 'tests').is_dir():
        raise ValueError('maintained tests directory is missing')
    return [sys.executable, '-u', '-m', 'pytest', '-vv', '-x', '--tb=short',
            '--durations=20', 'tests']


def main(argv=None):
    """Run local regressions and preserve pytest's exit status.

    Args:
        argv: Optional CLI arguments; only the checkout location is selectable.
    Returns:
        The test process exit status. A failed or interrupted run is not success.
    Raises:
        OSError, ValueError: The checkout or test process is unavailable.
        SystemExit: Invalid arguments are supplied.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    return subprocess.run(pytest_command(root), cwd=root).returncode


if __name__ == '__main__':
    raise SystemExit(main())
