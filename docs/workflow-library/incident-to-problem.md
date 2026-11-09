# Incident to permanent fix

## Trigger

A service degrades or fails.

## Intended outcome

Service restored, cause removed, and a control changed so the class of failure does not recur.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Service restored, cause removed, and a control changed so the class of failure does not recur.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| ordinary | Coordinate proportionate restoration and later causal work | Incident observations, authorised restoration and service validation |
| major | Use declared command and stakeholder cadence | Command log, business-impact priority and notification-clock assessment |
| suspected-security | Hand security handling to the incident response scope while preserving service coordination | Preserved evidence, scoped security handoff and authorised restoration |

Return disproved hypotheses to the problem owner with their evidence; new fix revisions follow readiness and change review. Stop destructive recovery without evidence preservation and the required scope authority; stop deployment at failed health criteria. Close restoration separately from causal resolution; permanent closure needs independent fix validation and recurrence measures. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Affected service and observed business impact
- Current incident/restoration authority
- Evidence preservation and communication needs

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return disproved hypotheses to the problem owner with their evidence; new fix revisions follow readiness and change review.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop destructive recovery without evidence preservation and the required scope authority; stop deployment at failed health criteria.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close restoration separately from causal resolution; permanent closure needs independent fix validation and recurrence measures.

**Bounded paths and scope:**

Ordinary, major and suspected-security contexts retain actual observations, authority and evidence preservation; command intensity and the referenced response scope differ.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| ordinary | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| major | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| suspected-security | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Incident to permanent fix workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Service Desk Analyst</strong><p>captures impact and what the user was trying to do</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Incident Manager</strong><p>classifies by business effect and drives restoration</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Site Reliability Engineer</strong><p>restores service while preserving evidence</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Major Incident Manager</strong><p>takes command when impact exceeds normal handling</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Problem Manager</strong><p>establishes the systemic cause</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Technical Lead</strong><p>designs the permanent fix</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Software Engineer</strong><p>implements and tests the candidate permanent fix in the explicitly permitted pre-production scope</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Change Manager</strong><p>obtains the named human change decision for the permanent fix</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Software Engineer</strong><p>deploys the exact reviewed and authorised permanent-fix candidate</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Test Analyst</strong><p>performs independent validation of the deployed permanent fix against predeclared criteria</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>Detection Engineer</strong><p>or Observability Engineer closes the detection gap the incident exposed</p></div></li>
<li data-step="12"><span class="ai-workflow-step-number" aria-hidden="true">12</span><div><strong>Continual Improvement Manager</strong><p>confirms the improvement happened and held</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-incident-to-problem.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Service Desk Analyst | captures impact and what the user was trying to do | incident record with impact and urgency | Symptom-only records are returned for clarification |
| 2 | Incident Manager | classifies by business effect and drives restoration | priority, working hypothesis, comms cadence | Priority from business impact, not technical severity |
| 3 | Site Reliability Engineer | restores service while preserving evidence | service restored; evidence preserved | Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised |
| 4 | Major Incident Manager | takes command when impact exceeds normal handling | command log, stakeholder comms, notification assessment | Comms on a fixed clock; regulatory clocks assessed |
| 5 | Problem Manager | establishes the systemic cause | problem record with root cause and known error | "Human error" alone rejected as a root cause |
| 6 | Technical Lead | designs the permanent fix | fix approach and effort | The fix addresses the cause, not the latest symptom |
| 7 | Software Engineer | implements and tests the candidate permanent fix in the explicitly permitted pre-production scope | versioned candidate, pre-production test evidence and rollback rehearsal | Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision |
| 8 | Change Manager | obtains the named human change decision for the permanent fix | change authorisation | Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects |
| 9 | Software Engineer | deploys the exact reviewed and authorised permanent-fix candidate | versioned fix, execution evidence and rollback observations | Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria |
| 10 | Test Analyst | performs independent validation of the deployed permanent fix against predeclared criteria | independent regression, service and residual-defect evidence | Actual execution and independent validation evidence are required before closure; failed criteria remain blocking |
| 11 | Detection Engineer | or Observability Engineer closes the detection gap the incident exposed | new or tuned alert with a runbook | Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure |
| 12 | Continual Improvement Manager | confirms the improvement happened and held | measured recurrence rate | Baseline measured before the change, not asserted after |

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

> Apply the `incident-to-problem` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.

Approval and execution are separate handoffs. Candidate preparation stays within explicitly permitted pre-production scope. Every production, pilot, credential or irreversible effect requires prior exact named human authority under the applicable policy. If operational proof is required before a wider approval, obtain separate prior authorisation for the bounded pilot needed to collect it; if no policy route permits collection, stop and consult the authority. Draft rendering and review evidence do not release a publication. An existing policy-permitted waiver must identify the competent human authority, exact gate and scope, and validity period before the gated action; mandatory controls and unsupported factual claims remain blocking.
