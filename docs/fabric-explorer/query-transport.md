# Accepted snapshot queries and layout transport

The desktop viewer builds its query index once when an imported candidate is
sealed. The accepted worker owns one compact graph with shared identity/value
dictionaries, search metadata and forward/reverse adjacency. The query index
borrows this storage; it does not retain another expanded graph. Queries do not reopen selected
files or replay canonical history. A refresh creates an independent candidate;
failed refreshes preserve the previous accepted graph and capture.

The sandboxed preload exposes named lookup, details, search, counts,
neighbours, path, grouping and layout methods. Every native handler authenticates
the current main frame, session and document before calling the controller.
Requests retain their exact session, source capability and accepted generation.
Main and preload reject stale replies before publication. No method accepts a
native pathname, executable project content or a caller-supplied layout graph.

Search and projection results use the maintained consumer response-chunk
contract. Each logical frame is at most 2 MiB in UTF8, inside the physical 8 MiB
contract limit. A consumer stages at most 1 GiB of wire data and enforces the
request's cumulative vertex/edge limits, contiguous sequence, terminal metadata
and final response correlation. A record is never split or silently truncated.
If one complete record or scalar reply cannot fit the logical frame, the query
fails explicitly with a resource-limit error. Existing paged attributes retain
their exact captured source locator; raw source pages remain independently
bounded to 256 KiB.

Pull jobs retain numeric selections and terminal metadata. The worker checks
record sizes before reconstruction and expands only the records admitted to
the current physical frame. Returned records are detached from stored data;
changing a result cannot change a later query or the accepted graph.

The worker retains at most eight unfinished pull jobs and eight visible
projections. Opaque continuation tokens are consumed once. Projection tokens
select already bounded numeric vertex/edge handles in the accepted worker;
handles are stable only within that generation and never replace canonical
source identities. The consumer must release its projection when replacing or
closing that view. Source closure and successful generation replacement release
the old worker and all its ephemeral state.

Main creates a four-byte shared atomic cancellation flag for accepted-worker
query and layout calls. Cancellation changes that flag rather than terminating
the worker, so unrelated queries and the accepted snapshot remain available.
Candidate import cancellation can still terminate its separate disposable
worker. Layouts operate only on retained visible projections. Layout positions
and SCC membership are navigation aids, not canonical facts or business
approval. Fractional coordinates cross the private channel as exact big-endian
IEEE754 bit strings and are restored as finite numbers by preload; source
semantic integers and float domains remain unchanged.

The application has no graph editing, note persistence, lifecycle decisions or
source writer. Layout and query state are disposable; reverting this viewer
increment requires no source-data migration.
