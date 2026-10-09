# Enterprise workflows

The release contains **24 named workflows**. A workflow connects roles, stages, gates and outcomes.

| Workflow | Title | Steps | Intended outcome |
| --- | --- | ---: | --- |
| `idea-to-production` | Idea to production | 13 | A change running in production with a measured benefit and a named owner. |
| `new-service-onboarding` | New service onboarding | 12 | A service with codified infrastructure, a pipeline, environments, observability and an on-call owner. |
| `production-change` | Production change | 8 | The change in production, recorded, with a proven way back. |
| `incident-to-problem` | Incident to permanent fix | 9 | Service restored, cause removed, and a control changed so the class of failure does not recur. |
| `vulnerability-to-remediation` | Vulnerability to remediation | 8 | The exposure removed or consciously accepted, with evidence either way. |
| `codebase-takeover` | Inherited codebase takeover | 8 | A reviewed, measured, supportable system with a sequenced improvement plan. |
| `access-request-to-review` | Access request to periodic review | 6 | Access that is appropriate, evidenced, and removed when no longer needed. |
| `data-product-delivery` | Data product delivery | 8 | A governed, documented, monitored data product with an owner. |
| `ai-system-approval` | AI system from idea to approved production use | 8 | An AI system classified, assessed, monitored, and accountable to a named human. |
| `supplier-onboarding` | Supplier onboarding to exit | 7 | A contracted supplier with assurance, monitored performance and a tested way out. |
| `business-case-to-benefits` | Business case to realised benefits | 7 | Benefits are baselined, owned, measured after go-live and used for continue/correct/close decisions. |
| `design-to-operational-readiness` | Design to operational readiness | 7 | The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service. |
| `migration-and-cutover` | Migration and cutover | 8 | Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects. |
| `organisational-change-and-adoption` | Organisational change and adoption | 6 | Affected cohorts are ready, adopt the new behaviour and produce evidence that supports the intended business benefit. |
| `semantic-to-enterprise-publication` | Semantic artefact to enterprise publication | 5 | A released audience-specific publication whose semantic content is traceable to the approved source and has passed semantic and publication gates. |
| `architecture-model-to-repository-governance` | Architecture model to repository governance | 6 | Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners. |
| `service-retirement-and-decommission` | Service retirement and decommission | 8 | The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured. |
| `cyber-incident-breach-to-recovery` | Cyber incident / breach to recovery | 13 | The incident is contained and eradicated, evidence is preserved, recovery is accepted by the business, notification decisions are traceable, and control remediation is closed or owned. |
| `resilience-validation` | Resilience validation | 10 | Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority. |
| `demand-to-portfolio-to-funding` | Demand to portfolio to funding | 10 | Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision. |
| `source-to-contract-to-service` | Source to contract to service | 10 | The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance. |
| `siam-multi-supplier` | SIAM / multi-supplier service integration | 8 | One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation. |
| `enterprise-release-orchestration` | Enterprise release orchestration | 12 | The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance. |
| `regulatory-change-to-assurance` | Regulatory change to assurance | 10 | Applicability and obligations are translated into traceable requirements/controls, architecture and remediation changes are implemented, evidence is independently assured, and closure is authorised. |

## Operator interaction versus workflow execution

**You:** describe the needed outcome, name the workflow if known, provide the repository or source material, state the accountable decision owner and ask for the current gate. This is a request **inside Claude or Codex CLI**, not a terminal command. For example, in either provider:

```text
Use the migration-and-cutover workflow for our ERP replacement. First identify the current stage, mandatory inputs, unresolved dependencies, evidence gaps, acceptance owner and go/no-go decision. Do not change production or approve a waiver without explicit authority.
```

**The provider agent:** uses the workflow and role registries to plan stages, allocate role-specific work, call permitted tools, preserve evidence and present gate outcomes. A workflow definition is a **governed method**, not proof that downstream tools, approvals or integrations have run. If a task is consequential, use the explicit `/layered` or `$workflow-layered` entry point; the current router does not force every natural-language workflow request through Fabric.

**Human accountable roles:** supply evidence and decide on approval, risk acceptance, production change, legal obligations and other reserved business actions. Provider instructions and workflow metadata cannot substitute for those decisions.

The 24 detailed pages in the [workflow library](../workflow-library/idea-to-production.md) specify steps, deliverables and gates. They describe **what the agent should coordinate** and **which human role remains accountable**; they are not 24 separate executable shell scripts.

## How to use workflows

Ask explicitly for the workflow you want, or describe the situation so the system can select one.

### Example

> Use the `migration-and-cutover` workflow for our programme. Show the next gate, the accountable role, mandatory inputs, missing evidence and the artefacts required before cutover approval.

## Why workflows are better than ad-hoc prompts

A role tells the system **who** is relevant. A workflow tells it **how** the work should move and **where** the governance gates are.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../roles/"><small>← Previous · Using the system</small><strong>Roles and disciplines</strong></a>
  <a class="ai-next" href="../deliverables/"><small>Next · Using the system →</small><strong>Working with deliverables</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
