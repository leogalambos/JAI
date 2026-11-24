# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Shared bounds and exact identity normalization for role-context admission."""

import unicodedata

# Catalogue maxima when adopted were 33,845 and 1,235 UTF-8 bytes.
INSTRUCTION_BYTES = 36 * 1024
SECTION_BYTES = 1536


def alias_key(alias):
    """Return the NFKC, case-folded, whitespace-normalized key for a text alias."""
    return ' '.join(unicodedata.normalize('NFKC', alias).casefold().split())
