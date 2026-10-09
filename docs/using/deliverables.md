# Working with deliverables

Enterprise teams usually care about outputs. AI IT House is designed around that reality.

## Start with the requested output, not a renderer command

In Claude or Codex, specify the audience, exact decision, source evidence, mandatory sections, classification and formats. For example: "Prepare an ARB decision pack from these reviewed ADRs and risks; show omissions and unresolved claims; render DOCX and PPTX only after the semantic review." The provider should coordinate the artifact contract, publication projection, renderer and visual checks within its permitted tools. The engineer can inspect individual `publication.py`/`projection.py` commands in the [technical reference](../reference/runtime-tools-detailed.md), but a normal user need not issue them in a shell.

**Boundary:** a rendered file is not automatically an approved decision. Ask for artifact IDs, evidence provenance, semantic/projection/render hashes when relevant, QA outcome and authority status.

## Deliverable journey

1. identify the required outcome;
2. select the role(s) or workflow;
3. build or analyse the semantic content;
4. review the result;
5. project it into the target publication archetype;
6. render and visually check the final file.

## Typical deliverable families

- strategy and decision artefacts;
- architecture definitions and review packs;
- solution and detailed designs;
- risk and assurance packs;
- implementation specifications;
- migration and cutover packages;
- operational handover packs;
- audit and compliance evidence packs.

## Good working habit

Ask first for the **decision owners, required artefacts and review gates**. That consistently produces stronger work than asking for a long document without governance context.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../workflows/"><small>← Previous · Using the system</small><strong>Enterprise workflows</strong></a>
  <a class="ai-next" href="../demo-estate/"><small>Next · Using the system →</small><strong>Learning with the demo estate</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
