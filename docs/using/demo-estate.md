# Learning with the demo estate

Use the demo estate to practise a workflow with fictional local inputs before
applying it to your project. Choose a commented walkthrough, prepare its
practice pack and follow the explanation of each step.

## Choose a scenario practice pack

The maintained catalog contains 29 scenario packs spanning the 24 enterprise
workflow chains. Browse [commented task walkthroughs](../examples/index.md)
or ask `/hint` (`$workflow-hint` in Codex) to recommend a starting procedure.

=== "Claude Code"

    ```text
    /demo scenarios
    /guide proposal
    /demo scenario proposal --to /tmp/acme-proposal
    ```

=== "Codex CLI"

    ```text
    $workflow-demo scenarios
    $workflow-guide proposal
    $workflow-demo scenario proposal --to /tmp/acme-proposal
    ```

In Codex, use `$workflow-demo` and `$workflow-guide` with the same arguments.
Open the prepared project's `START.md`: it explains the fictional inputs,
Claude and Codex command pairs, expected outputs and escalation points. Ask
`/guide proposal --step 2` to explain a particular step. Preparation creates
inputs; it does not execute the workflow or establish an approved outcome.

Choose a new destination. Existing work is not overwritten by scenario
creation. An explicitly requested reset backs up the existing scenario
workspace. See [Remember useful knowledge](remembering-knowledge.md) for
capturing a lesson and [Build and reuse local know-how](reusing-knowledge.md)
for permission and reuse boundaries; saved custom scenarios do not
automatically become executable demo packs.

## Why the demo matters

The demos are not marketing toys. They exercise the system's workflows against seeded defects and realistic outputs.

## Recommended sequence

The original three projects remain available through `/demo setup`:
`invoice-service`, `policy-docs` and `acme-pay`. They contain separate seeded
exercises. This legacy setup does not create all 29 scenario practice packs.

Treat the following as a tour of separate exercises, not one prescribed engagement history. In particular, a later `/layered` exercise does not retrospectively govern earlier `/sabsa` authoring. Choose the arrangement using [Methodical workflows](methodical-workflows.md); follow the [worked cases](../examples/how-to-use-JAI/index.md) for coherent end-to-end engagements. Use Claude slash commands below or the corresponding Codex `$workflow-<name>` skills in the provider conversation.

1. `/demo setup`
2. `/analyse invoice-service`
3. `/criteria invoice-service`
4. `/review invoice-service`
5. `/diagnose ...`
6. `/sabsa prepare ...`
7. `/publish ...`
8. `/layered ...`

## What good results look like

Good results are typically characterised by:

- explicit scope and assumptions;
- visible review criteria;
- separation between findings and fixes;
- concrete next actions;
- professional deliverable structure;
- clear statement of uncertainty when evidence is weak.
