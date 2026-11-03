# Governed delivery protocol, version 1


## SABSA content profile extension

The active source journal representation is format 9. The sole runtime writer records
ordinary events without signatures or signing keys. Only explicit reserved L0
decisions carry a signature. The [recording contract](../architecture/governed-runtime-recording.md)
defines the exact row shape and authority boundary. It retains one
`validation_artifacts` sorted unique list of first-use content identities in the
existing content-addressed blob store; whole-file bytes are not repeated inline.
Independent replay verifies exact file hashes, availability, declared versus used
first-use identities, the 32 MiB transaction aggregate bound and original effects;
missing, extra or corrupted files/references are rejected. Fresh operations still check
relevant current material and authority. Historical captures are not a fallback
for unavailable current evidence. Older journal formats remain unsupported
archives; no acceptance or permission is imported into a new engagement.
Recovery requires the journal and its referenced blob closure, not the journal
alone. Semantic wire format `jai.semantic-return/1`, host encoder
`jai.semantic-encoder/2` and the authority boundary are unchanged by this storage
representation.

The profile's required `content_profile` field is `{logical_id, use_scope}`,
identifying an existing authoritative source-selection slot, or is `null` for
general processing without a SABSA-content
claim. The slot explicitly selects an exact immutable policy VersionRef; issued
mandates capture that version as a dependency. It cannot silently relax an
inherited SABSA requirement. The selected source contains canonical
`jai-sabsa-content-profile/1` JSON: source editions and
adopted scope, the original catalogue identity/version, required owned units,
relations and views, explicit entitled exclusions, audiences and bounded claim.

Semantic products carry one canonical `jai-sabsa-content/1` payload in their
existing immutable material. Its closed schema defines units, typed relationships
and view bindings. A locator names an exact product VersionRef and local unit or
relation key; `product: null` denotes the containing product, never a latest
lookup. Units belong to the product owner's layer and question. Relationship
navigation does not grant visibility or replace declared causal dependencies.

The [content decision](../architecture/governed-sabsa-content.md) defines the
closed field contract, original six-layer catalogue and special conceptual
attribute, management activity, measure and observation requirements. The
[operator guide](../operations/sabsa-content.md) describes current completeness
and deterministic JSON/Markdown views. These assessments reuse current governing
selection, dependency closure and independent reviews. Missing current semantic
content remains a gap; neither historical PASS nor structural validity supplies
acceptance or release permission. Public reports and views have a separate
confidentiality boundary and cannot disclose private provenance.

The [layer model](../architecture/sabsa-layer-model.md) and [delivery profile](sabsa-delivery-profile.md) define the protocol's processing and content obligations. Protocol validity alone grants no execution, acceptance, or release authority.

## Coordination

The [coordination contract](../architecture/governed-escalation-scheduling.md)
defines default pause, episode handling, explicit speculation and reconciliation.
The current closed schemas require:

- Profile `scheduling`: finite `collection_window_ms`, explicit `control_limits`,
  nullable `max_search_steps`, `max_escalation_rounds`, and nullable
  `initial_deadline_ms`. The last value records the actual optional initial
  global stop; it is never inferred from bootstrap message expiry.
- Context `speculation`: an exact grant reference or null, and `ready_basis`:
  the opaque fact tokens captured for that run. Completion consumes those
  delivered facts, never new facts arriving during execution.
- Handling assignments: `handling` with exact `episode`, `package` and typed
  `task`. These are narrowly entitled mandates, not caller-controlled pause bypasses.
- Escalation products: immutable `episode` metadata with `root`, `previous`,
  `collection_head`, `unfinished` and `decisive`. Later packages do not rewrite
  their predecessors or implicitly resolve uncovered conflicts.
- Final-result products: a typed `outcome` tied to the actual attempt and evidence.
  Missing information or exhausted search cannot create a contradiction proof.

Captured setter/integrator returns support closed `relay` intents under their
actual episode-handling rights. Setter returns support `resolve_escalation`
decisions under the actual owner's rights; native authority proofs remain null.
Reserved L0 decisions still require the real external human proof. A valid
speculative work return can finish its task while its results remain held;
finishing execution does not qualify or accept those results.

Pause follows the affected layer in its scope and actual dependency members
across scopes. Sharing a blob alone does not invalidate an independently governed
use. Reconciliation covers every affected assignment and held result, with exact
owner impact and scoped basis. Retaining a result while discarding its required
dependency is contradictory and rejects atomically. Retained unreviewed work
returns to ordinary pending/review state without requiring producer repetition.

## Selection and routing

Required local selection/work contexts and global capability routing are defined
by the [layer workflow](../architecture/governed-layer-workflow.md). See
[layered delivery](../using/layered-engagement.md) for engagement operation.

Each assignment has `routing: {policy: ref}` for the intrinsic current L0
capability source at the bootstrap scope. It has no per-layer profession table
or neighbor-selected route ID. Each entity context requires
`execution: {phase: selection}` or `execution: {phase: work, selection: ref}`;
controller audit contexts use `execution: null`. A selection return has no
records and one self-assignment `select_execution` decision with `specialties`,
`provider`, `workload_class`, `model_selector`, `reason`, the exact previous-plan
reference (or null), and null `authority_proof`. The actual plan persists for its
unchanged assignment. Each physical invocation receives fresh bounded one-use
authority. Superseding a staffing preference affects future issuance; it does
not by itself invalidate completed work or an already-issued bounded grant.
Original deadlines and cumulative allowances remain in force.

Role-specific semantic returns, explicit owner procedures and compatible
physical batches preserve exact ownership. Host encoding retains the actual semantic capture and its
relationship to admitted wire returns. Ordinary mechanical procedure steps are
controller events under an actual owner policy, never fictional model returns.
Each member retains its exact inputs and independent admission outcome; physical
usage counts once. Separate author/reviewer conversations remain mandatory.

Journal `validation_artifacts` binds the exact first-use content identities in
the content-addressed blob store. Replay uses those referenced bytes. New work
checks relevant mutable conditions at its action boundary, while ordinary
progress reuses established immutable facts; historical assets cannot waive
missing required current evidence. Transient live material
failure rejects an otherwise eligible completion before effects; explicit
runtime-recorded cancellation accounts for the physical failure. Quarantine depends on
replayable ledger/time/usage facts.

## Journal and encoder compatibility

Start a new engagement using the format-9 bootstrap and explicit current input
manifest. Archived records do not transfer acceptance, verification, or release
permission. There is no migration or compatibility execution route.

Native semantic envelopes retain wire format `jai.semantic-return/1`. Their
raw-to-encoded linkage records exact host encoder `jai.semantic-encoder/2` in
`capture.codec`. An older or absent native encoder identity is rejected clearly
as an unsupported historical version before recompilation or validation-asset
comparison. Preserve that archive and start a separately verified engagement;
there is no migration, historical re-encoding or inherited acceptance. Journal
format is 9. Ordinary process JSON returns have no semantic encoder.

The confined `json-process/1` dispatcher and explicit one-step workflow are
described in the [operator guide](../operations/normal-layered-workflow.md).
Native Codex/Claude execution uses the common bridge described in the
[native execution contract](../architecture/gen2-native-execution-bridge.md).
Provider qualification is separate from protocol support. The bounded
coordination model operates on existing tasks. See
[deployment and recovery](../operations/gen2-deployment-recovery.md) for packaging
and recovery requirements; packaging checks grant no acceptance or release authority.

## 1. Authority and storage boundary

Protocol messages propose typed actions or return assigned results. Fields naming a sender, reviewer, layer, or authority are claims, not credentials. The trusted dispatcher supplies a verified execution context outside the message: actual principal/run identity, current assignment and capabilities, exact issued context, permitted delivery/effects, and current scope visibility. The recorder independently checks that context and the actual returned bytes before any consequential effect.

An entity cannot create its own runtime-issued context or submit an authority receipt as if it were a controller credential. The host is the sole writer in the operator-controlled workspace; ordinary origin/control/read proofs do not exist. A human-authority proof is an exact immutable attachment referencing the existing signed wrapper protocol; do not reserialize that wrapper through this protocol's semantic canonicalizer. Historical event provenance records the verification basis at the time of the act. Replay verifies it without requiring an old live session or fabricating missing provenance.

Use the existing authoritative immutable lifecycle and atomic transaction mechanism. Messages, assignments, contexts, results, and decisions are typed lifecycle records, not a parallel store of approval state. Transport queues/caches may retry delivery but cannot grant applicability. Blob registration proves byte identity only; it does not select a source as governing or grant access to it.

## 2. Closed wire envelope and references

The transport identifier is `jai.governed-delivery/1`. Objects are closed: unknown fields and unknown discriminator values are rejected. Version 1 schemas use JSON Schema Draft 2020-12 with local references only. There is no remote schema retrieval, dynamic extension field, arbitrary operation list, or caller-supplied manifest escape hatch.

| Required field | Structural type and meaning |
| --- | --- |
| `protocol` | Constant `jai.governed-delivery/1`. |
| `message_type` | One of the types in section 3; selects exactly one payload definition. |
| `message_id` | Lowercase 64-hex digest calculated by section 4. |
| `request_id` | Nonempty string, at most 128 characters; idempotency key owned by the verified origin within the engagement/scope. |
| `correlation_id` | Nonempty string, at most 128 characters; groups an assignment, information exchange, or escalation without granting authority. |
| `engagement`, `scope` | Nonempty strings, each at most 128 characters; the ledger and governing context in which effects are requested. |
| `sender`, `recipient` | Participant references defined below; actual runtime routing must agree with these fields. |
| `context` | Exact issued context reference; `null` is allowed only for `bootstrap` or the runtime-issued `control_event`/`renew_control` operation. It grants no ordinary leaf authority. |
| `profile` | Exact version reference for the governing protocol/engagement policy profile; `null` is allowed only for `bootstrap`, which verifies its proposed profile against independent host configuration. |
| `expected_head` | Lowercase 64-hex engagement transaction head; zero repeated 64 times is the empty-ledger head. |
| `issued_at_ms`, `expires_at_ms` | Nonnegative integers no larger than 9007199254740991, UTC milliseconds since the Unix epoch. Fresh requests require `issued_at_ms < expires_at_ms` and the trusted assessment clock before expiry. |
| `causes` | Array of distinct prior message IDs, possibly empty; correlation is not a causal dependency by itself. |
| `attachments` | Array of attachment descriptors, possibly empty. |
| `payload` | Closed object selected by `message_type` and, for `decision`, its `action`. |

A **version reference** has exactly `engagement`, `scope`, `logical_id`, and `version_id`; the first three are nonempty strings and `version_id` is 64 lowercase hex. This names a particular stored version in its authorized scope, not the latest record with that logical ID. Cross-scope references require an explicit permitted dependency and access grant. Another engagement's content must be explicitly imported/referenced under policy; matching hashes do not transfer permissions.

Here `ref.scope` identifies the immutable record's **origin namespace**, not its applicability wherever it is used. A **use point** has exactly `{ref: VERSION_REFERENCE, use_scope: text}` and identity `(engagement, use_scope, version_id)`. The same immutable version may have independent applicability in several use scopes. Never rewrite `ref.scope`, clone the version, or globally change predicates by version ID to represent a new use. Section 3.3 defines activation and dependency contexts.

A **participant reference** is exactly `{ "kind": "assignment", "ref": VERSION_REFERENCE }`, `{ "kind": "authority", "id": STRING }`, or `{ "kind": "controller", "id": STRING }`. An assignment's immutable content identifies its layer, entity responsibility, and owner; those values are not repeated as editable envelope grants. Authority/controller IDs resolve in trusted configuration. An unknown or mismatched participant is rejected even when its JSON is valid.

An **ownership coordinate** has exactly `layer` (integer 1–6), `work_kind`, `question`, and `work_item`. For `work_kind: question`, `question` is one of `what`, `why`, `how`, `who`, `where`, `when`. For `integration`, `handoff`, or `measurement`, it is `null`: these are work kinds, not additional organizing questions. Engagement/scope come from the owning version reference. The verified actor also needs rights for the exact work item; same-layer membership is insufficient.

An **attachment descriptor** has exactly `blob_id` (64 lowercase hex), `byte_length` (nonnegative safe integer), `media_type` (nonempty string), `classification` (`public`, `internal`, `confidential`, or `restricted`), and `access_handle` (nonempty broker-issued string). A handle is not an arbitrary filesystem path or URL. The broker verifies exact bytes, length, declared access, and classification against the issued context. The descriptor does not grant access by appearing in a message.

All counters and budget quantities use nonnegative integers no larger than 9007199254740991. Text is Unicode; schema length limits do not replace canonical normalization or semantic checks.

## 3. Message and payload catalogue

In the following table, `ref` means a version reference, `refs` an array of version references, `text` a nonempty string, and `message` a prior message ID. Reference arrays are ordered unless the payload explicitly says otherwise; duplicate semantic references are rejected.

| `message_type` | Exact required payload fields | Entitled origin and permitted meaning |
| --- | --- | --- |
| `bootstrap` | `controller_id: text`, `use_scopes: text[]`, `profile: profile_record`, `l0_inputs: source_record[]` | Trusted host controller only, against an empty engagement and independently configured authority. Section 3.1 defines the finite independently authorized scope list and narrow initialization exception; null context cannot authorize ordinary operations. |
| `control_event` | Closed event-specific object in section 3.2 | The sole runtime controller records bounded context renewal, actual execution facts, or cumulative usage. It cannot manufacture a leaf's semantic return. |
| `record_proposal` | `logical_id: text`, `record_type: enum`, `record: closed typed record` | Trusted recording operation checks the actual origin and the closed record contract below, then constructs an existing lifecycle manifest. It registers pending content; it does not select or qualify it. |
| `assignment` | `assignment: ref`, `owner: ownership`, `responsibility: enum`, `inputs: refs`, `criteria: ref` | Entitled setter or dispatcher delivering the already-authorized exact assignment. Responsibility is `setter`, `author`, `reviewer`, `integrator`, `integration_reviewer`, `receiver`, or `measurement`. Effects and limits are resolved from that exact assignment record, not separately supplied delivery grants. Delivery cannot create actor privileges from labels. |
| `submission` | `assignment: ref`, `candidate: ref`, `evidence: refs`, `limitations: text[]` | Assigned producer (author or integrator) returns an answer, bundle, or final-result candidate against the issued assignment/input closure; no claim of independent acceptance is implied. |
| `observation` | `assignment: ref`, `observation: ref`, `inputs: refs`, `material: blob_id[]` | Assigned measurement execution returns facts and exact supporting material. An observation does not grant sufficiency or review. |
| `review` | `assignment: ref`, `assessment: ref`, `subject: ref`, `criteria: ref`, `verdict: enum`, `findings: refs`, `conditions: refs` | Assigned independent reviewer delivers the exact recorded assessment. Verdict is `supported`, `supported_with_conditions`, `rework_required`, or `blocked`. Conditions must be profile-permitted; they cannot waive a required obligation. |
| `integration` | `assignment: ref`, `bundle: ref`, `answers: refs`, `integration_review: ref` | Integrator offers the exact assembled bundle and its independent integration review. The profile requires all six question answers or permitted explicit exclusions. |
| `handoff` | `assignment: ref`, `handoff: ref`, `bundle: ref`, `interface: ref`, `obligations: refs` | Owning setter/integrator delivers an exact handoff record offering a reviewed, integrated bundle under the pre-established interface. |
| `handoff_acceptance` | `assessment: ref`, `handoff: ref`, `interface: ref`, `verdict: enum`, `findings: refs` | Assigned receiver delivers its exact receiving assessment. Verdict is `accepted`, `information_required`, or `change_required`; it cannot substitute for professional review. |
| `information_request` | `assignment: ref`, `needed: refs`, `question: text`, `blocked_obligations: refs` | Assigned entity or dispatcher identifies missing authorized material. An empty `needed` array is allowed when a required source has not been identified; `question` must then describe the gap. |
| `information_response` | `request: message`, `provided: refs`, `remaining_gaps: text[]` | Entitled provider supplies exact material or explains unresolved gaps, routed through the owning setter/neighbor. New inputs do not silently alter an existing assignment. |
| `change_request` | `assignment: ref`, `subjects: refs`, `reason: text`, `findings: refs`, `proposals: refs` | Entity requests a change outside its authority. Proposals remain non-governing until an entitled owner decides. |
| `escalation` | `assignment: ref`, `package: ref`, `conflicts: refs`, `affected: refs`, `requested_decisions: text[]` | Layer integration owner aggregates conflicts and dependencies; submitting the package triggers the default pause policy. No finding is erased by summarization. |
| `decision` | Closed action-specific object in section 6 | An entitled owner, operator, controller, or human authority requests only the effects of the selected action. |
| `relay` | `original_message: message`, `original_origin: participant`, `route: ref` | Verified adjacent sender forwards an immutable original message under an authorized route. The outer sender is the immediate neighbor; original provenance and bytes are not rewritten. |

Each referenced semantic record has a type appropriate to the field; a structurally valid reference to a different kind is a semantic error. `record_type` is `source`, `profile`, `assignment`, `context`, `product`, or `assessment`, selecting the corresponding closed definition below. The `assignment` delivery message references an already-recorded assignment; `record_proposal` supplies its typed creation route. No source/assignment creation API is exempt from section 7.

Integration and handoff work use their own assignments. Their criteria/interface are fixed by the governing profile and owning setter before production. A receiver may ask for changes but cannot retroactively revise that interface. L1/L2 review/integration baselines precede substantive L3–L5 production. Early management questions may use explicit scoped consultation/relay assignments without pretending later architecture work is complete.

Registration and delivery are distinct semantic steps. Registration produces pending, non-governing content; it does not qualify a result or select a proof. For assigned executions, both steps are validated and committed atomically from the actual closed `RunReturn` under `run_completed` (section 3.2). Direct top-level leaf record/result messages are not an alternate authoritative return path. The existing message payloads remain the closed semantic intent vocabulary inside that return. Trusted non-leaf input/configuration operations still use their own independently authorized typed route.

Typed delivery must reference the exact returned records and match their content. Assignment delivery's owner, responsibility, criteria, and input references match its record; `inputs` is the distinct ordered locator projection of stored input bindings, retaining the first occurrence of each exact `VersionRef`. Observation delivery uses the same projection. The immutable record retains every named input occurrence and its scoped use selector; two uses of one immutable locator do not collapse into one governing dependency. Effects and limits come from the stored assignment and current verified grants. A changed verdict, subject, criteria, evidence, limitations, interface, or answers cannot override the returned record. Any semantic mismatch rejects the complete semantic return, without partial registration or delivery.

`submission` can deliver a pending bundle before its independent integration review. A later `integration` intent selects the already-delivered bundle and separately qualified integration assessment under a new entitled assignment; it cannot reopen the old run. A subsequent handoff likewise uses its own assignment. Physical run completion is distinct from assignment completion and positive review. An information/change request can end the invocation with no candidate while the assignment remains open and required inputs unresolved. Responding to resolved inputs requires a newly authorized context, and a new assignment version when its inputs/meaning changed, rather than leaving the provider invocation running indefinitely.

### 3.1 Closed control records and bootstrap

The wire record is proposed content, never a caller-supplied generic lifecycle manifest. The recorder adds verified engagement/scope/provenance, derives prerequisite bindings from the validated fields, and constructs the existing lifecycle manifest and version identity. Client-supplied arbitrary `kind`, `bindings`, `members`, state changes, proof roles, or transaction operations are not accepted. The deterministic record-to-manifest mapping cannot relax these contracts. Domain answer text may remain opaque material, but authority-critical fields cannot.

Every record includes `owner`. Assignment, product, and assessment records use an ownership coordinate. Sources may instead use an authority participant for L0/external-owned inputs; profiles use an entitled authority/controller participant. Contexts use their target assignment's ownership coordinate, or the controller participant for the bootstrap controller context. Record ownership never overrides type-specific creator rights: an assigned author cannot edit a dispatcher-owned context merely because it targets that author's work. L0-owned requirements must not be relabeled as L1-owned inputs when imported. The following are the remaining exact fields. A `binding` is `{slot_id: text, refs: refs}`; each declared slot occurs once. A `material` is a nonempty array of blob IDs whose bytes are authorized in the issued context. A `criterion` is `{id: text, requirement: ref, statement: text, evidence_slots: text[]}`; criterion IDs are unique and applicable requirements remain binding.

`criterion.evidence_slots` declares additional named prerequisites requiring separately qualified observation products. Use `[]` when the criterion is checked by inspecting the assigned candidate and its ordinary independent review. The answer slot, candidate reference, assessed-subject input and review/proof slots are not observation bindings. A supported review does not invent a missing observation or erase this owner-declared prerequisite.

| Record type | Closed content fields | Creation and type guards |
| --- | --- | --- |
| `source` | `source_role` (`input`, `criteria`, `policy`, `assumption`), `origin: participant`, `material: material`, `criteria: criterion[]`, `inherited: refs` | Entitled input/criteria owner; source provenance is verified, not self-certified by `origin`. A criteria source has nonempty criteria; other source kinds have an empty criteria array. A source record does not make its factual claims true. |
| `profile` | `profile_id: text`, `protocol` constant, `source_profiles: refs`, `content_profile: source-slot selector or null`, `obligations: obligation[]`, `max_clock_skew_ms: integer`, `max_request_duration_ms: positive integer`, `local_budget: {iteration_ms, max_reworks}`, `authority_policy_id: text`, `routing_policy_id: text`, `scheduling: {collection_window_ms, control_limits, max_search_steps, max_escalation_rounds, initial_deadline_ms}` | Entitled configuration owner/controller with independent authority. Local defaults are ten minutes per iteration and three semantic reworks, not separate rework/reformulation pools. The routing ID resolves the captured capability policy; the authority ID is checked against known L0 policy when a signed human act is used. Declaring an ID creates no additional rights. Source/content profiles have exact versions. |
| `assignment` | `responsibility: enum`, `assigned_actor: text`, `routing: {policy: ref}`, `use_scope: text`, `issued_under: ref or null`, `input_uses: prerequisite_use[]`, `profile: ref`, `inherited: refs`, `inputs: binding[]`, `criteria: ref`, `effects: effect_grant[]`, `limits: budget_limit[]`, `deadline_ms: integer or null` | The local entitled setter formulates its work. Empty aggregate limits and a null deadline mean no overall cap; invocation grants remain finite. The host can derive only the L1 or exact adjacent structural layer entry; it cannot supply domain answers or choose another layer's staff. The functional actor chooses professional execution separately. |
| `context` | `assignment: ref or null`, `profile: ref`, `purpose: enum`, `run_id: text`, `issued_to: text`, `execution: null or selection/work discriminator`, `inputs: binding[]`, `attachments: attachment[]`, `effects: effect_grant[]`, `expires_at_ms: integer`, `speculation: ref or null`, `ready_basis: text[]` | Trusted host only. Entity contexts require an explicit phase; work references one actual same-entity selection. Controller audit contexts use null assignment/execution. Fields alone grant no authority. |
| `product` | `product_kind` (`answer`, `observation`, `finding`, `bundle`, `handoff`, `escalation`, `final_result`), `assignment: ref`, `profile: ref`, `inputs: binding[]`, `material: material`, `evidence: refs`, `related: binding[]`, `limitations: text[]` | Actual verified assigned return; kind and related-slot meanings are profile-constrained. Required answers, observation inputs, bundle answers, handoff/interface, escalation conflicts/attempts, or final-result members cannot disappear through empty arrays. A finding is diagnostic, not an answer, proof, or permission. |
| `assessment` | `assessment_kind` (`professional`, `integration`, `receiving`), `assignment: ref`, `subject: ref`, `criteria: ref`, `profile: ref`, `assessed_closure: use_point[]`, `assessed_hash: digest`, `verdict: enum`, `findings: refs`, `conditions: refs` | Actual independent assigned return. Professional/integration verdicts use review values; receiving uses handoff-acceptance values. Recorder recomputes the scoped closure/hash and checks issuer/subject/criteria/independence before qualification. |

`product.evidence` and the matching semantic/submission field reference additional observation products that must be qualified before use. They do not contain request, criteria, assignment or other source citations. Ordinary document-derived answers use `[]`; the host already binds their input and criteria provenance. Citations to those sources may remain in the authored material. This meaning also applies to integration, measurement and finding products; a supported review does not turn a source citation into an observation.

An `obligation` has exactly `slot_id: text`, `owner: ownership`, `subject_kind` (`source`, `answer`, `observation`, `bundle`, `handoff`, `escalation`, `final_result`), `role` (`input`, `evidence`, `professional_review`, `integration_review`, `receiving_acceptance`, `human_acceptance`, `release_permission`, `answer`, `management_activity`), `required_kind` (`source`, `product`, `assessment`, `decision`), `minimum: positive integer`, `maximum: positive integer`, `allow_exclusion: boolean`, and `exclusion_owner: participant or null`. Require `minimum <= maximum`, unique slot IDs, compatible kind/role, and an entitled exclusion owner when exclusions are permitted. Materializing a profile must account for all six question obligations at each included layer; a caller cannot weaken its required closure by supplying fewer references. Omitted obligations are missing, not automatically excluded.

An `effect_grant` has exactly `operation` (`read`, `propose`, `materialize`, or `measure`), `owner: ownership`, `targets: refs`, `destination_handle: text or null`, and `tool_policy: ref or null`. Read grants require nonempty targets; materialization requires a broker-resolved destination and exact content; measurement requires a qualified tool policy. A propose grant covers only the assigned owned record types/operations under the governing profile, not an arbitrary manifest or another owner. These requests require verified authority and effective runtime containment.

Initialization is a finite trusted-control operation, not a self-authorizing leaf message. Before it, host configuration independently identifies the controller, authority/trust policy, permitted engagement/scope, and attributable L0 ingress. A `bootstrap` request has null context/profile, an empty-ledger expected head, a closed profile and nonempty L0 source records. In that payload, `profile_record` is exactly `{logical_id: text, record: profile}` and each `source_record` is exactly `{logical_id: text, record: source}`; duplicate logical IDs are forbidden. Verify actual controller/L0 provenance and approved policy IDs independently of those fields. Atomically register the profile and L0 inputs and derive one bounded controller context referencing them; no author/reviewer result or acceptance is created. Its created context reference is returned in the commit receipt. If the trust anchor, authorized inputs, or policy is unavailable, bootstrap fails closed. Repeating it follows normal committed-request idempotency; a different initialization against an existing engagement is forbidden.

The required `use_scopes` is a nonempty unique finite list including the bootstrap envelope scope. The sole runtime records this exact operator-supplied engagement scope at bootstrap. Ordinary later messages cannot enlarge it; neither a role label nor a local read creates a new semantic scope. Bootstrap registers each source/profile immutable origin record once and establishes distinct initial source/profile use points in those preauthorized scopes. Integrity/origin qualification of these primitive inputs grants no derived review, acceptance, or release. Each scope initially selects the same exact L0 manifest independently. A later source transition in one scope affects another only through its actual scoped dependencies. After bootstrap no operation enrolls a new independent scope: work requiring one starts a new explicitly authorized engagement. This finite boundary avoids both a general activation privilege and a second scope-recovery workflow.

The controller context permits only authorized recording/delivery of initial setter assignments, not semantic authorship. Subsequent assignments and contexts are created through the closed record contracts under existing issued authority. No actor can register its own context, profile, or actor identity to gain powers. Profile revisions and L0 changes require their actual entitled provenance and cancel affected applicability through the usual transition rules.

### 3.2 Bounded host controls and actual execution returns

Context creation does not establish that execution has started. A provider need not remain running during subsequent semantic registration or review. The closed `control_event` type records actual execution and accounting facts under runtime authority.

`control_event` has exactly `event` and the fields for that discriminator:

| `event` | Remaining exact fields | Guard and effect |
| --- | --- | --- |
| `renew_control` | `previous_context: ref`, `profile_use: use_point` | The recorded engagement controller, existing governed engagement, qualified permitted profile use and current head. Envelope context is null; its profile reference equals `profile_use.ref`. Recompute a finite target-scope controller context from current protected policy and qualified sources. An explicitly granted cross-scope profile reference may support that context; renewal creates no semantic input uses or mandate. Record that exact profile-use prerequisite. Previous context is navigation, not an expired grant; renewal resets no budget or semantic rights. |
| `run_started` | `run_context: ref`, `run_id: text`, `observed_at_ms: integer` | Fresh controller context; exact issued run/owner with valid reservation. Record actual start before invocation: `issued → running`. Context creation alone remains `issued`. |
| `run_completed` | `run_context: ref`, `run_id: text`, `observed_at_ms: integer`, `return_blob_id: digest or null`, `usage: usage_total[]` | Fresh controller context; actual matching physical completion. Valid current return is consumed atomically as specified below; paused/expired/replaced/cancelled work cannot gain semantic authority. Null return means no admissible semantic result. |
| `run_cancelled` | `run_context: ref`, `run_id: text`, `observed_at_ms: integer`, `reason: text`, `usage: usage_total[]` | Host-confirmed pre-start stop or actual cancellation for the exact issued/running run. Record `cancelled` and reconcile complete known usage; do not invent a provider acknowledgement. |
| `usage_audit` | `run_context: ref`, `run_id: text`, `observed_at_ms: integer`, `usage: usage_total[]` | Independently measured cumulative usage for that exact known run, including terminal runs. Apply monotonic increments only; no result, assignment, selection, or permission is created/reopened. |

The envelope sender/recipient are the engagement controller recorded by the sole trusted runtime. Workers cannot call this outer writer API; they return only the captured RunReturn for their issued context. Renewal derives a current finite controller context from the exact profile and permitted scope. It does not use a signing credential, reset budgets or preserve revoked semantic rights.

Control-plane provenance comes from the actual local runtime and exact issued context. A historical controller context supplies audit identity/profile/scope; its obsolete business inputs or expired execution lease do not disable authorized staging, owner-directed transition, or reconstruction. Pending storage is not source acceptance. Human-reserved decisions still require their separate exact human proof, and current entity execution still checks the issued assignment's own input applicability, lease, and budget. This separation permits a valid owner decision to repair a blocked basis without accepting an output or bypassing verification.

A `usage_total` has exactly `metric` (`tokens`, `cost_minor_units`, or `elapsed_ms`), `unit: text`, and `total` (nonnegative safe integer). Pairs `(metric, unit)` are unique and must match issued policy units. Completion/cancellation supplies every reserved metric/unit; otherwise no qualification or reservation release occurs. Progressive `usage_audit` may contain a nonempty subset. Runtime-captured observations, not LLM estimates, establish totals. Apply only `new_total - recorded_total`, reject decreases, and retain overrun incidents honestly. Repeated completion under another request ID cannot spend a reservation twice. Observation time must not precede actual start and must not exceed the runtime assessment clock plus permitted skew; pre-start cancellation uses the issued instant as its lower bound.

A `RunReturn` is an immutable canonical JSON artifact with exactly `assignment: ref`, `context: ref`, `records: record_proposal_payload[]`, and nonempty `intents: return_intent[]`. A proposal has the existing exact `logical_id`, `record_type`, and typed `record` fields. A return intent has exactly `message_type`, `recipient: participant`, and the corresponding existing closed `payload`. There are no transport heads, message/request IDs, arbitrary operations, generic manifests, signatures, or future completion references in this artifact. A pure deterministic identity-preview helper may calculate proposed record IDs without storing them or granting authority. References inside the package name existing versions or earlier topologically ordered package records; forward/cyclic references are forbidden.

| Issued responsibility | Allowed proposed records | Allowed return intents |
| --- | --- | --- |
| `setter` | Local owned `source_role: criteria` and profile-authorized child assignments, including only the adjacent receiving routes in section 3.3; a handoff product only for an assigned handoff work item. Inherited requirements remain unchanged. | Child `assignment` delivery; owned `decision` limited to `rework`, `reformulate`, `select`, `invalidate`, or policy-limited `terminate`; `handoff`; common information/change intents. |
| `author` | Owned answer products. | `submission`; common information/change intents. |
| `reviewer` | Professional assessment and its owned finding products. | `review`; common information/change intents. |
| `integration_reviewer` | Integration assessment and its owned finding products. | `review`; common information/change intents. |
| `integrator` | Owned bundle, handoff, escalation, or final-result products. | `submission`, `integration`, `handoff`, or `escalation`; common information/change intents. |
| `receiver` | Receiving assessment and its owned finding products. | `handoff_acceptance`; common information/change intents. |
| `measurement` | Owned observation products. | `observation`; common information/change intents. |

Common intents are `information_request`, `information_response`, and `change_request`, only under the issued task and routing rights. All records belong to the issued work owner except explicitly authorized setter-owned child assignments. No leaf return can create profiles, contexts, controller authority, external/L0 input or policy sources, or human acceptance/release. Local setter criteria are the sole source-record case above; that does not permit foreign-source modification. Reserved `continue`, `accept`, `release`, human-owned reformulation/reinstatement, and operator speculation approval remain separate exact human/host authority routes; an outer controller completion cannot confer those rights.

The final intent is the producing run's terminal response. An actual setter work
return may prefix permitted local assignment or decision intents; each runs in
order through the same shadow-state authority checks and the complete return is
atomic. No prefix completes another producer or authorizes a reserved human act.
Other work responsibilities return exactly one intent. The selection phase
always has exactly one self-assignment choice and no records. "Terminal" ends
this invocation; it does not force an answer or a positive review.

| Terminal intent | Assignment and governing result |
| --- | --- |
| `information_request` or `change_request`, with no candidate required | Run returns and usage is accounted. Assignment remains open with required information/owner decision unresolved; no candidate is qualified. New work needs an entitled new context and, for changed assignment inputs, a new assignment version. |
| `information_response` | Complete the specifically assigned response task only when its delivery obligations hold; otherwise retain its unresolved required gaps. It cannot complete another actor's question. |
| `submission`, `observation`, `assignment`, owned `decision`, or `handoff` | Complete this invocation and, for a non-setter producer, its task when the exact delivery obligations hold. A setter's logical mandate remains open within its original bounds. A pending candidate, delivered child assignment, observation, or handoff is not a positive independent review or release grant. |
| `review` or `handoff_acceptance` | Complete that assessment task with its actual verdict. `blocked`, negative, or information-required verdicts do not qualify the subject. |
| `integration` | Complete only the assigned integration/publication task when the already-existing independent proof and all required slots qualify. |
| `escalation` | Atomically apply the layer/dependent pause. An explicitly assigned escalation-preparation task may finish, but ordinary affected work remains paused; no completion ordering may resume it. |

A setter's logical task may span several finite runs and remains open after its handoff is accepted and the next setter is issued. This permits later ordinary clarification or rework within its original authority without artificial L0 restoration. Fresh contexts require an open eligible mandate, current head, applicable local allowance and any explicitly imposed aggregate limits. A terminal run cannot return again. The existing explicit entitled termination action can end the logical mandate. An absent overall deadline never creates an unbounded execution grant or reopens a completed/cancelled task.

A finding uses the existing product fields with `product_kind: finding`, material/evidence, and exactly two related bindings: `subject` with the reviewed subject reference and `criterion:ID` with the exact criteria-source reference containing that criterion ID. Only the assigned reviewer, integration reviewer, or receiver may create it. It may support its assessment's findings list but cannot govern an answer slot, act as a review proof, or grant acceptance. Its validity checks origin/material/subject/criterion integrity; it does not recursively require independent review of every finding. Disputes use the existing owner/escalation route.

For a valid current `run_completed`, the shared authoritative validator verifies exact canonical artifact bytes and original issued assignment/context; validates every closed record and intent under the original producer's rights; derives pending registrations; validates all typed semantic intents; and commits their effects, actual usage, assignment outcome from the table above, and `running → returned` atomically. The broker may construct transport metadata and copy deterministic payload projections, but cannot patch semantic record/intent fields. No intermediate state is visible. No additional raw return validator or direct leaf-ingest bypass exists. Another completion request for that terminal run fails `P_STATE`; an exact committed retry remains a historical acknowledgement after current visibility checks.

Actual late completion for paused, expired, replaced, or cancelled work commits only explicitly typed quarantine/accounting effects. A cancelled run remains cancelled; late material is linked as audit, not a reopened run. The response is `committed` for that audited control operation and its receipt/effects identify the lack of semantic qualification; it is not a rejected request that secretly mutated state. An invalid current package instead rejects the entire semantic completion without ledger mutation or partial record creation. Its real cost must then be recorded through a separately recorded `usage_audit`; rejected semantics cannot erase spend. Reservation is retained until a valid complete host completion/cancellation accounts for it. There is no implicit repair, timestamp rewrite, or automatic acceptance of quarantined content.

### 3.3 Scoped applicability and exact reuse

This predeployment clarification preserves the immutable lifecycle's scoped-applicability invariant. Record origin and current use are different coordinates. Store predicates, basis/proof selections, dependency edges, traversal/visited sets, and impact roots by use point. A version-ID-only cache or invalidation set is insufficient.

The immutable assignment is the use mandate; there is no separate mandate store or public `activate_use` action. Its `use_scope` is the explicitly authorized target work scope, which may differ from its version reference's origin namespace. Its `issued_under` names the exact actual issuing setter assignment, or is null only for the initial L1 route below. Contexts and messages operate in the assignment's target scope; changing an origin reference's scope is never a way to move work.

An assignment's `input_uses` is an array of closed selectors `{at: text, use_scope: text}`. Each `at` is a JSON Pointer to one existing typed causal version-reference occurrence in that assignment, excluding `issued_under`. Reject duplicates, unknown paths, scalar targets, navigation-only references, and caller-defined relationship types. Unselected occurrences resolve in the assignment's target `use_scope`. The `issued_under` prerequisite resolves in the issuing assignment's own `use_scope`, independently of its origin namespace. The recorder derives all scoped reliance edges and includes their exact endpoints in validated effects. Fixed assessment use points are never rewritten.

Only the actual entitled setter's returned content may issue ordinary child assignments. `issued_under` must equal that verified producer's assignment reference. Same-layer issuance retains the exact authorized work item and target scope. An ordinary question setter issues only its own question's author/reviewer work; an explicitly profile-entitled integration or handoff coordinator may issue the layer's question setters, which then issue their own authors and reviewers. It cannot bypass them by assigning another question's author or reviewer directly. Measurement work uses the profile's closed same-layer subject rule. Normalize the parent's governing inherited/input references to exact reference/use-point pairs; every such obligation must remain represented in the child, irrespective of array order or local slot names. Reject omission, predecessor substitution under the same logical identity, or changed inherited use bindings. A setter may add compatible owned local criteria and inputs; it cannot reinterpret incoming obligations. Authors and reviewers cannot issue their own replacement mandates.

The controller's sole semantic entry-assignment route is L1, with null `issued_under`, an owner explicitly required by the current profile, and the exact current attributable L0 source manifest as inherited inputs. Initially that manifest comes from bootstrap; later versions can become current only through the exact signed owner-authorized source transition. Its criteria must be an exact current attributable L0 criteria source; absent or ambiguous criteria block initialization of that task. Entry issuance is unique for the scope, owner, and exact governing source manifest. A new signed source manifest permits a fresh pending entry assignment without restoring the cancelled predecessor or its proofs. Reissuing an unchanged cancelled mandate, including under a different logical label, is forbidden. Protected routing/effect/budget rules constrain execution but cannot supply domain meaning. A controller cannot mint an arbitrary-layer baseline or change the manifest by choosing a convenient subset.

Explicit source/root reinstatement is not lease renewal or resource replenishment. It cannot reopen a terminal physical run, extend an explicitly imposed mandate/global deadline, or reset aggregate usage. A governing resource-input change follows its existing entitled transition; a label, new request or repeated source selection is not a substitute. Local operational time extension is separate: the operator may add time to an exact paused unit under the recorded policy, affecting future fresh grants only. It changes neither the immutable profile, semantic criteria nor acceptance. Restoration of a product whose inputs and execution requirements still hold remains separate: fresh applicable review and an explicit reinstatement decision restore only that product's use, without reviving cancelled acceptances or release permissions.

Source reinstatement requires its actual human owner's exact signed `reinstate` decision, intact material, and already restored prerequisites; its `fresh_proofs` is empty because a substitute professional review cannot manufacture L0 ownership. It restores the specified source use, not a different source selection. An exact human root-restoration decision may establish the latest terminal root's semantic applicability without reopening that old task. One successor root may consume that decision reference through the reserved input binding `root_reinstatement`, containing exactly that one reference. The current full L0 manifest, profile, owner and scope still identify the same generation; any explicitly recorded aggregate stop and usage remain binding, and local time is not silently renewed. A copied receipt or a new logical label cannot authorize another successor. Revoking an establishing applicability grant cancels the affected current uses and their dependent permissions; history and unrelated uses remain intact.

Cross-layer work addresses the receiving layer as a whole. After an actual
offered handoff exists, the host derives its deterministic local receiving entry
with exact `incoming_handoff` and `incoming_interface` bindings. After actual
qualified selected acceptance, it may derive the local coordinating setter with
`incoming_acceptance`. Both preserve the exact scoped interface and relevant L0
axioms. Local broker capabilities come from global L0 availability and actual
local ownership, not the upstream profession/tool template. The receiving layer
formulates its own questions, roles and method. The upper layer cannot issue its
authors/reviewers or substitute staffing fields in the host-derived gateway.
Receiving inspection does not depend on its future acceptance, and the host
does not infer domain questions or verdicts from opaque prose.

Registration of an authorized assignment atomically derives pending uses only for its exact named prerequisites and their typed dependency closure. Protected directional access and issued context visibility are additionally required, but do not authorize semantic use by themselves. A visible historical record is not a governing input. Controller renewal can refer to an existing qualified profile use; it creates no new semantic use. Cross-engagement use remains unsupported until an explicit profile defines it.

Existing cancelled or invalidated use points cannot be reset by registration, a replacement assignment, or another scope label. The issuing mandate lineage is derived from immutable `issued_under` links. A cancelled lineage cannot authorize a fresh target scope; its entitled upstream owner must explicitly reconcile the cancellation and satisfy reinstatement requirements. A qualified point cannot silently acquire different prerequisite bindings. The actual owner changes governing inputs through a new exact assignment/handoff and atomic cancellation of affected uses; lower layers receive that manifest and may request changes, not select which old conditions to retain.

New uses start pending, inapplicable, insufficient, and unreviewed. Registration copies no review, acceptance, permission, execution lease, or human grant. Unchanged evidence is reusable only where type-specific qualification demonstrates its required current closure. A reused assessment must cover the exact subject use, criteria/profile, authority, and scoped closure; otherwise fresh review is required. An imported assignment/context record is historical data, not a new execution credential. Semantic cancellation of an issuing mandate propagates through reliance; its completed run or expired execution lease does not itself revoke the committed mandate.

For example, two upstream-authorized assignments may name the same immutable version A in independent `use-a` and `use-b` contexts. Superseding A only in `use-a` cancels that point and its actual dependents while an independently qualified `use-b` point survives. If the second assignment instead explicitly selects A in `use-a` through `input_uses`, its result depends on that point and cancellation propagates. No additional generic governing-use edge is needed. Creating a different version ID for A would not demonstrate this invariant. Corrupt bytes or forged origin block every use relying on them; independent scope is not an integrity bypass.

Selection scope is the message's target use scope. Basis slots are keyed by that scope and the declared owner/slot; proof slots by that scope, exact subject version, role, and slot. A proof lookup is not a reverse causal edge. Scope-aware impact follows only actual resolved reliance and proof dependencies; no global invalidation merely because a version has another obsolete use.

Qualification of a candidate precedes governing selection. Human acceptance and release additionally require that exact output to occupy every required output-basis slot for its owner and product kind in the governing profile. A superseded output can remain a truthful, qualified historical result while ceasing to be an authorized governing input. Explicitly assigned historical inspection remains possible; it cannot turn inspection into current applicability. An entitled owner may explicitly select a historical result again only while its verification requirements still hold, and cancelled acceptance or release never revives through that selection.

An entitled setter may select an actual negative review in the same required proof slot. It governs the disposition of that exact subject and blocks qualification with its recorded review verdict; it is not supporting PASS evidence. Replacing a slot retires its predecessor for that slot and permanently cancels acceptances and release permissions relying on the changed justification. A later positive assessment requires an explicit selection and new acceptance/release; neither an old PASS nor a restored closure revives those cancelled permissions. Current-basis responses derive `review_dispositions` from the selected assessments, including negative verdicts, while `proofs` contains supporting assessments only. No independent mutable disposition flag or newer-record rule exists.

Assessment closure arrays and their hashes contain full use points. Current-basis response closure, evidence, proofs, establishing/cancelling decisions, and conflicts also carry use points; selected entries include their `use_scope`. Commit receipts add `affected_uses: use_point[]` while `created_versions` remains origin references. Effect digests bind scoped state/selection/dependency changes, and human acceptance/permission closure hashes include those points. These are amendments to the exact response definitions below, not optional display labels.

All reference/material arrays may be empty structurally unless explicitly nonempty above. Semantic obligations enforce their required slots/cardinalities. `subjects`, `replacements`, `conflicts`, `requested_decisions`, speculative `assignments`/`limits`, and an accepted final result's required members must be nonempty. Optional information requests may name an unidentified gap rather than invent a reference.

## 4. Canonicalization, identity, retries, and time

Parse raw JSON with the existing strict lifecycle JSON rules before schema validation: reject duplicate object members, duplicate keys after NFC normalization, floats including lexical `1.0`, non-finite constants, and unsupported values. Recursively NFC-normalize strings and keys; preserve string whitespace and array order. Canonical bytes are compact UTF-8 JSON with sorted keys and no ASCII escaping. A generic parser that discards duplicates or turns `1.0` into an integer cannot establish this rule.

Reuse `jai.lifecycle.version.v2\0` for semantic version manifests and `jai.lifecycle.blob.v2\0` for exact blob bytes. Version and blob IDs are unprefixed lowercase SHA-256 hex. Do not invent new identities for the same semantic records. Protocol message IDs are:

```text
sha256(UTF8("jai.delivery.message.v1\0") +
       canonical(envelope with only message_id removed)).hexdigest()
```

The escaped `\0` denotes one NUL byte. No transport attestation or signature field is included in the closed message envelope, so no proof or self-reference is silently excluded from hashing. A different context, recipient, payload, timestamp, or expected head creates a different message ID. A message ID establishes content identity, not correctness or origin.

The recorder processes a request in this order:

1. Use the sole local writer and actual runtime-issued context. Reject a direct outer assignment sender; worker identity comes from its captured run. Perform strict parsing, schema and identity validation, controller/scope checks, and actual-context agreement. Only an explicit L0 decision requires an external signature; bootstrap and `renew_control` require no internal proof.
2. Look up a committed request by recorded origin, engagement, scope, and `request_id`. Exact stored message identity returns its original immutable receipt without reapplying effects. Different content or original trust binding is an idempotency conflict. Entity packets remain purpose-specific; local operator receipt queries require no signing proof.
3. For a new request, verify expiry, allowed clock skew, assignment/run status, exact issued context/profile, current grants, permitted route, and `expected_head`. Use the trusted assessment clock; sender time never chooses the assessment instant.
4. Derive and validate the new transition once: semantic kinds, ownership, prerequisites, review independence, budgets and exact effects. Compare the serialized row canonically with those validated values, check the same head under the existing writer lock and persist atomically. No internal signing preview or second derivation is performed. Cold reconstruction separately rederives historical effects.

An exact committed retry is a historical acknowledgement, not a new current grant. It may return after the original expiry/head changed only after step 1; current applicability is queried separately. A rejected, uncommitted request grants nothing. A corrected submission uses a new `request_id` and message identity, preserving references to any earlier attempt where available.

Every request has a finite deadline. The governing policy sets allowed future-clock skew and per-operation limits; absent required time policy is an error. Signed operator wrappers keep their own timestamp representation and canonical signature bytes, referenced as exact blobs rather than embedded and reserialized here.

## 5. Minimal state dimensions and transitions

State belongs to exact scoped versions. Do not encode every combination in one large status enum or infer a status from timestamps. Typed records and qualified proofs determine effective state.

| Subject | State dimension | Allowed transition and guard |
| --- | --- | --- |
| Assignment | `open`, `paused`, `completed`, `cancelled` | Owner creates `open`; valid escalation pauses affected assignments; authorized resolution resumes against exact contexts or creates replacements; completed/cancelled assignments cannot accept new governing author results. |
| Execution run | `issued`, `running`, `returned`, `quarantined`, `cancelled` | Dispatcher issues one exact context/effect lease; completion is bound to it. Paused/replaced/expired work cannot become a governing return; its actual completion/cost may be quarantined. |
| Semantic version | Existing scoped validity/applicability/sufficiency predicates | New result starts pending, inapplicable, insufficient, and unreviewed. Qualification requires type-specific evidence and selected proofs. Explicit invalidation cancels affected applicability; history remains immutable. |
| Review | Immutable verdict plus selected-proof applicability | Independent origin, exact subject/criteria/context, issuer entitlement, and evidence must qualify. A stored verdict alone is insufficient. Replacement of a subject cancels its affected proofs. |
| Layer bundle | Exact selected answer/exclusion versions plus integration proof | Six question obligations and cross-question consistency must hold. An integration proof references the already-existing bundle; proof selection is not a reverse causal dependency. |
| Handoff | Exact offer plus receiving decision | Receiver decision references an existing offer/interface. Final eligibility selects that decision; the offer never depends causally on its own future acceptance. |
| Escalation | `open`, `resolved`, `terminated` | Opening applies pause atomically. Entitled owner resolution records decisions; closure requires reconciliation and no unresolved required conflict. Termination is an explicit allowed decision. |
| Acceptance/permission | Exact subject/closure/policy and qualified proof | Local support, integration, receiving acceptance, human acceptance, and release permission are separate predicates. Closure changes cancel affected applicability; no automatic reinstatement. |

The finite execution/assignment/escalation transition matrices are:

| Subject: from | Event → to | Required guard |
| --- | --- | --- |
| Assignment: absent | Authorized typed creation → `open` | Owner, profile, criteria, input slots, permitted effects, and finite limits qualify. |
| Assignment: `open` | Scoped escalation → `paused` | Atomically include the affected layer and dependent closure. |
| Assignment: `open` | Assigned deliverable recorded → `completed` | Exact issued return meets the assignment's delivery conditions; this does not imply independent review or acceptance. |
| Producing assignment: `paused` | Valid grant-bound speculative deliverable recorded → `completed` | Original execution is preserved; result holds remain until complete impact reconciliation. Coordinating setters retain their continuing-task semantics. |
| Assignment: `open` or `paused` | Owner cancellation/replacement/termination → `cancelled` | Entitled exact decision; cancel affected current use. |
| Assignment: `paused` | Authorized reconciled resume → `open` | Exact current owner impact and governing basis permit retention; issue fresh normal contexts afterward. Otherwise cancel/reissue the affected work. |
| Run: absent | Authorized dispatch reservation → `issued` | Open assignment or valid bounded speculation, exact context, available enforced allowance. |
| Run: `issued` | Actual execution start → `running` | Dispatcher records start before invocation; context, deadline, rights, and reservation remain valid. |
| Run: `issued` | Pre-start cancellation → `cancelled` | Dispatcher/owner stop, pause, or expiry; release unused reservation and account actual known cost. |
| Run: `running` | Verified `run_completed` with a current valid `RunReturn` → `returned` | Actual matching bytes, current eligible assignment/context, complete cost reconciliation, and atomic typed return consumption. Registration itself does not qualify the candidate. |
| Run: `running` | Verified stale/paused/replaced completion → `quarantined` | Dispatcher records audit/material and usage only; no governing selection. |
| Run: `running` | Confirmed cancellation → `cancelled` | Stop acknowledged and actual usage reconciled; no automatic result. |
| Escalation: absent | Authorized aggregate recording → `open` | Retain individual conflicts/attempts, apply pause atomically. |
| Escalation: `open` | Owner decisions plus reconciliation → `resolved` | Every required conflict is addressed and applicable replacement/input decisions identified. |
| Escalation: `open` | Entitled termination → `terminated` | Exact scope/assignment authority; no infeasibility claim inferred. |

Other transitions are forbidden. Completed/cancelled assignments and returned/quarantined/cancelled runs are terminal for that version/run. New work needs a new version/run. A late physical completion after a terminal cancellation creates only a linked dispatcher audit/accounting event; it does not reopen the cancelled run or duplicate spend. Resolved/terminated escalations remain historical; a later conflict creates a new escalation.

Candidate registration, assessment, proof selection, and governing selection follow this acyclic order:

1. Record a candidate as pending and non-governing. Its required input/evidence/profile closure must be assessable; the candidate need not already be selected or independently reviewed.
2. Record and qualify an actual assessment of that exact pending candidate. Qualification checks its inputs, issuer, independence, criteria, and recomputed closure, excluding the assessment it is currently establishing. It does not require the subject's future review proof or selection.
3. Select the qualified proof for its exact subject/role slot. This can qualify the candidate's local-review predicate.
4. Select the now-qualified candidate as the current basis for its owned slot. Integration, handoff, and final-result qualification repeat this pattern with their required proof roles.

Neither review nor qualification may require its own future acceptance. A pending subject can be independently assessed before selection. Missing current evidence remains blocking; removing a circular prerequisite is not permission to skip it.

A negative review creates findings and permits owner-directed rework, not arbitrary semantic edits. Rework creates a new candidate/assignment revision preserving governing meaning. Reformulation creates a new owned requirement/assignment version and cancels affected use; inherited meaning can change only through its owner's adjacent route. Budget exhaustion produces blocked/search-exhausted outcome, never support or demonstrated nonexistence.

Every causal reference points to an existing immutable version. Review→subject is causal; subject→selected-review is a lookup, not another causal edge. Receiving-decision→handoff is causal; final-result selection requires both without changing the old offer. Future candidates are proposals until recorded and qualified. Reject a candidate that introduces a scoped causal cycle.

## 6. Closed decision actions

Every decision payload has `action` and `reason: text` plus exactly the fields below. There is no free-form effect map or manifest list. Referenced replacement records must already have verified origin of their own; a decision cannot manufacture them.

| `action` | Additional required fields | Entitlement and effect guard |
| --- | --- | --- |
| `rework` | `assignment: ref`, `replacement: ref`, `findings: refs` | Owned setter decision; replacement preserves inherited requirements and required evidence. Create pending work, never accept its result. |
| `reformulate` | `subject: ref`, `replacement: ref`, `authority_proof: blob_id or null` | Exact semantic owner changes owned meaning. L0-reserved changes require actual entitled L0 provenance and any mandatory signed proof; a null proof cannot waive that requirement. |
| `select` | `slot: selection_slot`, `candidate: ref`, `previous: ref or null` | Entitled selector chooses one compatible qualified basis/proof; slot role derives from the qualified record and profile, not a caller label. Competing unresolved candidates cannot both govern the same slot. |
| `continue` | `replacements: replacement[]`, `verification_path: ref`, `authority_proof: blob_id` | Verified continuation capability permits exact source transitions, atomic cancellation, and fresh verification. It cannot create another owner's derived answer, observation, or review proof. |
| `exclude_content` | `content_policy: ref`, `obligations: text[]`, `authority_proof: blob_id` | Signed L0 `delivery-change` names exact obligations in the current content policy. A subsequent explicitly selected policy in the same governed slot may cite that decision for unchanged requirement identities only. The approval remains subject to scope, expiry and revocation; it grants no review, acceptance or release. |
| `speculate` | `escalation: ref`, `assignments: refs`, `inputs: use_point[]`, `limits: budget_limit[]`, `expires_at_ms`, `authority_proof: blob_id` | Exact external L0 authorization permits only named work within current inputs, finite shared bounds and expiry. No result acceptance, ownership expansion or release follows. |
| `resolve_escalation` | `escalation: ref`, `package: ref`, `conflicts: refs`, `impacts`, `decisions: refs`, `authority_proof: blob_id or null` | Actual owner covers the exact revision/conflicts and classifies scoped impact as unchanged, changed or unknown. Relay is adjacent; a no-change resolution need not invent a cancellation. Reserved L0 responses require actual human proof. |
| `resume` | `escalation: ref`, `resolutions: refs`, `reconciliation: reconciliation[]` | Entitled resolution and dispatcher policy reconcile every affected result/context; no unconditional restart or acceptance. |
| `invalidate` | `subjects: refs` | Entitled owner/integrity authority cancels the scoped affected dependency/proof closure atomically; no silent alternative selection. |
| `reinstate` | `subjects: refs`, `fresh_proofs: refs`, `authority_proof: blob_id or null` | Explicit entitled decision plus current type-specific evidence. Cancelled proofs/acceptance are not revived from history. |
| `accept` | `subject: ref`, `closure_hash: digest`, `authority_proof: blob_id` | Exact-output human acceptance capability; the exact output must be selected in all required output-basis slots, and local/integration/receiving proofs plus the current closure must already qualify. |
| `release` | `subject: ref`, `acceptance: ref`, `closure_hash: digest`, `authority_proof: blob_id` | Exact release entitlement for the currently selected output, with current acceptance/permission rules. A read-only eligibility result does not execute release. |
| `terminate` | `subjects: refs`, `authority_proof: blob_id or null` | Entitled scope termination, or the policy-limited termination of an owned assignment; it is not evidence that no solution exists. |

`replacement` has exactly `previous: ref` and `replacement: ref`. `budget_limit`
has exactly `metric`, positive safe-integer `ceiling`, and `unit`. The current
native speculative adapter enforces `elapsed_ms` with unit `ms`; unsupported token
or currency ceilings are rejected. `reconciliation` has exactly `subject: ref`,
`outcome` (`retain`, `reverify`, `rework`, or `discard`), `basis: use_point[]` and
`impact: ref` identifying the owner's exact resolution. It has no preissued fresh
context requirement. Names alone do not establish unchanged current meaning.

A `selection_slot` is exactly `{kind: "basis", owner: ownership, slot_id: text}` or `{kind: "proof", subject: ref, role: enum, slot_id: text}`. Proof role is `professional_review`, `integration_review`, `receiving_acceptance`, `human_acceptance`, or `release_permission`. Slot IDs must exist in the governing profile. Basis identity is engagement/scope plus owner and slot ID; proof identity is exact subject reference plus role and slot ID. The qualified assessment/decision kind and assigned authority must entail that role. A caller cannot attach a professional review to an integration/acceptance slot. Selection may be initiated only by a profile-entitled owner/selector or the controller applying that actor's actual qualified result. The controller cannot choose a semantic result on its own.

The runtime requires one selector with `minimum = maximum = 1` for each owner, subject kind, and selector role. It rejects nonsingleton selector quorums and duplicate selectors. Input and evidence bindings retain their declared array cardinalities. The reserved protocol obligation role `management_activity` is rejected by profile validation. This restriction concerns that obligation role; management activity definitions, measures, and observations in the SABSA content profile have their own content contract. A rejected obligation cannot be silently omitted or treated as satisfied.

Decision types do not replace the existing external authority protocol. The actual capability and signature verification determine whether an authority proof permits the particular effects. An authentic receipt approving continuation cannot qualify `accept`, `release`, a foreign-owner reformulation, or a synthetic reviewer verdict.

## 7. Uniform semantic validation and dependency effects

Apply these guards to ordinary CLI/API recording, message ingestion, typed source/assignment creation, lifecycle plan/apply, proof selection, replay, eligibility, and convenience commands. An alternate path must not relax them:

- Resolve exact referenced kinds/versions and verify declared inputs and owner rights for engagement, scope, layer, question/work kind, and work item.
- Bind the returned content to its trusted dispatch and issued context; reject substituted origin, candidate, criteria, or effects.
- Keep professional review in the author's layer with a distinct assigned execution; integration review and receiving acceptance have their own entitlements. Check the exact assessed prerequisite closure and profile; layerless/wrong-issuer proofs cannot qualify through generic lifecycle selection.
- Preserve immediate-neighbor communication. A relay's outer runtime-recorded sender is separate from original producer provenance. Validate the route against the original message, inherited confidentiality, and permitted receiver; do not treat relay possession as authorship or broad access.
- Require all selected proof roles and declared obligations conjunctively. A missing required slot, conflicting selected basis, unresolved contradiction, or stale proof blocks qualification. No timestamp/new-hash selection and no predecessor fallback.
- Compute scoped dependency impact, including selected proofs and evidence dependencies. Atomically cancel affected answers, local/integration reviews, handoff acceptance, human acceptance, and permissions while preserving unrelated closures.
- Preserve signature/trust/capability, expiry/replay, exclusive-lock expected-head, candidate replay, raw-byte consistency, and atomic replace/fsync protections. Invalid candidates cannot expose partially applied effects.

Provenance/navigation links are not all causal reliance. Preserve that distinction when computing impact and rejecting cycles. The read-only current-basis query takes an exact output version and scope and returns selected input/profile versions, required closure, supporting evidence/proofs, establishing/cancelling decisions, unresolved conflicts, and separate qualification/acceptance/release reasons. It never chooses a fallback or grants a permission.

## 8. Pause, speculation, and late execution

Opening an escalation atomically pauses the affected layer and dependent work; budget exceptions must be explicit speculation decisions. Pause stops new substantive dispatch, requests cancellation of in-flight runs, and invalidates their right to produce a governing result against a superseded context. Work required to preserve state and decide the escalation remains policy-scoped.

Before speculative dispatch, reserve its maximum permitted spend against every applicable shared ceiling: `spent + outstanding_reservations + proposed_reservation <= ceiling`. Reserve atomically under the governing policy/head. Unknown impact remains speculative. No metering or enforceable stopping boundary means no speculative authorization for that metric. Token/cost unit definitions and pricing versions are fixed in the policy; a caller cannot change units to evade a cap.

On `run_completed` or confirmed `run_cancelled`, reconcile complete runtime-measured usage for every reserved metric/unit and release only unused reservation. Progressive `usage_audit` records monotonic increments without inventing a completion. Concurrent or late events cannot reuse the same reservation. A run without a known enforceable bound is not dispatched under a hard cap. Unavoidable completion after cancellation remains accounted for; it does not become a qualified answer. An overrun is a budget/control incident that pauses affected work, not permission to hide cost or accept the result.

The closed `control_event` route in section 3.2 is the only completion/cancellation/usage path. A stale run return can produce committed quarantine/accounting effects only; a semantically rejected current package cannot secretly mutate state and its actual costs require a separate runtime-recorded usage event. A quarantined result can be used only after an entitled reconciliation and ordinary current-input verification/review, never by changing its original timestamp or assignment reference.

## 9. Error contract and conformance boundary

Errors identify `code`, `message_id` when identifiable, `request_id` when safe to disclose, and public-safe details. Do not expose hidden attachments, another scope's receipt, private paths, or authority secrets. Error responses are not authorizations and do not themselves create governing records.

| Code | Meaning and effect |
| --- | --- |
| `P_PARSE` | Invalid raw JSON, duplicate/NFC-colliding keys, float/constant, or unsupported lexical value; no consequential mutation. |
| `P_SCHEMA` | Unsupported protocol, unknown field/type/action, invalid structural shape; no consequential mutation. |
| `P_IDENTITY` | Message/content/attachment identity mismatch; no consequential mutation. |
| `P_ORIGIN` | Unverified or mismatched actor/run/authority; no receipt disclosure or consequential mutation. |
| `P_CONTEXT` | Wrong, stale, undeclared, or unavailable required context/profile/material; request corrected inputs through the authorized route. |
| `P_SCOPE` | Wrong ownership, assignment, access, adjacency, or effect rights; no consequential mutation. |
| `P_IDEMPOTENCY` | A committed request key is reused with different content or trust binding; no reapplication. |
| `P_EXPIRED` | New request outside its trusted time policy; no governing effect. |
| `P_HEAD` | Expected head changed; no partial application; obtain a new assessed context/request where needed. |
| `P_STATE` | Paused/completed/replaced assignment, illegal transition, or unmet prerequisite; no governing effect. |
| `P_PROOF` | Missing, revoked, wrong-subject/issuer/closure, insufficient, or unauthorized proof; no qualification. |
| `P_BUDGET` | Missing/unenforceable allowance or exhausted shared reservation; no dispatch/grant. |
| `P_CONFLICT` | Contradictory selected state, unresolved obligation, or causal cycle; no candidate commit. |
| `P_INTEGRITY` | Corrupt history, forged proof, or inconsistent persisted bytes; fail closed and preserve evidence. |

When several checks could fail, report the first safe failure in the section 4 processing order; do not reveal protected content to explain a denied request. A public-safe list of additional independently established issues may accompany it. Receipt status distinguishes `committed`, `already_committed`, and `rejected`; quarantined dispatcher completion is a different typed operation, not an implicit fourth success state for the rejected sender request.

### 9.1 Exact response and query records

A processing response is exactly `{status, receipt, error}`. `status` is `committed`, `already_committed`, or `rejected`. The first two require a non-null immutable commit receipt and null error; rejection requires null receipt and a non-null error. For `already_committed`, the receipt is the exact original committed receipt, not a new grant or a newly calculated head.

A **commit receipt** has exactly `protocol` (the protocol constant), `message_id`, `request_id`, `origin_binding` (identity digest of the recorded origin/context/assignment basis, not a signature), `assessed_at_ms`, `before_head`, `after_head`, `transaction_id` (nonempty string), `created_versions: refs`, `affected_uses: use_point[]`, and `effect_digest` (digest of canonical exact validated transaction operations before persistence). Heads and digests are 64 lowercase hex; time is a safe nonnegative integer. The transaction records complete typed operations, scoped point changes, and original authority proofs; a summary receipt cannot conceal or widen approved effects. Retrieving a receipt is an ordinary local query; worker packet visibility remains governed separately. A record-only registration returns created versions without selecting them. A fresh governing-effect operation must pass current eligibility again.

An **error record** has exactly `code` (the section 9 enum), `message: text`, `message_id: digest or null`, `request_id: text or null`, and `field: text or null`. `field` is a public-safe schema/property pointer, not a hidden source locator. Unknown IDs remain null; inaccessible request details are not echoed.

A **current-basis request** is a read-only object with exactly `protocol`, `subject: ref`, and `assessment_scope: text`. It assesses the point `(assessment_scope, subject.version_id)` while preserving the subject's origin reference. This is an ordinary trusted-workspace query, not a worker browsing endpoint or a signed read request; entity visibility remains enforced by its issued packet and broker. The response has exactly `protocol`, `subject: ref`, `assessment_scope: text`, `assessed_at_ms`, `head: digest`, `selected: selection[]`, `closure: use_point[]`, `evidence: use_point[]`, `proofs: use_point[]`, `review_dispositions: review_disposition[]`, `established_by: use_point[]`, `cancelled_by: use_point[]`, `conflicts: use_point[]`, and `eligibility`. A `review_disposition` is exactly `{subject: use_point, assessment: use_point, verdict: enum}`, using the existing professional/integration or receiving verdicts. A `selection` is exactly `{use_scope: text, slot: selection_slot, version: ref}`. `eligibility` has exactly `qualified`, `accepted`, `release_eligible` (booleans) and `reasons` (objects with exactly `code` and public-safe `message`). Results are assessments at the returned head/time, not grants; changed inputs/policy require reassessment. No selected fallback is invented when a required slot has no current basis.

## 10. Schema reference

The repository contract package is `.ai/runtime/protocol/governed-delivery/v1/`.
Its schemas use JSON Schema Draft 2020-12 and local references:

| Schema | Contract surface |
| --- | --- |
| `common.schema.json` | Shared references, ownership, attachments, and bounded values. |
| `record.schema.json` | Source, profile, assignment, context, product, and assessment records. |
| `decision.schema.json` | Closed decision actions. |
| `message.schema.json` | Transport envelopes and typed payloads. |
| `response.schema.json` | Commit receipts and errors. |
| `query.schema.json` | Current-basis requests and responses. |
| `control.schema.json` | Runtime control events. |
| `run-return.schema.json` | Atomic assigned returns and semantic intents. |

Structural validity establishes only the declared shape. It does not establish
source truth, professional sufficiency, independent execution, authority,
effective confinement, acceptance, or release permission. Those conditions
remain separate obligations at their respective processing boundaries.
