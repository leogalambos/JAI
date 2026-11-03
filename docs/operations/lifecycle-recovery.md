# Start or recover a governed engagement


## New-format startup

Current source work requires journal format **9**, protocol `jai.governed-delivery/1`,
and a typed bootstrap recorded by the sole runtime writer. Source/blob
identity domains remain unchanged. Prior journals are unsupported historical
archives; never edit them to look like a current engagement or import their PASS,
acceptance or release permissions.

Format 9 retains the distinction between record validity and established governing
use, and records stable plans, owner procedures and physical invocations. Earlier
formats cannot be resumed under these changed meanings. Preserve them and start
a fresh engagement from the actual authorized inputs. Ordinary work consumes established input facts; it does not
reassess the contents or historical support of accepted upstream tasks.

The journal references immutable validation files in its adjacent
`<journal-name>.blobs/` directory instead of embedding whole-file copies. Preserve
the journal and all referenced blobs together, along with the pinned enrollment
and session locator. A journal alone is not a complete recovery archive. Cold
reconstruction verifies required file identity and availability; a missing or
corrupted blob is an explicit failure, not permission to substitute a working file.

For a current-format restart, resume the recorded engagement locator. Prepared
native manifests are durable before dispatch. Reconcile a started or uncertain
physical invocation using its actual handle/capture; do not issue its members
again or claim that cancellation proves termination. Exact completed replay
returns the existing receipt without another physical charge. Missing member
results remain unresolved without discarding independent admitted members.
See [review and release readiness](validation.md).

The journal grows with its accepted transactions. Its secure reader captures a
finite regular-file snapshot rather than applying the 32 MiB limit used for an
individual material file. Material/proof bounds and the transaction validation-
artifact bound remain separate. A larger journal does not waive L0 signature,
identity, chain, expiry or current-basis checks. Normal updates reuse the verified
prefix and validate newly added dependency edges; they do not walk every accepted
use point again. Cold reconstruction and explicit audit still verify history.

The workflow CLI operates an already bootstrapped Store. The host prepares the
actual operator inputs, criteria, capability snapshots and closed profile and
records their bootstrap through the ordinary writer. Bootstrap, work and queries
need no internal signer or keyring. Workers return captured results under their
actual issued contexts; they cannot provide a replacement controller identity.
Only explicit reserved L0 decisions use known public keys and the external human
signing companion. See [runtime recording](../architecture/governed-runtime-recording.md).

Once the host has prepared the complete bootstrap message, the supported ingress is:

```sh
python3 .ai/runtime/fabric/fabric.py validate --message /operator/bootstrap.json
python3 .ai/runtime/fabric/fabric.py submit engagement-id \
  --message /operator/bootstrap.json
```

These source-checkout commands use placeholders for actual host-owned files.
The configured Fabric location must be the same Store used by the host adapter
and subsequent workflow commands. Validation alone records nothing. Submission
checks the typed transition, exact effects, current head, scope, expiry and replay.
L0 signatures are checked when an explicit L0 decision is submitted or its grant
is relevant to a new action. See the
[protocol](../reference/governed-delivery-protocol.md) for the closed bootstrap
contract and [runtime paths](../configuration/runtime.md) for Store location.

After successful bootstrap, use the exact `entry`, `run --phase selection`,
`run --phase work`, `local-entry` and `status` commands in
[the operating guide](normal-layered-workflow.md). Deployment, native provider
integration and automatic recovery orchestration remain separate work; these
instructions do not claim a fresh installation rehearsal.

## An updated input blocks work

Preserve the existing record and classify the cause before changing anything.

| Cause | Required treatment |
| --- | --- |
| A legitimate input or assumption changed | Capture new immutable bytes and a new owner-attributed source. The exact entitled owner decision selects the new scoped version and cancels affected applicability. |
| Required current material is missing | Restore its exact authorized bytes, or obtain the owner's actual input change. A new digest alone does not verify a replacement. |
| A source is obsolete only outside this output's closure | Retain its history. Assess the specific output and scoped dependency closure rather than blocking on unrelated history. |
| A signature, digest or chain is corrupt | Reject it and preserve the diagnostic. Do not change a historical hash, invent a proof, or force approval. |
| The journal predates the current contract | Keep it as an archive and start a fresh current-format engagement with newly established verification. |

A current-format source update is a typed owner act, not permission to rewrite a
past file. Use the maintained external human review/signing procedure for exact
reserved `delivery-change` effects. The proof must still bind the real signer,
scope, predecessor head, approved effects, expiry and one-time request identity.
The historical controller context is an audit binding: its expired execution
lease or cancelled old input cannot veto a genuine owner authorization needed
to record the replacement. This is not an ignore-drift or force-approval mode.

From the update's effective point, cancelled records and dependent permissions
cannot justify the affected output. New records remain pending until their
required verification and review succeed. No valid current basis means blocked;
JAI must not fall back to the replaced predecessor. Reinstatement is an explicit
traceable act with applicable verification requirements and never revives old
acceptance/release permissions.

## Resume entity execution

Obtain an entitled current assignment for the changed inputs. Use its actual
current professional plan, or obtain a new local choice if that mandate or plan
has changed. Every work invocation receives a fresh finite context; the plan is
not a consumed execution grant. Restart does not reset a running local window.
At timeout, report the paused unit and obtain an explicit operator time extension
or stop. An extension applies only to future fresh grants and unfinished work;
it does not revive old contexts or alter explicit aggregate caps. A completed or
cancelled logical task is not reopened by changing a label.

Rework preserves the governing criteria. Reformulation is an owner's explicit
change; inherited meaning goes through its adjacent owner. Historical findings
are delivered as marked read-only feedback, not new current evidence. Keep a
stable reviewer for the same owner, criteria and scoped input generation unless
an entitled replacement decision preserves the reason and previous findings.

Missing current capability material rejects an otherwise eligible
completion before effects. The host can still record the actual physical stop,
measured usage and failure audit through the existing typed cancellation route.
Recorded obsolete/late/over-budget runs can be quarantined reproducibly. Neither
case creates accepted professional output.

When new verification succeeds, inspect the exact output UsePoint with workflow
`status` or the authenticated current-basis query. Obtain new exact human result
acceptance and, separately, release permission where required. File creation,
an execution receipt and professional review do not publish or authorize a
release. Publication follows the separate [release procedure](../reference/versioning.md).
