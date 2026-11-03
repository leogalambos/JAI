# Idea to production

## Trigger

A business need, opportunity or customer problem arrives with no agreed solution.

## Intended outcome

A change running in production with a measured benefit and a named owner.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Idea to production workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Business Relationship Manager</strong><p>captures the demand with a business outcome and an owner</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Product Manager</strong><p>decides whether and why to pursue it, against evidence</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Business Analyst</strong><p>elicits and specifies the need with testable acceptance criteria</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Solution Architect</strong><p>designs the solution end to end and records the decisions</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Security Architect</strong><p>designs the controls the solution needs</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Technical Lead</strong><p>breaks the work down and sets the technical approach</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Software Engineer</strong><p>implements with tests and telemetry</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Test Analyst</strong><p>verifies against the claims and reports residual risk</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Release Engineer</strong><p>assembles the release and proves the rollback</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Change Manager</strong><p>authorises the production change proportionate to its risk</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>GitOps and Continuous Delivery Engineer</strong><p>promotes the artefact and runs the progressive rollout</p></div></li>
<li data-step="12"><span class="ai-workflow-step-number" aria-hidden="true">12</span><div><strong>Site Reliability Engineer</strong><p>observes against the service objective and owns the run</p></div></li>
<li data-step="13"><span class="ai-workflow-step-number" aria-hidden="true">13</span><div><strong>Product Analyst</strong><p>measures whether the stated benefit arrived</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-idea-to-production.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Business Relationship Manager | captures the demand with a business outcome and an owner | demand record with outcome and owner | Demand with no named business outcome does not enter the pipeline |
| 2 | Product Manager | decides whether and why to pursue it, against evidence | roadmap item with problem statement and success measure | The customer problem and its evidence are stated |
| 3 | Business Analyst | elicits and specifies the need with testable acceptance criteria | requirements baseline with traceability | Every requirement is atomic, testable and traced to a source |
| 4 | Solution Architect | designs the solution end to end and records the decisions | solution architecture and ADRs | Reviewed by someone who will operate it; failure modes documented |
| 5 | Security Architect | designs the controls the solution needs | security requirements and threat model | Every control traces to a threat and a business risk |
| 6 | Technical Lead | breaks the work down and sets the technical approach | technical breakdown and readiness-checked items | Acceptance criteria and dependencies exist before start |
| 7 | Software Engineer | implements with tests and telemetry | reviewed, merged change with rollback path | Peer reviewed; no secrets in source; telemetry present |
| 8 | Test Analyst | verifies against the claims and reports residual risk | test evidence and residual risk statement | Exit criteria agreed before execution and met or waived |
| 9 | Release Engineer | assembles the release and proves the rollback | release manifest and tested rollback | Manifest states exactly which artefact versions ship where |
| 10 | Change Manager | authorises the production change proportionate to its risk | change authorisation | Risk class matched to approval path; emergency changes logged within the window |
| 11 | GitOps and Continuous Delivery Engineer | promotes the artefact and runs the progressive rollout | deployed change with health gate | Health gate and automatic rollback defined and exercised |
| 12 | Site Reliability Engineer | observes against the service objective and owns the run | service operating within SLO, or an error-budget decision | Error budget policy actually enforced |
| 13 | Product Analyst | measures whether the stated benefit arrived | benefit measurement against the success measure | Result reported with effect size, not just direction |

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

> Apply the `idea-to-production` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
