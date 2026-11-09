# Demand to portfolio to funding

**Trigger.** A new business/technology demand needs to be qualified, compared with alternatives and either rejected, redirected or committed into a funded portfolio.

**Outcome.** Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision.

## Mandatory artefacts

- Demand record
- Qualification assessment
- Capability-fit assessment
- Application portfolio impact assessment
- Architecture impact assessment
- Risk/value assessment
- Estimate and capacity view
- Prioritisation decision
- Funding decision
- Portfolio commitment

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Demand & Intake Manager](../../it-roles-product-delivery-and-agile/references/demand-and-intake-manager.md) | captures demand with owner, problem/outcome, urgency and evidence status | demand record | No anonymous or outcome-free demand enters prioritisation |
| 2 | [Demand & Intake Manager](../../it-roles-product-delivery-and-agile/references/demand-and-intake-manager.md) | qualifies completeness, duplicates, mandatory obligations and routing | qualification assessment | Disposition is explicit: reject, redirect, discover or assess |
| 3 | [Enterprise Architect](../../it-roles-architecture/references/enterprise-architect.md) | checks business capability fit, reuse and enterprise target-state alignment | capability-fit assessment | Existing capability/service reuse and strategic conflicts are explicit |
| 4 | [Application Portfolio Manager](../../it-roles-architecture/references/application-portfolio-manager.md) | assesses affected application portfolio, lifecycle posture, duplication and invest/tolerate/migrate/retire consequences | application portfolio impact assessment | Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner |
| 5 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | assesses architecture/integration/data/security/operational impact at decision-appropriate depth | architecture impact assessment | Material cross-domain dependencies and constraints are identified |
| 6 | [IT Risk Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/it-risk-manager.md) | frames risk/opportunity, compliance urgency and value-at-risk alongside benefit evidence | risk/value assessment | Regulatory/risk urgency is evidence-based and not double-counted as value |
| 7 | [Resource Manager](../../it-roles-commercial-sourcing-and-enablement/references/resource-manager.md) | coordinates indicative sizing and scarce-capability/capacity demand | estimate and capacity view | Uncertainty ranges and constrained skills/capacity are explicit |
| 8 | [Portfolio Manager](../../it-roles-product-delivery-and-agile/references/portfolio-manager.md) | applies transparent prioritisation criteria across value, risk, strategy, capacity and dependencies | prioritisation decision | Prioritisation can be reconstructed from declared criteria and exceptions |
| 9 | [IT Financial Management / TBM Manager](../../it-roles-commercial-sourcing-and-enablement/references/it-financial-management-tbm-manager.md) | validates TCO/funding profile and financial comparability | funding economics and cost profile | Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model |
| 10 | [Portfolio Manager](../../it-roles-product-delivery-and-agile/references/portfolio-manager.md) | makes or routes the delegated funding/portfolio commitment decision | portfolio commitment | Commitment has authority, funding/capacity basis and review condition |

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

- Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| discovery | Reject, redirect or investigate uncertain need before detailed commitment | Qualification evidence, alternatives and next decision |
| funding | Compare risk/value, lifecycle, cost and capacity against declared criteria | Reconstructible prioritisation and actual funding/commitment authority |

Return unsupported value, lifecycle or estimate assumptions to their accountable owners. Stop anonymous/outcome-free prioritisation and commitments lacking eligible authority, funding or capacity basis. Record reject/redirect/discover/defer/commit with rationale and accountable review condition. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Named demand owner and business outcome
- Capability/application baseline and constraints
- Decision criteria, cost horizon and available capacity

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return unsupported value, lifecycle or estimate assumptions to their accountable owners.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop anonymous/outcome-free prioritisation and commitments lacking eligible authority, funding or capacity basis.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Record reject/redirect/discover/defer/commit with rationale and accountable review condition.

**Bounded paths and scope:**

Discovery terminates after qualification; a funding commitment requires the downstream evidence and eligible authority.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| discovery | 1, 2 | 2 |
| funding | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
