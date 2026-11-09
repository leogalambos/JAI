<!-- JAI:OUTPUT-CONTRACTS:START -->
# Demand & Intake Manager: output contracts

Own the controlled entry of demand into the IS/IT portfolio: qualification, duplication/capability fit, minimum evidence, sizing readiness, risk/value framing and transparent prioritisation handoff.

[Full catalogue](index.md)

<a id="output-demand-and-intake-manager-1"></a>

## Demand and intake register

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Demand and intake register.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `demand-and-intake-manager:1`.

**Required inputs:**

- Business demand/problem statement and owner
- Strategic/capability priorities
- Current portfolio and roadmap
- Architecture/security/data constraints
- Sizing/capacity/funding signals

**Specification:** `kind/role/demand-and-intake-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Demand and intake register.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `governed-register`.

Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.

**Evidence accompanying the work product:**

- actual source-attributed records
- uniqueness, completeness and relationship reconciliation

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/demand-and-intake-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Demand and intake register.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Business Analyst; Enterprise Architect; Portfolio Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required; exceptions -> owner + expiry/review.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.delivery_verification`** — `array`

- For the specific output 'Demand and intake register', provide verifiable evidence satisfying: Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules. Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population. Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness. Existing source requirement: Every demand item has a business owner, outcome, current state and auditable disposition; duplicates and redirected items remain traceable. Required delivery form: Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Scope, decision right, owner and affected enterprise boundary are explicit.
- G2: Mandatory evidence is attributable, current enough for the decision and contradictions are visible.
- G3: Options/trade-offs and material dependencies are represented; the preferred path is not presented as inevitable.
- G4: No role both produces and independently assures/approves the same consequential evidence without a recorded compensating control.
- G5: Receiving roles, acceptance criteria, residual risks and reopen triggers are named.
- G6: The authoritative system(s) of record and review/expiry conditions are identified.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Business demand/problem statement and owner" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Strategic/capability priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Current portfolio and roadmap" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Architecture/security/data constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.contract_input_5`** — `object`

- Analyse the specific input "Sizing/capacity/funding signals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/demand-and-intake-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/demand-and-intake-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/demand-and-intake-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/demand-and-intake-manager:1.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Demand & Intake Manager:** COBIT portfolio/demand concepts; ITIL 4 relationship and portfolio practices; Lean portfolio management concepts; TOGAF capability-based planning concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-demand-and-intake-manager-2"></a>

## Demand qualification and impact assessment

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Demand qualification and impact assessment.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `demand-and-intake-manager:2`.

**Required inputs:**

- Business demand/problem statement and owner
- Strategic/capability priorities
- Current portfolio and roadmap
- Architecture/security/data constraints
- Sizing/capacity/funding signals

**Specification:** `kind/role/demand-and-intake-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Demand qualification and impact assessment.

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

**`role/demand-and-intake-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Demand qualification and impact assessment.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Business Analyst; Enterprise Architect; Portfolio Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required; exceptions -> owner + expiry/review.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.delivery_verification`** — `array`

- For the specific output 'Demand qualification and impact assessment', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Items advance only when the minimum evidence for their decision class is present or an explicit exception is owned. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Scope, decision right, owner and affected enterprise boundary are explicit.
- G2: Mandatory evidence is attributable, current enough for the decision and contradictions are visible.
- G3: Options/trade-offs and material dependencies are represented; the preferred path is not presented as inevitable.
- G4: No role both produces and independently assures/approves the same consequential evidence without a recorded compensating control.
- G5: Receiving roles, acceptance criteria, residual risks and reopen triggers are named.
- G6: The authoritative system(s) of record and review/expiry conditions are identified.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Business demand/problem statement and owner" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Strategic/capability priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Current portfolio and roadmap" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Architecture/security/data constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.contract_input_5`** — `object`

- Analyse the specific input "Sizing/capacity/funding signals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/demand-and-intake-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/demand-and-intake-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/demand-and-intake-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/demand-and-intake-manager:2.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Demand & Intake Manager:** COBIT portfolio/demand concepts; ITIL 4 relationship and portfolio practices; Lean portfolio management concepts; TOGAF capability-based planning concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-demand-and-intake-manager-3"></a>

## Prioritisation and routing decision paper

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Prioritisation and routing decision paper.
- **Mandatory examples:** Identify the specific choice, accountable authority and decision deadline. Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation. Compare viable options including the do-nothing baseline against common criteria.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `demand-and-intake-manager:3`.

**Required inputs:**

- Business demand/problem statement and owner
- Strategic/capability priorities
- Current portfolio and roadmap
- Architecture/security/data constraints
- Sizing/capacity/funding signals

**Specification:** `kind/role/demand-and-intake-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Prioritisation and routing decision paper.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/decision-paper`](spec-type-decision-paper.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `decision-paper`.

Bounded decision paper with consistent option comparison and a clear authority/decision request.

**Evidence accompanying the work product:**

- baseline and feasible alternatives
- cost/benefit/uncertainty and consequences

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/demand-and-intake-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Prioritisation and routing decision paper.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Business Analyst; Enterprise Architect; Portfolio Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required; exceptions -> owner + expiry/review.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.delivery_verification`** — `array`

- For the specific output 'Prioritisation and routing decision paper', provide verifiable evidence satisfying: Separate the requested decision from information for noting; state decision scope, eligible authority, deadline and consequences of deferral. List feasible options with consistent evaluation criteria, evidence, costs, benefits and constraints; justify any unavailable baseline. State recommendation, implementation dependencies, uncertainty and residual exposure; show which assumptions would change the preferred option. Existing source requirement: The recommendation is reproducible from declared criteria and records conflicts, assumptions and authority. Required delivery form: Bounded decision paper with consistent option comparison and a clear authority/decision request.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Scope, decision right, owner and affected enterprise boundary are explicit.
- G2: Mandatory evidence is attributable, current enough for the decision and contradictions are visible.
- G3: Options/trade-offs and material dependencies are represented; the preferred path is not presented as inevitable.
- G4: No role both produces and independently assures/approves the same consequential evidence without a recorded compensating control.
- G5: Receiving roles, acceptance criteria, residual risks and reopen triggers are named.
- G6: The authoritative system(s) of record and review/expiry conditions are identified.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Business demand/problem statement and owner" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Strategic/capability priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Current portfolio and roadmap" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Architecture/security/data constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.contract_input_5`** — `object`

- Analyse the specific input "Sizing/capacity/funding signals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/demand-and-intake-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/demand-and-intake-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/demand-and-intake-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/demand-and-intake-manager:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Demand & Intake Manager:** COBIT portfolio/demand concepts; ITIL 4 relationship and portfolio practices; Lean portfolio management concepts; TOGAF capability-based planning concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-demand-and-intake-manager-4"></a>

## Intake-to-portfolio commitment roadmap

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Intake-to-portfolio commitment roadmap.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `demand-and-intake-manager:4`.

**Required inputs:**

- Business demand/problem statement and owner
- Strategic/capability priorities
- Current portfolio and roadmap
- Architecture/security/data constraints
- Sizing/capacity/funding signals

**Specification:** `kind/role/demand-and-intake-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Intake-to-portfolio commitment roadmap.

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

**`role/demand-and-intake-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Intake-to-portfolio commitment roadmap.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Business Analyst; Enterprise Architect; Portfolio Manager), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required; exceptions -> owner + expiry/review.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.delivery_verification`** — `array`

- For the specific output 'Intake-to-portfolio commitment roadmap', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Portfolio handoff is explicit; no item is presented as committed before funding/capacity authority has acted. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Scope, decision right, owner and affected enterprise boundary are explicit.
- G2: Mandatory evidence is attributable, current enough for the decision and contradictions are visible.
- G3: Options/trade-offs and material dependencies are represented; the preferred path is not presented as inevitable.
- G4: No role both produces and independently assures/approves the same consequential evidence without a recorded compensating control.
- G5: Receiving roles, acceptance criteria, residual risks and reopen triggers are named.
- G6: The authoritative system(s) of record and review/expiry conditions are identified.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Business demand/problem statement and owner" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Strategic/capability priorities" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Current portfolio and roadmap" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Architecture/security/data constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.contract_input_5`** — `object`

- Analyse the specific input "Sizing/capacity/funding signals" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/demand-and-intake-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

**`role/demand-and-intake-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/demand-and-intake-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/demand-and-intake-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/demand-and-intake-manager:4.irrelevant_detail`** — `object`

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
- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Demand & Intake Manager:** COBIT portfolio/demand concepts; ITIL 4 relationship and portfolio practices; Lean portfolio management concepts; TOGAF capability-based planning concepts. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
