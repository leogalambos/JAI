# New service onboarding

## Trigger

A new service or component needs to exist, be deployable and be operable.

## Intended outcome

An owned service with controlled configuration and change, proportionate validation, observability, support, recovery and service-level evidence.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Select the service context before choosing implementation mechanisms. The twelve stages describe a cloud-native reference chain; functional outcomes remain required where the implementation differs. An inapplicable mechanism is not a waiver of security, legal or acceptance obligations.

**Invariant outcomes:**

- Named end-to-end ownership, service boundary, dependencies and configuration identity.
- Applicable security, privacy, legal, access and credential-lifecycle requirements with evidence.
- Measurable service objectives, actionable monitoring, incident ownership and support readiness.
- Authorised change and release, recoverability or tested exit, and receiving acceptance of the exact service revision.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| cloud-native | Use landing zones, infrastructure as code, image provenance and GitOps where these are the adopted platform mechanisms. | Reviewed platform configuration, actual delivery/provenance records, operational validation and recovery evidence. |
| SaaS/COTS | Use supplier configuration, integration, identity, contractual service controls and a supported release/change route. Do not invent customer-owned container images or infrastructure pipelines. | Supplier assurance limits, tenant configuration, identity tests, service commitments, observed integration/support checks and exercised exit or recovery arrangements. |
| on-premises/existing-platform | Reuse approved platform configuration and deployment mechanisms. A new cloud landing zone or container platform is not required solely because a service is new. | Owned configuration baseline, compatible deployment records, capacity/failure validation, monitoring and tested restoration. |
| data/AI overlay | Combine the selected hosting variant with versioned data/model lineage, access purpose, validation, monitoring and retraining/change ownership. | Data/model versions, applicable-use and privacy assessment, evaluation limits, drift controls and rollback or withdrawal evidence. |
| critical/regulated overlay | Combine the selected hosting variant with applicable resilience, segregation, retention and competent regulatory assessment obligations. | Traceable obligation assessment, business impact/recovery evidence, independent validation and exact accountable acceptance. |

Record each substituted or inapplicable mechanism with context evidence, the invariant outcome it preserves, its alternative owner and the receiving review. Unknown applicability remains pending. Rework returns only affected material to its owner; failed readiness uses the existing stop/rollback or supplier exit route, never an inferred release approval.

**Entry information (selected once per actual context version):**

- Service outcome and accountable owner
- Platform/service sourcing context
- Data classification and service-level needs

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return missing readiness evidence to its service/platform/supplier owner; reuse valid platform evidence by version.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop service activation for an unowned critical dependency, missing mandatory control or absent applicable change authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept the supported service, or cancel onboarding with owned data/access and supplier exit disposition.

**Bounded paths and scope:**

SaaS and inherited-platform mechanisms replace owned IaC/image/pipeline records with configuration, dependency assurance and governed change evidence; overlays select a base mechanism explicitly.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| cloud-native | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| saas-cots | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| existing-platform | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| data-ai/cloud-native | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| data-ai/saas-cots | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| data-ai/existing-platform | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| critical-regulated/cloud-native | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| critical-regulated/saas-cots | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |
| critical-regulated/existing-platform | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | 12 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

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
| 2 | Infrastructure as Code Engineer | codifies the infrastructure and its guardrails | controlled service configuration baseline and verification evidence | Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails |
| 3 | Container Platform Engineer | establishes the image build chain and base image lineage | service dependency and supply-chain assurance evidence | Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance |
| 4 | CI/CD Platform Engineer | wires the service onto the shared pipeline platform | controlled service change path with identity and provenance evidence | Changes use governed identities, traceable inputs and an authorised observable change path |
| 5 | Secrets and Configuration Management Engineer | issues the service's credentials with a lifecycle | dynamic short-lived credentials and a tested revocation path | Static credentials only as a time-bound exception |
| 6 | Environment Manager | provisions the non-production environments and their data | environments with owners, refresh cadence and masked data | No unmasked production personal data anywhere |
| 7 | GitOps and Continuous Delivery Engineer | defines promotion and rollback across environments | service promotion or supplier-change model and recovery evidence | Change identity and sequence are traceable; recovery and escalation limits are explicit and validated |
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
