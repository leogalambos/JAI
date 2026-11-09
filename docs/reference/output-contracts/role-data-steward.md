<!-- JAI:OUTPUT-CONTRACTS:START -->
# Data Steward: output contracts

Take day-to-day responsibility for the meaning, quality and correct use of data in one domain

[Full catalogue](index.md)

<a id="output-data-steward-1"></a>

## Business glossary entries for the domain

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Business glossary entries for the domain.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `data-steward:1`.

**Required inputs:**

- Business definitions and rules
- Quality measurement results
- Access requests
- Privacy constraints

**Specification:** `kind/role/data-steward:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Business glossary entries for the domain.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/catalogue`](spec-type-catalogue.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `governed-catalogue`.

Structured entity definitions/entries with stable identifiers, metadata, ownership and relationships.

**Evidence accompanying the work product:**

- source reconciliation and lifecycle state
- duplicate/reference integrity checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/data-steward:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Business glossary entries for the domain.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.receiving_acceptance`** — `array`

- For each receiving role (Data Quality Analyst; Data Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.delivery_verification`** — `array`

- For the specific output 'Business glossary entries for the domain', provide verifiable evidence satisfying: Define the catalogued entity type, unique identifier, classification, required descriptive fields and inclusion/exclusion rules. Provide usable entries with owner, state, source/version, discovery/access reference and relevant service or dependency relationships. Check identifiers, required metadata, broken references, duplicates and lifecycle status; name unresolved gaps and responsible maintainers. Required delivery form: Structured entity definitions/entries with stable identifiers, metadata, ownership and relationships.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Business glossary entries for the domain") is published on the agreed cadence, including adverse results.
- G5: No definition is published without agreement from the domain business owner
- G6: competing definitions are escalated, not merged into a vague one
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.contract_input_1`** — `object`

- Analyse the specific input "Business definitions and rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.contract_input_2`** — `object`

- Analyse the specific input "Quality measurement results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.contract_input_3`** — `object`

- Analyse the specific input "Access requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.contract_input_4`** — `object`

- Analyse the specific input "Privacy constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/data-steward:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/data-steward:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/data-steward:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/data-steward:1.irrelevant_detail`** — `object`

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
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Data Steward:** DAMA-DMBOK 2; DCAM; internal data governance policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-data-steward-2"></a>

## data quality rules and thresholds

**At a glance**

- **Purpose:** Produce and govern the role deliverable: data quality rules and thresholds.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `data-steward:2`.

**Required inputs:**

- Business definitions and rules
- Quality measurement results
- Access requests
- Privacy constraints

**Specification:** `kind/role/data-steward:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: data quality rules and thresholds.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/requirements-specification`](spec-family-requirements-specification.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `requirements-specification`.

Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.

**Evidence accompanying the work product:**

- forward/backward traceability
- conflict, interface and change-impact checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/data-steward:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: data quality rules and thresholds.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.receiving_acceptance`** — `array`

- For each receiving role (Data Quality Analyst; Data Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.delivery_verification`** — `array`

- For the specific output 'data quality rules and thresholds', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Business glossary entries for the domain") is published on the agreed cadence, including adverse results.
- G5: No definition is published without agreement from the domain business owner
- G6: competing definitions are escalated, not merged into a vague one
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.contract_input_1`** — `object`

- Analyse the specific input "Business definitions and rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.contract_input_2`** — `object`

- Analyse the specific input "Quality measurement results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.contract_input_3`** — `object`

- Analyse the specific input "Access requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.contract_input_4`** — `object`

- Analyse the specific input "Privacy constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/data-steward:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/data-steward:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/data-steward:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/data-steward:2.irrelevant_detail`** — `object`

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
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Data Steward:** DAMA-DMBOK 2; DCAM; internal data governance policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-data-steward-3"></a>

## issue log and remediation actions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: issue log and remediation actions.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `data-steward:3`.

**Required inputs:**

- Business definitions and rules
- Quality measurement results
- Access requests
- Privacy constraints

**Specification:** `kind/role/data-steward:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: issue log and remediation actions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `governed-register`.

Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.

**Evidence accompanying the work product:**

- actual source-attributed records
- uniqueness, completeness and relationship reconciliation

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/data-steward:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: issue log and remediation actions.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.receiving_acceptance`** — `array`

- For each receiving role (Data Quality Analyst; Data Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.delivery_verification`** — `array`

- For the specific output 'issue log and remediation actions', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Business glossary entries for the domain") is published on the agreed cadence, including adverse results.
- G5: No definition is published without agreement from the domain business owner
- G6: competing definitions are escalated, not merged into a vague one
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.contract_input_1`** — `object`

- Analyse the specific input "Business definitions and rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.contract_input_2`** — `object`

- Analyse the specific input "Quality measurement results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.contract_input_3`** — `object`

- Analyse the specific input "Access requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.contract_input_4`** — `object`

- Analyse the specific input "Privacy constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/data-steward:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/data-steward:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/data-steward:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/data-steward:3.irrelevant_detail`** — `object`

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

- **JAI authored enterprise-delivery practice** — Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review. Basis: `jai-practice`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Data Steward:** DAMA-DMBOK 2; DCAM; internal data governance policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-data-steward-4"></a>

## access and usage decisions record

**At a glance**

- **Purpose:** Produce and govern the role deliverable: access and usage decisions record.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `data-steward:4`.

**Required inputs:**

- Business definitions and rules
- Quality measurement results
- Access requests
- Privacy constraints

**Specification:** `kind/role/data-steward:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: access and usage decisions record.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `governed-register`.

Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.

**Evidence accompanying the work product:**

- actual source-attributed records
- uniqueness, completeness and relationship reconciliation

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/data-steward:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: access and usage decisions record.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.receiving_acceptance`** — `array`

- For each receiving role (Data Quality Analyst; Data Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.delivery_verification`** — `array`

- For the specific output 'access and usage decisions record', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Business glossary entries for the domain") is published on the agreed cadence, including adverse results.
- G5: No definition is published without agreement from the domain business owner
- G6: competing definitions are escalated, not merged into a vague one
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.contract_input_1`** — `object`

- Analyse the specific input "Business definitions and rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.contract_input_2`** — `object`

- Analyse the specific input "Quality measurement results" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.contract_input_3`** — `object`

- Analyse the specific input "Access requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.contract_input_4`** — `object`

- Analyse the specific input "Privacy constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/data-steward:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

**`role/data-steward:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/data-steward:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/); [source](https://www.w3.org/TR/vocab-dqv/); [source](https://doi.org/10.6028/NIST.AI.100-1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/data-steward:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/data-steward:4.irrelevant_detail`** — `object`

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

- **JAI authored enterprise-delivery practice** — Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review. Basis: `jai-practice`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Catalog Vocabulary Version 3 (DCAT 3)](https://www.w3.org/TR/vocab-dcat-3/)** — Dataset/catalogue identity, distributions, provenance, access and descriptive metadata. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)** — Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://doi.org/10.6028/NIST.AI.100-1)** — Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Data Steward:** DAMA-DMBOK 2; DCAM; internal data governance policy. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
