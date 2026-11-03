<!-- JAI:OUTPUT-CONTRACTS:START -->
# Binary Reverse Engineer: output contracts

Understand undocumented software or hardware behaviour from its compiled form, lawfully

[Full catalogue](index.md)

<a id="output-binary-reverse-engineer-1"></a>

## Reverse engineering analysis notes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Reverse engineering analysis notes.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `binary-reverse-engineer:1`.

**Required inputs:**

- Authorisation and licence position
- Target binaries or firmware
- Analysis environment
- Analysis objective

**Specification:** `kind/role/binary-reverse-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Reverse engineering analysis notes.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/binary-reverse-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Reverse engineering analysis notes.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Malware Analyst; Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.delivery_verification`** — `array`

- For the specific output 'Reverse engineering analysis notes', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: The legal basis for reverse engineering (interoperability, security research, licence terms, jurisdiction) is confirmed in writing before work starts
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and licence position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Target binaries or firmware" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Analysis environment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Analysis objective" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/binary-reverse-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/binary-reverse-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/binary-reverse-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/binary-reverse-engineer:1.irrelevant_detail`** — `object`

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

- **Binary Reverse Engineer:** applicable copyright and interoperability law; reverse engineering methodology; safe handling practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-binary-reverse-engineer-2"></a>

## behaviour and protocol documentation

**At a glance**

- **Purpose:** Produce and govern the role deliverable: behaviour and protocol documentation.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `binary-reverse-engineer:2`.

**Required inputs:**

- Authorisation and licence position
- Target binaries or firmware
- Analysis environment
- Analysis objective

**Specification:** `kind/role/binary-reverse-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: behaviour and protocol documentation.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/binary-reverse-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: behaviour and protocol documentation.

**`role/binary-reverse-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Malware Analyst; Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/binary-reverse-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/binary-reverse-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/binary-reverse-engineer:2.delivery_verification`** — `array`

- For the specific output 'behaviour and protocol documentation', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/binary-reverse-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: The legal basis for reverse engineering (interoperability, security research, licence terms, jurisdiction) is confirmed in writing before work starts

**`role/binary-reverse-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and licence position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/binary-reverse-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Target binaries or firmware" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/binary-reverse-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Analysis environment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/binary-reverse-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Analysis objective" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/binary-reverse-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/binary-reverse-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/binary-reverse-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/binary-reverse-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/binary-reverse-engineer:2.irrelevant_detail`** — `object`

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

- **Binary Reverse Engineer:** applicable copyright and interoperability law; reverse engineering methodology; safe handling practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-binary-reverse-engineer-3"></a>

## interoperability or security findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: interoperability or security findings.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `binary-reverse-engineer:3`.

**Required inputs:**

- Authorisation and licence position
- Target binaries or firmware
- Analysis environment
- Analysis objective

**Specification:** `kind/role/binary-reverse-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: interoperability or security findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/binary-reverse-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: interoperability or security findings.

**`role/binary-reverse-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Malware Analyst; Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/binary-reverse-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/binary-reverse-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/binary-reverse-engineer:3.delivery_verification`** — `array`

- For the specific output 'interoperability or security findings', provide verifiable evidence satisfying: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Finding record with reproducible evidence and risk rating.

**`role/binary-reverse-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: The legal basis for reverse engineering (interoperability, security research, licence terms, jurisdiction) is confirmed in writing before work starts

**`role/binary-reverse-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and licence position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/binary-reverse-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Target binaries or firmware" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/binary-reverse-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Analysis environment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/binary-reverse-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Analysis objective" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/binary-reverse-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/binary-reverse-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/binary-reverse-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/binary-reverse-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/binary-reverse-engineer:3.irrelevant_detail`** — `object`

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

- **Binary Reverse Engineer:** applicable copyright and interoperability law; reverse engineering methodology; safe handling practice. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-binary-reverse-engineer-4"></a>

## tooling and scripts for repeat analysis

**At a glance**

- **Purpose:** Produce and govern the role deliverable: tooling and scripts for repeat analysis.
- **Mandatory examples:** Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision. Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints. Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `binary-reverse-engineer:4`.

**Required inputs:**

- Authorisation and licence position
- Target binaries or firmware
- Analysis environment
- Analysis objective

**Specification:** `kind/role/binary-reverse-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: tooling and scripts for repeat analysis.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/software-change`](spec-family-software-change.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/binary-reverse-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: tooling and scripts for repeat analysis.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Malware Analyst; Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.delivery_verification`** — `array`

- For the specific output 'tooling and scripts for repeat analysis', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: The legal basis for reverse engineering (interoperability, security research, licence terms, jurisdiction) is confirmed in writing before work starts
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and licence position" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Target binaries or firmware" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Analysis environment" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Analysis objective" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/binary-reverse-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

**`role/binary-reverse-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/binary-reverse-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/binary-reverse-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/binary-reverse-engineer:4.irrelevant_detail`** — `object`

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

- **[NIST SP 800-218, Secure Software Development Framework Version 1.1](https://doi.org/10.6028/NIST.SP.800-218)** — Secure development practices, protected source/build inputs, verification and vulnerability response. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Binary Reverse Engineer:** applicable copyright and interoperability law; reverse engineering methodology; safe handling practice. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
