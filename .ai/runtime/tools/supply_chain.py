#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""SBOM, digest provenance and release-file integrity controls.

The package includes source digests and SPDX evidence. GitHub Actions may additionally
attach keyless OIDC-signed provenance to the published ZIP when available.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import platform
import re
import tempfile
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
EXCLUDE = {
    "SBOM.spdx.json",
    "PROVENANCE.json",
    "COMPATIBILITY.json",
    "QUALIFICATION-A-H.json",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_files(root):
    """Yield public distribution files covered by supply-chain integrity.

    Args:
        root: Existing, nonsymlink package source directory.
    Yields:
        Deterministically ordered regular paths selected by release packaging,
        excluding generated integrity evidence to avoid circular digests.
        Private and generated directories are pruned before descent.
    Raises:
        ValueError: If root is missing, is not a directory or is a symlink.
        OSError: If a maintained distribution directory cannot be enumerated.
    """
    spec = importlib.util.spec_from_file_location(
        '_jai_supply_chain_release_bundle', Path(__file__).with_name('release_bundle.py'))
    distribution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(distribution)
    source = Path(root)
    for path in distribution.files(source):
        if path.name not in EXCLUDE:
            yield source / path.relative_to(source.resolve())


def tree_digest(root) -> str:
    root = Path(root)
    digest = hashlib.sha256()
    for path in tree_files(root):
        rel = path.relative_to(root).as_posix()
        digest.update(rel.encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _declared_dependencies(root):
    rows = {}
    sources = []
    for name in ('requirements.txt', 'requirements-ci.txt','requirements-rendering.txt'):
        path = Path(root) / name
        if not path.is_file() or path.is_symlink():
            continue
        data = path.read_bytes()
        sources.append({'file': name, 'sha256': sha(data)})
        for line in data.decode('utf-8').splitlines():
            line = line.split('#', 1)[0].strip()
            if not line or line.startswith('-'):
                continue
            match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9_.-]*)([<>=!~0-9A-Za-z.,+*\-]*)', line)
            if match is None:
                continue
            canonical = re.sub(r'[-_.]+', '-', match[1]).lower()
            item = rows.setdefault(canonical, {'name': match[1], 'constraints': set(), 'sources': set()})
            item['constraints'].add(match[2]); item['sources'].add(name)
    dependencies = []
    for canonical, item in sorted(rows.items()):
        doc = {'SPDXID': 'SPDXRef-Dependency-' + canonical, 'name': item['name'],
            'downloadLocation': 'NOASSERTION', 'filesAnalyzed': False,
            'licenseDeclared': 'NOASSERTION', 'licenseConcluded': 'NOASSERTION',
            'comment': 'Declared requirements only, not measured installed/transitive closure: '
                + json.dumps({'constraints': sorted(item['constraints']), 'sources': sorted(item['sources'])}, sort_keys=True)}
        pins = {value[2:] for value in item['constraints'] if re.fullmatch(r'==[A-Za-z0-9][A-Za-z0-9.+\-]*', value)}
        if len(pins) == 1:
            doc['versionInfo'] = next(iter(pins))
        dependencies.append(doc)
    return dependencies, sources


def sbom(root, out):
    """Generate file-integrity SPDX plus declared Python dependency inventory.

    Args:
        root: Public distribution source selected by maintained packaging rules.
        out: Generated SPDX destination, excluded from circular file hashing.
    Returns:
        SPDX document with exact source-file checksums and dependency declarations
        derived from maintained requirements. Unknown dependency licenses remain
        NOASSERTION; installed/transitive resolution is not fabricated.
    Raises:
        OSError, ValueError: Public source, requirements or output is unavailable.
    """
    root = Path(root)
    files = []
    for index, path in enumerate(tree_files(root), 1):
        files.append({
            "SPDXID": f"SPDXRef-File-{index}",
            "fileName": "./" + path.relative_to(root).as_posix(),
            "checksums": [{"algorithm": "SHA256", "checksumValue": sha(path.read_bytes())}],
            "licenseConcluded": "BSD-4-Clause",
            "licenseInfoInFiles": ["BSD-4-Clause"],
        })
    version = (root / "VERSION").read_text().strip()
    dependencies, declaration_sources = _declared_dependencies(root)
    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    doc = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"ai-it-house-{version}",
        "documentNamespace": f"https://www.egothor.org/spdx/ai-it-house/{version}/{tree_digest(root)}",
        "creationInfo": {"created": now, "creators": ["Organization: Egothor", "Person: Leo Galambos"]},
        "packages": [{
            "SPDXID": "SPDXRef-Package",
            "name": "ai-it-house",
            "versionInfo": version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": True,
            "licenseDeclared": "BSD-4-Clause",
            "licenseConcluded": "BSD-4-Clause",
        }, *dependencies],
        "files": files,
        "relationships": [
            {"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": "SPDXRef-Package"},
            *[{"spdxElementId": "SPDXRef-Package", "relationshipType": "CONTAINS", "relatedSpdxElement": item["SPDXID"]} for item in files],
            *[{"spdxElementId": "SPDXRef-Package", "relationshipType": "DEPENDS_ON", "relatedSpdxElement": item["SPDXID"]} for item in dependencies],
        ],
        "annotations": [{
            "annotationType": "OTHER",
            "annotator": "Tool: AI IT House supply_chain.py",
            "annotationDate": now,
            "comment": "Declared dependency input files: " + json.dumps(declaration_sources, sort_keys=True)
                + "; installed and transitive dependency/license closure requires separate qualified environment evidence. GitHub OIDC attestation, when available, is external to this unsigned source inventory.",
        }],
    }
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


def compatibility(root, out):
    from schema_resolver import release_scope
    root = Path(root)
    manifest = json.loads((root / ".ai/runtime/_meta/release-manifest.json").read_text())
    doc = {
        "release": (root / "VERSION").read_text().strip(),
        "generated_from": "runtime/_meta/release-manifest.json",
        "components": manifest.get("compatibility", []),
        "supported_capabilities": release_scope(root),
        "rendering": {'html_pdf':'WeasyPrint 70 (optional, resource fetches denied) or operator LibreOffice',
            'docx_pptx_xlsx_visual':'actual Office bytes: local native-sandbox renderer when available, otherwise operator LibreOffice; HTML PDF is not a substitute',
            'operator_assurance':'LOCAL_OPERATOR_ATTESTATION; no enterprise identity or immutable audit claim'},
    }
    Path(out).write_text(json.dumps(doc, indent=2) + "\n")
    return doc


def provenance(root, sbom_path, qualification_path, out):
    from schema_resolver import release_scope
    root = Path(root)
    sbom_file = Path(sbom_path)
    qualification_file = Path(qualification_path)
    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    digest = tree_digest(root)
    doc = {
        "provenance_version": "3.0.0",
        "artifact": "ai-it-house",
        "version": (root / "VERSION").read_text().strip(),
        "artifact_digest": digest,
        "source_revision": f"source-tree-sha256:{digest}",
        "build_environment": {"python": platform.python_version(), "platform": platform.platform()},
        "build_workflow": "AI IT House GA qualification A-G followed by supply-chain Gate H and CI publication on a protected release tag.",
        "builder_identity": "AI IT House deterministic release build",
        "supported_capabilities": release_scope(root),
        "timestamp": now,
        "test_results": json.loads(qualification_file.read_text()),
        "sbom_digest": sha(sbom_file.read_bytes()),
        "integrity_model": "SHA-256 of source and ZIP, SPDX SBOM and CI audit trail; optional GitHub OIDC/Sigstore attestation where supported",
        "build_signing_status": "no-private-key-in-build",
        "publication_signing": {
            "mode": "automated-ci-release",
            "attestation": "github-oidc-if-supported",
            "subject": "distribution ZIP",
            "local_build_attested": False,
        },
    }
    Path(out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


def verify(root, sbom_path, prov_path, compat_path=None):
    from schema_resolver import release_scope
    root = Path(root)
    sbom_doc = json.loads(Path(sbom_path).read_text())
    provenance_doc = json.loads(Path(prov_path).read_text())
    problems = []
    if provenance_doc.get("artifact_digest") != tree_digest(root):
        problems.append("artifact/source tree digest mismatch")
    if provenance_doc.get('supported_capabilities') != release_scope(root):
        problems.append('provenance release scope mismatch')
    if provenance_doc.get("sbom_digest") != sha(Path(sbom_path).read_bytes()):
        problems.append("SBOM digest mismatch")
    if provenance_doc.get("build_signing_status") != "no-private-key-in-build":
        problems.append("build signing state is not keyless")
    pub = provenance_doc.get("publication_signing", {})
    if pub.get("mode") != "automated-ci-release" or pub.get("attestation") != "github-oidc-if-supported":
        problems.append("CI publication integrity policy missing")
    if sbom_doc.get("packages", [{}])[0].get("licenseDeclared") != "BSD-4-Clause":
        problems.append("SBOM licence mismatch")
    dependencies, _ = _declared_dependencies(root)
    if [row for row in sbom_doc.get('packages', []) if row.get('SPDXID') != 'SPDXRef-Package'] != dependencies:
        problems.append('SBOM declared dependency inventory mismatch')
    # The file catalogue is a working integrity control, not a decorative inventory.
    # Compare all declared paths and checksums with the authoritative release tree.
    observed = {}
    for entry in sbom_doc.get("files", []):
        rel = str(entry.get("fileName", "")).removeprefix("./")
        hashes = [item.get("checksumValue") for item in entry.get("checksums", [])
                  if item.get("algorithm") == "SHA256"]
        if not rel or rel in observed or len(hashes) != 1:
            problems.append("SBOM duplicate/malformed file entry")
            continue
        observed[rel] = hashes[0]
    expected = {path.relative_to(root).as_posix(): sha(path.read_bytes())
                for path in tree_files(root)}
    if observed.keys() != expected.keys():
        problems.append("SBOM file coverage mismatch")
    elif any(observed[rel] != digest for rel, digest in expected.items()):
        problems.append("SBOM file checksum mismatch")
    if compat_path:
        compat = json.loads(Path(compat_path).read_text())
        if compat.get("release") != (root / "VERSION").read_text().strip():
            problems.append("compatibility release mismatch")
        if compat.get("supported_capabilities")!=release_scope(root):
            problems.append("compatibility release scope mismatch")
    qualifications = provenance_doc.get("test_results", {})
    gates = qualifications.get("gates", {})
    if set(gates) != set("ABCDEFG") or not all(gates.values()):
        problems.append("provenance does not record all-pass A-G qualification")
    if problems:
        raise ValueError("; ".join(problems))
    return True


def self_test():
    from schema_resolver import release_scope
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "VERSION").write_text("26.10.0\n")
        (root / "LICENSE").write_text("BSD\n")
        (root / "x.py").write_text("# x\n")
        (root / ".ai/runtime/_meta").mkdir(parents=True)
        (root/'.ai/runtime/schema').mkdir()
        (root/'.ai/runtime/schema/release-scope.schema.json').write_bytes((RUNTIME/'schema/release-scope.schema.json').read_bytes())
        (root/'RELEASE-SCOPE.json').write_text(json.dumps(release_scope(RUNTIME)))
        (root / ".ai/runtime/_meta/release-manifest.json").write_text(json.dumps({"compatibility": []}))
        qualification = root / ".ai/runtime/_meta/qualification-A-G.json"
        qualification.write_text(json.dumps({"gates": {gate: True for gate in "ABCDEFG"}}))
        sbom_file, compat_file, prov_file = root / "SBOM.spdx.json", root / "COMPATIBILITY.json", root / "PROVENANCE.json"
        sbom(root, sbom_file)
        compatibility(root, compat_file)
        provenance(root, sbom_file, qualification, prov_file)
        verify(root, sbom_file, prov_file, compat_file)
        # A corrupt file-level SBOM digest must be rejected even if provenance
        # is recomputed to match that corrupted SBOM container.
        good_sbom=sbom_file.read_bytes()
        corrupted=json.loads(good_sbom)
        corrupted["files"][0]["checksums"][0]["checksumValue"]="0"*64
        sbom_file.write_text(json.dumps(corrupted))
        changed_sbom=json.loads(sbom_file.read_text())
        assert changed_sbom["files"][0]["checksums"][0]["checksumValue"]=="0"*64
        provenance(root, sbom_file, qualification, prov_file)
        try:
            verify(root, sbom_file, prov_file, compat_file)
            raise AssertionError("corrupt SBOM per-file digest accepted")
        except ValueError:
            pass
        sbom_file.write_bytes(good_sbom)
        provenance(root, sbom_file, qualification, prov_file)
        verify(root, sbom_file, prov_file, compat_file)
        (root / "x.py").write_text("# tampered\n")
        try:
            verify(root, sbom_file, prov_file, compat_file)
            raise AssertionError("tamper accepted")
        except ValueError:
            pass
    print("PASS supply-chain: SPDX SBOM + digest provenance + tamper detection + automated CI publication policy")
    return 0


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("self-test")
    sb = sub.add_parser("sbom"); sb.add_argument("--root", required=True); sb.add_argument("--out", required=True)
    co = sub.add_parser("compatibility"); co.add_argument("--root", required=True); co.add_argument("--out", required=True)
    pr = sub.add_parser("provenance"); pr.add_argument("--root", required=True); pr.add_argument("--sbom", required=True); pr.add_argument("--qualification", required=True); pr.add_argument("--out", required=True)
    ve = sub.add_parser("verify"); ve.add_argument("--root", required=True); ve.add_argument("--sbom", required=True); ve.add_argument("--provenance", required=True); ve.add_argument("--compatibility")
    args = parser.parse_args()
    if args.cmd == "self-test": return self_test()
    if args.cmd == "sbom": sbom(args.root, args.out); return 0
    if args.cmd == "compatibility": compatibility(args.root, args.out); return 0
    if args.cmd == "provenance": provenance(args.root, args.sbom, args.qualification, args.out); return 0
    verify(args.root, args.sbom, args.provenance, args.compatibility); print("PASS provenance/SBOM/compatibility integrity"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
