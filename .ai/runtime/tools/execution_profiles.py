#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Resolve operator execution preferences independently of governance profiles.

The result is a JSON snapshot to capture once at entry to a run. Reading a
snapshot never reloads project or user files. Preferences do not grant authority,
change budgets, restrict the professional catalogue, or prove served-model facts.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path

import model_router

BASE = Path(__file__).resolve().parents[1] / 'models/execution-profiles.json'
RESPONSIBILITIES = ('setter', 'author', 'reviewer')
CONTEXT_POLICIES = {'isolated-handoffs', 'task-isolated', 'manual'}
EFFORTS = {
    'codex': {'none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra'},
    'claude': {'low', 'medium', 'high', 'xhigh', 'max'},
}
_NAME = re.compile(r'^[a-z][a-z0-9-]{0,63}$')
_CONFIG_FIELDS = {'schema_version', 'execution_profile', 'context_policy', 'profiles', 'overrides', 'analytics'}
_PROFILE_FIELDS = {'extends', 'description', 'context_policy', 'responsibilities', 'providers'}
_ROLE_FIELDS = {'workload_class', 'reasoning_effort', 'model_selector'}


def _object(value, allowed, label):
    if not isinstance(value, dict) or set(value) - allowed:
        raise ValueError(f'{label}: expected object with fields {sorted(allowed)}')


def _name(value, label):
    if not isinstance(value, str) or not _NAME.fullmatch(value):
        raise ValueError(f'{label}: expected a lowercase profile identifier')


def _read(path, optional=False):
    try:
        value = json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        if optional:
            return None
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f'Invalid execution configuration: {exc}') from exc
    return value


def _validate_roles(roles, label, provider=None):
    _object(roles, set(RESPONSIBILITIES), label)
    for role, values in roles.items():
        _object(values, _ROLE_FIELDS, f'{label}/{role}')
        workload = values.get('workload_class')
        if 'workload_class' in values and (not isinstance(workload, str)
                or workload not in {'light', 'standard', 'heavy', 'research'}):
            raise ValueError(f'{label}/{role}: unknown workload_class {workload!r}')
        effort = values.get('reasoning_effort')
        supported = EFFORTS[provider] if provider else EFFORTS['codex'] & EFFORTS['claude']
        if 'reasoning_effort' in values and (not isinstance(effort, str) or effort not in supported):
            raise ValueError(f'{label}/{role}: unsupported reasoning_effort {effort!r}')
        selector = values.get('model_selector')
        if 'model_selector' in values and (not isinstance(selector, str) or not selector.strip()):
            raise ValueError(f'{label}/{role}: nonempty model_selector required')


def _validate_profile(value, label):
    _object(value, _PROFILE_FIELDS, label)
    if 'extends' in value:
        _name(value['extends'], f'{label}/extends')
    if 'description' in value and (not isinstance(value['description'], str) or not value['description'].strip()):
        raise ValueError(f'{label}: description must be nonempty text')
    if 'context_policy' in value and (not isinstance(value['context_policy'], str)
            or value['context_policy'] not in CONTEXT_POLICIES):
        raise ValueError(f'{label}: unsupported context_policy')
    if 'responsibilities' in value:
        _validate_roles(value['responsibilities'], f'{label}/responsibilities')
    if 'providers' in value:
        _object(value['providers'], set(EFFORTS), f'{label}/providers')
        for provider, roles in value['providers'].items():
            _validate_roles(roles, f'{label}/providers/{provider}', provider)


def _validate_config(value):
    _object(value, _CONFIG_FIELDS, 'execution configuration')
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('execution configuration: schema_version must be 1')
    if 'execution_profile' in value:
        _name(value['execution_profile'], 'execution_profile')
    if 'context_policy' in value and (not isinstance(value['context_policy'], str)
            or value['context_policy'] not in CONTEXT_POLICIES):
        raise ValueError('execution configuration: unsupported context_policy')
    if 'profiles' in value:
        if not isinstance(value['profiles'], dict):
            raise ValueError('profiles must be an object')
        for name, spec in value['profiles'].items():
            _name(name, 'profile name')
            _validate_profile(spec, f'profile {name}')
            if name == 'workload' and set(spec) & {'extends', 'responsibilities', 'providers'}:
                raise ValueError('workload is a routing mode, not a fixed responsibility profile')
            if spec.get('extends') == 'workload':
                raise ValueError('A named profile cannot inherit the workload routing mode')
    if 'overrides' in value:
        _validate_profile(value['overrides'], 'overrides')
        if 'extends' in value['overrides']:
            raise ValueError('overrides cannot extend a profile; select execution_profile instead')
    if 'analytics' in value:
        _validate_analytics(value['analytics'])


def _validate_analytics(value):
    _object(value, {'task_class', 'review_scope'}, 'analytics')
    for key, label in value.items():
        _name(label, f'analytics/{key}')


def _user_path():
    root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
    return root / 'ai-it-house/profiles.json'


def _configuration(project, user_config):
    root = Path(project).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('project must be an existing directory')
    builtins = _read(BASE)
    _validate_config(builtins)
    merged = copy.deepcopy(builtins)
    sources = ['bundled']
    configured = False
    paths = [('user', Path(user_config).expanduser() if user_config is not None else _user_path()),
             ('project', root / '.jai/config.json'), ('local', root / '.jai/config.local.json')]
    for label, path in paths:
        if label in {'project', 'local'}:
            _project_path(root, path)
        value = _read(path, optional=not (label == 'user' and user_config is not None))
        if value is None:
            continue
        _validate_config(value)
        merged = model_router.merge(merged, value)
        sources.append(label)
        configured = configured or bool(set(value) & {'execution_profile', 'context_policy', 'overrides'})
    active = merged.get('execution_profile', 'standard')
    if active in merged['profiles']:
        baseline = _expanded(builtins['profiles'], active) if active in builtins['profiles'] else None
        configured = configured or _expanded(merged['profiles'], active) != baseline
    return merged, sources, configured


def _expanded(profiles, name, visiting=()):
    if name not in profiles:
        raise ValueError(f'Unknown execution profile {name!r}')
    if name in visiting:
        raise ValueError('Execution profile inheritance cycle: ' + ' -> '.join((*visiting, name)))
    spec = profiles[name]
    parent = _expanded(profiles, spec['extends'], (*visiting, name)) if 'extends' in spec else {}
    return model_router.merge(parent, {key: value for key, value in spec.items() if key != 'extends'})


def _context_policy(config, name):
    spec = model_router.merge(_expanded(config['profiles'], name), config.get('overrides', {}))
    return config.get('context_policy', spec.get('context_policy', 'isolated-handoffs'))


def routing_mode(snapshot):
    """Read explicit routing semantics without changing immutable legacy snapshots.

    Args:
        snapshot: Captured execution preference with an optional routing_mode field.
    Returns:
        workload or profile. Older snapshots retain their configured-flag semantics.
    Raises:
        ValueError: An explicit routing mode is unsupported or malformed.
    """
    if 'routing_mode' not in snapshot:
        return 'profile' if snapshot.get('configured') else 'workload'
    mode = snapshot['routing_mode']
    if not isinstance(mode, str) or mode not in {'workload', 'profile'}:
        raise ValueError('Unsupported execution routing_mode')
    return mode


def _selection_status(config, configured):
    selected = config.get('execution_profile', 'standard')
    if selected not in config['profiles']:
        raise ValueError(f'Unknown execution profile {selected!r}')
    mode = 'workload' if selected == 'workload' or not configured else 'profile'
    return {'active': 'workload' if mode == 'workload' else selected,
            'selected_profile': selected, 'routing_mode': mode, 'configured': configured,
            'context_policy': _context_policy(config, selected)}


def _project_path(root, path):
    # Resolve existing ancestors as well as dangling symlinks before reads/writes;
    # project preference commands must not overwrite an external target.
    if path.is_symlink() or (root / '.jai').is_symlink():
        raise ValueError('Project execution configuration must not use symlinks')
    if not path.resolve().is_relative_to(root):
        raise ValueError('Project execution configuration escapes project root')


def available(project, user_config=None):
    """List expanded profiles and the active project preference without writing.

    Args:
        project: Existing project directory, independent of the process cwd.
        user_config: Optional user configuration path; absence uses XDG defaults.
    Returns:
        JSON object with profile/mode entries, actual routing, selected name,
        context policy and configuration source labels.
    Raises:
        ValueError, OSError: Invalid configuration, cyclic inheritance or unsafe path.
    """
    config, sources, configured = _configuration(project, user_config)
    profiles = config['profiles']
    entries = []
    for name in sorted(profiles):
        expanded = _expanded(profiles, name)
        entries.append({'name': name, 'description': expanded.get('description', ''),
                        'routing_mode': 'workload' if name == 'workload' else 'profile'})
    return {'schema_version': 1, **_selection_status(config, configured),
            'sources': sources, 'profiles': entries}


def resolve(project, registry, provider, profile=None, user_config=None, context_policy=None):
    """Capture effective operator model/context preferences for one new run.

    Args:
        project: Existing project root whose `.jai` configuration is read once.
        registry: Explicit validated model registry, never loaded from ambient state.
        provider: Active native provider, `codex` or `claude`.
        profile: Optional explicit per-run profile or workload mode; takes precedence
            without writing. Workload selection preserves the current context policy.
        user_config: Optional user preferences file instead of the XDG default.
        context_policy: Validated explicit context from the current session receipt;
            overrides project/default context for this new snapshot only.
    Returns:
        Independent JSON snapshot containing resolved per-responsibility models,
        context behavior and provenance labels. `configured` distinguishes opted-in
        preferences from legacy workload routing. Operator analytics cohort labels
        default to `unspecified`; no served-model fact or task class is inferred.
    Raises:
        ValueError, OSError: Invalid registry/configuration or unsupported provider.
    """
    if context_policy is not None and (not isinstance(context_policy, str)
            or context_policy not in CONTEXT_POLICIES):
        raise ValueError('Unsupported explicit execution context policy')
    if not isinstance(provider, str) or provider not in EFFORTS:
        raise ValueError(f'Unsupported execution provider {provider!r}')
    problems = model_router.validate_registry(registry)
    if problems:
        raise ValueError('; '.join(problems))
    config, sources, configured = _configuration(project, user_config)
    profiles = config['profiles']
    # Validate the whole inheritance graph at selection time, not on every turn.
    for name in profiles:
        _expanded(profiles, name)
    previous_name = config.get('execution_profile', 'standard')
    name = profile if profile is not None else previous_name
    _name(name, 'execution_profile')
    spec = model_router.merge(_expanded(profiles, name), config.get('overrides', {}))
    roles = model_router.merge(spec.get('responsibilities', {}), spec.get('providers', {}).get(provider, {}))
    configured = configured or profile is not None
    mode = 'workload' if name == 'workload' or not configured else 'profile'
    resolved = {}
    for role in RESPONSIBILITIES if mode == 'profile' else ():
        settings = roles.get(role, {})
        workload = settings.get('workload_class', 'standard')
        _, selected = model_router.resolve_snapshot(registry, provider, workload)
        for field in ('model_selector', 'reasoning_effort'):
            if field in settings:
                selected[field] = settings[field]
        if 'model_identity' in selected:
            selected['model_identity'] = selected['model_selector']
        if selected.get('reasoning_effort') is not None and selected['reasoning_effort'] not in EFFORTS[provider]:
            raise ValueError(f'{provider}/{role}: unsupported reasoning_effort')
        resolved[role] = {'workload_class': workload, 'model': selected}
    context = context_policy if context_policy is not None else _context_policy(
        config, previous_name if profile == 'workload' else name)
    if profile is not None or context_policy is not None:
        sources.append('invocation')
    return {'schema_version': 1, 'execution_profile': 'workload' if mode == 'workload' else name,
            'routing_mode': mode, 'context_policy': context,
            'provider': provider, 'responsibilities': resolved,
            'configured': configured, 'sources': sources,
            'analytics': {'task_class': 'unspecified', 'review_scope': 'unspecified',
                          **config.get('analytics', {})},
            'context': {
                'workers': 'fresh-bounded', 'reviewer': 'independent',
                'task_entry': 'fresh-worker' if context != 'manual' else 'provider-managed',
                'main_compaction': 'manual' if context == 'manual' else 'provider-managed',
                'handoff': 'explicit-versioned-inputs',
            }}


def mapping(snapshot, responsibility, workload, registry=None):
    """Read a captured responsibility preference without consulting mutable files.

    Args:
        snapshot: Result of `resolve`, captured with the run's inputs.
        responsibility: Native responsibility; aliases retain full professional scope.
        workload: Original locally selected workload class for legacy/unmapped work.
        registry: Already validated captured registry for unchanged workload routing.
    Returns:
        `(workload_class, mapping)` with an independent model mapping copy. A
        preference applies only when the local entity selects its workload class;
        alternate classes retain the captured registry mapping and full autonomy.
    Raises:
        ValueError: A fallback mapping needs a registry or snapshot is malformed.
    """
    aliases = {'integration_reviewer': 'reviewer', 'receiver': 'reviewer',
               'integrator': 'author', 'measurement': 'author'}
    role = aliases.get(responsibility, responsibility)
    if (routing_mode(snapshot) == 'profile' and role in RESPONSIBILITIES
            and workload == snapshot['responsibilities'][role]['workload_class']):
        spec = snapshot['responsibilities'][role]
        return spec['workload_class'], copy.deepcopy(spec['model'])
    if registry is None:
        raise ValueError('Captured registry required for unchanged workload routing')
    try:
        result = registry['providers'][snapshot['provider']]['classes'][workload]
    except (KeyError, TypeError) as error:
        raise ValueError('Captured workload mapping unavailable') from error
    return workload, copy.deepcopy(result)


def routing_observation(snapshot, responsibility, workload, model):
    """Compare a captured work selection with an active profile preference.

    Args:
        snapshot: Pinned execution preference; legacy routing semantics are retained.
        responsibility: Actual local work responsibility, including review aliases.
        workload: Exact captured selected workload class, not an estimated difficulty.
        model: Validated selected model mapping, including native execution provider
            when available. These are selected/requested settings, not served facts.
    Returns:
        Safe routing comparison with preference/selected tuples and differs flag.
        Workload routing has no fixed preference, so differs is None. A different
        workload counts as a deviation even if it maps to the same model/effort.
        This does not verify domain-specific model-diversity requirements.
    Raises:
        ValueError: Routing mode, selected workload or model identity is malformed.
    """
    mode = routing_mode(snapshot)
    if not isinstance(workload, str) or not workload or not isinstance(model, dict):
        raise ValueError('An exact captured workload and selected model mapping are required')
    if not isinstance(model.get('model_selector'), str) or not model['model_selector']:
        raise ValueError('Selected model identity is required')
    aliases = {'integration_reviewer': 'reviewer', 'receiver': 'reviewer',
               'integrator': 'author', 'measurement': 'author'}
    role = aliases.get(responsibility, responsibility)
    preferred = snapshot.get('responsibilities', {}).get(role) if mode == 'profile' else None
    preference = ({'provider': snapshot['provider'], 'workload_class': preferred['workload_class'],
                   'model_selector': preferred['model']['model_selector'],
                   'reasoning_effort': preferred['model'].get('reasoning_effort')} if preferred else None)
    selected = {'provider': model.get('execution', {}).get('provider', snapshot['provider']),
                'workload_class': workload, 'model_selector': model['model_selector'],
                'reasoning_effort': model.get('reasoning_effort')}
    return {'routing_mode': mode, 'responsibility': responsibility, 'preference': preference,
            'selected': selected, 'differs': selected != preference if preference is not None else None,
            'served_model': None}


def validate_snapshot(snapshot, registry):
    """Check a captured execution snapshot without loading mutable preferences.

    Args:
        snapshot: Captured execution profile value from a model registry snapshot.
        registry: Its enclosing registry; only declared workloads are inspected.
    Returns:
        A list of human-readable validation problems, empty for a valid snapshot.
    Raises:
        No expected validation exception escapes; invalid values become problems.
    """
    try:
        fields = {'schema_version', 'execution_profile', 'context_policy', 'provider',
                  'responsibilities', 'configured', 'sources', 'context', 'analytics'}
        _object(snapshot, fields | {'routing_mode'}, 'execution snapshot')
        if not fields <= set(snapshot):
            raise ValueError('execution snapshot: missing fields')
        if type(snapshot['schema_version']) is not int or snapshot['schema_version'] != 1:
            raise ValueError('execution snapshot: schema_version must be 1')
        _name(snapshot['execution_profile'], 'execution snapshot profile')
        provider = snapshot['provider']
        if provider not in EFFORTS or provider not in registry.get('providers', {}):
            raise ValueError('execution snapshot: unsupported provider')
        if snapshot['context_policy'] not in CONTEXT_POLICIES:
            raise ValueError('execution snapshot: unsupported context policy')
        if type(snapshot['configured']) is not bool:
            raise ValueError('execution snapshot: configured must be boolean')
        _validate_analytics(snapshot['analytics'])
        if set(snapshot['analytics']) != {'task_class', 'review_scope'}:
            raise ValueError('execution snapshot: complete analytics cohort labels required')
        if (not isinstance(snapshot['sources'], list) or not snapshot['sources']
                or any(source not in {'bundled', 'user', 'project', 'local', 'invocation'}
                       for source in snapshot['sources'])):
            raise ValueError('execution snapshot: invalid source labels')
        mode = routing_mode(snapshot)
        if 'routing_mode' in snapshot and mode == 'profile' and (not snapshot['configured']
                or snapshot['execution_profile'] == 'workload'):
            raise ValueError('execution snapshot: named profile routing requires an explicit profile preference')
        if 'routing_mode' in snapshot and mode == 'workload' and snapshot['execution_profile'] != 'workload':
            raise ValueError('execution snapshot: workload mode requires the workload selection identity')
        expected_roles = set() if 'routing_mode' in snapshot and mode == 'workload' else set(RESPONSIBILITIES)
        if not isinstance(snapshot['responsibilities'], dict) or set(snapshot['responsibilities']) != expected_roles:
            raise ValueError('execution snapshot: exact responsibility preferences required')
        for role, spec in snapshot['responsibilities'].items():
            _object(spec, {'workload_class', 'model'}, f'execution snapshot/{role}')
            if set(spec) != {'workload_class', 'model'}:
                raise ValueError('execution snapshot: incomplete responsibility preference')
            workload = spec['workload_class']
            if workload not in registry.get('workload_classes', {}):
                raise ValueError('execution snapshot: unknown workload class')
            mapping = spec['model']
            _object(mapping, {'model_selector', 'reasoning_effort', 'fallbacks', 'model_kind', 'model_provider', 'model_identity'}, f'execution snapshot/{role}/model')
            _validate_roles({role: {key: value for key, value in mapping.items() if key in _ROLE_FIELDS}},
                            'execution snapshot', provider)
            metadata_problems = model_router._mapping_problems(provider, workload, mapping)
            if metadata_problems:
                raise ValueError('; '.join(metadata_problems))
            if 'model_selector' not in mapping:
                raise ValueError('execution snapshot: model selector required')
            fallbacks = mapping.get('fallbacks', [])
            if not isinstance(fallbacks, list):
                raise ValueError('execution snapshot: fallbacks must be an array')
            for fallback in fallbacks:
                _object(fallback, {'model_selector', 'reasoning_effort'}, 'execution snapshot fallback')
                if 'model_selector' not in fallback:
                    raise ValueError('execution snapshot: fallback model selector required')
                _validate_roles({role: fallback}, 'execution snapshot fallback', provider)
        expected = {
            'workers': 'fresh-bounded', 'reviewer': 'independent',
            'task_entry': 'fresh-worker' if snapshot['context_policy'] != 'manual' else 'provider-managed',
            'main_compaction': 'manual' if snapshot['context_policy'] == 'manual' else 'provider-managed',
            'handoff': 'explicit-versioned-inputs',
        }
        if snapshot['context'] != expected:
            raise ValueError('execution snapshot: context isolation invariant changed')
        return []
    except (ValueError, TypeError, KeyError) as exc:
        return [str(exc)]


def select(project, profile, *, local=False, session=False, user_config=None, context_policy=None):
    """Select a known profile atomically for future runs or return a session choice.

    Args:
        project: Existing project root; writes remain inside its `.jai` directory.
        profile: Existing built-in/custom profile identifier, or workload routing mode.
        local: Write `config.local.json` instead of shared `config.json`.
        session: Return the explicit per-run selection without changing any file.
        user_config: Optional user preferences path for catalogue resolution.
        context_policy: Optional previous session receipt context; valid only with
            session=True and never written into project configuration.
    Returns:
        JSON selection receipt. Session selections must be passed explicitly to
        the next bootstrap; they are not an ambient override of active runs.
    Raises:
        ValueError, OSError: Unknown/invalid profile, unsafe target, or failed write.
    """
    if context_policy is not None:
        if not isinstance(context_policy, str) or context_policy not in CONTEXT_POLICIES:
            raise ValueError('Unsupported explicit execution context policy')
        if not session:
            raise ValueError('Context transport requires a session selection')
    info = available(project, user_config)
    _name(profile, 'execution_profile')
    if profile not in {item['name'] for item in info['profiles']}:
        raise ValueError(f'Unknown execution profile {profile!r}')
    merged, _, _ = _configuration(project, user_config)
    current_context = info['context_policy']
    receipt = {'execution_profile': profile, 'scope': 'session' if session else ('local' if local else 'project'),
               'routing_mode': 'workload' if profile == 'workload' else 'profile',
               'applies_to': 'new-runs', 'active_runs_changed': False}
    if session:
        receipt.update(effective_profile=profile, effective_routing_mode=receipt['routing_mode'],
                       shadowed=False, context_policy=(context_policy if context_policy is not None else
                            current_context if profile == 'workload' else _context_policy(merged, profile)))
        return receipt
    root = Path(project).resolve(strict=True)
    target = root / '.jai' / ('config.local.json' if local else 'config.json')
    _project_path(root, target)
    config = _read(target, optional=True) or {'schema_version': 1}
    _validate_config(config)
    config['execution_profile'] = profile
    if profile == 'workload' and _context_policy(merged, profile) != current_context:
        config['context_policy'] = current_context
    target.parent.mkdir(exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent,
                                         prefix='.profile-', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(config, stream, indent=2, ensure_ascii=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        _project_path(root, target)
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    effective = available(project, user_config)
    receipt['effective_profile'] = effective['active']
    receipt['effective_routing_mode'] = effective['routing_mode']
    receipt['context_policy'] = effective['context_policy']
    receipt['shadowed'] = receipt['effective_profile'] != profile
    return receipt


def main(argv=None):
    """Run the native-command backing utility; it does not launch a provider.

    Args:
        argv: Optional argument list; None reads command-line arguments.
    Returns:
        Zero on successful JSON output, two for invalid input or filesystem errors.
    Raises:
        SystemExit: Argparse handles syntax errors and help requests.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='.')
    parser.add_argument('--provider', choices=sorted(EFFORTS), default='codex')
    parser.add_argument('--user-config')
    parser.add_argument('--model-config')
    commands = parser.add_subparsers(dest='command')
    commands.add_parser('list')
    show = commands.add_parser('show')
    show.add_argument('profile')
    use = commands.add_parser('use')
    use.add_argument('profile')
    use.add_argument('--local', action='store_true')
    use.add_argument('--session', action='store_true')
    use.add_argument('--context-policy', choices=sorted(CONTEXT_POLICIES))
    effective = commands.add_parser('effective')
    effective.add_argument('--session-profile')
    effective.add_argument('--context-policy', choices=sorted(CONTEXT_POLICIES))
    args = parser.parse_args(argv)
    try:
        if args.command in {None, 'list'}:
            result = available(args.project, args.user_config)
        elif args.command == 'use':
            result = select(args.project, args.profile, local=args.local, session=args.session,
                            user_config=args.user_config, context_policy=args.context_policy)
        else:
            registry, _ = model_router.effective_registry(args.model_config)
            result = resolve(args.project, registry, args.provider,
                             profile=args.profile if args.command == 'show' else args.session_profile,
                             user_config=args.user_config,
                             context_policy=None if args.command == 'show' else args.context_policy)
            if routing_mode(result) == 'workload':
                result['workload_mappings'] = copy.deepcopy(registry['providers'][args.provider]['classes'])
    except (ValueError, OSError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
