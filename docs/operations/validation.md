# Validate the current 26.10.14 candidate

Owner: JAI maintainers. Last reviewed: 2026-10-26.

Scope: {{ JAI_SCOPE }}. Read RELEASE-SCOPE.json and QUALIFICATION-A-H.json
inside the exact ZIP, not a prior checkout or historical PASS. Compare release,
source bindings, all eight named gates and supported capabilities. Source edits
require fresh evidence; this page does not assert a new gate result.

Maintainer diagnostic, from the development root:

```sh
python3 .ai/runtime/tools/release_ga.py qualify
python3 .ai/runtime/tools/release_bundle.py --root . --dist build/dist build
```

A structural/semantic/governance result is not model correctness. D checks
supported application denials and provider projections, not certified host
confinement. E checks publication; F needs real renders, with actual Office
bytes inspected separately from HTML/PDF. G is fixture/harness qualification,
not live model qualification. H verifies source-bound integrity/provenance and
packaging; a checksum is not a human signature. Required missing checks fail.

The source suite and extracted/installed ZIP acceptance are separate evidence.
See [operator actions](operator-walkthrough.md) for signed L0 and returned
Office evidence. Privileged worker deployment
is NOT_SUPPORTED / NOT_VERIFIED, never reported as a passing host test.

The owner alone reviews Git, signing and publication. The tag-triggered CI can
publish after its own qualification; an agent must not trigger it autonomously.
[Imported 26.10.4 results](../reference/validation-26-10-4-history.md) are HISTORICAL.
