#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Optional, non-release-blocking performance diagnostics.

Neither this utility nor its measurements participate in GA gates A-H.
A reference can only be provided explicitly from an external file.
"""
from __future__ import annotations

import argparse
import json
import platform
import resource
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / '.ai/runtime/ci/performance-stages.json'


def environment():
    return {
        'python': platform.python_version(),
        'implementation': platform.python_implementation(),
        'platform': platform.platform(),
    }


def size_count(root):
    files = [p for p in Path(root).rglob('*') if p.is_file()
             and '.git' not in p.parts and '__pycache__' not in p.parts
             and not p.name.endswith('.pyc')]
    return len(files), sum(p.stat().st_size for p in files)


def run_once(stage):
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.perf_counter()
    try:
        proc = subprocess.run(stage['command'], cwd=ROOT, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True,
                              timeout=stage['timeout_seconds'])
        timed_out = False
        ok = proc.returncode == 0
        detail = proc.stdout[-1500:] if not ok else ''
    except subprocess.TimeoutExpired:
        timed_out = True
        ok = False
        detail = f'timeout at stage {stage["name"]}'
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    count, size = size_count(ROOT)
    return {
        'name': stage['name'], 'ok': ok, 'timeout': timed_out,
        'wall_time': time.perf_counter() - start,
        'cpu_time': (after.ru_utime + after.ru_stime)
                    - (before.ru_utime + before.ru_stime),
        'peak_memory_kb': after.ru_maxrss, 'artifact_count': count,
        'input_size': size, 'cache_status': 'not-declared', 'detail': detail,
    }


def run(profile, samples=3):
    cfg = json.loads(CONFIG.read_text())
    rows = []
    for stage in cfg['profiles'][profile]:
        measurements = [run_once(stage) for _ in range(max(1, samples))]
        last = dict(measurements[-1])
        last.update({
            'ok': all(x['ok'] for x in measurements),
            'timeout': any(x['timeout'] for x in measurements),
            'wall_time': statistics.median(x['wall_time'] for x in measurements),
            'cpu_time': statistics.median(x['cpu_time'] for x in measurements),
            'peak_memory_kb': max(x['peak_memory_kb'] for x in measurements),
            'samples': len(measurements),
        })
        if not last['ok']:
            last['detail'] = '; '.join(x['detail'] for x in measurements if not x['ok'])[-3000:]
        rows.append(last)
    return rows


def compare(rows, reference, threshold_percent):
    """Optional analysis. Incomparable machine measurements are not failures."""
    if reference.get('environment') != environment():
        return {'status': 'incomparable-environment', 'regressions': [],
                'note': 'Reference environment differs; no speed claim is made.'}
    previous = {x['name']: x for x in reference.get('stages', [])}
    regressions = []
    for row in rows:
        old = previous.get(row['name'])
        if old and old.get('wall_time', 0) > 0 and row['wall_time'] > old['wall_time'] * (1 + threshold_percent / 100):
            regressions.append(row['name'])
    return {'status': 'comparable', 'regressions': regressions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=('fast', 'full'), default='fast')
    parser.add_argument('--samples', type=int, default=3)
    parser.add_argument('--out', help='Optional report path; generated at runtime')
    parser.add_argument('--compare-to', type=Path,
                        help='Optional externally supplied benchmark reference')
    args = parser.parse_args()
    if args.samples < 1:
        parser.error('--samples must be >= 1')
    rows = run(args.profile, args.samples)
    report = {'profile': args.profile, 'samples': args.samples,
              'environment': environment(), 'stages': rows,
              'release_gate': False}
    if args.compare_to:
        ref = json.loads(args.compare_to.read_text())
        threshold = json.loads(CONFIG.read_text())['regression_limit_percent']
        report['comparison'] = compare(rows, ref, threshold)
    for row in rows:
        print(('PASS' if row['ok'] else 'FAIL'), row['name'],
              f"wall={row['wall_time']:.3f}s samples={row['samples']}")
    if 'comparison' in report:
        print('INFO benchmark comparison:', report['comparison']['status'],
              report['comparison']['regressions'])
    if args.out:
        target = Path(args.out)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + '\n')
    # A failed benchmark command remains a failure when explicitly run.
    # Benchmark speed variation, however, never blocks the release.
    return 0 if all(row['ok'] for row in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
