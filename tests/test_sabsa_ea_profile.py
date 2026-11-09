# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Check edition-bound SABSA projection through actual local files and CLI routes."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import sabsa_ea as bridge


def test_projection_hashes_ignore_only_nonsemantic_bookkeeping(tmp_path):
    source = {'id': 'BD-001', 'title': 'Driver', 'owner': 'Owner', '_dirtype': 'driver', '_path': 'private', 'status': 'draft'}
    assert bridge.semantic_payload(source) == {'id': 'BD-001', 'title': 'Driver', 'owner': 'Owner'}
    assert bridge.semantic_hash(source) == bridge.semantic_hash(dict(source, status='reviewed', _path='other'))
    assert bridge.semantic_hash(source) != bridge.semantic_hash(dict(source, title='Different'))
    assert bridge.canonical({'b': 2, 'a': 1}) == bridge.canonical({'a': 1, 'b': 2})
    assert bridge.sha({}) == hashlib.sha256(bridge.canonical({})).hexdigest()
    assert bridge.projected_snapshot({}) == bridge.projected_snapshot({})
    assert bridge.projected_snapshot({'BD-001': source}) != bridge.projected_snapshot({})
    assert bridge.mapping_hash() != bridge.mapping_hash({'mapping_version': 'changed'})
    path = tmp_path / 'source.json'
    path.write_text('{}')
    assert bridge.load_json(path) == {}
    with pytest.raises(FileNotFoundError):
        bridge.load_json(tmp_path / 'missing')
    path.write_text('{')
    with pytest.raises(json.JSONDecodeError):
        bridge.load_json(path)
    module = tmp_path / 'tiny.py'; module.write_text('VALUE = 3\n')
    assert bridge.load_module('projection_test_source', module).VALUE == 3
    with pytest.raises(FileNotFoundError):
        bridge.load_module('missing_source', tmp_path / 'missing.py')


def test_stable_ids_and_projection_detect_actual_source_or_mapping_changes():
    assert bridge.ea_id('') == 'sabsa-id-'
    assert bridge.ea_id('01 café').startswith('sabsa-id-')
    assert bridge.ea_id('X' * 200) == bridge.ea_id('X' * 200)
    assert bridge.ea_id('X' * 200) != bridge.ea_id('X' * 199 + 'Y')
    assert bridge.rel_id('source', 'field', 'target') != bridge.rel_id('source', 'field', 'other')
    source = {'id': 'BD-001', 'title': 'Driver', 'owner': 'Owner', '_dirtype': 'driver'}
    entry = bridge.element_from('BD-001', source, bridge.mapping()['rules']['driver'], 'P', bridge.mapping()['mapping_version'])
    assert entry['properties']['JAI.ArchiMateEdition'] == '3.2'
    assert entry['source']['stable_id'] == 'BD-001'
    repository = bridge.repo_tool.empty_repository('example', 'Example')
    entries = {'BD-001': source}
    bridge.project_entries(entries, repository, 'P', 'Project', 'Owner')
    assert bridge.check_projection(entries, repository, 'P')['valid']
    assert not bridge.check_projection({'BD-001': dict(source, title='Different')}, repository, 'P')['valid']
    assert bridge.check_projection({}, repository, 'P')['orphan'] == ['BD-001']
    with pytest.raises(ValueError, match='unmapped'):
        bridge.project_entries({'X': dict(source, _dirtype='unknown')}, repository, 'P', 'Project', 'Owner')


def test_project_check_and_mapping_cli_use_real_library_and_repository(tmp_path, capsys):
    library = tmp_path / 'library'
    bridge.sabsa.cmd_init(SimpleNamespace(lib=str(library), name='Test', organisation='Example', scope='Synthetic', owner='Owner'))
    repository = tmp_path / 'repository'
    args = SimpleNamespace(lib=str(library), repo=str(repository), project_id='P', project_name='Project', owner='Owner', repository_id='example', repository_name='Example')
    assert bridge.cmd_project(args) == 0
    assert bridge.cmd_check(args) == 0
    assert bridge.cmd_mapping(SimpleNamespace()) == 0
    assert bridge.repo_tool.resolve_repo(repository).is_file()
    assert '"target_profile"' in capsys.readouterr().out
