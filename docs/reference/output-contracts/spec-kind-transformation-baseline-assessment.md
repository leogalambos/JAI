<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/transformation-baseline-assessment

**Specification:** `kind/transformation-baseline-assessment`; **content version:** `1.2.0`.

Provide the proposed transformation-baseline-assessment information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`transformation-baseline-assessment.baseline_boundary`** — `object`

- Define dated baseline scope, business entities, value streams and assessment authority limitations.

**`transformation-baseline-assessment.capability_evidence`** — `object`

- Assess current capabilities using attributable observations, sampling limits and explicitly uncertain measurements.

**`transformation-baseline-assessment.pain_points`** — `object`

- Locate business pain points, causal hypotheses, impacts and gaps in the supporting evidence.

**`transformation-baseline-assessment.dependency_map`** — `object`

- Map organizational, system, supplier and data dependencies with accountable ownership and constraints.

**`transformation-baseline-assessment.gap_prioritisation`** — `object`

- Prioritize gaps using explicit value, risk, feasibility and confidence criteria without invented certainty.

**`transformation-baseline-assessment.baseline_decision`** — `object`

- Identify decisions supported by the baseline, evidence owners and conditions for independent acceptance.

### Conditionally required information

**`transformation-baseline-assessment.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`transformation-baseline-assessment.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`transformation-baseline-assessment.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`transformation-baseline-assessment.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`transformation-baseline-assessment.irrelevant_detail`** — `object`

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

- **JAI authored enterprise-delivery practice** — Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review. Basis: `jai-practice`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
<!-- JAI:OUTPUT-CONTRACTS:END -->
