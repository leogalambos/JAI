<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/runbook

**Specification:** `kind/runbook`; **content version:** `1.2.0`.

Determine whether an authorised operator can safely execute the recovery procedure.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/runbook`](spec-type-runbook.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `operational-procedure`.

Executable-by-operator procedure with prerequisites, exact targets, expected observations and recovery branches.

**Evidence accompanying the work product:**

- versioned verification checkpoints
- rehearsal environment/results or explicit untested scope

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`runbook.operational_trigger`** — `object`

- State the trigger, permitted operators, service boundary and stop conditions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`runbook.prerequisites`** — `array`

- Identify access permissions, tools, versions, dependencies and safety checks without embedding secrets.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`runbook.procedure_steps`** — `array`

- Give ordered actions, exact targets, expected outputs and verification at each critical step.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`runbook.failure_recovery`** — `object`

- Specify failure detection, rollback, safe state and conditions requiring escalation.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`runbook.operational_validation`** — `object`

- Record last rehearsal environment, evidence, owner and next review trigger.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`runbook.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`runbook.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`runbook.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`runbook.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`runbook.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`runbook.duplicate_claim`** — `object`

- Reference an existing claim instead of repeating it without new analytical value.

### Proportionate scope

Inherited size guidance is reproduced below. It is not evidence of substantive completeness; verbosity is not a quality measure.

```json
{
  "semantic_units": {
    "metric": "semantic_units",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ]
  },
  "pages": {
    "metric": "pages",
    "calibration_basis": "Modality-specific information coverage; numerical envelopes require approved enterprise calibration.",
    "minimum_is_quality_gate": false,
    "calibration_status": "synthetic-only",
    "allowance_rules": [
      "Document complexity and audience need; excess requires review, not automatic rejection."
    ],
    "annex_rules": [
      "Reference canonical detail rather than repeat it."
    ],
    "target": [
      2,
      10
    ],
    "soft_max": 14,
    "basis": "Indicative pilot intervals from approved implementation direction; assurance and handover use proposed evidence-pack intervals requiring calibration.",
    "exclude": [
      "controlled_annexes",
      "source_register"
    ],
    "target_is_informational": true
  }
}
```

### Professional sources and their limits

- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Linux Systems Administrator:** CIS Benchmarks for the distribution; ITIL 4 operations practices; vendor lifecycle policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
