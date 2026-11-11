# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Bounded strace evidence interpreter; ambiguities are coverage gaps, never zero activity.

Usage: pinned-python trace.py --manifest ABS --trace ABS --output ABS.
Input is a combined strace -f -ttt -yy log with the qualification runner's fixed
syscall filter. This module observes evidence only and never controls a product.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path
import posixpath
import re

NONFILE = '@nonfile'
MAX_LINES = 1_000_000
MAX_EVENTS = 100_000
MAX_EVENT_EXAMPLES = 1_000
NETWORK = {'socket', 'socketpair', 'connect', 'bind', 'listen', 'accept', 'accept4', 'sendto', 'sendmsg', 'sendmmsg', 'recvfrom', 'recvmsg', 'recvmmsg', 'getsockname', 'getpeername', 'getsockopt', 'setsockopt', 'shutdown'}
ASYNC = {'io_setup', 'io_submit', 'io_uring_setup', 'io_uring_enter', 'io_uring_register'}
FD_WRITES = {'write', 'writev', 'pwrite64', 'pwritev', 'pwritev2', 'ftruncate', 'fchmod', 'fchown', 'futimes', 'fsetxattr', 'fremovexattr', 'fallocate'}
PATH_WRITES = {'truncate', 'chmod', 'chown', 'lchown', 'utime', 'utimes', 'mkdir', 'rmdir', 'unlink', 'mknod', 'setxattr', 'lsetxattr', 'removexattr', 'lremovexattr'}
AT_WRITES = {'mkdirat', 'unlinkat', 'mknodat', 'fchmodat', 'fchmodat2', 'fchownat', 'utimensat'}
READ_ONLY = {'access', 'faccessat', 'faccessat2', 'stat', 'stat64', 'lstat', 'lstat64', 'fstat', 'fstat64', 'newfstatat', 'statx', 'readlink', 'readlinkat', 'getcwd', 'getxattr', 'lgetxattr', 'fgetxattr', 'listxattr', 'llistxattr', 'flistxattr', 'statfs', 'fstatfs', 'statfs64', 'fstatfs64', 'wait4', 'waitid', 'kill', 'tkill', 'tgkill', 'exit', 'exit_group'}


def _arguments(text: str) -> list[str]:
    items, begin, depth, quoted, escaped = [], 0, 0, False, False
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '([{':
            depth += 1
        elif char in ')]}':
            depth -= 1
        elif char == ',' and depth == 0:
            items.append(text[begin:index].strip())
            begin = index + 1
    if quoted or depth != 0:
        raise ValueError('Unbalanced syscall arguments.')
    return items + [text[begin:].strip()]


def _quoted(value: str) -> str | None:
    if not value.startswith('"') or not value.endswith('"'):
        return None
    try:
        result = ast.literal_eval(value)
        return result if isinstance(result, str) else None
    except (ValueError, SyntaxError):
        return None


def _number(value: str) -> int | None:
    match = re.match(r'(-?0x[0-9a-fA-F]+|-?\d+)', value)
    return int(match[1], 0 if 'x' in match[1] else 10) if match else None


def analyze_trace(lines, manifest: dict, *, complete_input: bool = False) -> dict:
    """Classify fixed-filter process evidence with explicit ownership and uncertainty.

    Args:
        lines: Iterable of combined timestamped strace lines, not executable content.
        manifest: Fixed sourceRoot, initialCwd and trustedExecutables qualification inputs.
        complete_input: Opt in to consuming all input with exact online decision
            counters and bounded event/adverse examples. False preserves the
            existing bounded-input limits; either mode retains semantic gaps.
    Returns:
        Per-process lineage, exact classified-effect counters, gap totals and
        bounded examples. Complete input consumption does not imply clean or
        complete semantic coverage. Default CLI limits are unchanged.
    Raises:
        ValueError: Required absolute manifest paths or syscall argument structure are invalid.
    """
    root = posixpath.normpath(manifest['sourceRoot'])
    cwd = posixpath.normpath(manifest['initialCwd'])
    trusted = set(manifest['trustedExecutables'])
    if not root.startswith('/') or not cwd.startswith('/') or any(not path.startswith('/') for path in trusted):
        raise ValueError('Absolute trace interpretation inputs required.')
    processes, pending, mutations, network, executions, gaps, counts = {}, {}, [], [], [], [], {}
    other_mutations = []
    categories = {'sourceMutations': mutations, 'otherMutations': other_mutations,
                  'network': network, 'executions': executions}
    event_totals = {key: 0 for key in categories}
    decisions = {key: 0 for key in ('sourceMutationAttempts', 'successfulSourceMutations',
        'deniedSourceMutations', 'unapprovedMutationAttempts', 'evidenceMutationAttempts',
        'ipActions', 'successfulIpActions', 'unknownNetworkActions', 'untrustedExecAttempts')}
    adverse_examples = {key: [] for key in decisions}
    gap_counts, children = {}, {}
    root_pid = None
    app_root = posixpath.normpath(manifest.get('appRoot', cwd))
    evidence_root = posixpath.dirname(root) if manifest.get('appRoot') else None
    line_count = 0
    input_exhausted = False

    def effect(key, event):
        decisions[key] += 1
        if len(adverse_examples[key]) < MAX_EVENT_EXAMPLES:
            adverse_examples[key].append(event)

    def record(category, event):
        event_totals[category] += 1
        if not complete_input or len(categories[category]) < MAX_EVENT_EXAMPLES:
            categories[category].append(event)
        if category == 'sourceMutations':
            effect('sourceMutationAttempts', event)
            if event['success']:
                effect('successfulSourceMutations', event)
            if event['denied']:
                effect('deniedSourceMutations', event)
        elif category == 'otherMutations':
            if event['scope'] in ('external', 'fixed-runtime'):
                effect('unapprovedMutationAttempts', event)
            elif event['scope'] == 'evidence':
                effect('evidenceMutationAttempts', event)
        elif category == 'executions' and not event['trusted']:
            effect('untrustedExecAttempts', event)
        elif category == 'network' and event['call'] in ('connect', 'sendto', 'sendmsg', 'sendmmsg', 'descriptor-write'):
            if event['family'] in ('AF_INET', 'AF_INET6'):
                effect('ipActions', event)
                if event['success']:
                    effect('successfulIpActions', event)
            elif event['family'] not in ('AF_UNIX', 'AF_LOCAL', 'AF_NETLINK'):
                effect('unknownNetworkActions', event)

    def process(pid):
        return processes.setdefault(pid, {'pid': pid, 'parent': None, 'cwd': [cwd], 'fds': {i: {'path': NONFILE, 'cloexec': False} for i in range(3)}, 'maps': [], 'exit': None, 'pidNamespace': None})

    def gap(pid, call, reason):
        key = (call, reason)
        gap_counts[key] = gap_counts.get(key, 0) + 1
        if len(gaps) < 1000:
            gaps.append({'pid': pid, 'call': call, 'reason': reason})

    def descriptor(token, context):
        match = re.match(r'(-?\d+)(?:<(.+)>)?(\(deleted\))?$', token)
        if not match:
            return None
        number = int(match[1])
        if number == -1:
            return NONFILE
        if match[2] is not None:
            annotation = match[2]
            if re.fullmatch(r'\{eventfd-count=(?:0x[0-9a-fA-F]+|\d+), eventfd-id=\d+, eventfd-semaphore=[01]\}', annotation):
                return NONFILE
            if annotation.startswith('/memfd:') and '...' not in annotation:
                return NONFILE
            annotation = re.sub(r'<(?:char|block) \d+:\d+>$', '', annotation)
            if '<' in annotation or ('>' in annotation and not annotation.startswith(('UNIX', 'TCP', 'UDP'))):
                return None
            if annotation.startswith('/') and '...' not in annotation:
                return posixpath.normpath(annotation.removesuffix(' (deleted)'))
            if annotation.startswith(('pipe:', 'socket:', 'anon_inode:', 'UNIX', 'TCP', 'UDP', 'NETLINK', 'eventfd', 'eventpoll', 'inotify')):
                return NONFILE
            return None
        return context['fds'].get(number, {}).get('path')

    def socket_family(token, context):
        if re.fullmatch(r'\d+<UNIX(?:-STREAM|-DGRAM|-SEQPACKET)?:\[[^<>]*?(?:->[^<>]*)?\]>', token):
            return 'AF_UNIX'
        if re.fullmatch(r'\d+<(?:TCP|UDP)(?:v6)?:\[.+\]>', token):
            return 'AF_INET6' if 'v6:' in token else 'AF_INET'
        return context['fds'].get(_number(token), {}).get('family')

    def path(value, context, directory='AT_FDCWD'):
        name = _quoted(value)
        if name is None:
            return None
        if name.startswith('/'):
            return posixpath.normpath(name)
        parent = context['cwd'][0] if directory == 'AT_FDCWD' else descriptor(directory, context)
        return posixpath.normpath(posixpath.join(parent, name)) if parent and parent != NONFILE else None

    def source(value):
        return value is not None and (value == root or value.startswith(root + '/'))

    def mutation(pid, call, paths, result, success):
        if any(value is None for value in paths):
            gap(pid, call, 'Unresolved source-capable path or descriptor.')
        selected = [value for value in paths if source(value)]
        for value in paths:
            if value is None or value == NONFILE or source(value):
                continue
            within = lambda base: base is not None and (value == base or value.startswith(base + '/'))
            scope = ('application' if within(app_root) else 'evidence' if within(evidence_root) else
                     'discard-device' if value in ('/dev/null', '/dev/zero') and call in ('open', 'openat', 'openat2', 'write', 'writev', 'pwrite64', 'pwritev', 'pwritev2') else
                     'fixed-runtime' if value in trusted else 'external')
            record('otherMutations', {'pid': pid, 'call': call, 'path': value, 'scope': scope, 'success': success, 'result': result})
        if selected:
            record('sourceMutations', {'pid': pid, 'call': call, 'paths': selected, 'success': success, 'denied': result.startswith('-1 ') and any(code in result for code in ('EACCES', 'EPERM', 'EROFS')), 'result': result})

    for original in lines:
        line_count += 1
        if not complete_input and (line_count > MAX_LINES or sum(event_totals.values()) >= MAX_EVENTS):
            gap(None, None, 'Trace evidence limit exceeded; remaining input is not classified.')
            break
        text = original.rstrip('\n')
        match = re.match(r'^(?:\[pid\s+(\d+)\]\s+|(\d+)\s+)?(\d+\.\d+)\s+(.*)$', text)
        if not match:
            if text.startswith('strace:'):
                gap(None, None, 'Tracer diagnostic: ' + text[:300])
            elif text.strip():
                gap(None, None, 'Unparsed timestamp/process line: ' + text[:200])
            continue
        pid = int(match[1] or match[2] or 0)
        body = match[4]
        if root_pid is None:
            root_pid = pid
            process(pid)['pidNamespace'] = False
        context = process(pid)
        if pid in children:
            parent, inherited = children.pop(pid)
            context.update(inherited)
            context['parent'] = parent
        if body.startswith('+++ exited with '):
            context['exit'] = {'kind': 'exit', 'code': _number(body[len('+++ exited with '):])}
            continue
        if body.startswith('+++ killed by '):
            context['exit'] = {'kind': 'signal', 'detail': body}
            continue
        if body.startswith('--- '):
            continue
        if body.endswith('<unfinished ...>'):
            if pid in pending:
                gap(pid, None, 'Multiple unfinished calls for one process.')
            pending[pid] = body[:-len('<unfinished ...>')]
            continue
        resumed = re.match(r'^<\.\.\. (\w+) resumed>(.*)$', body)
        if resumed:
            prefix = pending.pop(pid, None)
            if prefix is None or not prefix.startswith(resumed[1] + '('):
                gap(pid, resumed[1], 'Unpaired resumed syscall.')
                continue
            body = prefix + resumed[2]
        call_match = re.match(r'^(\w+)\((.*)\)\s+=\s+(.+)$', body)
        if not call_match:
            gap(pid, None, 'Unparsed syscall/result: ' + body[:200])
            continue
        call, raw_arguments, result = call_match.groups()
        counts[call] = counts.get(call, 0) + 1
        try:
            args = _arguments(raw_arguments)
            number = _number(result)
            success = number is not None and number >= 0
            if call in ASYNC:
                gap(pid, call, 'Asynchronous I/O is outside this bounded decoder; source targets cannot be excluded.')
            elif call in ('open', 'creat', 'openat', 'openat2'):
                target = path(args[1], context, args[0]) if call.startswith('openat') else path(args[0], context)
                # Successful -yy results observe the actual opened object, including
                # aliases or a child's cwd not yet reconstructed from clone ordering.
                if success and '<' in result:
                    observed = descriptor(result, context)
                    if observed is None:
                        gap(pid, call, 'Unresolved successful open result annotation.')
                    else:
                        target = observed
                if target is None:
                    gap(pid, call, 'Unresolved or truncated opened path.')
                flags = args[2] if call.startswith('openat') else args[1] if len(args) > 1 else ''
                if call == 'creat' or any(flag in flags for flag in ('O_WRONLY', 'O_RDWR', 'O_CREAT', 'O_TRUNC', 'O_APPEND')):
                    mutation(pid, call, [target], result, success)
                if success:
                    context['fds'][number] = {'path': target, 'cloexec': 'O_CLOEXEC' in flags}
            elif call in FD_WRITES:
                family = socket_family(args[0], context)
                if '<TCP' in args[0] or '<UDP' in args[0]:
                    family = family or 'AF_INET'
                if family is not None and call in ('write', 'writev', 'pwrite64', 'pwritev', 'pwritev2'):
                    record('network', {'pid': pid, 'call': 'descriptor-write', 'family': family, 'success': success, 'result': result})
                elif '<socket:' in args[0]:
                    gap(pid, call, 'Unresolved socket descriptor write family.')
                mutation(pid, call, [descriptor(args[0], context)], result, success)
            elif call in ('sendfile', 'sendfile64', 'splice', 'copy_file_range'):
                destination = args[0] if call.startswith('sendfile') else args[2]
                family = socket_family(destination, context)
                if '<TCP' in destination or '<UDP' in destination:
                    family = family or 'AF_INET'
                if family is not None:
                    record('network', {'pid': pid, 'call': 'descriptor-write', 'family': family, 'success': success, 'result': result})
                elif '<socket:' in destination:
                    gap(pid, call, 'Unresolved transfer socket family.')
                mutation(pid, call, [descriptor(destination, context)], result, success)
            elif call in PATH_WRITES:
                mutation(pid, call, [path(args[0], context)], result, success)
            elif call in AT_WRITES:
                mutation(pid, call, [descriptor(args[0], context) if args[1] == 'NULL' else path(args[1], context, args[0])], result, success)
            elif call in ('rename', 'link'):
                mutation(pid, call, [path(args[0], context), path(args[1], context)], result, success)
            elif call in ('renameat', 'renameat2', 'linkat'):
                mutation(pid, call, [path(args[1], context, args[0]), path(args[3], context, args[2])], result, success)
            elif call in ('symlink', 'symlinkat'):
                mutation(pid, call, [path(args[1], context) if call == 'symlink' else path(args[2], context, args[1])], result, success)
            elif call in ('chdir', 'fchdir'):
                target = path(args[0], context) if call == 'chdir' else descriptor(args[0], context)
                if success:
                    context['cwd'][0] = target
                    if target is None or target == NONFILE:
                        gap(pid, call, 'Unresolved working directory.')
            elif call in ('dup', 'dup2', 'dup3'):
                if success:
                    context['fds'][number] = {**context['fds'].get(_number(args[0]), {}), 'path': descriptor(args[0], context), 'cloexec': call == 'dup3' and 'O_CLOEXEC' in raw_arguments}
            elif call == 'fcntl':
                if success and 'F_DUPFD' in raw_arguments:
                    context['fds'][number] = {**context['fds'].get(_number(args[0]), {}), 'path': descriptor(args[0], context), 'cloexec': 'F_DUPFD_CLOEXEC' in raw_arguments}
                elif success and 'F_SETFD' in raw_arguments:
                    entry = context['fds'].get(_number(args[0]))
                    if entry is not None:
                        entry['cloexec'] = 'FD_CLOEXEC' in raw_arguments
            elif call == 'close':
                if success:
                    context['fds'].pop(_number(args[0]), None)
            elif call == 'close_range':
                lower, upper = _number(args[0]), 2**32 - 1 if args[1] == '~0U' else _number(args[1])
                if success and lower is not None and upper is not None:
                    if 'CLOSE_RANGE_UNSHARE' in raw_arguments:
                        context['fds'] = {key: dict(value) for key, value in context['fds'].items()}
                    for fd in list(context['fds']):
                        if lower <= fd <= upper:
                            if 'CLOSE_RANGE_CLOEXEC' in raw_arguments:
                                context['fds'][fd]['cloexec'] = True
                            else:
                                context['fds'].pop(fd)
                elif success:
                    gap(pid, call, 'Unresolved descriptor range.')
            elif call in ('clone', 'clone3', 'fork', 'vfork'):
                if success and number > 0:
                    # A return value inside a PID namespace is not a tracer host PID.
                    # Only an observed host prefix can establish an ordinary child.
                    if context['pidNamespace'] is not False:
                        gap(pid, call, 'Unresolved namespace-local child lineage; return ID is not a proven host PID.')
                    else:
                        inherited = {
                            'fds': context['fds'] if 'CLONE_FILES' in raw_arguments else {key: dict(value) for key, value in context['fds'].items()},
                            'cwd': context['cwd'] if 'CLONE_FS' in raw_arguments else list(context['cwd']),
                            'maps': context['maps'] if 'CLONE_VM' in raw_arguments else [dict(value) for value in context['maps']],
                            'pidNamespace': 'CLONE_NEWPID' in raw_arguments,
                        }
                        if number in processes:
                            processes[number]['pidNamespace'] = inherited['pidNamespace']
                            processes[number]['parent'] = pid
                            gap(pid, call, 'Child acted before observed clone completion; inherited state lineage is unresolved.')
                        else:
                            children[number] = (pid, inherited)
            elif call in ('execve', 'execveat'):
                target = path(args[0], context) if call == 'execve' else path(args[1], context, args[0])
                record('executions', {'pid': pid, 'path': target, 'trusted': target in trusted, 'success': success, 'result': result})
                if target is None:
                    gap(pid, call, 'Unresolved executable.')
                if success:
                    context['fds'] = {key: dict(value) for key, value in context['fds'].items() if not value['cloexec']}
            elif call in ('mmap', 'mmap2'):
                target = descriptor(args[4], context)
                if 'MAP_SHARED' in args[3] and 'PROT_WRITE' in args[2]:
                    mutation(pid, call, [target], result, success)
                if success:
                    context['maps'].append({'start': number, 'length': _number(args[1]), 'path': target, 'shared': 'MAP_SHARED' in args[3]})
            elif call in ('mprotect', 'munmap'):
                start, length = _number(args[0]), _number(args[1])
                if start is None or length is None:
                    gap(pid, call, 'Unresolved mapped range.')
                else:
                    for mapping in list(context['maps']):
                        if mapping['length'] is None:
                            gap(pid, call, 'Unknown mapped extent.')
                        elif start < mapping['start'] + mapping['length'] and mapping['start'] < start + length:
                            if call == 'mprotect' and mapping['shared'] and 'PROT_WRITE' in args[2]:
                                mutation(pid, call, [mapping['path']], result, success)
                            elif call == 'munmap' and success and start <= mapping['start'] and start + length >= mapping['start'] + mapping['length']:
                                context['maps'].remove(mapping)
            elif call == 'mremap':
                gap(pid, call, 'Remapped ancestry is outside this bounded decoder.')
            elif call == 'ioctl':
                target = descriptor(args[0], context)
                if (target is None or source(target)) and not any(command in raw_arguments for command in ('TCGETS', 'FIONREAD', 'FS_IOC_GET')):
                    gap(pid, call, 'Source-capable ioctl is outside this bounded decoder.')
            elif call in NETWORK:
                family = next(iter(re.findall(r'AF_[A-Z0-9_]+', raw_arguments)), None)
                if family is None:
                    family = socket_family(args[0], context)
                record('network', {'pid': pid, 'call': call, 'family': family, 'success': success, 'result': result})
                if call in ('socket', 'accept', 'accept4') and success:
                    context['fds'][number] = {'path': NONFILE, 'cloexec': 'CLOEXEC' in raw_arguments, 'family': family}
                if call == 'socketpair' and success:
                    endpoints = _arguments(args[3][1:-1]) if args[3].startswith('[') and args[3].endswith(']') else []
                    if len(endpoints) != 2 or any(_number(item) is None for item in endpoints):
                        gap(pid, call, 'Unresolved socketpair endpoints.')
                    else:
                        for endpoint in endpoints:
                            context['fds'][_number(endpoint)] = {'path': NONFILE, 'cloexec': 'CLOEXEC' in raw_arguments, 'family': family}
                if family is None and call in ('connect', 'sendto', 'sendmsg', 'sendmmsg'):
                    gap(pid, call, 'Unresolved network family.')
            elif call not in READ_ONLY:
                gap(pid, call, 'Unsupported syscall in the declared evidence filter.')
        except (ValueError, IndexError, TypeError):
            gap(pid, call, 'Malformed or truncated syscall arguments.')
    else:
        input_exhausted = True

    for child_pid, (parent, _) in children.items():
        gap(parent, 'clone', 'Unresolved child lineage; returned ID has no observed host process prefix.')
    for pid in pending:
        gap(pid, None, 'Unfinished syscall at end of trace.')
    for pid, context in processes.items():
        if context['exit'] is None:
            gap(pid, None, 'No observed process/thread exit.')
    if not event_totals['executions']:
        gap(None, None, 'No observed executable start; empty/partial trace cannot qualify.')
    summary = {**decisions, 'processes': len(processes), 'lines': line_count}
    return {'format': 'jai.fabric-explorer.security-trace/1', 'coverage': {'complete': not gap_counts, 'gaps': gaps, 'gapCount': sum(gap_counts.values()), 'gapCounts': [{'call': call, 'reason': reason, 'count': count} for (call, reason), count in gap_counts.items()], 'unfinishedPids': sorted(pending)}, 'summary': summary,
            'clean': not gap_counts and not summary['successfulSourceMutations'] and not summary['ipActions'] and not summary['unknownNetworkActions'] and not summary['untrustedExecAttempts'] and not summary['unapprovedMutationAttempts'],
            'eventRetention': {'completeInputRequested': complete_input, 'inputFullyConsumed': input_exhausted, 'maxExamplesPerCategory': MAX_EVENT_EXAMPLES if complete_input else None, 'totals': event_totals, 'retained': {key: len(value) for key, value in categories.items()}}, 'adverseExamples': adverse_examples,
            'sourceMutations': mutations, 'otherMutations': other_mutations, 'network': network, 'executions': executions, 'processes': [{'pid': value['pid'], 'parent': value['parent'], 'exit': value['exit']} for value in processes.values()], 'syscallCounts': counts}


def main() -> int:
    """Read fixed manifest/raw trace and publish evidence without touching selected sources.

    Returns:
        Zero only for complete clean evidence; two for unknown or adverse observations.
    Raises:
        OSError: Evidence cannot be read or written.
        ValueError: Manifest/input contract is invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('manifest', 'trace', 'output'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    if not all(path.is_absolute() for path in (args.manifest, args.trace, args.output)):
        raise ValueError('Absolute evidence paths required.')
    specification = importlib.util.spec_from_file_location('security_qualification_fixtures', Path(__file__).with_name('fixtures.py'))
    if specification is None or specification.loader is None:
        raise ValueError('Fixed sibling fixture module unavailable.')
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    manifest = module.load_manifest(args.manifest)
    if args.trace.stat().st_size > 128 * 1024 * 1024:
        report = {'format': 'jai.fabric-explorer.security-trace/1', 'clean': False, 'coverage': {'complete': False, 'gaps': [{'reason': 'Raw trace exceeds the 128 MiB interpretation ceiling.'}]}}
    else:
        with args.trace.open(encoding='utf-8', errors='strict') as stream:
            report = analyze_trace(stream, manifest)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    return 0 if report['clean'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
