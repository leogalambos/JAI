# Offline content qualification

Owner: JAI maintainers · Last reviewed: 2026-10-20

Mandatory content qualification uses local dependencies, fixtures and
reference data. It never requires live Codex/Claude, paid inference or
additional evaluation downloads. Checkout, dependency acquisition and the
existing authorized release/signing infrastructure are separate operations.

## Enforce offline execution

On Linux, the offline runner requires locally installed `libseccomp`. It
blocks network socket families for the entire child process tree while
allowing local Unix-domain IPC. Python child auditing also rejects provider
CLI execution and wrappers; an allowlisted environment excludes credential
variables. This is qualification containment, not a hostile-code sandbox.

```bash
python3 .ai/runtime/tools/offline_guard.py scan --root .
regression_budget="$(python3 .ai/runtime/tools/qualification_core.py budget --scope regression)"
python3 .ai/runtime/tools/offline_guard.py run --root . --timeout "$regression_budget" -- \
  python3 -u .ai/runtime/tools/qualification_core.py regression
```

Unavailable kernel controls produce `NOT_EXECUTED` and a non-passing exit;
there is no unguarded fallback. Static auditing complements runtime controls
but cannot prove arbitrary program behavior. CI runs qualification commands
through this same runner after dependency installation.

## Core and full-source profiles

The core distribution includes runtime configuration, DCS registries,
135 expert Markdown references, 30 small representative JSON regression
fixtures, validators and optional provider tooling. It excludes the extended
enterprise payload, private working inputs, build directories, caches and
bulky execution results. Minimal existing release evidence remains subject
to the unchanged release policy.

```bash
python3 .ai/runtime/tools/expert_references.py validate --root . --all
python3 .ai/runtime/tools/content_eval.py run --root . --profile core \
  --output build/core-content-evaluation.json
```

`core` exercises the representative fixtures only; it does not claim full
catalogue scenario coverage. `full-source` is the default for the source
project and evaluates the extended corpus as well:

```bash
python3 .ai/runtime/tools/content_eval.py run --root . \
  --profile full-source --output build/full-content-evaluation.json
python3 .ai/runtime/tools/content_scenarios.py run --root . \
  --output build/content-scenarios.json
```

Full-source data unavailable or failing integrity validation produces
`NOT_EXECUTED` and a nonzero exit. Absence is never a PASS and does not silently
select the core profile. Full-source qualification cannot be claimed from a
core-only installation.

## Optional local evaluation package

The core pins individual extended payload digests in
`content/evaluation-package.json`. From a complete source checkout, create
an optional versioned archive and companion digest:

```bash
python3 .ai/runtime/tools/evaluation_package.py build --root . \
  --output build/optional-evaluation.zip
```

Verify the companion archive digest before unpacking it into a local
`extended-evaluation/` directory. Then check pinned payloads and run:

```bash
python3 .ai/runtime/tools/evaluation_package.py check --root . \
  --data-root ./extended-evaluation
python3 .ai/runtime/tools/content_eval.py run --root . \
  --profile full-source --extended-root ./extended-evaluation
```

No command downloads absent data. The optional archive contains synthetic
inputs, not generated CI reports, professional approvals or customer evidence.
A different release's corpus must match the installed pinned descriptor.

## What a passing result establishes

The shared deterministic checks cover binding integrity, workflow receiving
contracts, reference structure, content predicates and negative cases.
The seven end-to-end scenarios exercise the host-verification fixture
interface, including identity, stale snapshots, rollback and separation of
duties. They remain deterministic synthetic simulations and do not qualify
live worker isolation. The separate expert-reference regression suite covers
invalid selected overrides and precedence failures.

Seeded-defect recall and reference false positives are labelled
`synthetic-regression`. The mutation recipes and detector rules are related;
these metrics are not independent human-gold measurements or estimates of
provider performance. Counts and denominators accompany measured rates.

`PASS` means an executed check met its stated criteria. `NOT_EXECUTED` means
it was not exercised. Missing renderer dependencies never produce PASS;
required unexecuted gates remain non-passing. Optional unavailable features
cannot be advertised as qualified. Structural qualification is distinct from
professional acceptance, domain correctness and production activation.

Existing A–H, security, authorization, evidence and governance gates remain
mandatory. Run the existing full release qualification entrypoint in the
prepared environment:

```bash
qualification_budget="$(python3 .ai/runtime/tools/qualification_core.py budget --scope qualification)"
python3 .ai/runtime/tools/offline_guard.py run --root . --timeout "$qualification_budget" -- \
  python3 -u .ai/runtime/tools/release_ga.py qualify
```

The provider harness is separate and never a dependency of qualification;
see [optional provider evaluation](optional-provider-evaluation.md).

## Bounded CI regression execution

The canonical mandatory regression inventory lives in
`qualification_core.py`. CI and gate A execute the same 22 modules in their
maintained order, each in a separate offline-controlled process with a
600-second ceiling. Every module remains mandatory. A failure, timeout or
unavailable control prevents qualification; module isolation does not waive
checks or permit live provider execution.

Run the complete regression inventory with the aggregate kernel guard:

```bash
regression_budget="$(python3 .ai/runtime/tools/qualification_core.py budget --scope regression)"
python3 .ai/runtime/tools/offline_guard.py run --root . --timeout "$regression_budget" -- python3 -u .ai/runtime/tools/qualification_core.py regression
```

Run full A–H qualification with its own aggregate budget:

```bash
qualification_budget="$(python3 .ai/runtime/tools/qualification_core.py budget --scope qualification)"
python3 .ai/runtime/tools/offline_guard.py run --root . --timeout "$qualification_budget" -- python3 -u .ai/runtime/tools/release_ga.py qualify
```

The regression ceiling is 13,320 seconds: 22 module ceilings plus 120 seconds
for orchestration. The complete A–H ceiling is 19,440 seconds: all individual
command ceilings, including evidence generation and the final policy check,
plus the same margin. These are maximum resource budgets, not expected run
times. A regression test checks their relationship to the actual gate commands.
The workflow job ceiling remains finite at 360 minutes. Independent individual
commands retain the guard's default 900-second ceiling unless explicitly set.

Each regression result identifies its module, elapsed seconds and execution
ceiling. Unbuffered verbose pytest diagnostics identify the last active test
when a module times out. Captured stdout and stderr survive timeout termination;
they are displayed after the guarded process finishes, rather than streamed
live. Treat diagnostics as local operational records. Do not automatically
publish private project inputs or unsanitized customer output from local runs.
