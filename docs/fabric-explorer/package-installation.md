# Install the standalone viewer

The viewer is optional and installs separately from the JAI command-line tools.
Installing, upgrading or removing the viewer does not change the CLI installation.
The application runs offline without Node.js, Python, npm or a compiler.

Packages are target-specific: Linux x64/arm64 and macOS x64/arm64 use tar.gz;
Windows x64 uses ZIP. A package contains the Electron runtime, the compiled
application, an installation-only helper, notices and an inventory. Required
operating-system desktop libraries remain prerequisites. Building and inspecting
a target package does not establish native support: Windows and macOS native
qualification remains deferred.

Obtain the archive, detached asset manifest, signature and generated installation
script from the reviewed distributor channel. Keep these files together. The
installation script embeds the exact archive and manifest hashes and the fixed
trusted distributor public key. A key supplied by a source project or an arbitrary
download is not trusted. Release installation rejects missing or invalid
signatures. Installation metadata is read through bounded regular-file handles: the
manifest is at most 64 KiB, the detached Ed25519 signature is exactly 64 bytes,
and the fixed public-key file is at most 16 KiB. An unsigned development package requires both development metadata
and an explicit development option; it is not a release artifact.

## Preview and install

On Linux/macOS, run the supplied shell script with `--dry-run` first, then without
that option to install. On Windows, use the supplied PowerShell script with
`-DryRun`, then without it. Dry-run reads and hashes local inputs and checks the
platform; it does not download, extract, execute Electron or write application
state. A missing local asset fails without changing the current installation.
No installation operation downloads dependencies or compiles software.

For an explicitly labeled unsigned development package, add
`--allow-development` on Linux/macOS or `-AllowDevelopment` on Windows. Do not use
this option to represent the package as a signed release.

The default binary locations are:

| Platform | Installation root | Separate application preferences/data |
| --- | --- | --- |
| Linux | `${XDG_DATA_HOME:-~/.local/share}/jai-fabric-explorer/install` | `${XDG_CONFIG_HOME:-~/.config}/JAI Fabric Explorer` |
| macOS | `~/Applications/JAI Fabric Explorer` | `~/Library/Application Support/JAI Fabric Explorer` |
| Windows | `%LOCALAPPDATA%\JAI Fabric Explorer Install` | `%APPDATA%\JAI Fabric Explorer` |

Run `launch-viewer` in the installation root on Linux/macOS, or
`launch-viewer.cmd` on Windows. The launcher directly starts the packaged native
application. It does not run a Node bootstrap. Linux establishes the private,
application-declared cache before Electron starts, disables Mesa shader-cache
writes and selects the memory GSettings backend. Do not bypass Electron's sandbox
with `--no-sandbox`.

## Upgrade, rollback and remove

Close the viewer before changing its installed files. Run the new package's
installation script to upgrade. It verifies the payload, stages a complete
immutable version and atomically replaces the active-version pointer. The
previous version remains available. Bad hashes, wrong architecture, unavailable
assets and failed staging leave the existing active version intact.

Keep the verified archive and installation script for offline management. The
helper runs from a temporary extracted runtime, allowing removal of installed
files without trying to delete the executing Windows binary.

| Operation | Linux/macOS option | Windows option |
| --- | --- | --- |
| Roll back | `--rollback` | `-Operation rollback` |
| Remove binaries and launchers | `--uninstall` | `-Operation uninstall` |
| Separately delete application preferences/data | `--purge-preferences` | `-Operation purge` |

Add the relevant dry-run option to preview any operation. Uninstall preserves
preferences/data and unrelated files. Purge is a separate deliberate action; it
removes the viewer's configured preferences/data directory. Unsigned development
management still requires the explicit development option.

An interrupted operation can leave an exclusive `.install-claim` or an owned
`.stage-*` directory. The installer fails closed instead of guessing whether
another process is active. Close other installer processes, preserve any useful
logs, and inspect only this viewer's installation root before removing its stale
claim/staging data. Never remove unrelated directories or alter source journals.
The active pointer is never deleted before replacement; a completed pointer
publication selects a complete version even if later reporting is interrupted.

Release signing and any operating-system signing/notarization are distributor
operations. Local unsigned functional tests do not establish those assurances.
