# Demand to portfolio to funding

## Trigger

A new business/technology demand needs to be qualified, compared with alternatives and either rejected, redirected or committed into a funded portfolio.

## Intended outcome

Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| discovery | Reject, redirect or investigate uncertain need before detailed commitment | Qualification evidence, alternatives and next decision |
| funding | Compare risk/value, lifecycle, cost and capacity against declared criteria | Reconstructible prioritisation and actual funding/commitment authority |

Return unsupported value, lifecycle or estimate assumptions to their accountable owners. Stop anonymous/outcome-free prioritisation and commitments lacking eligible authority, funding or capacity basis. Record reject/redirect/discover/defer/commit with rationale and accountable review condition. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Named demand owner and business outcome
- Capability/application baseline and constraints
- Decision criteria, cost horizon and available capacity

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return unsupported value, lifecycle or estimate assumptions to their accountable owners.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop anonymous/outcome-free prioritisation and commitments lacking eligible authority, funding or capacity basis.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Record reject/redirect/discover/defer/commit with rationale and accountable review condition.

**Bounded paths and scope:**

Discovery terminates after qualification; a funding commitment requires the downstream evidence and eligible authority.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| discovery | 1, 2 | 2 |
| funding | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Demand to portfolio to funding workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Demand &amp; Intake Manager</strong><p>captures demand with owner, problem/outcome, urgency and evidence status</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Demand &amp; Intake Manager</strong><p>qualifies completeness, duplicates, mandatory obligations and routing</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Enterprise Architect</strong><p>checks business capability fit, reuse and enterprise target-state alignment</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Application Portfolio Manager</strong><p>assesses affected application portfolio, lifecycle posture, duplication and invest/tolerate/migrate/retire consequences</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Solution Architect</strong><p>assesses architecture/integration/data/security/operational impact at decision-appropriate depth</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>IT Risk Manager</strong><p>frames risk/opportunity, compliance urgency and value-at-risk alongside benefit evidence</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Resource Manager</strong><p>coordinates indicative sizing and scarce-capability/capacity demand</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Portfolio Manager</strong><p>applies transparent prioritisation criteria across value, risk, strategy, capacity and dependencies</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>IT Financial Management / TBM Manager</strong><p>validates TCO/funding profile and financial comparability</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Portfolio Manager</strong><p>makes or routes the delegated funding/portfolio commitment decision</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-demand-to-portfolio-to-funding.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Demand & Intake Manager | captures demand with owner, problem/outcome, urgency and evidence status | demand record | No anonymous or outcome-free demand enters prioritisation |
| 2 | Demand & Intake Manager | qualifies completeness, duplicates, mandatory obligations and routing | qualification assessment | Disposition is explicit: reject, redirect, discover or assess |
| 3 | Enterprise Architect | checks business capability fit, reuse and enterprise target-state alignment | capability-fit assessment | Existing capability/service reuse and strategic conflicts are explicit |
| 4 | Application Portfolio Manager | assesses affected application portfolio, lifecycle posture, duplication and invest/tolerate/migrate/retire consequences | application portfolio impact assessment | Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner |
| 5 | Solution Architect | assesses architecture/integration/data/security/operational impact at decision-appropriate depth | architecture impact assessment | Material cross-domain dependencies and constraints are identified |
| 6 | IT Risk Manager | frames risk/opportunity, compliance urgency and value-at-risk alongside benefit evidence | risk/value assessment | Regulatory/risk urgency is evidence-based and not double-counted as value |
| 7 | Resource Manager | coordinates indicative sizing and scarce-capability/capacity demand | estimate and capacity view | Uncertainty ranges and constrained skills/capacity are explicit |
| 8 | Portfolio Manager | applies transparent prioritisation criteria across value, risk, strategy, capacity and dependencies | prioritisation decision | Prioritisation can be reconstructed from declared criteria and exceptions |
| 9 | IT Financial Management / TBM Manager | validates TCO/funding profile and financial comparability | funding economics and cost profile | Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model |
| 10 | Portfolio Manager | makes or routes the delegated funding/portfolio commitment decision | portfolio commitment | Commitment has authority, funding/capacity basis and review condition |

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

> Apply the `demand-to-portfolio-to-funding` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
