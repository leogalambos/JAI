# Test categories and selective execution

Owner: project maintainers. Review when test boundaries, runner entry points or
the impact map change.

Run commands below from the source checkout root with the Python test
dependencies from `requirements-ci.txt`. Native tests also need the pinned
Node/npm environment and installed dependencies for the selected Fabric Explorer
packages. Desktop tests require the prepared SDK described in the
[desktop build guide](../fabric-explorer/desktop-shell.md).

## Categories

Each maintained test receives one semantic level. File or module defaults apply
to every test inside it; an explicit individual-test classification can override
the default. A category describes the behaviour under test, not an assumed
execution time.

| Category | Meaning | Appropriate use |
| --- | --- | --- |
| `unit` | Isolated computation without a real filesystem, process or service boundary | Local implementation feedback |
| `integration` | Collaboration with real filesystem, process, repository or component dependencies | Affected component neighbourhood |
| `contract` | Producer/consumer agreement, schema, protocol or semantic interface obligations, including rejection behaviour | Boundary changes and routine workflow controls |
| `e2e` | Complete user/workflow progression through multiple components | Broad stable changes and explicit complete verification |

Additional tags express independent properties:

| Tag | Meaning |
| --- | --- |
| `control` | Curated representative component or interface check for routine workflow execution |
| `slow` | Known expensive regression or scenario; not a claim about every untagged test's speed |
| `security` | Authority, permission, integrity or other security invariant |
| `performance` | Performance/resource behaviour; inspect the test to distinguish synthetic assertions from real measurements |

The existing regression suite uses real repository and filesystem fixtures
extensively. Uncertain tests are conservatively classified as integration tests;
they are not labelled unit tests merely because they use pytest or mocks.
Control selection is deliberate and smaller than the complete contract category.
It includes positive collaboration cases and negative semantic/permission cases.
The long complete layered progression remains in the full suite.

## Execution profiles

Inspect a plan without running its tests:

```bash
python3 scripts/run_tests.py --profile control --list
```

Run routine component and semantic interface checks:

```bash
python3 scripts/run_tests.py --profile control
```

Run development tests for changed files, including affected consumers:

```bash
python3 scripts/run_tests.py --profile development
python3 scripts/run_tests.py --profile development --changed .ai/runtime/tools/operator_actions.py
python3 scripts/run_tests.py --profile development --base HEAD
```

With no explicit inputs, development mode uses staged, unstaged and untracked
changes. Repeat `--changed` for multiple repository-relative inputs. A Git base
selects changes relative to that revision. Inspect the reported reasons when
selection expands: missing dependency knowledge requires broader verification.
An invalid baseline is an error, not an empty passing selection.

Filter a profile by category, or restrict its runtime:

```bash
python3 scripts/run_tests.py --profile full --scope python --category contract
python3 scripts/run_tests.py --profile control --scope native
python3 scripts/run_tests.py --profile development --scope python --changed tests/test_prepublish.py
```

Repeated `--category` arguments mean OR; the result is intersected with the
profile and changed-input scope. A filtered run does not establish that all
tests passed. The selector preserves child-process failures and reports the
scope it actually chose. Listing is a plan, not test evidence.

For complete maintained Python and native verification on stable sources:

```bash
python3 scripts/run_tests.py --profile full
```

Run this after a broad change is stable or before release, rather than after
each edit. Direct `python3 -m pytest tests` and the existing
`python3 scripts/prepublish.py --root .` retain their complete root Python
regression semantics. Those older commands do not include all application
Python and native suites; the full selector does. Existing `npm test` commands
retain their previous package behaviour.

Python markers are also directly executable:

```bash
python3 -m pytest -m 'contract and security' tests
python3 -m pytest -m control apps/fabric-explorer/reader/test
```

Native packages expose equivalent entry points:

```bash
npm --prefix apps/fabric-explorer/desktop run test:control
npm --prefix apps/fabric-explorer/desktop run test:development -- --changed apps/fabric-explorer/desktop/src/shell/paths.ts
npm --prefix apps/fabric-explorer/packages/contracts run test:category -- --category contract
node apps/fabric-explorer/tools/test-selection.mjs --profile full --package packaging --list
```

`--changed` paths remain repository-relative even when npm changes the working
directory. The native selector handles Vitest and Node test files, including
the separate build and packaging tests. Vendored SDK qualification keeps its
existing explicit `test:sdk` command. Native platform and physical desktop/GPU
qualification remain separate environment-specific checks; a portable control
pass cannot establish them.

## Maintaining classification and impact

`ci/test-catalog.json` maintains Python module defaults, individual contract
classifications, curated controls and explicit source/input impacts. The root
pytest plugin applies these as ordinary registered pytest markers. Authors can
use an individual `@pytest.mark.contract` (or another semantic level) to express
a more specific classification. Maintain control membership deliberately rather
than making every new test a routine gate.

`apps/fabric-explorer/test-categories.json` records native test-file categories
and control membership. Every test in a classified file inherits that category.
Split mixed native files when their cases need different execution scopes.
Native classification is independent from Vitest's naming conventions.
The native catalogue also declares compiled-asset entry points and their test
consumers. Worker consumers are additive to static import consumers. Before
executing them, the selector rebuilds current contract and worker bundles;
an existing `dist` file alone is insufficient evidence of current-source tests.
Test-asset preparation preserves unrelated built qualification assets.

When adding a test, classify it and give a rationale. When adding a source
dependency, resource, fixture, generated contract, subprocess entry point or
dynamic import, update the impact mapping and test the selection. Static import
analysis complements explicit resource knowledge; it cannot prove the absence
of all runtime dependencies. Unknown changes deliberately widen execution.
Use `--list` to review scope changes before accepting a new mapping.

Source validation CI runs the Python control profile and built native contract
checks. Desktop CI runs selected desktop and reader controls in addition to
building actual assets. Manual native-reader qualification remains explicit.
The release pipeline continues its separate publication checks.

Preserve test evidence for unchanged inputs. Record the tested revision or
relevant input digest, profile, selected scope, result and reason to rerun in
private local evidence. Measure total time to a verified result and selector
overhead; a shorter test count alone is not proof of sufficient coverage.
