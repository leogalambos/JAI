#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Check readable line width in human-facing release documentation."""
from __future__ import annotations

import argparse
from pathlib import Path

WIDTH = 72
ROOT_DOCS = (
    "LICENSE",
    "LICENSING.md",
    "README.md",
    "CHANGELOG.md",
    "MIGRATION.md",
    "VALIDATION.md",
)
RUNTIME_DOCS = (
    "README.md",
    "CHANGELOG.md",
    "CHANGE-RECORD.md",
    "GUIDE.md",
    "LICENSE",
    "LICENSE-POLICY.md",
    "_meta/ARCHETYPES.md",
    "ea/README.md",
    "ea/adapters/README.md",
    "evals/README.md",
    "integrations/README.md",
    "publication/README.md",
    "sabsa/overlays/README.md",
    "staging/README.md",
    "standards/code-documentation.md",
    "standards/defect-analysis.md",
    "standards/testing.md",
)


def human_docs(root: Path):
    for rel in ROOT_DOCS:
        path = root / rel
        if path.is_file():
            yield path
    runtime = root / ".ai/runtime"
    for rel in RUNTIME_DOCS:
        path = runtime / rel
        if path.is_file():
            yield path


def exempt(line: str, in_fence: bool) -> bool:
    stripped = line.strip()
    if in_fence:
        return True
    if stripped.startswith("|") and stripped.endswith("|"):
        return True
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return True
    if stripped.startswith("http://") or stripped.startswith("https://"):
        return True
    if len(stripped.split()) == 1 and "https://" in stripped:
        return True
    return False


def check(root: Path):
    problems = []
    for path in human_docs(root):
        in_fence = False
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if len(line) <= WIDTH or exempt(line, in_fence):
                continue
            rel = path.relative_to(root).as_posix()
            problems.append(f"{rel}:{number}: {len(line)} characters")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    problems = check(Path(args.root).resolve())
    for problem in problems:
        print("FAIL", problem)
    if problems:
        print(f"FAIL human text width: {len(problems)} overlong prose lines")
        return 1
    print(
        "PASS human text width: prose is <=72 characters in "
        "human-facing documentation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
