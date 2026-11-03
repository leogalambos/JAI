<!-- JAI:OUTPUT-CONTRACTS:START -->
# Service Catalogue Manager: output contracts

Maintain an accurate, usable catalogue of what IT actually offers and on what terms

[Full catalogue](index.md)

<a id="output-service-catalogue-manager-1"></a>

## Service catalogue entries with owners and terms

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Service catalogue entries with owners and terms.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-catalogue-manager:1`.

**Required inputs:**

- Service definitions
- Entitlement rules
- Cost and charging information
- User feedback

**Specification:** `kind/role/service-catalogue-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Service catalogue entries with owners and terms.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/catalogue`](spec-type-catalogue.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/service-catalogue-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Service catalogue entries with owners and terms.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Service Desk Analyst; Request Fulfilment Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.delivery_verification`** — `array`

- For the specific output 'Service catalogue entries with owners and terms', provide verifiable evidence satisfying: Each entry has an owner, a lifecycle status and a last-verified date. Required delivery form: Structured entries in the service or asset management tool.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Service catalogue entries with owners and terms") is published on the agreed cadence, including adverse results.
- G5: Every catalogue entry has an owner, a current description in user language and a review date
- G6: entries describing retired services are removed
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Service definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Entitlement rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Cost and charging information" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.contract_input_4`** — `object`

- Analyse the specific input "User feedback" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-catalogue-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-catalogue-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-catalogue-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-catalogue-manager:1.irrelevant_detail`** — `object`

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

### Role framework context

- **Service Catalogue Manager:** ITIL 4 service catalogue management; ISO/IEC 20000-1. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-service-catalogue-manager-2"></a>

## request and service definitions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: request and service definitions.
- **Mandatory examples:** Define measurable availability, support, capacity and recovery targets. Describe support responsibilities, suppliers, monitoring, continuity and lifecycle costs. Identify customers, service owner, outcomes, boundaries and demand assumptions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-catalogue-manager:2`.

**Required inputs:**

- Service definitions
- Entitlement rules
- Cost and charging information
- User feedback

**Specification:** `kind/role/service-catalogue-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: request and service definitions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/service-design`](spec-type-service-design.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/service-catalogue-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: request and service definitions.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Service Desk Analyst; Request Fulfilment Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.delivery_verification`** — `array`

- For the specific output 'request and service definitions', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Service catalogue entries with owners and terms") is published on the agreed cadence, including adverse results.
- G5: Every catalogue entry has an owner, a current description in user language and a review date
- G6: entries describing retired services are removed
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Service definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Entitlement rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Cost and charging information" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.contract_input_4`** — `object`

- Analyse the specific input "User feedback" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-catalogue-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-catalogue-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-catalogue-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-catalogue-manager:2.irrelevant_detail`** — `object`

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

- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Catalogue Manager:** ITIL 4 service catalogue management; ISO/IEC 20000-1. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-service-catalogue-manager-3"></a>

## catalogue review and currency evidence

**At a glance**

- **Purpose:** Produce and govern the role deliverable: catalogue review and currency evidence.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-catalogue-manager:3`.

**Required inputs:**

- Service definitions
- Entitlement rules
- Cost and charging information
- User feedback

**Specification:** `kind/role/service-catalogue-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: catalogue review and currency evidence.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/catalogue`](spec-type-catalogue.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/service-catalogue-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: catalogue review and currency evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Service Desk Analyst; Request Fulfilment Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.delivery_verification`** — `array`

- For the specific output 'catalogue review and currency evidence', provide verifiable evidence satisfying: Chain of custody is unbroken and the set is reproducible from the record. Required delivery form: Immutable evidence set with hashes, timestamps and custody record.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Service catalogue entries with owners and terms") is published on the agreed cadence, including adverse results.
- G5: Every catalogue entry has an owner, a current description in user language and a review date
- G6: entries describing retired services are removed
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Service definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Entitlement rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Cost and charging information" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.contract_input_4`** — `object`

- Analyse the specific input "User feedback" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-catalogue-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-catalogue-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-catalogue-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-catalogue-manager:3.irrelevant_detail`** — `object`

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

### Role framework context

- **Service Catalogue Manager:** ITIL 4 service catalogue management; ISO/IEC 20000-1. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-service-catalogue-manager-4"></a>

## catalogue usability improvements

**At a glance**

- **Purpose:** Produce and govern the role deliverable: catalogue usability improvements.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-catalogue-manager:4`.

**Required inputs:**

- Service definitions
- Entitlement rules
- Cost and charging information
- User feedback

**Specification:** `kind/role/service-catalogue-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: catalogue usability improvements.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/catalogue`](spec-type-catalogue.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/service-catalogue-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: catalogue usability improvements.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Service Desk Analyst; Request Fulfilment Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.delivery_verification`** — `array`

- For the specific output 'catalogue usability improvements', provide verifiable evidence satisfying: Each entry has an owner, a lifecycle status and a last-verified date. Required delivery form: Structured entries in the service or asset management tool.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Service catalogue entries with owners and terms") is published on the agreed cadence, including adverse results.
- G5: Every catalogue entry has an owner, a current description in user language and a review date
- G6: entries describing retired services are removed
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Service definitions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Entitlement rules" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Cost and charging information" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.contract_input_4`** — `object`

- Analyse the specific input "User feedback" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-catalogue-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/service-catalogue-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-catalogue-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-catalogue-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-catalogue-manager:4.irrelevant_detail`** — `object`

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

### Role framework context

- **Service Catalogue Manager:** ITIL 4 service catalogue management; ISO/IEC 20000-1. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
