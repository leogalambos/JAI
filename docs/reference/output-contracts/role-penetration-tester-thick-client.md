<!-- JAI:OUTPUT-CONTRACTS:START -->
# Penetration Tester (Thick Client): output contracts

Test installed desktop applications and their local trust assumptions

[Full catalogue](index.md)

<a id="output-penetration-tester-thick-client-1"></a>

## Thick client test plan

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Thick client test plan.
- **Mandatory examples:** Define test levels, techniques, environments, representative data and responsibilities. Define traceable entry/exit criteria, coverage measurement and defect disposition rules. Define risk-based test objectives, quality targets, scope and exclusions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `penetration-tester-thick-client:1`.

**Required inputs:**

- Signed authorisation and scope
- Application installers and documentation
- Test accounts and server scope
- Supported platform matrix

**Specification:** `kind/role/penetration-tester-thick-client:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Thick client test plan.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/test-strategy`](spec-type-test-strategy.md)
- [`domain/testing`](spec-domain-testing.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/penetration-tester-thick-client:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Thick client test plan.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.delivery_verification`** — `array`

- For the specific output 'Thick client test plan', provide verifiable evidence satisfying: Every milestone has an acceptance test and a named accountable owner. Required delivery form: Document with milestones, owners, dependencies and assumptions.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Written authorisation, signed scope and rules of engagement exist and are current before a single packet is sent.
- G2: All targets are confirmed in scope and owned by the authorising party; anything out of scope is stopped and reported immediately.
- G3: Emergency stop conditions and contacts are agreed and tested before execution.
- G4: Sensitive data encountered is minimised, protected, reported and destroyed per the engagement agreement.
- G5: Findings state whether the server validates independently
- G6: a client-side control bypass is only material where the server trusts the client, and the report must say which
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.contract_input_1`** — `object`

- Analyse the specific input "Signed authorisation and scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.contract_input_2`** — `object`

- Analyse the specific input "Application installers and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.contract_input_3`** — `object`

- Analyse the specific input "Test accounts and server scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.contract_input_4`** — `object`

- Analyse the specific input "Supported platform matrix" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Conditionally required information

**`role/penetration-tester-thick-client:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

**`role/penetration-tester-thick-client:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Optional information (MAY)

**`role/penetration-tester-thick-client:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Professional basis:** [source](https://www.iso.org/standard/79429.html) (informed-by; not a verbatim standard requirement).

### Prohibited content (MUST NOT)

**`role/penetration-tester-thick-client:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/penetration-tester-thick-client:1.irrelevant_detail`** — `object`

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

### Role framework context

- **Penetration Tester (Thick Client):** OWASP testing practice for thick clients; PTES; platform security documentation. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-penetration-tester-thick-client-2"></a>

## local storage, privilege and tampering findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: local storage, privilege and tampering findings.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `penetration-tester-thick-client:2`.

**Required inputs:**

- Signed authorisation and scope
- Application installers and documentation
- Test accounts and server scope
- Supported platform matrix

**Specification:** `kind/role/penetration-tester-thick-client:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: local storage, privilege and tampering findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/penetration-tester-thick-client:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: local storage, privilege and tampering findings.

**`role/penetration-tester-thick-client:2.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/penetration-tester-thick-client:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/penetration-tester-thick-client:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/penetration-tester-thick-client:2.delivery_verification`** — `array`

- For the specific output 'local storage, privilege and tampering findings', provide verifiable evidence satisfying: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Finding record with reproducible evidence and risk rating.

**`role/penetration-tester-thick-client:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Written authorisation, signed scope and rules of engagement exist and are current before a single packet is sent.
- G2: All targets are confirmed in scope and owned by the authorising party; anything out of scope is stopped and reported immediately.
- G3: Emergency stop conditions and contacts are agreed and tested before execution.
- G4: Sensitive data encountered is minimised, protected, reported and destroyed per the engagement agreement.
- G5: Findings state whether the server validates independently
- G6: a client-side control bypass is only material where the server trusts the client, and the report must say which

**`role/penetration-tester-thick-client:2.contract_input_1`** — `object`

- Analyse the specific input "Signed authorisation and scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:2.contract_input_2`** — `object`

- Analyse the specific input "Application installers and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:2.contract_input_3`** — `object`

- Analyse the specific input "Test accounts and server scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:2.contract_input_4`** — `object`

- Analyse the specific input "Supported platform matrix" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/penetration-tester-thick-client:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/penetration-tester-thick-client:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/penetration-tester-thick-client:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/penetration-tester-thick-client:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/penetration-tester-thick-client:2.irrelevant_detail`** — `object`

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

- **Penetration Tester (Thick Client):** OWASP testing practice for thick clients; PTES; platform security documentation. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-penetration-tester-thick-client-3"></a>

## client-server trust boundary findings

**At a glance**

- **Purpose:** Produce and govern the role deliverable: client-server trust boundary findings.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `penetration-tester-thick-client:3`.

**Required inputs:**

- Signed authorisation and scope
- Application installers and documentation
- Test accounts and server scope
- Supported platform matrix

**Specification:** `kind/role/penetration-tester-thick-client:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: client-server trust boundary findings.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/penetration-tester-thick-client:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: client-server trust boundary findings.

**`role/penetration-tester-thick-client:3.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/penetration-tester-thick-client:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/penetration-tester-thick-client:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/penetration-tester-thick-client:3.delivery_verification`** — `array`

- For the specific output 'client-server trust boundary findings', provide verifiable evidence satisfying: Reproduction steps are complete enough for an independent party to confirm. Required delivery form: Finding record with reproducible evidence and risk rating.

**`role/penetration-tester-thick-client:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Written authorisation, signed scope and rules of engagement exist and are current before a single packet is sent.
- G2: All targets are confirmed in scope and owned by the authorising party; anything out of scope is stopped and reported immediately.
- G3: Emergency stop conditions and contacts are agreed and tested before execution.
- G4: Sensitive data encountered is minimised, protected, reported and destroyed per the engagement agreement.
- G5: Findings state whether the server validates independently
- G6: a client-side control bypass is only material where the server trusts the client, and the report must say which

**`role/penetration-tester-thick-client:3.contract_input_1`** — `object`

- Analyse the specific input "Signed authorisation and scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:3.contract_input_2`** — `object`

- Analyse the specific input "Application installers and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:3.contract_input_3`** — `object`

- Analyse the specific input "Test accounts and server scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:3.contract_input_4`** — `object`

- Analyse the specific input "Supported platform matrix" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/penetration-tester-thick-client:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/penetration-tester-thick-client:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/penetration-tester-thick-client:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/penetration-tester-thick-client:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/penetration-tester-thick-client:3.irrelevant_detail`** — `object`

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

- **Penetration Tester (Thick Client):** OWASP testing practice for thick clients; PTES; platform security documentation. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-penetration-tester-thick-client-4"></a>

## remediation guidance

**At a glance**

- **Purpose:** Produce and govern the role deliverable: remediation guidance.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `penetration-tester-thick-client:4`.

**Required inputs:**

- Signed authorisation and scope
- Application installers and documentation
- Test accounts and server scope
- Supported platform matrix

**Specification:** `kind/role/penetration-tester-thick-client:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: remediation guidance.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/penetration-tester-thick-client:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: remediation guidance.

**`role/penetration-tester-thick-client:4.receiving_acceptance`** — `array`

- For each receiving role (Software Engineer; Application Security Engineer), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/penetration-tester-thick-client:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/penetration-tester-thick-client:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/penetration-tester-thick-client:4.delivery_verification`** — `array`

- For the specific output 'remediation guidance', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/penetration-tester-thick-client:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Written authorisation, signed scope and rules of engagement exist and are current before a single packet is sent.
- G2: All targets are confirmed in scope and owned by the authorising party; anything out of scope is stopped and reported immediately.
- G3: Emergency stop conditions and contacts are agreed and tested before execution.
- G4: Sensitive data encountered is minimised, protected, reported and destroyed per the engagement agreement.
- G5: Findings state whether the server validates independently
- G6: a client-side control bypass is only material where the server trusts the client, and the report must say which

**`role/penetration-tester-thick-client:4.contract_input_1`** — `object`

- Analyse the specific input "Signed authorisation and scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:4.contract_input_2`** — `object`

- Analyse the specific input "Application installers and documentation" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:4.contract_input_3`** — `object`

- Analyse the specific input "Test accounts and server scope" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/penetration-tester-thick-client:4.contract_input_4`** — `object`

- Analyse the specific input "Supported platform matrix" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/penetration-tester-thick-client:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/penetration-tester-thick-client:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/penetration-tester-thick-client:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/penetration-tester-thick-client:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/penetration-tester-thick-client:4.irrelevant_detail`** — `object`

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

- **Penetration Tester (Thick Client):** OWASP testing practice for thick clients; PTES; platform security documentation. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
