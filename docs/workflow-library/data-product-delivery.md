# Data product delivery

## Trigger

A business area needs a trusted dataset, metric or report.

## Intended outcome

A governed, documented, monitored data product with an owner.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- A governed, documented, monitored data product with an owner.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| nonpersonal | Apply governed definitions, lineage and fit-for-purpose quality measurement | Source access, tested transforms and agreed metric definitions |
| personal-regulated | Resolve privacy/jurisdiction obligations before processing and test controls | Competent impact/applicability position and permitted processing scope |

Return definition conflicts to the data owner/steward and failed quality checks to the producing transform owner. Stop processing outside authorised purpose or when mandatory privacy/control prerequisites are unresolved. Accept the product for its bounded use or withdraw it with consumer notification and owned correction/retention actions. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Intended data use and accountable data owner
- Source definitions and access/processing permissions
- Quality tolerances and receiving consumer needs

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return definition conflicts to the data owner/steward and failed quality checks to the producing transform owner.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop processing outside authorised purpose or when mandatory privacy/control prerequisites are unresolved.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the product for its bounded use or withdraw it with consumer notification and owned correction/retention actions.

**Bounded paths and scope:**

Nonpersonal use replaces privacy/DPIA work with evidenced classification and bounded permitted-use decision; personal/regulated use retains competent impact review.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| nonpersonal | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |
| personal-regulated | 1, 2, 3, 4, 5, 6, 7, 8 | 8 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.

**Context guards:**

- **nonpersonal** requires evidence that the statement "personal data are processed" is false; unknown applicability remains pending.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Data product delivery workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Data Governance Lead</strong><p>confirms the critical data elements, owners and tolerances</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Data Protection Officer</strong><p>advises on lawful basis and minimisation</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Data Architect</strong><p>designs the structures and the flows, including trust boundaries</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Data Engineer</strong><p>builds the pipelines with declared quality expectations</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Analytics Engineer</strong><p>models and tests the consumable datasets</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Data Quality Analyst</strong><p>measures fitness against the stated purpose</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Business Intelligence Analyst</strong><p>publishes the reporting product on agreed definitions</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Data Steward</strong><p>runs it day to day and arbitrates definition disputes</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-data-product-delivery.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Data Governance Lead | confirms the critical data elements, owners and tolerances | governed element definitions | Owner, steward, definition and quality tolerance exist |
| 2 | Data Protection Officer | advises on lawful basis and minimisation | privacy position and DPIA where required | DPIA completed before processing begins |
| 3 | Data Architect | designs the structures and the flows, including trust boundaries | data model and flow design | Every flow crossing a trust or jurisdiction boundary has a control |
| 4 | Data Engineer | builds the pipelines with declared quality expectations | pipelines with freshness and completeness checks | Checks fail loudly rather than degrading silently |
| 5 | Analytics Engineer | models and tests the consumable datasets | tested, documented models with lineage | Uniqueness, referential integrity and freshness tested |
| 6 | Data Quality Analyst | measures fitness against the stated purpose | quality measurement against tolerance | No bare percentage without a fitness-for-purpose statement |
| 7 | Business Intelligence Analyst | publishes the reporting product on agreed definitions | dashboards on a single agreed metric definition | Two dashboards may not disagree silently |
| 8 | Data Steward | runs it day to day and arbitrates definition disputes | stewardship decisions and issue log | Competing definitions escalated, not averaged |

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

> Apply the `data-product-delivery` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
