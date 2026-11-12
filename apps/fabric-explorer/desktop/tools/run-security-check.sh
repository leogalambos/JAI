#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# Qualify the viewer's actual Linux process tree against owned write-denied synthetic sources.
# Usage: bash apps/fabric-explorer/desktop/tools/run-security-check.sh
# No downloads, installations, real project inputs or sandbox-disabling options are used.
# Inputs: fixed local toolchain and a Linux desktop with ACL/ptrace support; no arguments.
# Outputs: private build evidence, raw trace, source-integrity and classification reports.
# Exit: 0 clean observations, 1 failed run/integrity, 2 unavailable/incomplete qualification, 130 interrupted.
# Native builds require the prepared SDK source cache; no SDK download occurs here.
set -euo pipefail
if [[ $# -ne 0 ]]; then printf '%s\n' 'Použití: run-security-check.sh (bez parametrů)' >&2; exit 2; fi
task_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
task_app="$task_root/apps/fabric-explorer/desktop"
task_node_bin="$task_root/build/fabric-explorer/toolchain/node/node-v24.22.2-linux-x64/bin"
task_node="$task_node_bin/node"
task_npm="$task_root/build/fabric-explorer/toolchain/npm/package/bin/npm-cli.js"
task_python="$task_root/build/fabric-explorer/helper-venv/bin/python"
task_electron="$task_app/node_modules/electron/dist/electron"
task_output="$task_root/build/fabric-explorer/security-native-$(date -u +%Y%m%dT%H%M%SZ)-$$"
task_manifest="$task_output/security-input.json"
task_restore_allowed=true
mkdir -p "$task_output"
finish() {
  local task_status=$?
  trap - EXIT
  if [[ -f $task_manifest && $task_restore_allowed == true ]]; then
    if ! "$task_python" -I -B "$task_app/../qualification/fixtures.py" restore --manifest "$task_manifest" >"$task_output/restore.log" 2>&1; then
      printf '%s\n' 'Obnovení oprávnění testovacích souborů selhalo; zachovejte adresář výsledků.' >&2
      task_status=1
    fi
  elif [[ -f $task_manifest ]]; then
    printf '%s\n' 'Po nedokončeném sledovaném běhu zůstávají syntetické zdroje pouze pro čtení. Oprávnění se automaticky neobnovují.' >&2
  fi
  printf '\nNávratový kód: %s\nAdresář výsledků: %s\n' "$task_status" "$task_output"
  exit "$task_status"
}
trap finish EXIT
trap 'exit 130' INT TERM
export PATH="$task_node_bin:$PATH"
unset NODE_OPTIONS ELECTRON_RUN_AS_NODE ELECTRON_OVERRIDE_DIST_PATH ELECTRON_MIRROR ELECTRON_NIGHTLY_MIRROR ELECTRON_CUSTOM_DIR ELECTRON_CUSTOM_FILENAME ELECTRON_SKIP_BINARY_DOWNLOAD
printf '%s\n' 'Bezpečnostní ověření: 6 konečných fází, pouze syntetické soubory.' 'Žádné ruční odpovědi nejsou potřeba. Otevře se jedno okno; během testu ho neovládejte.' 'Sledovaná část má limit 180 sekund. Zavření okna nebo Ctrl+C test ukončí.' 'Sandbox zůstává zapnutý. Surový záznam procesů zůstane v adresáři výsledků.'
printf '%s\n' 'Fáze 1/6: kontrola prostředí a možnosti sledovat jediný neškodný proces.'
[[ $(uname -s) == Linux ]] || { printf '%s\n' 'Tento připravený test je určen pro Linux.' >&2; exit 2; }
[[ -n ${DISPLAY:-} || -n ${WAYLAND_DISPLAY:-} ]] || { printf '%s\n' 'Chybí grafická relace. Test spusťte z terminálu na svém desktopu.' >&2; exit 2; }
for task_command in strace setfacl getfacl timeout sha256sum; do
  if ! command -v "$task_command" >/dev/null; then
    printf 'Chybí nutný nástroj: %s. Test nic neinstaluje.\n' "$task_command" >&2
    exit 2
  fi
done
for task_binary in "$task_node" "$task_python" "$task_electron"; do
  if [[ ! -x $task_binary ]]; then
    printf 'Chybí připravený spustitelný soubor: %s. Test nic nestahuje.\n' "$task_binary" >&2
    exit 2
  fi
done
if ! timeout --foreground 10 strace --kill-on-exit -I 1 -f -qq -o "$task_output/trace-preflight.log" /usr/bin/true 2>"$task_output/trace-preflight.stderr"; then
  printf '%s\n' 'Operační systém nepovolil sledování procesů. Test není ověřený; nepřidávejte --no-sandbox ani sudo.' >&2
  exit 2
fi
printf '%s\n' 'Fáze 2/6: sestavení pevné aplikace a jediného testovacího vstupu; bez instalace závislostí.'
"$task_node" "$task_npm" --prefix "$task_app" run build:contracts 2>&1 | tee "$task_output/build.log"
"$task_node" "$task_app/tools/build.mjs" --with-security-check 2>&1 | tee -a "$task_output/build.log"
"$task_node" "$task_app/tools/configure-reader.mjs"
sha256sum "$task_node" "$task_python" "$task_electron" >"$task_output/runtime-binaries.sha256"
"$task_node" --input-type=module - "$task_app" "$task_output" <<'JS'
import {readFileSync,writeFileSync,readdirSync} from 'node:fs';
import {join,relative} from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const [directory,output]=process.argv.slice(2); const inputs=[];
function record(file){inputs.push({path:relative(directory,file),sha256:createHash('sha256').update(readFileSync(file)).digest('hex')});}
function visit(path){for(const entry of readdirSync(path,{withFileTypes:true})){const file=join(path,entry.name);if(entry.isDirectory()&&entry.name!=='__pycache__')visit(file);else if(entry.isFile()&&/\.(?:ts|tsx|mjs|py|css|html|sh)$/.test(entry.name))record(file);}}
for(const name of ['src','test','tools','../qualification','../reader','../packages/contracts/src'])visit(join(directory,name));
for(const name of ['package.json','package-lock.json','../packages/contracts/package-lock.json','tsconfig.json','dist/main.cjs','dist/preload.cjs','dist/import-worker.cjs','dist/renderer/renderer.js','dist/renderer/renderer.css','dist/security-native.cjs','dist/security-assets/preload.cjs','dist/security-assets/renderer/index.html','dist/security-assets/renderer/renderer.js','dist/security-assets/renderer/renderer.css'])record(join(directory,name));
writeFileSync(join(output,'tested-inputs.json'),JSON.stringify({revision:execFileSync('git',['rev-parse','HEAD'],{cwd:directory,encoding:'utf8'}).trim(),at:new Date().toISOString(),scope:'Linux viewer security qualification; development-only helpers; synthetic sources',rerunTrigger:'changed relevant source, built assets, dependency/runtime or OS enforcement environment',inputs},null,2)+'\n');
JS
printf '%s\n' 'Fáze 3/6: příprava syntetických zdrojů a ověření, že OS odmítá jejich změnu.'
"$task_python" -I -B "$task_app/../qualification/fixtures.py" prepare --directory "$task_output" --python "$task_python" --electron "$task_electron" --initial-cwd "$task_app" 2>&1 | tee "$task_output/prepare.log"
task_native_cache="$task_output/application/JAI Fabric Explorer/cache/native"
# Native libraries initialize before entrypoint JavaScript; establish their write boundary before exec.
mkdir -m 700 "$task_output/application/JAI Fabric Explorer"
mkdir -m 700 "$task_output/application/JAI Fabric Explorer/cache"
mkdir -m 700 "$task_native_cache"
"$task_node" --input-type=module - "$task_output" "$task_native_cache" <<'JS'
import {writeFileSync} from 'node:fs';
import {join} from 'node:path';
const [output,cache]=process.argv.slice(2);
writeFileSync(join(output,'launch-environment.json'),JSON.stringify({format:'jai.fabric-explorer.native-environment/1',MESA_SHADER_CACHE_DISABLE:'true',XDG_CACHE_HOME:cache,GSETTINGS_BACKEND:'memory',scope:'Linux pre-runtime development composition; packaged launch must carry this contract'},null,2)+'\n');
JS
printf '%s\n' 'Fáze 4/6: automatické načtení, prohlížení a zavření pod sledováním procesů; nejvýše 180 sekund.'
cd -- "$task_app"
task_native_status=0
task_restore_allowed=false
env MESA_SHADER_CACHE_DISABLE=true XDG_CACHE_HOME="$task_native_cache" GSETTINGS_BACKEND=memory timeout --foreground --kill-after=5 180 strace --kill-on-exit -I 1 -f --always-show-pid -ttt -yy -s 4096 -o "$task_output/process.trace" -e 'trace=%file,%process,%network,write,writev,pwrite64,pwritev,pwritev2,ftruncate,fallocate,fchmod,fchown,fsetxattr,fremovexattr,sendfile,splice,copy_file_range,io_setup,io_submit,io_uring_setup,io_uring_enter,io_uring_register,dup,dup2,dup3,close,close_range,fcntl,mmap,mremap,mprotect,munmap,ioctl' "$task_electron" "$task_app/dist/security-native.cjs" "$task_output" "$task_manifest" 2>&1 | tee "$task_output/native.log" || task_native_status=$?
printf '%s\n' 'Fáze 5/6: vyhodnocení skutečných pokusů o zápis, síťovou komunikaci a spuštění procesů.'
task_trace_status=0
"$task_python" -I -B "$task_app/../qualification/trace.py" --manifest "$task_manifest" --trace "$task_output/process.trace" --output "$task_output/trace-report.json" 2>&1 | tee "$task_output/trace-analysis.log" || task_trace_status=$?
printf '%s\n' 'Fáze 6/6: porovnání bajtů, adresářů a identit zdrojů před obnovením testovacích oprávnění.'
task_integrity_status=0
"$task_python" -I -B "$task_app/../qualification/fixtures.py" check --manifest "$task_manifest" --output "$task_output/source-integrity.json" 2>&1 | tee "$task_output/integrity.log" || task_integrity_status=$?
if ! "$task_node" --input-type=module - "$task_output/security-native.json" <<'JS'
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const report=JSON.parse(readFileSync(process.argv[2],'utf8'));
assert.equal(report.format,'jai.fabric-explorer.security-native/1');
assert.equal(report.status,'passed');
assert.equal(report.completedCases,8); assert.equal(report.totalCases,8);
assert.equal(report.observations.length,8); assert(report.observations.every(item=>item.status==='pass'));
assert.equal(report.integrity.unchanged,true); assert.equal(report.consoleErrors.length,0);
assert.equal(report.runtimePolicy.spellCheckerEnabled,false);
assert.deepEqual(report.runtimePolicy.spellCheckerLanguages,[]);
assert.deepEqual(report.runtimePolicy.dictionaryDownloads,[]);
assert.deepEqual(report.runtimePolicy.dictionaryFiles,[]);
JS
then
  task_native_status=1
fi
if [[ $task_native_status -ne 0 || $task_integrity_status -ne 0 ]]; then
  printf 'Ověření není úspěšné: aplikace=%s, sledování=%s, integrita=%s. Zachovejte výsledky.\n' "$task_native_status" "$task_trace_status" "$task_integrity_status" >&2
  exit 1
fi
if [[ $task_trace_status -ne 0 ]]; then
  if [[ $task_trace_status == 2 ]]; then
    printf '%s\n' 'Průchod aplikací a integrita prošly. Automatické vyhodnocení záznamu obsahuje otevřené operace nebo mezery; kvalifikace není dokončená.' 'Záznam zachovejte k nezávislému posouzení. Nový běh bez konkrétní opravy není potřeba.' >&2
    exit 2
  fi
  printf 'Vyhodnocení záznamu selhalo s kódem %s. Zachovejte výsledky.\n' "$task_trace_status" >&2
  exit 1
fi
task_restore_allowed=true
printf '%s\n' 'Běh dokončen. Výsledky ještě posoudí nezávislá kontrola; samotné dokončení není schválení S10.'
