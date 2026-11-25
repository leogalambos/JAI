#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate role installation projections from the canonical role library."""

import argparse
import json
from pathlib import Path

from compose_role_library import compose

_ROOT = Path(__file__).resolve().parents[1]
_OUTPUT = _ROOT / '.ai/runtime/knowledge/infrastructure-role-guidance.json'
_INSTALL_OUTPUT = _ROOT / '.ai/setup/role-projection.json'
_MODULES = {
    'methods/zero-trust/resource-access',
    'products/hashicorp/terraform/governed-plans',
    'domains/cloud/landing-zone-evidence',
    'domains/cloud/delivery-pipelines',
}


def _render(compilation):
    overlays, references = {}, {}
    for slug, row in compilation.manifest['roles'].items():
        if row['legacy_anchor'] != slug:
            continue
        if not any(module['id'] in _MODULES for module in row['modules']):
            continue
        relative = row['projection_path']
        baseline = (_ROOT / '.ai' / relative).read_bytes()
        instruction = compilation.instructions[slug]
        if not instruction.startswith(baseline):
            raise ValueError(f'{slug}: infrastructure guidance must preserve the exact legacy instruction')
        deferred = {}
        prefix = '.ai/' + str(Path(relative).parent) + '/'
        for module in row['modules']:
            for section in module['sections']:
                if section['delivery'] != 'optional':
                    continue
                projection = section['projection_path']
                name = projection.removeprefix(prefix)
                deferred[name] = section['reference_sha256']
                references[projection.removeprefix('.ai/')] = compilation.files[projection].decode('utf-8')
        overlays[relative] = {
            'baseline': row['legacy_instruction_sha256'],
            'supplement': instruction[len(baseline):].decode('utf-8'),
            'references': deferred,
        }
        if row.get('context_sections'):
            overlays[relative]['context_sections'] = row['context_sections']
    return json.dumps({'schema_version': 1, 'roles': overlays, 'references': references}, ensure_ascii=False, indent=2) + '\n'


def _provider_instruction(path, raw, sections, provider_files):
    """Defer assignment-scoped passages to individually linked provider references."""
    role = Path(path)
    index = f'knowledge/direct/{role.stem}.md'
    links = []
    for section in sections:
        reference = section['reference']
        if reference is None:
            reference = f'knowledge/direct/{role.stem}/{section["id"]}.md'
            start, end = section['start'], section['end']
            provider_files[(role.parent / reference).as_posix()] = raw[start:end].decode('utf-8')
        scope = ', '.join(f'{key} {" or ".join(values)}' for key, values in section['scope'].items())
        links.append(f'- [{section["id"]}](../{reference.removeprefix("knowledge/")}) ({scope})')
    for section in sorted(sections, key=lambda entry: entry['start'], reverse=True):
        raw = raw[:section['start']] + raw[section['end']:]
    raw = raw.replace(b'## Professional knowledge\n\n', b'', 1)
    provider_files[(role.parent / index).as_posix()] = (
        '# Task-specific professional knowledge\n\n'
        'Read a reference only if the assigned work matches the scope listed for it.\n\n'
        + '\n'.join(links)
        + '\n'
    )
    return raw + f'\n\nFor task-specific guidance, consult [the reference index]({index}).\n'.encode()


def _render_install_projection(compilation):
    """Produce the stdlib installer input from the exact composed catalogue."""
    runtime, skills, provider, discovery = {}, {}, {}, {}
    for source, raw in compilation.files.items():
        if source.startswith('.ai/runtime/'):
            runtime[source.removeprefix('.ai/runtime/')] = json.loads(raw)
        elif not (_ROOT / source).is_file() or (_ROOT / source).read_bytes() != raw:
            skills[source.removeprefix('.ai/')] = raw.decode('utf-8')
    for row in compilation.registry['roles']:
        path, slug = row['path'], row['slug']
        role = compilation.manifest['roles'][slug]
        if path in skills and role.get('context_sections'):
            direct = _provider_instruction(
                path, compilation.instructions[slug], role['context_sections'], provider)
            provider[path] = direct.decode('utf-8')
        if role['professional_parent']:
            category = f'skills/{row["skill"]}/SKILL.md'
            discovery.setdefault(category, []).append(
                f'- [{row["name"]}](references/{slug}.md) · `{row["tool_tier"]}` · `{row["operator_agent"]}`')
    return json.dumps({'schema_version': 1, 'runtime': runtime, 'skills': skills,
                       'provider': provider, 'discovery': discovery}, ensure_ascii=False,
                      indent=2) + '\n'


def main():
    """Write role installation projections or report drift in check mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    compilation = compose(_ROOT)
    generated = {_OUTPUT: _render(compilation),
                 _INSTALL_OUTPUT: _render_install_projection(compilation)}
    if args.check:
        stale = [str(path.relative_to(_ROOT)) for path, raw in generated.items()
                 if not path.is_file() or path.read_text(encoding='utf-8') != raw]
        if stale:
            parser.exit(1, 'Generated role projection drift: ' + ', '.join(stale) + '\n')
        return 0
    for path, raw in generated.items():
        path.write_text(raw, encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
