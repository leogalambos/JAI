---
description: Set up, reset or check the demo projects for trying every command
argument-hint: <setup|list|reset PROJECT|check|scenarios|describe SCENARIO [--step N]|scenario SCENARIO --to DIRECTORY|reset-scenario SCENARIO --to DIRECTORY|check-scenarios>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Run `python3 ~/.ai/it-role-house/demo/demo.py $ARGUMENTS` (with no argument, run `list`). Report what it did. After setup or reset, tell me to open the active AI CLI in the demo folder, and suggest the first command of the 20-minute tour in the guide.

For a task walkthrough, use `scenarios` to discover the scenario IDs, then
`describe SCENARIO` or `describe SCENARIO --step N` to explain its inputs,
command pairs, purpose and inspection points. Description is read-only:
it does not execute a workflow or advance a recorded execution state.

Use `scenario SCENARIO --to DIRECTORY` only when the user requests a new
practice workspace. Report the actual destination and generated files,
then invite the user to open Claude or Codex in that directory and read
`START.md`. Inputs are fictional text examples, including labelled text
derivatives where the guide discusses binary documents. Missing source
code or evidence must still be supplied before source-dependent work.
Do not claim that creating a scenario executed its guided commands,
produced a reviewed deliverable or recorded approval. An existing
destination must not be overwritten implicitly; follow the tool's safe
reset and backup behaviour only when reset is explicitly requested.

`/guide SCENARIO` explains the same walkthrough. Its Codex equivalents are
`$workflow-demo` and `$workflow-guide`; no extra top-level command is
required. The maintained walkthrough catalogue is `docs/examples/index.md`.


If the user is unsure which task scenario fits a project, offer
`/hint <project question>` or `$workflow-hint <project question>` for
experimental advice. Do not execute the hint or its recommended steps
automatically. A hint's selected ID can be inspected with `describe ID`;
selection and description create no workspace. Only an explicit practice
request with `scenario ID --to DIRECTORY` creates fictional inputs. Keep
legacy `setup` limited to its original three tour projects and retain
non-overwrite defaults and explicit reset backups. A hint does not supply
missing evidence, source code, human authority or a monitoring scheduler.


## Operational specification — Demonstration discipline

**Preconditions and boundary.** State which fixture, source release, provider adapter and scenario are being demonstrated.

**Execution and required evidence.** Distinguish simulated outputs from runtime observations and show actual command output, validation evidence, and limitations.

**Acceptance and escalation.** A demonstration is not proof of production conformance or approval.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
