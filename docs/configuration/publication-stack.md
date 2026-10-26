# Publication stack

After changing optional tools or Python environments, use
`python3 ~/.ai/it-role-house/tools/operator_actions.py configure --refresh`.
See [automatic discovery and refresh](../getting-started/install.md#reconfigure-jai-after-installing-additional-tools).
Explicit backend arguments take precedence over automatic selection. Every
conversion checks the actual selected tool again; discovery is not a render
receipt or permission to leave the sandbox.

Publication is a controlled projection of approved semantics, not a free-standing writing step.

## Chain of custody

<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Architecture and delivery diagram">
<img src="../../assets/diagrams/publication-chain.svg" alt="Enterprise publication chain from semantic source through projection, renderer and visual QA to approval">
</div>

The publication profile connects the six layers:

```text
L1 intended audience / decision / authorised use
  ↓
L2 semantic material available for publication
  ↓
L3 inclusion, omission, evidence and release rules
  ↓
L4 publication/document design
  ↓
L5 renderer and output implementation
  ↓
L6 rendered artefact + hashes + visual evidence
```

## Current DCS-bound projection manifest

The manifest binds the publication to both JAI lineage and content identity. It carries the relationship between:

- intent;
- semantic snapshot;
- policy;
- design;
- realisation;
- evidence;
- semantic/projection/render hashes.

The current content-aware renderer validates the matching DCS-bound v4
manifest and hash-bound QA sidecars. Historical v3 lineage remains readable
for compatibility; it does not satisfy the current render boundary. See
[DCS publication integrity](../capabilities/document-content-specifications.md).

## Why the projection layer matters

A single semantic source may be used to create an executive one-pager, ARB pack and technical design. Those documents should not all contain the same detail, but each must be able to demonstrate that mandatory content for its audience/use was included and that omissions were permitted rather than accidental.

## Publication archetypes

The release ships thirteen first-class archetypes, including:

- Executive One-Pager;
- Decision Paper;
- Architecture Review Board Pack;
- Architecture Definition;
- Solution Design / HLD;
- Detailed Design / LLD;
- Risk & Assurance Pack;
- Implementation Specification;
- Migration & Cutover Pack;
- Operational Handover;
- Roadmap;
- Benefits Review;
- Audit / Compliance Evidence Pack.

## Output formats

The publication stack supports first-class enterprise outputs such as HTML, DOCX, PPTX and XLSX, with PDF/SVG/EA interchange used where the relevant renderer/profile applies.

For SABSA documentation, Markdown is the default. Explicit LaTeX source and DOCX requests use Pandoc; compiling the LaTeX PDF additionally needs XeLaTeX, TeX packages and fonts. Office rendering for visual QA is a separate optional dependency from DOCX generation. See [sandbox and environment prerequisites](../getting-started/sandbox-prerequisites.md) for the dependency/access matrix and [deployment notes](../getting-started/deployment-notes.md) for controlled build qualification.

## Semantic, projection and render identity

Do not collapse the three hashes:

```text
semantic_hash   = what the approved semantic source was
projection_hash = what this audience/use was supposed to receive
render_hash     = the exact emitted file
```

The separation is essential for detecting both content omission and post-render file changes.

## Visual QA

Render-based visual QA checks the visible result after rendering. It complements, rather than replaces, semantic review and ProjectionManifest coverage checks.

## 26.10.14 actual-format rendering

HTML/PDF prefers optional WeasyPrint 70 with URL fetches and custom font-face
loads denied. System fonts remain host dependencies. Host LibreOffice is a
reference/fallback, not a required in-sandbox service. Actual DOCX/PPTX/XLSX
bytes receive their own native PDF/raster evidence; HTML PDF is not their QA.
Receipts bind hashes, tool/version, profile, command and actual pages.

Office retains editable text/tables and diagram topology; HTML/PDF/SVG provides
vector diagrams. Native Office vector shape embedding is not claimed. Layout
and pagination differ by backend; inspect actual outputs. The evaluated corpus
covers diacritics, long tables, multipage output, document control, a diagram,
substantive slides and a workbook. LibreOffice HTML import flattens inline SVG
and paginates differently; WeasyPrint is preferred for HTML/PDF fidelity.

See [operator walkthrough](../operations/operator-walkthrough.md) for prepare, render,
verify and resume. Critical QA thresholds and hashes remain mandatory. Missing
rendering produces an explicit handoff, never a fake PASS.

## Dependencies by task

Do not install every optional tool to start core authoring. Python package
imports use the interpreter invoking JAI, not whichever `pip` happens to be
on PATH. For a clean renderer venv, follow [installation](../getting-started/install.md#a-clean-optional-renderer-environment).

| Task | Dependency | Where / prerequisite | Scope |
| --- | --- | --- | --- |
| Core contracts, Fabric and structured workflows | Python 3.10+, jsonschema and PyYAML from requirements.txt | JAI's Python interpreter | Required for applicable core validation |
| Build the documentation website | MkDocs, Material and pymdown-extensions; mistune for Markdown processing | Maintainer/docs environment; requirements.txt includes these convenience dependencies | Development/documentation, not a native provider prerequisite |
| HTML/CSS to PDF | WeasyPrint 70, Pyphen 0.17.x; Pango/HarfBuzz/Fontconfig libraries and usable fonts | Same Python/venv as JAI render command, plus host libraries | Optional; no Office fidelity claim |
| Actual DOCX/PPTX/XLSX visual review | LibreOffice or qualified Office renderer, usable fonts and writable temporary profile | Agent sandbox if available, otherwise reviewed host C action | Optional; actual Office bytes must be rendered |
| PDF page images/text | Poppler pdftoppm / pdftotext, Pillow for image analysis | Renderer/QA host; executables on PATH | Applicable visual QA |
| SVG visual QA | CairoSVG, Cairo libraries, Pillow | QA Python interpreter and host libraries | Optional diagram QA |
| SABSA DOCX / LaTeX source | Pandoc | Publication host PATH | Optional; standard publication DOCX generation itself does not require Pandoc |
| Compile LaTeX PDF | XeLaTeX, TeX packages and document fonts | Publication host PATH | Optional; not required for HTML PDF |
| Local browser screenshots | Chromium and writable disposable profile | Effective native sandbox or explicit host C task | Optional; no unsafe sandbox-disabling flags |
| Signed Fabric L0 | OpenSSL with Ed25519 support, separate operator key and protected public pin | Signer outside agent access; verifier needs only trusted public key | Optional formal decisions, not first-run authoring |
| EA XSD conformance | lxml | JAI validation interpreter | Task-specific validation |
| Qualification regression | requirements-ci.txt | Disposable developer/release environment | Development only |

Example Fedora host packages, for the human operator to review and install
only when that task is needed:

```sh
sudo dnf install libreoffice poppler-utils dejavu-sans-fonts
```

For browser QA, `chromium` is a separate optional Fedora package. Pandoc and
`texlive-xetex` serve the SABSA/LaTeX path; they are not PDF backend substitutes
for actual Office visual review. Other systems use their native package tools.
The agent never runs package installation as an implicit authorization grant.

Host rendering of untrusted documents requires appropriate containment.
Never use sudo just to render, widen provider permissions, or interpret a
renderer failure as FORMAL_L0. A/B/C are execution routes; D remains a
separate signed decision requirement. See the
[operator walkthrough](../operations/operator-walkthrough.md).
