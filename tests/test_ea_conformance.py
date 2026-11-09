# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise loss reporting at the actual exchange-file boundary."""
import copy
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.ai/runtime/tools'
spec = importlib.util.spec_from_file_location('ea_quality_conformance', TOOLS / 'ea_conformance.py')
ea = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ea)
repo = ea.repo_tool
FIXTURE = ROOT / '.ai/runtime/ea/fixtures/conformance/reference-portable.xml'


def _changed_fixture(tmp_path, change):
    document = etree.parse(str(FIXTURE))
    change(document)
    target = tmp_path / 'model.xml'
    document.write(str(target), encoding='utf-8', xml_declaration=True)
    return target


def test_portable_fixture_has_bounded_quality_claims_and_no_losses():
    result = ea.conform(FIXTURE)
    assert result['valid'], result
    assert result['l1']['scope'] == 'open-group-authored-exchange-3.1-xsd'
    assert result['qualification']['standard_conformance'] == 'not-established'
    assert result['qualification']['external_tool_interoperability'] == 'not-exercised'
    assert result['l3']['first_import_losses'] == []


@pytest.mark.parametrize('kind', ['translated-name', 'property-values', 'layout', 'organizations'])
def test_first_import_losses_are_not_hidden_by_stable_second_roundtrip(tmp_path, kind):
    def change(document):
        if kind == 'translated-name':
            element = document.find('.//' + ea.q('element'))
            name = etree.SubElement(element, ea.q('name'), {'{http://www.w3.org/XML/1998/namespace}lang': 'fr'})
            name.text = 'Client'
        elif kind == 'property-values':
            definition = etree.SubElement(document.find(ea.q('propertyDefinitions')), ea.q('propertyDefinition'), {'identifier': 'pd-multi', 'type': 'string'})
            etree.SubElement(definition, ea.q('name')).text = 'Labels'
            element = document.find('.//' + ea.q('element'))
            prop = etree.SubElement(element.find(ea.q('properties')), ea.q('property'), {'propertyDefinitionRef': 'pd-multi'})
            etree.SubElement(prop, ea.q('value')).text = 'first'
            etree.SubElement(prop, ea.q('value')).text = 'second'
        elif kind == 'layout':
            document.find('.//' + ea.q('node')).set('x', '999')
        else:
            org = etree.SubElement(document.getroot(), ea.q('organizations'))
            item = etree.SubElement(org, ea.q('item'), {'identifierRef': 'e-a'})
            etree.SubElement(item, ea.q('label')).text = 'Business'
    result = ea.conform(_changed_fixture(tmp_path, change))
    assert not result['valid'], result
    assert result['l3']['first_import_losses'], result


def test_unknown_namespaced_extension_never_satisfies_portable_conformance(tmp_path):
    target = _changed_fixture(tmp_path, lambda document: etree.SubElement(document.getroot(), '{urn:vendor:extension}payload'))
    result = ea.conform(target)
    assert not result['valid'], result
    assert result['unsupported']['unknown_elements']


@pytest.mark.parametrize('field,value', [('name', 'Renamed'), ('description', 'Changed rationale'), ('properties', {'source': 'revised'})])
def test_repository_snapshot_detects_material_fields(field, value):
    original = repo.empty_repository('test', 'Test')
    repo.import_open_exchange(FIXTURE, original)
    altered = copy.deepcopy(original)
    altered['elements'][0][field] = value
    assert ea.compare(ea.snapshot(original), ea.snapshot(altered))


def test_unknown_concept_type_is_an_error_in_exchange_check(tmp_path):
    target = _changed_fixture(tmp_path, lambda document: document.find('.//' + ea.q('element')).set('{http://www.w3.org/2001/XMLSchema-instance}type', 'InventedConcept'))
    result = ea.conform(target)
    assert not result['l2']['valid'], result
    assert any('InventedConcept' in error for error in result['l2']['errors'])


def test_property_definition_datatype_loss_is_not_a_conformance_pass(tmp_path):
    target = _changed_fixture(tmp_path, lambda document: document.find('.//' + ea.q('propertyDefinition')).set('type', 'number'))
    result = ea.conform(target)
    assert not result['valid'], result
    assert any(loss['location'].startswith('property-definition:') for loss in result['l3']['first_import_losses'])


def test_generic_graph_declares_notation_and_heuristic_viewpoint(tmp_path):
    model = repo.empty_repository('test', 'Test')
    repo.import_open_exchange(FIXTURE, model)
    view = repo.generated_view(model, 'business')
    assert view['viewpoint'] == 'Custom'
    assert view['notation'] == 'repository-graph'
    assert view['selection_status'] == 'heuristic-unreviewed'
    target = tmp_path / 'view.svg'
    repo.render_view_svg(model, view, target)
    rendered = target.read_text()
    assert 'Repository graph' in rendered
    assert 'ArchiMate notation is not asserted' in rendered


def test_exchange_helpers_preserve_canonical_values_and_report_input_errors(tmp_path):
    assert ea.canonical({'b': 2, 'a': 1}) == ea.canonical({'a': 1, 'b': 2})
    assert ea.canonical({}) == '{}'
    with pytest.raises(TypeError):
        ea.canonical({'unsupported': set()})
    target = tmp_path / 'data.json'
    target.write_text('{}')
    assert ea.load_json(target) == {}
    target.write_text('{')
    with pytest.raises(json.JSONDecodeError):
        ea.load_json(target)
    with pytest.raises(FileNotFoundError):
        ea.load_json(tmp_path / 'missing')
    module = tmp_path / 'sample.py'
    module.write_text('VALUE = 42\n')
    assert ea.load_module('test_ea_sample', module).VALUE == 42
    with pytest.raises(FileNotFoundError):
        ea.load_module('test_ea_missing', tmp_path / 'missing.py')


def test_xml_boundary_and_structural_errors(tmp_path):
    doc, errors = ea.l1(FIXTURE)
    assert errors == []
    assert ea.l2(doc) == ([], [])
    assert ea.unsupported_constructs(doc) == {'unknown_elements': [], 'unknown_attributes': []}
    target = tmp_path / 'invalid.xml'
    target.write_text('<unfinished')
    assert ea.l1(target)[0] is None
    assert ea.conform(target)['valid'] is False
    target.write_text('<wrong/>')
    assert ea.l1(target)[1]
    wrong = etree.ElementTree(etree.Element('wrong'))
    assert ea.l2(wrong)[0]


def test_cli_check_records_bounded_report_and_self_test_passes(tmp_path, capsys):
    report = tmp_path / 'report.json'
    assert ea.cmd_check(SimpleNamespace(xml=str(FIXTURE), report=str(report))) == 0
    assert json.loads(report.read_text())['qualification']['standard_conformance'] == 'not-established'
    assert ea.snapshot_from_fixture(FIXTURE)['elements']
    assert ea.self_test() == 0
    assert 'PASS' in capsys.readouterr().out
