# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Write synthetic nontext-target canonical chains for viewer integration tests.

Usage: pinned-python -I -B make_findings_fixture.py ABSOLUTE_OUTPUT float|nan|object|unicode.
The fixed public synthetic baseline is rehashed with the maintained findings
canonical function. No private keys or runtime authority are involved.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import findings


def main():
    """Write one bounded test-only chain while preserving exact nontext target semantics.

    Returns:
        Zero after exclusive output creation.
    Raises:
        ValueError: Output is not an explicit absolute path or case is unsupported.
        OSError: Synthetic fixture publication fails.
    """
    if len(sys.argv) != 3 or not Path(sys.argv[1]).is_absolute(): raise ValueError('Explicit output and case required')
    values = {'float': 1.5, 'nan': float('nan'), 'object': {'counter': 9007199254740993}, 'unicode': {'text': 'Ωλ東京' * 20, 'symbol': '\U0001f600'}}
    target = values[sys.argv[2]]
    events = [json.loads(line) for line in (ROOT / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl').read_bytes().splitlines()]
    previous = '0' * 64
    for event in events:
        if event['data']['op'] == 'add': event['data']['target'] = target
        event['prev'] = previous; event['hash'] = hashlib.sha256((previous + findings.canonical(event['data']) + str(event['seq'])).encode()).hexdigest(); previous = event['hash']
    with Path(sys.argv[1]).open('xb') as output:
        for event in events: output.write(findings.canonical(event).encode() + b'\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
