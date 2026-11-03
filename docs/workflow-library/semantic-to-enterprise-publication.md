# Semantic artefact to enterprise publication

## Trigger

A specialist artefact is substantively complete and requires enterprise-grade publication.

## Intended outcome

A released audience-specific publication whose semantic content is traceable to the approved source and has passed semantic and publication gates.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Semantic artefact to enterprise publication workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Owning specialist</strong><p>finalises claims, decisions, assumptions, evidence and acceptance criteria</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Evidence &amp; Rationale Reviewer</strong><p>checks evidence strength, assumptions, alternatives, rationale and residual risk</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Enterprise Publication Editor</strong><p>selects the publication archetype and renders audience-specific DOCX/PPTX/XLSX/HTML/SVG outputs from the exact approved semantic snapshot</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Visual Quality Reviewer</strong><p>checks density, hierarchy, legibility, tables, diagrams, document control and package integrity</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Named authority</strong><p>reviews completed semantic, publication and actual visual evidence and records the human release decision</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-semantic-to-enterprise-publication.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Owning specialist | finalises claims, decisions, assumptions, evidence and acceptance criteria | semantic publication model | Semantic source is complete enough to review; unresolved items are explicit |
| 2 | Evidence & Rationale Reviewer | checks evidence strength, assumptions, alternatives, rationale and residual risk | semantic gate result and located findings | Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking |
| 3 | Enterprise Publication Editor | selects the publication archetype and renders audience-specific DOCX/PPTX/XLSX/HTML/SVG outputs from the exact approved semantic snapshot | rendered publication set with semantic hash | All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release |
| 4 | Visual Quality Reviewer | checks density, hierarchy, legibility, tables, diagrams, document control and package integrity | publication gate result and findings | Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking |
| 5 | Named authority | reviews completed semantic, publication and actual visual evidence and records the human release decision | release approval | Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers |

## Running this workflow: operator and implementer boundary

Use the next prompt in the provider conversation, not as a shell command.
You supply permitted inputs, actual owners, gate acceptance and authority for
real-system changes. The agent returns evidence and blockers; a listed stage
is not proof of execution, approval or release.

For consequential work, explicitly start `/layered` or `$workflow-layered`;
natural-language routing does not universally enforce Fabric. L0 authority
remains human, and Codex protected authority commands require the human's
trusted terminal. Follow the [interaction model](../using/interaction-model.md),
[layered engagement](../using/layered-engagement.md) and
[human authority](../operations/human-authority.md). Keep the workflow-specific
stop conditions and gates on this page.

## How to use this workflow

A practical prompt pattern is:

> Apply the `semantic-to-enterprise-publication` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.

Approval and execution are separate handoffs. Candidate preparation stays within explicitly permitted pre-production scope. Every production, pilot, credential or irreversible effect requires prior exact named human authority under the applicable policy. If operational proof is required before a wider approval, obtain separate prior authorisation for the bounded pilot needed to collect it; if no policy route permits collection, stop and consult the authority. Draft rendering and review evidence do not release a publication. An existing policy-permitted waiver must identify the competent human authority, exact gate and scope, and validity period before the gated action; mandatory controls and unsupported factual claims remain blocking.

Semantic-source approval precedes publication editing and is distinct from the final publication-release decision after visual review. Professional Semantic Gate PASS does not itself supply human approval. Preparatory draft work may use only an existing separately permitted route; it cannot bypass the editor's approved-source precondition.
