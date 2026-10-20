#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Explicitly opt-in provider evaluation; no mandatory qualification imports this tool.

Only bundled public-synthetic references may leave the local machine. Reports
contain metadata and lengths, never captured prompts, provider prose or stderr.
Offline report inspection validates integrity but cannot confer professional approval.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

LEVELS = ('simple', 'medium', 'complex')


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def _runtime(root):
    root = Path(root).resolve()
    return root / '.ai/runtime' if (root / '.ai/runtime').is_dir() else root


def _identifier(value):
    return value if (isinstance(value, str) and not value.startswith(('/', '.', '~'))
                     and '..' not in value and re.fullmatch(r'[A-Za-z0-9_.:/@+-]{1,160}', value)) else None


def preflight(provider, executable=None):
    """Inspect CLI availability without executing it, authenticating or reading credentials.

    Args:
        provider: Literal codex or claude.
        executable: Optional explicitly selected executable; defaults to provider.
    Returns:
        Sanitized availability record; version/authentication remain unobserved.
    Raises:
        ValueError: For an unsupported provider.
    """
    if provider not in ('codex', 'claude'):
        raise ValueError('unsupported provider')
    found = shutil.which(executable or provider)
    return {'provider': provider, 'state': 'AVAILABLE' if found else 'UNAVAILABLE',
            'cli_version': None, 'authentication': 'not-inspected',
            'live_execution': False, 'professional_qualification': False}


def prepare_plan(root, provider, family, cases=3, model=None):
    """Validate public bundled inputs and prepare a bounded plan without inference.

    Args:
        root: Source or installed runtime root.
        provider: codex or claude.
        family: One supported document family.
        cases: Number of bundled complexity levels, integer 1 through 3.
        model: Required explicit provider selector for execution, optional for planning.
    Returns:
        Integrity-hashed public-synthetic plan with no private input paths.
    Raises:
        ValueError, OSError: For invalid arguments or invalid bundled references.
    """
    if provider not in ('codex', 'claude'):
        raise ValueError('unsupported provider')
    if type(cases) is not int or not 1 <= cases <= 3:
        raise ValueError('cases must be an integer from 1 through 3')
    if model is not None and _identifier(model) != model:
        raise ValueError('invalid model selector')
    from expert_references import ExpertReferences
    references = ExpertReferences(root)
    family = references.canonical_family(family)
    runtime = _runtime(root)
    selected = []
    from content_spec import ContentSpec
    specifications = ContentSpec(root)
    for level in LEVELS[:cases]:
        path = runtime / 'content/expert_references' / family / (level + '.md')
        result = references.validate(path, kind=family, complexity=level, bundled=True)
        if (result.get('structural_coverage') != 'PASS'
                or result.get('content_presence') != 'PASS'):
            raise ValueError('bundled reference failed validation')
        # Export permission is independent of the reference resolver: overrides are
        # deliberately excluded from this capability until a separate consent design.
        text = path.read_text(encoding='utf-8')
        import yaml
        metadata = yaml.safe_load(text.split('---', 2)[1])
        if metadata.get('classification') != 'public-synthetic' or not metadata.get('fictional_context'):
            raise ValueError('provider export requires public-synthetic fictional input')
        selected.append({'complexity': level, 'reference_hash': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'compiled_spec_hash': specifications.compile(references.bindings[family]['spec_ref'], {})['compiled_spec_hash']})
    plan = {'schema_version': '1.0.0', 'provider': provider, 'family': family,
            'model_selector': model, 'reasoning_effort': None, 'cases': selected, 'invocations': len(selected),
            'classification': 'public-synthetic', 'context_fingerprint': _digest({'family': family, 'cases': selected}),
            'live_execution': False,
            'automatic_retry': False, 'fallback_provider': False,
            'cost_estimate': None, 'cost_limit': 'invocation and timeout limits only',
            'professional_qualification': False}
    plan['plan_hash'] = _digest(plan)
    return plan


def _terminate(process):
    if process.poll() is None:
        if os.name == 'posix':
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    process.communicate()


def _capture(command, timeout, cwd):
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, cwd=cwd,
                               start_new_session=os.name == 'posix')
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return {'state': 'COMPLETED' if process.returncode == 0 else 'FAILED',
                'exit_code': process.returncode, 'stdout': stdout, 'stderr': stderr}
    except subprocess.TimeoutExpired:
        _terminate(process)
        return {'state': 'TIMEOUT', 'exit_code': None, 'stdout': '', 'stderr': ''}
    except KeyboardInterrupt:
        _terminate(process)
        return {'state': 'CANCELLED', 'exit_code': None, 'stdout': '', 'stderr': ''}


def _observed(raw):
    models, usage, text = [], None, ''
    try:
        values = [json.loads(raw)]
    except (ValueError, TypeError):
        try:
            values = [json.loads(line) for line in raw.splitlines() if line.strip()]
        except ValueError:
            return {'valid': False, 'model': None, 'usage': None, 'output_characters': 0}
    if not values or not all(isinstance(value, dict) for value in values):
        return {'valid': False, 'model': None, 'usage': None, 'output_characters': 0}
    for value in values:
        if _identifier(value.get('model')):
            models.append(value['model'])
        payload = value.get('result', value.get('output', ''))
        item = value.get('item', {})
        if isinstance(item, dict) and item.get('type') == 'agent_message':
            payload = item.get('text', '')
        if isinstance(payload, str):
            text += payload
        candidate = value.get('usage')
        if isinstance(candidate, dict):
            # Numeric usage is useful; arbitrary provider keys/string values can leak.
            usage = {key: number for key, number in candidate.items()
                     if key in ('input_tokens', 'output_tokens', 'total_tokens')
                     and type(number) is int and number >= 0}
    return {'valid': bool(text), 'model': models[-1] if models else None,
            'usage': usage, 'output_characters': len(text)}


def run_plan(root, plan, consent_live=False, max_invocations=0, timeout=60, executable=None):
    """Execute public synthetic evaluation only after explicit bounded operator consent.

    Args:
        root: Source or installed runtime root containing unchanged bundled references.
        plan: Unmodified prepare_plan result with an explicit model selector.
        consent_live: Must be exactly True; consent is never inferred.
        max_invocations: Positive integer cap covering every selected case.
        timeout: Per-process seconds, positive and at most 3600.
        executable: Optional CLI path for an explicitly selected installation or fake test.
    Returns:
        Integrity-hashed sanitized execution report. No raw provider output is retained.
        Missing CLI is UNAVAILABLE and never PASS. Versions/models not observed are null.
    Raises:
        ValueError: For absent consent, invalid limits or changed inputs/plan.
        OSError: If the executable cannot start.
    """
    if consent_live is not True:
        raise ValueError('explicit --consent-live is required')
    if type(max_invocations) is not int or not 1 <= max_invocations <= 30:
        raise ValueError('max-invocations must be an integer from 1 through 30')
    if type(timeout) not in (int, float) or not 0 < timeout <= 3600:
        raise ValueError('timeout must be positive and at most 3600 seconds')
    fresh = prepare_plan(root, plan.get('provider'), plan.get('family'), len(plan.get('cases', [])), plan.get('model_selector'))
    if fresh != plan or not plan['model_selector'] or plan['invocations'] > max_invocations:
        raise ValueError('plan integrity, explicit model or invocation budget invalid')
    provider = plan['provider']
    command_path = shutil.which(executable or provider)
    report = {'schema_version': '1.0.0', 'plan': plan, 'consent_live': True,
              'provider': provider, 'cli_version': None, 'model_selector': plan['model_selector'],
              'environment': {'system': platform.system(), 'python': platform.python_version()},
              'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'max_invocations': max_invocations, 'timeout_seconds': timeout,
              'state': 'UNAVAILABLE' if not command_path else 'COMPLETED',
              'runs': [], 'qualification': 'optional-captured-provider-run',
              'professional_approval': False, 'metrics': {'state': 'not-measurable',
              'reason': 'No independent outcome labels supplied.', 'tp': None, 'fp': None,
              'fn': None, 'tn': None, 'precision': None, 'recall': None, 'fpr': None},
              'limitations': ['Captured output is not independently labelled human-gold.',
                              'Invocation count does not cap provider token charges.',
                              'Provider prose, prompts and stderr are not retained.']}
    if command_path:
        with tempfile.TemporaryDirectory(prefix='jai-optional-eval-') as directory:
            version = _capture([command_path, '--version'], min(timeout, 10), directory)
            match = re.search(r'(?<![A-Za-z0-9])([0-9]+\.[0-9]+(?:\.[0-9]+)?)(?![A-Za-z0-9])', version['stdout'])
            report['cli_version'] = match.group(1) if version['state'] == 'COMPLETED' and match else None
            for case in plan['cases']:
                path = _runtime(root) / 'content/expert_references' / plan['family'] / (case['complexity'] + '.md')
                prompt = ('Evaluate this fictional professional example. Identify omissions, unsupported claims, '
                          'and limitations. Do not claim executed tests or professional approval.\n' + path.read_text())
                arguments = ([command_path, 'exec', '--json', '--skip-git-repo-check', '--model', plan['model_selector'], '--sandbox', 'read-only', prompt]
                             if provider == 'codex' else [command_path, '--print', '--output-format', 'json', '--model', plan['model_selector'], '--tools', '', prompt])
                started = time.monotonic()
                captured = _capture(arguments, timeout, directory)
                observed = _observed(captured['stdout'])
                state = captured['state']
                if state == 'COMPLETED' and not observed['valid']:
                    state = 'INVALID_OUTPUT'
                report['runs'].append({'complexity': case['complexity'], 'state': state,
                                       'exit_code': captured['exit_code'],
                                       'elapsed_seconds': round(time.monotonic() - started, 6),
                                       'observed_model': observed['model'], 'usage': observed['usage'],
                                       'output_characters': observed['output_characters']})
                if state != 'COMPLETED':
                    report['state'] = state
                    break
    report['report_hash'] = _digest(report)
    return report


def inspect_report(report):
    """Validate a captured report without executing any provider.

    Args:
        report: JSON-compatible report from run_plan.
    Returns:
        Public summary preserving non-measurable metrics and execution limitations.
    Raises:
        ValueError: If integrity or the recognized report shape is invalid.
    """
    payload = dict(report)
    recorded = payload.pop('report_hash', None)
    if recorded != _digest(payload) or payload.get('schema_version') != '1.0.0':
        raise ValueError('invalid captured report integrity')
    if payload.get('qualification') != 'optional-captured-provider-run':
        raise ValueError('unsupported report qualification')
    return {'state': payload['state'], 'provider': payload['provider'],
            'run_count': len(payload['runs']), 'metrics': payload['metrics'],
            'professional_approval': False, 'limitations': payload['limitations']}


def main(argv=None):
    """Run explicit optional CLI; return nonzero for unavailable or failed execution.

    Args:
        argv: Optional CLI tokens, defaulting to sys.argv.
    Returns:
        Integer exit status; plan/preflight never invoke a subprocess.
    Raises:
        SystemExit: For invalid CLI syntax.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('preflight', 'plan', 'run', 'report'))
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--provider', choices=('codex', 'claude'))
    parser.add_argument('--family', help='Bundled reference family or explicitly mapped canonical document kind.')
    parser.add_argument('--cases', type=int, default=3)
    parser.add_argument('--model')
    parser.add_argument('--executable')
    parser.add_argument('--max-invocations', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=60)
    parser.add_argument('--consent-live', action='store_true')
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'report':
            if not args.input:
                raise ValueError('--input is required')
            result = inspect_report(json.loads(args.input.read_text()))
        elif args.command == 'preflight':
            result = preflight(args.provider, args.executable)
        else:
            plan = prepare_plan(args.root, args.provider, args.family, args.cases, args.model)
            result = plan if args.command == 'plan' else run_plan(args.root, plan, args.consent_live, args.max_invocations, args.timeout, args.executable)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result.get('state', 'COMPLETED') in ('COMPLETED', 'AVAILABLE') else 1
    except (OSError, ValueError, KeyError, TypeError):
        parser.exit(1, 'Optional evaluation failed: invalid input, unavailable resource or execution error.\n')


if __name__ == '__main__':
    raise SystemExit(main())
