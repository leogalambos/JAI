# Migration and cutover

`workflow: migration-and-cutover`  ·  `steps: 11`  ·  `tool-tier: route`

**Trigger.** A project must move data/services from a current state to a target state through a controlled production cutover.

**Outcome.** Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.

This chain is an enterprise hand-off model, not a rigid project schedule. Run steps in parallel where sensible, but do not skip the acceptance gate between accountable roles.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Data Architect](../../it-roles-architecture/references/data-architect.md) | defines source/target models, authoritative ownership and data constraints | migration data model and ownership boundaries | Every migrated domain has an accountable data owner and target definition |
| 2 | [Data Migration and Cutover Lead](../../it-roles-product-delivery-and-agile/references/data-migration-and-cutover-lead.md) | builds migration strategy, reconciliation rules and integrated cutover sequence | migration plan, cutover runbook and rollback plan | Every object has mapping, acceptance and rollback/restore semantics |
| 3 | [Data Engineer](../../it-roles-data-analytics-and-ai/references/data-engineer.md) | implements and rehearses candidate migration pipelines in the explicitly permitted pre-production environment | pre-production rehearsal evidence and exceptions | Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects |
| 4 | [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | independently assesses migration, reconciliation and business acceptance evidence | test and residual-risk report | Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking |
| 5 | [Service Transition and Operational Readiness Manager](../../it-roles-service-management-and-support/references/service-transition-and-operational-readiness-manager.md) | confirms monitoring, support, recovery and receiving-team readiness | operational cutover constraints and acceptance evidence | No critical operational readiness gap is unowned |
| 6 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | prepares the candidate release manifest and rehearses deployment and rollback within the permitted pre-production scope | candidate release manifest and rehearsal deployment/rollback evidence | Exact artefact versions and rollback steps are known; no production effects before the human change decision |
| 7 | [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | obtains the named human decision for the production window and stop/go governance | production change authorisation | Pre-production rehearsal, reconciliation design and operational readiness evidence precede exact human authorisation covering cutover and validation effects, data, versions, environment, window and rollback boundaries; no destructive test or data exposure outside that prior approved scope |
| 8 | [Data Engineer](../../it-roles-data-analytics-and-ai/references/data-engineer.md) | executes the approved production cutover with the release operator and records reconciliation and rollback observations | actual cutover execution, reconciliation and stop/go evidence | Prior exact human change authorisation covers data, versions, environment, window and rollback; stop on failed criteria or changed scope |
| 9 | [Test Analyst](../../it-roles-quality-and-testing/references/test-analyst.md) | performs independent actual post-cutover validation of reconciliation, service behaviour and stability against predeclared criteria | executed independent validation cases, observed results, reconciliation evidence and located defects | Prior exact human change authorisation covers the validation effects and data boundaries; no unapproved destructive tests or data exposure; record actual observations and untested conditions without substituting the migration executor's self-check |
| 10 | [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | assesses independent post-cutover validation, reconciliation and stability evidence | independent production validation and residual-risk report | Independent validation uses actual authorised execution evidence against predeclared criteria; unresolved blocking defects prevent service acceptance |
| 11 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | accepts the migrated service after stability and reconciliation checks | service acceptance and residual issues | Service, data and ownership acceptance are explicit before legacy retirement |

## Operating this chain

Read the linked role reference before acting as a step and use the operator agent declared for that role's tool tier. A hand-off is complete only when the receiving step applies the stated gate and accepts the evidence. Failed gates remain explicit; they are not converted into assumptions simply to preserve a milestone.

Preparatory work is limited to its explicitly permitted scope. Named human approval must precede every effect it authorises; neither a role title nor a later review supplies authority retrospectively. All policy-required pre-approval evidence remains mandatory. Collect candidate evidence only within explicitly permitted pre-production scope. If policy requires operational proof, obtain a separate prior named human approval for the bounded pilot needed to collect it, then seek the wider approval; no pilot permission is implied. If no governing route permits the required evidence collection, stop and consult the accountable authority before proceeding. Any policy-permitted waiver must already be issued by the competent named human authority for the exact gate, scope and validity period before the gated action; non-waivable controls remain blocking.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| rehearsal | Exercise permitted data and environments without production cutover effects | Throughput, error handling, repeatability and rollback observations |
| cutover | Execute only the exact prior authorised production plan/window | Authority, actual actions, reconciliation and independent validation |

Return failed rehearsal/reconciliation to migration or data/design owners; preserve valid unchanged evidence. Stop at failed predeclared criteria, changed scope or missing exact production/data authority. Accept migrated service/data/ownership or execute the previously authorised restore/forward-recovery branch before legacy retirement. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Source/target inventory and data owners
- Mapping, reconciliation and recovery semantics
- Permitted rehearsal and production cutover boundaries

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed rehearsal/reconciliation to migration or data/design owners; preserve valid unchanged evidence.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop at failed predeclared criteria, changed scope or missing exact production/data authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept migrated service/data/ownership or execute the previously authorised restore/forward-recovery branch before legacy retirement.

**Bounded paths and scope:**

Rehearsal cannot satisfy actual production execution gates; a rehearsal-only scope stops before production authorisation and cutover.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| rehearsal | 1, 2, 3, 4, 5, 6 | 6 |
| cutover | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | 11 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
