---
description: Show compact project execution efficiency and evidence-qualified profile comparisons inside the conversation
argument-hint: "[last | profile name | compare profile-a profile-b]"
allowed-tools: Read, Grep, Glob, Bash
---

Claude exposes `/jai-stats`; Codex exposes `$workflow-stats`. Handle the request
inside the current native conversation, without asking the operator to open a
terminal. Arguments: $ARGUMENTS.

Use `~/.ai/it-role-house/tools/execution_stats.py` internally with `--project ROOT`;
the source equivalent is `.ai/runtime/tools/execution_stats.py`. With no arguments
show recorded project history compactly; `last` shows the last recorded run,
`profile NAME` filters it, and `compare A B` compares compatible recorded cohorts.
State clearly when no actual measurements or compatible cohorts exist.

Normal task output comes first. The default efficiency footer is one compact
Markdown table with a header and one aggregate row, never a long narrative that
pushes the work out of view. Show detail only on explicit request. Physical model
time is not wall-clock time. Worker completion is not human acceptance. Include
unknown tokens/prices/severity/causes only as unavailable in requested detail;
omit unknown columns from the compact footer. A low finding count does not prove
quality. Distinguish requested settings from provider-observed model facts.

Recommendations are advisory with confidence and evidence limitations. Rework
alone cannot establish weak effort: changing inputs, unclear criteria or useful
review can cause it. Never automatically switch a profile. Do not claim savings
from incompatible tasks, providers, review scopes or unspecified cohorts.

The normal layered host supplies `efficiency` in completion/checkpoint/next/close
responses and an explicit `efficiency` operation. Use the returned `table` after
the actual work output. Statistics derive from already verified event suffixes;
do not replay journals on every turn, scan private task inputs, or copy prompts,
filenames, finding prose or provider captures into analytics. Ordinary retained
workflows with no recorded runtime linkage must report metrics unavailable,
rather than invent measurements or count this conversation as a governed run.
