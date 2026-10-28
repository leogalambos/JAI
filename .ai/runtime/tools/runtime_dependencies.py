#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Observe runtime package metadata without importing optional application code."""
from __future__ import annotations

import importlib.metadata
import importlib.util
import re


def jsonschema_status():
    """Observe this interpreter's runtime validator using only the standard library.

    Returns:
        Fresh mapping with status ready/missing/incompatible/unknown, available
        and compatible booleans (None when unknown), version, required range and
        runtime-only scope. Lookup errors remain bounded unknown diagnostics;
        they never assert a missing package or successful contract validation.
        This function takes no arguments, installs nothing and does not import
        jsonschema or any rendering backend. It does not raise lookup exceptions.
    """
    result={'available':None,'compatible':None,'version':'not verified',
            'required':'jsonschema>=4.26,<5',
            'scope':'runtime contract validation; not installation','status':'unknown'}
    try:
        result['available']=importlib.util.find_spec('jsonschema') is not None
        if not result['available']:
            result.update(compatible=False,version='not installed',status='missing')
            return result
        version=importlib.metadata.version('jsonschema')
        if not isinstance(version,str):
            result['reason']='package version metadata is not a string'
            return result
        result['version']=version
        match=re.fullmatch(r'(\d+)\.(\d+)(?:\.\d+)*',result['version'])
        if match is None:
            result['reason']='package version is not a verified stable release'
            return result
        result['compatible']=(4,26)<=tuple(map(int,match.groups()))<(5,0)
        result['status']='ready' if result['compatible'] else 'incompatible'
    except Exception as exc:
        result['reason']=type(exc).__name__+': '+str(exc)[:2000]
    return result
