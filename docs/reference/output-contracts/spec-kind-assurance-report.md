<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/assurance-report

**Specification:** `kind/assurance-report`; **content version:** `1.2.0`.

Determine whether delivery controls provide sufficient evidenced assurance for the stated scope.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `assurance-assessment`.

Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.

**Evidence accompanying the work product:**

- criterion-to-test-to-observation traceability
- independent reviewer and limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`assurance-report.assurance_scope`** — `object`

- Define assurance objectives, applicable criteria, period and exclusions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`assurance-report.assurance_method`** — `object`

- Identify independent assessor, sampling approach, limitations and evidence collection method.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`assurance-report.control_tests`** — `array`

- Link each tested criterion to procedure, evidence, sample and observed outcome.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`assurance-report.assurance_findings`** — `array`

- Record located deviations, significance, management response and corrective owners.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`assurance-report.assurance_conclusion`** — `object`

- Bound the assurance conclusion by tested scope, evidence and remaining uncertainty.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`assurance-report.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`assurance-report.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`assurance-report.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/74393.html); [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`assurance-report.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`assurance-report.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`assurance-report.duplicate_claim`** — `object`

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

- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Secure Delivery / DevSecOps Architect:** NIST SSDF SP 800-218; SLSA; OWASP SAMM; ISO/IEC 27001:2022 secure development controls. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
