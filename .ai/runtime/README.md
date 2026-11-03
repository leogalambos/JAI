# JAI common runtime

This provider-neutral runtime supplies the full role catalogue, workflow chains,
SABSA-layer processing, schemas and tools to both Claude Code and Codex.

Operators work through their provider prompts and workflow commands. Ordinary
role work and workflows do not require a full matrix. For layered engagements,
the native parent supplies exact adjacent-layer handoffs and independent local
review; reserved human decisions use the external signing companion.

The runtime records immutable versioned inputs and scoped applicability in the
current journal format. New inputs do not rewrite historical records or inherit
acceptance. Keep the journal, referenced files and session locator together for
recovery. Start new engagements rather than importing acceptance from older
unsupported formats.

Use the installed `GUIDE.md` for commands and maintained public operating
instructions. This package contains no private signing key or signing authority.

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
