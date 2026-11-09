# Design to operational readiness

`workflow: design-to-operational-readiness`  ·  `steps: 7`  ·  `tool-tier: route`

**Trigger.** A solution design is becoming build/release ready and must prove it can be operated safely before go-live.

**Outcome.** The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.

This chain is an enterprise hand-off model, not a rigid project schedule. Run steps in parallel where sensible, but do not skip the acceptance gate between accountable roles.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | defines the target architecture, NFRs, dependencies and failure modes | solution architecture and decision records | Quality attributes and failure modes are explicit and testable |
| 2 | [Security Architect](../../it-roles-architecture/references/security-architect.md) | defines security controls and residual security risks | security architecture and control requirements | Controls trace to risks and objectives |
| 3 | [Operational and Technology Resilience Architect](../../it-roles-architecture/references/operational-and-technology-resilience-architect.md) | tests the design against failure domains, impact tolerances and recovery paths | resilience architecture and validation scenarios | Resilience claims identify dependencies, failure domains and validation method |
| 4 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | defines SLOs, observability, alerting and operability signals | SLO/monitoring design and runbook requirements | Alerts are actionable and every SLO has a data source |
| 5 | [Service Transition and Operational Readiness Manager](../../it-roles-service-management-and-support/references/service-transition-and-operational-readiness-manager.md) | assembles and assesses operational acceptance evidence | operational readiness assessment and evidence pack | Every readiness criterion is pass/fail/waived with evidence and owner |
| 6 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | checks the production change path and risk-class approval | change authorisation decision | Change risk and readiness evidence match the approval route |
| 7 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | accepts service ownership and residual operational risk | service acceptance | Support ownership, SLOs and residual risks are explicitly accepted |

## Operating this chain

Read the linked role reference before acting as a step and use the operator agent declared for that role's tool tier. A hand-off is complete only when the receiving step applies the stated gate and accepts the evidence. Failed gates remain explicit; they are not converted into assumptions simply to preserve a milestone.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| new-service | Establish complete receiving operations evidence | Runbooks, monitoring, access, recovery and support rehearsal |
| existing-service-delta | Assess affected readiness and dependencies while reusing unchanged approved evidence | Exact design delta, impact and current evidence references |

Return failed readiness criteria to the accountable design/platform/support owner before the change decision. Stop go-live for unowned critical readiness gaps or absent required change authority. Accept operational responsibility with explicit residual risks or defer activation with owned remediation. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Versioned solution and measurable quality requirements
- Receiving service owner and support model
- Risk, resilience and readiness criteria

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed readiness criteria to the accountable design/platform/support owner before the change decision.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop go-live for unowned critical readiness gaps or absent required change authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept operational responsibility with explicit residual risks or defer activation with owned remediation.

**Bounded paths and scope:**

New-service and changed-service readiness share evidence types; unchanged valid platform evidence is referenced rather than re-executed.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| new-service | 1, 2, 3, 4, 5, 6, 7 | 7 |
| existing-service-delta | 1, 2, 3, 4, 5, 6, 7 | 7 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
