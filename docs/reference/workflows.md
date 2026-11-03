# Workflow catalogue

Choose a chain by its starting situation and required result. Every entry lists the concrete artefacts handed between its stages; its linked procedure specifies the accountable roles, activities and blocking gates. The artefacts are expected deliverables, not pre-existing approvals or automatic permission to release.

For invocation, see the [workflow selection guide](../using/workflows.md) and [usage modes](../using/usage-modes.md). For individual professions, see the [role catalogue](roles.md). Buyer-side sourcing is distinct from the supplier-side [commercial profile](../capabilities/commercial-delivery.md).

<!-- JAI:OUTPUT-CONTRACTS:START -->
| Workflow | Start when | Expected result |
| --- | --- | --- |
| [Idea to production](../workflow-library/idea-to-production.md) | A business need, opportunity or customer problem arrives with no agreed solution. | A change running in production with a measured benefit and a named owner. |
| [New service onboarding](../workflow-library/new-service-onboarding.md) | A new service or component needs to exist, be deployable and be operable. | A service with codified infrastructure, a pipeline, environments, observability and an on-call owner. |
| [Production change](../workflow-library/production-change.md) | A change must reach production: a feature, a fix, an infrastructure change or a configuration change. | The change in production, recorded, with a proven way back. |
| [Incident to permanent fix](../workflow-library/incident-to-problem.md) | A service degrades or fails. | Service restored, cause removed, and a control changed so the class of failure does not recur. |
| [Vulnerability to remediation](../workflow-library/vulnerability-to-remediation.md) | A vulnerability is reported, discovered by scanning, or published by a vendor. | The exposure removed or consciously accepted, with evidence either way. |
| [Inherited codebase takeover](../workflow-library/codebase-takeover.md) | The organisation acquires, inherits or repatriates a system nobody present built. | A reviewed, measured, supportable system with a sequenced improvement plan. |
| [Access request to periodic review](../workflow-library/access-request-to-review.md) | Someone needs access, changes role, or leaves. | Access that is appropriate, evidenced, and removed when no longer needed. |
| [Data product delivery](../workflow-library/data-product-delivery.md) | A business area needs a trusted dataset, metric or report. | A governed, documented, monitored data product with an owner. |
| [AI system from idea to approved production use](../workflow-library/ai-system-approval.md) | A business area wants to deploy a model or an AI-assisted workflow. | An AI system classified, assessed, monitored, and accountable to a named human. |
| [Supplier onboarding to exit](../workflow-library/supplier-onboarding.md) | A technology supplier or SaaS product is being considered. | A contracted supplier with assurance, monitored performance and a tested way out. |
| [Business case to realised benefits](../workflow-library/business-case-to-benefits.md) | An investment has a proposed business case and needs measurable benefits governed through and beyond delivery. | Benefits are baselined, owned, measured after go-live and used for continue/correct/close decisions. |
| [Design to operational readiness](../workflow-library/design-to-operational-readiness.md) | A solution design is becoming build/release ready and must prove it can be operated safely before go-live. | The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service. |
| [Migration and cutover](../workflow-library/migration-and-cutover.md) | A project must move data/services from a current state to a target state through a controlled production cutover. | Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects. |
| [Organisational change and adoption](../workflow-library/organisational-change-and-adoption.md) | Technology or process change requires people to work differently for the intended outcome to materialise. | Affected cohorts are ready, adopt the new behaviour and produce evidence that supports the intended business benefit. |
| [Semantic artefact to enterprise publication](../workflow-library/semantic-to-enterprise-publication.md) | A specialist artefact is substantively complete and requires enterprise-grade publication. | A released audience-specific publication whose semantic content is traceable to the approved source and has passed semantic and publication gates. |
| [Architecture model to repository governance](../workflow-library/architecture-model-to-repository-governance.md) | A project/domain architecture needs to become a governed enterprise repository model and published view set. | Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners. |
| [Service retirement and decommission](../workflow-library/service-retirement-and-decommission.md) | A service, application, platform or technology component is approved for retirement, replacement or exit. | The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured. |
| [Cyber incident / breach to recovery](../workflow-library/cyber-incident-breach-to-recovery.md) | A suspected or confirmed cyber incident may affect systems, data, customers, regulatory obligations or business operations. | The incident is contained and eradicated, evidence is preserved, recovery is accepted by the business, notification decisions are traceable, and control remediation is closed or owned. |
| [Resilience validation](../workflow-library/resilience-validation.md) | A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure. | Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority. |
| [Demand to portfolio to funding](../workflow-library/demand-to-portfolio-to-funding.md) | A new business/technology demand needs to be qualified, compared with alternatives and either rejected, redirected or committed into a funded portfolio. | Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision. |
| [Source to contract to service](../workflow-library/source-to-contract-to-service.md) | A capability may be sourced externally and must move from requirement/RFI/RFP through supplier selection and contract controls to implementation and accepted service. | The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance. |
| [SIAM / multi-supplier service integration](../workflow-library/siam-multi-supplier.md) | A service depends on multiple suppliers/teams and end-to-end accountability, OLAs, incidents, problems, changes or acceptance are fragmented across boundaries. | One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation. |
| [Enterprise release orchestration](../workflow-library/enterprise-release-orchestration.md) | Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process. | The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance. |
| [Regulatory change to assurance](../workflow-library/regulatory-change-to-assurance.md) | A new or changed law, regulation, supervisory expectation or contractual compliance obligation may affect IS/IT services, controls or architecture. | Applicability and obligations are translated into traceable requirements/controls, architecture and remediation changes are implemented, evidence is independently assured, and closure is authorised. |

## Idea to production

**Workflow key:** `idea-to-production`.

**Start when:** A business need, opportunity or customer problem arrives with no agreed solution.

**Expected result:** A change running in production with a measured benefit and a named owner.

**Concrete stage outputs and receiving conditions:**

1. **Business Relationship Manager:** demand record with outcome and owner.
   **Receiving condition:** Demand with no named business outcome does not enter the pipeline
   **Output specifications:** [`business-relationship-manager:2`](output-contracts/role-business-relationship-manager.md#output-business-relationship-manager-2)
2. **Product Manager:** roadmap item with problem statement and success measure.
   **Receiving condition:** The customer problem and its evidence are stated
   **Output specifications:** [`product-manager:1`](output-contracts/role-product-manager.md#output-product-manager-1); [`product-manager:3`](output-contracts/role-product-manager.md#output-product-manager-3)
3. **Business Analyst:** requirements baseline with traceability.
   **Receiving condition:** Every requirement is atomic, testable and traced to a source
   **Output specifications:** [`business-analyst:1`](output-contracts/role-business-analyst.md#output-business-analyst-1)
4. **Solution Architect:** solution architecture and ADRs.
   **Receiving condition:** Reviewed by someone who will operate it; failure modes documented
   **Output specifications:** [`solution-architect:1`](output-contracts/role-solution-architect.md#output-solution-architect-1); [`solution-architect:4`](output-contracts/role-solution-architect.md#output-solution-architect-4)
5. **Security Architect:** security requirements and threat model.
   **Receiving condition:** Every control traces to a threat and a business risk
   **Output specifications:** [`security-architect:2`](output-contracts/role-security-architect.md#output-security-architect-2); [`security-architect:4`](output-contracts/role-security-architect.md#output-security-architect-4)
6. **Technical Lead:** technical breakdown and readiness-checked items.
   **Receiving condition:** Acceptance criteria and dependencies exist before start
   **Output specifications:** [`technical-lead:4`](output-contracts/role-technical-lead.md#output-technical-lead-4)
7. **Software Engineer:** reviewed, merged change with rollback path.
   **Receiving condition:** Peer reviewed; no secrets in source; telemetry present
   **Output specifications:** [`software-engineer:1`](output-contracts/role-software-engineer.md#output-software-engineer-1); [`software-engineer:2`](output-contracts/role-software-engineer.md#output-software-engineer-2); [`software-engineer:4`](output-contracts/role-software-engineer.md#output-software-engineer-4)
8. **Test Analyst:** test evidence and residual risk statement.
   **Receiving condition:** Exit criteria agreed before execution and met or waived
   **Output specifications:** [`test-analyst:2`](output-contracts/role-test-analyst.md#output-test-analyst-2); [`test-analyst:4`](output-contracts/role-test-analyst.md#output-test-analyst-4)
9. **Release Engineer:** release manifest and tested rollback.
   **Receiving condition:** Manifest states exactly which artefact versions ship where
   **Output specifications:** [`release-engineer:2`](output-contracts/role-release-engineer.md#output-release-engineer-2); [`release-engineer:4`](output-contracts/role-release-engineer.md#output-release-engineer-4)
10. **Change Manager:** change authorisation.
   **Receiving condition:** Risk class matched to approval path; emergency changes logged within the window
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1)
11. **GitOps and Continuous Delivery Engineer:** deployed change with health gate.
   **Receiving condition:** Health gate and automatic rollback defined and exercised
   **Output specifications:** [`gitops-and-continuous-delivery-engineer:3`](output-contracts/role-gitops-and-continuous-delivery-engineer.md#output-gitops-and-continuous-delivery-engineer-3); [`gitops-and-continuous-delivery-engineer:4`](output-contracts/role-gitops-and-continuous-delivery-engineer.md#output-gitops-and-continuous-delivery-engineer-4)
12. **Site Reliability Engineer:** service operating within SLO, or an error-budget decision.
   **Receiving condition:** Error budget policy actually enforced
   **Output specifications:** [`site-reliability-engineer:1`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-1)
13. **Product Analyst:** benefit measurement against the success measure.
   **Receiving condition:** Result reported with effect size, not just direction
   **Output specifications:** [`product-analyst:1`](output-contracts/role-product-analyst.md#output-product-analyst-1); [`product-analyst:2`](output-contracts/role-product-analyst.md#output-product-analyst-2)

[Roles, activities and acceptance gates for this chain](../workflow-library/idea-to-production.md#workflow-steps-and-gates).

## New service onboarding

**Workflow key:** `new-service-onboarding`.

**Start when:** A new service or component needs to exist, be deployable and be operable.

**Expected result:** A service with codified infrastructure, a pipeline, environments, observability and an on-call owner.

**Concrete stage outputs and receiving conditions:**

1. **Cloud Architect:** target platform design.
   **Receiving condition:** Resilience claims substantiated by a tested failure scenario
   **Output specifications:** [`cloud-architect:1`](output-contracts/role-cloud-architect.md#output-cloud-architect-1)
2. **Infrastructure as Code Engineer:** versioned modules, remote locked state, policy-as-code.
   **Receiving condition:** Applies idempotently from clean; plan reviewed before apply
   **Output specifications:** [`infrastructure-as-code-engineer:1`](output-contracts/role-infrastructure-as-code-engineer.md#output-infrastructure-as-code-engineer-1); [`infrastructure-as-code-engineer:3`](output-contracts/role-infrastructure-as-code-engineer.md#output-infrastructure-as-code-engineer-3)
3. **Container Platform Engineer:** signed images with SBOM, immutable tags.
   **Receiving condition:** Non-root, no build secrets, pinned digests
   **Output specifications:** [`container-platform-engineer:1`](output-contracts/role-container-platform-engineer.md#output-container-platform-engineer-1); [`container-platform-engineer:4`](output-contracts/role-container-platform-engineer.md#output-container-platform-engineer-4)
4. **CI/CD Platform Engineer:** pipeline with federated identity and signed provenance.
   **Receiving condition:** No static cloud credentials in the CI system
   **Output specifications:** [`ci-cd-platform-engineer:1`](output-contracts/role-ci-cd-platform-engineer.md#output-ci-cd-platform-engineer-1); [`ci-cd-platform-engineer:3`](output-contracts/role-ci-cd-platform-engineer.md#output-ci-cd-platform-engineer-3); [`ci-cd-platform-engineer:4`](output-contracts/role-ci-cd-platform-engineer.md#output-ci-cd-platform-engineer-4)
5. **Secrets and Configuration Management Engineer:** dynamic short-lived credentials and a tested revocation path.
   **Receiving condition:** Static credentials only as a time-bound exception
   **Output specifications:** [`secrets-and-configuration-management-engineer:2`](output-contracts/role-secrets-and-configuration-management-engineer.md#output-secrets-and-configuration-management-engineer-2); [`secrets-and-configuration-management-engineer:3`](output-contracts/role-secrets-and-configuration-management-engineer.md#output-secrets-and-configuration-management-engineer-3)
6. **Environment Manager:** environments with owners, refresh cadence and masked data.
   **Receiving condition:** No unmasked production personal data anywhere
   **Output specifications:** [`environment-manager:1`](output-contracts/role-environment-manager.md#output-environment-manager-1); [`environment-manager:2`](output-contracts/role-environment-manager.md#output-environment-manager-2); [`environment-manager:3`](output-contracts/role-environment-manager.md#output-environment-manager-3)
7. **GitOps and Continuous Delivery Engineer:** desired-state repositories and promotion model.
   **Receiving condition:** The same immutable artefact is promoted, never rebuilt
   **Output specifications:** [`gitops-and-continuous-delivery-engineer:1`](output-contracts/role-gitops-and-continuous-delivery-engineer.md#output-gitops-and-continuous-delivery-engineer-1)
8. **Observability Engineer:** dashboards and owned, actionable alerts.
   **Receiving condition:** Every alert has an owner, an action and a runbook
   **Output specifications:** [`observability-engineer:2`](output-contracts/role-observability-engineer.md#output-observability-engineer-2); [`observability-engineer:3`](output-contracts/role-observability-engineer.md#output-observability-engineer-3)
9. **Site Reliability Engineer:** SLOs and error budget policy.
   **Receiving condition:** Exhausting the budget changes something, or the SLO is decorative
   **Output specifications:** [`site-reliability-engineer:1`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-1)
10. **Application Support Analyst:** runbook and known-error entries.
   **Receiving condition:** A competent on-call engineer who has never seen it can follow it
   **Output specifications:** [`application-support-analyst:2`](output-contracts/role-application-support-analyst.md#output-application-support-analyst-2)
11. **Configuration Manager:** configuration items with verified relationships.
   **Receiving condition:** Owner, lifecycle status and verified-by date present
   **Output specifications:** [`configuration-manager:3`](output-contracts/role-configuration-manager.md#output-configuration-manager-3)
12. **IT Service Owner:** service definition and service level agreement.
   **Receiving condition:** Named business contact and an agreed SLA exist
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1)

[Roles, activities and acceptance gates for this chain](../workflow-library/new-service-onboarding.md#workflow-steps-and-gates).

## Production change

**Workflow key:** `production-change`.

**Start when:** A change must reach production: a feature, a fix, an infrastructure change or a configuration change.

**Expected result:** The change in production, recorded, with a proven way back.

**Concrete stage outputs and receiving conditions:**

1. **Software Engineer:** reviewed change and rollback plan.
   **Receiving condition:** Small enough to review in one pass
   **Output specifications:** [`software-engineer:1`](output-contracts/role-software-engineer.md#output-software-engineer-1); [`software-engineer:4`](output-contracts/role-software-engineer.md#output-software-engineer-4)
2. **Infrastructure as Code Engineer:** reviewed plan; destructive operations flagged.
   **Receiving condition:** The applied plan is the reviewed plan
   **Output specifications:** [`infrastructure-as-code-engineer:1`](output-contracts/role-infrastructure-as-code-engineer.md#output-infrastructure-as-code-engineer-1); [`infrastructure-as-code-engineer:3`](output-contracts/role-infrastructure-as-code-engineer.md#output-infrastructure-as-code-engineer-3)
3. **Test Analyst:** test evidence with coverage and residual risk.
   **Receiving condition:** Residual risk accepted by a named person
   **Output specifications:** [`test-analyst:2`](output-contracts/role-test-analyst.md#output-test-analyst-2); [`test-analyst:4`](output-contracts/role-test-analyst.md#output-test-analyst-4)
4. **Release Engineer:** release manifest with signed provenance.
   **Receiving condition:** Every artefact traceable to a source commit
   **Output specifications:** [`release-engineer:2`](output-contracts/role-release-engineer.md#output-release-engineer-2)
5. **Change Manager:** change record and schedule slot.
   **Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1); [`change-manager:2`](output-contracts/role-change-manager.md#output-change-manager-2)
6. **GitOps and Continuous Delivery Engineer:** rollout with automatic reversal armed.
   **Receiving condition:** Rollback exercised, not merely documented
   **Output specifications:** [`gitops-and-continuous-delivery-engineer:3`](output-contracts/role-gitops-and-continuous-delivery-engineer.md#output-gitops-and-continuous-delivery-engineer-3); [`gitops-and-continuous-delivery-engineer:4`](output-contracts/role-gitops-and-continuous-delivery-engineer.md#output-gitops-and-continuous-delivery-engineer-4)
7. **Site Reliability Engineer:** post-release confirmation or a reversal decision.
   **Receiving condition:** Reversal executed on trigger, not on debate
   **Output specifications:** [`site-reliability-engineer:1`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-1); [`site-reliability-engineer:3`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-3)
8. **Configuration Manager:** updated configuration items.
   **Receiving condition:** Record updated the same day the change lands
   **Output specifications:** [`configuration-manager:1`](output-contracts/role-configuration-manager.md#output-configuration-manager-1); [`configuration-manager:3`](output-contracts/role-configuration-manager.md#output-configuration-manager-3)

[Roles, activities and acceptance gates for this chain](../workflow-library/production-change.md#workflow-steps-and-gates).

## Incident to permanent fix

**Workflow key:** `incident-to-problem`.

**Start when:** A service degrades or fails.

**Expected result:** Service restored, cause removed, and a control changed so the class of failure does not recur.

**Concrete stage outputs and receiving conditions:**

1. **Service Desk Analyst:** incident record with impact and urgency.
   **Receiving condition:** Symptom-only records are returned for clarification
   **Output specifications:** [`service-desk-analyst:1`](output-contracts/role-service-desk-analyst.md#output-service-desk-analyst-1)
2. **Incident Manager:** priority, working hypothesis, comms cadence.
   **Receiving condition:** Priority from business impact, not technical severity
   **Output specifications:** [`incident-manager:1`](output-contracts/role-incident-manager.md#output-incident-manager-1); [`incident-manager:2`](output-contracts/role-incident-manager.md#output-incident-manager-2); [`incident-manager:4`](output-contracts/role-incident-manager.md#output-incident-manager-4)
3. **Site Reliability Engineer:** service restored; evidence preserved.
   **Receiving condition:** Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised
   **Output specifications:** [`site-reliability-engineer:3`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-3)
4. **Major Incident Manager:** command log, stakeholder comms, notification assessment.
   **Receiving condition:** Comms on a fixed clock; regulatory clocks assessed
   **Output specifications:** [`major-incident-manager:1`](output-contracts/role-major-incident-manager.md#output-major-incident-manager-1); [`major-incident-manager:2`](output-contracts/role-major-incident-manager.md#output-major-incident-manager-2); [`major-incident-manager:3`](output-contracts/role-major-incident-manager.md#output-major-incident-manager-3)
5. **Problem Manager:** problem record with root cause and known error.
   **Receiving condition:** "Human error" alone rejected as a root cause
   **Output specifications:** [`problem-manager:1`](output-contracts/role-problem-manager.md#output-problem-manager-1); [`problem-manager:2`](output-contracts/role-problem-manager.md#output-problem-manager-2)
6. **Technical Lead:** fix approach and effort.
   **Receiving condition:** The fix addresses the cause, not the latest symptom
   **Output specifications:** [`technical-lead:1`](output-contracts/role-technical-lead.md#output-technical-lead-1); [`technical-lead:4`](output-contracts/role-technical-lead.md#output-technical-lead-4)
7. **Software Engineer:** versioned candidate, pre-production test evidence and rollback rehearsal.
   **Receiving condition:** Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision
   **Output specifications:** [`software-engineer:1`](output-contracts/role-software-engineer.md#output-software-engineer-1); [`software-engineer:2`](output-contracts/role-software-engineer.md#output-software-engineer-2); [`software-engineer:4`](output-contracts/role-software-engineer.md#output-software-engineer-4)
8. **Change Manager:** change authorisation.
   **Receiving condition:** Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1)
9. **Software Engineer:** versioned fix, execution evidence and rollback observations.
   **Receiving condition:** Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria
   **Output specifications:** [`software-engineer:1`](output-contracts/role-software-engineer.md#output-software-engineer-1); [`software-engineer:4`](output-contracts/role-software-engineer.md#output-software-engineer-4)
10. **Test Analyst:** independent regression, service and residual-defect evidence.
   **Receiving condition:** Actual execution and independent validation evidence are required before closure; failed criteria remain blocking
   **Output specifications:** [`test-analyst:1`](output-contracts/role-test-analyst.md#output-test-analyst-1); [`test-analyst:2`](output-contracts/role-test-analyst.md#output-test-analyst-2)
11. **Detection Engineer:** new or tuned alert with a runbook.
   **Receiving condition:** Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure
   **Output specifications:** [`detection-engineer:1`](output-contracts/role-detection-engineer.md#output-detection-engineer-1); [`detection-engineer:2`](output-contracts/role-detection-engineer.md#output-detection-engineer-2)
12. **Continual Improvement Manager:** measured recurrence rate.
   **Receiving condition:** Baseline measured before the change, not asserted after
   **Output specifications:** [`continual-improvement-manager:2`](output-contracts/role-continual-improvement-manager.md#output-continual-improvement-manager-2)

[Roles, activities and acceptance gates for this chain](../workflow-library/incident-to-problem.md#workflow-steps-and-gates).

## Vulnerability to remediation

**Workflow key:** `vulnerability-to-remediation`.

**Start when:** A vulnerability is reported, discovered by scanning, or published by a vendor.

**Expected result:** The exposure removed or consciously accepted, with evidence either way.

**Concrete stage outputs and receiving conditions:**

1. **Vulnerability Management Analyst:** prioritised findings with owners and targets.
   **Receiving condition:** Prioritised on exploitability and exposure, not severity score alone
   **Output specifications:** [`vulnerability-management-analyst:1`](output-contracts/role-vulnerability-management-analyst.md#output-vulnerability-management-analyst-1); [`vulnerability-management-analyst:2`](output-contracts/role-vulnerability-management-analyst.md#output-vulnerability-management-analyst-2)
2. **Threat Intelligence Analyst:** exploitability and targeting assessment.
   **Receiving condition:** Source reliability and analytic confidence stated
   **Output specifications:** [`threat-intelligence-analyst:2`](output-contracts/role-threat-intelligence-analyst.md#output-threat-intelligence-analyst-2)
3. **Application Security Engineer:** remediation guidance per finding.
   **Receiving condition:** Scanner noise tuned rather than forwarded
   **Output specifications:** [`application-security-engineer:3`](output-contracts/role-application-security-engineer.md#output-application-security-engineer-3)
4. **Container Platform Engineer:** candidate images and validation evidence.
   **Receiving condition:** Base image owner and cadence identified; candidate preparation does not deploy to production
   **Output specifications:** [`container-platform-engineer:1`](output-contracts/role-container-platform-engineer.md#output-container-platform-engineer-1); [`container-platform-engineer:4`](output-contracts/role-container-platform-engineer.md#output-container-platform-engineer-4)
5. **Change Manager:** change authorisation, approved window and rollback conditions.
   **Receiving condition:** Named change authority approves before any production change; the authorised emergency route applies to urgent changes; risk of patching weighed against risk of waiting
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1)
6. **Software Engineer:** patched system or dependency with execution and verification evidence.
   **Receiving condition:** Current change authorisation and rollback conditions confirmed before deployment; fix verified, not assumed from a version number
   **Output specifications:** [`software-engineer:1`](output-contracts/role-software-engineer.md#output-software-engineer-1)
7. **Penetration Tester (Network and Infrastructure):** retest verification.
   **Receiving condition:** Only within a current signed authorisation
   **Output specifications:** [`penetration-tester-network-and-infrastructure:4`](output-contracts/role-penetration-tester-network-and-infrastructure.md#output-penetration-tester-network-and-infrastructure-4)
8. **IT Risk Manager:** time-bound risk acceptance with a compensating control.
   **Receiving condition:** Accepted by the owner carrying the risk
   **Output specifications:** [`it-risk-manager:4`](output-contracts/role-it-risk-manager.md#output-it-risk-manager-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/vulnerability-to-remediation.md#workflow-steps-and-gates).

## Inherited codebase takeover

**Workflow key:** `codebase-takeover`.

**Start when:** The organisation acquires, inherits or repatriates a system nobody present built.

**Expected result:** A reviewed, measured, supportable system with a sequenced improvement plan.

**Concrete stage outputs and receiving conditions:**

1. **Codebase Reviewer:** review report with located, measured findings.
   **Receiving condition:** Criteria fixed before any code is read
   **Output specifications:** [`codebase-reviewer:1`](output-contracts/role-codebase-reviewer.md#output-codebase-reviewer-1)
2. **Application Architect:** boundary definition and refactoring roadmap.
   **Receiving condition:** Boundaries enforced by automated checks, not prose
   **Output specifications:** [`application-architect:1`](output-contracts/role-application-architect.md#output-application-architect-1); [`application-architect:3`](output-contracts/role-application-architect.md#output-application-architect-3)
3. **Test Architect:** test and environment strategy.
   **Receiving condition:** Production-like data obtained lawfully
   **Output specifications:** [`test-architect:1`](output-contracts/role-test-architect.md#output-test-architect-1); [`test-architect:2`](output-contracts/role-test-architect.md#output-test-architect-2)
4. **Software Modernisation Engineer:** characterisation test suite.
   **Receiving condition:** Undocumented behaviour treated as a requirement until proven otherwise
   **Output specifications:** [`software-modernisation-engineer:2`](output-contracts/role-software-modernisation-engineer.md#output-software-modernisation-engineer-2)
5. **Infrastructure as Code Engineer:** reproducible environment definition.
   **Receiving condition:** Applies from clean; drift detectable
   **Output specifications:** [`infrastructure-as-code-engineer:1`](output-contracts/role-infrastructure-as-code-engineer.md#output-infrastructure-as-code-engineer-1)
6. **Observability Engineer:** instrumentation and baseline signals.
   **Receiving condition:** Baseline captured before the first change
   **Output specifications:** [`observability-engineer:1`](output-contracts/role-observability-engineer.md#output-observability-engineer-1); [`observability-engineer:2`](output-contracts/role-observability-engineer.md#output-observability-engineer-2)
7. **Technical Lead:** incremental delivery plan.
   **Receiving condition:** No step requires a simultaneous big-bang cutover
   **Output specifications:** [`technical-lead:4`](output-contracts/role-technical-lead.md#output-technical-lead-4)
8. **IT Service Owner:** service definition, SLA, risk profile.
   **Receiving condition:** A service with no owner is reported as ungoverned
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1); [`it-service-owner:4`](output-contracts/role-it-service-owner.md#output-it-service-owner-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/codebase-takeover.md#workflow-steps-and-gates).

## Access request to periodic review

**Workflow key:** `access-request-to-review`.

**Start when:** Someone needs access, changes role, or leaves.

**Expected result:** Access that is appropriate, evidenced, and removed when no longer needed.

**Concrete stage outputs and receiving conditions:**

1. **Service Desk Analyst:** request with entitlement and approval path.
   **Receiving condition:** Entitlement and approval path defined for the request type
   **Output specifications:** [`service-desk-analyst:1`](output-contracts/role-service-desk-analyst.md#output-service-desk-analyst-1)
2. **Data Owner:** access decision recorded with its purpose.
   **Receiving condition:** Purpose-free access grants refused
   **Output specifications:** [`data-owner:2`](output-contracts/role-data-owner.md#output-data-owner-2)
3. **Identity and Access Management Engineer:** provisioned access, automated where integrated.
   **Receiving condition:** Leaver revocation evidenced automatically, not attested
   **Output specifications:** [`identity-and-access-management-engineer:2`](output-contracts/role-identity-and-access-management-engineer.md#output-identity-and-access-management-engineer-2); [`identity-and-access-management-engineer:3`](output-contracts/role-identity-and-access-management-engineer.md#output-identity-and-access-management-engineer-3)
4. **Privileged Access Management Administrator:** vaulted account with session monitoring.
   **Receiving condition:** Break-glass tested on a schedule; every use reviewed
   **Output specifications:** [`privileged-access-management-administrator:1`](output-contracts/role-privileged-access-management-administrator.md#output-privileged-access-management-administrator-1); [`privileged-access-management-administrator:2`](output-contracts/role-privileged-access-management-administrator.md#output-privileged-access-management-administrator-2)
5. **Identity Governance Specialist:** certification campaign results.
   **Receiving condition:** Reviewers have actual knowledge of the access
   **Output specifications:** [`identity-governance-specialist:1`](output-contracts/role-identity-governance-specialist.md#output-identity-governance-specialist-1)
6. **Internal IT Auditor:** audit finding or assurance.
   **Receiving condition:** Auditor never operated the control
   **Output specifications:** [`internal-it-auditor:3`](output-contracts/role-internal-it-auditor.md#output-internal-it-auditor-3)

[Roles, activities and acceptance gates for this chain](../workflow-library/access-request-to-review.md#workflow-steps-and-gates).

## Data product delivery

**Workflow key:** `data-product-delivery`.

**Start when:** A business area needs a trusted dataset, metric or report.

**Expected result:** A governed, documented, monitored data product with an owner.

**Concrete stage outputs and receiving conditions:**

1. **Data Governance Lead:** governed element definitions.
   **Receiving condition:** Owner, steward, definition and quality tolerance exist
   **Output specifications:** [`data-governance-lead:1`](output-contracts/role-data-governance-lead.md#output-data-governance-lead-1); [`data-governance-lead:2`](output-contracts/role-data-governance-lead.md#output-data-governance-lead-2)
2. **Data Protection Officer:** privacy position and DPIA where required.
   **Receiving condition:** DPIA completed before processing begins
   **Output specifications:** [`data-protection-officer:2`](output-contracts/role-data-protection-officer.md#output-data-protection-officer-2)
3. **Data Architect:** data model and flow design.
   **Receiving condition:** Every flow crossing a trust or jurisdiction boundary has a control
   **Output specifications:** [`data-architect:1`](output-contracts/role-data-architect.md#output-data-architect-1); [`data-architect:3`](output-contracts/role-data-architect.md#output-data-architect-3)
4. **Data Engineer:** pipelines with freshness and completeness checks.
   **Receiving condition:** Checks fail loudly rather than degrading silently
   **Output specifications:** [`data-engineer:1`](output-contracts/role-data-engineer.md#output-data-engineer-1); [`data-engineer:3`](output-contracts/role-data-engineer.md#output-data-engineer-3)
5. **Analytics Engineer:** tested, documented models with lineage.
   **Receiving condition:** Uniqueness, referential integrity and freshness tested
   **Output specifications:** [`analytics-engineer:1`](output-contracts/role-analytics-engineer.md#output-analytics-engineer-1); [`analytics-engineer:3`](output-contracts/role-analytics-engineer.md#output-analytics-engineer-3)
6. **Data Quality Analyst:** quality measurement against tolerance.
   **Receiving condition:** No bare percentage without a fitness-for-purpose statement
   **Output specifications:** [`data-quality-analyst:1`](output-contracts/role-data-quality-analyst.md#output-data-quality-analyst-1)
7. **Business Intelligence Analyst:** dashboards on a single agreed metric definition.
   **Receiving condition:** Two dashboards may not disagree silently
   **Output specifications:** [`business-intelligence-analyst:1`](output-contracts/role-business-intelligence-analyst.md#output-business-intelligence-analyst-1); [`business-intelligence-analyst:2`](output-contracts/role-business-intelligence-analyst.md#output-business-intelligence-analyst-2)
8. **Data Steward:** stewardship decisions and issue log.
   **Receiving condition:** Competing definitions escalated, not averaged
   **Output specifications:** [`data-steward:3`](output-contracts/role-data-steward.md#output-data-steward-3); [`data-steward:4`](output-contracts/role-data-steward.md#output-data-steward-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/data-product-delivery.md#workflow-steps-and-gates).

## AI system from idea to approved production use

**Workflow key:** `ai-system-approval`.

**Start when:** A business area wants to deploy a model or an AI-assisted workflow.

**Expected result:** An AI system classified, assessed, monitored, and accountable to a named human.

**Concrete stage outputs and receiving conditions:**

1. **AI Governance Officer:** risk classification and inventory entry.
   **Receiving condition:** No production AI without a classification and an accountable human
   **Output specifications:** [`ai-governance-officer:1`](output-contracts/role-ai-governance-officer.md#output-ai-governance-officer-1)
2. **Data Protection Officer:** privacy and fairness position.
   **Receiving condition:** Impact assessment before processing, not retrospectively
   **Output specifications:** [`data-protection-officer:2`](output-contracts/role-data-protection-officer.md#output-data-protection-officer-2)
3. **Data Scientist:** candidate model with held-out performance and stated limits.
   **Receiving condition:** Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated
   **Output specifications:** [`data-scientist:1`](output-contracts/role-data-scientist.md#output-data-scientist-1); [`data-scientist:2`](output-contracts/role-data-scientist.md#output-data-scientist-2)
4. **AI and ML Architect:** serving and monitoring architecture.
   **Receiving condition:** Drift, degradation and harmful-output monitoring designed in
   **Output specifications:** [`ai-and-ml-architect:1`](output-contracts/role-ai-and-ml-architect.md#output-ai-and-ml-architect-1); [`ai-and-ml-architect:4`](output-contracts/role-ai-and-ml-architect.md#output-ai-and-ml-architect-4)
5. **AI Safety and Model Red Team Specialist:** adversarial findings with severity and owners.
   **Receiving condition:** Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation
   **Output specifications:** [`ai-safety-and-model-red-team-specialist:1`](output-contracts/role-ai-safety-and-model-red-team-specialist.md#output-ai-safety-and-model-red-team-specialist-1); [`ai-safety-and-model-red-team-specialist:2`](output-contracts/role-ai-safety-and-model-red-team-specialist.md#output-ai-safety-and-model-red-team-specialist-2); [`ai-safety-and-model-red-team-specialist:3`](output-contracts/role-ai-safety-and-model-red-team-specialist.md#output-ai-safety-and-model-red-team-specialist-3)
6. **Named authority:** exact scoped human approval or rejection.
   **Receiving condition:** Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve
   **Output specifications:** [ai-system-approval:6](output-contracts/workflow-ai-system-approval.md#output-ai-system-approval-6)
7. **Machine Learning Engineer:** authorised deployed version and reproducible training lineage.
   **Receiving condition:** Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run
   **Output specifications:** [`machine-learning-engineer:1`](output-contracts/role-machine-learning-engineer.md#output-machine-learning-engineer-1); [`machine-learning-engineer:2`](output-contracts/role-machine-learning-engineer.md#output-machine-learning-engineer-2)
8. **MLOps Engineer:** monitored model with defined thresholds and rollback.
   **Receiving condition:** Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist
   **Output specifications:** [`mlops-engineer:2`](output-contracts/role-mlops-engineer.md#output-mlops-engineer-2); [`mlops-engineer:4`](output-contracts/role-mlops-engineer.md#output-mlops-engineer-4)
9. **AI Governance Officer:** periodic assessment, challenge route and next review trigger.
   **Receiving condition:** The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval
   **Output specifications:** [`ai-governance-officer:3`](output-contracts/role-ai-governance-officer.md#output-ai-governance-officer-3)

[Roles, activities and acceptance gates for this chain](../workflow-library/ai-system-approval.md#workflow-steps-and-gates).

## Supplier onboarding to exit

**Workflow key:** `supplier-onboarding`.

**Start when:** A technology supplier or SaaS product is being considered.

**Expected result:** A contracted supplier with assurance, monitored performance and a tested way out.

**Concrete stage outputs and receiving conditions:**

1. **IT Procurement Specialist:** tender, evaluation and recommendation.
   **Receiving condition:** Security, privacy, exit and continuity requirements in the tender, not added after
   **Output specifications:** [`it-procurement-specialist:1`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-1); [`it-procurement-specialist:2`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-2); [`it-procurement-specialist:3`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-3)
2. **Third-Party Risk Manager:** risk assessment and tier.
   **Receiving condition:** Critical suppliers have a tested exit or substitution plan
   **Output specifications:** [`third-party-risk-manager:1`](output-contracts/role-third-party-risk-manager.md#output-third-party-risk-manager-1)
3. **Security Architect:** supplier control requirements.
   **Receiving condition:** Requirements traced to threats, not copied from a questionnaire
   **Output specifications:** [`security-architect:4`](output-contracts/role-security-architect.md#output-security-architect-4)
4. **Contract Manager:** contract and obligation register.
   **Receiving condition:** Obligations on both sides tracked with owners
   **Output specifications:** [`contract-manager:1`](output-contracts/role-contract-manager.md#output-contract-manager-1)
5. **Vendor Manager:** scorecards and governance cadence.
   **Receiving condition:** Renewal started early enough for a real alternative to exist
   **Output specifications:** [`vendor-manager:1`](output-contracts/role-vendor-manager.md#output-vendor-manager-1); [`vendor-manager:2`](output-contracts/role-vendor-manager.md#output-vendor-manager-2)
6. **Service Level Manager:** aligned SLAs and OLAs.
   **Receiving condition:** No internal commitment exceeding what the supply chain can deliver
   **Output specifications:** [`service-level-manager:1`](output-contracts/role-service-level-manager.md#output-service-level-manager-1); [`service-level-manager:4`](output-contracts/role-service-level-manager.md#output-service-level-manager-4)
7. **Business Continuity Manager:** exercised continuity and exit plan.
   **Receiving condition:** Exit tested, not described
   **Output specifications:** [`business-continuity-manager:2`](output-contracts/role-business-continuity-manager.md#output-business-continuity-manager-2); [`business-continuity-manager:3`](output-contracts/role-business-continuity-manager.md#output-business-continuity-manager-3)

[Roles, activities and acceptance gates for this chain](../workflow-library/supplier-onboarding.md#workflow-steps-and-gates).

## Business case to realised benefits

**Workflow key:** `business-case-to-benefits`.

**Start when:** An investment has a proposed business case and needs measurable benefits governed through and beyond delivery.

**Expected result:** Benefits are baselined, owned, measured after go-live and used for continue/correct/close decisions.

**Concrete stage outputs and receiving conditions:**

1. **Portfolio Manager:** investment decision context and thresholds.
   **Receiving condition:** The initiative has an accountable sponsor and an explicit decision threshold
   **Output specifications:** [`portfolio-manager:1`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-1); [`portfolio-manager:2`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-2)
2. **Business Analyst:** requirements and outcome baseline.
   **Receiving condition:** Outcome statements are measurable and sourced
   **Output specifications:** [`business-analyst:1`](output-contracts/role-business-analyst.md#output-business-analyst-1)
3. **Benefits Realisation Manager:** benefits map, register and realisation plan.
   **Receiving condition:** No benefit without owner, baseline, target, source and timing
   **Output specifications:** [`benefits-realisation-manager:1`](output-contracts/role-benefits-realisation-manager.md#output-benefits-realisation-manager-1); [`benefits-realisation-manager:2`](output-contracts/role-benefits-realisation-manager.md#output-benefits-realisation-manager-2); [`benefits-realisation-manager:3`](output-contracts/role-benefits-realisation-manager.md#output-benefits-realisation-manager-3)
4. **Product Manager:** roadmap with success measures.
   **Receiving condition:** Roadmap outcomes trace to registered benefits rather than feature volume
   **Output specifications:** [`product-manager:1`](output-contracts/role-product-manager.md#output-product-manager-1)
5. **Organisational Change and Adoption Manager:** adoption plan and readiness measures.
   **Receiving condition:** Benefit dependencies on behaviour have explicit owners and measures
   **Output specifications:** [`organisational-change-and-adoption-manager:2`](output-contracts/role-organisational-change-and-adoption-manager.md#output-organisational-change-and-adoption-manager-2); [`organisational-change-and-adoption-manager:3`](output-contracts/role-organisational-change-and-adoption-manager.md#output-organisational-change-and-adoption-manager-3)
6. **Product Analyst:** observed benefit results and confidence.
   **Receiving condition:** Results use the pre-agreed method and disclose uncertainty
   **Output specifications:** [`product-analyst:1`](output-contracts/role-product-analyst.md#output-product-analyst-1); [`product-analyst:2`](output-contracts/role-product-analyst.md#output-product-analyst-2)
7. **Benefits Realisation Manager:** post-implementation benefits review.
   **Receiving condition:** Variance, disbenefits and corrective actions are owned and decision-ready
   **Output specifications:** [`benefits-realisation-manager:4`](output-contracts/role-benefits-realisation-manager.md#output-benefits-realisation-manager-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/business-case-to-benefits.md#workflow-steps-and-gates).

## Design to operational readiness

**Workflow key:** `design-to-operational-readiness`.

**Start when:** A solution design is becoming build/release ready and must prove it can be operated safely before go-live.

**Expected result:** The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.

**Concrete stage outputs and receiving conditions:**

1. **Solution Architect:** solution architecture and decision records.
   **Receiving condition:** Quality attributes and failure modes are explicit and testable
   **Output specifications:** [`solution-architect:1`](output-contracts/role-solution-architect.md#output-solution-architect-1); [`solution-architect:4`](output-contracts/role-solution-architect.md#output-solution-architect-4)
2. **Security Architect:** security architecture and control requirements.
   **Receiving condition:** Controls trace to risks and objectives
   **Output specifications:** [`security-architect:1`](output-contracts/role-security-architect.md#output-security-architect-1); [`security-architect:4`](output-contracts/role-security-architect.md#output-security-architect-4)
3. **Operational and Technology Resilience Architect:** resilience architecture and validation scenarios.
   **Receiving condition:** Resilience claims identify dependencies, failure domains and validation method
   **Output specifications:** [`operational-and-technology-resilience-architect:1`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-1); [`operational-and-technology-resilience-architect:2`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-2); [`operational-and-technology-resilience-architect:4`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-4)
4. **Site Reliability Engineer:** SLO/monitoring design and runbook requirements.
   **Receiving condition:** Alerts are actionable and every SLO has a data source
   **Output specifications:** [`site-reliability-engineer:1`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-1)
5. **Service Transition and Operational Readiness Manager:** operational readiness assessment and evidence pack.
   **Receiving condition:** Every readiness criterion is pass/fail/waived with evidence and owner
   **Output specifications:** [`service-transition-and-operational-readiness-manager:1`](output-contracts/role-service-transition-and-operational-readiness-manager.md#output-service-transition-and-operational-readiness-manager-1); [`service-transition-and-operational-readiness-manager:3`](output-contracts/role-service-transition-and-operational-readiness-manager.md#output-service-transition-and-operational-readiness-manager-3)
6. **Change Manager:** change authorisation decision.
   **Receiving condition:** Change risk and readiness evidence match the approval route
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1)
7. **IT Service Owner:** service acceptance.
   **Receiving condition:** Support ownership, SLOs and residual risks are explicitly accepted
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1)

[Roles, activities and acceptance gates for this chain](../workflow-library/design-to-operational-readiness.md#workflow-steps-and-gates).

## Migration and cutover

**Workflow key:** `migration-and-cutover`.

**Start when:** A project must move data/services from a current state to a target state through a controlled production cutover.

**Expected result:** Migration completes with reconciled data, controlled rollback boundaries, operational acceptance and owned residual defects.

**Concrete stage outputs and receiving conditions:**

1. **Data Architect:** migration data model and ownership boundaries.
   **Receiving condition:** Every migrated domain has an accountable data owner and target definition
   **Output specifications:** [`data-architect:1`](output-contracts/role-data-architect.md#output-data-architect-1); [`data-architect:3`](output-contracts/role-data-architect.md#output-data-architect-3)
2. **Data Migration and Cutover Lead:** migration plan, cutover runbook and rollback plan.
   **Receiving condition:** Every object has mapping, acceptance and rollback/restore semantics
   **Output specifications:** [`data-migration-and-cutover-lead:1`](output-contracts/role-data-migration-and-cutover-lead.md#output-data-migration-and-cutover-lead-1); [`data-migration-and-cutover-lead:2`](output-contracts/role-data-migration-and-cutover-lead.md#output-data-migration-and-cutover-lead-2); [`data-migration-and-cutover-lead:4`](output-contracts/role-data-migration-and-cutover-lead.md#output-data-migration-and-cutover-lead-4)
3. **Data Engineer:** pre-production rehearsal evidence and exceptions.
   **Receiving condition:** Permitted data and test scope are explicit; rehearsal proves throughput, error handling and repeatability without production cutover effects
   **Output specifications:** [`data-engineer:1`](output-contracts/role-data-engineer.md#output-data-engineer-1); [`data-engineer:3`](output-contracts/role-data-engineer.md#output-data-engineer-3)
4. **Test Manager:** test and residual-risk report.
   **Receiving condition:** Rehearsal exit criteria are defined before execution; any permitted exception has prior named authority for its exact scope; mandatory controls remain blocking
   **Output specifications:** [`test-manager:2`](output-contracts/role-test-manager.md#output-test-manager-2); [`test-manager:3`](output-contracts/role-test-manager.md#output-test-manager-3)
5. **Service Transition and Operational Readiness Manager:** operational cutover constraints and acceptance evidence.
   **Receiving condition:** No critical operational readiness gap is unowned
   **Output specifications:** [`service-transition-and-operational-readiness-manager:3`](output-contracts/role-service-transition-and-operational-readiness-manager.md#output-service-transition-and-operational-readiness-manager-3)
6. **Release Engineer:** candidate release manifest and rehearsal deployment/rollback evidence.
   **Receiving condition:** Exact artefact versions and rollback steps are known; no production effects before the human change decision
   **Output specifications:** [`release-engineer:2`](output-contracts/role-release-engineer.md#output-release-engineer-2); [`release-engineer:4`](output-contracts/role-release-engineer.md#output-release-engineer-4)
7. **Change Manager:** production change authorisation.
   **Receiving condition:** Pre-production rehearsal, reconciliation design and operational readiness evidence precede exact human authorisation covering cutover and validation effects, data, versions, environment, window and rollback boundaries; no destructive test or data exposure outside that prior approved scope
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1)
8. **Data Engineer:** actual cutover execution, reconciliation and stop/go evidence.
   **Receiving condition:** Prior exact human change authorisation covers data, versions, environment, window and rollback; stop on failed criteria or changed scope
   **Output specifications:** [`data-engineer:1`](output-contracts/role-data-engineer.md#output-data-engineer-1); [`data-engineer:3`](output-contracts/role-data-engineer.md#output-data-engineer-3)
9. **Test Analyst:** executed independent validation cases, observed results, reconciliation evidence and located defects.
   **Receiving condition:** Prior exact human change authorisation covers the validation effects and data boundaries; no unapproved destructive tests or data exposure; record actual observations and untested conditions without substituting the migration executor's self-check
   **Output specifications:** [`test-analyst:2`](output-contracts/role-test-analyst.md#output-test-analyst-2); [`test-analyst:4`](output-contracts/role-test-analyst.md#output-test-analyst-4)
10. **Test Manager:** independent production validation and residual-risk report.
   **Receiving condition:** Independent validation uses actual authorised execution evidence against predeclared criteria; unresolved blocking defects prevent service acceptance
   **Output specifications:** [`test-manager:2`](output-contracts/role-test-manager.md#output-test-manager-2); [`test-manager:3`](output-contracts/role-test-manager.md#output-test-manager-3)
11. **IT Service Owner:** service acceptance and residual issues.
   **Receiving condition:** Service, data and ownership acceptance are explicit before legacy retirement
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1); [`it-service-owner:4`](output-contracts/role-it-service-owner.md#output-it-service-owner-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/migration-and-cutover.md#workflow-steps-and-gates).

## Organisational change and adoption

**Workflow key:** `organisational-change-and-adoption`.

**Start when:** Technology or process change requires people to work differently for the intended outcome to materialise.

**Expected result:** Affected cohorts are ready, adopt the new behaviour and produce evidence that supports the intended business benefit.

**Concrete stage outputs and receiving conditions:**

1. **Business Relationship Manager:** business outcome and stakeholder context.
   **Receiving condition:** There is a named sponsor and business outcome
   **Output specifications:** [`business-relationship-manager:1`](output-contracts/role-business-relationship-manager.md#output-business-relationship-manager-1); [`business-relationship-manager:3`](output-contracts/role-business-relationship-manager.md#output-business-relationship-manager-3)
2. **Organisational Change and Adoption Manager:** change impact assessment and adoption strategy.
   **Receiving condition:** Every material cohort has impact, readiness and owner
   **Output specifications:** [`organisational-change-and-adoption-manager:1`](output-contracts/role-organisational-change-and-adoption-manager.md#output-organisational-change-and-adoption-manager-1); [`organisational-change-and-adoption-manager:2`](output-contracts/role-organisational-change-and-adoption-manager.md#output-organisational-change-and-adoption-manager-2)
3. **IT Trainer:** training assets and proficiency checks.
   **Receiving condition:** Training maps to changed tasks and has proficiency evidence
   **Output specifications:** [`it-trainer:2`](output-contracts/role-it-trainer.md#output-it-trainer-2); [`it-trainer:4`](output-contracts/role-it-trainer.md#output-it-trainer-4)
4. **Product Manager:** release/adoption alignment.
   **Receiving condition:** No cohort is asked to adopt functionality unavailable or unstable in its wave
   **Output specifications:** [`product-manager:4`](output-contracts/role-product-manager.md#output-product-manager-4)
5. **Product Analyst:** adoption observations and segmentation.
   **Receiving condition:** Adoption is measured by behaviour/outcome, not attendance alone
   **Output specifications:** [`product-analyst:4`](output-contracts/role-product-analyst.md#output-product-analyst-4)
6. **Benefits Realisation Manager:** benefit/adoption review.
   **Receiving condition:** Below-target adoption or benefits have owned reinforcement or reforecast actions
   **Output specifications:** [`benefits-realisation-manager:4`](output-contracts/role-benefits-realisation-manager.md#output-benefits-realisation-manager-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/organisational-change-and-adoption.md#workflow-steps-and-gates).

## Semantic artefact to enterprise publication

**Workflow key:** `semantic-to-enterprise-publication`.

**Start when:** A specialist artefact is substantively complete and requires enterprise-grade publication.

**Expected result:** A released audience-specific publication whose semantic content is traceable to the approved source and has passed semantic and publication gates.

**Concrete stage outputs and receiving conditions:**

1. **Owning specialist:** semantic publication model.
   **Receiving condition:** Semantic source is complete enough to review; unresolved items are explicit
   **Output specifications:** [semantic-to-enterprise-publication:1](output-contracts/workflow-semantic-to-enterprise-publication.md#output-semantic-to-enterprise-publication-1)
2. **Evidence & Rationale Reviewer:** semantic gate result and located findings.
   **Receiving condition:** Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking
   **Output specifications:** [semantic-to-enterprise-publication:2](output-contracts/workflow-semantic-to-enterprise-publication.md#output-semantic-to-enterprise-publication-2)
3. **Enterprise Publication Editor:** rendered publication set with semantic hash.
   **Receiving condition:** All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release
   **Output specifications:** [semantic-to-enterprise-publication:3](output-contracts/workflow-semantic-to-enterprise-publication.md#output-semantic-to-enterprise-publication-3)
4. **Visual Quality Reviewer:** publication gate result and findings.
   **Receiving condition:** Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking
   **Output specifications:** [semantic-to-enterprise-publication:4](output-contracts/workflow-semantic-to-enterprise-publication.md#output-semantic-to-enterprise-publication-4)
5. **Named authority:** release approval.
   **Receiving condition:** Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers
   **Output specifications:** [semantic-to-enterprise-publication:5](output-contracts/workflow-semantic-to-enterprise-publication.md#output-semantic-to-enterprise-publication-5)

[Roles, activities and acceptance gates for this chain](../workflow-library/semantic-to-enterprise-publication.md#workflow-steps-and-gates).

## Architecture model to repository governance

**Workflow key:** `architecture-model-to-repository-governance`.

**Start when:** A project/domain architecture needs to become a governed enterprise repository model and published view set.

**Expected result:** Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners.

**Concrete stage outputs and receiving conditions:**

1. **Solution Architect:** project architecture model and source artefacts.
   **Receiving condition:** Elements/relationships have stable identities and evidence basis
   **Output specifications:** [`solution-architect:1`](output-contracts/role-solution-architect.md#output-solution-architect-1); [`solution-architect:4`](output-contracts/role-solution-architect.md#output-solution-architect-4)
2. **Architecture Repository and Modelling Lead:** canonical project model.
   **Receiving condition:** No model fact is silently reinterpreted to fit a tool
   **Output specifications:** [`architecture-repository-and-modelling-lead:1`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-1); [`architecture-repository-and-modelling-lead:3`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-3)
3. **Architecture Repository Engineer:** repository revision plus interchange artefacts.
   **Receiving condition:** Repository structural validation passes
   **Output specifications:** [`architecture-repository-and-modelling-lead:3`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-3)
4. **Model Consistency Reviewer:** consistency findings/gate.
   **Receiving condition:** No blocking integrity error remains
   **Output specifications:** [`architecture-repository-and-modelling-lead:4`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-4)
5. **Enterprise Architect:** accepted enterprise model/repository decisions.
   **Receiving condition:** Cross-project dependencies and reusable/reference elements have owners
   **Output specifications:** [`enterprise-architect:1`](output-contracts/role-enterprise-architect.md#output-enterprise-architect-1); [`enterprise-architect:4`](output-contracts/role-enterprise-architect.md#output-enterprise-architect-4)
6. **Technical Design Authority Member:** approved/rejected repository release.
   **Receiving condition:** Exceptions and residual risks have named authority and expiry/review
   **Output specifications:** [`technical-design-authority-member:1`](output-contracts/role-technical-design-authority-member.md#output-technical-design-authority-member-1); [`technical-design-authority-member:2`](output-contracts/role-technical-design-authority-member.md#output-technical-design-authority-member-2); [`technical-design-authority-member:3`](output-contracts/role-technical-design-authority-member.md#output-technical-design-authority-member-3)

[Roles, activities and acceptance gates for this chain](../workflow-library/architecture-model-to-repository-governance.md#workflow-steps-and-gates).

## Service retirement and decommission

**Workflow key:** `service-retirement-and-decommission`.

**Start when:** A service, application, platform or technology component is approved for retirement, replacement or exit.

**Expected result:** The component is retired without hidden dependencies, unmanaged data/access, stale records or unowned residual obligations, and the retirement benefit is measured.

**Concrete stage outputs and receiving conditions:**

1. **IT Service Owner:** retirement mandate and target date.
   **Receiving condition:** Scope and authority are explicit
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1)
2. **Technology Lifecycle and Decommission Manager:** dependency impact and retirement plan.
   **Receiving condition:** Every material dependency has an owned disposition or named waiver
   **Output specifications:** [`technology-lifecycle-and-decommission-manager:1`](output-contracts/role-technology-lifecycle-and-decommission-manager.md#output-technology-lifecycle-and-decommission-manager-1); [`technology-lifecycle-and-decommission-manager:2`](output-contracts/role-technology-lifecycle-and-decommission-manager.md#output-technology-lifecycle-and-decommission-manager-2)
3. **Data Protection Officer:** data disposition position.
   **Receiving condition:** Regulated/personal data disposition is authorised before irreversible action
   **Output specifications:** [`data-protection-officer:1`](output-contracts/role-data-protection-officer.md#output-data-protection-officer-1); [`data-protection-officer:2`](output-contracts/role-data-protection-officer.md#output-data-protection-officer-2)
4. **Change Manager:** prior scoped human production-change authorisation.
   **Receiving condition:** Dependency and data-disposition plans and rehearsal evidence are available before destructive action; approval covers exact credential and service changes, not a completed retirement
   **Output specifications:** [`change-manager:1`](output-contracts/role-change-manager.md#output-change-manager-1)
5. **Identity and Access Management Engineer:** access-transfer evidence and the exact owned, time-bounded shutdown-access list.
   **Receiving condition:** Prior exact human change approval covers each removal or transfer; retain only explicitly owned bounded shutdown credentials needed for the approved shutdown, with purpose, expiry and final revocation owner
   **Output specifications:** [`identity-and-access-management-engineer:3`](output-contracts/role-identity-and-access-management-engineer.md#output-identity-and-access-management-engineer-3)
6. **Site Reliability Engineer:** actual shutdown, final credential revocation and reconciliation evidence, and verified technical state.
   **Receiving condition:** Prior exact human change and data-disposition authorisation covers every effect; stop on changed scope or failed dependency/archive checks; the assigned IAM actor closes retained shutdown access and verifies final credential reconciliation before asset reconciliation
   **Output specifications:** [`site-reliability-engineer:3`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-3)
7. **IT Asset Manager:** asset/configuration closure.
   **Receiving condition:** Systems of record match the retired technical state
   **Output specifications:** [`it-asset-manager:1`](output-contracts/role-it-asset-manager.md#output-it-asset-manager-1); [`it-asset-manager:3`](output-contracts/role-it-asset-manager.md#output-it-asset-manager-3)
8. **Architecture Repository and Modelling Lead:** repository retirement revision.
   **Receiving condition:** Repository has no unowned active dependency into the retired element
   **Output specifications:** [`architecture-repository-and-modelling-lead:3`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-3); [`architecture-repository-and-modelling-lead:4`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-4)
9. **Benefits Realisation Manager:** benefits closure result.
   **Receiving condition:** Benefit or disbenefit variance has an accountable owner
   **Output specifications:** [`benefits-realisation-manager:4`](output-contracts/role-benefits-realisation-manager.md#output-benefits-realisation-manager-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/service-retirement-and-decommission.md#workflow-steps-and-gates).

## Cyber incident / breach to recovery

**Workflow key:** `cyber-incident-breach-to-recovery`.

**Start when:** A suspected or confirmed cyber incident may affect systems, data, customers, regulatory obligations or business operations.

**Expected result:** The incident is contained and eradicated, evidence is preserved, recovery is accepted by the business, notification decisions are traceable, and control remediation is closed or owned.

**Concrete stage outputs and receiving conditions:**

1. **Security Analyst Tier 1:** incident record with source/time/scope.
   **Receiving condition:** A real event or explicit false-positive rationale is recorded
   **Output specifications:** [`security-analyst-tier-1:1`](output-contracts/role-security-analyst-tier-1.md#output-security-analyst-tier-1-1); [`security-analyst-tier-1:2`](output-contracts/role-security-analyst-tier-1.md#output-security-analyst-tier-1-2); [`security-analyst-tier-1:3`](output-contracts/role-security-analyst-tier-1.md#output-security-analyst-tier-1-3)
2. **Incident Responder:** triage decision and containment objectives.
   **Receiving condition:** Severity/scope have evidence and an accountable incident lead
   **Output specifications:** [`incident-responder:2`](output-contracts/role-incident-responder.md#output-incident-responder-2)
3. **Incident Responder:** containment actions and status.
   **Receiving condition:** Containment does not destroy material evidence without authority
   **Output specifications:** [`incident-responder:1`](output-contracts/role-incident-responder.md#output-incident-responder-1); [`incident-responder:2`](output-contracts/role-incident-responder.md#output-incident-responder-2)
4. **Digital Forensics Examiner:** evidence register and forensic timeline.
   **Receiving condition:** Evidence integrity, time source and custody are documented
   **Output specifications:** [`digital-forensics-examiner:1`](output-contracts/role-digital-forensics-examiner.md#output-digital-forensics-examiner-1); [`digital-forensics-examiner:2`](output-contracts/role-digital-forensics-examiner.md#output-digital-forensics-examiner-2); [`digital-forensics-examiner:3`](output-contracts/role-digital-forensics-examiner.md#output-digital-forensics-examiner-3)
5. **IT Risk Manager:** impact assessment with uncertainty and affected obligations.
   **Receiving condition:** Critical impact claims distinguish confirmed fact from inference
   **Output specifications:** [`it-risk-manager:2`](output-contracts/role-it-risk-manager.md#output-it-risk-manager-2)
6. **Data Protection Officer:** breach/notification decision basis.
   **Receiving condition:** Notification/non-notification has correct authority, clock and evidence
   **Output specifications:** [`data-protection-officer:4`](output-contracts/role-data-protection-officer.md#output-data-protection-officer-4)
7. **Incident Responder:** eradication evidence and residual technical risks.
   **Receiving condition:** Known persistence and exploited control gaps are addressed or explicitly owned
   **Output specifications:** [`incident-responder:1`](output-contracts/role-incident-responder.md#output-incident-responder-1); [`incident-responder:2`](output-contracts/role-incident-responder.md#output-incident-responder-2)
8. **Disaster Recovery Coordinator:** recovery evidence and service restoration status.
   **Receiving condition:** Recovery uses trusted state/data and respects RTO/RPO/business priorities
   **Output specifications:** [`disaster-recovery-coordinator:2`](output-contracts/role-disaster-recovery-coordinator.md#output-disaster-recovery-coordinator-2)
9. **IT Service Owner:** business recovery acceptance.
   **Receiving condition:** Service owner confirms agreed validation signals and residual limitations
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1); [`it-service-owner:4`](output-contracts/role-it-service-owner.md#output-it-service-owner-4)
10. **Crisis Manager:** communication/regulatory action record.
   **Receiving condition:** Communications are authorised, consistent and evidence-based
   **Output specifications:** [`crisis-manager:2`](output-contracts/role-crisis-manager.md#output-crisis-manager-2); [`crisis-manager:3`](output-contracts/role-crisis-manager.md#output-crisis-manager-3)
11. **Problem Manager:** lessons learned and systemic findings.
   **Receiving condition:** Findings address causes and failed controls, not only symptoms
   **Output specifications:** [`problem-manager:1`](output-contracts/role-problem-manager.md#output-problem-manager-1)
12. **Control Owner:** control remediation plan.
   **Receiving condition:** Every material finding has a control owner, due date and verification method
   **Output specifications:** [`control-owner:4`](output-contracts/role-control-owner.md#output-control-owner-4)
13. **Internal IT Auditor:** closure assurance result.
   **Receiving condition:** No open critical finding is silently closed or self-assured
   **Output specifications:** [`internal-it-auditor:4`](output-contracts/role-internal-it-auditor.md#output-internal-it-auditor-4)

[Roles, activities and acceptance gates for this chain](../workflow-library/cyber-incident-breach-to-recovery.md#workflow-steps-and-gates).

## Resilience validation

**Workflow key:** `resilience-validation`.

**Start when:** A critical service or architecture needs evidence that resilience, RTO/RPO and dependency assumptions work under realistic failure.

**Expected result:** Business criticality, dependencies and recovery objectives are validated through exercised failure scenarios, findings are remediated and retested, and residual resilience risk is accepted by the correct authority.

**Concrete stage outputs and receiving conditions:**

1. **Business Continuity Manager:** business criticality baseline.
   **Receiving condition:** Criticality and tolerances have business ownership
   **Output specifications:** [`business-continuity-manager:1`](output-contracts/role-business-continuity-manager.md#output-business-continuity-manager-1); [`business-continuity-manager:4`](output-contracts/role-business-continuity-manager.md#output-business-continuity-manager-4)
2. **Operational and Technology Resilience Architect:** dependency/failure-domain model.
   **Receiving condition:** No critical path has an unknown/unowned dependency
   **Output specifications:** [`operational-and-technology-resilience-architect:2`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-2)
3. **Disaster Recovery Coordinator:** validated recovery objectives.
   **Receiving condition:** Objectives are feasible end to end, not only per component
   **Output specifications:** [`disaster-recovery-coordinator:2`](output-contracts/role-disaster-recovery-coordinator.md#output-disaster-recovery-coordinator-2); [`disaster-recovery-coordinator:3`](output-contracts/role-disaster-recovery-coordinator.md#output-disaster-recovery-coordinator-3)
4. **Operational and Technology Resilience Architect:** resilience design with failure assumptions.
   **Receiving condition:** Design addresses single/shared failure modes and measurable outcomes
   **Output specifications:** [`operational-and-technology-resilience-architect:1`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-1); [`operational-and-technology-resilience-architect:3`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-3)
5. **Test Manager:** approved exercise plan.
   **Receiving condition:** Test design can falsify the resilience claims and protects production safety
   **Output specifications:** [`test-manager:1`](output-contracts/role-test-manager.md#output-test-manager-1)
6. **Chaos and Resilience Engineer:** exercise evidence.
   **Receiving condition:** Execution matches approved scope and evidence is attributable
   **Output specifications:** [`chaos-and-resilience-engineer:1`](output-contracts/role-chaos-and-resilience-engineer.md#output-chaos-and-resilience-engineer-1); [`chaos-and-resilience-engineer:2`](output-contracts/role-chaos-and-resilience-engineer.md#output-chaos-and-resilience-engineer-2)
7. **Control Tester:** findings register.
   **Receiving condition:** Findings distinguish observation, criterion, impact and evidence
   **Output specifications:** [`control-tester:3`](output-contracts/role-control-tester.md#output-control-tester-3)
8. **Operational and Technology Resilience Architect:** remediation plan.
   **Receiving condition:** Every material finding has owner/date/design response
   **Output specifications:** [`operational-and-technology-resilience-architect:4`](output-contracts/role-operational-and-technology-resilience-architect.md#output-operational-and-technology-resilience-architect-4)
9. **Test Manager:** retest result.
   **Receiving condition:** Critical findings are demonstrated fixed, not administratively closed
   **Output specifications:** [`test-manager:2`](output-contracts/role-test-manager.md#output-test-manager-2)
10. **IT Service Owner:** resilience acceptance.
   **Receiving condition:** Acceptance states evidence, residual risk and next validation date
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1)

[Roles, activities and acceptance gates for this chain](../workflow-library/resilience-validation.md#workflow-steps-and-gates).

## Demand to portfolio to funding

**Workflow key:** `demand-to-portfolio-to-funding`.

**Start when:** A new business/technology demand needs to be qualified, compared with alternatives and either rejected, redirected or committed into a funded portfolio.

**Expected result:** Demand is traceable from intake through capability/architecture/risk/value assessment, sizing/capacity and prioritisation to an explicit funding/portfolio commitment decision.

**Concrete stage outputs and receiving conditions:**

1. **Demand & Intake Manager:** demand record.
   **Receiving condition:** No anonymous or outcome-free demand enters prioritisation
   **Output specifications:** [`demand-and-intake-manager:1`](output-contracts/role-demand-and-intake-manager.md#output-demand-and-intake-manager-1)
2. **Demand & Intake Manager:** qualification assessment.
   **Receiving condition:** Disposition is explicit: reject, redirect, discover or assess
   **Output specifications:** [`demand-and-intake-manager:2`](output-contracts/role-demand-and-intake-manager.md#output-demand-and-intake-manager-2)
3. **Enterprise Architect:** capability-fit assessment.
   **Receiving condition:** Existing capability/service reuse and strategic conflicts are explicit
   **Output specifications:** [`enterprise-architect:1`](output-contracts/role-enterprise-architect.md#output-enterprise-architect-1)
4. **Application Portfolio Manager:** application portfolio impact assessment.
   **Receiving condition:** Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner
   **Output specifications:** [`application-portfolio-manager:1`](output-contracts/role-application-portfolio-manager.md#output-application-portfolio-manager-1); [`application-portfolio-manager:2`](output-contracts/role-application-portfolio-manager.md#output-application-portfolio-manager-2)
5. **Solution Architect:** architecture impact assessment.
   **Receiving condition:** Material cross-domain dependencies and constraints are identified
   **Output specifications:** [`solution-architect:1`](output-contracts/role-solution-architect.md#output-solution-architect-1)
6. **IT Risk Manager:** risk/value assessment.
   **Receiving condition:** Regulatory/risk urgency is evidence-based and not double-counted as value
   **Output specifications:** [`it-risk-manager:2`](output-contracts/role-it-risk-manager.md#output-it-risk-manager-2)
7. **Resource Manager:** estimate and capacity view.
   **Receiving condition:** Uncertainty ranges and constrained skills/capacity are explicit
   **Output specifications:** [`resource-manager:1`](output-contracts/role-resource-manager.md#output-resource-manager-1)
8. **Portfolio Manager:** prioritisation decision.
   **Receiving condition:** Prioritisation can be reconstructed from declared criteria and exceptions
   **Output specifications:** [`portfolio-manager:1`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-1); [`portfolio-manager:4`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-4)
9. **IT Financial Management / TBM Manager:** funding economics and cost profile.
   **Receiving condition:** Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model
   **Output specifications:** [`it-financial-management-tbm-manager:1`](output-contracts/role-it-financial-management-tbm-manager.md#output-it-financial-management-tbm-manager-1); [`it-financial-management-tbm-manager:2`](output-contracts/role-it-financial-management-tbm-manager.md#output-it-financial-management-tbm-manager-2)
10. **Portfolio Manager:** portfolio commitment.
   **Receiving condition:** Commitment has authority, funding/capacity basis and review condition
   **Output specifications:** [`portfolio-manager:2`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-2)

[Roles, activities and acceptance gates for this chain](../workflow-library/demand-to-portfolio-to-funding.md#workflow-steps-and-gates).

## Source to contract to service

**Workflow key:** `source-to-contract-to-service`.

**Start when:** A capability may be sourced externally and must move from requirement/RFI/RFP through supplier selection and contract controls to implementation and accepted service.

**Expected result:** The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance.

**Concrete stage outputs and receiving conditions:**

1. **Business Analyst:** sourcing requirement baseline.
   **Receiving condition:** Requirements are testable and distinguish need from preferred solution
   **Output specifications:** [`business-analyst:1`](output-contracts/role-business-analyst.md#output-business-analyst-1)
2. **IT Procurement Specialist:** RFI/RFP pack and response evidence.
   **Receiving condition:** Supplier responses are comparable and procurement rules are followed
   **Output specifications:** [`it-procurement-specialist:1`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-1); [`it-procurement-specialist:2`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-2)
3. **Vendor Manager:** supplier assessment.
   **Receiving condition:** Material supplier assumptions and dependency risks are evidenced
   **Output specifications:** [`vendor-manager:1`](output-contracts/role-vendor-manager.md#output-vendor-manager-1)
4. **Third-Party Risk Manager:** security/privacy/supplier risk assessment.
   **Receiving condition:** Critical risks/obligations are resolved, mitigated or accepted by correct authority
   **Output specifications:** [`third-party-risk-manager:1`](output-contracts/role-third-party-risk-manager.md#output-third-party-risk-manager-1); [`third-party-risk-manager:3`](output-contracts/role-third-party-risk-manager.md#output-third-party-risk-manager-3)
5. **Enterprise Applications Architect:** architecture-fit decision.
   **Receiving condition:** Selection does not create hidden target-state or integration contradictions
   **Output specifications:** [`enterprise-applications-architect:2`](output-contracts/role-enterprise-applications-architect.md#output-enterprise-applications-architect-2); [`enterprise-applications-architect:4`](output-contracts/role-enterprise-applications-architect.md#output-enterprise-applications-architect-4)
6. **IT Procurement Specialist:** selection decision.
   **Receiving condition:** Decision is traceable to declared criteria, evidence and authority
   **Output specifications:** [`it-procurement-specialist:2`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-2); [`it-procurement-specialist:3`](output-contracts/role-it-procurement-specialist.md#output-it-procurement-specialist-3)
7. **Contract Manager:** contract control schedule.
   **Receiving condition:** Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path
   **Output specifications:** [`contract-manager:1`](output-contracts/role-contract-manager.md#output-contract-manager-1)
8. **Implementation Consultant:** implementation plan and evidence.
   **Receiving condition:** Implementation deviations are approved, not silently normalised
   **Output specifications:** [`implementation-consultant:1`](output-contracts/role-implementation-consultant.md#output-implementation-consultant-1); [`implementation-consultant:3`](output-contracts/role-implementation-consultant.md#output-implementation-consultant-3)
9. **Service Transition and Operational Readiness Manager:** service acceptance.
   **Receiving condition:** No production acceptance with missing critical operational ownership/evidence
   **Output specifications:** [`service-transition-and-operational-readiness-manager:3`](output-contracts/role-service-transition-and-operational-readiness-manager.md#output-service-transition-and-operational-readiness-manager-3); [`service-transition-and-operational-readiness-manager:4`](output-contracts/role-service-transition-and-operational-readiness-manager.md#output-service-transition-and-operational-readiness-manager-4)
10. **Vendor Manager:** vendor governance baseline.
   **Receiving condition:** Contractual obligations map to measured service/vendor governance
   **Output specifications:** [`vendor-manager:1`](output-contracts/role-vendor-manager.md#output-vendor-manager-1); [`vendor-manager:2`](output-contracts/role-vendor-manager.md#output-vendor-manager-2)

[Roles, activities and acceptance gates for this chain](../workflow-library/source-to-contract-to-service.md#workflow-steps-and-gates).

## SIAM / multi-supplier service integration

**Workflow key:** `siam-multi-supplier`.

**Start when:** A service depends on multiple suppliers/teams and end-to-end accountability, OLAs, incidents, problems, changes or acceptance are fragmented across boundaries.

**Expected result:** One governed service-integration model joins supplier responsibilities into end-to-end service outcomes with measurable SLAs/OLAs, clear process ownership and cross-supplier escalation.

**Concrete stage outputs and receiving conditions:**

1. **SIAM Manager:** SIAM operating model.
   **Receiving condition:** No customer outcome or integration process is ownerless
   **Output specifications:** [`siam-manager:1`](output-contracts/role-siam-manager.md#output-siam-manager-1)
2. **Service Level Manager:** SLA/OLA matrix.
   **Receiving condition:** Every SLA has sufficient underpinning measures/owners
   **Output specifications:** [`service-level-manager:1`](output-contracts/role-service-level-manager.md#output-service-level-manager-1); [`service-level-manager:4`](output-contracts/role-service-level-manager.md#output-service-level-manager-4)
3. **Architecture Repository and Modelling Lead:** shared dependency register/view set.
   **Receiving condition:** Material supplier/service dependencies have stable IDs and owners
   **Output specifications:** [`architecture-repository-and-modelling-lead:3`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-3)
4. **Incident Manager:** cross-supplier incident model.
   **Receiving condition:** Severity and service restoration ownership cannot bounce between suppliers
   **Output specifications:** [`incident-manager:1`](output-contracts/role-incident-manager.md#output-incident-manager-1)
5. **Problem Manager:** cross-supplier problem model.
   **Receiving condition:** Root causes crossing contracts still receive one end-to-end owner
   **Output specifications:** [`problem-manager:1`](output-contracts/role-problem-manager.md#output-problem-manager-1)
6. **Enterprise Release Manager:** integrated change/release calendar.
   **Receiving condition:** Cross-supplier change collisions and blackout constraints are governed
   **Output specifications:** [`enterprise-release-manager:1`](output-contracts/role-enterprise-release-manager.md#output-enterprise-release-manager-1)
7. **SIAM Manager:** supplier escalation matrix.
   **Receiving condition:** Escalation cannot be blocked by contractual ownership ambiguity
   **Output specifications:** [`siam-manager:3`](output-contracts/role-siam-manager.md#output-siam-manager-3)
8. **IT Service Owner:** shared service acceptance.
   **Receiving condition:** Service acceptance is end-to-end, not a collection of supplier self-attestations
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1)

[Roles, activities and acceptance gates for this chain](../workflow-library/siam-multi-supplier.md#workflow-steps-and-gates).

## Enterprise release orchestration

**Workflow key:** `enterprise-release-orchestration`.

**Start when:** Multiple products/platforms/suppliers must release into a shared business/technology environment and need one dependency, readiness and go/no-go process.

**Expected result:** The integrated release is sequenced, independently readiness-checked, authorised, executed by technical owners, validated and closed with measurable release performance.

**Concrete stage outputs and receiving conditions:**

1. **Enterprise Release Manager:** integrated release calendar.
   **Receiving condition:** All material releases and blackout/business constraints are represented
   **Output specifications:** [`enterprise-release-manager:1`](output-contracts/role-enterprise-release-manager.md#output-enterprise-release-manager-1)
2. **Architecture Repository and Modelling Lead:** release dependency register.
   **Receiving condition:** No critical dependency is missing an owner or sequence
   **Output specifications:** [`architecture-repository-and-modelling-lead:3`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-3); [`architecture-repository-and-modelling-lead:4`](output-contracts/role-architecture-repository-and-modelling-lead.md#output-architecture-repository-and-modelling-lead-4)
3. **Organisational Change and Adoption Manager:** business readiness.
   **Receiving condition:** Affected business cohorts have executable readiness actions/evidence
   **Output specifications:** [`organisational-change-and-adoption-manager:3`](output-contracts/role-organisational-change-and-adoption-manager.md#output-organisational-change-and-adoption-manager-3)
4. **Data Migration and Cutover Lead:** cutover readiness.
   **Receiving condition:** Cutover and data reconciliation are rehearsed/evidenced for critical transitions
   **Output specifications:** [`data-migration-and-cutover-lead:2`](output-contracts/role-data-migration-and-cutover-lead.md#output-data-migration-and-cutover-lead-2); [`data-migration-and-cutover-lead:3`](output-contracts/role-data-migration-and-cutover-lead.md#output-data-migration-and-cutover-lead-3)
5. **SIAM Manager:** supplier readiness.
   **Receiving condition:** No critical supplier dependency is relying on informal availability
   **Output specifications:** [`siam-manager:4`](output-contracts/role-siam-manager.md#output-siam-manager-4)
6. **Release Engineer:** technical/rollback readiness.
   **Receiving condition:** Release artefacts are traceable and rollback is exercised/feasible
   **Output specifications:** [`release-engineer:2`](output-contracts/role-release-engineer.md#output-release-engineer-2); [`release-engineer:4`](output-contracts/role-release-engineer.md#output-release-engineer-4)
7. **Secure Delivery / DevSecOps Architect:** secure delivery readiness evidence.
   **Receiving condition:** Critical secure-delivery controls and provenance are evidenced; deviations are owned, time-bound and visible to independent release assurance
   **Output specifications:** [`secure-delivery-devsecops-architect:3`](output-contracts/role-secure-delivery-devsecops-architect.md#output-secure-delivery-devsecops-architect-3)
8. **Release Quality Gatekeeper:** release gate assurance.
   **Receiving condition:** Producer cannot waive its own failed critical gate
   **Output specifications:** [`release-quality-gatekeeper:1`](output-contracts/role-release-quality-gatekeeper.md#output-release-quality-gatekeeper-1); [`release-quality-gatekeeper:2`](output-contracts/role-release-quality-gatekeeper.md#output-release-quality-gatekeeper-2)
9. **Enterprise Release Manager:** go/no-go decision.
   **Receiving condition:** Decision cites evidence, waivers, residual risk and abort triggers
   **Output specifications:** [`enterprise-release-manager:3`](output-contracts/role-enterprise-release-manager.md#output-enterprise-release-manager-3)
10. **Release Engineer:** release execution evidence.
   **Receiving condition:** Executed artefacts/plan match what was approved
   **Output specifications:** [`release-engineer:3`](output-contracts/role-release-engineer.md#output-release-engineer-3); [`release-engineer:4`](output-contracts/role-release-engineer.md#output-release-engineer-4)
11. **Site Reliability Engineer:** technical post-release validation.
   **Receiving condition:** Rollback/reversal triggers are acted on, not debated after breach
   **Output specifications:** [`site-reliability-engineer:1`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-1); [`site-reliability-engineer:3`](output-contracts/role-site-reliability-engineer.md#output-site-reliability-engineer-3)
12. **IT Service Owner:** release acceptance.
   **Receiving condition:** Closure states outcome, impact, residual issues and owners
   **Output specifications:** [`it-service-owner:1`](output-contracts/role-it-service-owner.md#output-it-service-owner-1)

[Roles, activities and acceptance gates for this chain](../workflow-library/enterprise-release-orchestration.md#workflow-steps-and-gates).

## Regulatory change to assurance

**Workflow key:** `regulatory-change-to-assurance`.

**Start when:** A new or changed law, regulation, supervisory expectation or contractual compliance obligation may affect IS/IT services, controls or architecture.

**Expected result:** Applicability and obligations are translated into traceable requirements/controls, architecture and remediation changes are implemented, evidence is independently assured, and closure is authorised.

**Concrete stage outputs and receiving conditions:**

1. **Compliance Officer (Technology):** regulatory change record.
   **Receiving condition:** Source, jurisdiction, dates and version are attributable
   **Output specifications:** [`compliance-officer-technology:1`](output-contracts/role-compliance-officer-technology.md#output-compliance-officer-technology-1)
2. **Compliance Officer (Technology):** applicability decision.
   **Receiving condition:** In/out-of-scope rationale and authority are explicit
   **Output specifications:** [`compliance-officer-technology:2`](output-contracts/role-compliance-officer-technology.md#output-compliance-officer-technology-2)
3. **GRC Analyst:** obligations register.
   **Receiving condition:** Each obligation retains source citation/context and applicability owner
   **Output specifications:** [`grc-analyst:1`](output-contracts/role-grc-analyst.md#output-grc-analyst-1); [`grc-analyst:3`](output-contracts/role-grc-analyst.md#output-grc-analyst-3)
4. **Business Analyst:** requirements baseline.
   **Receiving condition:** Requirements preserve obligation intent and are testable
   **Output specifications:** [`business-analyst:1`](output-contracts/role-business-analyst.md#output-business-analyst-1)
5. **Control Owner:** control mapping and gap register.
   **Receiving condition:** Every requirement maps to effective control evidence or an owned gap
   **Output specifications:** [`control-owner:1`](output-contracts/role-control-owner.md#output-control-owner-1); [`control-owner:3`](output-contracts/role-control-owner.md#output-control-owner-3)
6. **Enterprise Architect:** architecture impact assessment.
   **Receiving condition:** Cross-domain impacts and affected governed models are explicit
   **Output specifications:** [`enterprise-architect:1`](output-contracts/role-enterprise-architect.md#output-enterprise-architect-1)
7. **Portfolio Manager:** remediation roadmap.
   **Receiving condition:** Mandatory deadlines and dependencies are funded/owned or escalated
   **Output specifications:** [`portfolio-manager:1`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-1); [`portfolio-manager:2`](output-contracts/role-portfolio-manager.md#output-portfolio-manager-2)
8. **Control Owner:** evidence pack.
   **Receiving condition:** Evidence is attributable to implemented control version and period
   **Output specifications:** [`control-owner:2`](output-contracts/role-control-owner.md#output-control-owner-2)
9. **Internal IT Auditor:** assurance report.
   **Receiving condition:** Assurance is independent and reports exceptions/limitations
   **Output specifications:** [`internal-it-auditor:3`](output-contracts/role-internal-it-auditor.md#output-internal-it-auditor-3)
10. **Compliance Officer (Technology):** closure decision.
   **Receiving condition:** Closure states remaining exceptions, authority and future review triggers
   **Output specifications:** [`compliance-officer-technology:2`](output-contracts/role-compliance-officer-technology.md#output-compliance-officer-technology-2)

[Roles, activities and acceptance gates for this chain](../workflow-library/regulatory-change-to-assurance.md#workflow-steps-and-gates).
<!-- JAI:OUTPUT-CONTRACTS:END -->
