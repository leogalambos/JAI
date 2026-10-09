# Data product delivery

`workflow: data-product-delivery`  ·  `steps: 8`  ·  `tool-tier: route`

**Trigger.** A business area needs a trusted dataset, metric or report.

**Outcome.** A governed, documented, monitored data product with an owner.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Data Governance Lead](../../it-roles-data-analytics-and-ai/references/data-governance-lead.md) | confirms the critical data elements, owners and tolerances | governed element definitions | Owner, steward, definition and quality tolerance exist |
| 2 | [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | advises on lawful basis and minimisation | privacy position and DPIA where required | DPIA completed before processing begins |
| 3 | [Data Architect](../../it-roles-architecture/references/data-architect.md) | designs the structures and the flows, including trust boundaries | data model and flow design | Every flow crossing a trust or jurisdiction boundary has a control |
| 4 | [Data Engineer](../../it-roles-data-analytics-and-ai/references/data-engineer.md) | builds the pipelines with declared quality expectations | pipelines with freshness and completeness checks | Checks fail loudly rather than degrading silently |
| 5 | [Analytics Engineer](../../it-roles-data-analytics-and-ai/references/analytics-engineer.md) | models and tests the consumable datasets | tested, documented models with lineage | Uniqueness, referential integrity and freshness tested |
| 6 | [Data Quality Analyst](../../it-roles-data-analytics-and-ai/references/data-quality-analyst.md) | measures fitness against the stated purpose | quality measurement against tolerance | No bare percentage without a fitness-for-purpose statement |
| 7 | [Business Intelligence Analyst](../../it-roles-analysis/references/business-intelligence-analyst.md) | publishes the reporting product on agreed definitions | dashboards on a single agreed metric definition | Two dashboards may not disagree silently |
| 8 | [Data Steward](../../it-roles-data-analytics-and-ai/references/data-steward.md) | runs it day to day and arbitrates definition disputes | stewardship decisions and issue log | Competing definitions escalated, not averaged |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
