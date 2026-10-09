# Optional performance diagnostics (not a release gate)

Release qualification A–H evaluates structural, semantic, security,
behavioral, publication, and supply-chain correctness. It does **not** compare
runner speed, Python patch version, kernel, or hardware with a developer's
machine. There is no benchmark baseline stored in the source repository.

For optional local analysis, invoke:

```sh
python3 .ai/runtime/tools/performance_budget.py --profile fast --samples 3 \
  --out .ai/runtime/_meta/performance-report.json
```

To compare two runs from a **controlled, equivalent environment**, pass
`--compare-to /path/to/previous-report.json`. Environment mismatch is reported
as *incomparable*, not as failure. Store such reports as CI run artifacts or
outside the repository. Do not merge machine-dependent measurements into
source control. Stage timeouts are retained as safeguards for explicitly
requested benchmark runs, not as release thresholds.
