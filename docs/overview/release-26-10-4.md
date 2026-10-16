# What's new in 26.10.4

AI IT House **26.10.4 — Unified Lifecycle GA** completes the convergence work that began after the 26.10.0 Enterprise GA baseline. The release deliberately adds no new roles, workflows or artefact classes. Its purpose is to make the existing capabilities operate against one normative Justifiable AI (JAI) architecture and one current production-write namespace.

## Release identity

Production versions use `YY.MM.VV`: year, month, and version within the month. The lifecycle target that had previously been planned as `26.11.0` was completed during October and is therefore released as **26.10.4**.

| Release | Purpose |
| --- | --- |
| 26.10.0 | Enterprise GA baseline |
| 26.10.1 | JAI architecture convergence |
| 26.10.2 | Native JAI enforcement |
| 26.10.3 | Unified-lifecycle hardening |
| **26.10.4** | **Profile-native Unified Lifecycle GA** |

## What changed materially

### JAI is the normative architecture

The six JAI layers are the single top-level architecture for AI IT House. **L0 Human Authority remains external to JAI**; it is an authority boundary, not a seventh AI layer.

Artifact, SABSA, EA, Publication and Runtime now operate as scoped profiles or enforcement mechanisms of the JAI core. A subsystem may be authoritative only for its declared domain. For example, the EA repository is authoritative for the **EA-domain projection**, while JAI owns global semantic identity.

### Native writes use 26.10.4

The current schema registry and Artifact Contract v3 write only into the `26.10.4` namespace. Releases 26.10.0–26.10.3 remain readable and forward-migratable. Historical records are preserved rather than rewritten.

### SABSA is profile-native at source

New or modified SABSA objects persist canonical JAI semantic references and JAI L2 profile metadata. SABSA coordinates remain orthogonal to JAI layers: a SABSA layer/question is not inferred from a JAI layer number.

### Runtime evidence is profile-native

Agent Contracts embed JAI responsibility bindings, managed policy declares the JAI runtime profile, and new Execution Records are JAI **L6 Execution and Evidence** records in the tamper-evident execution chain.

### Publication is profile-native end to end

Production rendering requires a matching ProjectionManifest v3. The manifest binds L1–L6 lineage, semantic source, projection and render identity. Rendering emits evidence containing output hashes and QA outcomes.

### Layered enforcement has an explicit routing boundary

The six-layer JAI core is the normative architecture and `/layered` enforces the supervised contract/review/rework/escalation cycle once a layered engagement is opened. **26.10.4 does not claim that every direct role invocation is automatically forced through that Fabric path.** Deployments that require all consequential work to be layered-by-construction must enforce consequential-task classification and routing at the entry boundary.

This distinction keeps the release claim narrower than the research ambition: the shipped Fabric is strongly supervised, while universal mandatory entry routing remains a deployment control.

### Behavioral qualification no longer overclaims

Gate G distinguishes two different things:

- the **universal release** qualifies the behavioral harness, golden corpus, thresholds and adversarial evaluator;
- a **specific provider/model** is not declared qualified merely because packaged reference fixtures pass.

A live provider/model claim requires captured live results plus a typed qualification-evidence manifest.

## Corrective repack

The final 26.10.4 distribution also corrects release-identity drift found after the first build. `roles.json`, `workflows.json`, current EA operator wording and the current EA schema title now agree with `VERSION=26.10.4`. Historical `26.10.3` references remain where they identify a migration source, schema namespace, compatibility input, changelog entry or audit record.

The corrected distribution remains **26.10.4** because this was a corrective repack of the same functional release, not a new version.

## Current generated inventory

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

## Qualification status

The packaged `QUALIFICATION-A-H.json` reports **A–H = 8/8 PASS**. The distribution state is `ready-for-release-owner-signature`; the build deliberately does not contain or use the release owner's private signing key.

See [Validation and release controls](../operations/validation.md) for the gate details and [26.10.4 release and migration](../reference/release-migration.md) for compatibility rules.
