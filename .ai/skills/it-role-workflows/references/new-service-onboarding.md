# New service onboarding

`workflow: new-service-onboarding`  ·  `steps: 12`  ·  `tool-tier: route`

**Trigger.** A new service or component needs to exist, be deployable and be operable.

**Outcome.** A service with codified infrastructure, a pipeline, environments, observability and an on-call owner.

This chain illustrates cloud-native implementation mechanisms. Select the service
context using the applicability guidance below before acting. Preserve its
operational and acceptance outcomes when a SaaS, COTS or existing platform uses
different mechanisms; absence of a container pipeline is not itself a failed
service outcome. Missing support readiness or accountable ownership remains a gap.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Cloud Architect](../../it-roles-architecture/references/cloud-architect.md) | sets the landing zone, resilience and residency constraints | target platform design | Resilience claims substantiated by a tested failure scenario |
| 2 | [Infrastructure as Code Engineer](../../it-roles-infrastructure-cloud-and-operations/references/infrastructure-as-code-engineer.md) | codifies the infrastructure and its guardrails | controlled service configuration baseline and verification evidence | Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails |
| 3 | [Container Platform Engineer](../../it-roles-infrastructure-cloud-and-operations/references/container-platform-engineer.md) | establishes the image build chain and base image lineage | service dependency and supply-chain assurance evidence | Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance |
| 4 | [CI/CD Platform Engineer](../../it-roles-software-development-and-engineering/references/ci-cd-platform-engineer.md) | wires the service onto the shared pipeline platform | controlled service change path with identity and provenance evidence | Changes use governed identities, traceable inputs and an authorised observable change path |
| 5 | [Secrets and Configuration Management Engineer](../../it-roles-security-operations-and-defensive-security/references/secrets-and-configuration-management-engineer.md) | issues the service's credentials with a lifecycle | dynamic short-lived credentials and a tested revocation path | Static credentials only as a time-bound exception |
| 6 | [Environment Manager](../../it-roles-infrastructure-cloud-and-operations/references/environment-manager.md) | provisions the non-production environments and their data | environments with owners, refresh cadence and masked data | No unmasked production personal data anywhere |
| 7 | [GitOps and Continuous Delivery Engineer](../../it-roles-software-development-and-engineering/references/gitops-and-continuous-delivery-engineer.md) | defines promotion and rollback across environments | service promotion or supplier-change model and recovery evidence | Change identity and sequence are traceable; recovery and escalation limits are explicit and validated |
| 8 | [Observability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/observability-engineer.md) | instruments the service against its objectives | dashboards and owned, actionable alerts | Every alert has an owner, an action and a runbook |
| 9 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | agrees the service objective and the error budget policy | SLOs and error budget policy | Exhausting the budget changes something, or the SLO is decorative |
| 10 | [Application Support Analyst](../../it-roles-service-management-and-support/references/application-support-analyst.md) | accepts the service into support with a runbook | runbook and known-error entries | A competent on-call engineer who has never seen it can follow it |
| 11 | [Configuration Manager](../../it-roles-service-management-and-support/references/configuration-manager.md) | records the service, its relationships and its owner | configuration items with verified relationships | Owner, lifecycle status and verified-by date present |
| 12 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | takes end-to-end ownership of value, cost and risk | service definition and service level agreement | Named business contact and an agreed SLA exist |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.

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
