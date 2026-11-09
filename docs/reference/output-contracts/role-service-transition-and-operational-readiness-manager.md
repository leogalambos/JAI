<!-- JAI:OUTPUT-CONTRACTS:START -->
# Service Transition and Operational Readiness Manager: output contracts

Prove that a new or changed service can be operated, supported, monitored, recovered and owned before it is accepted into production.

[Full catalogue](index.md)

<a id="output-service-transition-and-operational-readiness-manager-1"></a>

## Operational readiness assessment

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Operational readiness assessment.
- **Mandatory examples:** Define service acceptance criteria for support, resilience, security, capacity and monitoring. Record receiving operations recommendation, residual risks and pending authority decisions. Link each criterion to observed evidence, gaps and accountable remediation owners.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-transition-and-operational-readiness-manager:1`.

**Required inputs:**

- Solution architecture and NFRs
- Support and ownership model
- Monitoring/SLO design
- Cutover plan

**Specification:** `kind/role/service-transition-and-operational-readiness-manager:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Operational readiness assessment.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/operational-readiness-assessment`](spec-type-operational-readiness-assessment.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `readiness-assessment`.

Service acceptance criteria and observed readiness evidence with receiving-operations disposition.

**Evidence accompanying the work product:**

- support/security/recovery/capacity evidence
- open actions and receiving acceptance status

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/service-transition-and-operational-readiness-manager:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Operational readiness assessment.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.receiving_acceptance`** — `array`

- For each receiving role (Application Support Analyst; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.delivery_verification`** — `array`

- For the specific output 'Operational readiness assessment', provide verifiable evidence satisfying: Define service boundary and named receiving operations owner; enumerate support, access, monitoring, capacity, resilience and security readiness criteria. Record evidence and disposition for each applicable criterion, including missing/unexecuted checks, impact and remediation accountability. Separate readiness recommendation from deployment permission; identify unresolved risks, receiving acceptance conditions and early-life support exit criteria. Existing source requirement: Every operational capability is pass/fail/waived with evidence, owner and due date. Required delivery form: Service acceptance criteria and observed readiness evidence with receiving-operations disposition.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Operational acceptance criteria are agreed before go-live readiness is assessed.
- G2: Monitoring and alerting are actionable and have named owners/runbooks.
- G3: Backup/restore or recovery claims have test evidence appropriate to criticality.
- G4: Support ownership, escalation and supplier dependencies are explicit.
- G5: No critical readiness gap is hidden inside a generic project risk; it is pass/fail/waived with authority.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.contract_input_1`** — `object`

- Analyse the specific input "Solution architecture and NFRs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.contract_input_2`** — `object`

- Analyse the specific input "Support and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.contract_input_3`** — `object`

- Analyse the specific input "Monitoring/SLO design" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.contract_input_4`** — `object`

- Analyse the specific input "Cutover plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-transition-and-operational-readiness-manager:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-transition-and-operational-readiness-manager:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-transition-and-operational-readiness-manager:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-transition-and-operational-readiness-manager:1.irrelevant_detail`** — `object`

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

- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Transition and Operational Readiness Manager:** ITIL 4 transition/deployment practices; ISO/IEC 20000-1; SRE production readiness review practices. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-service-transition-and-operational-readiness-manager-2"></a>

## Service transition and handover plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Service transition and handover plan.
- **Mandatory examples:** Define sequenced increments, resources, milestones and measurable acceptance. Describe current and target outcomes, accountable owners and planning assumptions. Link dependencies, funding constraints, risks and decision dates to affected increments.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-transition-and-operational-readiness-manager:2`.

**Required inputs:**

- Solution architecture and NFRs
- Support and ownership model
- Monitoring/SLO design
- Cutover plan

**Specification:** `kind/role/service-transition-and-operational-readiness-manager:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Service transition and handover plan.

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

**`role/service-transition-and-operational-readiness-manager:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Service transition and handover plan.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.receiving_acceptance`** — `array`

- For each receiving role (Application Support Analyst; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.delivery_verification`** — `array`

- For the specific output 'Service transition and handover plan', provide verifiable evidence satisfying: State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions. For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome. Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options. Existing source requirement: Receiving operations roles explicitly accept the handover and its open risks. Required delivery form: Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Operational acceptance criteria are agreed before go-live readiness is assessed.
- G2: Monitoring and alerting are actionable and have named owners/runbooks.
- G3: Backup/restore or recovery claims have test evidence appropriate to criticality.
- G4: Support ownership, escalation and supplier dependencies are explicit.
- G5: No critical readiness gap is hidden inside a generic project risk; it is pass/fail/waived with authority.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.contract_input_1`** — `object`

- Analyse the specific input "Solution architecture and NFRs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.contract_input_2`** — `object`

- Analyse the specific input "Support and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.contract_input_3`** — `object`

- Analyse the specific input "Monitoring/SLO design" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.contract_input_4`** — `object`

- Analyse the specific input "Cutover plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-transition-and-operational-readiness-manager:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-transition-and-operational-readiness-manager:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-transition-and-operational-readiness-manager:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-transition-and-operational-readiness-manager:2.irrelevant_detail`** — `object`

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
- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Transition and Operational Readiness Manager:** ITIL 4 transition/deployment practices; ISO/IEC 20000-1; SRE production readiness review practices. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-service-transition-and-operational-readiness-manager-3"></a>

## Operational acceptance criteria and evidence pack

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Operational acceptance criteria and evidence pack.
- **Mandatory examples:** Define tested obligations, assurance period, sample and exclusions. Link procedures and observed results to immutable evidence and located deviations. Limit the independent conclusion to tested scope, evidence strength and unresolved findings.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-transition-and-operational-readiness-manager:3`.

**Required inputs:**

- Solution architecture and NFRs
- Support and ownership model
- Monitoring/SLO design
- Cutover plan

**Specification:** `kind/role/service-transition-and-operational-readiness-manager:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Operational acceptance criteria and evidence pack.

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

**`role/service-transition-and-operational-readiness-manager:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Operational acceptance criteria and evidence pack.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.receiving_acceptance`** — `array`

- For each receiving role (Application Support Analyst; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.delivery_verification`** — `array`

- For the specific output 'Operational acceptance criteria and evidence pack', provide verifiable evidence satisfying: State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions. For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure. Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure. Existing source requirement: Monitoring, recovery, security, support, supplier and configuration criteria are evidenced, not self-attested. Required delivery form: Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Operational acceptance criteria are agreed before go-live readiness is assessed.
- G2: Monitoring and alerting are actionable and have named owners/runbooks.
- G3: Backup/restore or recovery claims have test evidence appropriate to criticality.
- G4: Support ownership, escalation and supplier dependencies are explicit.
- G5: No critical readiness gap is hidden inside a generic project risk; it is pass/fail/waived with authority.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.contract_input_1`** — `object`

- Analyse the specific input "Solution architecture and NFRs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.contract_input_2`** — `object`

- Analyse the specific input "Support and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.contract_input_3`** — `object`

- Analyse the specific input "Monitoring/SLO design" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.contract_input_4`** — `object`

- Analyse the specific input "Cutover plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-transition-and-operational-readiness-manager:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-transition-and-operational-readiness-manager:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-53Ar5); [source](https://www.iso.org/standard/70636.html); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-transition-and-operational-readiness-manager:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-transition-and-operational-readiness-manager:3.irrelevant_detail`** — `object`

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
- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Transition and Operational Readiness Manager:** ITIL 4 transition/deployment practices; ISO/IEC 20000-1; SRE production readiness review practices. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-service-transition-and-operational-readiness-manager-4"></a>

## Early-life support and service acceptance report

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Early-life support and service acceptance report.
- **Mandatory examples:** Define service acceptance criteria for support, resilience, security, capacity and monitoring. Record receiving operations recommendation, residual risks and pending authority decisions. Link each criterion to observed evidence, gaps and accountable remediation owners.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `service-transition-and-operational-readiness-manager:4`.

**Required inputs:**

- Solution architecture and NFRs
- Support and ownership model
- Monitoring/SLO design
- Cutover plan

**Specification:** `kind/role/service-transition-and-operational-readiness-manager:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Early-life support and service acceptance report.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/operational-readiness-assessment`](spec-type-operational-readiness-assessment.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `readiness-assessment`.

Service acceptance criteria and observed readiness evidence with receiving-operations disposition.

**Evidence accompanying the work product:**

- support/security/recovery/capacity evidence
- open actions and receiving acceptance status

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/service-transition-and-operational-readiness-manager:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Early-life support and service acceptance report.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.receiving_acceptance`** — `array`

- For each receiving role (Application Support Analyst; Site Reliability Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.delivery_verification`** — `array`

- For the specific output 'Early-life support and service acceptance report', provide verifiable evidence satisfying: Define service boundary and named receiving operations owner; enumerate support, access, monitoring, capacity, resilience and security readiness criteria. Record evidence and disposition for each applicable criterion, including missing/unexecuted checks, impact and remediation accountability. Separate readiness recommendation from deployment permission; identify unresolved risks, receiving acceptance conditions and early-life support exit criteria. Existing source requirement: The service exits early-life support only when stability and ownership thresholds are met. Required delivery form: Service acceptance criteria and observed readiness evidence with receiving-operations disposition.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Operational acceptance criteria are agreed before go-live readiness is assessed.
- G2: Monitoring and alerting are actionable and have named owners/runbooks.
- G3: Backup/restore or recovery claims have test evidence appropriate to criticality.
- G4: Support ownership, escalation and supplier dependencies are explicit.
- G5: No critical readiness gap is hidden inside a generic project risk; it is pass/fail/waived with authority.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.contract_input_1`** — `object`

- Analyse the specific input "Solution architecture and NFRs" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.contract_input_2`** — `object`

- Analyse the specific input "Support and ownership model" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.contract_input_3`** — `object`

- Analyse the specific input "Monitoring/SLO design" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.contract_input_4`** — `object`

- Analyse the specific input "Cutover plan" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/service-transition-and-operational-readiness-manager:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

**`role/service-transition-and-operational-readiness-manager:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/service-transition-and-operational-readiness-manager:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/70636.html); [source](https://doi.org/10.6028/NIST.SP.800-34r1); [source](https://sre.google/sre-book/service-level-objectives/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/service-transition-and-operational-readiness-manager:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/service-transition-and-operational-readiness-manager:4.irrelevant_detail`** — `object`

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

- **[ISO/IEC 20000-1:2018, Service management system requirements](https://www.iso.org/standard/70636.html)** — Service requirements, agreements, transition, operation and measurement concepts. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems](https://doi.org/10.6028/NIST.SP.800-34r1)** — Recovery priorities, dependencies, recovery procedures, exercises and maintenance. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[Google Site Reliability Engineering, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Service Transition and Operational Readiness Manager:** ITIL 4 transition/deployment practices; ISO/IEC 20000-1; SRE production readiness review practices. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
