# Commercial delivery

For the 135-reference library and coherent proposal-package authoring, see
[proposal production](../using/proposal-production.md). Use the
[review and release readiness](../operations/validation.md) for independent
practical evaluation; a pilot disposition does not authorize an offer.

The opt-in `commercial-delivery/1` profile extends JAI with the supplier lifecycle: opportunity, proposal, negotiation, delivery, service operation, renewal and exit. It preserves existing technical workflows and canonical identities. It coordinates commercial work; it does not sign contracts or exercise human authority.


Commercial delivery takes the **supplier's** perspective. The enterprise workflow library's [Source to contract to service](../workflow-library/source-to-contract-to-service.md) and [Supplier onboarding to exit](../workflow-library/supplier-onboarding.md) describe the **buyer's** sourcing and supplier-governance responsibilities. They are complementary views of a contractual relationship, not interchangeable proposal workflows.

## Start with the conversation command

Use an installation that includes the commercial extension and start a new provider session after installation. Files in a source branch do not establish that the command or skill is installed in your current session.

| Provider | Conversation input |
| --- | --- |
| Claude Code | `/commercial <scope and source locations>` |
| Codex CLI | `$workflow-commercial <scope and source locations>` |

Identify the human commercial owner, the existing engagement if applicable, input locations and intended internal and client audiences. Specify whether you need a complete bid, a bounded clarification/calculation or linked client drafts, and identify the readers and intended use of each document. Explicitly request profile activation. Keep confidential sources in a protected workspace.

For example, choose your provider:

=== "Claude Code"

    ```text
    /commercial Prepare a supplier proposal using ./client-input/. Reuse the existing engagement and establish the commercial owner and authorised profile scope. Maintain separate internal and client outputs. Record unanswered discovery questions before estimating.
    ```

=== "Codex CLI"

    ```text
    $workflow-commercial Prepare a supplier proposal using ./client-input/. Reuse the existing engagement and establish the commercial owner and authorised profile scope. Maintain separate internal and client outputs. Record unanswered discovery questions before estimating.
    ```

The text following the command is a natural-language instruction, not a fixed subcommand grammar. There are no documented conversational `/commercial prepare` or `/commercial approve` subcommands.

The expected sequence is:

1. Establish ownership, authority and profile scope while preserving canonical identities.
2. Qualify the opportunity; expose missing or conflicting information.
3. Develop discovery questions and measurable business outcomes across the domain matrix.
4. Obtain bounded specialist contributions and develop solution options, effort, staffing, cost, price, terms and uncertainty models.
5. Run the applicable existing phase checks; obtain independent commercial review and same-version resource capacity, delivery/service feasibility and receiving-owner dispositions. Prepare client and internal projections.
6. Present unresolved risks and decisions to the human owner. Monitor subsequent delivery and operations against the accepted baseline.

These are orchestration instructions supported by validators, not a guarantee that a command alone executes every step. Request actual engagement, contract, output, review and evidence identifiers. Blocked gates and unknown estimates must remain visible.

## Complete bid documents and readers

Bid / Proposal Manager owns the dossier index, response integration and version
alignment. Specialist authors own their supporting models and evidence. A full
bid contains both a usable client offer and a protected internal basis for
deciding whether, and how, to deliver it.

| Work product | Readers and intended use | Required substance |
| --- | --- | --- |
| Client proposal and contractual scope | Client sponsor, evaluators, procurement, legal and receiving owners evaluating and commissioning the offer | Outcomes, solution and service boundaries, deliverables, acceptance, phases, responsibilities, price/payment terms, assumptions, exclusions and required disclosures. |
| Internal bid dossier and decision view | Delegated bid authority, commercial owner and independent assurance assessing exposure and conditions | An indexed version set, options and rationale, technical baseline, specialist models, uncertainty, departures, review dispositions and actual decision status. A summary links to the detailed basis. |
| Technical baseline and phase/work-package plan | Technical reviewers, project/delivery leads and service owners planning execution | Requirement-to-deliverable and acceptance links, activities and quantities, dependencies, transition/service/exit obligations and phase decision points. |
| Basis of estimate and work/cost breakdown | Technical work owners, estimators, delivery planners and finance reconstructing the estimate | Attributable inputs, methods, units, productivity assumptions, effort ranges, allocation bases and accessible calculation sources. |
| Time-phased resource pyramid and capacity plan | Resource/line managers and delivery/service owners arranging feasible staffing | Skills and seniority by period and work package, sourcing, calendars, onboarding, supervision, shared commitments, headroom and unresolved conflicts. |
| Financial/cash-flow model and recommendation | Pricing/finance specialists, commercial decision owner and independent assurance testing economics | Reproducible cost and sell-rate bases, non-labour/lifecycle costs, reserve treatment, margin versus markup, discounts, price adjustments, payment timing and downside scenarios. |
| Assurance and bid-to-delivery handover | Commissioning authority, responsible authors and receiving delivery/service owners acting on findings and commitments | Exact inspected versions, limitations, required rework, actual capacity/feasibility dispositions, accepted obligations and unresolved conditions. Human approvals remain separate records. |

Every document or controlled view identifies its readers, task, owner,
version/status, access boundary, supporting evidence and next action. Adapt its
structure and detail to those readers. Preserve complete models and contractual
annexes; a short executive view is not a substitute for them. No universal page
limit, phase count or staffing ratio defines adequacy.

### Reconcile estimates, capacity and commitments

Maintain a reconstructable chain from source requirement and evidence through
deliverable/acceptance, phase/work package, activities/quantities, skill/seniority
and effort, calendar capacity and duration, cost, reserve/adjustment, price and
cash terms. Shared costs and teams need explicit allocation bases and reconciled
totals. Effort divided by nominal headcount is not evidence of a feasible
schedule or service coverage.

Count funded project work, including assigned onboarding and supervision, once
in demand. Distinguish other commitments and true unavailability. If using a net
capacity view, remove the same activity from both demand and supply. State
whether rates use paid, available or productive hours and recover support costs
once; do not deduct an activity from capacity while also charging it as full
project demand or recover it again through a loaded rate.

Estimate maturity and commitment status are separate. Distinguish supported
estimates, provisional ranges, discovery-dependent and not-yet-estimable work
from proposed and actually authorised price/date commitments. A discovery or
pilot phase defines the observation, acceptance, owner and criterion for
recalculating the next phase. Unknown later work must not acquire unsupported
precision merely to fill an offer.

Use existing `options` and `bid-review` checks on the current snapshot through
an authorised execute-tier operator. They calculate from supplied inputs and
report blockers; they do not establish completeness or the truth of assumptions.
Independent commercial assurance challenges the exact models and obligations.
Resource Manager confirms period-specific capacity, while delivery and relevant
service owners assess feasibility and accept their receiving obligations on the
same version set. These dispositions do not authorise submission or contracts.
Material scope, staffing, schedule, rate or term changes reopen the affected
models, acceptances, review and human decisions; unchanged evidence is reused.

The [eight-component proposal helper](../using/proposal-production.md) produces
linked client drafts, not this entire internal dossier. `CONSISTENT_DRAFT`,
`consistency_pass` or governed readiness `ready` alone cannot establish complete
models, financial truth or submission authority. Preserve the full protected
internal basis and all required client disclosures, including open-book detail
when policy or contract requires it. Internal/client projections are controlled
views of the same baseline, not a reason to conceal a material limitation.

## Choose the assurance scope

[Methodical workflows](../using/methodical-workflows.md) explains three modes: direct domain work, layered creation from the start, and a new layered decision using existing domain outputs.

For direct domain work, continue in the existing conversation:

```text
In the current commercial engagement, incorporate the client's answers from ./client-input/answers.md. Preserve unknown estimates, version the affected assumptions and arrange independent review of the revised outputs.
```

For layered creation from the start, use Claude `/layered` or Codex `$workflow-layered`:

=== "Claude Code"

    ```text
    /layered Prepare the supplier proposal using commercial-delivery/1. Establish adjacent execution contracts from intent through evidence, use commercial specialists, and return unsupported work for bounded rework before escalating unresolved conflicts.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the supplier proposal using commercial-delivery/1. Establish adjacent execution contracts from intent through evidence, use commercial specialists, and return unsupported work for bounded rework before escalating unresolved conflicts.
    ```

For a subsequent bid decision, start a new decision scope:

=== "Claude Code"

    ```text
    /layered Decide whether the reviewed proposal is ready for submission. Use its exact snapshot and supporting evidence; assess unresolved estimates, margin exposure, staffing commitments and contractual risks. Present authority decisions to the commercial owner.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Decide whether the reviewed proposal is ready for submission. Use its exact snapshot and supporting evidence; assess unresolved estimates, margin exposure, staffing commitments and contractual risks. Present authority decisions to the commercial owner.
    ```

The last example does not retrospectively establish that creation followed layered contracts. Direct `/commercial` does not automatically start a complete six-layer execution chain. Conversely, `/layered` needs the commercial methodology and specialists; it cannot replace their domain knowledge.

After award, continue the profile for mobilisation, stage forecasts, actuals, service monitoring and exit planning. Re-estimation changes the forecast, not a signed baseline. Stop-loss, risk acceptance and contractual changes remain human authority acts.

## Worked proposal: from discovery to bid decision

Consider a fictional enterprise requesting a managed integration service. It supplies desired outcomes but declines to disclose precise ticket volumes. The supplier's engineers can offer only a broad transition estimate. The task is to prepare a reviewable proposal while keeping that uncertainty visible.

**Chosen arrangement:** direct commercial preparation followed by a new layered bid-issue decision. Commercial authors and independent reviewers already apply domain controls during preparation. The later `/layered` scope evaluates whether the exact proposal is fit to issue; it does not recreate a six-layer history for its preparation. This exercise is an instructional sequence, not an executed bid or permission to submit one.

### Alternative: govern creation from the start

If policy requires justification of the creation process, start here **instead of** the direct preparation prompt below:

=== "Claude Code"

    ```text
    /layered Prepare the managed integration service proposal using
    commercial-delivery/1 and ./client-input/. Establish adjacent contracts,
    independent production and review, and the full source-to-effort-to-price
    chain. Preserve unknowns, separate client/internal views and stop before
    binding commitments or proposal issue.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the managed integration service proposal using
    commercial-delivery/1 and ./client-input/. Establish adjacent contracts,
    independent production and review, and the full source-to-effort-to-price
    chain. Preserve unknowns, separate client/internal views and stop before
    binding commitments or proposal issue.
    ```

The following stages then become checkpoints inside that engagement, rather than separate domain runs. Required provider controls still need actual qualification evidence.

### 1. Qualify the opportunity and organise discovery

=== "Claude Code"

    ```text
    /commercial Qualify the managed integration service opportunity from
    ./client-input/. Reuse the existing engagement where present. Identify
    the commercial owner, profile scope, measurable outcomes, unanswered
    discovery questions and bid/no-bid considerations. Keep client and internal
    information separate and do not assume missing service volumes.
    ```

=== "Codex CLI"

    ```text
    $workflow-commercial Qualify the managed integration service opportunity
    from ./client-input/. Reuse the existing engagement where present.
    Identify the commercial owner, profile scope, measurable outcomes,
    unanswered discovery questions and bid/no-bid considerations. Keep client
    and internal information separate and do not assume missing service volumes.
    ```

**Expected output:** an engagement identifier, source/claim register, initial matrix, opportunity assessment and questions linked to the assumptions they resolve. **Checkpoint:** refusal to disclose volume is recorded as unavailable input, not a numerical answer. Establish which qualified host controls are available before strict dispatch.

### 2. Develop options, estimates and a delivery pyramid

Continue in the same provider conversation after supplying actual answers:

```text
Continue engagement <ID>. Incorporate the discovery answers from <source>.
Compare a paid discovery stage followed by a repriced rollout with a bounded
initial service commitment. Obtain specialist transition and operations
estimates; retain provenance, applicability, units, intervals and unknowns.
Build phase-specific work packages, staffing and capacity assumptions, and
arrange independent review of the exact versions.
```

**Expected output:** reviewed solution options, work packages, a resource pyramid, estimate states and risk treatments. Public benchmarks remain attributable estimates. Effort is distinct from elapsed time, and service coverage is distinct from ticket-handling workload. **Checkpoint:** staging can improve later estimates; a contractual cap limits exposure without necessarily reducing technical uncertainty.

### 3. Calculate economics and prepare both views

```text
Continue engagement <ID>. Calculate costs, proposed price, margin, reserves
and cash-flow exposure for the reviewed options. Show the assumptions,
sensitivity to volume and staffing, and dependencies on contractual terms.
Prepare internal and client proposal projections with required disclosures.
Have an independent checker verify calculations and the exact output snapshot.
Stop before proposal issue or binding commitment.
```

**Expected output:** internal reasoning and economics, client-facing contractual scope, calculation evidence, review records and unresolved decisions. **Checkpoint:** missing estimates remain explicit; reserves and overhead are counted once; confidential rates and margins are withheld according to the disclosure policy. The supported profile projection is a JSON payload, not an automatically approved PDF or Word export.

### 4. Ask the new bid-issue question

=== "Claude Code"

    ```text
    /layered Assess whether proposal snapshot <reference and digest> is ready
    to issue, using commercial-delivery/1. Independently assess the source and
    calculation evidence, staffing commitments, disclosures, uncertainty and
    contractual exposure. Identify unresolved conditions and reserve bid issue,
    risk acceptance and binding commitments for the human commercial owner.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Assess whether proposal snapshot <reference and digest>
    is ready to issue, using commercial-delivery/1. Independently assess the
    source and calculation evidence, staffing commitments, disclosures,
    uncertainty and contractual exposure. Identify unresolved conditions and
    reserve bid issue, risk acceptance and binding commitments for the human
    commercial owner.
    ```

Request `/fabric-report <decision-engagement-ID>` or `$workflow-fabric-report <decision-engagement-ID>`. Expect exact governing versions, actual evidence and readiness that can remain blocked or conditional. Native execution evidence and any physical-control qualification are distinct claims; neither a prompt nor passing unit tests proves unobserved deployment controls. Human authorisation and contractual acceptance remain separate from preparation and review.

### 5. Carry the economics into delivery

After actual award and authorised mobilisation, continue against the accepted baseline. Feed completed-stage actuals into remaining-work estimates, update forecasts and trigger review when agreed thresholds are exceeded. Do not rewrite the signed baseline to hide variance. Contract changes, stop-loss and acceptance decisions return to their accountable human owners.

## Apply the SABSA-like method

The commercial domain matrix has six perspectives—Contextual, Conceptual, Logical, Physical, Component and Management—and six questions per layer: **what, why, who, when, where and how**. It develops the chain from business need to delivery and operation. Every cell requires an answer or justified non-applicability decision, an owner and a review reference. Structural validation cannot establish business correctness.

The matrix organises commercial content across SABSA views. Gen2 uses these canonical six SABSA perspectives with local setter, author and independent reviewer responsibilities; execution contracts do not restore a fixed production layer followed by a separate global review layer. Professional roles are chosen locally. Maintain the internal chain from source passage and business need through requirements, work packages, effort, capacity, costs, price, baseline, forecast and publications.

Client outputs retain required contractual disclosures. Internal outputs additionally preserve confidential rates, margins, assumptions and rationale unless explicit disclosure policy requires their release. The supported projection surface is a JSON payload. PDF, DOCX, attachments and other export surfaces are rejected by this profile's surface policy.

## Route expertise across domains

`commercial_router.py` selects expertise separately from `model_router.py`, which selects model workloads. A compact root catalog points to 17 integrity-checked domain shards describing the canonical role registry, including five dedicated supplier commercial specialisms. The JSON files are internal, provider-neutral metadata, not native Codex or Claude agent registrations. They identify roles and skill/reference paths; they do not grant tools or dispatch agents.

Exact role names first select their domain. General hierarchical lookup loads at most three candidate shards. The selected operator loads the relevant skill and reference; the router does not read every role reference. `flat` loads all shard metadata as an explicit baseline; `deterministic` uses exact role/deliverable matching. Ambiguity returns `unresolved`; missing, damaged or truncated catalogs produce `discovery_failure`. Shard digests detect catalog/cache mismatch. Metadata segmentation reduces loaded content but is not a filesystem security boundary.

For example, a procurement coordinator may request a firewall implementation estimate. The orchestrator supplies technical constraints, input versions and permitted classifications rather than automatically exposing internal margins. The request carries contract ownership, recipient, deadline, decimal budget and consultation ancestry. The response records assumptions, passages, applicability, estimate state, unit, interval and uncertainty. An independent reviewer checks its exact digest before incorporation.

The runtime rejects identical maker/checker principals, replay, stale reservations and excessive depth or budget. `reserve_consultation` uses episode locking, expected revisions, durable writes and atomic replacement. The host must protect consultation state and authenticated execution records against worker writes. The orchestrator incorporates the result through a new versioned dependency; ownership and technical authority do not transfer.

No independent human-annotated benchmark establishes better routing accuracy or lower total execution cost. The shipped corpus is an author-created smoke corpus. Evaluation reports top-match, recall, metadata size and observed wall time; invocation cost is not applicable because routing makes no LLM call. `top_correct` requires a unique correct winner; `tie_contains_expected` separately records ties containing the expected role.

## Review, approval and provider boundaries

Keep domain validity, evidence verification, independent review, snapshot approval, authority authorisation and contractual acceptance separate. A structurally valid JSON file is neither a verified claim nor an approved proposal. Governed readiness uses exact native execution provenance, immutable material, scoped independent review and current Gen2 justification; declared agent names or echoed context tokens are insufficient.

The shared domain integration supplies these facts from the existing Store. Only L0 signs reserved decisions; ordinary producer/checker records require no internal signing keys or HMAC service. Calculation, disclosure and consultation requirements retain their business meaning. Actual acceptance and release remain separate runtime decisions rather than domain booleans manufactured by a callback.

Provider-control registries describe particular assurance claims. Unmeasured controls remain unverified, and a policy or contract that specifically requires such a control remains blocked without its evidence. An old blanket `not_run` label must not prevent all ordinary native work or be converted into a false isolation PASS. Unit tests and configuration parity do not constitute live deployment tests. Actual tool and filesystem restrictions remain the L0-owned provider sandbox's responsibility; prompt tool declarations alone do not prove physical isolation.

## Maintainer interfaces

These are optional source-checkout diagnostics, not additional operator steps after a conversation command. Installed equivalents use `~/.ai/it-role-house/tools/` and `~/.ai/it-role-house/commercial/`.

```bash
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 validate .ai/runtime/commercial/examples/snapshot.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 gate .ai/runtime/commercial/examples/snapshot.json --phase qualification
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 plan .ai/runtime/commercial/implementation-plan.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 evaluate .ai/runtime/commercial/routing-corpus.json
python3 .ai/runtime/tools/commercial_router.py 'firewall effort' --contract ctr-1 --domain network-and-telecommunications
```

The CLI rejects an omitted profile. The synthetic snapshot passes structural validation but fails qualification because required commercial inputs are missing. `readiness` remains blocked without trusted host callbacks. The CLI exposes `validate`, `import`, `discover`, `readiness`, `trace`, `project`, `calc`, `route`, `evaluate`, `plan`, `gate`, `archive`, `restore` and lifecycle/scheduling interfaces. The plan checker verifies structure and acyclicity, not task completion.

```bash
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 import .ai/runtime/commercial/examples/snapshot.json --store ./commercial-store --expected-revision 0
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 archive ./commercial-archive.json --store ./commercial-store
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 restore ./commercial-archive.json --store ./commercial-restored
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 schedule ./schedule-input.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 roster ./roster-input.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 axes ./presented-receipts.json
python3 .ai/runtime/tools/commercial.py --profile commercial-delivery/1 rollback ./activation-reference.json --store ./engagement-store --expected-revision 2
```

Imports require an expected revision and preserve immutable history. Archives contain internal plaintext and require protected storage. Restore verifies model integrity but establishes no operational permission or current Gen2 justification by itself; governed use still requires its actual current basis and any specifically required recovery evidence.

`commercial_lifecycle.activate` and `EngagementStore.activate` use a trusted host verifier to authenticate a human scope receipt while preserving canonical objects and memberships. The CLI cannot activate without that verifier. `rollback` retrieves the original using an existing `activation_digest`; it rejects replacement originals and subsequent canonical-content changes. `EngagementStore` and commercial `SnapshotStore` are distinct host-owned stores, not competing semantic masters; host permissions must protect both.

`assess_axes` distinguishes the six acceptance states. `approve_snapshot` verifies an authenticated receipt against the exact manifest, policy and prior review; it does not create a signature. CLI `axes` distinguishes presented receipt IDs from verified IDs and leaves axes unverified without host context. No JSON `authenticated` flag can authorise scope, approval or release.

`commercial_scheduler.schedule` schedules a dependency DAG into calendar buckets, respecting shared pools, skills, regions, client waits, work windows and external reservations. It reports effort, allocations and earliest finish; its greedy algorithm does not prove optimality. `validate_service_roster` checks explicit shifts, active coverage, backup and on-call constraints against sizing inputs. Aggregate roster success does not prove a response-time SLA percentile.

### Exact governed output binding

The trusted parent uses the current `lifecycle.Store` and pins exact product
UsePoints through `governed_domain.GovernedDomain`; never edit `.fabric/` directly.
The host mapping is outside the immutable domain material. Producer/reviewer
tokens identify pre-issued contexts and stable logical records, not their own
future product hashes. Actual captured return membership, exact material and
current scoped independent review establish the callback facts.

`commercial_mapping` constructs the domain contract and claim digests, exact
producing assignment and layer, and scoped output uses. The actual producer
records these bytes through the existing governed return/admission path. It is
not a second journal append API and requires no routine dispatch signature.

`GovernedDomain.commercial_callbacks()` supplies the retained identity and
binding callback interfaces from current Gen2 facts. The resolver checks exact
domain/claim hashes, assignment/output references, immutable mapping bytes and
current qualification. Revoked or insufficient justification fails readiness
even when a historical mapping remains intact. An echoed context token or a
domain `authenticated` flag supplies no authority. Qualification, independent
acceptance, contractual approval and release remain separate decisions.

The native command handles these internal references and callbacks. Users supply
the actual task and source material through prompts rather than writing workers
or bootstrap JSON. See the [review and release readiness](../operations/validation.md)
for source wiring and verification limits; installed activation is separate.

The [implementation matrix](commercial-delivery-implementation.md)
records coverage and remaining deployment acceptance.


## Specialist competence and accountability

Commercial work requires dedicated roles rather than a nearby generalist:

| Scope | Specialist |
| --- | --- |
| Capture, bid planning, response compliance and proposal integration | Bid / Proposal Manager |
| Estimation methods, basis of estimate, uncertainty and actuals calibration | Estimation / Cost Engineering Specialist |
| Selling price, margin, cash flow, payment and finance scenarios | Commercial Pricing / Deal Finance Specialist |
| Supplier negotiation, contractual economics, change and exit | Supplier Commercial / Deal Manager |
| Independent challenge of bids, estimates, price and commercial risk | Independent Commercial Assurance Reviewer |

Select these roles through `/commercial` or `$workflow-commercial`; the shared
role references apply to Claude and Codex. Pre-sales contributes solution
feasibility, technical specialists contribute domain evidence, resource management
contributes staffing constraints, and TBM/FinOps contribute technology cost inputs.
None replaces supplier pricing, bid management or estimate engineering.

The reviewer works in the advise tier with an independent execution identity,
returns findings and rework criteria, and never edits or approves the assessed
bid. Contract, finance, legal and human commercial authorities retain their own
approval responsibilities. Mixed requests are decomposed into role contracts;
unavailable specialist metadata is escalated as a capability gap.

Compact discovery projections are rebuilt from canonical `roles.json` with
`.ai/runtime/tools/generate_commercial_catalog.py`; `--check` detects drift.
The bounded phrase rules in `commercial/specialist-routing.json` are discovery
hints, not an exhaustive language classifier or a replacement for scope review.
The coordinator must confirm specialist fit even when a phrase is not recognised.
