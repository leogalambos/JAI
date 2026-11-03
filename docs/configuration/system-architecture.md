# System architecture

AI IT House {{ JAI_VERSION }} separates **normative semantic architecture**, **domain profiles**, **runtime enforcement** and **provider-specific rendering**.

This page is for maintainers locating configuration and implementation
boundaries. For the request-to-context mechanism, continue with the
[execution and context algorithm](../overview/execution-context-algorithm.md).
Operators choosing how much assurance their task needs should instead start
with [Methodical workflows](../using/methodical-workflows.md).

## JAI as the normative top-level architecture

The layered delivery mode uses a six-layer SABSA matrix. Ad-hoc specialist work
and selected workflows reuse the same catalogue without requiring the whole
matrix. Human Authority is the external L0 boundary in every mode.

```text
                         L0 HUMAN AUTHORITY
                                │
                         JUSTIFIABLE AI CORE
                                │
        L1 Contextual → L2 Conceptual → L3 Logical → L4 Physical → L5 Component → L6 Management
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
     Artifact                SABSA / EA              Publication
      profile                 profiles                 profile
                                │                        │
                                └──────── Runtime profile┘
                                         │
                              Fabric assurance ledger
                                         │
                         provider/host enforcement + evidence
```

Artifact, SABSA, EA, Publication and Runtime are profiles or enforcement mechanisms of that core. They do not become parallel global sources of truth.

## Scoped authority

Examples:

- JAI owns canonical semantic identity;
- SABSA owns its methodology coordinates/semantics within the SABSA profile;
- the EA repository is authoritative for the **EA-domain projection**;
- ProjectionManifest is authoritative for the audience-specific publication projection it describes;
- ExecutionRecord is evidence of what the runtime recorded, not proof that an external system behaved correctly beyond that evidence.

This scope discipline prevents the phrase “source of truth” from being used without saying **for what**.

## Provider-neutral package structure

- `.ai/runtime/` — provider-neutral JAI core, roles, workflows, schemas, publication, policies, EA/SABSA tooling and Fabric runtime;
- `.ai/agents/` — canonical agent definitions and authority/tool boundaries;
- `.ai/skills/` — knowledge and procedure skills;
- `.ai/commands/` — user-facing workflow commands;
- `.ai/adapters/` — provider-specific rendering/compatibility logic;
- `.ai/setup/` — installation/uninstallation implementation.

## Common runtime services

The common runtime includes:

- JAI core registries and profiles;
- role/workflow catalogue;
- Artifact Contract v3 registry;
- provider-neutral model/workload routing;
- SABSA semantic tooling;
- scoped EA repository and ArchiMate/Open Exchange tooling;
- publication projection, rendering and visual QA;
- policy/agent enforcement and content-hashed Execution Records (not immutable custody);
- output validation and tag-driven product release checks;
- Justifiable Fabric supervision runtime.

## Skills versus agents

A useful mental model is:

- **skill** = knowledge, method or procedure;
- **agent** = execution/authority boundary with tools and workload class.

Governance therefore does not depend on a “personality prompt” alone. Reviews, writes, execution and authority can be separated by tool capabilities and runtime policy.

## Fabric relationship to the semantic model

The governed runtime records immutable versions, dependencies, decisions and
scoped applicability. Product and evidence records carry exact references and
content identities so audit can explain the basis of a particular output. The
ledger does not make unrelated historical conclusions current.

## Publication path

The production publication sequence is:

```text
semantic source
→ publication profile
→ DCS-bound ProjectionManifest v4
→ publication model with JAI lineage
→ renderer
→ render evidence / visual QA
→ authority / publish
```

A production render that bypasses the matching ProjectionManifest is not the supported current write path.

## Layered engagement path

The `/layered` path adds the supervised JAI execution cycle around consequential work:

```text
task and governing inputs
→ each layer: local setter, author and independent reviewer
→ six-question integration and adjacent-layer handoff
→ bounded rework, reformulation or escalation where needed
→ completed output with its relevant evidence
→ separate human acceptance and release decisions when required
```

See [Layered runtime and assurance model](../capabilities/layered-runtime.md) for detailed enforcement semantics.

## Implementation details

[Execution and context assembly](../overview/execution-context-algorithm.md) describes context assembly and runtime boundaries.
See how the architecture maps to supported procedures and actual runtime calls.
