# Governed process dispatch

The local-process adapter supports a Linux host route, `json-process/1`, around
an existing journal-format-9 Store. It is distinct from the native Claude Code
and Codex parent interface described in [layered delivery](../using/layered-engagement.md).
Process execution alone does not establish professional review, acceptance or
release permission. Actual confinement depends on the configured host boundary.

## Host invocation

The runtime receives an actually issued leaf context and host configuration.
It is the sole journal writer and needs no signing key for dispatch, control or
recording. Only explicit L0 decisions use the external human signing companion.
See [runtime recording](../architecture/governed-runtime-recording.md) for the
workspace boundary and the distinction between evidence and authorization.

```sh
python3 .ai/runtime/tools/governed_dispatch.py \
  --store /operator/engagement.jsonl \
  --engagement engagement-id \
  --context /operator/issued-context-ref.json \
  --config /operator/dispatch-config.json
```

All paths above are placeholders for operator-owned host files. The context file
contains its exact VersionRef, not a worker-selected actor or a fabricated
assignment. The context must be issued, currently applicable, within its finite
deadline, and limited exclusively by `elapsed_ms` with unit `ms`. The dispatcher
records actual start and measured usage, captures the process return, and records
the existing Store completion under its issued context. Success reports `status: completed`, the Store
`completion` response, `usage_ms`, and `audit_blob_id`; failure returns a diagnostic
and a nonzero CLI status. Successful execution does not establish professional
PASS, acceptance, or permission to release.

## Closed host configuration

```json
{
  "protocol": "jai.host-dispatch/1",
  "workers": [{
    "provider": "json-process/1",
    "argv": ["/usr/bin/python3", "/worker/main.py"],
    "files": [{"path": "/operator/worker/main.py", "name": "main.py", "sha256": "REPLACE_WITH_EXACT_SHA256"}]
  }],
  "destinations": [],
  "tools": [],
  "limits": {"packet_bytes": 100000, "total_bytes": 1000000}
}
```

Replace the illustrative digest with the actual lowercase 64-character SHA-256.
Enroll the functional chooser and each available work implementation in
`workers`. The dispatcher selects the exact matching entry from the current
context phase and captured choice; the caller cannot substitute a different
model or worker. Only explicitly enrolled flat worker assets are mounted under `/worker`.
Destination entries are `{handle, owner, root}`: `owner` is the exact assignment
ownership object, and `root` is an existing absolute host directory. Tool entries
are `{policy, worker}`, with an exact tool-policy VersionRef and the same worker
configuration shape. Enrollment does not replace the issued effect grant.
Unknown fields/providers, unsupported metrics, unavailable native isolation,
and assets overlapping L0 signing material, Store or controller material fail closed.

## Worker transport

The worker reads one JSON line with protocol `jai.process/1`, operation `input`,
the exact `run_id`, `assignment`, `context`, `manifest`, `attachments`, and
`manifest_hash`, and `execution`. Selection executes the global functional
chooser with no domain-effect rights and returns one actual `select_execution`
decision. Work consumes that same entity's exact choice in a fresh context.
Manifest entries contain `{handle, ref, use_scope, record}`.
Attachment entries identify exact authorized bytes by handle, blob ID and size;
an attachment must belong to a readable declared input, not merely exist in the
Store. Only purpose-specific records are delivered; another entity's transcript
and the complete engagement history are not recursively included.

Every entity also receives the full captured public role catalogue read-only at
`/catalogue/catalogue.json` and `/catalogue/instructions/<slug>.md`. Reading an
unselected specialty requires no task grant or neighbor request. Selected prompt
instructions only reduce context size. Full private routing/model configuration
is not delivered as ordinary policy-material handles. The same public bytes
remain readable when separately supplied as an authorized business input.

Review packets carry the exact structural `assessment_basis`, not a supplied
verdict. A setter receives bounded direct-child `owned_returns`; same-layer
rows can include its own issued child mandate and verified published material.
Cross-layer rows expose interface outcomes, not the other layer's staff or work
in progress. `current_slots` reports raw selected references and establishing
acts; an invalid current reference is never replaced by null or an older PASS.
Entitled revision feedback is explicitly historical and is not a new governing
input. All delivery remains subject to the existing byte bounds.

A completed child can publish an existing result without creating another
record. Its terminal intent is visible through the exact result fact captured in
the parent's `ready_basis`; integration publication additionally requires a valid,
unheld bundle. A context issued before that fact cannot see the later publication.
This projection does not create a new readiness token, qualify pending evidence or
repeat the child work. The existing producer, scope and adjacent-layer filters
still apply.

Each request is one JSON line with a unique per-process string `id`, an
`operation`, and exactly its operation fields:

| Operation | Fields | Effect |
| --- | --- | --- |
| `read` | `handle` | Read an authorized exact manifest attachment. |
| `propose` | `data` | Capture base64 output bytes; host returns `blob_id` and `size`. |
| `materialize` | `subject`, `blob_id`, `destination_handle` | Create an immutable version artifact under the exact granted owner's enrolled root. |
| `measure` | `tool_policy`, `targets` | Run the enrolled exact tool in the same native boundary. |
| `return` | `value` | Return the single canonical governed RunReturn from this process. |

Responses carry the same `id`, `ok`, and `result`, or `error: {code, message}`.
A measurement executable receives a bounded JSON input packet and emits raw
stdout; its captured blob and actual exit status are evidence of execution,
not a professional verdict. Raw measurement bytes count against the invocation's
existing aggregate byte limit. Nested tool brokers are unsupported.

New result material must be bytes captured from this run or explicitly delivered
authorized inputs/published outcomes. Echoing a digest, another context, or a host path cannot establish
producer identity. A worker needing clarification returns its own typed
`information_request` in RunReturn. Supplying a response and issuing another
context belongs to the later orchestration workflow. Missing declared bytes
prevent launch; corrupted identities are integrity failures and
cannot be replaced with guessed summaries.

## Native boundary and pending artifacts

Bubblewrap namespaces, read-only mounts, cleared environment, closed inherited
descriptors, and a native libseccomp filter enforce isolation. Shells and child
processes remain usable inside private scratch; forbidden host operations fail
through the native boundary, not a command blacklist. The worker cannot access
L0 signing material, ledger, controller, global project, or host network sockets. Network
retrieval is unsupported by this backend; this is not a role/layer policy
prohibiting public knowledge.

Broker grants supplement that boundary with exact JAI ownership, input,
tool-policy and destination authorization. Each operation rechecks current Store
state. The existing expected-head checks reject conflicting writes; an unrelated
commit does not invalidate an otherwise eligible run. Interrupted or rejected
execution records actual usage and an audit of effects already performed.
Materialized bytes may therefore remain as historical pending artifacts after
cancellation. Filesystem creation and ledger commitment are not one atomic
transaction, and such artifacts grant no current applicability or permission.

Native Codex/Claude execution, external services, unmeasurable token/cost limits,
automatic scheduling and the replacement release gate remain unsupported. There is
no weaker fallback when the required native boundary is unavailable.
