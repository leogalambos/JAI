#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# Website of the Egothor team: https://www.egothor.org
"""Validate the one-source Markdown manual and native command help contract.

The product deliberately does not carry an installed HTML site. Provider command
metadata and the installed GUIDE.md are sufficient for local help, while the
maintained MkDocs source covers the full reference and examples. This validator
uses only Python standard library so that the structural gate is self-contained.
"""
from __future__ import annotations
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[3]
# YAML list navigation entries in the product's MkDocs layout; no YAML plugin needed.
NAV = re.compile(r'^\s*-[ \t]+(?:[^\n:]+):\s+([^\s#]+\.md)\s*$', re.M)
LINK = re.compile(r'!?\[([^\]\n]+)\]\(([^)\n]+)\)')
MEDIA = re.compile(r'<(?:img|script)[^>]+src=["\']([^"\']+)["\']')
HTML_ANCHOR = re.compile(r'<a\b[^>]*\bhref\s*=\s*["\']([^"\']+)["\']', re.I)


def _mkdocs_page_url(rel: str) -> str:
    """Return the directory-style URL that MkDocs serves for a source page."""
    if rel == 'index.md':
        return '/'
    if rel.endswith('/index.md'):
        return '/' + rel[:-len('index.md')]
    return '/' + rel[:-3] + '/'


def check(root: Path) -> list[str]:
    problems: list[str] = []
    docroot = root / 'docs'
    mkdoc = root / 'mkdocs.yml'
    if not (docroot.is_dir() and mkdoc.is_file()):
        return ['canonical docs/ directory or mkdocs.yml missing']
    markdown = {p.relative_to(docroot).as_posix(): p for p in docroot.rglob('*.md')}
    if not markdown:
        problems.append('no documentation Markdown files exist')
    navigation = NAV.findall(mkdoc.read_text(encoding='utf-8'))
    if not navigation:
        problems.append('MkDocs navigation contains no Markdown entries')
    listed = set(navigation)
    if len(listed) != len(navigation):
        problems.append('MkDocs navigation contains duplicate Markdown pages')
    for page in sorted(set(markdown) - listed):
        problems.append(f'Markdown page not included in MkDocs navigation: docs/{page}')
    for page in sorted(listed - set(markdown)):
        problems.append(f'MkDocs navigation references missing Markdown: docs/{page}')
    for rel, source in markdown.items():
        text = source.read_text(encoding='utf-8')
        # Ignore fenced samples (they may legitimately contain example broken links).
        inside = False
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith('```') or stripped.startswith('~~~'):
                inside = not inside
                continue
            if inside or line.lstrip().startswith('<!--'):
                continue
            # Markdown links resolve from the source .md file; raw HTML src
            # attributes resolve from MkDocs directory-style output URLs.
            candidates = [(href, 'markdown') for _label, href in LINK.findall(line)]
            candidates += [(href, 'html') for href in MEDIA.findall(line)]
            for destination, link_kind in candidates:
                destination = destination.strip().split(' ', 1)[0]
                target = unquote(destination.split('#', 1)[0].split('?', 1)[0]).strip('<>')
                if not target or target.startswith(('https://','http://','mailto:','tel:','data:','//','/')):
                    continue
                base = source.parent if link_kind == 'markdown' or source.stem == 'index' else source.parent / source.stem
                path = (base / target).resolve()
                try:
                    path.relative_to(docroot.resolve())
                except ValueError:
                    # Maintained docs may explicitly reference source code in parent.
                    try: path.relative_to(root.resolve())
                    except ValueError: problems.append(f'docs/{rel}:{lineno}: link escapes project: {target}')
                    else:
                        if not path.exists(): problems.append(f'docs/{rel}:{lineno}: missing source link: {target}')
                    continue
                if not path.exists():
                    problems.append(f'docs/{rel}:{lineno}: unresolved local link: {target}')
            # Markdown link targets are rewritten to MkDocs URLs, but HTML
            # <a href> values are emitted unchanged. Resolve these from the
            # rendered page URL: a sibling "page.md" link would incorrectly
            # become "/parent/current-page/page.md" and return HTTP 404.
            for href in HTML_ANCHOR.findall(line):
                href = href.strip()
                parsed = urlsplit(href)
                if not href or href.startswith(('#', '//')) or parsed.scheme or parsed.netloc:
                    continue
                rendered_path = unquote(urlsplit(urljoin(
                    'https://docs.example.invalid' + _mkdocs_page_url(rel), href
                )).path)
                if rendered_path.endswith('.md'):
                    problems.append(
                        f'docs/{rel}:{lineno}: raw HTML link to Markdown source '
                        f'is not rewritten by MkDocs: {href}; use a /page/ URL'
                    )
                    continue
                if rendered_path.endswith('/'):
                    slug = rendered_path.strip('/')
                    destinations = ([docroot / 'index.md'] if not slug else [
                        docroot / (slug + '.md'), docroot / slug / 'index.md'
                    ])
                else:
                    # Non-Markdown files retain their original asset URLs.
                    destinations = [docroot / rendered_path.lstrip('/')]
                if not any(path.is_file() for path in destinations):
                    problems.append(
                        f'docs/{rel}:{lineno}: unresolved rendered HTML link: '
                        f'{href} -> {rendered_path}'
                    )
    # The human/operator and agent/runtime boundary must be explicit in each
    # task-oriented entry. This is a product documentation contract: the
    # operational examples must never regress to being a list of Python calls.
    boundary_markers = {
        'using/interaction-model.md': ('## First: choose the interface', 'behind the scenes'),
        'using/layered-engagement.md': ('## Operator journey:', '## Behind the scenes:'),
        'operations/human-authority.md': ('## What the human does', 'Codex CLI'),
        'capabilities/justifiable-fabric.md': ('## What the operator uses', 'Behind the scenes'),
        'reference/installed-cli-guide.md': ('## Operator versus runtime:', '## 5. Direct tools for maintainers'),
        'reference/runtime-tools-detailed.md': ('## Intended reader and invocation boundary', 'developer/maintainer'),
        'getting-started/quick-start.md': ('Claude command | Codex skill', 'special Codex'),
        'runtime-reference/current-help.md': ('## Editorial contract:', 'operator → behind-the-scenes'),
    }
    for name, markers in boundary_markers.items():
        content = (docroot / name).read_text(encoding='utf-8') if name in markdown else ''
        if not content or any(marker not in content for marker in markers):
            problems.append(f'docs/{name}: missing CLI-user versus runtime boundary')
    for name in sorted(markdown):
        content = markdown[name].read_text(encoding='utf-8')
        if name.startswith('examples/') and '## Run this scenario in the provider CLI' not in content:
            problems.append(f'docs/{name}: scenario lacks operator entry and implementation boundary')
        if name.startswith('workflow-library/') and '## Running this workflow: operator and implementer boundary' not in content:
            problems.append(f'docs/{name}: workflow lacks operator versus implementer boundary')
    layer_path = docroot / 'using/layered-engagement.md'
    if layer_path.is_file():
        user_half = layer_path.read_text(encoding='utf-8').split('## Behind the scenes:', 1)[0]
        if 'python3 ~/.ai/it-role-house/' in user_half:
            problems.append('docs/using/layered-engagement.md: internal Python invocation in operator journey')

    # Check deterministic local diagrams as actual XML, not only link existence.
    for diagram in (docroot/'assets/diagrams').rglob('*.svg'):
        try: ET.parse(diagram)
        except ET.ParseError as exc:
            problems.append(f'malformed SVG {diagram.relative_to(root)}: {exc}')
    if 'hooks/jai_repository_links.py' not in mkdoc.read_text(encoding='utf-8'):
        problems.append('MkDocs must resolve product VERSION and repository metadata through its source hook')
    # Installed help derives from provider command contracts and GUIDE, not HTML.
    if (root / '.ai/runtime/docs').exists():
        problems.append('obsolete installed HTML documentation directory returned')
    if (root / '.ai/runtime/tools/generate_runtime_help.py').exists():
        problems.append('obsolete HTML help generator returned')
    for obsolete in ('SIGNING.md','CLEANUP-REPORT.md'):
        if (root / obsolete).exists():
            problems.append(f'owner-only release memo in customer package: {obsolete}')
    # CI definitions are executed only when located in GitHub's workflow directory.
    for workflow in ('pages.yml', 'validate-library.yml'):
        if not (root / '.github/workflows' / workflow).is_file():
            problems.append(f'active GitHub Actions workflow missing: {workflow}')
    guide = root / '.ai/runtime/GUIDE.md'
    command_dir = root / '.ai/commands'
    if not guide.is_file():
        problems.append('installed CLI GUIDE.md missing')
    elif (root/'docs/reference/installed-cli-guide.md').read_bytes() != guide.read_bytes():
        problems.append('installed GUIDE.md drift: regenerate from docs/reference/installed-cli-guide.md')
    if not command_dir.is_dir():
        problems.append('provider command contracts missing')
    else:
        guide_text = guide.read_text(encoding='utf-8')
        reference = (root / 'docs/reference/commands.md').read_text(encoding='utf-8')
        for command in sorted(command_dir.glob('*.md')):
            slug = command.stem
            content = command.read_text(encoding='utf-8')
            if 'description:' not in content[:500]:
                problems.append(f'command frontmatter description missing: {slug}')
            if f'### /{slug}\n' not in guide_text:
                problems.append(f'installed GUIDE.md does not cover /{slug}')
            if f'/{slug}' not in reference:
                problems.append(f'Markdown command reference does not cover /{slug}')
            if 'docs/index.html' in content or '.ai/runtime/docs/' in content:
                problems.append(f'command points to discontinued runtime HTML: {slug}')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    problems = check(root)
    if problems:
        print(f'FAIL documentation contract ({len(problems)} problem(s))')
        for problem in problems: print(' -', problem)
        return 1
    print(f'PASS Markdown documentation contract: {len(list((root/"docs").rglob("*.md")))} pages; provider commands and GUIDE; no installed HTML')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
