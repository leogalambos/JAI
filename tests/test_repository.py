# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Check repository identities, typed properties and real exchange/view operations."""
import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('quality_repository', ROOT / '.ai/runtime/tools/repository.py')
repository = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repository)
FIXTURE = ROOT / '.ai/runtime/ea/fixtures/conformance/reference-portable.xml'


@pytest.mark.parametrize('text,expected', [('False', False), ('True', True), ('false', False), ('true', True), ('null', None), ('[]', []), ('{}', {}), ('plain', 'plain'), ('[broken', '[broken'), ('', '')])
def test_property_values_retain_type_across_legacy_boolean_spellings(text, expected):
    assert repository.parse_maybe_json(text) == expected
    assert type(repository.parse_maybe_json(text)) is type(expected)


def test_repository_identity_hash_and_file_boundary(tmp_path):
    model = repository.empty_repository('example', 'Example')
    assert repository.now_utc().endswith('Z')
    assert 'updated_at' not in repository.repository_payload(model)['repository']
    before = repository.repository_hash(model)
    repository.touch(model)
    assert repository.repository_hash(model) == before
    path = repository.save_repo(tmp_path / 'model', model)
    assert repository.resolve_repo(tmp_path / 'model') == path
    assert repository.load_repo(path)[1] == model
    assert repository.load_json(path) == model
    target = tmp_path / 'unicode.json'
    repository.write_json(target, {'title': 'Café'})
    assert repository.load_json(target) == {'title': 'Café'}
    assert repository.canonical({'b': 2, 'a': 1}) == repository.canonical({'a': 1, 'b': 2})
    with pytest.raises(SystemExit, match='repository not found'):
        repository.load_repo(tmp_path / 'missing.json')
    target.write_text('{')
    with pytest.raises(json.JSONDecodeError):
        repository.load_json(target)


def test_index_replacement_and_empty_selection_helpers():
    values = []
    repository.upsert(values, {'id': 'x', 'name': 'Initial'})
    repository.upsert(values, {'id': 'x', 'name': 'Updated'})
    assert repository.index_by(values) == {'x': {'id': 'x', 'name': 'Updated'}}
    assert repository.index_by([]) == {}
    assert repository.split_csv(None) == []
    assert repository.split_csv('x, y,,') == ['x', 'y']
    assert repository.local_name(repository.q('element')) == 'element'
    assert repository.type_group('ApplicationComponent') == 'application'
    assert repository.type_group('Unknown') == 'other'


def test_xml_property_roundtrip_preserves_source_and_false():
    parent = ET.Element(repository.q('element'))
    repository.add_text(parent, 'name', 'Café', 'en')
    assert repository.child_text(parent, 'name') == 'Café'
    assert repository.child_text(parent, 'missing', 'fallback') == 'fallback'
    assert repository.first_child(parent, 'name').get(repository.xml_lang()) == 'en'
    assert len(repository.children(parent, 'name')) == 1
    assert repository.first_child(parent, 'missing') is None
    assert repository.xsi_type().endswith('}type')
    repository.add_properties(parent, {'custom': ['a'], 'AIITHouse.IncludeRetired': False}, {'custom': 'p1', 'AIITHouse.IncludeRetired': 'p2'}, 'en')
    props = repository.prop_map_from_xml(parent, {'p1': 'custom', 'p2': 'AIITHouse.IncludeRetired'})
    assert repository.pop_ai_properties(props) == {'AIITHouse.IncludeRetired': False}
    assert repository.non_ai_properties(props) == {'custom': ['a']}
    assert repository.archi_properties_for_element({'id': 'e'})['AIITHouse.RepositoryId'] == 'e'
    assert repository.archi_properties_for_relationship({'id': 'r'})['AIITHouse.RepositoryId'] == 'r'
    assert repository.archi_properties_for_view({'id': 'v', 'include_retired': False})['AIITHouse.IncludeRetired'] is False


def test_real_import_export_graph_and_lifecycle_boundaries(tmp_path):
    model = repository.empty_repository('example', 'Example')
    repository.import_open_exchange(FIXTURE, model)
    assert repository.validate_repository(model)[0] == []
    assert model['views'][0]['include_retired'] is False
    with pytest.raises(ValueError, match='not empty'):
        repository.import_open_exchange(FIXTURE, model)
    output = tmp_path / 'export.xml'
    repository.export_open_exchange(model, output)
    imported = repository.empty_repository('roundtrip', 'Round trip')
    repository.import_open_exchange(output, imported)
    assert imported['views'][0]['include_retired'] is False
    views = repository.generate_views(model, tmp_path / 'views', None, 'all')
    assert views and (tmp_path / 'views/view-set.json').is_file()
    assert repository.generated_view(model, 'business')['element_refs']
    repository.render_view_svg(model, views[0], tmp_path / 'graph.svg')
    assert 'Repository graph' in (tmp_path / 'graph.svg').read_text()
    assert repository.impact(model, 'e-a')['outbound'][0]['id'] == 'r-1'
    data = repository.portfolio_data(model)
    assert data['projects']
    assert 'Example' in repository.portfolio_markdown(data)
    repository.set_lifecycle(model, 'e-p', 'retiring', 'Owner', '2026-11-08')
    with pytest.raises(ValueError, match='active dependencies'):
        repository.decommission(model, 'e-p', 'Owner', '2026-11-08')
    assert model['elements'][1]['lifecycle_state'] == 'retiring'
    with pytest.raises(ValueError, match='unknown'):
        repository.impact(model, 'missing')


def test_repository_self_test(capsys):
    assert repository.self_test() == 0
    assert 'PASS' in capsys.readouterr().out


def test_repository_self_test_accepts_semantically_equivalent_namespace_prefixes(monkeypatch, capsys):
    # Other XML producers share ElementTree's process-global prefix registry.
    # Isolate that mutable registry, then exercise real export/import semantics.
    monkeypatch.setattr(ET, '_namespace_map', dict(ET._namespace_map))
    ET.register_namespace('exchange', repository.ARCHI_NS)
    ET.register_namespace('schema', repository.XSI_NS)
    assert repository.self_test() == 0
    result = capsys.readouterr().out
    assert '20/20 PASS' in result
    assert 'FAIL ' not in result


def test_generated_view_qualification_survives_real_exchange_roundtrip(tmp_path):
    model = repository.empty_repository('example', 'Example')
    repository.import_open_exchange(FIXTURE, model)
    model['views'] = [repository.generated_view(model, 'business')]
    output = tmp_path / 'qualified.xml'
    repository.export_open_exchange(model, output)
    restored = repository.empty_repository('restored', 'Restored')
    repository.import_open_exchange(output, restored)
    for field in ('notation', 'selection_profile', 'selection_status'):
        assert restored['views'][0].get(field) == model['views'][0][field]
