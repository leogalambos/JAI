# DAST integration and control assurance for containerised delivery

## When to use this workflow

An existing containerised CI/CD pipeline needs a DAST control introduced, qualified, reassessed or evaluated for release.

## Intended outcome

An implemented and qualified DAST integration with operational takeover, or a bounded qualification, release evidence or continuous assurance decision.

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

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="DAST integration and control assurance for containerised delivery workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Solution Architect</strong><p>Assess the mandate, readiness and independently sourced interface inventory. Compare combined runtime, separate containers, representative stacks, remote service and shared network namespace against the required perspectives.</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Security Architect</strong><p>Map risk and policy to measurable requirements, test perspectives, identities, environment fidelity, compensating controls and gate criteria. Review the control trust model and protected release path.</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Control Owner</strong><p>Consolidate supplied implementation and qualification evidence from application, CI/CD, IAM, infrastructure, scanner platform, QA and release platform owners. Assess approved image provenance, isolation, evidence integrity, negative gate results and operational readiness.</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Internal IT Auditor</strong><p>Independently assess exact versions of the requirements, design, qualification dossier and operational readiness. Identify unsupported claims and blocking findings.</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Named authority</strong><p>Record the named human security acceptance of the independently reviewed control. Reference separate risk and policy decisions for permitted exceptions.</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Control Owner</strong><p>Assess supplied evidence for the exact release candidate against the accepted qualification, policy and required scenarios. Preserve findings from incomplete runs and distinguish validity from compliance.</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Named authority</strong><p>Record the protected gate decision and verify the exact human release decision and any separately authorised exceptions. Preserve original technical findings and validity.</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Control Owner</strong><p>Review supplied operating evidence for drift, scoped coverage, invalid or missing runs, unresolved findings, exceptions and cleanup. Identify the required requalification scope and ownership.</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>Named authority</strong><p>Record the application owner mandate, delivery owner, resources, applicable policies and exact project and pipeline scope.</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Solution Architect</strong><p>Compare deployment options and confirm a feasible design for the existing pipeline. Obtain the security architect’s design disposition of trust boundaries, scope and environment differences.</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>Software Engineer</strong><p>Implement approved application testability changes for startup, readiness, API contracts and isolated test data. Record an evidence-backed no-change disposition where existing behaviour suffices.</p></div></li>
<li data-step="12"><span class="ai-workflow-step-number" aria-hidden="true">12</span><div><strong>Network Engineer</strong><p>Implement the approved test environment network boundaries and verify isolation, lifecycle and capacity with non-offensive connectivity checks.</p></div></li>
<li data-step="13"><span class="ai-workflow-step-number" aria-hidden="true">13</span><div><strong>Identity and Access Management Engineer</strong><p>Implement scoped test identities, protected secret delivery and revocation under the approved test environment design.</p></div></li>
<li data-step="14"><span class="ai-workflow-step-number" aria-hidden="true">14</span><div><strong>Container Platform Engineer</strong><p>Establish the approved scanner platform artifact and lifecycle. Verify provenance, digest, dependencies, bounded privileges and update ownership.</p></div></li>
<li data-step="15"><span class="ai-workflow-step-number" aria-hidden="true">15</span><div><strong>Control Owner</strong><p>Obtain the approved scanner profile reference from the responsible AppSec team and specify the evidence interface, required contexts, scope coverage and validity criteria for supplied reports.</p></div></li>
<li data-step="16"><span class="ai-workflow-step-number" aria-hidden="true">16</span><div><strong>CI/CD Platform Engineer</strong><p>Implement candidate identity, deployment readiness, protected intake of supplied DAST reports, cleanup and failure handling in the existing pipeline. Validate the integration with synthetic reports.</p></div></li>
<li data-step="17"><span class="ai-workflow-step-number" aria-hidden="true">17</span><div><strong>Release Engineer</strong><p>Implement the protected release decision interface and fail-closed policy checks on the evidence manifest. Exercise missing, stale, mismatched and unauthorised evidence with synthetic fixtures.</p></div></li>
<li data-step="18"><span class="ai-workflow-step-number" aria-hidden="true">18</span><div><strong>Test Manager</strong><p>Independently verify the integration against the qualification plan. Consolidate technical test results and externally supplied AppSec qualification evidence into a traceable verdict.</p></div></li>
<li data-step="19"><span class="ai-workflow-step-number" aria-hidden="true">19</span><div><strong>Named authority</strong><p>Record the application owner operational takeover after security acceptance and identify the delivery owner closing the integration.</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-dast-control-assurance.svg). Use the applicable path table for the sequence, including variant-only stages.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Read the methodology for the current stage

Use the selected path, current stage and exact input revisions. Load the
referenced sections before performing the activity or assessing its handoff.
Carry accepted requirements and previous decisions by reference.

| Stage | Required sections |
| --- | --- |
| 9 · Mandate | [Decision rights](../reference/dast-methodology.md#accountability-and-decision-rights) and [A0](../reference/dast-methodology.md#implementation-lifecycle) |
| 1–2 · Readiness and requirements | [Lifecycle](../reference/dast-methodology.md#implementation-lifecycle), [requirements SR-01–SR-28](../reference/dast-methodology.md#security-requirements-catalogue) and [coverage](../reference/dast-methodology.md#qualification-and-coverage) |
| 10 · Feasibility and design | [Deployment patterns and fidelity](../reference/dast-methodology.md#deployment-patterns-and-fidelity) and [qualification](../reference/dast-methodology.md#qualification-and-coverage) |
| 11–17 · Implementation | [Workstreams](../reference/dast-methodology.md#implementation-lifecycle), [execution and evidence](../reference/dast-methodology.md#recurring-execution-and-evidence-handoff) and [gate](../reference/dast-methodology.md#output-security-gate-and-exceptions) |
| 18, 3–5 · Qualification and acceptance | [Criteria AC-01–AC-12 and qualification cases](../reference/dast-methodology.md#qualification-and-coverage), [decision rights](../reference/dast-methodology.md#accountability-and-decision-rights) and [completion](../reference/dast-methodology.md#example-and-completion) |
| 19 · Operational takeover | [A7](../reference/dast-methodology.md#implementation-lifecycle) and [operating assurance](../reference/dast-methodology.md#remediation-and-operating-assurance) |
| 6–7 · Release evidence and decision | [Execution and evidence](../reference/dast-methodology.md#recurring-execution-and-evidence-handoff) and [gate and exceptions](../reference/dast-methodology.md#output-security-gate-and-exceptions) |
| 8 · Continuous assurance | [Remediation, metrics and requalification](../reference/dast-methodology.md#remediation-and-operating-assurance) |

## Workflow steps and gates

| Step | Accountable role | Activity | Versioned handoff | Acceptance gate |
| ---: | --- | --- | --- | --- |
| 1 | Solution Architect | Assess the mandate, readiness and independently sourced interface inventory. Compare combined runtime, separate containers, representative stacks, remote service and shared network namespace against the required perspectives. | readiness and deployment decision | The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations. |
| 2 | Security Architect | Map risk and policy to measurable requirements, test perspectives, identities, environment fidelity, compensating controls and gate criteria. Review the control trust model and protected release path. | security architecture and traceability baseline | Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition. |
| 3 | Control Owner | Consolidate supplied implementation and qualification evidence from application, CI/CD, IAM, infrastructure, scanner platform, QA and release platform owners. Assess approved image provenance, isolation, evidence integrity, negative gate results and operational readiness. | control qualification dossier | The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible. |
| 4 | Internal IT Auditor | Independently assess exact versions of the requirements, design, qualification dossier and operational readiness. Identify unsupported claims and blocking findings. | independent security assessment | The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations. |
| 5 | Named authority | Record the named human security acceptance of the independently reviewed control. Reference separate risk and policy decisions for permitted exceptions. | formal security acceptance record | The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance. |
| 6 | Control Owner | Assess supplied evidence for the exact release candidate against the accepted qualification, policy and required scenarios. Preserve findings from incomplete runs and distinguish validity from compliance. | release evidence assessment | Evidence must bind the observed deployment, approved profile, identity, run and policy to the exact candidate. Missing, stale, out-of-scope or untrusted evidence cannot support ordinary promotion. |
| 7 | Named authority | Record the protected gate decision and verify the exact human release decision and any separately authorised exceptions. Preserve original technical findings and validity. | DAST gate and release authority record | Untrusted evidence and non-waivable failures block. Any permitted exception is exact, current and sufficient. Promotion requires the verified release decision and all mandatory controls. |
| 8 | Control Owner | Review supplied operating evidence for drift, scoped coverage, invalid or missing runs, unresolved findings, exceptions and cleanup. Identify the required requalification scope and ownership. | continuous assurance disposition | Material changes invalidate affected evidence where required and return impacted scope to qualification. Follow-up has accountable owners and review dates. |
| 9 | Named authority | Record the application owner mandate, delivery owner, resources, applicable policies and exact project and pipeline scope. | integration mandate | A named application owner authorises the bounded change. Policy, scope, risk ownership and available resources are explicit. |
| 10 | Solution Architect | Compare deployment options and confirm a feasible design for the existing pipeline. Obtain the security architect’s design disposition of trust boundaries, scope and environment differences. | reviewed integration design and implementation backlog | The design binds readiness and requirements to a deployment decision, representative test environment, specific implementation changes and qualification plan. Critical uncertainties have observed feasibility evidence. |
| 11 | Software Engineer | Implement approved application testability changes for startup, readiness, API contracts and isolated test data. Record an evidence-backed no-change disposition where existing behaviour suffices. | reviewed application changes | Application revision and tests are recorded. Release authentication and authorisation remain effective and test fixtures are isolated. |
| 12 | Network Engineer | Implement the approved test environment network boundaries and verify isolation, lifecycle and capacity with non-offensive connectivity checks. | isolated environment evidence | The environment revision identifies approved connectivity, blocked destinations, resource limits, concurrency isolation and teardown results. |
| 13 | Identity and Access Management Engineer | Implement scoped test identities, protected secret delivery and revocation under the approved test environment design. | test identity lifecycle evidence | Required identities and roles are scoped, credential material stays out of records, and issue, expiry and revocation have observed evidence. |
| 14 | Container Platform Engineer | Establish the approved scanner platform artifact and lifecycle. Verify provenance, digest, dependencies, bounded privileges and update ownership. | approved scanner platform baseline | The recorded platform is reproducible and isolated. Its immutable identity and lifecycle ownership are explicit. |
| 15 | Control Owner | Obtain the approved scanner profile reference from the responsible AppSec team and specify the evidence interface, required contexts, scope coverage and validity criteria for supplied reports. | control profile and evidence interface baseline | Approved profile and scope revisions are traceable to mandatory scenarios, qualified measurement and complementary controls. Missing coverage has an explicit disposition. |
| 16 | CI/CD Platform Engineer | Implement candidate identity, deployment readiness, protected intake of supplied DAST reports, cleanup and failure handling in the existing pipeline. Validate the integration with synthetic reports. | reviewed pipeline evidence integration | Versioned pipeline changes bind evidence to the actual candidate and observed deployment. Synthetic tests demonstrate error handling, cleanup and tamper rejection. The intake is tested against the exact environment, identity, platform and control interface revisions. |
| 17 | Release Engineer | Implement the protected release decision interface and fail-closed policy checks on the evidence manifest. Exercise missing, stale, mismatched and unauthorised evidence with synthetic fixtures. | protected release gate implementation | The gate evidence shows exact candidate binding, blocked promotion for failed prerequisites, validated exceptions and separate release authority. |
| 18 | Test Manager | Independently verify the integration against the qualification plan. Consolidate technical test results and externally supplied AppSec qualification evidence into a traceable verdict. | system and negative integration qualification | Every applicable workstream has completion evidence and applicable requirements trace to tests. Unresolved integration failures block acceptance. |
| 19 | Named authority | Record the application owner operational takeover after security acceptance and identify the delivery owner closing the integration. | operational takeover decision and lifecycle handoff | The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers. |

## Running this workflow: operator and implementer boundary

> Use `dast-control-assurance`, path `integration`, for this existing CI/CD pipeline. Inspect the attached application and pipeline revisions, mandate, policy and architecture. Identify the current stage, accountable owner, versioned handoff and blockers.

Use `release-evidence` with an accepted qualification and a candidate manifest. Use
`continuous-assurance` with a qualification reference, review period and actual
operating observations. For a consequential engagement, use
[`/layered` or `$workflow-layered`](../using/workflows.md#operator-interaction-versus-workflow-execution)
with the intended path and exact evidence references. The integration path implements defensive pipeline components and qualifies them with synthetic reports. The responsible AppSec team supplies approved scanner profile references and actual DAST qualification evidence.

## Evidence to prepare

- **Qualification.** Bring the application mandate, inventory from sources
  independent of scanner discovery, deployment decision, requirements traceability
  and risk-based qualification criteria. Identify each mandatory scenario by
  interface, identity, application state and network perspective. Document
  compensating controls and assess differences in IAM, gateway, TLS and other
  security-relevant behaviour. Bring observed qualification results for
  identity and session, evidence binding, isolation, concurrency, failure
  cleanup and protected promotion. Review complementary tests for scenarios
  outside DAST coverage. Keep coverage, detection assurance and findings distinct.
- **Release evidence.** Bring the manifest and observed deployment identity,
  authorised runner and run identifiers, scanner and profile revisions,
  validity and coverage evidence, retained findings, evidence integrity and
  the policy revision. Assess required contexts against an independently
  versioned denominator. Treat an empty denominator as not applicable with
  justification. Missing or invalid evidence leaves compliance unknown.
  Preserve known findings even when the run is incomplete.
- **Continuous assurance.** Bring actual valid-run rates (including missing
  runs in the denominator), scoped coverage, session and detection degradation,
  remediation and exception status, provenance failures and cleanup results.
  Check changes to application surface, IAM, deployment, scanner, profile,
  policy and runner permissions for impact on qualification. Return affected
  scope to qualification and carry forward compatible evidence.

## Decision boundaries

A valid and compliant run can support `ALLOW` under the DAST policy. An
authorised, exact, current exception may support `ALLOW_WITH_EXCEPTION` where
policy permits. Each affected requirement or finding must be covered.
Otherwise the gate records `BLOCK`. Untrusted evidence and non-waivable
requirements block promotion. Policy alone determines whether the control is
`NOT_REQUIRED`. False-positive disposition, risk acceptance and control
exception have distinct evidence and decision owners. A gate result cannot
authorise release on its own.

The assigned security acceptance authority and application owner decide
qualification and operational takeover. Security governance and the risk owner
decide applicable exceptions within their respective mandates. The release
authority decides promotion for the exact candidate. Hand confirmed findings
to [vulnerability remediation](vulnerability-to-remediation.md).

The handoff checker validates versioned evidence fields, registered paths
and signed authority for the exact handoff. The reviewer and human authorities
must confirm that the referenced prerequisite dossiers and release evidence
are current and compatible. A populated reference field alone does not
establish a verified chain of custody.

See the [versioned handoff requirements](../reference/output-contracts/workflow-dast-control-assurance.md).

## Introduce DAST into an existing project

Start with the existing application, pipeline revision, deployment definitions
and the application owner's mandate. In `integration`, step 9 establishes
authority, steps 1–2 assess readiness and fix security criteria, and step 10
turns them into a reviewed deployment decision and implementation backlog.

Steps 11–17 register separate outputs for application testability, network
isolation, IAM, scanner platform, the approved control interface, pipeline
evidence integration and protected enforcement. Owners may work concurrently
where dependencies permit. The pipeline integration consumes the approved
environment, identity, platform and evidence interface versions. The protected
gate consumes the pipeline evidence revision. Step 18 joins the workstreams
and requires observed tests or a justified no-change disposition for each
applicable component. Use recorded scanner reports and synthetic fixtures to
exercise evidence ingestion, validity handling, failure cleanup and promotion
blocking. The AppSec team supplies the corresponding real qualification evidence.

Steps 3–5 consolidate the qualification, independently assess the exact
outputs and record security acceptance. Step 19 records separate operational
takeover. Use `qualification` when implementation outputs already exist,
`release-evidence` for the exact candidate and `continuous-assurance` for
operating evidence and material changes. Re-enter the affected integration
stages when scope, architecture or policy changes materially.

Assign separate principals to evidence intake, promotion enforcement and
independent review. Review the exact mandate and design before workstream
implementation, and confirm that the accepted qualification and takeover refer
to the same application and scope. The handoff validator checks required
records and exact authority for the current boundary. Reviewers and human
owners verify the actual predecessor records.
