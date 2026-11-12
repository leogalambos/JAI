---
description: Add supplier-side opportunity, discovery, commercial economics and delivery monitoring to an existing JAI engagement.
---

# Commercial

> **Agents named here** are subagents: `commercial-coordinator` is a read-only routing adviser; the parent orchestrator dispatches it through the active provider's delegation mechanism.

Use the `commercial-delivery` skill and the `commercial-coordinator` agent's procedure. This is an opt-in extension, preserving existing technical `/layered` and `/sabsa` behaviour.

1. Establish the human commercial owner and explicit profile scope change. Reuse canonical identities, source passages and existing engagement memberships. Capture whether the requested outcome is a complete bid, a bounded clarification/calculation or a linked client-draft package. Identify each requested document's readers, decision or execution use, necessary detail and disclosure boundary using the `commercial-delivery` skill's shared work-product contract.
2. Qualify the opportunity; iterate discovery with the six-question domain matrix. Unknown client/expert estimates remain explicit.
3. Assign the dedicated bid/proposal, estimation/cost engineering, pricing/deal finance, supplier deal-management and independent commercial-assurance roles to their respective scopes; never substitute an adjacent role. Route specialist consultation through the orchestrator. Load compact root metadata, selected domain shard, then selected role reference. Do not load the full role catalog into every worker context.
4. Commission the dedicated specialists to produce the actual versioned work products, including the internal calculation models and source files needed for a full bid. Bind them through existing artifact contracts, commercial records and controlled attachments; a document title or typed model record is not the model. Separate baseline, forecast, actual, accrual and cash; retain source quantities, calendars and units and validate service coverage alongside workload. The parent uses the existing discovery, estimation, pricing and capacity facilities for the corresponding phase rather than introducing another calculation or validation mechanism.
5. Have an authorised execute-tier operator run the relevant existing phase checks against the current commercial snapshot, including `options` and `bid-review` as applicable. Retain actual blockers and calculations. Commission independent semantic assurance of the material role work products and obtain Resource Manager capacity and delivery/service-owner feasibility and receiving-obligation dispositions on the same version set. Use the existing internal/client projection paths and disclosure policy; preserve the complete protected internal basis and all required client contractual disclosures. Distinguish phase completeness, governed readiness, professional acceptance and the real human bid/price/contract decision: none substitutes for the others.
6. Monitor stages and operations, learning from actuals. Re-estimation creates a forecast; it does not rewrite a signed baseline.

For a complete bid, the parent collects the actual recipient-ready documents and
reproducible specialist models specified in the shared skill, not merely the
eight linked client-draft components. Confirm that authorised readers can obtain
the required source calculations and that document commitments reconcile with
the phase results and accepted baseline. Unknown, inaccessible or not-yet-
estimable content retains its owner and blocking consequence for the affected
commitment; do not fill it with unsupported prose or mark it accepted from a
successful checker result.

Existing phase-check examples (source checkout; substitute the actual current
snapshot path) are:

```bash
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 gate COMMERCIAL_SNAPSHOT.json --phase options
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 gate COMMERCIAL_SNAPSHOT.json --phase bid-review
```

These commands use existing estimate/price/capacity calculations where the
snapshot supplies their inputs. They do not execute an AI author, establish
complete dossier content, or grant approval. The read-only coordinator advises
the parent; the authorised operator executes commands. A `CONSISTENT_DRAFT`,
`consistency_pass` or readiness `ready` result alone cannot establish a complete
internal bid dossier, reproducible model, financially sound offer or authority
to submit. The linked proposal helper retains `DRAFT_NOT_FOR_SUBMISSION` and
`release_ready: false`; use its existing reference/DCS selection and publication
handoff within that declared scope.

Metadata discovery example (source checkout):

```bash
python3 .ai/runtime/tools/commercial_router.py 'firewall implementation effort' --contract ctr-1 --domain network-and-telecommunications
```

Installed equivalent uses `~/.ai/it-role-house/tools/commercial_router.py`.
Routing does not dispatch or authorize a provider. The consequential branch uses
the canonical `layered-justifiable-delivery` skill and its
`references/domain-handoff.md` native Gen2 contract. The trusted parent supplies
exact scoped product, captured execution and selected-review facts through
`governed_domain.GovernedDomain`; producer names alone establish nothing.
Keep unmeasured physical-control claims explicitly unverified. A specifically
required security policy remains blocking when unmet; missing generic hardening
evidence does not disable ordinary native commercial work. Qualification,
acceptance and release retain their separate existing requirements.


## Compact execution feedback

Present the task result first, then a compact one-row Markdown efficiency table.
Use actual recorded host `efficiency.table` when linked to a native governed run.
Otherwise report measurements unavailable in one row; never invent model time,
rework, findings, acceptance or a governed execution record. Detailed history and
advisory comparisons are available through `/jai-stats` / `$workflow-stats` inside
the conversation. Do not append a long efficiency narrative or switch profiles
without an explicit operator selection.
