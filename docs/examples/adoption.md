# Plan adoption of a new working practice

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `organisational-change-and-adoption` workflow recipe.
It is not an additional native slash command.

ACME is introducing a new service-desk categorization practice across three offices. Alice owns the process and Bob coordinates local team leads. The problem is not merely publishing instructions: staff need to recognize categories, handle exceptions and keep service quality observable during transition.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-service-desk-adoption/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- current-process.md — existing intake, categorization and handoff steps
- pilot-feedback.csv — anonymized observations and unresolved questions
- target-practice.md — proposed categories, responsibilities and examples
- adoption-brief.md — participating teams, dates, measures and constraints

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Start with analysis of the actual work and feedback. Use the layered path to connect the intended outcome with training, ownership and evidence. Review materials before publication; a polished guide does not demonstrate that staff can use the new practice.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Understand the affected work

=== "Claude Code"

    ```text
    /analyse input/ for the service-desk practice change. Identify affected roles, ambiguous categories and evidence missing from the pilot. Do not infer adoption from attendance.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for the service-desk practice change. Identify affected roles, ambiguous categories and evidence missing from the pilot. Do not infer adoption from attendance.
    ```

Inspect whether the analysis distinguishes office differences from individual mistakes. If a category depends on information agents never receive, more training will not fix the process. Ask Bob for representative anonymized tickets and the decision points used by experienced staff.

### 2. Frame the adoption outcome

=== "Claude Code"

    ```text
    /layered Prepare a bounded adoption plan for the participating service desks. Connect desired outcomes to training, local support, exception handling and measurable observations.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare a bounded adoption plan for the participating service desks. Connect desired outcomes to training, local support, exception handling and measurable observations.
    ```

Check that success is expressed as changed work, such as correct handoffs or fewer avoidable recategorizations. Course completion and guide downloads are supporting measures. The plan should name who owns category clarification after launch and who can pause rollout.

### 3. Set material-review criteria

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set review criteria for the training and operating guidance: recognizable examples, role clarity, accessibility, exceptions and feedback routes. Avoid invented pilot results.

Confirm the criteria shown by review before allowing assessment to start.

Read the proposed criteria from a new team member's position. Decide whether an example gives enough information to choose a category. A correct label with no explanation teaches memorization rather than the decision rule staff need for unfamiliar tickets.

### 4. Prepare the guide

=== "Claude Code"

    ```text
    /develop Develop the adoption guidance and practice examples as documentation only, using the agreed plan and actual pilot feedback. Keep draft outcomes separate from observed results.
    ```

=== "Codex CLI"

    ```text
    $workflow-develop Develop the adoption guidance and practice examples as documentation only, using the agreed plan and actual pilot feedback. Keep draft outcomes separate from observed results.
    ```

Inspect whether each lesson explains the task, a decision and the consequence of choosing incorrectly. Use fictional tickets for illustration and label them as such. Do not copy confidential customer reports into a broadly distributed training pack.

### 5. Review, rework and prepare handoff

=== "Claude Code"

    ```text
    /review <reported-review-target> the adoption guidance against the agreed criteria. Record confusing examples and missing exception routes before distribution.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the adoption guidance against the agreed criteria. Record confusing examples and missing exception routes before distribution.
    ```

Read the findings with Alice and use rework for corrections. If no representative learner has tried the guide, preserve that limitation. Put the reviewed guidance and the proposed feedback process under output/; publishing it does not establish successful rollout.

## Handle an escalation or changed evidence

Suppose one office cannot use the new category because its supplier contract requires a different reporting field. Alice's example reply is: “Keep that office on the existing reporting path while we agree a mapped category. Do not count it as an adoption failure or alter contractual reporting.” Resume with `/layered` or `$workflow-layered` to revise the rollout boundary and explain the temporary exception.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review finds that examples rely on unexplained internal abbreviations, use `/rework` or `$workflow-rework` to rewrite them and retain the original finding until verified. If rollout expands to external suppliers, revisit the scope and ownership model first. Internal staff guidance does not establish supplier obligations or their acceptance.

## Know when to stop

Finish with a reviewed guide, role-specific practice examples, an exception route, local support owners and a measurement plan. Distinguish proposed surveys from actual feedback. Record learner trials and rollout observations only when performed; otherwise mark them NOT_EXECUTED and leave adoption effectiveness unclaimed.

Use the **Adoption and change enablement** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
