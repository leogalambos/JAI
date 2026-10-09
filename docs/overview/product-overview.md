# Product overview

AI IT House **{{ JAI_VERSION }}** is a provider-neutral, locally installed IS/IT knowledge and delivery framework for enterprise teams using AI-assisted tooling. The release supports **Claude Code** and **Codex / OpenAI-oriented execution surfaces** while keeping the core role model, workflows, artefact contracts, JAI semantics and governance rules provider-neutral.

The **26.10.4 Unified Lifecycle GA** baseline completed the transition from several parallel domain models to a single normative Justifiable AI core with scoped Artifact, SABSA, EA, Publication and Runtime profiles.

## What problem it solves

Enterprise AI-assisted work commonly fails in several distinct ways:

1. the task starts with the wrong specialist viewpoint;
2. work skips lifecycle or governance gates;
3. generated content is persuasive but weakly evidenced;
4. authorship, review and authority collapse into one model conversation;
5. publication loses traceability to the semantic decision;
6. later nobody can reconstruct which requirement, evidence or approval justified the use;
7. a failed tool call or missing observation is silently converted into a confident-looking answer;
8. a system retries or rephrases until something appears acceptable instead of escalating non-convergence.

AI IT House addresses these failure modes through:

- curated role knowledge and explicit tool tiers;
- 24 canonical enterprise workflows;
- typed Artifact Contract v3 and a 28-class artefact taxonomy;
- the six-layer JAI architecture with explicit human authority boundary;
- append-only traceability and bounded supervision for consequential engagements;
- SABSA semantic modelling and scoped EA/Open Exchange projection;
- publication projection, render evidence and visual QA;
- managed policy, reviewer isolation and provider parity;
- A–H enterprise release qualification.

## Release scope at a glance

| Item | Count |
| --- | ---: |
| Roles | 281 |
| Agents | 33 |
| Skills | 23 |
| Workflows | 24 |
| Artifact types | 28 |
| Schemas | 32 |
| Renderers | 4 |
| Tests | 31 |
| Provider adapters | 2 |

Counts are generated from canonical package sources; manual documentation counts are not authoritative over the release manifest.

## The normative architecture

The JAI core has six responsibility layers:

1. Intent and Context;
2. Meaning and Domain Model;
3. Reasoning, Policy and Control;
4. Solution Design;
5. Realisation and Tooling;
6. Execution and Evidence.

**L0 Human Authority is external.** Agents may prepare evidence, recommendations and dossiers, but they cannot manufacture L0 authority.

For consequential work, `/layered` operationalises the downward/upward cycle with typed contracts, independent review, bounded recovery and release gating. See [Running a layered justifiable engagement](../using/layered-engagement.md).

## Supported working domains

The catalogue covers architecture, business analysis, service design, software engineering, cloud and infrastructure, operations, governance/risk/compliance, cyber security, SABSA security architecture, data/AI, testing, delivery and sourcing.

## What “Unified Lifecycle” means

The release does **not** mean that one AI model autonomously owns the entire lifecycle. It means that the major production subsystems share JAI semantic identity, release namespace and traceability rules:

- Artifact Contract v3 writes current JAI-bound artefacts;
- SABSA objects are profile-native at source;
- EA is an architecture-domain projection, not a competing global truth store;
- Publication requires a projection manifest and carries JAI lineage;
- Runtime Agent/Policy/Execution records are JAI-bound;
- historical 26.10.0–26.10.3 data remains forward-migratable.

## What it is not

AI IT House does **not** replace accountable human roles and does **not** guarantee arbitrary natural-language truth. A structurally complete, well-reviewed record can still rest on a bad requirement, incorrect source observation or mistaken expert judgement.

The platform also does not claim that every possible direct role invocation is automatically forced through a `/layered` episode. The full Fabric supervision mechanism is strongly enforced **once that path is used**. Organisations requiring layered-by-construction for every consequential task should enforce that classification/routing at their entry boundary.

## Why “Universal” is fair but bounded

The platform spans a broad set of IS/IT working contexts and output types. “Universal” should be read as broad enterprise applicability and shared governance/runtime mechanisms — not as unlimited autonomy, infallibility or automatic suitability for every environment.

<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../../"><small>← Previous · Home</small><strong>Home</strong></a>
  <a class="ai-next" href="../release-26-10-4/"><small>Next · Executive overview →</small><strong>What's new in 26.10.4</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
