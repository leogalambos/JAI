<!-- JAI:OUTPUT-CONTRACTS:START -->
# family/analysis-report

**Specification:** `family/analysis-report`; **content version:** `1.2.0`.

Shared semantic obligations for analysis-report.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`family/analysis-report.analysis_baseline`** — `object`

- Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions.
- State scope, precise question, method, period and source/population boundaries; disclose missing data, selection bias and the limits of the measurement or investigative method.

**`family/analysis-report.analysis_observations`** — `array`

- Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- For each finding, link source and exact observation or calculation, distinguish event chronology from causal inference, and expose counterevidence, uncertainty and unsupported hypotheses.

**`family/analysis-report.analysis_conclusion`** — `object`

- Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request.
- Bound conclusions by the observations, specify recipient actions and unresolved questions, and distinguish recommendations from actual decisions. Do not invent a do-nothing baseline or two alternatives merely to package an operational, research or investigative report.

### Conditionally required information

**`family/analysis-report.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`family/analysis-report.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`family/analysis-report.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`family/analysis-report.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`family/analysis-report.irrelevant_detail`** — `object`

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
