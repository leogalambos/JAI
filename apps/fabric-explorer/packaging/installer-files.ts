/** Bounded reads for installation metadata, before JSON or cryptographic decoding. */
import { constants } from 'node:fs';
import { lstat, open } from 'node:fs/promises';

/**
 * Read a nonlinked regular metadata file through one read-only handle.
 * @param path Bootstrap-selected local metadata path, never a renderer path.
 * @param maximum Maximum byte length, checked on the opened handle before allocation.
 * @param exact Optional required size, used for the 64-byte Ed25519 signature.
 * @returns Exact stable bytes, with at most maximum+1 bytes allocated for growth detection.
 * @throws {Error} For a link, nonregular file, oversized/changed input or filesystem failure. The handle is closed on every path.
 */
export async function readInstallerFile(path:string,maximum:number,exact?:number):Promise<Buffer> {
  if(!Number.isSafeInteger(maximum)||maximum<0||maximum>65536||(exact!==undefined&&(!Number.isSafeInteger(exact)||exact<0||exact>maximum)))throw new Error('Invalid installation metadata bound');
  const admitted=await lstat(path,{bigint:true});
  if(!admitted.isFile()||admitted.nlink!==1n)throw new Error('Installation metadata must be a regular file');
  const handle=await open(path,constants.O_RDONLY|(constants.O_NOFOLLOW??0)|(constants.O_NONBLOCK??0));
  try {
    const before=await handle.stat({bigint:true});
    if(!before.isFile()||before.nlink!==1n||before.dev!==admitted.dev||before.ino!==admitted.ino||before.size>BigInt(maximum)||(exact!==undefined&&before.size!==BigInt(exact)))throw new Error('Installation metadata size or identity mismatch');
    const bytes=Buffer.alloc(Number(before.size)+1);
    let length=0;
    while(length<bytes.length) {
      const result=await handle.read(bytes,length,bytes.length-length,length);
      if(result.bytesRead===0)break;
      length+=result.bytesRead;
    }
    const after=await handle.stat({bigint:true});
    if(length!==Number(before.size)||after.size!==before.size||after.mtimeNs!==before.mtimeNs||after.ctimeNs!==before.ctimeNs)throw new Error('Installation metadata changed during read');
    return bytes.subarray(0,length);
  } finally {
    await handle.close();
  }
}
