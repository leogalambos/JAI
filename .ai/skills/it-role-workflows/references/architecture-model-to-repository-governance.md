# Architecture model to repository governance

`workflow: architecture-model-to-repository-governance`  ·  `steps: 6`  ·  `tool-tier: route`

**Trigger.** A project/domain architecture needs to become a governed enterprise repository model and published view set.

**Outcome.** Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | finalises project model facts, decisions and project ownership boundaries | project architecture model and source artefacts | Elements/relationships have stable identities and evidence basis |
| 2 | [Architecture Repository and Modelling Lead](../../it-roles-architecture/references/architecture-repository-and-modelling-lead.md) | maps model facts into the canonical repository/metamodel and repository conventions | canonical project model | No model fact is silently reinterpreted to fit a tool |
| 3 | Architecture Repository Engineer | imports/updates the canonical repository, preserving IDs, lifecycle and provenance | repository revision plus interchange artefacts | Repository structural validation passes |
| 4 | Model Consistency Reviewer | checks references, orphans, cross-project ownership, lifecycle conflicts and view drift | consistency findings/gate | No blocking integrity error remains |
| 5 | [Enterprise Architect](../../it-roles-architecture/references/enterprise-architect.md) | resolves enterprise/domain overlap, shared elements and portfolio dependencies | accepted enterprise model/repository decisions | Cross-project dependencies and reusable/reference elements have owners |
| 6 | [Technical Design Authority Member](../../it-roles-architecture/references/technical-design-authority-member.md) | applies architecture governance to material conformance/exception decisions | approved/rejected repository release | Exceptions and residual risks have named authority and expiry/review |

## Operating this chain

Use `tools/repository.py` for canonical repository validation, Open Exchange import/export, view generation, impact and portfolio reports. Open Exchange XML is an interchange artefact; it is not the authoritative EA-domain projection store.
