#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Validate and compose readable role sources into a complete staged generation."""

import argparse
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
import hashlib
from heapq import heappop, heappush
import json
from pathlib import Path, PurePosixPath
import re
import tempfile

import yaml


_SLUG = r'[a-z0-9]+(?:-[a-z0-9]+)*'
_MODULE_ID = rf'{_SLUG}(?:/{_SLUG})*'
_CONTROL_FIELDS = (
    'archetype', 'sfia_responsibility_band', 'tool_tier', 'allowed_tools',
    'operator_agent', 'layer', 'layer_name', 'layer_agent', 'layer_operator', 'jai',
)
_OBLIGATIONS = ('inputs', 'deliverables', 'gates')


@dataclass(frozen=True)
class Compilation:
    """Complete in-memory generation built from a single set of source bytes.

    Registry and instruction keys retain the legacy shape. Manifest describes
    provenance and reverse dependencies. Files are UTF-8 byte strings indexed
    by repository-relative projection path for a separate staging operation.
    """

    registry: dict
    instructions: dict
    manifest: dict
    files: dict


class _ClosedLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ValueError('YAML aliases are unsupported')
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError('YAML mapping keys must be strings')
            if key in mapping:
                raise ValueError(f'duplicate YAML key {key!r}')
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def _json(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def _mapping(value, where):
    if not isinstance(value, dict):
        raise ValueError(f'{where}: expected mapping')
    return value


def _closed(value, required, optional, where):
    fields = set(_mapping(value, where))
    missing = set(required) - fields
    unknown = fields - set(required) - set(optional)
    if missing or unknown:
        raise ValueError(f'{where}: missing fields {sorted(missing)}, unknown fields {sorted(unknown)}')


def _version(value, where):
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ValueError(f'{where}: unsupported schema_version')


def _string(value, where, pattern=None):
    if not isinstance(value, str) or not value.strip() or (pattern and not re.fullmatch(pattern, value)):
        raise ValueError(f'{where}: invalid string {value!r}')


def _day(value, where):
    _string(value, where, r'\d{4}-\d{2}-\d{2}')
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f'{where}: invalid review date {value!r}') from exc


def _list(value, where, pattern=None):
    if not isinstance(value, list):
        raise ValueError(f'{where}: expected list')
    for item in value:
        _string(item, where, pattern)
    if len(set(value)) != len(value):
        raise ValueError(f'{where}: duplicate list entry')


def _read(base, relative, *, readable=False):
    label = f'{relative}'
    if not isinstance(relative, str):
        raise ValueError(f'{label}: invalid relative path')
    parts = relative.split('/')
    if any(part in ('', '.', '..') or '\\' in part for part in parts):
        raise ValueError(f'{label}: path escape or noncanonical path')
    if readable and (any(not re.fullmatch(_SLUG, part) for part in parts[:-1])
                     or not re.fullmatch(rf'{_SLUG}\.(?:yaml|yml|md)', parts[-1])):
        raise ValueError(f'{label}: expected readable lowercase path')
    path = base
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f'{label}: symbolic links are unsupported')
    if not path.is_file() or not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f'{label}: source missing or outside source root')
    raw = path.read_bytes()
    raw.decode('utf-8', errors='strict')
    return raw


def _load_yaml(raw, where):
    try:
        return yaml.load(raw.decode('utf-8'), Loader=_ClosedLoader)
    except (yaml.YAMLError, ValueError, RecursionError) as exc:
        raise ValueError(f'{where}: {exc}') from exc


def _documents(library, folder, identity, validate):
    documents = {}
    directory = library / folder
    if directory.is_symlink():
        raise ValueError(f'{folder}: symbolic links are unsupported')
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'{path.relative_to(library)}: symbolic links are unsupported')
        if path.suffix not in {'.yaml', '.yml'}:
            continue
        source = path.relative_to(library).as_posix()
        raw = _read(library, source, readable=True)
        document = _load_yaml(raw, source)
        validate(document, source)
        key = document[identity]
        if key in documents:
            raise ValueError(f'duplicate {identity} {key}: {documents[key][1]} and {source}')
        documents[key] = document, source, _sha(raw)
    return documents


def _validate_role(role, where):
    _closed(role, ('schema_version', 'slug'),
            ('extends', 'name', 'aliases', 'includes', 'facets', 'overrides',
             *_OBLIGATIONS, 'workflow_references'), where)
    _version(role, where)
    _string(role['slug'], where, _SLUG)
    if 'extends' in role:
        _string(role['extends'], where, _SLUG)
        _string(role.get('name'), f'{where}: name')
    elif 'name' in role:
        _string(role['name'], where)
    for key, pattern in (('aliases', None), ('includes', _MODULE_ID), ('workflow_references', None)):
        _list(role.get(key, []), f'{where}: {key}', pattern)
    facets = role.get('facets', {})
    _closed(facets, (), ('product', 'method', 'profession'), f'{where}: facets')
    for values in facets.values():
        _list(values, f'{where}: facets', _SLUG)
    overrides = role.get('overrides', {})
    _closed(overrides, (), ('mission', 'scope'), f'{where}: overrides')
    for key, value in overrides.items():
        _string(value, f'{where}: {key}')
    for group in _OBLIGATIONS:
        for key, value in _mapping(role.get(group, {}), f'{where}: {group}').items():
            _string(key, f'{where}: {group} key', _SLUG)
            if re.fullmatch(r'g[0-9]+' if group == 'gates' else r'[0-9]+', key):
                raise ValueError(f'{where}: {group}.{key} is reserved for the inherited professional reference')
            _string(value, f'{where}: {group}.{key}')


def _validate_module(module, where):
    _closed(module, ('schema_version', 'id', 'title', 'version', 'applicability', 'sections', 'sources'),
            ('includes',), where)
    _version(module, where)
    _string(module['id'], where, _MODULE_ID)
    for key in ('title', 'version', 'applicability'):
        _string(module[key], f'{where}: {key}')
    _list(module.get('includes', []), f'{where}: includes', _MODULE_ID)
    sources = _mapping(module['sources'], f'{where}: sources')
    for key, source in sources.items():
        label = f'{where}: sources.{key}'
        _string(key, label, _SLUG)
        fields = ('publisher', 'authority', 'title', 'applicability', 'reviewed', 'owner',
                  'use_restrictions', 'review_trigger')
        _closed(source, fields, ('url', 'locator'), label)
        if ('url' in source) == ('locator' in source):
            raise ValueError(f'{label}: expected exactly one URL or governed locator')
        for field, value in source.items():
            _string(value, f'{label}.{field}', r'https?://\S+' if field == 'url' else None)
        _day(source['reviewed'], label)
    if not isinstance(module['sections'], list):
        raise ValueError(f'{where}: expected section list')
    keys = {}
    for section in module['sections']:
        _closed(section, ('id', 'delivery', 'source', 'applicability', 'exclusions', 'owner', 'reviewed'),
                ('text', 'reference', 'read_when'), f'{where}: section')
        key = section['id']
        label = f'{where}: section {key!r}'
        _string(key, label, _SLUG)
        for field in ('source', 'applicability', 'exclusions', 'owner'):
            _string(section[field], f'{label}: {field}')
        if section['source'] not in sources:
            raise ValueError(f'{label}: unknown source key {section["source"]}')
        _day(section['reviewed'], label)
        delivery = section['delivery']
        if delivery not in ('required', 'optional'):
            raise ValueError(f'{label}: unsupported section delivery {delivery!r}')
        if ('text' in section) == ('reference' in section) or (delivery == 'optional' and 'text' in section):
            raise ValueError(f'{label}: expected section text or a named reference, optional sections require a reference')
        if delivery == 'optional':
            _string(section.get('read_when'), f'{label}: read_when')
        elif 'read_when' in section:
            raise ValueError(f'{label}: required sections cannot be deferred')
        payload = 'text' if 'text' in section else 'reference'
        _string(section[payload], label, r'.+\.md' if payload == 'reference' else None)
        if key in keys and keys[key] != section:
            raise ValueError(f'{label}: conflicting section definitions')
        keys[key] = section
    module['sections'] = list(keys.values())


def _order(nodes, dependencies, label):
    """Return the smallest available ID in each dependency-first position."""
    following = {key: [] for key in nodes}
    waiting = {}
    ready = []
    for key in sorted(nodes):
        incoming = dependencies(key)
        waiting[key] = len(incoming)
        for dep in incoming:
            if dep not in following:
                raise ValueError(f'{label} {key}: missing dependency {dep}')
            following[dep].append(key)
        if not incoming:
            heappush(ready, key)
    ordered = []
    while ready:
        key = heappop(ready)
        ordered.append(key)
        for dependent in following[key]:
            waiting[dependent] -= 1
            if not waiting[dependent]:
                heappush(ready, dependent)
    if len(ordered) != len(following):
        key = min(key for key, total in waiting.items() if total)
        chain = []
        while key not in chain:
            chain.append(key)
            key = min(dep for dep in dependencies(key) if waiting[dep])
        raise ValueError(f'{label} cycle: ' + ' -> '.join((*chain, key)))
    return ordered


def _migrations(library, roles, legacy, baseline):
    if not (library / 'migrations.yaml').exists() and not (library / 'migrations.yaml').is_symlink():
        migrations = {}
    else:
        raw = _read(library, 'migrations.yaml', readable=True)
        config = _load_yaml(raw, 'migrations.yaml')
        _closed(config, ('schema_version', 'migrations'), (), 'migrations.yaml')
        _version(config, 'migrations.yaml')
        migrations = _mapping(config['migrations'], 'migrations.yaml')
    collisions = roles.keys() & legacy.keys()
    if collisions != migrations.keys():
        raise ValueError(f'migration ownership mismatch, expected {sorted(collisions)}, got {sorted(migrations)}')
    for slug, migration in migrations.items():
        document, source, _ = roles[slug]
        _closed(migration, ('source', 'legacy_row_sha256', 'legacy_instruction_sha256'), (), slug)
        if (source != migration['source'] or 'extends' in document
                or _sha(_canonical(legacy[slug])) != migration['legacy_row_sha256']
                or _sha(baseline[slug]) != migration['legacy_instruction_sha256']):
            raise ValueError(f'{slug}: migration source or legacy digest mismatch')
        if set(document) - {'schema_version', 'slug', 'includes', 'facets'}:
            raise ValueError(f'{slug}: legacy migration may only add modules and facets')
    return migrations


def _selected_modules(roots, modules, global_order, where):
    selected = set()
    pending = list(sorted(roots, reverse=True))
    while pending:
        key = pending.pop()
        if key not in modules:
            raise ValueError(f'{where}: missing knowledge dependency {key}')
        if key not in selected:
            selected.add(key)
            pending.extend(modules[key][0].get('includes', []))
    return [key for key in global_order if key in selected]


def _obligations(chain, roles):
    merged = {group: {} for group in _OBLIGATIONS}
    origins = {}
    for slug in chain:
        role, source, _ = roles[slug]
        for group in _OBLIGATIONS:
            for key, value in sorted(role.get(group, {}).items()):
                if key in merged[group] and merged[group][key] != value:
                    raise ValueError(f'conflicting role requirement {group}.{key}: '
                                     f'{origins[group, key]} -> {source}')
                merged[group][key] = value
                origins.setdefault((group, key), source)
    return merged


def _knowledge(modules, module_order, references, row, files):
    snippets, evidence, sources = [], [], {}
    for key in module_order:
        module, owner_path, digest = modules[key]
        for source_key, source in module['sources'].items():
            if source_key in sources and sources[source_key][0] != source:
                raise ValueError(f'conflicting source record {source_key}: '
                                 f'{sources[source_key][1]} and {owner_path}')
            sources.setdefault(source_key, (source, owner_path))
        sections = []
        snippets.append(f'\n### {module["title"]}\n\nApplicability: {module["applicability"]}\n')
        for section in module['sections']:
            sid = section['id']
            source = module['sources'][section['source']]
            record = {'id': sid, 'delivery': section['delivery'], 'source': section['source'],
                      'section_sha256': _sha(_canonical(section)),
                      'source_record_sha256': _sha(_canonical(source))}
            if 'reference' in section:
                relative = section['reference']
                raw = references[key, sid]
                record['reference_sha256'] = _sha(raw)
            else:
                raw = section['text'].encode()
            if section['delivery'] == 'required':
                content = raw.decode().rstrip()
            else:
                link = f'knowledge/{key}/{relative}'
                path = f'.ai/skills/{row["skill"]}/references/{link}'
                if path in files and files[path] != raw:
                    raise ValueError(f'{owner_path}: conflicting projection {path}')
                files[path] = raw
                record['projection_path'] = path
                content = f'Consult [{sid}]({link}). Read when: {section["read_when"]}'
            locator = source.get('url', source.get('locator'))
            rendered = (
                f'\n#### {sid}\n\n{content}\n\n'
                f'Applicability: {section["applicability"]}. Exclusions: {section["exclusions"]}. '
                f'Owner: {section["owner"]}. Reviewed: {section["reviewed"]}. '
                f'Source: {source["publisher"]}, {source["title"]} ({locator}). '
                f'Recheck when {source["review_trigger"]}.\n'
            )
            snippets.append(rendered)
            record['rendered_section_sha256'] = _sha(rendered.encode())
            sections.append(record)
        evidence.append({'id': key, 'version': module['version'], 'source_path': owner_path,
                         'source_sha256': digest, 'sections': sections})
    records = {key: {'source_path': path, **record} for key, (record, path) in sorted(sources.items())}
    return ''.join(snippets), evidence, records


def _compile_role(slug, chain, roles, modules, order, row, baseline, references, files):
    scope, facets, workflows, roots = [], {}, [], set()
    for key in chain:
        entry, _, _ = roles[key]
        row['aliases'] = list(dict.fromkeys([*row['aliases'], *entry.get('aliases', [])]))
        if 'mission' in entry.get('overrides', {}):
            row['mission'] = entry['overrides']['mission']
        if 'scope' in entry.get('overrides', {}):
            scope.append(entry['overrides']['scope'])
        for facet, values in entry.get('facets', {}).items():
            facets.setdefault(facet, set()).update(values)
        roots.update(entry.get('includes', []))
        workflows.extend(entry.get('workflow_references', []))
    requirements = _obligations(chain, roles)
    deliverables = requirements['deliverables'].values()
    row['primary_deliverables'] = list(dict.fromkeys([*row['primary_deliverables'], *deliverables]))
    selected = _selected_modules(roots, modules, order, slug)
    knowledge, provenance, sources = _knowledge(modules, selected, references, row, files)
    header = (f'# {row["name"]}\n\nProfessional basis: {row["category"]}.\n\n'
              f'Assignment mission: {row["mission"]}\n\n'
              'Apply the inherited professional procedure, required inputs, deliverables, gates, '
              'authority limits and independent review throughout this assignment. '
              'Apply specialist scope and knowledge within those controls.\n')
    notes = '\n'.join(f'- {item}' for item in scope)
    if scope:
        header += '\nCumulative specialization scope:\n\n' + notes + '\n'
    if any(requirements.values()):
        header += '\n## Additional professional obligations\n'
        for group, entries in requirements.items():
            for key, value in entries.items():
                header += f'\n- {group}/{key}: {value}'
        header += '\n'
    prefix = b''
    if 'extends' in roles[slug][0]:
        prefix = header.encode() + b'\n'
    instruction = prefix + baseline
    if knowledge:
        block = ('## Professional knowledge\n' + knowledge + '\n').encode()
        instruction = prefix + block + baseline if prefix else baseline + b'\n\n' + block
    return instruction, provenance, {'facets': {key: sorted(values) for key, values in sorted(facets.items())},
                                     'workflow_references': sorted(set(workflows)),
                                     'scope': scope, 'obligations': requirements, 'sources': sources}


def _indexes(rows, provenance):
    entries, facets = {}, {key: {} for key in ('profession', 'product', 'method', 'deliverable', 'alias')}
    for slug, row in sorted(rows.items()):
        source = provenance[slug]
        values = source.get('facets', {})
        entries[slug] = {'name': row['name'], 'profession': row['category'], 'aliases': row['aliases'],
                         'source_path': f'{source["source_root"]}/{source["source_path"]}',
                         'installed_reference': row['path'], 'deliverables': row['primary_deliverables'],
                         'facets': values}
        groups = {'profession': [row['category'], *values.get('profession', [])],
                  'product': values.get('product', []), 'method': values.get('method', []),
                  'deliverable': row['primary_deliverables'], 'alias': row['aliases']}
        for kind, labels in groups.items():
            for label in sorted(set(labels)):
                facets[kind].setdefault(label, []).append(slug)
    return entries, facets


def compose(repository_root, library_root=None):
    """Compile exact legacy roles and authorized additive specialist sources.

    Args:
        repository_root: Checkout containing the maintained legacy catalogue
            and exact role reference files beneath .ai.
        library_root: Optional separately staged source tree. Defaults to
            .ai/role-library under the repository root.

    Returns:
        Complete in-memory projection and provenance. No files are published
        or modified, even when a source validation fails.

    Raises:
        ValueError: Conflicting or unsafe data, malformed UTF-8 or YAML,
            missing dependencies, unsupported features, or an unpinned migration.
        OSError: A source file cannot be read.
    """
    root = Path(repository_root).resolve() / '.ai'
    library = Path(library_root) if library_root is not None else root / 'role-library'
    if library.is_symlink():
        raise ValueError('role library root must not be a symbolic link')
    registry_raw = _read(root, 'runtime/roles.json')
    registry = json.loads(registry_raw)
    legacy = {row['slug']: row for row in registry['roles']}
    if len(legacy) != len(registry['roles']) or len(legacy) != registry['count']:
        raise ValueError('legacy role identities or count mismatch')
    baseline = {}
    for slug, row in legacy.items():
        _string(slug, 'legacy role slug', _SLUG)
        _string(row['skill'], 'legacy category skill', _SLUG)
        expected = f'skills/{row["skill"]}/references/{slug}.md'
        if row['path'] != expected:
            raise ValueError(f'{slug}: legacy path differs from native exact lookup')
        baseline[slug] = _read(root, expected)
    roles = _documents(library, 'roles', 'slug', _validate_role)
    modules = _documents(library, 'knowledge', 'id', _validate_module)
    migrations = _migrations(library, roles, legacy, baseline)
    for slug, (role, source, _) in roles.items():
        if 'extends' not in role and slug not in migrations:
            raise ValueError(f'{source}: a specialization requires exactly one professional parent')
    module_order = _order(modules, lambda key: modules[key][0].get('includes', []), 'knowledge module')
    references = {}
    for module_id, (module, source, _) in modules.items():
        for section in module['sections']:
            if 'reference' in section:
                references[module_id, section['id']] = _read(
                    library / PurePosixPath(source).parent, section['reference'], readable=True
                )

    def parent(slug):
        if slug in roles and 'extends' in roles[slug][0]:
            return [roles[slug][0]['extends']]
        return []

    role_order = _order(legacy.keys() | roles.keys(), parent, 'professional role')
    contracts = {}
    if roles.keys() - legacy.keys():
        source = json.loads(_read(root, 'runtime/artifacts/contracts/role-deliverables.v3.json'))
        contracts = {row['id']: row for row in source['contracts']}
        if len(contracts) != len(source['contracts']):
            raise ValueError('duplicate authoritative output contract')
    rows, instructions, files, provenance, chains, reverse = {}, {}, {}, {}, {}, {}
    descendants = {slug: [] for slug in role_order}
    for slug in role_order:
        parents = parent(slug)
        chain = [*chains[parents[0]], slug] if parents else [slug]
        chains[slug] = chain
        anchor = chain[0]
        row = deepcopy(legacy[anchor])
        instruction = baseline[anchor]
        source = row['path']
        for ancestor in chain[:-1]:
            descendants[ancestor].append(slug)
        module_evidence, details = [], {}
        if slug in roles:
            spec, source, _ = roles[slug]
            row.update(slug=slug, name=spec.get('name', row['name']),
                       path=f'skills/{row["skill"]}/references/{slug}.md')
            authored = [item for item in chain if item in roles]
            instruction, module_evidence, details = _compile_role(
                slug, authored, roles, modules, module_order, row, instruction, references, files
            )
            for module in module_evidence:
                reverse.setdefault(module['id'], []).append(slug)
        if slug != anchor:
            output_refs = []
            for number in range(1, len(row['primary_deliverables']) + 1):
                cid = f'{anchor}:{number}'
                contract = contracts.get(cid)
                if contract is None or contract.get('role_slug') != anchor or not contract.get('version'):
                    raise ValueError(f'{slug}: missing authoritative output {cid}')
                output_refs.append({'id': cid, 'version': contract['version']})
            row['inherited_outputs'] = {'schema_version': 1, 'owner': anchor, 'contracts': output_refs}
        rows[slug] = row
        instructions[slug] = instruction
        provenance[slug] = {
            'source_kind': 'composed' if slug in roles else 'legacy-passthrough',
            'source_path': source,
            'source_root': '.ai/role-library' if slug in roles else '.ai',
            'source_sha256': roles[slug][2] if slug in roles else _sha(instruction),
            'professional_parent': parents[0] if parents else None,
            'ancestry': chain[:-1],
            'legacy_anchor': anchor,
            'legacy_row_sha256': _sha(_canonical(legacy[anchor])),
            'legacy_instruction_sha256': _sha(baseline[anchor]),
            'projection_path': row['path'],
            'instruction_sha256': _sha(instruction),
            'controls': deepcopy({field: row[field] for field in _CONTROL_FIELDS if field in row}),
            'inherited_definitions': [
                {'slug': item, 'source_path': roles[item][1], 'source_sha256': roles[item][2]}
                for item in chain[:-1] if item in roles
            ],
            'modules': module_evidence,
            **details,
        }
        files['.ai/' + row['path']] = instruction
    registry['roles'] = [rows[slug] for slug in (*legacy, *sorted(roles.keys() - legacy.keys()))]
    registry['count'] = len(rows)
    manifest = {'schema_version': 1, 'legacy_catalogue_sha256': _sha(registry_raw),
                'digest_domains': {'legacy_row_sha256': 'canonical JSON bytes',
                                   'section_sha256': 'canonical JSON section metadata',
                                   'source_sha256': 'raw UTF-8 source file bytes',
                                   'instruction_sha256': 'emitted UTF-8 role instruction bytes',
                                   'reference_sha256': 'raw UTF-8 reference file bytes',
                                   'rendered_section_sha256': 'emitted UTF-8 section bytes'},
                'roles': {slug: provenance[slug] for slug in sorted(provenance)},
                'roles_by_module': {key: sorted(reverse.get(key, [])) for key in sorted(modules)},
                'descendants_by_role': {key: sorted(descendants[key]) for key in sorted(descendants)}}
    files['.ai/runtime/roles.json'] = _json(registry) if migrations or roles else registry_raw
    files['.ai/runtime/role-composition.json'] = _json(manifest)
    entries, facets = _indexes(rows, provenance)
    files['.ai/runtime/role-indexes/by-role-slug.json'] = _json({'schema_version': 1, 'roles': entries})
    files['.ai/runtime/role-indexes/facets.json'] = _json({'schema_version': 1, 'facets': facets})
    return Compilation(registry, instructions, manifest, files)


def _main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--library', type=Path)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument('--stage', type=Path, help='Create a new directory with generated files.')
    destination.add_argument('--check', type=Path, help='Compare an existing staged directory with source.')
    args = parser.parse_args()
    try:
        generation = compose(args.root, args.library)
        if args.stage is not None:
            if args.stage.exists() or args.stage.is_symlink():
                raise ValueError('staging directory must be new')
            with tempfile.TemporaryDirectory(dir=args.stage.parent) as temporary:
                staged = Path(temporary) / 'generation'
                for relative, raw in generation.files.items():
                    target = staged / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(raw)
                staged.rename(args.stage)
        else:
            actual = {}
            for path in args.check.rglob('*'):
                if path.is_symlink():
                    raise ValueError(f'{path}: symbolic links are unsupported')
                if path.is_file():
                    actual[path.relative_to(args.check).as_posix()] = path.read_bytes()
            if actual != generation.files:
                paths = actual.keys() | generation.files.keys()
                drift = sorted(path for path in paths if actual.get(path) != generation.files.get(path))
                raise ValueError('generation drift: ' + ', '.join(drift))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    _main()
