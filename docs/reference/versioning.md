# Product version and release tags

## One product version authority

The root `VERSION` file is the only authority for the product version. Its format
is `YY.MM.VV`; the prepared version is **26.11.1**. Preparing source or building
documentation does not publish a release. Documentation follows the source
`VERSION` and may be newer than an installed published package.

Edit `VERSION`, then synchronize and inspect the maintained projections:

```sh
python3 scripts/versioning.py sync --root .
python3 scripts/versioning.py check --root .
```

Do not edit product-version projections individually. Synchronization updates:

- `.ai/VERSION` and `.ai/runtime/VERSION`;
- current product-version fields in the role and workflow catalogues and the
  optional evaluation-package descriptor;
- the generated runtime release manifest;
- generated resource-inventory sections in the source and runtime READMEs and
  the public compatibility reference.

The installed CLI guide has one maintained source:
`docs/reference/installed-cli-guide.md`. In the source tree,
`.ai/runtime/GUIDE.md` is a symbolic link to that document. Installation and
archive construction materialize its bytes so installed help does not depend
on the checkout. Version synchronization does not create a second editable guide.

MkDocs expands `{{ JAI_VERSION }}` from the authoritative product version while
building the site. Generated HTML is not edited afterward.

## Contract identities and history

A product version is separate from a schema, protocol, journal or artifact-contract
version. Change those identities only when their own contracts change. Updating
`VERSION` must not rewrite existing records or make historical acceptance apply
to new inputs. A domain registry's origin version is also distinct from the
current product version and remains unchanged unless its model changes.

## Local preparation

After completing the public changelog and reviewing the synchronized source,
run comprehensive regressions locally before publication:

```sh
python3 scripts/prepublish.py --root .
```

This entry runs the complete maintained `tests/` directory with verbose,
unbuffered pytest output, stops at the first failure and reports slow tests. It
preserves the test process exit status; an incomplete or failing run is not a
successful local preflight. Install the test dependencies from
`requirements-ci.txt` and the native tools needed by the maintained tests in
your local environment. This is an operator-run prerequisite, not a signed
receipt or a remotely inferred approval.

Validate documentation and construct a local candidate when needed:

```sh
python3 .ai/runtime/tools/generate_docs.py --check --root .
python3 .ai/runtime/tools/docs_contract.py --root .
python3 -m mkdocs build --strict
python3 .ai/runtime/tools/release_bundle.py build --root . --dist dist
```

The packaging command validates current source contracts and produces
`ai-it-house-universal-26.11.1.zip` and its `.sha256` checksum in a fresh output
directory. Existing outputs are not overwritten. Private inputs, local journals,
private keys, build trees, obsolete code and archived development reports are
excluded. A local build performs no Git operation or remote publication and does
not replace the comprehensive local regression prerequisite.

## Tag-driven publication

Publication is a separate operator action. First commit and push the reviewed,
synchronized source to `main`. Only when publication is intended, create and push
the matching tag. For the prepared version, those future commands are:

```sh
git tag -a 'release@26.11.1' -m 'JAI 26.11.1'
git push origin 'release@26.11.1'
```

The `release@YY.MM.VV` tag is the publication trigger. GitHub Actions requires
that the tagged commit is on `main` and that its version matches the committed
`VERSION`. GitHub performs bounded source, policy, registry, documentation and
archive checks. It installs only source/documentation dependencies, builds the
public site and constructs the archive, checksum and SPDX source/dependency
inventory. It does not run the comprehensive regression suite or install Office
renderers; those belong to the local prepublication step above. A separate
publication job verifies the checksum and creates the GitHub Release only after
its fast validation succeeds. An existing release is not overwritten.

The SPDX inventory describes source files and declared dependencies, rather than
claiming a complete observed dependency environment. GitHub build attestations
are attached where supported by the repository. A checksum alone identifies
bytes; it is not a signature. These build controls do not grant business
acceptance or release permission for an output produced by a JAI engagement.

Do not move a published tag. Corrections require a new product version. Preparing
26.11.1 in the repository has not itself performed the publication steps above.

## Diagnostics

```sh
python3 scripts/versioning.py check --root .
python3 scripts/versioning.py check --root . --tag 'release@26.11.1'
python3 .ai/runtime/tools/generate_docs.py --check --root .
```

A stale projection causes validation to fail with its location. Rerun version
synchronization and inspect the changes; avoid global replacement of version
numbers, which would also alter independent contracts and historical identities.
