# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Resolve source-authored GitHub CTA href values, never inject HTML post-build.

GitHub supplies GITHUB_REPOSITORY for Pages and PR workflows. For a local
clone the origin remote is sufficient; an unpacked ZIP needs an explicit
JAI_GITHUB_REPOSITORY=owner/repository setting. Fail closed on missing identity.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
REPOSITORY_TOKEN = "__JAI_GITHUB_REPOSITORY__"
PRODUCT_VERSION_TOKEN = "{{ JAI_VERSION }}"
PRODUCT_VERSION_RE = re.compile(r"[0-9]{2}\.(?:0[1-9]|1[0-2])\.[0-9]+\Z")


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


def on_page_markdown(markdown, *, page, config, files):
    """MkDocs hook: expand the source VERSION and only source-authored CTA URLs."""
    root = Path(__file__).resolve().parents[1]
    if PRODUCT_VERSION_TOKEN in markdown:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        if not PRODUCT_VERSION_RE.fullmatch(version):
            raise ValueError("invalid authoritative product VERSION")
        markdown = markdown.replace(PRODUCT_VERSION_TOKEN, version)
    if page.file.src_uri == "index.md":
        markdown = expand_homepage(markdown, resolved_repository(root))
    return markdown
