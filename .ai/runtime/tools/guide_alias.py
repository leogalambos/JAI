# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""The single declared source GUIDE alias and its regular installed representation."""
from __future__ import annotations

import os
from pathlib import Path

GUIDE_ALIAS = '.ai/runtime/GUIDE.md'
GUIDE_SOURCE = 'docs/reference/installed-cli-guide.md'
GUIDE_LINK = '../../docs/reference/installed-cli-guide.md'


def guide_bytes(root, canonical_bytes=None, alias_bytes=None):
    """Validate the declared GUIDE relationship and return canonical public bytes.

    Args:
        root: Package directory containing the maintained public documentation.
        canonical_bytes: Optional canonical bytes already selected by the secure
            archive snapshot; avoids opening that resource a second time.
        alias_bytes: Optional regular alias bytes already read by that snapshot.
            Actual Git symlinks are inspected without following their targets.
    Returns:
        Canonical guide bytes for a regular installed or archived GUIDE.md.
        Git's Windows symlink stub and materialized archives are accepted without
        making either a second maintained source.
    Raises:
        ValueError: The alias points elsewhere, contains drift or crosses a link
            in a declared parent directory or canonical source path.
        OSError: A required declared package resource is unavailable.
    """
    root = Path(root)
    if root.is_symlink():
        raise ValueError('GUIDE package root must be a real directory')
    for relative in (GUIDE_SOURCE, GUIDE_ALIAS):
        current = root
        for part in Path(relative).parts[:-1]:
            current /= part
            if current.is_symlink():
                raise ValueError('GUIDE declared resource parents must be real directories')
    source, alias = root / GUIDE_SOURCE, root / GUIDE_ALIAS
    if source.is_symlink():
        raise ValueError('GUIDE canonical source must be a regular public file')
    canonical_bytes = source.read_bytes() if canonical_bytes is None else canonical_bytes
    if alias.is_symlink():
        if os.readlink(alias) != GUIDE_LINK:
            raise ValueError('GUIDE symlink must name its declared relative canonical source')
    else:
        alias_bytes = alias.read_bytes() if alias_bytes is None else alias_bytes
        if alias_bytes not in (GUIDE_LINK.encode('utf-8'), canonical_bytes):
            raise ValueError('GUIDE must be its declared Git alias or exact materialized canonical guide')
    return canonical_bytes
