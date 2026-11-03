# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Closed wire and explicit L0 signature helpers; lifecycle owns all authoritative state."""
from __future__ import annotations

import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import urldefrag, urlsplit

import jsonschema
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

import operator_actions as operator

PROTOCOL = 'jai.governed-delivery/1'
PACKAGE = Path(__file__).resolve().parents[1] / 'protocol/governed-delivery/v1'



class ProtocolError(ValueError):
    """Carry a public-safe protocol guard code without exposing private material."""
    def __init__(self, code, message, field=None):
        """Record code, public-safe message and optional safe property field."""
        super().__init__(message)
        self.code, self.field = code, field


def _require_scope(trust, engagement, scope):
    if (engagement not in trust['engagements'] and '*' not in trust['engagements']
            or scope not in trust['scopes'] and '*' not in trust['scopes']):
        raise ProtocolError('P_SCOPE', 'Known signing key lacks the exact engagement or scope grant')


def _refs(value):
    if isinstance(value, dict):
        if '$ref' in value:
            yield value['$ref']
        for child in value.values():
            yield from _refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _refs(child)


@lru_cache(maxsize=4)
def _compiled_package(package_uri, sources):
    schemas = {name: json.loads(raw) for name, raw in sources}
    resources = []
    for filename, schema in schemas.items():
        for target in _refs(schema):
            location, _ = urldefrag(target)
            parsed = urlsplit(location)
            if parsed.scheme or parsed.netloc or (location and location not in schemas):
                raise ValueError('offline package references required')
        schema['$id'] = package_uri + '/' + filename
        jsonschema.Draft202012Validator.check_schema(schema)
        resources.append((schema['$id'], Resource.from_contents(schema)))
    def unavailable(uri):
        raise NoSuchResource(ref=uri)
    registry = Registry(retrieve=unavailable).with_resources(resources)
    validators = {(name, None): jsonschema.Draft202012Validator(schema, registry=registry)
                  for name, schema in schemas.items()}
    for name, schema in schemas.items():
        for definition in schema.get('$defs', {}):
            validators[name, definition] = jsonschema.Draft202012Validator(
                {'$ref': schema['$id'] + '#/$defs/' + definition}, registry=registry)
    return validators


def validator(name, definition=None):
    """Return an offline Draft-2020-12 validator for a declared package schema.

    Args:
        name: Exact local schema filename.
        definition: Optional exact named definition within that schema.
    Returns:
        Content-keyed compiled validator with no remote retrieval capability.
    Raises:
        ValueError: A schema or reference escapes the closed package.
    """
    # Read every current package member before using compiled representations;
    # schema changes must never retain a validator for an earlier contract.
    sources = tuple((path.name, path.read_bytes()) for path in sorted(PACKAGE.glob('*.schema.json')))
    validators = _compiled_package(PACKAGE.as_uri(), sources)
    if (name, definition) not in validators:
        raise ValueError('unknown governed schema')
    return validators[name, definition]


def validate(value, schema='message.schema.json'):
    """Validate value against a closed local schema, raising safe P_SCHEMA errors.

    Args:
        value: Strictly parsed semantic JSON value.
        schema: Maintained local schema name.
    Returns:
        The unchanged validated value.
    Raises:
        ProtocolError: The value violates the closed structural contract.
    """
    if not validator(schema).is_valid(value):
        raise ProtocolError('P_SCHEMA', 'Closed governed protocol shape required')
    return value


def message_id(message):
    """Hash complete message content except its sole message_id field.

    Args:
        message: Strict semantic message object.
    Returns:
        Domain-separated lowercase content digest; no authority is granted.
    """
    import lifecycle
    return hashlib.sha256(b'jai.delivery.message.v1\0' + lifecycle.canonical(
        {key: value for key, value in message.items() if key != 'message_id'})).hexdigest()


def action_descriptor(message, policy_digest):
    """Construct the exact non-self-referential human intent descriptor.

    Args:
        message: Closed decision message, with or without its future proof digest.
        policy_digest: Independently resolved governing policy digest.
    Returns:
        Complete human-approved intent; only authority_proof is removed.
    Raises:
        ProtocolError: The message is not a typed decision.
    """
    if message.get('message_type') != 'decision':
        raise ProtocolError('P_SCHEMA', 'Human intent requires an exact decision')
    return {'protocol': PROTOCOL, 'delivery_request_id': message['request_id'],
            **{key: copy.deepcopy(message[key]) for key in (
                'engagement', 'scope', 'expected_head', 'context', 'profile',
                'issued_at_ms', 'expires_at_ms', 'causes')},
            'policy_digest': policy_digest, 'origin': copy.deepcopy(message['sender']),
            'decision': {key: copy.deepcopy(value) for key, value in message['payload'].items()
                         if key != 'authority_proof'}}



def proof_bytes(proof):
    """Return exact wrapper bytes and parsed proof, preserving caller byte identity.

    Args:
        proof: Exact bytes or an in-memory wrapper encoded by its own canonicalizer.
    Returns:
        Pair of exact bytes and parsed request/receipt wrapper.
    Raises:
        ProtocolError: Wrapper parsing or its closed outer shape is invalid.
    """
    try:
        raw = proof if isinstance(proof, bytes) else operator.canonical(proof)
        def pairs(items):
            result = {}
            for key, value in items:
                if key in result:
                    raise ValueError('duplicate proof member')
                result[key] = value
            return result
        def constant(value):
            raise ValueError('nonfinite proof number')
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
        if set(value) != {'request', 'receipt'}:
            raise ValueError('wrapper')
        return raw, value
    except (ValueError, TypeError, KeyError) as error:
        raise ProtocolError('P_ORIGIN', 'External proof wrapper required') from error


def verify_proof(proof, purpose, assessed_at_ms, live=True):
    """Verify exact-purpose external Ed25519 authorization and its time window.

    Args:
        proof: Exact external request/receipt bytes or wrapper object.
        purpose: Exact delivery-change, delivery-accept or delivery-release L0 purpose.
        assessed_at_ms: Immutable trusted assessment instant.
        live: Require current outer expiry for a new operation.
    Returns:
        Verified wrapper and independently resolved protected public trust snapshot.
    Raises:
        ProtocolError: Origin, purpose, signature, acceptance or timing is invalid.
    """
    raw, wrapper = proof_bytes(proof)
    try:
        request = wrapper['request']
        if request['kind'] != purpose or purpose not in {'delivery-change', 'delivery-accept', 'delivery-release'}:
            raise ValueError('wrong purpose')
        result = operator.verify_receipt(request, wrapper['receipt'], live=live)
        if not result['accepted'] or result['performed']:
            raise ValueError('authorization must be pending exact effects')
        at = assessed_at_ms / 1000
        if not request['created_at'] <= at < request['expires_at']:
            raise ValueError('proof not valid at assessment')
        trust = operator.trusted_key(purpose, wrapper['receipt']['key_id'], historical=not live)
        if not trust['valid_from_ms'] <= assessed_at_ms < trust['valid_until_ms']:
            raise ValueError('assessment outside externally enrolled key window')
        return {'raw': raw, 'wrapper': wrapper, 'trust': trust}
    except (ValueError, KeyError, TypeError, OSError) as error:
        raise ProtocolError('P_ORIGIN', 'External purpose, signature or assessment binding failed') from error
