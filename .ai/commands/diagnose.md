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

## Consequential Gen2 use

For a result requiring governed layered justification, use the canonical
`layered-justifiable-delivery` skill and its `references/domain-handoff.md`
native handoff with the actual request, exact criteria/candidate and evidence.
Ordinary bounded work keeps this command's scope and independent responsibilities;
the parent handles runtime transport without user-authored JSON. This command
itself grants no human acceptance or release permission.


## Compact execution feedback

Present the task result first, then a compact one-row Markdown efficiency table.
Use actual recorded host `efficiency.table` when linked to a native governed run.
Otherwise report measurements unavailable in one row; never invent model time,
rework, findings, acceptance or a governed execution record. Detailed history and
advisory comparisons are available through `/jai-stats` / `$workflow-stats` inside
the conversation. Do not append a long efficiency narrative or switch profiles
without an explicit operator selection.
