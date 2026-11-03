# Fictional native Gen2 exercise

Status: NOT_EXECUTED. The inputs below are fictional practice material, not
customer facts, measured evidence, a reviewed result or human approval. This
exercise is separate from the policy review's planted-flaw exercise.

Use the existing native provider session. No journal or PASS is seeded by demo
setup. The parent captures inputs and exact references internally; do not write
bootstrap JSON, import an archived engagement or create a signing key for setup.

1. Read `gen2-inputs/brief.md` and `gen2-inputs/criteria.md`.
2. In Claude, request:

   ```text
   /layered For this fictional policy decision, use gen2-inputs/brief.md and gen2-inputs/criteria.md. Produce a justified policy proposal, preserve unknowns and report the engagement and exact current basis. Do not implement access changes or claim operational measurements, acceptance or release.
   ```

   In Codex, request the same work:

   ```text
   $workflow-layered For this fictional policy decision, use gen2-inputs/brief.md and gen2-inputs/criteria.md. Produce a justified policy proposal, preserve unknowns and report the engagement and exact current basis. Do not implement access changes or claim operational measurements, acceptance or release.
   ```

3. Inspect the actual result and engagement reported by the workflow. Ask
   `/fabric-report <actual-engagement>` or
   `$workflow-fabric-report <actual-engagement>`. An intact history alone is not
   sufficient evidence or permission. If no current product exists, the audit
   must say so. Do not invent an engagement identifier or result to continue.
4. Practise continuation by asking to resume that same engagement with its
   unfinished work and original bounds. If an input changes, request the existing
   owner's input-version change; do not edit a historical record or reuse PASS.
   Required human acceptance and release remain separate external L0 acts.

The layer formulates its questions and chooses local specialties/models from the
complete catalogue. Authors and reviewers stay independent. Missing evidence or
expired bounds produce an explicit pause rather than fabricated success.

`/demo reset policy-docs` restores this exercise through the existing explicit
project-reset operation. Preserve work before requesting a reset; that operation
replaces the original tour project. Scenario-catalogue exercises retain their
separate backup-preserving reset behavior.
