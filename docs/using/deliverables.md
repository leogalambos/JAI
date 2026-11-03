# Working with deliverables

Enterprise teams usually care about outputs. AI IT House is designed around that reality.

## Start with the requested output, not a renderer command

In Claude or Codex, specify the audience, exact decision, source evidence, mandatory sections, classification and formats. For example: "Prepare an ARB decision pack from these reviewed ADRs and risks; show omissions and unresolved claims; render DOCX and PPTX only after the semantic review." The provider should coordinate the artifact contract, publication projection, renderer and visual checks within its permitted tools. The engineer can inspect individual `publication.py`/`projection.py` commands in the [technical reference](../reference/runtime-tools-detailed.md), but a normal user need not issue them in a shell.

**Boundary:** a rendered file is not automatically an approved decision. Ask for artifact IDs, evidence provenance, semantic/projection/render hashes when relevant, QA outcome and authority status.

## Deliverable journey

1. Identify the required outcome, intended use, recipient and relevant boundaries.
2. Select appropriate [roles](../reference/roles.md) or a [workflow](../reference/workflows.md).
3. Follow the output link to its exact [content contract](../reference/output-contracts/index.md). Read its selected shared foundations and overlays together with the local requirements.
4. Establish the required inputs and evidence. Distinguish required content, conditionally required content, optional additions and prohibited information. Unknown applicability remains unresolved.
5. Produce the actual work product and request independent review against that contract. Correct findings or escalate a deficiency to the owner entitled to resolve it.
6. For a document or audience-specific rendition, project the reviewed semantic content, render the requested formats and inspect their actual bytes. For code, configuration, tests or operational work, use the corresponding executable or operational checks; a rendered description cannot substitute for the work.
7. Submit the exact result and supporting evidence to its receiving handoff. Obtain any separately reserved acceptance or release decision before relying on the result for that use.

These steps explain the reader's path through existing controls. A contract
listed as proposed/advisory does not become an approved external standard merely
because it is selected, and successful validation does not manufacture human
authority.

## Worked example: a rollback procedure for a release

This is a fictional teaching scenario. It describes expected work and decisions,
not an executed deployment, an actual review receipt or release approval.

**Request.** A warehouse team wants a rollback procedure for a read-only stock
dashboard. The change replaces the web application image without changing the
database schema. The request names the target release, environment, receiving
operations team and evidence expected from a rehearsal.

**Select the output.** The Release Engineer's
[rollback procedure and evidence of test](../reference/output-contracts/role-release-engineer.md#output-release-engineer-4)
has contract ID `release-engineer:4`. Its page links the applicable foundations,
including the [runbook requirements](../reference/output-contracts/spec-type-runbook.md).
This supplies a precise starting point instead of a request for a generic
"deployment document".

| Content class | What the example must establish |
| --- | --- |
| Required | Trigger, exact release/environment, operator prerequisites, ordered steps and expected observations, failure/stop conditions, safe recovery, and actual rehearsal evidence with its limits |
| Conditional | Whether personal data is processed and whether regulatory requirements apply; a true condition requires the corresponding analysis, while an unknown condition remains a gap |
| Optional | A supporting annotated rehearsal transcript when it helps the recipient understand a specific step or conclusion |
| Prohibited | Credentials, invented observations or an assertion that a planned rehearsal already passed |

**Prepare and review.** The author produces a draft with correct steps but omits
what to do when the health check fails. The reviewer locates that omission
against the recovery requirement and returns `rework_required`. The reviewer
does not edit the procedure. The author adds a safe-state branch, escalation
contact and evidence from the required rehearsal before asking for a new review.
If no rehearsal has occurred, the evidence remains missing; clearer prose alone
cannot close that finding.

**Resolve a condition.** Suppose the input description does not say whether
operational logs contain personal identifiers. The author requests clarification
from the source owner and keeps privacy applicability unresolved. In the
fictional revised scope, the owner supplies a reviewed data-flow description and
log configuration showing that this dashboard and its rollback use anonymous
aggregate stock counts without personal identifiers. That explicit scope can
support a false privacy condition; merely omitting customer names from the
draft could not. A later input change requires reassessment of affected content.

**Hand over the result.** The
[idea-to-production workflow](../workflow-library/idea-to-production.md#workflow-steps-and-gates)
uses this contract at its release preparation stage. The receiving handoff
includes the exact procedure, release manifest and test evidence; its gate
requires the manifest to state which artefact versions ship where. The procedure
does not satisfy that complete handoff on its own. A supported local review,
receiving acceptance and any reserved human decision remain distinct. JAI can
prepare the exact release request; only the entitled human can sign it when
required.

Markdown is sufficient for this procedure unless the recipient needs another
rendition. Asking for a PDF does not add missing recovery behaviour, execution
evidence or permission to deploy. Conversely, this documentary example does not
require every code or configuration output to pass through a document renderer.

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

## Expert authoring references

The [bundled expert references](expert-reference-documents.md) provide complete
fictional examples at three complexity levels. They support authoring without
replacing registered DCS rules, independent review or existing human authority.
