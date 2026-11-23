# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Verify additive composition against a real local catalogue tree."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from tools.compose_role_library import compose


ROOT = Path(__file__).resolve().parents[1]


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding='utf-8')
    return path


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _role(slug, parent='security-engineer', **fields):
    return {'schema_version': 1, 'slug': slug, 'name': slug.title(), 'extends': parent, **fields}


def _module(key, includes=()):
    source = {'publisher': 'Example Institute', 'title': 'Product practice',
              'authority': 'vendor documentation', 'url': 'https://example.org/practice',
              'applicability': 'Example product 1', 'reviewed': '2026-11-23',
              'owner': 'Catalogue maintainer', 'use_restrictions': 'Original paraphrase.',
              'review_trigger': 'the supported product version changes'}
    return {'schema_version': 1, 'id': key, 'title': key, 'version': '1.0.0',
            'includes': list(includes), 'applicability': 'Example product 1',
            'sections': [{'id': 'check', 'delivery': 'required', 'text': f'Do the {key} check.',
                          'source': 'example-institute', 'applicability': 'Example product 1',
                          'exclusions': 'Other editions', 'owner': 'Catalogue maintainer',
                          'reviewed': '2026-11-23'}],
            'sources': {'example-institute': source}}


def test_passthrough_preserves_all_catalogue_and_instruction_bytes(tmp_path):
    result = compose(ROOT, tmp_path)
    expected = (ROOT / '.ai/runtime/roles.json').read_bytes()
    assert result.files['.ai/runtime/roles.json'] == expected
    assert result.registry == json.loads(expected)
    assert set(result.instructions) == {row['slug'] for row in result.registry['roles']}
    for row in result.registry['roles']:
        assert (ROOT / '.ai' / row['path']).read_bytes() == result.instructions[row['slug']]


def test_diamond_and_professional_inheritance_are_deterministic_and_additive(tmp_path):
    for slug, includes in [('top', ['right', 'left']), ('shared', []),
                           ('right', ['shared']), ('left', ['shared'])]:
        _write(tmp_path / f'knowledge/{slug}.yaml', _module(slug, includes))
    role_file = _write(tmp_path / 'roles/profession/parent.yaml',
                       _role('product-engineer', includes=['top'], aliases=['Example engineer'],
                             gates={'exact-gate': 'Verify the original exact boundary.'}))
    _write(tmp_path / 'roles/profession/child.yaml',
           _role('product-review', parent='product-engineer', includes=['right'],
                 aliases=['Example reviewer'], facets={'product': ['example']},
                 overrides={'mission': 'Provide the product decision.', 'scope': 'Supported products only.'},
                 gates={'exact-gate': 'Verify the original exact boundary.'}))
    original = compose(ROOT, tmp_path)
    assert original.files == compose(ROOT, tmp_path).files
    descendant = original.manifest['roles']['product-review']
    assert descendant['ancestry'] == ['security-engineer', 'product-engineer']
    assert descendant['inherited_definitions'][0]['source_sha256'] == _digest(role_file.read_bytes())
    assert original.manifest['descendants_by_role']['security-engineer'] == ['product-engineer', 'product-review']
    assert descendant['controls'] == original.manifest['roles']['security-engineer']['controls']
    assert [row['id'] for row in descendant['modules']] == ['shared', 'left', 'right', 'top']
    assert original.manifest['roles_by_module']['shared'] == ['product-engineer', 'product-review']
    assert original.instructions['product-review'].count(b'Do the shared check.') == 1
    assert original.instructions['product-review'].count(b'Verify the original exact boundary.') == 1
    assert original.instructions['security-engineer'] in original.instructions['product-review']
    assert b'Assignment mission: Provide the product decision.' in original.instructions['product-review']
    assert b'Supported products only.' in original.instructions['product-review']
    assert descendant['instruction_sha256'] == _digest(original.instructions['product-review'])
    role_file.rename(role_file.with_name('relocated.yaml'))
    relocated = compose(ROOT, tmp_path)
    assert relocated.instructions == original.instructions
    assert relocated.manifest['roles']['product-engineer']['source_path'] == 'roles/profession/relocated.yaml'
    entries = json.loads(relocated.files['.ai/runtime/role-indexes/by-role-slug.json'])['roles']
    assert entries['product-engineer']['source_path'] == '.ai/role-library/roles/profession/relocated.yaml'
    assert entries['product-engineer']['installed_reference'].endswith('/product-engineer.md')
    facets = json.loads(relocated.files['.ai/runtime/role-indexes/facets.json'])['facets']
    assert facets['alias']['Example engineer'] == ['product-engineer', 'product-review']
    assert facets['product']['example'] == ['product-review']


def test_role_without_modules_preserves_professional_instruction(tmp_path):
    _write(tmp_path / 'roles/clean.yaml', _role('product-engineer'))
    result = compose(ROOT, tmp_path)
    assert result.manifest['roles']['product-engineer']['modules'] == []
    assert result.instructions['security-engineer'] in result.instructions['product-engineer']


def test_legacy_migration_pins_original_source_and_keeps_row(tmp_path):
    previous = compose(ROOT, tmp_path)
    slug = 'security-engineer'
    row = next(row for row in previous.registry['roles'] if row['slug'] == slug)
    original = previous.instructions[slug]
    _write(tmp_path / 'knowledge/sabsa.yaml', _module('sabsa'))
    source = 'roles/methods/security-engineer.yaml'
    _write(tmp_path / source, {'schema_version': 1, 'slug': slug, 'includes': ['sabsa']})
    config = {'schema_version': 1, 'migrations': {slug: {
        'source': source,
        'legacy_row_sha256': _digest(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                               separators=(',', ':')).encode()),
        'legacy_instruction_sha256': _digest(original),
    }}}
    _write(tmp_path / 'migrations.yaml', config)
    next_result = compose(ROOT, tmp_path)
    assert next_result.registry == previous.registry
    assert next_result.instructions[slug].startswith(original)
    config['migrations'][slug]['legacy_instruction_sha256'] = '0' * 64
    _write(tmp_path / 'migrations.yaml', config)
    with pytest.raises(ValueError, match='migration source or legacy digest mismatch'):
        compose(ROOT, tmp_path)
    assert next_result.instructions[slug].startswith(original)


def test_optional_reference_is_named_and_version_pinned(tmp_path):
    slug = 'product-engineer'
    _write(tmp_path / 'roles/example.yaml', _role(slug, includes=['example']))
    module = _module('example')
    section = module['sections'][0]
    del section['text']
    section.update(delivery='optional', reference='decision.md',
                   read_when='The planned change relies on a decision.')
    _write(tmp_path / 'knowledge/example.yaml', module)
    raw = b'# Decision details\n'
    (tmp_path / 'knowledge/decision.md').write_bytes(raw)
    result = compose(ROOT, tmp_path)
    item = result.manifest['roles'][slug]['modules'][0]['sections'][0]
    assert result.files[item['projection_path']] == raw
    assert item['reference_sha256'] == _digest(raw)
    assert raw not in result.instructions[slug]
    assert b'knowledge/example/decision.md' in result.instructions[slug]


@pytest.mark.parametrize(('content', 'error'), [
    ('schema_version: 1\nslug: one\nslug: two\n', 'duplicate YAML key'),
    ('schema_version: 1\nslug: !!python/object:builtins.object {}\n', 'could not determine a constructor'),
    ('schema_version: 1\nslug: &name one\nname: *name\n', 'YAML aliases are unsupported'),
    ({'allowed_tools': 'Bash'}, 'unknown fields'),
    ({'overrides': {'gate': 'Skip review'}}, 'unknown fields'),
    ({'extends': ['security-engineer']}, 'invalid string'),
    ({'extends': 'missing-parent'}, 'missing dependency'),
    ({'extends': 'example-engineer'}, 'professional role cycle'),
    ({'includes': ['missing']}, 'missing knowledge dependency'),
    ({'gates': {'g1': 'Waive peer review.'}}, 'reserved for the inherited professional reference'),
    ({'deliverables': {'1': 'An unrelated document.'}}, 'reserved for the inherited professional reference'),
])
def test_role_validation_rejects_unknown_or_unsafe_authoring(tmp_path, content, error):
    path = tmp_path / 'roles/example.yaml'
    if isinstance(content, str):
        path.parent.mkdir()
        path.write_text(content, encoding='utf-8')
    else:
        _write(path, _role('example-engineer') | content)
    with pytest.raises(ValueError, match=error):
        compose(ROOT, tmp_path)


@pytest.mark.parametrize(('mutation', 'error'), [
    ('cycle', 'knowledge module cycle: example -> example'),
    ('missing', 'missing dependency missing'),
    ('duplicate-id', 'duplicate id example'),
    ('section-conflict', 'conflicting section definitions'),
    ('control', 'unknown fields'),
    ('escaping-reference', 'path escape'),
    ('symlink-reference', 'symbolic links are unsupported'),
    ('unsupported-delivery', 'unsupported section delivery'),
])
def test_knowledge_validation_rejects_conflicts_and_unsafe_paths(tmp_path, mutation, error):
    module = _module('example')
    if mutation in ('cycle', 'missing'):
        module['includes'] = ['example' if mutation == 'cycle' else 'missing']
    elif mutation == 'duplicate-id':
        _write(tmp_path / 'knowledge/other.yaml', module)
    elif mutation == 'section-conflict':
        module['sections'].append(module['sections'][0] | {'text': 'Conflicting check.'})
    elif mutation == 'control':
        module['sections'][0]['can_approve'] = True
    elif mutation == 'unsupported-delivery':
        module['sections'][0]['delivery'] = 'conditional'
    else:
        section = module['sections'][0]
        del section['text']
        section['reference'] = '../out.md' if mutation == 'escaping-reference' else 'out.md'
        if mutation == 'symlink-reference':
            (tmp_path / 'knowledge').mkdir()
            (tmp_path / 'knowledge/out.md').symlink_to(tmp_path / 'out.md')
    _write(tmp_path / 'knowledge/example.yaml', module)
    with pytest.raises(ValueError, match=error):
        compose(ROOT, tmp_path)


def test_disagreement_in_inherited_requirement_stops_generation(tmp_path):
    _write(tmp_path / 'roles/first.yaml',
           _role('parent', gates={'independent-review': 'Obtain independent review.'}))
    _write(tmp_path / 'roles/second.yaml',
           _role('child', parent='parent', gates={'independent-review': 'Review is optional.'}))
    with pytest.raises(ValueError, match=r'conflicting role requirement gates\.independent-review.*first.yaml.*second.yaml'):
        compose(ROOT, tmp_path)


def test_disagreement_in_source_provenance_stops_generation(tmp_path):
    first, second = _module('first'), _module('second')
    second['sources']['example-institute']['reviewed'] = '2026-10-23'
    _write(tmp_path / 'knowledge/first.yaml', first)
    _write(tmp_path / 'knowledge/second.yaml', second)
    _write(tmp_path / 'roles/example.yaml', _role('example-engineer', includes=['second', 'first']))
    with pytest.raises(ValueError, match='conflicting source record example-institute'):
        compose(ROOT, tmp_path)


def test_legacy_slug_cannot_gain_second_authoritative_definition(tmp_path):
    _write(tmp_path / 'roles/source.yaml', _role('security-engineer'))
    with pytest.raises(ValueError, match='migration ownership mismatch'):
        compose(ROOT, tmp_path)


def test_cli_stages_independent_builds_and_leaves_prior_good_output_after_failure(tmp_path):
    library = tmp_path / 'source'
    role = _write(library / 'roles/example.yaml', _role('example-engineer'))
    command = [sys.executable, str(ROOT / 'tools/compose_role_library.py'), '--library', str(library)]
    previous, duplicate, failed = (tmp_path / name for name in ('previous', 'duplicate', 'failed'))
    subprocess.run([*command, '--stage', str(previous)], check=True, capture_output=True)
    subprocess.run([*command, '--stage', str(duplicate)], check=True, capture_output=True)
    for path in duplicate.rglob('*'):
        if path.is_file():
            assert path.read_bytes() == (previous / path.relative_to(duplicate)).read_bytes()
    subprocess.run([*command, '--check', str(previous)], check=True, capture_output=True)
    role.write_text('schema_version: 1\nslug: bad\nslug: duplicate\n', encoding='utf-8')
    rejected = subprocess.run([*command, '--stage', str(failed)], text=True, capture_output=True)
    assert rejected.returncode == 1
    assert 'duplicate YAML key' in rejected.stderr
    assert not failed.exists()
    assert (previous / '.ai/runtime/roles.json').read_bytes() == (duplicate / '.ai/runtime/roles.json').read_bytes()
