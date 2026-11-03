# Architecture model to repository governance

## Trigger

A project/domain architecture needs to become a governed enterprise repository model and published view set.

## Intended outcome

Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Architecture model to repository governance workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Solution Architect</strong><p>finalises project model facts, decisions and project ownership boundaries</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Architecture Repository and Modelling Lead</strong><p>maps model facts into the canonical repository/metamodel and repository conventions</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Architecture Repository Engineer</strong><p>imports/updates the canonical repository, preserving IDs, lifecycle and provenance</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Model Consistency Reviewer</strong><p>checks references, orphans, cross-project ownership, lifecycle conflicts and view drift</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Enterprise Architect</strong><p>resolves enterprise/domain overlap, shared elements and portfolio dependencies</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Technical Design Authority Member</strong><p>applies architecture governance to material conformance/exception decisions</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-architecture-model-to-repository-governance.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Solution Architect | finalises project model facts, decisions and project ownership boundaries | project architecture model and source artefacts | Elements/relationships have stable identities and evidence basis |
| 2 | Architecture Repository and Modelling Lead | maps model facts into the canonical repository/metamodel and repository conventions | canonical project model | No model fact is silently reinterpreted to fit a tool |
| 3 | Architecture Repository Engineer | imports/updates the canonical repository, preserving IDs, lifecycle and provenance | repository revision plus interchange artefacts | Repository structural validation passes |
| 4 | Model Consistency Reviewer | checks references, orphans, cross-project ownership, lifecycle conflicts and view drift | consistency findings/gate | No blocking integrity error remains |
| 5 | Enterprise Architect | resolves enterprise/domain overlap, shared elements and portfolio dependencies | accepted enterprise model/repository decisions | Cross-project dependencies and reusable/reference elements have owners |
| 6 | Technical Design Authority Member | applies architecture governance to material conformance/exception decisions | approved/rejected repository release | Exceptions and residual risks have named authority and expiry/review |

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

> Apply the `architecture-model-to-repository-governance` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
