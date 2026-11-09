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

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| native-model | Maintain source semantics and governed canonical identities | Exact revisions, ownership and integrity results |
| interchange | Assess supported format and observable losses without inventing tool qualification | Export/import artifacts, exact format profile and loss disposition |

Return inconsistent source facts to their owner and exchange losses to the mapping/repository owner. Stop publication/release with blocking identity/reference errors, unsupported semantic reinterpretation or missing authority. Publish an explicitly bounded reviewed revision or reject/defer release with owned exceptions and review dates. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Exact source model and project boundary
- Stable identifier namespace and evidence
- Selected notation/exchange profile and ownership rules

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return inconsistent source facts to their owner and exchange losses to the mapping/repository owner.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop publication/release with blocking identity/reference errors, unsupported semantic reinterpretation or missing authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Publish an explicitly bounded reviewed revision or reject/defer release with owned exceptions and review dates.

**Bounded paths and scope:**

Native and interchange paths share semantic integrity; native-only scope does not assert exported files or external-tool qualification.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| native-model | 1, 2, 3, 4, 5, 6 | 6 |
| interchange | 1, 2, 3, 4, 5, 6 | 6 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
