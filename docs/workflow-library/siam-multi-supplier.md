# SIAM / multi-supplier service integration

## Trigger

A service depends on multiple suppliers/teams and end-to-end accountability, OLAs, incidents, problems, changes or acceptance are fragmented across boundaries.

## Intended outcome

One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="SIAM / multi-supplier service integration workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>SIAM Manager</strong><p>defines end-to-end service scope, integrator authority and supplier responsibility model</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Service Level Manager</strong><p>decomposes customer SLA into measurable OLAs/underpinning supplier obligations</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Architecture Repository and Modelling Lead</strong><p>maintains cross-supplier service/technology/dependency model</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Incident Manager</strong><p>defines cross-supplier incident ownership, bridge, evidence and handoff rules</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Problem Manager</strong><p>owns systemic problem process across supplier boundaries</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Enterprise Release Manager</strong><p>integrates supplier change/release windows, collisions and readiness</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>SIAM Manager</strong><p>defines dispute/escalation clocks, evidence standard and decision authority</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>IT Service Owner</strong><p>accepts the integrated service and residual multi-supplier risks</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-siam-multi-supplier.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | SIAM Manager | defines end-to-end service scope, integrator authority and supplier responsibility model | SIAM operating model | No customer outcome or integration process is ownerless |
| 2 | Service Level Manager | decomposes customer SLA into measurable OLAs/underpinning supplier obligations | SLA/OLA matrix | Every SLA has sufficient underpinning measures/owners |
| 3 | Architecture Repository and Modelling Lead | maintains cross-supplier service/technology/dependency model | shared dependency register/view set | Material supplier/service dependencies have stable IDs and owners |
| 4 | Incident Manager | defines cross-supplier incident ownership, bridge, evidence and handoff rules | cross-supplier incident model | Severity and service restoration ownership cannot bounce between suppliers |
| 5 | Problem Manager | owns systemic problem process across supplier boundaries | cross-supplier problem model | Root causes crossing contracts still receive one end-to-end owner |
| 6 | Enterprise Release Manager | integrates supplier change/release windows, collisions and readiness | integrated change/release calendar | Cross-supplier change collisions and blackout constraints are governed |
| 7 | SIAM Manager | defines dispute/escalation clocks, evidence standard and decision authority | supplier escalation matrix | Escalation cannot be blocked by contractual ownership ambiguity |
| 8 | IT Service Owner | accepts the integrated service and residual multi-supplier risks | shared service acceptance | Service acceptance is end-to-end, not a collection of supplier self-attestations |

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

> Apply the `siam-multi-supplier` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
