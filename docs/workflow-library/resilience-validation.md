# Resilience validation

## Trigger

A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure.

## Intended outcome

Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| isolated-exercise | Test representative failure conditions in permitted nonproduction scope | Scenario relevance, actual observations and extrapolation limits |
| production-exercise | Use prior scoped authority, safeguards and enforced stop criteria | Actual approval, operating safeguards, observations and recovery status |

Return falsified design assumptions or failed retests to the resilience/control owner with located evidence. Stop exercise effects outside approved scope or when safety/availability limits are breached. Accept bounded demonstrated resilience with residual risk and next review, or retain failed claims and owned remediation. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Business-owned criticality and impact tolerances
- Dependency/failure-domain baseline
- Falsifiable claims, recovery targets and permitted exercise scope

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return falsified design assumptions or failed retests to the resilience/control owner with located evidence.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop exercise effects outside approved scope or when safety/availability limits are breached.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept bounded demonstrated resilience with residual risk and next review, or retain failed claims and owned remediation.

**Bounded paths and scope:**

Isolated and production exercises both require actual scoped observations; production additionally retains prior authority and safety limits.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| isolated-exercise | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |
| production-exercise | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Resilience validation workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Business Continuity Manager</strong><p>confirms business criticality, impact tolerances and priority services/processes</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Operational and Technology Resilience Architect</strong><p>maps technical/supplier/data dependencies and correlated failure domains</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Disaster Recovery Coordinator</strong><p>validates RTO/RPO and recovery sequencing against dependency reality</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Operational and Technology Resilience Architect</strong><p>defines resilience/recovery architecture and degradation patterns</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Test Manager</strong><p>builds the exercise plan, entry/exit criteria, injects and evidence capture method</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Chaos and Resilience Engineer</strong><p>executes authorised failure experiments/exercises and captures telemetry</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Control Tester</strong><p>independently evaluates evidence and records control/resilience findings</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Operational and Technology Resilience Architect</strong><p>coordinates owned remediation across architecture, operations and suppliers</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Test Manager</strong><p>retests failed claims after remediation using comparable criteria</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>IT Service Owner</strong><p>accepts demonstrated resilience or explicitly accepts residual risk within authority</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-resilience-validation.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Business Continuity Manager | confirms business criticality, impact tolerances and priority services/processes | business criticality baseline | Criticality and tolerances have business ownership |
| 2 | Operational and Technology Resilience Architect | maps technical/supplier/data dependencies and correlated failure domains | dependency/failure-domain model | No critical path has an unknown/unowned dependency |
| 3 | Disaster Recovery Coordinator | validates RTO/RPO and recovery sequencing against dependency reality | validated recovery objectives | Objectives are feasible end to end, not only per component |
| 4 | Operational and Technology Resilience Architect | defines resilience/recovery architecture and degradation patterns | resilience design with failure assumptions | Design addresses single/shared failure modes and measurable outcomes |
| 5 | Test Manager | builds the exercise plan, entry/exit criteria, injects and evidence capture method | approved exercise plan | Test design can falsify the resilience claims and protects production safety |
| 6 | Chaos and Resilience Engineer | executes authorised failure experiments/exercises and captures telemetry | exercise evidence | Execution matches approved scope and evidence is attributable |
| 7 | Control Tester | independently evaluates evidence and records control/resilience findings | findings register | Findings distinguish observation, criterion, impact and evidence |
| 8 | Operational and Technology Resilience Architect | coordinates owned remediation across architecture, operations and suppliers | remediation plan | Every material finding has owner/date/design response |
| 9 | Test Manager | retests failed claims after remediation using comparable criteria | retest result | Critical findings are demonstrated fixed, not administratively closed |
| 10 | IT Service Owner | accepts demonstrated resilience or explicitly accepts residual risk within authority | resilience acceptance | Acceptance states evidence, residual risk and next validation date |

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

> Apply the `resilience-validation` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
