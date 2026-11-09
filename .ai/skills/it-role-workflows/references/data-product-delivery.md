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

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- A governed, documented, monitored data product with an owner.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| nonpersonal | Apply governed definitions, lineage and fit-for-purpose quality measurement | Source access, tested transforms and agreed metric definitions |
| personal-regulated | Resolve privacy/jurisdiction obligations before processing and test controls | Competent impact/applicability position and permitted processing scope |

Return definition conflicts to the data owner/steward and failed quality checks to the producing transform owner. Stop processing outside authorised purpose or when mandatory privacy/control prerequisites are unresolved. Accept the product for its bounded use or withdraw it with consumer notification and owned correction/retention actions. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Intended data use and accountable data owner
- Source definitions and access/processing permissions
- Quality tolerances and receiving consumer needs

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return definition conflicts to the data owner/steward and failed quality checks to the producing transform owner.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop processing outside authorised purpose or when mandatory privacy/control prerequisites are unresolved.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the product for its bounded use or withdraw it with consumer notification and owned correction/retention actions.

**Bounded paths and scope:**

Nonpersonal use replaces privacy/DPIA work with evidenced classification and bounded permitted-use decision; personal/regulated use retains competent impact review.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| nonpersonal | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| personal-regulated | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.

**Context guards:**

- **nonpersonal** requires evidence that the statement "personal data are processed" is false; unknown applicability remains pending.
<!-- END workflow-applicability -->
