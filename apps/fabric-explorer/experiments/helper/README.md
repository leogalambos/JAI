# Disposable canonical-reader packaging probe

This experiment demonstrates specific read-only fixture operations using the
maintained JAI reader. It is not the product helper, an application IPC protocol,
a graph adapter or a release package. A successful local run does not qualify
another OS, a minimum-OS floor, all runtime resources, current permissions or
performance. Production adoption requires a separately reviewed implementation.

## Reproduce

Use the repository's pinned CPython version and a new scratch virtual environment.
The Linux-x64/CPython3.14 lock records exact downloaded distribution hashes;
other native targets require their own native resolution/hash inventory.

```sh
python3 -m venv build/fabric-explorer/helper-venv
build/fabric-explorer/helper-venv/bin/python -m pip install --require-hashes -r apps/fabric-explorer/experiments/helper/requirements-linux-x64-py314.lock
build/fabric-explorer/helper-venv/bin/python -m pip check
build/fabric-explorer/helper-venv/bin/python apps/fabric-explorer/experiments/helper/create_fixture.py --output build/fabric-explorer/helper-fixture
build/fabric-explorer/helper-venv/bin/python apps/fabric-explorer/experiments/helper/build_probe.py --output build/fabric-explorer/helper-native --verifier /usr/bin/openssl --verifier-license /usr/share/licenses/openssl-libs/LICENSE.txt
build/fabric-explorer/helper-venv/bin/python apps/fabric-explorer/experiments/helper/smoke_probe.py --executable build/fabric-explorer/helper-native/dist/jai-reader-probe/jai-reader-probe --fixtures build/fabric-explorer/helper-fixture --report build/fabric-explorer/helper-native/smoke-report.json
```

Use new/empty output directories; the fixture generator refuses an existing
destination. The generator uses the maintained ordinary writer harness on a
POSIX host and creates no signing key. Copy only its synthetic output to native
reader test hosts. Do not disable the canonical writer's locking guard to
generate fixtures on a platform without that writer implementation.

Windows uses the virtual environment's `Scripts/python.exe` and the resulting
`jai-reader-probe.exe`. Native Windows test input dependencies are declared in
`requirements-test.txt`; prepare an exact native hash lock before qualification.
The verifier's direct and delayed PE imports are inspected recursively, with
non-system DLLs copied adjacent to its executable. System API sets remain
explicit OS dependencies. macOS uses `otool` dependency inspection, relocates
non-system libraries, and applies ad-hoc development signatures after changing
load commands. These code paths require real native verification; a prepared
script is not successful native evidence or release signing.

The builder requires the fixed CPython/OpenSSL versions. It retains the canonical
module closure and copies offline governed protocol schemas at their maintained
frozen resource location. It inventories exact app files in its scratch output.
No source tree is copied. Audit nested executable archives as well as loose
files before making any source-exclusion or legal-distribution claim.
Supply the actual verifier distribution's license through `--verifier-license`;
the example location is distribution-specific. The bundle retains JAI, CPython,
OpenSSL and selected Python-package license texts. Its notice inventory explicitly
does not claim a complete native-dependency SBOM or legal release clearance.

## Observations and boundaries

The smoke runner starts the executable with an empty ambient PATH, unusable
ambient Python locations and a caller-independent temporary working directory.
It verifies an ordinary author/reviewer/selection canonical-history fixture
covering all six record families and derived decisions, six recorded findings states
under explicit round configuration, a diagnostic-only projection and RFC8032's
public Ed25519 vector with a negative modified-message check. No private signing
key or local user enrollment is involved. It compares source bytes and directory
entries before/after and records `qualifiedPlatform: false` in its raw report.

The CLI supports only `fabric`, `findings`, `diagnostic` and `verifier`; no write,
repair, signing, general command or module operation is exposed. `fabric` calls
the canonical `Store.read`; `findings` verifies its separate chain through the
canonical parser and secure snapshot. Omitting round configuration keeps state
reduction unknown. Diagnostic parsing never claims canonical replay or current
authority. Errors are bounded categories without raw source paths or payloads.

This one-shot prototype intentionally does not implement production acquisition
memory limits, long-lived checkpoint reuse, chunked IPC, cancellation or safe
multi-root capability admission. Its canonical read may capture an entire
journal. Use controlled synthetic fixtures, not arbitrary unbounded input.
Signed historical replay with enrolled trust, full semantic resource closure
and versioned production authority display require additional targeted cases.
The public verifier vector is distinct from proof that signed journal trust
enrollment is portable. The selected verifier's own runtime library dependencies
are part of the native build and need inspection on each actual target.

Raw build logs, package reports, artifact inventories, screenshots and host
measurements belong in scratch/private evidence. Do not publish them as a
portable qualification result. The experiment reads only synthetic fixtures.
Report destinations must resolve outside the selected fixture tree, including
existing ancestor/final symlink aliases and Windows case-insensitive paths.
The smoke runner checks that boundary before processing and again before report
publication; existing hard-linked or nonregular report targets are rejected.
