# SABSA and enterprise architecture

## SABSA support

The SABSA capability treats the architecture as a structured, traceable library rather than one monolithic report.

<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Architecture and delivery diagram">
<img src="../../assets/diagrams/sabsa-chain.svg" alt="SABSA traceability chain from business drivers through attributes, risk, controls, services, mechanisms and operational measures">
</div>

The release supports all **36 SABSA matrix cells** as projection-capable architecture content and maintains structured semantic types for the runtime.

## SABSA in the 26.10.4 JAI model

SABSA is a **profile of the JAI semantic core**, not a parallel global truth hierarchy.

A SABSA object can retain its own orthogonal coordinates, for example:

```text
SABSA: Conceptual / Why / objective
JAI:   L3 responsibility while evaluating the objective against policy/risk
```

The coordinates are intentionally not collapsed into each other. A SABSA layer/question is not inferred from the JAI layer number.

New or updated SABSA source objects in 26.10.4 persist a canonical JAI semantic reference and profile metadata. Legacy libraries remain readable and can be upgraded on write/migration.

## Operator request and implementation boundary

In a **Claude Code** session use the `/sabsa` and `/repository` commands shown below; in **Codex CLI** use `$workflow-sabsa` and `$workflow-repository` with the equivalent arguments. For example, ask for the `acme-pay` SABSA coverage questions and a traceable EA projection. These names are provider commands/skills, **not Python shell calls**. The provider performs permitted `sabsa.py`, `repository.py` and EA bridge operations and should report the resulting object IDs, validation status and open architecture questions. Approval remains bound to the current snapshot and authorised owner; asking the assistant to "approve" does not supply that authority by itself.

## Main commands

```text
/sabsa prepare <library>
/sabsa create <library>
/sabsa update <element> <library>
/sabsa review <library>
/sabsa suggest <library>
/sabsa questions <library>
/sabsa approve <library>
/sabsa approval <library>
/sabsa document <library> [as docx]
/sabsa template <library>
```

## Enterprise architecture repository

The EA repository is JSON-based, with ArchiMate/Open Exchange used as an interoperability boundary.

In 26.10.4 its authority is explicitly scoped:

```text
authoritative_for: ea-domain-projection
global_source_of_truth: false
semantic_identity_authority: JAI
```

That means the repository is authoritative for architecture-domain projection state, lifecycle, views, relationships and related EA governance; it does not create a second global identity for an object that already exists in JAI/SABSA semantics.

```text
/repository validate architecture-repository.json
/repository views architecture-repository.json all
/repository portfolio architecture-repository.json
/repository export architecture-repository.json model.xml
```

Legacy repository versions `26.10`, `26.10.1`, `26.10.2` and `26.10.3` are accepted for read/migrate; current writes use the JAI-scoped profile-native model.

## SABSA → EA projection

The intended direction is:

```text
JAI canonical semantic identity
        │
        ├── SABSA specialisation / coordinates
        │
        └── EA-domain projection
               │
               └── ArchiMate/Open Exchange interchange
```

The bridge preserves source specialisation and canonical references so that EA views remain traceable to the semantic origin rather than becoming an independent copy of the truth.

## Why this matters

Organisations often struggle to keep security architecture, enterprise architecture and published documents aligned. The 26.10.4 profile model gives each subsystem a clear scope while preserving stable identity and traceability across them.

<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../../workflow-library/regulatory-change-to-assurance/"><small>← Previous · Workflow library</small><strong>Regulatory change to assurance</strong></a>
  <a class="ai-next" href="../artifacts-publication/"><small>Next · Capabilities →</small><strong>Publication and visual QA</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
