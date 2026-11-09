# SIAM / multi-supplier service integration

**Trigger.** A service depends on multiple suppliers/teams and end-to-end accountability, OLAs, incidents, problems, changes or acceptance are fragmented across boundaries.

**Outcome.** One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation.

## Mandatory artefacts

- SIAM operating model
- SLA/OLA matrix
- Dependency register
- Cross-supplier incident model
- Cross-supplier problem model
- Integrated change calendar
- Escalation matrix
- Shared service acceptance

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [SIAM Manager](../../it-roles-service-management-and-support/references/siam-manager.md) | defines end-to-end service scope, integrator authority and supplier responsibility model | SIAM operating model | No customer outcome or integration process is ownerless |
| 2 | [Service Level Manager](../../it-roles-service-management-and-support/references/service-level-manager.md) | decomposes customer SLA into measurable OLAs/underpinning supplier obligations | SLA/OLA matrix | Every SLA has sufficient underpinning measures/owners |
| 3 | [Architecture Repository and Modelling Lead](../../it-roles-architecture/references/architecture-repository-and-modelling-lead.md) | maintains cross-supplier service/technology/dependency model | shared dependency register/view set | Material supplier/service dependencies have stable IDs and owners |
| 4 | [Incident Manager](../../it-roles-service-management-and-support/references/incident-manager.md) | defines cross-supplier incident ownership, bridge, evidence and handoff rules | cross-supplier incident model | Severity and service restoration ownership cannot bounce between suppliers |
| 5 | [Problem Manager](../../it-roles-service-management-and-support/references/problem-manager.md) | owns systemic problem process across supplier boundaries | cross-supplier problem model | Root causes crossing contracts still receive one end-to-end owner |
| 6 | [Enterprise Release Manager](../../it-roles-product-delivery-and-agile/references/enterprise-release-manager.md) | integrates supplier change/release windows, collisions and readiness | integrated change/release calendar | Cross-supplier change collisions and blackout constraints are governed |
| 7 | [SIAM Manager](../../it-roles-service-management-and-support/references/siam-manager.md) | defines dispute/escalation clocks, evidence standard and decision authority | supplier escalation matrix | Escalation cannot be blocked by contractual ownership ambiguity |
| 8 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | accepts the integrated service and residual multi-supplier risks | shared service acceptance | Service acceptance is end-to-end, not a collection of supplier self-attestations |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| steady-state | Govern end-to-end measures and shared responsibilities | Underpinning levels, ownership and service results |
| cross-supplier-disruption | Use one incident/problem/escalation owner across contractual boundaries | Command/restoration ownership, supplier actions and customer impact |

Return ownership gaps, level mismatches or collisions to the integration/service owner rather than bouncing between suppliers. Stop unsupported end-to-end acceptance or cross-supplier effects outside actual authority. Accept the integrated outcome with owned residual issues, or escalate unresolved contract boundaries to the entitled authority. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Customer outcomes and service boundary
- Supplier contracts, SLAs/OLAs and dependency owners
- Integration decision and escalation rights

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return ownership gaps, level mismatches or collisions to the integration/service owner rather than bouncing between suppliers.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop unsupported end-to-end acceptance or cross-supplier effects outside actual authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the integrated outcome with owned residual issues, or escalate unresolved contract boundaries to the entitled authority.

**Bounded paths and scope:**

Steady-state/disruption share accountable service outcomes, dependencies and escalation; incident actions require actual scope.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| steady-state | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| cross-supplier-disruption | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
