# Service retirement and decommission

## Trigger

A service, application, platform or technology component is approved for retirement, replacement or exit.

## Intended outcome

The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured.


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

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Service retirement and decommission workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>IT Service Owner</strong><p>confirms retirement scope, accountable owner and business/service decision</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Technology Lifecycle and Decommission Manager</strong><p>runs repository impact analysis and builds the retirement/disposition plan</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Data Protection Officer</strong><p>advises on retention, archive, destruction and privacy obligations where applicable</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Change Manager</strong><p>obtains the named human change decision for the exact retirement execution window and rollback boundary</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Identity and Access Management Engineer</strong><p>transfers or revokes approved nonessential access and prepares final credential closure with the shutdown operator</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Site Reliability Engineer</strong><p>executes the approved service or platform shutdown and coordinates final credential closure with the assigned IAM actor</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>IT Asset Manager</strong><p>reconciles CMDB/assets and coordinates licence/supplier closure evidence</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Architecture Repository and Modelling Lead</strong><p>updates repository lifecycle state, removes/retains views appropriately and records residual dependencies</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Benefits Realisation Manager</strong><p>measures retirement cost/risk/complexity benefit and records variance</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-service-retirement-and-decommission.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | IT Service Owner | confirms retirement scope, accountable owner and business/service decision | retirement mandate and target date | Scope and authority are explicit |
| 2 | Technology Lifecycle and Decommission Manager | runs repository impact analysis and builds the retirement/disposition plan | dependency impact and retirement plan | Every material dependency has an owned disposition or named waiver |
| 3 | Data Protection Officer | advises on retention, archive, destruction and privacy obligations where applicable | data disposition position | Regulated/personal data disposition is authorised before irreversible action |
| 4 | Change Manager | obtains the named human change decision for the exact retirement execution window and rollback boundary | prior scoped human production-change authorisation | Dependency and data-disposition plans and rehearsal evidence are available before destructive action; approval covers exact credential and service changes, not a completed retirement |
| 5 | Identity and Access Management Engineer | transfers or revokes approved nonessential access and prepares final credential closure with the shutdown operator | access-transfer evidence and the exact owned, time-bounded shutdown-access list | Prior exact human change approval covers each removal or transfer; retain only explicitly owned bounded shutdown credentials needed for the approved shutdown, with purpose, expiry and final revocation owner |
| 6 | Site Reliability Engineer | executes the approved service or platform shutdown and coordinates final credential closure with the assigned IAM actor | actual shutdown, final credential revocation and reconciliation evidence, and verified technical state | Prior exact human change and data-disposition authorisation covers every effect; stop on changed scope or failed dependency/archive checks; the assigned IAM actor closes retained shutdown access and verifies final credential reconciliation before asset reconciliation |
| 7 | IT Asset Manager | reconciles CMDB/assets and coordinates licence/supplier closure evidence | asset/configuration closure | Systems of record match the retired technical state |
| 8 | Architecture Repository and Modelling Lead | updates repository lifecycle state, removes/retains views appropriately and records residual dependencies | repository retirement revision | Repository has no unowned active dependency into the retired element |
| 9 | Benefits Realisation Manager | measures retirement cost/risk/complexity benefit and records variance | benefits closure result | Benefit or disbenefit variance has an accountable owner |

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

> Apply the `service-retirement-and-decommission` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.

Approval and execution are separate handoffs. Candidate preparation stays within explicitly permitted pre-production scope. Every production, pilot, credential or irreversible effect requires prior exact named human authority under the applicable policy. If operational proof is required before a wider approval, obtain separate prior authorisation for the bounded pilot needed to collect it; if no policy route permits collection, stop and consult the authority. Draft rendering and review evidence do not release a publication. An existing policy-permitted waiver must identify the competent human authority, exact gate and scope, and validity period before the gated action; mandatory controls and unsupported factual claims remain blocking.
