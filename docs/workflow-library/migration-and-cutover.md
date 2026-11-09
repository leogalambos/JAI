# Migration and cutover

## Trigger

A project must move data/services from a current state to a target state through a controlled production cutover.

## Intended outcome

Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.


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

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Migration and cutover workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Data Architect</strong><p>defines source/target models, authoritative ownership and data constraints</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Data Migration and Cutover Lead</strong><p>builds migration strategy, reconciliation rules and integrated cutover sequence</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Data Engineer</strong><p>implements and rehearses candidate migration pipelines in the explicitly permitted pre-production environment</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Test Manager</strong><p>independently assesses migration, reconciliation and business acceptance evidence</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Service Transition and Operational Readiness Manager</strong><p>confirms monitoring, support, recovery and receiving-team readiness</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Release Engineer</strong><p>prepares the candidate release manifest and rehearses deployment and rollback within the permitted pre-production scope</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Change Manager</strong><p>obtains the named human decision for the production window and stop/go governance</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Data Engineer</strong><p>executes the approved production cutover with the release operator and records reconciliation and rollback observations</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Test Analyst</strong><p>performs independent actual post-cutover validation of reconciliation, service behaviour and stability against predeclared criteria</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Test Manager</strong><p>assesses independent post-cutover validation, reconciliation and stability evidence</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>IT Service Owner</strong><p>accepts the migrated service after stability and reconciliation checks</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-migration-and-cutover.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Data Architect | defines source/target models, authoritative ownership and data constraints | migration data model and ownership boundaries | Every migrated domain has an accountable data owner and target definition |
| 2 | Data Migration and Cutover Lead | builds migration strategy, reconciliation rules and integrated cutover sequence | migration plan, cutover runbook and rollback plan | Every object has mapping, acceptance and rollback/restore semantics |
| 3 | Data Engineer | implements and rehearses candidate migration pipelines in the explicitly permitted pre-production environment | pre-production rehearsal evidence and exceptions | Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects |
| 4 | Test Manager | independently assesses migration, reconciliation and business acceptance evidence | test and residual-risk report | Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking |
| 5 | Service Transition and Operational Readiness Manager | confirms monitoring, support, recovery and receiving-team readiness | operational cutover constraints and acceptance evidence | No critical operational readiness gap is unowned |
| 6 | Release Engineer | prepares the candidate release manifest and rehearses deployment and rollback within the permitted pre-production scope | candidate release manifest and rehearsal deployment/rollback evidence | Exact artefact versions and rollback steps are known; no production effects before the human change decision |
| 7 | Change Manager | obtains the named human decision for the production window and stop/go governance | production change authorisation | Pre-production rehearsal, reconciliation design and operational readiness evidence precede exact human authorisation covering cutover and validation effects, data, versions, environment, window and rollback boundaries; no destructive test or data exposure outside that prior approved scope |
| 8 | Data Engineer | executes the approved production cutover with the release operator and records reconciliation and rollback observations | actual cutover execution, reconciliation and stop/go evidence | Prior exact human change authorisation covers data, versions, environment, window and rollback; stop on failed criteria or changed scope |
| 9 | Test Analyst | performs independent actual post-cutover validation of reconciliation, service behaviour and stability against predeclared criteria | executed independent validation cases, observed results, reconciliation evidence and located defects | Prior exact human change authorisation covers the validation effects and data boundaries; no unapproved destructive tests or data exposure; record actual observations and untested conditions without substituting the migration executor's self-check |
| 10 | Test Manager | assesses independent post-cutover validation, reconciliation and stability evidence | independent production validation and residual-risk report | Independent validation uses actual authorised execution evidence against predeclared criteria; unresolved blocking defects prevent service acceptance |
| 11 | IT Service Owner | accepts the migrated service after stability and reconciliation checks | service acceptance and residual issues | Service, data and ownership acceptance are explicit before legacy retirement |

## Running this workflow: operator and implementer boundary

Use the next prompt in the provider conversation, not as a shell command.
You supply permitted inputs, actual owners, gate acceptance and authority for
real-system changes. The agent returns evidence and blockers; a listed stage
is not proof of execution, approval or release.

For consequential work, explicitly start `/layered` or `$workflow-layered`;
natural-language routing does not universally enforce Fabric. L0 authority
remains human, and Codex protected authority commands require the human's
trusted terminal. Follow the [interaction model](../using/interaction-model.md),
[layered engagement](../using/layered-engagement.md) and
[human authority](../operations/human-authority.md). Keep the workflow-specific
stop conditions and gates on this page.

## How to use this workflow

A practical prompt pattern is:

> Apply the `migration-and-cutover` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.

Approval and execution are separate handoffs. Candidate preparation stays within explicitly permitted pre-production scope. Every production, pilot, credential or irreversible effect requires prior exact named human authority under the applicable policy. If operational proof is required before a wider approval, obtain separate prior authorisation for the bounded pilot needed to collect it; if no policy route permits collection, stop and consult the authority. Draft rendering and review evidence do not release a publication. An existing policy-permitted waiver must identify the competent human authority, exact gate and scope, and validity period before the gated action; mandatory controls and unsupported factual claims remain blocking.
