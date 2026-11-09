# Supplier onboarding to exit

`workflow: supplier-onboarding`  ·  `steps: 7`  ·  `tool-tier: route`

**Trigger.** A technology supplier or SaaS product is being considered.

**Outcome.** A contracted supplier with assurance, monitored performance and a tested way out.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [IT Procurement Specialist](../../it-roles-commercial-sourcing-and-enablement/references/it-procurement-specialist.md) | runs the selection with the right requirements in the tender | tender, evaluation and recommendation | Security, privacy, exit and continuity requirements in the tender, not added after |
| 2 | [Third-Party Risk Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/third-party-risk-manager.md) | assesses and tiers the supplier risk | risk assessment and tier | Critical suppliers have a tested exit or substitution plan |
| 3 | [Security Architect](../../it-roles-architecture/references/security-architect.md) | sets the control requirements the supplier must meet | supplier control requirements | Requirements traced to threats, not copied from a questionnaire |
| 4 | [Contract Manager](../../it-roles-commercial-sourcing-and-enablement/references/contract-manager.md) | extracts obligations into a tracked register | contract and obligation register | Obligations on both sides tracked with owners |
| 5 | [Vendor Manager](../../it-roles-commercial-sourcing-and-enablement/references/vendor-manager.md) | manages performance and the relationship after signature | scorecards and governance cadence | Renewal started early enough for a real alternative to exist |
| 6 | [Service Level Manager](../../it-roles-service-management-and-support/references/service-level-manager.md) | aligns supplier commitments with what was promised internally | aligned SLAs and OLAs | No internal commitment exceeding what the supply chain can deliver |
| 7 | [Business Continuity Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/business-continuity-manager.md) | proves the organisation survives the supplier failing | exercised continuity and exit plan | Exit tested, not described |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `advise`, `author`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- A contracted supplier with assurance, monitored performance and a tested way out.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| ordinary | Assess comparable offers and proportionate service obligations | Declared criteria, supplier responses and owned contract measures |
| critical | Exercise continuity/substitution and test enforceable exit | Dependency risks, recovery/exit evidence and residual decisions |

Return noncomparable responses, unowned obligations or failed exit tests to procurement/contract/supplier owners. Stop commitments beyond authority or activation with unresolved mandatory supplier/security/privacy obligations. Accept the governed supplier service or terminate selection/exit with retained obligations and data/access disposition. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Sourcing requirements and owner
- Supplier/service criticality and data use
- Procurement rules and contract decision rights

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return noncomparable responses, unowned obligations or failed exit tests to procurement/contract/supplier owners.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop commitments beyond authority or activation with unresolved mandatory supplier/security/privacy obligations.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the governed supplier service or terminate selection/exit with retained obligations and data/access disposition.

**Bounded paths and scope:**

Criticality changes continuity/exit depth; all suppliers retain accountable obligations and proportionate assurance.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| ordinary | 1, 2, 3, 4, 5, 6, 7 | 7 |
| critical | 1, 2, 3, 4, 5, 6, 7 | 7 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
