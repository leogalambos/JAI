---
description: Set up, reset or check the demo projects for trying every command
argument-hint: <setup|list|reset PROJECT|check>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Run `python3 ~/.ai/it-role-house/demo/demo.py $ARGUMENTS` (with no argument, run `list`). Report what it did. After setup or reset, tell me to open the active AI CLI in the demo folder, and suggest the first command of the 20-minute tour in the guide.


## Operational specification — Demonstration discipline

**Preconditions and boundary.** State which fixture, source release, provider adapter and scenario are being demonstrated.

**Execution and required evidence.** Distinguish simulated outputs from runtime observations and show actual command output, validation evidence, and limitations.

**Acceptance and escalation.** A demonstration is not proof of production conformance or approval.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
