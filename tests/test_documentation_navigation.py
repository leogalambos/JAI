# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Regression tests for one canonical navigation tree and homepage rendering."""
from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest

import yaml
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('navigation_hook', ROOT / 'hooks/jai_repository_links.py')
links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(links)


class DocumentationVersionChromeTests(unittest.TestCase):
    def test_footer_displays_canonical_version_after_copyright_without_a_banner(self):
        from jinja2 import DictLoader, Environment

        environment = Environment(loader=DictLoader({
            'copyright.html': (ROOT / 'overrides/partials/copyright.html').read_text(),
        }))
        rendered = environment.get_template('copyright.html').render(config={
            'copyright': 'Copyright example',
            'extra': {'jai_product_version': '26.11.1', 'generator': False}})
        self.assertIn('Documentation 26.11.1', rendered)
        self.assertLess(rendered.index('Copyright example'), rendered.index('Documentation 26.11.1'))
        self.assertNotIn('{% block announce %}', (ROOT / 'overrides/main.html').read_text())

    def test_sitewide_version_uses_root_authority_and_preserves_other_metadata(self):
        config = {'extra': {'jai_product_version': 'stale', 'generator': False}}
        self.assertIs(links.on_config(config), config)
        self.assertEqual(config['extra']['jai_product_version'],
                         (ROOT / 'VERSION').read_text().strip())
        self.assertFalse(config['extra']['generator'])

    def test_sitewide_version_refuses_malformed_source_instead_of_claiming_a_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'hooks').mkdir()
            (root / 'VERSION').write_text('not-a-version\n')
            with patch.object(links, '__file__', str(root / 'hooks/jai_repository_links.py')):
                with self.assertRaisesRegex(ValueError, 'authoritative product VERSION'):
                    links.on_config({})


def page(title, url, source='index.md'):
    return SimpleNamespace(title=title, url=url, children=None, file=SimpleNamespace(src_uri=source))


def section(title, *children):
    return SimpleNamespace(title=title, children=list(children))


class CanonicalNavigationTests(unittest.TestCase):
    def test_resolved_tree_changes_are_reflected_without_a_second_catalogue(self):
        home = page('Home', '')
        target = page('New title & purpose', 'renamed/path/')
        tree = SimpleNamespace(items=[home, section('New group', target)])
        self.assertIs(links.on_nav(tree, config=None, files=None), tree)
        with patch.object(links, 'resolved_repository', return_value='team/JAI'):
            text = links.on_page_markdown((ROOT / 'docs/index.md').read_text(), page=home, config=None, files=None)
        self.assertIn('<summary>New group</summary>', text)
        self.assertIn('New title &amp; purpose', text)
        self.assertIn('href="renamed/path/"', text)
        self.assertNotIn(links.HOME_NAV_TOKEN, text)
        self.assertIn('aria-current="page"', text)
        self.assertIn('https://github.com/team/JAI/releases', text)

    def test_home_collapses_groups_without_hiding_any_canonical_links(self):
        home = page('Home', '')
        install = page('Install', 'start/install/')
        learn = page('Learn', 'using/learn/')
        tree = SimpleNamespace(items=[home, section('Start', install), section('Use', learn)])
        rendered = links.render_navigation(tree, home)
        self.assertNotIn('<details open>', rendered)
        self.assertEqual(rendered.count('<details>'), 2)
        self.assertIn('href="start/install/"', rendered)
        self.assertIn('href="using/learn/"', rendered)
        self.assertEqual(rendered.count('aria-current="page"'), 1)
        self.assertIn('<details open><summary>Use</summary>', links.render_navigation(tree, learn))

    def test_relative_urls_work_for_nested_pages_and_non_directory_outputs(self):
        current = page('Current', 'guide/current/index.html')
        target = page('Target', 'guide/other.html')
        tree = SimpleNamespace(items=[section('Guide', current, target), page('External', 'https://example.org/project/')])
        rendered = links.render_navigation(tree, current)
        self.assertIn('href="../other.html"', rendered)
        self.assertIn('href="https://example.org/project/"', rendered)
        self.assertIn('<details open>', rendered)
        self.assertEqual(rendered.count('aria-current="page"'), 1)

    def test_unsafe_titles_are_escaped_and_unsafe_schemes_rejected(self):
        current = page('Home', '')
        tree = SimpleNamespace(items=[section('<img src=x>', page('"Unsafe"', 'safe/'))])
        rendered = links.render_navigation(tree, current)
        self.assertIn('&lt;img src=x&gt;', rendered)
        self.assertNotIn('<img', rendered)
        with self.assertRaises(ValueError):
            links.render_navigation(SimpleNamespace(items=[page('Bad', 'javascript:alert(1)')]), current)

    def test_empty_tree_and_build_reset_do_not_reuse_old_links(self):
        home = page('Home', '')
        links.on_nav(SimpleNamespace(items=[page('Old link', 'old/')]), config=None, files=None)
        empty = SimpleNamespace(items=[])
        links.on_nav(empty, config=None, files=None)
        self.assertEqual(links.render_navigation(empty, home), '<ul class="ai-canonical-nav-list"></ul>')
        self.assertNotIn('Old link', links.render_navigation(links._navigation, home))

    def test_missing_or_duplicate_marker_and_uninitialized_build_fail_closed(self):
        raw = (ROOT / 'docs/index.md').read_text()
        home = page('Home', '')
        for source in (raw.replace(links.HOME_NAV_TOKEN, ''), raw + links.HOME_NAV_TOKEN):
            with patch.object(links, 'resolved_repository', return_value='team/JAI'), self.assertRaises(ValueError):
                links.on_page_markdown(source, page=home, config=None, files=None)
        with patch.object(links, '_navigation', None), patch.object(links, 'resolved_repository', return_value='team/JAI'), self.assertRaises(ValueError):
            links.on_page_markdown(raw, page=home, config=None, files=None)

    def test_remote_identity_has_no_network_dependency(self):
        with patch.object(links.subprocess, 'run', return_value=SimpleNamespace(stdout='git@github.com:team/JAI.git\n')) as run:
            self.assertEqual(links.repository_from_remote(ROOT), 'team/JAI')
            self.assertEqual(run.call_args.args[0][-3:], ['remote', 'get-url', 'origin'])
        with patch.object(links.subprocess, 'run', side_effect=OSError):
            self.assertIsNone(links.repository_from_remote(ROOT))

    def test_real_build_uses_changed_configuration_and_preserves_project_prefix(self):
        from mkdocs.commands.build import build
        from mkdocs.config import load_config

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'docs').mkdir()
            (root / 'hooks').mkdir()
            (root / 'hooks/links.py').write_text((ROOT / 'hooks/jai_repository_links.py').read_text())
            (root / 'docs/index.md').write_text(
                '# Home\n<nav>' + links.HOME_NAV_TOKEN + '</nav>\n'
                '<a href="https://github.com/__JAI_GITHUB_REPOSITORY__">Source</a>\n'
                '<a href="https://github.com/__JAI_GITHUB_REPOSITORY__/releases">Download</a>\n')
            (root / 'docs/first.md').write_text('# First\n' + links.RELEASE_INVENTORY_TOKEN + '\n')
            (root / '.ai/runtime/_meta').mkdir(parents=True)
            (root / '.ai/runtime/_meta/release-manifest.json').write_text((ROOT / '.ai/runtime/_meta/release-manifest.json').read_text())
            (root / 'VERSION').write_text((ROOT / 'VERSION').read_text())
            (root / 'docs/second.md').write_text('# Second\n')
            config_path = root / 'mkdocs.yml'
            for title, order in [('Original group', ['first', 'second']), ('Revised group', ['second', 'first'])]:
                config_path.write_text(
                    'site_name: Fixture\nsite_url: https://example.org/project/\n'
                    'theme:\n  name: material\n  features: [navigation.footer]\n'
                    'hooks: [hooks/links.py]\nnav:\n  - Home: index.md\n  - ' + title + ':\n' +
                    ''.join('      - ' + slug.title() + ': ' + slug + '.md\n' for slug in order))
                with patch.dict('os.environ', {'JAI_GITHUB_REPOSITORY': 'team/JAI'}):
                    build(load_config(config_file=str(config_path)), dirty=False)
                home = (root / 'site/index.html').read_text()
                self.assertIn('<summary>' + title + '</summary>', home)
                self.assertIn('href="first/"', home)
                self.assertIn('href="second/"', home)
                self.assertNotIn(links.HOME_NAV_TOKEN, home)
                first_html = (root / 'site/first/index.html').read_text()
                self.assertNotIn('Registered qualification checks', first_html)
                self.assertIn('commercial-coordinator', first_html)
                self.assertNotIn(links.RELEASE_INVENTORY_TOKEN, first_html)
                footer = first_html.split('<nav class="md-footer__inner', 1)[1].split('</nav>', 1)[0]
                if order[0] == 'first':
                    self.assertIn('aria-label="Next: Second"', footer)
                else:
                    self.assertIn('aria-label="Previous: Second"', footer)
                    self.assertNotIn('aria-label="Next: Second"', footer)

    def test_inventory_follows_manifest_counts_and_identifiers(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / '.ai/runtime/_meta/release-manifest.json'
            target.parent.mkdir(parents=True)
            manifest = json.loads((ROOT / '.ai/runtime/_meta/release-manifest.json').read_text())
            (root / 'VERSION').write_text(manifest['release'])
            manifest['agents'].append('new-agent')
            manifest['counts']['agents'] += 1
            target.write_text(json.dumps(manifest))
            rendered = links.render_release_inventory(root)
            self.assertIn('| Agent procedures | ' + str(manifest['counts']['agents']) + ' |', rendered)
            self.assertIn('`new-agent`', rendered)
            self.assertNotIn('Registered qualification checks', rendered)
            manifest['agents'].remove('new-agent')
            manifest['agents'][0] = 'renamed-agent'
            manifest['counts']['agents'] -= 1
            target.write_text(json.dumps(manifest))
            self.assertIn('`renamed-agent`', links.render_release_inventory(root))
            self.assertNotIn('`new-agent`', links.render_release_inventory(root))

    def test_invalid_inventory_fails_instead_of_displaying_stale_counts(self):
        original = json.loads((ROOT / '.ai/runtime/_meta/release-manifest.json').read_text())
        invalid = []
        for field, replacement in [('agents', 0), ('schemas', True), ('roles', -1)]:
            broken = json.loads(json.dumps(original))
            broken['counts'][field] = replacement
            invalid.append(broken)
        broken = json.loads(json.dumps(original))
        broken['agents'][0] = '<script>'
        invalid.extend([broken, {'release': '0.0.0'}, [], {'release': original['release'], 'counts': {}}])
        broken = json.loads(json.dumps(original))
        broken['agents'][0] = broken['agents'][1]
        invalid.append(broken)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / '.ai/runtime/_meta/release-manifest.json'
            target.parent.mkdir(parents=True)
            (root / 'VERSION').write_text(original['release'])
            for manifest in invalid:
                with self.subTest(manifest=manifest):
                    target.write_text(json.dumps(manifest))
                    with self.assertRaises(ValueError):
                        links.render_release_inventory(root)
            target.unlink()
            with self.assertRaises(OSError):
                links.render_release_inventory(root)

    def test_every_document_has_one_canonical_navigation_entry_and_method_precedes_cases(self):
        config = (ROOT / 'mkdocs.yml').read_text()
        nav = yaml.safe_load(config.split('\nnav:\n', 1)[1])
        paths = []

        def collect(entries):
            for entry in entries:
                self.assertIsInstance(entry, dict)
                self.assertEqual(len(entry), 1)
                target = next(iter(entry.values()))
                if isinstance(target, list):
                    collect(target)
                else:
                    self.assertIsInstance(target, str)
                    paths.append(target)

        collect(nav)
        documents = {str(p.relative_to(ROOT / 'docs')) for p in (ROOT / 'docs').rglob('*.md')}
        self.assertNotIn('    - navigation.instant', config)
        self.assertIn('    - navigation.footer', config)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), documents)
        for document in documents:
            self.assertNotIn('<!-- AI-PAGE-NAV -->', (ROOT / 'docs' / document).read_text(), document)
        self.assertLess(paths.index('using/methodical-workflows.md'), paths.index('examples/how-to-use-JAI/security-assessment.md'))
        self.assertLess(paths.index('using/layered-engagement.md'), paths.index('examples/how-to-use-JAI/android-development.md'))
        home = (ROOT / 'docs/index.md').read_text()
        sidebars = re.findall(r'<nav\b[^>]*\bclass="ai-sidebar-nav-v31"[^>]*>(.*?)</nav>', home, re.S)
        self.assertEqual(len(sidebars), 1)
        sidebar = sidebars[0]
        self.assertIn(links.HOME_NAV_TOKEN, sidebar)
        self.assertNotIn('<a ', sidebar)


if __name__ == '__main__':
    unittest.main()


class CanonicalRoleCoverageTests(unittest.TestCase):
    def test_discipline_table_tracks_real_registry_membership_and_escapes_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / '.ai/runtime/roles.json'
            registry.parent.mkdir(parents=True)
            rows = [
                {'slug': 'one', 'skill': 'it-roles-a', 'category': 'Area A', 'name': 'One'},
                {'slug': 'two', 'skill': 'it-roles-a', 'category': 'Area A', 'name': 'Two'},
                {'slug': 'three', 'skill': 'it-roles-b', 'category': 'Area <B>', 'name': 'Three | safe'},
            ]
            registry.write_text(json.dumps({'count': 3, 'roles': rows}))
            rendered = links.render_discipline_coverage(root)
            self.assertIn('| Area A | 2 | One, Two |', rendered)
            self.assertIn('| Area &lt;B&gt; | 1 | Three &#124; safe |', rendered)
            rows.pop()
            registry.write_text(json.dumps({'count': 2, 'roles': rows}))
            self.assertNotIn('Area &lt;B&gt;', links.render_discipline_coverage(root))
            registry.write_text(json.dumps({'count': 0, 'roles': []}))
            self.assertEqual(len(links.render_discipline_coverage(root).splitlines()), 2)

    def test_discipline_table_rejects_malformed_or_inconsistent_domain_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / '.ai/runtime/roles.json'
            registry.parent.mkdir(parents=True)
            first = {'slug': 'one', 'skill': 'it-roles-a', 'category': 'Area A', 'name': 'One'}
            for changed in ({'category': ''}, {'name': 7}, {'category': 'Other'}, {'name': 'Bad\nrow'}):
                second = dict(first, slug='two', name='Two')
                second.update(changed)
                registry.write_text(json.dumps({'count': 2, 'roles': [first, second]}))
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    links.render_discipline_coverage(root)

    def test_schema_count_follows_manifest_and_fails_closed_on_invalid_or_stale_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / '.ai/runtime/_meta/release-manifest.json'
            target.parent.mkdir(parents=True)
            (root / 'VERSION').write_text('26.10.4')
            for count in (0, 33, 34):
                target.write_text(json.dumps({'release': '26.10.4', 'counts': {'schemas': count}}))
                self.assertEqual(links.render_schema_count(root), str(count))
            for manifest in ({'release': '26.10.3', 'counts': {'schemas': 33}},
                             {'release': '26.10.4', 'counts': {'schemas': True}},
                             {'release': '26.10.4', 'counts': {'schemas': -1}}, {}):
                target.write_text(json.dumps(manifest))
                with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                    links.render_schema_count(root)

    def test_public_coverage_tokens_expand_on_non_home_pages(self):
        source = '{{ JAI_DISCIPLINE_COVERAGE }}\n{{ JAI_SCHEMA_COUNT }}'
        rendered = links.on_page_markdown(source, page=page('Coverage', 'overview/coverage-matrix/', 'overview/coverage-matrix.md'), config=None, files=None)
        self.assertNotIn('{{ JAI_', rendered)
        self.assertIn('| Commercial, Sourcing and Enablement | 20 |', rendered)

    def test_render_role_coverage_tracks_changed_rows_and_domain_membership(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / '.ai/runtime/roles.json'
            registry.parent.mkdir(parents=True)
            registry.write_text(json.dumps({'count': 0, 'roles': []}))
            self.assertEqual(links.render_role_coverage(root), '0 IS/IT roles across 0 domains')
            rows = [{'slug': 'one', 'skill': 'it-roles-a'}, {'slug': 'two', 'skill': 'it-roles-a'}, {'slug': 'three', 'skill': 'it-roles-b'}]
            registry.write_text(json.dumps({'count': 3, 'roles': rows}))
            self.assertEqual(links.render_role_coverage(root), '3 IS/IT roles across 2 domains')
            registry.write_text(json.dumps({'count': 4, 'roles': rows}))
            with self.assertRaises(ValueError): links.render_role_coverage(root)
            rows[2]['slug'] = 'one'
            registry.write_text(json.dumps({'count': 3, 'roles': rows}))
            with self.assertRaises(ValueError): links.render_role_coverage(root)


def test_public_pages_do_not_expose_empty_front_matter_as_separators():
    """Metadata removal must not leave visible separators above page content."""
    for path in (ROOT / 'docs').rglob('*.md'):
        source = path.read_text(encoding='utf-8')
        assert not re.match(r'\A---\s*\n---(?:\n|$)', source), path


def test_public_catalogues_describe_all_canonical_deliverables_and_handoffs():
    """Every retained profession and workflow has concrete, discoverable outputs."""
    roles = json.loads((ROOT / '.ai/runtime/roles.json').read_text())['roles']
    role_page = (ROOT / 'docs/reference/roles.md').read_text()
    for role in roles:
        row = next(line for line in role_page.splitlines()
                   if line.startswith(f"| {role['name']} |"))
        for output in role['primary_deliverables']:
            assert output.replace('|', '&#124;').replace('\n', ' ') in row
    workflows = json.loads((ROOT / '.ai/runtime/workflows.json').read_text())['workflows']
    workflow_page = (ROOT / 'docs/reference/workflows.md').read_text()
    for workflow in workflows:
        section = workflow_page.split('## ' + workflow['title'] + '\n', 1)[1].split('\n## ', 1)[0]
        assert workflow['trigger'] in section
        assert workflow['outcome'] in section
        assert f"../workflow-library/{workflow['key']}.md#workflow-steps-and-gates" in section
        for step in workflow['steps']:
            assert f"**{step['role']}:** {step['hands_over']}" in section


def test_homepage_workflow_coverage_tracks_canonical_counts_and_rejects_invalid_identity(tmp_path):
    target = tmp_path / '.ai/runtime/workflows.json'
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({'count': 2, 'workflows': [{'key': 'first'}, {'key': 'second'}]}))
    assert links.render_workflow_coverage(tmp_path) == '2 enterprise workflow chains'
    target.write_text(json.dumps({'count': 1, 'workflows': [{'key': 'first'}]}))
    assert links.render_workflow_coverage(tmp_path) == '1 enterprise workflow chain'
    target.write_text(json.dumps({'count': 0, 'workflows': []}))
    assert links.render_workflow_coverage(tmp_path) == '0 enterprise workflow chains'
    for invalid in ([], {'count': 2, 'workflows': [{'key': 'same'}, {'key': 'same'}]},
                    {'count': 1, 'workflows': []}, {'count': 1, 'workflows': [{'key': ''}]},
                    {'count': True, 'workflows': [{'key': 'first'}]}):
        target.write_text(json.dumps(invalid))
        with unittest.TestCase().assertRaises(ValueError):
            links.render_workflow_coverage(tmp_path)
    target.unlink()
    with unittest.TestCase().assertRaises(OSError):
        links.render_workflow_coverage(tmp_path)


def test_homepage_offers_contextual_catalogues_and_beginner_routes_without_link_pile():
    source = (ROOT / 'docs/index.md').read_text()
    assert source.count(links.HOME_NAV_TOKEN) == 1
    assert 'assets/images/hero-scene.jpg' in source
    assert 'Turn complexity into<br><span>justifiable progress.</span>' in source
    assert 'https://doi.org/10.13140/RG.2.2.29244.19843' in source
    assert 'Human Authority &amp; Workflows' not in source
    assert 'ai-home-learning-links' not in source
    cards = re.findall(r'<article class="ai-home-path-card">(.*?)</article>', source, re.S)
    assert len(cards) == 3
    for card, target in zip(cards, ('reference/roles/', 'reference/workflows/', 'using/layered-engagement/')):
        assert f'href="{target}"' in card
        assert 'aria-hidden="true"' in card
        assert '<h3>' in card and '<p>' in card
    assert 'Trace requirements from top to bottom:' in cards[2]
    assert 'business intent, design, implementation and evidence' in cards[2]
    assert len(re.findall(r'class="ai-matrix-cell(?: ai-matrix-highlight)?"', cards[2])) == 36
    assert 'href="using/demo-estate/"' in source
    assert 'href="using/experimental-hint/"' in source
    assert 'Experimental hint' in source
    assert 'Open source' in source
    assert 'href="about/license-attribution/"' in source
    assert 'href="reference/output-contracts/"' in source
    assert 'href="operations/human-authority/"' in source
    with unittest.TestCase().assertRaises(ValueError):
        links.expand_homepage(source.replace('href="https://github.com/__JAI_GITHUB_REPOSITORY__"', 'href="missing/"'), 'team/JAI')
    links.on_nav(SimpleNamespace(items=[page('Home', '')]), config=None, files=None)
    with patch.object(links, 'resolved_repository', return_value='team/JAI'):
        rendered = links.on_page_markdown(source, page=page('Home', ''), config=None, files=None)
    assert '{{ JAI_WORKFLOW_COVERAGE }}' not in rendered
    assert links.render_workflow_coverage(ROOT) in rendered
    assert 'href="https://github.com/team/JAI"' in rendered
