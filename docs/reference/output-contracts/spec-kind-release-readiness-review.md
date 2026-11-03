<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/release-readiness-review

**Specification:** `kind/release-readiness-review`; **content version:** `1.2.0`.

Provide the proposed release-readiness-review information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/operational-readiness-assessment`](spec-type-operational-readiness-assessment.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`release-readiness-review.release_scope`** — `object`

- Identify exact release scope, included changes, environments, owners and excluded capabilities.

**`release-readiness-review.build_provenance`** — `object`

- Trace source revision, dependency inventory, build digest and attributable provenance to the candidate.

**`release-readiness-review.verification_summary`** — `object`

- Distinguish executed verification results, failures, blocked checks and missing mandatory evidence.

**`release-readiness-review.operability_readiness`** — `object`

- Assess monitoring, recovery rehearsal, receiving operations, service dependencies and support readiness.

**`release-readiness-review.open_risks`** — `object`

- Record unresolved defects, residual risks, compensating controls and competent disposition owners.

**`release-readiness-review.release_disposition`** — `object`

- Separate evidence-based release recommendation from human deployment authority and approval.

### Conditionally required information

**`release-readiness-review.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`release-readiness-review.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`release-readiness-review.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`release-readiness-review.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`release-readiness-review.irrelevant_detail`** — `object`

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
