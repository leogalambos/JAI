# Business case to realised benefits

## Trigger

An investment has a proposed business case and needs measurable benefits governed through and beyond delivery.

## Intended outcome

Benefits are baselined, owned, measured after go-live and used for continue/correct/close decisions.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Benefits are baselined, owned, measured after go-live and used for continue/correct/close decisions.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| new-investment | Compare feasible options including the baseline before committing benefits | Reconciled costs, benefit owners and sensitivity |
| continuation-review | Use actual observations and revise forecasts transparently | Preagreed method, variance, disbenefits and continued-investment decision |

Return unsupported benefit assumptions or double-counted value to the financial/benefit owner. Stop an unsupported funding claim or commitment outside actual portfolio authority. Approve/defer/reject investment or close a benefits period with owned corrective actions and a review condition. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Investment decision boundary and sponsor
- Outcome baseline and measurement sources
- Cost/benefit horizon and capacity assumptions

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return unsupported benefit assumptions or double-counted value to the financial/benefit owner.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop an unsupported funding claim or commitment outside actual portfolio authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Approve/defer/reject investment or close a benefits period with owned corrective actions and a review condition.

**Bounded paths and scope:**

Investment and continuation share evidenced options, baselines and accountability; future benefits stay forecasts until actually observed.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| new-investment | 1, 2, 3, 4, 5, 6, 7 | 7 |
| continuation-review | 1, 2, 3, 4, 5, 6, 7 | 7 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Business case to realised benefits workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Portfolio Manager</strong><p>qualifies the investment against strategy, capacity and funding constraints</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Business Analyst</strong><p>makes the problem, scope, assumptions and outcome measures testable</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Benefits Realisation Manager</strong><p>turns the case into owned benefits with baselines, targets and dependencies</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Product Manager</strong><p>aligns product outcomes and roadmap to the benefit hypotheses</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Organisational Change and Adoption Manager</strong><p>defines adoption dependencies and measures behavioural readiness</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Product Analyst</strong><p>measures post-go-live outcomes from the agreed sources</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Benefits Realisation Manager</strong><p>compares actuals to the approved case and recommends action</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-business-case-to-benefits.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Portfolio Manager | qualifies the investment against strategy, capacity and funding constraints | investment decision context and thresholds | The initiative has an accountable sponsor and an explicit decision threshold |
| 2 | Business Analyst | makes the problem, scope, assumptions and outcome measures testable | requirements and outcome baseline | Outcome statements are measurable and sourced |
| 3 | Benefits Realisation Manager | turns the case into owned benefits with baselines, targets and dependencies | benefits map, register and realisation plan | No benefit without owner, baseline, target, source and timing |
| 4 | Product Manager | aligns product outcomes and roadmap to the benefit hypotheses | roadmap with success measures | Roadmap outcomes trace to registered benefits rather than feature volume |
| 5 | Organisational Change and Adoption Manager | defines adoption dependencies and measures behavioural readiness | adoption plan and readiness measures | Benefit dependencies on behaviour have explicit owners and measures |
| 6 | Product Analyst | measures post-go-live outcomes from the agreed sources | observed benefit results and confidence | Results use the pre-agreed method and disclose uncertainty |
| 7 | Benefits Realisation Manager | compares actuals to the approved case and recommends action | post-implementation benefits review | Variance, disbenefits and corrective actions are owned and decision-ready |

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

> Apply the `business-case-to-benefits` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
