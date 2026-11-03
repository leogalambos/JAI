# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Guard corrected public authority, schema and onboarding contracts."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_current_fabric_reference_excludes_retired_mutation_commands():
    text = (ROOT/'docs/reference/runtime-tools-detailed.md').read_text()
    section = text.split('#### `fabric.py`', 1)[1].split('#### `demo.py`', 1)[0]
    assert 'current-basis ENGAGEMENT --query QUERY.json' in section
    assert 'validate --message MESSAGE.json' in section
    assert 'usage: fabric.py init' not in section
    assert 'archive' in section.lower()


def test_protocol_table_includes_required_coordination_fields():
    text = (ROOT/'docs/reference/governed-delivery-protocol.md').read_text()
    rows = {line.split('|')[1].strip(): line for line in text.splitlines() if line.startswith('| `')}
    assert '`scheduling:' in rows['`profile`']
    assert '`speculation:' in rows['`context`']
    assert '`ready_basis:' in rows['`context`']


def test_onboarding_has_current_criteria_and_external_authority_boundary():
    for name in ['installed-cli-guide.md', 'command-walkthroughs.md']:
        text = (ROOT/'docs/reference'/name).read_text()
        assert 'invoice-service/.claude/review-criteria.md' not in text
        assert 'invoice-service/.ai/review-criteria.md' in text
        assert '#### C9 Money handling' not in text
    text = (ROOT/'docs/reference/installed-cli-guide.md').read_text()
    assert 'Switch to the default mode' not in text
    assert 'Nothing\nelse needs setting up' not in text
    assert 'reviewers never see this guide' not in text


def test_artifact_contract_fields_are_not_sabsa_layers():
    text = (ROOT/'docs/capabilities/artifacts-publication.md').read_text()
    assert '| JAI layer |' not in text
    schema = json.loads((ROOT/'.ai/runtime/artifacts/schema/artifact-contract-v3.schema.json').read_text())
    for field in ['intent', 'semantics', 'justification', 'design', 'realisation', 'evidence']:
        assert field in schema['properties']['jai']['required']
        assert f'`{field}`' in text


def test_current_operator_pages_allow_observed_native_office_qa_before_operator_route():
    pages = ['using/interaction-model.md', 'reference/command-walkthroughs.md',
             'reference/commands.md', 'reference/runtime-tools-detailed.md']
    for name in pages:
        text = (ROOT/'docs'/name).read_text()
        assert 'Actual Office QA is OPERATOR_ASSISTED' not in text, name
        assert 'route A when a working native Office renderer is available' in text, name
        assert 'route C through the operator when required' in text, name
        assert 'external Ed25519 receipts require' in text, name
