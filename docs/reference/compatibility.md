# Compatibility matrix

Local availability is separate from product support. The installer runs bounded
optional discovery; [refresh it after tool changes](../getting-started/install.md#reconfigure-jai-after-installing-additional-tools).
Version probes use portable Python subprocesses, but actual rendering and
provider confinement remain environment-dependent and are not certified by discovery.

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
- Agents: **27**
- Skills: **24**
- Workflows: **24**
- Artifact Types: **28**
- Schemas: **33**
- Renderers: **4**
- Provider Adapters: **2**

### Compatibility matrix

- **Claude Code**
  - Minimum: provider-supported
  - Supported: Native role and workflow projections; effective isolation
    depends on the host sandbox.
- **Codex CLI**
  - Minimum: provider-supported
  - Supported: Native role and workflow skills; effective isolation
    depends on the host sandbox.
- **Python**
  - Minimum: 3.10
  - Supported: Standard-library installation; runtime contract workflows
    also require their declared dependencies.
- **Pandoc**
  - Minimum: optional
  - Supported: Optional document conversion.
- **WeasyPrint**
  - Minimum: 70.x optional
  - Supported: HTML/PDF publication using a CLI-first/current-Python
    fallback with constrained resource fetching; not Office fidelity.
- **Pyphen**
  - Minimum: determined by the installed WeasyPrint dependency
    requirements
  - Supported: WeasyPrint transitive dependency; the optional pip recipe
    selects 0.17.x without rejecting working OS packages.
- **LibreOffice**
  - Minimum: Office-compatible host renderer
  - Supported: Office document rendering in the native sandbox when
    available, otherwise through an explicit operator handoff.
- **Poppler**
  - Minimum: pdftoppm on PATH
  - Supported: PDF page rasterization for visual inspection.
- **OpenSSL**
  - Minimum: Ed25519 genpkey and pkeyutl -rawin
  - Supported: Host-confirmed key creation and explicit human signing;
    private keys stay outside agent access.
- **Fonts/system libraries**
  - Minimum: DejaVu Sans and renderer-native layout libraries
  - Supported: Required by the selected rendering tools.
- **lxml**
  - Minimum: 5.x
  - Supported: Architecture exchange conformance checks.
- **jsonschema**
  - Minimum: >=4.18,<5
  - Supported: Required for runtime contract validation; not required
    for installation.
- **Pillow**
  - Minimum: runtime-supported
  - Supported: Image inspection and visual QA.
- **GitHub Actions**
  - Minimum: release@YY.MM.VV tag workflow
  - Supported: Validated source archives and checksums are published
    only after a matching release tag is pushed.
<!-- GENERATED-INVENTORY:END -->

## Generation and data compatibility

**Gen2 is the 26.11.xx release family; Gen1 is the preceding 26.10.xx family.**
The professional catalogue and provider-facing workflows remain available, but
the engagement evaluator and current-applicability model have changed.

| Material | Gen2 treatment | Acceptance boundary |
| --- | --- | --- |
| Current journal-format-9 engagement | Resume through its recorded locator and actual durable state | Preserve exact inputs, decisions and applicable permissions; reconcile uncertain invocations before new work |
| Unsupported earlier engagement journal | Keep as an immutable historical archive and start a fresh Gen2 engagement from authorised inputs | No journal migration, imported PASS result or inherited acceptance/release permission |
| Retained professional-domain model | Use the supported reader and current write contract for that specific domain/profile | A domain reader does not establish a Gen2 execution history or accept the model for a new use |
| Earlier publication representation | Apply the publication profile's explicit read/render boundary | Readable historical lineage alone does not satisfy current content, rendering or release requirements |

Compatibility belongs to the named subsystem and schema, not merely a product
version interval. Retained domain readers may interpret their supported old
representations; this is not a release-wide promise to migrate Gen1 engagements.
Use [startup and recovery](../operations/lifecycle-recovery.md) for a new
engagement and [versioned applicability](../architecture/governed-runtime-cutover.md)
for current input changes. The [publication stack](../configuration/publication-stack.md)
explains its separate manifest boundary.
