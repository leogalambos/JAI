# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Audit observes exact Gen2 facts without granting or rewriting anything."""
import json
import os
from pathlib import Path
import sys

import pytest

from governed_fixtures import GovernedHarness, HUMAN

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import governed_audit as audit
import lifecycle as lc
import provider_projection as projection


def _host(tmp_path, monkeypatch, **kwargs):
    host = GovernedHarness(tmp_path, monkeypatch, **kwargs)
    host.bootstrap()
    return host


def test_report_uses_one_captured_snapshot_and_keeps_permission_facts_distinct(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch)
    _, subject, proof = host.qualified_answer()
    host.accept(subject)
    host.accept(subject, release=True)
    original_read = host.store.read
    captured = original_read()
    before = host.path.read_bytes()
    calls = []
    def read_once():
        calls.append(True)
        return captured
    monkeypatch.setattr(host.store, 'read', read_once)
    result = audit.report(host.store)
    assert len(calls) == 1
    assert result['head'] == captured.head and result['history_verified']
    output, = result['outputs']
    assert output['subject'] == {'ref': subject, 'use_scope': host.scope}
    assert output['basis']['qualified'] and output['basis']['accepted'] and output['basis']['release_eligible']
    assert output['required_proofs'][0]['proof'] == {'ref': proof, 'use_scope': host.scope}
    assert output['decisions'] and output['inputs'] and all(item['status'] == 'available' for item in output['material'])
    assert result['authority_granted'] is False and result['read_only']
    rendered = audit.format_report(result)
    assert subject['version_id'] in rendered and 'release permission=True' in rendered
    assert 'this report grants none' in rendered
    assert host.path.read_bytes() == before
    with pytest.raises(KeyError):
        audit.format_report({})


def test_owner_update_reports_cancelled_old_basis_and_missing_current_review_without_fallback(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch)
    _, old, _ = host.qualified_answer()
    host.accept(old)
    host.accept(old, release=True)
    _, input_a, input_b = host.transition_inputs('Updated service requirements B.', remove_old_material=True)
    actor = host.setup_author(suffix='B')
    current, record = host.product('current-unreviewed', actor)
    host.commit(host.submission(actor, current, record))
    before = host.path.read_bytes()
    previous = audit.report(host.store, old)
    output, = previous['outputs']
    assert not output['basis']['qualified'] and not output['basis']['accepted'] and not output['basis']['release_eligible']
    assert output['cancellations'] and any(item['relationship'] == 'direct' for item in output['cancellations'])
    assert any(input_a == item['point']['ref'] for item in output['inputs'])
    assert any(item['payload'].get('reason') for item in output['decisions'])
    pending = audit.report(host.store, {'ref': current, 'use_scope': 'default'})
    output, = pending['outputs']
    assert not output['basis']['qualified'] and not output['basis']['accepted']
    assert any(item['status'] == 'missing' for item in output['required_proofs'])
    assert any(input_b == item['point']['ref'] for item in output['inputs'])
    assert pending['governing_inputs'] != previous['outputs'][0]['inputs']
    assert input_b in [item['ref'] for item in pending['governing_inputs']]
    assert input_a not in [item['ref'] for item in pending['governing_inputs']]
    default = audit.report(host.store)
    assert default['outputs'] == [], 'A cancelled slot pointer is not a current output or fallback.'
    old_slot = next(item for item in default['inventory'] if item['point']['ref'] == old)
    assert old_slot['selected_slot'] and not old_slot['current_selected']
    explanation = old_slot['unusable_selection']
    assert explanation['reason'].startswith('No current basis:')
    assert any({'ref': old, 'use_scope': host.scope} in item['affected'] for item in explanation['cancellations'])
    assert any(item['payload'].get('reason') == 'Explicit approved governing input revision'
               for item in explanation['decisions'])
    assert 'Explicit approved governing input revision' in audit.format_report(default)
    assert host.path.read_bytes() == before


def test_required_material_gap_does_not_confuse_history_integrity_or_unrelated_inventory(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch)
    _, subject, _ = host.qualified_answer()
    obsolete_blob = host.material('Unselected historical note outside this output closure.')
    host.record('historical-note', 'source', {'owner': HUMAN, 'source_role': 'input', 'origin': HUMAN,
                'material': [obsolete_blob], 'criteria': [], 'inherited': []})
    (host.store.material / obsolete_blob).unlink()
    unrelated = audit.report(host.store, subject)
    assert unrelated['history_verified'] and unrelated['outputs'][0]['basis']['qualified']
    needed = host.store.read().resolve(subject, 'product')['material'][0]
    (host.store.material / needed).unlink()
    before = host.path.read_bytes()
    missing = audit.report(host.store, subject)
    assert missing['history_verified'] and not missing['outputs'][0]['basis']['qualified']
    assert any(item['blob_id'] == needed and item['status'] == 'unavailable'
               for item in missing['outputs'][0]['material'])
    assert obsolete_blob not in [item['blob_id'] for item in missing['outputs'][0]['material']]
    assert host.path.read_bytes() == before


def test_no_selection_and_ambiguous_versions_never_infer_a_current_subject(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch)
    empty = audit.report(host.store)
    assert empty['outputs'] == [] and empty['inventory'] == []
    actor = host.setup_author(suffix='first')
    first, first_record = host.product('coexisting', actor, material=[host.material('First candidate.')])
    host.commit(host.submission(actor, first, first_record))
    other_actor = host.setup_author(suffix='second')
    second, second_record = host.product('coexisting', other_actor, material=[host.material('Different candidate.')])
    host.commit(host.submission(other_actor, second, second_record))
    before = host.path.read_bytes()
    ambiguous = audit.report(host.store, 'coexisting')
    assert ambiguous['status'] == 'ambiguous' and ambiguous['outputs'] == []
    assert {item['ref']['version_id'] for item in ambiguous['selector_candidates']} == {first['version_id'], second['version_id']}
    assert audit.report(host.store, second['version_id'])['outputs'][0]['subject']['ref'] == second
    assert audit.report(host.store)['outputs'] == []
    assert audit.report(host.store, 'absent')['status'] == 'not-found'
    with pytest.raises(lc.ERROR):
        audit.report(host.store, first, scope='unknown')
    assert host.path.read_bytes() == before


def test_scope_cancellations_do_not_cross_to_independently_justified_use(tmp_path, monkeypatch):
    host = _host(tmp_path, monkeypatch, use_scopes=('default', 'retained'))
    _, old, _ = host.qualified_answer(suffix='default')
    host.accept(old)
    host.accept(old, release=True)
    host.enter_scope('retained')
    _, retained, _ = host.qualified_answer(suffix='retained')
    host.accept(retained)
    host.accept(retained, release=True)
    host.enter_scope('default')
    host.transition_inputs('Changed default scope only.')
    before = host.path.read_bytes()
    result = audit.report(host.store, {'ref': retained, 'use_scope': 'retained'}, scope='retained')
    output, = result['outputs']
    assert output['basis']['release_eligible'] and output['cancellations'] == []
    assert result['scope'] == 'retained' and result['available_scopes'] == ['default', 'retained']
    assert all(item['proof']['use_scope'] == 'retained' for item in output['required_proofs'] if item['proof'])
    assert host.path.read_bytes() == before


def test_cli_newest_locator_and_failures_are_read_only(tmp_path, monkeypatch, capsys):
    absent = tmp_path / 'not-created'
    assert audit.main(['--home', str(absent), '--json']) == 2
    assert json.loads(capsys.readouterr().out)['history_verified'] is False
    assert not absent.exists()
    older = _host(tmp_path, monkeypatch, engagement='older')
    newer = _host(tmp_path, monkeypatch, engagement='newer')
    os.utime(older.path, ns=(1, 1))
    before = {path.name: path.read_bytes() for path in tmp_path.glob('*.jsonl')}
    assert audit.main(['--home', str(tmp_path), '--json']) == 0
    value = json.loads(capsys.readouterr().out)
    assert value['engagement'] == newer.engagement and value['outputs'] == []
    assert {path.name: path.read_bytes() for path in tmp_path.glob('*.jsonl')} == before
    newer.path.write_text('{"format": 1}\n')
    corrupt = newer.path.read_bytes()
    assert audit.main(['newer', '--home', str(tmp_path), '--json']) == 2
    failed = json.loads(capsys.readouterr().out)
    assert failed['status'] == 'unavailable' and not failed['history_verified'] and not failed['outputs']
    assert newer.path.read_bytes() == corrupt
    assert audit.main(['../escape', '--home', str(tmp_path)]) == 2


def test_restored_command_and_independent_auditor_share_provider_projections():
    registry = json.loads((ROOT / '.ai/runtime/models/model-registry.json').read_bytes())
    command = ROOT / '.ai/commands/fabric-report.md'
    auditor = ROOT / '.ai/agents/fabric-auditor.md'
    codex_command = projection.render_codex_skill(command, 'command', 'fabric-report', registry).decode()
    codex_agent = projection.render_codex_skill(auditor, 'agent', 'fabric-auditor', registry).decode()
    claude_agent = projection.render_claude_agent(auditor, registry).decode()
    assert 'name: workflow-fabric-report' in codex_command
    assert 'name: agent-fabric-auditor' in codex_agent
    assert projection.split_frontmatter(auditor.read_text())[1] in codex_agent
    assert projection.split_frontmatter(claude_agent)[0]['tools'] == 'Read, Grep, Glob'
    assert 'Never select, sign, submit, accept or release' in codex_agent
    assert 'governed_audit.py' in codex_command
