# Service retirement and decommission

`workflow: service-retirement-and-decommission`  ·  `steps: 9`  ·  `tool-tier: route`

**Trigger.** A service, application, platform or technology component is approved for retirement, replacement or exit.

**Outcome.** The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | confirms retirement scope, accountable owner and business/service decision | retirement mandate and target date | Scope and authority are explicit |
| 2 | [Technology Lifecycle and Decommission Manager](../../it-roles-service-management-and-support/references/technology-lifecycle-and-decommission-manager.md) | runs repository impact analysis and builds the retirement/disposition plan | dependency impact and retirement plan | Every material dependency has an owned disposition or named waiver |
| 3 | [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | advises on retention, archive, destruction and privacy obligations where applicable | data disposition position | Regulated/personal data disposition is authorised before irreversible action |
| 4 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | obtains the named human change decision for the exact retirement execution window and rollback boundary | prior scoped human production-change authorisation | Dependency and data-disposition plans and rehearsal evidence are available before destructive action; approval covers exact credential and service changes, not a completed retirement |
| 5 | [Identity and Access Management Engineer](../../it-roles-security-operations-and-defensive-security/references/identity-and-access-management-engineer.md) | transfers or revokes approved nonessential access and prepares final credential closure with the shutdown operator | access-transfer evidence and the exact owned, time-bounded shutdown-access list | Prior exact human change approval covers each removal or transfer; retain only explicitly owned bounded shutdown credentials needed for the approved shutdown, with purpose, expiry and final revocation owner |
| 6 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | executes the approved service or platform shutdown and coordinates final credential closure with the assigned IAM actor | actual shutdown, final credential revocation and reconciliation evidence, and verified technical state | Prior exact human change and data-disposition authorisation covers every effect; stop on changed scope or failed dependency/archive checks; the assigned IAM actor closes retained shutdown access and verifies final credential reconciliation before asset reconciliation |
| 7 | [IT Asset Manager](../../it-roles-service-management-and-support/references/it-asset-manager.md) | reconciles CMDB/assets and coordinates licence/supplier closure evidence | asset/configuration closure | Systems of record match the retired technical state |
| 8 | [Architecture Repository and Modelling Lead](../../it-roles-architecture/references/architecture-repository-and-modelling-lead.md) | updates repository lifecycle state, removes/retains views appropriately and records residual dependencies | repository retirement revision | Repository has no unowned active dependency into the retired element |
| 9 | [Benefits Realisation Manager](../../it-roles-product-delivery-and-agile/references/benefits-realisation-manager.md) | measures retirement cost/risk/complexity benefit and records variance | benefits closure result | Benefit or disbenefit variance has an accountable owner |

## Operating this chain

Use `repository.py impact` before retirement and `repository.py decommission` for the canonical lifecycle transition. A blocking active dependency is not converted into a harmless warning; it must be resolved or explicitly waived by the correct authority.

Preparatory work is limited to its explicitly permitted scope. Named human approval must precede every effect it authorises; neither a role title nor a later review supplies authority retrospectively. All policy-required pre-approval evidence remains mandatory. Collect candidate evidence only within explicitly permitted pre-production scope. If policy requires operational proof, obtain a separate prior named human approval for the bounded pilot needed to collect it, then seek the wider approval; no pilot permission is implied. If no governing route permits the required evidence collection, stop and consult the accountable authority before proceeding. Any policy-permitted waiver must already be issued by the competent named human authority for the exact gate, scope and validity period before the gated action; non-waivable controls remain blocking.
