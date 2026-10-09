#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Record a human approval for a staged library change. Run by a person, not an agent.

The approver agent holds no Write, so it cannot create this record. That is the point:
the act of approving sits outside the agent layer, where no instruction can reach it.

Usage
-----
    python3 approve_change.py --approver "L. Novak" --change CR-2026-014 \
        --scope ~/.ai/it-role-house/skills --scope ~/.ai/it-role-house/agents --expires 1
    python3 approve_change.py --revoke
"""
import argparse
import getpass
import hashlib
import json
import os
import subprocess
import sys
import time
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING = os.path.join(LIB, "staging")
APPROVAL = os.path.join(STAGING, "APPROVAL.json")
STAGED_TREE = os.path.join(STAGING, ".claude")


def tree_hash(root):
    h = hashlib.sha256()
    if not os.path.isdir(root):
        return None
    for dp, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(dp, f)
            h.update(os.path.relpath(p, root).encode())
            with open(p, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()[:16]


def require_person():
    """Approving a library change is a person's act: a terminal, or the hook's approval prompt."""
    if sys.stdin.isatty() and sys.stdout.isatty():
        return "terminal"
    home = os.path.dirname(LIB)
    try:
        if "guard_authority.py" in open(os.path.join(home, "settings.json"), encoding="utf-8").read():
            return "claude-code-approval-prompt"
    except OSError:
        pass
    sys.exit("approving a library change is a person's decision, and no approval gate is active: run it in "
             "your own terminal")


def main():
    ap = argparse.ArgumentParser(description="Record or revoke approval for a staged library change.")
    ap.add_argument("--approver", help="the person approving; must not be the author")
    ap.add_argument("--change", help="change record reference, e.g. CR-2026-014")
    ap.add_argument("--scope", action="append", default=[], help="path the approval covers; repeatable")
    ap.add_argument("--expires", type=float, default=1, help="validity in days (default 1)")
    ap.add_argument("--skip-validator", action="store_true", help="record anyway if the validator fails")
    ap.add_argument("--revoke", action="store_true")
    args = ap.parse_args()

    os.makedirs(STAGING, exist_ok=True)

    if args.revoke:
        if os.path.exists(APPROVAL):
            os.remove(APPROVAL)
            print("approval revoked")
        else:
            print("no approval record to revoke")
        return 0

    via = None if args.revoke else require_person()
    if not args.approver or not args.change or not args.scope:
        ap.error("--approver, --change and at least one --scope are required")

    validator = os.path.join(LIB, "scripts", "check_agent_policy.py")
    verdict = "not run"
    if os.path.isdir(STAGED_TREE) and os.path.isfile(validator):
        run = subprocess.run([sys.executable, validator, STAGED_TREE], capture_output=True, encoding="utf-8", errors="replace")
        verdict = "pass" if run.returncode == 0 else "FAIL"
        print(run.stdout.strip()[-800:])
        if run.returncode != 0 and not args.skip_validator:
            sys.exit("\nrefusing to approve: the staged tree fails its own policy check. "
                     "Fix it, or pass --skip-validator and justify it in the change record.")
    else:
        print(f"note: no staged tree at {STAGED_TREE}; approval will record 'not run'")

    expires = time.time() + args.expires * 86400
    rec = {
        "change": args.change,
        "approver": args.approver,
        "recorded_by": getpass.getuser(),
        "recorded": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "expires": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(expires)),
        "expires_epoch": expires,
        "scope": [os.path.expanduser(s) for s in args.scope],
        "staged_tree_hash": tree_hash(STAGED_TREE),
        "validator": verdict,
        "single_use": True,
        "approved_via": via,
    }
    json.dump(rec, open(APPROVAL, "w", encoding="utf-8"), indent=2)
    print(f"\napproval recorded: {args.change} by {args.approver}, expires {rec['expires']}")
    print(f"scope: {', '.join(rec['scope'])}")
    print("library-release may now apply the change. The record is single-use and should be "
          "consumed on release.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
