## AI IS/IT house

A provider-neutral IS/IT delivery and governance library is installed in `~/.ai/it-role-house/`, with Claude-native skills, agents and commands exposed under `~/.claude/`.

The user guide is `~/.ai/it-role-house/GUIDE.md`; `/guide` shows it and `/demo` creates practice projects.

- **Software products and document libraries** — analyse, review, develop, rework, govern: use the `library-lifecycle` skill or `/analyse`, `/review`, `/develop`, `/rework`, `/govern`. Review criteria resolve from the request, project `.ai/review-criteria.md` (legacy `.claude/review-criteria.md` is also accepted by tools where applicable), user `~/.ai/review-criteria.md`, or the package default.
- **Problem research and development** — use `research-and-development` or `/research`.
- **SABSA security architecture** — use `sabsa-library` or `/sabsa`.
- **Defects** — diagnose before fixing, using `defect-analysis`, the `defect-analyst` subagent or `/diagnose`.
- **Consequential decisions** that must be justified later — use `/layered`.
- **Specific IS/IT roles, deliverables, RACI or segregation of duties** — use the `it-roles-*` skills or delegate to the `role-router` subagent. Match on the requested deliverable, not merely the job title.

Source code written by the agent follows `~/.ai/it-role-house/standards/code-documentation.md` and `~/.ai/it-role-house/standards/testing.md`; installed hooks enforce documentation, tests and a passing test run after the last production-code change.

Names explicitly described as agents are Claude subagents and must be delegated through the Agent tool, not invoked as skills. Preserve separation of duties: reviewers never fix, authors never verify, and role operators must stay within their tool tier. Never edit `.fabric/` or `.findings/` directly. Authority acts — accepting risk, granting an exception, accepting a product, approving a protected library change — belong to the human and must never be pre-approved or routed around.
