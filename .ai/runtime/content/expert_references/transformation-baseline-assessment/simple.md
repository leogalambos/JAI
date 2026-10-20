---
reference_id: example:transformation-baseline-assessment:simple
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: transformation-baseline-assessment
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/transformation-baseline-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: HFS-FAR
methodology_context: "TOGAF-inspired baseline/target architecture and evidence-led capability assessment"
---

# Enterprise transformation baseline and capability assessment — Field Appointment Reliability

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** technician appointment scheduling. **Context:** Harborline Field Services. **Complexity:** simple. **Status:** proposed pilot; no exercised build or customer evidence. **Decision authority:** Field Operations Manager, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-transformation-baseline-assessment.baseline_boundary"></a>
## 1. Baseline boundary

Baseline scope: **technician appointment scheduling** serving **dispatchers, technicians and a service desk**. The current state is **a shared spreadsheet and a fragile legacy dispatcher** under **2,100 appointments per week across 240 technicians**. The assessment answers what is actually known, what prevents business outcomes and which capabilities need change; it does not start by assuming the preferred technology is correct. Stakeholders: Field Operations Manager for outcomes, Application Lead for architecture evidence, Service Desk Lead for service continuity and Security Lead for risk. Unknown vendor obligations, personal-data flows and jurisdiction applicability are explicitly open.

<a id="dcs-proposed-transformation-baseline-assessment.capability_evidence"></a>
## 2. Capability evidence

Use capability IDs for business demand, processes, people, information, applications and technology. For each, distinguish current owner, service users, observed outcomes, interfaces, operating evidence and maturity confidence. The example capabilities include order/appointment/settlement acceptance, identity and authorization, reconciliation, incident recovery and change authorization. Rate evidence sufficiency on observed records, interviews and modelled assumptions separately. A 'mature' self-assessment without process logs is a hypothesis, not a measured baseline.

<a id="dcs-proposed-transformation-baseline-assessment.pain_points"></a>
## 3. Pain points

Material pain points: **service outage and unwanted appointment duplication** and **a duplicated callback creates two technician assignments**. Establish baseline for **duplicate-booking count and unacknowledged appointment queue age**, lead time from request to completed business outcome, manual reconciliation work, failed-change rate and support burden. Do not invent baseline measurements from the synthetic operating target. Each issue has a causal hypothesis, business owner, affected population, evidence gap and counterfactual challenge. Retain competing explanations such as poor identity policy rather than immediately blaming an integration platform.

### Worked assessment matrix (synthetic)

| Capability | Current observation | Evidence confidence | Next verification |
|---|---|---|---|
| Business outcome | a shared spreadsheet and a fragile legacy dispatcher | Hypothesis | Baseline measure |
| Data lineage | Multi-component state dependencies | Not observed | Source-to-target trace |
| Operational readiness | Alert & recovery ownership unclear | Not observed | Service review |
| Security governance | Entity and role policy unknown | Not verified | Control mapping |

The matrix is a proposed verification instrument for **technician appointment scheduling**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-transformation-baseline-assessment.dependency_map"></a>
## 4. Dependency map

Model dependencies across systems, suppliers, skills, data ownership, operational teams and external obligations. The critical chain is **dispatch portal → booking API → authoritative appointment store → notification worker**. Distinguish a shared runtime failure domain from organizational coupling (e.g., the only approving specialist). Mark boundaries where independent assurance is required. For the planned transition, map candidate changes onto upstream/downstream consumers, data transformations, controls and sunset obligations. A capability cannot be considered isolated if its data or identity service remains shared.

<a id="dcs-proposed-transformation-baseline-assessment.gap_prioritisation"></a>
## 5. Gap prioritisation

Prioritize gaps using business impact, urgency, effort, evidence confidence and regulatory constraints. Use ordered bands rather than false precision: immediate safety/control correction; validated high-value intervention; deferred low-value convenience. A gap may be critical due to absent evidence even when no failure has yet been observed. Protect scope boundaries and no-regression conditions; avoid forcing all legacy components into replacement when a safer process fix suffices. Funding estimates are provisional until finance validates the baseline.

<a id="dcs-proposed-transformation-baseline-assessment.baseline_decision"></a>
## 6. Baseline decision

Recommendation: establish an evidenced baseline before committing to **a managed scheduling SaaS with a one-way dispatch sync**. Approve only bounded discovery, instrumentation and controlled proof activities first. Entry conditions for target-design approval: verified data authority, risk taxonomy, ownership of the critical interfaces, observed service metrics and residual unknowns. The report is suitable for transformation decision support, not a certificate of enterprise maturity.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| HFS-FAR-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| HFS-FAR-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| HFS-FAR-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| HFS-FAR-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `HFS-FAR-REQ-01` traced to business owner; exact build `HFS-FAR-BUILD-01` and change `HFS-FAR-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **a duplicated callback creates two technician assignments**; completed handoff acknowledged by Service Desk Lead. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** HFS-FAR-REQ → HFS-FAR-ARCH → HFS-FAR-SEC → HFS-FAR-BUILD → HFS-FAR-TEST → HFS-FAR-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** TOGAF-inspired baseline/target architecture and evidence-led capability assessment. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
