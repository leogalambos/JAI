<!-- JAI:OUTPUT-CONTRACTS:START -->
# Internal IT Auditor: output contracts

Give independent, evidence-based assurance about whether controls are designed and operating properly

[Full catalogue](index.md)

<a id="output-internal-it-auditor-1"></a>

## Audit plan and engagement scope

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Audit plan and engagement scope.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `internal-it-auditor:1`.

**Required inputs:**

- Risk-based audit universe
- Control documentation
- System-generated evidence
- Prior findings

**Specification:** `kind/role/internal-it-auditor:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Audit plan and engagement scope.

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

**`role/internal-it-auditor:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Audit plan and engagement scope.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; Compliance Officer (Technology)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.delivery_verification`** — `array`

- For the specific output 'Audit plan and engagement scope', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Independence is declared and preserved
- G6: where the auditor previously operated the control, the engagement is reassigned rather than disclosed and continued
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.contract_input_1`** — `object`

- Analyse the specific input "Risk-based audit universe" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.contract_input_2`** — `object`

- Analyse the specific input "Control documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.contract_input_3`** — `object`

- Analyse the specific input "System-generated evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.contract_input_4`** — `object`

- Analyse the specific input "Prior findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/internal-it-auditor:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/internal-it-auditor:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/internal-it-auditor:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/internal-it-auditor:1.irrelevant_detail`** — `object`

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

- **Internal IT Auditor:** IIA Global Internal Audit Standards; ISACA IT audit framework and COBIT 2019; ISO 19011. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate binding obligation, interpretation, control, evidence, independent test and bounded assurance/risk conclusion.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-internal-it-auditor-2"></a>

## audit working papers and evidence

**At a glance**

- **Purpose:** Produce and govern the role deliverable: audit working papers and evidence.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `internal-it-auditor:2`.

**Required inputs:**

- Risk-based audit universe
- Control documentation
- System-generated evidence
- Prior findings

**Specification:** `kind/role/internal-it-auditor:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: audit working papers and evidence.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `assurance-assessment`.

Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.

**Evidence accompanying the work product:**

- criterion-to-test-to-observation traceability
- independent reviewer and limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/internal-it-auditor:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: audit working papers and evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; Compliance Officer (Technology)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.delivery_verification`** — `array`

- For the specific output 'audit working papers and evidence', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Existing source requirement: Chain of custody is unbroken and the set is reproducible from the record. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Independence is declared and preserved
- G6: where the auditor previously operated the control, the engagement is reassigned rather than disclosed and continued
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.contract_input_1`** — `object`

- Analyse the specific input "Risk-based audit universe" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.contract_input_2`** — `object`

- Analyse the specific input "Control documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.contract_input_3`** — `object`

- Analyse the specific input "System-generated evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.contract_input_4`** — `object`

- Analyse the specific input "Prior findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/internal-it-auditor:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/internal-it-auditor:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/internal-it-auditor:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/internal-it-auditor:2.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Internal IT Auditor:** IIA Global Internal Audit Standards; ISACA IT audit framework and COBIT 2019; ISO 19011. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate binding obligation, interpretation, control, evidence, independent test and bounded assurance/risk conclusion.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-internal-it-auditor-3"></a>

## audit report with findings and ratings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: audit report with findings and ratings.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `internal-it-auditor:3`.

**Required inputs:**

- Risk-based audit universe
- Control documentation
- System-generated evidence
- Prior findings

**Specification:** `kind/role/internal-it-auditor:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: audit report with findings and ratings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `assurance-assessment`.

Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.

**Evidence accompanying the work product:**

- criterion-to-test-to-observation traceability
- independent reviewer and limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/internal-it-auditor:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: audit report with findings and ratings.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; Compliance Officer (Technology)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.delivery_verification`** — `array`

- For the specific output 'audit report with findings and ratings', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Existing source requirement: Conclusions are traceable to dated evidence; opinion is visibly separated from fact. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Independence is declared and preserved
- G6: where the auditor previously operated the control, the engagement is reassigned rather than disclosed and continued
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.contract_input_1`** — `object`

- Analyse the specific input "Risk-based audit universe" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.contract_input_2`** — `object`

- Analyse the specific input "Control documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.contract_input_3`** — `object`

- Analyse the specific input "System-generated evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.contract_input_4`** — `object`

- Analyse the specific input "Prior findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/internal-it-auditor:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/internal-it-auditor:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/internal-it-auditor:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/internal-it-auditor:3.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Internal IT Auditor:** IIA Global Internal Audit Standards; ISACA IT audit framework and COBIT 2019; ISO 19011. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate binding obligation, interpretation, control, evidence, independent test and bounded assurance/risk conclusion.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-internal-it-auditor-4"></a>

## follow-up and closure verification

**At a glance**

- **Purpose:** Produce and govern the role deliverable: follow-up and closure verification.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `internal-it-auditor:4`.

**Required inputs:**

- Risk-based audit universe
- Control documentation
- System-generated evidence
- Prior findings

**Specification:** `kind/role/internal-it-auditor:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: follow-up and closure verification.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/assurance-report`](spec-type-assurance-report.md)
- [`domain/security`](spec-domain-security.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `assurance-assessment`.

Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.

**Evidence accompanying the work product:**

- criterion-to-test-to-observation traceability
- independent reviewer and limitations

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/internal-it-auditor:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: follow-up and closure verification.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.receiving_acceptance`** — `array`

- For each receiving role (Control Owner; Compliance Officer (Technology)), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.delivery_verification`** — `array`

- For the specific output 'follow-up and closure verification', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Assessment criteria are fixed and documented before evidence collection begins.
- G2: Every finding is supported by retained, dated, attributable evidence.
- G3: The assessor is independent of the activity being assessed; any conflict is declared and documented.
- G4: Management responses record an owner, a date and an accepted residual risk for every finding.
- G5: Independence is declared and preserved
- G6: where the auditor previously operated the control, the engagement is reassigned rather than disclosed and continued
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.contract_input_1`** — `object`

- Analyse the specific input "Risk-based audit universe" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.contract_input_2`** — `object`

- Analyse the specific input "Control documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.contract_input_3`** — `object`

- Analyse the specific input "System-generated evidence" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.contract_input_4`** — `object`

- Analyse the specific input "Prior findings" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/internal-it-auditor:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

**`role/internal-it-auditor:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/internal-it-auditor:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.isaca.org/resources/cobit); [source](https://doi.org/10.6028/NIST.SP.800-30r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/internal-it-auditor:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/internal-it-auditor:4.irrelevant_detail`** — `object`

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
- **[COBIT governance and management framework](https://www.isaca.org/resources/cobit)** — Enterprise information and technology objectives, accountability, performance and governance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments](https://doi.org/10.6028/NIST.SP.800-30r1)** — Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Internal IT Auditor:** IIA Global Internal Audit Standards; ISACA IT audit framework and COBIT 2019; ISO 19011. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Separate binding obligation, interpretation, control, evidence, independent test and bounded assurance/risk conclusion.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
