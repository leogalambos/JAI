/** Main-process broker ports; native picker paths are never renderer capabilities. */
import type { AdmittedSource, BytePage, SourceFamily } from '@jai/fabric-explorer-contracts';

/** Explicit main-process selection; projectPath is an association anchor, not a source read grant. */
export interface SourceSelection {
  readonly projectPath: string;
  readonly path: string;
  readonly family: SourceFamily;
}

/** Successful raw-source admission; canonical semantic import has not occurred. */
export interface OpenedSources {
  readonly capability: string;
  readonly sources: readonly AdmittedSource[];
}

/** Stable app-owned opaque namespace registry, persisted separately from ephemeral capabilities. */
export interface NamespaceRegistry {
  /**
   * Obtain an existing namespace or persist a new opaque one.
   * @param kind Namespace category; none is an authentication credential.
   * @param identityKey App-computed digest of filesystem identity and source addressing, never a raw path.
   * @returns A stable nonempty opaque identifier unique within this registry.
   * @throws {Error} If app-owned persistence is unavailable or inconsistent.
   */
  getOrCreate(kind: 'project' | 'root' | 'source', identityKey: string): Promise<string>;
}

/** Main-only read interface; no arbitrary pathname operation crosses the preload boundary. */
export interface BrokerPort {
  /**
   * Admit deliberately selected files without opening a writer or creating an input.
   * @param sessionId Trusted owning renderer session.
   * @param selections Paths returned by native main-process pickers.
   * @param signal Optional cancellation of this admission attempt.
   * @returns Opaque capability and public source descriptors, with no semantic snapshot claim.
   * @throws {Error} For denied paths, resource limits, overlap, cancellation or failed secure acquisition.
   */
  open(sessionId: string, selections: readonly SourceSelection[], signal?: AbortSignal): Promise<OpenedSources>;
  /**
   * Release an owned capability and its native handles.
   * @param sessionId Trusted owning session.
   * @param capability Broker-issued capability; already-closed owned handles are idempotent.
   * @returns Completion after the handle is unusable.
   * @throws {Error} For a capability belonging to another session or failed cleanup.
   */
  close(sessionId: string, capability: string): Promise<void>;
  /**
   * Revoke all source access belonging to a closing renderer session.
   * @param sessionId Trusted owning session.
   * @returns Completion after its capabilities and work are revoked.
   * @throws {Error} If native cleanup fails.
   */
  disposeSession(sessionId: string): Promise<void>;
}

/** Internal raw page port for trusted import/source-page consumers, not a pre-import public snapshot API. */
export interface PageBrokerPort extends BrokerPort {
  /**
   * Read a bounded exact byte page from one previously admitted source.
   * @param sessionId Owning session.
   * @param capability Active opaque root selection capability.
   * @param sourceId Admitted opaque source ID, never a relative pathname.
   * @param page Unsigned decimal offset and 1..256 KiB byte length.
   * @param signal Optional cancellation signal.
   * @returns Exact raw bytes with EOF; pointer/sequence are empty/null until a semantic source mapper supplies them.
   * @throws {Error} For stale/foreign handles, changed/unsafe files, bounds, cancellation or failed reads.
   */
  readPage(sessionId: string, capability: string, sourceId: string, page: { readonly offset: string; readonly length: number }, signal?: AbortSignal): Promise<BytePage>;
}
