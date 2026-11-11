# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Create synthetic unsigned canonical history for viewer-only integration tests.

Usage: pinned-python -I -B make_fabric_fixture.py ABSOLUTE_EMPTY_DIRECTORY.
Writes only synthetic fixture journals/material inside that test directory;
prints one metadata JSON object. This test utility is not part of the reader.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / '.ai/runtime/tools'), str(ROOT / 'tests')]
from governed_fixtures import GovernedHarness


def main():
    """Create all seven record families through the actual maintained fixture writer.

    Returns:
        Zero after successful synthetic fixture construction and parity metadata.
    Raises:
        ValueError: Target is not an explicit empty absolute fixture directory.
        OSError: Fixture output fails.
    """
    if len(sys.argv) != 2: raise ValueError('Explicit fixture directory required')
    target = Path(sys.argv[1])
    if not target.is_absolute() or not target.is_dir() or list(target.iterdir()): raise ValueError('Empty absolute fixture directory required')
    fixture = GovernedHarness(target, None, engagement='synthetic-viewer-integration')
    fixture.bootstrap(); actor = fixture.setup_author(); product, record = fixture.product('synthetic-result', actor)
    fixture.commit(fixture.submission(actor, product, record)); fixture.review(actor, product)
    state = fixture.store.read()
    print(json.dumps({'filename': fixture.path.name, 'versions': len(state.versions), 'uses': len(state.states),
                      'sequence': len(state.transactions), 'head': state.head, 'versionRefs': [state._reference(identifier) for identifier in state.versions],
                      'usePoints': [{'ref': state._reference(identifier), 'use_scope': scope} for scope, identifier in state.states]}, separators=(',', ':')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
