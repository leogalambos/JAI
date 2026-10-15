# Publication stack

Publication is a controlled projection of approved semantics, not a free-standing writing step.

## Chain of custody

<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Architecture and delivery diagram">
<img src="../../assets/diagrams/publication-chain.svg" alt="Enterprise publication chain from semantic source through projection, renderer and visual QA to approval">
</div>

26.10.4 makes the chain profile-native:

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

## ProjectionManifest v3

The manifest binds the publication to both JAI lineage and content identity. It carries the relationship between:

- intent;
- semantic snapshot;
- policy;
- design;
- realisation;
- evidence;
- semantic/projection/render hashes.

The production renderer validates the matching manifest before emitting the supported current-release artefact.

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

<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../policy/"><small>← Previous · Configuration</small><strong>Governance, policy & approvals</strong></a>
  <a class="ai-next" href="../../using/interaction-model/"><small>Next · Using the system →</small><strong>Interaction patterns</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
