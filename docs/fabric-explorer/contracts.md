# Fabric Explorer model and consumer contracts

Owner: Fabric Explorer API maintainers. Contract version: `1`.
This reference defines the maintained model and consumer protocol.

This specification governs the renderer-independent TypeScript package
`@jai/fabric-explorer-contracts`. Consumers are the desktop broker/preload,
recorded-source adapter, graph/query workers and read-only UI. The package
validates transport and projection structure. It does not replay journals,
verify signatures, assess a product or grant authority. Maintained
[source contracts](source-contract.md), [architecture](architecture.md) and
[resource limits](qualification.md) remain authoritative for those boundaries.

## Identity and provenance

Project and root IDs are opaque stable namespaces assigned by the local broker.
They are not a path, display name, session ID or root capability. Re-admission
of the same project/root must preserve these namespaces; moving a selected path
does not authorize merging unrelated projects. The broker owns that persistent
association. Source `engagement`, origin `scope`, `logical_id`, `version_id`
and `use_scope` remain exact strings. Only `version_id` has the source digest
shape; only `use_scope` inherits the canonical 128-character key bound. Do not
normalize findings text or truncate identity fields.

Source IDs are stable application-assigned identifiers, not canonical ledger
names. They must be distinct within an admitted capability/catalog and snapshot
because import/paging address a source by that ID. Ambiguous catalogs are
rejected, never merged or silently rebound. Project/root/source provenance
still preserves its complete namespace. Finding `ledgerId` similarly identifies
the stable ledger namespace, not merely its filename/display label.

An `ElementIdentity` is a closed discriminated union:

| Kind | Exact identity fields beyond `projectId` | Maintained basis |
| --- | --- | --- |
| `version` | `ref` with engagement, scope, logical_id, version_id | Canonical immutable reference |
| `use` | `ref`, `useScope` | Canonical origin reference plus applicability use point |
| `finding` | `ledgerId`, `findingId` | Findings ID is ledger-local |
| `blob` | `rootId`, `blobId` | Material namespace plus canonical digest |
| `participant` | `participant` authority/controller ID or assignment reference | Canonical participant definition; not a permission |
| `ownership` | `owner` layer/work_kind/question/work_item tuple | Canonical ownership descriptor; not an enterprise identity claim |
| `location` | stable `origin` locator subset, `text` | Unresolved textual location; never resolved by label similarity |

Identity keys encode tagged tuples using JSON string-array encoding. Their
purpose is injective local addressing, not canonical lifecycle hashing. Keys
never include labels, current generation, source head, absolute paths or session
capabilities. A missing exact version/use is represented by an `unresolved`
vertex with the same target identity/key; resolving it later preserves its key.
Textual unresolved locations use the separate `location` identity.
Their stable origin subset is project/root/source/family, relative file locator,
record pointer and optional record sequence. It deliberately excludes source
revision, observation time and adapter version; ordinary append refresh therefore
does not replace an unchanged textual-location identity.

Each source locator carries project/root/source namespace, source family
(`fabric`, `findings`, `audit`), relative file locator, JSON pointer, optional
sequence, exact source revision and adapter version. Relative locators reject
absolute paths, traversal, empty components, backslashes and NUL; they do not
authorize filesystem access. The broker independently resolves them within an
admitted capability. JSON pointers follow RFC 6901 escaping. Source revisions
record byte length/digest, optional ledger head/sequence and observation time;
they describe an observed revision set, not an atomic cross-ledger commit.

An edge identity is either `explicit` (project namespace, exact immutable origin
element identity, explicit source edge ID and exact endpoint identities) or
`occurrence` (project namespace, origin identity, originating JSON pointer,
occurrence and exact endpoint identities). The origin contains its version/use
point when applicable; reusing a source edge ID in another version or use point
cannot rebind an overlay. Explicit source IDs take precedence when available.
Endpoint pairs alone are insufficient. Reordering source occurrences can change
occurrence keys; later annotation reconciliation must expose that limitation.
An `OverlayTarget` contains only a versioned stable element/edge identity; no
note content, colour state, persistence operation or source mutation is defined.

## Semantic payloads and model values

`SemanticValue` uses an unambiguous tagged tree: `null`, `boolean`, `string`,
`integer`, `float64`, `array` and `object`. Integer values are canonical decimal strings;
object values are ordered `{key,value}` entries, not a JavaScript property bag.
All values are tagged, so a source object resembling an integer tag remains a
source object. Duplicate exact object keys are rejected. Producer-side lifecycle NFC rules are not reverified by the viewer; recorded
strings and keys are not silently normalized. Lifecycle mode accepts safe JS integers or `bigint` and
rejects floats/nonfinite/unsafe numeric inputs. Findings mode preserves float64
values, including signed zero and nonfinite values, as exactly 16 lowercase
hexadecimal digits in big-endian IEEE-754 byte order. Its JS convenience encoder
treats every `number` as float64 and requires `bigint` for source integers: JS
cannot recover Python integer `1` versus float `1.0` after ordinary parsing.
The recorded-source helper must tag numbers before crossing that boundary; this
encoder is not a source parser. Audit/lifecycle attributes use lifecycle numeric
rules; only findings-source attributes admit float64. Decoding uses `bigint`
for integers, number for explicitly admitted float64 and null-prototype objects.

The source-semantic nesting limit is 64. Tagged wrappers are representation
overhead and do not reduce that logical limit. Wire preflight separately bounds
physical JSON nesting at 256, sufficient for 64 tagged source levels and the
closed administrative envelope. The 8 MiB frame limit applies before parsing.
This is not a change to the 64-level source JSON limit or 100 MiB decoded-record
limit; large source records must use paging rather than a larger IPC frame.

Vertices carry identity/key, label, provenance and `attributes`: either inline
tagged full fields or an explicit source-paging descriptor with byte length and
media type. Queries can therefore project a valid large source record without
forcing it into an 8 MiB frame. Complete fields remain available through details
and bounded source pages; no silent field dropping is permitted. Version vertices retain the six maintained record
families source/profile/assignment/context/product/assessment and derived decision.
Finding attributes preserve target, location, event actors/notes/times, rounds,
recorded expiry and reducer state; the six states are open/resolved/verified/
stuck/withdrawn/accepted. An accepted finding is not automatically expired or
permission-granting. Blob availability and verification are independent facts.
Labels are plain display text; they are neither HTML nor persistent keys.

Verification explicitly separates decoded structure, chain integrity, canonical
replay, public-trust availability, material availability and recorded
applicability. Diagnostic mode cannot claim successful canonical replay or
derived applicability. The viewer always records `authorityGranted:false` and
`freshAssessment:false`. A timestamped saved audit is recorded evidence, not a
current decision. Shape validation never establishes the truth of these claims;
legacy verified observations can be retained as historical metadata. Current
recorded-mode sources use unknown chain/trust and recorded replay; validators
reject attempts to turn those observations into verified claims.

`SnapshotDescriptor` records generation, observed source revisions, counts and
verification. `GraphProjection` separately contains bounded visible vertices and
edges, hidden counts, completeness and omission reasons. There is no requirement
to transfer the full graph into the UI. Endpoints must be represented, including
unresolved targets; duplicate IDs and inconsistent identity keys are rejected.
No renderer, layout coordinates or annotation persistence enters semantic DTOs.

## Relationship direction

The package exports a frozen relation-direction registry. Each edge keeps its
class, exact originating field and recorded derivation basis. The viewer projects
recorded causal membership and scope-specific dependency structure; the DTO
validator does not authenticate those source claims.

| Class | Display arrow | Causal treatment |
| --- | --- | --- |
| causal-dependency | dependency use → consuming use | Requires canonical-dependency basis |
| input-binding | input → consumer | Causal only with canonical-dependency basis |
| profile / criteria / inheritance / assignment | prerequisite → containing record | Causal only with canonical-dependency basis |
| assessed-subject | subject use → assessment | Association unless canonical classification says otherwise |
| material-attachment | record → blob | Noncausal |
| participant / ownership | record → descriptor | Noncausal |
| decision-effect | decision → affected use | Recorded effect, not inferred causal flow |
| finding-subject | finding → exact subject | Exact-reference basis; textual locations excluded |
| location-association | finding/record → unresolved location | Noncausal |
| other-reference | referencing record → referenced record | Noncausal; a helper-classified dependency instead uses its causal class and direction |

Association cycles are allowed. Traversal explicitly selects relation classes
and causal membership; a connected graph never proves validity or authority.

## Read-only consumer protocol

Every frame uses protocol `jai.fabric-explorer.consumer/1`, request ID and
`binding:{sessionId,capability,generation}`. Session IDs/capabilities are opaque
broker handles; generations are unsigned decimal strings, never JS numbers.
Root admission has null capability/generation. Before initial import generation
may be null; queries/refresh require an existing generation. The receiver checks
binding against its own expected session/capability/current generation. Structural
validation alone cannot authenticate a capability.

| Operation | Request payload | Successful result |
| --- | --- | --- |
| `roots.pick` | selected source families; no paths | opaque capability and admitted source/root descriptors from native picker |
| `roots.close` | empty | closed acknowledgement |
| `snapshot.import` | selected admitted source IDs | new snapshot descriptor |
| `snapshot.refresh` | empty | replacement snapshot descriptor |
| `request.cancel` | target request ID | accepted/not-active acknowledgement, not proof of quiescence |
| `element.lookup` | exact element identity | vertex or not-found |
| `search.page` | text, typed filters, page limit and optional cursor | bounded vertices, hidden/completion counts and next cursor |
| `graph.counts` | typed filters | lossless vertex/edge/finding counts |
| `graph.neighbours` | identity, direction, relation classes, bounded work/result limits | graph projection with completeness/omissions |
| `graph.path` | endpoint identities, direction, relation classes and bounded work limits | projection plus found/complete; incomplete cannot assert absence |
| `element.details` | exact identity | inline semantic attributes or source-paging descriptor |
| `source.page` | admitted source ID, record pointer/sequence, byte offset/length | exact base64 byte page with length and EOF |

Responses echo the request binding. Import/refresh return a candidate generation
inside their snapshot payload, never silently rewrite the request binding. An
in-flight response can publish only if its original session/capability/generation
still matches current state. Cancellation binds its target to that same context;
it cannot cancel itself or a request from another session/root/generation.
Picker families form an allowed-family set: every admitted source must belong
to that set, without requiring a source from each family. Import success must
capture every explicitly selected source ID. Additional already-admitted
dependency revisions may be included; actual admission remains broker-owned.

Search, neighbour and path results may use `response-chunk` frames instead of a
single response. Exact identities can make a legitimate default 8,000-edge view
larger than one frame. Each chunk binds request ID, operation, session/capability/
generation and a contiguous zero-based decimal sequence. Nonterminal chunks
contain at least one vertex/edge; search chunks have no edges. Cumulative counts
cannot exceed the requested limit or 5,000/20,000 visible bounds. Terminal
metadata carries source snapshot/completeness/omissions (and path-found state)
or search cursor/counts. No chunk may follow a terminal. An incomplete path
cannot assert absence. The pure transition validator checks these rules; actual
staging/assembly remains owned by the query consumer. It validates the complete
projection, unique identities and endpoint/source-revision consistency before
publication. An individual edge chunk may reference a vertex in another chunk.
Neither a chunk nor its successful receipt publishes a partial snapshot.

Cursors bind session, capability, generation, operation-specific query key,
offset and opaque broker token. Query keys encode only closed viewer-query
values and are not source hashes. The receiver recomputes the key and validates
the server-owned token; changing query text/filter/order or generation invalidates
the cursor. No pagination token authorizes a filesystem path.

All envelopes and discriminated payloads are closed. Unknown versions,
operations, fields and mutation/approval/note commands are rejected. Source
attributes and explicitly namespaced `extensions` hold opaque tagged values;
they are never dynamic methods or authority flags. Failure replies carry typed
error codes and bounded diagnostics. Invalid unbound input can produce a
separate typed rejection notice; it cannot impersonate a bound successful reply.
Administrative JSON numbers use safe plain decimal integer lexemes, without
fraction/exponent/negative-zero spellings. Source numeric values use the tagged
semantic representation, so findings float64 and large integers remain intact.

## Limits, compatibility and tests

The package fixes 8 MiB UTF-8 frames, 256 KiB raw pages, 1,000 visible diagnostics,
5,000/20,000 maximum visible vertices/edges and 10,000 visited vertices / 50,000
scanned edges / 32 hops. Default visible limits remain 2,000/8,000. A limit-bound
answer identifies omitted counts/reasons. It cannot silently become complete or
claim no path. Helper concurrency two and worker concurrency eight are declared
contract limits; queue and process ownership belongs to the runtime implementation.

Protocol/model version changes require explicit compatibility review. Unknown
wrapper fields fail closed; unknown legitimate source attributes remain inside
their tagged payload. The recorded-source adapter rejects unsupported journal
formats; this package validates DTO structure rather than parsing sources. No automatic migration, mutation,
source lock, network access or user-installed runtime is introduced.

Synthetic goldens must identify themselves as projection/transport examples,
not admitted history. Contract tests cover all maintained family descriptors,
same label/different identity, cross-project/ledger namespaces, versions/use
points, parallel edges, unresolved targets, arbitrary-precision integers,
source normalization differences, closed/versioned schemas, bounds, stale
sessions/generations/cursors and cancellation targets. They prove structural and
binding contracts only; filesystem denial, recorded projection parity and
desktop/GPU behaviour remain the responsibility of their owning integration tests.
