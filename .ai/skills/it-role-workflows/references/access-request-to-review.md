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

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Access that is appropriate, evidenced, and removed when no longer needed.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| ordinary | Apply least-privilege decisions and integrated provisioning | Specific decision, actual grant/refusal and revocation evidence |
| privileged | Apply vaulting, session monitoring and reviewed break-glass arrangements | Privileged decision, monitoring and exercised emergency access |
| leaver-transfer | Revoke or transfer entitlements at the actual lifecycle event | Event, actual revocations, residual access owner and expiry |

Return purpose-free or ambiguous requests to the requester/data owner; failed provisioning returns to IAM with actual observations. Stop granting access without a valid individual decision, required identity proof or current privileged-access scope. Close on evidenced grant/refusal/revocation; retain certification and independent audit findings with owners. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Subject identity and requested entitlement
- Justified use purpose and asset policy
- Approval path and identity lifecycle event

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return purpose-free or ambiguous requests to the requester/data owner; failed provisioning returns to IAM with actual observations.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop granting access without a valid individual decision, required identity proof or current privileged-access scope.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close on evidenced grant/refusal/revocation; retain certification and independent audit findings with owners.

**Bounded paths and scope:**

Ordinary/privileged/lifecycle requests require the actual decision, identity lifecycle evidence and applicable privileged-control disposition; no access event is inferred.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| ordinary | 1, 2, 3, 5, 6 | 6 |
| privileged | 1, 2, 3, 4, 5, 6 | 6 |
| leaver-transfer | 1, 2, 3, 5, 6 | 6 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
