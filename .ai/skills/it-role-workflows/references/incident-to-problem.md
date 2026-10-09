# Incident to permanent fix

`workflow: incident-to-problem`  ·  `steps: 9`  ·  `tool-tier: route`

**Trigger.** A service degrades or fails.

**Outcome.** Service restored, cause removed, and a control changed so the class of failure does not recur.

Restoration and diagnosis are different jobs with different objectives. The common failure is closing the incident and never opening the problem, which makes the backlog look healthy while the estate rots.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Service Desk Analyst](../../it-roles-service-management-and-support/references/service-desk-analyst.md) | captures impact and what the user was trying to do | incident record with impact and urgency | Symptom-only records are returned for clarification |
| 2 | [Incident Manager](../../it-roles-service-management-and-support/references/incident-manager.md) | classifies by business effect and drives restoration | priority, working hypothesis, comms cadence | Priority from business impact, not technical severity |
| 3 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | restores service while preserving evidence | service restored; evidence preserved | Evidence kept before destructive recovery |
| 4 | [Major Incident Manager](../../it-roles-service-management-and-support/references/major-incident-manager.md) | takes command when impact exceeds normal handling | command log, stakeholder comms, notification assessment | Comms on a fixed clock; regulatory clocks assessed |
| 5 | [Problem Manager](../../it-roles-service-management-and-support/references/problem-manager.md) | establishes the systemic cause | problem record with root cause and known error | "Human error" alone rejected as a root cause |
| 6 | [Technical Lead](../../it-roles-product-delivery-and-agile/references/technical-lead.md) | designs the permanent fix | fix approach and effort | The fix addresses the cause, not the latest symptom |
| 7 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | authorises the fix through the normal path | change authorisation | Emergency path used only where justified, and logged |
| 8 | [Detection Engineer](../../it-roles-security-operations-and-defensive-security/references/detection-engineer.md) | or Observability Engineer closes the detection gap the incident exposed | new or tuned alert with a runbook | The alert would have fired earlier for this failure |
| 9 | [Continual Improvement Manager](../../it-roles-service-management-and-support/references/continual-improvement-manager.md) | confirms the improvement happened and held | measured recurrence rate | Baseline measured before the change, not asserted after |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
