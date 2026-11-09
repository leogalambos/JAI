# Enterprise release orchestration

**Trigger.** Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process.

**Outcome.** The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.

## Mandatory artefacts

- Integrated release calendar
- Dependency register
- Business readiness
- Cutover readiness
- Supplier readiness
- Rollback readiness
- Secure delivery readiness evidence
- Go/no-go decision
- Post-release validation

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Enterprise Release Manager](../../it-roles-product-delivery-and-agile/references/enterprise-release-manager.md) | builds integrated release scope/calendar and identifies cross-system dependencies/blackouts | integrated release calendar | All material releases and blackout/business constraints are represented |
| 2 | [Architecture Repository and Modelling Lead](../../it-roles-architecture/references/architecture-repository-and-modelling-lead.md) | validates technical/service dependency graph and critical sequencing constraints | release dependency register | No critical dependency is missing an owner or sequence |
| 3 | [Organisational Change and Adoption Manager](../../it-roles-product-delivery-and-agile/references/organisational-change-and-adoption-manager.md) | validates communications/training/adoption/business readiness for affected cohorts | business readiness | Affected business cohorts have executable readiness actions/evidence |
| 4 | [Data Migration and Cutover Lead](../../it-roles-product-delivery-and-agile/references/data-migration-and-cutover-lead.md) | validates cutover sequence, data reconciliation, checkpoints and abort criteria | cutover readiness | Cutover and data reconciliation are rehearsed/evidenced for critical transitions |
| 5 | [SIAM Manager](../../it-roles-service-management-and-support/references/siam-manager.md) | validates supplier staffing, dependencies, handoffs and escalation readiness | supplier readiness | No critical supplier dependency is relying on informal availability |
| 6 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | validates technical release artefacts, provenance and executable rollback | technical/rollback readiness | Release artefacts are traceable and rollback is exercised/feasible |
| 7 | [Secure Delivery / DevSecOps Architect](../../it-roles-architecture/references/secure-delivery-devsecops-architect.md) | checks that release provenance, pipeline controls, policy-as-code and software supply-chain evidence conform to the approved secure-delivery architecture | secure delivery readiness evidence | Critical secure-delivery controls and provenance are evidenced; deviations are owned, time-bound and visible to independent release assurance |
| 8 | [Release Quality Gatekeeper](../../it-roles-quality-and-testing/references/release-quality-gatekeeper.md) | independently checks mandatory release criteria and evidence | release gate assurance | Producer cannot waive its own failed critical gate |
| 9 | [Enterprise Release Manager](../../it-roles-product-delivery-and-agile/references/enterprise-release-manager.md) | issues delegated integrated go/no-go or routes decision to higher authority | go/no-go decision | Decision cites evidence, waivers, residual risk and abort triggers |
| 10 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | executes the authorised technical release through controlled pipelines | release execution evidence | Executed artefacts/plan match what was approved |
| 11 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | monitors agreed technical/service signals and triggers reversal if thresholds breach | technical post-release validation | Rollback/reversal triggers are acted on, not debated after breach |
| 12 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | confirms business/service outcome and closes or escalates residual issues | release acceptance | Closure states outcome, impact, residual issues and owners |

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

- The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| coordinated | Sequence dependent releases and validate integrated readiness | Dependency register, business/supplier/technical/security readiness |
| staged | Use bounded waves with evidence-driven continuation and recovery | Wave criteria, actual results, abort triggers and remaining exposure |

Return failed independent gates to producer owners; changed artifacts/readiness need corresponding renewed review. Stop execution without exact go/no-go authority or when approved abort/reversal triggers fire. Close with actual end-to-end outcome, residual issues and service-owner acceptance, or execute the authorised recovery branch. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Integrated release scope/calendar and business windows
- Owned application/data/supplier dependencies
- Readiness criteria and go/no-go authority

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed independent gates to producer owners; changed artifacts/readiness need corresponding renewed review.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop execution without exact go/no-go authority or when approved abort/reversal triggers fire.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close with actual end-to-end outcome, residual issues and service-owner acceptance, or execute the authorised recovery branch.

**Bounded paths and scope:**

Coordinated/staged release share readiness, authority and actual observation requirements, with explicit wave boundaries.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| coordinated | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| staged | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
