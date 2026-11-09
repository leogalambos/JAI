# Production change

`workflow: production-change`  ·  `steps: 8`  ·  `tool-tier: route`

**Trigger.** A change must reach production: a feature, a fix, an infrastructure change or a configuration change.

**Outcome.** The change in production, recorded, with a proven way back.

The point of this chain is that nobody both authorises and implements. Where headcount forces it, record the combination as an accepted control weakness with a compensating review.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | produces the change with its rollback path designed first | reviewed change and rollback plan | Small enough to review in one pass |
| 2 | [Infrastructure as Code Engineer](../../it-roles-infrastructure-cloud-and-operations/references/infrastructure-as-code-engineer.md) | produces any infrastructure change as a reviewed plan | reviewed plan; destructive operations flagged | The applied plan is the reviewed plan |
| 3 | [Test Analyst](../../it-roles-quality-and-testing/references/test-analyst.md) | verifies and states what is not covered | test evidence with coverage and residual risk | Residual risk accepted by a named person |
| 4 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | packages the release and verifies provenance | release manifest with signed provenance | Every artefact traceable to a source commit |
| 5 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | authorises at the level the risk class requires | change record and schedule slot | Standard changes pre-authorised and measured, not queued for ceremony |
| 6 | [GitOps and Continuous Delivery Engineer](../../it-roles-software-development-and-engineering/references/gitops-and-continuous-delivery-engineer.md) | deploys progressively behind a health gate | rollout with automatic reversal armed | Rollback exercised, not merely documented |
| 7 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | watches the agreed signals for the agreed window | post-release confirmation or a reversal decision | Reversal executed on trigger, not on debate |
| 8 | [Configuration Manager](../../it-roles-service-management-and-support/references/configuration-manager.md) | updates the record of what now exists | updated configuration items | Record updated the same day the change lands |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- The change in production, recorded, with a proven way back.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| standard | Use a current preauthorised standard change only within its measured bounds | Applicable standard model/version and observed change results |
| normal | Obtain the risk-appropriate decision before deployment | Reviewed candidate, test evidence and exact authority decision |
| emergency | Use the prior authorised emergency route and explicit scope | Urgency, eligible authority, emergency record and later review |

Return failed review/tests to the source owner before seeking another decision; a changed plan needs corresponding review. Stop on scope drift, absent authority, failed health gate or unsafe recovery condition. Close with actual health and configuration reconciliation, or execute the previously authorised reversal/forward recovery route. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Exact candidate scope and current baseline
- Change risk and eligible authority route
- Verification and recovery criteria

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed review/tests to the source owner before seeking another decision; a changed plan needs corresponding review.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop on scope drift, absent authority, failed health gate or unsafe recovery condition.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close with actual health and configuration reconciliation, or execute the previously authorised reversal/forward recovery route.

**Bounded paths and scope:**

Approval class is separate from application/IaC/settings mechanism; exact authored alternatives prevent fabricated code or IaC evidence.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| standard/application | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| standard/infrastructure-as-code | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| standard/configuration | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| normal/application | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| normal/infrastructure-as-code | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| normal/configuration | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| emergency/application | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| emergency/infrastructure-as-code | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| emergency/configuration | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
