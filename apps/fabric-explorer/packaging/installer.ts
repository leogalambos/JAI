/** Installation-only filesystem transaction; normal application startup never loads it. */
import { constants, createReadStream } from 'node:fs';
import * as fs from 'node:fs/promises';
import { createHash, randomUUID } from 'node:crypto';
import { join, relative, isAbsolute, sep } from 'node:path';
import { parseInventory, verifyManifest, sha256, type AssetManifest, type Inventory, type Target, runtimeExecutable } from './manifest.ts';
/** Trusted local bootstrap inputs; never renderer-provided installation authority. */
export interface InstallOptions {payloadRoot:string;
  manifestBytes:Uint8Array;
  signature:Uint8Array|null;
  publicKey:string|null;
  allowDevelopment:boolean;
  installRoot:string;
  preferencesRoot:string;
  platform:string;
  architecture:string;
  dryRun:boolean}
/** Finite operation result with planned actions and no native qualification claim. */
export interface InstallResult {operation:string;
  dryRun:boolean;
  version:string|null;
  actions:string[]}
const marker='jai-fabric-explorer-install/1\n';
const versionPattern=/^[A-Za-z0-9][A-Za-z0-9._-]{0,79}-[a-f0-9]{16}$/;
function fail(message:string):never {throw new Error(message);
  }
function inside(root:string,path:string):boolean {const p=relative(root,path);
  return p===''||(!p.startsWith('..'+sep)&&p!=='..'&&!isAbsolute(p));
  }
async function missing(path:string):Promise<boolean> {try {await fs.lstat(path);
  return false;
  } catch(e) {if((e as NodeJS.ErrnoException).code==='ENOENT')return true;
  throw e;
  }}
async function regular(path:string):Promise<void> {const s=await fs.lstat(path);
  if(!s.isFile()||s.nlink!==1)fail('Expected owned regular file');
  }
async function hashFile(path:string):Promise<string> {const hash=createHash('sha256');
  for await(const bytes of createReadStream(path))hash.update(bytes);
  return hash.digest('hex');
  }
/**
 * Inspect every entry, including link chains, without executing or altering the payload.
 * @param root Local extracted package root.
 * @param manifest Already authenticated manifest binding inventory and notices.
 * @returns The bound inventory after complete entry, link, hash, size and mode inspection; no writes occur.
 * @throws {Error} For an oversized inventory, metadata mismatch, extra/missing entry, hardlink, escaping link, changed bytes or filesystem read failure. No payload is executed.
 */
export async function inspectPayload(root:string,manifest:AssetManifest):Promise<Inventory> {
  const base=await fs.realpath(root);
  const inventoryPath=join(base,'inventory.json');
  await regular(inventoryPath);
  if((await fs.lstat(inventoryPath)).size>16*1024*1024)fail('Inventory size limit');
  const bytes=await fs.readFile(inventoryPath);
  if(bytes.length!==manifest.inventory.byteLength||sha256(bytes)!==manifest.inventory.sha256)fail('Inventory digest mismatch');
  const inventory=parseInventory(bytes);
  if(inventory.target!==manifest.target||inventory.productVersion!==manifest.productVersion)fail('Inventory binding mismatch');
  const expected=new Map(inventory.entries.map(e=>[e.path,e]));
  const seen=new Set<string>();
  async function walk(directory:string,prefix:string):Promise<void> {
    for(const name of await fs.readdir(directory)) {const path=prefix?prefix+'/'+name:name;
  const full=join(directory,name);
  const stat=await fs.lstat(full);
      if(path==='inventory.json')continue;
      const entry=expected.get(path);
  if(!entry)fail('Unexpected payload entry');
  seen.add(path);
      if(entry.kind==='symlink') {if(!stat.isSymbolicLink()||await fs.readlink(full)!==entry.target)fail('Link mismatch');
  const target=await fs.realpath(full);
  if(!inside(base,target))fail('Escaping payload link');
  }
      else if(entry.kind==='directory') {if(!stat.isDirectory()||stat.isSymbolicLink())fail('Directory mismatch');
  if(process.platform!=='win32'&&(stat.mode&0o777)!==entry.mode)fail('Mode mismatch');
  await walk(full,path);
  }
      else {if(!stat.isFile()||stat.nlink!==1||stat.size!==entry.size)fail('File mismatch');
  if(process.platform!=='win32'&&(stat.mode&0o777)!==entry.mode)fail('Mode mismatch');
  if(await hashFile(full)!==entry.sha256)fail('File digest mismatch');
  }
    }
  }
  await walk(base,'');
  if(seen.size!==expected.size)fail('Missing payload entry');
  const notices=join(base,manifest.notices.fileName);
  await regular(notices);
  if(await hashFile(notices)!==manifest.notices.sha256)fail('Notices digest mismatch');
  const sbom=join(base,manifest.sbom.fileName);
  await regular(sbom);
  if(await hashFile(sbom)!==manifest.sbom.sha256)fail('SBOM digest mismatch');
  return inventory;
}
function roots(installRoot:string,preferencesRoot:string):void {if(!isAbsolute(installRoot)||!isAbsolute(preferencesRoot)||inside(installRoot,preferencesRoot)||inside(preferencesRoot,installRoot))fail('Installation and preferences must be separate absolute roots');
  }
async function checkOwned(root:string,allowMissing:boolean):Promise<void> {
  if(await missing(root)) {if(allowMissing)return;
  fail('Installation is missing');
  }
  const stat=await fs.lstat(root);
  if(!stat.isDirectory()||stat.isSymbolicLink())fail('Unsafe installation root');
  if(await missing(join(root,'.viewer-install'))) {if((await fs.readdir(root)).length===0&&allowMissing)return;
  fail('Unrecognized installation root');
  }
  await regular(join(root,'.viewer-install'));
  if(await fs.readFile(join(root,'.viewer-install'),'utf8')!==marker)fail('Unrecognized installation root');
}
async function pointer(root:string):Promise<{current:string;
  previous:string}|null> {
  const path=join(root,'active');
  if(await missing(path))return null;
  await regular(path);
  const text=await fs.readFile(path,'utf8');
  const fields=text.split('\n');
  if(fields.length!==3||fields[2]!==''||!versionPattern.test(fields[0])||(fields[1]!==''&&!versionPattern.test(fields[1])))fail('Invalid active version pointer');
  return {current:fields[0],previous:fields[1]};
}
async function ownedVersions(root:string):Promise<string[]> {
  const path=join(root,'owned-versions.json');
  if(await missing(path))return [];
  await regular(path);
  const stat=await fs.stat(path);
  if(stat.size>1024*1024)fail('Version registry limit');
  const value:unknown=JSON.parse(await fs.readFile(path,'utf8'));
  if(!Array.isArray(value)||value.length>10000||value.some(v=>typeof v!=='string'||!versionPattern.test(v))||new Set(value).size!==value.length)fail('Invalid version registry');
  return value;
}
async function atomicPointer(root:string,current:string,previous:string):Promise<void> {
  const temp=join(root,'.active-'+randomUUID());
  try {await fs.writeFile(temp,current+'\n'+previous+'\n',{flag:'wx',mode:0o600});
  await fs.rename(temp,join(root,'active'));
  }finally {await fs.rm(temp,{force:true});
  }
}
function shellQuote(value:string):string {return "'"+value.replaceAll("'","'\\''")+"'";
  }
/**
 * Launcher performs no Node bootstrap and establishes Linux cache policy before Electron.
 * @param root Absolute per-user installation root.
 * @param target Explicit supported platform target.
 * @returns The native entrypoint filename and script body; generation performs no filesystem writes.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function launcher(root:string,target:Target):{name:string;
  body:string} {
  if(target==='win32-x64') {
    if(/[\r\n%"!]/.test(root))fail('Unsupported Windows installation path');
    return {name:'launch-viewer.cmd',body:`@echo off
setlocal DisableDelayedExpansion
set "ELECTRON_RUN_AS_NODE="
set "VIEWER_VERSION="
for /f "tokens=1,* delims=:" %%A in ('findstr /n /r /x "[A-Za-z0-9][A-Za-z0-9._-]*-[a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9]" "${root}\\active" ^| findstr /b "1:"') do set "VIEWER_VERSION=%%B"
if not defined VIEWER_VERSION exit /b 1
if not "%VIEWER_VERSION:~97,1%"=="" exit /b 1
"${root}\\versions\\%VIEWER_VERSION%\\runtime\\electron.exe" %*
`};
  }
  const executable=runtimeExecutable(target);
  return {name:'launch-viewer',body:'#!/bin/sh\nset -eu\nroot='+shellQuote(root)+'\nIFS= read -r version < "$root/active"\nprintf \'%s\\n\' "$version" | LC_ALL=C grep -Eq \'^[A-Za-z0-9][A-Za-z0-9._-]{0,79}-[a-f0-9]{16}$\' || exit 1\nunset ELECTRON_RUN_AS_NODE\n'+(target.startsWith('linux')?'export MESA_SHADER_CACHE_DISABLE=true\nexport GSETTINGS_BACKEND=memory\nbase="${XDG_CONFIG_HOME:-${HOME}/.config}"\nexport XDG_CACHE_HOME="$base/JAI Fabric Explorer/cache"\numask 077\nmkdir -p "$base"\nfor directory in "$base/JAI Fabric Explorer" "$XDG_CACHE_HOME"; do\n  [ ! -L "$directory" ] || exit 1\n  if [ ! -e "$directory" ]; then mkdir -m 700 "$directory"; fi\n  [ -d "$directory" ] && [ "$(stat -c %u "$directory")" = "$(id -u)" ] && [ "$(stat -c %a "$directory")" = 700 ] || exit 1\ndone\n':'')+'exec "$root/versions/$version/'+executable+'" "$@"\n'};
}
async function claim(root:string):Promise<()=>Promise<void>> {
  await fs.mkdir(root,{recursive:true,mode:0o700});
  const handle=await fs.open(join(root,'.install-claim'),constants.O_CREAT|constants.O_EXCL|constants.O_WRONLY,0o600);
  return async()=>{await handle.close();await fs.unlink(join(root,'.install-claim'));};
}
/**
 * Validate before writes, stage a whole version, then publish with one atomic pointer rename.
 * @param options Authenticated local package inputs and separate installation/preferences roots.
 * @returns An install plan when dryRun is true; otherwise the activated version and performed action names.
 * @throws {Error} For invalid trust/target/payload or ownership, concurrent installation, or filesystem failure. Validation precedes writes; staging failures preserve the active pointer. A failure after atomic publication may leave the complete new version active.
 */
export async function install(options:InstallOptions):Promise<InstallResult> {
  roots(options.installRoot,options.preferencesRoot);
  const manifest=verifyManifest(options.manifestBytes,options.signature,options.publicKey,options.allowDevelopment);
  if(manifest.target!==options.platform+'-'+options.architecture)fail('Wrong package architecture');
  await inspectPayload(options.payloadRoot,manifest);await checkOwned(options.installRoot,true);
  const version=manifest.productVersion+'-'+manifest.asset.sha256.slice(0,16);const actions=['verify package','stage '+version,'atomically activate '+version];
  if(options.dryRun)return {operation:'install',dryRun:true,version,actions};
  const release=await claim(options.installRoot);let staging:string|null=null;
  try {
    // Recheck mutable ownership after the exclusive claim, without accepting the claim as a marker.
    const names=await fs.readdir(options.installRoot);if(!names.includes('.viewer-install')&&names.some(n=>n!=='.install-claim'))fail('Unrecognized installation root');
    if(!names.includes('.viewer-install'))await fs.writeFile(join(options.installRoot,'.viewer-install'),marker,{flag:'wx',mode:0o600});
    const old=await pointer(options.installRoot);const versions=join(options.installRoot,'versions');await fs.mkdir(versions,{recursive:true,mode:0o700});
    const versionRootStat=await fs.lstat(versions);if(!versionRootStat.isDirectory()||versionRootStat.isSymbolicLink())fail('Unsafe versions directory');
    const destination=join(versions,version);
    if(await missing(destination)) {staging=join(options.installRoot,'.stage-'+randomUUID());await fs.mkdir(staging,{mode:0o700});await fs.cp(options.payloadRoot,staging,{recursive:true,dereference:false,verbatimSymlinks:true,preserveTimestamps:true});await inspectPayload(staging,manifest);await fs.rename(staging,destination);staging=null;}
    else {const stat=await fs.lstat(destination);if(!stat.isDirectory()||stat.isSymbolicLink())fail('Unsafe version directory');await inspectPayload(destination,manifest);}
    const launch=launcher(options.installRoot,manifest.target);const launchPath=join(options.installRoot,launch.name);if(!await missing(launchPath))await regular(launchPath);const launchTemp=join(options.installRoot,'.launcher-'+randomUUID());try {await fs.writeFile(launchTemp,launch.body,{flag:'wx',mode:0o700});await fs.rename(launchTemp,launchPath);}finally {await fs.rm(launchTemp,{force:true});}
    const owned=await ownedVersions(options.installRoot);if(!owned.includes(version)) {owned.push(version);const registryTemp=join(options.installRoot,'.versions-'+randomUUID());try {await fs.writeFile(registryTemp,JSON.stringify(owned)+'\n',{flag:'wx',mode:0o600});await fs.rename(registryTemp,join(options.installRoot,'owned-versions.json'));}finally {await fs.rm(registryTemp,{force:true});}}
    await atomicPointer(options.installRoot,version,old?.current===version?(old?.previous??''):(old?.current??''));
    return {operation:'install',dryRun:false,version,actions};
  } finally {try {if(staging!==null)await fs.rm(staging,{recursive:true,force:true});}finally {await release();}}
}
/**
 * Swap the two recorded version names without deleting either immutable payload.
 * @param installRoot Owned installation root.
 * @param dryRun Report read-only actions without writes.
 * @returns The previous version selected for activation; dry-run leaves the pointer unchanged.
 * @throws {Error} For missing/invalid previous version, concurrent changes or filesystem failure; atomic pointer replacement never deletes the old pointer first.
 */
export async function rollback(installRoot:string,dryRun=false):Promise<InstallResult> {
  await checkOwned(installRoot,false);const old=await pointer(installRoot);if(!old?.previous)fail('No previous version');
  const stat=await fs.lstat(join(installRoot,'versions',old.previous));if(!stat.isDirectory()||stat.isSymbolicLink())fail('Previous version unavailable');
  if(!dryRun) {const release=await claim(installRoot);try {const current=await pointer(installRoot);if(current?.current!==old.current||current.previous!==old.previous)fail('Installation changed');await atomicPointer(installRoot,old.previous,old.current);}finally {await release();}}
  return {operation:'rollback',dryRun,version:old.previous,actions:['activate previous version']};
}
/**
 * Remove only recorded payload versions; preferences require a distinct explicit purge.
 * @param installRoot Owned installation root.
 * @param dryRun Report read-only actions without writes.
 * @returns The removed active version and action names; unrelated files and preferences remain untouched.
 * @throws {Error} For invalid ownership, an active installation claim or filesystem failure. Removal may be partial if an OS denies a later deletion; preferences are never implicitly purged.
 */
export async function uninstall(installRoot:string,dryRun=false):Promise<InstallResult> {
  await checkOwned(installRoot,false);const old=await pointer(installRoot);const actions=['remove viewer launchers and recorded versions','preserve preferences'];
  if(dryRun)return {operation:'uninstall',dryRun:true,version:old?.current??null,actions};
  const release=await claim(installRoot);try {for(const name of ['launch-viewer','launch-viewer.cmd','active']) {const path=join(installRoot,name);if(!await missing(path)){await regular(path);await fs.unlink(path);}}
    for(const name of await ownedVersions(installRoot))await fs.rm(join(installRoot,'versions',name),{recursive:true,force:true});
    await fs.rm(join(installRoot,'owned-versions.json'),{force:true});
  }finally {await release();}
  return {operation:'uninstall',dryRun:false,version:old?.current??null,actions};
}
/**
 * Explicit preference purge is separate from binary removal and checks root separation.
 * @param installRoot Owned installation root.
 * @param preferencesRoot Separate explicitly selected viewer preferences root.
 * @param dryRun Report read-only actions without writes.
 * @returns A separate purge result; only the explicit preferences root is removed outside dry-run.
 * @throws {Error} For overlapping/unsafe roots or filesystem failure. Explicit recursive purge can be partial if the OS rejects a deletion.
 */
export async function purgePreferences(installRoot:string,preferencesRoot:string,dryRun=false):Promise<InstallResult> {
  roots(installRoot,preferencesRoot);await checkOwned(installRoot,false);
  if(!await missing(preferencesRoot)){const s=await fs.lstat(preferencesRoot);if(!s.isDirectory()||s.isSymbolicLink())fail('Unsafe preferences root');}
  if(!dryRun)await fs.rm(preferencesRoot,{recursive:true,force:true});return {operation:'purge',dryRun,version:null,actions:['remove explicitly selected viewer preferences']};
}
