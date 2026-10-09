# Defect analysis standard

A defect is analysed before it is fixed. Reading the failing code and
theorising is not analysis: it finds a plausible cause, not the actual
one. This standard requires three comparisons, because each one can find
what the others miss, and a root cause supported by evidence from them.
`/diagnose` follows it; the `defect-analyst` agent performs it;
`defect.py` does the mechanical parts and validates the analysis before
a fix may start.

## 1. Reproduce and characterise

- State the symptom exactly: observed against expected, with the input,
the environment and the version.
- Build the smallest reproduction that is a **command**: it exits 0 when
the behaviour is correct and non-zero when the defect occurs. Every
comparison below reuses it.
- **Measure determinism before anything else.** Run the reproduction
many times (`defect.py repeat`). A defect that occurs in some runs and
not others is evidence about timing, ordering, shared state or the
environment — never dismiss it as "flaky".

## 2. Three comparisons — all three, every time

Each is either carried out, with its evidence, or marked not applicable
**with the reason**. "Not applicable" without a reason is not accepted.

### A. Against the last known good state

When did it work, and what changed since?

- Find a **last known good** state: a release, a tag, a commit, a
deployment, a date when the behaviour was right.
- Find the **first known bad** state. With the reproduction command,
`defect.py bisect` runs `git bisect` in a separate worktree — your
working tree is never touched — and names the first commit at which it
fails.
- List **everything that changed** between them, not only code:
dependencies and lockfiles, configuration, infrastructure, data and its
volume, the runtime and its version, feature flags (`defect.py
changes`).
- The first bad change is the strongest single piece of evidence there
is; it is not yet the root cause — explain *why* that change produces
the defect.
- Not applicable only when the behaviour has never worked (a defect
present since the code was written).

### B. Against a working analogue

Where does similar code, or the same code, behave correctly?

- Find the **analogue**: a sibling function or endpoint that does the
same kind of thing correctly; the same code on another input, tenant,
environment, instance, platform or version that works; the reference
implementation or the documented pattern.
- **Diff them** (`defect.py compare`): code, inputs, configuration,
environment, timing. List every difference.
- **Find the difference that matters**: transplant one difference at a
time — the working version's check into the failing one, the failing
input into the working path — and see which flips the behaviour. A
difference is confirmed when introducing it breaks the working case or
removing it fixes the failing one.
- Not applicable only when there is genuinely no analogue — say what you
looked for.

### C. Timing and time-dependent behaviour

Does time, ordering or duration take part in the defect?

- **Completion:** does an operation get the time it needs? Timeouts
against actual durations (measure them); asynchronous work not awaited,
futures not joined, callbacks assumed to have run; a process ending
before its background work.
- **Ordering and concurrency:** two threads, requests, consumers or
retries interleaving; check-then-act on shared state; a cache read
before it was written; messages arriving out of order; at-least-once
delivery processed twice.
- **Other timed events:** scheduled jobs, TTLs and cache expiry, token
and certificate expiry, connection-pool and lock timeouts, retries and
back-off, garbage collection, daily and monthly boundaries, time zones
and daylight saving, clock skew between machines, leap years.
- **Change over time:** resource exhaustion that builds up (leaks,
unclosed connections, growing queues), behaviour that depends on load or
on how long the system has run.
- **How to test it:** vary timing deliberately — inject delays, slow the
dependency down (a proxy such as Toxiproxy, a stub with configurable
latency), run in parallel, run many times, fix the clock, shift the time
zone. Correlate the failures with timestamps in the logs. `defect.py
timing` lists the timing-sensitive constructs in the code under
suspicion; `defect.py repeat` measures failure rate and duration.
- Not applicable only with evidence — for example, the reproduction
fails in every one of many single-threaded runs, takes far less time
than any timeout involved, and touches no clock, schedule or shared
state.

## 3. Hypotheses, then experiments

- Write **competing hypotheses**, each with the prediction that would
distinguish it from the others.
- Run the **discriminating experiment** for each; look for evidence
against your favourite first.
- Stop when one hypothesis explains *all* the evidence — the
comparisons, the determinism measurement, the logs — and the others are
refuted.

## 4. Root cause, fix, verification

- Distinguish the **root cause** (the decision or code that makes the
defect possible), the **trigger** (what made it happen now) and
**contributing factors** (what failed to catch it — a missing test, a
missing alert).
- **Fix the root cause**, not the symptom. A longer timeout that merely
makes a race rarer is not a fix.
- **A regression test first**, seen to fail on the defective code
(testing standard). For timing defects the test controls time and
ordering — an injected clock, a latch or barrier, Awaitility instead of
`sleep` — so that it fails every time on the defective code, not
occasionally.
- **Verify**: the reproduction now passes — for an intermittent defect,
every one of many repeated runs — and the full suite passes.
- Record what would have caught it earlier, and fix that too when it is
cheap.

## The analysis, as validated

The `defect-analyst` agent returns its analysis as JSON, and `defect.py
analysis validate` refuses it unless every part is present: the symptom
and reproduction; a determinism measurement (runs and failures); each of
the three comparisons either done, with its evidence, or not applicable,
with its reason; the hypotheses with their experiments and outcomes; the
root cause with its location, trigger and contributing factors; the
proposed fix and regression test. Only a validated analysis goes forward
to a fix. `defect.py analysis render` turns it into a report; `defect.py
analysis findings` turns the root cause into a finding in the ledger, so
that the fix follows the usual rework loop and is verified by someone
other than whoever made it.
