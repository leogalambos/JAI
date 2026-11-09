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

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| reversible-preparation | Prepare archives, dependency changes and bounded shutdown access without premature retirement | Plan/rehearsal evidence and scope-specific access ownership |
| authorised-retirement | Execute exact approved shutdown/data/credential effects and reconcile state | Prior decisions, actual execution, final access revocation and records reconciliation |

Return unresolved dependencies, archive failures or unowned retained access to their owners before destructive action. Stop irreversible effects outside exact authority or on failed dependency, data, credential or recovery criteria. Complete final credential/asset/model reconciliation and benefit closure, or use the authorised recovery/deferral route. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Actual retirement mandate and exact service/assets
- Owned dependency and data-disposition plans
- Rehearsal and prior production-change authority

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return unresolved dependencies, archive failures or unowned retained access to their owners before destructive action.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop irreversible effects outside exact authority or on failed dependency, data, credential or recovery criteria.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Complete final credential/asset/model reconciliation and benefit closure, or use the authorised recovery/deferral route.

**Bounded paths and scope:**

Reversible preparation terminates before authorisation for destructive execution; retirement retains actual credential/data/asset reconciliation.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| reversible-preparation | 1, 2, 3 | 3 |
| authorised-retirement | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 9 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
