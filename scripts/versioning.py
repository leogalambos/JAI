#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Synchronise JAI product identity from the one authoritative root VERSION.

`sync` changes only product-version projections and generated documentation.
It never rewrites contract versions, migration targets, frozen schemas, audit
records, changelogs, historical release pages, SBOM or provenance evidence.

A release@YY.MM.VV tag must match the *committed* root VERSION. The CI build
validates the match and produces release evidence without mutating this value.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TAG = re.compile(r"release@([0-9]{2}\.(?:0[1-9]|1[0-2])\.[0-9]+)\Z")
VERSION = re.compile(r"[0-9]{2}\.(?:0[1-9]|1[0-2])\.[0-9]+\Z")
# Root VERSION is the sole input, the others are compatibility projections.
MIRRORS = ("VERSION", ".ai/VERSION", ".ai/runtime/VERSION")
# Only these catalog fields denote the CURRENT DISTRIBUTION version.
PRODUCT_CATALOGS = {
    ".ai/runtime/roles.json": "version",
    ".ai/runtime/workflows.json": "version",
    ".ai/runtime/content/evaluation-package.json": "release",
}
GENERATED_MANIFEST = ".ai/runtime/_meta/release-manifest.json"
NATIVE_WRITE = "ArtifactContract-v3"


def to_tuple(version: str) -> tuple[int, int, int]:
    if not VERSION.fullmatch(version):
        raise ValueError(f"invalid YY.MM.VV product version: {version!r}")
    return tuple(map(int, version.split(".")))


def identity_from_tag(tag: str) -> str:
    match = TAG.fullmatch(tag)
    if not match:
        raise ValueError(f"expected release@YY.MM.VV, received: {tag!r}")
    return match.group(1)


def source_version(root: Path) -> str:
    path = Path(root) / "VERSION"
    if not path.is_file():
        raise ValueError(f"missing authoritative product VERSION: {path}")
    version = path.read_text(encoding="utf-8").strip()
    to_tuple(version)
    return version


def verify_tag(root: Path, tag: str) -> str:
    requested = identity_from_tag(tag)
    actual = source_version(root)
    if requested != actual:
        raise ValueError(
            f"tag {tag} does not match committed VERSION={actual}; "
            "edit VERSION, run 'python3 scripts/versioning.py sync', "
            "commit and push before creating the tag"
        )
    return actual


def catalog_projection(text: str, key: str, version: str, rel: str) -> str:
    """Change an allowlisted top-level scalar without reserialising large JSONs."""
    data = json.loads(text)
    if not isinstance(data, dict) or not isinstance(data.get(key), str):
        raise ValueError(f"missing top-level string {key} in {rel}")
    # All current catalogues begin with the version property. Do not touch
    # identically named fields of nested roles, workflows or contracts.
    pattern = re.compile(r'\A(\{\s*"' + re.escape(key) + r'"\s*:\s*)"[^"]+"')
    if rel == '.ai/runtime/content/evaluation-package.json':
        # Descriptor metadata follows schema identity; match only its top-level
        # two-space release field, never pinned file hashes or nested baselines.
        pattern = re.compile(r'^(  "release"\s*:\s*)"[^"]+"', re.MULTILINE)
    replaced, count = pattern.subn(lambda m: m.group(1) + json.dumps(version), text, count=1)
    if count != 1:
        raise ValueError(f"cannot safely project top-level {key} in {rel}")
    if json.loads(replaced)[key] != version:
        raise ValueError(f"invalid product-version projection: {rel}")
    return replaced


def expected_catalogs(root: Path, version: str) -> dict[Path, str]:
    output = {}
    for rel, key in PRODUCT_CATALOGS.items():
        path = root / rel
        if not path.is_file():
            raise ValueError(f"missing active product catalogue: {rel}")
        output[path] = catalog_projection(path.read_text(encoding="utf-8"), key, version, rel)
    return output


def check(root: Path, tag: str | None = None) -> list[str]:
    """Check product projections, not compatibility baselines or release history."""
    root = root.resolve()
    errors: list[str] = []
    try:
        version = source_version(root)
        if tag:
            verify_tag(root, tag)
        for rel in MIRRORS[1:]:
            path = root / rel
            if not path.is_file() or path.read_text(encoding="utf-8").strip() != version:
                errors.append(f"stale product VERSION projection: {rel}")
        for path, rendered in expected_catalogs(root, version).items():
            if path.read_text(encoding="utf-8") != rendered:
                errors.append(f"stale active catalogue version: {path.relative_to(root)}")
        manifest = root / GENERATED_MANIFEST
        if not manifest.is_file() or json.loads(manifest.read_text(encoding="utf-8")).get("release") != version:
            errors.append(f"stale generated product manifest: {GENERATED_MANIFEST}")
        policy_path = root / ".ai/runtime/release/release-policy.json"
        if policy_path.is_file():
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            if policy.get("signing", {}).get("mode") != "automated-ci-release":
                errors.append("release policy requires automated publication")
        # Stable write identities are contract invariants, not product versions.
        for rel in ("artifacts/contracts/role-deliverables.v3.json",
                    "artifacts/role-deliverables.json"):
            path = root / ".ai/runtime" / rel
            if not path.is_file():
                errors.append(f"missing artifact contract catalogue: {rel}")
                continue
            for contract in json.loads(path.read_text(encoding="utf-8")).get("contracts", []):
                if contract.get("compatibility", {}).get("writes") != NATIVE_WRITE:
                    errors.append(f"{contract.get('id')}: write contract must be {NATIVE_WRITE}")
                    break
        generator = root / ".ai/runtime/tools/generate_docs.py"
        if generator.is_file():
            result = subprocess.run(
                [sys.executable, str(generator), "--check", "--root", str(root)],
                cwd=root, capture_output=True, text=True,
            )
            if result.returncode:
                errors.append("generated documentation out of date: " +
                              (result.stdout + result.stderr).strip()[:800])
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
    return errors


def sync(root: Path, generate_docs: bool = True) -> None:
    """Idempotently project VERSION into allowlisted, actively versioned files."""
    root = root.resolve()
    version = source_version(root)
    # Validate all destinations before changing any file (fail closed).
    catalogs = expected_catalogs(root, version)
    for rel in MIRRORS[1:]:
        if not (root / rel).is_file():
            raise ValueError(f"missing product VERSION projection: {rel}")
    for rel in MIRRORS[1:]:
        path = root / rel
        if path.read_text(encoding="utf-8") != version + "\n":
            path.write_text(version + "\n", encoding="utf-8")
    for path, rendered in catalogs.items():
        if path.read_text(encoding="utf-8") != rendered:
            path.write_text(rendered, encoding="utf-8")
    if generate_docs:
        generator = root / ".ai/runtime/tools/generate_docs.py"
        if not generator.is_file():
            raise ValueError(f"missing documentation generator: {generator}")
        subprocess.run([sys.executable, str(generator), "--root", str(root)],
                       check=True, cwd=root)
        problems = check(root)
        if problems:
            raise ValueError("; ".join(problems))
    print(f"PASS synchronized product identity {version}; historical identities unchanged")


def prepare(root: Path, version: str | None = None, generate_docs: bool = True) -> None:
    """Backward-compatible API name: never override root VERSION from a tag."""
    if version is not None and version != source_version(root):
        raise ValueError(f"requested version {version} differs from authoritative VERSION={source_version(root)}")
    sync(root, generate_docs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    a = commands.add_parser("sync", help="project root VERSION into active metadata and generated docs")
    a.add_argument("--root", type=Path, default=Path("."))
    a = commands.add_parser("check", help="verify all maintained projections without modifying files")
    a.add_argument("--root", type=Path, default=Path("."))
    a.add_argument("--tag", help="also require exact match with release@YY.MM.VV")
    # Keep prior CLI operational, but enforce source-version ownership.
    a = commands.add_parser("prepare", help="compatibility alias for sync; tag must match VERSION")
    a.add_argument("--root", type=Path, default=Path("."))
    identity = a.add_mutually_exclusive_group()
    identity.add_argument("--tag")
    identity.add_argument("--version")
    args = parser.parse_args()
    try:
        if args.command == "sync":
            sync(args.root)
        elif args.command == "prepare":
            if args.tag:
                verify_tag(args.root, args.tag)
            prepare(args.root, args.version)
        else:
            problems = check(args.root, args.tag)
            if problems:
                raise ValueError("; ".join(problems))
            print(f"PASS VERSION={source_version(args.root)} and synchronized products")
    except (ValueError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        parser.exit(1, f"FAIL versioning: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
