# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Closed-schema freshness and real external-proof boundary regressions."""
import copy
import json
import time

import pytest

from governed_fixtures import HumanSigner, delivery, lc, op


def _schema_package(tmp_path, monkeypatch):
    package = tmp_path / 'schemas'
    package.mkdir()
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
              '$defs': {'bounded': {'type': 'integer', 'minimum': 0, 'maximum': 1}},
              '$ref': '#/$defs/bounded'}
    (package / 'value.schema.json').write_text(json.dumps(schema))
    monkeypatch.setattr(delivery, 'PACKAGE', package)
    return package, schema


def test_validator_and_validate_use_exact_definition_and_closed_boundaries(tmp_path, monkeypatch):
    _schema_package(tmp_path, monkeypatch)
    assert delivery.validator('value.schema.json', 'bounded').is_valid(0)
    assert delivery.validate(1, 'value.schema.json') == 1
    with pytest.raises(delivery.ProtocolError) as failure:
        delivery.validate(2, 'value.schema.json')
    assert failure.value.code == 'P_SCHEMA'
    with pytest.raises(ValueError, match='unknown governed schema'):
        delivery.validator('missing.schema.json')
    with pytest.raises(ValueError, match='unknown governed schema'):
        delivery.validator('value.schema.json', 'missing')


def test_schema_compilation_observes_edits_additions_and_removals(tmp_path, monkeypatch):
    package, schema = _schema_package(tmp_path, monkeypatch)
    first = delivery.validator('value.schema.json')
    assert first.is_valid(1)
    schema['$defs']['bounded']['maximum'] = 0
    (package / 'value.schema.json').write_text(json.dumps(schema))
    assert not delivery.validator('value.schema.json').is_valid(1)
    added = package / 'extra.schema.json'
    added.write_text(json.dumps({'$schema': schema['$schema'], 'const': 'extra'}))
    assert delivery.validator('extra.schema.json').is_valid('extra')
    added.unlink()
    with pytest.raises(ValueError, match='unknown governed schema'):
        delivery.validator('extra.schema.json')
    assert not delivery.validator('value.schema.json').is_valid(1)


@pytest.mark.parametrize('reference', ['https://example.invalid/schema.json',
                                       'file:///tmp/external.schema.json',
                                       '../external.schema.json', 'absent.schema.json'])
def test_schema_compilation_rejects_unavailable_or_external_references(tmp_path, monkeypatch, reference):
    package, schema = _schema_package(tmp_path, monkeypatch)
    assert delivery.validator('value.schema.json').is_valid(0)
    schema['$ref'] = reference
    (package / 'value.schema.json').write_text(json.dumps(schema))
    with pytest.raises(ValueError, match='offline package references required'):
        delivery.validator('value.schema.json')


def test_proof_bytes_preserves_exact_wrapper_bytes_and_rejects_other_shapes():
    raw = b'{ "request": {}, "receipt": {} }\n'
    retained, wrapper = delivery.proof_bytes(raw)
    assert retained == raw
    assert wrapper == {'request': {}, 'receipt': {}}
    encoded, reparsed = delivery.proof_bytes(wrapper)
    assert encoded == op.canonical(wrapper)
    assert reparsed == wrapper
    for invalid in (b'{}', b'not-json', b'{"request":{},"request":{},"receipt":{}}',
                    {'request': {}, 'receipt': {}, 'extra': True}):
        with pytest.raises(delivery.ProtocolError) as failure:
            delivery.proof_bytes(invalid)
        assert failure.value.code == 'P_ORIGIN'


def test_verify_proof_checks_real_signature_purpose_and_assessment_expiry(tmp_path, monkeypatch):
    signers = HumanSigner(tmp_path / 'keys', monkeypatch)
    source = tmp_path / 'message'
    source.write_bytes(b'exact technical request')
    now = int(time.time() * 1000)
    proof = signers.wrapper('delivery-change', source, tmp_path / 'ledger', {}, now_ms=now)
    verified = delivery.verify_proof(proof, 'delivery-change', now)
    assert verified['wrapper'] == proof
    assert verified['trust']['key_id'] == signers.keys['human']['entry']['key_id']
    expiry = int(proof['request']['expires_at'] * 1000)
    assert delivery.verify_proof(proof, 'delivery-change', expiry - 1, live=False)
    with pytest.raises(delivery.ProtocolError):
        delivery.verify_proof(proof, 'delivery-change', expiry, live=False)
    with pytest.raises(delivery.ProtocolError):
        delivery.verify_proof(proof, 'delivery-accept', now)
    forged = copy.deepcopy(proof)
    forged['receipt']['signature'] = 'Zm9yZ2Vk'
    with pytest.raises(delivery.ProtocolError):
        delivery.verify_proof(forged, 'delivery-change', now)

