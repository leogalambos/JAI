---
description: Independently audit exact Gen2 justification, cancellations and current permissions
argument-hint: "[engagement] [output or requested audit scope]"
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Delegate this natural-language audit request to the independent `fabric-auditor`
agent through the active provider's native delegation mechanism:

$ARGUMENTS

The parent resolves the existing engagement under `FABRIC_HOME` or `./.fabric/`.
Without a name, discover the newest `.jsonl` locator and disclose the chosen
engagement. File modification time only chooses a journal locator; it never
chooses governing inputs or output versions. Ask for clarification when an
output name identifies several immutable versions or use scopes.

Internally run `python3 <runtime>/tools/governed_audit.py [engagement] [subject]
--home <existing-home> --scope <use-scope> --json`. The installed runtime is
`~/.ai/it-role-house`; use the source runtime when explicitly working in its
checkout. Keep the actual report/head as the auditor's input. This transport is
the parent's responsibility; never ask the user to construct JSON or call it.
If the auditor has no native shell, the parent supplies the report rather than
widening its tool tier. A small report may be relayed verbatim. For a large
report, retain its complete bytes in authorized scratch and send a small base
request with engagement/head/scope, exact output references, mandatory limits
and an index of report sections. Use actual native Read where available;
otherwise relay requested exact sections, including cross-dependencies and
cancellations, through the ordinary parent conversation. Do not inline the
whole history, silently truncate constraints or guess semantic relevance.
Reports are never recorded into the engagement as an approval.

Report history integrity separately from current justification and supporting
material. Show exact governing input versions/use scopes, selected outputs,
required or missing evidence, review dispositions, relevant establishing and
cancelling decisions, open items, and distinct qualification/acceptance/release
facts. Preserve negative verdicts and limitations. An empty or partial engagement
has no invented output or PASS. An audit grants no permission and never runs a
workflow step, restarts work, imports Gen1 acceptance or signs a human act.

Use only the maintained Gen2 runtime and existing provider projections. Old
paper/strict graph verdicts are not executable alternatives or new acceptance
criteria. Source restoration and installed activation are separate milestones.
