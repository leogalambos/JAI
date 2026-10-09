# AI IT House — Enterprise GA

This release combines the provider-neutral AI IT House runtime,
executable agent/command/skill contracts, governed enterprise artifact
production, JAI/SABSA/EA capabilities, release qualification, and a
**single maintained Markdown manual** rendered by MkDocs Material.
Claude Code and Codex CLI use their native commands and skill
adapters; an installed HTML help site is neither needed nor included.

<!-- GENERATED-INVENTORY:START -->
## Current generated release inventory

This block is generated from canonical package sources by
`.ai/runtime/tools/generate_docs.py`. Manual count edits are not
authoritative.

- Roles: **281**
- Agents: **33**
- Skills: **23**
- Workflows: **24**
- Artifact Types: **28**
- Schemas: **32**
- Renderers: **4**
- Tests: **32**
- Provider Adapters: **2**

### Compatibility matrix

- **Claude Code**
  - Minimum: provider-supported
  - Tested: adapter contract
  - Supported: yes
- **Codex CLI**
  - Minimum: provider-supported
  - Tested: adapter contract
  - Supported: yes
- **Python**
  - Minimum: 3.10
  - Tested: 3.12 release CI target
  - Supported: yes
- **Pandoc**
  - Minimum: optional
  - Tested: publication tool detects at runtime
  - Supported: optional
- **LibreOffice**
  - Minimum: optional
  - Tested: publication tool detects at runtime
  - Supported: publication
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

## Documentation and runtime contracts

The current manual is authored under `docs/` and navigated by
`mkdocs.yml`. The full CLI guide is maintained as
`docs/reference/installed-cli-guide.md`;
`.ai/runtime/GUIDE.md` is its checked generated deployment copy.
Runtime command, agent and skill contracts remain under `.ai/`, where
CLI providers load their operational instructions. They are not HTML
documentation.

The v4.0 manual covers L0 human authority, the six JAI layers, typed
contracts and evidence flow, SABSA and EA profiles, artifact
publication, provider execution boundaries, A–H release gates, and
production workflows. Version 26.10.0 is retained only for authentic
compatibility/migration identities and examples explicitly identified
as originating with that release.

## Key design properties

- Homepage composition remains implemented as HTML/CSS rather than
embedding a screenshot.
- Workflow and architecture diagrams remain deterministic SVG assets
where practical.
- Mermaid authoring remains configured for additional diagrams.
- The desktop navigation and footer behavior from the v3.3 visual
baseline is preserved.
- New layered-runtime diagrams are static local SVGs and therefore do
not depend on a Mermaid CDN to render.

## Corrective v4.0 repack

All current documentation pages are in `mkdocs.yml` navigation and
their local links are checked by `docs_contract.py`. The site uses the
original MkDocs design and SVG visual assets. The runtime CLI guide is
generated from its Markdown page and verified by `generate_docs.py
--check`.

## Build

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Production check:

```bash
python3 .ai/runtime/tools/docs_contract.py --root .
python3 .ai/runtime/tools/generate_docs.py --check --root .
mkdocs build --strict
```

## Release qualification and evidence

The package includes `QUALIFICATION-A-H.json`, `COMPATIBILITY.json`,
`SBOM.spdx.json`, and `PROVENANCE.json` plus authoritative
runtime schema,
policy and JAI registry files. Their recorded qualification scope and
provenance should be checked for **this exact source tree**; an
earlier PASS does not authorize a modified distribution.
The root `VERSION` is the sole product-version authority.
For a new release, edit `VERSION` and run:

```sh
python3 scripts/versioning.py sync
```

Commit/push the result and create a matching `release@YY.MM.VV` tag.
A mismatching tag is rejected. The tag publishes a qualified
production ZIP directly through GitHub Actions with a SHA-256 checksum.
GitHub OIDC provenance is attached automatically where supported;
the runtime integrity checks remain independent of that attestation.

The complete documentation site is rendered by
`.github/workflows/pages.yml` from the Markdown tree. GitHub Pages
publishing is a repository action; it is not performed by installing
the runtime ZIP.
