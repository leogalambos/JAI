# Resilience validation

**Trigger.** A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure.

**Outcome.** Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.

## Mandatory artefacts

- Business criticality baseline
- Dependency/failure-domain model
- Validated RTO/RPO register
- Resilience design
- Exercise plan
- Exercise evidence
- Findings register
- Remediation plan
- Retest result
- Resilience acceptance

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Business Continuity Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/business-continuity-manager.md) | confirms business criticality, impact tolerances and priority services/processes | business criticality baseline | Criticality and tolerances have business ownership |
| 2 | [Operational and Technology Resilience Architect](../../it-roles-architecture/references/operational-and-technology-resilience-architect.md) | maps technical/supplier/data dependencies and correlated failure domains | dependency/failure-domain model | No critical path has an unknown/unowned dependency |
| 3 | [Disaster Recovery Coordinator](../../it-roles-governance-risk-compliance-audit-and-privacy/references/disaster-recovery-coordinator.md) | validates RTO/RPO and recovery sequencing against dependency reality | validated recovery objectives | Objectives are feasible end to end, not only per component |
| 4 | [Operational and Technology Resilience Architect](../../it-roles-architecture/references/operational-and-technology-resilience-architect.md) | defines resilience/recovery architecture and degradation patterns | resilience design with failure assumptions | Design addresses single/shared failure modes and measurable outcomes |
| 5 | [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | builds the exercise plan, entry/exit criteria, injects and evidence capture method | approved exercise plan | Test design can falsify the resilience claims and protects production safety |
| 6 | [Chaos and Resilience Engineer](../../it-roles-quality-and-testing/references/chaos-and-resilience-engineer.md) | executes authorised failure experiments/exercises and captures telemetry | exercise evidence | Execution matches approved scope and evidence is attributable |
| 7 | [Control Tester](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-tester.md) | independently evaluates evidence and records control/resilience findings | findings register | Findings distinguish observation, criterion, impact and evidence |
| 8 | [Operational and Technology Resilience Architect](../../it-roles-architecture/references/operational-and-technology-resilience-architect.md) | coordinates owned remediation across architecture, operations and suppliers | remediation plan | Every material finding has owner/date/design response |
| 9 | [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | retests failed claims after remediation using comparable criteria | retest result | Critical findings are demonstrated fixed, not administratively closed |
| 10 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | accepts demonstrated resilience or explicitly accepts residual risk within authority | resilience acceptance | Acceptance states evidence, residual risk and next validation date |

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
