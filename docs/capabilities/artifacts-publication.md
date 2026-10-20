# Publication and visual QA

## How a reader uses publication in Claude/Codex

**Operator:** provide reviewed semantic inputs, specify the business decision, intended audience, archetype and formats. Request `/publish ...` in Claude or `$workflow-publish ...` in Codex; ask for mandatory-content coverage, omissions, rendered output locations and visual-QA evidence. The operator does **not** run `publication.py` or `projection.py` as separate manual steps. **Behind the scenes:** the provider agent creates/checks the artifact and projection contracts, invokes the renderer under its permissions and gathers the actual QA result. A generated file, a renderer self-test and an authorised publication are different statuses; unresolved claims and required human approvals must remain visible. See [deliverables](../using/deliverables.md) and the [developer reference](../reference/runtime-tools-detailed.md).

## Typed artefact taxonomy

SABSA also has a domain-native document path through `/sabsa document` (Claude) or `$workflow-sabsa document` (Codex). Its six narrative viewpoint profiles combine authored semantic chapters, complete specifications and typed business traceability; they can emit Markdown, controlled LaTeX/PDF and Word. Editable CSV catalogues use a separate export/validate/import exchange around canonical local entries. The generic `/publish` projection contracts described below should not be confused with the SABSA renderer's own snapshot and draft checks. See [SABSA documents and catalogues](sabsa-ea.md#latex-documents-and-editable-csv-catalogues).

For SABSA the conversation default is Markdown. Ask naturally for a viewpoint and formats, such as “Component Engineering Specification as LaTeX and PDF”; request DOCX when needed. Authors supply reviewed narrative rather than asking a renderer to invent it. TeX emission needs Pandoc, controlled PDF compilation adds XeLaTeX and fonts, and DOCX generation uses Pandoc. Required visual QA applies to the files produced; Office conversion is not a prerequisite for producing SABSA TeX/PDF. The [worked tutorials](../examples/how-to-use-JAI/index.md) place these choices in an engagement.

The current taxonomy defines **28 artefact classes**.

| Artifact type | Production mode | Render targets | Acceptance profile |
| --- | --- | --- | --- |
| `architecture-definition` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `architecture-decision` | internal | html, docx, pptx, xlsx | decision-defensible |
| `solution-design` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `decision-paper` | internal | html, docx, pptx, xlsx | decision-defensible |
| `business-case` | internal | html, docx, pptx, xlsx | decision-defensible |
| `risk-assessment` | internal | html, docx, pptx, xlsx | evidence-assured |
| `assurance-report` | internal | html, docx, pptx, xlsx | evidence-assured |
| `control-design` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `implementation-specification` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `migration-plan` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `cutover-plan` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `operational-readiness-assessment` | internal | html, docx, pptx, xlsx | evidence-assured |
| `service-design` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `runbook` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `test-strategy` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `test-report` | internal | html, docx, pptx, xlsx | evidence-assured |
| `benefits-review` | internal | html, docx, pptx, xlsx | decision-defensible |
| `roadmap` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `register` | internal | html, xlsx, docx | enterprise-publication |
| `dashboard` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `presentation` | internal | pptx, html | enterprise-publication |
| `dataset` | internal | html, xlsx, docx | enterprise-publication |
| `catalogue` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `document` | internal | html, docx, pptx, xlsx | enterprise-publication |
| `diagram` | internal | svg, html, docx, pptx | model-conformance |
| `model` | internal | open-exchange, json, svg | model-conformance |
| `prototype` | external_handoff | external/type-specific | engineering-handoff |
| `configuration-baseline` | external_handoff | external/type-specific | configuration-handoff |

## Artifact Contract v3

The current production contract is JAI-native. It composes artefact concerns across L1–L6 rather than treating publication as a flat set of fields.

A simplified mapping is:

| JAI layer | Artefact concern |
| --- | --- |
| L1 | purpose, audience, owner, intended decision/use |
| L2 | artefact type, schema, required inputs/relations |
| L3 | evidence/review/acceptance and policy obligations |
| L4 | mandatory sections/views/diagram requirements |
| L5 | producer, renderer, formats, system-of-record/handoff |
| L6 | actual validation/evidence and semantic/projection/render hashes |

Artifact Contract v2 remains compatibility input only; current production writes use the release-independent `ArtifactContract-v3` identity.

## Projection and integrity model

A production audience artefact is generated through:

```text
semantic source
→ publication profile
→ DCS-bound ProjectionManifest v4
→ publication model with JAI lineage
→ renderer
→ render evidence / visual QA
→ approval / publish
```

Three SHA-256 identities remain distinct:

- **semantic hash** — source semantic snapshot;
- **projection hash** — audience-specific content selection/mapping;
- **render hash** — exact emitted file.

This prevents a polished document from implying that it is complete merely because it carries the hash of a richer semantic source.

## Mandatory coverage and omissions

A publication profile declares which semantic fields/sections are mandatory. A production projection is expected to reach 100% mandatory coverage unless a permitted omission is explicitly justified by the profile/contract.

Material claims and evidence must either be represented in the audience projection or be excluded under a rule that allows the omission for that use.

## Production render boundary

The current content-aware renderer requires the matching DCS-bound v4
manifest and QA sidecars. Historical v3 manifests remain compatibility
inputs; they do not authorize a new render. Directly rendering a semantic model without the projection contract is not the profile-native production path.

Render output is accompanied by evidence such as file hashes and QA outcomes so that the concrete published file can be distinguished from the semantic/projection state that produced it.

## Visual QA

Render-based visual QA complements semantic integrity by inspecting what a human actually sees. Relevant defect classes include:

- clipping/overflow;
- blank or nearly blank outputs;
- broken/empty diagrams;
- extreme text density;
- unreadable labels/fonts;
- tables beyond the page;
- missing legends/context;
- overlapping elements;
- broken TOC/cross-references or required document controls.

A visually correct artefact can still be semantically wrong; a semantically correct source can still be unusable when rendered. The gates remain separate for that reason.
