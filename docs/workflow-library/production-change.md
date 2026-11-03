# Production change

## Trigger

A change must reach production: a feature, a fix, an infrastructure change or a configuration change.

## Intended outcome

The change in production, recorded, with a proven way back.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Production change workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Software Engineer</strong><p>produces the change with its rollback path designed first</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Infrastructure as Code Engineer</strong><p>produces any infrastructure change as a reviewed plan</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Test Analyst</strong><p>verifies and states what is not covered</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Release Engineer</strong><p>packages the release and verifies provenance</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Change Manager</strong><p>authorises at the level the risk class requires</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>GitOps and Continuous Delivery Engineer</strong><p>deploys progressively behind a health gate</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Site Reliability Engineer</strong><p>watches the agreed signals for the agreed window</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Configuration Manager</strong><p>updates the record of what now exists</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-production-change.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Software Engineer | produces the change with its rollback path designed first | reviewed change and rollback plan | Small enough to review in one pass |
| 2 | Infrastructure as Code Engineer | produces any infrastructure change as a reviewed plan | reviewed plan; destructive operations flagged | The applied plan is the reviewed plan |
| 3 | Test Analyst | verifies and states what is not covered | test evidence with coverage and residual risk | Residual risk accepted by a named person |
| 4 | Release Engineer | packages the release and verifies provenance | release manifest with signed provenance | Every artefact traceable to a source commit |
| 5 | Change Manager | authorises at the level the risk class requires | change record and schedule slot | Standard changes pre-authorised and measured, not queued for ceremony |
| 6 | GitOps and Continuous Delivery Engineer | deploys progressively behind a health gate | rollout with automatic reversal armed | Rollback exercised, not merely documented |
| 7 | Site Reliability Engineer | watches the agreed signals for the agreed window | post-release confirmation or a reversal decision | Reversal executed on trigger, not on debate |
| 8 | Configuration Manager | updates the record of what now exists | updated configuration items | Record updated the same day the change lands |

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

> Apply the `production-change` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
