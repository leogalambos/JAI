# Commented task walkthroughs

Owner: JAI maintainers. Last reviewed: 2026-10-20.

Start here when you know the task but do not yet know which JAI commands
to use. Each walkthrough explains a plausible problem, the documents to
supply, a sequence of provider prompts, what to inspect and how to respond
when evidence or scope changes. The examples use fictional ACME teams,
Alice and Bob in settings drawn from common public business practice.
They are not case studies, executed traces or claims about real entities.

## Choose a starting task

For a first exercise, choose the closest business question rather than
the most impressive output format:

- A customer needs a credible offer: start with the
  [commercial proposal](proposal.md).
- You need security architecture for a service: start with
  [SABSA development](sabsa-development.md).
- You need to assess an existing deployed system: use the
  [security assessment](how-to-use-JAI/security-assessment.md).
- A test fails intermittently: use
  [incident diagnosis](incident-diagnosis.md).
- Your team must receive a new service: compare
  [service onboarding](service-onboarding.md) with
  [operational readiness](operational-readiness.md).
- You need to understand unfamiliar source before committing to changes:
  use [codebase takeover](inherited-codebase.md).

The coverage table below maps all 24 enterprise workflow recipes to a
primary walkthrough. Five additional guides cover proposal, SABSA,
assessment, an architecture board and a general consequential decision:
29 commented walkthroughs in total. A mapping illustrates a recipe; it
does not claim that every action in that recipe runs automatically.

## Prepare the workspace before asking for outputs

To practise with fictional inputs, use `/demo scenarios` or
`$workflow-demo scenarios` to discover all 29 scenario IDs. For example:

```text
/guide proposal
/demo describe proposal --step 1
/demo scenario proposal --to /tmp/acme-proposal
```

The Codex equivalents are `$workflow-guide proposal`,
`$workflow-demo describe proposal --step 1` and
`$workflow-demo scenario proposal --to /tmp/acme-proposal`. Only the
existing `/guide` and `/demo` commands are needed for this assistance.
Open the active AI CLI in the new directory and read `START.md`.
Description explains the steps without running them; workspace creation
adds fictional inputs without executing workflows or granting approval.

The starter packs use an `inputs/` directory. Some guides use `input/`
or show PDF, spreadsheet, model and application-source examples: the
packs provide labelled text derivatives and name the actual seeded
paths in their prompts. They do not fabricate binary documents, source
checkouts or successful tests. Supply permitted real inputs separately
when trying the full task. Stop at missing evidence, independent review
or human authority, then resume only after the requirement is satisfied.
Choose a new destination and preserve existing work; resetting is an
explicit operation with backup safeguards.

Follow the [installation guide](../getting-started/install.md) for your
provider. Create a new project directory for the task, then start Claude
Code or Codex there. Each guide specifies its own input documents and
working layout. A typical layout separates original inputs, draft work
and reviewed outputs; use the names stated in that guide, not an assumed
universal generated folder structure.

Write a short `PROJECT.md` that states the question, scope, accountable
owner, confidentiality and exclusions. Provide dated documents with
recognizable purpose. A service design, actual restoration result and
supplier obligation answer different questions. Do not replace a missing
record with a fictional “representative” result and then cite it as fact.

Use sanitized material for learning. In real work, retain project handling
rules and avoid exposing customer data in widely distributed documents.
The example prompts have not been run for you. Their deliverables and
checks are proposed until your actual session produces evidence.

## Read command pairs correctly

The Claude examples use slash commands such as `/analyse`. Codex examples
use the corresponding installed skill, such as `$workflow-analyse`.
Enter them in the provider conversation, not in a terminal shell. Choose
one provider column; the pairs are alternatives, not two mandatory runs.

Enterprise workflow names such as `production-change` describe role and
handoff recipes. They are not extra native commands: there is no generic
`/assessment`, `/release` or slash command for every catalogue key. State
the intended workflow and task in the supported command's request. Use
[commands and direct tools](../using/commands.md) for the actual entry
points, and the [workflow catalogue](../reference/workflows.md) for the
roles and handoffs behind them.

A path shown as `<reported-review-target>` or `<reported-ledger>` must be
replaced with the actual path or identifier returned in your session.
Do not type the angle-bracket placeholder literally. Ask JAI to report
its created files and identifiers, then inspect them before continuing.
A prompt naming a desired output directory does not guarantee a fixed
filename or prove that an artifact was generated successfully.

## Understand the normal pauses

Analysis establishes what is present and what is unknown. Criteria fix
how the material will be assessed. `/criteria .` or
`$workflow-criteria .` displays or initializes criteria for the current
project; discuss task-specific criteria explicitly. It does not run the
review or certify that the project satisfies them.

The review workflow displays the criteria source and hash and waits for
your explicit confirmation before the reviewer reads the target. Read
that material and answer the requested confirmation when it matches the
task. This pause is expected: it prevents a reviewer from inventing the
criteria after seeing the work. A changed criterion requires a visible
change, not quiet reinterpretation of an inconvenient finding.

A review can return findings. Use the actual ledger in `/rework` or
`$workflow-rework`, then require verification by the appropriate reviewer.
An author correcting text or code does not verify that correction. A
failed check may be useful evidence; preserve its result and explain the
next action instead of retrying until the record looks favorable.

An escalation is also useful output. It can identify missing evidence,
conflicting requirements, unclear ownership or a decision reserved for a
human. Reply with the requested evidence or a bounded scope decision,
then continue the existing engagement with its actual identifiers. Do
not start a fresh conversation merely to bypass an unresolved blocker.

Where the runtime requires a signed external L0 authority act, an ordinary
chat reply is insufficient. The authorized human must follow the exact
instruction the runtime emits through the trusted authority path. The
guides intentionally do not invent a universal approval command.

## Select the right assurance arrangement

Domain work does not always require a fresh six-layer engagement. An
assessment can remain an assessment, and a local diagnosis can remain a
bounded defect investigation. The walkthroughs explain why a particular
entry point is useful at that stage. Use the layered path when the task
needs the explicit consequential decision and evidence chain described
in [layered engagement](../using/layered-engagement.md).

The execution layers L1–L6 do not replace external L0 human authority.
Role routing also differs from provider model routing. Expert references
can help an author understand an artifact's structure, but they are not
project evidence or approved business facts. See
[execution and context assembly](../overview/execution-context-algorithm.md)
for the implementation and procedural boundaries.

Publication needs its own care. `/publish` and `$workflow-publish` use the
supported approved semantic snapshot and registered publication profile;
an arbitrary Markdown file is not automatically eligible. New rendered
outputs can remain draft or incomplete. A successful render establishes
neither semantic approval nor actual independent human review. Keep
unavailable rendering or runtime checks NOT_EXECUTED.

## Coverage of the enterprise workflows

| Workflow recipe | Primary walkthrough | Boundary to keep visible |
| --- | --- | --- |
| `idea-to-production` | [Build an Android application](how-to-use-JAI/android-development.md) | Domain design and local development; store publication and production acceptance need separate evidence. |
| `new-service-onboarding` | [Introduce a service](service-onboarding.md) | Operating handoff; receiving ownership is not created by writing a runbook. |
| `production-change` | [Prepare a production change](production-change.md) | Reviewed change packet; no authority to execute production commands. |
| `incident-to-problem` | [Diagnose an intermittent defect](incident-diagnosis.md) | Local reproduction and bounded correction; production impact remains separately evidenced. |
| `vulnerability-to-remediation` | [Remediate a dependency](vulnerability-remediation.md) | Applicability and a local patch; no automatic estate scan or deployment. |
| `codebase-takeover` | [Take over inherited code](inherited-codebase.md) | Evidence-based takeover; does not justify an unsolicited rewrite. |
| `access-request-to-review` | [Review service access](access-review.md) | Entitlement assessment; human certification and access changes remain separate. |
| `data-product-delivery` | [Deliver a data product](data-product-delivery.md) | Purpose, quality and ownership; no invented data or operating results. |
| `ai-system-approval` | [Prepare an AI-system decision](ai-system-approval.md) | Evidence and approval packet; AI output cannot grant deployment approval. |
| `supplier-onboarding` | [Onboard a supplier](supplier-onboarding.md) | Receiving-service boundary; supplier acceptance requires actual responses. |
| `business-case-to-benefits` | [Develop a business case and benefits plan](business-case-benefits.md) | Assumptions and measurement; forecast savings are not realized benefits. |
| `design-to-operational-readiness` | [Assess operational readiness](operational-readiness.md) | Launch evidence and receiving conditions; no automatic go-live decision. |
| `migration-and-cutover` | [Plan a cloud migration](cloud-migration.md) | Cutover and recovery preparation; execution requires its own authorization. |
| `organisational-change-and-adoption` | [Introduce a working practice](adoption.md) | Learning and feedback; attendance does not prove effective adoption. |
| `semantic-to-enterprise-publication` | [Publish an enterprise document](enterprise-publication.md) | Approved semantic snapshot and registered profile; rendering is not approval. |
| `architecture-model-to-repository-governance` | [Maintain an architecture repository](architecture-repository.md) | Stable model identity and review; diagrams do not establish new model facts. |
| `service-retirement-and-decommission` | [Retire a service](service-retirement.md) | Dependencies and records obligations; shutdown is not permission to delete. |
| `cyber-incident-breach-to-recovery` | [Coordinate cyber recovery](cyber-incident.md) | Bounded recovery and evidence; no unsolicited offensive activity. |
| `resilience-validation` | [Prepare a resilience exercise](resilience-validation.md) | Exercise scope and observations; tabletop discussion is not a recovery measurement. |
| `demand-to-portfolio-to-funding` | [Prepare a funding decision](demand-funding.md) | Demand and portfolio evidence; recommendation does not allocate money. |
| `source-to-contract-to-service` | [Source a service](sourcing-contract.md) | Evaluation and service handoff; no automatic supplier selection or contract signature. |
| `siam-multi-supplier` | [Integrate several suppliers](siam-multi-supplier.md) | End-to-end coordination; proposed service levels do not amend contracts. |
| `enterprise-release-orchestration` | [Prepare an enterprise release](enterprise-release.md) | Cross-service readiness; does not rerun or replace JAI's own release pipeline. |
| `regulatory-change-to-assurance` | [Respond to a regulatory change](regulatory-change.md) | Obligation-to-evidence work; drafting is not legal advice or regulator acceptance. |

## Additional domain and decision guides

| Guide | Use it when | What it does not establish |
| --- | --- | --- |
| [Commercial proposal](proposal.md) | Customer discovery, evidence, assumptions and offer preparation need a coherent sequence. | Customer acceptance, approved pricing or permission to send an offer. |
| [SABSA development](sabsa-development.md) | Business drivers must become traceable security architecture. | An approved standard or implemented controls merely because entries exist. |
| [Security assessment](how-to-use-JAI/security-assessment.md) | An existing deployed system needs an evidence-based assessment. | Control effectiveness when operating evidence is absent. |
| [Architecture Review Board pack](architecture-board.md) | A board needs a decision-ready account of options and implications. | A board decision or signed architecture exception. |
| [Consequential decision](justifiable-decision.md) | You need the general layered pattern with explicit authority boundaries. | Human authority created by agent consensus. |

## Finish with a useful handoff

Before calling the task complete, identify what was produced, what was
actually checked, which findings remain and who acts next. Distinguish
AI-authored proposed material, independently reviewed material and
human-approved decisions. Keep evidence identifiers and current scope
with the handoff so the next person can understand its limits.

Continue with [methodical workflows](../using/methodical-workflows.md)
for choosing an approach, [deliverables](../using/deliverables.md) for
artifact handling and [interaction patterns](../using/interaction-model.md)
for the distinction between conversation, tools and runtime state.
