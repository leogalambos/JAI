---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# How to use JAI: worked learning guides

JAI helps you organise substantial work around a clear outcome, explicit sources, independent review and evidence. These tutorials show how to steer that process: what to ask for, why the next step matters, what should be produced and when you need to make a decision.

Both scenarios are fictional teaching exercises using the current JAI workflow contracts. The [security assessment](security-assessment.md) compares a deployed system with business-driven security requirements. The [Android development guide](android-development.md) keeps architecture, implementation and release evidence aligned through small changes. Choose the one closest to your task; each is self-contained.

## Understand the working parts

A **workflow** coordinates the work. A specialist **author** creates architecture or implementation artefacts. A different **reviewer** assesses the result and verifies rework. Deterministic **tools** check structure, trace dependencies and generate publications. The **human owner** decides matters such as scope, risk acceptance and final authority.

This separation gives you useful questions to ask at every stage: which source supports this claim, who authored it, who reviewed it, which checks actually ran, and what remains undecided? A polished document is useful only when those questions have clear answers.

| Your task | Workflow | Main artefacts | Why use it |
| --- | --- | --- | --- |
| Establish a business-driven security architecture | SABSA | Sources, typed architecture entries, matrix answers and narrative chapters | Connect technical choices to business outcomes |
| Implement a bounded change | Develop | Reviewed code, tests and execution evidence | Keep implementation scope and acceptance criteria explicit |
| Make a consequential decision | Layered delivery | Contracts, evidence, reviews and escalation dossier | Show what supports the decision and where human authority is needed |
| Communicate reviewed architecture | SABSA document publication | Viewpoint documents and catalogue exports | Give readers usable views of the canonical source |

SABSA's six architecture viewpoints and JAI's six delivery layers serve different purposes. A SABSA coordinate describes an architectural perspective; a JAI layer describes a delivery responsibility. Their numbers are not interchangeable.

## Run this scenario in the provider CLI

Use the prompts in your existing Claude Code or Codex project conversation. They are conversation requests, not shell commands. Each tab contains one complete prompt for that provider; copy only the tab you use.

Start with preparation because JAI needs the intended outcome and evidence before deriving requirements. You provide `PROJECT.md` and available sources. The SABSA workflow should organise those sources, ask about missing context and propose business drivers with explicit provenance.

**Expected output:** a source register, initial drivers and open questions. **Checkpoint:** the proposed scope and drivers describe your business need rather than a product chosen in advance.

=== "Claude Code"

    ```text
    /sabsa prepare project/sabsa — use project/PROJECT.md and the supplied
    sources. Establish the intended decision, scope and business drivers.
    Separate stated facts, justified inferences and assumptions, and show
    questions that must be resolved before requirements are treated as
    settled.
    ```

=== "Codex"

    ```text
    $workflow-sabsa prepare project/sabsa — use project/PROJECT.md and the
    supplied sources. Establish the intended decision, scope and business
    drivers. Separate stated facts, justified inferences and assumptions, and
    show questions that must be resolved before requirements are treated as
    settled.
    ```

**Operator:** provide material, inspect assumptions and make the decisions that belong to you. **Behind the scenes:** JAI routes authoring and independent review, invokes permitted tools and reports actual results. A workflow name or a generated file does not prove that a check ran. In Codex, protected authority actions are handed to the actual human as exact commands for a trusted terminal; the agent cannot impersonate that human.

## Learn the iterative pattern

Each tutorial uses the same pattern: establish intent, build a bounded part, inspect its evidence, review it independently, and reconcile changes before proceeding. You do not need to ask for the entire engagement in one prompt. Smaller stages make unsupported assumptions and inconsistent decisions easier to find.

| Learning goal | Security assessment | Android development |
| --- | --- | --- |
| Establish intent | Business exposure and assessment boundary | User benefit, privacy and failure consequences |
| Build the model | Requirements, then a reference realisation | Requirements, then an implementable increment |
| Use evidence | Compare observed deployment with the reference | Reconcile code, tests, device observations and architecture |
| Handle change | Findings and a transformation roadmap | Reviewed development increments and model updates |
| Reach a decision | Identify justified changes and unresolved exposure | Distinguish release evidence from remaining conditions |

## Choose a useful publication

The SABSA workflow uses Markdown by default. Ask naturally for another format when the audience needs it: a Logical Security Architecture as LaTeX and PDF, a Component Engineering Specification as Word, or editable CSV catalogues for structured maintenance.

The six viewpoint publications combine authored chapters with full element fields and bodies, provenance and typed business paths. Canonical Markdown entries and narrative chapters carry the meaning. Generated publications present it; missing decisions remain gaps. CSV supports export, validation and import of edits to existing local entries while retaining stable IDs and schema. It is an editable projection, not a second source of authority.

See [deliverables](../../using/deliverables.md), [publication dependencies](../../configuration/publication-stack.md) and [sandbox prerequisites](../../getting-started/sandbox-prerequisites.md) for the relevant output and access requirements.

## Teaching and validation status

These pages describe proposed exercises and expected artefacts, not executed provider conversations, customer assessments or Android release results. Repository documentation checks and deterministic examples are separate validation activities. In your engagement, request actual evidence for each claimed result and keep unperformed work visible.
