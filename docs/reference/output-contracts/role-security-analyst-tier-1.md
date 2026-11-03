<!-- JAI:OUTPUT-CONTRACTS:START -->
# Security Analyst Tier 1: output contracts

Triage security alerts quickly and accurately so that real threats reach the right people fast

[Full catalogue](index.md)

<a id="output-security-analyst-tier-1-1"></a>

## Alert triage records with verdict and rationale

**At a glance**

- **Purpose:** Produce and govern the role deliverable: Alert triage records with verdict and rationale.
- **Mandatory examples:** Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks. Provide actual uniquely identified records with source, owner, status and review date. Define required columns, datatypes, identifiers, allowed states and ownership.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `security-analyst-tier-1:1`.

**Required inputs:**

- Alert queue
- Triage playbooks
- Asset criticality context
- Threat intelligence context

**Specification:** `kind/role/security-analyst-tier-1:1`; **content version:** `1.2.0`.

Produce and govern the role deliverable: Alert triage records with verdict and rationale.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/register`](spec-type-register.md)
- [`domain/data`](spec-domain-data.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/security-analyst-tier-1:1.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: Alert triage records with verdict and rationale.

**`role/security-analyst-tier-1:1.receiving_acceptance`** — `array`

- For each receiving role (Security Analyst Tier 2; Incident Responder), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/security-analyst-tier-1:1.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/security-analyst-tier-1:1.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/security-analyst-tier-1:1.delivery_verification`** — `array`

- For the specific output 'Alert triage records with verdict and rationale', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/security-analyst-tier-1:1.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: No alert is closed as benign without a recorded reason
- G6: bulk closure of a queue is treated as a control failure, not as productivity

**`role/security-analyst-tier-1:1.contract_input_1`** — `object`

- Analyse the specific input "Alert queue" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:1.contract_input_2`** — `object`

- Analyse the specific input "Triage playbooks" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:1.contract_input_3`** — `object`

- Analyse the specific input "Asset criticality context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:1.contract_input_4`** — `object`

- Analyse the specific input "Threat intelligence context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/security-analyst-tier-1:1.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/security-analyst-tier-1:1.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/security-analyst-tier-1:1.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/security-analyst-tier-1:1.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/security-analyst-tier-1:1.irrelevant_detail`** — `object`

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

### Role framework context

- **Security Analyst Tier 1:** MITRE ATT&CK; NIST SP 800-61; SOC triage playbooks. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-security-analyst-tier-1-2"></a>

## escalation handovers

**At a glance**

- **Purpose:** Produce and govern the role deliverable: escalation handovers.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `security-analyst-tier-1:2`.

**Required inputs:**

- Alert queue
- Triage playbooks
- Asset criticality context
- Threat intelligence context

**Specification:** `kind/role/security-analyst-tier-1:2`; **content version:** `1.2.0`.

Produce and govern the role deliverable: escalation handovers.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/security-analyst-tier-1:2.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: escalation handovers.

**`role/security-analyst-tier-1:2.receiving_acceptance`** — `array`

- For each receiving role (Security Analyst Tier 2; Incident Responder), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/security-analyst-tier-1:2.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/security-analyst-tier-1:2.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/security-analyst-tier-1:2.delivery_verification`** — `array`

- For the specific output 'escalation handovers', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/security-analyst-tier-1:2.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: No alert is closed as benign without a recorded reason
- G6: bulk closure of a queue is treated as a control failure, not as productivity

**`role/security-analyst-tier-1:2.contract_input_1`** — `object`

- Analyse the specific input "Alert queue" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:2.contract_input_2`** — `object`

- Analyse the specific input "Triage playbooks" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:2.contract_input_3`** — `object`

- Analyse the specific input "Asset criticality context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:2.contract_input_4`** — `object`

- Analyse the specific input "Threat intelligence context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/security-analyst-tier-1:2.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/security-analyst-tier-1:2.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/security-analyst-tier-1:2.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/security-analyst-tier-1:2.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/security-analyst-tier-1:2.irrelevant_detail`** — `object`

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

- **Security Analyst Tier 1:** MITRE ATT&CK; NIST SP 800-61; SOC triage playbooks. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-security-analyst-tier-1-3"></a>

## enrichment and initial scoping notes

**At a glance**

- **Purpose:** Produce and govern the role deliverable: enrichment and initial scoping notes.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `security-analyst-tier-1:3`.

**Required inputs:**

- Alert queue
- Triage playbooks
- Asset criticality context
- Threat intelligence context

**Specification:** `kind/role/security-analyst-tier-1:3`; **content version:** `1.2.0`.

Produce and govern the role deliverable: enrichment and initial scoping notes.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/security-analyst-tier-1:3.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: enrichment and initial scoping notes.

**`role/security-analyst-tier-1:3.receiving_acceptance`** — `array`

- For each receiving role (Security Analyst Tier 2; Incident Responder), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/security-analyst-tier-1:3.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/security-analyst-tier-1:3.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/security-analyst-tier-1:3.delivery_verification`** — `array`

- For the specific output 'enrichment and initial scoping notes', provide verifiable evidence satisfying: Reviewed by a competent second party; complete, dated and attributable. Required delivery form: Versioned artefact in the agreed system of record.

**`role/security-analyst-tier-1:3.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: No alert is closed as benign without a recorded reason
- G6: bulk closure of a queue is treated as a control failure, not as productivity

**`role/security-analyst-tier-1:3.contract_input_1`** — `object`

- Analyse the specific input "Alert queue" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:3.contract_input_2`** — `object`

- Analyse the specific input "Triage playbooks" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:3.contract_input_3`** — `object`

- Analyse the specific input "Asset criticality context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:3.contract_input_4`** — `object`

- Analyse the specific input "Threat intelligence context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/security-analyst-tier-1:3.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/security-analyst-tier-1:3.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/security-analyst-tier-1:3.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/security-analyst-tier-1:3.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/security-analyst-tier-1:3.irrelevant_detail`** — `object`

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

- **Security Analyst Tier 1:** MITRE ATT&CK; NIST SP 800-61; SOC triage playbooks. Canonical role context; not proof that every listed framework applies to this output.


<a id="output-security-analyst-tier-1-4"></a>

## detection feedback for tuning

**At a glance**

- **Purpose:** Produce and govern the role deliverable: detection feedback for tuning.
- **Mandatory examples:** Identify decisions or downstream uses, accountable recipients and verifiable next actions. Provide attributable substantive findings, reasoning and limitations for the specific subject. Identify document purpose, audience, subject boundary and authoritative source versions.
- **Conditions to resolve:** personal data are processed; an applicable regulatory requirement exists. Unknown applicability remains unresolved.
- **Optional example:** Include versioned calculations, logs or technical detail only when linked to a specific required claim.
- **Review:** assess substantive content, evidence and gaps against the full selected contract; acceptance and release remain separate.

This orientation gives selected examples. The complete local and linked foundation requirements, prohibitions and evidence duties below remain applicable.

**Contract ID:** `security-analyst-tier-1:4`.

**Required inputs:**

- Alert queue
- Triage playbooks
- Asset criticality context
- Threat intelligence context

**Specification:** `kind/role/security-analyst-tier-1:4`; **content version:** `1.2.0`.

Produce and govern the role deliverable: detection feedback for tuning.

**Status:** proposed/advisory; publication of this contract does not approve it, certify a delivered output or grant acceptance/release. MUST describes the stated JAI content obligation, not a claim that an external standard mandates it.

**Also applicable:** all requirements in these linked foundations and overlays form part of this contract, subject to their explicit conditions:

- [`global/invariants`](spec-global-invariants.md)
- [`type/document`](spec-type-document.md)
- [`domain/delivery`](spec-domain-delivery.md)

Conditions below are not evaluated for a hypothetical engagement. Unknown applicability stays unresolved; it does not mean that the requirement may be omitted. Required information can be carried in prose, structured records or referenced material; matching a heading alone does not demonstrate quality.

**Evidence policy for the following units:** versioned source reference or explicitly labelled assumption; retain pending status and identify owner; never fabricate.

### Required information (MUST)

**`role/security-analyst-tier-1:4.delivery_scope`** — `object`

- Identify the subject entities, boundaries, outcomes and versioned sources for: Produce and govern the role deliverable: detection feedback for tuning.

**`role/security-analyst-tier-1:4.receiving_acceptance`** — `array`

- For each receiving role (Security Analyst Tier 2; Incident Responder), identify the concrete downstream use, requested action, acceptance measure and accountable recipient.

**`role/security-analyst-tier-1:4.contract_relations`** — `array`

- Identify actual entity IDs and relationship instances for: owner_role -> receiving_roles; material claims -> evidence; decision -> approver where approval is required.

**`role/security-analyst-tier-1:4.decision_purpose_correction`** — `object`

- Identify the specific downstream operational action or choice, its accountable recipient and competent authority; confirm or correct the source-derived proposed action without inventing approval.

**`role/security-analyst-tier-1:4.delivery_verification`** — `array`

- For the specific output 'detection feedback for tuning', provide verifiable evidence satisfying: Mapped to an ATT&CK technique, with documented true- and false-positive behaviour. Required delivery form: Detection rule in version control with test cases.

**`role/security-analyst-tier-1:4.role_gate_observations`** — `array`

- Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.
- G1: Nothing is declared a false positive without a recorded reason; unexplained closures hide real intrusions.
- G2: Evidence handling preserves integrity and chain of custody wherever legal or disciplinary action is conceivable.
- G3: Containment actions with business impact are authorised at the agreed level before execution.
- G4: Regulatory notification clocks (e.g. GDPR 72 hours, NIS2/DORA timelines) are assessed explicitly and the assessment is recorded.
- G5: No alert is closed as benign without a recorded reason
- G6: bulk closure of a queue is treated as a control failure, not as productivity

**`role/security-analyst-tier-1:4.contract_input_1`** — `object`

- Analyse the specific input "Alert queue" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:4.contract_input_2`** — `object`

- Analyse the specific input "Triage playbooks" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:4.contract_input_3`** — `object`

- Analyse the specific input "Asset criticality context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

**`role/security-analyst-tier-1:4.contract_input_4`** — `object`

- Analyse the specific input "Threat intelligence context" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.

### Conditionally required information

**`role/security-analyst-tier-1:4.privacy_analysis`** — `object`

Applies when: `{"field": "processes_personal_data", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.

**`role/security-analyst-tier-1:4.regulatory_analysis`** — `object`

Applies when: `{"field": "regulatory_requirement", "op": "eq", "value": true}`. If the needed context is unknown, resolve it before claiming completeness.

- Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.

### Optional information (MAY)

**`role/security-analyst-tier-1:4.supporting_annex`** — `object`

- Include versioned calculations, logs or technical detail only when linked to a specific required claim.

### Prohibited content (MUST NOT)

**`role/security-analyst-tier-1:4.unsupported_material_claim`** — `object`

- Do not assert material conclusions without dated evidence or an explicitly labelled assumption.

### Content to omit unless justified

**`role/security-analyst-tier-1:4.irrelevant_detail`** — `object`

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

- **Security Analyst Tier 1:** MITRE ATT&CK; NIST SP 800-61; SOC triage playbooks. Canonical role context; not proof that every listed framework applies to this output.
<!-- JAI:OUTPUT-CONTRACTS:END -->
