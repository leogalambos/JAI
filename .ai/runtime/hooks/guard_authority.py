#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""PreToolUse hook: authority stays with a person, and the records are written only by their tools.

Authority acts get "ask": Claude Code shows you the decision and you approve or deny it.
  * fabric.py authorise                 a decision on a layered engagement
  * fabric.py review ... --layer 0      accepting a product
  * findings.py accept-risk             accepting a review finding as a risk instead of fixing it
  * approve_change.py                   approving a change to the role library itself
In non-interactive permission modes (auto, dontAsk, bypassPermissions) nobody would see the prompt,
and "ask" is reported to degrade to "allow" there, so the hook denies instead: it fails closed.

Records get "deny" when touched other than through their tool:
  * the fabric logs (.fabric/) and findings ledgers (.findings/)
  * the signing key (~/.config/justifiable-fabric/)

This is a string-level guard: it makes the ordinary path safe and any bypass deliberate. It is not a
sandbox against a determined adversary with a shell.

Protocol: tool-call JSON on stdin; a JSON decision on stdout; exit 0.
"""
import json
import os
import re
import sys
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

AUTHORITY = [
    (re.compile(r"fabric\.py['\"]?\s+authorise\b"), "an authority decision on a layered engagement"),
    (re.compile(r"fabric\.py['\"]?\s+review\b[^|;&]*--layer[ =]0\b"), "accepting a product as its authority"),
    (re.compile(r"findings\.py['\"]?\s+accept-risk\b"), "accepting a review finding as a risk instead of fixing it"),
    (re.compile(r"approve_change\.py\b(?![^|;&]*--revoke)"), "approving a change to the role library itself"),
]
NONINTERACTIVE = {"auto", "dontAsk", "bypassPermissions", "acceptEdits", "plan"}
RECORDS = re.compile(r"(^|[\s/\\'\"=])\.(fabric|findings)[/\\]")
WRITES = re.compile(r"(>>?|\btee\b|\bsed\s+-i|\bmv\b|\bcp\b|\brm\b|\btruncate\b|\bdd\b|\bln\b)")
TOOLS = re.compile(r"\b(fabric|findings)\.py\b")
KEY = "justifiable-fabric"


def decide(decision, reason, payload=None):
    # Claude Code supports permissionDecision="ask". Codex PreToolUse intentionally does not;
    # for authority acts Codex therefore fails closed and asks the human to run the command manually.
    provider = "claude"
    if "--provider" in sys.argv:
        try:
            provider = sys.argv[sys.argv.index("--provider") + 1].lower()
        except (IndexError, ValueError):
            provider = "claude"
    elif os.environ.get("CODEX_HOME"):
        provider = "codex"
    if provider == "codex" and decision == "ask":
        decision = "deny"
        reason += "\nCodex cannot elevate a PreToolUse hook to an approval prompt; run this authority command manually."
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))
    return 0


def main():
    try:
        p = json.load(sys.stdin)
    except ValueError:
        return 0
    tool = p.get("tool_name", "")
    ti = p.get("tool_input") or {}
    mode = p.get("permission_mode", "default")

    if tool in ("Bash", "PowerShell", "shell", "shell_command", "exec_command", "apply_patch"):             # Claude Code on Windows falls back to PowerShell
        cmd = ti.get("command", "")
        if KEY in cmd:
            return decide("deny", "The signing key is read only by fabric.py itself.", p)
        for rx, what in AUTHORITY:
            if rx.search(cmd):
                if mode in NONINTERACTIVE:
                    return decide("deny",
                        f"This is {what}, and the session's permission mode is '{mode}', so nobody would see "
                        "an approval prompt. Authority acts are refused here. Show the operator the decision "
                        f"and the command, and let them run it or switch to the default mode:\n  {cmd}", p)
                return decide("ask",
                    f"AUTHORITY ACT: {what}.\n\n{cmd}\n\nApprove only if this is your own decision. "
                    "An agent's recommendation is not authority; the record will say you approved it.", p)
        if RECORDS.search(cmd) and WRITES.search(cmd) and not TOOLS.search(cmd):
            return decide("deny", "Fabric logs and findings ledgers are append-only and hash-chained; "
                                  "write them only through fabric.py or findings.py.", p)
        return 0

    path = (ti.get("file_path") or ti.get("path") or ti.get("notebook_path") or "").replace("\\", "/")
    if tool == "Read" and KEY in path:
        return decide("deny", "The signing key is read only by fabric.py itself.", p)
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        if KEY in path:
            return decide("deny", "The signing key is managed by fabric.py.", p)
        if "/.fabric/" in path or path.startswith(".fabric/") or "/.findings/" in path or path.startswith(".findings/"):
            return decide("deny", f"{path} is an append-only, hash-chained record; write it only through "
                                  "fabric.py or findings.py.", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
