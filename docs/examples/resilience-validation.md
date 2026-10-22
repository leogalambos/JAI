# Validate resilience with a bounded exercise

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `resilience-validation` workflow recipe.
It is not an additional native slash command.

ACME wants evidence that its ordering service can continue or recover during a supplier connection failure. Alice owns service continuity and Bob coordinates the exercise. The familiar setting is a tabletop followed, where authorized, by a controlled rehearsal; this guide does not authorize disruption.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-ordering-resilience/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- service-map.md — dependencies, failure boundaries and owners
- continuity-objectives.md — business impact, recovery targets and assumptions
- exercise-scope.md — environment, permitted actions, stop conditions and contacts
- prior-results.md — actual previous exercises and unresolved improvements

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use a layered exercise plan because failure injection can affect customers and suppliers. A tabletop can validate understanding and expose missing decisions; it cannot demonstrate measured recovery performance. Keep rehearsal execution separate from planning and documentary review.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Understand the failure boundary

=== "Claude Code"

    ```text
    /analyse input/ for a supplier-connection loss exercise. Identify business effects, hidden dependencies and gaps in prior evidence. Do not induce failures.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for a supplier-connection loss exercise. Identify business effects, hidden dependencies and gaps in prior evidence. Do not induce failures.
    ```

Inspect whether the service continues accepting orders when supplier acknowledgments stop. A service-health endpoint may remain green while orders accumulate. Ask for queue behavior, retry limits and reconciliation ownership so the exercise tests the business service rather than only a process monitor.

### 2. Prepare the exercise plan

=== "Claude Code"

    ```text
    /layered Prepare a bounded resilience exercise for the environment in input/exercise-scope.md. Include observable outcomes, stop conditions, restoration and evidence capture.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare a bounded resilience exercise for the environment in input/exercise-scope.md. Include observable outcomes, stop conditions, restoration and evidence capture.
    ```

Check that the scope identifies who may stop the exercise and how participants contact that person if the service channel fails. A planning document does not grant permission to disconnect a supplier. Unavailable authorization or environment access must remain a prerequisite.

### 3. Fix the evidence criteria

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set review criteria for this exercise: permitted actions, business observations, measurement timing, reconciliation, restoration and known simulation limits.

Confirm the criteria shown by review before allowing assessment to start.

Read what each observation can establish. A tabletop answer explains a proposed response; a measured rehearsal can show duration in the exercised environment. Neither automatically proves production performance under every failure mode. Require timestamps and environment identities for any duration claim.

### 4. Review readiness to exercise

=== "Claude Code"

    ```text
    /review <reported-review-target> the exercise plan against the fixed criteria and supplied scope. Locate safety, observation and restoration gaps before any operator acts.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the exercise plan against the fixed criteria and supplied scope. Locate safety, observation and restoration gaps before any operator acts.
    ```

Inspect the stop procedure and the expected steady state after restoration. If duplicate orders are possible, the plan needs reconciliation evidence. Do not accept a generic 'rollback available' assertion when the exercise changes business data that routing reversal cannot undo.

### 5. Rework and assess actual observations

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework exercise-readiness findings using supplied evidence. If operators later provide results, preserve observations separately from proposed steps and prepare the follow-up under output/.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework exercise-readiness findings using supplied evidence. If operators later provide results, preserve observations separately from proposed steps and prepare the follow-up under output/.
    ```

Read the actual exercise log before accepting a recovery claim. Record whether the exercise was tabletop, staging or production and which planned steps were not executed. An unexpected stop is useful evidence; it should not be rewritten as a completed scenario to improve the score.

## Handle an escalation or changed evidence

Suppose the exercise team discovers that the supposed test supplier endpoint routes to a live partner. Alice's example reply is: “Stop preparation for fault injection. Continue only as a tabletop until the isolated endpoint and partner boundary are confirmed.” Resume with `/layered` or `$workflow-layered` to revise the plan. The restriction does not prevent useful analysis, but it changes what evidence the exercise can produce.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review finds that the plan measures API recovery while ignoring unreconciled orders, use `/rework` or `$workflow-rework` to add business recovery observations. If scope expands to a regional outage, reopen objectives and dependency analysis. A supplier-link exercise cannot justify a claim about regional resilience.

## Know when to stop

Deliver the reviewed plan, actual observations if provided, an explicit list of unexecuted actions and an improvement register. Mark the recovery target unmet, met in the exercised environment or NOT_EXECUTED as evidence supports. JAI's report is not permission for disruptive testing or acceptance of residual continuity risk.

Use the **Resilience validation** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
