# Validation — AI IT House 26.10.11

## Production boundary

26.10.11 uses the six-layer Justifiable AI core as its single normative
architecture. Artifact Contract v3 is the native production write model.
Artifact Contract v2 is read/migration-only and is hash-frozen by the
Native Write Policy.

## Enterprise qualification

```sh
python3 .ai/runtime/tools/release_ga.py qualify
```

The independent release gates are:

- **A — Structural:** Native JAI enforcement, schemas, v3 artifact
  contracts, generated documentation and policy.
- **B — Semantic:** SABSA, scoped EA projection, ArchiMate
  interoperability and repository consistency.
- **C — Governance:** authorities/workflows, v3 governance contracts,
  immutable execution records and service objectives.
- **D — Runtime Security:** authority enforcement, model routing,
  provider parity, adapter mutation controls and regression tests.
- **E — Publication:** JAI-lineaged ProjectionManifest v3, enterprise
  renderers and publication integrity.
- **F — Visual:** render-based visual QA.
- **G — Behavioral:** enterprise scenarios, deterministic thresholds,
  adversarial checks and a hard fixture/live-evidence boundary. The
  universal package does not claim qualification of a mutable external
  provider/model; live qualification requires captured results plus a
  typed evidence manifest.
- **H — Supply Chain:** licence policy, SPDX SBOM, digest provenance,
  distribution archive checksums and automated GitHub release policy.

`QUALIFICATION-A-H.json` is the authoritative qualification result.

## Automated production release

```sh
# Change VERSION and synchronize product metadata before committing the tag.
# Only VERSION is edited manually; no global string replacement.
python3 scripts/versioning.py sync
# Commit the result, push main, then publish this exact source version.
git tag -a 'release@26.10.11' -m 'JAI 26.10.11'
git push origin 'release@26.10.11'
```

The root `VERSION` is the authoritative product version.
The synchronization script updates installation mirrors, current
catalog metadata and generated documentation. GitHub Actions rejects
tags that disagree with the committed `VERSION` and never changes
its source identity. Independent JAI/schema contract versions and
historical migrations remain unchanged. After A-H
qualification it generates a production distribution ZIP and `.sha256`
checksum and publishes GitHub Release `YY.MM.VV` automatically. GitHub
OIDC attestations protect eligible builds; a private GitHub Free/Pro
repository may publish using digest provenance only.

## Compatibility

- 26.10.0 Artifact Contract v2: read/migrate only.
- 26.10.1 JAI/v3: read/migrate only.
- 26.10.2 JAI/v3: read/migrate only.
- 26.10.3 JAI/v3: read/migrate only.
- Native writes: `ArtifactContract-v3` (independent of product release).

Verified carry-over reviews are recorded in:

- `.ai/runtime/_meta/26.10.1-carryover-audit.json`
- `.ai/runtime/_meta/26.10.2-carryover-audit.json`
- `.ai/runtime/_meta/26.10.3-carryover-audit.json`
