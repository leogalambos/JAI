<!-- JAI:OUTPUT-CONTRACTS:START -->
# Records Manager: output contracts

Decide how long information is kept, why, and make sure it is actually disposed of

[Full catalogue](index.md)

<a id="output-records-manager-1"></a>

## Retention schedule with legal justification

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Retention schedule with legal justification.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `records-manager:1`.

**Required inputs:**

- Legal and regulatory retention requirements
- Business use requirements
- System and repository inventory
- Litigation holds

**Specification:** `kind/role/records-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Retention schedule with legal justification.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/roadmap`](spec-type-roadmap.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/records-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Retention schedule with legal justification.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Data Custodian; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.delivery_verification`** — `array`

- For the specific output 'Retention schedule with legal justification', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: Legal hold overrides scheduled disposal and is applied before any disposal run
- G6: disposal that destroys data under hold is treated as a serious legal incident
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Legal and regulatory retention requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Business use requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.contract_input_3`** — `object`

- Analyse the specific input "System and repository inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Litigation holds" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/records-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/records-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/records-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/records-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/records-manager:1.irrelevant_detail`** — `object`

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

- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Records Manager:** ISO 15489; MoReq or national equivalents; sector retention regulations. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-records-manager-2"></a>

## records classification scheme

**At a glance**

- **Purpose:** Produce and govern the role deliverable: records classification scheme.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `records-manager:2`.

**Required inputs:**

- Legal and regulatory retention requirements
- Business use requirements
- System and repository inventory
- Litigation holds

**Specification:** `kind/role/records-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: records classification scheme.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/records-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: records classification scheme.

**`role/records-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Data Custodian; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/records-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/records-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/records-manager:2.delivery_verification`** — `array`

- For the specific output 'records classification scheme', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/records-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: Legal hold overrides scheduled disposal and is applied before any disposal run
- G6: disposal that destroys data under hold is treated as a serious legal incident

**`role/records-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Legal and regulatory retention requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Business use requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:2.contract_input_3`** — `object`

- Analyse the specific input "System and repository inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Litigation holds" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/records-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/records-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/records-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/records-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/records-manager:2.irrelevant_detail`** — `object`

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

### Role framework context

- **Records Manager:** ISO 15489; MoReq or national equivalents; sector retention regulations. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-records-manager-3"></a>

## disposal authorisations and certificates

**At a glance**

- **Purpose:** Produce and govern the role deliverable: disposal authorisations and certificates.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `records-manager:3`.

**Required inputs:**

- Legal and regulatory retention requirements
- Business use requirements
- System and repository inventory
- Litigation holds

**Specification:** `kind/role/records-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: disposal authorisations and certificates.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/records-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: disposal authorisations and certificates.

**`role/records-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Data Custodian; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/records-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/records-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/records-manager:3.delivery_verification`** — `array`

- For the specific output 'disposal authorisations and certificates', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/records-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: Legal hold overrides scheduled disposal and is applied before any disposal run
- G6: disposal that destroys data under hold is treated as a serious legal incident

**`role/records-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Legal and regulatory retention requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Business use requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:3.contract_input_3`** — `object`

- Analyse the specific input "System and repository inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Litigation holds" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/records-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/records-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/records-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/records-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/records-manager:3.irrelevant_detail`** — `object`

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

### Role framework context

- **Records Manager:** ISO 15489; MoReq or national equivalents; sector retention regulations. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-records-manager-4"></a>

## legal hold register

**At a glance**

- **Purpose:** Produce and govern the role deliverable: legal hold register.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `records-manager:4`.

**Required inputs:**

- Legal and regulatory retention requirements
- Business use requirements
- System and repository inventory
- Litigation holds

**Specification:** `kind/role/records-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: legal hold register.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/records-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: legal hold register.

**`role/records-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Data Custodian; IT Asset Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/records-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/records-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/records-manager:4.delivery_verification`** — `array`

- For the specific output 'legal hold register', provide verifiable evidence satisfying: Every row has an owner, a date, a status and a next action. Required delivery form: Structured table in the system of record (CSV/tool export).

**`role/records-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every policy statement has a named owner, an effective date and a review date.
- G2: Exceptions are time-bound, risk-assessed, approved at the correct authority level and tracked to expiry.
- G3: Reported position is based on independent evidence, not self-assessment alone.
- G4: Any breach of tolerance triggers a defined action, not merely a note in the minutes.
- G5: Legal hold overrides scheduled disposal and is applied before any disposal run
- G6: disposal that destroys data under hold is treated as a serious legal incident

**`role/records-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Legal and regulatory retention requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Business use requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:4.contract_input_3`** — `object`

- Analyse the specific input "System and repository inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/records-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Litigation holds" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/records-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/records-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/records-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/records-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/records-manager:4.irrelevant_detail`** — `object`

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

### Role framework context

- **Records Manager:** ISO 15489; MoReq or national equivalents; sector retention regulations. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
