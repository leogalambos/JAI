# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise versioned metamodel, notation and offline exchange-schema boundaries."""
import copy
import importlib.util
from pathlib import Path
import sys
from lxml import etree
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
import archimate_profile as profile

SOURCE = ROOT / '.ai/runtime/tools/repository.py'
loader = importlib.util.spec_from_file_location('profile_repository', SOURCE)
repo = importlib.util.module_from_spec(loader)
loader.loader.exec_module(repo)


def model():
    value = repo.empty_repository('profile-example', 'Profile example')
    value['projects'] = [{'id': 'P', 'name': 'Example', 'owner': 'Owner', 'status': 'delivery', 'benefits': [], 'artifacts': []}]
    value['elements'] = [{'id': ident, 'type': kind, 'name': ident, 'project_id': 'P', 'owner': 'Owner', 'lifecycle_state': 'active', 'horizon': 'current', 'properties': {}}
                         for ident, kind in [('actor', 'BusinessActor'), ('process', 'BusinessProcess'), ('data', 'BusinessObject')]]
    value['relationships'] = [{'id': 'assignment', 'type': 'Assignment', 'source': 'actor', 'target': 'process', 'project_id': 'P', 'owner': 'Owner', 'lifecycle_state': 'active'},
                              {'id': 'access', 'type': 'Access', 'source': 'process', 'target': 'data', 'access_type': 'Read', 'project_id': 'P', 'owner': 'Owner', 'lifecycle_state': 'active'}]
    return value


def test_pinned_profile_has_complete_triple_lookup_and_honest_source():
    metadata = profile.metadata()
    assert metadata['language_edition'] == '3.2'
    assert metadata['exchange_schema_version'] == '3.1'
    assert metadata['licence'] == 'MIT'
    assert profile.allowed('BusinessActor', 'Assignment', 'BusinessProcess')
    assert not profile.allowed('BusinessActor', 'Access', 'BusinessActor')
    assert not profile.allowed('Invented', 'Association', 'BusinessActor')
    assert len(profile.relationship_matrix()) == 62
    assert sum(len(codes) for targets in profile.relationship_matrix().values()
               for codes in targets.values()) == 11569


@pytest.mark.parametrize('kind', list(profile.CODES))
def test_all_relationship_families_have_legal_positive_and_illegal_negative_cases(kind):
    matrix = profile.relationship_matrix()
    positive = next((source, target) for source, targets in matrix.items()
                    for target in targets if source not in ('Junction', 'Relationship')
                    and target not in ('Junction', 'Relationship') and profile.allowed(source, kind, target))
    assert profile.allowed(positive[0], kind, positive[1])
    assert not profile.allowed('InventedConcept', kind, positive[1])
    value = model()
    value['elements'] = [dict(value['elements'][0], id='source', type=positive[0]),
                         dict(value['elements'][0], id='target', type=positive[1])]
    value['relationships'] = [dict(value['relationships'][0], source='source', target='target', type=kind)]
    assert profile.validate(value)['valid']


def test_metamodel_checks_types_attributes_and_junction_semantics():
    value = model()
    assert profile.validate(value)['valid']
    bad = copy.deepcopy(value)
    bad['relationships'][0]['type'] = 'Access'
    assert any('ILLEGAL_RELATIONSHIP' in item for item in profile.validate(bad)['errors'])
    bad = copy.deepcopy(value)
    bad['relationships'][1]['access_type'] = 'Observe'
    assert any('ACCESS_MODE' in item for item in profile.validate(bad)['errors'])
    bad = copy.deepcopy(value)
    bad['elements'].append(dict(value['elements'][0], id='junction', type='AndJunction'))
    bad['relationships'][0]['target'] = 'junction'
    bad['relationships'][1]['source'] = 'junction'
    assert any('JUNCTION' in item for item in profile.validate(bad)['errors'])


def test_junction_continuity_and_large_specialization_graph_are_checked_without_recursion():
    value = model()
    value['elements'].append(dict(value['elements'][0], id='junction', type='AndJunction'))
    value['relationships'] = [dict(value['relationships'][0], id='before', type='Triggering', source='process', target='junction'),
                              dict(value['relationships'][0], id='after', type='Triggering', source='junction', target='process')]
    assert profile.validate(value)['valid']
    value['elements'] = [dict(value['elements'][0], id='e'+str(i)) for i in range(1100)]
    value['relationships'] = [dict(value['relationships'][0], id='r'+str(i), type='Specialization', source='e'+str(i), target='e'+str(i+1)) for i in range(1099)]
    assert profile.validate(value)['valid']
    value['relationships'].append(dict(value['relationships'][0], id='cycle', source='e1099', target='e0'))
    assert any('SPECIALIZATION_CYCLE' in error for error in profile.validate(value)['errors'])


def test_version_selection_rejects_unsupported_editions():
    with pytest.raises(ValueError, match='EDITION'):
        profile.validate(model(), edition='4')


@pytest.mark.parametrize('mutation', ['duplicate-element', 'duplicate-relationship', 'cross-kind', 'empty-element', 'empty-relationship', 'missing-element', 'whitespace-relationship'])
def test_metamodel_rejects_ambiguous_or_empty_identifiers_and_cli_cannot_pass(mutation, tmp_path, monkeypatch, capsys):
    import json
    value = model()
    if mutation == 'duplicate-element':
        value['elements'].append(dict(value['elements'][0], name='Conflicting duplicate'))
    elif mutation == 'duplicate-relationship':
        value['relationships'].append(dict(value['relationships'][0], target='data'))
    elif mutation == 'cross-kind':
        value['relationships'][0]['id'] = value['elements'][0]['id']
    elif mutation == 'empty-element':
        value['elements'][0]['id'] = ''
    elif mutation == 'missing-element':
        del value['elements'][0]['id']
    else:
        value['relationships'][0]['id'] = '' if mutation == 'empty-relationship' else '  '
    result = profile.validate(value)
    assert not result['valid'], result
    assert any('IDENTIFIER' in error for error in result['errors'])
    source = tmp_path / 'ambiguous.json'
    source.write_text(json.dumps(value))
    monkeypatch.setattr(sys, 'argv', ['repository.py', 'validate-archimate', str(source)])
    with pytest.raises(SystemExit) as finished:
        repo.main()
    assert finished.value.code == 1
    assert '"valid": false' in capsys.readouterr().out


def test_association_to_relationship_retains_model_and_exchange_scope(tmp_path):
    value = model()
    value['relationships'].append(dict(value['relationships'][0], id='association',
                                       type='Association', source='data', target='assignment'))
    assert profile.validate(value)['valid']
    assert repo.validate_repository(value)[0] == []
    target = tmp_path / 'relation-target.xml'
    repo.export_open_exchange(value, target)
    restored = repo.empty_repository('restored', 'Restored')
    repo.import_open_exchange(target, restored)
    assert any(item['target'] == 'assignment' for item in restored['relationships'])
    assert profile.exchange_schema_errors(target) == []


def test_official_exchange_schema_runs_offline_and_rejects_deep_invalid_content(tmp_path):
    value = model()
    value['views'] = [repo.generated_view(value, 'business')]
    target = tmp_path / 'model.xml'
    repo.export_open_exchange(value, target)
    assert profile.exchange_schema_errors(target) == []
    document = etree.parse(str(target))
    document.find('.//{*}node').set('w', 'not-a-number')
    document.write(str(target))
    assert profile.exchange_schema_errors(target)


def test_exchange_model_version_is_distinct_from_language_and_schema_editions(tmp_path):
    value = model()
    value['repository']['version'] = '7.4'
    output = tmp_path / 'version.xml'
    repo.export_open_exchange(value, output)
    document = etree.parse(str(output))
    assert document.getroot().get('version') == '7.4'
    assert profile.exchange_schema_errors(output) == []
    restored = repo.empty_repository('restored', 'Restored')
    repo.import_open_exchange(output, restored)
    assert restored['repository']['version'] == '7.4'
    assert restored['repository']['archimate_profile'] == {
        'language_edition': '3.2', 'exchange_schema_version': '3.1',
        'profile': 'archimate-3.2-portable'}
    second = tmp_path / 'second.xml'
    repo.export_open_exchange(restored, second)
    assert etree.parse(str(second)).getroot().get('version') == '7.4'


def test_project_merge_preserves_repository_version_and_retains_source_model_version(tmp_path):
    value = model()
    value['repository']['version'] = '7.4'
    source = tmp_path / 'source.xml'
    repo.export_open_exchange(value, source)
    target = repo.empty_repository('enterprise', 'Enterprise')
    target['repository']['version'] = '2.0'
    repo.import_open_exchange(source, target, project_id='IMPORTED', merge=True)
    assert target['repository']['version'] == '2.0'
    export = tmp_path / 'project.xml'
    assert repo.index_by(target['projects'])['IMPORTED']['source_model_version'] == '7.4'
    repo.export_open_exchange(target, export)
    assert etree.parse(str(export)).getroot().get('version') == '2.0'
    repo.export_open_exchange(target, export, project='P')
    assert etree.parse(str(export)).getroot().get('version') == '7.4'


def test_viewpoint_contract_requires_concern_and_traceable_scope():
    value = model()
    view = repo.generated_view(value, 'business')
    assert profile.validate_viewpoint(value, view)['status'] == 'REVIEW_PENDING'
    view['viewpoint_contract'] = {
        'stakeholders': ['Service owner'], 'concerns': ['Who performs the purchase process?'],
        'decision': 'Assign accountable performers', 'boundary': 'Purchase service',
        'included_types': ['BusinessActor', 'BusinessProcess', 'BusinessObject'],
        'completeness_criteria': ['All in-scope process performers are linked'],
        'exclusions': [], 'review_status': 'pending'}
    assert profile.validate_viewpoint(value, view)['structurally_complete']
    view['element_refs'].append('absent')
    assert not profile.validate_viewpoint(value, view)['structurally_complete']


def test_viewpoint_contract_survives_exchange_and_generated_presets_are_explicit(tmp_path):
    value = model()
    view = repo.generated_view(value, 'business')
    assert view['viewpoint_contract']['concerns']
    assert view['viewpoint_contract']['review_status'] == 'pending'
    value['views'] = [view]
    output = tmp_path / 'view.xml'
    repo.export_open_exchange(value, output)
    restored = repo.empty_repository('restored', 'Restored')
    repo.import_open_exchange(output, restored)
    assert restored['views'][0]['viewpoint_contract'] == view['viewpoint_contract']


def test_render_honours_exact_empty_relationship_selection(tmp_path):
    value = model()
    view = repo.generated_view(value, 'business')
    view['relationship_refs'] = []
    output = tmp_path / 'no-edges.svg'
    result = profile.render(value, view, output)
    assert result['status'] == 'DRAFT_NOTATION'
    document = etree.parse(str(output))
    assert not document.xpath('//*[local-name()="text" and (text()="Assignment" or text()="Access")]')
    assert not document.xpath('//*[local-name()="path" and @marker-start]')
    assert view['relationship_refs'] == []


@pytest.mark.parametrize('problem', ['missing', 'outside-view'])
def test_viewpoint_and_renderer_reject_invalid_relationship_scope(problem, tmp_path):
    value = model()
    view = repo.generated_view(value, 'business')
    if problem == 'missing':
        view['relationship_refs'] = ['missing']
    else:
        view['element_refs'].remove('data')
        view['relationship_refs'] = ['access']
    checked = profile.validate_viewpoint(value, view)
    assert not checked['structurally_complete'], checked
    assert any('RELATIONSHIP' in error for error in checked['errors'])
    output = tmp_path / 'invalid.svg'
    with pytest.raises(ValueError, match='NOTATION_VIEW'):
        profile.render(value, view, output)
    assert not output.exists()


def test_selected_association_to_relationship_is_rendered_at_its_anchor(tmp_path):
    value = model()
    value['relationships'].append(dict(value['relationships'][0], id='annotation', type='Association', source='data', target='assignment'))
    view = repo.generated_view(value, 'business')
    view['relationship_refs'] = ['assignment', 'annotation']
    assert profile.validate_viewpoint(value, view)['structurally_complete']
    output = tmp_path / 'association.svg'
    result = profile.render(value, view, output)
    assert result['relationships'] == 2
    document = etree.parse(str(output))
    assert document.xpath('//*[local-name()="path" and @data-relationship-id="annotation"]')
    assert document.xpath('//*[local-name()="text" and text()="Association"]')


def test_selected_self_relationship_has_visible_nonzero_loop(tmp_path):
    value = model()
    value['relationships'] = [dict(value['relationships'][0], id='loop', source='process', target='process', type='Triggering')]
    view = repo.generated_view(value, 'business')
    output = tmp_path / 'loop.svg'
    assert profile.render(value, view, output)['relationships'] == 1
    document = etree.parse(str(output))
    path = document.xpath('//*[local-name()="path" and @data-relationship-id="loop"]')[0]
    assert 'C' in path.get('d')


@pytest.mark.parametrize('name', [
    'Enterprise customer account and entitlement administration business owner',
    'CustomerEvidenceProcessingRestrictionVersionIdentifierWithoutAnyWordBreaks0123456789',
    'e\u0301' * 40,
    'α' * 40,
    'Café e\u0301vidence α→β ★ ' + 'Ｗ' * 24 + ' customer-processing restriction'])
def test_long_node_labels_wrap_losslessly_and_resize_layout(name, tmp_path):
    value = model()
    value['elements'][0]['name'] = name
    value['elements'][1]['name'] = 'Validate cross-border customer onboarding and regulated service eligibility requirements'
    view = repo.generated_view(value, 'business')
    view['name'] = 'Illustrative enterprise operations dependency and regulatory evidence traceability view ' * 2
    output = tmp_path / 'long.svg'
    profile.render(value, view, output)
    document = etree.parse(str(output))
    groups = {item.get('data-element-id'): item for item in document.xpath('//*[local-name()="g" and @data-element-id]')}
    assert set(groups) == {'actor', 'process', 'data'}
    actor = groups['actor']
    assert actor.find('{http://www.w3.org/2000/svg}title').text == name
    label = actor.xpath('./*[local-name()="text" and @class="element-name"]')[0]
    spans = label.findall('{http://www.w3.org/2000/svg}tspan')
    assert len(spans) > 1
    assert ''.join(span.text or '' for span in spans) == name
    import unicodedata
    assert all(sum(0 if unicodedata.combining(char) else 2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1
                   for char in span.text or '') <= 24 for span in spans)
    assert all(not unicodedata.combining((span.text or ' ')[0]) for span in spans)
    assert actor.get('aria-label') == name
    rect = actor.find('{http://www.w3.org/2000/svg}rect')
    assert float(rect.get('height')) > 80
    assert max(float(span.get('y')) for span in spans) < float(rect.get('y')) + float(rect.get('height')) - 20
    next_row = groups['data'].find('{http://www.w3.org/2000/svg}rect')
    assert float(next_row.get('y')) > float(rect.get('y')) + float(rect.get('height')) + 60
    heading = document.xpath('//*[local-name()="text" and @class="view-name"]')[0]
    assert ''.join(heading.itertext()) == view['name']
    assert len(heading.findall('{http://www.w3.org/2000/svg}tspan')) > 1


def test_notation_renderer_distinguishes_relationships_and_refuses_unqualified_symbols(tmp_path):
    value = model()
    view = repo.generated_view(value, 'business')
    target = tmp_path / 'notation.svg'
    result = profile.render(value, view, target)
    assert result['status'] == 'DRAFT_NOTATION'
    text = target.read_text()
    assert 'Assignment' in text and 'Access' in text
    assert 'marker-start=' in text and 'stroke-dasharray=' in text
    assert 'marker-start="url(#open-start)"' in text
    assert 'semantic and visual review pending' in text
    value['elements'][0]['type'] = 'UnknownElement'
    with pytest.raises(ValueError, match='NOTATION'):
        profile.render(value, view, target)


def test_profile_cli_and_repository_cli_are_explicit_and_do_not_mutate_source(tmp_path, monkeypatch, capsys):
    import json
    value = model()
    value['views'] = [repo.generated_view(value, 'business')]
    path = tmp_path / 'source.json'
    path.write_text(json.dumps(value))
    original = path.read_bytes()
    assert profile.main(['validate', str(path)]) == 0
    assert profile.main(['render', str(path), '--view', value['views'][0]['id'], '--out', str(tmp_path / 'profile.svg')]) == 0
    monkeypatch.setattr(sys, 'argv', ['repository.py', 'validate-archimate', str(path)])
    with pytest.raises(SystemExit) as finished:
        repo.main()
    assert finished.value.code == 0
    monkeypatch.setattr(sys, 'argv', ['repository.py', 'render-archimate', str(path), '--view', value['views'][0]['id'], '--out', str(tmp_path / 'repository.svg')])
    repo.main()
    assert path.read_bytes() == original
    assert (tmp_path / 'repository.svg').is_file()
    assert 'DRAFT_NOTATION' in capsys.readouterr().out


def test_sabsa_projection_declares_language_exchange_and_mapping_basis(tmp_path):
    import sabsa_ea as bridge
    mapping = bridge.mapping()
    assert mapping['target_language_edition'] == '3.2'
    assert mapping['exchange_schema_version'] == '3.1'
    assert mapping['reference_mapping']['target_edition'] == '3.0'
    entries = {'BD-1': {'id': 'BD-1', 'title': 'Business driver', 'owner': 'Owner', '_dirtype': 'driver'}}
    value = repo.empty_repository('example', 'Example')
    manifest = bridge.project_entries(entries, value, 'P', 'Project', 'Owner')
    assert manifest['target_profile']['language_edition'] == '3.2'
    assert value['elements'][0]['properties']['JAI.ArchiMateEdition'] == '3.2'
    target = tmp_path / 'mapping.xml'
    repo.export_open_exchange(value, target)
    restored = repo.empty_repository('restored', 'Restored')
    repo.import_open_exchange(target, restored)
    assert restored['elements'][0]['properties']['JAI.MappingSourceEdition'] == '3.0'
    assert bridge.validate_mapping() == []
    assert bridge.self_test() == 0
