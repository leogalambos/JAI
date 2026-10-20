---
reference_id: example:threat-model:simple
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: threat-model
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/threat-model
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: HFS-FAR
methodology_context: "Structured asset/trust-boundary threat modeling and OWASP application security design principles"
---

# Structured threat model and trust-boundary assessment — Field Appointment Reliability

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** technician appointment scheduling. **Context:** Harborline Field Services. **Complexity:** simple. **Status:** proposed pilot; no exercised build or customer evidence. **Decision authority:** Field Operations Manager, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-threat-model.assets_and_scope"></a>
## 1. Assets and scope

Model **technician appointment scheduling** with assets: accepted business state, authorisation decisions, user personal data (**technician identity, customer address and appointment window**) and operational recovery evidence. Trust boundary: **SaaS webhook → enterprise integration boundary**. Define system context, in/out scope, likely threat actors (external caller, compromised integration identity, inadvertent operator), assumptions and exposed interfaces. The expected business invariant is **dispatch and booking identifiers reconcile to the authoritative SaaS record**; a 'successful HTTP response' is not the protected asset. The model describes hypotheses only, not observed compromise.

<a id="dcs-proposed-threat-model.trust_flows"></a>
## 2. Trust flows

Data-flow diagram source: **dispatch portal → booking API → authoritative appointment store → notification worker**. Number each crossing and assign initiating actor, data class, authoritative service and authentication/authorization mechanism. Mark where attacker-controlled metadata enters; do not trust client-supplied jurisdiction or tenant claims. Differentiate a processing queue from final business state and identify where integrity reconciliation occurs. In more complex systems, include supplier APIs and shared policy/identity failure domains.

<a id="dcs-proposed-threat-model.threat_scenarios"></a>
## 3. Threat scenarios

Scenario T-01 **duplicate scheduling after webhook replay**: precondition is a stale or overprivileged identity / malformed event; vulnerable condition is insufficient independent authorization or deduplication; business impact is **service outage and unwanted appointment duplication**. T-02 compromised supply chain or pipeline identity changes a deployable artifact; T-03 dependency outage disrupts reconciliation and causes uncertain state. Rate risk qualitatively using the organization's actual scoring method. Do not assign probability from fictional examples; demonstrate uncertainty and ownership.

### Worked design matrix (synthetic)

| Threat ID | Initiating condition | Business impact | Proposed guard |
|---|---|---|---|
| TH-01 | duplicate scheduling after webhook replay | service outage and unwanted appointment duplication | Server-side policy + business idempotency |
| TH-02 | Altered release binary | Unauthorized behavior | Signed provenance + exact digest |
| TH-03 | Dependency unavailable | Unknown final state | Checkpoint + reconciliation |
| TH-04 | Wrong-tenant route | Protected-data disclosure | Identity and entity policy validation |

The matrix is a proposed verification instrument for **technician appointment scheduling**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-threat-model.security_controls"></a>
## 4. Security controls

Preventive controls: workload identity, least-privilege policy, binding of business key to tenant/entity, contract/schema validation, deterministic idempotency and protected CI promotion. Detective controls: immutable audit events, anomalous route alerts, reconciliation mismatches and privilege drift. Recovery: **reconcile against exported accepted bookings, never replay acknowledgements blindly**. Distinguish controls implemented from controls merely proposed. A fail-open exception is not acceptable without explicit competent authority and relevant legal permissibility.

<a id="dcs-proposed-threat-model.validation_plan"></a>
## 5. Validation plan

Test cases include wrong-tenant identity, replay of an accepted business key, malformed or stale schema, unsigned build replacement, lost acknowledgment, multi-supplier timeout and recovery under **8 hours/24 hours**. Each negative case specifies expected rejection/controlled-pending outcome and audit observation; detailed exploitation instructions are unnecessary. Measure **duplicate-booking count and unacknowledged appointment queue age** and zero unexplained business-state divergence for the tested scope. No tests were actually executed in this synthetic model.

<a id="dcs-proposed-threat-model.residual_risk"></a>
## 6. Residual risk

Open risk: **service outage and unwanted appointment duplication**. Assign treatment owner Head of Operations, engineering implementation owner Application Lead and independent challenger Security Lead. Propose decision to defer production until critical attack paths have validated controls, acceptable residual risk and tested recovery. Changes to interface trust boundaries, suppliers, privilege model or data jurisdiction trigger review. No approval inferred from a completed threat-model form.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| HFS-FAR-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| HFS-FAR-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| HFS-FAR-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| HFS-FAR-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `HFS-FAR-REQ-01` traced to business owner; exact build `HFS-FAR-BUILD-01` and change `HFS-FAR-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **a duplicated callback creates two technician assignments**; completed handoff acknowledged by Service Desk Lead. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** HFS-FAR-REQ → HFS-FAR-ARCH → HFS-FAR-SEC → HFS-FAR-BUILD → HFS-FAR-TEST → HFS-FAR-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** Structured asset/trust-boundary threat modeling and OWASP application security design principles. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
