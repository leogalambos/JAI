# Example: New service onboarding

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `new-service-onboarding` workflow recipe.
It is not an additional native slash command.

ACME is introducing a customer-notification service to operations. Alice is the receiving service owner and Bob leads delivery. Messages are delivered successfully in a demonstration, but operations still needs support ownership, alerting, recovery and a clear handover boundary.

The names and circumstances are fictional examples of common operating
practice. They do not describe an actual customer or executed engagement.

## Prepare a project workspace

Create `acme-service-introduction/` with `input/`, `working/` and `output/`.
Keep supplied records in `input/`, drafts in `working/` and the reviewed
handoff in `output/`. These are chosen destinations; ask JAI to report
its actual file paths rather than assuming fixed generated filenames.

Supply:

- service-design.md — service purpose, dependencies and expected service levels
- support-model.md — hours, contacts, access and escalation ownership
- runbooks/ — delivery failure, recovery, deployment and rollback drafts
- acceptance-evidence.md — dated results and outstanding readiness conditions

Add `PROJECT.md` with the question, accountable owner, exclusions and
handling rules. If a record is absent, list the gap and request it from
its owner. Narrow conclusions while it is missing; do not fill gaps with
plausible invented evidence.

## Run this scenario in the provider CLI

Follow the [installation guide](../getting-started/install.md) for the
appropriate JAI adapter, then start Claude Code or Codex in this project.
Enter the prompts below in that provider's conversation, not a shell.
Choose one provider and keep the same project conversation throughout.

Use the service-onboarding chain to prepare the operating handoff. The operational-readiness walkthrough examines readiness in more depth; this one emphasizes receiving ownership and support integration. Use the layered path for decisions that alter accountability, service targets or release risk.

Ask for actual report paths, findings ledgers and engagement identifiers.
Inspect them between stages. Use `<reported-review-target>` for the actual
artifact path that JAI reports; do not type that placeholder literally. Replace `<reported-ledger>` below with the
ledger actually returned by review; the placeholder is not a real ledger.

### 1. Understand the service to be received

=== "Claude Code"

    ```text
    /analyse input/ for notification-service onboarding. Identify receiving roles, dependency owners and missing operating evidence. Keep delivery demonstration separate from acceptance.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for notification-service onboarding. Identify receiving roles, dependency owners and missing operating evidence. Keep delivery demonstration separate from acceptance.
    ```

Inspect the boundary between message acceptance and actual delivery. A success response may only mean a message entered a queue. Ask Bob how failures reach the support team and whether personal information could appear in logs or support tickets.

### 2. Frame the introduction

=== "Claude Code"

    ```text
    /layered Prepare the service-onboarding plan for the notification service. Identify required handoffs, receiving-owner decisions, support access and unresolved acceptance conditions.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the service-onboarding plan for the notification service. Identify required handoffs, receiving-owner decisions, support access and unresolved acceptance conditions.
    ```

Check whether proposed responsibilities have actual named receiving owners. A delivery team's promise to write a runbook later does not establish operational capability. The plan should distinguish service introduction from the authority to launch a particular production release.

### 3. Set handover criteria

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set onboarding review criteria covering support ownership, incident routing, access, monitoring, runbooks and evidence of readiness. Preserve unperformed checks.

Confirm the criteria shown by review before allowing assessment to start.

Read the criteria with a new on-call operator in mind. Can that person identify a stuck queue, reach a dependency owner and stop repeated notifications? A contact list alone does not establish support access or the ability to recover safely.

### 4. Review the handover material

=== "Claude Code"

    ```text
    /review <reported-review-target> the notification-service handover against the fixed criteria. Locate missing receiving-team evidence, unsafe procedures and unclear support boundaries.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the notification-service handover against the fixed criteria. Locate missing receiving-team evidence, unsafe procedures and unclear support boundaries.
    ```

Inspect whether the runbook explains what to do when a supplier endpoint is unavailable. A procedure that simply says 'retry' may amplify duplicate messages. Keep untested recovery steps visible and ask the receiving team for an authorized rehearsal where needed.

### 5. Rework the receiving packet

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework the open onboarding findings using actual owner responses and results. Prepare a proposed operating handoff under output/ without claiming acceptance.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework the open onboarding findings using actual owner responses and results. Prepare a proposed operating handoff under output/ without claiming acceptance.
    ```

Inspect the final responsibility map, procedures and outstanding actions together. A finding about missing support access closes with evidence of appropriate access and verification, not with a sentence in the handover. Alice's actual acceptance remains separate from AI review.

## Handle an escalation or changed evidence

Suppose the receiving team cannot support the proposed overnight service. Alice's example reply is: “Prepare a daytime-only introduction and identify queued-message behavior outside those hours. Overnight support is not accepted.” Resume with `/layered` or `$workflow-layered` to revise the proposed service boundary and customer implications. Do not rewrite the target as achieved or appoint Bob's delivery team as an unagreed permanent support team.

Resume the existing engagement with its actual identifiers when one is
active. A conversational reply can clarify or restrict work; it does not
replace a signed L0 act. If the runtime requires an authority operation,
the authorized human follows the exact instruction emitted through the
trusted authority path. Do not invent a substitute approval command.

If review finds that the escalation route leads to an unattended mailbox, use `/rework` or `$workflow-rework` with the reported ledger to obtain and verify a usable route. If the service later adds urgent fraud notifications, revisit scope and support criteria. Evidence adequate for routine messages may not support the new consequence of delay.

## Know when to stop

Finish with a reviewed operating handoff, receiving-owner decisions, support integration evidence and an explicit list of open readiness conditions. Use the dedicated readiness guide when a launch decision needs deeper evidence. Mark rehearsals or access checks NOT_EXECUTED unless performed, and never equate document completion with service acceptance.

The **Service onboarding** chain in the
[enterprise workflow catalogue](../reference/workflows.md) describes the
roles and handoffs behind this example. It is a workflow recipe, not an
additional slash command. Authors do not verify their own findings. The
example has not been executed as part of this guide.
