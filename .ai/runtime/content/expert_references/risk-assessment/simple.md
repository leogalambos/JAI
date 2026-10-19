---
reference_id: example:risk-assessment:simple
schema_version: '1.0.0'
document_kind: risk-assessment
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/risk-assessment
approval_status: not-human-approved
---

> **SYNTHETIC EXPERT EXAMPLE — NOT AN APPROVED PROJECT RECORD.** Every organisation, date, amount, performance result, evidence reference and approval below is invented for demonstration. Frameworks guide professional structure, but this document claims neither regulatory conformance nor independent expert certification. Never reuse facts as production evidence.

**Case:** Harborline Field Services · Field Appointment Reliability · `HFS-FAR` · SIMPLE complexity. **Status:** illustrative proposal; L0 approval absent. **Decision/action authority:** Field Operations Manager. **Scope:** single-business-unit, low-coupling rollout.

# Information-security and service risk assessment — Field Appointment Reliability

<a id="dcs-risk-assessment.assessment_scope"></a>
## Assessment scope and assets at risk

Risk assessment `HFS-FAR-RA-01` covers technician appointment scheduling and the supporting boundary one internal scheduling service, managed identity provider, dispatch integration and managed booking SaaS. Business asset: reliable fulfilment of reduce appointment rework from an illustrative 2.3% to at most 0.5% within two quarters; information asset: technician names, customer addresses and appointment times; technology assets: integration interfaces, identity plane, state stores and telemetry. Exposure: internal business service; no payment-card data.

Assessment owner is Head of Operations; independent reviewer remains unassigned. This document is an illustrative analysis only; real owners must establish the applicable legal/regulatory obligations for each operating location.

<a id="dcs-risk-assessment.scoring_method"></a>
## Scoring method and decision appetite

Working qualitative 5×5 method: likelihood 1 (rare) to 5 (frequent); impact 1 (negligible) to 5 (critical interruption, compromise or liability); product gives a **relative prioritisation score**, not a probabilistic annual-loss estimate. Bands: 1–5 low, 6–10 moderate, 11–15 high, 16–25 severe.

Risk appetite is assumed for this synthetic exercise: no severe untreated risk may move to production; high residual risk requires named executive acceptance and documented compensating controls. The actual organisation must substitute its approved appetite and scoring rubric; regulatory breaches cannot be made acceptable by selecting a low number.

<a id="dcs-risk-assessment.risk_scenarios"></a>
## Threat-event scenarios and supporting assumptions

The critical initiating events include vendor availability and duplicated appointment updates, operator error and malicious misuse of privileged interfaces. A failure may cause loss or duplication of business records, unavailable processing or unauthorised disclosure. Threat and control effectiveness are hypotheses; no production penetration test, audit or outage history was available for the fictional organisation.

Evidence obligations: service-dependency map `HFS-FAR-E-MAP`, access review `HFS-FAR-E-IAM`, recovery exercises `HFS-FAR-E-REC` and lineage/reconciliation sample `HFS-FAR-E-LOG`. The consequence is evaluated for each business process and recovery time window rather than assuming technical availability equals business continuity.

<a id="dcs-risk-assessment.risk_evaluation"></a>
## Inherent and residual risk evaluation

| ID | Scenario | Inherent L×I | Residual L×I | Treatment/control hypothesis | Risk owner |
|---|---|---:|---:|---|---|
| R-01 | Vendor outage prevents scheduling | 3 × 4 = 12 | 2 × 4 = 8 | Export cache, rehearsed 8 h recovery | Head of Operations |
| R-02 | Duplicate webhook produces two assignments | 4 × 3 = 12 | 2 × 3 = 6 | Business-key idempotency, daily reconciliation | Application Lead |

All control-related residual scores are **projections contingent on test evidence**; they are not claims that mitigations have been implemented. There is no statistical confidence claim for the likelihood values. A measured control failure reopens the corresponding assessment and invalidates any contingent approval.

<a id="dcs-risk-assessment.risk_treatment"></a>
## Risk treatment, escalation and acceptance

For each risk owner, create actions with deadlines ahead of proposed 2027-03-15: implement idempotency and recoverability; verify least-privilege access and data-handling restrictions; conduct controlled failure/recovery rehearsal and preserve evidence; assign monitoring to the receiving team.

Decision rule: production promotion is blocked if any severe untreated item persists, if a risk owner is missing, or if required regulatory applicability is unknown. High residual risk requires a recorded L0 authority decision tied to the canonical risk snapshot. Proposed treatments do not themselves constitute acceptance. Reassess after architecture changes, new suppliers or critical incidents.

## Evidence register, assumptions and limitations

- **HFS-FAR-E-MAP — Dependency map:** versioned system and data-flow relationships **Status:** illustrative.
- **HFS-FAR-E-REC — Recovery exercise:** reproducible recovery drill measurements **Status:** not executed.
- **HFS-FAR-E-IAM — Access-control review:** owner-scoped privilege and segregation checks **Status:** not executed.

Illustrative evidence IDs are internal cross-references, **not accessible customer records or claims of completed tests**. Acceptance requires attachment of real, dated evidence by the accountable role. Assumptions remain open until verified.

## Decision and downstream control

This is a proposed, non-authoritative reference. `HFS-FAR-DR-01` must be reviewed by the accountable authority and bound to a hash of the final canonical semantic record; no implied approval arises from the presence of an approval field. The owner must close material evidence gaps before using the document as the basis for deployment or risk acceptance.

**Downstream references:** HFS-FAR-HLD-01, HFS-FAR-TEST-01, HFS-FAR-OPS-01. Revalidate when scope, data classification, controlling evidence or major dependencies change.
