<!-- JAI:OUTPUT-CONTRACTS:START -->
# sabsa/policy-architecture

**Specification:** `sabsa/policy-architecture`; **content version:** `1.2.0`.

Strategy, policy, standards and policy traceability

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`sabsa/policy-architecture.business_traceability`** — `array`

- Trace selected security elements to business drivers, measurable attributes and source model IDs.

**`sabsa/policy-architecture.matrix_coverage`** — `array`

- Account for all 36 SABSA cells through selected source elements or explicit applicability reasons; never invent missing architecture facts.

**`sabsa/policy-architecture.policy_hierarchy`** — `array`

- Link business strategy and security policy to standards, owners and scope.

**`sabsa/policy-architecture.policy_enforcement`** — `array`

- Map policy statements to control objectives, mechanisms, exceptions and compliance evidence.

### Conditionally required information

**`sabsa/policy-architecture.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`sabsa/policy-architecture.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`sabsa/policy-architecture.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`sabsa/policy-architecture.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`sabsa/policy-architecture.irrelevant_detail`** — `object`

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
  },
  "elements": {
    "metric": "elements",
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
