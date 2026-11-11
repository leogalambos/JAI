#!/usr/bin/env bash
# Qualify viewer accessibility using fixed synthetic sources and explicit visual/keyboard observations.
# Usage: bash apps/fabric-explorer/desktop/tools/run-accessibility-check.sh [--automatic|--manual|--visual-details]
# Default: build once, run finite automation, then open the four-step Czech visual/keyboard session.
# No downloads, source dependency installation, core tests or real project data are used.
# Native builds require the prepared SDK source cache; no SDK download occurs here.
set -euo pipefail
task_mode=both
if [[ $# -gt 1 ]]; then printf '%s\n' 'Použití: run-accessibility-check.sh [--automatic|--manual|--visual-details]' >&2; exit 2; fi
case ${1:-} in
  '') ;;
  --automatic) task_mode=automatic ;;
  --manual) task_mode=manual ;;
  --visual-details) task_mode=visual-details ;;
  *) printf '%s\n' 'Použití: run-accessibility-check.sh [--automatic|--manual|--visual-details]' >&2; exit 2 ;;
esac
task_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
task_node_bin="$task_root/build/fabric-explorer/toolchain/node/node-v24.22.2-linux-x64/bin"
task_node="$task_node_bin/node"
task_npm="$task_root/build/fabric-explorer/toolchain/npm/package/bin/npm-cli.js"
task_app="$task_root/apps/fabric-explorer/desktop"
task_output="$task_root/build/fabric-explorer/accessibility-native-$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$task_output"
trap 'task_status=$?; printf "\nNávratový kód: %s\nAdresář výsledků: %s\n" "$task_status" "$task_output"' EXIT
export PATH="$task_node_bin:$PATH"
unset NODE_OPTIONS ELECTRON_RUN_AS_NODE ELECTRON_OVERRIDE_DIST_PATH ELECTRON_MIRROR ELECTRON_NIGHTLY_MIRROR ELECTRON_CUSTOM_DIR ELECTRON_CUSTOM_FILENAME ELECTRON_SKIP_BINARY_DOWNLOAD
test -x "$task_app/node_modules/electron/dist/electron"
task_phases=2
if [[ $task_mode == both ]]; then task_phases=3; fi
printf 'Fáze 1/%s: sestavení aplikace a testu. Žádná instalace závislostí.\n' "$task_phases"
if [[ $task_mode == manual ]]; then
  "$task_node" "$task_npm" --prefix "$task_app" run build:contracts 2>&1 | tee "$task_output/build.log"
  "$task_node" "$task_app/tools/build.mjs" --with-accessibility-manual 2>&1 | tee -a "$task_output/build.log"
else
  "$task_node" "$task_npm" --prefix "$task_app" run build:native-smoke 2>&1 | tee "$task_output/build.log"
fi
"$task_node" "$task_app/tools/configure-reader.mjs"
"$task_node" --input-type=module - "$task_app" "$task_output" "$task_mode" <<'JS'
import {readFileSync,writeFileSync,readdirSync} from 'node:fs';
import {join,relative} from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const [directory,output,mode]=process.argv.slice(2); const inputs=[];
function visit(path){for(const entry of readdirSync(path,{withFileTypes:true})){if(entry.isDirectory())visit(join(path,entry.name));else if(/\.(?:ts|tsx|mjs|css|html|sh)$/.test(entry.name)){const file=join(path,entry.name);inputs.push({path:relative(directory,file),sha256:createHash('sha256').update(readFileSync(file)).digest('hex')});}}}
for(const name of ['src','test','tools'])visit(join(directory,name));
for(const name of ['package.json','package-lock.json','tsconfig.json','tsconfig.accessibility-manual.json','dist/main.cjs','dist/preload.cjs','dist/renderer/renderer.js','dist/renderer/renderer.css','dist/accessibility-manual.cjs',...(mode==='manual'?[]:['dist/accessibility-native.cjs','dist/canvas-accessibility.js','dist/visual-details-native.cjs'])])inputs.push({path:name,sha256:createHash('sha256').update(readFileSync(join(directory,name))).digest('hex')});
writeFileSync(join(output,'tested-inputs.json'),JSON.stringify({revision:execFileSync('git',['rev-parse','HEAD'],{cwd:directory,encoding:'utf8'}).trim(),at:new Date().toISOString(),scope:'viewer presentation and development-only accessibility helpers',rerunTrigger:'changed relevant source, built assets, toolchain or host accessibility setup',inputs},null,2)+'\n');
JS
if [[ $task_mode == automatic || $task_mode == both ]]; then
  printf '%s\n' 'Automatická část: 18 očíslovaných kroků, včetně šesti kombinací motivu a měřítka.' 'Tato část má horní limit 180 sekund. Testovací okno ponechte v popředí a během běhu ho neovládejte.' 'Zavření okna nebo Ctrl+C ukončí celý test. Sandbox zůstává zapnutý.'
  if timeout --foreground 180 "$task_app/node_modules/electron/dist/electron" "$task_app/dist/accessibility-native.cjs" "$task_output" 2>&1 | tee "$task_output/automatic.log"; then
    :
  else
    task_native_status=$?
    if [[ $task_native_status == 2 ]]; then
      printf '%s\n' 'Automatický test není dokončený: chybí ověření nebo vypršel časový limit. Nejde o úspěšný výsledek.' 'Zachovejte výstup. Samostatná vizuální kontrola se spouští parametrem --manual; chybějící ověření zůstává otevřené.'
    fi
    exit "$task_native_status"
  fi
fi
if [[ $task_mode == visual-details ]]; then
  printf '%s\n' 'Doplňující snímky: 6 očíslovaných kroků (příprava a čtyři vizuální kontexty), celkem 10 snímků.' 'Zachytí pouze graf při 200 % a sbalený/rozbalený přesný identifikátor při 150/200 % v obou motivech.' 'Předchozí klávesnicové testy a výsledky se neopakují. Běh má horní limit 180 sekund a nevyžaduje ruční odpovědi.' 'Testovací okno ponechte otevřené; zastavení zavřením okna nebo Ctrl+C. Sandbox zůstává zapnutý.'
  timeout --foreground 180 "$task_app/node_modules/electron/dist/electron" "$task_app/dist/visual-details-native.cjs" "$task_output" 2>&1 | tee "$task_output/visual-details.log"
fi
if [[ $task_mode == manual || $task_mode == both ]]; then
  printf 'Fáze %s/%s: krátká česká vizuální kontrola. Orca není potřeba.\n' "$task_phases" "$task_phases"
  printf '%s\n' 'Nejprve proběhnou čtyři očíslované kroky automatické přípravy syntetických dat, nejvýše 60 sekund.' 'Potom se zobrazí vždy jen jeden ze čtyř ručních úkolů.' 'Tlačítkem Přejít do prohlížeče otevřete aplikaci. Klávesa F8 vás vrátí k aktuálnímu úkolu.' 'Neověřené výsledky ponechte jako Neověřeno. Nic se samo neoznačí jako úspěšné.' 'Ruční část nemá animaci ani časový limit. Ukončení: tlačítko ve formuláři, zavření okna nebo Ctrl+C.'
  "$task_app/node_modules/electron/dist/electron" "$task_app/dist/accessibility-manual.cjs" "$task_output" 2>&1 | tee "$task_output/manual.log"
fi
