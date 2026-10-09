#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate YY.MM.VV versioning and first-production-release policy."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
PACKAGE = RUNTIME.parents[1]
POLICY = RUNTIME / "release/release-policy.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def version_tuple(value):
    yy, mm, vv = value.split(".")
    return int(yy), int(mm), int(vv)


def changelog_versions(path):
    text = Path(path).read_text(encoding="utf-8")
    return re.findall(r"^##\s+([0-9]+\.[0-9]+\.[0-9]+)\b", text, re.MULTILINE)


def validate(final=False):
    policy = load(POLICY)
    problems = []
    version = (PACKAGE / "VERSION").read_text().strip()
    for mirror in (PACKAGE / ".ai/VERSION", RUNTIME / "VERSION"):
        if not mirror.is_file() or mirror.read_text().strip() != version:
            problems.append(f"package VERSION mirror differs: {mirror}")
    regex = policy.get("version_regex", "")
    if not re.match(regex, version):
        problems.append(f"version {version!r} does not match YY.MM.VV policy")
    first = policy.get("first_production_release")
    try:
        if version_tuple(version) < version_tuple(first):
            problems.append(f"production version {version} predates first production release {first}")
    except Exception:
        problems.append("invalid first production release version")
    for path in (PACKAGE / "CHANGELOG.md", RUNTIME / "CHANGELOG.md"):
        versions_in_log = changelog_versions(path)
        for item in versions_in_log:
            if not re.match(regex, item):
                problems.append(f"{path.name}: non-production version {item}")
            elif version_tuple(item) < version_tuple(first):
                problems.append(f"{path.name}: pre-GA history {item} is forbidden")
        if version == first and versions_in_log != [version]:
            problems.append(f"{path.name}: first production changelog must contain only {version}")
    if policy.get("version_scheme") != "YY.MM.VV":
        problems.append("version scheme is not YY.MM.VV")
    if policy.get("pre_ga_versions_in_changelog") is not False:
        problems.append("pre-GA changelog policy must be false")
    if set(policy.get("required_gates", [])) != set("ABCDEFGH"):
        problems.append("release policy must require gates A-H")
    signing = policy.get("signing", {})
    if signing.get("mode") != "automated-ci-release":
        problems.append("release must be automatically published by GitHub Actions")
    if signing.get("publication_requires_manual_approval") is not False:
        problems.append("release publication must not require manual signing or approval")
    if signing.get("private_key_in_package") is not False:
        problems.append("signing keys must not be packaged")
    if signing.get("attestation") != "github-oidc-if-supported":
        problems.append("unsupported release provenance attestation configuration")
    if final:
        for name in policy.get("required_release_files", []):
            if not (PACKAGE / name).is_file():
                problems.append(f"required release file missing: {name}")
        for candidate in PACKAGE.glob("*.sig"):
            problems.append(
                f"signature files must not be packaged: {candidate.name}"
            )
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["check", "self-test"])
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    problems = validate(args.final)
    if problems:
        print(f"FAILED ({len(problems)} problems)")
        for problem in problems:
            print(" -", problem)
        raise SystemExit(1)
    print("PASS release policy: YY.MM.VV, production-only history, A-H policy, automated publication")


if __name__ == "__main__":
    main()
