# Importing local source journals

## Before you open a project: are there records to display?

Fabric Explorer displays existing journals. Installing JAI, using a specialist
role, or completing an ordinary development task does **not** by itself create
a Fabric history. A project directory, source files and chat history are not
viewer inputs.

| Work performed | Records available to the viewer | Usual location |
| --- | --- | --- |
| A layered engagement actually started through the governed runtime (`/layered` or `$workflow-layered`) | Fabric records for the engagement and its captured materials | Project `.fabric/`, unless the host adapter selects another home |
| Another JAI operation actually submits records to the Fabric runtime | The records that operation committed; a six-layer run is not required | The operation's explicit journal home; direct Fabric CLI defaults to `~/.ai/fabric/` or `FABRIC_HOME` |
| A review records findings | Findings and their recorded subjects or textual locations; Fabric may be absent | Project `.findings/`, or the location selected by `FINDINGS_HOME` |
| Roles or workflows were used without writing either journal family | No recorded history to import | No source journal is implied by using JAI |

**If no layered engagement or other Fabric-writing operation has run, do not
expect a Fabric journal just because JAI was used in the project.** A review may
still have produced findings independently. Read-only inspection and the viewer
itself do not generate the missing history.

### Choose only the source families you have

Check the project for existing `.jsonl` journals and select the matching families
in **Sources** before choosing **Open sources…**:

- **Fabric and Findings:** select both when both journal families exist.
- **Findings only:** deselect Fabric. Findings can be explored without a Fabric
  journal; their textual locations remain unresolved associations where no exact
  recorded subject is available.
- **Fabric only:** deselect Findings. The viewer can display the Fabric history
  without a findings ledger.
- **Neither family:** there is no recorded graph for the viewer to import.

An empty directory or an empty journal supplies no graph facts. When the records
live outside the project, select the intended project and use the manual file
dialog to choose the engagement's existing journal from its actual home. The
project lookup checks `.fabric/` and `.findings/`; it does not automatically
search `~/.ai/fabric/` or environment-selected homes. Missing project sources can
therefore open a file dialog even when the journal exists elsewhere.

For Fabric, keep the journal together with its companion
`<journal-name>.blobs/` directory so recorded material remains available. See
[Fabric storage and recovery](../capabilities/justifiable-fabric.md#storage-and-recovery)
for the difference between project-local and direct-CLI storage.

## Select and load supported journals

Fabric Explorer imports sources selected through its native project picker. For Fabric and Findings, direct regular `.jsonl` files in the selected project’s `.fabric/` and `.findings/` directories are selected automatically when lookup returns a complete bounded list. Missing, inaccessible or over-limit lookup uses a manual file dialog rooted in the project or its available family directory. Audit and nonstandard source locations remain manual. Lookup does not parse or validate journal contents. The single **Open sources…** action admits read-only handles and immediately imports the accepted selection into a coherent snapshot. A separate initial Import action is not required. Loading reports progress and can be cancelled. **Retry import** is available after a failed or cancelled load when sources remain admitted without a usable snapshot; **Refresh snapshot** explicitly observes later source changes. A successful snapshot is an **observed revision set**: each journal has its own digest, head, sequence and observation time. It is not a globally atomic transaction across Fabric and Findings.

| Selected family | Supported input | Interpretation |
| --- | --- | --- |
| Fabric | Format `9`, protocol `jai.governed-delivery/1`, manifest `jai.lifecycle.manifest/2` | Direct projection of recorded effects across six record families and recorded decisions |
| Findings | Unversioned append-only findings envelope | Direct event parsing and recorded state reduction; no invented envelope version |
| Audit | Optional `jai.gen2-audit/1` selection | Explicit unsupported-adapter diagnostic in this import build; never silently omitted or treated as a full journal |

An existing empty Fabric journal has no declared format or protocol. Its report retains null declarations and an explicit empty-journal limitation; future records must use a supported format. An empty source cannot supply record facts.

The application transfers native read-only source handles to its fixed TypeScript import worker. Each source is streamed once into its private archive while recorded data is projected directly into the compact graph; no Python runtime or intermediate fact transport is involved. It reads recorded manifests and effects to build version, use-point and dependency views. It does not call the canonical Store, replay or derivation engine, verify journal chains or signatures, consult public trust, or assess authority and current applicability. A recorded use state or decision remains a source claim. Successful parsing grants no authority and does not make an assessment fresh. Source heads remain recorded claims; physical JSONL row counts and row ordinals identify direct-adapter source locators. Recorded sequence claims remain in attributes and provenance; the capture digest identifies the exact displayed bytes.

Selecting a Fabric journal also permits read-only access to its referenced companion material at `<journal>.blobs/<digest>` beneath the same retained source directory. Each material name must have the exact digest-name shape; each object is bounded at 32 MiB. Availability records whether this admitted path can be read, without verifying its content digest or authenticity. The application does not search unrelated directories or load project code. Unavailable companion material is shown as missing; absent public trust does not prevent viewing recorded data.

Full source fields are retained as exact tagged semantic values or explicit bounded raw-record pages. Large integers remain exact; Findings floating-point values retain their bit patterns. Findings IDs are ledger-local, version origin scopes remain distinct from use scopes, and parallel relations have separate identities. Missing exact references retain their exact unresolved identity. Textual findings targets and locations become unresolved location associations; matching text never asserts a governed subject relation.

Source-reference edges retain their recorded historical dependency classification. Additional scoped governing relations are display projections from recorded selectors, manifests, dependencies and requirements. These structural relations do not assess whether any prerequisite is valid or currently governing. Namespaced edge metadata preserves the different recorded and projected bases. Material attachment and decision-effect arrows retain their own recorded direction and basis.

## Refresh and retained snapshots

Refresh compares the selected files with the accepted capture. Unchanged file identities and metadata reuse the accepted worker and generation without parsing or rebuilding. Explicit Import deliberately creates a cold candidate even for unchanged inputs. A changed-source candidate streams and projects its selection again; it does not verify canonical history or retain a cross-worker parsed-prefix cache. Malformed or incomplete tails and unknown formats fail the candidate.

The selected file's native identity is pinned. The canonical writer may atomically replace a journal during a valid update; this counts as a replacement of the admitted file. The application retains the previous snapshot and reports: “Selected file was replaced; reopen sources to admit the new file.” Reopen and deliberately reselect the source to admit its new identity. Refresh does not silently widen or renew a read grant.

A candidate is built in a separate worker. Only a complete parsed source set can replace the published worker and metadata in one operation. Unsupported input, changed files, resource limits, worker failure or cancellation retain the previous usable generation with an import-error/stale indication. Late results from a cancelled or closed session cannot publish.

The accepted snapshot retains a private application-owned archive of the exact captured input bytes. Inspector paging uses those bytes and the captured record span, even if the live journal changes or the candidate worker stops. It never substitutes current filesystem bytes for an old revision. Replacing a snapshot or closing the session releases its workers and capture archives. No source file is written by these operations.

## Resource limits

Selected raw inputs are bounded at 1 GiB in aggregate, with at most 128 selected files. A JSONL record body is limited to 100 MiB, excluding its LF or CRLF terminator; physical source spans can therefore include at most two additional bytes. Material objects are limited to 32 MiB, nesting to 64 levels and source pages to 256 KiB. Each logical tagged fact is limited to 1 MiB and cumulative logical fact JSON to 512 MiB across all sources. A complete derived Findings wrapper must fit the same fact limit; a 100 MiB raw-record guard is not an unconditional promise of derived inline capacity. Graph limits remain 100,000 vertices, 500,000 edges and 512 MiB of compact encoding. Limit failures preserve the previous accepted view.

The worker consumes typed facts synchronously without serializing an intermediate wire stream. The application retains at most an accepted and candidate raw archive, each bounded at 1 GiB. Private disk capacity requires filesystem overhead beyond these byte limits. No Python capture lease, fact spool or parsed checkpoint cache is part of the production import path.

A nonempty or in-use temporary capture cache fails closed. Recovery is manual: close all Fabric Explorer instances, clear only the viewer's `JAI Fabric Explorer/temp/captures` directory under the platform application-data directory, then reopen the viewer. Keep original journals, preferences and the namespace registry in place. The viewer does not automatically remove unknown stale files or another instance's cache.

The import report records supported and observed versions, selected/accepted/rejected sources, skipped items, graph counts and unresolved counts. At most 1,000 diagnostics are displayed, with the full diagnostic total retained. Failed sources retain their known selected source ID, record pointer and local sequence separately; an unverified revision is never invented merely to populate a source locator. A failed report can describe individual source outcomes, but it never installs a partial snapshot. Logs and reports use bounded diagnostics rather than native exception paths.

During loading, the status line updates at most once per second with bytes read out of the captured total, physical records read, facts projected and sources processed. Record and fact totals are not known in advance. Building graph indexes is named separately; graph layout/display preparation follows publication. Progress does not reread sources or count them in a preliminary pass. The finite performance observer prints the same loading counts in its terminal.

Manual refresh is the supported update mechanism. No background filesystem watcher is installed.

## Developer boundaries

Application import code lives under `desktop/src/import`, and native source/archive ownership under `desktop/src/broker`. The fixed compiled worker is `dist/import-worker.cjs`. Main receives snapshot descriptors, reports and bounded source pages; the full compact graph remains inside the accepted worker. Development Python fixture writers are separate from the production import path. Recorded JSON is structurally interpreted once; worker-generated graph records use a private typed packing path without repeating public schema validation. Public graph/transport admission retains its full validation. Identity strings retain their Unicode and field bounds when constructed; tagged attributes remain lossless.

Tests exercise actual source handles, stream/archive parity, lossless values, model limits, atomic publication, unchanged refresh, explicit reimport, cancellation and previous-revision paging. Native Windows and macOS qualification remains a separate platform task. Portable Node admission pins the opened file identity but does not claim atomic confinement against hostile parent-directory replacement during initial path acquisition.

## Recorded observation metadata

The viewer displays decoded recorded content. Source observations use `mode: recorded`, `chain: unknown`, `replay: recorded` and `publicTrust: unknown`; chain, signature and lifecycle verification is not performed by the viewer. A captured SHA256 identifies the exact bytes displayed and does not authenticate their origin. Recorded dependency classifications describe the source relationships; they do not grant authority or constitute a fresh assessment.

Direct adapters use version `/2` to distinguish physical-row locator semantics from earlier recorded-claim locators. Immutable version IDs use the published format serializer solely to preserve identity. Recorded use transitions and implicit structural use projections drive the display without checking legal transitions, deadlines or permissions. Missing references remain unresolved. Unsupported or unreadable structures still fail explicitly. Object-valued attributes preserve all members; their serialized member order can differ from the former reconstructed canonical wrapper order. Array order and original captured bytes remain exact.
