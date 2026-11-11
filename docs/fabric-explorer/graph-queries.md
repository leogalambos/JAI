# Indexed graph queries

The accepted snapshot owns its graph and query index inside the application
worker. Queries use existing [read-only contracts](contracts.md), retain exact
record identities, and do not reopen source files or assess current authority.
Positions and layout direction never change semantic edge arrows.

The index shares the worker's sealed compact graph, canonical-ID ordering and
separate forward/reverse adjacency. It scans scalar columns and reconstructs
complete records only for bounded output. Parallel edges keep distinct edge IDs. A self-loop
is considered once during a bidirectional traversal. Worker-local numeric
handles address this exact generation only; they are not persisted annotation
addresses or replacements for stable element identities.

## Search, filters and groups

Search matches literal case-insensitive substrings of the displayed label or
exact identity address. It does not rewrite original strings or source hashes.
Identity order is exact key order; label order is case-folded label followed by
exact key, independent of platform locale and input record order.

Empty filter arrays mean all. Project selectors apply to every vertex. Family
selectors constrain version/use vertices, with a use inheriting its exact
version's family; an unresolved version/use with unknown family cannot match a
nonempty family selector. Other vertex kinds pass the family dimension. Finding
states constrain findings only, preserving the surrounding fabric context.
Active dimensions combine with AND.

A nonempty relation filter in search/counts requires an eligible incident edge.
The edge must match the selected relation and project, and both endpoints must
pass the base vertex selectors. Empty relation filters keep isolated vertices.
Traversal requests use the existing contract's nonempty relation list; the
application supplies all registered relations explicitly for an unfiltered
traversal.

Search pagination reports `hidden` as the number of matching results remaining
**after the current page**, excluding earlier pages and nonmatches. `complete`
means the terminal page. Opaque cursors authenticate the exact inspectable
query key, offset, session, capability and generation with a private per-index
secret. Changing case in the query may match the same records but changes its
query key; an earlier cursor cannot be reused for that changed query. Cursors
can be replayed within their immutable generation and expire with that worker
index. There is no accumulating cursor registry.

Internal groups count project, vertex kind, known record family or finding
state. Grouping does not merge vertices or edges. Internal edges, cross-group
edges and edges touching ungrouped vertices are reported separately; family
and finding-state groups therefore do not pretend to partition nonapplicable
vertex kinds. Group addresses are injective tagged tuples, not semantic hashes.

## Traversal and bounded visibility

Forward traversal follows `Edge.from` to `Edge.to`; reverse follows the opposite
search direction while retaining original arrows in the result. Bidirectional
search considers both. Causal-only traversal uses the stored canonical causal
flag, including its historical/governing evidence; it never infers causality
from labels or layout positions.

| Budget | Default | Maximum |
| --- | ---: | ---: |
| Visible vertices | 2,000 | 5,000 |
| Visible edges | 8,000 | 20,000 |
| Visited vertices | 10,000 | 10,000 |
| Distinct considered edges | 50,000 | 50,000 |
| Hops | 32 | 32 |

Visited work is separate from visible capacity. Every distinct considered edge
is charged **before** relation/causal predicates, so a filtered high-degree hub
cannot bypass the scan limit. Cycles are bounded by visited/edge tracking.
Explicit zero-edge and zero-hop requests remain valid. Already represented
endpoints may retain a self-loop at zero hops; an unseen eligible endpoint past
the hop bound produces an incomplete work-limited result.

Neighbour projections describe the selected reachable component. `complete`
requires exploration and representation without work, visible, unresolved or
unavailable omissions. Intentional focus, disconnected records and excluded
relations may produce only `filter` omissions and remain query-complete.

Path search returns one deterministic breadth-first observed path, retaining
the chosen original parallel edge. `found: false` is returned only after proving
absence in the indexed observed selection, with an empty complete filtered path
projection. A bounded search without that proof returns `found: null` and an
incomplete explored frontier. A discovered path may have `found: true` with an
incomplete projection if its visible budget cannot display the full path.
Unresolved records remain explicit uncertainty, not claims of source validity.
A represented identity has a zero-length path to itself.

Projection `hiddenVertices` and `hiddenEdges` are exact **global snapshot totals
minus returned records**. They are not invented counts of undiscovered reachable
records. Every returned edge has represented endpoints. Original complete
attributes remain available; transport splits bounded results into physical
frames rather than silently dropping inspector fields.

## Cancellation and generation lifetime

Main owns an atomic cancellation flag observed inside accepted-worker query
loops and numeric sorting checkpoints. Cancelling a query does not terminate
the accepted graph worker or invalidate its archive. Index construction occurs
once in the separately cancellable candidate worker. Publication and stale
response rejection remain bound to the exact accepted generation.

The index is bounded by the accepted import model (100,000 vertices and 500,000
edges). Search/filter/group scans reuse immutable metadata and a single cached
filter view. Adjacency queries inspect only their bounded reachable work; they
do not copy or rescan the entire graph's semantic records for each query. These
bounds are not a claim of constant memory or platform/GPU qualification.
