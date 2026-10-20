---
reference_id: example:threat-model:complex
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: threat-model
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/threat-model
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: OPG-RSM
methodology_context: "Structured asset/trust-boundary threat modeling and OWASP application security design principles"
---

# Structured threat model and trust-boundary assessment — Regulated Settlement Modernisation

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-border settlement instruction processing and finality reconciliation. **Context:** Orion Payments Group. **Complexity:** complex. **Status:** proposed transformation; no enacted jurisdictional approval or production evidence. **Decision authority:** Group Payments Executive, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-threat-model.assets_and_scope"></a>
## 1. Assets and scope

Model **cross-border settlement instruction processing and finality reconciliation** with assets: accepted business state, authorisation decisions, user personal data (**payer/payee identifiers, transaction metadata, finality state and restricted audit records**) and operational recovery evidence. Trust boundary: **channel boundary → policy decision → immutable journal → regulated ledger and regional processors**. Define system context, in/out scope, likely threat actors (external caller, compromised integration identity, inadvertent operator), assumptions and exposed interfaces. The expected business invariant is **each authorised instruction has immutable lineage and zero unexplained unmatched finality amounts**; a 'successful HTTP response' is not the protected asset. The model describes hypotheses only, not observed compromise.

<a id="dcs-proposed-threat-model.trust_flows"></a>
## 2. Trust flows

Data-flow diagram source: **channel → policy gateway → signed journal → settlement orchestration → ledger / regional connector → reconciliation**. Number each crossing and assign initiating actor, data class, authoritative service and authentication/authorization mechanism. Mark where attacker-controlled metadata enters; do not trust client-supplied jurisdiction or tenant claims. Differentiate a processing queue from final business state and identify where integrity reconciliation occurs. In more complex systems, include supplier APIs and shared policy/identity failure domains.

<a id="dcs-proposed-threat-model.threat_scenarios"></a>
## 3. Threat scenarios

Scenario T-01 **a privileged policy change enables unauthorised cross-jurisdiction routing**: precondition is a stale or overprivileged identity / malformed event; vulnerable condition is insufficient independent authorization or deduplication; business impact is **financial integrity, data-residency breach and loss of transaction finality**. T-02 compromised supply chain or pipeline identity changes a deployable artifact; T-03 dependency outage disrupts reconciliation and causes uncertain state. Rate risk qualitatively using the organization's actual scoring method. Do not assign probability from fictional examples; demonstrate uncertainty and ownership.

### Worked design matrix (synthetic)

| Threat ID | Initiating condition | Business impact | Proposed guard |
|---|---|---|---|
| TH-01 | a privileged policy change enables unauthorised cross-jurisdiction routing | financial integrity, data-residency breach and loss of transaction finality | Server-side policy + business idempotency |
| TH-02 | Altered release binary | Unauthorized behavior | Signed provenance + exact digest |
| TH-03 | Dependency unavailable | Unknown final state | Checkpoint + reconciliation |
| TH-04 | Wrong-tenant route | Protected-data disclosure | Identity and entity policy validation |

The matrix is a proposed verification instrument for **cross-border settlement instruction processing and finality reconciliation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-threat-model.security_controls"></a>
## 4. Security controls

Preventive controls: workload identity, least-privilege policy, binding of business key to tenant/entity, contract/schema validation, deterministic idempotency and protected CI promotion. Detective controls: immutable audit events, anomalous route alerts, reconciliation mismatches and privilege drift. Recovery: **freeze new acceptance and perform authorised compensating reconciliation; never reverse finalised ledgers as a generic rollback**. Distinguish controls implemented from controls merely proposed. A fail-open exception is not acceptable without explicit competent authority and relevant legal permissibility.

<a id="dcs-proposed-threat-model.validation_plan"></a>
## 5. Validation plan

Test cases include wrong-tenant identity, replay of an accepted business key, malformed or stale schema, unsigned build replacement, lost acknowledgment, multi-supplier timeout and recovery under **30 minutes/5 minutes**. Each negative case specifies expected rejection/controlled-pending outcome and audit observation; detailed exploitation instructions are unnecessary. Measure **finality reconciliation exceptions, policy-denied jurisdiction routes and settlement cut-off lag** and zero unexplained business-state divergence for the tested scope. No tests were actually executed in this synthetic model.

### Dependency and challenge analysis

For OPG-RSM, a release or transformation claim is invalid if **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning channel boundary → policy decision → immutable journal → regulated ledger and regional processors, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-threat-model.residual_risk"></a>
## 6. Residual risk

Open risk: **financial integrity, data-residency breach and loss of transaction finality**. Assign treatment owner Enterprise Financial Risk Officer, engineering implementation owner Chief Payments Architect and independent challenger Enterprise Financial Risk Officer. Propose decision to defer production until critical attack paths have validated controls, acceptable residual risk and tested recovery. Changes to interface trust boundaries, suppliers, privilege model or data jurisdiction trigger review. No approval inferred from a completed threat-model form.

## Enterprise-level adversarial review and exceptional paths

**Compound failure exercise:** independently simulate supplier unavailability, revocation of a privileged deployment identity and loss of trustworthy state observations. The safety response must be bounded: freeze new acceptance and perform authorised compensating reconciliation; never reverse finalised ledgers as a generic rollback. The test never permits bypassing jurisdictional or risk authority; every state-changing activity needs a decision owner, reversible boundary, observed invariant and auditable approval.

**Jurisdiction and third-party boundary:** do not assume an authorization in one market extends to another or that a supplier statement covers the entire fourteen jurisdictions, three failure domains, regional connectors, dual-run ledger, evidence store. A transition must preserve retention and finality duties, business data ownership, security of pipeline credentials and a record of exceptions with expiry.

**Contested decision:** compare the recommended approach **append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints** with maintaining the baseline and an aggressive fast-cutover alternative. Ask what evidence would invalidate the preference and estimate the operational consequence of an unplanned halt during **an eighteen-month phased programme with parallel-run cut-offs**. Neither an attractive ROI nor a technically green build overrides a critical missing control or competent stakeholder approval.

## Example decision register

| Decision | Alternatives / objections | Evidence needed | Owner and status |
|---|---|---|---|
| DR-01 — approve scoped approach | append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints vs controlled baseline | Business invariant and dependency mapping | Group Payments Executive — OPEN |
| DR-02 — permit protected integration | Deny or quarantine unknown actor/entity vs permissive routing | Independent negative authorization and reconciliation | Enterprise Financial Risk Officer — OPEN |
| DR-03 — accept operations handover | Reversible pilot vs direct cutover | 30 minutes/5 minutes timed recovery, staffed on-call | Critical Service Operations Director — OPEN |

All decision IDs above are local worked-example identifiers; they are not proof that any person approved or that underlying evidence exists.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| OPG-RSM-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| OPG-RSM-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| OPG-RSM-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| OPG-RSM-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `OPG-RSM-REQ-01` traced to business owner; exact build `OPG-RSM-BUILD-01` and change `OPG-RSM-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **unexplained ledger imbalance or illegal cross-region failover invalidates settlement finality**; completed handoff acknowledged by Critical Service Operations Director. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** OPG-RSM-REQ → OPG-RSM-ARCH → OPG-RSM-SEC → OPG-RSM-BUILD → OPG-RSM-TEST → OPG-RSM-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** Structured asset/trust-boundary threat modeling and OWASP application security design principles. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
