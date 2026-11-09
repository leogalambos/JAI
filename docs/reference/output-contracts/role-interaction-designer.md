<!-- JAI:OUTPUT-CONTRACTS:START -->
# Interaction Designer: output contracts

Design the detailed behaviour of the interface: states, transitions, feedback and micro-interactions

[Full catalogue](index.md)

<a id="output-interaction-designer-1"></a>

## Interaction specifications and state diagrams

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Interaction specifications and state diagrams.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `interaction-designer:1`.

**Required inputs:**

- User flows
- Technical capabilities and constraints
- Accessibility requirements
- Design system behaviour

**Specification:** `kind/role/interaction-designer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Interaction specifications and state diagrams.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/requirements-specification`](spec-family-requirements-specification.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `requirements-specification`.

Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.

**Evidence accompanying the work product:**

- forward/backward traceability
- conflict, interface and change-impact checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/interaction-designer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Interaction specifications and state diagrams.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.receiving_acceptance`** — `array`

- For each receiving role (Frontend Engineer; Design System Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.delivery_verification`** — `array`

- For the specific output 'Interaction specifications and state diagrams', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Existing source requirement: Every requirement is atomic, testable and traced to a source and a priority. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Motion respects reduced-motion preferences and no interaction depends on hover, timing or pointer precision alone
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.contract_input_1`** — `object`

- Analyse the specific input "User flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.contract_input_2`** — `object`

- Analyse the specific input "Technical capabilities and constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.contract_input_3`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.contract_input_4`** — `object`

- Analyse the specific input "Design system behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/interaction-designer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/interaction-designer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/interaction-designer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/interaction-designer:1.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Interaction Designer:** WCAG 2.2 AA including motion and timing criteria; platform interaction guidelines. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-interaction-designer-2"></a>

## motion and feedback definitions

**At a glance**

- **Purpose:** Produce and govern the role deliverable: motion and feedback definitions.
- **Mandatory examples:** Specify deployment, verification, rollback and reproducible acceptance tests. Specify schemas, error states, concurrency and compatibility requirements. Define typed configuration values, units, versions and permitted ranges without secrets.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `interaction-designer:2`.

**Required inputs:**

- User flows
- Technical capabilities and constraints
- Accessibility requirements
- Design system behaviour

**Specification:** `kind/role/interaction-designer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: motion and feedback definitions.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/implementation-specification`](spec-type-implementation-specification.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `implementation-specification`.

Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.

**Evidence accompanying the work product:**

- parameter/schema constraints
- reproducible acceptance and recovery procedure

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/interaction-designer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: motion and feedback definitions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.receiving_acceptance`** — `array`

- For each receiving role (Frontend Engineer; Design System Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.delivery_verification`** — `array`

- For the specific output 'motion and feedback definitions', provide verifiable evidence satisfying: Identify exact component/environment versions and each required parameter with type, unit, permitted range, default and secret-reference handling. State interface schemas, input/output semantics, error responses, concurrency/idempotency expectations and external dependency constraints. Give reproducible build/deploy/verification steps, expected results, stop conditions and recovery path; identify evidence still required before execution. Required delivery form: Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Motion respects reduced-motion preferences and no interaction depends on hover, timing or pointer precision alone
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.contract_input_1`** — `object`

- Analyse the specific input "User flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.contract_input_2`** — `object`

- Analyse the specific input "Technical capabilities and constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.contract_input_3`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.contract_input_4`** — `object`

- Analyse the specific input "Design system behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/interaction-designer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/interaction-designer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-218); [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/interaction-designer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/interaction-designer:2.irrelevant_detail`** — `object`

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
  "typed": {
    "metric": "typed",
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
- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Interaction Designer:** WCAG 2.2 AA including motion and timing criteria; platform interaction guidelines. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-interaction-designer-3"></a>

## input and error handling behaviour

**At a glance**

- **Purpose:** Produce and govern the role deliverable: input and error handling behaviour.
- **Mandatory examples:** Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `interaction-designer:3`.

**Required inputs:**

- User flows
- Technical capabilities and constraints
- Accessibility requirements
- Design system behaviour

**Specification:** `kind/role/interaction-designer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: input and error handling behaviour.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`family/requirements-specification`](spec-family-requirements-specification.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `requirements-specification`.

Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.

**Evidence accompanying the work product:**

- forward/backward traceability
- conflict, interface and change-impact checks

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/interaction-designer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: input and error handling behaviour.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.receiving_acceptance`** — `array`

- For each receiving role (Frontend Engineer; Design System Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.delivery_verification`** — `array`

- For the specific output 'input and error handling behaviour', provide verifiable evidence satisfying: Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers. State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions. Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility. Required delivery form: Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Motion respects reduced-motion preferences and no interaction depends on hover, timing or pointer precision alone
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.contract_input_1`** — `object`

- Analyse the specific input "User flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.contract_input_2`** — `object`

- Analyse the specific input "Technical capabilities and constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.contract_input_3`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.contract_input_4`** — `object`

- Analyse the specific input "Design system behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/interaction-designer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/interaction-designer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/72089.html); [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/interaction-designer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/interaction-designer:3.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 29148:2018, Requirements engineering](https://www.iso.org/standard/72089.html)** — Requirements information items, requirement quality and traceability. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[ISO 9241-210:2019, Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)** — Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)** — Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[W3C WCAG Evaluation Methodology (WCAG-EM) 2.0](https://www.w3.org/TR/wcag-em-2/)** — Evaluation scope, representative sample, evaluation and reporting; W3C Group Note, informative methodology rather than a conformance standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **Interaction Designer:** WCAG 2.2 AA including motion and timing criteria; platform interaction guidelines. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-interaction-designer-4"></a>

## prototype demonstrating behaviour

**At a glance**

- **Purpose:** Produce and govern the role deliverable: prototype demonstrating behaviour.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `interaction-designer:4`.

**Required inputs:**

- User flows
- Technical capabilities and constraints
- Accessibility requirements
- Design system behaviour

**Specification:** `kind/role/interaction-designer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: prototype demonstrating behaviour.

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

**`role/interaction-designer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: prototype demonstrating behaviour.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.receiving_acceptance`** — `array`

- For each receiving role (Frontend Engineer; Design System Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.delivery_verification`** — `array`

- For the specific output 'prototype demonstrating behaviour', provide verifiable evidence satisfying: State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers. Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient. State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly. Required delivery form: Actual editable design/prototype assets or interaction-tool project with linked screens, transitions and loading, empty, error states; implementation code is required only when explicitly in scope.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Design decisions are traceable to research evidence or are explicitly labelled as assumptions to be tested.
- G2: WCAG 2.2 AA is met, including keyboard operation, focus order, contrast and assistive-technology labelling.
- G3: All states are specified: loading, empty, partial, error, offline, permission-denied and success.
- G4: Content is written and reviewed with the design, not filled in with placeholder text at build time.
- G5: Motion respects reduced-motion preferences and no interaction depends on hover, timing or pointer precision alone
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.contract_input_1`** — `object`

- Analyse the specific input "User flows" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.contract_input_2`** — `object`

- Analyse the specific input "Technical capabilities and constraints" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.contract_input_3`** — `object`

- Analyse the specific input "Accessibility requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.contract_input_4`** — `object`

- Analyse the specific input "Design system behaviour" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.interaction_prototype_assets`** — `object`

- Supply the actual editable prototype/design assets or interaction-tool project with exact revision, tool/version, access/export constraints and links between screens and flows. A narrative description cannot replace requested prototype assets; do not require an executable code experiment for a noncoding design.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.interaction_state_coverage`** — `array`

- Map intended user tasks to screens, inputs, transitions and feedback. Cover loading, empty, error, permission and success states, keyboard/focus behaviour and recovery where applicable; explain exclusions and unresolved design questions.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.interaction_evaluation_evidence`** — `array`

- Link actual review/usability/accessibility evaluation observations to the exact prototype revision, task/state and remediation decision. Distinguish observed results from planned evaluation and explicit not-tested states; never invent participant findings.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/interaction-designer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

**`role/interaction-designer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/interaction-designer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/77520.html); [source](https://www.w3.org/TR/WCAG22/); [source](https://www.w3.org/TR/wcag-em-2/) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/interaction-designer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/interaction-designer:4.irrelevant_detail`** — `object`

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

- **Interaction Designer:** WCAG 2.2 AA including motion and timing criteria; platform interaction guidelines. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
