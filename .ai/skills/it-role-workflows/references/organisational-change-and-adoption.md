# Organisational change and adoption

`workflow: organisational-change-and-adoption`  ·  `steps: 6`  ·  `tool-tier: route`

**Trigger.** Technology or process change requires people to work differently for the intended outcome to materialise.

**Outcome.** Affected cohorts are ready, adopt the new behaviour and produce evidence that supports the intended business benefit.

This chain is an enterprise hand-off model, not a rigid project schedule. Run steps in parallel where sensible, but do not skip the acceptance gate between accountable roles.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Business Relationship Manager](../../it-roles-service-management-and-support/references/business-relationship-manager.md) | anchors the change in a business outcome, sponsor and affected relationship context | business outcome and stakeholder context | There is a named sponsor and business outcome |
| 2 | [Organisational Change and Adoption Manager](../../it-roles-product-delivery-and-agile/references/organisational-change-and-adoption-manager.md) | assesses stakeholder impacts, readiness and adoption barriers | change impact assessment and adoption strategy | Every material cohort has impact, readiness and owner |
| 3 | [IT Trainer](../../it-roles-commercial-sourcing-and-enablement/references/it-trainer.md) | turns role impacts into role-based learning and performance support | training assets and proficiency checks | Training maps to changed tasks and has proficiency evidence |
| 4 | [Product Manager](../../it-roles-product-delivery-and-agile/references/product-manager.md) | coordinates release timing and product communications with adoption readiness | release/adoption alignment | No cohort is asked to adopt functionality unavailable or unstable in its wave |
| 5 | [Product Analyst](../../it-roles-analysis/references/product-analyst.md) | measures actual usage and behavioural outcomes | adoption observations and segmentation | Adoption is measured by behaviour/outcome, not attendance alone |
| 6 | [Benefits Realisation Manager](../../it-roles-product-delivery-and-agile/references/benefits-realisation-manager.md) | connects adoption evidence to benefit realisation and corrective decisions | benefit/adoption review | Below-target adoption or benefits have owned reinforcement or reforecast actions |

## Operating this chain

Read the linked role reference before acting as a step and use the operator agent declared for that role's tool tier. A hand-off is complete only when the receiving step applies the stated gate and accepts the evidence. Failed gates remain explicit; they are not converted into assumptions simply to preserve a milestone.

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
