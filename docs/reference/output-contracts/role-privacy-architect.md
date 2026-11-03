<!-- JAI:OUTPUT-CONTRACTS:START -->
# Privacy Architect: output contracts

Translate privacy obligations and risk into solution and enterprise architecture constraints, patterns and traceable design decisions.

[Full catalogue](index.md)

<a id="output-privacy-architect-1"></a>

## Privacy architecture and design requirements

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Privacy architecture and design requirements.
- **Mandatory examples:** Identify stakeholders, system boundary, concerns and architecture baseline. Identify target gaps, accountable owners and decisions required to close them. Link business, data, application and technology viewpoints using stable source-model IDs.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-architect:1`.

**Required inputs:**

- Privacy/legal requirements and DPO positions
- Processing purposes and data categories
- Solution architecture and data flows
- Security architecture and trust boundaries

**Specification:** `kind/role/privacy-architect:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Privacy architecture and design requirements.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/architecture-definition`](spec-type-architecture-definition.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-architect:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Privacy architecture and design requirements.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; Solution Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.delivery_verification`** — `array`

- For the specific output 'Privacy architecture and design requirements', provide verifiable evidence satisfying: Every requirement traces to purpose, processing context, privacy obligation/risk and verification method. Required delivery form: Versioned specification with traceable numbered requirements.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every personal-data flow has a stated purpose, owner and legal/privacy basis supplied by the accountable privacy function.
- G2: Data minimisation, retention/deletion and rights handling are designed, not deferred to policy text.
- G3: Jurisdiction, processor/subprocessor and cross-border dependencies are explicit where applicable.
- G4: Privacy requirements have verification methods that engineering/testing can execute.
- G5: Exceptions are time-bound and do not substitute the architect for the DPO or legal authority.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.contract_input_1`** — `object`

- Analyse the specific input "Privacy/legal requirements and DPO positions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.contract_input_2`** — `object`

- Analyse the specific input "Processing purposes and data categories" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.contract_input_3`** — `object`

- Analyse the specific input "Solution architecture and data flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.contract_input_4`** — `object`

- Analyse the specific input "Security architecture and trust boundaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/privacy-architect:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/privacy-architect:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/privacy-architect:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-architect:1.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Privacy Architect:** GDPR and applicable privacy law; ISO/IEC 27701; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-privacy-architect-2"></a>

## Personal-data flow and processing architecture

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Personal-data flow and processing architecture.
- **Mandatory examples:** Provide stable identified entities and typed relationships with ownership and provenance. Define entity/relation types, constraints, model boundary and source baseline. Evidence referential integrity, constraint checks, cross-view consistency and known gaps.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-architect:2`.

**Required inputs:**

- Privacy/legal requirements and DPO positions
- Processing purposes and data categories
- Solution architecture and data flows
- Security architecture and trust boundaries

**Specification:** `kind/role/privacy-architect:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Personal-data flow and processing architecture.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/model`](spec-type-model.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-architect:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Personal-data flow and processing architecture.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; Solution Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.delivery_verification`** — `array`

- For the specific output 'Personal-data flow and processing architecture', provide verifiable evidence satisfying: Data classes, purposes, recipients, stores, jurisdictions and retention points are represented with stable identifiers. Required delivery form: Model in the EA tool plus a published view set.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every personal-data flow has a stated purpose, owner and legal/privacy basis supplied by the accountable privacy function.
- G2: Data minimisation, retention/deletion and rights handling are designed, not deferred to policy text.
- G3: Jurisdiction, processor/subprocessor and cross-border dependencies are explicit where applicable.
- G4: Privacy requirements have verification methods that engineering/testing can execute.
- G5: Exceptions are time-bound and do not substitute the architect for the DPO or legal authority.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.contract_input_1`** — `object`

- Analyse the specific input "Privacy/legal requirements and DPO positions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.contract_input_2`** — `object`

- Analyse the specific input "Processing purposes and data categories" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.contract_input_3`** — `object`

- Analyse the specific input "Solution architecture and data flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.contract_input_4`** — `object`

- Analyse the specific input "Security architecture and trust boundaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/privacy-architect:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/privacy-architect:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/privacy-architect:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-architect:2.irrelevant_detail`** — `object`

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
  "elements": {
    "metric": "elements",
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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Privacy Architect:** GDPR and applicable privacy law; ISO/IEC 27701; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-privacy-architect-3"></a>

## Privacy engineering patterns and reference controls

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Privacy engineering patterns and reference controls.
- **Mandatory examples:** Identify actual governed entities with owners, source, status and lifecycle dates. Evidence duplicate detection, relationship integrity and reconciliation against sources. Define entity classes, stable identifiers, required attributes and relations.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-architect:3`.

**Required inputs:**

- Privacy/legal requirements and DPO positions
- Processing purposes and data categories
- Solution architecture and data flows
- Security architecture and trust boundaries

**Specification:** `kind/role/privacy-architect:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Privacy engineering patterns and reference controls.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/catalogue`](spec-type-catalogue.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-architect:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Privacy engineering patterns and reference controls.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; Solution Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.delivery_verification`** — `array`

- For the specific output 'Privacy engineering patterns and reference controls', provide verifiable evidence satisfying: Patterns state applicability, constraints, verification and known trade-offs. Required delivery form: Versioned pattern catalogue.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every personal-data flow has a stated purpose, owner and legal/privacy basis supplied by the accountable privacy function.
- G2: Data minimisation, retention/deletion and rights handling are designed, not deferred to policy text.
- G3: Jurisdiction, processor/subprocessor and cross-border dependencies are explicit where applicable.
- G4: Privacy requirements have verification methods that engineering/testing can execute.
- G5: Exceptions are time-bound and do not substitute the architect for the DPO or legal authority.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.contract_input_1`** — `object`

- Analyse the specific input "Privacy/legal requirements and DPO positions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.contract_input_2`** — `object`

- Analyse the specific input "Processing purposes and data categories" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.contract_input_3`** — `object`

- Analyse the specific input "Solution architecture and data flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.contract_input_4`** — `object`

- Analyse the specific input "Security architecture and trust boundaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/privacy-architect:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/privacy-architect:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.w3.org/TR/vocab-dcat-3/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/privacy-architect:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-architect:3.irrelevant_detail`** — `object`

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

- **Privacy Architect:** GDPR and applicable privacy law; ISO/IEC 27701; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-privacy-architect-4"></a>

## Privacy architecture decision and exception record

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Privacy architecture decision and exception record.
- **Mandatory examples:** Describe rejected options, reversibility, debt and operational consequences. Record decision status, owner, date and architecture concern. Compare feasible alternatives against explicit drivers and constraints.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-architect:4`.

**Required inputs:**

- Privacy/legal requirements and DPO positions
- Processing purposes and data categories
- Solution architecture and data flows
- Security architecture and trust boundaries

**Specification:** `kind/role/privacy-architect:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Privacy architecture decision and exception record.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/architecture-decision`](spec-type-architecture-decision.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-architect:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Privacy architecture decision and exception record.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; Solution Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.delivery_verification`** — `array`

- For the specific output 'Privacy architecture decision and exception record', provide verifiable evidence satisfying: Exceptions identify residual privacy risk, decision authority, compensating measures and review/expiry. Required delivery form: Decision/exception register with owner and expiry.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every personal-data flow has a stated purpose, owner and legal/privacy basis supplied by the accountable privacy function.
- G2: Data minimisation, retention/deletion and rights handling are designed, not deferred to policy text.
- G3: Jurisdiction, processor/subprocessor and cross-border dependencies are explicit where applicable.
- G4: Privacy requirements have verification methods that engineering/testing can execute.
- G5: Exceptions are time-bound and do not substitute the architect for the DPO or legal authority.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.contract_input_1`** — `object`

- Analyse the specific input "Privacy/legal requirements and DPO positions" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.contract_input_2`** — `object`

- Analyse the specific input "Processing purposes and data categories" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.contract_input_3`** — `object`

- Analyse the specific input "Solution architecture and data flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.contract_input_4`** — `object`

- Analyse the specific input "Security architecture and trust boundaries" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/privacy-architect:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/privacy-architect:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/privacy-architect:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/privacy-architect:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-architect:4.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Privacy Architect:** GDPR and applicable privacy law; ISO/IEC 27701; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
