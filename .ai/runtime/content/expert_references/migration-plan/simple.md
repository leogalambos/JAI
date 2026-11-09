---
reference_id: example:migration-plan:simple
schema_version: '1.0.0'
document_kind: migration-plan
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/migration-plan
approval_status: not-human-approved
content_revision: 1.0.0
---

# Migration Plan — Harbor Stock Service

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** one service, one team and one bounded change. **Illustrative evaluation population:** 100 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-migration-plan.reference_migration_mapping"></a>
## Migration Mapping

Map customer_key to party_id using lookup map-6, preserve timestamps in UTC and convert amount units only with explicit rules. Duplicate natural keys are quarantined for owner resolution; they are not silently assigned new identities.

**Acceptance question:** Identify source/target inventories, semantic mappings and exceptions.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-migration-plan.reference_migration_reconciliation"></a>
## Migration Reconciliation

For a synthetic 100-row wave, 98 accepted plus two quarantined must reconcile to 100 input rows. Compare amounts in consistent currencies and verify referential integrity to accounts. Equal row counts alone cannot detect swapped customer identities.

**Acceptance question:** Define counts, totals and business-invariant checks per wave.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-migration-plan.reference_migration_acceptance"></a>
## Migration Acceptance

Move one bounded cohort, review reconciliation and downstream reads, then proceed. Record the latest-safe rollback point and owner disposition for every quarantine item. The plan is not evidence that a wave ran or that customers accepted it.

**Acceptance question:** Specify rehearsals, sequencing, recovery and receiving acceptance.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

Source and target each contain 100 rows, so the migration is correct.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Require identity, amount and relationship reconciliation as well as counts. Defer progression when quarantined records or business invariants remain unresolved.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
