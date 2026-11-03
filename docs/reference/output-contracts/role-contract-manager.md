<!-- JAI:OUTPUT-CONTRACTS:START -->
# Contract Manager: output contracts

Make sure what was agreed is written down correctly and then actually happens

[Full catalogue](index.md)

<a id="output-contract-manager-1"></a>

## Contract repository and obligation register

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Contract repository and obligation register.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `contract-manager:1`.

**Required inputs:**

- Negotiated commercial terms
- Legal drafting
- Delivery performance
- Regulatory requirements for contracts

**Specification:** `kind/role/contract-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Contract repository and obligation register.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/contract-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Contract repository and obligation register.

**`role/contract-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Vendor Manager; Third-Party Risk Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/contract-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/contract-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/contract-manager:1.delivery_verification`** — `array`

- For the specific output 'Contract repository and obligation register', provide verifiable evidence satisfying: Every row has an owner, a date, a status and a next action. Required delivery form: Structured table in the system of record (CSV/tool export).

**`role/contract-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Contract repository and obligation register") is published on the agreed cadence, including adverse results.
- G5: Every obligation on both sides is extracted into a tracked register with an owner
- G6: obligations that live only in the contract document are not managed

**`role/contract-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Negotiated commercial terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Legal drafting" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Delivery performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Regulatory requirements for contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:1.contract_repository_identity`** — `array`

- Identify contracting parties, operative signed contract/version, applicable jurisdiction or governing-law reference, effective/expiry dates and authoritative record location; preserve draft and superseded status explicitly.

**`role/contract-manager:1.contract_obligation_records`** — `array`

- For each tracked obligation, identify contract/clause, responsible party and owner, deliverable or performance measure, due/renewal/notice dates, dependencies, acceptance evidence and current status.

**`role/contract-manager:1.contract_lifecycle_integrity`** — `object`

- Define access/classification, authorised variation links, renewal/termination triggers and reconciliation of the obligation register with operative contract versions; expose missing documents or unresolved interpretations.

### Conditionally required information

**`role/contract-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/contract-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/contract-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/contract-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/contract-manager:1.irrelevant_detail`** — `object`

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

- **Contract Manager:** organisational contract standards; DORA contractual requirements where applicable; IACCM/WorldCC practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-contract-manager-2"></a>

## variation and change records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: variation and change records.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `contract-manager:2`.

**Required inputs:**

- Negotiated commercial terms
- Legal drafting
- Delivery performance
- Regulatory requirements for contracts

**Specification:** `kind/role/contract-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: variation and change records.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/contract-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: variation and change records.

**`role/contract-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Vendor Manager; Third-Party Risk Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/contract-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/contract-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/contract-manager:2.delivery_verification`** — `array`

- For the specific output 'variation and change records', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/contract-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Contract repository and obligation register") is published on the agreed cadence, including adverse results.
- G5: Every obligation on both sides is extracted into a tracked register with an owner
- G6: obligations that live only in the contract document are not managed

**`role/contract-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Negotiated commercial terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Legal drafting" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Delivery performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Regulatory requirements for contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/contract-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/contract-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/contract-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/contract-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/contract-manager:2.irrelevant_detail`** — `object`

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

- **Contract Manager:** organisational contract standards; DORA contractual requirements where applicable; IACCM/WorldCC practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-contract-manager-3"></a>

## obligation compliance monitoring

**At a glance**

- **Purpose:** Produce and govern the role deliverable: obligation compliance monitoring.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `contract-manager:3`.

**Required inputs:**

- Negotiated commercial terms
- Legal drafting
- Delivery performance
- Regulatory requirements for contracts

**Specification:** `kind/role/contract-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: obligation compliance monitoring.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/contract-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: obligation compliance monitoring.

**`role/contract-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Vendor Manager; Third-Party Risk Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/contract-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/contract-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/contract-manager:3.delivery_verification`** — `array`

- For the specific output 'obligation compliance monitoring', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/contract-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Contract repository and obligation register") is published on the agreed cadence, including adverse results.
- G5: Every obligation on both sides is extracted into a tracked register with an owner
- G6: obligations that live only in the contract document are not managed

**`role/contract-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Negotiated commercial terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Legal drafting" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Delivery performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Regulatory requirements for contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:3.binding_obligation_baseline`** — `array`

- Identify the executed contract/version, applicable clause or obligation ID, accountable party, effective/due dates and agreed measurable acceptance or performance threshold; distinguish proposed terms from binding obligations.

**`role/contract-manager:3.obligation_observations`** — `array`

- For each obligation due in the reporting period, link actual performance/delivery evidence, measurement period and status; separate met, breached, disputed, not yet due and insufficient-evidence cases.

**`role/contract-manager:3.obligation_remedies`** — `array`

- For each material deviation, identify impact, notice/cure deadlines, contractually available remedies, escalation owner and required legal/commercial decision; do not invent a right, waive an obligation or claim a dispute resolved without authority.

### Conditionally required information

**`role/contract-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/contract-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/contract-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/contract-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/contract-manager:3.irrelevant_detail`** — `object`

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

- **Contract Manager:** organisational contract standards; DORA contractual requirements where applicable; IACCM/WorldCC practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-contract-manager-4"></a>

## dispute and remedy records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: dispute and remedy records.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `contract-manager:4`.

**Required inputs:**

- Negotiated commercial terms
- Legal drafting
- Delivery performance
- Regulatory requirements for contracts

**Specification:** `kind/role/contract-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: dispute and remedy records.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/contract-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: dispute and remedy records.

**`role/contract-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Vendor Manager; Third-Party Risk Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/contract-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/contract-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/contract-manager:4.delivery_verification`** — `array`

- For the specific output 'dispute and remedy records', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/contract-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Intake is rejected unless all mandatory inputs are present or a named owner and date exist for each gap.
- G2: No commitment is made beyond demonstrated capacity for the period.
- G3: Every deviation from the documented process is logged with its reason and its expiry.
- G4: The primary deliverable ("Contract repository and obligation register") is published on the agreed cadence, including adverse results.
- G5: Every obligation on both sides is extracted into a tracked register with an owner
- G6: obligations that live only in the contract document are not managed

**`role/contract-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Negotiated commercial terms" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Legal drafting" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Delivery performance" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Regulatory requirements for contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/contract-manager:4.dispute_factual_record`** — `array`

- Identify dispute/claim ID, parties, operative contract/clause and relevant governing-law reference, asserted event, dated chronology, evidence, amounts/remedies claimed and disputed versus agreed facts.

**`role/contract-manager:4.notice_remedy_control`** — `array`

- Record applicable contractual notice/cure/escalation deadlines, required delivery method, notices actually issued, rights reserved, proposed remedies and accountable commercial/legal owners; do not fabricate authority or a legal entitlement.

**`role/contract-manager:4.dispute_disposition`** — `object`

- Record positions, negotiation/decision status, authorised settlement or remedy where actually agreed, outstanding actions, implementation evidence and closure conditions; a recommendation is not an executed settlement.

### Conditionally required information

**`role/contract-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/contract-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/contract-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/contract-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/contract-manager:4.irrelevant_detail`** — `object`

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

- **Contract Manager:** organisational contract standards; DORA contractual requirements where applicable; IACCM/WorldCC practice. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
