# Research and defect analysis

Two capabilities often stand out in practice: disciplined research and disciplined defect analysis.

Use this page to distinguish an open research question from a reproducible
defect and understand their evidence requirements. For command syntax, use
the [command reference](../reference/commands.md); then choose a
[commented task walkthrough](../examples/index.md) for an end-to-end case.
These capabilities do not substitute for the broader assurance-method choice
in [Methodical workflows](../using/methodical-workflows.md).

## Research

`/research` is designed to move from question to defensible answer with explicit evidence handling and bounded experimentation when needed.

### Good use cases

- technology option assessment;
- control or design trade-off analysis;
- root-cause hypotheses requiring validation;
- questions where the organisation needs a structured argument rather than a quick opinion.

## Defect analysis

`/diagnose` forces the investigation to respect software engineering reality:

- compare with the last known good state;
- compare with a working analogue;
- treat timing/order effects as first-class possibilities;
- produce a regression-proof fix contract.

This is a materially stronger pattern than “guess a patch from the failing symptom”.
