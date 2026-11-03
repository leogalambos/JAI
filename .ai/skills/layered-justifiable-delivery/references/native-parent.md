# Internal native parent procedure

Owner: JAI runtime maintainers. Contract revision: 2026-11-01.

This reference is for the trusted orchestrating parent. It is not the user
interface, a network API, another evaluation engine, or permission to sign L0 acts.

## Foreground runtime

Use `tools/governed_layered.py` from the installed common runtime, or
`.ai/runtime/tools/governed_layered.py` when operating from its source package.
Capture the actual task/criteria in private files; never interpolate their text
into shell commands. Use the current provider's existing foreground execution
session facility, keeping stdin open across native model turns. If that facility
uses a private PTY, configure that private PTY for noncanonical, no-echo input
before starting the runtime so complete JSON frames are not truncated. Do not
reconfigure the operator's own interactive terminal.

Internal start arguments are `start --home .fabric --engagement ID --task FILE
--provider codex|claude --work-item ID`. Optional `--deadline-ms ABSOLUTE_MS`
and `--limit-ms MS` impose explicit global caps; omission means no aggregate cap.
Local defaults are `--iteration-ms 600000 --max-reworks 3`. Local selection/work
shares its incoming unit's iteration; preparation does not start its clock.
Optional `--criteria FILE`, `--config FILE` and `--model-config FILE` preserve
actual explicit input/enrollment. Omitted criteria reuse task bytes verbatim.
The generated `.fabric/ID.session.json` locates the journal and pinned enrollment;
it contains no governing workflow state. Cold resume uses `resume --session FILE`.
An explicit changed `--config` creates a distinct pinned locator; no old hash is
ignored and no old conclusion is transferred.

Start returns a prepared physical invocation. Resume returns a journal-derived checkpoint.
Subsequent closed JSON-line frames have `id`, `operation` and exactly that
operation's fields. The shared native operations are:

| Operation | Fields | Meaning |
| --- | --- | --- |
| `issue_batch` | `jobs`; optional `bound_ms`, `invocation_id` | Issue compatible logical jobs as one bounded physical invocation; a singleton uses the same path. |
| `prepare` | `invocation` | Persist exact member packets, resources and the combined prompt before a provider call. |
| `start` | `invocation`, `provider`, `handle`, `capture` | Bind the actual provider observation to that prepared invocation. |
| `request` | `invocation`, `member_key`, `request` | Relay an actual member request under that member's input and tool rights. |
| `complete` | `invocation`, `raw`, `capture` | Retain the actual semantic envelope and assess its members independently. |
| `status` | `invocation` | Read the physical state and its logical members. |
| `stop` | `invocation`, `capture` | Record an actual cancellation observation; uncertainty retains the reservation. |
| `local_budget_status` | `assignment` | Read an exact assignment or explicit unit's remaining local window, revision, stage and pending observations. |
| `pause_due` | `scope` | Record elapsed active windows and report operator notices without a semantic verdict. |
| `extend_local_budget` | `unit_id`, `expected_revision`, `additional_ms`, `operator_instruction_ref` | Extend only the exact paused revision under the actual operator instruction; old grants remain expired. |
| `stop_local_budget` | `unit_id`, `expected_revision`, `target`, `reason`, `operator_instruction_ref` | Stop the unit or task operationally without claiming a business outcome or remote termination. |
| `close` | none | Close the foreground host session. |

Each job contains `assignment`, `phase` and its actual `selection` for work;
`speculation` identifies an existing explicit grant when applicable. Layered operations:

| Operation | Fields | Meaning |
| --- | --- | --- |
| `next` | `scope`, `speculation` | Advance ordinary owner procedures, then offer one compatible physical invocation or waiting/reconciliation facts. |
| `checkpoint` | `scope` | Read exact current input locators, inflight bindings, pending effects and episodes. |
| `entry` | `scope`, `work_item`, `limits`, `deadline_ms` | Enter actual owner-approved current L0 inputs through the existing root gate, without inheriting old conclusions. |
| `local_entry` | `handoff`, `phase`, `acceptance` | Create a receiver/setter gateway from the actual adjacent interface. |
| `handling_entry` | `episode`, `task`, `layer` | Use the existing collect/relay/resolve/reconcile mandate. |
| `output_status` | `subject` | Assess one exact output UsePoint; this grants nothing. |
| `human_handoff` | `episode`, `scope` | Read actual conflict/option/evidence dossier without requiring a signing key. |
| `prepare_human` | `payload`, `purpose`, `scope` | Prepare an actual unsigned L0 change proposal when a matching key is enrolled. |

Use null for absent nullable fields required by the operation; omit optional
fields unless supplied. Do not introduce arbitrary extra fields. Finite loop bounds belong to the orchestrator; waiting stops the
loop instead of polling. Call readiness/next at real scheduling boundaries, not
after each broker read. Do not reconstruct the journal between turns.

## Actual native lifecycle

1. For an `invoke` result, execute the exact prepared native intent. A selection
   phase asks each actual local entity for its staffing/model choice. Work uses
   its current recorded plan. The plan remains usable for unchanged assignments;
   each invocation still receives fresh bounded grants. Compatible jobs share
   one actual physical handle, while author and reviewer responsibilities remain
   physically separate. Preserve every individual question and local responsibility.
   Deliver `prepared.invocation.arguments.message` inline as the actual Codex
   tool message, or the corresponding prepared prompt field for the active
   provider. Never substitute a file-only "read these instructions" stub. A
   retained message file is diagnostic evidence, not a required native Read tool.
   This is a small base prompt with immutable resource references, not the entire
   catalogue, professional instructions, schema or historical input bodies.
   Follow its procedure/input/constraint indexes as needed. Catalogue navigation
   exposes every category, page, complete role record and instruction; it is not
   a role whitelist. Neighboring input parts remain available across questions;
   local producers choose their actual dependencies without an automatic Q filter.
   `bounds.local_budget` identifies the actual incoming local unit, phase,
   revision and remaining iteration. Planning and ready integration have separate
   windows; a question's local entities share its allowance and common rework
   counter. Actual physical start activates the iteration clock. The finite grant
   lease and any explicitly supplied aggregate caps still constrain the call.
   Finish before its effective deadline, including broker/return transport.
   Resume preserves the original as-of presentation and cannot revive a grant.
2. Bind the actual returned provider handle with `start` and its observed capture.
   Pass the actual provider observation as `capture`; the runtime retains it as
   `provider_observation`, separately from `host_delivery: prepared.host_delivery`.
   The latter contains the exact
   `manifest_blob_id` and `prompt_blob_id` delivered in this invocation. It is
   trusted host presentation metadata, not a provider attestation or business
   approval. Do not reconstruct it from current code after a crash. A bound cold
   resume restores its original bytes and handle map; an unbound uncertain call
   requires actual platform reconciliation or the existing cancellation path.
   Keep requested model controls separate from unobservable served-model facts.
3. Relay one actual broker request through `request`, identifying its physical
   invocation and issued member key; forward the actual response to that same
   member's native context. Exact handles are listed in the prepared resource
   indexes and original `read_index`. Resource handles identify captured bytes;
   they never grant additional source or material permissions. The complete
   intrinsic catalogue and all instruction handles remain accessible. Decode and
   deliver actual bytes through deterministic transport, without rewriting content.
   Native Read may use supplied immutable resource paths when actually available.
   Without dedicated native Read/Write tools, use only a reviewed fixed-purpose
   semantic carrier for the exact delivered input file or explicitly assigned
   artifact path, under the actual role ceiling and L0 sandbox. A carrier grants
   no general shell, arbitrary execution, extra document access or reviewer fixing
   rights. If no appropriate carrier is available, relay deterministically decoded
   broker content inline to the same entity and capture its returned body. Do not
   ask it to recover bytes from an inaccessible file or infer additional tools.
4. Collect the actual `jai.semantic-return/1` envelope: `results` identify issued
   opaque member keys and contain the closed role-specific semantics named by the
   prepared contract. Selection supplies actual professionals/model choice;
   setters supply actual questions, criteria and owner procedures; authors supply
   actual materials and evidence; reviewers supply actual verdicts, findings and
   conditions. Exceptional owner actions retain their explicit decision semantics.
   Do not ask the model to construct wire records, wire envelopes, hashes or structural
   metadata through stencil/reference/propose round trips. The host codec stages
   inline materials and derives exact mechanical identities from each issued packet.
   It never supplies missing professional conclusions or rewrites domain JSON.
5. Call `complete` with the invocation, exact raw semantic envelope and actual
   terminal tool capture. Raw capture, codec, encoded member returns and input
   identities remain traceable. The same Store admits valid independent members
   and quarantines invalid or stale ones, without repeating accepted jobs. Missing
   required evidence still prevents the affected output's acceptance or release.
   Staffing plans are reusable for unchanged assignments; plan replacement governs
   future grants without revoking earlier bounded grants merely for a preference
   change. Replacing an owner procedure cancels its affected dependent applicability.
   After an actual owning L0 decision changes the governing inputs, use `entry`
   for a lawful new current-basis root where needed. Preserve the explicit finite
   bounds; do not reinstate an unchanged cancelled basis or select an old PASS.
   Collect output according to the actual delivered role/tool ceiling. Choosers
   and nonfixing reviewers return message bodies for parent capture. Authors with
   Write/Edit may instead write their own artifact to authorized scratch inside
   the effective sandbox. The parent captures and stages the exact artifact
   bytes; a mutable file path is not the immutable material identity. Do not
   impose a universal response-only or no-file rule on authoring roles.
6. Continue eligible work through `next`. Recorded owner procedures mechanically
   instantiate ordinary local mandates and select eligible unconditional reviews;
   they do not invent model choices, answers or verdicts. Conditional, negative,
   conflicting or discretionary cases return to the actual owner. Existing adjacent
   gateways carry the reviewed interface to its receiving layer. No response or timestamp substitutes for current
   justification, governing selection, independent review or required L0 authority.

For an exposed prepared invocation without a confirmed handle, `next` returns
`reconcile`, its exact invocation/member identities and deterministic task name;
it does not spawn individual members or prepare another call.
Inspect the actual native platform record. If invocation is confirmed, use its
actual handle through normal `start` or existing bound continuation. If it is
unknown or cannot be continued, record the actual observation through the same
`stop` operation. An actual `not-dispatched` observation can close an unstarted
call; an actual `terminated` observation can close a started call. Unknown outcomes
retain uncertainty and the physical reservation; never fabricate termination.
Late cancelled output remains history without semantic admission or a renewed
grant. Each member consumes its actual whole physical duration locally, while
the shared root is charged only once per physical invocation.
Pending physical requests retain their uncertainty and must not be repeated.

## Operational local timeout

An ordinary substantive qualification error is feedback, not permission to change
the result or weaken a guard. Retain the actual failed action, diagnostic and
exact affected record references in private evidence. If `next` stops at that
qualification boundary, inspect `checkpoint` readiness and the actual current
plan/receipts. Use the existing `issue_batch` operation only for a genuinely
eligible actual owner assignment and its current selection, then relay the exact
diagnostic to that owner as runtime feedback. The owner chooses whether an
explicit rework or reformulation is warranted; the parent never edits criteria,
business identifiers, observations or PASS. All ordinary ownership, applicability,
dependency and finite-grant checks still apply.

Readiness is an automation scheduling hint. After an actual substantive
qualification denial it may remain false with `owner_procedure_advances_or_waits`;
do not override that hint or restore routine bookkeeping model turns. Use the
actual chooser receipt/current plan, rather than inventing a choice from an empty
readiness selection. Ordinary explicit issuance must still establish a genuinely
eligible owner grant under the existing execution-right checks. This handoff is
for the captured qualification failure, not a general retry or a new scheduler.

Sweep `pause_due` first. An expired local window requires the operator's actual
operational extension or stop before new owner work; no old grant is revived.
This handoff is limited to substantive qualification feedback such as missing
required evidence. Corrupted history, invalid signatures, forged origin or an
integrity failure stops processing for investigation. Do not treat every proof
error as ordinary qualification feedback or add a catch-all retry.

`next` sweeps due active windows and includes `operator_notices`. It can still
offer eligible unrelated work; an exhausted unit remains paused. Without eligible
work, `paused` requests the operator's operational choice, not a signed business
decision or an automatic negative review. The checkpoint includes local unit IDs,
revisions, remaining time, stage and actual pending observations.

The operator may inspect or act through the existing layered CLI:

```text
budget-status --session FILE --unit-id ID
extend-budget --session FILE --unit-id ID --expected-revision N --additional-ms MS --operator-instruction FILE
stop-budget --session FILE --unit-id ID --expected-revision N --target unit|task --reason TEXT --operator-instruction FILE
```

The instruction file contains the actual operator instruction; its exact bytes
are captured in CAS and bound to the ordinary controller event. It is not a new
business axiom, private key, signature or model-manufactured permission. A positive
extension makes the same iteration pending; its clock begins at the next actual
dispatch. Iteration/rework counts are unchanged. Do not silently extend, revive
expired contexts, clear pending effects or claim an unknown platform call ended.

## External human handoff

Always render the actual dossier before discussing signing readiness. Missing
keys do not hide conflicts or turn an ordinary information request into L0.
`prepare_human` accepts an explicit proposed change payload; it does not select
the human's answer. Without matching public enrollment it returns a readiness
gap and no signing package, message or fictitious signer.

When prepared, the package contains the exact unsigned message, intent and
operator request. The operator runs the existing `operator_actions.py sign`
tool in the host terminal using the package's exact `sign_command`. Display that
command inline with the actual decision request; do not leave the operator to
construct it from package metadata. Its default
key is `~/.local/share/jai-operator/private.pem`; the operator may append
`--key /another/private.pem` to select another location outside all agent-accessible
mounts. Installation offers confirmed creation but never enrolls public trust.
The agent never reads that key. Bind the actual public
receipt with internal `bind-human --package DIRECTORY --receipt FILE`; this
verifies and writes the exact proof/message without journal submission.

The operator then uses the package's exact `fabric.py submit` command and
`FABRIC_HOME` against the same journal. Never run a reserved authority command
on the operator's behalf or bypass its native hook denial. Resume from the
actual resulting journal state; a chat approval is not a signed receipt.
