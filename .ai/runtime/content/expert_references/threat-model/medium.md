---
reference_id: example:threat-model:medium
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: threat-model
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/threat-model
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: MRG-OEI
methodology_context: "Structured asset/trust-boundary threat modeling and OWASP application security design principles"
---

# Structured threat model and trust-boundary assessment — Order Event Integration

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-channel order ingestion and ERP fulfilment synchronisation. **Context:** Meridian Retail Group. **Complexity:** medium. **Status:** proposed phased delivery; no live ERP, market or regulatory evidence. **Decision authority:** Digital Commerce Sponsor, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-threat-model.assets_and_scope"></a>
## 1. Assets and scope

Model **cross-channel order ingestion and ERP fulfilment synchronisation** with assets: accepted business state, authorisation decisions, user personal data (**order ID, pseudonymous customer link, delivery address and fulfilment status**) and operational recovery evidence. Trust boundary: **commerce cloud → broker → region-scoped ERP service**. Define system context, in/out scope, likely threat actors (external caller, compromised integration identity, inadvertent operator), assumptions and exposed interfaces. The expected business invariant is **every accepted order has one explainable final ERP state and an evidence trail**; a 'successful HTTP response' is not the protected asset. The model describes hypotheses only, not observed compromise.

<a id="dcs-proposed-threat-model.trust_flows"></a>
## 2. Trust flows

Data-flow diagram source: **commerce write → transactional outbox → broker → idempotent ERP adapter → reconciliation**. Number each crossing and assign initiating actor, data class, authoritative service and authentication/authorization mechanism. Mark where attacker-controlled metadata enters; do not trust client-supplied jurisdiction or tenant claims. Differentiate a processing queue from final business state and identify where integrity reconciliation occurs. In more complex systems, include supplier APIs and shared policy/identity failure domains.

<a id="dcs-proposed-threat-model.threat_scenarios"></a>
## 3. Threat scenarios

Scenario T-01 **country-routing error or privileged replay of events**: precondition is a stale or overprivileged identity / malformed event; vulnerable condition is insufficient independent authorization or deduplication; business impact is **customer-data misrouting, delayed order promises and incomplete reconciliation**. T-02 compromised supply chain or pipeline identity changes a deployable artifact; T-03 dependency outage disrupts reconciliation and causes uncertain state. Rate risk qualitatively using the organization's actual scoring method. Do not assign probability from fictional examples; demonstrate uncertainty and ownership.

### Worked design matrix (synthetic)

| Threat ID | Initiating condition | Business impact | Proposed guard |
|---|---|---|---|
| TH-01 | country-routing error or privileged replay of events | customer-data misrouting, delayed order promises and incomplete reconciliation | Server-side policy + business idempotency |
| TH-02 | Altered release binary | Unauthorized behavior | Signed provenance + exact digest |
| TH-03 | Dependency unavailable | Unknown final state | Checkpoint + reconciliation |
| TH-04 | Wrong-tenant route | Protected-data disclosure | Identity and entity policy validation |

The matrix is a proposed verification instrument for **cross-channel order ingestion and ERP fulfilment synchronisation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-threat-model.security_controls"></a>
## 4. Security controls

Preventive controls: workload identity, least-privilege policy, binding of business key to tenant/entity, contract/schema validation, deterministic idempotency and protected CI promotion. Detective controls: immutable audit events, anomalous route alerts, reconciliation mismatches and privilege drift. Recovery: **stop affected consumers, preserve offsets, correct mapping and reconcile before replay**. Distinguish controls implemented from controls merely proposed. A fail-open exception is not acceptable without explicit competent authority and relevant legal permissibility.

<a id="dcs-proposed-threat-model.validation_plan"></a>
## 5. Validation plan

Test cases include wrong-tenant identity, replay of an accepted business key, malformed or stale schema, unsigned build replacement, lost acknowledgment, multi-supplier timeout and recovery under **2 hours/15 minutes**. Each negative case specifies expected rejection/controlled-pending outcome and audit observation; detailed exploitation instructions are unnecessary. Measure **p95 broker-to-ERP lag, replay rejection and unmatched order IDs** and zero unexplained business-state divergence for the tested scope. No tests were actually executed in this synthetic model.

### Dependency and challenge analysis

For MRG-OEI, a release or transformation claim is invalid if **country data-handling decisions, broker retention, ERP freeze windows and vendor SLAs** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning commerce cloud → broker → region-scoped ERP service, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-threat-model.residual_risk"></a>
## 6. Residual risk

Open risk: **customer-data misrouting, delayed order promises and incomplete reconciliation**. Assign treatment owner Head of Digital Risk, engineering implementation owner Integration Architect and independent challenger Head of Digital Risk. Propose decision to defer production until critical attack paths have validated controls, acceptable residual risk and tested recovery. Changes to interface trust boundaries, suppliers, privilege model or data jurisdiction trigger review. No approval inferred from a completed threat-model form.

## Example decision register

| Decision | Alternatives / objections | Evidence needed | Owner and status |
|---|---|---|---|
| DR-01 — approve scoped approach | transactional outbox plus managed broker with a quarantine stream and idempotent consumers vs controlled baseline | Business invariant and dependency mapping | Digital Commerce Sponsor — OPEN |
| DR-02 — permit protected integration | Deny or quarantine unknown actor/entity vs permissive routing | Independent negative authorization and reconciliation | Head of Digital Risk — OPEN |
| DR-03 — accept operations handover | Reversible pilot vs direct cutover | 2 hours/15 minutes timed recovery, staffed on-call | Service Operations Manager — OPEN |

All decision IDs above are local worked-example identifiers; they are not proof that any person approved or that underlying evidence exists.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| MRG-OEI-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| MRG-OEI-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| MRG-OEI-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| MRG-OEI-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `MRG-OEI-REQ-01` traced to business owner; exact build `MRG-OEI-BUILD-01` and change `MRG-OEI-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **duplicate or out-of-order messages create an incorrect fulfilment state**; completed handoff acknowledged by Service Operations Manager. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** MRG-OEI-REQ → MRG-OEI-ARCH → MRG-OEI-SEC → MRG-OEI-BUILD → MRG-OEI-TEST → MRG-OEI-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** Structured asset/trust-boundary threat modeling and OWASP application security design principles. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
