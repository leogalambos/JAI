<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/risk-assessment

**Specification:** `kind/risk-assessment`; **content version:** `1.2.0`.

Select treatments and decide whether residual change risks are acceptable.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/risk-assessment`](spec-type-risk-assessment.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `risk-assessment`.

Scenario-based risk assessment using explicit evaluation criteria and treatment accountability.

**Evidence accompanying the work product:**

- likelihood/impact rationale and uncertainty
- current/residual exposure and treatment evidence

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`risk-assessment.assessment_scope`** — `object`

- Identify assets, business outcomes, boundaries and accountable risk owners.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`risk-assessment.scoring_method`** — `object`

- Define likelihood, impact, evaluation scales and the applicable risk appetite.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`risk-assessment.risk_scenarios`** — `array`

- Describe causes, events, consequences and the evidence behind each scenario.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`risk-assessment.risk_evaluation`** — `array`

- Link inherent and residual scores to scenarios, control effectiveness and uncertainty.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`risk-assessment.risk_treatment`** — `array`

- Assign response actions, owners, deadlines and residual-risk acceptance authority.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`risk-assessment.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`risk-assessment.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`risk-assessment.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`risk-assessment.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`risk-assessment.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`risk-assessment.duplicate_claim`** — `object`

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
      4,
      12
    ],
    "soft_max": 16,
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

- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **IT Risk Manager:** ISO 31000; NIST SP 800-30 and 800-37; COBIT 2019 APO12; FAIR for quantification. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate binding obligation, interpretation, control, evidence, independent test and bounded assurance/risk conclusion.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
