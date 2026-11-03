## AI IS/IT house

A provider-neutral IS/IT delivery and governance library is installed in `~/.ai/it-role-house/`. Codex-facing skills are generated under `~/.codex/skills/` from that common source.

The user guide is `~/.ai/it-role-house/GUIDE.md`. Workflow commands from the Claude distribution are exposed to Codex as skills named `workflow-<name>` (for example `$workflow-review` and `$workflow-develop`). Claude subagent procedures are exposed as `agent-<name>` skills (for example `$agent-role-router` and `$agent-codebase-reviewer`). These are behavioural/operator contracts; use Codex subagent delegation where available when isolation or independent review is required.

Routing:
- software/document lifecycle: `library-lifecycle`, or `$workflow-analyse`, `$workflow-review`, `$workflow-develop`, `$workflow-rework`, `$workflow-govern`;
- research and development: `research-and-development` or `$workflow-research`;
- SABSA: `sabsa-library` or `$workflow-sabsa`;
- defect diagnosis: `defect-analysis`, `$agent-defect-analyst` or `$workflow-diagnose`;
- consequential decisions: `$workflow-layered`;
- specific IS/IT roles, deliverables, RACI or segregation of duties: `it-roles-*` and `$agent-role-router`.

Source code written by the agent follows `~/.ai/it-role-house/standards/code-documentation.md` and `~/.ai/it-role-house/standards/testing.md`; installed hooks enforce documentation, tests and a passing test run after the last production-code change.

Preserve separation of duties: reviewers never fix, authors never verify, and role operators stay within their source tool tier. Never edit `.fabric/` or `.findings/` directly. Authority acts belong to the human. Codex PreToolUse hooks cannot manufacture an interactive approval request, so an authority command attempted by Codex is intentionally denied and the human must run that command explicitly. Do not bypass that fail-closed boundary.
