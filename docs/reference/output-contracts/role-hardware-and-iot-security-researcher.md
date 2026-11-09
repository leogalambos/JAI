<!-- JAI:OUTPUT-CONTRACTS:START -->
# Hardware and IoT Security Researcher: output contracts

Assess the security of physical devices where the attacker has the hardware in their hands

[Full catalogue](index.md)

<a id="output-hardware-and-iot-security-researcher-1"></a>

## Hardware assessment plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Hardware assessment plan.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `hardware-and-iot-security-researcher:1`.

**Required inputs:**

- Authorisation and device ownership
- Devices and documentation
- Lab equipment and safe workspace
- Threat model for the device

**Specification:** `kind/role/hardware-and-iot-security-researcher:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Hardware assessment plan.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/roadmap`](spec-type-roadmap.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `outcome-roadmap`.

Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.

**Evidence accompanying the work product:**

- current/target baseline and planning assumptions
- resource/funding constraints and decision triggers

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/hardware-and-iot-security-researcher:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Hardware assessment plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.receiving_acceptance`** — `array`

- For each receiving role (Embedded Firmware Engineer; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.delivery_verification`** — `array`

- For the specific output 'Hardware assessment plan', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Criteria were fixed before evidence collection and the method is reproducible. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Findings state whether the attack requires physical possession, proximity or remote access, because access prerequisites materially affect likelihood, impact and remediation options
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and device ownership" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.contract_input_2`** — `object`

- Analyse the specific input "Devices and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.contract_input_3`** — `object`

- Analyse the specific input "Lab equipment and safe workspace" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.contract_input_4`** — `object`

- Analyse the specific input "Threat model for the device" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/hardware-and-iot-security-researcher:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/hardware-and-iot-security-researcher:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/hardware-and-iot-security-researcher:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/hardware-and-iot-security-researcher:1.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Hardware and IoT Security Researcher:** OWASP IoT Top 10; IEC 62443 for industrial devices; ETSI EN 303 645 for consumer IoT. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-hardware-and-iot-security-researcher-2"></a>

## firmware extraction and analysis findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: firmware extraction and analysis findings.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `hardware-and-iot-security-researcher:2`.

**Required inputs:**

- Authorisation and device ownership
- Devices and documentation
- Lab equipment and safe workspace
- Threat model for the device

**Specification:** `kind/role/hardware-and-iot-security-researcher:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: firmware extraction and analysis findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/analysis-report`](spec-family-analysis-report.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `evidence-based-analysis-report`.

Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.

**Evidence accompanying the work product:**

- versioned source/period/population and reproducible method
- observations, uncertainty, counterevidence and accountable follow-up

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/hardware-and-iot-security-researcher:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: firmware extraction and analysis findings.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.receiving_acceptance`** — `array`

- For each receiving role (Embedded Firmware Engineer; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.delivery_verification`** — `array`

- For the specific output 'firmware extraction and analysis findings', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Findings state whether the attack requires physical possession, proximity or remote access, because access prerequisites materially affect likelihood, impact and remediation options
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and device ownership" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.contract_input_2`** — `object`

- Analyse the specific input "Devices and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.contract_input_3`** — `object`

- Analyse the specific input "Lab equipment and safe workspace" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.contract_input_4`** — `object`

- Analyse the specific input "Threat model for the device" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/hardware-and-iot-security-researcher:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/hardware-and-iot-security-researcher:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/hardware-and-iot-security-researcher:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/hardware-and-iot-security-researcher:2.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Hardware and IoT Security Researcher:** OWASP IoT Top 10; IEC 62443 for industrial devices; ETSI EN 303 645 for consumer IoT. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-hardware-and-iot-security-researcher-3"></a>

## debug interface and supply chain exposure findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: debug interface and supply chain exposure findings.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `hardware-and-iot-security-researcher:3`.

**Required inputs:**

- Authorisation and device ownership
- Devices and documentation
- Lab equipment and safe workspace
- Threat model for the device

**Specification:** `kind/role/hardware-and-iot-security-researcher:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: debug interface and supply chain exposure findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/analysis-report`](spec-family-analysis-report.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `evidence-based-analysis-report`.

Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.

**Evidence accompanying the work product:**

- versioned source/period/population and reproducible method
- observations, uncertainty, counterevidence and accountable follow-up

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/hardware-and-iot-security-researcher:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: debug interface and supply chain exposure findings.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.receiving_acceptance`** — `array`

- For each receiving role (Embedded Firmware Engineer; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.delivery_verification`** — `array`

- For the specific output 'debug interface and supply chain exposure findings', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Findings state whether the attack requires physical possession, proximity or remote access, because access prerequisites materially affect likelihood, impact and remediation options
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and device ownership" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.contract_input_2`** — `object`

- Analyse the specific input "Devices and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.contract_input_3`** — `object`

- Analyse the specific input "Lab equipment and safe workspace" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.contract_input_4`** — `object`

- Analyse the specific input "Threat model for the device" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/hardware-and-iot-security-researcher:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/hardware-and-iot-security-researcher:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/hardware-and-iot-security-researcher:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/hardware-and-iot-security-researcher:3.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Hardware and IoT Security Researcher:** OWASP IoT Top 10; IEC 62443 for industrial devices; ETSI EN 303 645 for consumer IoT. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-hardware-and-iot-security-researcher-4"></a>

## hardening recommendations

**At a glance**

- **Purpose:** Produce and govern the role deliverable: hardening recommendations.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `hardware-and-iot-security-researcher:4`.

**Required inputs:**

- Authorisation and device ownership
- Devices and documentation
- Lab equipment and safe workspace
- Threat model for the device

**Specification:** `kind/role/hardware-and-iot-security-researcher:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: hardening recommendations.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/analysis-report`](spec-family-analysis-report.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `evidence-based-analysis-report`.

Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.

**Evidence accompanying the work product:**

- versioned source/period/population and reproducible method
- observations, uncertainty, counterevidence and accountable follow-up

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/hardware-and-iot-security-researcher:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: hardening recommendations.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.receiving_acceptance`** — `array`

- For each receiving role (Embedded Firmware Engineer; Security Architect), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.delivery_verification`** — `array`

- For the specific output 'hardening recommendations', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Success and failure criteria are written before the experiment runs.
- G2: Negative results are reported, not quietly abandoned.
- G3: Prototype code is labelled non-production and is never deployed to a production path without a rewrite decision.
- G4: Licensing, export-control, data-protection and ethical constraints are checked before using external data or models.
- G5: Findings state whether the attack requires physical possession, proximity or remote access, because access prerequisites materially affect likelihood, impact and remediation options
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.contract_input_1`** — `object`

- Analyse the specific input "Authorisation and device ownership" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.contract_input_2`** — `object`

- Analyse the specific input "Devices and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.contract_input_3`** — `object`

- Analyse the specific input "Lab equipment and safe workspace" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.contract_input_4`** — `object`

- Analyse the specific input "Threat model for the device" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/hardware-and-iot-security-researcher:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/hardware-and-iot-security-researcher:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/hardware-and-iot-security-researcher:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/hardware-and-iot-security-researcher:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/hardware-and-iot-security-researcher:4.irrelevant_detail`** — `object`

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
- **[NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls](https://doi.org/10.6028/NIST.SP.800-53Ar5)** — Assessment objectives, methods, evidence, findings and bounded assessment conclusions. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Hardware and IoT Security Researcher:** OWASP IoT Top 10; IEC 62443 for industrial devices; ETSI EN 303 645 for consumer IoT. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
