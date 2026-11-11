import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {encodeManifest,sha256,type AssetManifest} from '../manifest.ts';
const helper=fileURLToPath(new URL('../../desktop/dist/installer.cjs',import.meta.url));
const electron=fileURLToPath(new URL('../../desktop/node_modules/electron/dist/'+(process.platform==='win32'?'electron.exe':process.platform==='darwin'?'Electron.app/Contents/MacOS/Electron':'electron'),import.meta.url));
test('actual Electron Node-mode compiled helper performs dry-run, upgrade, rollback, removal and explicit purge',async()=>{
  const base=await fs.mkdtemp(join(tmpdir(),'viewer-compiled-cli-'));
  try {
    await fs.stat(helper);await fs.stat(electron);
    const payload=join(base,'payload');const root=join(base,'installed');const preferences=join(base,'preferences');const manifestFile=join(base,'asset.manifest.json');
    await fs.mkdir(join(payload,'notices'),{recursive:true});await fs.chmod(join(payload,'notices'),0o755);
    for(const name of ['sbom.json','third-party.txt']){await fs.writeFile(join(payload,'notices',name),'{}',{mode:0o644});}
    const entries=[{path:'notices',kind:'directory',mode:0o755},...['sbom.json','third-party.txt'].map(name=>({path:'notices/'+name,kind:'file',mode:0o644,size:2,sha256:sha256(Buffer.from('{}'))}))];
    const manifest:AssetManifest={format:'jai.fabric-explorer.asset/1',status:'development',product:'jai-fabric-explorer',productVersion:'1',target:'linux-x64',sourceRevision:{commit:'a'.repeat(40),dirty:false,closureSha256:'b'.repeat(64)},signatureKeyId:null,notices:{fileName:'notices/third-party.txt',sha256:sha256(Buffer.from('{}'))},runtime:{name:'electron',version:'45.2.3',archiveSha256:'c'.repeat(64)},asset:{fileName:'viewer.tar.gz',byteLength:1,sha256:'d'.repeat(64)},inventory:{fileName:'inventory.json',byteLength:0,sha256:'e'.repeat(64)},sbom:{fileName:'notices/sbom.json',sha256:sha256(Buffer.from('{}'))}};
    async function prepare(version:string):Promise<void>{manifest.productVersion=version;const inventory=Buffer.from(JSON.stringify({format:'jai.fabric-explorer.inventory/1',productVersion:version,target:manifest.target,entries}));await fs.writeFile(join(payload,'inventory.json'),inventory);manifest.inventory={...manifest.inventory,byteLength:inventory.length,sha256:sha256(inventory)};await fs.writeFile(manifestFile,encodeManifest(manifest));}
    function invoke(operation:string,flags:string[]=[]){const args=operation==='install'?[operation,root,preferences,payload,manifestFile,'-','-',...flags]:[operation,root,preferences,...flags];return spawnSync(electron,[helper,...args],{timeout:5000,encoding:'utf8',env:{...process.env,ELECTRON_RUN_AS_NODE:'1'}});}
    await prepare('1');let result=invoke('install',['--allow-development','--dry-run']);assert.equal(result.status,0,result.stderr);assert.equal(JSON.parse(result.stdout).dryRun,true);await assert.rejects(fs.stat(root),{code:'ENOENT'});
    result=invoke('install');assert.notEqual(result.status,0);await assert.rejects(fs.stat(root),{code:'ENOENT'});
    result=invoke('install',['--allow-development']);assert.equal(result.status,0,result.stderr);const old=(await fs.readFile(join(root,'active'),'utf8')).split('\n')[0];await fs.mkdir(preferences);await fs.writeFile(join(preferences,'settings'),'retain');
    await prepare('2');result=invoke('install',['--allow-development']);assert.equal(result.status,0,result.stderr);assert.match(await fs.readFile(join(root,'active'),'utf8'),/^2-/);
    result=invoke('rollback',['--dry-run']);assert.equal(result.status,0,result.stderr);assert.equal(JSON.parse(result.stdout).dryRun,true);assert.match(await fs.readFile(join(root,'active'),'utf8'),/^2-/);
    result=invoke('rollback');assert.equal(result.status,0,result.stderr);assert.equal((await fs.readFile(join(root,'active'),'utf8')).split('\n')[0],old);
    result=invoke('uninstall');assert.equal(result.status,0,result.stderr);assert.equal(await fs.readFile(join(preferences,'settings'),'utf8'),'retain');await assert.rejects(fs.stat(join(root,'active')),{code:'ENOENT'});
    result=invoke('purge');assert.equal(result.status,0,result.stderr);await assert.rejects(fs.stat(preferences),{code:'ENOENT'});
  } finally {await fs.rm(base,{recursive:true,force:true});}
});
test('actual CLI rejects oversized signature before unbounded file allocation',async()=>{const base=await fs.mkdtemp(join(tmpdir(),'viewer-signature-bound-'));try{const signature=join(base,'signature');const manifest=join(base,'manifest');const marker=join(base,'allocation-observed');await fs.writeFile(signature,Buffer.alloc(65));await fs.writeFile(manifest,'{}');const preload=join(base,'read-observer.cjs');await fs.writeFile(preload,`const fs=require('node:fs');const original=fs.promises.readFile;fs.promises.readFile=async function(path,...args){if(String(path)===${JSON.stringify(signature)})fs.writeFileSync(${JSON.stringify(marker)},'unbounded read requested');return original.call(this,path,...args);};require('node:module').syncBuiltinESMExports();`);const result=spawnSync(electron,['--require',preload,helper,'install',join(base,'install'),join(base,'prefs'),join(base,'payload'),manifest,signature,'-','--allow-development'],{timeout:5000,env:{...process.env,ELECTRON_RUN_AS_NODE:'1'}});assert.notEqual(result.status,0);await assert.rejects(fs.stat(marker),{code:'ENOENT'});}finally{await fs.rm(base,{recursive:true,force:true});}});
