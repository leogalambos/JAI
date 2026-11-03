<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/test-strategy

**Specification:** `kind/test-strategy`; **content version:** `1.2.0`.

Provide the proposed test-strategy-plan information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-strategy`](spec-type-test-strategy.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`test-strategy.test_objectives`** — `object`

- Define critical business invariants, release risks, scope and the confidence tests can and cannot provide.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-strategy.levels_techniques`** — `array`

- Allocate test levels, design techniques and responsibilities against specific risks and interfaces.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-strategy.environment_data`** — `object`

- Define representative environments, deterministic data, workload, time controls and captured execution evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-strategy.coverage_metrics`** — `array`

- Trace risks and requirements to cases and distinguish passed, failed, blocked and unexecuted coverage.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-strategy.execution_governance`** — `object`

- Define sequencing, staffing, triage, retest, blocking exit criteria and authorised deviation handling.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`test-strategy.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`test-strategy.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`test-strategy.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`test-strategy.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`test-strategy.irrelevant_detail`** — `object`

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
