# Layered runtime and assurance model

The layered runtime is the implementation-specific bridge between the research architecture in **Leo Galambos, _Towards Justifiable AI Systems_ (2026)** and the production controls shipped in AI IT House.

Use this page to understand runtime states, controls and their limitations.
For operating the engagement cycle, follow
[Layered engagement](../using/layered-engagement.md); for choosing whether the
method fits your task, use [Methodical workflows](../using/methodical-workflows.md).
The [execution and context algorithm](../overview/execution-context-algorithm.md)
explains how supported entry points assemble and control work.

The research model is not treated as a claim that every model response is correct. Its operational idea is narrower and more useful: intermediate work is inspectable; other components challenge it against explicit obligations; and the resulting state determines whether the system may continue, request more evidence, rework, escalate or remain blocked.

## Six JAI responsibilities

The authoritative layer registry is `.ai/runtime/jai/core/layers.json`.

| Layer | Responsibility | Acceptance question |
| --- | --- | --- |
| **L1 Intent and Context** | purpose, accountable authority, scope, material context | Is the intended outcome, accountable authority, scope and material context explicit? |
| **L2 Meaning and Domain Model** | concepts, terminology, claims, assumptions, uncertainty | Do all parties mean the same thing and is uncertainty represented? |
| **L3 Reasoning, Policy and Control** | decisions, policy constraints, evidence obligations, trade-offs, escalation | Are decisions, policy constraints, evidence obligations, trade-offs and escalation rules justified? |
| **L4 Solution Design** | process/technical/analytical design | Does the design satisfy accepted semantics and controls without inventing new facts? |
| **L5 Realisation and Tooling** | implementation through permitted tools and bounded mechanisms | Is the design implemented through permitted tools and bounded execution mechanisms? |
| **L6 Execution and Evidence** | observation, deterministic checks, outcomes and failures | Is the observable result evidenced, attributable, reproducible and suitable for authority review? |

**L0 Human Authority** sits above L1 but is explicitly external to JAI.

## Article principle → JAI control

| Architectural principle | JAI implementation |
| --- | --- |
| Requirements descend as constraints/tasks | adjacent-layer typed Fabric contracts |
| Products return with evidence and uncertainty | typed fragments, evidence, failures and review records |
| Lower-level work is checked before higher-level use | review direction rules plus `supported_by` acceptance enforcement |
| Missing evidence changes behavior | explicit `unknown`/failure states, rework or escalation rather than implicit success |
| Dissent must not disappear | review records and conflict/escalation states remain in the fabric |
| Non-convergence must be bounded | per-lineage rework, per-layer reformulation, contract/round/step budgets |
| A lower layer may challenge feasibility, not rewrite purpose | formal reformulation owned by the layer that issued the requirement |
| Authority cannot be manufactured by an agent | external L0, authority guard and signed/recorded authority transitions |
| Evidence changes can invalidate prior use | reverse dependency invalidation and strict release re-check |
| Release is separate from generation | strict `release` gate after review, authority and fabric verification |

## Deterministic control versus AI judgement

JAI deliberately separates the two.

### Deterministic runtime controls

Examples include:

- record typing and relation signatures;
- adjacency rules;
- direction of reviews;
- context-digest binding;
- hash-chained append-only records;
- rework/reformulation/round/episode budgets;
- legal escalation direction;
- sticky `outside_authority` semantics;
- strict release checks;
- evidence-file drift detection;
- authority command guarding.

### Judgement-dependent work

Examples include:

- whether a decomposition preserves business meaning;
- whether evidence substantively warrants a claim;
- whether a design trade-off is acceptable;
- whether a risk should be accepted;
- whether a human exception is justified.

The Fabric can record, constrain and route these judgements. It cannot turn a weak premise into a true one merely because the record is structurally complete.

## Profile-native Unified Lifecycle GA

The platform integrates its subsystems into the JAI model:

- **Artifact profile** — Artifact Contract v3 composes L1–L6 concerns and writes only to the current native namespace;
- **SABSA profile** — canonical SABSA identity persists at source while SABSA coordinates remain orthogonal to JAI;
- **EA profile** — architecture objects are a scoped EA projection, not a competing global truth model;
- **Publication profile** — ProjectionManifest v3 carries JAI lineage from semantic source through rendering evidence;
- **Runtime profile** — Agent Contracts, policy and Execution Records bind authority and actual L6 observations to JAI.

The assurance fabric is an append-only ledger over canonical object references and hashes. It is not a second semantic source of truth.

## Bounded recovery ladder

A failed result does not automatically trigger another prompt. The supervision policy has four deterministic categories:

1. **local repair** while rework and episode budget remain;
2. **escalate exhausted/budget** when retryable work cannot converge locally;
3. **escalate contradiction** for contradictory/conflicting observations;
4. **operator decision** when escalation reaches the human boundary, an authority matter is involved, or autonomous budgets are exhausted.

This distinction is what makes reformulation and escalation auditable rather than conversational.

## Current implementation boundary

The reference article describes a protected runtime boundary and warns that a correct checker that can be bypassed does not provide whole-system operational control. AI IT House implements substantial enforcement for Fabric records, layer transitions, authority acts and release eligibility. It does **not** establish that every external tool, provider or direct workflow invocation in every deployment is non-bypassable.

In particular:

- the `guard_authority.py` hook is a valuable ordinary-path guard but explicitly describes itself as a **string-level guard**, not a sandbox against a determined shell adversary;
- Layer 6 lacks normal Write/Edit capabilities, but preventing shell-based mutation ultimately benefits from host/sandbox controls such as a read-only mount;
- direct role/workflow paths remain available outside `/layered`, so an organisation that mandates layered supervision for all consequential work must enforce that routing policy at the entry boundary;
- Gate G's packaged fixtures demonstrate the behavioral qualification machinery, not live quality of a specific mutable provider/model.

These boundaries should appear in an assurance case rather than being hidden behind the phrase “JAI compliant.”

## Related pages

- [Running a layered justifiable engagement](../using/layered-engagement.md)
- [Justifiable Fabric](justifiable-fabric.md)
- [Human authority and escalation](../operations/human-authority.md)
- [Validation and release controls](../operations/validation.md)
- [Justifiable AI research lineage](../about/justifiable-ai.md)
