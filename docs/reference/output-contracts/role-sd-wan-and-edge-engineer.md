<!-- JAI:OUTPUT-CONTRACTS:START -->
# SD-WAN and Edge Engineer: output contracts

Connect distributed sites reliably and cost-effectively, with policy applied at the edge

[Full catalogue](index.md)

<a id="output-sd-wan-and-edge-engineer-1"></a>

## SD-WAN overlay design and policy configuration

**At a glance**

- **Purpose:** Produce and govern the role deliverable: SD-WAN overlay design and policy configuration.
- **Mandatory examples:** Describe bounded component responsibilities and deployment topology. Map measurable quality requirements to design verification and acceptance. Define versioned interface inputs, outputs, trust boundaries and failure handling.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sd-wan-and-edge-engineer:1`.

**Required inputs:**

- Site connectivity requirements
- Application performance requirements
- Circuit inventory and contracts
- Security policy

**Specification:** `kind/role/sd-wan-and-edge-engineer:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: SD-WAN overlay design and policy configuration.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/solution-design`](spec-type-solution-design.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `solution-design`.

Versioned solution design with component responsibilities, interfaces and measurable quality responses.

**Evidence accompanying the work product:**

- requirements-to-design traceability
- independent design review

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/sd-wan-and-edge-engineer:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: SD-WAN overlay design and policy configuration.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.receiving_acceptance`** — `array`

- For each receiving role (Network Engineer; Firewall and Perimeter Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.delivery_verification`** — `array`

- For the specific output 'SD-WAN overlay design and policy configuration', provide verifiable evidence satisfying: Define the proposed implementation boundary, use cases and external dependencies. State measurable availability, performance, security and operational acceptance targets. Describe component responsibilities, deployment topology and design rationale. Existing source requirement: Every statement is testable and maps to at least one control. Required delivery form: Versioned solution design with component responsibilities, interfaces and measurable quality responses.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Failover between transports is tested per site design with measured application impact, not assumed from the vendor datasheet
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.contract_input_1`** — `object`

- Analyse the specific input "Site connectivity requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.contract_input_2`** — `object`

- Analyse the specific input "Application performance requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.contract_input_3`** — `object`

- Analyse the specific input "Circuit inventory and contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.contract_input_4`** — `object`

- Analyse the specific input "Security policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sd-wan-and-edge-engineer:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sd-wan-and-edge-engineer:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sd-wan-and-edge-engineer:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sd-wan-and-edge-engineer:1.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[IETF RFC 2026, The Internet Standards Process — Revision 3](https://www.rfc-editor.org/rfc/rfc2026)** — Distinguishing standards-track status and specification maturity; select the actual applicable protocol RFCs and their updates rather than treating the process document as a network design standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SD-WAN and Edge Engineer:** vendor SD-WAN design guidance; zero trust principles (NIST SP 800-207); IETF routing standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Identify applicable protocol/technology editions, topology and trust assumptions, measurable network behaviour and compatibility evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-sd-wan-and-edge-engineer-2"></a>

## site connectivity and failover design

**At a glance**

- **Purpose:** Produce and govern the role deliverable: site connectivity and failover design.
- **Mandatory examples:** Describe bounded component responsibilities and deployment topology. Map measurable quality requirements to design verification and acceptance. Define versioned interface inputs, outputs, trust boundaries and failure handling.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sd-wan-and-edge-engineer:2`.

**Required inputs:**

- Site connectivity requirements
- Application performance requirements
- Circuit inventory and contracts
- Security policy

**Specification:** `kind/role/sd-wan-and-edge-engineer:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: site connectivity and failover design.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/solution-design`](spec-type-solution-design.md)
- [`domain/architecture`](spec-domain-architecture.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `solution-design`.

Versioned solution design with component responsibilities, interfaces and measurable quality responses.

**Evidence accompanying the work product:**

- requirements-to-design traceability
- independent design review

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/sd-wan-and-edge-engineer:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: site connectivity and failover design.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.receiving_acceptance`** — `array`

- For each receiving role (Network Engineer; Firewall and Perimeter Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.delivery_verification`** — `array`

- For the specific output 'site connectivity and failover design', provide verifiable evidence satisfying: Define the proposed implementation boundary, use cases and external dependencies. State measurable availability, performance, security and operational acceptance targets. Describe component responsibilities, deployment topology and design rationale. Existing source requirement: Defines site paths, routing, failure detection, convergence targets, degraded operation and validation scenarios. Required delivery form: Versioned solution design with component responsibilities, interfaces and measurable quality responses.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Failover between transports is tested per site design with measured application impact, not assumed from the vendor datasheet
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.contract_input_1`** — `object`

- Analyse the specific input "Site connectivity requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.contract_input_2`** — `object`

- Analyse the specific input "Application performance requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.contract_input_3`** — `object`

- Analyse the specific input "Circuit inventory and contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.contract_input_4`** — `object`

- Analyse the specific input "Security policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sd-wan-and-edge-engineer:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sd-wan-and-edge-engineer:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/74393.html); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1); [source](https://www.rfc-editor.org/rfc/rfc2026) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sd-wan-and-edge-engineer:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sd-wan-and-edge-engineer:2.irrelevant_detail`** — `object`

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

- **[ISO/IEC/IEEE 42010:2022, Architecture description](https://www.iso.org/standard/74393.html)** — Stakeholders, concerns, viewpoints, architecture views and correspondence. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[IETF RFC 2026, The Internet Standards Process — Revision 3](https://www.rfc-editor.org/rfc/rfc2026)** — Distinguishing standards-track status and specification maturity; select the actual applicable protocol RFCs and their updates rather than treating the process document as a network design standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SD-WAN and Edge Engineer:** vendor SD-WAN design guidance; zero trust principles (NIST SP 800-207); IETF routing standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Identify applicable protocol/technology editions, topology and trust assumptions, measurable network behaviour and compatibility evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-sd-wan-and-edge-engineer-3"></a>

## application steering policy

**At a glance**

- **Purpose:** Produce and govern the role deliverable: application steering policy.
- **Mandatory examples:** Identify managed assets, tool/schema versions and authorised configuration scope. Provide typed desired settings, permitted ranges and secret-manager references. Evidence reproducibility, drift checks, deployment validation and rollback to a known baseline.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sd-wan-and-edge-engineer:3`.

**Required inputs:**

- Site connectivity requirements
- Application performance requirements
- Circuit inventory and contracts
- Security policy

**Specification:** `kind/role/sd-wan-and-edge-engineer:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: application steering policy.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/configuration-baseline`](spec-type-configuration-baseline.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `versioned-configuration`.

Typed desired-state configuration with exact targets, versioned values and controlled secret references.

**Evidence accompanying the work product:**

- reproduction/drift observations
- verification and recovery to a known baseline

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/sd-wan-and-edge-engineer:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: application steering policy.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.receiving_acceptance`** — `array`

- For each receiving role (Network Engineer; Firewall and Perimeter Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.delivery_verification`** — `array`

- For the specific output 'application steering policy', provide verifiable evidence satisfying: Identify managed components, exact versions, environments, approved parameter values, exceptions and configuration owner without exposing secrets. Describe how the baseline is created/applied, validated and changed, including dependencies and recovery from an unsuccessful change. Compare observed configuration with the declared baseline, classify drift, identify material impact and record authorised remediation or unresolved exceptions. Existing source requirement: Every statement is testable and maps to at least one control. Required delivery form: Typed desired-state configuration with exact targets, versioned values and controlled secret references.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Failover between transports is tested per site design with measured application impact, not assumed from the vendor datasheet
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.contract_input_1`** — `object`

- Analyse the specific input "Site connectivity requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.contract_input_2`** — `object`

- Analyse the specific input "Application performance requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.contract_input_3`** — `object`

- Analyse the specific input "Circuit inventory and contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.contract_input_4`** — `object`

- Analyse the specific input "Security policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sd-wan-and-edge-engineer:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sd-wan-and-edge-engineer:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sd-wan-and-edge-engineer:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sd-wan-and-edge-engineer:3.irrelevant_detail`** — `object`

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

- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[IETF RFC 2026, The Internet Standards Process — Revision 3](https://www.rfc-editor.org/rfc/rfc2026)** — Distinguishing standards-track status and specification maturity; select the actual applicable protocol RFCs and their updates rather than treating the process document as a network design standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SD-WAN and Edge Engineer:** vendor SD-WAN design guidance; zero trust principles (NIST SP 800-207); IETF routing standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Identify applicable protocol/technology editions, topology and trust assumptions, measurable network behaviour and compatibility evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.


<a id="output-sd-wan-and-edge-engineer-4"></a>

## edge security configuration

**At a glance**

- **Purpose:** Produce and govern the role deliverable: edge security configuration.
- **Mandatory examples:** Identify managed assets, tool/schema versions and authorised configuration scope. Provide typed desired settings, permitted ranges and secret-manager references. Evidence reproducibility, drift checks, deployment validation and rollback to a known baseline.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `sd-wan-and-edge-engineer:4`.

**Required inputs:**

- Site connectivity requirements
- Application performance requirements
- Circuit inventory and contracts
- Security policy

**Specification:** `kind/role/sd-wan-and-edge-engineer:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: edge security configuration.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/configuration-baseline`](spec-type-configuration-baseline.md)
- [`domain/operations`](spec-domain-operations.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

### Primary work product and evidence

**Primary work product:** `versioned-configuration`.

Typed desired-state configuration with exact targets, versioned values and controlled secret references.

**Evidence accompanying the work product:**

- reproduction/drift observations
- verification and recovery to a known baseline

The historical artifact-type field is retained for compatibility; it does not require replacing this work product with a report or an EA diagram. Content guidance only; existing execution and human authority boundaries remain.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/sd-wan-and-edge-engineer:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: edge security configuration.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.receiving_acceptance`** — `array`

- For each receiving role (Network Engineer; Firewall and Perimeter Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.delivery_verification`** — `array`

- For the specific output 'edge security configuration', provide verifiable evidence satisfying: Identify managed components, exact versions, environments, approved parameter values, exceptions and configuration owner without exposing secrets. Describe how the baseline is created/applied, validated and changed, including dependencies and recovery from an unsuccessful change. Compare observed configuration with the declared baseline, classify drift, identify material impact and record authorised remediation or unresolved exceptions. Required delivery form: Typed desired-state configuration with exact targets, versioned values and controlled secret references.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: No change merges without passing automated tests and peer review by someone who did not write it.
- G2: A defect is fixed only after its root cause is established by comparing against the last known good state, a working analogue and timing factors, and a regression test reproduces it first (it-role-library/standards/defect-analysis.md).
- G3: Every public behaviour added or changed has unit tests covering normal, boundary and failure cases; every boundary to an external system has an integration test against the real dependency; the full suite was run after the last change and passed (it-role-library/standards/testing.md).
- G4: Secrets, credentials and personal data never appear in source, logs or fixtures.
- G5: Every public element of the change carries a doc comment stating its contract — parameters, result, exceptions — and no comment narrates what the code does (it-role-library/standards/code-documentation.md).
- G6: The change ships with the telemetry needed to tell whether it is working in production.
- G7: A rollback or forward-fix path is defined and has been tried at least once for high-risk changes.
- G8: Failover between transports is tested per site design with measured application impact, not assumed from the vendor datasheet
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.contract_input_1`** — `object`

- Analyse the specific input "Site connectivity requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.contract_input_2`** — `object`

- Analyse the specific input "Application performance requirements" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.contract_input_3`** — `object`

- Analyse the specific input "Circuit inventory and contracts" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.contract_input_4`** — `object`

- Analyse the specific input "Security policy" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/sd-wan-and-edge-engineer:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

**`role/sd-wan-and-edge-engineer:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/sd-wan-and-edge-engineer:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://doi.org/10.6028/NIST.SP.800-128); [source](https://www.rfc-editor.org/rfc/rfc2026); [source](https://doi.org/10.6028/NIST.SP.800-160v1r1) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/sd-wan-and-edge-engineer:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/sd-wan-and-edge-engineer:4.irrelevant_detail`** — `object`

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

- **[NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://doi.org/10.6028/NIST.SP.800-128)** — Configuration baselines, controlled changes, impact analysis and monitoring. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[IETF RFC 2026, The Internet Standards Process — Revision 3](https://www.rfc-editor.org/rfc/rfc2026)** — Distinguishing standards-track status and specification maturity; select the actual applicable protocol RFCs and their updates rather than treating the process document as a network design standard. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.
- **[NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://doi.org/10.6028/NIST.SP.800-160v1r1)** — Life-cycle requirements, design rationale, verification and assurance of system security. Basis: `informed-by`. JAI-authored interpretation of the named subject. No clause-level conformance, certification or automatic applicability is asserted.

### Role framework context

- **SD-WAN and Edge Engineer:** vendor SD-WAN design guidance; zero trust principles (NIST SP 800-207); IETF routing standards. Canonical role context; not proof that every listed framework applies to this output.
  **Practical method:** Identify applicable protocol/technology editions, topology and trust assumptions, measurable network behaviour and compatibility evidence.
  **Selection:** Relevant candidates only; this is not a mandatory framework list.
  **Applicability assessment:** `global.framework_applicability`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
