# Immutable scoped lifecycle (format 2)

Status: architectural decision for fresh engagements. Retain the existing typed
layered graph and use one authoritative lifecycle engine for identity, replay,
governing selection and exact release eligibility.

## Decision and alternatives

File hashes alone cannot express applicability or replacement. Editing records
loses historical truth. A parallel database leaves existing commands outside
governance. Replacing the whole graph discards its layer and adjacency controls.
Instead, persist existing graph operations inside atomic format-2 transactions.
Unsupported or unmarked ledgers are archives only, never executable engagements.
Fresh reconstruction uses maintained public specifications and new acceptance.

## Identity and predicates (C1, C2)

Logical IDs are stable identities, never paths. Immutable version manifests bind
logical identity, kind, exact content/member versions and semantic context.
Locators, display labels and transaction time are nonauthoritative. Canonical
semantic JSON recursively normalizes NFC strings and keys, rejects duplicate or
normalization-colliding keys and floats, sorts object keys and uses compact UTF-8.
Version and blob hashes use the domains `jai.lifecycle.version.v2\0` and
`jai.lifecycle.blob.v2\0`. Blobs bind exact bytes. Unordered members sort by role
and logical ID; ordered arrays preserve order. Distinct conclusions can share
content without sharing record identity.

Integrity, validity, scoped applicability, review, acceptance and permission are
separate predicates. A PASS observation grants none of the others. Historical
versions remain integral when obsolete. Only required current locators must
match their exact bytes; unrelated obsolete working-file drift does not block.
Ledger corruption always blocks globally.

Validity, applicability, sufficiency and review predicates are evaluated for the
exact `(scope, version)` context. Supersession in scope A does not invalidate an
unchanged version still governing an independent scope B. Explicit reliance may
name a different prerequisite scope; impact traversal follows those actual
cross-scope dependencies and closure identity binds the exact contexts.

## Governed changes and exact proofs (C3, C4)

One plan/apply mechanism handles replacement, invalidation and explicit
reinstatement. A plan binds predecessor selections, head, policy, request ID,
expiry, exact complete effects and allowed verification path. Transitive effects
cross scopes: affected conclusions, reviews, acceptance and permissions are
cancelled while unrelated branches remain. Replacement starts pending,
unreviewed and unaccepted. Historical reinstatement requires fresh applicable
verification and never revives cancelled proofs.

Plans grant nothing. External Ed25519 trust pins bind signer, public key and
explicit capabilities: `lifecycle-update` permits continuation; `accept` permits
human acceptance. Neither implies the other. Receipts bind exact source bytes,
effects, policy and head; forged, stale, expired and replayed requests fail.
Historical proof verification remains mandatory. Signed operator wrappers retain
their own serialization, including finite timestamp floats, and are bound by
proof digest; lifecycle canonicalization must not reserialize them.

Signed Fabric review and authorisation requests archive one assessment
context: the exact governing policy manifest and version,
supervision-policy source bytes, budget configuration and assessment
time. Historical replay reconstructs the original decision from those
immutable inputs, so later policy, budget or clock changes do not
rewrite historical truth. Current signing, application and eligibility
checks still enforce current controls; stale policies and expired
exceptions block current use. A governed continuation needs fresh
applicable verification and review, followed by separate human
acceptance. It never inherits prior acceptance or permission.

## Obligations and release (C5)

Exact governing contract and policy versions declare required input categories,
evidence/reviewer roles, multiplicity and permitted exclusions. Explicit scoped
selections fill every required slot with exact versions or independently reviewed,
contract-permitted exclusions. Missing, duplicate, conflicting or unauthorized
slots fail before prerequisite evaluation. Empty caller dependencies prove nothing.

Causal reliance runs dependent to prerequisite: conclusion to inputs, review to
subject and review evidence, acceptance to output and preacceptance closure,
permission to acceptance. Provenance/navigation are separate. Governing proof
selection maps exact subject and role to exact proof; this lookup is not a reverse
causal edge. Evaluate subject/input closure, selected review closure, then
acceptance/permission closure. Every required prerequisite must pass conjunctively;
latest-by-time, predecessor fallback and an alternative supporting path are forbidden.

One evaluator serves justify, status, acceptance planning and release. Acceptance
binds exact output and preacceptance closure/policy, excluding acceptance itself.
Closure changes cancel it. Release additionally requires new current human
acceptance and permission. The read-only gate reports eligibility, never release.
Synthetic signer/gate tests demonstrate technical behavior only, not human approval.

## Persistence and deployment (C2, C6)

Each JSONL line is a complete transaction: format 2, engagement, sequence,
previous hash, unique transaction ID, operations and optional proof. All mutations
validate a complete candidate under exclusive lock, check expected head and
atomically replace/fsync file and parent. Failed commands leave bytes unchanged.
Unknown operations, malformed envelopes, duplicate IDs and invalid proofs fail.
There is no raw-entry compatibility parser or optional parallel lifecycle store.

See [deployment and recovery](../operations/lifecycle-recovery.md). Windows
security limitations remain fail-closed rather than weakening secure-file checks.
