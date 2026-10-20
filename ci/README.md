# JAI enterprise CI environment

This directory is the source-controlled operating-system dependency contract
for complete qualification in the **validate-library** manual preflight
and **tag-driven release** pipelines. Ordinary pushes and pull requests use
Python-only source checks and do not install or exercise release renderers.

- `system-packages.txt`: required Ubuntu 24.04 packages for Office rendering,
  PDF rasterisation, SVG conversion, and predictable fonts.
- `../requirements-ci.txt`: canonical direct Python dependencies, also bringing
  in MkDocs dependencies from `requirements.txt`.
- `../.github/actions/setup-qualification/action.yml`: shared installation and
  fail-fast execution, not two separately maintained CI setups.
- `../scripts/check_ci_environment.py`: checks Python imports and installed
  versions, executables, HTML→PDF→PNG and SVG→PNG smoke tests before any gates.

Any new external Python import or invoked system executable used by a
qualification or release tool must be declared here and tested by the
preflight. Full qualification jobs archive the resolved `pip freeze --all` report and
preflight JSON evidence, including on failure, to aid diagnosis.

The five directly declared Python packages are version-pinned, while
`requirements.txt` and transitive dependencies still have compatible ranges.
This is **not a full hash-locked dependency closure**; for strict bit-for-bit
reproducibility, generate a tested platform-specific hashed lockfile from this
manifest and use `pip --require-hashes` after a separate controlled lock update.
The workflows never claim a fully locked environment without such a file.

No reviewer approvals are added to release. A valid matching tag triggers
normal A–H gates and automatic publication if qualification succeeds.

## Bounded source checks and non-overlapping release tests

The source policy job has a ten-minute ceiling and a three-minute smoke-test
ceiling. It checks source/provider policy, version identity, documentation,
registry integrity and selected small regression modules. It does not run the
full synthetic evaluation or A–H. New pushes cancel obsolete source runs;
tag release runs are not cancelled by later source pushes.

The manual full-qualification input defaults to false. Enable it explicitly
for a complete candidate preflight. Tags always run A–H once with the full
environment. `scripts/ci_test_plan.py supplementary` selects every test module
outside Gate A's canonical inventory, so each module runs once in a full job.
There is no overlapping `unittest discover` pass or preliminary full corpus
evaluation. New test modules enter the supplementary selection automatically.
Source smoke success is not release qualification or human approval.

CI opts into live offline-guard output. Captures, kernel network denial and
process-group timeout enforcement remain active. See the maintained
[offline qualification guide](../docs/validation/offline-content-qualification.md).

## Optional performance measurements

Performance measurements are not a release prerequisite. A–H gates check
correctness, contracts, functional tests, and supply-chain integrity. The
benchmarking utility is opt-in and writes no baseline to the repository;
see `.ai/runtime/ci/PERFORMANCE-POLICY.md`. Historical developer hardware
or runtime fingerprints must not be committed as a qualification baseline.
