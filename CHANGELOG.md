# Changelog

## Unreleased

- SABSA: six authored English narrative viewpoint profiles, complete
  source-backed specifications and typed business paths, semantic
  narrative approval coverage, a reusable populated example, and
  controlled LaTeX/PDF publication, deterministic editable CSV catalogue
  exchange with preflight validation, and landscape proportional Word
  catalogue tables.
- Adds "How to use JAI" tutorials for a security assessment and Android
  development, with complete Claude Code and Codex prompts in native
  tabs, explanatory checkpoints and expected artefacts.
- Fixes duplicate navigation markers on expandable tutorial sections
  while preserving nested links, toggle controls and keyboard focus.
- Documents task-specific sandbox and publication prerequisites,
  including TeX resources, fonts, temporary files and resolver access.
- Clarifies default runtime paths and installer destination overrides;
  ordinary installation needs no path exports, and overrides do not
  establish complete runtime relocation or migrate existing files.
- Adds archival of completed private finding ledgers under exclusive
  maintenance, preserving event and hash bytes without changing
  authority.
- Excludes private inputs and local audit and build outputs from release
  bundles.

## 26.10.4 — Unified Lifecycle GA

- Corrective repack: synchronizes `roles.json` and `workflows.json`
  release metadata with 26.10.4.
- Removes stale 26.10.3 current-state references from the EA operator
  surface and the current EA schema title.
- Adds release-blocking conformance checks that distinguish historical
  compatibility references from current-release identity.
- Implements the Unified Lifecycle GA target previously planned as
  26.11.0, released as 26.10.4 to preserve the mandatory `YY.MM.VV`
  year/month/in-month-version scheme.
- Verified the 26.10.3 hardening baseline before implementation and
  closed its remaining GA carry-over rather than reopening already
  satisfied convergence work.
- Advances Artifact Contract v3 and all current schemas to the 26.10.4
  native-write namespace with deterministic forward migration from
  26.10.0, 26.10.1, 26.10.2 and 26.10.3.
- Makes SABSA authoring profile-native at source: new or modified
  elements persist canonical JAI semantic references and L2 profile
  metadata; legacy libraries remain readable and upgrade on write or
  explicit migration.
- Makes runtime authority profile-native: Agent Contracts carry embedded
  JAI bindings, managed policy declares its JAI runtime profile, and
  every new ExecutionRecord is a JAI L6 evidence object in the
  tamper-evident chain.
- Makes production publication profile-native end to end: projection
  writes JAI lineage into the publication model, production rendering
  requires the matching ProjectionManifest v3, and render evidence is
  emitted with output hashes and QA outcomes.
- Corrects Gate G semantics. Packaged reference results are now
  explicitly fixture-only and cannot be accepted as live provider/model
  qualification. Live qualification requires a typed evidence manifest
  containing provider/model identity and hashes for captured results.
- Adds a 26.10.4 release-blocking Unified Lifecycle suite covering
  native profile writes, migration, semantic identity, runtime evidence,
  publication lineage and behavioral qualification boundaries.
- No new roles, workflows or artifact types; this release completes the
  lifecycle/integrity objective on the 26.10.3 functional baseline.

## 26.10.3 — Unified Lifecycle Hardening

- Closed independently verified 26.10.2 carry-over gaps before the 26.11
  unified-lifecycle GA.
- Made the current schema registry the resolver for active integration,
  execution-record, behavioral and agent/runtime validation paths;
  legacy schema copies remain compatibility inputs only.
- Advanced Artifact Contract v3/JAI native writes to 26.10.3 and added
  deterministic 26.10.2 -> 26.10.3 migration while preserving original
  26.10.0 source hashes and audit history.
- Made EA repository writes profile-native: release schema version,
  explicit `authoritative_for: ea-domain-projection`,
  `global_source_of_truth: false`, and JAI semantic-identity authority;
  legacy 26.10 repositories remain readable and upgrade on write.
- Strengthened SABSA -> EA projection with canonical semantic
  references, orthogonal JAI L2 bindings and SABSA source
  specialisations; legacy bridge identifiers remain read-compatible.
- Added release-blocking architecture-claim lint and bounded cross-gate
  regression mode so documentation/authority drift and duplicate
  long-running qualification paths cannot silently pass.
- No new roles, workflows or artifact types; this is a
  convergence/hardening release on the 26.10.2 baseline.

Production release history starts with the first generally available
release. Pre-production development builds are intentionally omitted.

## 26.10.2 — Native JAI Enforcement

- Makes Artifact Contract v3 / JAI the only production write model;
  v2 is cryptographically frozen as a read/migration fixture.
- Carries forward and closes 26.10.1 convergence gaps: full migration
  provenance, retention preservation, JAI publication lineage and fabric
  semantic object references.
- Moves Gate A/C and schema/referential validation from v2 authority
  to the native v3 registry and adds a first-class Native Write Policy.
- Adds exhaustive 1,124-contract migration loss/hash checks and direct
  26.10.0/26.10.1 forward migration into the 26.10.2 namespace.
- Makes generated validation documentation release-blocking and
  records the verified 26.10.1 carry-over audit.
- Preserves SABSA/EA/profile semantics, provider parity and A-H
  qualification while adding no new roles, workflows or artifact types.

## 26.10.1 — Justifiable Architecture Convergence

- Makes the six-layer Justifiable AI core the single normative top-level
  architecture;
  L0 remains an external human-authority boundary.
- Adds versioned JAI core registries, layer/profile/transition schemas
  and scoped
  authority rules.
- Introduces Artifact Contract v3 as the native write model with
  forward-only v2
  migration and 26.10.0 read compatibility.
- Recasts SABSA, EA, Publication and Runtime as orthogonal/scoped JAI
  profiles; EA is
  authoritative only for architecture-domain projection.
- Normalises all 281 role layer names from the JAI registry and adds
  explicit role JAI
  bindings.
- Converts the fabric towards an assurance-ledger role by supporting
  canonical object
  references and hashes on fragments.
- Adds A–H qualification mapping and release-blocking convergence tests.

## 26.10.0 — Enterprise GA

- Establish the first production release under the `YY.MM.VV` version
  scheme.
- Make Artifact Contract v2, typed artifacts, SABSA/EA projection,
  publication projection, visual QA, behavioral qualification and the
  A–H enterprise gates production controls.
- Replace provider-specific canonical model selectors with configurable
  workload classes: `light`, `standard`, `heavy` and `research`.
- Resolve workload classes through a provider/model registry for Claude
  Code and Codex, with user overrides and extensible classes.
- Add GA release policy, service objectives and a reference support SLA.
- Produce deterministic unsigned build artefacts and require the release
  owner to sign the distribution SHA-256 manifest externally with their
  OpenPGP/GPG key.
- Retain provider parity, reviewer isolation, managed policy, immutable
  execution records, SPDX SBOM, interoperability conformance and
  generated-document drift controls as release gates.
