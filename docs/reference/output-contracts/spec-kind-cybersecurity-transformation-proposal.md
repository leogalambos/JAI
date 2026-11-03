<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/cybersecurity-transformation-proposal

**Specification:** `kind/cybersecurity-transformation-proposal`; **content version:** `1.2.0`.

Provide the proposed cybersecurity-transformation-proposal information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`cybersecurity-transformation-proposal.security_baseline`** — `object`

- Identify business risk, current security evidence, transformation scope and mandate limitations.

**`cybersecurity-transformation-proposal.target_control_architecture`** — `object`

- Trace target control outcomes and trust boundaries to risks, business drivers and alternatives.

**`cybersecurity-transformation-proposal.transformation_waves`** — `array`

- Sequence security work packages, prerequisites, owners and deployment dependencies.

**`cybersecurity-transformation-proposal.assurance_roadmap`** — `array`

- Define control verification, measurable outcomes, independent review and residual uncertainty.

**`cybersecurity-transformation-proposal.resourcing_cost`** — `object`

- Reconcile scope-specific effort and separately priced security options, excluded from base programme totals.

**`cybersecurity-transformation-proposal.risk_acceptance`** — `object`

- State residual risk, competent acceptance authority and conditions without claiming certification or approval.

### Conditionally required information

**`cybersecurity-transformation-proposal.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`cybersecurity-transformation-proposal.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`cybersecurity-transformation-proposal.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`cybersecurity-transformation-proposal.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

**`cybersecurity-transformation-proposal.unapproved_commitment`** — `object`

- Do not present illustrative fees, supplier commitments, legal terms, compliance claims or synthetic tests as authorised, executed or verified facts.

### Content to omit unless justified

**`cybersecurity-transformation-proposal.irrelevant_detail`** — `object`

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
