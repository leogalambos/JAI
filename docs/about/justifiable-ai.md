# Justifiable AI

AI IT House's layered delivery capability is informed by:

**Leo Galambos, _Towards Justifiable AI Systems: A SABSA-Driven Methodology for Self-Monitoring, Auditable and Conditionally Assured Agentic Systems_ (2026)**  
[DOI: 10.13140/RG.2.2.29244.19843](https://doi.org/10.13140/RG.2.2.29244.19843){ target="_blank" rel="noopener" }

## Research idea in plain terms

The central architectural problem is not whether an AI answer sounds persuasive. It is whether the organisation is **entitled to use** a candidate for a specified purpose under current evidence, policy and authority.

The paper therefore separates generation from evidence, review, authority and release. Requirements flow downward; evidence, disagreement and operating feedback flow upward. Missing observations or unresolved dissent are intended to change system behavior — request more evidence, return work, escalate, invalidate or block — rather than appear only in an audit log after the fact.

## Six responsibilities, not six mandatory model calls

The paper proposes six architectural responsibilities that AI IT House adopts as its JAI core:

| Layer | Responsibility |
| --- | --- |
| L1 | Intent and Context |
| L2 | Meaning and Domain Model |
| L3 | Reasoning, Policy and Control |
| L4 | Solution Design |
| L5 | Realisation and Tooling |
| L6 | Execution and Evidence |

A layer is an abstraction and accountability boundary. It may contain several agents, deterministic validators and human specialists. The design does not assume that a higher layer is technically more competent, nor that six separate LLM invocations are inherently safer.

## What JAI operationalises

AI IT House implements a production-specific interpretation of the architecture using:

- canonical JAI layer, authority and relation registries;
- six layer agents used inside layered engagements;
- typed adjacent-layer contracts;
- context-digest binding;
- bottom-up review before upward promotion;
- explicit evidence/failure/conflict records;
- bounded rework and requirement reformulation;
- upward-only escalation to external L0 Human Authority;
- append-only hash-chained Fabric records;
- strict release checks and dependency invalidation;
- managed authority hooks and provider adapters.

The implementation uses a deterministic Python supervision runtime rather than embedding the paper's illustrative Prolog core.

## What it does not prove

The paper itself is a methodology/research-programme contribution, not a report of a validated production system. Conversely, the existence of a runtime implementation does not automatically prove its semantic quality in every domain.

Keep four assurance levels separate:

1. **auditability** — can the relevant course of events be reconstructed?;
2. **structural eligibility** — do the finite records satisfy an encoded release policy?;
3. **substantive assurance** — are requirements, decomposition, evidence and argument actually valid?;
4. **operational control** — can release/action occur only through the authorised path in the deployment?

The current release contains strong controls for the first two and selected mechanisms for the fourth. The third remains dependent on evidence quality, domain competence and empirical evaluation; the fourth remains deployment-dependent wherever provider/host/tool bypass is possible.

## Why human authority remains outside JAI

An agent may recommend a risk exception but cannot make the responsible person's decision true by writing the word “approved.” L0 is deliberately external so that the system can prepare and constrain a decision without impersonating the authority that owns it.

Human approval is also not a truth oracle: it can authorise a bounded use or accept a stated residual risk, but it cannot transform incorrect technical evidence into a fact.

## Further reading in this documentation

- [Layered runtime and assurance model](../capabilities/layered-runtime.md)
- [Running a layered justifiable engagement](../using/layered-engagement.md)
- [Justifiable Fabric](../capabilities/justifiable-fabric.md)
- [Human authority and escalation](../operations/human-authority.md)
- [Boundaries and limitations](../reference/limitations.md)
