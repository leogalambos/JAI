# Compatibility matrix

## Runtime/tooling compatibility

| Component | Minimum | Tested | Supported |
| --- | --- | --- | --- |
| Claude Code | provider-supported | adapter contract | yes |
| Codex CLI | provider-supported | adapter contract | yes |
| Python | 3.10 | 3.12 release CI target | yes |
| Pandoc | optional | publication tool detects at runtime | optional |
| LibreOffice | optional | publication tool detects at runtime | publication |
| lxml | 5.x | XSD conformance suite | EA conformance |
| jsonschema | 4.x | Draft 2020-12 | semantic schemas |
| Pillow | runtime-supported | visual QA fixture rendering | visual QA |
| GitHub Actions | tag-triggered release workflow | A–H, ZIP/SHA-256 and publication | automated release publishing |

## Data/schema compatibility from the 26.10.4 baseline

| Source release | Read/migrate | Current write |
| --- | --- | --- |
| 26.10.0 | supported | no |
| 26.10.1 | supported | no |
| 26.10.2 | supported | no |
| 26.10.3 | supported | no |
| **26.10.4 and later (same v3 contract)** | native | **yes** |

Migration is forward-only. Historical schema namespaces and migration sources are intentionally retained so that previous data can be interpreted without pretending it originated in the current release.

See [26.10.4 release and migration](release-migration.md) for subsystem-specific behavior.
