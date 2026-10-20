---
description: Show the user guide for this library, or the section for one command, with its demo
argument-hint: "[command or topic]"
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Read `~/.ai/it-role-house/GUIDE.md`. If I named a command or topic ($ARGUMENTS), show me just that section — what it does, its syntax, what happens, the demo to try, what to expect and how to check it worked — and offer to run the demo now. If I named nothing, give me the contents and the 20-minute tour. Do not show the 'what to expect' answer keys of review demos before I have run the review, unless I ask for them. If I ask for the full website/manual, use `docs/index.md` from a source checkout or an actual verified deployment URL from project configuration. Do not invent a Pages address. If only the installed runtime is available, explain that `GUIDE.md` is its offline guide and the full maintained documentation is distributed in the repository `docs/` tree.

For a task scenario ID, read its maintained demonstration description:
`python3 ~/.ai/it-role-house/demo/demo.py describe SCENARIO`.
Use `--step N` for a requested numbered step. Explain required inputs,
the Claude slash command and Codex `$workflow-...` equivalent, why the
step belongs in the sequence, and what the reader should inspect.
Do not execute the scenario or claim a step has completed merely because
its description was shown. Use `scenarios` to resolve a scenario ID instead
of inventing one. Preserve the review-demo answer-key rule above.

Link to the corresponding maintained page when the source documentation
is available. For hands-on practice, explain
`/demo scenario SCENARIO --to DIRECTORY` and its `$workflow-demo`
equivalent. Creation requires an explicit practice destination and
produces fictional inputs and `START.md`, not actual evidence or
approval. If inputs, application source, independent review or human
authority are missing, explain the pause and the evidence needed to
resume the original workflow. Do not introduce another top-level command.


If the user has a project question rather than a known command or scenario,
explain `/hint <project question>` and `$workflow-hint <project question>` as
experimental advisory navigation. `/guide` explains maintained instructions;
`/hint` interprets a problem and recommends an adaptation. Do not execute
`/hint`, a recommended workflow or a demo merely because help was requested.
When following a hint, resolve its actual returned scenario IDs with `scenarios`
and read `describe ID` or `describe ID --step N`; report invalid IDs explicitly.
Do not infer completed steps, project evidence, independent approval or automatic
monitoring from a recommendation. Preserve the existing answer-key restriction.


## Operational specification — Assisted navigation

**Preconditions and boundary.** Confirm user objective and installed provider/runtime context, then direct users to the canonical command, skill, workflow or documentation section.

**Execution and required evidence.** Prefer a minimal validated path with prerequisites, artifacts, verification and troubleshooting steps.

**Acceptance and escalation.** State capability boundaries and distinguish optional components from mandatory controls.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.

## Conversational knowledge authoring assistance

Apply the knowledge-platform and fail-closed limits in the maintained hint
capture contract and the installed GUIDE before planning local storage,
delete or restore operations; ordinary bundled guidance remains available.

Help alone remains read-only. If the user explicitly asks to remember a selected
lesson or procedure from the current prompt/conversation, follow the
`Conversational knowledge capture` branch in the maintained hint command contract
(`~/.ai/it-role-house/commands/hint.md`; source `.ai/commands/hint.md`) directly.
Do not require another slash command, manual JSON or user-authored detailed steps.
Explain the selected content and ask only missing essential metadata before any
write. Original explicit save intent persists through answers: complete that task
without a separate save instruction. Preparation alone never grants final save.

Use only visible selected context, not unavailable history. Default responsibility
to the operator role only when implicit ownership is clear; ask about unclear
ownership, confidentiality, reliability and authorised library location. Show the full readable preview of
saved knowledge and actual destination. AI editorial extraction and
storage never constitute human approval. Existing safe immutable storage remains
in force; stored lessons enter hint/guide only after explicit read/disclosure scope selection,
never automatic demo execution. Ordinary help
does not authorise writes, hidden history scans or automatic session capture.

## Explicit local know-how explanation

For an explicitly selected local knowledge record, follow the hint contract's
knowledge-assisted selection and lifecycle branches. Require read/provider
content-disclosure permission, selected roots, permitted confidentiality classes
and applicability contexts. Resolve exact library index, record ID and version
from the selector; call `knowledge.py describe` with the same explicit scope
before explaining custom scenario steps or lessons. Do not treat a matching ID
as a maintained catalogue scenario, invent a guide URL or execute embedded text.
Explain source type, reported evidence/review, staleness, supersession and declared
conflicts without manufacturing approval. Export/delete/restore need their own
explicit requests; ordinary guide help and read permission authorise no writes.
