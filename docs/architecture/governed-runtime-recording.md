# Runtime recording and recovery

The runtime maintains an append-only journal of ordinary work events and explicit
decisions. Ordinary author, reviewer and coordination records are not individually
signed. Only reserved L0 decisions require an external human signature.

## Identity and stored material

Canonical record content and explicit dependencies determine immutable version
identities. Repeated insertion or exact replay retains its established identity
and receipt; it does not create a second authority act.

The current journal format uses references to content-addressed supporting files
instead of repeatedly embedding complete files. Retain the journal and all
required referenced material together. Hashes identify content; they cannot
recover deleted files.

A cold initialization or explicit audit checks the historical prefix and its
required supporting material. Normal continuation reuses established state
instead of reconstructing and reverifying the whole history at every step.
Mutable conditions are checked when relevant to the new action.

## Integrity and applicability

Unavailable or corrupted required material is an explicit integrity gap.
A changed working file does not rewrite the historical snapshot or make a
truthful old execution applicable to the new input. The
[versioned lifecycle](governed-runtime-cutover.md) determines which uses remain
current and which decisions cancelled them.

## Restart and retention

Keep the newest journal, referenced files, session locator and pinned
enrollment/configuration together. Reconcile prepared or uncertain invocations
before repeating work. A recorded return and its exact handle must not be
silently replaced by a new model call.

Software recovery does not restore permission by rolling back the journal.
If the available reader does not support a stored format, retain the immutable
archive and begin distinct work from actual authorised inputs; no migration or
acceptance continuity is assumed.

Follow [deployment and recovery](../operations/gen2-deployment-recovery.md).
