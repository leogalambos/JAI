#!/usr/bin/env sh
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
# Install/update JAI using a selected Python, preserving its inherited PATH.
# Usage: [JAI_PYTHON=/absolute/path/to/python] bash ./install.sh [installer options]
# Inputs: package files, installer arguments, PATH and optional JAI_PYTHON.
# Outputs: installation summary and local capability diagnostics on stdout/stderr.
# Exit: selected Python/installer exit status; nonzero if Python is unavailable.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "${JAI_PYTHON:-python3}" "$HERE/.ai/setup/installer.py" "$@"
