# Operate a layer-local workflow


For ordinary operator use, request `/layered <intent>` in Claude or
`$workflow-layered <intent>` in Codex. The native parent handles bootstrap,
selection, fresh professional contexts and continuation through the existing
Gen2 bridge. See the [layered delivery](../using/layered-engagement.md)
and [installed command guide](../reference/installed-cli-guide.md#layered).
Users do not prepare JSON packets or write workers for that route.

The explicit commands below remain the maintainer reference for the configured
local-process transport and shared structural workflow operations. A process
worker configuration is required for that transport; it is not a prerequisite
for native Claude/Codex delegation. Both routes use the same ownership,
applicability, budget and decision rules.

The host provides explicit operations and a bounded driver around the existing
Store and dispatcher. It does not invent a solving strategy or retry indefinitely. The
[layer model](../architecture/sabsa-layer-model.md) defines the six content
layers. Incoming work addresses a layer as a whole: outcomes, requirements and
interfaces enter the layer, which formulates its own questions and hires its own
professional specialties. A neighbor cannot choose its internal author,
reviewer, model or method.

## Prerequisites

Use a bootstrapped journal-format-9 engagement in the controlled workspace.
Its current L0 sources include the explicit input/criterion manifest and global
capability policy; its profile declares the relevant ownership and obligations.
The policy captures the complete common role catalogue and instruction bytes,
explicit model availability, functional chooser and finite global capabilities.
The [startup and recovery boundary](lifecycle-recovery.md) explains the host-adapter
prerequisite. Ordinary recording and queries do not require a key or proof.
Only an explicit reserved L0 decision uses its known public key and external
human signature, as defined by [runtime recording](../architecture/governed-runtime-recording.md).

The host configuration contains `workers`, destinations, tools and byte bounds
as described in [process dispatch](governed-dispatch.md). It enrolls both the
functional chooser and the available work executables. Actual argv and asset
identities must match the captured policy/choice. No internal dispatch private key
exists. L0's private key is used only by the external human signing companion.

The following source-checkout commands use illustrative operator-owned paths.
Replace them with actual files. This example deliberately supplies an optional
overall stop. Set `JAI_DEADLINE_MS` to that explicitly approved absolute
UTC-millisecond deadline; `limits.json` contains finite limits such as
`[{"metric":"elapsed_ms","unit":"ms","ceiling":60000}]` within the existing
aggregate allowance. Ordinary layered entry may instead omit the overall stop
and use local iteration windows. Do not enlarge limits merely to make a failed
result pass.

## Create the L1 gateway

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  entry --scope default --work-item service-controls \
  --limits /operator/limits.json --deadline-ms "$JAI_DEADLINE_MS"
```

This derives the structural L1 coordinating setter from the current attributable
L0 manifest. It does not author domain questions, criteria or answers. Save the
returned `assignment` VersionRef as `entry-ref.json`. The Store rejects arbitrary
L2–L6 roots or a reissued cancelled generation with no entitled restoration.

## Execute the entity's choice, then its work

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  preview /operator/entry-ref.json

python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  run /operator/entry-ref.json --phase selection
```

The actual functional chooser reads its mandate and intrinsic common catalogue.
Its captured return has no records and one `select_execution` decision for its
own assignment. It chooses specialties, provider, workload and an available exact
model. This phase cannot create a domain result, materialize, measure, accept or
release anything. Save the intrinsic decision VersionRef returned in
`completion.receipt.created_versions` as `choice-ref.json`; do not manufacture a
choice from chat or a proposed JSON result.

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  run /operator/entry-ref.json --phase work --selection /operator/choice-ref.json
```

Work uses a fresh context for the same assignment and functional actor. Its exact
unrevoked professional plan remains reusable while the assignment is unchanged;
each invocation grant is single-use. Both phases share the local iteration
window and any explicitly configured cumulative cap. A terminal physical run is never
reopened; a completed or cancelled logical task needs an entitled new mandate.
An executing setter may return sequential typed local assignments/decisions
before its permitted terminal intent; each is checked in order and the whole
return is rejected atomically if any part is invalid.

Every entity can read `/catalogue/catalogue.json` and all
`/catalogue/instructions/<slug>.md` without a neighbor request. Selected prompt
instructions reduce context size; they are not a catalogue access restriction.
Task inputs and another entity's private work are still governed separately.

## Local quality and the next layer

The local coordinating setter delegates its questions. Each question has a
setter, author and independent same-layer reviewer. The setter selects exact
reviews and bases through its own captured decisions; the host does not turn an
actor's PASS statement into acceptance. A complete-layer bundle requires the
six current selected answers and independent integration review. The integration
reviewer differs from the bundle producer and every answer producer. A profile
that declares only transport obligations cannot claim complete-layer work.

After an actual offered handoff exists, save its exact UsePoint as
`handoff-use.json`, for example `{"ref": {"…": "exact VersionRef"},
"use_scope": "default"}`. The illustrative ellipsis is not executable data.

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  local-entry /operator/handoff-use.json --phase receiver
```

The host derives a local receiving gateway from that exact adjacent interface,
L0 obligations and global capabilities. The upstream layer supplies no staffing
fields or local tool template. Execute the receiver's selection/work phases as
above. After its actual receiving assessment is accepted and selected in the
required proof slot, save that assessment VersionRef as `acceptance-ref.json`:

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  local-entry /operator/handoff-use.json --phase setter \
  --acceptance /operator/acceptance-ref.json
```

The receiving layer's coordinating entity now chooses its own professionals and
formulates its local work. A receiving assessment is separate from professional
review, human result acceptance and permission to release.

## Inspect the result and handle unsuccessful work

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  status /operator/output-use.json
```

`output-use.json` contains an exact output UsePoint. Status reports current
justification and `complete_layer`; it performs no acceptance or publication.
The same owner/profile/criteria and governing input generation retain the
reviewer instance across revisions. Slot aliases or repeated references cannot
reset that generation. Replacing a reviewer requires a traceable entitled owner
decision preserving the prior findings.

Fresh contexts deliver bounded facts: exact review closure, published owned child
outcomes, current slot references and explicitly historical revision feedback.
An invalid current slot keeps its raw selected reference for compare-and-swap;
it is not displayed as an empty slot or replaced by an older PASS. These facts
do not create new governing inputs or change the actual author's result.

Return missing information or a changed requirement through the typed owner
route. Existing rework/reformulation limits still apply. The bounded coordination
operations below handle existing assignments; substantive content generation is
the assigned entities' work. Native Codex/Claude execution and external retrieval are
unsupported by this process adapter; that technical limit is not a policy
forbidding common public knowledge. Acceptance, release permission and actual
publication remain separate gates.

## Bounded coordination and escalation

Use the same controlled-workspace Store and host configuration as above.
These Bash examples name actual operator-owned input files, with illustrative
paths to replace before running:

```sh
JAI_WORKFLOW=(python3 .ai/runtime/tools/governed_workflow.py
  --store /operator/engagement.jsonl --engagement engagement-id
  --config /operator/host-config.json)

"${JAI_WORKFLOW[@]}" ready --scope default
"${JAI_WORKFLOW[@]}" step --scope default
"${JAI_WORKFLOW[@]}" drive --scope default --max-steps 4
"${JAI_WORKFLOW[@]}" attempt-status /operator/attempt-ref.json
```

`ready` reports eligible phases and wait reasons. `step` executes one eligible
phase; `drive` executes at most its declared phase count and stops on waiting,
blocked work or actual resource exhaustion. Finishing a bounded driver call is
not itself proof that the whole attempt exhausted its resources. An open setter
waits for relevant new facts; its own audits and unrelated journal changes do not
cause repeated execution. Facts arriving after the run's delivered basis remain
eligible for its next step.

An explicit escalation immediately pauses the affected layer and dependent work,
including future productive admission. Collection does not delay that pause.
Packages preserve individual conflicts and original provenance. Later findings
produce immutable revisions; owner responses cover the exact revision/conflicts.
An intermediate layer may relay a request but cannot change the actual owner's
requirement.

```sh
"${JAI_WORKFLOW[@]}" handling-entry /operator/episode-ref.json --task collect
```

The same command supports `relay`, `resolve` and `reconcile`, optionally naming
the entitled layer with `--layer`. The runtime derives the narrow control mandate;
this is not a way to mark arbitrary productive work exempt from pause. Execute its
returned assignment through the ordinary selection/work phases. Historical
conflict material is labeled separately from current justification, so an owner's
input change does not disable the work needed to reconcile its consequences.

## Explicit speculative permission and reconciliation

Without an actual grant, productive work stays paused. Speculation requires one
externally signed L0 `delivery-change` decision naming the episode, existing
assignments, exact governing inputs, finite shared limits and expiry. The native
adapter meters `elapsed_ms`; token or currency ceilings are not supported meters.
The grant does not approve a result, choose local staff or authorize release.

```sh
"${JAI_WORKFLOW[@]}" prepare-decision /operator/speculate-payload.json \
  --scope default > /operator/prepared.json
```

The closed payload follows the maintained [protocol](../reference/governed-delivery-protocol.md).
Preparation returns `message`, `intent`, `parameters`, `purpose` and `target`.
Save the exact message and intent separately. Create the existing operator request
with `operator_actions.request`, using the intent file as its source and the
returned purpose, target and parameters unchanged. Request creation grants nothing.
Only the operator signs it outside the agent sandbox, supplying the actual
private key to the existing companion:

```sh
python3 .ai/runtime/tools/operator_actions.py sign /operator/request.json \
  --workspace /operator --key /outside-agent/keys/operator-private.pem
```

The signing key must be outside the agent workspace and mounts. Combine the
unchanged request and actual returned receipt as `{"request": ..., "receipt": ...}`
in the proof file. The host then ingests that proof:

```sh
"${JAI_WORKFLOW[@]}" submit-decision /operator/message.json \
  --authority-proof /operator/proof.json
```

The host fills only the proof binding; it does not sign human consent or rewrite
the approved meaning. Changed intent, expired approval or a stale predecessor
requires a new exact request, not a force option. The returned grant reference
can be supplied as `--speculation /operator/grant-ref.json` to `run`, `ready`,
`step` or `drive`. Actual phases consume the shared allowance once; cancellation
and late returns retain actual measured costs.

Authorized speculative records remain held and non-governing until complete
owner impact reconciliation. Expiry ends new execution permission; it does not
erase authentic execution history. Equal hashes alone do not prove that new
requirements have no impact. Explicitly retained unchanged work returns to its
ordinary pending/review state without obligatory producer reexecution. Required
proof selection and independent review still govern its use. Changed or unknown
impact cancels affected applicability and requires the necessary new work.

Prepare the controller's complete `resume` payload with `prepare-decision`, then
submit its exact message through `submit-decision`. Ordinary reconciliation
reopens eligible unfinished work atomically; a fresh context is issued afterward.
Completed work is not reopened. The actual owner's semantic resolution must
already exist; the host cannot write that reasoning. Reserved L0 resolutions use
the existing externally attested protocol ingress described in the
[startup and recovery guide](lifecycle-recovery.md).

`attempt-status` distinguishes a verified candidate, adequately supported
contradiction, insufficient information, actual search/resource exhaustion and
human termination. Exhausted search does not mean that no solution exists.
None of these observations silently creates L0 result acceptance or release.
