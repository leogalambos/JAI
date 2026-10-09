# Change record template

Copy to `it-role-library/staging/CR-<year>-<nnn>.md`. A change without
one is rejected by `library-approver`, because an unexplained change
cannot be reversed by someone who was not in the conversation that
produced it.

```markdown
# CR-2026-014 — <one line, what changes>

**Author:** <name or agent>            **Date:** <yyyy-mm-dd>
**Type:** role | archetype | tier | agent | generator | documentation

## What changes
<The diff in words. Every file touched, named.>

## Why
<The problem. Not the solution restated as a problem.>

## Considered and rejected
<At least one alternative, and why it lost. A change with no rejected alternative was
not a decision.>

## Blast radius
- Roles affected: <count, named categories>
- Archetypes edited: <which, and how many roles inherit each>
- Tiers changed: <which, and whether anything got wider>
- Agents affected: <which>

## What could break
<Be specific. "Nothing" is almost never true for an archetype or tier edit.>

## Reversal
<The exact way back, not "revert the commit" unless the commit is the only artefact.>

## Validator
<Paste the output of check_agent_policy.py against the staged tree.>

## Approval
- Reviewed by: <library-approver output summary>
- Approved by: <human name>   Recorded: <approve_change.py output>
- Conditions: <any, with an owner each>
```
