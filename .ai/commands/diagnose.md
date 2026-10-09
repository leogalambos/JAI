---
description: "Find the root cause of a defect before fixing it: last known good, a working analogue, and timing"
argument-hint: <symptom, failing test or issue>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---
> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `defect-analyst`.

Diagnose: $ARGUMENTS. Use the `defect-analysis` skill. First ask me when it last worked and where something similar works, if I have not said. Dispatch the `defect-analyst` agent, validate its analysis with `defect.py analysis validate` before anything else, and show me the report. Then ask whether to fix it through the rework loop, with a regression test first.


## Operational specification — Diagnostic evidence

**Preconditions and boundary.** Establish observed symptoms, environment, version, reproducibility and failure impact before hypothesizing causes.

**Execution and required evidence.** Rank hypotheses, verify against logs/traces/tests, and keep an evidence trail for eliminated explanations.

**Acceptance and escalation.** Distinguish established root cause from plausible cause; recommend bounded corrective actions with regression tests.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
