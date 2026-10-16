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

## Choose a SABSA document and format in the conversation

For SABSA, Markdown is the workflow default. State the viewpoint and audience when requesting another format: “Produce the Logical Security Architecture in English as LaTeX and PDF from the reviewed sources; show draft reasons and rendered-QA evidence.” In Claude prefix that request with `/sabsa document <library>`; in Codex use `$workflow-sabsa document <library>`. Ask for DOCX if a Word review is needed. This selects existing publication formats rather than changing a global output setting.

Six distinct viewpoint profiles provide business context, security concept, logical architecture, physical design, component engineering and operational assurance. Each combines authored chapter prose with complete element fields and bodies, provenance and typed business paths. Canonical entry Markdown and `narratives/<layer>/` chapter files are semantic inputs; generated documents are audience projections. Review and correct the inputs before regenerating the output. Missing narrative and unresolved claims remain visible as publication gaps.

You can also ask for editable CSV catalogues. Export the current local entries, retain stable IDs and schema, validate proposed edits, then import them into canonical sources and re-review. Imports update existing local IDs; they do not create a competing CSV authority, replace narrative prose or approve changes. Source changes invalidate earlier snapshot approval.

Markdown needs no external document renderer. Emitting TeX or DOCX uses Pandoc; compiling the controlled PDF edition also needs XeLaTeX, installed TeX packages and the selected fonts. Independently render and inspect the formats actually delivered. LibreOffice/Word supports Office visual QA; the SABSA TeX/PDF path does not invoke an Office renderer. See the [publication stack](../configuration/publication-stack.md) for dependencies and gates.

The [How to use JAI series](../examples/how-to-use-JAI/index.md) demonstrates these choices inside a security assessment and an iterative Android project. Successful generation is one check; architecture approval and a product release decision remain separate statuses.
