# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Protect complete workflow labels, figure ownership and readable SVG geometry."""
from pathlib import Path
import importlib.util
import json
import re
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('workflow_diagrams', ROOT / 'tools/generate_workflow_diagrams.py')
diagrams = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagrams)
NS = {'svg': 'http://www.w3.org/2000/svg'}


def test_every_canonical_workflow_activity_is_complete_and_inside_its_node():
    workflows = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())['workflows']
    for workflow in workflows:
        svg = ET.fromstring(diagrams.render_workflow(workflow))
        nodes = svg.findall('svg:g', NS)
        assert len(nodes) == len(workflow['steps'])
        for step, node in zip(workflow['steps'], nodes):
            texts = node.findall('svg:text', NS)
            visible = ' '.join(text.text for text in texts)
            expected = f"{step['step']}. {step['role']} {step['does']}"
            assert re.sub(r'\s*/\s*', '/', visible) == re.sub(r'\s*/\s*', '/', expected)
            box = node.find('svg:rect', NS)
            assert all(float(box.attrib['y']) < float(text.attrib['y'])
                       < float(box.attrib['y']) + float(box.attrib['height'])
                       for text in texts)
            assert all(int(text.attrib['font-size']) >= 16 for text in texts)


def test_empty_or_nonconsecutive_workflow_steps_are_rejected():
    for steps in ([], [{'step': 2, 'role': 'Author', 'does': 'creates an output'}]):
        with pytest.raises(ValueError, match='consecutively numbered'):
            diagrams.render_workflow({'key': 'example', 'title': 'Example',
                                      'outcome': 'An explicit output', 'steps': steps})


def test_owned_figure_replacement_preserves_manual_content_and_rejects_bad_markers():
    source = 'Introduction\n' + diagrams.START + '\nOld figure\n' + diagrams.END + '\nTable\n'
    result = diagrams.replace_figure(source, 'New figure')
    assert result == 'Introduction\n' + diagrams.START + '\nNew figure\n' + diagrams.END + '\nTable\n'
    assert diagrams.replace_figure(result, 'New figure') == result
    for invalid in ('', diagrams.END + diagrams.START, source + diagrams.START):
        with pytest.raises(ValueError, match='marker pair'):
            diagrams.replace_figure(invalid, 'New figure')


def test_cli_generation_and_check_mode_keep_manual_text_and_detect_source_drift(tmp_path):
    source = tmp_path / '.ai/runtime/workflows.json'
    source.parent.mkdir(parents=True)
    workflow = {'key': 'example', 'title': 'Example', 'outcome': 'A reviewed output',
                'steps': [{'step': 1, 'role': 'Author', 'does': 'creates the requested output with evidence'}]}
    source.write_text(json.dumps({'workflows': [workflow]}))
    page = tmp_path / 'docs/workflow-library/example.md'
    page.parent.mkdir(parents=True)
    page.write_text('Intro\n' + diagrams.START + '\nOld\n' + diagrams.END + '\nTable\n')
    assert diagrams.main(['--root', str(tmp_path)]) == 0
    before = {str(p.relative_to(tmp_path)): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    assert diagrams.generate(tmp_path, check=True) == 0
    assert page.read_text().startswith('Intro\n') and page.read_text().endswith('\nTable\n')
    assert '<ol class="ai-workflow-steps" role="list"' in page.read_text()
    assert '<svg' not in page.read_text()
    assert '<strong>Author</strong>' in page.read_text()
    assert 'Open the full-size workflow diagram' in page.read_text()
    assert 'Follow the numbered order' in page.read_text()
    assert before == {str(p.relative_to(tmp_path)): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    workflow['steps'][0]['does'] = 'creates a revised output with its new evidence'
    source.write_text(json.dumps({'workflows': [workflow]}))
    unchanged = page.read_bytes()
    assert diagrams.generate(tmp_path, check=True) == 1
    assert page.read_bytes() == unchanged
    assert diagrams.generate(tmp_path) == 0
    assert 'revised output' in page.read_text()


def test_concept_diagrams_identify_current_layers_conditions_and_separate_permissions():
    assets = diagrams.concept_diagrams()
    for name, content in assets.items():
        svg = ET.fromstring(content)
        assert svg.find('svg:title', NS).text
        assert svg.find('svg:desc', NS).text
    layers = ' '.join(' '.join(ET.fromstring(assets['layered-runtime-cycle.svg']).itertext()).split())
    for label in ('L0: external human authority', 'L1 Contextual', 'L2 Conceptual',
                  'L3 Logical', 'L4 Physical', 'L5 Component', 'L6 Management'):
        assert label in layers
    assert 'crosscutting' in layers
    contract = ' '.join(' '.join(ET.fromstring(assets['gen2-effective-output-contract.svg']).itertext()).split())
    for label in ('Condition = true', 'Condition = false', 'Condition = unknown'):
        assert label in contract
    lifecycle = ' '.join(' '.join(ET.fromstring(assets['gen2-input-applicability.svg']).itertext()).split())
    for label in ('Continue work', 'Accept this output', 'Permit release', 'no inherited PASS'):
        assert label in lifecycle


def test_primary_workflow_overviews_preserve_all_stages_as_ordered_readable_text():
    workflows = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())['workflows']
    for workflow in workflows:
        page = (ROOT / 'docs/workflow-library' / (workflow['key'] + '.md')).read_text()
        block = re.search(r'<ol class="ai-workflow-steps".*?</ol>', page, re.S)
        assert block is not None
        overview = ET.fromstring(block.group(0))
        items = overview.findall('li')
        assert len(items) == len(workflow['steps'])
        for item, step in zip(items, workflow['steps']):
            assert item.attrib['data-step'] == str(step['step'])
            assert item.find('div/strong').text == step['role']
            assert item.find('div/p').text == step['does']
        assert '<svg' not in page
        assert f'../assets/diagrams/workflow-{workflow["key"]}.svg' in page
        assert '## Workflow steps and gates' in page
