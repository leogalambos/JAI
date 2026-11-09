# Organisational change and adoption

## Trigger

Technology or process change requires people to work differently for the intended outcome to materialise.

## Intended outcome

Affected cohorts are ready, adopt the new behaviour and produce evidence that supports the intended business benefit.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Affected cohorts are ready, adopt the new behaviour and produce evidence that supports the intended business benefit.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| single-cohort | Use task-specific readiness and proficiency checks | Cohort impact, training results and observed behaviour |
| multi-wave | Align each cohort with available stable capability and reinforcement | Wave dependencies, readiness gates and segmented adoption results |

Return low readiness/proficiency or unavailable capability to the adoption/product owner before the next wave. Stop forcing adoption of unavailable/unstable functionality or making unsupported realised-benefit claims. Close the wave with behavioural/outcome observations or reforecast benefits and assign reinforcement. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Business outcome and named sponsor
- Affected cohorts and changed tasks
- Release capability/stability and measurement baseline

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return low readiness/proficiency or unavailable capability to the adoption/product owner before the next wave.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop forcing adoption of unavailable/unstable functionality or making unsupported realised-benefit claims.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close the wave with behavioural/outcome observations or reforecast benefits and assign reinforcement.

**Bounded paths and scope:**

Single/multi-cohort cases share task readiness and observed behaviour; waves and denominators remain explicit.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| single-cohort | 1, 2, 3, 4, 5, 6 | 6 |
| multi-wave | 1, 2, 3, 4, 5, 6 | 6 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Organisational change and adoption workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Business Relationship Manager</strong><p>anchors the change in a business outcome, sponsor and affected relationship context</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Organisational Change and Adoption Manager</strong><p>assesses stakeholder impacts, readiness and adoption barriers</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>IT Trainer</strong><p>turns role impacts into role-based learning and performance support</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Product Manager</strong><p>coordinates release timing and product communications with adoption readiness</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Product Analyst</strong><p>measures actual usage and behavioural outcomes</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Benefits Realisation Manager</strong><p>connects adoption evidence to benefit realisation and corrective decisions</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-organisational-change-and-adoption.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Business Relationship Manager | anchors the change in a business outcome, sponsor and affected relationship context | business outcome and stakeholder context | There is a named sponsor and business outcome |
| 2 | Organisational Change and Adoption Manager | assesses stakeholder impacts, readiness and adoption barriers | change impact assessment and adoption strategy | Every material cohort has impact, readiness and owner |
| 3 | IT Trainer | turns role impacts into role-based learning and performance support | training assets and proficiency checks | Training maps to changed tasks and has proficiency evidence |
| 4 | Product Manager | coordinates release timing and product communications with adoption readiness | release/adoption alignment | No cohort is asked to adopt functionality unavailable or unstable in its wave |
| 5 | Product Analyst | measures actual usage and behavioural outcomes | adoption observations and segmentation | Adoption is measured by behaviour/outcome, not attendance alone |
| 6 | Benefits Realisation Manager | connects adoption evidence to benefit realisation and corrective decisions | benefit/adoption review | Below-target adoption or benefits have owned reinforcement or reforecast actions |

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

> Apply the `organisational-change-and-adoption` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
