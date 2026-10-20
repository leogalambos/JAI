# Enterprise workflows

The enterprise library contains **24 named workflows**. A workflow connects
roles, stages, gates and outcomes. Use this chooser after selecting your
assurance arrangement in [How to use JAI](../examples/how-to-use-JAI/index.md).
The `/commercial` extension adds supplier-side coordination; it is distinct
from these enterprise chains and their buyer-side sourcing processes.

## Choose by the outcome you need

Use this short chooser to find a starting case. For all 24 chains, exact
stage counts and registered outcomes, use the generated
[workflow reference](../reference/workflows.md). Each chain retains its
detailed page with role hand-offs, gates and an operating prompt.

| Your task | Start here |
| --- | --- |
| Deliver a new product, data product or AI system | [Commented task walkthroughs](../examples/index.md), then the matching delivery chain in the workflow reference. |
| Assess or improve an inherited system | [Inherited codebase](../examples/inherited-codebase.md) or the relevant assessment case. |
| Restore service, remove a vulnerability or validate recovery | Select incident, vulnerability or resilience work from [commented task walkthroughs](../examples/index.md); retain its evidence and emergency boundaries. |
| Prepare a supplier proposal or select a supplier | [Proposal](../examples/proposal.md) for supplier-side work; the workflow reference's sourcing and supplier chains for buyer-side work. |
| Govern architecture, access, change or release | Choose the corresponding chain in the [workflow reference](../reference/workflows.md). |
| Publish an approved semantic artefact | [Enterprise publication](../examples/enterprise-publication.md). |
| The task spans several outcomes or remains unclear | Ask experimental `/hint` or `$workflow-hint`; inspect its sources and assumptions before proceeding. |

Choose the assurance method separately through
[Methodical workflows](methodical-workflows.md). A workflow title describes
the intended outcome; it is not a claim that approval or execution occurred.

## Operator interaction versus workflow execution

**You:** describe the needed outcome, name the workflow if known, provide the repository or source material, state the accountable decision owner and ask for the current gate. This is a request **inside Claude or Codex CLI**, not a terminal command. For example, in either provider:

```text
Use the migration-and-cutover workflow for our ERP replacement. First identify the current stage, mandatory inputs, unresolved dependencies, evidence gaps, acceptance owner and go/no-go decision. Do not change production or approve a waiver without explicit authority.
```

**The provider agent:** uses the workflow and role registries to plan stages, allocate role-specific work, call permitted tools, preserve evidence and present gate outcomes. A workflow definition is a **governed method**, not proof that downstream tools, approvals or integrations have run. If a task is consequential, use the explicit `/layered` or `$workflow-layered` entry point; the current router does not force every natural-language workflow request through Fabric.

**Human accountable roles:** supply evidence and decide on approval, risk acceptance, production change, legal obligations and other reserved business actions. Provider instructions and workflow metadata cannot substitute for those decisions.

Use the grouped **Workflow library** in the navigation to open any of the 24 detailed chains. The pages specify **what the agent should coordinate** and **which human role remains accountable**; they are not 24 separate executable shell scripts. [Source to contract to service](../workflow-library/source-to-contract-to-service.md) and [Supplier onboarding](../workflow-library/supplier-onboarding.md) describe buyer-side obligations. Use [Commercial delivery](../capabilities/commercial-delivery.md) when you are the supplier preparing and delivering a proposal.

## How to use workflows

Ask explicitly for the workflow you want, or describe the situation so the system can select one.

### Example

> Use the `migration-and-cutover` workflow for our programme. Show the next gate, the accountable role, mandatory inputs, missing evidence and the artefacts required before cutover approval.

## Why workflows are better than ad-hoc prompts

A role tells the system **who** is relevant. A workflow tells it **how** the work should move and **where** the governance gates are.
