# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Attach maintained test tags before pytest applies native ``-m`` selection."""
import importlib.util
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location('jai_test_selection_plugin', Path(__file__).parent / 'scripts/test_selection.py')
_SELECTION = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_SELECTION)


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Apply classifications to collected ``items`` before native marker filtering.

    ``config`` is pytest's configuration (no additional options are required).
    Items outside maintained test roots remain unchanged. Explicit category
    decorators override the catalog; conflicting categories and unclassified
    maintained modules raise pytest.UsageError. Markers are added in place.
    """
    root = Path(__file__).parent
    try:
        catalog = _SELECTION.load_catalog(root)
        for item in items:
            path = Path(str(item.path)).resolve()
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError:
                continue
            if not (relative.startswith('tests/') or relative.startswith('apps/')):
                continue
            node = relative + '::' + item.nodeid.split('::', 1)[1]
            tags = _SELECTION.tags_for_node(catalog, node)
            explicit = {mark.name for mark in item.iter_markers()} & _SELECTION.CATEGORIES
            if len(explicit) > 1:
                raise ValueError(f'Test has conflicting category decorators: {node}')
            if explicit:
                tags.difference_update(_SELECTION.CATEGORIES)
            for tag in tags:
                item.add_marker(getattr(pytest.mark, tag))
    except ValueError as exc:
        raise pytest.UsageError(str(exc)) from exc
