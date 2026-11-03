# Inherited codebase takeover

## Trigger

The organisation acquires, inherits or repatriates a system nobody present built.

## Intended outcome

A reviewed, measured, supportable system with a sequenced improvement plan.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Inherited codebase takeover workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Codebase Reviewer</strong><p>audits against fixed criteria and reports prioritised findings</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Application Architect</strong><p>assesses structure and defines module boundaries</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Test Architect</strong><p>establishes how the system can be verified at all</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Software Modernisation Engineer</strong><p>captures existing behaviour before changing it</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Infrastructure as Code Engineer</strong><p>codifies whatever it currently runs on</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Observability Engineer</strong><p>makes its behaviour visible before changing it</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Technical Lead</strong><p>sequences the work so each slice ships independently</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>IT Service Owner</strong><p>accepts ownership with a cost and risk position</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-codebase-takeover.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Codebase Reviewer | audits against fixed criteria and reports prioritised findings | review report with located, measured findings | Criteria fixed before any code is read |
| 2 | Application Architect | assesses structure and defines module boundaries | boundary definition and refactoring roadmap | Boundaries enforced by automated checks, not prose |
| 3 | Test Architect | establishes how the system can be verified at all | test and environment strategy | Production-like data obtained lawfully |
| 4 | Software Modernisation Engineer | captures existing behaviour before changing it | characterisation test suite | Undocumented behaviour treated as a requirement until proven otherwise |
| 5 | Infrastructure as Code Engineer | codifies whatever it currently runs on | reproducible environment definition | Applies from clean; drift detectable |
| 6 | Observability Engineer | makes its behaviour visible before changing it | instrumentation and baseline signals | Baseline captured before the first change |
| 7 | Technical Lead | sequences the work so each slice ships independently | incremental delivery plan | No step requires a simultaneous big-bang cutover |
| 8 | IT Service Owner | accepts ownership with a cost and risk position | service definition, SLA, risk profile | A service with no owner is reported as ungoverned |

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

> Apply the `codebase-takeover` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
