#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""PreToolUse hook: the library is immutable unless a change has been approved.

Agent frontmatter restricts tool *types*, not *targets*. An agent holding Write can write
anywhere, so "staging only" in a prompt is an instruction, not a control. This hook is the
control: it reads the tool call before it runs and refuses writes into the live library
unless a current approval record covers them.

Install via settings.json:
    "hooks": {"PreToolUse": [{"matcher": "Write|Edit|MultiEdit|NotebookEdit",
      "hooks": [{"type": "command",
                 "command": "python3 ~/.ai/it-role-house/hooks/guard_library_write.py"}]}]}

Protocol: tool call JSON on stdin; exit 0 allows, exit 2 blocks and returns stderr to the model.
"""
import json
import os
import re
import sys
import time
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

# Common provider-neutral installation root.
LIB = os.path.realpath(os.path.expanduser(os.environ.get("AI_IT_HOUSE") or "~/.ai/it-role-house"))
DOT = LIB
STAGING = os.path.join(LIB, "staging")
APPROVAL = os.path.join(STAGING, "APPROVAL.json")
MANIFEST = os.path.join(LIB, "MANIFEST")


def owned():
    """Return absolute managed files and protected managed skill directories from install state.

    Exact-file ownership lets users keep their own Claude/Codex agents and commands in the same parent
    directories. Skill subtrees are protected as directories so an untracked file cannot be slipped into a
    package-owned skill and change its behaviour.
    """
    state = os.path.join(LIB, "install-state.json")
    try:
        rec = json.load(open(state, encoding="utf-8"))
        files = {os.path.realpath(os.path.expanduser(p)) for p in rec.get("files", {})}
    except (OSError, ValueError):
        files = set()
    skill_dirs = set()
    for path in files:
        parts = path.replace("\\", "/").split("/")
        if "skills" in parts:
            i = len(parts) - 1 - parts[::-1].index("skills")
            if i + 1 < len(parts):
                skill_dirs.add(os.path.realpath("/".join(parts[: i + 2]) or "/"))
    return files, skill_dirs


def protected(path):
    if under(path, LIB):
        return True
    files, skill_dirs = owned()
    return path in files or any(under(path, d) for d in skill_dirs)

def target(payload):
    ti = payload.get("tool_input") or {}
    for key in ("file_path", "path", "notebook_path", "filePath"):
        if ti.get(key):
            return os.path.realpath(os.path.expanduser(ti[key]))
    edits = ti.get("edits") or []
    if edits and isinstance(edits, list) and isinstance(edits[0], dict):
        p = edits[0].get("file_path")
        if p:
            return os.path.realpath(os.path.expanduser(p))
    return None



def targets(payload):
    """Return all file targets, including files named by Codex apply_patch payloads."""
    ti = payload.get("tool_input") or {}
    if payload.get("tool_name") == "apply_patch":
        cwd = payload.get("cwd") or os.getcwd()
        out = []
        for line in (ti.get("command") or "").splitlines():
            m = re.match(r"\*\*\* (?:Update|Add|Delete) File: (.+)$", line.strip())
            if m:
                p = m.group(1).strip()
                if not os.path.isabs(p):
                    p = os.path.join(cwd, p)
                out.append(os.path.realpath(os.path.expanduser(p)))
        return out
    p = target(payload)
    return [p] if p else []

def under(path, root):
    root = os.path.realpath(root)
    return path == root or path.startswith(root + os.sep)


def approval_covers(path):
    if not os.path.isfile(APPROVAL):
        return False, "no approval record at it-role-house/staging/APPROVAL.json"
    try:
        rec = json.load(open(APPROVAL, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return False, f"approval record unreadable: {exc}"
    if time.time() > float(rec.get("expires_epoch", 0)):
        return False, f"approval expired at {rec.get('expires')} (approver {rec.get('approver')})"
    scopes = [os.path.realpath(os.path.expanduser(s)) for s in rec.get("scope", [])]
    if not any(under(path, s) for s in scopes):
        return False, f"approval covers {rec.get('scope')}, not this path"
    return True, f"approved by {rec.get('approver')} until {rec.get('expires')}"


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0  # malformed payload is not this hook's business
    paths = targets(payload)
    if not paths:
        return 0
    for path in paths:
        if under(path, STAGING):
            continue
        if not protected(path):
            continue
        ok, why = approval_covers(path)
        if ok:
            sys.stderr.write(f"library write permitted: {why}\n")
            continue
        sys.stderr.write(
            "Blocked: the IS/IT role library is immutable without a recorded approval.\n"
            f"  path   : {path}\n"
            f"  reason : {why}\n\n"
            "The separation is deliberate. library-author stages a change under\n"
            "it-role-house/staging/, library-approver reviews it, a human records the approval\n"
            "with scripts/approve_change.py, and library-release applies it. Editing the live tree\n"
            "directly collapses author, approver and releaser into one actor.\n"
            "Where the library is in git, open a pull request instead and let CI be the gate.\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
