<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/software-supply-chain-assessment

**Specification:** `kind/software-supply-chain-assessment`; **content version:** `1.2.0`.

Provide the proposed software-supply-chain-assessment information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`domain/security`](spec-domain-security.md)
- [`type/assurance-report`](spec-type-assurance-report.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`software-supply-chain-assessment.supply_chain_scope`** — `object`

- Define software products, build systems, suppliers and distribution boundaries under assessment.

**`software-supply-chain-assessment.dependency_inventory`** — `object`

- Inventory direct and transitive dependencies, versions, origin, licensing and known evidence gaps.

**`software-supply-chain-assessment.build_provenance`** — `object`

- Assess attributable build provenance, reproducibility, isolated execution and source integrity.

**`software-supply-chain-assessment.publisher_integrity`** — `object`

- Verify publisher identities, artifact digests, signing trust and controlled acquisition practices.

**`software-supply-chain-assessment.supplier_risks`** — `object`

- Evaluate supplier exposure, maintenance, compromise paths and uncertainty with accountable owners.

**`software-supply-chain-assessment.release_conditions`** — `object`

- Define evidence-based release conditions, remediation and competent exception authority.

### Conditionally required information

**`software-supply-chain-assessment.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`software-supply-chain-assessment.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`software-supply-chain-assessment.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`software-supply-chain-assessment.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`software-supply-chain-assessment.irrelevant_detail`** — `object`

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
