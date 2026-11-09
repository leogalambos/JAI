<!-- JAI:OUTPUT-CONTRACTS:START -->
# Product Designer: output contracts

Own the whole design of a product area: research, interaction, visual and the outcome it produces

[Full catalogue](index.md)

<a id="output-product-designer-1"></a>

## Design strategy for the product area

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Design strategy for the product area.
- **Mandatory examples:** Compare investment and operating choices, dependencies, resource assumptions and rejected alternatives. Trace target outcomes and measurable success to business direction and baseline constraints. Assign sequenced initiatives, accountable owners, outcome measures and review triggers.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-designer:1`.

**Required inputs:**

- Product strategy
- User research
- Usage and funnel data
- Technical feasibility

**Specification:** `kind/role/product-designer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Design strategy for the product area.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/strategy`](spec-family-strategy.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `strategy`.

Evidenced strategic choices with target outcomes, alternatives, investment assumptions and execution accountability.

**Evidence accompanying the work product:**

- baseline and rejected options
- outcome measures, dependencies and review triggers

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/product-designer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Design strategy for the product area.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; UI Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.delivery_verification`** — `array`

- For the specific output 'Design strategy for the product area', provide verifiable evidence satisfying: Trace target outcomes and measurable success to business direction and baseline constraints. Compare investment and operating choices, dependencies, resource assumptions and rejected alternatives. Assign sequenced initiatives, accountable owners, outcome measures and review triggers. Existing source requirement: Traces user/business outcomes to research, design principles, priorities, constraints and measurable evaluation. Required delivery form: Evidenced strategic choices with target outcomes, alternatives, investment assumptions and execution accountability.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Design decisions cite research evidence or are explicitly marked as assumptions with a plan to test them
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.contract_input_1`** — `object`

- Analyse the specific input "Product strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.contract_input_2`** — `object`

- Analyse the specific input "User research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.contract_input_3`** — `object`

- Analyse the specific input "Usage and funnel data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.contract_input_4`** — `object`

- Analyse the specific input "Technical feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-designer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-designer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.isaca.org/resources/cobit); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-designer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-designer:1.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Designer:** ISO 9241-210; WCAG 2.2 AA; design system governance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-product-designer-2"></a>

## end-to-end designs and prototypes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: end-to-end designs and prototypes.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-designer:2`.

**Required inputs:**

- Product strategy
- User research
- Usage and funnel data
- Technical feasibility

**Specification:** `kind/role/product-designer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: end-to-end designs and prototypes.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `interactive-design-prototype`.

Actual editable design/prototype assets or interaction-tool project with linked screens, transitions and loading, empty, error states; implementation code is required only when explicitly in scope.

**Evidence accompanying the work product:**

- exact design revision, tool/version, access and export constraints
- state/flow coverage and observed evaluation findings or explicit not-tested status

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/product-designer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: end-to-end designs and prototypes.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; UI Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.delivery_verification`** — `array`

- For the specific output 'end-to-end designs and prototypes', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Existing source requirement: Loading, empty, partial, error, offline and success states are all specified. Required delivery form: Actual editable design/prototype assets or interaction-tool project with linked screens, transitions and loading, empty, error states; implementation code is required only when explicitly in scope.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Design decisions cite research evidence or are explicitly marked as assumptions with a plan to test them
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.contract_input_1`** — `object`

- Analyse the specific input "Product strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.contract_input_2`** — `object`

- Analyse the specific input "User research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.contract_input_3`** — `object`

- Analyse the specific input "Usage and funnel data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.contract_input_4`** — `object`

- Analyse the specific input "Technical feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.interaction_prototype_assets`** — `object`

- Supply the actual editable prototype/design assets or interaction-tool project with exact revision, tool/version, access/export constraints and links between screens and flows. A narrative description cannot replace requested prototype assets; do not require an executable code experiment for a noncoding design.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.interaction_state_coverage`** — `array`

- Map intended user tasks to screens, inputs, transitions and feedback. Cover loading, empty, error, permission and success states, keyboard/focus behaviour and recovery where applicable; explain exclusions and unresolved design questions.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.interaction_evaluation_evidence`** — `array`

- Link actual review/usability/accessibility evaluation observations to the exact prototype revision, task/state and remediation decision. Distinguish observed results from planned evaluation and explicit not-tested states; never invent participant findings.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-designer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-designer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-designer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-designer:2.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Designer:** ISO 9241-210; WCAG 2.2 AA; design system governance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-product-designer-3"></a>

## research-backed design rationale

**At a glance**

- **Purpose:** Produce and govern the role deliverable: research-backed design rationale.
- **Mandatory examples:** Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-designer:3`.

**Required inputs:**

- Product strategy
- User research
- Usage and funnel data
- Technical feasibility

**Specification:** `kind/role/product-designer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: research-backed design rationale.

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

**`role/product-designer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: research-backed design rationale.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; UI Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.delivery_verification`** — `array`

- For the specific output 'research-backed design rationale', provide verifiable evidence satisfying: Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions. Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence. Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request. Existing source requirement: Links design choices and rejected alternatives to attributable user research, assumptions and validation limits. Required delivery form: Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Design decisions cite research evidence or are explicitly marked as assumptions with a plan to test them
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.contract_input_1`** — `object`

- Analyse the specific input "Product strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.contract_input_2`** — `object`

- Analyse the specific input "User research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.contract_input_3`** — `object`

- Analyse the specific input "Usage and funnel data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.contract_input_4`** — `object`

- Analyse the specific input "Technical feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-designer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-designer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-designer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-designer:3.irrelevant_detail`** — `object`

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
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Designer:** ISO 9241-210; WCAG 2.2 AA; design system governance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-product-designer-4"></a>

## measured design outcomes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: measured design outcomes.
- **Mandatory examples:** Link test cases and requirements to actual outcomes, timestamps and execution evidence. Explain defects, untested scope, achieved exit criteria and residual release risk. Identify build, requirements, environment, reporting period and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `product-designer:4`.

**Required inputs:**

- Product strategy
- User research
- Usage and funnel data
- Technical feasibility

**Specification:** `kind/role/product-designer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: measured design outcomes.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-report`](spec-type-test-report.md)
- [`domain/testing`](spec-domain-testing.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `test-results`.

Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.

**Evidence accompanying the work product:**

- expected/actual observations and execution references
- coverage denominators and residual defects

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/product-designer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: measured design outcomes.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.receiving_acceptance`** — `array`

- For each receiving role (UX Designer; UI Designer; Frontend Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.delivery_verification`** — `array`

- For the specific output 'measured design outcomes', provide verifiable evidence satisfying: Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan. State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage. Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation. Existing source requirement: Compares measured user outcomes against baseline and targets, reporting methods, uncertainty and next actions. Required delivery form: Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Design decisions cite research evidence or are explicitly marked as assumptions with a plan to test them
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.contract_input_1`** — `object`

- Analyse the specific input "Product strategy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.contract_input_2`** — `object`

- Analyse the specific input "User research" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.contract_input_3`** — `object`

- Analyse the specific input "Usage and funnel data" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.contract_input_4`** — `object`

- Analyse the specific input "Technical feasibility" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/product-designer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/product-designer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/product-designer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/product-designer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/product-designer:4.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation](https://www.iso.org/standard/79429.html)** — Test planning, test specifications and reporting information needs. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Product Designer:** ISO 9241-210; WCAG 2.2 AA; design system governance. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
