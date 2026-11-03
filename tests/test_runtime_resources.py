# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise runtime file ownership in isolated interpreters and temporary fixtures."""
from pathlib import Path
import subprocess
import sys
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RuntimeResourceTests(unittest.TestCase):
    def run_isolated(self, program, *arguments):
        """Run a fixture without changing the parent interpreter's streams or globals."""
        result = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(program), *map(str, arguments)],
            cwd=ROOT, text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_selftests_close_files_without_resource_warnings(self):
        for source in (".ai/runtime/tools/findings.py",):
            with self.subTest(source=source):
                self.run_isolated('''
                    import gc, runpy, sys, warnings
                    source = sys.argv[1]
                    sys.argv = [source, "selftest"]
                    with warnings.catch_warnings(record=True) as observed:
                        warnings.simplefilter("always", ResourceWarning)
                        try:
                            runpy.run_path(source, run_name="__main__")
                        except SystemExit as exc:
                            assert exc.code in (None, 0), exc.code
                        gc.collect()
                    leaked = [str(w.message) for w in observed
                              if issubclass(w.category, ResourceWarning)]
                    assert not leaked, "\\n".join(leaked)
                ''', source)

    def test_findings_input_closes_real_files_on_success_and_parse_failure(self):
        self.run_isolated('''
            import argparse, builtins, contextlib, io, json, runpy, tempfile
            from pathlib import Path
            from unittest.mock import patch
            module = runpy.run_path(".ai/runtime/tools/findings.py")
            command = module["cmd_add"]
            with tempfile.TemporaryDirectory() as directory:
                command.__globals__["HOME"] = directory
                source = Path(directory) / "review.json"
                real_open, handles = builtins.open, []
                def tracked_open(*args, **kwargs):
                    handle = real_open(*args, **kwargs)
                    handles.append(handle)
                    return handle
                for payload, succeeds in (("not JSON", False),
                    (json.dumps({"reviewer": "reviewer", "criteria": "criteria", "findings": []}), True)):
                    source.write_text(payload, encoding="utf-8")
                    handles.clear()
                    with patch("builtins.open", tracked_open), contextlib.redirect_stdout(io.StringIO()):
                        try:
                            command(argparse.Namespace(ledger="fixture", file=str(source)))
                        except json.JSONDecodeError:
                            assert not succeeds
                        else:
                            assert succeeds
                    assert handles and all(h.closed for h in handles), "input remains open"
                source.write_bytes(b"\\xff")
                handles.clear()
                with patch("builtins.open", tracked_open):
                    try:
                        command(argparse.Namespace(ledger="fixture", file=str(source)))
                    except UnicodeDecodeError:
                        pass
                    else:
                        raise AssertionError("invalid UTF-8 was accepted")
                assert handles and all(h.closed for h in handles), "failed read remains open"
                stream = io.StringIO(json.dumps({"reviewer": "r", "criteria": "c", "findings": []}))
                with patch("sys.stdin", stream), contextlib.redirect_stdout(io.StringIO()):
                    command(argparse.Namespace(ledger="fixture", file="-"))
                assert not stream.closed, "borrowed stdin was closed"
        ''')

    def test_current_cas_read_closes_binary_file_and_preserves_hash(self):
        self.run_isolated('''
            import errno, hashlib, os, sys, tempfile
            from pathlib import Path
            from unittest.mock import patch
            sys.path.insert(0, str(Path(".ai/runtime/tools").resolve()))
            import lifecycle as lc
            with tempfile.TemporaryDirectory() as directory:
                store = lc.Store(Path(directory) / "journal.jsonl", "resources")
                payload = bytes(range(256))
                identifier = store.put_blob(payload)
                real_fdopen, real_fstat, handles, descriptors = os.fdopen, os.fstat, [], []
                def tracked_fdopen(*args, **kwargs):
                    descriptors.append(args[0])
                    handle = real_fdopen(*args, **kwargs)
                    handles.append(handle)
                    return handle
                with patch("os.fdopen", tracked_fdopen):
                    result = store._blob(identifier)
                assert result == payload
                assert hashlib.sha256(result).digest() == hashlib.sha256(payload).digest()
                assert lc.blob(result) == identifier
                assert handles and all(handle.closed for handle in handles)
                for descriptor in descriptors:
                    try:
                        real_fstat(descriptor)
                    except OSError as exc:
                        assert exc.errno == errno.EBADF
                    else:
                        raise AssertionError("successful CAS descriptor remains open")
                descriptors.clear()
                def failed_metadata(descriptor):
                    descriptors.append(descriptor)
                    raise OSError("fixture metadata failure")
                with patch("os.fstat", failed_metadata):
                    try:
                        store._blob(identifier)
                    except OSError:
                        pass
                    else:
                        raise AssertionError("metadata failure was swallowed")
                assert descriptors
                for descriptor in descriptors:
                    try:
                        real_fstat(descriptor)
                    except OSError as exc:
                        assert exc.errno == errno.EBADF
                    else:
                        raise AssertionError("failed CAS descriptor remains open")
                (store.material / identifier).write_bytes(b"tampered")
                try:
                    store._blob(identifier)
                except lc.ERROR as exc:
                    assert exc.code == "P_INTEGRITY"
                else:
                    raise AssertionError("corrupted CAS material was accepted")
        ''')

    def test_current_fabric_validate_closes_files_without_resource_warnings(self):
        self.run_isolated('''
            import contextlib, gc, io, json, runpy, sys, tempfile, warnings
            from pathlib import Path
            sys.path.insert(0, str(Path("tests").resolve()))
            from governed_fixtures import GovernedHarness
            from unittest.mock import patch
            class Environment:
                def setenv(self, name, value):
                    import os
                    os.environ[name] = str(value)
            with tempfile.TemporaryDirectory() as directory:
                host = GovernedHarness(Path(directory), Environment())
                message = host.bootstrap_message()
                path = Path(directory) / "message.json"
                path.write_text(json.dumps(message))
                module = runpy.run_path(".ai/runtime/fabric/fabric.py")
                output = io.StringIO()
                with warnings.catch_warnings(record=True) as observed, contextlib.redirect_stdout(output):
                    warnings.simplefilter("always", ResourceWarning)
                    assert module["main"](["validate", "--message", str(path)]) == 0
                    gc.collect()
                report = json.loads(output.getvalue())
                assert report["structurally_valid"] and not report["authority_granted"]
                assert report["message_id"] == message["message_id"]
                assert not [warning for warning in observed if issubclass(warning.category, ResourceWarning)]
        ''')
