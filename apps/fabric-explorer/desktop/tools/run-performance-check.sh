#!/usr/bin/env bash
# Run finite Linux development-composition performance observations over prepared synthetic corpora.
# Usage: bash tools/run-performance-check.sh --smoke|--qualification|--endurance|--activity|--animation|--imports|--all ABS_HOST_INPUT_JSON
# Inputs: reviewed manifest paths in the host-input JSON, pinned local runtimes and application sources.
# Outputs: private build/evidence files only. Exit 0: smoke collected; 1: failure; 2: incomplete qualification; 130: stop.
# No dependency installation, downloads, sandbox disabling or real project source mutation.
# Native builds require the prepared SDK source cache; no SDK download occurs here.
set -euo pipefail
umask 077
if [[ $# -ne 2 || $2 != /* ]]; then printf '%s\n' 'Použití: run-performance-check.sh --smoke|--qualification|--endurance|--activity|--animation|--imports|--all ABS_HOST_INPUT_JSON' >&2; exit 2; fi
case $1 in
  --smoke) task_mode=smoke ;;
  --qualification) task_mode=qualification ;;
  --endurance) task_mode=endurance ;;
  --activity) task_mode=activity ;;
  --animation) task_mode=animation ;;
  --imports) task_mode=imports ;;
  --all) task_mode=all ;;
  *) printf '%s\n' 'Neznámý režim testu.' >&2; exit 2 ;;
esac
task_input=$2
task_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
task_node_bin="$task_root/build/fabric-explorer/toolchain/node/node-v24.22.2-linux-x64/bin"
task_node="$task_node_bin/node"
task_app="$task_root/apps/fabric-explorer/desktop"
task_parent="$task_root/build/fabric-explorer/performance-native-$(date -u +%Y%m%dT%H%M%SZ)-$$"
task_output="$task_parent/observations"
mkdir -m 700 "$task_parent"
trap 'task_status=$?; printf "\nNávratový kód: %s\nAdresář výsledků: %s\n" "$task_status" "$task_parent"' EXIT
export PATH="$task_node_bin:/usr/bin:/bin"
unset NODE_OPTIONS ELECTRON_RUN_AS_NODE ELECTRON_OVERRIDE_DIST_PATH ELECTRON_MIRROR ELECTRON_NIGHTLY_MIRROR ELECTRON_CUSTOM_DIR ELECTRON_CUSTOM_FILENAME ELECTRON_SKIP_BINARY_DOWNLOAD
test -r "$task_input"
test -x "$task_node"
test -x "$task_app/node_modules/electron/dist/electron"
printf '%s\n' 'Fáze 1/2: sestavení aplikace a vývojového měření; žádná instalace závislostí.'
"$task_node" "$task_app/tools/build.mjs" --with-performance-check 2>&1 | tee "$task_parent/build.log"
"$task_node" "$task_app/tools/configure-reader.mjs"
task_limit="$("$task_node" -e 'const plan=require(process.argv[1]).performanceCases(process.argv[2]); process.stdout.write(String(Math.ceil(plan.reduce((sum,row)=>sum+row.watchdogMs+2000,0)/1000)+400));' "$task_app/dist/performance-plan.cjs" "$task_mode")"
printf 'Fáze 2/2: automatický režim %s; celková vnější mez %s sekund.\n' "$task_mode" "$task_limit"
printf '%s\n' 'Není potřeba nic hodnotit ani zadávat. Graf během automatického měření neovládejte.' 'Zastavení: tlačítko ve vieweru, Escape, zavření okna nebo Ctrl+C. Žádné automatické opakování.' 'Režim smoke načte pouze S. Režim imports má 3 případy S/M/L, každý 6 kroků, bez opakování dalších populací. Výdrž se spouští samostatně nebo jako součást režimu all.' 'Výsledek není automatickým potvrzením zabalené aplikace, minimálního referenčního počítače ani ostatních operačních systémů.'
timeout --foreground --signal=INT --kill-after=5s "$task_limit" "$task_node" "$task_app/dist/performance-host.cjs" "$task_app/node_modules/electron/dist/electron" "$task_input" "$task_output" "$task_mode" 2>&1 | tee "$task_parent/host.log"
