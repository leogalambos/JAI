# Idea to production

`workflow: idea-to-production`  ·  `steps: 13`  ·  `tool-tier: route`

**Trigger.** A business need, opportunity or customer problem arrives with no agreed solution.

**Outcome.** A change running in production with a measured benefit and a named owner.

The most common enterprise value stream, and the one where handoffs are usually implicit. Each arrow below is a place where work is accepted or refused; an unconfirmed handoff reappears later as someone else's incident.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Business Relationship Manager](../../it-roles-service-management-and-support/references/business-relationship-manager.md) | captures the demand with a business outcome and an owner | demand record with outcome and owner | Demand with no named business outcome does not enter the pipeline |
| 2 | [Product Manager](../../it-roles-product-delivery-and-agile/references/product-manager.md) | decides whether and why to pursue it, against evidence | roadmap item with problem statement and success measure | The customer problem and its evidence are stated |
| 3 | [Business Analyst](../../it-roles-analysis/references/business-analyst.md) | elicits and specifies the need with testable acceptance criteria | requirements baseline with traceability | Every requirement is atomic, testable and traced to a source |
| 4 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | designs the solution end to end and records the decisions | solution architecture and ADRs | Reviewed by someone who will operate it; failure modes documented |
| 5 | [Security Architect](../../it-roles-architecture/references/security-architect.md) | designs the controls the solution needs | security requirements and threat model | Every control traces to a threat and a business risk |
| 6 | [Technical Lead](../../it-roles-product-delivery-and-agile/references/technical-lead.md) | breaks the work down and sets the technical approach | technical breakdown and readiness-checked items | Acceptance criteria and dependencies exist before start |
| 7 | [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | implements with tests and telemetry | reviewed, merged change with rollback path | Peer reviewed; no secrets in source; telemetry present |
| 8 | [Test Analyst](../../it-roles-quality-and-testing/references/test-analyst.md) | verifies against the claims and reports residual risk | test evidence and residual risk statement | Exit criteria agreed before execution and met or waived |
| 9 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | assembles the release and proves the rollback | release manifest and tested rollback | Manifest states exactly which artefact versions ship where |
| 10 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | authorises the production change proportionate to its risk | change authorisation | Risk class matched to approval path; emergency changes logged within the window |
| 11 | [GitOps and Continuous Delivery Engineer](../../it-roles-software-development-and-engineering/references/gitops-and-continuous-delivery-engineer.md) | promotes the artefact and runs the progressive rollout | deployed change with health gate | Health gate and automatic rollback defined and exercised |
| 12 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | observes against the service objective and owns the run | service operating within SLO, or an error-budget decision | Error budget policy actually enforced |
| 13 | [Product Analyst](../../it-roles-analysis/references/product-analyst.md) | measures whether the stated benefit arrived | benefit measurement against the success measure | Result reported with effect size, not just direction |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- A change running in production with a measured benefit and a named owner.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| new-product | Discover and test the product hypothesis before committing build scope | Problem evidence, options and success baseline |
| existing-service-change | Reuse current service controls and assess only changed dependencies | Current baseline, change impact and receiving acceptance |

Return unmet requirements or failed verification to the accountable requirement/design/change owner; retain accepted unchanged work. Stop production effects without current scoped change authority or on failed rollout health criteria. Reject/defer the demand with rationale, or close delivery after observed outcome and receiving service acceptance. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Business outcome and accountable sponsor
- Problem evidence and intended users
- Existing service and change constraints

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return unmet requirements or failed verification to the accountable requirement/design/change owner; retain accepted unchanged work.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop production effects without current scoped change authority or on failed rollout health criteria.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Reject/defer the demand with rationale, or close delivery after observed outcome and receiving service acceptance.

**Bounded paths and scope:**

New and changed products share requirement/design/execution/outcome evidence; current baseline and changed scope differ in values, not schema.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| new-product | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 | 13 |
| existing-service-change | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 | 13 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
