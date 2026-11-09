# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise generated cases, immutable baseline preservation and path ownership."""
import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import generate_reference_completion as generator


def baseline(tmp_path):
    base = tmp_path / generator.DIRECTORY
    base.mkdir(parents=True)
    entries = []
    for level in ('simple', 'medium', 'complex'):
        path = base / 'adr' / (level + '.md')
        path.parent.mkdir(exist_ok=True)
        raw = ('original ' + level).encode()
        path.write_bytes(raw)
        entries.append({'path': 'adr/' + level + '.md', 'document_kind': 'adr',
                        'sha256': hashlib.sha256(raw).hexdigest()})
    (base / 'index.json').write_text(json.dumps({
        'families': ['adr'], 'new_proposed_families': [], 'entries': entries,
        'reference_count': 3, 'levels': ['simple', 'medium', 'complex']}))
    return base


def test_all_authored_cases_have_distinct_reasoning_and_exact_anchor_sets():
    for family, (_, fields, wrong, disposition) in generator.REFERENCE_CASES.items():
        texts = []
        for level in generator.CONTEXTS:
            text = generator.render_reference(family, level)
            assert wrong in text and disposition in text
            assert all(f'dcs-proposed-{family}.reference_{field}' in text for field in fields)
            assert 'NOT_EXECUTED' in text and 'not-human-approved' in text
            texts.append(text)
        assert len(set(texts)) == 3
    with pytest.raises(KeyError):
        generator.render_reference('unknown-family', 'medium')
    with pytest.raises(KeyError):
        generator.render_reference('software-change', 'unregistered-level')


def test_build_preserves_baseline_and_cli_checks_without_writing(tmp_path):
    base = baseline(tmp_path)
    original = (base / 'adr/simple.md').read_bytes()
    outputs = generator.build(tmp_path)
    assert len(outputs) == 55
    assert base / 'adr/simple.md' not in outputs
    assert generator.main(['--root', str(tmp_path), '--check']) == 1
    assert (base / 'adr/simple.md').read_bytes() == original
    assert generator.main(['--root', str(tmp_path)]) == 0
    assert generator.main(['--root', str(tmp_path), '--check']) == 0
    assert (base / 'adr/simple.md').read_bytes() == original


def test_changed_baseline_cannot_be_silently_rehashed(tmp_path):
    base = baseline(tmp_path)
    (base / 'adr/simple.md').write_text('changed without independent review')
    with pytest.raises(ValueError, match='Baseline reference changed'):
        generator.build(tmp_path)


def test_symlink_target_cannot_overwrite_external_material(tmp_path):
    base = baseline(tmp_path)
    target = tmp_path / 'outside.md'
    target.write_text('preserve')
    folder = base / 'software-change'
    folder.mkdir()
    (folder / 'simple.md').symlink_to(target)
    with pytest.raises(ValueError, match='symlink'):
        generator.main(['--root', str(tmp_path)])
    assert target.read_text() == 'preserve'


def test_project_role_example_preserves_other_sections_and_refreshes_owned_reasoning():
    source = ('## 7. Gates\nOriginal gate\n## 15. Worked example\n\n'
              '**Request.** Produce a tested change.\n\n'
              '**Expected shape of a good response:**\n1. Restate the request.\n'
              '## 16. Additional maintained material\nPreserve this.\n')
    record = {'effective_deliverable': {'name': 'Actual source change'},
              'acceptance_criteria': ['Reproduce the exact source revision and observed tests.']}
    reference = generator.render_reference('software-change', 'medium')
    result = generator.project_role_example(source, record, 'software-change', reference)
    assert 'Original gate' in result and 'Preserve this.' in result
    assert '**Expected shape of a good response:**' not in result
    assert 'unique order-key constraint' in result
    assert generator.project_role_example(result, record, 'software-change', reference) == result
    with pytest.raises(ValueError, match='worked-example'):
        generator.project_role_example('no numbered section', record, 'software-change', reference)


def test_role_example_outputs_use_canonical_family_and_preserve_role_gates():
    outputs = generator.role_example_outputs(ROOT, ['software-engineer'])
    assert len(outputs) == 1
    path, projected = next(iter(outputs.items()))
    original = path.read_text()
    assert original.split('## 15.', 1)[0] == projected.split('## 15.', 1)[0]
    assert 'software-change' in projected and generator.EXAMPLE_START in projected
    with pytest.raises(ValueError, match='Unknown or empty'):
        generator.role_example_outputs(ROOT, ['unregistered-role'])


def test_role_examples_use_newly_generated_reference_text_before_disk_write():
    reference = ROOT / generator.DIRECTORY / 'software-change/medium.md'
    original = reference.read_text()
    current = original.replace('unique order-key constraint', 'current candidate uniqueness rule')
    outputs = generator.role_example_outputs(
        ROOT, ['software-engineer'], reference_texts={reference: current})
    assert 'current candidate uniqueness rule' in next(iter(outputs.values()))
    assert reference.read_text() == original


@pytest.mark.parametrize('relative', [False, True])
def test_cli_projects_roles_from_same_generation_candidate(tmp_path, monkeypatch, relative):
    baseline(tmp_path)
    observed = []
    def project(root, role_slugs=None, reference_texts=None):
        observed.append(reference_texts)
        assert reference_texts is not None
        assert tmp_path / generator.DIRECTORY / 'diagram/medium.md' in reference_texts
        return {}
    monkeypatch.setattr(generator, 'role_example_outputs', project)
    monkeypatch.chdir(tmp_path)
    root_arg = '.' if relative else str(tmp_path)
    assert generator.main(['--root', root_arg, '--role-examples', '--check']) == 1
    assert len(observed) == 1
