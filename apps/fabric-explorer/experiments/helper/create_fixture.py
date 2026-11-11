# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Create only synthetic portable fixture bytes using the existing test harness.

Run on a maintained POSIX writer host, then transfer the output for native
reader tests. No signing identity is created and no private source is copied.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import sys


def main(argv=None):
    """Create a new synthetic ordinary-history fixture directory.

    Args:
        argv: Optional explicit CLI arguments; defaults to process arguments.
    Returns:
        Zero after canonical fixture generation; failures propagate.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[4]
    output = args.output.absolute()
    if output.exists():
        raise ValueError('Fixture output must not already exist')
    sys.path.insert(0, str(root / 'tests'))
    import pytest
    from governed_fixtures import GovernedHarness
    with pytest.MonkeyPatch.context() as patch:
        host = GovernedHarness(output, patch, engagement='synthetic-reader-proof')
        host.bootstrap()
        host.qualified_answer(text='Synthetic reader packaging fixture only.')
        state = host.store.read()
        if host._human_signer is not None:
            raise ValueError('Ordinary fixture unexpectedly created a signing identity')
        expected = {'engagement': host.engagement, 'head': state.head,
                    'transactions': len(state.transactions), 'versions': len(state.versions),
                    'uses': len(state.states),
                    'families': dict(Counter(value['kind'] for value in state.versions.values()))}
    shutil.copyfile(root / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl',
                    output / 'findings-review.jsonl')
    expected['files'] = {p.relative_to(output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(output.rglob('*')) if p.is_file()}
    (output / 'expected.json').write_text(json.dumps(expected, indent=2) + '\n')
    print(json.dumps({'status': 'synthetic-fixture-created',
                      'transactions': expected['transactions']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
