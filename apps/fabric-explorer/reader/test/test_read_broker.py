# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Real retained-root broker admission and fixed-helper byte transport integration."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / 'apps/fabric-explorer/reader'))
from readonly_files import ReadOnlyRoot
spec = importlib.util.spec_from_file_location('explorer_raw_reader', REPO / 'apps/fabric-explorer/reader/raw_reader.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


@pytest.fixture
def inputs(tmp_path):
    project = tmp_path / 'project'; project.mkdir()
    external = tmp_path / 'external'; external.mkdir()
    app = tmp_path / 'app'; app.mkdir()
    source = external / 'engagement.jsonl'; source.write_bytes(b'first\nsecond\n')
    selection = {'projectPath': str(project), 'path': str(source), 'family': 'fabric'}
    reader = module.Reader(ReadOnlyRoot, [app])
    yield reader, selection, source, app
    reader.close()


def test_external_explicit_source_exact_pages_append_and_release(inputs):
    reader, selection, source, app = inputs
    before = source.read_bytes()
    admitted = reader.admit([selection]); descriptor = admitted['sources'][0]
    result = reader.page(admitted['token'], descriptor['token'], '2', 4)
    assert base64.b64decode(result['bytesBase64']) == before[2:6]
    assert result == {'bytesBase64': base64.b64encode(before[2:6]).decode(), 'byteLength': 4, 'eof': False}
    with source.open('ab') as stream: stream.write(b'new\n')
    page = reader.page(admitted['token'], descriptor['token'], str(len(before)), 256)
    assert base64.b64decode(page['bytesBase64']) == b'new\n' and page['eof']
    assert source.read_bytes() == before + b'new\n' and list(app.iterdir()) == []
    reader.release(admitted['token']); reader.release(admitted['token'])
    with pytest.raises(KeyError): reader.page(admitted['token'], descriptor['token'], '0', 4)


def test_replaced_leaf_denied_without_bytes(inputs):
    reader, selection, source, _ = inputs
    admitted = reader.admit([selection]); token = admitted['sources'][0]['token']
    alternate = source.with_name('other'); alternate.write_bytes(b'hostile')
    alternate.replace(source)
    with pytest.raises(ValueError, match='identity'): reader.page(admitted['token'], token, '0', 7)


def test_replaced_root_denied(inputs):
    reader, selection, source, _ = inputs
    admitted = reader.admit([selection]); parent = source.parent
    if os.name == 'nt':
        before = source.read_bytes()
        with pytest.raises(OSError) as rejected:
            parent.rename(parent.with_name('old'))
        # Windows refuses moving the retained native directory itself. Both
        # documented native rename refusal statuses are explicit, not a skip
        # or acceptance of arbitrary filesystem errors.
        assert rejected.value.winerror in {5, 32}
        assert source.read_bytes() == before
        page = reader.page(admitted['token'], admitted['sources'][0]['token'], '0', len(before))
        assert base64.b64decode(page['bytesBase64']) == before
        assert not parent.with_name('old').exists()
        reader.release(admitted['token'])
        parent.rename(parent.with_name('old'))
        assert (parent.with_name('old') / source.name).read_bytes() == before
        return
    parent.rename(parent.with_name('old')); parent.mkdir(); source.write_bytes(b'hostile')
    with pytest.raises(ValueError, match='root'): reader.page(admitted['token'], admitted['sources'][0]['token'], '0', 7)


def test_symlink_hardlink_traversal_and_wrong_family_denied(inputs):
    reader, selection, source, _ = inputs
    linked = source.with_name('link.jsonl'); linked.symlink_to(source)
    with pytest.raises((ValueError, OSError)): reader.admit([{**selection, 'path': str(linked)}])
    os.link(source, source.with_name('alias.jsonl'))
    with pytest.raises(ValueError): reader.admit([selection])
    with pytest.raises(ValueError): reader.admit([{**selection, 'path': str(source.parent / '..' / source.parent.name / source.name)}])
    with pytest.raises(ValueError): reader.admit([{**selection, 'family': 'audit'}])
    assert not reader.groups


@pytest.mark.parametrize('direction', ['same', 'source-parent', 'write-parent'])
def test_overlap_denied_in_both_directions(tmp_path, direction):
    top = tmp_path / 'top'; top.mkdir(); child = top / 'child'; child.mkdir()
    source_root, write_root = {'same': (top, top), 'source-parent': (top, child), 'write-parent': (child, top)}[direction]
    source = source_root / 'journal.jsonl'; source.write_bytes(b'unchanged')
    reader = module.Reader(ReadOnlyRoot, [write_root])
    try:
        with pytest.raises(ValueError, match='overlap'):
            reader.admit([{'projectPath': str(top), 'path': str(source), 'family': 'findings'}])
        assert source.read_bytes() == b'unchanged' and not reader.groups
    finally: reader.close()


def test_write_root_replacement_revalidated_before_read(inputs):
    reader, selection, _, app = inputs
    admitted = reader.admit([selection])
    if os.name == 'nt':
        with pytest.raises(OSError) as rejected:
            app.rename(app.with_name('oldapp'))
        assert rejected.value.winerror in {5, 32}
        before = Path(selection['path']).read_bytes()
        page = reader.page(admitted['token'], admitted['sources'][0]['token'], '0', len(before))
        assert base64.b64decode(page['bytesBase64']) == before
        assert app.exists() and not app.with_name('oldapp').exists()
        reader.close()
        app.rename(app.with_name('oldapp'))
        assert app.with_name('oldapp').is_dir()
        return
    app.rename(app.with_name('oldapp')); app.mkdir()
    with pytest.raises(ValueError, match='root'): reader.page(admitted['token'], admitted['sources'][0]['token'], '0', 4)


@pytest.mark.parametrize('offset,length', [('01', 4), ('-1', 4), ('0', 0), ('0', 262145), ('0', True), ('9'*21, 4)])
def test_page_bounds_denied(inputs, offset, length):
    reader, selection, _, _ = inputs; admitted = reader.admit([selection])
    with pytest.raises(ValueError): reader.page(admitted['token'], admitted['sources'][0]['token'], offset, length)


def test_fixed_helper_process_protocol_and_eof_cleanup(inputs, tmp_path):
    _, selection, source, app = inputs
    before = source.read_bytes()
    process = subprocess.Popen([sys.executable, '-I', '-B', str(REPO / 'apps/fabric-explorer/reader/raw_reader.py'), str(REPO / '.ai/runtime/tools')],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=app,
                               env={'LANG': 'C.UTF-8'}, text=True)
    def request(number, operation, args):
        process.stdin.write(json.dumps({'id': number, 'operation': operation, 'args': args}) + '\n'); process.stdin.flush()
        response = json.loads(process.stdout.readline()); assert response['id'] == number
        return response
    try:
        assert request(1, 'configure', {'writeRoots': [str(app)]})['ok']
        admitted = request(2, 'admit', {'selections': [selection]})['result']
        page = request(3, 'page', {'group': admitted['token'], 'token': admitted['sources'][0]['token'], 'offset': '0', 'length': 20})
        assert base64.b64decode(page['result']['bytesBase64']) == before
        assert not request(4, 'write', {'path': str(source), 'bytes': 'forbidden'})['ok']
        process.stdin.close(); assert process.wait(timeout=10) == 0
        assert source.read_bytes() == before and list(app.iterdir()) == []
    finally:
        if process.poll() is None: process.kill(); process.wait()


def test_duplicate_fields_and_oversized_frame_fail_closed(inputs):
    _, _, _, app = inputs
    command = [sys.executable, '-I', '-B', str(REPO / 'apps/fabric-explorer/reader/raw_reader.py'), str(REPO / '.ai/runtime/tools')]
    completed = subprocess.run(command, input=b'{"id":1,"id":2,"operation":"configure","args":{}}\n', capture_output=True, cwd=app, env={'LANG': 'C.UTF-8'})
    assert completed.returncode == 0 and not json.loads(completed.stdout)['ok']
    completed = subprocess.run(command, input=b'x' * (module.FRAME + 1), capture_output=True, cwd=app, env={'LANG': 'C.UTF-8'})
    assert completed.returncode == 2 and completed.stdout == b''


def test_structured_and_aggregate_limits_are_independent_sparse_bounds(inputs):
    reader, selection, source, _ = inputs
    audit = source.with_suffix('.json')
    with audit.open('wb') as stream: stream.truncate(100 * 1024 * 1024 + 1)
    with pytest.raises(ValueError): reader.admit([{**selection, 'path': str(audit), 'family': 'audit'}])
    # A large journal is a finite stream rather than one structured JSON file.
    with source.open('wb') as stream: stream.truncate(600 * 1024 * 1024)
    admitted = reader.admit([selection])
    assert reader.page(admitted['token'], admitted['sources'][0]['token'], '0', 4)['byteLength'] == 4
    second = source.with_name('second.jsonl')
    with second.open('wb') as stream: stream.truncate(600 * 1024 * 1024)
    with pytest.raises(ValueError, match='aggregate'):
        reader.admit([selection, {**selection, 'path': str(second)}])
    with source.open('ab') as stream: stream.truncate(module.TOTAL + 1)
    with pytest.raises(ValueError): reader.page(admitted['token'], admitted['sources'][0]['token'], '0', 4)


def test_native_namespace_identity_transport_preserves_integers_above_53_bits(inputs):
    _, selection, _, app = inputs
    assigned = {}
    class LargeIdentityRoot(ReadOnlyRoot):
        def __init__(self, path):
            super().__init__(path)
            key = str(path)
            assigned.setdefault(key, 9007199254740992 + len(assigned))
            self.identity = ('posix', 9007199254740993, assigned[key])
        def observe_ancestry(self):
            return (*super().observe_ancestry()[:-1], self.identity)
    reader = module.Reader(LargeIdentityRoot, [app])
    try:
        descriptor = reader.admit([selection])['sources'][0]
        transported = json.loads(json.dumps(descriptor))
        assert transported['project'] == ['posix', '9007199254740993', str(assigned[selection['projectPath']])]
        assert transported['root'] == ['posix', '9007199254740993', str(assigned[str(Path(selection['path']).parent)])]
        assert transported['project'] != transported['root']
        assert 'identity' not in transported
    finally: reader.close()
