# Canonical corpus calibration

`corpus.py` prepares a bounded synthetic pilot through the maintained canonical lifecycle and findings writers, then verifies it with the canonical readers. It does not produce a bare graph DTO or claim performance qualification.

Run from the repository with the pinned helper interpreter:

```sh
build/fabric-explorer/helper-venv/bin/python -I -B apps/fabric-explorer/benchmarks/corpus.py --output /absolute/absent/pilot --tier pilot
```

The destination must be absent and its parent must exist. Defaults are 24 ordinary bulk inputs, 10 findings and two earlier-reference targets per input. Deliberate pilot bounds are 100 bulk inputs, 10 findings, eight earlier references, up to four nonempty bulk shards and 64 MiB of total prepared output. Use `--bulk-shards` to split the total bulk input count across independent engagements; it does not multiply that count. The pilot calibrates graph count and byte formulas. The maintained target dimensions and measurement rules are in [Qualification](../../../docs/fabric-explorer/qualification.md).

The manifest uses `jai.fabric-explorer.performance-corpus/1`. Resolve `sourceSets.base.sourcePaths` relative to the `base` directory; use the corresponding `append` or `malformed` sibling for other sets. Each source records its family, relative path, project root, length and digest. The valid append set contains a canonically appended finding resolution. The malformed set contains an explicit incomplete fabric tail. These are separately prepared variants; the measured application never modifies them.

Canonical admission reports versions, uses, transactions and findings. Graph vertices and edges remain `null` until the shipped helper/import/model oracle observes them. Target, observed and canonical transaction dimensions are distinct. The manifest separately accounts for selected metadata and unique material bytes actually requested by canonical replay. Unreferenced material files do not contribute. Pilot material padding is optional and bounded to 1 MiB per shard, attached exactly once. `explicitPaddingBytes` is the reported subset of input bytes used as material or physical JSON-whitespace padding; it is not added a second time to totals. Byte dimensions are not claims of indexed complexity.

The fixed seed is 20261109. Writer clocks and UUID generation are controlled during preparation. Labels, names and identities are synthetic; corpus manifests contain no private input provenance. Preparation publishes a new directory only after successful canonical admission and bound checks; failure removes only its unpublished staging directory. The generator does not change shared runtime code or read a selected project for execution.

Direct tests cover writer/reader admission, deterministic output, immutable separate variants, parameter and storage limits, fixed-tier override refusal, distributed padding and unreferenced material exclusion. They do not measure native rendering, runtime latency, peak memory, target-host suitability or complete S/M/L topology. Directed association cycles remain unestablished. Fixed candidates request exact counts and input bytes; independent actual import evidence must qualify each tier separately.

## Fixed S candidate

Use `--tier S` without pilot parameter overrides to prepare the fixed S candidate. It contains 175 bulk inputs, 643 exact earlier references and 100 findings, plus a separately registered new version of the rich journal's `input-A`. The latter preserves the same logical identity and origin scope with a distinct canonical version ID. A referenced 1 MiB material object adds one blob vertex and one relation. Remaining byte workload uses legal physical JSON whitespace outside canonical values; unchanged canonical readers verify the resulting journals.

S requests 1,000 vertices, 3,000 edges and 100 findings. The manifest retains `observedCounts: null` until the actual viewer oracle produces separate evidence. Base input totals exactly 10 MiB of selected encoded metadata plus unique material actually requested by canonical replay. `selectedMetadataBytes` alone is smaller; material and metadata padding are explicit separate fields. A valid append adds a finding resolution and therefore has its own observed byte total. All three immutable prepared variants remain within the 64 MiB preparation envelope.

The source generator reports canonical admission and byte accounting. A real helper/archive/native-worker oracle must independently assert the requested graph counts, and the shipped model must admit its complete encoded graph under the existing limits before these sources are used as qualified S input. No GUI, latency, memory or target-host verdict follows from preparation.

## Fixed M and L candidates

Use `--tier M` or `--tier L` without pilot overrides. These commands prepare
candidates; they do not assert that the viewer admits them or meets performance
budgets. The M construction has 4,804 bulk inputs across eight shards and
32,653 earlier references. L has 19,732 bulk inputs across 32 shards and
180,273 earlier references. Findings counts are 5,000 and 20,000 respectively.
The same calibrated mapper count equations determine their expected graph
counts; the real viewer oracle remains the authority for observed counts.
Both tiers include the same separately registered `input-A` revision as S.
The small versioned pilot demonstrated its additional two vertices and five
relations; reducing the bootstrap input count by one preserves the target
counts. Actual fixed-tier admission and version/cycle witnesses are still
required, rather than inferred from this arithmetic.

Each shard has one referenced 1 MiB material-padding object. Remaining physical
input bytes are legal JSON whitespace distributed across the single-row bulk
journals, rather than one oversized record. Preparation rejects a bulk row
exceeding 100 MiB. Metadata, material and padding remain separately reported;
padding does not add semantic graph complexity. All prepared variants together
are bounded at four times the tier's input target: 1,000 MiB for M and 4 GiB for
L. Allow sufficient free disk space before preparation. These source distributions
are synthetic workload definitions, not observations of production traffic.
