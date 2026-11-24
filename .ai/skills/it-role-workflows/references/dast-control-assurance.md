# DAST integration and control assurance for containerised delivery

## When to use this workflow

An existing containerised CI/CD pipeline needs a DAST control introduced, qualified, reassessed or evaluated for release.

## Intended outcome

An implemented and qualified DAST integration with operational takeover, or a bounded qualification, release evidence or continuous assurance decision.

## Read the methodology for the current stage

Use the selected path, current stage and exact input revisions. Load the
referenced sections before performing the activity or assessing its handoff.
Carry accepted requirements and previous decisions by reference.

| Stage | Required sections |
| --- | --- |
| 9 · Mandate | [Decision rights](dast-methodology.md#accountability-and-decision-rights) and [A0](dast-methodology.md#implementation-lifecycle) |
| 1–2 · Readiness and requirements | [Lifecycle](dast-methodology.md#implementation-lifecycle), [requirements SR-01–SR-28](dast-methodology.md#security-requirements-catalogue) and [coverage](dast-methodology.md#qualification-and-coverage) |
| 10 · Feasibility and design | [Deployment patterns and fidelity](dast-methodology.md#deployment-patterns-and-fidelity) and [qualification](dast-methodology.md#qualification-and-coverage) |
| 11–17 · Implementation | [Workstreams](dast-methodology.md#implementation-lifecycle), [execution and evidence](dast-methodology.md#recurring-execution-and-evidence-handoff) and [gate](dast-methodology.md#output-security-gate-and-exceptions) |
| 18, 3–5 · Qualification and acceptance | [Criteria AC-01–AC-12 and qualification cases](dast-methodology.md#qualification-and-coverage), [decision rights](dast-methodology.md#accountability-and-decision-rights) and [completion](dast-methodology.md#example-and-completion) |
| 19 · Operational takeover | [A7](dast-methodology.md#implementation-lifecycle) and [operating assurance](dast-methodology.md#remediation-and-operating-assurance) |
| 6–7 · Release evidence and decision | [Execution and evidence](dast-methodology.md#recurring-execution-and-evidence-handoff) and [gate and exceptions](dast-methodology.md#output-security-gate-and-exceptions) |
| 8 · Continuous assurance | [Remediation, metrics and requalification](dast-methodology.md#remediation-and-operating-assurance) |

## Workflow steps and gates

| Step | Accountable role | Activity | Versioned handoff | Acceptance gate |
| ---: | --- | --- | --- | --- |
| 1 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | Assess the mandate, readiness and independently sourced interface inventory. Compare combined runtime, separate containers, representative stacks, remote service and shared network namespace against the required perspectives. | readiness and deployment decision | The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations. |
| 2 | [Security Architect](../../it-roles-architecture/references/security-architect.md) | Map risk and policy to measurable requirements, test perspectives, identities, environment fidelity, compensating controls and gate criteria. Review the control trust model and protected release path. | security architecture and traceability baseline | Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition. |
| 3 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | Consolidate supplied implementation and qualification evidence from application, CI/CD, IAM, infrastructure, scanner platform, QA and release platform owners. Assess approved image provenance, isolation, evidence integrity, negative gate results and operational readiness. | control qualification dossier | The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible. |
| 4 | [Internal IT Auditor](../../it-roles-governance-risk-compliance-audit-and-privacy/references/internal-it-auditor.md) | Independently assess exact versions of the requirements, design, qualification dossier and operational readiness. Identify unsupported claims and blocking findings. | independent security assessment | The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations. |
| 5 | Named authority | Record the named human security acceptance of the independently reviewed control. Reference separate risk and policy decisions for permitted exceptions. | formal security acceptance record | The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance. |
| 6 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | Assess supplied evidence for the exact release candidate against the accepted qualification, policy and required scenarios. Preserve findings from incomplete runs and distinguish validity from compliance. | release evidence assessment | Evidence must bind the observed deployment, approved profile, identity, run and policy to the exact candidate. Missing, stale, out-of-scope or untrusted evidence cannot support ordinary promotion. |
| 7 | Named authority | Record the protected gate decision and verify the exact human release decision and any separately authorised exceptions. Preserve original technical findings and validity. | DAST gate and release authority record | Untrusted evidence and non-waivable failures block. Any permitted exception is exact, current and sufficient. Promotion requires the verified release decision and all mandatory controls. |
| 8 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | Review supplied operating evidence for drift, scoped coverage, invalid or missing runs, unresolved findings, exceptions and cleanup. Identify the required requalification scope and ownership. | continuous assurance disposition | Material changes invalidate affected evidence where required and return impacted scope to qualification. Follow-up has accountable owners and review dates. |
| 9 | Named authority | Record the application owner mandate, delivery owner, resources, applicable policies and exact project and pipeline scope. | integration mandate | A named application owner authorises the bounded change. Policy, scope, risk ownership and available resources are explicit. |
| 10 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | Compare deployment options and confirm a feasible design for the existing pipeline. Obtain the security architect’s design disposition of trust boundaries, scope and environment differences. | reviewed integration design and implementation backlog | The design binds readiness and requirements to a deployment decision, representative test environment, specific implementation changes and qualification plan. Critical uncertainties have observed feasibility evidence. |
| 11 | [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | Implement approved application testability changes for startup, readiness, API contracts and isolated test data. Record an evidence-backed no-change disposition where existing behaviour suffices. | reviewed application changes | Application revision and tests are recorded. Release authentication and authorisation remain effective and test fixtures are isolated. |
| 12 | [Network Engineer](../../it-roles-network-and-telecommunications/references/network-engineer.md) | Implement the approved test environment network boundaries and verify isolation, lifecycle and capacity with non-offensive connectivity checks. | isolated environment evidence | The environment revision identifies approved connectivity, blocked destinations, resource limits, concurrency isolation and teardown results. |
| 13 | [Identity and Access Management Engineer](../../it-roles-security-operations-and-defensive-security/references/identity-and-access-management-engineer.md) | Implement scoped test identities, protected secret delivery and revocation under the approved test environment design. | test identity lifecycle evidence | Required identities and roles are scoped, credential material stays out of records, and issue, expiry and revocation have observed evidence. |
| 14 | [Container Platform Engineer](../../it-roles-infrastructure-cloud-and-operations/references/container-platform-engineer.md) | Establish the approved scanner platform artifact and lifecycle. Verify provenance, digest, dependencies, bounded privileges and update ownership. | approved scanner platform baseline | The recorded platform is reproducible and isolated. Its immutable identity and lifecycle ownership are explicit. |
| 15 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | Obtain the approved scanner profile reference from the responsible AppSec team and specify the evidence interface, required contexts, scope coverage and validity criteria for supplied reports. | control profile and evidence interface baseline | Approved profile and scope revisions are traceable to mandatory scenarios, qualified measurement and complementary controls. Missing coverage has an explicit disposition. |
| 16 | [CI/CD Platform Engineer](../../it-roles-software-development-and-engineering/references/ci-cd-platform-engineer.md) | Implement candidate identity, deployment readiness, protected intake of supplied DAST reports, cleanup and failure handling in the existing pipeline. Validate the integration with synthetic reports. | reviewed pipeline evidence integration | Versioned pipeline changes bind evidence to the actual candidate and observed deployment. Synthetic tests demonstrate error handling, cleanup and tamper rejection. The intake is tested against the exact environment, identity, platform and control interface revisions. |
| 17 | [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | Implement the protected release decision interface and fail-closed policy checks on the evidence manifest. Exercise missing, stale, mismatched and unauthorised evidence with synthetic fixtures. | protected release gate implementation | The gate evidence shows exact candidate binding, blocked promotion for failed prerequisites, validated exceptions and separate release authority. |
| 18 | [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | Independently verify the integration against the qualification plan. Consolidate technical test results and externally supplied AppSec qualification evidence into a traceable verdict. | system and negative integration qualification | Every applicable workstream has completion evidence and applicable requirements trace to tests. Unresolved integration failures block acceptance. |
| 19 | Named authority | Record the application owner operational takeover after security acceptance and identify the delivery owner closing the integration. | operational takeover decision and lifecycle handoff | The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers. |

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- An implemented and qualified DAST integration with operational takeover, or a bounded qualification, release evidence or continuous assurance decision.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| integration | Introduce DAST into an existing project pipeline | Approved mandate, implemented workstreams, qualification evidence and operational takeover |
| qualification | Qualify initial or materially changed DAST control scope | Application mandate, source architecture, qualification dossier, independent review and human acceptance |
| release-evidence | Assess evidence for a specific candidate under a current qualification | Accepted qualification, exact candidate, collected evidence, protected gate and exact release decision |
| continuous-assurance | Assess operating results and material changes | Accepted qualification, operating observations, measured degradation, owned actions and requalification scope |

Return failed criteria to the accountable stage and preserve valid evidence for unaffected scope. Block on absent or incompatible prerequisites, untrusted evidence, or missing required authority. Use only supplied scan evidence. Record the bounded decision and route material changes to qualification and confirmed findings to vulnerability remediation. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Exact application and control scope, decision owner and applicable policy
- Versioned input bundle for the selected path

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed criteria to the accountable stage and preserve valid evidence for unaffected scope.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Block on absent or incompatible prerequisites, untrusted evidence, or missing required authority. Use only supplied scan evidence.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Record the bounded decision and route material changes to qualification and confirmed findings to vulnerability remediation.

**Bounded paths and scope:**

Choose integration to introduce DAST into an existing pipeline, qualification for an already implemented control, release-evidence for an exact candidate within accepted scope, and continuous-assurance for operating review. Reconcile scope and exact versions before carrying evidence across paths.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| integration | 9, 1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 3, 4, 5, 19 | 19 |
| qualification | 1, 2, 3, 4, 5, 19 | 19 |
| release-evidence | 6, 7 | 7 |
| continuous-assurance | 8 | 8 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

## Evidence by path

- **Qualification (1–5, 19).** Supply the application mandate, policy, source
  architecture and independently derived interface inventory. Retain
  risk-to-evidence traceability, expected identities and network perspectives,
  environment fidelity, qualification observations, protected gate evidence,
  and open gaps. Independently assess the exact dossier before human security
  acceptance and operational takeover.
- **Release evidence (6–7).** Supply the accepted qualification and the exact
  candidate manifest, deployment, run, approved profile and policy. Assess all
  mandatory contexts and evidence integrity. Preserve incomplete-run findings
  and separate validity, compliance, gate and release decisions. Check every
  exception for policy permission, completeness, exact scope and expiry.
- **Continuous assurance (8).** Supply qualified scope, actual operating
  observations and the review period. Assess validity and coverage trends,
  missing runs, drift, remediation and exceptions. Define owned actions and
  return materially changed scope to qualification.

Use only supplied evidence. Keep explicit dispositions for absent exceptions,
findings and material changes where the handoff requires those fields. Require
the versioned reviewed handoff in each acceptance decision. Human authorities
supply the actual decisions for qualification and release, within their
distinct mandates.

### Integration path

Start at the signed application mandate (9), assess the existing pipeline
and application (1–2), then obtain a reviewed design and backlog (10).
Assign each workstream in 11–17 to its registered owner. Respect the dependency
between the approved environment, identities, platform, control interface,
evidence pipeline and protected release gate. Use supplied AppSec reports and
synthetic integration fixtures. At 18, require exact workstream revisions and
positive and negative observations, then proceed to consolidation, independent
review and formal security acceptance (3–5). The application owner separately
records operational takeover (19). Return failed criteria to their owning
workstreams and repeat affected qualification only.
