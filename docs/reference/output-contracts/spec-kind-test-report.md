<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/test-report

**Specification:** `kind/test-report`; **content version:** `1.2.0`.

Determine whether tested requirements satisfy exit criteria and residual defects permit progression.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-report`](spec-type-test-report.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`test-report.test_scope`** — `object`

- Identify tested requirements, exclusions, build versions and the reporting period.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-report.test_environment`** — `object`

- Record environment, data constraints, tools and reproducible execution configuration.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-report.execution_results`** — `array`

- Link test cases and requirement IDs to execution timestamps, actual outcomes and evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-report.defect_analysis`** — `array`

- Record unresolved defects, severity, retest state and their impact on acceptance.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-report.test_conclusion`** — `object`

- Compare achieved coverage with exit criteria and explain limitations and residual release risk.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`test-report.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify personal-data flows, lawful handling constraints, minimisation and review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-report.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`test-report.technical_annex`** — `object`

- Include deeper calculations or technical detail only when linked to a reader need.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`test-report.unsupported_material_claim`** — `object`

- Never state a material conclusion as established without evidence or explicit uncertainty.

### Content to omit unless justified

**`test-report.irrelevant_detail`** — `object`

- Remove detail that does not support the stated purpose or a referenced annex.

**`test-report.duplicate_claim`** — `object`

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
      3,
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

- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Test Analyst:** ISTQB; ISO/IEC/IEEE 29119; risk-based testing practice. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
