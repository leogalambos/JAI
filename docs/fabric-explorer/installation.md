# Install and update

Fabric Explorer installs separately from the JAI command-line tools. Running the
main `./install.sh` does not build or install the viewer. Viewer installation,
upgrade and removal do not change the CLI installation.

## Install from a repository clone

The clone provides separate viewer entrypoints: `./install-viewer.sh` on Linux
and macOS, and `install-viewer.cmd` on Windows. Running an entrypoint without a
mode prints instructions; it does not silently build or download the viewer.
The entrypoint selects the current host's supported OS and architecture.

### Explicitly build and install a development package

From the repository root on Linux or macOS:

```sh
./install-viewer.sh --build --allow-development --dry-run
./install-viewer.sh --build --allow-development
```

From the repository root in a Windows terminal:

```bat
install-viewer.cmd --build --allow-development --dry-run
install-viewer.cmd --build --allow-development
```

The first command inspects the host and prints the plan. It does not acquire
dependencies, compile, download a runtime or install the application. The second
command explicitly acquires the required build inputs, builds a package for
the current platform and installs it. Network access is needed when those
inputs are not already available locally. A previously prepared build cache is
not a prerequisite for using a fresh clone.

Source builds require stable Node.js **24.0.0 or newer**, npm **11.0.0 or newer**, Git and unzip. Archive
creation on Linux/macOS requires GNU tar on `PATH`; macOS's default BSD tar is
not sufficient for that build path. Windows source packaging additionally
requires tar, zip and PowerShell. The entrypoint does not install this toolchain for
you. Unsupported hosts fail rather than silently selecting another target.

Use `JAI_VIEWER_NODE` to select an absolute path to a supported Node executable
and `JAI_VIEWER_NPM_CLI` to select an absolute path to its
`npm-cli.js` when the intended toolchain is not selected through `PATH`.
The system toolchain can be used directly; Fedora 44's Node.js 24.18.0 and
npm 11.16.0 meet these minimums. Locked dependencies retain their own engine
constraints; the qualification toolchain recorded in the dependency baseline
is a reproducibility reference, not an exact-version installation requirement.
The local source-build output is an unsigned development package, so the
explicit `--allow-development` option is required. Building it does not create
a signed release or establish native qualification for another platform.

### Install an existing local package

If a matching package has already been supplied, point the clone entrypoint at
its directory. Replace `./viewer-packages` below with the directory containing
the archive and matching installation files:

```sh
./install-viewer.sh --package-dir ./viewer-packages --dry-run
./install-viewer.sh --package-dir ./viewer-packages
```

Windows uses `install-viewer.cmd` with the same arguments. Add
`--allow-development` to each command only for an explicitly labelled unsigned
development package. This route requires neither Node.js/npm nor Python. It
does not fall back to a source build if the local package is missing.

Use that same package-directory route for a management operation, adding
exactly one of `--rollback`, `--uninstall` or `--purge-preferences`. The operation
can also be previewed with `--dry-run`. Keep the explicit development option
when managing an unsigned development package.

## Choose a package

Use a reviewed, prebuilt archive for the operating system and architecture of
the machine that will run it. Keep the supplied archive, matching manifest and
installation script together, plus the matching signature for a signed release.
The supplied prebuilt-package installer verifies its local inputs and does not
compile software or download dependencies. This is distinct from the clone
entrypoint's explicit `--build` mode described above.

| Packaging target | Archive format |
| --- | --- |
| Linux x64 or arm64 | tar.gz |
| macOS x64 or arm64 | tar.gz |
| Windows x64 | ZIP |

These are separate packaging targets, not a claim that every target has completed
native qualification or has a released download available. Unsigned development
packages must remain explicitly identified as development packages. Distributor
signing and any OS signing or notarization are separate release conditions.

The package supplies the viewer and its Electron runtime. It requires the
operating system's desktop libraries, but no end-user Python, Node.js, npm or
compiler. Do not disable the runtime sandbox to make a launch succeed.

## Preview and install

1. Read the package's platform, version and signing status. Use the matching
   installation script from the reviewed distribution channel.
2. On Linux or macOS, run that shell script with `--dry-run`. On Windows, run
   the supplied PowerShell script with `-DryRun`.
3. Check the reported destination and operation. Run the same script without
   the dry-run option to install.
4. Start the installed launcher.

For an explicitly labelled unsigned development package, add
`--allow-development` on Linux/macOS or `-AllowDevelopment` on Windows to the
installation and management commands. That option does not turn the package
into a signed release.

| Platform | Default installation root | Launcher |
| --- | --- | --- |
| Linux | `${XDG_DATA_HOME:-~/.local/share}/jai-fabric-explorer/install` | `launch-viewer` inside that root |
| macOS | `~/Applications/JAI Fabric Explorer` | `launch-viewer` inside that root |
| Windows | `%LOCALAPPDATA%\JAI Fabric Explorer Install` | `launch-viewer.cmd` inside that root |

For example, the default Linux launcher is:

```sh
"${XDG_DATA_HOME:-$HOME/.local/share}/jai-fabric-explorer/install/launch-viewer"
```

The viewer starts without opening a project automatically. Continue with
[Explore data](exploring.md) to select local sources.

## Upgrade, roll back or remove

Close the viewer before changing its installed files. Keep the verified package
and its installation script for later offline management. To upgrade, run the
new package's installer: it verifies the payload, stages a complete version and
atomically selects it. Bad inputs or failed staging preserve the current active
version.

| Operation | Linux/macOS option | Windows option |
| --- | --- | --- |
| Preview the operation | Add `--dry-run` | Add `-DryRun` |
| Roll back to the previous installed version | `--rollback` | `-Operation rollback` |
| Remove viewer binaries and launchers | `--uninstall` | `-Operation uninstall` |
| Deliberately remove viewer preferences/data | `--purge-preferences` | `-Operation purge` |

Uninstall preserves preferences/data. Purge is a separate deliberate action;
neither operation is a way to repair or delete selected source journals. If an
installation is interrupted, preserve its logs and inspect only the viewer's
installation root before removing stale installer state. Do not delete
unrelated directories or change source files to repair an application install.

## Building from source

The clone entrypoints above make source building an explicit development
workflow. They use the maintained viewer build and packaging tools for the
current platform. The main JAI installer remains separate and does not trigger
that workflow or install a native viewer runtime. Running a prebuilt viewer
requires neither Node.js/npm nor Python; only the explicit source-build route
requires the development toolchain.
