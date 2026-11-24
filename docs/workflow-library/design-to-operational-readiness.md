# Design to operational readiness

## Trigger

A solution design is becoming build/release ready and must prove it can be operated safely before go-live.

## Intended outcome

The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- The receiving service organisation explicitly accepts an evidenced, supportable and recoverable service.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| new-service | Establish complete receiving operations evidence | Runbooks, monitoring, access, recovery and support rehearsal |
| existing-service-delta | Assess affected readiness and dependencies while reusing unchanged approved evidence | Exact design delta, impact and current evidence references |
| zero-trust-migration | Existing hybrid network transition | Versioned inventory, observed dependencies, policy and independently measured reversal evidence. |
| zero-trust-greenfield | Requirements-led Zero Trust design | Attributable requirements, candidate enforcement design and independent verification of design coverage. |
| zero-trust-assessment | Independent existing Zero Trust or hybrid estate assessment | Commissioned scope, actual control observations, evidence gaps and prioritized remediation. |
| terraform-readiness | Terraform implementation and promotion readiness | Versioned configuration, state topology, reviewed immutable plan and bounded recovery evidence. |
| aws-greenfield | AWS infrastructure greenfield | Validate the organization, organizational unit, account and Region against requirements and placement constraints and record independent receiving evidence. |
| aws-migration | AWS infrastructure migration | Validate the organization, organizational unit, account and Region against on-premises inventory, dependency observations and migration constraints and record independent receiving evidence. |
| aws-assessment | AWS infrastructure assessment | Validate the organization, organizational unit, account and Region against independent commission, exact current inventory and evidence coverage and record independent receiving evidence. |
| azure-greenfield | Microsoft Azure infrastructure greenfield | Validate the tenant, management group, subscription and region against requirements and placement constraints and record independent receiving evidence. |
| azure-migration | Microsoft Azure infrastructure migration | Validate the tenant, management group, subscription and region against on-premises inventory, dependency observations and migration constraints and record independent receiving evidence. |
| azure-assessment | Microsoft Azure infrastructure assessment | Validate the tenant, management group, subscription and region against independent commission, exact current inventory and evidence coverage and record independent receiving evidence. |
| google-cloud-greenfield | Google Cloud infrastructure greenfield | Validate the organization, folder, project and location against requirements and placement constraints and record independent receiving evidence. |
| google-cloud-migration | Google Cloud infrastructure migration | Validate the organization, folder, project and location against on-premises inventory, dependency observations and migration constraints and record independent receiving evidence. |
| google-cloud-assessment | Google Cloud infrastructure assessment | Validate the organization, folder, project and location against independent commission, exact current inventory and evidence coverage and record independent receiving evidence. |

Return failed readiness criteria to the accountable design/platform/support owner before the change decision. Stop go-live for unowned critical readiness gaps or absent required change authority. Accept operational responsibility with explicit residual risks or defer activation with owned remediation. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Versioned solution and measurable quality requirements
- Receiving service owner and support model
- Risk, resilience and readiness criteria

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed readiness criteria to the accountable design/platform/support owner before the change decision.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop go-live for unowned critical readiness gaps or absent required change authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Accept operational responsibility with explicit residual risks or defer activation with owned remediation.

**Bounded paths and scope:**

New-service and changed-service readiness share evidence types; unchanged valid platform evidence is referenced rather than re-executed.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| new-service | 1, 2, 3, 4, 5, 6, 7 | 7 |
| existing-service-delta | 1, 2, 3, 4, 5, 6, 7 | 7 |
| zero-trust-migration | 1, 2, 3, 4, 5, 6, 7 | 7 |
| zero-trust-greenfield | 1, 2, 3 | 3 |
| zero-trust-assessment | 1, 2, 3 | 3 |
| terraform-readiness | 1, 2, 3 | 3 |
| aws-greenfield | 1, 2, 3, 4 | 4 |
| aws-migration | 1, 2, 3, 4 | 4 |
| aws-assessment | 1, 2, 3 | 3 |
| azure-greenfield | 1, 2, 3, 4 | 4 |
| azure-migration | 1, 2, 3, 4 | 4 |
| azure-assessment | 1, 2, 3 | 3 |
| google-cloud-greenfield | 1, 2, 3, 4 | 4 |
| google-cloud-migration | 1, 2, 3, 4 | 4 |
| google-cloud-assessment | 1, 2, 3 | 3 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Design to operational readiness workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Solution Architect</strong><p>defines the target architecture, NFRs, dependencies and failure modes</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Security Architect</strong><p>defines security controls and residual security risks</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Operational and Technology Resilience Architect</strong><p>tests the design against failure domains, impact tolerances and recovery paths</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Site Reliability Engineer</strong><p>defines SLOs, observability, alerting and operability signals</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Service Transition and Operational Readiness Manager</strong><p>assembles and assesses operational acceptance evidence</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Change Manager</strong><p>checks the production change path and risk-class approval</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>IT Service Owner</strong><p>accepts service ownership and residual operational risk</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-design-to-operational-readiness.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Solution Architect | defines the target architecture, NFRs, dependencies and failure modes | solution architecture and decision records | Quality attributes and failure modes are explicit and testable |
| 2 | Security Architect | defines security controls and residual security risks | security architecture and control requirements | Controls trace to risks and objectives |
| 3 | Operational and Technology Resilience Architect | tests the design against failure domains, impact tolerances and recovery paths | resilience architecture and validation scenarios | Resilience claims identify dependencies, failure domains and validation method |
| 4 | Site Reliability Engineer | defines SLOs, observability, alerting and operability signals | SLO/monitoring design and runbook requirements | Alerts are actionable and every SLO has a data source |
| 5 | Service Transition and Operational Readiness Manager | assembles and assesses operational acceptance evidence | operational readiness assessment and evidence pack | Every readiness criterion is pass/fail/waived with evidence and owner |
| 6 | Change Manager | checks the production change path and risk-class approval | change authorisation decision | Change risk and readiness evidence match the approval route |
| 7 | IT Service Owner | accepts service ownership and residual operational risk | service acceptance | Support ownership, SLOs and residual risks are explicitly accepted |

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

> Apply the `design-to-operational-readiness` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.

## Zero Trust and cloud readiness

Use `zero-trust-migration` for an existing network. Record the versioned
estate, observed dependencies and required flow tests before design. Carry
the baseline through target design and the transition candidate. Rehearse the
required access decisions, coexistence, continuity and reversal before
receiving readiness. Record exception ownership and expiry. Advance actual
rollout through production change with its applicable authority.

Use `zero-trust-greenfield` for an attributable set of requirements and an
independent design assessment. Use `zero-trust-assessment` for an independently
commissioned review of an existing Zero Trust or hybrid estate. Keep
observations, evidence gaps and remediation disposition distinct.

The `terraform-readiness` path binds the saved plan digest to its target,
environment, source version, toolchain and state identity. Protect the saved
plan and state as sensitive. Replan after relevant drift or an input change.
Identify the selected Terraform or OpenTofu edition and licensing separately.

The `aws-*`, `azure-*` and `google-cloud-*` variants distinguish
`greenfield`, `migration` and `assessment`. Pin the exact hierarchy,
placement, identity, connectivity, policy, logging, data residency, recovery
and operating model. For migration, capture the on-premises dependencies and
continuity requirements. For assessment, compare intended controls with
observed evidence under an independent receiving duty.

- [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [CISA Zero Trust Maturity Model](https://www.cisa.gov/resources-tools/resources/zero-trust-maturity-model)
- [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)
- [OpenTofu documentation](https://opentofu.org/docs/intro/)

For migration, the baseline's `verification_scope` includes the exact
`allowed_flow_ids`, `denied_flow_ids`, `dependency_ids` and
`reversal_limit_seconds`. Carry this record through design, candidate and
observations. The observations identify each required flow and dependency
and cite a versioned evidence record for each result. The readiness receiver
checks completeness and restoration within the approved limit.
