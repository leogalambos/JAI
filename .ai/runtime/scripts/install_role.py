#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Promote one role reference file into a standalone skill under ~/.ai/it-role-house/skills/.

The library keeps one copy of each role, inside its category skill's references/ folder.
That is the right default: a home-directory install loads every skill description in every
session, so 17 descriptions beat 258. But if you work in one role constantly, having it as
its own top-level skill makes it trigger directly instead of via the router.

This generates that standalone form from the same source, so the content still has exactly
one home. Re-run it after the library is updated, or delete it and use the reference again.

Usage
-----
    python3 install_role.py solution-architect
    python3 install_role.py solution-architect --root ~/.ai/it-role-house --dry-run
    python3 install_role.py --list architecture
"""
import argparse
import json
import os
import shutil
import sys
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]


def default_root():
    """Prefer the install this script actually lives in, then ~/.ai/it-role-house."""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../it-role-library
    guess = os.path.dirname(here)
    if os.path.isfile(os.path.join(guess, "it-role-library", "roles.json")):
        return guess
    return os.path.expanduser(os.environ.get("AI_IT_HOUSE") or "~/.ai/it-role-house")


def load(root):
    path = os.path.join(root, "it-role-library", "roles.json")
    if not os.path.isfile(path):
        sys.exit(f"error: no catalogue at {path}")
    return json.load(open(path, encoding="utf-8"))["roles"]


def main():
    parser = argparse.ArgumentParser(description="Promote a role reference into a standalone skill.")
    parser.add_argument("role", nargs="?", help="role slug, e.g. solution-architect")
    parser.add_argument("--root", default=default_root(),
                        help="the .claude directory (defaults to this script's own install)")
    parser.add_argument("--list", metavar="SUBSTRING", help="list matching role slugs and exit")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = os.path.expanduser(args.root)
    roles = load(root)

    if args.list is not None:
        needle = args.list.lower()
        hits = [r for r in roles
                if needle in r["slug"] or needle in r["category"].lower() or needle in r["name"].lower()]
        for r in sorted(hits, key=lambda r: r["slug"]):
            print(f"{r['slug']:52s} {r['tool_tier']:8s} {r['category']}")
        print(f"\n{len(hits)} of {len(roles)} roles")
        return 0

    if not args.role:
        parser.error("give a role slug, or use --list")

    match = [r for r in roles if r["slug"] == args.role]
    if not match:
        near = [r["slug"] for r in roles if args.role in r["slug"]][:8]
        sys.exit(f"error: no role '{args.role}'" + (f"; did you mean: {', '.join(near)}" if near else ""))
    role = match[0]

    src = os.path.join(root, role["path"])
    if not os.path.isfile(src):
        sys.exit(f"error: reference file missing at {src}")
    body = open(src, encoding="utf-8").read()

    # drop the reference banner and re-point the bundled checker to the new location
    if body.startswith("> Reference file"):
        body = body.split("\n\n", 1)[1]
    body = body.replace("python3 ../scripts/check_gates.py --skill .",
                        "python3 scripts/check_gates.py --skill SKILL.md")

    # the description is rebuilt from the catalogue so it stays inside the 1024-char limit
    arts = role["primary_deliverables"][:3]
    parts = [f"{role['name']}: {role['mission'].rstrip('.')}.",
             f"Delivers {'; '.join(arts)}.",
             f"Use when the request concerns {arts[0].lower()}"
             + (f" or {arts[1].lower()}" if len(arts) > 1 else "")
             + (f", or applies {' or '.join(role['reference_frameworks'][:2])}"
                if role["reference_frameworks"] else "") + "."]
    if role["aliases"]:
        parts.append(f"Also titled {', '.join(role['aliases'])}.")
    desc = " ".join(parts)
    while len(desc) > 1020 and len(parts) > 3:
        parts.pop()
        desc = " ".join(parts)

    front = ["---", f"name: {role['slug']}",
             'description: "' + desc[:1020].replace("\\", "\\\\").replace('"', '\\"') + '"',
             f"allowed-tools: {role['allowed_tools']}", "---", ""]
    dest = os.path.join(root, "skills", role["slug"])
    target = os.path.join(dest, "SKILL.md")

    print(f"role     : {role['name']}")
    print(f"tier     : {role['tool_tier']}  ({role['allowed_tools']})")
    print(f"operator : {role['operator_agent']}")
    print(f"source   : {src}")
    print(f"target   : {target}")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    if os.path.exists(target):
        sys.exit(f"error: {target} already exists; delete it first if you meant to refresh it")

    os.makedirs(os.path.join(dest, "scripts"), exist_ok=True)
    open(target, "w", encoding="utf-8").write("\n".join(front) + body)
    checker = os.path.join(root, "skills", role["skill"], "scripts", "check_gates.py")
    if os.path.isfile(checker):
        shutil.copy(checker, os.path.join(dest, "scripts", "check_gates.py"))
        os.chmod(os.path.join(dest, "scripts", "check_gates.py"), 0o755)

    print("\nwritten. The role now triggers directly as well as through the router.")
    print("It is a copy: re-run this after the library changes, or delete the folder to go back to the "
          "reference.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
