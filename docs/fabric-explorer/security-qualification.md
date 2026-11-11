# Linux read-only and process qualification

The development qualification runner observes the actual viewer and its child
processes while they read synthetic Fabric and Findings sources protected by
operating-system write-denied ACLs. It does not use personal project data.

The Linux launch contract is established before Electron starts: Mesa disk
shader caching is disabled, `XDG_CACHE_HOME` names a private directory inside
the declared application cache, and `GSETTINGS_BACKEND=memory` prevents native
desktop settings persistence. These settings apply only to the launched test
process tree. The user's `HOME` and desktop runtime directory are preserved.
Application JavaScript starts after native-library initialization, so the
launcher owns this boundary. Packaged launch qualification must carry the same
contract; this check does not qualify launching the development Electron binary
without that environment.

From a Linux desktop terminal, with the pinned local development toolchain and
dependencies already present, run:

```sh
bash apps/fabric-explorer/desktop/tools/run-security-check.sh
```

The runner requires `strace`, `setfacl`, `getfacl`, `timeout` and `sha256sum`.
It first checks tracing support, builds a dedicated development helper, creates
synthetic sources, proves that source writes fail, then observes one finite
viewer session. The observed session has a 180-second limit followed by a
five-second forced-stop allowance. It needs no manual answers. Closing the
window or pressing Ctrl+C stops the run. Do not disable Electron sandboxing or
run the test as root to turn an unavailable observation into a passing result.

The evidence directory contains exact tested-input and runtime hashes, the raw
process trace, classified operations, native observations and a source-integrity
comparison. Treat these records as private: they contain local paths and process
metadata. Completion alone does not establish release approval. Independent
review must distinguish successful actions, denied attempts and unresolved trace
coverage, including process descendants and descriptor-relative operations.
Local desktop IPC is assessed separately from IP network communication.
At session creation, the dictionary-language list is synchronously cleared
before yielding or creating a window, and session/window spellchecking is
disabled. The native check records the empty list, dictionary download-start
events and downloaded files; it requires no download event or dictionary file.
The enable flag alone does not cancel Chromium's queued dictionary loads.
The forged-session case deliberately invokes a request with a foreign session.
Electron logs its rejection as `session-mismatch`; the runner labels this expected
negative observation before and after the call. Unexpected renderer errors still
fail qualification.

Fixture preparation and deliberate negative write probes happen before the
observed application interval. The application interval does not deliberately
modify sources or start a test HTTP endpoint. Source bytes, directory membership
and physical identities are compared before restoring test permissions. An
interrupted or failed observed run leaves the synthetic sources read-only;
automatic permission restoration is suppressed. The runner never deletes source
directories. Normal application builds exclude the qualification helper.

This check covers the Linux development composition only. It does not qualify
Windows or macOS, packaged runtime contents, signatures, performance or every
possible future operation. Re-run affected checks when relevant application,
helper, dependency, runtime or operating-system enforcement inputs change.

## Trace interpretation limits

A completed functional journey and unchanged source bytes do not establish
complete process-wide observation. Desktop runtime namespaces, remapped paths,
helper processes and successful asynchronous I/O can exceed a syscall decoder's
evidence model. In particular, a syscall log may show an asynchronous submission
without identifying the targets stored in its shared-memory request queue.
Unknown targets or process ancestry must remain explicit coverage gaps.

For a long retained trace, complete-input accounting uses exact decision
counters independently of bounded event examples. This prevents a limited
sample from hiding a later adverse event, but it does not resolve unsupported
semantics. Distinguish full input consumption from complete interpretation and
from a clean result. Do not exempt a helper merely by name, silently discard
unknown operations or turn an incomplete report into a pass. The
[support policy](support.md) states the current product assurance boundary.
