<!-- JAI:OUTPUT-CONTRACTS:START -->
# kind/dataset

**Specification:** `kind/dataset`; **content version:** `1.2.0`.

Provide the proposed dataset information required for a bounded receiving-role decision or operational action.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/dataset`](spec-type-dataset.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`dataset.reference_dataset_contract`** — `object`

- Specify field meanings, keys, units, nulls and schema version.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`dataset.reference_dataset_lineage`** — `object`

- Record source, transformations and permitted handling.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`dataset.reference_dataset_quality`** — `object`

- Measure dimensions and disclose rejected and unresolved records.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`dataset.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

**`dataset.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`dataset.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`dataset.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`dataset.irrelevant_detail`** — `object`

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
  "rows": {
    "metric": "rows",
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

- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
<!-- JAI:OUTPUT-CONTRACTS:END -->
