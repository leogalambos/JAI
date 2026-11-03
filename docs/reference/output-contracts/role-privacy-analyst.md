<!-- JAI:OUTPUT-CONTRACTS:START -->
# Privacy Analyst: output contracts

Do the detailed privacy work: assessments, records, rights requests and advice on new processing

[Full catalogue](index.md)

<a id="output-privacy-analyst-1"></a>

## Data protection impact assessments

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Data protection impact assessments.
- **Mandatory examples:** Link assets, causes, events, consequences and inherent/residual ratings to evidence. Define scope, likelihood, impact scales and applicable risk appetite. Assign treatments, deadlines, risk owners and residual acceptance authority.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-analyst:1`.

**Required inputs:**

- Proposed processing and system designs
- Data flows and inventory
- Legal position
- Rights requests

**Specification:** `kind/role/privacy-analyst:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Data protection impact assessments.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/risk-assessment`](spec-type-risk-assessment.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-analyst:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Data protection impact assessments.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; project teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.delivery_verification`** — `array`

- For the specific output 'Data protection impact assessments', provide verifiable evidence satisfying: Criteria were fixed before evidence collection and the method is reproducible. Required delivery form: Structured assessment document with scoring method stated.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Data protection impact assessments") has been walked through with the people who will build, test and operate the result.
- G5: A DPIA is completed before processing begins where the risk threshold is met
- G6: a retrospective DPIA is recorded as a compliance failure, not as completion
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.contract_input_1`** — `object`

- Analyse the specific input "Proposed processing and system designs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.contract_input_2`** — `object`

- Analyse the specific input "Data flows and inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.contract_input_3`** — `object`

- Analyse the specific input "Legal position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.contract_input_4`** — `object`

- Analyse the specific input "Rights requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.processing_description`** — `object`

- Describe the envisaged processing operations, purposes, categories of data/subjects, recipients, retention and relevant data flows; identify controller and applicable jurisdiction.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.necessity_proportionality`** — `object`

- Assess necessity and proportionality of processing in relation to its purpose, less intrusive alternatives and data-minimisation/retention choices using the actual proposal.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.data_subject_risks`** — `array`

- Describe risks to the rights and freedoms of affected people, including who may be harmed, likelihood, severity, assumptions and supporting evidence; business risk alone is insufficient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.privacy_safeguards`** — `array`

- Map each material rights/freedoms risk to proposed safeguards, responsible owner, verification evidence and remaining exposure; record DPO advice where sought and any decision or consultation still required without implying permission to process.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/privacy-analyst:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

**`role/privacy-analyst:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/privacy-analyst:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-30r1); [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/privacy-analyst:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-analyst:1.irrelevant_detail`** — `object`

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

- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Regulation (EU) 2016/679, Article 35 — Data protection impact assessment](https://eur-lex.europa.eu/eli/reg/2016/679/oj)** — Article 35 assessment content and accountability where EU GDPR applies; engagement-specific legal applicability and competent interpretation must be established. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Privacy Analyst:** GDPR; ISO/IEC 27701; EDPB guidance; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-privacy-analyst-2"></a>

## records of processing activity entries

**At a glance**

- **Purpose:** Produce and govern the role deliverable: records of processing activity entries.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-analyst:2`.

**Required inputs:**

- Proposed processing and system designs
- Data flows and inventory
- Legal position
- Rights requests

**Specification:** `kind/role/privacy-analyst:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: records of processing activity entries.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-analyst:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: records of processing activity entries.

**`role/privacy-analyst:2.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; project teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/privacy-analyst:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/privacy-analyst:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/privacy-analyst:2.delivery_verification`** — `array`

- For the specific output 'records of processing activity entries', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/privacy-analyst:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Data protection impact assessments") has been walked through with the people who will build, test and operate the result.
- G5: A DPIA is completed before processing begins where the risk threshold is met
- G6: a retrospective DPIA is recorded as a compliance failure, not as completion

**`role/privacy-analyst:2.contract_input_1`** — `object`

- Analyse the specific input "Proposed processing and system designs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:2.contract_input_2`** — `object`

- Analyse the specific input "Data flows and inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:2.contract_input_3`** — `object`

- Analyse the specific input "Legal position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:2.contract_input_4`** — `object`

- Analyse the specific input "Rights requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/privacy-analyst:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/privacy-analyst:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/privacy-analyst:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/privacy-analyst:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-analyst:2.irrelevant_detail`** — `object`

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

- **Privacy Analyst:** GDPR; ISO/IEC 27701; EDPB guidance; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-privacy-analyst-3"></a>

## data subject rights request handling

**At a glance**

- **Purpose:** Produce and govern the role deliverable: data subject rights request handling.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-analyst:3`.

**Required inputs:**

- Proposed processing and system designs
- Data flows and inventory
- Legal position
- Rights requests

**Specification:** `kind/role/privacy-analyst:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: data subject rights request handling.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-analyst:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: data subject rights request handling.

**`role/privacy-analyst:3.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; project teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/privacy-analyst:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/privacy-analyst:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/privacy-analyst:3.delivery_verification`** — `array`

- For the specific output 'data subject rights request handling', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/privacy-analyst:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Data protection impact assessments") has been walked through with the people who will build, test and operate the result.
- G5: A DPIA is completed before processing begins where the risk threshold is met
- G6: a retrospective DPIA is recorded as a compliance failure, not as completion

**`role/privacy-analyst:3.contract_input_1`** — `object`

- Analyse the specific input "Proposed processing and system designs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:3.contract_input_2`** — `object`

- Analyse the specific input "Data flows and inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:3.contract_input_3`** — `object`

- Analyse the specific input "Legal position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:3.contract_input_4`** — `object`

- Analyse the specific input "Rights requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/privacy-analyst:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/privacy-analyst:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/privacy-analyst:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/privacy-analyst:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-analyst:3.irrelevant_detail`** — `object`

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

- **Privacy Analyst:** GDPR; ISO/IEC 27701; EDPB guidance; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-privacy-analyst-4"></a>

## privacy notices and consent design input

**At a glance**

- **Purpose:** Produce and govern the role deliverable: privacy notices and consent design input.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `privacy-analyst:4`.

**Required inputs:**

- Proposed processing and system designs
- Data flows and inventory
- Legal position
- Rights requests

**Specification:** `kind/role/privacy-analyst:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: privacy notices and consent design input.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/privacy-analyst:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: privacy notices and consent design input.

**`role/privacy-analyst:4.receiving_acceptance`** — `array`

- For each receiving role (Data Privacy Engineer; project teams), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/privacy-analyst:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/privacy-analyst:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/privacy-analyst:4.delivery_verification`** — `array`

- For the specific output 'privacy notices and consent design input', provide verifiable evidence satisfying: States processing purposes, required disclosures, lawful-basis assumptions, consent choices and unresolved legal or DPO advice. Required delivery form: Privacy notice and consent design input.

**`role/privacy-analyst:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Every requirement is atomic, testable, prioritised and traced to a named source.
- G2: Conflicting stakeholder positions are recorded as open conflicts, never averaged into a vague compromise.
- G3: Assumptions and constraints are listed separately from requirements and each has an owner.
- G4: The primary deliverable ("Data protection impact assessments") has been walked through with the people who will build, test and operate the result.
- G5: A DPIA is completed before processing begins where the risk threshold is met
- G6: a retrospective DPIA is recorded as a compliance failure, not as completion

**`role/privacy-analyst:4.contract_input_1`** — `object`

- Analyse the specific input "Proposed processing and system designs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:4.contract_input_2`** — `object`

- Analyse the specific input "Data flows and inventory" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:4.contract_input_3`** — `object`

- Analyse the specific input "Legal position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/privacy-analyst:4.contract_input_4`** — `object`

- Analyse the specific input "Rights requests" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/privacy-analyst:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/privacy-analyst:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/privacy-analyst:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/privacy-analyst:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/privacy-analyst:4.irrelevant_detail`** — `object`

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

- **Privacy Analyst:** GDPR; ISO/IEC 27701; EDPB guidance; NIST Privacy Framework. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
