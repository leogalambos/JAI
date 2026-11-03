<!-- JAI:OUTPUT-CONTRACTS:START -->
# Standards Body Representative: output contracts

Represent the organisation's interests in external standards work and bring the outcomes back inside

[Full catalogue](index.md)

<a id="output-standards-body-representative-1"></a>

## Position papers and contributions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Position papers and contributions.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `standards-body-representative:1`.

**Required inputs:**

- Organisational position and interests
- Draft standards and working documents
- Internal technical impact analysis
- Legal and antitrust constraints

**Specification:** `kind/role/standards-body-representative:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Position papers and contributions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/standards-body-representative:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Position papers and contributions.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Product Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.delivery_verification`** — `array`

- For the specific output 'Position papers and contributions', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every factual claim is verified with the accountable owner or a primary source.
- G2: Commitments made externally are deliverable and have been confirmed with the team who must deliver them.
- G3: Material carries an owner and a review date; unowned content is retired.
- G4: Confidential, personal or customer-identifying information is removed before publication.
- G5: Antitrust and IPR rules of the body are observed strictly
- G6: commercially sensitive discussion in a standards forum is stopped and reported immediately
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.contract_input_1`** — `object`

- Analyse the specific input "Organisational position and interests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.contract_input_2`** — `object`

- Analyse the specific input "Draft standards and working documents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.contract_input_3`** — `object`

- Analyse the specific input "Internal technical impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.contract_input_4`** — `object`

- Analyse the specific input "Legal and antitrust constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/standards-body-representative:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/standards-body-representative:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/standards-body-representative:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/standards-body-representative:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/standards-body-representative:1.irrelevant_detail`** — `object`

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

- **[HM Treasury, The Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)** — Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Standards Body Representative:** the relevant body's process (ISO, IETF, W3C, ETSI, OASIS); antitrust and competition law; IPR and patent policy of the body. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-standards-body-representative-2"></a>

## standards participation and voting records

**At a glance**

- **Purpose:** Produce and govern the role deliverable: standards participation and voting records.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `standards-body-representative:2`.

**Required inputs:**

- Organisational position and interests
- Draft standards and working documents
- Internal technical impact analysis
- Legal and antitrust constraints

**Specification:** `kind/role/standards-body-representative:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: standards participation and voting records.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/standards-body-representative:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: standards participation and voting records.

**`role/standards-body-representative:2.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Product Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/standards-body-representative:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/standards-body-representative:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/standards-body-representative:2.delivery_verification`** — `array`

- For the specific output 'standards participation and voting records', provide verifiable evidence satisfying: Requirements are specific, measurable and technology-explicit. Required delivery form: Controlled document referencing the parent policy.

**`role/standards-body-representative:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every factual claim is verified with the accountable owner or a primary source.
- G2: Commitments made externally are deliverable and have been confirmed with the team who must deliver them.
- G3: Material carries an owner and a review date; unowned content is retired.
- G4: Confidential, personal or customer-identifying information is removed before publication.
- G5: Antitrust and IPR rules of the body are observed strictly
- G6: commercially sensitive discussion in a standards forum is stopped and reported immediately

**`role/standards-body-representative:2.contract_input_1`** — `object`

- Analyse the specific input "Organisational position and interests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:2.contract_input_2`** — `object`

- Analyse the specific input "Draft standards and working documents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:2.contract_input_3`** — `object`

- Analyse the specific input "Internal technical impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:2.contract_input_4`** — `object`

- Analyse the specific input "Legal and antitrust constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/standards-body-representative:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/standards-body-representative:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/standards-body-representative:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/standards-body-representative:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/standards-body-representative:2.irrelevant_detail`** — `object`

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

- **Standards Body Representative:** the relevant body's process (ISO, IETF, W3C, ETSI, OASIS); antitrust and competition law; IPR and patent policy of the body. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-standards-body-representative-3"></a>

## impact assessment of draft standards

**At a glance**

- **Purpose:** Produce and govern the role deliverable: impact assessment of draft standards.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `standards-body-representative:3`.

**Required inputs:**

- Organisational position and interests
- Draft standards and working documents
- Internal technical impact analysis
- Legal and antitrust constraints

**Specification:** `kind/role/standards-body-representative:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: impact assessment of draft standards.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/standards-body-representative:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: impact assessment of draft standards.

**`role/standards-body-representative:3.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Product Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/standards-body-representative:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/standards-body-representative:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/standards-body-representative:3.delivery_verification`** — `array`

- For the specific output 'impact assessment of draft standards', provide verifiable evidence satisfying: Requirements are specific, measurable and technology-explicit. Required delivery form: Controlled document referencing the parent policy.

**`role/standards-body-representative:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every factual claim is verified with the accountable owner or a primary source.
- G2: Commitments made externally are deliverable and have been confirmed with the team who must deliver them.
- G3: Material carries an owner and a review date; unowned content is retired.
- G4: Confidential, personal or customer-identifying information is removed before publication.
- G5: Antitrust and IPR rules of the body are observed strictly
- G6: commercially sensitive discussion in a standards forum is stopped and reported immediately

**`role/standards-body-representative:3.contract_input_1`** — `object`

- Analyse the specific input "Organisational position and interests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:3.contract_input_2`** — `object`

- Analyse the specific input "Draft standards and working documents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:3.contract_input_3`** — `object`

- Analyse the specific input "Internal technical impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:3.contract_input_4`** — `object`

- Analyse the specific input "Legal and antitrust constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/standards-body-representative:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/standards-body-representative:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/standards-body-representative:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/standards-body-representative:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/standards-body-representative:3.irrelevant_detail`** — `object`

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

- **Standards Body Representative:** the relevant body's process (ISO, IETF, W3C, ETSI, OASIS); antitrust and competition law; IPR and patent policy of the body. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-standards-body-representative-4"></a>

## internal adoption guidance

**At a glance**

- **Purpose:** Produce and govern the role deliverable: internal adoption guidance.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `standards-body-representative:4`.

**Required inputs:**

- Organisational position and interests
- Draft standards and working documents
- Internal technical impact analysis
- Legal and antitrust constraints

**Specification:** `kind/role/standards-body-representative:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: internal adoption guidance.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/standards-body-representative:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: internal adoption guidance.

**`role/standards-body-representative:4.receiving_acceptance`** — `array`

- For each receiving role (Enterprise Architect; Product Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/standards-body-representative:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/standards-body-representative:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/standards-body-representative:4.delivery_verification`** — `array`

- For the specific output 'internal adoption guidance', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/standards-body-representative:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every factual claim is verified with the accountable owner or a primary source.
- G2: Commitments made externally are deliverable and have been confirmed with the team who must deliver them.
- G3: Material carries an owner and a review date; unowned content is retired.
- G4: Confidential, personal or customer-identifying information is removed before publication.
- G5: Antitrust and IPR rules of the body are observed strictly
- G6: commercially sensitive discussion in a standards forum is stopped and reported immediately

**`role/standards-body-representative:4.contract_input_1`** — `object`

- Analyse the specific input "Organisational position and interests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:4.contract_input_2`** — `object`

- Analyse the specific input "Draft standards and working documents" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:4.contract_input_3`** — `object`

- Analyse the specific input "Internal technical impact analysis" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/standards-body-representative:4.contract_input_4`** — `object`

- Analyse the specific input "Legal and antitrust constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/standards-body-representative:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/standards-body-representative:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/standards-body-representative:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/standards-body-representative:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/standards-body-representative:4.irrelevant_detail`** — `object`

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

- **Standards Body Representative:** the relevant body's process (ISO, IETF, W3C, ETSI, OASIS); antitrust and competition law; IPR and patent policy of the body. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
