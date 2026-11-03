# JAI continuous integration

The source validation workflow runs offline product identity, provider policy,
documentation and registry checks, plus selected regression modules. The Pages
workflow validates and builds the public documentation independently of release.

The release workflow is triggered only by a pushed `release@YY.MM.VV` tag. It
requires that the tagged commit is on `main` and that the tag matches committed
`VERSION`. Its bounded job installs source/documentation dependencies from
`requirements.txt`, checks current contracts and public documentation, then
constructs the source archive and SHA-256 checksum. It does not run comprehensive
regressions or install Office renderers. A separate job publishes those exact assets
only after validation succeeds. An existing release is never overwritten.

## Environment inputs

- `system-packages.txt` declares Ubuntu rendering and font dependencies.
- `../requirements.txt` supplies the fast source and documentation jobs.
- `../requirements-ci.txt` declares local regression dependencies.
- `../.github/actions/setup-qualification/action.yml` and
  `../scripts/check_ci_environment.py` describe the fuller renderer environment;
  the release workflow does not invoke that setup.

Direct pins and compatible dependency ranges are not a complete hash-locked
transitive environment. The SPDX inventory describes source files and declared
dependencies; it does not claim an observed installed dependency closure.

The release ZIP omits private inputs, local journals, private keys, generated
build trees, obsolete code and archived development reports. Test output stays
in CI rather than becoming product documentation. A release checksum identifies
bytes; business acceptance and release of an engagement's output remain separate
explicit decisions. Optional GitHub build attestations are external to JAI's L0
operator-signing mechanism.

## Comprehensive local prepublication tests

Before authorizing publication, the operator runs:

```sh
python3 scripts/prepublish.py --root .
```

This runs `python -u -m pytest -vv -x --tb=short --durations=20 tests` with the
selected interpreter. The complete maintained suite is selected, output is live,
and the first failure stops execution without being reported as success. There
is no mandatory aggregate runtime limit or a remote passed-receipt service.
Use a local environment with the declared test dependencies and required tools.

Local validation does not push a tag, create a GitHub Release or deploy Pages.
Performance measurements remain optional and are not publication prerequisites.
