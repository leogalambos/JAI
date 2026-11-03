# Governed delivery protocol v1 assets

The active candidate requires journal format 7, assignment `routing: {policy: ref}`
and explicit entity `execution` selection/work contexts. Selection returns no
records and one actual self-assignment `select_execution` decision; work consumes
that captured choice once. Typed setter assignment/decision prefixes remain
subject to the same ordered Store checks and atomic rejection. These contracts
do not add a static per-layer workforce table: local entities choose available
professionals, while every layer intrinsically reads the full public catalogue.
Current implementation evidence is maintained separately from the historical
P03 test mapping. The shared native lifecycle is implemented independently of provider-specific
spawn adapters; these schemas do not establish actual provider execution or
automatic scheduling.

These standalone Draft 2020-12 schemas implement the closed structural contracts
in the maintained governed-delivery protocol specification. The schema
families cover shared definitions, typed records, decision actions, messages,
processing responses, read-only current-basis queries, closed host control
events, and canonical provider RunReturn artifacts. References are local
to this package; implementations must not fetch remote schemas or follow paths
outside the declared package.

`conformance/manifest.json` indexes structurally valid and invalid examples,
strict raw parsing/canonicalization vectors, and semantic scenarios. Positive
examples demonstrate shape, not sufficient evidence, authentic authority,
effective confinement, or permission to use a result. Synthetic manifests and
blob bytes in the fixture registry establish reproducible real identities; they
do not prescribe P03's record-to-manifest mapping or supply signing credentials.

`tests/test_governed_delivery_protocol.py` exercises offline shape validation,
closed discriminators and boundaries, exact fixture/message identities, and the
existing strict lifecycle canonicalizer. The six-layer parameterization proves
structural representation only. It does not establish runtime ownership rights.

Semantic vectors include trusted-origin and reconstructible initial-state
fixtures, proposed schema-valid messages, expected first guards, effects, and
unchanged-state requirements. Exact fixture references bind typed record bodies
using the explicitly documented synthetic manifest mapping. Shared immutable
material is included by fixture reference instead of duplicated for every case.
These original portable vectors remain **specified, not executed as literal
transition fixtures**. The P03 engine and separate signed runtime tests execute
the mapped invariants; their actual scope and results are recorded in the
maintained governed-runtime test mapping. This does not turn every portable
vector into an executed test. Synthetic authority witness material is not a valid
signed wrapper; actual runtime tests use technical signature fixtures without a
production bypass.

The compound A/B scenario is explicitly a **non-executable roadmap**, showing
matched initial head/controller context and fresh B assignments, contexts,
observation, candidate, and review. Its later integration/acceptance phases need
complete transition messages and proofs in P03/P05/P08 before execution. It does
not claim current eligibility. P04 must separately demonstrate containment.

Ordinary leaf message examples describe typed payload projections, not an
alternate direct-ingest authority route. Actual provider execution starts with
`run_started` and returns a canonical `RunReturn` consumed atomically by
`run_completed`. Closed controls cover controller-context renewal, cancellation, monotonic usage
auditing, native-origin binding and durable broker observations. Finding shape binds one
reviewed subject and one named criterion; runtime entitlement remains a separate
requirement. The added examples refine the same protocol contract; they do not
provide a compatibility engine or synthetic production authority.

The sole runtime writer records ordinary events without signatures. Only explicit
reserved L0 decisions carry an external human proof; normal dispatch, control and
read operations have no signing key or attestation. Format 7 retains exact
versions, actual issued-context binding, ownership, independent review and
canonical historical effects. Earlier internally signed formats are unsupported
archives, with no migration or inherited acceptance.

Changes to these assets require a matching normative protocol revision and
independent review. This package adds no alternate recording API, authority
store, production validator, runtime state engine, or compatibility reader.

## Governed SABSA content

`sabsa-content-profile.schema.json` defines the engagement's exact adopted content
requirements. A profile's required `content_profile` identifies the fixed policy
slot `{logical_id, use_scope}` or `null` for general processing without a SABSA-content claim.
The explicit selected version is pinned in each mandate.
`sabsa-content.schema.json` defines canonical semantic product material. It reuses
ordinary immutable product material, owner bindings, reviews and selection; it
does not create a second semantic journal. The original minimum catalogue lives
at `sabsa/governed-catalogue.json` in the runtime.

Registration checks the owned payload's shape and meaning at the declared
boundary. Current-output assessment additionally resolves required units,
relationships, views, business traces and applicable independent reviews within
the exact output closure. Structural success does not establish substantive
quality, acceptance or permission to release. The maintained
[protocol reference](../../../../../docs/reference/governed-delivery-protocol.md)
and [operator guide](../../../../../docs/operations/sabsa-content.md) explain these
separate assessments and private/public projections.

## Shared process/native broker boundary

`broker-request.schema.json` is the single closed request vocabulary for both
transports. `reference` deterministically builds an immutable version reference;
it does not register, select or accept the proposed record. `propose.data` remains
base64 encoded actual bytes. A native adapter encodes text or artifacts it
actually received; an LLM need not calculate hashes or encode its source text.

An optional `run_started.native` binds the actual provider handle, immutable
delivered packet, captured tool envelope and finite transport limits. It does
not attest to an unobservable model identity. Subsequent controls carry the same
handle and exact context. Handle reuse requires the same immutable assignment,
actor, owner and scope after an observed terminal return; cancellation alone
does not prove a producer stopped.

`broker_requested` records intent before materialization or measurement.
`broker_observed` records the exact response and cumulative logical frame bytes.
Pure reads, proposals and reference construction need only the observation.
Exact request replay returns the captured response without repeating its effect.
Native logical-frame accounting does not charge that replay as a new admitted
frame; the existing process transport retains its conservative actual-wire
byte bound, including retransmitted request bytes. A conflicting identifier is rejected; a
physical intent without an acknowledgement is explicitly uncertain and is never
blindly repeated. Cancellation followed by a fresh eligible context can resume
work while retaining the original uncertain history. Late physical observations
remain history, not renewed permission.

The foreground `governed_native.py` carrier retains the existing Store between
parent calls. It launches no model and owns no separate journal. Its `issue`,
`start`, `request`, `complete`, `stop` and `status` operations use the same
admission and effect checks as process dispatch. Complete receives actual JSON
text without repairing its semantics; late results may be quarantined.
The full captured catalogue and every role instruction remain intrinsic lazy
read handles, independent of the selected specialty.
