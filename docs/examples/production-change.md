# Prepare a controlled production change

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `production-change` workflow recipe.
It is not an additional native slash command.

ACME needs to change API traffic routing from an old application pool to a new one. Alice is the change owner and Bob is the service operator. This walkthrough prepares and reviews the change; it does not use conversational commands to operate production.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-routing-change/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- change-request.md — purpose, release identity, window and service owner
- routing-map.md — current and intended routes and dependent clients
- rehearsal-results.md — actual staging observations and known differences
- rollback-plan.md — reversal steps, limits and decision authority

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use the layered workflow because a production change connects business intent, technical design and execution evidence. Review the proposed runbook independently. Local analysis is useful, but it cannot substitute for an authorized production operator or the change authority.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Understand the current route

=== "Claude Code"

    ```text
    /analyse input/ for the traffic-routing change. Identify client paths, stateful dependencies and differences between staging and production. Keep production execution outside this task.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for the traffic-routing change. Identify client paths, stateful dependencies and differences between staging and production. Keep production execution outside this task.
    ```

Inspect whether the route diagram includes retries, connection persistence and asynchronous callbacks. If clients cache endpoints, switching one load-balancer target may not move all traffic. Ask for the relevant configuration or observation instead of assuming the drawing is complete.

### 2. Develop the bounded decision and plan

=== "Claude Code"

    ```text
    /layered Prepare the routing-change decision and execution plan from input/. Include prerequisites, traffic observations, abort thresholds and the authorized operator's handoff.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the routing-change decision and execution plan from input/. Include prerequisites, traffic observations, abort thresholds and the authorized operator's handoff.
    ```

Check that the plan defines what success looks like at each step. A final 'service healthy' line is too late if orders can be accepted by the wrong pool. Require a clear point after which rollback needs reconciliation rather than a simple route reversal.

### 3. Set review criteria

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set review criteria for this routing plan: release identity, rehearsed steps, evidence capture, abort conditions, rollback feasibility and customer impact.

Confirm the criteria shown by review before allowing assessment to start.

Read the criteria before the review. Decide which observations must be available during the window and who can interpret them. A dashboard screenshot without a time range or environment should not count as evidence that the new route handled the intended requests.

### 4. Review the runbook

=== "Claude Code"

    ```text
    /review <reported-review-target> the proposed routing plan against the fixed criteria and rehearsal records. Locate unsafe assumptions and missing operator decisions.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the proposed routing plan against the fixed criteria and rehearsal records. Locate unsafe assumptions and missing operator decisions.
    ```

Inspect findings about order state, route propagation and rollback separately. If staging lacks the production queue, a successful rehearsal leaves that integration untested. Keep the limitation in the decision packet rather than rewriting the rehearsal as a complete production simulation.

### 5. Rework and prepare the operator packet

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework open routing-change findings and prepare the proposed operator packet under output/. Do not mark production steps executed.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework open routing-change findings and prepare the proposed operator packet under output/. Do not mark production steps executed.
    ```

Inspect every command or configuration snippet with the actual operator before use. The packet should distinguish preparation checks, change steps and evidence to record afterward. Human scheduling and authorization remain outside document generation, and post-change observations remain pending until supplied.

## Handle an escalation or changed evidence

Suppose the proposed abort threshold depends on a metric unavailable during the window. Alice's example reply is: “Hold execution. Prepare a reliable order-failure observation or propose another window; do not replace the threshold with operator intuition.” Resume with `/layered` or `$workflow-layered` to resolve the observation gap. This is a safe way to change the plan without claiming that an unobservable control has been satisfied.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review finds that reversal would duplicate queued orders, use `/rework` or `$workflow-rework` on the rollback finding. If the change expands from routing to a database migration, revise the layered scope before continuing. The earlier review cannot cover a different irreversibility boundary or recovery procedure.

## Know when to stop

Deliver the reviewed proposed plan, verified findings, prerequisite checklist and operator evidence template. Record staging tests actually run; leave production execution and outcome NOT_EXECUTED until an authorized operator supplies evidence. The completed document is not itself a completed production change.

Use the **Production change** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
