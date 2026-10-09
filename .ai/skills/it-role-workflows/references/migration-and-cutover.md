# Migration and cutover

`workflow: migration-and-cutover`  ·  `steps: 8`  ·  `tool-tier: route`

**Trigger.** A project must move data/services from a current state to a target state through a controlled production cutover.

**Outcome.** Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.

This chain is an enterprise hand-off model, not a rigid project schedule. Run steps in parallel where sensible, but do not skip the acceptance gate between accountable roles.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Data Architect](../../it-roles-architecture/references/data-architect.md) | defines source/target models, authoritative ownership and data constraints | migration data model and ownership boundaries | Every migrated domain has an accountable data owner and target definition |
| 2 | [Data Migration and Cutover Lead](../../it-roles-product-delivery-and-agile/references/data-migration-and-cutover-lead.md) | builds migration strategy, reconciliation rules and integrated cutover sequence | migration plan, cutover runbook and rollback plan | Every object has mapping, acceptance and rollback/restore semantics |
| 3 | [Data Engineer](../../it-roles-data-analytics-and-ai/references/data-engineer.md) | implements and rehearses migration pipelines against production-like volume | migration execution evidence and exceptions | Rehearsal proves throughput, error handling and repeatability |
| 4 | [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | independently assesses migration, reconciliation and business acceptance evidence | test and residual-risk report | Exit criteria were defined before execution and are met or explicitly waived |
| 5 | [Service Transition and Operational Readiness Manager](../../it-roles-service-management-and-support/references/service-transition-and-operational-readiness-manager.md) | confirms monitoring, support, recovery and receiving-team readiness | operational cutover constraints and acceptance evidence | No critical operational readiness gap is unowned |
| 6 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | integrates deployment artefacts with the cutover critical path | release manifest and deployment/rollback evidence | Exact artefact versions and rollback steps are known |
| 7 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | authorises the production window and stop/go governance | production change authorisation | Rehearsal, reconciliation and operational evidence are available to the decision |
| 8 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | accepts the migrated service after stability and reconciliation checks | service acceptance and residual issues | Service, data and ownership acceptance are explicit before legacy retirement |

## Operating this chain

Read the linked role reference before acting as a step and use the operator agent declared for that role's tool tier. A hand-off is complete only when the receiving step applies the stated gate and accepts the evidence. Failed gates remain explicit; they are not converted into assumptions simply to preserve a milestone.
