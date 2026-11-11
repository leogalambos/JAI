# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Keep the explorer's synthetic input inventory aligned with canonical readers.

These are source compatibility checks, not a second lifecycle evaluator or an
assertion that a desktop viewer has been implemented or qualified.
"""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import findings
import governed_delivery as wire
import lifecycle as lc

FIXTURES = ROOT / 'apps/fabric-explorer/test/fixtures'
PROTOCOL = ROOT / '.ai/runtime/protocol/governed-delivery/v1'
INVENTORY = json.loads((FIXTURES / 'manifest.json').read_text(encoding='utf-8'))


def _record(case):
    value = lc.loads((ROOT / case['path']).read_bytes())
    for part in case['pointer'].strip('/').split('/') if case['pointer'] else []:
        value = value[part]
    return value


@pytest.mark.parametrize('case', INVENTORY['records'], ids=lambda case: case['id'])
def test_inventory_records_match_their_canonical_schemas(case):
    record = _record(case)
    wire.validator('record.schema.json', case['family']).validate(record)
    if 'discriminator' in case:
        assert record[case['discriminator']] == case['value']


def test_inventory_covers_all_declared_families_and_source_variants():
    definitions = json.loads((PROTOCOL / 'record.schema.json').read_text())['$defs']
    families = {branch['properties']['record_type']['const']
                for branch in definitions['proposal']['oneOf']}
    assert {case['family'] for case in INVENTORY['records']} == families
    for family, discriminator in (('source', 'source_role'), ('product', 'product_kind'),
                                   ('assessment', 'assessment_kind')):
        expected = set(definitions[family]['properties'][discriminator]['enum'])
        assert {case['value'] for case in INVENTORY['records']
                if case['family'] == family} == expected
    assert len({case['id'] for case in INVENTORY['records']}) == len(INVENTORY['records'])


@pytest.mark.parametrize('case', INVENTORY['decisions'], ids=lambda case: case['id'])
def test_decision_examples_are_messages_and_do_not_claim_admission(case):
    message = lc._parse_message((ROOT / case['path']).read_bytes())
    assert message['message_type'] == 'decision'
    assert message['payload']['action'] == case['action']
    assert INVENTORY['record_examples_are_committed_history'] is False


def test_inventory_scenarios_resolve_to_existing_canonical_tests():
    for scenario in INVENTORY['scenarios']:
        module, function = scenario['test'].split('::')
        assert f'def {function}(' in (ROOT / module).read_text(encoding='utf-8')
    assert INVENTORY['findings']['max_rounds'] == 3


def test_findings_fixture_reduces_without_modifying_its_bytes(monkeypatch):
    source = FIXTURES / INVENTORY['findings']['file']
    before = source.read_bytes()
    monkeypatch.setattr(findings, 'HOME', str(FIXTURES))
    monkeypatch.setattr(findings, 'MAX_ROUNDS', INVENTORY['findings']['max_rounds'])
    events = findings.load(source.stem)
    actual = findings.state(events)
    expected = json.loads((FIXTURES / 'expected-findings.json').read_text(encoding='utf-8'))
    assert set(actual) == set(expected)
    for identifier, fields in expected.items():
        assert {name: actual[identifier][name] for name in fields} == fields
    assert {item['state'] for item in actual.values()} == {
        'open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted'}
    assert source.read_bytes() == before


@pytest.mark.parametrize('change', ['data', 'sequence', 'predecessor', 'truncated'])
def test_findings_fixture_corruption_is_rejected(change):
    raw = (FIXTURES / INVENTORY['findings']['file']).read_bytes()
    events = [json.loads(line) for line in raw.splitlines()]
    altered = copy.deepcopy(events)
    if change == 'data':
        altered[0]['data']['reviewer'] = 'substituted-reviewer'
    elif change == 'sequence':
        altered[0]['seq'] = 2
    elif change == 'predecessor':
        altered[1]['prev'] = 'f' * 64
    else:
        with pytest.raises(findings.LedgerError):
            findings._parse_events(raw[:-2], 'synthetic-review')
        return
    with pytest.raises(findings.LedgerError):
        findings._parse_events(('\n'.join(json.dumps(event) for event in altered)
                                + '\n').encode(), 'synthetic-review')


def test_source_identity_preserves_versions_and_lossless_semantic_values():
    material = {'text': 'e\u0301', 'counter': 9007199254740993}
    original = lc.manifest('synthetic-input', 'delivery.source', material)
    changed = lc.manifest('synthetic-input', 'delivery.source', {**material, 'counter': 1})
    assert original['logical_id'] == changed['logical_id']
    assert lc.version_id(original) != lc.version_id(changed)
    assert lc.loads(lc.canonical(material)) == {'text': 'é', 'counter': 9007199254740993}
    assert findings.canonical('e\u0301') != findings.canonical('é')
    assert lc.canonical('e\u0301') == lc.canonical('é')
