# Behavioral Quality harness — 26.10.4

This directory contains the provider-neutral enterprise scenario
harness for the 26.10.4 Unified Lifecycle GA release. It measures
captured behavior against explicit expected roles, workflows, critical
requirements, evidence, artefacts, traceability, reviewer findings and
segregation-of-duties invariants.

The packaged `reference-results/` are **evaluator fixtures only**.
26.10.4 explicitly refuses to treat them as live provider/model
qualification evidence. They may be evaluated only with
`--fixture-mode` to prove corpus conformance and evaluator behavior.

A provider/model qualification is deployment-specific and must capture
the ten packaged scenarios using the selected provider/model. Store the
result JSONs in a separate directory and provide an evidence manifest
with `capture_type: live-provider`, provider/model identity, timestamp,
scenario count and SHA-256 hashes of every captured result. Run:

```sh
python3 .ai/runtime/tools/behavioral_eval.py qualify \
  --results /path/to/captured-results \
  --evidence /path/to/qualification-evidence.json
```

This separation prevents a universal package release from falsely
claiming that a mutable external model achieved the thresholds. Gate G
qualifies the behavioral harness, golden enterprise corpus, threshold
policy and adversarial defect detection; provider/model certification
is an explicit downstream evidence step.
