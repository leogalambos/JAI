<!-- JAI:OUTPUT-CONTRACTS:START -->
# type/assurance-report

**Specification:** `type/assurance-report`; **content version:** `1.2.0`.

Common typed foundation for assurance-report; no substitute for a substantive document kind.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`type/assurance-report.identity`** — `object`

- Identify stable artifact ID, owner, source version and intended usage.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`type/assurance-report.assurance_criteria`** — `array`

- Define tested obligations, assurance period, sample and exclusions.
- State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`type/assurance-report.assurance_observations`** — `array`

- Link procedures and observed results to immutable evidence and located deviations.
- For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`type/assurance-report.bounded_conclusion`** — `object`

- Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`type/assurance-report.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`type/assurance-report.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`type/assurance-report.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`type/assurance-report.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`type/assurance-report.irrelevant_detail`** — `object`

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

- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
<!-- JAI:OUTPUT-CONTRACTS:END -->
