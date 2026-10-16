---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# How to use JAI

Start with the method, choose what must be justified, and then follow a worked case. JAI's commands select procedures; they are not interchangeable shortcuts to an automatically approved result. This learning path keeps the explanation beside the cases that demonstrate it.

## 1. Learn the method before choosing a command

Read [Choosing and running a methodical workflow](../../using/methodical-workflows.md) first. It explains the three valid arrangements:

| Arrangement | What you ask JAI to establish | Worked illustration |
| --- | --- | --- |
| Direct domain workflow | A domain model, its sources, domain checks and independent review | [Security assessment](security-assessment.md) |
| Domain work followed by a layered decision | Whether an exact existing model and other evidence support a new decision | [Android development and release](android-development.md) |
| Layered creation with a named domain | The justification of the creation process itself, through L1–L6 contracts, evidence and review | Alternatives at the beginning of both cases; [proposal creation](../../capabilities/commercial-delivery.md#worked-proposal-from-discovery-to-bid-decision) |

These arrangements answer different questions. A later `/layered` decision does not retroactively turn earlier `/sabsa` work into a layered creation history. Conversely, a direct `/sabsa` workflow already has architect/reviewer separation: the absence of `/layered` does not mean the absence of all review.

Next read [Interaction patterns](../../using/interaction-model.md) for provider syntax and operator responsibilities. If you choose a layered arrangement, [Running a layered engagement](../../using/layered-engagement.md) explains the complete cycle, including unsuccessful work and human authority.

## 2. Work through a complete case

### Security assessment: stop at a reviewed assessment

[Assess a deployed system with SABSA](security-assessment.md) follows `/sabsa` from business drivers to a reference architecture, observed deployment, findings and a transformation roadmap. Its main exercise stops at assessment and architecture-owner approval; it does not make a formal release or risk-acceptance decision. That scope explains why its main sequence uses `/sabsa` rather than `/layered`. An optional decision extension shows where to introduce the latter if needed.

### Android: build, reconcile, then ask a new release question

[Keep Android development aligned with SABSA](android-development.md) uses `/sabsa` for architecture, `/develop` for a bounded code increment, and `/layered` in step 7 for release readiness. The last step is a new consequential question using the architecture and actual implementation evidence. It does not certify the history of the preceding authoring work.

### Commercial proposal: discover, estimate and expose commitment risk

[Commercial delivery](../../capabilities/commercial-delivery.md#worked-proposal-from-discovery-to-bid-decision) develops a supplier proposal with incomplete service volumes, staged estimates, staffing and separate internal/client views. It shows direct commercial preparation followed by a bid decision, as well as the alternative of layered creation from the start. Its provider-qualification limits remain explicit.

Each case explains its chosen arrangement before presenting commands. Choose an alternative **before** production begins if your policy requires the creation process itself to be layered.

## 3. Continue with the reference you actually need

| Your next question | Read |
| --- | --- |
| Which conversation command or Codex skill should I use? | [Commands and direct tools](../../using/commands.md) |
| Which enterprise stages, roles and handoffs apply? | [Workflow library](../../using/workflows.md) |
| What should the output contain, and how is it published? | [Working with deliverables](../../using/deliverables.md) |
| How can I practise without using a real client system? | [Demo estate](../../using/demo-estate.md) |
| Which domain capabilities and technical boundaries exist? | [SABSA and EA](../../capabilities/sabsa-ea.md), [Commercial delivery](../../capabilities/commercial-delivery.md), [Layered runtime](../../capabilities/layered-runtime.md) |
| What may only the human decide? | [Human authority and escalation](../../operations/human-authority.md) |

The [quick start](../../getting-started/quick-start.md) is a short installation smoke tour. The [command walkthroughs](../../reference/command-walkthroughs.md) are individual reference exercises. Neither replaces the end-to-end methodology and cases in this learning path.

## Teaching and validation status

The cases are fictional teaching exercises, not executed provider transcripts, customer assessments or successful release records. Their commands describe requested work and expected artefacts. Repository checks can validate links, syntax and deterministic fixtures; they do not establish live provider isolation, completed reviews or human authority. Request actual evidence and state identifiers in each real engagement.
