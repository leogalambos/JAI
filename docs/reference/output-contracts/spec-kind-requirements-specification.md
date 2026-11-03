<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/requirements-specification

**Specification:** `kind/requirements-specification`; **content version:** `1.2.0`.

Provide the proposed requirements-specification information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/requirements-specification`](spec-family-requirements-specification.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`requirements-specification.business_problem`** — `object`

- Describe actors, observable business problem, normal and exceptional scenarios and source evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`requirements-specification.functional_requirements`** — `array`

- State uniquely identified triggers, inputs, processing rules, outputs, exception behaviour and acceptance oracles.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`requirements-specification.quality_constraints`** — `object`

- Quantify quality attributes, measurement windows, operating loads and applicable legal constraints without inventing applicability.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`requirements-specification.traceability_priorities`** — `array`

- Trace requirements to sources, dependencies, priorities and conflict/change dispositions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`requirements-specification.acceptance_model`** — `object`

- Define measurable positive and negative acceptance cases, receiving authority and unresolved decisions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`requirements-specification.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

**`requirements-specification.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`requirements-specification.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`requirements-specification.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`requirements-specification.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
<!-- JAI:OUTPUT-CONTRACTS:END -->
