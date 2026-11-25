# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Check role-profile coverage, professional content, and generated paths."""
from pathlib import Path

import pytest
from mkdocs.config import load_config
from mkdocs.structure.files import Files

from hooks import jai_base_role_profiles as profiles

ROOT = Path(__file__).resolve().parents[1]


def test_base_role_inventory_registers_every_profile_and_catalogue_link():
    """Check the exact canonical population reaches the index and catalogue."""
    roles = profiles._roles(ROOT)
    config = load_config(config_file=str(ROOT / 'mkdocs.yml'))
    files = config.plugins.on_files(Files([]), config=config)
    catalogue = (ROOT / 'docs/reference/roles.md').read_text(encoding='utf-8')
    linked_catalogue = profiles.link_base_rows(catalogue, roles)
    index = profiles.render_base_index(roles)

    assert len(files) == len(roles)
    for role in roles:
        path = profiles.base_profile_path(role['slug'])
        relative_path = path.removeprefix('reference/')
        assert f"[{role['name']}]({relative_path})" in linked_catalogue
        assert f"[{role['name']}]({relative_path})" in index
        page = files.get_file_from_path(path)
        assert page is not None
        assert '## Scope and routing' in page.content_string
        assert '## Required inputs' in page.content_string
        assert '## Output contracts and gates' in page.content_string
        portrait = f'assets/images/role-portraits/{role["skill"].removeprefix("it-roles-")}.webp'
        assert f'![](../../{portrait})' in page.content_string
        assert (ROOT / 'docs' / portrait).is_file()
        assert '.ai-current-profile-parent' in page.content_string


def test_base_role_profiles_explain_engineering_and_adversarial_authority():
    """Check distinctive working decisions and professionally bounded roles."""
    roles = {role['slug']: role for role in profiles._roles(ROOT)}
    engineering = profiles.render_base_profile(ROOT, roles['software-engineer'])
    assert 'Work item with acceptance criteria' in engineering
    assert 'Resolve behaviour and affected contracts' in engineering
    assert 'Professional application example' in engineering
    assert '../output-contracts/role-software-engineer.md' in engineering

    adversarial = profiles.render_base_profile(ROOT, roles['penetration-tester-api'])
    assert 'Signed authorisation and scope' in adversarial
    assert 'Written authorisation, signed scope and rules of engagement' in adversarial
    assert '## Working method' not in adversarial


def test_role_profiles_reject_inconsistent_reference_paths():
    """Reject a registry record pointing outside its canonical role reference."""
    role = profiles._roles(ROOT)[0]
    with pytest.raises(ValueError, match='Invalid base role reference'):
        profiles.render_base_profile(ROOT, {**role, 'path': '../INBOX/private.md'})
