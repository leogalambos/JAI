#!/bin/sh
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# POSIX routing: existing package installation needs no Node.js, npm or source build tools.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
build=no
allow=no
dry=no
operation=install
package_dir=
while [ "$#" -gt 0 ]; do
  case "$1" in
    --help|-h) cat <<'HELP'
Usage: ./install-viewer.sh --package-dir DIRECTORY [--allow-development] [--dry-run]
       ./install-viewer.sh --build --allow-development [--dry-run]
       ./install-viewer.sh --package-dir DIRECTORY --rollback|--uninstall|--purge-preferences [--allow-development] [--dry-run]
No implicit build or download. --dry-run prints a plan without build/install subprocesses or writes.
Source build requires Node.js 24.22.2, npm 11.21.2, git, tar, unzip (and zip on Windows).
Non-Windows source packaging requires GNU tar on PATH; macOS BSD tar is insufficient.
JAI_VIEWER_NODE and JAI_VIEWER_NPM_CLI can select explicitly installed matching host tools.
HELP
      exit 0;;
    --build) build=yes;;
    --allow-development) allow=yes;;
    --dry-run) dry=yes;;
    --package-dir) [ "$#" -ge 2 ] || { echo '--package-dir requires a directory' >&2; exit 2; }; package_dir=$2; shift;;
    --rollback|--uninstall|--purge-preferences) [ "$operation" = install ] || { echo 'Choose one management operation' >&2; exit 2; }; operation=$1;;
    *) echo "Unknown viewer installation argument: $1" >&2; exit 2;;
  esac
  shift
done
case "$(uname -s):$(uname -m)" in
  Linux:x86_64|Linux:amd64) target=linux-x64;; Linux:aarch64|Linux:arm64) target=linux-arm64;;
  Darwin:x86_64|Darwin:amd64) target=darwin-x64;; Darwin:arm64|Darwin:aarch64) target=darwin-arm64;;
  *) echo 'Unsupported viewer platform/architecture; no changes made' >&2; exit 2;;
esac
if [ "$build" = yes ]; then
  [ -z "$package_dir" ] && [ "$operation" = install ] || { echo '--build conflicts with --package-dir and management operations' >&2; exit 2; }
  [ "$allow" = yes ] || { echo 'Unsigned source builds require --allow-development' >&2; exit 2; }
  set -- --build --allow-development
  [ "$dry" = no ] || set -- "$@" --dry-run
  exec "${JAI_VIEWER_NODE:-node}" "$HERE/install-from-source.mjs" "$@"
fi
[ -n "$package_dir" ] || { echo 'No package selected. Use --package-dir DIRECTORY, or explicitly --build --allow-development after installing the documented build prerequisites.' >&2; exit 2; }
[ -d "$package_dir" ] || { echo 'Local package directory is missing; no build is performed' >&2; exit 2; }
set -- "$package_dir"/jai-fabric-explorer-*-"$target".tar.gz.install.sh
[ "$#" -eq 1 ] && [ -f "$1" ] || { echo 'Expected exactly one matching local package sidecar; select a directory containing one version for this platform' >&2; exit 2; }
sidecar=$1
if [ "$dry" = yes ]; then printf 'Plan %s for %s using existing local verified installer; development permission: %s. No installation or integrity verification executed.\n' "$operation" "$sidecar" "$allow"; exit 0; fi
set --
[ "$allow" = no ] || set -- "$@" --allow-development
[ "$operation" = install ] || set -- "$@" "$operation"
exec sh "$sidecar" "$@"
