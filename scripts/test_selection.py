# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Maintained Python test categories and conservative source-impact selection.

The catalog is an explicit reviewable classification, not an inference from test
names. Import analysis adds consumers to the explicit non-code impact rules;
unknown or unmapped changed resources select the complete Python suite.
"""
from __future__ import annotations

import ast
import fnmatch
import json
import os
from pathlib import Path
import subprocess

CATEGORIES = frozenset({'unit', 'integration', 'contract', 'e2e'})
TAGS = CATEGORIES | {'control', 'slow', 'security', 'performance'}


def load_catalog(root):
    """Return the validated catalog in checkout ``root``; raise ValueError on invalid tags or paths."""
    root = Path(root)
    data = json.loads((root / 'ci/test-catalog.json').read_text(encoding='utf-8'))
    if data.get('version') != 1 or not data.get('modules'):
        raise ValueError('Unsupported or empty test catalog')
    for name, entry in data['modules'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts or not name.endswith('.py'):
            raise ValueError(f'Invalid test catalog path: {name}')
        if entry.get('category') not in CATEGORIES or set(entry.get('tags', [])) - TAGS:
            raise ValueError(f'Invalid test catalog tags: {name}')
    for node, entry in data.get('node_tags', {}).items():
        if node.split('::')[0] not in data['modules'] or entry.get('category') not in CATEGORIES:
            raise ValueError(f'Invalid catalog node: {node}')
        if set(entry.get('tags', [])) - TAGS:
            raise ValueError(f'Invalid catalog node tags: {node}')
    for rule in data.get('impact_rules', []):
        if not rule.get('paths') or not rule.get('tests') or set(rule['tests']) - set(data['modules']):
            raise ValueError('Invalid impact rule: patterns and catalogued consumers are required')
    for node in data.get('control', {}):
        if 'control' not in data.get('node_tags', {}).get(node, {}).get('tags', []):
            raise ValueError(f'Control node lacks control tag: {node}')
    return data


def tags_for_node(catalog, nodeid):
    """Return inherited catalog tags for a root-relative pytest node ID, or raise ValueError if unclassified."""
    module = nodeid.split('::')[0]
    entry = catalog['modules'].get(module)
    if entry is None:
        raise ValueError(f'Unclassified maintained test: {module}; add it to ci/test-catalog.json')
    tags = {entry['category'], *entry.get('tags', [])}
    for prefix, override in catalog.get('node_tags', {}).items():
        if nodeid == prefix or nodeid.startswith(prefix + '[') or nodeid.startswith(prefix + '::'):
            tags.difference_update(CATEGORIES)
            tags.add(override['category'])
            tags.update(override.get('tags', []))
    return tags


def changed_paths(root, base=None):
    """Return changed tracked and untracked root-relative paths; invalid Git baselines raise ValueError.

    With ``base``, include that revision through the current working tree. Without
    it, include staged, unstaged and untracked files, preserving rename deletions.
    """
    root = Path(root)
    if base is not None and base.startswith('-'):
        raise ValueError('Invalid Git baseline: revisions cannot begin with an option prefix')
    command = ['git', 'diff', '--name-only', '--no-renames', '-z']
    command += [base] if base is not None else ['HEAD']
    result = subprocess.run(command + ['--'], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError('Cannot establish changed inputs from Git baseline; supply --changed or a valid --base')
    untracked = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=root, capture_output=True)
    if untracked.returncode:
        raise ValueError('Cannot establish untracked changed inputs')
    return sorted(set((result.stdout + untracked.stdout).decode().strip('\0').split('\0')) - {''})


def _source_graph(root):
    files = set()
    for directory in ('scripts', 'tools', '.ai/runtime/tools', 'tests'):
        files.update((root / directory).rglob('*.py'))
    # All maintained app consumers participate, including qualification and
    # example/corpus writers. Never traverse dependency trees or private inputs.
    excluded = {'node_modules', 'build', 'dist', 'vendor', 'vendors', 'obsolete',
                'INBOX', '.git', '__pycache__', '.venv', 'venv'}
    for directory, children, names in os.walk(root / 'apps'):
        children[:] = [name for name in children if name not in excluded]
        files.update(Path(directory) / name for name in names if name.endswith('.py'))
    files = {p for p in files if '__pycache__' not in p.parts}
    stems = {}
    for p in files:
        stems.setdefault(p.stem, set()).add(p.relative_to(root).as_posix())
    dependencies = {}
    for p in files:
        relative = p.relative_to(root).as_posix()
        try:
            tree = ast.parse(p.read_text(encoding='utf-8'))
        except (SyntaxError, UnicodeError, OSError):
            continue
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name.split('.')[-1] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add((node.module or '').split('.')[-1])
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith('.py'):
                # Existing tests also load tools through importlib file locations.
                names.add(Path(node.value).stem)
        dependencies[relative] = set().union(*(stems.get(name, set()) for name in names)) if names else set()
    return dependencies


def select_impacted(root, catalog, changed):
    """Return (test module paths, reason) for changed root-relative inputs.

    Explicit resource rules and the transitive local Python import graph are
    additive. Any unknown input broadens to all maintained Python modules. Empty
    changes select no tests; invalid/outside-root paths raise ValueError.
    """
    root = Path(root).resolve()
    all_tests = set(catalog['modules'])
    if not changed:
        return [], 'No changed inputs'
    normalized = []
    for raw in changed:
        path = Path(raw)
        path = path if path.is_absolute() else root / path
        try:
            normalized.append(path.resolve().relative_to(root).as_posix())
        except ValueError as exc:
            raise ValueError(f'Changed input escapes checkout: {raw}') from exc
    graph = _source_graph(root)
    selected = set()
    for path in normalized:
        mapped = False
        if path in all_tests:
            selected.add(path)
            mapped = True
        for rule in catalog.get('impact_rules', []):
            if any(fnmatch.fnmatchcase(path, pattern) for pattern in rule['paths']):
                selected.update(rule['tests'])
                mapped = True
        closure = {path}
        while True:
            expanded = closure | {source for source, deps in graph.items() if deps & closure}
            if expanded == closure:
                break
            closure = expanded
        consumers = all_tests & closure
        if consumers:
            selected.update(consumers)
            mapped = True
        if not mapped:
            return sorted(all_tests), f'Unknown impact: {path}; complete Python coverage required'
    return sorted(selected), 'Explicit resource rules plus transitive local Python consumers'


def maintained_modules(root):
    """Return all maintained Python test paths without importing test code or private inputs."""
    root = Path(root)
    return sorted({p.relative_to(root).as_posix() for pattern in ('tests/test_*.py', 'apps/**/test_*.py')
                   for p in root.glob(pattern) if '__pycache__' not in p.parts})
