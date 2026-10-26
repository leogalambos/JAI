# System architecture

AI IT House {{ JAI_VERSION }} separates **normative semantic architecture**, **domain profiles**, **runtime enforcement** and **provider-specific rendering**.

This page is for maintainers locating configuration and implementation
boundaries. For the request-to-context mechanism, continue with the
[execution and context algorithm](../overview/execution-context-algorithm.md).
Operators choosing how much assurance their task needs should instead start
with [Methodical workflows](../using/methodical-workflows.md).

## JAI as the normative top-level architecture

The six-layer Justifiable AI core is the single top-level architecture for production semantics. Human Authority is the external L0 boundary.

```text
                         L0 HUMAN AUTHORITY
                                │
                         JUSTIFIABLE AI CORE
                                │
        L1 Intent → L2 Meaning → L3 Policy → L4 Design → L5 Realisation → L6 Evidence
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
- behavioral evaluation and A–H release qualification;
- Justifiable Fabric supervision runtime.

## Skills versus agents

A useful mental model is:

- **skill** = knowledge, method or procedure;
- **agent** = execution/authority boundary with tools and workload class.

Governance therefore does not depend on a “personality prompt” alone. Reviews, writes, execution and authority can be separated by tool capabilities and runtime policy.

## Fabric relationship to the semantic model

In 26.10.4 the Fabric is an **assurance ledger**, not a second semantic database. Product/evidence Fabric records carry canonical references/hashes so that audit and supervision can point to the same semantic identities used by Artifact/SABSA/EA/Publication profiles.

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
intent
→ L1…L6 contracts
→ evidence
→ bottom-up review
→ bounded rework/reformulation/escalation
→ L0 decision when required
→ strict release gate
```

See [Layered runtime and assurance model](../capabilities/layered-runtime.md) for detailed enforcement semantics.

## Implementation details

[Execution and context assembly](../overview/execution-context-algorithm.md) describes the inspected implementation.
See how the architecture maps to supported procedures and actual runtime calls.
