# JAI — AI IT House

Human-governed AI assistance for enterprise IS/IT, architecture, security and
delivery, available through Claude Code and Codex.

JAI combines a complete professional role catalogue, maintained enterprise
workflows and a versioned layered delivery core. AI prepares work and evidence;
accountable humans retain reserved decisions, deployment and publication authority.

## Three ways to use JAI

| Mode | Choose it when | Start here |
| --- | --- | --- |
| A specialist role | You need a bounded professional question, analysis or deliverable | [Role selection](docs/using/roles.md) and the [complete catalogue by category](docs/reference/roles.md) |
| A workflow | You need an ordered process involving several responsibilities | [Workflow guide](docs/using/workflows.md) and all [24 enterprise workflow chains](docs/reference/workflows.md) |
| The layered matrix | You need a traceable solution from business intent to realisation and management | [Layered engagement](docs/using/layered-engagement.md) |

The [mode selection guide](docs/using/usage-modes.md) gives examples and explains
how to work incrementally. The full catalogue contains 286 professional roles.
The 17 provider-facing commands are entry points into JAI; they are distinct
from the 24 enterprise workflow chains.

## The layered model

| Perspective | Main concern |
| --- | --- |
| L1 Contextual | Business purpose, stakeholders, scope, constraints and required qualities |
| L2 Conceptual | Principles, domains, trust, strategies and control objectives |
| L3 Logical | Technology-independent services, information and control behaviour |
| L4 Physical | Concrete technical and organisational mechanisms |
| L5 Component | Components, interfaces, configuration and implementation detail |
| L6 Management | Governance, assurance, operation, support and improvement |

Each perspective addresses What, Why, How, Who, Where and When. Management
concerns also apply across the other perspectives.

Inside each layer, a setter establishes the question, an author proposes a
candidate and an independent reviewer assesses it. The local entities choose
their own professional specialties from the complete catalogue. Reviewed answers
are integrated before the neighbouring layer accepts their exact handoff.

Work progresses through bounded steps and durable checkpoints. Pausing and
resuming do not require regenerating completed work. Partial progress does not
imply completion or release of the entire matrix. See the
[layer model](docs/architecture/sabsa-layer-model.md).

## Justification that survives change

Inputs, assumptions, claims, evidence, reviews and decisions refer to explicit
versions. An owner-led change records new material and explicitly cancels affected
applicability and dependent permissions without rewriting historical truth.
New results do not inherit old positive reviews automatically.

Authorisation to continue, acceptance of a specific output and permission to
release it are separate decisions. An obsolete record outside the output's
relevant justification does not block all work; missing required current
evidence still blocks the affected result.

Only reserved human decisions require signatures. The installer offers confirmed
creation of a private operator key and preserves existing keys by default.
The [host signing procedure](docs/operations/human-authority.md) uses the default
key location or an explicit alternative. Ordinary work records are unsigned.

## Install and begin

The optional [Fabric Explorer](docs/fabric-explorer/index.md) provides local,
read-only visual exploration of Fabric and findings. It is distributed and
installed separately as a prebuilt desktop package; the JAI installer below
does not build or install it.

From a repository clone, the separate viewer installer can explicitly build
and install the current platform's development package:

```sh
./install-viewer.sh --build --allow-development
```

Windows uses `install-viewer.cmd` with the same flags. See the
[viewer installation guide](docs/fabric-explorer/installation.md) for build
prerequisites and installation from an existing package without Node.js.

From the reviewed source checkout, inspect the installation plan and apply it
in your host terminal:

```sh
bash ./install.sh --dry-run
bash ./install.sh
```

See [installation](docs/getting-started/install.md) for prerequisites, provider
selection, signing-key confirmation and deployment paths. Start a new provider
session after installing its projections.

Then describe the desired result and relevant sources in Claude Code or Codex.
For the full matrix, use `/layered` in Claude Code or `$workflow-layered` in Codex.
Users do not create bootstrap JSON or worker transport envelopes.

## Documentation

- [Quick start](docs/getting-started/quick-start.md)
- [Three usage modes](docs/using/usage-modes.md)
- [Roles by professional category](docs/reference/roles.md)
- [Enterprise workflow catalogue](docs/reference/workflows.md)
- [Provider command reference](docs/reference/commands.md)
- [Complete installed CLI guide](docs/reference/installed-cli-guide.md)
- [Deployment and recovery](docs/operations/gen2-deployment-recovery.md)
- [Human authority](docs/operations/human-authority.md)
- [Boundaries and limitations](docs/reference/limitations.md)
- [Prepared version changes](CHANGELOG.md)

Build the documentation locally with the repository's Python dependencies:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

The source CLI guide is canonical. Its runtime source alias is a symlink;
installation materialises the guide's bytes for offline use. Building the site
does not install the runtime.

## Version and publication

`VERSION` identifies the product version. The current prepared version is
**26.11.0**. Preparation of source or documentation does not announce publication.
Maintainers follow the [version and release procedure](docs/reference/versioning.md);
creating or pushing a release tag is a separate owner action.

JAI does not guarantee arbitrary professional truth, provide enterprise identity
management or replace the provider's effective sandbox. The current runtime
does not embed Prolog. See the research basis in
[Towards Justifiable AI Systems](https://doi.org/10.13140/RG.2.2.29244.19843).

## Licence and attribution

See [LICENSE](LICENSE) and [licensing and attribution](docs/about/license-attribution.md).

## Current generated inventory

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

---

<div align="center">

**JAI · Justifiable AI** *Not simply an AI-generated answer — a
traceable path from intent to evidence and accountable decisions.*

[Architecture](#the-layered-model) · [Getting started](#install-and-begin) ·
[Version and publication](#version-and-publication)

</div>
