# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Lossless bounded UTF-8 JSON transport across Python accounting and Node decoding."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'apps/fabric-explorer/reader'))
from semantic_reader import _encoded, _FactList, SemanticReadError
from raw_reader import _encode_wire


@pytest.mark.parametrize('text', ['plain', 'Ωλ東京' * 20, '\U0001f600', '\ud800', '\udfff', '\ud83d\ude00', 'control\x00\n"\\'])
def test_fact_json_uses_utf8_without_changing_cross_language_values(text):
    value = {'label': text, 'integer': {'type': 'integer', 'value': str(2 ** 80)}, 'bits': {'type': 'float64', 'bits': '8000000000000000'}}
    expected = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8', 'backslashreplace')
    actual = _encoded(value)
    assert actual == expected
    assert _encode_wire(value) == actual
    assert json.loads(actual) == json.loads(json.dumps(value, ensure_ascii=True))
    node = ROOT / 'build/fabric-explorer/toolchain/node/node-v24.22.2-linux-x64/bin/node'
    decoded = subprocess.run([str(node), '-e', "let text='';process.stdin.setEncoding('utf8');process.stdin.on('data',v=>text+=v);process.stdin.on('end',()=>process.stdout.write(JSON.stringify(JSON.parse(text))));"], input=actual, capture_output=True, check=True, timeout=5)
    assert json.loads(decoded.stdout) == json.loads(actual)


def test_fact_budget_counts_exact_utf8_bytes_at_boundary():
    fact = {'kind': 'version', 'sourceId': 'synthetic-source', 'label': 'Ωλ東京' * 20}
    size = len(json.dumps(fact, ensure_ascii=False, separators=(',', ':')).encode())
    limits = {'maxVertices': 1, 'maxEdges': 1, 'maxEncodedGraphBytes': size}
    accepted = _FactList(limits)
    rejected = _FactList({**limits, 'maxEncodedGraphBytes': size - 1})
    try:
        accepted.append(fact)
        assert accepted.encoded == size
        with pytest.raises(SemanticReadError): rejected.append(fact)
    finally:
        accepted.release(); rejected.release()
