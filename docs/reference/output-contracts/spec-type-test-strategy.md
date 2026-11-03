<!-- JAI:OUTPUT-CONTRACTS:START -->
# type/test-strategy

**Specification:** `type/test-strategy`; **content version:** `1.2.0`.

Common typed foundation for test-strategy; no substitute for a substantive document kind.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`type/test-strategy.identity`** — `object`

- Identify stable artifact ID, owner, source version and intended usage.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`type/test-strategy.test_risk_scope`** — `object`

- Define risk-based test objectives, quality targets, scope and exclusions.
- Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`type/test-strategy.test_approach`** — `array`

- Define test levels, techniques, environments, representative data and responsibilities.
- Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`type/test-strategy.test_exit_criteria`** — `array`

- Define traceable entry/exit criteria, coverage measurement and defect disposition rules.
- Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`type/test-strategy.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`type/test-strategy.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`type/test-strategy.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`type/test-strategy.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`type/test-strategy.irrelevant_detail`** — `object`

- Remove material unrelated to the stated purpose, required input analysis or receiving-role action.

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
  }
}
```

### Professional sources and their limits

- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
<!-- JAI:OUTPUT-CONTRACTS:END -->
