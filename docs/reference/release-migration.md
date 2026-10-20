# Historical 26.10.4 release and migration

This page records the frozen 26.10.4 release baseline. For releases built from newer tags, active artifact writes use stable `ArtifactContract-v3` rather than a new product-numbered schema; signing/publication follows the current `release-policy.json`.

## Versioning rule

Production versions are `YY.MM.VV`:

- `YY` — year;
- `MM` — month;
- `VV` — version within that month.

For that reason the Unified Lifecycle GA target completed in October 2026 is **26.10.4**, not 26.11.0.

## Native and legacy namespaces

In the historical 26.10.4 baseline, 26.10.4 was the production-write
namespace and earlier supported versions were compatibility inputs. This
statement does not select the namespace for the current release.

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

The historical 26.10.4 baseline used ProjectionManifest v3 and JAI lineage.
Its compatibility contract described how older semantic material could be
migrated or loaded; its production render evidence belonged to that baseline.
For current production rendering and DCS binding, see
[artifacts and publication](../capabilities/artifacts-publication.md).

### Runtime records

New Execution Records are 26.10.4 runtime-profile/L6 records. Existing historical execution evidence remains historical.

## Current release procedure

This page preserves the 26.10.4 baseline; it is not the current release
runbook. Follow [Versioning and release policy](versioning.md) for current
requirements and commands.

The current root `VERSION` is the authoritative product identity. Synchronise
its generated projections with `scripts/versioning.py sync`, check them,
and commit the consistent state before tagging. A `release@YY.MM.VV` tag must
match that committed identity; the tag does not manufacture a replacement
version. Publication remains conditional on the current required checks.

The baseline's former external-signature process does not govern the current
automated workflow. Do not treat historical qualification or compatibility
tables on this page as evidence that a later release has passed its gates.

## Historical 26.10.4 upgrade checklist

1. Back up local configuration and any local policy/model-routing overrides.
2. Run the installer in dry-run mode.
3. Resolve collisions or locally modified managed files before forcing an update.
4. Validate existing EA/SABSA/artefact repositories before migration.
5. Install/update 26.10.4.
6. Re-run structural validation and any local provider parity checks.
7. For consequential layered engagements already in progress, preserve their `.fabric` history; do not rewrite old records simply to change a release number.
8. Requalify deployment-specific provider/model behavior if the deployment claims a live provider/model behavioral assurance statement.
