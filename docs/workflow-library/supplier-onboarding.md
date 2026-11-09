# Supplier onboarding to exit

**Perspective:** enterprise buyer managing a supplier. For supplier-side bid preparation, pricing and delivery monitoring, use [Commercial delivery](../capabilities/commercial-delivery.md). The two perspectives have different accountable owners even when they refer to the same contract.

## Trigger

A technology supplier or SaaS product is being considered.

## Intended outcome

A contracted supplier with assurance, monitored performance and a tested way out.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- A contracted supplier with assurance, monitored performance and a tested way out.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| ordinary | Assess comparable offers and proportionate service obligations | Declared criteria, supplier responses and owned contract measures |
| critical | Exercise continuity/substitution and test enforceable exit | Dependency risks, recovery/exit evidence and residual decisions |

Return noncomparable responses, unowned obligations or failed exit tests to procurement/contract/supplier owners. Stop commitments beyond authority or activation with unresolved mandatory supplier/security/privacy obligations. Accept the governed supplier service or terminate selection/exit with retained obligations and data/access disposition. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Sourcing requirements and owner
- Supplier/service criticality and data use
- Procurement rules and contract decision rights

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return noncomparable responses, unowned obligations or failed exit tests to procurement/contract/supplier owners.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop commitments beyond authority or activation with unresolved mandatory supplier/security/privacy obligations.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the governed supplier service or terminate selection/exit with retained obligations and data/access disposition.

**Bounded paths and scope:**

Criticality changes continuity/exit depth; all suppliers retain accountable obligations and proportionate assurance.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| ordinary | 1, 2, 3, 4, 5, 6, 7 | 7 |
| critical | 1, 2, 3, 4, 5, 6, 7 | 7 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Supplier onboarding to exit workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>IT Procurement Specialist</strong><p>runs the selection with the right requirements in the tender</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Third-Party Risk Manager</strong><p>assesses and tiers the supplier risk</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Security Architect</strong><p>sets the control requirements the supplier must meet</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Contract Manager</strong><p>extracts obligations into a tracked register</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Vendor Manager</strong><p>manages performance and the relationship after signature</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Service Level Manager</strong><p>aligns supplier commitments with what was promised internally</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Business Continuity Manager</strong><p>proves the organisation survives the supplier failing</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-supplier-onboarding.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | IT Procurement Specialist | runs the selection with the right requirements in the tender | tender, evaluation and recommendation | Security, privacy, exit and continuity requirements in the tender, not added after |
| 2 | Third-Party Risk Manager | assesses and tiers the supplier risk | risk assessment and tier | Critical suppliers have a tested exit or substitution plan |
| 3 | Security Architect | sets the control requirements the supplier must meet | supplier control requirements | Requirements traced to threats, not copied from a questionnaire |
| 4 | Contract Manager | extracts obligations into a tracked register | contract and obligation register | Obligations on both sides tracked with owners |
| 5 | Vendor Manager | manages performance and the relationship after signature | scorecards and governance cadence | Renewal started early enough for a real alternative to exist |
| 6 | Service Level Manager | aligns supplier commitments with what was promised internally | aligned SLAs and OLAs | No internal commitment exceeding what the supply chain can deliver |
| 7 | Business Continuity Manager | proves the organisation survives the supplier failing | exercised continuity and exit plan | Exit tested, not described |

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

> Apply the `supplier-onboarding` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
