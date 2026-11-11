# Support and compatibility

Owner: JAI runtime maintainers. Reviewed: 2026-11-11.

## Current validation scope

Fabric Explorer is an optional, separately installed, read-only desktop viewer.
An installed unsigned Linux x64 development package has completed owner-observed
functional and ergonomic checks on the owner's workstation. These observations
do not establish a signed production release, a clean-machine qualification or
support for every Linux distribution, desktop, graphics driver or display scale.

| Target | Qualification boundary |
| --- | --- |
| Linux x64 | Installed development-package functionality and ergonomics observed on one workstation. Minimum-OS and clean-machine qualification remain separate. |
| Linux arm64 | Packaging target; native qualification remains pending. |
| Windows x64 | Packaging target; native qualification remains pending. |
| macOS x64 | Packaging target; native qualification remains pending. |
| macOS arm64 | Packaging target; native qualification remains pending. |

The [platform baseline](https://github.com/leogalambos/JAI/blob/main/apps/fabric-explorer/config/platform-baseline.json) defines the intended
OS and architecture combinations. A packaging recipe or an inspected archive
does not establish native support, and an older archive does not qualify a
changed application. Development performance measurements are bound to their
measured composition and host; they are not an assertion of current packaged
performance on a minimum-reference computer. Wider assistive-technology
qualification remains separate. Usability acceptance is based on the owner's
functional and ergonomic assessment; a five-user timed study is not a current
acceptance requirement.

## Source compatibility

Use the maintained [source contract](source-contract.md) for accepted formats and
their graph mapping. After opening sources, inspect **Source compatibility** and
the import diagnostics for supported or unknown versions, rejected records and
explicit bounds. Unknown or unreadable input must not be treated as a successful
complete import. Successful parsing does not certify the source's correctness,
current permissions or canonical validity.

The viewer does not migrate, repair or initialize source journals. Preserve
their original bytes when investigating an incompatibility; use the producing
tool's maintained procedure for any source change. A failed refresh retains the
previous accepted snapshot and identifies it as stale. See
[importing](importing.md) and [exploration](exploring.md).

## Installation and recovery

Follow [installation](installation.md) for verified local installation, upgrade,
rollback, uninstall and the separate deliberate preferences purge. Retain the
reviewed archive and matching installation files for offline management.
Unsigned development packages require the explicit development option; they
must not be presented as signed releases. Viewer management does not change the
JAI command-line installation or authorize changes to selected source data.

After a crash, the viewer does not reopen a project automatically. Corrupt
preferences fall back safely; if troubleshooting requires a reset, use the
documented application-data operation rather than deleting project directories.

## Diagnostics and assurance limits

Record the application version, OS and architecture, relevant source-format
versions, the action that failed and the visible diagnostic. Prefer a minimal
synthetic reproduction. Logs, source pages and screenshots can expose local
paths, source contents or identifiers: inspect and redact them before sharing,
and never upload private project data automatically or assume a public support
channel is an approved destination.

The read-only application APIs and source-integrity checks are distinct from a
proof of every operating-system effect. Native runtime namespaces and
asynchronous I/O can leave gaps in syscall-trace interpretation. A partial trace
must remain partial; an unchanged source snapshot does not prove that all
runtime network, process or filesystem activity was observed. See
[security qualification](security-qualification.md) for that boundary.

## Maintenance triggers

Reassess affected evidence when the source format, adapter, dependency/runtime,
privileged boundary, packaging/installer, OS enforcement or user interaction
changes. Preserve valid results for unchanged inputs and select new checks by
impact; do not infer qualification from an unchanged version label alone.
Review upstream advisories at dependency changes and before release, following
the [qualification envelope](qualification.md). Signing, notarization and actual
publication require their own reviewed release process.

The maintainers review this page when any boundary above changes. This page
defines validation and maintenance limits; it does not promise an external
support service, response time or future delivery date.
