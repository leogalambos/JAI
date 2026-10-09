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
