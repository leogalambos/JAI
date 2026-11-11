/** Generate fixed-digest local installers. No installer downloads any input. */
import { parseManifest, sha256, runtimeExecutable, signatureKeyId } from '../manifest.ts';
/** Exact manifest and fixed distributor key embedded through the reviewed channel. */
export interface BootstrapInput {manifestBytes:Uint8Array;
  publicKey:string|null}
function quote(value:string):string {return "'"+value.replaceAll("'","'\\''")+"'";
  }
/**
 * POSIX bootstrap verifies trusted sibling bytes before any extraction or runtime execution.
 * @param input Fixed manifest bytes and reviewed distributor public key.
 * @returns A POSIX shell script binding exact local asset/manifest hashes and reviewed trust.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function posixBootstrap(input:BootstrapInput):string {
  const m=parseManifest(input.manifestBytes);
  if(m.status==='release'&&(input.publicKey===null||signatureKeyId(input.publicKey)!==m.signatureKeyId))throw new Error('Release requires the reviewed distributor key');
  if(m.target==='win32-x64')throw new Error('Not a POSIX target');
  const key=input.publicKey??'';
  if(key.includes('TRUSTED_VIEWER_KEY'))throw new Error('Invalid key delimiter');
  return `#!/bin/sh
set -eu
asset_name=${quote(m.asset.fileName)}
asset_digest=${quote(m.asset.sha256)}
manifest_digest=${quote(sha256(input.manifestBytes))}
${m.target.startsWith('darwin')?'[ "$(uname -s)" = Darwin ] || { echo "Wrong platform" >&2; exit 1; }':'[ "$(uname -s)" = Linux ] || { echo "Wrong platform" >&2; exit 1; }'}
case "$(uname -m)" in ${m.target.endsWith('arm64')?'aarch64|arm64':'x86_64|amd64'}) ;; *) echo "Wrong architecture" >&2; exit 1;; esac
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
asset="$base/$asset_name"
manifest="$asset.manifest.json"
allow=
dry=no
operation=install
for arg in "$@"; do case "$arg" in --allow-development) allow=--allow-development;; --dry-run) dry=yes;; --uninstall) operation=uninstall;; --rollback) operation=rollback;; --purge-preferences) operation=purge;; *) echo 'Unknown installation argument' >&2; exit 1;; esac; done
[ -f "$asset" ] && [ -f "$manifest" ] || { echo 'Required local package is missing' >&2; exit 1; }
if command -v sha256sum >/dev/null 2>&1; then digest() { sha256sum "$1" | cut -d ' ' -f 1; }; else digest() { shasum -a 256 "$1" | cut -d ' ' -f 1; }; fi
[ "$(digest "$asset")" = "$asset_digest" ] && [ "$(digest "$manifest")" = "$manifest_digest" ] || { echo 'Package digest mismatch' >&2; exit 1; }
${m.status==='release'?'[ -f "$asset.manifest.sig" ] || exit 1':'[ "$allow" = --allow-development ] || { echo \'Development package requires --allow-development\' >&2; exit 1; }'}
${m.target.startsWith('darwin')?'root="$HOME/Applications/JAI Fabric Explorer"\npreferences="$HOME/Library/Application Support/JAI Fabric Explorer"':'root="${XDG_DATA_HOME:-$HOME/.local/share}/jai-fabric-explorer/install"\npreferences="${XDG_CONFIG_HOME:-$HOME/.config}/JAI Fabric Explorer"'}
if [ "$dry" = yes ]; then printf 'Plan %s for %s in %s; preferences %s\\n' "$operation" "$asset_name" "$root" "$preferences"; exit 0; fi
umask 077
stage=$(mktemp -d "\${TMPDIR:-/tmp}/jai-viewer-install.XXXXXXXX")
trap 'rm -rf -- "$stage"' EXIT HUP INT TERM
mkdir "$stage/payload"
tar -xpzf "$asset" -C "$stage/payload"
cat > "$stage/distributor-key.pem" <<'TRUSTED_VIEWER_KEY'
${key}
TRUSTED_VIEWER_KEY
key="$stage/distributor-key.pem"
${input.publicKey===null?'key=-':''}
signature=-
[ ! -f "$asset.manifest.sig" ] || signature="$asset.manifest.sig"
if [ "$operation" = install ]; then
  ELECTRON_RUN_AS_NODE=1 "$stage/payload/${runtimeExecutable(m.target)}" "$stage/payload/installer.cjs" install "$root" "$preferences" "$stage/payload" "$manifest" "$signature" "$key" \${allow:+"$allow"}
else
  ELECTRON_RUN_AS_NODE=1 "$stage/payload/${runtimeExecutable(m.target)}" "$stage/payload/installer.cjs" "$operation" "$root" "$preferences"
fi
`;
}
/**
 * Windows bootstrap uses fixed hashes and the platform ZIP extractor, never npm or Python.
 * @param input Fixed manifest bytes and reviewed distributor public key.
 * @returns A PowerShell script binding exact local asset/manifest hashes and reviewed trust.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function powershellBootstrap(input:BootstrapInput):string {
  const m=parseManifest(input.manifestBytes);
  if(m.status==='release'&&(input.publicKey===null||signatureKeyId(input.publicKey)!==m.signatureKeyId))throw new Error('Release requires the reviewed distributor key');
  if(m.target!=='win32-x64')throw new Error('Not a Windows target');
  const key=(input.publicKey??'').replaceAll("'","''");
  return `param([switch]$DryRun, [switch]$AllowDevelopment, [ValidateSet('install','uninstall','rollback','purge')][string]$Operation = 'install')
$ErrorActionPreference = 'Stop'
if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT -or [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString() -ne 'X64') { throw 'Wrong platform or architecture' }
$asset = Join-Path $PSScriptRoot '${m.asset.fileName}'
$manifest = "$asset.manifest.json"
if (!(Test-Path -LiteralPath $asset -PathType Leaf) -or !(Test-Path -LiteralPath $manifest -PathType Leaf)) { throw 'Required local package is missing' }
if ((Get-FileHash -LiteralPath $asset -Algorithm SHA256).Hash.ToLowerInvariant() -ne '${m.asset.sha256}' -or (Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne '${sha256(input.manifestBytes)}') { throw 'Package digest mismatch' }
${m.status==='release'?`if (!(Test-Path -LiteralPath "$asset.manifest.sig" -PathType Leaf)) { throw 'Release signature missing' }`:`if (!$AllowDevelopment) { throw 'Development package requires -AllowDevelopment' }`}
$root = Join-Path $env:LOCALAPPDATA 'JAI Fabric Explorer Install'
$preferences = Join-Path $env:APPDATA 'JAI Fabric Explorer'
if ($DryRun) { Write-Output "Plan $Operation for $asset in $root; preferences $preferences"; exit 0 }
$stage = Join-Path ([IO.Path]::GetTempPath()) ('jai-viewer-install-' + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $stage | Out-Null
$previousNode = $env:ELECTRON_RUN_AS_NODE
try {
  Expand-Archive -LiteralPath $asset -DestinationPath (Join-Path $stage 'payload')
  $key = '-'
  ${input.publicKey===null?'':`$key = Join-Path $stage 'distributor-key.pem'\n  [IO.File]::WriteAllText($key, '${key}', [Text.UTF8Encoding]::new($false))`}
  $signature = '-'
  if (Test-Path -LiteralPath "$asset.manifest.sig") { $signature = "$asset.manifest.sig" }
  $env:ELECTRON_RUN_AS_NODE = '1'
  $arguments = @((Join-Path $stage 'payload\\installer.cjs'), $Operation, $root, $preferences)
  if ($Operation -eq 'install') {
    $arguments += @((Join-Path $stage 'payload'), $manifest, $signature, $key)
    if ($AllowDevelopment) { $arguments += '--allow-development' }
  }
  & (Join-Path $stage 'payload\\runtime\\electron.exe') @arguments
  if ($LASTEXITCODE -ne 0) { throw 'Viewer installation failed' }
} finally {
  $env:ELECTRON_RUN_AS_NODE = $previousNode
  Remove-Item -LiteralPath $stage -Recurse -Force
}
`;
}
