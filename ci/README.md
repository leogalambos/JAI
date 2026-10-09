# JAI enterprise CI environment

This directory is the source-controlled operating-system dependency contract
for the **validate-library** and **tag-driven release** pipelines.

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
preflight. Both workflows archive the resolved `pip freeze --all` report and
preflight JSON evidence, including on failure, to aid diagnosis.

The five directly declared Python packages are version-pinned, while
`requirements.txt` and transitive dependencies still have compatible ranges.
This is **not a full hash-locked dependency closure**; for strict bit-for-bit
reproducibility, generate a tested platform-specific hashed lockfile from this
manifest and use `pip --require-hashes` after a separate controlled lock update.
The workflows never claim a fully locked environment without such a file.

No reviewer approvals are added to release. A valid matching tag triggers
normal A–H gates and automatic publication if qualification succeeds.

## Optional performance measurements

Performance measurements are not a release prerequisite. A–H gates check
correctness, contracts, functional tests, and supply-chain integrity. The
benchmarking utility is opt-in and writes no baseline to the repository;
see `.ai/runtime/ci/PERFORMANCE-POLICY.md`. Historical developer hardware
or runtime fingerprints must not be committed as a qualification baseline.
