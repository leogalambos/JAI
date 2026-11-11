# Public workflow reference showcase

This example visualizes the maintained **Idea to production** and **Vulnerability to remediation** workflow definitions. Its 42 source records preserve the actual stage order, accountable role, activity, handover and gate, with public Markdown paths, line numbers and content digests. Nineteen shared role-reference records connect the stages that quote them; Software Engineer and Change Manager each occur in both workflows.

The data is a reference map of documentation. It does **not** claim that either workflow ran, that a review passed or that a production change or risk was approved. There are no findings or assessment/decision records. The canonical source owner identifies the public documentation maintainers for attribution only. Source inheritance represents published stage ordering and quoted role dependencies, not observed execution or a newly granted authority. A shared role is one documentation reference, not a live assignment to a person.

From the repository root, use a Python environment with the project's maintained runtime dependencies:

```sh
python3 -I -B apps/fabric-explorer/examples/public_workflows.py /absolute/path/to/new-showcase
```

The destination must be new or empty. The generator reads only the public stage tables in [Idea to production](../../../docs/workflow-library/idea-to-production.md) and [Vulnerability to remediation](../../../docs/workflow-library/vulnerability-to-remediation.md). Immutable material is stored through the canonical Store API; the journal is created by the maintained Fabric `submit` CLI. There is no manual journal construction or fallback writer. `showcase.json` records public provenance, and the capture request/receipt make the operation reproducible.

Open the generated project in Fabric Explorer with **fabric** selected as the source family. In **Search → Filters**, choose the **inheritance** relation. Search for `Role · Software Engineer`, choose its use point, then use **Explore selected neighbourhood** with **Both directions**, **4 hops** and **Causal only**. The resulting 22-vertex, 22-relation view has nine branch points with at least three distinct neighbours. It connects both workflows through shared role references while leaving unrelated profile/input-binding provenance out of the illustration. The complete reference is larger than that bounded view. Inspect a relation to see its exact direction and provenance. The viewer's raw source/material fields retain the original source observations.

The example tests cover exact public-stage and shared-role extraction, safe output rejection, canonical writer creation and an actual TypeScript-worker import/query with unchanged source bytes. The query requires a bounded view spanning both workflows with multiple real branch points rather than a simple chain. They do not establish screenshot legibility, native accessibility or workflow execution. Regenerate into a fresh directory when a maintained workflow table changes. Remove only the generated destination to discard the example; no application or source schema is changed.
