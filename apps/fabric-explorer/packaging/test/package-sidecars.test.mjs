/** Real filesystem and CLI coverage for manifest-bound external development installers. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm, lstat, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { generateDevelopmentSidecars } from '../bootstrap-sidecars.mjs';
import { encodeManifest, sha256 } from '../manifest.ts';
const cli=resolve('apps/fabric-explorer/packaging/bootstrap-sidecars.mjs');
async function fixture(run) {const root=await mkdtemp(join(tmpdir(),'jai-sidecars-'));try {await run(root);}finally {await rm(root,{recursive:true,force:true});}}
function metadata(target='linux-x64') {return {format:'jai.fabric-explorer.asset/1',status:'development',product:'jai-fabric-explorer',productVersion:'1',target,sourceRevision:{commit:'a'.repeat(40),dirty:true,closureSha256:'b'.repeat(64)},signatureKeyId:null,runtime:{name:'electron',version:'45.2.3',archiveSha256:'c'.repeat(64)},asset:{fileName:target==='win32-x64'?'viewer.zip':'viewer.tar.gz',byteLength:1,sha256:'d'.repeat(64)},inventory:{fileName:'inventory.json',byteLength:1,sha256:'e'.repeat(64)},sbom:{fileName:'notices/sbom.json',sha256:'f'.repeat(64)},notices:{fileName:'notices/third-party.txt',sha256:'0'.repeat(64)}};}
async function manifest(root,value) {const bytes=encodeManifest(value);await writeFile(join(root,value.asset.fileName+'.manifest.json'),bytes);return bytes;}
test('sidecar CLI binds exact existing manifest bytes, preserves input bytes and is idempotent',async()=>fixture(async root=>{
 const bytes=await manifest(root,metadata());const before=sha256(bytes);
 execFileSync(process.execPath,[cli,root,'--allow-development']);const path=join(root,'viewer.tar.gz.install.sh');
 const script=await readFile(path,'utf8');assert.ok(script.includes(before));assert.match(script,/XDG_DATA_HOME/);assert.equal((await lstat(path)).mode&0o777,0o755);
 assert.deepEqual(await generateDevelopmentSidecars(root),[path]);assert.equal(sha256(await readFile(join(root,'viewer.tar.gz.manifest.json'))),before);
 assert.notEqual(spawnSync(process.execPath,[cli,root]).status,0);execFileSync('sh',['-n',path]);
}));
test('Windows and macOS scripts select their frozen generators without execution',async()=>fixture(async root=>{
 await manifest(root,metadata('win32-x64'));const files=await generateDevelopmentSidecars(root);assert.match(await readFile(files[0],'utf8'),/Expand-Archive/);assert.equal((await lstat(files[0])).mode&0o777,0o644);
 await rm(join(root,'viewer.zip.manifest.json'));await manifest(root,metadata('darwin-arm64'));assert.match(await readFile((await generateDevelopmentSidecars(root))[0],'utf8'),/Darwin/);
}));
test('empty, release, mismatched names and conflicting outputs fail without replacing scripts',async()=>fixture(async root=>{
 await assert.rejects(generateDevelopmentSidecars(root),/No completed/);
 const release={...metadata(),status:'release',signatureKeyId:'a'.repeat(64)};await manifest(root,release);await assert.rejects(generateDevelopmentSidecars(root),/unsigned development/);
 await manifest(root,metadata());const path=join(root,'viewer.tar.gz.install.sh');await writeFile(path,'preserve');await assert.rejects(generateDevelopmentSidecars(root),/already differs/);assert.equal(await readFile(path,'utf8'),'preserve');
 await rm(path);await symlink('viewer.tar.gz.manifest.json',path);await assert.rejects(generateDevelopmentSidecars(root),/regular file/);
 await rm(path);await rm(join(root,'viewer.tar.gz.manifest.json'));await writeFile(join(root,'wrong.manifest.json'),encodeManifest(metadata()));await assert.rejects(generateDevelopmentSidecars(root),/filename mismatch/);
}));
