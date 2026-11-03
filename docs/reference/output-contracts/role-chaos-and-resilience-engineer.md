<!-- JAI:OUTPUT-CONTRACTS:START -->
# Chaos and Resilience Engineer: output contracts

Prove the system survives the failures it claims to survive, under controlled conditions

[Full catalogue](index.md)

<a id="output-chaos-and-resilience-engineer-1"></a>

## Failure hypothesis and experiment design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Failure hypothesis and experiment design.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chaos-and-resilience-engineer:1`.

**Required inputs:**

- Architecture and dependency map
- Service level objectives
- Incident history
- Business criticality windows

**Specification:** `kind/role/chaos-and-resilience-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Failure hypothesis and experiment design.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chaos-and-resilience-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Failure hypothesis and experiment design.

**`role/chaos-and-resilience-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Problem Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/chaos-and-resilience-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/chaos-and-resilience-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/chaos-and-resilience-engineer:1.delivery_verification`** — `array`

- For the specific output 'Failure hypothesis and experiment design', provide verifiable evidence satisfying: Defines steady state, failure hypothesis, authorised scope, blast radius, stop criteria, recovery and observable success/failure measures. Required delivery form: Predeclared resilience experiment protocol.

**`role/chaos-and-resilience-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Failure hypothesis and experiment design") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every experiment defines steady state, blast radius, abort conditions and a tested stop mechanism before it runs, and business owners are informed

**`role/chaos-and-resilience-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Architecture and dependency map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Service level objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Incident history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Business criticality windows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/chaos-and-resilience-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/chaos-and-resilience-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/chaos-and-resilience-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/chaos-and-resilience-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chaos-and-resilience-engineer:1.irrelevant_detail`** — `object`

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

- **Chaos and Resilience Engineer:** chaos engineering principles; Google SRE practice; ISO 22301 exercising guidance. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-chaos-and-resilience-engineer-2"></a>

## game day plan and results

**At a glance**

- **Purpose:** Produce and govern the role deliverable: game day plan and results.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chaos-and-resilience-engineer:2`.

**Required inputs:**

- Architecture and dependency map
- Service level objectives
- Incident history
- Business criticality windows

**Specification:** `kind/role/chaos-and-resilience-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: game day plan and results.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/roadmap`](spec-type-roadmap.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chaos-and-resilience-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: game day plan and results.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Problem Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.delivery_verification`** — `array`

- For the specific output 'game day plan and results', provide verifiable evidence satisfying: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Document with milestones, owners, dependencies and assumptions.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Failure hypothesis and experiment design") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every experiment defines steady state, blast radius, abort conditions and a tested stop mechanism before it runs, and business owners are informed
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Architecture and dependency map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Service level objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Incident history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Business criticality windows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/chaos-and-resilience-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

**`role/chaos-and-resilience-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/chaos-and-resilience-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/chaos-and-resilience-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chaos-and-resilience-engineer:2.irrelevant_detail`** — `object`

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

- **Chaos and Resilience Engineer:** chaos engineering principles; Google SRE practice; ISO 22301 exercising guidance. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-chaos-and-resilience-engineer-3"></a>

## resilience gap findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: resilience gap findings.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chaos-and-resilience-engineer:3`.

**Required inputs:**

- Architecture and dependency map
- Service level objectives
- Incident history
- Business criticality windows

**Specification:** `kind/role/chaos-and-resilience-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: resilience gap findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chaos-and-resilience-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: resilience gap findings.

**`role/chaos-and-resilience-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Problem Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/chaos-and-resilience-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/chaos-and-resilience-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/chaos-and-resilience-engineer:3.delivery_verification`** — `array`

- For the specific output 'resilience gap findings', provide verifiable evidence satisfying: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Finding record with reproducible evidence and risk rating.

**`role/chaos-and-resilience-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Failure hypothesis and experiment design") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every experiment defines steady state, blast radius, abort conditions and a tested stop mechanism before it runs, and business owners are informed

**`role/chaos-and-resilience-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Architecture and dependency map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Service level objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Incident history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Business criticality windows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/chaos-and-resilience-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/chaos-and-resilience-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/chaos-and-resilience-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/chaos-and-resilience-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chaos-and-resilience-engineer:3.irrelevant_detail`** — `object`

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

- **Chaos and Resilience Engineer:** chaos engineering principles; Google SRE practice; ISO 22301 exercising guidance. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-chaos-and-resilience-engineer-4"></a>

## steady-state and blast-radius definitions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: steady-state and blast-radius definitions.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `chaos-and-resilience-engineer:4`.

**Required inputs:**

- Architecture and dependency map
- Service level objectives
- Incident history
- Business criticality windows

**Specification:** `kind/role/chaos-and-resilience-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: steady-state and blast-radius definitions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/chaos-and-resilience-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: steady-state and blast-radius definitions.

**`role/chaos-and-resilience-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Problem Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/chaos-and-resilience-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/chaos-and-resilience-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/chaos-and-resilience-engineer:4.delivery_verification`** — `array`

- For the specific output 'steady-state and blast-radius definitions', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/chaos-and-resilience-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Exit criteria are agreed before execution starts and are not renegotiated during the crunch without a recorded decision.
- G2: Residual risk is stated in business terms and accepted by a named person before release.
- G3: No production personal data is used in test environments without an approved lawful basis and masking.
- G4: An intermittent test failure is investigated as a timing, ordering or shared-state defect, never retried or quarantined away without a ticket and an analysis (it-role-library/standards/defect-analysis.md).
- G5: Automated tests are deterministic, test one behaviour each, mock only collaborators and run integration tests against real dependencies (it-role-library/standards/testing.md).
- G6: The primary deliverable ("Failure hypothesis and experiment design") distinguishes what was tested, what was not tested and what cannot be tested.
- G7: Every experiment defines steady state, blast radius, abort conditions and a tested stop mechanism before it runs, and business owners are informed

**`role/chaos-and-resilience-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Architecture and dependency map" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Service level objectives" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Incident history" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/chaos-and-resilience-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Business criticality windows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/chaos-and-resilience-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/chaos-and-resilience-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/chaos-and-resilience-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/chaos-and-resilience-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/chaos-and-resilience-engineer:4.irrelevant_detail`** — `object`

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

- **Chaos and Resilience Engineer:** chaos engineering principles; Google SRE practice; ISO 22301 exercising guidance. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
