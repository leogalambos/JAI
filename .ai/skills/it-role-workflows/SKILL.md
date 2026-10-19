---
name: it-role-workflows
description: "Route enterprise IS/IT work across 24 end-to-end workflow chains, including idea-to-production, onboarding, change, incident, security, data/AI, benefits, operational readiness, migration/cutover, adoption, publication, EA repository governance, decommission, cyber recovery, resilience, demand/funding, sourcing, SIAM, enterprise release and regulatory assurance. Use when work spans roles or when the user needs sequencing, hand-offs, accountable roles, mandatory artefacts and blocking gates. Read the matching reference before answering."
allowed-tools: Read, Grep, Glob
---

# Enterprise workflows across roles

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-router`.

`workflows: 24`  ·  `tool-tier: route` (`Read, Grep, Glob`)  ·  `version: 1.0.0`

The role skills define single roles. This one defines the chains between them: the value streams, the hand-offs and the gate that must hold at each boundary. Routing and explanation only — it writes nothing and runs nothing.

## Chains

| Workflow | Steps | Trigger |
| --- | --- | --- |
| [Idea to production](references/idea-to-production.md) | 13 | A business need, opportunity or customer problem arrives with no agreed solution. |
| [New service onboarding](references/new-service-onboarding.md) | 12 | A new service or component needs to exist, be deployable and be operable. |
| [Production change](references/production-change.md) | 8 | A change must reach production: a feature, a fix, an infrastructure change or a configuration change. |
| [Incident to permanent fix](references/incident-to-problem.md) | 9 | A service degrades or fails. |
| [Vulnerability to remediation](references/vulnerability-to-remediation.md) | 8 | A vulnerability is reported, discovered by scanning, or published by a vendor. |
| [Inherited codebase takeover](references/codebase-takeover.md) | 8 | The organisation acquires, inherits or repatriates a system nobody present built. |
| [Access request to periodic review](references/access-request-to-review.md) | 6 | Someone needs access, changes role, or leaves. |
| [Data product delivery](references/data-product-delivery.md) | 8 | A business area needs a trusted dataset, metric or report. |
| [AI system from idea to approved production use](references/ai-system-approval.md) | 8 | A business area wants to deploy a model or an AI-assisted workflow. |
| [Supplier onboarding to exit](references/supplier-onboarding.md) | 7 | A technology supplier or SaaS product is being considered. |

| [Business case to realised benefits](references/business-case-to-benefits.md) | 7 | An investment has a proposed business case and needs measurable benefits governed through and beyond delivery. |
| [Design to operational readiness](references/design-to-operational-readiness.md) | 7 | A solution design is becoming build/release ready and must prove it can be operated safely before go-live. |
| [Migration and cutover](references/migration-and-cutover.md) | 8 | A project must move data/services from a current state to a target state through a controlled production cutover. |
| [Organisational change and adoption](references/organisational-change-and-adoption.md) | 6 | Technology or process change requires people to work differently for the intended outcome to materialise. |
| [Semantic artefact to enterprise publication](references/semantic-to-enterprise-publication.md) | 5 | A specialist artefact is substantively complete and requires enterprise-grade publication. |
| [Architecture model to repository governance](references/architecture-model-to-repository-governance.md) | 6 | A project/domain architecture needs to become a governed enterprise repository model and published view set. |
| [Service retirement and decommission](references/service-retirement-and-decommission.md) | 8 | A service, application, platform or technology component is approved for retirement, replacement or exit. |
| [Cyber incident / breach to recovery](references/cyber-incident-breach-to-recovery.md) | 13 | A suspected or confirmed cyber incident may affect systems, data, customers, regulatory obligations or business operations. |
| [Resilience validation](references/resilience-validation.md) | 10 | A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure. |
| [Demand to portfolio to funding](references/demand-to-portfolio-to-funding.md) | 9 | A new business/technology demand needs to be qualified, compared with alternatives and either rejected, redirected or committed into a funded portfolio. |
| [Source to contract to service](references/source-to-contract-to-service.md) | 10 | A capability may be sourced externally and must move from requirement/RFI/RFP through supplier selection and contract controls to implementation and accepted service. |
| [SIAM / multi-supplier service integration](references/siam-multi-supplier.md) | 8 | A service depends on multiple suppliers/teams and end-to-end accountability, OLAs, incidents, problems, changes or acceptance are fragmented across boundaries. |
| [Enterprise release orchestration](references/enterprise-release-orchestration.md) | 11 | Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process. |
| [Regulatory change to assurance](references/regulatory-change-to-assurance.md) | 10 | A new or changed law, regulation, supervisory expectation or contractual compliance obligation may affect IS/IT services, controls or architecture. |

## How to use this

1. Identify which chain the request sits in. If it sits in none, use `role-router` for a single role instead.
2. Identify the step. Requests usually arrive mid-chain, and the real problem is often the unfinished step before it.
3. Read that step's role reference and operate it with the agent named for its tier.
4. State explicitly what the previous step should have handed over. Missing inputs upstream are the most common reason a step cannot be completed, and naming the gap is more useful than working around it.

## What these chains are not

They are not a project plan and not a mandated sequence. Real work skips steps, loops back and runs steps in parallel. The value is in knowing which hand-off you are at and which gate you are about to skip — not in walking all thirteen steps of a value stream for a one-line change.

## Content acceptance at a handoff

When operating a registered handoff, the execute-tier operator loads its
exact `handoff_id` from `content/workflow-acceptance.json` and delegates the
acceptance check to the existing trusted host's `content_workflow.check`.
This routing skill remains read-only and does not execute the checker.
Require the canonical source, registered contract and replayable content QA,
then an independent authenticated receiver with a host-assigned receiving
role and evidence for the specific gate. Producer names, declared roles,
advisory findings and successful rendering cannot establish acceptance.

The shared content profile and checker apply identically to Claude and
Codex. A final named human authority step uses the existing signed JAI L0
acceptance; agents cannot replace it. Record pending acceptance explicitly
and preserve every existing security, evidence and governance block.
