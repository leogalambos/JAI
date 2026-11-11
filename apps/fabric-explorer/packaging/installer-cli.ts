/** Fixed installation entry executed by the bundled runtime, never by normal app startup. */
import { readInstallerFile } from './installer-files.ts';
import { install, rollback, uninstall, purgePreferences } from './installer.ts';
const args=process.argv.slice(2);
async function main():Promise<void> {
  const [operation,root,preferences,payload,manifest,signature,key]=args;
  const flags=args.slice(operation==='install'?7:3);
  if(!operation||!root||!preferences)throw new Error('Missing installation arguments');
  if(flags.some(f=>f!=='--allow-development'&&f!=='--dry-run'))throw new Error('Unknown installation argument');
  const dryRun=flags.includes('--dry-run');
  let result;
  if(operation==='install') {
    if(!payload||!manifest||!signature||!key)throw new Error('Missing package arguments');
    let signatureBytes:Buffer|null=null;
    if(signature!=='-')signatureBytes=await readInstallerFile(signature,64,64);
    result=await install({installRoot:root,preferencesRoot:preferences,payloadRoot:payload,manifestBytes:await readInstallerFile(manifest,65536),signature:signatureBytes,publicKey:key==='-'?null:new TextDecoder('utf-8',{fatal:true}).decode(await readInstallerFile(key,16384)),allowDevelopment:flags.includes('--allow-development'),platform:process.platform,architecture:process.arch,dryRun});
  } else if(operation==='rollback')result=await rollback(root,dryRun);
  else if(operation==='uninstall')result=await uninstall(root,dryRun);
  else if(operation==='purge')result=await purgePreferences(root,preferences,dryRun);
  else throw new Error('Unknown installation operation');
  process.stdout.write(JSON.stringify(result)+'\n');
}
main().catch(()=>{process.stderr.write('Viewer installation operation failed. Verify the local package and owned installation state.\n');
  process.exitCode=1;
  });
