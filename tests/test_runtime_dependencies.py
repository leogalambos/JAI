# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Lightweight runtime observations never depend on optional renderer success."""
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.ai/runtime/tools'))
import runtime_dependencies


@pytest.mark.parametrize('version,status,compatible',[('4.26.0','ready',True),('4.23.0','incompatible',False),('5.0.0','incompatible',False),('invalid','unknown',None),(None,'unknown',None)])
def test_jsonschema_status_distinguishes_qualified_incompatible_and_unknown_metadata(version,status,compatible):
    with patch('importlib.util.find_spec',return_value=True), patch('importlib.metadata.version',return_value=version):
        result=runtime_dependencies.jsonschema_status()
    assert result['available'] is True
    assert result['status']==status
    assert result['compatible'] is compatible
    assert isinstance(result['version'],str)


def test_jsonschema_status_reports_absence_without_importing_package():
    with patch('importlib.util.find_spec',return_value=None), patch('importlib.metadata.version',side_effect=AssertionError('no package import/query needed')):
        result=runtime_dependencies.jsonschema_status()
    assert result['status']=='missing'
    assert result['available'] is False and result['compatible'] is False


def test_jsonschema_status_lookup_failure_is_unknown_not_missing():
    with patch('importlib.util.find_spec',side_effect=RuntimeError('metadata lookup failed')):
        result=runtime_dependencies.jsonschema_status()
    assert result['status']=='unknown'
    assert result['available'] is None and result['compatible'] is None
    assert 'metadata lookup failed' in result['reason']
