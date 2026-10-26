# Compatibility matrix

<!-- GENERATED-INVENTORY:START -->
## Current generated release inventory

This block is generated from canonical package sources by
`.ai/runtime/tools/generate_docs.py`. Manual count edits are not
authoritative.

Supported scope: **GA_COMPATIBLE/2**.

Enabled features: `role-workflows`, `workspace-authoring`,
`local-publication`, `human-git`, `operator-handoff`,
`operator-attested-local-l0`.

- Roles: **286**
- Agents: **34**
- Skills: **24**
- Workflows: **24**
- Artifact Types: **28**
- Schemas: **33**
- Renderers: **4**
- Tests: **32**
- Provider Adapters: **2**

### Compatibility matrix

- **Claude Code**
  - Minimum: provider-supported strict sandbox
  - Tested: not installed on reference host; projections only, live
    NOT_VERIFIED
  - Supported: contract-scoped tools; reviewer shell unavailable without
    read-only isolation
- **Codex CLI**
  - Minimum: provider-supported
  - Tested: 0.164.0 host CLI help confirms sandbox/on-request values;
    live role confinement NOT_VERIFIED
  - Supported: role-authorized local QA in effective native sandbox
- **Python**
  - Minimum: 3.10
  - Tested: 3.12 release CI target
  - Supported: yes
- **Pandoc**
  - Minimum: optional
  - Tested: publication tool detects at runtime
  - Supported: optional
- **WeasyPrint**
  - Minimum: 70.x optional
  - Tested: actual HTML/PDF conversion; constrained resource fetching
  - Supported: SUPPORTED optional HTML/PDF; not Office fidelity
- **Pyphen**
  - Minimum: 0.17.x optional
  - Tested: clean optional renderer environment required; metadata
    inspection avoids legacy pkg_resources import
  - Supported: WeasyPrint transitive dependency constrained in
    requirements-rendering.txt
- **LibreOffice**
  - Minimum: Office-compatible host renderer
  - Tested: actual DOCX/PPTX/XLSX operator renders on Fedora
  - Supported: AUTO when native sandbox permits; otherwise
    OPERATOR_ASSISTED actual Office QA
- **Poppler**
  - Minimum: pdftoppm on PATH
  - Tested: actual PDF page rasterization
  - Supported: visual QA raster prerequisite
- **OpenSSL**
  - Minimum: Ed25519 pkeyutl -rawin
  - Tested: external receipts verified with fixed /usr/bin/openssl on
    Linux
  - Supported: OPERATOR_ASSISTED local L0; other trust adapters
    NOT_VERIFIED
- **Fonts/system libraries**
  - Minimum: DejaVu Sans; renderer-native text/layout libraries
  - Tested: Fedora reference glyph/layout corpus
  - Supported: host prerequisite; other platforms NOT_VERIFIED
- **lxml**
  - Minimum: 5.x
  - Tested: XSD conformance suite
  - Supported: EA conformance
- **jsonschema**
  - Minimum: 4.x
  - Tested: Draft 2020-12
  - Supported: semantic schemas
- **Pillow**
  - Minimum: runtime-supported
  - Tested: visual QA fixture rendering
  - Supported: visual QA
- **GitHub Actions**
  - Minimum: release workflow
  - Tested: tag, A-H gates, ZIP SHA-256, CI publication
  - Supported: automatic release publication
<!-- GENERATED-INVENTORY:END -->

## Runtime/tooling compatibility

Current tooling is generated below from the release manifest. Presence of a
binary is not proof of confinement or actual-format visual fidelity.

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