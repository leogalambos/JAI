# Source to contract to service

**Trigger.** A capability may be sourced externally and must move from requirement/RFI/RFP through supplier selection and contract controls to implementation and accepted service.

**Outcome.** The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance.

## Mandatory artefacts

- Sourcing requirement baseline
- RFI/RFP pack
- Supplier assessment
- Security/privacy assessment
- Architecture-fit decision
- Selection decision
- Contract control schedule
- Implementation plan
- Service acceptance
- Vendor governance baseline

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Business Analyst](../../it-roles-analysis/references/business-analyst.md) | turns business/service need into outcome, requirement and acceptance baseline | sourcing requirement baseline | Requirements are testable and distinguish need from preferred solution |
| 2 | [IT Procurement Specialist](../../it-roles-commercial-sourcing-and-enablement/references/it-procurement-specialist.md) | creates and runs RFI/RFP process with comparable response structure | RFI/RFP pack and response evidence | Supplier responses are comparable and procurement rules are followed |
| 3 | [Vendor Manager](../../it-roles-commercial-sourcing-and-enablement/references/vendor-manager.md) | assesses supplier capability, viability, support and governance fit | supplier assessment | Material supplier assumptions and dependency risks are evidenced |
| 4 | [Third-Party Risk Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/third-party-risk-manager.md) | coordinates security/privacy/resilience risk assessment with specialist authorities | security/privacy/supplier risk assessment | Critical risks/obligations are resolved, mitigated or accepted by correct authority |
| 5 | [Enterprise Applications Architect](../../it-roles-architecture/references/enterprise-applications-architect.md) | assesses architecture/capability/integration fit and lock-in/exit implications | architecture-fit decision | Selection does not create hidden target-state or integration contradictions |
| 6 | [IT Procurement Specialist](../../it-roles-commercial-sourcing-and-enablement/references/it-procurement-specialist.md) | runs weighted selection and records rationale/conflicts | selection decision | Decision is traceable to declared criteria, evidence and authority |
| 7 | [Contract Manager](../../it-roles-commercial-sourcing-and-enablement/references/contract-manager.md) | translates agreed service/security/privacy/resilience/exit controls into enforceable clauses/schedules | contract control schedule | Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path |
| 8 | [Implementation Consultant](../../it-roles-commercial-sourcing-and-enablement/references/implementation-consultant.md) | coordinates implementation against contract/design acceptance criteria | implementation plan and evidence | Implementation deviations are approved, not silently normalised |
| 9 | [Service Transition and Operational Readiness Manager](../../it-roles-service-management-and-support/references/service-transition-and-operational-readiness-manager.md) | validates support, monitoring, CMDB, DR, security, ownership and service acceptance | service acceptance | No production acceptance with missing critical operational ownership/evidence |
| 10 | [Vendor Manager](../../it-roles-commercial-sourcing-and-enablement/references/vendor-manager.md) | establishes ongoing performance, risk, improvement, renewal and exit governance | vendor governance baseline | Contractual obligations map to measured service/vendor governance |

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

- The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| competitive | Compare offers against declared criteria and preserve procurement evidence | Comparable responses, evaluation and selection decision |
| direct-award | Apply the actual permitted exception route without fabricating competition | Authority, rationale, applicable rules and assessed risk/value |

Return noncomparable responses, control wording gaps or implementation deviations to procurement/contract/delivery owners. Stop unauthorised commitment or service acceptance with unresolved critical control/ownership gaps. Accept the contracted service and measured vendor governance, or terminate selection/implementation under the actual contract route. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Testable need and sourcing scope
- Procurement/contract authority and rules
- Architecture, risk and receiving-service constraints

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return noncomparable responses, control wording gaps or implementation deviations to procurement/contract/delivery owners.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop unauthorised commitment or service acceptance with unresolved critical control/ownership gaps.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the contracted service and measured vendor governance, or terminate selection/implementation under the actual contract route.

**Bounded paths and scope:**

Direct award requires the actual permitted exception and cannot fabricate competitive tender responses.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| competitive | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |
| direct-award | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
