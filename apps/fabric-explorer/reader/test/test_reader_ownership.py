# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""The viewer owns its filesystem adapters without installing them into canonical tools."""
from pathlib import Path
import importlib.util
import pytest

READER = Path(__file__).resolve().parents[1]


def test_native_snapshot_primitive_is_app_owned_and_reads_exact_bytes(tmp_path):
    path = READER / 'readonly_files.py'
    assert path.is_file(), 'Filesystem reader must belong to the viewer package'
    spec = importlib.util.spec_from_file_location('readonly_files', path)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    source = tmp_path / 'input'; source.write_bytes(b'bounded snapshot')
    with module.ReadOnlyRoot(tmp_path) as root:
        with root.capture('input', maximum=16) as captured:
            assert captured.read_all() == b'bounded snapshot'


def test_windows_snapshot_primitive_is_shipped_with_viewer():
    assert (READER / 'windows_readonly.py').is_file()


@pytest.mark.parametrize('family', ['findings', 'fabric'])
def test_isolated_semantic_bootstrap_never_imports_canonical_runtime(tmp_path, family):
    import json
    import subprocess
    import sys
    source = tmp_path / 'source'; source.mkdir()
    app = tmp_path / 'app'; app.mkdir()
    compatibility = tmp_path / 'compatibility'; compatibility.mkdir()
    if family == 'findings':
        fixture = READER.parent / 'test/fixtures/findings-review.jsonl'
        journal = source / 'review.jsonl'; journal.write_bytes(fixture.read_bytes())
    else:
        generated = subprocess.run([sys.executable, '-I', '-B', str(READER / 'test/make_fabric_fixture.py'), str(source)], capture_output=True, text=True, check=True, timeout=15)
        journal = source / json.loads(generated.stdout)['filename']
    before = journal.read_bytes()
    program = """
import sys
from pathlib import Path
script, compatibility = sys.argv[1:]
sys.path.insert(0, str(Path(script).parent))
def deny(event, args):
    if event == 'import' and args[0] in {'lifecycle', 'findings', 'operator_actions', 'governed_semantic'}:
        raise AssertionError('Canonical runtime import denied by viewer boundary test')
sys.addaudithook(deny)
import raw_reader
sys.argv = [script, compatibility]
code = raw_reader.main()
assert compatibility not in sys.path
raise SystemExit(code)
"""
    child = subprocess.Popen([sys.executable, '-I', '-B', '-c', program, str(READER / 'raw_reader.py'), str(compatibility)], cwd=app, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    def call(index, operation, args):
        child.stdin.write(json.dumps({'id': index, 'operation': operation, 'args': args}) + '\n'); child.stdin.flush()
        line = child.stdout.readline()
        assert line, child.stderr.read()
        return json.loads(line)
    try:
        assert call(1, 'configure', {'writeRoots': [str(app)]})['ok']
        opened = call(2, 'admit', {'selections': [{'projectPath': str(source), 'path': str(journal), 'family': family}]})['result']
        result = call(3, 'semantic.begin', {'group': opened['token'], 'sources': [{'token': opened['sources'][0]['token'], 'sourceId': 'synthetic-findings'}], 'limits': {'maxVertices': 100000, 'maxEdges': 500000, 'maxEncodedGraphBytes': 512 * 1024 * 1024}})
        assert result['ok']
        assert result['result']['sources'][0]['verification']['mode'] == 'recorded'
        child.stdin.close(); assert child.wait(timeout=10) == 0
        assert journal.read_bytes() == before
    finally:
        if child.poll() is None: child.kill(); child.wait()
