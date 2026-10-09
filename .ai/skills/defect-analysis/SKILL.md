---
name: defect-analysis
description: "Diagnoses a defect to its root cause before it is fixed, by three mandatory comparisons: against the last known good state (bisecting to the first bad change, without touching the working tree), against a working analogue (where the same kind of code works) and against timing (timeouts, async completion, ordering, clocks, schedules, expiry, intermittency). Then fixes it with a regression test, through the findings ledger, verified by the analyst. Use for 'why does this fail', 'this broke after the upgrade', 'it fails sometimes', 'works on staging but not production', 'fix this bug'."
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

# Defect analysis

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `defect-analyst`, `role-engineer`.

`tool-tier: orchestrate` (`Read, Grep, Glob, Bash, Task, Agent`) · `version: 1.0.0`

A defect is analysed before it is fixed, following `~/.ai/it-role-house/standards/defect-analysis.md`. You orchestrate; agents do the work.

## Steps

1. **Gather** from the user what they know: the symptom, how to trigger it, and — ask explicitly — **when it last
   worked** and **where something similar works**. Both are often known and save hours.
2. **Analyse.** Dispatch the `defect-analyst` agent with that information. It reproduces the defect as a command,
   measures how deterministic it is, carries out the three comparisons — last known good, working analogue,
   timing — tests competing hypotheses, and returns its analysis as JSON.
3. **Validate.** Save the JSON and run `python3 ~/.ai/it-role-house/tools/defect.py analysis validate <file>`. If it is refused, send the problems back
   to the analyst; do not proceed to a fix. Show the user `python3 ~/.ai/it-role-house/tools/defect.py analysis render <file>`.
4. **Record.** `python3 ~/.ai/it-role-house/tools/defect.py analysis findings <file> > root-cause.json`, then
   `python3 ~/.ai/it-role-house/tools/findings.py add defect-<date> root-cause.json`.
5. **Fix**, through the rework loop of `library-lifecycle`: the `role-engineer` agent writes the regression test
   first and sees it fail, then fixes the root cause — not the symptom — and runs the tests. The
   `defect-analyst` agent verifies: the reproduction passes, every repeated run for an intermittent defect, and
   records `findings.py verify`.

## Rules

- No fix before a validated analysis. A plausible explanation is not a root cause.
- A longer timeout, a retry or a `sleep` that makes a race rarer is not a fix for the race.
- Timing is never dismissed for an intermittent defect: the validator refuses it.
