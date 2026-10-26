# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Render canonical homepage navigation and resolve source-authored release URLs.

Navigation comes from the same resolved MkDocs tree as the Material sidebar
and page footers. All substitutions happen before Markdown is rendered.

GitHub supplies GITHUB_REPOSITORY for Pages and PR workflows. For a local
clone the origin remote is sufficient; an unpacked ZIP needs an explicit
JAI_GITHUB_REPOSITORY=owner/repository setting. Fail closed on missing identity.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

from mkdocs.utils import get_relative_url

REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
REPOSITORY_TOKEN = "__JAI_GITHUB_REPOSITORY__"
PRODUCT_VERSION_TOKEN = "{{ JAI_VERSION }}"
PRODUCT_VERSION_RE = re.compile(r"[0-9]{2}\.(?:0[1-9]|1[0-2])\.[0-9]+\Z")
RELEASE_INVENTORY_TOKEN = "{{ JAI_RELEASE_INVENTORY }}"
HOME_NAV_TOKEN = "<!-- JAI_CANONICAL_NAVIGATION -->"
_navigation = None


def on_nav(nav, *, config, files):
    """Retain the resolved MkDocs navigation for this build and return it unchanged.

    Args:
        nav: MkDocs Navigation built from the canonical configuration.
        config: MkDocs configuration (unused).
        files: MkDocs file collection (unused).

    Returns:
        The original navigation object; no pages or links are added.
    """
    global _navigation
    _navigation = nav
    return nav


def render_navigation(nav, page) -> str:
    """Render the canonical MkDocs tree as accessible, collapsible homepage HTML.

    Args:
        nav: Resolved MkDocs Navigation, including sections, pages and links.
        page: Current MkDocs page; its output URL is the relative-link base.

    Returns:
        Escaped HTML with current-page state and native disclosure controls.

    Raises:
        ValueError: A link uses a non-web URI scheme.
    """
    def contains_current(item):
        children = getattr(item, "children", None) or ()
        return item is page or any(contains_current(child) for child in children)

    def render(items, depth=0):
        result = ['<ul class="ai-canonical-nav-list">']
        for index, item in enumerate(items):
            title = escape(str(item.title))
            children = getattr(item, "children", None) or ()
            if children:
                # The learning section provides an initial foothold; the remainder
                # stays collapsed until requested, including on narrow screens.
                opened = contains_current(item) or (depth == 0 and index == 2)
                result.append(f'<li><details{" open" if opened else ""}><summary>{title}</summary>')
                result.append(render(children, depth + 1))
                result.append('</details></li>')
            else:
                url = str(item.url)
                scheme = urlsplit(url).scheme.lower()
                if scheme and scheme not in {"http", "https", "mailto"}:
                    raise ValueError(f"Unsupported navigation URL scheme: {scheme}")
                href = url if scheme or url.startswith(("/", "#")) else get_relative_url(url, page.url)
                current = ' class="active" aria-current="page"' if item is page else ''
                result.append(f'<li><a{current} href="{escape(href, quote=True)}">{title}</a></li>')
        result.append('</ul>')
        return ''.join(result)

    return render(nav.items)


def repository_from_remote(root: Path) -> str | None:
    """Read origin from a local checkout, without contacting GitHub."""
    try:
        raw = subprocess.run(
            ["git", "-C", str(root), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    m = re.fullmatch(r"(?:https://github\.com/|git@github\.com:)([^\s]+?)(?:\.git)?/?", raw)
    return m.group(1) if m else None


def resolved_repository(root: Path, env: dict[str, str] | None = None) -> str:
    """Find an unambiguous OWNER/REPO value; refuse invalid substitutions."""
    vars = os.environ if env is None else env
    repo = vars.get("JAI_GITHUB_REPOSITORY") or vars.get("GITHUB_REPOSITORY")
    if not repo:
        repo = repository_from_remote(root)
    if not repo or not REPO.fullmatch(repo):
        raise ValueError(
            "JAI repository identity unknown. Set JAI_GITHUB_REPOSITORY=OWNER/JAI "
            "for a local MkDocs build, or use GitHub Actions (GITHUB_REPOSITORY)."
        )
    return repo


def expand_homepage(markdown: str, repository: str) -> str:
    """The CTA markup is part of docs/index.md; only its href values vary."""
    if not REPO.fullmatch(repository):
        raise ValueError("Invalid OWNER/REPO repository identity")
    # Keep URLs recognisably external for the existing docs_contract.py
    # 404/link validator, which examines unrendered Markdown source.
    expected = (
        f'href="https://github.com/{REPOSITORY_TOKEN}"',
        f'href="https://github.com/{REPOSITORY_TOKEN}/releases"',
    )
    for source in expected:
        if markdown.count(source) != 1:
            raise ValueError(f"Expected exactly one source-authored homepage URL: {source}")
    return markdown.replace(REPOSITORY_TOKEN, repository)


def render_release_inventory(root: Path) -> str:
    """Render release counts and agent IDs from the generated canonical manifest.

    Args:
        root: Checkout root containing VERSION and the runtime release manifest.

    Returns:
        Markdown tables of registered inventory counts and exact agent identifiers.

    Raises:
        ValueError: Manifest identity, counts or enumerated membership is invalid.
        OSError: Authoritative release files cannot be read.
    """
    manifest = json.loads((root / ".ai/runtime/_meta/release-manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("release") != (root / "VERSION").read_text(encoding="utf-8").strip():
        raise ValueError("Inventory manifest does not match authoritative VERSION")
    labels = {
        "roles": "Role definitions", "agents": "Agent procedures",
        "skills": "Shared skills", "workflows": "Enterprise workflow chains",
        "artifact_types": "Artifact types", "schemas": "Registered schemas",
        "renderers": "Renderer entries", "tests": "Registered qualification checks",
        "provider_adapters": "Provider adapters",
    }
    counts = manifest.get("counts")
    if not isinstance(counts, dict) or any(type(counts.get(key)) is not int or counts[key] < 0 for key in labels):
        raise ValueError("Inventory requires non-negative integer counts")
    for key in ("agents", "skills", "renderers", "tests", "provider_adapters"):
        values = manifest.get(key)
        if not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values):
            raise ValueError(f"Invalid inventory membership: {key}")
        if len(values) != counts[key] or len(set(values)) != len(values):
            raise ValueError(f"Inventory count/membership mismatch: {key}")
    if any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) for name in manifest["agents"]):
        raise ValueError("Invalid inventory agent identifier")
    rows = ["| Component | Registered count |", "| --- | ---: |"]
    rows.extend(f"| {label} | {counts[key]} |" for key, label in labels.items())
    rows.extend(["", "## Registered agent procedures", "", "| Agent identifier |", "| --- |"])
    rows.extend(f"| `{name}` |" for name in manifest["agents"])
    return "\n".join(rows)


def render_role_coverage(root: Path) -> str:
    """Return homepage role/domain coverage derived from canonical registry rows.

    Args:
        root: Checkout containing .ai/runtime/roles.json.
    Returns:
        Plain English role and domain count; no hardcoded inventory values.
    Raises:
        ValueError: Count, role identity or skill-domain metadata is invalid.
        OSError: Canonical registry cannot be read.
    """
    registry = json.loads((root / ".ai/runtime/roles.json").read_text(encoding="utf-8"))
    roles = registry.get("roles")
    if (not isinstance(roles, list) or registry.get("count") != len(roles)
            or any(not isinstance(role, dict) or not isinstance(role.get("slug"), str)
                   or not isinstance(role.get("skill"), str)
                   or not role["skill"].startswith("it-roles-") for role in roles)
            or len({role["slug"] for role in roles}) != len(roles)):
        raise ValueError("Invalid canonical role coverage")
    return f"{len(roles)} IS/IT roles across {len({role['skill'] for role in roles})} domains"


def render_discipline_coverage(root: Path) -> str:
    """Render current domain counts and representative names from canonical roles.

    Args:
        root: Checkout containing the canonical runtime roles.json registry.
    Returns:
        Markdown table with one row per skill domain and up to four role names.
    Raises:
        ValueError: Registry identity, domain labels or role names are invalid.
        OSError: The registry cannot be read.
    """
    render_role_coverage(root)
    roles = json.loads((root / '.ai/runtime/roles.json').read_text(encoding='utf-8'))['roles']
    domains = {}
    for role in roles:
        label, name = role.get('category'), role.get('name')
        if any(not isinstance(value, str) or not value.strip() or '\n' in value or '\r' in value
               for value in (label, name)):
            raise ValueError('Invalid canonical discipline label or role name')
        domain = domains.setdefault(role['skill'], {'label': label, 'names': []})
        if domain['label'] != label:
            raise ValueError('Inconsistent canonical discipline label')
        domain['names'].append(name)
    rows = ['| Discipline | Roles | Representative roles |', '| --- | ---: | --- |']
    for domain in sorted(domains.values(), key=lambda item: item['label']):
        label = escape(domain['label']).replace('|', '&#124;')
        names = ', '.join(escape(name).replace('|', '&#124;') for name in domain['names'][:4])
        rows.append(f"| {label} | {len(domain['names'])} | {names} |")
    return '\n'.join(rows)


def render_schema_count(root: Path) -> str:
    """Return the registered schema count for the authoritative current release.

    Args:
        root: Checkout containing VERSION and the generated release manifest.
    Returns:
        Non-negative schema count as decimal text for Markdown substitution.
    Raises:
        ValueError: Manifest identity or schema count is invalid.
        OSError: Authoritative release files cannot be read.
    """
    manifest = json.loads((root / '.ai/runtime/_meta/release-manifest.json').read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('release') != (root / 'VERSION').read_text(encoding='utf-8').strip():
        raise ValueError('Schema manifest does not match authoritative VERSION')
    counts = manifest.get('counts')
    if not isinstance(counts, dict) or type(counts.get('schemas')) is not int or counts['schemas'] < 0:
        raise ValueError('Invalid registered schema count')
    return str(counts['schemas'])


def on_page_markdown(markdown, *, page, config, files):
    """Expand release inventory, version, CTA URLs and canonical navigation.

    Args:
        markdown: Source Markdown for the current page.
        page: Current MkDocs page.
        config: MkDocs configuration (unused).
        files: MkDocs file collection (unused).

    Returns:
        Markdown with canonical release inventory and navigation substitutions.

    Raises:
        ValueError: Required homepage markup, navigation or release metadata is invalid.
    """
    root = Path(__file__).resolve().parents[1]
    if RELEASE_INVENTORY_TOKEN in markdown:
        markdown = markdown.replace(RELEASE_INVENTORY_TOKEN, render_release_inventory(root))
    if "{{ JAI_ROLE_COVERAGE }}" in markdown:
        markdown = markdown.replace("{{ JAI_ROLE_COVERAGE }}", render_role_coverage(root))
    if "{{ JAI_DISCIPLINE_COVERAGE }}" in markdown:
        markdown = markdown.replace("{{ JAI_DISCIPLINE_COVERAGE }}", render_discipline_coverage(root))
    if "{{ JAI_SCHEMA_COUNT }}" in markdown:
        markdown = markdown.replace("{{ JAI_SCHEMA_COUNT }}", render_schema_count(root))
    if '{{ JAI_SCOPE }}' in markdown:
        sys.path.insert(0,str(root/'.ai/runtime/tools'))
        from schema_resolver import release_scope
        markdown=markdown.replace('{{ JAI_SCOPE }}',release_scope(root)['scope'])
    if PRODUCT_VERSION_TOKEN in markdown:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        if not PRODUCT_VERSION_RE.fullmatch(version):
            raise ValueError("invalid authoritative product VERSION")
        markdown = markdown.replace(PRODUCT_VERSION_TOKEN, version)
    if page.file.src_uri == "index.md":
        markdown = expand_homepage(markdown, resolved_repository(root))
        if markdown.count(HOME_NAV_TOKEN) != 1 or _navigation is None:
            raise ValueError("Homepage requires exactly one canonical navigation marker and a resolved MkDocs tree")
        markdown = markdown.replace(HOME_NAV_TOKEN, render_navigation(_navigation, page))
    return markdown
