---
reference_id: example:managed-security-services-proposal:simple
schema_version: '1.0.0'
content_revision: 2.1.0
document_kind: managed-security-services-proposal
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/managed-security-services-proposal
dcs_status: proposed-not-mapped
approval_status: not-human-approved
proposal_pack_id: HFS-FAR-PROPOSAL-EXAMPLE
---

> **SYNTHETIC, NON-BINDING PROFESSIONAL REFERENCE — NOT AN OFFER OR APPROVED CUSTOMER RECORD.** All named organisations, assumptions, workloads, fees, evidence identifiers, service levels and commercial terms are invented for educational purposes. No work, tests, negotiations, contractual signing or statutory assessments have occurred. Reuse document structure and reasoning only, never the synthetic facts or commitments.

# Managed security services proposal — Field Appointment Reliability

**Client:** Harborline Field Services · **Reference:** `HFS-FAR-MANAGED_SECURITY_SERVICES_PROPOSAL-01` · **Complexity:** simple · **Status:** non-binding illustration · **Basis:** unverified synthetic scenario · **Decision forum:** Operations Director and Procurement Lead.

<a id="dcs-proposed-managed-security-services-proposal.service_boundary"></a>

## Managed security service definition and entitlement

Proposed optional service for Harborline Field Services: **Business-hours monitoring with optional out-of-hours incident escalation for booking, dispatch and SaaS audit alerts; not an unconditional 24×7 SOC service.**. This is a managed detection/triage and escalation service; it does not transfer financial, legal or regulatory decision rights from the client. It does not automatically provide forensic retainer, platform licensing, full remediation or out-of-scope workload onboarding.

Protected estate: Booking SaaS, corporate SSO, dispatch connector, durable notification queue, daily reconciliation dashboard. Monitored data may include technician name, appointment address, job reference and visit window; access, lawful processing, retention and data location require joint DPA and customer policy review. Service launch is conditional on a signed asset boundary and working telemetry permissions.

<a id="dcs-proposed-managed-security-services-proposal.service_catalogue"></a>

## Services, event handling, exclusions and outputs

| Service | Supplier action | Excluded / requires client approval | Evidence |
| --- | --- | --- | --- |
| Log and alert onboarding | Connect allowlisted sources; verify ingestion health | Undocumented customer systems and unrestricted log copying | Source inventory and ingestion checkpoint |
| Detection engineering | Tune security and integrity use cases | Guarantee of finding every attack or fraud event | Rule tests and tuning record |
| Triage and qualification | Correlate events, categorize severity and notify owner | Final criminal/fraud finding or irreversible blocking decisions | Case timeline with analyst decisions |
| Incident advisory | Recommend containment; support authorized incident bridge | Self-directed production shutdown or legal notification | Escalation ticket and authority reference |
| Reporting and improvement | Monthly coverage, trends, false positives, gaps | Unproven claims of 100% visibility or certification | Service report and improvement backlog |


**Out of scope by default:** vulnerability remediation, forensic acquisition beyond contracted tooling, 24×7 staffed response where not explicitly specified, customer data transformation, SOC platform purchase and contractual third-party commitments.

<a id="dcs-proposed-managed-security-services-proposal.slo_escalation"></a>

## Service hours, measurable SLO, priority and escalation

**Illustrative service level:** High-priority alerts triaged within 60 minutes during 08:00–18:00 UK business days, excluding agreed holidays; emergency response outside these hours requires a separately purchased rota. Measurement starts when a complete, in-scope event is received by the supplier's functioning monitoring platform, not when an external event occurred undetected.

Severity P1: credible active compromise, consequential financial/data-integrity anomaly or critical service control loss; immediate escalation to the authorized customer incident commander. P2: material but contained issue; owner notified within the agreed coverage window. P3: nonurgent finding tracked in monthly improvement.

SLO exclusion candidates require contract approval (unavailable customer source telemetry, planned maintenance, client network blackout); an exclusion cannot hide provider-owned missed alerts. No MTTR or absolute containment guarantee is offered because corrective actions remain customer-authorized.

<a id="dcs-proposed-managed-security-services-proposal.client_supplier_raci"></a>

## RACI, authorization, privacy and incident authority

| Activity | Supplier | Client authority | Operating rule |
| --- | --- | --- | --- |
| Detection content | R | A: Security owner | Client validates prioritized risk scenarios |
| Case triage | R | A: Incident Commander | Escalate according to agreed severity |
| Privilege and log access | C | A/R: IAM and privacy | Time-bounded least privilege |
| Blocking production actions | Recommend | A/R: Operations/Risk | No unsupervised financial or data-state change |
| Regulatory/customer notification | Provide facts | A/R: Legal and DPO | Client retains statutory decision |
| Service acceptance | C | A/R: Service Owner | Signed source coverage and drill |


The client supplies data-classification decisions, lawful access, alert recipient rota, business risk owner and remediation executor. The supplier preserves observable triage actions and evidence while avoiding raw secrets or personal data in public reports.

<a id="dcs-proposed-managed-security-services-proposal.commercial_service_model"></a>

## Recurring fee, onboarding and commercial conditions

**Illustrative optional service pricing:** Optional monitoring £2,400 per month plus £4,500 onboarding; initial 12-month service estimate £33,300, excluded from the base programme investment. It is fully separate from £84,000 base supplier delivery and £140,000 programme envelope. Taxes, third-party ingestion/retention charges, data-transfer costs and specialist incident assistance are excluded until priced.

Before signing: define monitored asset count, event volume and retention window; onboarding completion; coverage hours and holidays; triage clock definition; severity disagreement procedure; service credit caps (if any); access rights and exit/export format. A service-level target must have measurable denominator, clock start and operational evidence.

A price statement in this synthetic reference is **neither an authorized supplier quotation nor a customer commitment**.

<a id="dcs-proposed-managed-security-services-proposal.transition_acceptance"></a>

## Onboarding, evidence gates and controlled exit

Illustrative onboarding sequence: (1) confirm scope and legal data flows; (2) integrate sampled security and integrity logs; (3) verify detection test cases without live customer disruption; (4) rehearse P1 escalation with named client responders; (5) run an agreed stabilization window; (6) sign receiving acceptance.

| Acceptance check | Evidence | Block condition |
| --- | --- | --- |
| Source coverage | Signed source inventory, telemetry gap map | Critical source absent |
| Detection quality | Observed positive/negative test outcomes | Unreviewed critical rule failure |
| Escalation | Timed P1 drill, contact acknowledgement | No functioning customer responder |
| Data protection | Confirmed lawful processing, access and retention | Undefined legal role or location |
| Exit readiness | Exportable cases, configurations and customer-held keys | Provider lock-in without agreed retrieval |


Supplier exit requires return/secure disposal of data under agreed retention and verified revocation of access, not only cancellation of invoice. Open incidents and evidence preservation must be transferred to named customer authority.

## Evidence register, reservations and governance

The proposal is based on a **fictional, unconfirmed scenario**. Open evidence obligations are `HFS-FAR-E-SCOPE` (signed requirements), `HFS-FAR-E-COST` (validated rate-card and cost owner), `HFS-FAR-E-SEC` (risk/legal applicability), and `HFS-FAR-E-TEST` (observed qualification and acceptance results). All remain **NOT PROVIDED / NOT EXECUTED**. A future contract must replace them with authorized evidence, source revisions and dates.

**Authority boundaries:** A commercial specialist may recommend scope and estimate but may not sign for the client, bind the supplier, make unverified assurance claims, accept residual business risk or bypass procurement/Legal/JAI L0 approval. A technically complete narrative is not contractual acceptance. Required independent reviewers: domain architect, security/risk, delivery authority, finance and client procurement as appropriate.

**Synthetic-fact containment:** Do not copy the organisation name, budget, performance numbers, vendor assertions, customer reference, regulatory conclusions or illustrative pass/fail statements into a live proposal. For a real opportunity, retrieve confirmed customer facts from authorized inputs, record uncertainty and rerun pricing and approval validations.

**Status:** `ai-authored-proposed`, `not-human-approved`; professional peer review and all customer approvals remain pending. **Applicable JAI context:** `HFS-FAR`; **document kind:** `managed-security-services-proposal`; **scenario:** `simple`.
