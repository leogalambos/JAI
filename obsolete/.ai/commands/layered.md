---
description: Run a consequential task through the six-layer justifiable delivery method
argument-hint: <intent, stated as you would to an accountable team>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Use the `layered-justifiable-delivery` skill for the following intent. Record it verbatim as the intent node, initialise a fabric under `.fabric/` in the current workspace, and run the layer cycle down and back up. Stop and hand over to me whenever an escalation reaches layer 1.

Intent: $ARGUMENTS


## Operational specification — Six-layer execution contract

**Preconditions and boundary.** Retain the verbatim intent; L1 defines authority and scope, L2 fixes meaning, L3 evaluates controls and rationale, L4 specifies design, L5 realizes it, and L6 records observed evidence.

**Execution and required evidence.** Use typed downward transitions and evidence-backed upward review; classify rework, reformulation and escalation separately and respect episode/revision budgets.

**Acceptance and escalation.** Escalate to L0 human authority when required. A completed run is not synonymous with independently approved release.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
