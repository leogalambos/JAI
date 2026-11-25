# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Publish the canonical professional base roles as linked MkDocs profiles."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from mkdocs.structure.files import File, InclusionLevel

_ROOT = Path(__file__).resolve().parents[1]
_INDEX = 'reference/base-role-profiles.md'
_CATALOGUE = 'reference/roles.md'
_INDEX_MARKER = '{{ JAI_BASE_ROLE_PROFILES }}'
_ROLE_HEADING = re.compile(r'^## ([1-9][0-9]*)\. [^\n]+$', re.MULTILINE)
_SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
_FIRST_TABLE_CELL = re.compile(r'^(\| )([^|]+?)( \| )', re.MULTILINE)
_ADVERSARIAL_SKILL = 'it-roles-offensive-security-and-adversarial-testing'


def _roles(root):
    registry = json.loads((root / '.ai/runtime/roles.json').read_text(encoding='utf-8'))
    roles = registry['roles']
    if (registry['count'] != len(roles) or len({row['slug'] for row in roles}) != len(roles)
            or len({row['name'] for row in roles}) != len(roles)):
        raise ValueError('The base role registry must have unique slugs and names')
    return roles


def base_profile_path(slug: str) -> str:
    """Return the docs-relative source path for a canonical base role slug."""
    if not _SLUG.fullmatch(slug):
        raise ValueError(f'Invalid base role slug: {slug}')
    return f'reference/base-role-profiles/{slug}.md'


def _role_sections(reference):
    fields = _ROLE_HEADING.split(reference)
    return {int(number): content.strip() for number, content in zip(fields[1::2], fields[2::2])}


def render_base_profile(root: Path, role: dict) -> str:
    """Render one base profile from the registry row and canonical role reference.

    Return Markdown for a virtual MkDocs page. Raise ValueError for invalid role
    paths or missing mandatory sections, and OSError if the reference is absent.
    """
    slug = role['slug']
    skill = role['skill']
    path = f'skills/{skill}/references/{slug}.md'
    if not _SLUG.fullmatch(slug) or not _SLUG.fullmatch(skill) or role['path'] != path:
        raise ValueError(f'Invalid base role reference: {slug}')
    reference = (root / '.ai' / path).read_text(encoding='utf-8')
    sections = _role_sections(reference)
    required = {1, 2, 3, 4, 7, 8}
    if not required.issubset(sections):
        raise ValueError(f'Missing base role profile sections: {slug}')

    # Preserve professional boundaries and evidence requirements for adversarial
    # roles without publishing an attack procedure in their public profiles.
    working_method = []
    if skill != _ADVERSARIAL_SKILL:
        method = sections[4].partition('#### External information and confidentiality')[0].rstrip()
        working_method = ['## Working method', method]
    gates = sections[7].partition('Verify the gate-check block')[0].rstrip()
    return '\n\n'.join([
        f'# {role["name"]}',
        '[Full role catalogue](../roles.md) › [Base role profiles](../base-role-profiles.md){ .ai-current-profile-parent }',
        f'![](../../assets/images/role-portraits/{skill.removeprefix("it-roles-")}.webp)'
        '{ .ai-role-portrait loading=lazy width=288 height=288 }',
        role['mission'].rstrip('.') + '.',
        f'**Discipline** {role["category"]}  \n**Role identifier** `{slug}`',
        '## Scope and routing', sections[1],
        '## When to assign the role', sections[2],
        '## Required inputs', sections[3],
        *working_method,
        '## Output contracts and gates',
        f'[Detailed deliverables and acceptance criteria](../output-contracts/role-{slug}.md)',
        gates,
        '## Checkpoints and escalation', sections[8],
    ]) + '\n'


def render_base_index(roles: list[dict]) -> str:
    """Group all base profile links by discipline in canonical catalogue order."""
    groups = defaultdict(list)
    for role in roles:
        groups[role['category']].append(role)

    sections = []
    for category, members in groups.items():
        sections.extend([f'## {category}', '\n'.join(
            f'- [{role["name"]}](base-role-profiles/{role["slug"]}.md)' for role in members)])
    return '\n\n'.join(sections)


def link_base_rows(markdown: str, roles: list[dict]) -> str:
    """Link the first cells of base catalogue rows to their detailed profiles."""
    names = {role['name']: role['slug'] for role in roles}

    def link(match):
        label = match[2]
        slug = names.get(label)
        if slug is None:
            return match[0]
        return f'{match[1]}[{label}](base-role-profiles/{slug}.md){match[3]}'

    return _FIRST_TABLE_CELL.sub(link, markdown)


def on_files(files, *, config):
    """Register one generated Markdown page per base role and return the files."""
    for role in _roles(_ROOT):
        filename = base_profile_path(role['slug'])
        files.append(File.generated(config, filename, content=render_base_profile(_ROOT, role),
                                    inclusion=InclusionLevel.NOT_IN_NAV))
    return files


def on_page_markdown(markdown, *, page, config, files):
    """Populate the base profile chapter index and link the full catalogue rows."""
    if page.file.src_uri == _INDEX:
        return markdown.replace(_INDEX_MARKER, render_base_index(_roles(_ROOT)))
    if page.file.src_uri == _CATALOGUE:
        return link_base_rows(markdown, _roles(_ROOT))
    return markdown
