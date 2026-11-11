# Disposable renderer projection probe

This experiment compares frozen Sigma/Graphology and Cytoscape candidates. It is
not application code and must not be promoted into the product without a
separate engineering decision. It reads no project ledgers and grants no
qualification or authority.

The corpus is a deterministic synthetic directed multigraph projection, seed
20261109. S/M/L contain 1,000/25,000/100,000 vertices and
3,000/100,000/500,000 relations. Findings are dimensional metadata only. No
canonical fabric import, raw input byte-size, real findings reduction or helper
memory is represented by this projection benchmark. The first relations preserve
parallel edges, a self-loop and a reverse association. Initial visible limits are
2,000/8,000, expanded limits 5,000/20,000; hidden counts remain reported.

Use the pinned build Node/npm from the parent dependency baseline. Install with
lifecycle scripts disabled, inspect the exact lock, then build:

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run check:corpus
npm run check:output
npm run check:manual
npm run check:runner
npm run check:controls
npm run check:animation
npm run check:geometry
npm run check:sigma-style
npm run check:projection
npm run check:worker
npm run check:phases
npm run check:memory
npm run check:lifecycle
npm run build
npm run probe -- --output=/tmp/fabric-explorer-renderer-observations --browser=/usr/bin/chromium-browser --size=M --scales=1,1.5,2
```

The browser must already exist on the native observation host. The runner
requests Chromium sandboxing and does not add `--no-sandbox`; a sandbox denial
is a failed launch, not a reason to weaken the acceptance environment. The
runner uses direct Playwright pipe transport, injects its own compiled IIFE/CSS
into an empty page and runs a compiled inline worker. It creates no HTTP server,
WebSocket listener or external fetch; page network routes are denied. It produces
screenshot/raw JSON under the explicit scratch/private destination and shuts down
its children. `out/` and the repository root `build/` are ignored local convenience
destinations. Other paths inside the checkout, including sibling public module
paths and symlink aliases to them, are rejected. Results must not be committed as
public evidence.

Run S/M/L separately. The same seed/topology and 20-second active pan/zoom
script apply to both candidates. Results include all frame samples, nearest-rank
p95, long tasks, peak summed process-tree RSS where available, selected-element
metadata, expansion, cancellation and context-loss observations. No failed or
slow sample is dropped. Windows RSS sampling is not implemented and is reported
unavailable rather than passing. The process tree includes the runner
and browser, and excludes a canonical reader/helper; it cannot prove product
memory budgets.

For an operator-observed run on a native desktop, enable the explicit manual
mode (a visible desktop is required; terminal JSON input is not used):

```sh
npm run probe -- --output=/tmp/fabric-explorer-renderer-manual --browser=/usr/bin/chromium-browser --size=M --scales=1,1.5,2 --manual=true
```

The default plan is finite: **six cases**, two renderers at three display scales,
with **eight numbered stages each (48 steps total)**. Terminal and browser both
show the current case, stage and overall step. Dense graphs belong to automatic
load testing and are deliberately not a human reading task. During each fixed
20-second measurement, a countdown states the remaining time. The automatic
sampling totals two minutes, plus loading and your manual review time.

Only literal `--manual=true` or `--manual=false` is accepted. Manual mode runs
Chromium headful and records the actual browser version, mode and GPU string.
For each renderer/scale, performance sampling completes first. The probe then
shows a separate two-vertex/four-relation fixture: e0/e1 are distinct parallel
relations, e2 is a self-loop and e3 has reverse direction. This smaller view is
for feature inspection only and contributes no performance samples.

Click both vertices and inspect their complete labels. Click both parallel
curves separately, checking e0 versus e1 in the inspector. Click the self-loop
e2, inspect the selected edge label and examine the arrowhead directions. Wheel
and drag remain available. Click selection updates highlighting and full inspector
text. Actual pointer events are retained separately from programmatic selection.

The browser presents the six checks with Pass, Fail and Not checked controls,
an optional note, and **Save and continue** / **Skip review** buttons. Save records
only the selected answers; unanswered checks remain unknown. Skip records every
criterion as unknown. Human review waits explicitly for Save, Skip or Stop and
has no inactivity deadline. No terminal JSON, hidden prompt or retry loop is used.
These observations are not Fabric decisions or automatic qualification.

Use the persistent **Stop test** button, **Escape**, close the test window, or
press terminal **Ctrl+C** to stop the entire run. No later case starts. Reports
are checkpointed after stages and cases: interruption retains completed
measurements and identifies the partial case, stage and stop reason. Format
`jai.renderer-probe.observations/2` distinguishes partial result records from
`completedCases`; `results.length` is not a completion count. Automatic work has
hard watchdogs: launch 20 s, graph loading 60 s, measurement 30 s for its fixed
20 s sample, other actions 15 s. An unresponsive phase stops the run without retries and is
reported as failed, never a passing sample. Manual waiting remains abortable.

A manual-feature screenshot and pointer history are saved per case. Context-loss probing
runs after the interaction; restoration remains an independent manual/native
check, not an inferred pass.

Without manual mode, programmatic selection demonstrates distinct identity and
inspector content only. The automated vertex-pointer attempt is reported, while
parallel-edge/self-loop picking, readable geometry and arrows stay unknown until
observed. High-DPI captures do not establish screen-reader or full keyboard
accessibility. Fixed corpus positions do not qualify a production layout algorithm
or worker failure handling.

All observations are labelled exploratory-only and the decision remains hold
until native reference-host performance and essential feature evidence are
independently assessed. A software-rendered/headless run is not GPU qualification.
No production renderer winner is encoded by this experiment.

A targeted follow-up can select `--renderer=sigma` or `--renderer=cytoscape`;
`--renderer=both` remains the default. Three scales with one candidate produce
three cases/24 steps, while the default remains six cases/48 steps. Progress
counters use the actual finite plan. Run into a fresh output directory to retain
prior reports. A changed geometry or measurement implementation requires new
observations; prior results remain evidence for their original source revision.

The Sigma adapter uses the SDK's dimensionless spread default (0.25). The
geometry regression calls the installed path factory rather than asserting pixel
results. Animation elapsed time uses a monotonic callback clock; frame intervals
compare successive frame timestamps, including slow final intervals. These
checks do not establish native painting, new readability verdicts or a corrected
third-party timeout. The selected element's complete label is shown separately
above raw metadata; operator readability observations are still required.

The Sigma style audit evaluates actual graph attributes through the installed
SDK for normal, selected and hidden relations and for the default node branch.
The adapter explicitly inherits `DEFAULT_STYLES.edges` before its overrides;
supplying a custom branch does not merge those bindings automatically. Successful
display-data checks establish bindings, not native font painting or readability.

New reports use `jai.renderer-probe.observations/3`; nested operator observations
use `jai.renderer-probe.operator-observation/2` and seven separate criteria.
`edgeLabelReadability` retains its original Selected element/inspector meaning.
The added `edgeCanvasLabelReadability` explicitly asks about the selected label
on the graph edge itself. Both default to unknown and are independent verdicts.
Historical six-criterion reports are retained unchanged, with no retrospective
conversion of inspector answers into canvas-label answers.

For the paired memory/phase diagnostic and a short selected-label review, use:

```sh
npm run probe -- --output=/tmp/fabric-explorer-memory-labels --browser=/usr/bin/chromium-browser --renderer=sigma --size=M --scales=1,1.5,2 --manual=true --diagnostics=memory-phases --review=labels
```

`--diagnostics=none` and `--review=all` remain the defaults. The focused run is
still three cases/eight stages each; stage one explicitly reports its blank,
harness-only, empty-renderer and bounded-graph subphases. Five baseline samples
are scheduled 100ms apart after two normal animation frames. Actual spacing,
overruns, capture duration and incomplete process inventories remain visible;
this is not a quiescence guarantee or continuous peak observation.

One Chromium process lifetime is reused across cases. The first case and later
warm cases are labelled distinctly; no cache purge or forced garbage collection
is performed. The empty renderer has identical canvas dimensions/DPI but zero
graph elements. Its first construction and all cold module/SDK tasks remain in
the overall task record even if later graph assignment benefits from warm state.
The early observer is injected before harness HTML and module evaluation;
coverage before observer installation remains unknown.

Browser process-tree RSS is separate from the Node measurement driver and from
the combined diagnostic total. Missing/changing process inventories produce
null incomplete totals, not zeros. Optional PSS/private counters are diagnostic
and never replace the frozen absolute RSS budget. Raw paired phase medians and
negative or positive deltas are retained with a non-additive warning; they are
not deducted from the application budget. No sampled exceedance is not proof of
a continuous peak or whole-product compliance, especially without the canonical
helper. Memory sampling ends after reset/cancellation and explicitly excludes
manual/context-loss phases; task evidence is refreshed through the final case
checkpoint, including those phases.

The worker retains the full synthetic corpus and sends only bounded views.
This reduces full-corpus UI transfer and clone exposure; a persistent worker
plus bounded UI clones can still increase steady-state memory. Projection stops
once its admitted relation limit is reached. Sigma reuses its public renderer
across graph-only changes through `setGraph`; selection/hover state and camera
are reset for each view. Both first construction and synchronous graph refresh
remain measured work, with no promise that reuse alone meets latency budgets.

`--review=labels` shows only the original inspector-label question and the
separate canvas-label question. Other criteria remain unknown rather than being
pre-filled. Reports use observation format4 and retain compiled asset SHA-256
values only in the caller-selected raw output. Old reports are never overwritten.

### Tiny visual check only

After building, run `node run-label-check.mjs --output=/absolute/scratch/new-run --browser=/path/to/chromium --scales=1,1.5,2`.
This separate headful check has twelve steps: empty Sigma construction, a two-vertex/four-relation scene, operator review, and screenshot/save at each scale. It never mounts the dense corpus or runs animation/memory benchmarks. A size-S synthetic corpus (1,000 vertices / 3,000 relations) is generated in the worker; only its first two vertices/four relations are transferred and mounted. Those scene labels and positions match the size-M feature scene. Chromium sandboxing stays enabled; all assets are injected offline over the Playwright pipe.

Record **path separation** (parallel e0/e1, reverse e3, loop e2) separately from **canvas label readability** after selecting each relation. The optional inspector question concerns the complete selected label card. Unanswered and skipped answers remain unknown. The distinct `jai.renderer-probe.labels-only/1` report and `jai.renderer-probe.label-observation/1` observations do not reinterpret earlier manual reports. Stop, Escape, window close and Ctrl+C end the entire run. Outputs must use a fresh ignored scratch directory or a directory outside the checkout.

The Sigma adapter retains its original public Graphology instance across replacements and uses public clear/add events plus a final refresh. This keeps the pinned SDK's edge-group index attached to the rendered graph. `npm run check:active-path` exercises the actual SDK grouping, style, spread and path-selection chain without creating a WebGL context; it cannot qualify native paint, picking, readability or performance. `npm run check:label-runner` checks finite control and tiny-scene bounds using a browser double.

The tiny runner exits with 0 for completed checks, 130 for operator interruption, and 2 for execution or cleanup failure. Partial observations and cleanup errors remain in the report. GPU metadata borrows Sigma's existing public stage canvas and caches its renderer information; it never allocates or loses a diagnostic WebGL context. The Canvas renderer reports this diagnostic as not applicable, with software status unknown. `npm run check:gpu-diagnostic` verifies allocation/loss counters against actual app source and the pinned public SDK accessor; it does not measure native latency or memory savings.
