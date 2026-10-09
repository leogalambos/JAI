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
