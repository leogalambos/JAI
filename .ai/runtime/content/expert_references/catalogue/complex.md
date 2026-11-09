---
reference_id: example:catalogue:complex
schema_version: '1.0.0'
document_kind: catalogue
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/catalogue
approval_status: not-human-approved
content_revision: 1.0.0
---

# Catalogue — Orion Settlement Platform

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** multiple jurisdictions, suppliers and irreversible business effects. **Illustrative evaluation population:** 10000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-catalogue.reference_catalogue_identity"></a>
## Catalogue Identity

The service catalogue uses stable IDs svc-orders and svc-stock. Display name Order API may change without a new service identity. Each record has a service owner, lifecycle state and versioned source; supplier product names are attributes, not primary keys.

**Acceptance question:** Specify entity classes, stable identifiers, ownership and lifecycle.

**Context application:** Partition evidence by jurisdiction, supplier and irreversible boundary. Do not aggregate away a failed cohort; legal applicability and residual risk decisions require their actual competent owners.

<a id="dcs-proposed-catalogue.reference_catalogue_relations"></a>
## Catalogue Relations

svc-orders consumes svc-stock through interface stock-v2. The relation records its source inventory version and owner confirmation status. An unconfirmed dependency is explicitly proposed, so an impact assessment cannot treat it as an observed production fact.

**Acceptance question:** Provide typed dependencies with provenance and receiver use.

**Context application:** Partition evidence by jurisdiction, supplier and irreversible boundary. Do not aggregate away a failed cohort; legal applicability and residual risk decisions require their actual competent owners.

<a id="dcs-proposed-catalogue.reference_catalogue_reconciliation"></a>
## Catalogue Reconciliation

Two rows named Order API with different IDs require reconciliation against the service boundary and owner evidence. Last-seen dates and retirement states prevent a disappeared inventory row from silently deleting a still-used dependency.

**Acceptance question:** Detect duplicate identities, missing owners and stale relationships.

**Context application:** Partition evidence by jurisdiction, supplier and irreversible boundary. Do not aggregate away a failed cohort; legal applicability and residual risk decisions require their actual competent owners.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

Every catalogue row has a name, so the portfolio is complete and every dependency is verified.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Return a bounded coverage statement against the named inventory and date. Resolve ownerless and duplicate records before downstream funding or retirement decisions rely on the catalogue.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
