# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Create local fictional walkthrough exercises without executing provider commands.

Catalogs are validated in full before any workspace write. Explicit reset renames
an owned exercise into a sibling backup; it never deletes prior user work.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import tempfile

CATALOG = Path(__file__).with_name('scenarios.json')
MARKER = '.jai-scenario.json'


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _relative(value):
    return (_text(value) and '\\' not in value and ':' not in value
            and not PurePosixPath(value).is_absolute()
            and all(part not in ('', '.', '..') for part in value.split('/')))


def load_catalog(path=CATALOG, *, require_discovery=False):
    """Return validated entries from path; raise ValueError on invalid data.

    Args:
        path: Local JSON catalog path, read without modifying it.
        require_discovery: Require versioned discovery and the packaged workflow registry.
    Returns:
        A list of scenario dictionaries with unique identifiers and input paths.
    Raises:
        ValueError: The file cannot be read or its schema or paths are invalid.
    """
    try:
        if Path(path).is_symlink():
            raise ValueError('Catalog must not be a symlink')
        data = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError(f'Invalid scenario catalog: {exc}') from exc
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('Invalid scenario catalog schema_version')
    entries = data.get('entries')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Scenario catalog entries must be nonempty')
    ids = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid scenario entry')
        for key in ('id', 'title', 'guide', 'project_name'):
            if not _text(entry.get(key)):
                raise ValueError(f'Missing scenario {key}')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', entry['id']) or entry['id'] in ids:
            raise ValueError('Invalid or duplicate scenario id')
        ids.add(entry['id'])
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', entry['project_name']):
            raise ValueError('Invalid project_name')
        if not _relative(entry['guide']) or not entry['guide'].endswith('.md'):
            raise ValueError('Invalid guide path')
        paths = set()
        if not isinstance(entry.get('inputs'), list) or not entry['inputs']:
            raise ValueError('Scenario inputs must be nonempty')
        for item in entry['inputs']:
            if not isinstance(item, dict):
                raise ValueError('Invalid input')
            path = item.get('path')
            if not _relative(path) or not path.startswith('inputs/') or path in paths or not _text(item.get('content')):
                raise ValueError('Invalid or duplicate input path/content')
            if any(path.startswith(p + '/') or p.startswith(path + '/') for p in paths):
                raise ValueError('Conflicting input paths')
            paths.add(path)
        steps = entry.get('steps')
        if not isinstance(steps, list) or not steps:
            raise ValueError('Scenario steps must be nonempty')
        for step in steps:
            if not isinstance(step, dict) or any(not _text(step.get(k)) for k in ('title', 'why', 'claude', 'codex', 'inspect')):
                raise ValueError('Invalid scenario step')
        for key in ('description', 'missing_evidence_exercise'):
            if key in entry and not _text(entry[key]):
                raise ValueError(f'Invalid {key}')
    if require_discovery or 'discovery_version' in data or any('discovery' in e for e in entries):
        _validate_discovery(data, entries, require_discovery)
    return entries


def _validate_discovery(data, entries, require_registry):
    if type(data.get('discovery_version')) is not int or data['discovery_version'] != 1:
        raise ValueError('Invalid or missing discovery_version')
    registry_path = Path(__file__).resolve().parent.parent / 'workflows.json'
    workflow_keys = None
    if require_registry:
        try:
            if registry_path.is_symlink():
                raise ValueError('Symlink registry')
            registry = json.loads(registry_path.read_text(encoding='utf-8'))
            workflows = registry['workflows']
            workflow_keys = [w['key'] for w in workflows]
            if (not workflow_keys or any(not _text(k) for k in workflow_keys)
                    or len(workflow_keys) != len(set(workflow_keys))):
                raise ValueError('Invalid registry keys')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ValueError('Invalid packaged workflow registry') from exc
    ids = {e['id'] for e in entries}
    fields = {'goals', 'domains', 'phases', 'prerequisites', 'input_kinds',
              'output_kinds', 'applicability_limits', 'related_scenarios', 'workflow_keys'}
    phases = {'planning', 'assessment', 'design', 'delivery', 'review', 'operations',
              'recovery', 'publication', 'retirement'}
    for entry in entries:
        discovery = entry.get('discovery')
        if not isinstance(discovery, dict) or set(discovery) != fields:
            raise ValueError('Invalid discovery fields')
        for field in fields:
            values = discovery[field]
            if (not isinstance(values, list) or len(values) > 32
                    or any(not _text(v) or len(v) > 500 for v in values)
                    or len(values) != len(set(values))
                    or (not values and field not in ('related_scenarios', 'workflow_keys'))):
                raise ValueError(f'Invalid discovery {field}')
        if not set(discovery['phases']) <= phases:
            raise ValueError('Invalid discovery phases')
        if not set(discovery['related_scenarios']) <= ids - {entry['id']}:
            raise ValueError('Invalid discovery related_scenarios')
        if workflow_keys is not None and not set(discovery['workflow_keys']) <= set(workflow_keys):
            raise ValueError('Invalid discovery workflow registry reference')
        if entry.get('workflow') and discovery['workflow_keys'] != [entry['workflow']]:
            raise ValueError('Discovery workflow does not match scenario workflow')


def _select(entries, scenario_id):
    for entry in entries:
        if entry['id'] == scenario_id:
            return entry
    raise ValueError(f'Unknown scenario: {scenario_id}')


def describe_scenario(entries, scenario_id, step=None):
    """Return read-only guidance for scenario_id, optionally one 1-based step.

    Args:
        entries: Validated catalog entries.
        scenario_id: Exact scenario identifier.
        step: Optional positive, 1-based step number.
    Returns:
        English Markdown instructions, explicitly unexecuted and fictional.
    Raises:
        ValueError: The identifier or step number is invalid.
    """
    entry = _select(entries, scenario_id)
    if step is not None and (type(step) is not int or not 1 <= step <= len(entry['steps'])):
        raise ValueError('Invalid step number')
    lines = [f"# {entry['title']}", '', 'This is a fictional exercise. Execution: NOT_EXECUTED.',
             'No approval, review result or project evidence is created by setup.', '',
             f"Maintained guide (relative to documentation root): {entry['guide']}", '',
             entry.get('description', ''), '', '## Inputs', '']
    lines.extend(f"- `{item['path']}`" for item in entry['inputs'])
    for number, item in enumerate(entry['steps'], 1):
        if step is not None and number != step:
            continue
        lines.extend(['', f"## {number}. {item['title']}", '', item['why'], '',
                      'Claude:', '', '```text', item['claude'], '```', '',
                      'Codex:', '', '```text', item['codex'], '```', '',
                      f"Inspect before continuing: {item['inspect']}"])
    if entry.get('missing_evidence_exercise'):
        lines.extend(['', '## Missing evidence exercise', '', entry['missing_evidence_exercise']])
    lines.extend(['', 'Stop on missing authority or evidence; ask the named human owner.',
                  'Conversational agreement is not a signed L0 authority act.', ''])
    return '\n'.join(lines)


def _destination(destination):
    path = Path(destination).expanduser().absolute()
    if '..' in path.parts or path == Path(path.anchor) or any(
            part in ('.git', '.fabric', '.findings') for part in path.parts):
        raise ValueError('Unsafe destination')
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError('Destination has a symlink component')
    if not path.parent.is_dir():
        raise ValueError('Destination parent directory must exist')
    return path


def create_scenario(entries, scenario_id, destination):
    """Create a fresh exercise at destination without overwriting any existing path.

    Args:
        entries: Fully validated catalog entries.
        scenario_id: Exact scenario identifier.
        destination: New directory whose parent exists and has no symlink components.
    Returns:
        The created absolute Path.
    Raises:
        ValueError: Unknown identifier or unsafe/existing destination.
        OSError: A filesystem operation fails; a partial new exercise may remain.
    """
    entry = _select(entries, scenario_id)
    path = _destination(destination)
    if path.exists():
        raise ValueError('Destination already exists; use explicit reset-scenario')
    path.mkdir()
    for item in entry['inputs']:
        target = path / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item['content'], encoding='utf-8')
    (path / 'START.md').write_text(describe_scenario(entries, scenario_id), encoding='utf-8')
    (path / MARKER).write_text(json.dumps({'schema_version': 1, 'scenario_id': scenario_id,
                                         'kind': 'jai-fictional-scenario'}, indent=2) + '\n', encoding='utf-8')
    return path


def reset_scenario(entries, scenario_id, destination):
    """Preserve an owned exercise in a sibling backup and recreate its inputs.

    Args:
        entries: Fully validated catalog entries.
        scenario_id: Identifier matching the existing ownership marker.
        destination: Existing exercise directory with no symlink components.
    Returns:
        Path of the backup containing all previous work, including unknown files.
    Raises:
        ValueError: The destination or its non-symlink ownership marker is invalid.
        OSError: Backup or creation fails; the backup is never deleted.
    """
    _select(entries, scenario_id)
    path = _destination(destination)
    marker = path / MARKER
    try:
        if not path.is_dir() or marker.is_symlink():
            raise ValueError('Invalid ownership marker')
        data = json.loads(marker.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError('Invalid ownership marker') from exc
    if (not isinstance(data, dict) or type(data.get('schema_version')) is not int
            or data != {'schema_version': 1, 'scenario_id': scenario_id, 'kind': 'jai-fictional-scenario'}):
        raise ValueError('Invalid ownership marker')
    backup = Path(tempfile.mkdtemp(prefix=path.name + '.backup-', dir=path.parent))
    backup.rmdir()
    path.rename(backup)
    create_scenario(entries, scenario_id, path)
    return backup


def main(argv=None):
    """Run scenario subcommands using argv, returning zero on success or two on error.

    Args:
        argv: Optional command arguments; defaults to process arguments.
    Returns:
        Integer exit status. Only creation and explicit reset write project files.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    listing = commands.add_parser('scenarios')
    listing.add_argument('--json', action='store_true')
    describe = commands.add_parser('describe')
    describe.add_argument('id')
    describe.add_argument('--step', type=int)
    for command in ('scenario', 'reset-scenario'):
        child = commands.add_parser(command)
        child.add_argument('id')
        child.add_argument('--to', required=True)
    commands.add_parser('check-scenarios')
    args = parser.parse_args(argv)
    try:
        entries = load_catalog()
        if args.command == 'scenarios':
            if args.json:
                print(json.dumps({'schema_version': 1, 'entries': [
                    {key: item[key] for key in ('id', 'title', 'guide', 'project_name')} for item in entries]}, indent=2))
            else:
                for item in entries:
                    print(f"{item['id']}: {item['title']} ({item['guide']})")
        elif args.command == 'describe':
            print(describe_scenario(entries, args.id, args.step))
        elif args.command == 'scenario':
            print(create_scenario(entries, args.id, args.to))
        elif args.command == 'reset-scenario':
            print(f'Previous work preserved: {reset_scenario(entries, args.id, args.to)}')
        else:
            print(f'PASS {len(entries)} local fictional scenarios; provider execution NOT_EXECUTED')
        return 0
    except (ValueError, OSError) as exc:
        print(f'ERROR: {exc}')
        return 2
