#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# Usage: bash run-recorded-labels-check.sh LOCAL_LINUX_PACKAGE.tar.gz EVIDENCE_PARENT
# Requires a local development archive produced by the viewer packager.
set -euo pipefail
if [[ $# != 2 || ! -f "$1" || ! -d "$2" ]]; then
  printf '%s\n' 'Supply a local Linux package and an existing evidence parent directory.' >&2
  exit 2
fi
task_desktop="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
task_run="$(mktemp -d "$(cd -- "$2" && pwd)/recorded-labels-XXXXXXXX")"
printf 'Evidence directory: %s\n' "$task_run"
mkdir "$task_run/payload" "$task_run/evidence"
tar -xzf "$1" -C "$task_run/payload"
task_runtime="$task_run/payload/runtime"
task_resources="$task_runtime/resources"
# Electron loads resources/app as its entry point. Keep the extracted application
# intact beside the launch driver, and use the runtime from the same archive.
mv -- "$task_resources/app" "$task_resources/packaged-app"
mkdir "$task_resources/app"
printf '%s\n' '{"name":"jai-recorded-labels-driver","version":"1.0.0","main":"main.cjs"}' > "$task_resources/app/package.json"
node -e 'require("node:fs").writeFileSync(process.argv[1], "require("+JSON.stringify(process.argv[2])+")\n")' \
  "$task_resources/app/main.cjs" "$task_desktop/test/recorded-labels-packaged.cjs"
unset NODE_OPTIONS ELECTRON_RUN_AS_NODE ELECTRON_OVERRIDE_DIST_PATH
timeout 115 "$task_runtime/electron" --ozone-platform=headless --use-angle=swiftshader \
  "$task_resources/packaged-app" "$task_run/evidence" 2>&1 | tee "$task_run/native.log"
test -f "$task_run/evidence/recorded-labels-native.json"
