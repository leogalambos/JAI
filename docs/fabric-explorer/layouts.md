# Visible graph layouts

Layouts consume an already bounded visible projection. They do not read source journals, expand a query, lay out the entire imported snapshot on selection, or change semantic records. Positions are ephemeral layout-space coordinates. The query index retains every original edge, including parallel relations and self-loops; layout never reverses arrows or replaces their source identities.

The worker uses generation-local numeric vertex and edge handles instead of copying long source identifiers and inspector fields. Each request/result binds the exact session, source capability, generation, request and projection. Handles and SCC group numbers have meaning only with that binding. A result from another projection or generation cannot be reused as current geometry.

## Algorithms

`layered` is the default. Iterative strongly connected component detection handles cycles without recursive stack growth. Only the derived condensation graph is ranked as a DAG. Four deterministic barycentric sweeps organize the layers. Cyclic components use a local ring with enough spacing for their members; disconnected components are packed into rows instead of one long column. Original vertices and relations remain available for inspection.

SCC groups are explicitly derived layout summaries. They contain sorted member handles, a cycle flag and exact counts of original internal, incoming and outgoing edges. Parallel edges count separately. A singleton with a self-loop is cyclic. Group numbers are projection-local ordinals; they do not assert enterprise ownership, source identity or authority, and they are separate from query-domain groups.

`force` is an explicit alternative for mixed association views. A seeded grid gives disconnected vertices a finite starting area. Each iteration processes every original edge for attraction and uses a spatial grid with at most 24 neighbor samples per vertex for approximate repulsion. A fixed cooling schedule and bounded movement avoid unbounded all-pairs computation. This is a navigation layout rather than a claim of optimal geometry or collision-free labels.

Both modes sort numeric handles before seeded work. The same projection, seed and configuration produce the same positions in the same maintained runtime regardless of input enumeration order or scheduler timing. Changing a seed can change tie-breaking, cyclic orientation and force positions. Renderer label placement and camera behavior are separate concerns.

## Configuration and limits

| Setting | Default | Allowed range |
| --- | --- | --- |
| Algorithm | `layered` | `layered`, `force` |
| Seed | `1` | Unsigned 32-bit integer |
| Force iterations | `60` | `1`–`200`; layered mode uses four sweeps |
| Node spacing | `48` units | Finite `8`–`256` |
| Layer spacing | `160` units | Finite `8`–`1024` |
| Charged work | `20,000,000` operations | Integer `1`–`50,000,000` |

The visible ceiling is 5,000 vertices and 20,000 edges. Normal query defaults remain 2,000 vertices and 8,000 edges. Compact layout input and result are independently limited to 2 MiB. Excess counts, bytes, invalid handles, missing endpoints, duplicate identities, nonfinite configuration or exhausted work produce an explicit error. No incomplete position set is labelled complete.

Work charges cover graph traversal, ordering, ranking and force evaluations. Cooperative checkpoints yield after 2,048 charged operations using the worker event loop. Cancellation can use an AbortSignal or the owning worker's atomic cancellation predicate. Iteration/work stopping rules are deterministic; wall-clock scheduling does not decide which coordinates become final. No per-frame layout result stream or unbounded work queue is introduced.

The result reports the selected algorithm, completed iteration count and charged work. Coordinates must be finite and remain within the fixed layout-space bound. The caller must compare the entire active binding before adopting them. Cancellation or failure returns no geometry and does not replace the accepted semantic snapshot.

## Development verification

Application-only tests cover cycles, DAG ranks, parallel/self relations, disconnected packing, input immutability, seed/order/scheduler determinism, visible ceilings, work limits and controlled cancellation. Generated small-graph cases compare SCC membership against an independent reachability oracle. Worker integration separately verifies the actual cancellation and stale-result boundary.

Engine performance smoke uses bounded synthetic projections and records seed, algorithm, iterations, work and elapsed time. These measurements do not rerun or establish browser/GPU qualification and do not replace finished-product performance testing. The layout engine adds no source-mutation API or persistent styling; graph rendering belongs to the canvas.

With the pinned local Node/npm toolchain and installed locked dependencies,
run `npm --prefix apps/fabric-explorer/desktop run build:native-smoke` and then
`npm --prefix apps/fabric-explorer/desktop run test:graph-smoke` from the repository
root. The finite smoke uses synthetic S (1,000/3,000) and M (25,000/100,000)
vertex/edge models, measures default-budget queries and layered layouts, and
checks query/layout cancellation. It prints JSON with runtime/hardware, work,
durations and whole Node-process RSS. That RSS includes the synthetic corpus
and runtime; it is not the graph-only Chromium memory increment. The smoke
artifact belongs only to the development build and is excluded by a normal build.

Layout changes require no source or preference migration. Rollback restores the previous compiled viewer/application increment; cached positions and group handles are disposable and must be recalculated for a new projection. Do not modify source journals or stable element identities to preserve old geometry.
