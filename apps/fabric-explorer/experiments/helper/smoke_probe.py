# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Run disposable native executable checks with no ambient runtime search path.

Raw reports belong in caller-supplied scratch/private output, not release docs.
This proves the supplied fixtures only, not full platform qualification.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import stat
import tempfile


def _manifest(root):
    return {p.relative_to(root).as_posix(): 'directory' if p.is_dir()
            else hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*'))}


def _report_destination(report, fixtures):
    source = os.path.normcase(str(fixtures.resolve(strict=True)))
    destination = report.resolve(strict=False)
    target = os.path.normcase(str(destination))
    try:
        overlaps = os.path.commonpath([source, target]) == source
    except ValueError:
        overlaps = False  # Distinct native Windows drives cannot contain each other.
    if overlaps:
        raise ValueError('Report output must be outside selected fixtures')
    if destination.exists():
        info = destination.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError('Existing report output must be a singly-linked regular file')
    return destination


def main(argv=None):
    """Exercise one standalone helper and write a factual smoke report.

    Args:
        argv: Optional explicit CLI arguments; defaults to process arguments.
    Returns:
        Zero when every observation matches the fixture contract; failures raise.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', type=Path, required=True)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args(argv)
    executable, fixtures = args.executable.absolute(), args.fixtures.absolute()
    report_path = _report_destination(args.report, fixtures)
    expected = json.loads((fixtures / 'expected.json').read_text())
    before = _manifest(fixtures)
    observed = []
    with tempfile.TemporaryDirectory(prefix='jai-reader-smoke-') as temporary:
        environment = {'PATH': '', 'PYTHONPATH': str(fixtures), 'PYTHONHOME': str(fixtures),
                       'FINDINGS_MAX_ROUNDS': '1', 'HOME': temporary,
                       'TMPDIR': temporary, 'TEMP': temporary, 'TMP': temporary}
        if os.name == 'nt':
            environment['SystemRoot'] = os.environ['SystemRoot']
        def run(*arguments):
            completed = subprocess.run([str(executable), *arguments], cwd=temporary,
                                       env=environment, capture_output=True, text=True, timeout=60)
            result = json.loads(completed.stdout)
            if completed.returncode != 0:
                raise ValueError(f'Native probe rejected smoke operation: {result}')
            if result['authority_granted'] or result['current_assessment']:
                raise ValueError('Reader unexpectedly claimed authority or fresh assessment')
            observed.append(result)
            return result
        fabric = run('fabric', '--journal', str(fixtures / (expected['engagement'] + '.jsonl')),
                     '--engagement', expected['engagement'])
        for name in ('head', 'transactions', 'versions', 'uses', 'families'):
            if fabric[name] != expected[name]:
                raise ValueError('Canonical fixture summary differs')
        if not fabric['history_verified']:
            raise ValueError('Ordinary canonical fixture was not replayed')
        findings = run('findings', '--journal', str(fixtures / 'findings-review.jsonl'),
                       '--max-rounds', '3')
        if set(findings['recorded_states']) != {'open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted'}:
            raise ValueError('Findings fixture states differ')
        diagnostic = run('diagnostic', '--journal', str(fixtures / (expected['engagement'] + '.jsonl')))
        if diagnostic['history_verified'] or diagnostic['semantic_state'] != 'unknown':
            raise ValueError('Diagnostic structure falsely claimed canonical state')
        run('verifier')
    if _manifest(fixtures) != before:
        raise ValueError('Reader modified selected fixture bytes or entries')
    report = {'format': 'jai.fabric-explorer.helper-smoke/1', 'status': 'passed',
              'qualifiedPlatform': False, 'scope': 'Supplied ordinary fixture and public Ed25519 vector only',
              'ambientPath': 'empty', 'sourceUnchanged': True, 'operations': observed}
    if _report_destination(args.report, fixtures) != report_path:
        raise ValueError('Report destination changed during the smoke run')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if _report_destination(args.report, fixtures) != report_path:
        raise ValueError('Report destination changed before publication')
    descriptor, staged = tempfile.mkstemp(prefix='.jai-reader-report-', dir=report_path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as output:
            output.write(json.dumps(report, indent=2) + '\n')
        if _report_destination(args.report, fixtures) != report_path:
            raise ValueError('Report destination changed before publication')
        os.replace(staged, report_path)
    finally:
        Path(staged).unlink(missing_ok=True)
    print(json.dumps({'status': 'passed', 'operations': len(observed), 'qualifiedPlatform': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
