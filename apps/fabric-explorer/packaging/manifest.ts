/** Exact-byte release metadata shared by build tooling and the installation helper. */
import { createHash, createPublicKey, verify } from 'node:crypto';
import { posix } from 'node:path';

/** Explicit release targets; no host inference or latest-version selection. */
export type Target = 'linux-x64' | 'linux-arm64' | 'win32-x64' | 'darwin-x64' | 'darwin-arm64';
/** One immutable package entry with exact bytes, permissions or relative link text. */
export type InventoryEntry = {path:string;
  kind:'file';
  size:number;
  sha256:string;
  mode:number} | {path:string;
  kind:'directory';
  mode:number} | {path:string;
  kind:'symlink';
  target:string};
/** Closed ordered package inventory; the containing manifest binds its exact bytes. */
export interface Inventory {format:'jai.fabric-explorer.inventory/1';
  productVersion:string;
  target:Target;
  entries:InventoryEntry[]}
/** Detached signed asset metadata; keys are supplied by the reviewed bootstrap. */
export interface AssetManifest {
  format:'jai.fabric-explorer.asset/1';
  status:'development'|'release';
  product:'jai-fabric-explorer';
  productVersion:string;
  target:Target;
  sourceRevision:{commit:string;
  dirty:boolean;
  closureSha256:string};
  signatureKeyId:string|null;
  notices:{fileName:'notices/third-party.txt';
  sha256:string};
  runtime:{name:'electron';
  version:'45.2.3';
  archiveSha256:string};
  asset:{fileName:string;
  byteLength:number;
  sha256:string};
  inventory:{fileName:'inventory.json';
  byteLength:number;
  sha256:string};
  sbom:{fileName:'notices/sbom.json';
  sha256:string};
}
const targets = new Set(['linux-x64','linux-arm64','win32-x64','darwin-x64','darwin-arm64']);
function requireValue(condition:unknown):asserts condition {if(!condition) throw new Error('Invalid package metadata');
  }
function object(value:unknown):Record<string,unknown> {requireValue(value!==null && typeof value==='object' && !Array.isArray(value));
  return value as Record<string,unknown>;
  }
function keys(value:Record<string,unknown>,expected:string[]):void {requireValue(Object.keys(value).sort().join(',')===expected.sort().join(','));
  }
function digest(value:unknown):void {requireValue(typeof value==='string' && /^[a-f0-9]{64}$/.test(value));
  }
function size(value:unknown):void {requireValue(Number.isSafeInteger(value) && (value as number)>=0);
  }
function version(value:unknown):void {requireValue(typeof value==='string' && /^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/.test(value));
  }
function mode(value:unknown):void {requireValue(Number.isInteger(value) && (value as number)>=0 && (value as number)<=0o777);
  }
/**
 * Reject paths whose platform interpretation could escape or alias the package root.
 * @param value Package-relative POSIX path.
 * @returns Nothing if the path has only confined portable components.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function validateRelativePath(value:string):void {
  requireValue(typeof value==='string' && value.length>0 && value.length<=4096 && !/[\\\x00-\x1f:]/.test(value));
  requireValue(!value.startsWith('/') && value.split('/').every(part=>part!=='' && part!=='.' && part!=='..'));
}
/**
 * Validate a relative link lexically; filesystem inspection also resolves link chains.
 * @param path Package-relative link entry.
 * @param target Exact relative link text.
 * @returns Nothing if the relative target stays lexically within the package root.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function validateLink(path:string,target:string):void {
  validateRelativePath(path);
  requireValue(typeof target==='string' && target.length>0 && target.length<=4096 && !/[\\\x00-\x1f:]/.test(target) && !target.startsWith('/'));
  const resolved=posix.normalize(posix.join(posix.dirname(path),target));
  requireValue(resolved!== '..' && !resolved.startsWith('../') && !resolved.startsWith('/'));
}
function decode(bytes:Uint8Array,limit:number):unknown {
  requireValue(bytes.byteLength<=limit);
  return JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
}
/**
 * Parse a closed manifest schema without altering the signed byte representation.
 * @param bytes Original bounded UTF-8 manifest bytes.
 * @returns A closed manifest parsed from the original bytes; parsing does not authenticate it.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function parseManifest(bytes:Uint8Array):AssetManifest {
  const v=object(decode(bytes,65536));
  keys(v,['format','status','product','productVersion','target','sourceRevision','signatureKeyId','notices','runtime','asset','inventory','sbom']);
  requireValue(v.format==='jai.fabric-explorer.asset/1' && (v.status==='release'||v.status==='development') && v.product==='jai-fabric-explorer' && targets.has(v.target as string));
  version(v.productVersion);
  const source=object(v.sourceRevision);
  keys(source,['commit','dirty','closureSha256']);
  requireValue(typeof source.commit==='string'&&/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(source.commit)&&typeof source.dirty==='boolean');
  digest(source.closureSha256);
  requireValue(v.signatureKeyId===null||typeof v.signatureKeyId==='string');
  if(v.signatureKeyId!==null)digest(v.signatureKeyId);
  if(v.status==='release')requireValue(v.signatureKeyId!==null);
  const notices=object(v.notices);
  keys(notices,['fileName','sha256']);
  requireValue(notices.fileName==='notices/third-party.txt');
  digest(notices.sha256);
  const r=object(v.runtime);
  keys(r,['name','version','archiveSha256']);
  requireValue(r.name==='electron'&&r.version==='45.2.3');
  digest(r.archiveSha256);
  for(const name of ['asset','inventory']) {const a=object(v[name]);
  keys(a,['fileName','byteLength','sha256']);
  requireValue(typeof a.fileName==='string');
  validateRelativePath(a.fileName);
  requireValue(/^[A-Za-z0-9][A-Za-z0-9._-]{0,199}$/.test(a.fileName));
  size(a.byteLength);
  digest(a.sha256);
  }
  requireValue(object(v.inventory).fileName==='inventory.json' && (object(v.inventory).byteLength as number)<=16*1024*1024);
  const s=object(v.sbom);
  keys(s,['fileName','sha256']);
  requireValue(s.fileName==='notices/sbom.json');
  digest(s.sha256);
  return v as unknown as AssetManifest;
}
/**
 * Encode validated metadata with fixed field order and one final newline.
 * @param value Closed manifest metadata to encode.
 * @returns UTF-8 JSON with fixed property order, two-space indentation and one final newline.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function encodeManifest(value:AssetManifest):Buffer {
  const v=value;
  const ordered={format:v.format,status:v.status,product:v.product,productVersion:v.productVersion,target:v.target,sourceRevision:{commit:v.sourceRevision.commit,dirty:v.sourceRevision.dirty,closureSha256:v.sourceRevision.closureSha256},signatureKeyId:v.signatureKeyId,notices:{fileName:v.notices.fileName,sha256:v.notices.sha256},runtime:{name:v.runtime.name,version:v.runtime.version,archiveSha256:v.runtime.archiveSha256},asset:{fileName:v.asset.fileName,byteLength:v.asset.byteLength,sha256:v.asset.sha256},inventory:{fileName:v.inventory.fileName,byteLength:v.inventory.byteLength,sha256:v.inventory.sha256},sbom:{fileName:v.sbom.fileName,sha256:v.sbom.sha256}};
  const bytes=Buffer.from(JSON.stringify(ordered,null,2)+'\n');
  parseManifest(bytes);
  return bytes;
}
/**
 * Parse an ordered, unique, closed inventory; links retain their exact targets.
 * @param bytes Original bounded UTF-8 inventory bytes.
 * @returns An ordered unique inventory; filesystem entry and link-chain verification remains separate.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function parseInventory(bytes:Uint8Array):Inventory {
  const v=object(decode(bytes,16*1024*1024));
  keys(v,['format','productVersion','target','entries']);
  requireValue(v.format==='jai.fabric-explorer.inventory/1'&&targets.has(v.target as string));
  version(v.productVersion);
  requireValue(Array.isArray(v.entries)&&v.entries.length<=100000);
  let previous='';
  for(const entry of v.entries) {const e=object(entry);
  requireValue(typeof e.path==='string');
  validateRelativePath(e.path);
  requireValue(e.path>previous && e.path!=='inventory.json');
  previous=e.path;
    if(e.kind==='file') {keys(e,['path','kind','size','sha256','mode']);
  size(e.size);
  digest(e.sha256);
  mode(e.mode);
  }
    else if(e.kind==='directory') {keys(e,['path','kind','mode']);
  mode(e.mode);
  }
    else {requireValue(e.kind==='symlink'&&typeof e.target==='string');
  keys(e,['path','kind','target']);
  validateLink(e.path,e.target);
  }
  }
  return v as unknown as Inventory;
}
/**
 * Verify the original bytes; unsigned development needs both explicit conditions.
 * @param bytes Exact signed manifest bytes.
 * @param signature Detached Ed25519 signature, or null for explicit development.
 * @param publicKey Reviewed distributor SPKI PEM, never asset-selected.
 * @param allowDevelopment Explicit opt-in; also requires development metadata.
 * @returns The authenticated manifest, or an explicitly permitted unsigned development manifest.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function verifyManifest(bytes:Uint8Array,signature:Uint8Array|null,publicKey:string|null,allowDevelopment:boolean):AssetManifest {
  const manifest=parseManifest(bytes);
  if(signature===null) {requireValue(allowDevelopment&&manifest.status==='development'&&manifest.signatureKeyId===null);
  return manifest;
  }
  requireValue(publicKey!==null&&signature.byteLength===64&&manifest.signatureKeyId===signatureKeyId(publicKey)&&verify(null,bytes,publicKey,signature));
  return manifest;
}
/**
 * SHA-256 for exact payload bytes, never a normalized source representation.
 * @param bytes Exact input bytes.
 * @returns The 64-character lowercase SHA-256 of the exact bytes.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function sha256(bytes:Uint8Array):string {return createHash('sha256').update(bytes).digest('hex');
  }

/**
 * Native Electron resources path; launching the executable needs no application argument.
 * @param target Explicit supported platform target.
 * @returns The native resources/app path inside the portable runtime payload.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function applicationPrefix(target:Target):string {
  return target.startsWith('darwin')?'runtime/Electron.app/Contents/Resources/app':'runtime/resources/app';
}

/**
 * Key identity describes the trusted SPKI, never a key selected by an asset.
 * @param publicKey Reviewed Ed25519 public SPKI PEM.
 * @returns The lowercase SHA-256 of the trusted Ed25519 DER SPKI.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function signatureKeyId(publicKey:string):string {const key=createPublicKey(publicKey);
  requireValue(key.asymmetricKeyType==='ed25519');
  return sha256(key.export({format:'der',type:'spki'}));
  }
/**
 * Fixed native executable path shared by staging and launch logic.
 * @param target Explicit supported platform target.
 * @returns The fixed package-relative native Electron executable path.
 * @throws {Error} If input, trust, ownership or filesystem invariants fail.
 */
export function runtimeExecutable(target:Target):string {return target.startsWith('darwin')?'runtime/Electron.app/Contents/MacOS/Electron':target==='win32-x64'?'runtime/electron.exe':'runtime/electron';
  }
