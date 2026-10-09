#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate release@YY.MM.VV against the product release policy."""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

TAG = re.compile(r"release@([0-9]{2}\.(?:0[1-9]|1[0-2])\.[0-9]+)\Z")


def version_for_tag(root: Path, tag: str) -> str:
    m = TAG.fullmatch(tag)
    if m is None:
        raise ValueError(f"Invalid release tag {tag!r}; expected release@YY.MM.VV")
    version = m.group(1)
    policy = json.loads((root / ".ai/runtime/release/release-policy.json").read_text(encoding="utf-8"))
    if policy.get("version_scheme") != "YY.MM.VV" or not re.fullmatch(policy.get("version_regex", "(?!)"), version):
        raise ValueError(f"Version {version!r} is not allowed by release-policy.json")
    if policy.get("signing", {}).get("mode") != "automated-ci-release":
        raise ValueError("Release policy must require automated CI publication")
    source = (root / "VERSION").read_text(encoding="utf-8").strip()
    if version != source:
        raise ValueError(
            f"release tag {tag} does not match source VERSION={source}; "
            "run versioning.py sync and commit VERSION before tagging"
        )
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        version = version_for_tag(args.root.resolve(), args.tag)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        parser.exit(1, f"FAIL release tag validation: {e}\n")
    print(f"PASS release tag {args.tag} → {version}")
    if path := os.environ.get("GITHUB_OUTPUT"):
        with open(path, "a", encoding="utf-8") as file:
            file.write(f"version={version}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
