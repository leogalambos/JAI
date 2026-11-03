# Regulatory change to assurance

## Trigger

A new or changed law, regulation, supervisory expectation or contractual compliance obligation may affect IS/IT services, controls or architecture.

## Intended outcome

Applicability and obligations are translated into traceable requirements/controls, architecture and remediation changes are implemented, evidence is independently assured, and closure is authorised.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Regulatory change to assurance workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Compliance Officer (Technology)</strong><p>records authoritative regulatory change source, effective dates and scope hypotheses</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Compliance Officer (Technology)</strong><p>determines technology applicability with legal/business input where needed</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>GRC Analyst</strong><p>decomposes applicable obligations into traceable obligation records</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Business Analyst</strong><p>translates obligations into atomic/testable business/technology requirements</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Control Owner</strong><p>maps requirements to existing/new controls and identifies gaps</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Enterprise Architect</strong><p>assesses architecture/process/data/service impact and target-state changes</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Portfolio Manager</strong><p>prioritises/funds time-bound remediation according to effective dates and risk</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Control Owner</strong><p>coordinates implementation evidence and control operating proof</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Internal IT Auditor</strong><p>independently tests design/operating evidence against obligation/control criteria</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Compliance Officer (Technology)</strong><p>authorises or routes closure based on assurance and residual exceptions</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-regulatory-change-to-assurance.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Compliance Officer (Technology) | records authoritative regulatory change source, effective dates and scope hypotheses | regulatory change record | Source, jurisdiction, dates and version are attributable |
| 2 | Compliance Officer (Technology) | determines technology applicability with legal/business input where needed | applicability decision | In/out-of-scope rationale and authority are explicit |
| 3 | GRC Analyst | decomposes applicable obligations into traceable obligation records | obligations register | Each obligation retains source citation/context and applicability owner |
| 4 | Business Analyst | translates obligations into atomic/testable business/technology requirements | requirements baseline | Requirements preserve obligation intent and are testable |
| 5 | Control Owner | maps requirements to existing/new controls and identifies gaps | control mapping and gap register | Every requirement maps to effective control evidence or an owned gap |
| 6 | Enterprise Architect | assesses architecture/process/data/service impact and target-state changes | architecture impact assessment | Cross-domain impacts and affected governed models are explicit |
| 7 | Portfolio Manager | prioritises/funds time-bound remediation according to effective dates and risk | remediation roadmap | Mandatory deadlines and dependencies are funded/owned or escalated |
| 8 | Control Owner | coordinates implementation evidence and control operating proof | evidence pack | Evidence is attributable to implemented control version and period |
| 9 | Internal IT Auditor | independently tests design/operating evidence against obligation/control criteria | assurance report | Assurance is independent and reports exceptions/limitations |
| 10 | Compliance Officer (Technology) | authorises or routes closure based on assurance and residual exceptions | closure decision | Closure states remaining exceptions, authority and future review triggers |

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

> Apply the `regulatory-change-to-assurance` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
