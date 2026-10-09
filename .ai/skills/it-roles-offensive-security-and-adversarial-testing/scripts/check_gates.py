#!/usr/bin/env python3
"""Validate a gate-check block against the output gates declared in a role skill.

The skill's section 7 lists blocking gates as `- [ ] **G1.** ...`. Section 5 requires the
response to carry a GATE CHECK block giving an explicit verdict per gate. This script
compares the two so that a missing or hand-waved verdict fails loudly instead of passing
because nobody re-read the list.

Usage
-----
    python3 scripts/check_gates.py --skill SKILL.md gate-check.txt
    python3 scripts/check_gates.py --skill . gate-check.txt        # directory: finds SKILL.md
    cat gate-check.txt | python3 scripts/check_gates.py --skill SKILL.md -

Accepted verdict lines (one per gate, case-insensitive, order irrelevant):
    G1: pass
    G2: fail - remediation owner Alice, due 2026-11-30
    G3: waived by Priya Rao until 2026-12-15 - reason: supplier evidence outstanding

Exit status is 0 only when every gate has a verdict, no gate is failed without an owner,
and every waiver carries both an approver and an expiry date.
"""
import argparse
import os
import re
import sys
for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
# Under a non-UTF-8 locale, arguments arrive surrogate-escaped; recover the real characters (a no-op otherwise).
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

GATE_RE = re.compile(r"^\s*-\s*\[[ xX]\]\s*\*\*(G\d+)\.\*\*\s*(.+?)\s*$")
VERDICT_RE = re.compile(r"^\s*\**(G\d+)\**\s*[:\-\u2014]\s*(.+?)\s*$", re.IGNORECASE)
WAIVER_BY_RE = re.compile(r"\b(?:waived|waiver)\b.*?\bby\s+([^,;]+?)\s*(?:\buntil\b|,|;|$)", re.IGNORECASE)
EXPIRY_RE = re.compile(r"\b(?:until|expires?|expiry)\b[^0-9]{0,12}(\d{4}-\d{2}-\d{2}|\d{1,2}\s+\w+\s+\d{4})",
                       re.IGNORECASE)
OWNER_RE = re.compile(r"\b(?:owner|assigned to|remediation owner)\b\s*:?\s*([^,;]+)", re.IGNORECASE)


def load_gates(skill_path):
    if os.path.isdir(skill_path):
        skill_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_path):
        sys.exit(f"error: no SKILL.md at {skill_path}")
    gates = {}
    with open(skill_path, encoding="utf-8") as fh:
        for line in fh:
            match = GATE_RE.match(line)
            if match:
                gates[match.group(1).upper()] = match.group(2)
    if not gates:
        sys.exit(f"error: no gates found in {skill_path}; expected lines like '- [ ] **G1.** ...'")
    return gates, skill_path


def load_verdicts(path):
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    verdicts = {}
    for line in text.splitlines():
        match = VERDICT_RE.match(line)
        if match:
            verdicts[match.group(1).upper()] = match.group(2)
    return verdicts


def classify(text):
    low = text.lower()
    if "waiv" in low:
        return "waived"
    if low.startswith("fail") or " fail" in low[:24]:
        return "fail"
    if low.startswith("pass") or low.startswith("ok") or low.startswith("met"):
        return "pass"
    return "unclear"


def main():
    parser = argparse.ArgumentParser(description="Validate a gate-check block against a skill's output gates.")
    parser.add_argument("--skill", default="SKILL.md", help="path to SKILL.md or its directory")
    parser.add_argument("gate_check", help="file containing the GATE CHECK block, or - for stdin")
    args = parser.parse_args()

    gates, skill_path = load_gates(args.skill)
    verdicts = load_verdicts(args.gate_check)
    problems = []
    counts = {"pass": 0, "fail": 0, "waived": 0, "unclear": 0}

    for gid in sorted(gates, key=lambda g: int(g[1:])):
        if gid not in verdicts:
            problems.append(f"{gid}: no verdict given - {gates[gid][:90]}")
            continue
        body = verdicts[gid]
        kind = classify(body)
        counts[kind] += 1
        if kind == "unclear":
            problems.append(f"{gid}: verdict '{body[:60]}' is not pass, fail or waived")
        elif kind == "fail" and not OWNER_RE.search(body):
            problems.append(f"{gid}: failed with no remediation owner named")
        elif kind == "waived":
            if not WAIVER_BY_RE.search(body):
                problems.append(f"{gid}: waived without naming the approver")
            if not EXPIRY_RE.search(body):
                problems.append(f"{gid}: waived without an expiry date")

    extra = sorted(set(verdicts) - set(gates), key=lambda g: int(g[1:]))
    for gid in extra:
        problems.append(f"{gid}: verdict given for a gate this skill does not declare")

    print(f"skill    : {skill_path}")
    print(f"gates    : {len(gates)} declared")
    print("verdicts : " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    if problems:
        print(f"\nFAILED ({len(problems)} problem{'s' if len(problems) != 1 else ''}):")
        for p in problems:
            print(f"  - {p}")
        return 1
    if counts["fail"] or counts["waived"]:
        print("\nOK: every gate accounted for. Note there are failed or waived gates; "
              "the deliverable is not released until those are closed or the waivers are recorded.")
    else:
        print("\nOK: every gate has an explicit pass verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
