# Source to contract to service

**Perspective:** enterprise buyer. This chain selects, contracts and accepts a supplier/service. For the supplier's opportunity, proposal and delivery economics, use [Commercial delivery](../capabilities/commercial-delivery.md). Choose the required assurance arrangement using [Methodical workflows](../using/methodical-workflows.md).

## Trigger

A capability may be sourced externally and must move from requirement/RFI/RFP through supplier selection and contract controls to implementation and accepted service.

## Intended outcome

The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Source to contract to service workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Business Analyst</strong><p>turns business/service need into outcome, requirement and acceptance baseline</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>IT Procurement Specialist</strong><p>creates and runs RFI/RFP process with comparable response structure</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Vendor Manager</strong><p>assesses supplier capability, viability, support and governance fit</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Third-Party Risk Manager</strong><p>coordinates security/privacy/resilience risk assessment with specialist authorities</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Enterprise Applications Architect</strong><p>assesses architecture/capability/integration fit and lock-in/exit implications</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>IT Procurement Specialist</strong><p>runs weighted selection and records rationale/conflicts</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Contract Manager</strong><p>translates agreed service/security/privacy/resilience/exit controls into enforceable clauses/schedules</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Implementation Consultant</strong><p>coordinates implementation against contract/design acceptance criteria</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Service Transition and Operational Readiness Manager</strong><p>validates support, monitoring, CMDB, DR, security, ownership and service acceptance</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Vendor Manager</strong><p>establishes ongoing performance, risk, improvement, renewal and exit governance</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-source-to-contract-to-service.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Business Analyst | turns business/service need into outcome, requirement and acceptance baseline | sourcing requirement baseline | Requirements are testable and distinguish need from preferred solution |
| 2 | IT Procurement Specialist | creates and runs RFI/RFP process with comparable response structure | RFI/RFP pack and response evidence | Supplier responses are comparable and procurement rules are followed |
| 3 | Vendor Manager | assesses supplier capability, viability, support and governance fit | supplier assessment | Material supplier assumptions and dependency risks are evidenced |
| 4 | Third-Party Risk Manager | coordinates security/privacy/resilience risk assessment with specialist authorities | security/privacy/supplier risk assessment | Critical risks/obligations are resolved, mitigated or accepted by correct authority |
| 5 | Enterprise Applications Architect | assesses architecture/capability/integration fit and lock-in/exit implications | architecture-fit decision | Selection does not create hidden target-state or integration contradictions |
| 6 | IT Procurement Specialist | runs weighted selection and records rationale/conflicts | selection decision | Decision is traceable to declared criteria, evidence and authority |
| 7 | Contract Manager | translates agreed service/security/privacy/resilience/exit controls into enforceable clauses/schedules | contract control schedule | Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path |
| 8 | Implementation Consultant | coordinates implementation against contract/design acceptance criteria | implementation plan and evidence | Implementation deviations are approved, not silently normalised |
| 9 | Service Transition and Operational Readiness Manager | validates support, monitoring, CMDB, DR, security, ownership and service acceptance | service acceptance | No production acceptance with missing critical operational ownership/evidence |
| 10 | Vendor Manager | establishes ongoing performance, risk, improvement, renewal and exit governance | vendor governance baseline | Contractual obligations map to measured service/vendor governance |

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

> Apply the `source-to-contract-to-service` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
