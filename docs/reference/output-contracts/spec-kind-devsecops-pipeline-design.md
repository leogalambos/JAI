<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/devsecops-pipeline-design

**Specification:** `kind/devsecops-pipeline-design`; **content version:** `1.2.0`.

Provide the proposed devsecops-pipeline-design information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`domain/security`](spec-domain-security.md)
- [`type/solution-design`](spec-type-solution-design.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`devsecops-pipeline-design.pipeline_scope`** — `object`

- Define repository, build, deployment, environment and pipeline trust boundaries.

**`devsecops-pipeline-design.stages_and_protection`** — `object`

- Specify isolated stages, protected transitions, independent reviews and promotion permissions.

**`devsecops-pipeline-design.security_quality_gates`** — `object`

- Define security and quality checks, failure behavior and non-waivable evidence requirements.

**`devsecops-pipeline-design.artifact_provenance`** — `object`

- Trace immutable artifacts through provenance, verification, signing and controlled distribution.

**`devsecops-pipeline-design.secrets_and_identity`** — `object`

- Specify least-privilege workload identities, secret references, rotation and exposure prevention.

**`devsecops-pipeline-design.operating_acceptance`** — `object`

- Define pipeline ownership, monitoring, recovery, change control and receiving acceptance.

### Conditionally required information

**`devsecops-pipeline-design.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`devsecops-pipeline-design.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`devsecops-pipeline-design.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`devsecops-pipeline-design.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`devsecops-pipeline-design.irrelevant_detail`** — `object`

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
