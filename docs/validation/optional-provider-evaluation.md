# Optional provider evaluation

Owner: JAI maintainers · Last reviewed: 2026-10-20

The optional harness supports Codex and Claude CLI integrations. Normal CI,
package builds and mandatory qualification never invoke it live. Its tests
use fake executables and deterministic captured results. JAI neither installs
a provider CLI nor configures credentials or authenticates for you.

## Prerequisites and planning

Install and authorize the selected provider CLI yourself using its supported
instructions. Confirm account permissions and charges before any live run.
Use an explicit model selector appropriate for that provider. Preflight only
locates an executable; it does not inspect credentials, authenticate, execute
the CLI or claim that the account is usable.

```bash
python3 .ai/runtime/tools/optional_provider_eval.py preflight \
  --provider codex --root .
python3 .ai/runtime/tools/optional_provider_eval.py plan \
  --provider codex --root . --family adr --cases 3 --model MODEL_ID
```

`plan` is the dry-run command. It validates the bundled inputs and records
scope without subprocess execution or inference. Missing executables produce
`UNAVAILABLE`, never a simulated PASS. `--executable` can select an existing
CLI installation; there is no automatic installation or fallback provider.

## Explicit live execution

Run from a normal operator terminal outside nested coding-agent execution,
only after reviewing the plan and authorizing the expense:

```bash
python3 .ai/runtime/tools/optional_provider_eval.py run \
  --provider codex --root . --family adr --cases 3 --model MODEL_ID \
  --max-invocations 3 --timeout 60 --consent-live \
  --output build/optional-provider-run.json
```

Substitute `--provider claude` and a valid Claude model selector for that
provider. One to three cases select the bundled complexity levels in order.
Codex uses its read-only sandbox; Claude tools are disabled. These flags
limit this evaluation to text assessment. No retries or provider fallback
occur. A failure stops remaining cases.
Timeout and cancellation terminate the subprocess group. Output files are
created exclusively, preventing accidental report overwrite.

`--max-invocations` caps inference calls, **not tokens or monetary charges**.
Apply account-side cost controls where supported. A version probe also runs
after explicit consent; it does not invoke inference. CLI authentication and
provider network access are permitted only in this optional operator action.

The harness exports only validated bundled `public-synthetic` fictional
examples. User, organisation and engagement overrides are excluded. It never
exports private references automatically, even if they are active locally.

## Offline analysis and limitations

```bash
python3 .ai/runtime/tools/optional_provider_eval.py report \
  --input build/optional-provider-run.json
```

The report command verifies captured-report integrity offline. Reports record
the selected and observed model separately, CLI version when observed,
execution environment, invocation budget, per-case status, duration and
reported token usage when available. Unobserved metadata remains null.
Prompts, provider prose, stderr and credential values are not retained.

Integrity hashes detect accidental changes; they are not independent signed
provider attestations. A completed call does not prove professional quality.
Without independent outcome labels, precision, recall and false-positive
rate remain `not-measurable`, with null counts and rates. Synthetic labels
must not be presented as human-gold.

For independently labelled evaluations, precision is TP/(TP+FP), recall is
TP/(TP+FN), and FPR is FP/(FP+TN). Report denominators, label origin and
uncertainty alongside rates; a zero denominator is not measurable. Targets
such as 95% precision/recall or 10% FPR are optional guidance, not release
gates or professional certification. Small samples do not justify broad
performance claims. This minimal harness does not import external gold labels
or automatically judge generated prose.
