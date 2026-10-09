# Service retirement and decommission

`workflow: service-retirement-and-decommission`  ·  `steps: 8`  ·  `tool-tier: route`

**Trigger.** A service, application, platform or technology component is approved for retirement, replacement or exit.

**Outcome.** The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | confirms retirement scope, accountable owner and business/service decision | retirement mandate and target date | Scope and authority are explicit |
| 2 | [Technology Lifecycle and Decommission Manager](../../it-roles-service-management-and-support/references/technology-lifecycle-and-decommission-manager.md) | runs repository impact analysis and builds the retirement/disposition plan | dependency impact and retirement plan | Every material dependency has an owned disposition or named waiver |
| 3 | [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | advises on retention, archive, destruction and privacy obligations where applicable | data disposition position | Regulated/personal data disposition is authorised before irreversible action |
| 4 | [Identity and Access Management Engineer](../../it-roles-security-operations-and-defensive-security/references/identity-and-access-management-engineer.md) | removes/transfers identities, privileged access, secrets/certificates as assigned | access/credential closure evidence | No active credential remains without owner and purpose |
| 5 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | applies the authorised production-change path and rollback boundary | approved execution window/decision | Destructive steps are within approved change authority |
| 6 | [IT Asset Manager](../../it-roles-service-management-and-support/references/it-asset-manager.md) | reconciles CMDB/assets and coordinates licence/supplier closure evidence | asset/configuration closure | Systems of record match the retired technical state |
| 7 | [Architecture Repository and Modelling Lead](../../it-roles-architecture/references/architecture-repository-and-modelling-lead.md) | updates repository lifecycle state, removes/retains views appropriately and records residual dependencies | repository retirement revision | Repository has no unowned active dependency into the retired element |
| 8 | [Benefits Realisation Manager](../../it-roles-product-delivery-and-agile/references/benefits-realisation-manager.md) | measures retirement cost/risk/complexity benefit and records variance | benefits closure result | Benefit or disbenefit variance has an accountable owner |

## Operating this chain

Use `repository.py impact` before retirement and `repository.py decommission` for the canonical lifecycle transition. A blocking active dependency is not converted into a harmless warning; it must be resolved or explicitly waived by the correct authority.
