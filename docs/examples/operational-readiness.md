# Assess readiness to operate a service

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `design-to-operational-readiness` workflow recipe.
It is not an additional native slash command.

ACME is preparing a new supplier-ordering API for service. Alice owns operations and Bob leads delivery. A feature demonstration has passed, but operations needs to know who responds at night, how recovery works and what dependencies can stop the service.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-readiness/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- service-design.md — service boundaries, targets and dependency owners
- runbooks/ — incident, recovery, deployment and rollback procedures
- test-results/ — dated load, backup and restoration results actually available
- readiness-scope.md — intended release, operating hours and receiving team

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use analysis and a fixed readiness review to expose missing operating evidence. Use the layered workflow to frame a go-live decision with its unresolved conditions. JAI can prepare the decision packet; it cannot become the receiving operations owner.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding.
Replace `<reported-review-target>` with the actual readiness evidence input
path you selected for review; analysis and criteria creation do not produce
a readiness assessment draft automatically.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Establish the service boundary

=== "Claude Code"

    ```text
    /analyse input/ for the ordering API's operational readiness. Identify dependencies, support boundaries and absent evidence. Do not infer a successful recovery from a backup schedule.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for the ordering API's operational readiness. Identify dependencies, support boundaries and absent evidence. Do not infer a successful recovery from a backup schedule.
    ```

Inspect whether the service map includes identity, messaging, supplier endpoints and monitoring ownership. A runbook referring to a team that no longer exists is an actionable handover gap. Ask Alice which team actually receives alerts and holds the necessary access.

### 2. Set readiness criteria

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set operational-readiness criteria for the release in input/readiness-scope.md. Cover monitoring, support, recovery, capacity, security dependencies and change rollback.

Confirm the criteria shown by review before allowing assessment to start.

Read the criteria with the intended operating hours in mind. A weekday support arrangement cannot silently satisfy a round-the-clock target. Distinguish a documented procedure, an exercised procedure and a demonstrated recovery time; they require different evidence.

### 3. Review the operating evidence

=== "Claude Code"

    ```text
    /review <reported-review-target> the supplied readiness materials against the agreed criteria. Record each unresolved prerequisite and the evidence required to close it.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the supplied readiness materials against the agreed criteria. Record each unresolved prerequisite and the evidence required to close it.
    ```

Inspect dated results and the environment they describe. A restoration test against a small developer dataset may not support the production recovery target. Ask for the measured data size and restore duration rather than treating a PASS label as sufficient.

### 4. Prepare the go-live decision

=== "Claude Code"

    ```text
    /layered Prepare a bounded readiness decision for the ordering API. Present unresolved recovery and support conditions, options to defer or limit launch, and named receiving owners.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare a bounded readiness decision for the ordering API. Present unresolved recovery and support conditions, options to defer or limit launch, and named receiving owners.
    ```

Check whether conditions have deadlines and a way to verify closure. A condition phrased 'operations will handle this' hides both ownership and evidence. Keep business launch pressure visible as context without turning it into authority to accept unmeasured recovery risk.

### 5. Close findings and hand over

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework readiness findings using actual new evidence. Prepare the receiving-service handoff under output/, preserving any conditions that remain open.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework readiness findings using actual new evidence. Prepare the receiving-service handoff under output/, preserving any conditions that remain open.
    ```

Read the handoff as the on-call operator would: which signal triggers action, where the procedure is and who can authorize rollback. If the receiving team has not accepted ownership, keep that status explicit. Document preparation does not constitute service acceptance.

## Handle an escalation or changed evidence

Suppose a database restore exceeded the target and the launch date is fixed by a customer event. Alice's example reply is: “Prepare a limited launch option with no critical orders and a clear stop condition. Recovery readiness remains open; I have not accepted the full service.” Resume with `/layered` or `$workflow-layered` to compare the limited launch with deferral. The reply is an input to the decision record, not an automatic go-live approval.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review finds a rollback procedure that would discard accepted orders, use `/rework` or `$workflow-rework` to revise the plan and request an appropriate rehearsal. If the business adds overnight operation, update scope and criteria before reviewing again. Previously adequate staffing evidence no longer covers the changed service.

## Know when to stop

The result should state ready, conditionally proposed or not ready against supplied evidence, with each missing check marked NOT_EXECUTED. Preserve test identities, observations and receiving-owner decisions. Production deployment, restored service and signed acceptance require their own actual records.

Use the **Operational readiness** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
