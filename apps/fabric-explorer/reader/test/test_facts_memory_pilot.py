# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Diagnostic accounting boundaries; actual matched canonical conditions run separately once."""
import importlib.util
import os
from pathlib import Path
import sys

import pytest

spec = importlib.util.spec_from_file_location('facts_memory_pilot', Path(__file__).resolve().parents[1] / 'dev/facts_memory_pilot.py')
pilot = importlib.util.module_from_spec(spec); spec.loader.exec_module(pilot)


def test_reachable_deduplicates_cycles_and_tracks_opaque_leaves():
    value = []; value.append(value); value.append(object())
    graph, opaque = pilot.reachable(value)
    assert len(graph) == 2 and id(value) in graph and opaque == {'object': 1}
    assert graph[id(value)] == sys.getsizeof(value)


def test_reachable_inclusive_bound_and_explicit_failure():
    assert len(pilot.reachable('one', maximum=1)[0]) == 1
    with pytest.raises(RuntimeError, match='object bound'):
        pilot.reachable(['one'], maximum=1)


def test_reachable_shared_bound_spans_categories_without_double_counting():
    identities = set(); item = object()
    pilot.reachable(item, maximum=1, shared=identities)
    pilot.reachable(item, maximum=1, shared=identities)
    with pytest.raises(RuntimeError, match='shared object bound'):
        pilot.reachable(object(), maximum=1, shared=identities)
    assert len(identities) == 1


def test_memory_uses_actual_page_size_and_reports_read_failure(tmp_path):
    if sys.platform != 'linux': pytest.skip('Linux accounting fixture')
    record = tmp_path / 'statm'; record.write_text('10 3 0\n')
    observed = pilot.memory(record)
    assert observed['supported'] and observed['currentBytes'] == 3 * os.sysconf('SC_PAGE_SIZE')
    assert observed['peakBytes'] > 0
    record.write_text('invalid')
    with pytest.raises((ValueError, IndexError)): pilot.memory(record)


def test_memory_marks_unsupported_platform_without_reading(monkeypatch):
    monkeypatch.setattr(pilot.sys, 'platform', 'unsupported-pilot-platform')
    assert pilot.memory() == {'supported': False, 'currentBytes': None, 'peakBytes': None}


def test_main_rejects_nonexplicit_inputs_before_import_or_write(monkeypatch):
    monkeypatch.setattr(pilot.sys, 'argv', ['pilot'])
    with pytest.raises(ValueError, match='Explicit manifest'): pilot.main()
