# Access request to periodic review

`workflow: access-request-to-review`  ·  `steps: 6`  ·  `tool-tier: route`

**Trigger.** Someone needs access, changes role, or leaves.

**Outcome.** Access that is appropriate, evidenced, and removed when no longer needed.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Service Desk Analyst](../../it-roles-service-management-and-support/references/service-desk-analyst.md) | records the request against a catalogue entitlement | request with entitlement and approval path | Entitlement and approval path defined for the request type |
| 2 | [Data Owner](../../it-roles-data-analytics-and-ai/references/data-owner.md) | or application owner decides whether the purpose justifies access | access decision recorded with its purpose | Purpose-free access grants refused |
| 3 | [Identity and Access Management Engineer](../../it-roles-security-operations-and-defensive-security/references/identity-and-access-management-engineer.md) | provisions through the identity platform | provisioned access, automated where integrated | Leaver revocation evidenced automatically, not attested |
| 4 | [Privileged Access Management Administrator](../../it-roles-security-operations-and-defensive-security/references/privileged-access-management-administrator.md) | vaults and monitors anything privileged | vaulted account with session monitoring | Break-glass tested on a schedule; every use reviewed |
| 5 | [Identity Governance Specialist](../../it-roles-security-operations-and-defensive-security/references/identity-governance-specialist.md) | certifies periodically that access is still appropriate | certification campaign results | Reviewers have actual knowledge of the access |
| 6 | [Internal IT Auditor](../../it-roles-governance-risk-compliance-audit-and-privacy/references/internal-it-auditor.md) | tests the control independently | audit finding or assurance | Auditor never operated the control |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
