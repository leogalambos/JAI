# Incident to permanent fix

`workflow: incident-to-problem`  ·  `steps: 12`  ·  `tool-tier: route`

**Trigger.** A service degrades or fails.

**Outcome.** Service restored, cause removed, and a control changed so the class of failure does not recur.

Restoration and diagnosis are different jobs with different objectives. The common failure is closing the incident and never opening the problem, which makes the backlog look healthy while the estate rots.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Service Desk Analyst](../../it-roles-service-management-and-support/references/service-desk-analyst.md) | captures impact and what the user was trying to do | incident record with impact and urgency | Symptom-only records are returned for clarification |
| 2 | [Incident Manager](../../it-roles-service-management-and-support/references/incident-manager.md) | classifies by business effect and drives restoration | priority, working hypothesis, comms cadence | Priority from business impact, not technical severity |
| 3 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | restores service while preserving evidence | service restored; evidence preserved | Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised |
| 4 | [Major Incident Manager](../../it-roles-service-management-and-support/references/major-incident-manager.md) | takes command when impact exceeds normal handling | command log, stakeholder comms, notification assessment | Comms on a fixed clock; regulatory clocks assessed |
| 5 | [Problem Manager](../../it-roles-service-management-and-support/references/problem-manager.md) | establishes the systemic cause | problem record with root cause and known error | "Human error" alone rejected as a root cause |
| 6 | [Technical Lead](../../it-roles-product-delivery-and-agile/references/technical-lead.md) | designs the permanent fix | fix approach and effort | The fix addresses the cause, not the latest symptom |
| 7 | [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | implements and tests the candidate permanent fix in the explicitly permitted pre-production scope | versioned candidate, pre-production test evidence and rollback rehearsal | Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision |
| 8 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | obtains the named human change decision for the permanent fix | change authorisation | Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects |
| 9 | [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | deploys the exact reviewed and authorised permanent-fix candidate | versioned fix, execution evidence and rollback observations | Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria |
| 10 | [Test Analyst](../../it-roles-quality-and-testing/references/test-analyst.md) | performs independent validation of the deployed permanent fix against predeclared criteria | independent regression, service and residual-defect evidence | Actual execution and independent validation evidence are required before closure; failed criteria remain blocking |
| 11 | [Detection Engineer](../../it-roles-security-operations-and-defensive-security/references/detection-engineer.md) | or Observability Engineer closes the detection gap the incident exposed | new or tuned alert with a runbook | Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure |
| 12 | [Continual Improvement Manager](../../it-roles-service-management-and-support/references/continual-improvement-manager.md) | confirms the improvement happened and held | measured recurrence rate | Baseline measured before the change, not asserted after |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.

Preparatory work is limited to its explicitly permitted scope. Named human approval must precede every effect it authorises; neither a role title nor a later review supplies authority retrospectively. All policy-required pre-approval evidence remains mandatory. Collect candidate evidence only within explicitly permitted pre-production scope. If policy requires operational proof, obtain a separate prior named human approval for the bounded pilot needed to collect it, then seek the wider approval; no pilot permission is implied. If no governing route permits the required evidence collection, stop and consult the accountable authority before proceeding. Any policy-permitted waiver must already be issued by the competent named human authority for the exact gate, scope and validity period before the gated action; non-waivable controls remain blocking.

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
