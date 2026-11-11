#!/bin/sh
# SPDX-License-Identifier: BSD-4-Clause
# Separate optional viewer installer; the main JAI installer remains unchanged.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec sh "$HERE/apps/fabric-explorer/packaging/install-from-source.sh" "$@"
