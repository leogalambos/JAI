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
        for source in (".ai/runtime/tools/findings.py", ".ai/runtime/fabric/fabric.py"):
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

    def test_fabric_evidence_closes_binary_file_and_preserves_hash(self):
        self.run_isolated('''
            import builtins, hashlib, runpy, tempfile
            from pathlib import Path
            from unittest.mock import patch
            module = runpy.run_path(".ai/runtime/fabric/fabric.py")
            class EvidenceSink:
                def add_node(self, *args, **kwargs):
                    return kwargs
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "evidence.bin"
                payload = bytes(range(256))
                source.write_bytes(payload)
                real_open, handles = builtins.open, []
                def tracked_open(*args, **kwargs):
                    handle = real_open(*args, **kwargs)
                    handles.append(handle)
                    return handle
                with patch("builtins.open", tracked_open):
                    result = module["make_evidence"](EvidenceSink(), 6, "fixture", "deterministic", str(source))
                assert result["sha256"] == hashlib.sha256(payload).hexdigest()
                assert result["size"] == len(payload)
                assert handles and all(h.closed for h in handles), "binary input remains open"
                handles.clear()
                with patch("builtins.open", tracked_open), patch("os.path.getsize", side_effect=OSError("fixture failure")):
                    try:
                        module["make_evidence"](EvidenceSink(), 6, "fixture", "deterministic", str(source))
                    except OSError:
                        pass
                    else:
                        raise AssertionError("size lookup failure was swallowed")
                assert handles and all(h.closed for h in handles), "failed evidence remains open"
                try:
                    module["make_evidence"](EvidenceSink(), 6, "fixture", "deterministic", str(source) + "-missing")
                except module["FabricError"]:
                    pass
                else:
                    raise AssertionError("missing evidence was accepted")
        ''')
