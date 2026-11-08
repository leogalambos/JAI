---
description: List, inspect or select project execution profiles for JAI models, effort and context preferences
argument-hint: "[profile-name | show profile-name | effective | profile-name --session]"
allowed-tools: Read, Grep, Glob, Bash
---

Operate execution preferences inside this native conversation. Claude exposes
`/jai-profile`; Codex exposes `$workflow-profile`. The operator does not need an
external terminal. Arguments: $ARGUMENTS.

Use `~/.ai/it-role-house/tools/execution_profiles.py` internally with the actual
project root and active provider (`--project ROOT --provider claude|codex`). The
source checkout equivalent is `.ai/runtime/tools/execution_profiles.py`. Resolve
the actual installed/source path; do not claim an uninstalled command is active.

With no arguments, run `list` and display a compact profile table with the active
selection and configuration source. `show NAME` displays that definition;
`effective` displays resolved responsibility mappings and context policy.
A bare NAME runs `use NAME`, persisting the new-project-run preference in
`.jai/config.json`. `workload` is a built-in routing mode: use `use workload` to
return to selected-class registry mappings without deleting context, analytics,
overrides or custom profiles. `--local` writes the local project preference and
can override a shared selection. Show the receipt's effective routing mode and
shadowing; a project write does not defeat a higher-precedence local selection.
Do not require an extra confirmation for that requested write.

With `--session`, run `use NAME --session` and retain the complete receipt,
including execution_profile and context_policy, in this conversation. When
switching a current session choice to workload, pass its actual receipt context
as `use workload --session --context-policy VALUE`; do not derive it from a
persisted profile that the session already overrode. Subsequent new layered
starts receive BOTH `--execution-profile NAME` and
`--execution-context-policy VALUE`. For session-effective diagnostics, run
`effective --session-profile NAME --context-policy VALUE`; show persisted and
session settings separately. List available choices normally, but mark the
actual session choice when one is retained. These are internal backing-tool
arguments: the user stays in this conversation and prepares no JSON or terminal
command. Session choices change no files or resumed engagements.

Display routing_mode independently of configured: an explicit workload choice is
configured=true but bypasses fixed role preferences. Its effective output shows
workload mappings, and no configuration defaults to active workload routing.
Named profiles retain their actual responsibility preferences. Profile preferences
do not waive professional prerequisites; report selected routing deviations and
blocked SABSA model pairs instead of claiming the profile was applied exactly.

Configuration is operational preference, not authority, acceptance, staffing
ownership, permission or resource allowance. Preserve the full catalogue and
local model/profession selection. Existing runs use their captured snapshot.
Unsupported models/effort must be reported at the actual host boundary, never
silently ignored or described as observed. Do not edit installed generated agents.

Explain context choices precisely: all workers retain required isolation and
author/reviewer separation. `task-isolated` requests a fresh task workspace in
conversation context, not a new filesystem checkout. A main-chat reset or
compaction is host-dependent and must be performed through an actual supported
native facility; otherwise explicitly report it as not performed. Do not replace
a host reset with a claim that the old conversation was forgotten. Apply a
`task-isolated` main-chat request only once at new-task entry, never on every
prepared invocation, internal handoff or cold resume. `manual` requests no JAI
main-chat action; it cannot disable worker isolation or host automatic compaction.
The single policy applies to the entire future run; per-boundary settings,
compaction thresholds and message-retention controls are not implemented.
Compaction retains a shorter summary; a reset starts new active conversation
history without deleting workspace files or durable JAI state. See the maintained
context operation glossary and B0–B10 boundary table in the configuration manual.

Do not append a fabricated efficiency table to a configuration-only operation.
For maintained syntax and limitations see the execution-profiles configuration
manual and `/jai-stats` / `$workflow-stats`.
