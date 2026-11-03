<!-- JAI:OUTPUT-CONTRACTS:START -->
# Release Quality Gatekeeper: output contracts

Hold the line on release quality in regulated environments where evidence, not opinion, decides

[Full catalogue](index.md)

<a id="output-release-quality-gatekeeper-1"></a>

## Release evidence pack

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Release evidence pack.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `release-quality-gatekeeper:1`.

**Required inputs:**

- Validation and verification evidence
- Change and configuration records
- Regulatory requirements
- Risk assessment

**Specification:** `kind/role/release-quality-gatekeeper:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Release evidence pack.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/release-quality-gatekeeper:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Release evidence pack.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.receiving_acceptance`** — `array`

- For each receiving role (Release Engineer; Internal IT Auditor), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.delivery_verification`** — `array`

- For the specific output 'Release evidence pack', provide verifiable evidence satisfying: Chain of custody is unbroken and the set is reproducible from the record. Required delivery form: Immutable evidence set with hashes, timestamps and custody record.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Release evidence pack") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Release is refused where evidence is incomplete, regardless of commercial pressure
- G8: every waiver names the approver, the risk and the expiry
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.contract_input_1`** — `object`

- Analyse the specific input "Validation and verification evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.contract_input_2`** — `object`

- Analyse the specific input "Change and configuration records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.contract_input_3`** — `object`

- Analyse the specific input "Regulatory requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.contract_input_4`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/release-quality-gatekeeper:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

**`role/release-quality-gatekeeper:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/release-quality-gatekeeper:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/release-quality-gatekeeper:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/release-quality-gatekeeper:1.irrelevant_detail`** — `object`

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

### Role framework context

- **Release Quality Gatekeeper:** GxP computerised systems validation (GAMP 5); IEC 62304 for medical device software; ISO 13485 where applicable. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-release-quality-gatekeeper-2"></a>

## gate decision record

**At a glance**

- **Purpose:** Produce and govern the role deliverable: gate decision record.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `release-quality-gatekeeper:2`.

**Required inputs:**

- Validation and verification evidence
- Change and configuration records
- Regulatory requirements
- Risk assessment

**Specification:** `kind/role/release-quality-gatekeeper:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: gate decision record.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/release-quality-gatekeeper:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: gate decision record.

**`role/release-quality-gatekeeper:2.receiving_acceptance`** — `array`

- For each receiving role (Release Engineer; Internal IT Auditor), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/release-quality-gatekeeper:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/release-quality-gatekeeper:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/release-quality-gatekeeper:2.delivery_verification`** — `array`

- For the specific output 'gate decision record', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/release-quality-gatekeeper:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Release evidence pack") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Release is refused where evidence is incomplete, regardless of commercial pressure
- G8: every waiver names the approver, the risk and the expiry

**`role/release-quality-gatekeeper:2.contract_input_1`** — `object`

- Analyse the specific input "Validation and verification evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:2.contract_input_2`** — `object`

- Analyse the specific input "Change and configuration records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:2.contract_input_3`** — `object`

- Analyse the specific input "Regulatory requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:2.contract_input_4`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/release-quality-gatekeeper:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/release-quality-gatekeeper:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/release-quality-gatekeeper:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/release-quality-gatekeeper:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/release-quality-gatekeeper:2.irrelevant_detail`** — `object`

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

- **Release Quality Gatekeeper:** GxP computerised systems validation (GAMP 5); IEC 62304 for medical device software; ISO 13485 where applicable. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-release-quality-gatekeeper-3"></a>

## deviation and waiver register

**At a glance**

- **Purpose:** Produce and govern the role deliverable: deviation and waiver register.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `release-quality-gatekeeper:3`.

**Required inputs:**

- Validation and verification evidence
- Change and configuration records
- Regulatory requirements
- Risk assessment

**Specification:** `kind/role/release-quality-gatekeeper:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: deviation and waiver register.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/release-quality-gatekeeper:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: deviation and waiver register.

**`role/release-quality-gatekeeper:3.receiving_acceptance`** — `array`

- For each receiving role (Release Engineer; Internal IT Auditor), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/release-quality-gatekeeper:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/release-quality-gatekeeper:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/release-quality-gatekeeper:3.delivery_verification`** — `array`

- For the specific output 'deviation and waiver register', provide verifiable evidence satisfying: Every row has an owner, a date, a status and a next action. Required delivery form: Structured table in the system of record (CSV/tool export).

**`role/release-quality-gatekeeper:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Release evidence pack") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Release is refused where evidence is incomplete, regardless of commercial pressure
- G8: every waiver names the approver, the risk and the expiry

**`role/release-quality-gatekeeper:3.contract_input_1`** — `object`

- Analyse the specific input "Validation and verification evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:3.contract_input_2`** — `object`

- Analyse the specific input "Change and configuration records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:3.contract_input_3`** — `object`

- Analyse the specific input "Regulatory requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:3.contract_input_4`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/release-quality-gatekeeper:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/release-quality-gatekeeper:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/release-quality-gatekeeper:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/release-quality-gatekeeper:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/release-quality-gatekeeper:3.irrelevant_detail`** — `object`

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

- **Release Quality Gatekeeper:** GxP computerised systems validation (GAMP 5); IEC 62304 for medical device software; ISO 13485 where applicable. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-release-quality-gatekeeper-4"></a>

## regulatory traceability matrix

**At a glance**

- **Purpose:** Produce and govern the role deliverable: regulatory traceability matrix.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `release-quality-gatekeeper:4`.

**Required inputs:**

- Validation and verification evidence
- Change and configuration records
- Regulatory requirements
- Risk assessment

**Specification:** `kind/role/release-quality-gatekeeper:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: regulatory traceability matrix.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/release-quality-gatekeeper:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: regulatory traceability matrix.

**`role/release-quality-gatekeeper:4.receiving_acceptance`** — `array`

- For each receiving role (Release Engineer; Internal IT Auditor), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/release-quality-gatekeeper:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/release-quality-gatekeeper:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/release-quality-gatekeeper:4.delivery_verification`** — `array`

- For the specific output 'regulatory traceability matrix', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/release-quality-gatekeeper:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Release evidence pack") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Release is refused where evidence is incomplete, regardless of commercial pressure
- G8: every waiver names the approver, the risk and the expiry

**`role/release-quality-gatekeeper:4.contract_input_1`** — `object`

- Analyse the specific input "Validation and verification evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:4.contract_input_2`** — `object`

- Analyse the specific input "Change and configuration records" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:4.contract_input_3`** — `object`

- Analyse the specific input "Regulatory requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/release-quality-gatekeeper:4.contract_input_4`** — `object`

- Analyse the specific input "Risk assessment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/release-quality-gatekeeper:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/release-quality-gatekeeper:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/release-quality-gatekeeper:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/release-quality-gatekeeper:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/release-quality-gatekeeper:4.irrelevant_detail`** — `object`

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

- **Release Quality Gatekeeper:** GxP computerised systems validation (GAMP 5); IEC 62304 for medical device software; ISO 13485 where applicable. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
