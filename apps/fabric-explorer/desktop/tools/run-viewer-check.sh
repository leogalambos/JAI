#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# Run finite Linux production-DOM journeys using synthetic sources only.
# Usage: bash apps/fabric-explorer/desktop/tools/run-viewer-check.sh [--focused]
# Inputs: pinned installed local toolchain/Electron; no download or real project input.
# Outputs: ignored build/fabric-explorer/viewer-native-* logs, screenshots and JSON.
# Exit: 0 only after a complete saved PASS; nonzero for failure, timeout or interruption.
set -euo pipefail
task_total=15
task_arguments=()
if [[ $# -gt 1 || ( $# -eq 1 && "$1" != --focused ) ]]; then
  printf '%s\n' 'Usage: run-viewer-check.sh [--focused]' >&2
  exit 2
fi
if [[ ${1:-} == --focused ]]; then
  task_total=7
  task_arguments=(--focused)
fi
task_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
task_node_bin="$task_root/build/fabric-explorer/toolchain/node/node-v24.22.2-linux-x64/bin"
task_node="$task_node_bin/node"
task_npm="$task_root/build/fabric-explorer/toolchain/npm/package/bin/npm-cli.js"
task_app="$task_root/apps/fabric-explorer/desktop"
task_output="$task_root/build/fabric-explorer/viewer-native-$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$task_output"
trap 'task_status=$?; printf "\nExit status: %s\nEvidence directory: %s\n" "$task_status" "$task_output"' EXIT
export PATH="$task_node_bin:$PATH"
unset NODE_OPTIONS ELECTRON_RUN_AS_NODE ELECTRON_OVERRIDE_DIST_PATH ELECTRON_MIRROR ELECTRON_NIGHTLY_MIRROR ELECTRON_CUSTOM_DIR ELECTRON_CUSTOM_FILENAME ELECTRON_SKIP_BINARY_DOWNLOAD
test -x "$task_app/node_modules/electron/dist/electron"
printf '%s\n' 'Phase 1/2: compile the fixed application and development-only journey helpers; no dependency installation.'
"$task_node" "$task_npm" --prefix "$task_app" run build:native-smoke 2>&1 | tee "$task_output/build.log"
"$task_node" "$task_app/tools/configure-reader.mjs"
printf 'Phase 2/2: %s numbered automatic application steps, including two SDK program comparisons and 11 finite canvas checks.\n' "$task_total"
if [[ $task_total == 7 ]]; then
  printf '%s\n' 'Focused recheck: source setup/import, refresh cleanup, canvas input, and shutdown. Previously passed search/filter/source/keyboard/scale journeys are retained separately.'
else
  printf '%s\n' 'Full journey: screenshots are captured at 100/150/200%.'
fi
printf '%s\n' 'Only synthetic source files are used.' 'One window opens; no manual terminal input or dense benchmark runs. Leave the controls alone during automation.' 'The native run has a 150-second watchdog (plus at most 20 seconds fixture setup); outer limit 180 seconds.' 'Stop the entire run with Ctrl+C or by closing its window. Electron sandbox remains enabled.'
timeout --foreground 180 "$task_app/node_modules/electron/dist/electron" "$task_app/dist/viewer-native.cjs" "${task_arguments[@]}" "$task_output" 2>&1 | tee "$task_output/native.log"
"$task_node" -e 'const fs=require("node:fs"),p=require("node:path");const root=process.argv[1];const expected=Number(process.argv[2]);const runs=fs.readdirSync(root).filter(n=>n.startsWith("viewer-"));if(runs.length!==1)throw Error("Expected one evidence run");const file=p.join(root,runs[0],"observations.json");const report=JSON.parse(fs.readFileSync(file,"utf8"));if(report.observations.length!==expected||report.observations.some(s=>s.status!=="pass"))throw Error("Incomplete journey evidence");console.log("Saved report: "+file);' "$task_output" "$task_total"
