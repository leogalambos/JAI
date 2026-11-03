<!-- JAI:OUTPUT-CONTRACTS:START -->
# type/catalogue

**Specification:** `type/catalogue`; **content version:** `1.2.0`.

Common typed foundation for catalogue; no substitute for a substantive document kind.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`type/catalogue.identity`** — `object`

- Identify stable artifact ID, owner, source version and intended usage.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`type/catalogue.catalogue_schema`** — `object`

- Define entity classes, stable identifiers, required attributes and relations.
- Define the catalogued entity type, unique identifier, classification, required descriptive fields and inclusion/exclusion rules.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`type/catalogue.catalogue_entries`** — `array`

- Identify actual governed entities with owners, source, status and lifecycle dates.
- Provide usable entries with owner, state, source/version, discovery/access reference and relevant service or dependency relationships.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`type/catalogue.catalogue_integrity`** — `array`

- Evidence duplicate detection, relationship integrity and reconciliation against sources.
- Check identifiers, required metadata, broken references, duplicates and lifecycle status; name unresolved gaps and responsible maintainers.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`type/catalogue.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`type/catalogue.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`type/catalogue.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`type/catalogue.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`type/catalogue.irrelevant_detail`** — `object`

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
<!-- JAI:OUTPUT-CONTRACTS:END -->
