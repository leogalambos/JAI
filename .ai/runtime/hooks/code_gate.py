#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Hook: code Claude writes is documented and tested, and its tests are run and pass.

PostToolUse on Write, Edit, MultiEdit — checks what Claude just wrote against the documentation standard
    (doc_check.py) and the testing standard (test_check.py): a whole file for Write; for an edit, only the
    declarations it touched. Problems go straight back to Claude (exit 2). Unfixed errors are remembered.
PostToolUse / PostToolUseFailure on Bash — notices test runs (mvn, gradle, pytest, npm test, jest, vitest,
    go test, dotnet test, cargo test, tox …) and records whether they failed.
Stop, SubagentStop — Claude, or a subagent such as role-engineer, cannot finish while code it wrote is
    undocumented or untested, while the tests have not been run since its last change to production code, or while
    the last run failed. A second attempt (stop_hook_active) is allowed and the user is told what remains, so a
    problem Claude cannot solve never traps the session.

Off for one project: .ai/no-doc-check (documentation) and .ai/no-test-check (tests).
Standards: ~/.ai/it-role-house/standards/code-documentation.md and testing.md.
"""
import json
import os
import re
import sys
import tempfile

for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True        # no __pycache__ inside an installed library: nothing left behind on uninstall
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import doc_check   # noqa: E402  (the checkers live beside this hook, in the library's tools folder)
import test_check  # noqa: E402

STANDARDS = "~/.ai/it-role-house/standards/"
STATE_DIR = os.path.join(tempfile.gettempdir(), "ai-it-house-gate")
TEST_RUN = re.compile(r"\b(mvnw?|mvn\.cmd)\b[^|;&]*\b(test|verify|install|package)\b|\bgradlew?(\.bat)?\b[^|;&]*"
                      r"\b(test|check|build|integrationTest)\b|\bpytest\b|\bpython3?\s+-m\s+(pytest|unittest)\b|"
                      r"\b(npm|pnpm|yarn)\s+(run\s+)?test\b|\b(jest|vitest)\b|\bgo\s+test\b|\bdotnet\s+test\b|"
                      r"\bcargo\s+test\b|\b(tox|nox)\b|\bmake\s+(test|check)\b")
SKIPS_TESTS = re.compile(r"-DskipTests|-Dmaven\.test\.skip|-x\s+test\b|--exclude-task\s+test")
FAILED = re.compile(r"BUILD FAILURE|BUILD FAILED|Tests run:.*(Failures|Errors): [1-9]|\b[1-9]\d* (failed|errors?)\b|"
                    r"^FAILED\b|^FAIL\b|Failed!|test result: FAILED|Tests:.*\b[1-9]\d* failed|There were test failures",
                    re.M)


def opted_out(path, marker):
    """True if the project holding path contains a common or provider-specific opt-out marker."""
    d = os.path.dirname(os.path.abspath(path)) if not os.path.isdir(path) else os.path.abspath(path)
    while True:
        for dot in (".ai", ".claude", ".codex"):
            if os.path.isfile(os.path.join(d, dot, marker)):
                return True
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def state_path(session):
    """The file holding this session's remembered problems and test runs."""
    return os.path.join(STATE_DIR, re.sub(r"[^\w-]", "_", session or "default") + ".json")


def load_state(session):
    """This session's state: unfixed doc and test errors per file, changed projects, test runs, a counter."""
    try:
        s = json.load(open(state_path(session), encoding="utf-8"))
    except (OSError, ValueError):
        s = {}
    for k, empty in (("doc", {}), ("test", {}), ("changed", {}), ("runs", {}), ("seq", 0)):
        s.setdefault(k, empty)
    return s


def save_state(session, s):
    """Persist the state, dropping files with nothing outstanding; remove it when nothing is left."""
    os.makedirs(STATE_DIR, exist_ok=True)
    s["doc"] = {p: k for p, k in s.get("doc", {}).items() if k}
    s["test"] = {p: k for p, k in s.get("test", {}).items() if k}
    if s["doc"] or s["test"] or s.get("changed"):
        json.dump(s, open(state_path(session), "w", encoding="utf-8"))
    elif os.path.exists(state_path(session)):
        os.remove(state_path(session))



def patch_paths(command, cwd):
    """Extract target files from an apply_patch patch body used by Codex hooks."""
    out = []
    for line in (command or "").splitlines():
        m = re.match(r"\*\*\* (?:Update|Add|Delete) File: (.+)$", line.strip())
        if m:
            p = m.group(1).strip()
            if not os.path.isabs(p):
                p = os.path.join(cwd or os.getcwd(), p)
            out.append(os.path.realpath(p))
    return out

def edited_ranges(path, tool, ti):
    """Line ranges Claude just wrote: None means the whole file (Write)."""
    if tool in ("Write", "apply_patch"):
        return None
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    news = [e.get("new_string", "") for e in ti.get("edits", [])] if tool == "MultiEdit" else [ti.get("new_string", "")]
    ranges = []
    for new in news:
        if not new.strip():
            continue
        start = 0
        while True:
            i = text.find(new, start)
            if i < 0:
                break
            first = text.count("\n", 0, i) + 1
            ranges.append((first, first + new.count("\n")))
            if not (ti.get("replace_all") or tool == "MultiEdit"):
                break
            start = i + max(len(new), 1)
    return ranges


def describe(path, found):
    """A report Claude can act on: must-fix errors, then judgement calls."""
    lines = [f"Code standards ({STANDARDS}code-documentation.md, testing.md) — {path}:"]
    for f in found[:15]:
        lines.append(f"  {'must fix' if f['severity'] == 'error' else 'consider'}  line {f['line']}  {f['message']}")
    if len(found) > 15:
        lines.append(f"  … and {len(found) - 15} more")
    if any(f["severity"] == "error" for f in found):
        lines.append("Fix the 'must fix' items as part of this change — document the contract, write the unit tests "
                     "(normal case, boundary, failure path) and integration tests the standard requires, then run "
                     "the tests. You cannot finish while they remain.")
    return "\n".join(lines)


def remember(bucket, path, found, recheck):
    """Record new error keys for path, and forget recorded ones the whole-file recheck no longer reports."""
    still = {f["key"] for f in recheck if f["severity"] == "error"}
    bucket[path] = [k for k in bucket.get(path, []) if k in still]
    for f in found:
        if f["severity"] == "error" and f["key"] not in bucket[path]:
            bucket[path].append(f["key"])


def on_write(p, s):
    """PostToolUse on a file write: check documentation and tests of what was written."""
    s["stop_attempts"] = 0
    ti = p.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path") or ""
    if not path or not doc_check.LANG.get(os.path.splitext(path)[1].lower()) or not os.path.isfile(path):
        return 0
    ranges = edited_ranges(path, p.get("tool_name", ""), ti)
    found = []
    if not doc_check.excluded(path) and not opted_out(path, "no-doc-check"):
        doc = doc_check.check_file(path, ranges)
        remember(s["doc"], path, doc, doc_check.check_file(path))
        found += doc
    root = test_check.project_root(path)
    if root and not opted_out(path, "no-test-check"):
        if test_check.is_test_path(path):
            found += test_check.check_test_file(path)
            for prod in [q for q in s["test"] if test_check.project_root(q) == root]:
                remember(s["test"], prod, [], test_check.check_production(prod))     # a new test may fix them
        elif not test_check.generated(path) and "experiments" not in re.split(r"[\\/]", path):
            s["seq"] += 1
            s["changed"][root] = s["seq"]
            tests = test_check.check_production(path, ranges)
            remember(s["test"], path, tests, test_check.check_production(path))
            found += tests
    if found:
        print(describe(path, found), file=sys.stderr)
        return 2                                   # PostToolUse: the file is written; Claude sees the message
    return 0


def on_command(p, s, failed_event):
    """PostToolUse / PostToolUseFailure on Bash: record a test run and whether it failed."""
    # A new test attempt invalidates the previous stop escape hatch.
    s["stop_attempts"] = 0
    cmd = (p.get("tool_input") or {}).get("command", "")
    if not TEST_RUN.search(cmd) or SKIPS_TESTS.search(cmd) or not s["changed"]:
        return 0
    resp = p.get("tool_response")
    text = json.dumps(resp) if isinstance(resp, (dict, list)) else str(resp or "")
    text = text.replace("\\n", "\n")
    code = resp.get("exit_code", resp.get("exitCode", resp.get("returncode"))) if isinstance(resp, dict) else None
    failed = failed_event or bool(FAILED.search(text)) or (isinstance(code, int) and code != 0)
    s["seq"] += 1
    here = test_check.project_root(p.get("cwd") or os.getcwd())
    for root in ([here] if here in s["changed"] else list(s["changed"])):
        s["runs"][root] = {"seq": s["seq"], "failed": failed}
    return 0


def on_stop(p, s, session):
    """Stop / SubagentStop: refuse to finish while code written this session is undocumented, untested or untested-run."""
    problems = []
    for path, keys in s["doc"].items():
        if os.path.isfile(path) and not opted_out(path, "no-doc-check"):
            problems += [f"{path}:{f['line']}  {f['message']}" for f in doc_check.check_file(path)
                         if f["severity"] == "error" and f["key"] in keys][:10]
    for path, keys in s["test"].items():
        if os.path.isfile(path) and not opted_out(path, "no-test-check"):
            problems += [f"{path}:{f['line']}  {f['message']}" for f in test_check.check_production(path)
                         if f["severity"] == "error" and f["key"] in keys][:10]
    for root, changed in s["changed"].items():
        if opted_out(root, "no-test-check"):
            continue
        run = s["runs"].get(root)
        if not run or run["seq"] < changed:
            problems.append(f"{root}: production code changed and the tests have not been run since — run them "
                            "(e.g. mvn -q verify, gradle test, pytest, npm test, go test ./...)")
        elif run["failed"]:
            problems.append(f"{root}: the last test run failed — fix the code or the tests (never disable or weaken a "
                            "test to make it pass), then run them again")
    if not problems:
        save_state(session, {"seq": s["seq"]})
        return 0
    text = "\n".join("  " + x for x in problems)
    attempts = int(s.get("stop_attempts", 0))
    if p.get("stop_hook_active") or attempts >= 1:   # Claude flag or second Codex stop attempt
        save_state(session, {"seq": s["seq"]})
        print(json.dumps({"systemMessage": "Code written this session does not yet meet the documentation and testing "
                                           f"standards ({STANDARDS}):\n" + text}))
        return 0
    s["stop_attempts"] = attempts + 1
    save_state(session, s)
    print("Before finishing — code written in this session does not yet meet the documentation and testing standards "
          f"({STANDARDS}):\n" + text + "\nFix these, run the tests, then finish.", file=sys.stderr)
    return 2                                       # Stop / SubagentStop: Claude continues and fixes it


def main():
    try:
        p = json.load(sys.stdin)
    except ValueError:
        return 0
    session = p.get("session_id", "")
    s = load_state(session)
    event, tool = p.get("hook_event_name", ""), p.get("tool_name", "")
    if event == "PostToolUse" and tool == "apply_patch":
        rc = 0
        for path in patch_paths((p.get("tool_input") or {}).get("command", ""), p.get("cwd") or os.getcwd()):
            q = dict(p)
            q["tool_name"] = "apply_patch"
            q["tool_input"] = {"file_path": path}
            rc = max(rc, on_write(q, s))
    elif event == "PostToolUse" and tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        rc = on_write(p, s)
    elif event in ("PostToolUse", "PostToolUseFailure") and tool in ("Bash", "PowerShell", "shell", "shell_command", "exec_command"):
        rc = on_command(p, s, event == "PostToolUseFailure")
    elif event in ("Stop", "SubagentStop"):
        return on_stop(p, s, session)
    else:
        return 0
    save_state(session, s)
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                        # never trap the session, never fail silently
        print(f"code_gate: internal error, standards not checked this time: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        sys.exit(1)                                # non-blocking: Claude Code shows the user a hook error notice
