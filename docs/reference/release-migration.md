# Historical 26.10.4 release and migration

This page records the frozen 26.10.4 release baseline. For releases built from newer tags, active artifact writes use stable `ArtifactContract-v3` rather than a new product-numbered schema; signing/publication follows the current `release-policy.json`.

## Versioning rule

Production versions are `YY.MM.VV`:

- `YY` — year;
- `MM` — month;
- `VV` — version within that month.

For that reason the Unified Lifecycle GA target completed in October 2026 is **26.10.4**, not 26.11.0.

## Native and legacy namespaces

26.10.4 is the only current production-write namespace. Earlier supported versions are compatibility inputs.

| Source | Read | Forward migrate | Native write |
| --- | --- | --- | --- |
| 26.10.0 | yes | yes | no |
| 26.10.1 | yes | yes | no |
| 26.10.2 | yes | yes | no |
| 26.10.3 | yes | yes | no |
| **26.10.4** | **yes** | n/a | **yes** |

Migration is forward-only. Production downgrade writes are not part of the compatibility contract.

## Preservation rules

Migration is designed to preserve:

- stable/canonical identifiers;
- original source hashes and provenance;
- material relations;
- execution/audit history;
- lifecycle/retention metadata where represented;
- prior schema/release identity as migration provenance.

Historical audit records are never rewritten to look as though they originated in 26.10.4.

## Corrective repack rule

The final 26.10.4 corrective repack fixed stale current-release identity in:

- `.ai/runtime/roles.json`;
- `.ai/runtime/workflows.json`;
- EA operator-facing current-state descriptions;
- the current 26.10.4 EA schema title.

The following `26.10.3` references are intentionally preserved and should **not** be mass-replaced:

- the historical `schema/26.10.3` namespace and its `$id` metadata;
- `migrate-26.10.3.py` and migration fixtures;
- compatibility read lists for 26.10.3 Artifact Contract v3;
- EA legacy schema-version allowlists used for read/migrate;
- 26.10.3 carry-over audit/changelog history;
- historical SBOM paths that contain prior release names.

The rule is:

> Current release-owned catalogue metadata, operator-facing current-state descriptions and current schema titles must match `VERSION`; historical, migration and backward-compatibility references retain the version they describe.

## Upgrade behavior by subsystem

### Artifact contracts

Artifact Contract v3 is the production authority. Earlier v3 namespaces and the frozen v2 baseline can be read/migrated through explicit compatibility code; new production contracts are written as 26.10.4 v3 structures.

### SABSA

Legacy libraries remain readable. New or modified objects gain the profile-native JAI semantic identity expected by 26.10.4.

### EA repository

Repositories with schema versions `26.10`, `26.10.1`, `26.10.2` and `26.10.3` are accepted for read/migrate. Once written by the current runtime they use the 26.10.4 EA-domain projection schema and JAI semantic-identity authority.

### Publication

Current production rendering uses ProjectionManifest v3 and JAI lineage. Older semantic material can be migrated/loaded according to its compatibility contract, but current production render evidence belongs to 26.10.4.

### Runtime records

New Execution Records are 26.10.4 runtime-profile/L6 records. Existing historical execution evidence remains historical.

## Automated release from a Git tag

To publish a new production distribution, push a tag named
`release@YY.MM.VV` on an existing commit from `main`. GitHub Actions
prepares the product identity from the tag, runs the A–H gates, builds
and checks the ZIP, and **immediately publishes** a GitHub Release named
`YY.MM.VV`. This flow has no draft, manual approval or GPG signature step.

The published Release contains the ZIP, SHA-256 checksum, SBOM,
provenance and qualification results. GitHub OIDC/Sigstore attestations
are added automatically where the repository plan supports them;
SHA-256 alone does not prove publisher identity.

The historical 26.10.4 release documentation describes its former
external-signature process; it does not govern releases created by the
current automated workflow.

## Upgrade checklist

1. Back up local configuration and any local policy/model-routing overrides.
2. Run the installer in dry-run mode.
3. Resolve collisions or locally modified managed files before forcing an update.
4. Validate existing EA/SABSA/artefact repositories before migration.
5. Install/update 26.10.4.
6. Re-run structural validation and any local provider parity checks.
7. For consequential layered engagements already in progress, preserve their `.fabric` history; do not rewrite old records simply to change a release number.
8. Requalify deployment-specific provider/model behavior if the deployment claims a live provider/model behavioral assurance statement.

<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../compatibility/"><small>← Previous · Reference</small><strong>Compatibility matrix</strong></a>
  <a class="ai-next" href="../limitations/"><small>Next · Reference →</small><strong>Boundaries and limitations</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
