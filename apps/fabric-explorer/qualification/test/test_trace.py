# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Synthetic syscall counterexamples and actual isolated CLI checks; no invented product trace."""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

MODULE = Path(__file__).resolve().parents[1] / 'trace.py'
SPEC = importlib.util.spec_from_file_location('security_trace', MODULE)
trace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trace)
ROOT = Path(__file__).resolve().parents[4]
PYTHON = ROOT / 'build/fabric-explorer/helper-venv/bin/python'
MANIFEST = {'sourceRoot': '/sources', 'initialCwd': '/application', 'trustedExecutables': ['/trusted/main', '/trusted/child']}


def analyze(*calls):
    records = [(10, 'execve("/trusted/main", ["main"], 0x0) = 0'), *calls]
    pids = sorted({pid for pid, _ in records})
    records += [(pid, '+++ exited with 0 +++') for pid in pids]
    return trace.analyze_trace([f'{pid} {1000 + index / 1000:.6f} {call}\n' for index, (pid, call) in enumerate(records)], MANIFEST)


def test_clean_empty_product_and_no_false_empty_trace_pass():
    assert analyze()['clean']
    empty = trace.analyze_trace([], MANIFEST)
    assert not empty['clean'] and not empty['coverage']['complete']


def test_denied_and_successful_source_opens_are_distinct():
    denied = analyze((10, 'openat(AT_FDCWD, "/sources/record", O_WRONLY|O_APPEND) = -1 EACCES (Permission denied)'))
    assert denied['summary']['sourceMutationAttempts'] == 1
    assert denied['summary']['deniedSourceMutations'] == 1
    assert denied['summary']['successfulSourceMutations'] == 0
    success = analyze((10, 'openat(AT_FDCWD, "/sources/record", O_RDWR|O_CREAT, 0600) = 3</sources/record>'))
    assert success['summary']['successfulSourceMutations'] == 1 and not success['clean']


def test_external_writes_are_not_silently_treated_as_clean_application_activity():
    result = analyze((10, 'openat(AT_FDCWD, "/outside/unapproved", O_WRONLY|O_CREAT, 0600) = 3</outside/unapproved>'))
    assert not result['clean']
    assert result['otherMutations'][0]['scope'] == 'external'
    assert result['summary']['unapprovedMutationAttempts'] == 1


def test_owned_application_and_exact_discard_device_writes_remain_explicit():
    result = analyze((10, 'openat(AT_FDCWD, "/application/log", O_WRONLY|O_CREAT, 0600) = 3</application/log>'),
                     (10, 'write(3, "log", 3) = 3'), (10, 'write(4</dev/null>, "discard", 7) = 7'))
    assert result['clean']
    assert [event['scope'] for event in result['otherMutations']] == ['application', 'application', 'discard-device']


def test_fallocate_is_a_source_fd_mutation_and_unmodeled_remap_is_an_explicit_gap():
    result = analyze((10, 'fallocate(3</sources/record>, 0, 0, 4096) = 0'))
    assert result['summary']['successfulSourceMutations'] == 1
    assert not analyze((10, 'mremap(0x1000, 4096, 8192, MREMAP_MAYMOVE) = 0x2000'))['coverage']['complete']


def test_ip_socket_byte_writes_cannot_bypass_network_attempt_reporting():
    result = analyze((10, 'socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) = 3'),
                     (10, 'write(3<TCP:[127.0.0.1:9]>, "request", 7) = -1 EPERM (Operation not permitted)'))
    assert result['summary']['ipActions'] == 1 and not result['clean']


def test_descriptor_relative_targets_and_multiple_rename_paths():
    result = analyze((10, 'openat(AT_FDCWD, "/sources", O_RDONLY|O_DIRECTORY) = 3</sources>'),
                     (10, 'openat(3, "record", O_WRONLY) = -1 EROFS (Read-only file system)'),
                     (10, 'renameat(3, "record", AT_FDCWD, "/application/new") = -1 EACCES (Permission denied)'))
    assert [event['paths'] for event in result['sourceMutations']] == [['/sources/record'], ['/sources/record']]
    assert result['coverage']['complete']


def test_inherited_duplicate_and_closed_descriptors_do_not_silently_escape():
    result = analyze((10, 'openat(AT_FDCWD, "/sources/record", O_RDONLY) = 3</sources/record>'),
                     (10, 'dup3(3, 7, 0) = 7'), (10, 'clone(child_stack=NULL, flags=SIGCHLD) = 20'),
                     (20, 'write(7, "unexpected", 10) = -1 EBADF (Bad file descriptor)'),
                     (20, 'close(7) = 0'), (20, 'write(7, "unknown", 7) = 7'))
    assert result['sourceMutations'][0]['paths'] == ['/sources/record']
    assert next(item for item in result['processes'] if item['pid'] == 20)['parent'] == 10
    assert not result['coverage']['complete']


def test_shared_descriptor_close_and_close_on_exec_are_not_retained_as_live_files():
    shared = analyze((10, 'openat(AT_FDCWD, "/sources/record", O_RDONLY) = 3'),
                     (10, 'clone(child_stack=NULL, flags=CLONE_FILES|SIGCHLD) = 20'), (20, 'close(3) = 0'),
                     (10, 'write(3, "unknown", 7) = 7'))
    assert not shared['coverage']['complete']
    executed = analyze((10, 'openat(AT_FDCWD, "/sources/record", O_RDONLY) = 3'),
                       (10, 'fcntl(3, F_DUPFD_CLOEXEC, 7) = 7'),
                       (10, 'execve("/trusted/child", ["child"], 0x0) = 0'),
                       (10, 'write(7, "unknown", 7) = 7'))
    assert not executed['coverage']['complete']


@pytest.mark.parametrize('call', [
    'sendfile(4</sources/out>, 3</application/in>, NULL, 10) = 10',
    'splice(3</application/in>, NULL, 4</sources/out>, NULL, 10, 0) = 10',
    'copy_file_range(3</application/in>, NULL, 4</sources/out>, NULL, 10, 0) = 10',
    'ftruncate(4</sources/out>, 0) = 0',
    'fchmod(4</sources/out>, 0600) = 0',
])
def test_fd_transfer_and_metadata_mutations(call):
    result = analyze((10, call))
    assert result['summary']['successfulSourceMutations'] == 1 and not result['clean']


def test_shared_source_mapping_and_write_permission_changes_are_observed():
    result = analyze((10, 'mmap(NULL, 4096, PROT_READ, MAP_SHARED, 3</sources/record>, 0) = 0x1000'),
                     (10, 'mprotect(0x1000, 4096, PROT_READ|PROT_WRITE) = -1 EACCES (Permission denied)'),
                     (10, 'mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, 3</sources/record>, 0) = 0x2000'))
    assert result['summary']['sourceMutationAttempts'] == 2
    assert result['summary']['successfulSourceMutations'] == 1


def test_local_desktop_ipc_and_denied_ip_egress_are_not_conflated():
    local = analyze((10, 'socket(AF_UNIX, SOCK_STREAM|SOCK_CLOEXEC, 0) = 3'),
                    (10, 'connect(3, {sa_family=AF_UNIX, sun_path="/run/user/session"}, 32) = 0'))
    assert local['clean'] and local['summary']['ipActions'] == 0
    remote = analyze((10, 'socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP) = 3'),
                     (10, 'connect(3, {sa_family=AF_INET6, sin6_port=htons(443)}, 28) = -1 EPERM (Operation not permitted)'))
    assert not remote['clean'] and remote['summary']['ipActions'] == 1 and remote['summary']['successfulIpActions'] == 0


def test_unapproved_child_exec_attempt_is_reported_even_when_os_denies_it():
    result = analyze((10, 'clone(child_stack=NULL, flags=SIGCHLD) = 20'),
                     (20, 'execve("/sources/project-program", ["project"], 0x0) = -1 EACCES (Permission denied)'))
    assert result['summary']['untrustedExecAttempts'] == 1
    assert not result['executions'][-1]['success'] and not result['clean']


def test_unfinished_resumed_and_unparsed_or_truncated_data_are_explicit():
    resumed = analyze((10, 'openat(AT_FDCWD, "/sources/record", O_WRONLY <unfinished ...>'),
                      (10, '<... openat resumed>) = -1 EACCES (Permission denied)'))
    assert resumed['coverage']['complete'] and resumed['summary']['deniedSourceMutations'] == 1
    for call in ['openat(AT_FDCWD, "/sources/long"..., O_RDONLY) = 3', '<... write resumed>"x", 1) = 1', 'unparsed-call', 'write(3, "x", 1 <unfinished ...>']:
        result = analyze((10, call))
        assert not result['clean'] and not result['coverage']['complete']


def test_async_io_and_unsupported_syscalls_are_gaps_not_zero_activity():
    for call in ['io_uring_setup(8, {flags=0}) = -1 EPERM (Operation not permitted)', 'new_unknown_call(3) = 0']:
        result = analyze((10, call))
        assert not result['coverage']['complete'] and not result['clean']


def test_isolated_cli_loads_fixed_sibling_module_and_reports_unknown_trace(tmp_path):
    source, application = tmp_path / 'synthetic-source', tmp_path / 'application'
    source.mkdir(); application.mkdir()
    manifest = {'format': 'jai.fabric-explorer.security-input/1', 'sourceRoot': str(source), 'projectRoot': str(source), 'fabric': str(source / 'fabric.jsonl'), 'findings': str(source / 'findings.jsonl'), 'appRoot': str(application), 'initialCwd': str(application), 'trustedExecutables': ['/trusted/main'], 'sourceSnapshotBefore': [], 'negativeWriteProbes': []}
    manifest_path = tmp_path / 'security-input.json'; manifest_path.write_text(json.dumps(manifest))
    raw = tmp_path / 'trace.log'; output = tmp_path / 'report.json'
    raw.write_text('10 1000.000000 execve("/trusted/main", ["main"], 0x0) = 0\n10 1000.000001 +++ exited with 0 +++\n')
    command = [str(PYTHON), '-I', '-B', str(MODULE), '--manifest', str(manifest_path), '--trace', str(raw), '--output', str(output)]
    completed = subprocess.run(command, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(output.read_text())['clean']
    raw.write_text('unparsed evidence\n')
    assert subprocess.run(command, capture_output=True, text=True).returncode == 2
    assert not json.loads(output.read_text())['coverage']['complete']


def test_fixed_discard_open_and_network_transfer_are_attributed():
    discarded = analyze((10, 'openat(AT_FDCWD, "/dev/null", O_RDWR) = 3</dev/null>'))
    assert discarded['clean'] and discarded['otherMutations'][0]['scope'] == 'discard-device'
    transfer = analyze((10, 'sendfile(4<TCP:[127.0.0.1:9]>, 3</sources/record>, NULL, 10) = 10'))
    assert transfer['summary']['ipActions'] == 1 and not transfer['clean']


def test_successful_open_uses_observed_fd_target_not_lexical_cwd_guess():
    result = analyze((10, 'openat(AT_FDCWD, "journal", O_WRONLY|O_TRUNC) = 3</sources/journal>'))
    assert not result['clean']
    assert result['sourceMutations'][0]['paths'] == ['/sources/journal']
    assert result['summary']['successfulSourceMutations'] == 1


@pytest.mark.parametrize('annotation,expected', [
    ('/sources/spaced record', '/sources/spaced record'),
    ('/dev/null<char 1:3>', '/dev/null'),
    ('/dev/dri/renderD129<char 226:129>', '/dev/dri/renderD129'),
    ('/dev/disk<block 8:0>', '/dev/disk'),
])
def test_full_returned_fd_preserves_path_and_device_decoration(annotation, expected):
    result = analyze((10, f'openat(AT_FDCWD, "alias", O_RDWR) = 5<{annotation}>'),
                     (10, 'write(5, "x", 1) = 1'))
    assert result['coverage']['complete']
    events = result['sourceMutations'] if expected.startswith('/sources/') else result['otherMutations']
    assert (events[0].get('paths') or [events[0]['path']]) == [expected]


@pytest.mark.parametrize('descriptor', [
    '27<{eventfd-count=0x1, eventfd-id=436, eventfd-semaphore=0}>',
    '11<{eventfd-count=0, eventfd-id=424, eventfd-semaphore=0}>',
    '40</memfd:wayland-cursor>(deleted)',
])
def test_exact_native_nonfilesystem_descriptors(descriptor):
    result = analyze((10, f'write({descriptor}, "x", 1) = 1'),
                     (10, f'fallocate({descriptor}, 0, 0, 2304) = 0'))
    assert result['clean'] and result['coverage']['complete']


def test_unix_annotation_and_both_socketpair_ends_supply_family():
    result = analyze((10, 'sendmsg(9<UNIX:[686391->686392]>, {msg_name=NULL, msg_namelen=0}, MSG_NOSIGNAL) = 8'),
                     (10, 'sendto(14<UNIX-STREAM:[687147]>, "C", 1, MSG_NOSIGNAL, NULL, 0) = 1'),
                     (10, 'socketpair(AF_UNIX, SOCK_STREAM, 0, [20<UNIX:[1->2]>, 21<UNIX:[2->1]>]) = 0'),
                     (10, 'sendto(20, "C", 1, 0, NULL, 0) = 1'),
                     (10, 'sendto(21, "C", 1, 0, NULL, 0) = 1'))
    assert result['clean']
    assert all(event['family'] == 'AF_UNIX' for event in result['network'])


def test_namespace_local_clone_return_never_creates_host_pid_or_inherits_state():
    result = analyze((10, 'clone(child_stack=NULL, flags=CLONE_NEWPID|SIGCHLD) = 20'),
                     (20, 'clone(child_stack=NULL, flags=SIGCHLD) = 2'),
                     (30, 'write(7, "unknown", 7) = 7'))
    assert {entry['pid'] for entry in result['processes']} == {10, 20, 30}
    assert not result['coverage']['complete']
    assert any('lineage' in entry['reason'] for entry in result['coverage']['gaps'])


def test_gap_aggregate_retains_total_after_example_cap():
    result = analyze(*[(10, 'unsupported_example(0) = 0')] * 1005)
    assert len(result['coverage']['gaps']) == 1000
    assert result['coverage']['gapCount'] == 1005
    assert result['coverage']['gapCounts'] == [{'call': 'unsupported_example', 'reason': 'Unsupported syscall in the declared evidence filter.', 'count': 1005}]


@pytest.mark.parametrize('descriptor', ['3<unknown:object>', '3<{eventfd-count=oops}>', '3</memfd:truncated...>(deleted)', '3</sources/path<char broken>>'])
def test_malformed_annotations_remain_unknown(descriptor):
    assert not analyze((10, f'write({descriptor}, "x", 1) = 1'))['coverage']['complete']


def test_child_before_clone_completion_keeps_lineage_unknown():
    result = analyze((20, 'write(7, "unknown", 7) = 7'),
                     (10, 'clone(child_stack=NULL, flags=SIGCHLD) = 20'))
    assert not result['coverage']['complete']
    assert any('before observed clone' in gap['reason'] for gap in result['coverage']['gaps'])


def test_unobserved_clone_return_is_not_a_process_and_remains_unknown():
    result = analyze((10, 'clone(child_stack=NULL, flags=SIGCHLD) = 2'))
    assert [row['pid'] for row in result['processes']] == [10]
    assert any('no observed host process' in gap['reason'] for gap in result['coverage']['gaps'])


def test_namespace_creation_does_not_attribute_local_id_to_existing_host_process():
    result = analyze((10, 'clone(child_stack=NULL, flags=CLONE_NEWPID|SIGCHLD) = 20'),
                     (20, 'clone(child_stack=NULL, flags=SIGCHLD) = 10'))
    assert next(row for row in result['processes'] if row['pid'] == 10)['parent'] is None
    assert not result['coverage']['complete']


def test_complete_input_aggregates_all_events_and_late_adverse_effects_after_sample_bounds(monkeypatch):
    monkeypatch.setattr(trace, 'MAX_EVENTS', 3)
    monkeypatch.setattr(trace, 'MAX_LINES', 4)
    monkeypatch.setattr(trace, 'MAX_EVENT_EXAMPLES', 2, raising=False)
    manifest = {'sourceRoot': '/evidence/sources', 'initialCwd': '/evidence/application',
                'appRoot': '/evidence/application', 'trustedExecutables': ['/trusted/main']}
    calls = ['execve("/trusted/main", ["main"], 0x0) = 0',
             'socket(AF_UNIX, SOCK_STREAM, 0) = 3<UNIX-STREAM:[1]>']
    calls += ['sendto(3<UNIX-STREAM:[1]>, "x", 1, 0, NULL, 0) = 1'] * 20
    calls += ['openat(AT_FDCWD, "/evidence/application/cache", O_WRONLY) = 4</evidence/application/cache>'] * 5
    calls += ['openat(AT_FDCWD, "/evidence/input.json", O_WRONLY) = 5</evidence/input.json>',
              'openat(AT_FDCWD, "/evidence/sources/record", O_WRONLY) = 6</evidence/sources/record>',
              'connect(7<TCP:[2]>, {sa_family=AF_INET, sin_port=htons(80), sin_addr=inet_addr("127.0.0.1")}, 16) = -1 ECONNREFUSED (Connection refused)',
              'sendto(8<unknown:socket>, "x", 1, 0, NULL, 0) = 1',
              'execve("/untrusted/late", ["late"], 0x0) = -1 ENOENT (No such file or directory)',
              '+++ exited with 0 +++']
    rows = [f'10 {1000+index/1000:.6f} {call}\n' for index, call in enumerate(calls)]
    legacy = trace.analyze_trace(iter(rows), manifest)
    assert not legacy['coverage']['complete']
    assert legacy['summary']['lines'] < len(rows)
    assert not legacy['eventRetention']['inputFullyConsumed']
    result = trace.analyze_trace(iter(rows), manifest, complete_input=True)
    assert result['summary']['lines'] == len(rows)
    assert result['eventRetention']['inputFullyConsumed']
    assert result['summary']['sourceMutationAttempts'] == 1
    assert result['summary']['successfulSourceMutations'] == 1
    assert result['summary']['evidenceMutationAttempts'] == 1
    assert result['summary']['ipActions'] == 1
    assert result['summary']['unknownNetworkActions'] == 1
    assert result['summary']['untrustedExecAttempts'] == 1
    assert not result['clean']
    assert result['eventRetention']['totals']['network'] == 23
    assert len(result['network']) == 2
    assert len(result['otherMutations']) == 2
    assert result['adverseExamples']['evidenceMutationAttempts'][0]['path'] == '/evidence/input.json'
    assert result['adverseExamples']['unknownNetworkActions'][0]['family'] is None
    assert result['adverseExamples']['ipActions'][0]['family'] == 'AF_INET'
    assert not any('evidence limit exceeded' in item['reason'] for item in result['coverage']['gapCounts'])


def test_complete_input_retains_exact_totals_when_adverse_examples_are_bounded(monkeypatch):
    monkeypatch.setattr(trace, 'MAX_EVENT_EXAMPLES', 2, raising=False)
    calls = ['execve("/trusted/main", ["main"], 0x0) = 0']
    calls += ['openat(AT_FDCWD, "/sources/record", O_WRONLY) = 3</sources/record>'] * 7
    calls += ['+++ exited with 0 +++']
    rows = [f'10 {1000+index/1000:.6f} {call}\n' for index, call in enumerate(calls)]
    result = trace.analyze_trace(iter(rows), MANIFEST, complete_input=True)
    assert result['summary']['successfulSourceMutations'] == 7
    assert result['eventRetention']['totals']['sourceMutations'] == 7
    assert len(result['sourceMutations']) == 2
    assert len(result['adverseExamples']['successfulSourceMutations']) == 2
    assert result['summary']['lines'] == len(rows)
    assert not result['clean']


def test_complete_input_empty_and_small_clean_traces_preserve_default_decisions():
    assert not trace.analyze_trace([], MANIFEST, complete_input=True)['clean']
    rows = ['10 1000.000000 execve("/trusted/main", ["main"], 0x0) = 0\n',
            '10 1000.001000 +++ exited with 0 +++\n']
    ordinary = trace.analyze_trace(iter(rows), MANIFEST)
    complete = trace.analyze_trace(iter(rows), MANIFEST, complete_input=True)
    assert ordinary['clean'] and complete['clean']
    assert complete['summary'] == ordinary['summary']
    assert complete['coverage'] == ordinary['coverage']
