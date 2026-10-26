#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Run mandatory checks with inherited network denial and provider-call auditing.

Linux seccomp denies non-Unix sockets and io_uring in the entire child process
tree. Local Unix IPC remains available. Python audit hooks additionally reject
provider executables and shell-wrapped calls. This is an offline qualification
control for trusted project tests, not a general hostile-code security sandbox.
Unavailable kernel enforcement is NOT_EXECUTED, never a successful offline run.
"""
from __future__ import annotations

import argparse
import ast
import ctypes
import codecs
import errno
import json
import math
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import threading
import time

_PROVIDERS = {'codex', 'claude', 'codex.exe', 'claude.exe', 'codex.cmd', 'claude.cmd'}
_ALLOWED_ENV = ('PATH', 'HOME', 'USER', 'LOGNAME', 'TMPDIR', 'TMP', 'TEMP',
                'LANG', 'LC_ALL', 'TZ', 'SYSTEMROOT', 'COMSPEC', 'PATHEXT',
                'FONTCONFIG_PATH', 'FONTCONFIG_FILE',
                # Public documentation identity, never a token or permission.
                'GITHUB_REPOSITORY', 'JAI_GITHUB_REPOSITORY')


def _provider_command(command):
    if isinstance(command, (str, bytes)):
        try:
            lexer = shlex.shlex(os.fsdecode(command), posix=True, punctuation_chars=';&|()')
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            return True
        for index, token in enumerate(tokens):
            preceding = tokens[index - 1] if index else ''
            if Path(token).name.lower() in _PROVIDERS and (
                    not index or preceding in ('exec', 'command', 'env', 'nohup')
                    or (preceding and all(char in ';&|()' for char in preceding))):
                return True
    elif isinstance(command, (list, tuple)):
        tokens = [os.fsdecode(value) for value in command if isinstance(value, (str, bytes, os.PathLike))]
    else:
        return False
    if not tokens:
        return False
    executable = Path(tokens[0]).name.lower()
    if executable in _PROVIDERS:
        return True
    if executable in ('sh', 'bash', 'dash', 'zsh', 'cmd', 'cmd.exe', 'powershell', 'pwsh', 'env'):
        return any(_provider_command(value) for value in tokens[1:])
    if executable in ('node', 'nodejs', 'python', 'python3') and len(tokens) > 1:
        return any(part.lower() in ('codex', 'claude', '@anthropic-ai')
                   for part in Path(tokens[1]).parts)
    return False


def scan_sources(root):
    """Find direct paid-provider commands or SDK imports in mandatory test source.

    Args:
        root: Project containing tests/; no private input directories are read.
    Returns:
        Located diagnostics for Python syntax errors, direct provider launches
        and inference SDK imports. Static inspection cannot prove arbitrary
        computed commands safe; runtime auditing and kernel denial complement it.
    """
    root = Path(root)
    findings = []
    for path in sorted((root / 'tests').rglob('*.py')):
        if path.is_symlink():
            findings.append({'path': str(path.relative_to(root)), 'line': 1, 'rule': 'MANDATORY_TEST_SYMLINK'})
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8'))
        except (SyntaxError, UnicodeError):
            findings.append({'path': str(path.relative_to(root)), 'line': 1, 'rule': 'MANDATORY_TEST_PARSE_ERROR'})
            continue
        for node in ast.walk(tree):
            rule = None
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                modules = [entry.name for entry in node.names] if isinstance(node, ast.Import) else [node.module or '']
                if any(name.split('.')[0] in ('openai', 'anthropic') for name in modules):
                    rule = 'MANDATORY_INFERENCE_SDK_IMPORT'
            if isinstance(node, ast.Call) and node.args:
                name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, 'id', '')
                if name in ('run', 'Popen', 'call', 'check_call', 'check_output', 'system', 'execvp', 'execv', 'spawnv', 'posix_spawn'):
                    try:
                        command = ast.literal_eval(node.args[0])
                    except (ValueError, TypeError):
                        continue
                    if _provider_command(command):
                        rule = 'MANDATORY_LIVE_PROVIDER_CALL'
            if rule:
                findings.append({'path': str(path.relative_to(root)), 'line': node.lineno, 'rule': rule})
    return findings


def safe_environment(root):
    """Build an allowlisted child environment without reading credential values.

    Args:
        root: Trusted project root, used only to locate the guard bootstrap.
    Returns:
        New environment containing selected operating-system settings and fixed
        offline controls, public documentation repository identity, and the
        explicit streaming preference when set. Repository identity is still
        validated by the documentation consumer; it grants no permissions.
        Arbitrary parent variables and credential keys are
        neither copied nor inspected. Credential-file access is not sandboxed.
    """
    environment = {key: os.environ[key] for key in _ALLOWED_ENV if key in os.environ}
    tools = Path(__file__).resolve().parent
    environment['PYTHONPATH'] = os.pathsep.join((str(tools / 'offline_bootstrap'), str(tools)))
    environment['JAI_OFFLINE_GUARD_ACTIVE'] = '1'
    environment['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    environment['PYTHONNOUSERSITE'] = '1'
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    if os.environ.get('JAI_OFFLINE_STREAM') == '1':
        environment['JAI_OFFLINE_STREAM'] = '1'
    return environment


def install_python_audit():
    """Install process-local denial of Python provider execution and networking.

    No arguments or return value. Audit violations raise RuntimeError; this
    complements the inherited Linux filter and does not replace OS enforcement.
    """
    def audit(event, args):
        if event == 'subprocess.Popen':
            if _provider_command(args[1]) or _provider_command([args[0]]):
                raise RuntimeError('OFFLINE_PROVIDER_EXECUTION_DENIED')
        elif event in ('os.system', 'os.exec', 'os.posix_spawn') and args:
            candidate = args[1] if event != 'os.system' and len(args) > 1 else args[0]
            if _provider_command(candidate):
                raise RuntimeError('OFFLINE_PROVIDER_EXECUTION_DENIED')
        elif event == 'socket.__new__' and len(args) > 1 and args[1] != 1:
            raise PermissionError(errno.EPERM, 'OFFLINE_NETWORK_DENIED')
    sys.addaudithook(audit)


def _install_network_filter():
    if sys.platform != 'linux':
        raise OSError('OS_NETWORK_DENIAL_UNAVAILABLE')
    library = ctypes.CDLL('libseccomp.so.2', use_errno=True)
    class Comparison(ctypes.Structure):
        _fields_ = [('arg', ctypes.c_uint), ('op', ctypes.c_int),
                    ('datum_a', ctypes.c_uint64), ('datum_b', ctypes.c_uint64)]
    library.seccomp_init.argtypes = [ctypes.c_uint32]
    library.seccomp_init.restype = ctypes.c_void_p
    library.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    library.seccomp_syscall_resolve_name.restype = ctypes.c_int
    library.seccomp_rule_add_array.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int,
                                             ctypes.c_uint, ctypes.POINTER(Comparison)]
    library.seccomp_rule_add_array.restype = ctypes.c_int
    library.seccomp_load.argtypes = [ctypes.c_void_p]
    library.seccomp_load.restype = ctypes.c_int
    library.seccomp_release.argtypes = [ctypes.c_void_p]
    context = library.seccomp_init(0x7fff0000)
    if not context:
        raise OSError('OS_NETWORK_DENIAL_UNAVAILABLE')
    try:
        # Restrict socket families rather than connect() so local Unix IPC can
        # serve renderers without permitting DNS, loopback or Internet traffic.
        comparison = Comparison(0, 1, 1, 0)  # SCMP_CMP_NE, AF_UNIX
        for name in (b'socket', b'socketpair'):
            syscall = library.seccomp_syscall_resolve_name(name)
            if syscall < 0 or library.seccomp_rule_add_array(context, 0x00050000 | errno.EPERM, syscall, 1, ctypes.byref(comparison)):
                raise OSError('OS_NETWORK_DENIAL_UNAVAILABLE')
        for name in (b'io_uring_setup', b'io_uring_enter', b'io_uring_register', b'socketcall'):
            syscall = library.seccomp_syscall_resolve_name(name)
            if syscall >= 0 and library.seccomp_rule_add_array(context, 0x00050000 | errno.EPERM, syscall, 0, None):
                raise OSError('OS_NETWORK_DENIAL_UNAVAILABLE')
        if library.seccomp_load(context):
            raise OSError('OS_NETWORK_DENIAL_UNAVAILABLE')
    finally:
        library.seccomp_release(context)


def _stream_pipe(pipe, sink, captured):
    decoder = codecs.getincrementaldecoder(pipe.encoding)(errors='replace')
    try:
        while chunk := pipe.buffer.read1(65536):
            value = decoder.decode(chunk)
            captured.append(value)
            sink.write(value)
            sink.flush()
        value = decoder.decode(b'', final=True)
        captured.append(value)
        if value:
            sink.write(value)
            sink.flush()
    finally:
        pipe.close()


def run_offline(command, root, timeout=900, stream=None):
    """Run a trusted command under inherited Linux network-denial controls.

    Args:
        command: Nonempty argument list, never executed through an implicit shell.
        root: Working directory for the child process.
        timeout: Positive maximum wall seconds; expiry is nonpassing.
        stream: Forward child output immediately while retaining capture. None
            inherits the explicit JAI_OFFLINE_STREAM=1 setting; False disables
            forwarding. True propagates streaming to nested guarded commands.
    Returns:
        Status, exit code and captured local output. NOT_EXECUTED is returned
        when required OS controls cannot load, not a waiver or qualification.
    Raises:
        ValueError: If timeout is invalid or command is not an argument list.
    """
    if not isinstance(command, (list, tuple)) or not command or not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('INVALID_OFFLINE_COMMAND_OR_TIMEOUT')
    if _provider_command(command):
        return {'status': 'FAIL', 'returncode': 1, 'reason': 'LIVE_PROVIDER_FORBIDDEN', 'stdout': '', 'stderr': ''}
    stream = os.environ.get('JAI_OFFLINE_STREAM') == '1' if stream is None else stream
    environment = safe_environment(root)
    if stream:
        environment['JAI_OFFLINE_STREAM'] = '1'
    else:
        environment.pop('JAI_OFFLINE_STREAM', None)
    try:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '_worker', *command],
                                   cwd=root, env=environment, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True, close_fds=True,
                                   start_new_session=True)
        deadline = time.monotonic() + timeout
        captures = ([], [])
        readers = []
        if stream:
            for pipe, sink, captured in zip((process.stdout, process.stderr),
                                            (sys.stdout, sys.stderr), captures):
                reader = threading.Thread(target=_stream_pipe, args=(pipe, sink, captured))
                reader.start()
                readers.append(reader)
        try:
            if stream:
                process.wait(timeout=timeout)
                for reader in readers:
                    reader.join(timeout=max(0, deadline - time.monotonic()))
                if any(reader.is_alive() for reader in readers):
                    raise subprocess.TimeoutExpired(command, timeout)
                stdout, stderr = (''.join(parts) for parts in captures)
            else:
                stdout, stderr = process.communicate(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            if os.name == 'posix':
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            if stream:
                process.wait()
                for reader in readers:
                    reader.join()
                stdout, stderr = (''.join(parts) for parts in captures)
            else:
                stdout, stderr = process.communicate()
            return {'status': 'FAIL', 'returncode': 124, 'reason': 'OFFLINE_TIMEOUT', 'stdout': stdout, 'stderr': stderr}
    except subprocess.TimeoutExpired:
        return {'status': 'FAIL', 'returncode': 124, 'reason': 'OFFLINE_TIMEOUT', 'stdout': '', 'stderr': ''}
    except OSError:
        return {'status': 'NOT_EXECUTED', 'returncode': 77, 'reason': 'OFFLINE_EXECUTION_UNAVAILABLE', 'stdout': '', 'stderr': ''}
    if process.returncode == 77 and 'OS_NETWORK_DENIAL_UNAVAILABLE' in stderr:
        return {'status': 'NOT_EXECUTED', 'returncode': 77, 'reason': 'OS_NETWORK_DENIAL_UNAVAILABLE', 'stdout': stdout, 'stderr': stderr}
    if process.returncode == 77 and 'OFFLINE_EXECUTION_UNAVAILABLE' in stderr:
        return {'status': 'NOT_EXECUTED', 'returncode': 77, 'reason': 'OFFLINE_EXECUTION_UNAVAILABLE', 'stdout': stdout, 'stderr': stderr}
    return {'status': 'PASS' if process.returncode == 0 else 'FAIL', 'returncode': process.returncode,
            'network_control': 'linux-seccomp-inherited', 'stdout': stdout, 'stderr': stderr}


def main(argv=None):
    """Scan mandatory source or execute a guarded qualification command.

    Args:
        argv: Optional arguments; run takes --root ROOT [--timeout SECONDS] [--stream] --
            COMMAND [ARGS...]. The default 900-second ceiling is unchanged.
    Returns:
        Zero only for successful scan/execution; one for failure, 77 for unavailable
        OS denial. Captured test output is local diagnostic output, not public
        customer evidence and must not be automatically published unsanitized.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == '_worker':
        try:
            _install_network_filter()
        except (OSError, AttributeError):
            print('OS_NETWORK_DENIAL_UNAVAILABLE', file=sys.stderr)
            return 77
        try:
            os.execvpe(argv[1], argv[1:], os.environ)
        except OSError:
            print('OFFLINE_EXECUTION_UNAVAILABLE', file=sys.stderr)
            return 77
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('scan', 'run'))
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--timeout', type=float, default=900,
                        help='Positive finite wall seconds (default: 900).')
    parser.add_argument('--stream', action='store_true',
                        help='Forward output immediately and retain diagnostic capture.')
    command_args = []
    if '--' in argv:
        index = argv.index('--')
        command_args, argv = argv[index + 1:], argv[:index]
    args = parser.parse_args(argv)
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('--timeout must be positive and finite')
    if args.command == 'scan':
        findings = scan_sources(args.root)
        print(json.dumps({'status': 'FAIL' if findings else 'PASS', 'findings': findings}, indent=2))
        return 1 if findings else 0
    if not command_args:
        print(json.dumps({'status': 'FAIL', 'reason': 'OFFLINE_COMMAND_REQUIRED'}))
        return 1
    streaming = args.stream or os.environ.get('JAI_OFFLINE_STREAM') == '1'
    options = {'stream': True} if streaming else {}
    result = run_offline(command_args, args.root, timeout=args.timeout, **options)
    if not streaming:
        sys.stdout.write(result['stdout'])
        sys.stderr.write(result['stderr'])
    print(json.dumps({key: value for key, value in result.items() if key not in ('stdout', 'stderr')}))
    return 0 if result['status'] == 'PASS' else 77 if result['status'] == 'NOT_EXECUTED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
