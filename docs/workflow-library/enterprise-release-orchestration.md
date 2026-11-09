# Enterprise release orchestration

## Trigger

Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process.

## Intended outcome

The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| coordinated | Sequence dependent releases and validate integrated readiness | Dependency register, business/supplier/technical/security readiness |
| staged | Use bounded waves with evidence-driven continuation and recovery | Wave criteria, actual results, abort triggers and remaining exposure |

Return failed independent gates to producer owners; changed artifacts/readiness need corresponding renewed review. Stop execution without exact go/no-go authority or when approved abort/reversal triggers fire. Close with actual end-to-end outcome, residual issues and service-owner acceptance, or execute the authorised recovery branch. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Integrated release scope/calendar and business windows
- Owned application/data/supplier dependencies
- Readiness criteria and go/no-go authority

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed independent gates to producer owners; changed artifacts/readiness need corresponding renewed review.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop execution without exact go/no-go authority or when approved abort/reversal triggers fire.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close with actual end-to-end outcome, residual issues and service-owner acceptance, or execute the authorised recovery branch.

**Bounded paths and scope:**

Coordinated/staged release share readiness, authority and actual observation requirements, with explicit wave boundaries.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| coordinated | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| staged | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Enterprise release orchestration workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Enterprise Release Manager</strong><p>builds integrated release scope/calendar and identifies cross-system dependencies/blackouts</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Architecture Repository and Modelling Lead</strong><p>validates technical/service dependency graph and critical sequencing constraints</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Organisational Change and Adoption Manager</strong><p>validates communications/training/adoption/business readiness for affected cohorts</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Data Migration and Cutover Lead</strong><p>validates cutover sequence, data reconciliation, checkpoints and abort criteria</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>SIAM Manager</strong><p>validates supplier staffing, dependencies, handoffs and escalation readiness</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Release Engineer</strong><p>validates technical release artefacts, provenance and executable rollback</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Secure Delivery / DevSecOps Architect</strong><p>checks that release provenance, pipeline controls, policy-as-code and software supply-chain evidence conform to the approved secure-delivery architecture</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Release Quality Gatekeeper</strong><p>independently checks mandatory release criteria and evidence</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Enterprise Release Manager</strong><p>issues delegated integrated go/no-go or routes decision to higher authority</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Release Engineer</strong><p>executes the authorised technical release through controlled pipelines</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>Site Reliability Engineer</strong><p>monitors agreed technical/service signals and triggers reversal if thresholds breach</p></div></li>
<li data-step="12"><span class="ai-workflow-step-number" aria-hidden="true">12</span><div><strong>IT Service Owner</strong><p>confirms business/service outcome and closes or escalates residual issues</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-enterprise-release-orchestration.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Enterprise Release Manager | builds integrated release scope/calendar and identifies cross-system dependencies/blackouts | integrated release calendar | All material releases and blackout/business constraints are represented |
| 2 | Architecture Repository and Modelling Lead | validates technical/service dependency graph and critical sequencing constraints | release dependency register | No critical dependency is missing an owner or sequence |
| 3 | Organisational Change and Adoption Manager | validates communications/training/adoption/business readiness for affected cohorts | business readiness | Affected business cohorts have executable readiness actions/evidence |
| 4 | Data Migration and Cutover Lead | validates cutover sequence, data reconciliation, checkpoints and abort criteria | cutover readiness | Cutover and data reconciliation are rehearsed/evidenced for critical transitions |
| 5 | SIAM Manager | validates supplier staffing, dependencies, handoffs and escalation readiness | supplier readiness | No critical supplier dependency is relying on informal availability |
| 6 | Release Engineer | validates technical release artefacts, provenance and executable rollback | technical/rollback readiness | Release artefacts are traceable and rollback is exercised/feasible |
| 7 | Secure Delivery / DevSecOps Architect | checks that release provenance, pipeline controls, policy-as-code and software supply-chain evidence conform to the approved secure-delivery architecture | secure delivery readiness evidence | Critical secure-delivery controls and provenance are evidenced; deviations are owned, time-bound and visible to independent release assurance |
| 8 | Release Quality Gatekeeper | independently checks mandatory release criteria and evidence | release gate assurance | Producer cannot waive its own failed critical gate |
| 9 | Enterprise Release Manager | issues delegated integrated go/no-go or routes decision to higher authority | go/no-go decision | Decision cites evidence, waivers, residual risk and abort triggers |
| 10 | Release Engineer | executes the authorised technical release through controlled pipelines | release execution evidence | Executed artefacts/plan match what was approved |
| 11 | Site Reliability Engineer | monitors agreed technical/service signals and triggers reversal if thresholds breach | technical post-release validation | Rollback/reversal triggers are acted on, not debated after breach |
| 12 | IT Service Owner | confirms business/service outcome and closes or escalates residual issues | release acceptance | Closure states outcome, impact, residual issues and owners |

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

> Apply the `enterprise-release-orchestration` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
