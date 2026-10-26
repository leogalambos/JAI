# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Small, offline regressions for homepage source URLs and release tag rules."""
from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


links = load('hooks/jai_repository_links.py', 'jai_repository_links')
tags = load('scripts/validate_release_tag.py', 'jai_validate_release_tag')


class SourceHomeCtaTests(unittest.TestCase):
    def test_hero_urls_are_source_authored_and_expanded(self):
        raw = (ROOT / 'docs/index.md').read_text(encoding='utf-8')
        self.assertIn('ai-home-actions-v31', raw)
        self.assertIn('Download JAI', raw)
        repository_href = 'href="https://github.com/__JAI_GITHUB_REPOSITORY__"'
        self.assertEqual(raw.count(repository_href), 1)
        rendered = links.expand_homepage(raw, 'some-owner/JAI')
        self.assertIn('href="https://github.com/some-owner/JAI/releases"', rendered)
        self.assertIn('href="https://github.com/some-owner/JAI"', rendered)
        self.assertNotIn('__JAI_GITHUB_', rendered)
        self.assertIn('href="getting-started/quick-start/"', rendered)
        self.assertIn('href="overview/product-overview/"', rendered)
        self.assertIn('href="security/product-operations/"', rendered)

    def test_strictly_rejects_invalid_repository_values(self):
        raw = (ROOT / 'docs/index.md').read_text(encoding='utf-8')
        for bad in ('owner', 'owner/repo/evil', 'owner/" onclick="x()'):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                links.expand_homepage(raw, bad)

    def test_requires_both_explicit_source_links(self):
        raw = (ROOT / 'docs/index.md').read_text(encoding='utf-8')
        for url in ('https://github.com/__JAI_GITHUB_REPOSITORY__/releases',
                    'https://github.com/__JAI_GITHUB_REPOSITORY__'):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, 'exactly one'):
                links.expand_homepage(raw.replace('href="'+url+'"', 'href=""'), 'owner/JAI')

    def test_github_actions_repo_context(self):
        with patch.object(links, 'repository_from_remote', return_value=None):
            self.assertEqual(links.resolved_repository(ROOT, {'GITHUB_REPOSITORY': 'team/JAI'}), 'team/JAI')
            with self.assertRaisesRegex(ValueError, 'unknown'):
                links.resolved_repository(ROOT, {})


class ReleaseTagTests(unittest.TestCase):
    def test_tag_matches_authoritative_source_version(self):
        version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
        self.assertEqual(tags.version_for_tag(ROOT, f'release@{version}'), version)
        yy, mm, vv = version.split('.')
        other = f'release@{yy}.{mm}.{int(vv) + 1}'
        with self.assertRaisesRegex(ValueError, 'does not match source VERSION'):
            tags.version_for_tag(ROOT, other)

    def test_mkdocs_version_token_expands_from_version_file(self):
        raw = (ROOT / 'docs/runtime-reference/current-help.md').read_text()
        self.assertIn(links.PRODUCT_VERSION_TOKEN, raw)
        fake_page = type('Page', (), {'file': type('File', (), {'src_uri': 'runtime-reference/current-help.md'})()})()
        text = links.on_page_markdown(raw, page=fake_page, config=None, files=None)
        self.assertNotIn(links.PRODUCT_VERSION_TOKEN, text)
        self.assertIn((ROOT / 'VERSION').read_text().strip(), text)

    def test_invalid_versions_fail_closed(self):
        version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
        yy, mm, vv = version.split('.')
        other = f'{yy}.{mm}.{int(vv) + 1}'
        for bad in (f'v{version}', f'release@{yy}.13.{vv}',
                    f'release@{version}-rc1',
                    f'release@{version}/evil'):
            with self.subTest(tag=bad), self.assertRaises(ValueError):
                tags.version_for_tag(ROOT, bad)


if __name__ == '__main__':
    unittest.main()
