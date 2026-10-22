# Commercial delivery

For the 96-reference library and coherent proposal-package authoring, see
[proposal production](../using/proposal-production.md). Use the
[colleague pilot rubric](../validation/proposal-pilot.md) for independent
practical evaluation; a pilot disposition does not authorize an offer.

The opt-in `commercial-delivery/1` profile extends JAI with the supplier lifecycle: opportunity, proposal, negotiation, delivery, service operation, renewal and exit. It preserves existing technical workflows and canonical identities. It coordinates commercial work; it does not sign contracts or exercise human authority.

**Owner:** JAI maintainers. **Last reviewed:** 16 October 2026. Source implementation is available; live provider qualification remains incomplete. This page combines the commercial operator guide and worked proposal in the [How to use JAI learning path](../examples/how-to-use-JAI/index.md). Read [methodical workflows](../using/methodical-workflows.md) before choosing an engagement method.

Commercial delivery takes the **supplier's** perspective. The enterprise workflow library's [Source to contract to service](../workflow-library/source-to-contract-to-service.md) and [Supplier onboarding to exit](../workflow-library/supplier-onboarding.md) describe the **buyer's** sourcing and supplier-governance responsibilities. They are complementary views of a contractual relationship, not interchangeable proposal workflows.

## Start with the conversation command

Use an installation that includes the commercial extension and start a new provider session after installation. Files in a source branch do not establish that the command or skill is installed in your current session.

| Provider | Conversation input |
| --- | --- |
| Claude Code | `/commercial <scope and source locations>` |
| Codex CLI | `$workflow-commercial <scope and source locations>` |

Identify the human commercial owner, the existing engagement if applicable, input locations and intended internal and client audiences. Explicitly request profile activation. Keep confidential sources in a protected workspace.

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
5. Obtain independent review of exact output versions and prepare client and internal projections.
6. Present unresolved risks and decisions to the human owner. Monitor subsequent delivery and operations against the accepted baseline.

These are orchestration instructions supported by validators, not a guarantee that a command alone executes every step. Request actual engagement, contract, output, review and evidence identifiers. Blocked gates and unknown estimates must remain visible.

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

Request `/fabric-report <decision-engagement-ID>` or `$workflow-fabric-report <decision-engagement-ID>`. Expect actual evidence identifiers and a readiness result that can remain blocked or conditional. Shipped live provider qualification is `not_run`; neither this prompt nor passing unit tests can override that state. Human authorisation and contractual acceptance remain separate from preparation and review.

### 5. Carry the economics into delivery

After actual award and authorised mobilisation, continue against the accepted baseline. Feed completed-stage actuals into remaining-work estimates, update forecasts and trigger review when agreed thresholds are exceeded. Do not rewrite the signed baseline to hide variance. Contract changes, stop-loss and acceptance decisions return to their accountable human owners.

## Apply the SABSA-like method

The commercial domain matrix has six layers—contextual, conceptual, logical, physical, component and operational—and six questions per layer: **what, why, who, when, where and how**. It develops the chain from business need to delivery and operation. Every cell requires an answer or justified non-applicability decision, an owner and a review reference. Structural validation cannot establish business correctness.

This matrix is independent of JAI execution layers L1–L6. The domain matrix organises what must be understood; execution contracts organise specification, production and checking. Maintain the internal chain from source passage and business need through requirements, work packages, effort, capacity, costs, price, baseline, forecast and publications.

Client outputs retain required contractual disclosures. Internal outputs additionally preserve confidential rates, margins, assumptions and rationale unless explicit disclosure policy requires their release. The supported projection surface is a JSON payload. PDF, DOCX, attachments and other export surfaces are rejected by this profile's surface policy.

## Route expertise across domains

`commercial_router.py` selects expertise separately from `model_router.py`, which selects model workloads. A compact root catalog points to 17 integrity-checked domain shards describing the canonical role registry, including five dedicated supplier commercial specialisms. The JSON files are internal, provider-neutral metadata, not native Codex or Claude agent registrations. They identify roles and skill/reference paths; they do not grant tools or dispatch agents.

Exact role names first select their domain. General hierarchical lookup loads at most three candidate shards. The selected operator loads the relevant skill and reference; the router does not read every role reference. `flat` loads all shard metadata as an explicit baseline; `deterministic` uses exact role/deliverable matching. Ambiguity returns `unresolved`; missing, damaged or truncated catalogs produce `discovery_failure`. Shard digests detect catalog/cache mismatch. Metadata segmentation reduces loaded content but is not a filesystem security boundary.

For example, a procurement coordinator may request a firewall implementation estimate. The orchestrator supplies technical constraints, input versions and permitted classifications rather than automatically exposing internal margins. The request carries contract ownership, recipient, deadline, decimal budget and consultation ancestry. The response records assumptions, passages, applicability, estimate state, unit, interval and uncertainty. An independent reviewer checks its exact digest before incorporation.

The runtime rejects identical maker/checker principals, replay, stale reservations and excessive depth or budget. `reserve_consultation` uses episode locking, expected revisions, durable writes and atomic replacement. The host must protect consultation state and authenticated execution records against worker writes. The orchestrator incorporates the result through a new versioned dependency; ownership and technical authority do not transfer.

No independent human-annotated benchmark establishes better routing accuracy or lower total execution cost. The shipped corpus is an author-created smoke corpus. Evaluation reports top-match, recall, metadata size and observed wall time; invocation cost is not applicable because routing makes no LLM call. `top_correct` requires a unique correct winner; `tie_contains_expected` separately records ties containing the expected role.

## Review, approval and provider boundaries

Keep domain validity, evidence verification, independent review, snapshot approval, authority authorisation and contractual acceptance separate. A structurally valid JSON file is neither a verified claim nor an approved proposal. Strict readiness requires exact-snapshot review and platform-authenticated execution identities; declared agent names are insufficient.

The capability registry records seven critical controls separately for Codex and Claude. Shipped live states are `not_run`. Strict dispatch requires current `tested/pass` evidence for the exact provider version, adapter version, model, deployment, product and configuration digest. Missing, invalid, future-dated or expired evidence blocks readiness; the default freshness limit is one day unless deployment policy specifies another limit.

The host must authenticate and protect the registry and evidence. These modules do not independently authenticate registry truth or enforce operating-system mounts. Unit tests and configuration parity do not constitute live isolation tests. Claude `allowed-tools` is preapproval, not an upper permission boundary: actual tools, `disallowedTools`, permissions, mounts and denial of `Agent` must enforce isolation. Codex CLI capabilities cannot be inferred from API tool-search features.

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

Imports require an expected revision and preserve immutable history. Archives contain internal plaintext and require protected storage. Restore verifies model integrity but leaves operational readiness blocked until the host verifies recovery evidence.

`commercial_lifecycle.activate` and `EngagementStore.activate` use a trusted host verifier to authenticate a human scope receipt while preserving canonical objects and memberships. The CLI cannot activate without that verifier. `rollback` retrieves the original using an existing `activation_digest`; it rejects replacement originals and subsequent canonical-content changes. `EngagementStore` and commercial `SnapshotStore` are distinct host-owned stores, not competing semantic masters; host permissions must protect both.

`assess_axes` distinguishes the six acceptance states. `approve_snapshot` verifies an authenticated receipt against the exact manifest, policy and prior review; it does not create a signature. CLI `axes` distinguishes presented receipt IDs from verified IDs and leaves axes unverified without host context. No JSON `authenticated` flag can authorise scope, approval or release.

`commercial_scheduler.schedule` schedules a dependency DAG into calendar buckets, respecting shared pools, skills, regions, client waits, work windows and external reservations. It reports effort, allocations and earliest finish; its greedy algorithm does not prove optimality. `validate_service_roster` checks explicit shifts, active coverage, backup and on-call constraints against sizing inputs. Aggregate roster success does not prove a response-time SLA percentile.

### Granular Fabric binding

The trusted host opens Fabric through its supported API; never edit `.fabric/` directly. `commercial_runtime.append_commercial_binding(fabric, mapping)` accepts `domain_contract_version`, `domain_digest`, `claim_ids`, `claim_digests`, `target_id`, `target_digest`, `layer` and `fragments` containing `id`/`digest` pairs. At L1 the target is the original requirement; lower layers target the adjacent contract. Each fragment must match the exact target and hash.

The API appends an immutable evidence node without exercising authority. Independent review remains necessary. `fabric_binding_resolver(ledger_path)` verifies actual nodes and binding digests for readiness; a report title or assumed file existence cannot substitute for this binding.

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
