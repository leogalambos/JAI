# New service onboarding

## Trigger

A new service or component needs to exist, be deployable and be operable.

## Intended outcome

A service with codified infrastructure, a pipeline, environments, observability and an on-call owner.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="New service onboarding workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Cloud Architect</strong><p>sets the landing zone, resilience and residency constraints</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Infrastructure as Code Engineer</strong><p>codifies the infrastructure and its guardrails</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Container Platform Engineer</strong><p>establishes the image build chain and base image lineage</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>CI/CD Platform Engineer</strong><p>wires the service onto the shared pipeline platform</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Secrets and Configuration Management Engineer</strong><p>issues the service&#x27;s credentials with a lifecycle</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Environment Manager</strong><p>provisions the non-production environments and their data</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>GitOps and Continuous Delivery Engineer</strong><p>defines promotion and rollback across environments</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Observability Engineer</strong><p>instruments the service against its objectives</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Site Reliability Engineer</strong><p>agrees the service objective and the error budget policy</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Application Support Analyst</strong><p>accepts the service into support with a runbook</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>Configuration Manager</strong><p>records the service, its relationships and its owner</p></div></li>
<li data-step="12"><span class="ai-workflow-step-number" aria-hidden="true">12</span><div><strong>IT Service Owner</strong><p>takes end-to-end ownership of value, cost and risk</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-new-service-onboarding.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Cloud Architect | sets the landing zone, resilience and residency constraints | target platform design | Resilience claims substantiated by a tested failure scenario |
| 2 | Infrastructure as Code Engineer | codifies the infrastructure and its guardrails | versioned modules, remote locked state, policy-as-code | Applies idempotently from clean; plan reviewed before apply |
| 3 | Container Platform Engineer | establishes the image build chain and base image lineage | signed images with SBOM, immutable tags | Non-root, no build secrets, pinned digests |
| 4 | CI/CD Platform Engineer | wires the service onto the shared pipeline platform | pipeline with federated identity and signed provenance | No static cloud credentials in the CI system |
| 5 | Secrets and Configuration Management Engineer | issues the service's credentials with a lifecycle | dynamic short-lived credentials and a tested revocation path | Static credentials only as a time-bound exception |
| 6 | Environment Manager | provisions the non-production environments and their data | environments with owners, refresh cadence and masked data | No unmasked production personal data anywhere |
| 7 | GitOps and Continuous Delivery Engineer | defines promotion and rollback across environments | desired-state repositories and promotion model | The same immutable artefact is promoted, never rebuilt |
| 8 | Observability Engineer | instruments the service against its objectives | dashboards and owned, actionable alerts | Every alert has an owner, an action and a runbook |
| 9 | Site Reliability Engineer | agrees the service objective and the error budget policy | SLOs and error budget policy | Exhausting the budget changes something, or the SLO is decorative |
| 10 | Application Support Analyst | accepts the service into support with a runbook | runbook and known-error entries | A competent on-call engineer who has never seen it can follow it |
| 11 | Configuration Manager | records the service, its relationships and its owner | configuration items with verified relationships | Owner, lifecycle status and verified-by date present |
| 12 | IT Service Owner | takes end-to-end ownership of value, cost and risk | service definition and service level agreement | Named business contact and an agreed SLA exist |

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

> Apply the `new-service-onboarding` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
