# New service onboarding

`workflow: new-service-onboarding`  ·  `steps: 12`  ·  `tool-tier: route`

**Trigger.** A new service or component needs to exist, be deployable and be operable.

**Outcome.** A service with codified infrastructure, a pipeline, environments, observability and an on-call owner.

Skipping any step here produces a service that works in development and is unsupportable in production. The last two steps are the ones most often deferred and most expensive to add later.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Cloud Architect](../../it-roles-architecture/references/cloud-architect.md) | sets the landing zone, resilience and residency constraints | target platform design | Resilience claims substantiated by a tested failure scenario |
| 2 | [Infrastructure as Code Engineer](../../it-roles-infrastructure-cloud-and-operations/references/infrastructure-as-code-engineer.md) | codifies the infrastructure and its guardrails | versioned modules, remote locked state, policy-as-code | Applies idempotently from clean; plan reviewed before apply |
| 3 | [Container Platform Engineer](../../it-roles-infrastructure-cloud-and-operations/references/container-platform-engineer.md) | establishes the image build chain and base image lineage | signed images with SBOM, immutable tags | Non-root, no build secrets, pinned digests |
| 4 | [CI/CD Platform Engineer](../../it-roles-software-development-and-engineering/references/ci-cd-platform-engineer.md) | wires the service onto the shared pipeline platform | pipeline with federated identity and signed provenance | No static cloud credentials in the CI system |
| 5 | [Secrets and Configuration Management Engineer](../../it-roles-security-operations-and-defensive-security/references/secrets-and-configuration-management-engineer.md) | issues the service's credentials with a lifecycle | dynamic short-lived credentials and a tested revocation path | Static credentials only as a time-bound exception |
| 6 | [Environment Manager](../../it-roles-infrastructure-cloud-and-operations/references/environment-manager.md) | provisions the non-production environments and their data | environments with owners, refresh cadence and masked data | No unmasked production personal data anywhere |
| 7 | [GitOps and Continuous Delivery Engineer](../../it-roles-software-development-and-engineering/references/gitops-and-continuous-delivery-engineer.md) | defines promotion and rollback across environments | desired-state repositories and promotion model | The same immutable artefact is promoted, never rebuilt |
| 8 | [Observability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/observability-engineer.md) | instruments the service against its objectives | dashboards and owned, actionable alerts | Every alert has an owner, an action and a runbook |
| 9 | [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | agrees the service objective and the error budget policy | SLOs and error budget policy | Exhausting the budget changes something, or the SLO is decorative |
| 10 | [Application Support Analyst](../../it-roles-service-management-and-support/references/application-support-analyst.md) | accepts the service into support with a runbook | runbook and known-error entries | A competent on-call engineer who has never seen it can follow it |
| 11 | [Configuration Manager](../../it-roles-service-management-and-support/references/configuration-manager.md) | records the service, its relationships and its owner | configuration items with verified relationships | Owner, lifecycle status and verified-by date present |
| 12 | [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | takes end-to-end ownership of value, cost and risk | service definition and service level agreement | Named business contact and an agreed SLA exist |

## Operating this chain

Each step is a role skill, operated by the agent matching its tool tier. Tiers used here: `author`, `execute`.

Read the linked reference file before acting as a step. Do not collapse two adjacent steps into one actor without checking section 13 of both: several of these adjacencies are deliberate separations, and `sod-reviewer` will tell you which.

A hand-off is complete only when the receiving step states the acceptance criteria it applied and confirms they are met. Unconfirmed hand-offs are where this chain actually breaks.
