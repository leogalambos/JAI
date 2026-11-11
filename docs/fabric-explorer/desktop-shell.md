# Desktop shell

The desktop shell runs locally on Electron with a sandboxed, context-isolated document. It supports native source selection, read-only direct TypeScript import, graph exploration, closing sources and presentation preferences.

Choose a project folder to associate sources with one stable logical project. For selected Fabric and Findings families, the main process looks for immediate regular `.jsonl` files in that project’s `.fabric/` and `.findings/` directories. A complete matching list is selected in filename order; no content is read by this lookup. It does not recurse, follow candidate links, inspect environment-selected homes or execute project configuration. Audit remains an explicit file selection. A missing, unreadable or over-limit lookup opens a native file dialog for that family. The dialog starts in the conventional directory when available, otherwise in the selected project folder. Manual files can be outside the project folder, including a separately managed Fabric home. Successful source selection immediately starts read-only loading, with progress and cancellation available throughout; there is no separate normal Import step. A failed or cancelled load may expose **Retry import** for an admitted selection without a usable snapshot. **Refresh snapshot** remains explicit for later source changes. Cancellation does not admit a partial selection. The narrow application-only selection cancellation remains separate from consumer-protocol work cancellation, which requires an admitted capability. An open native dialog must still be closed by the operator; its slot stays occupied until the native dialog promise settles, and late selections are discarded. Closing sources releases their handles; closing the window revokes its session.

Lookup examines at most 4,096 directory entries and respects the existing remaining capacity within 128 selected sources. It never silently uses a truncated list. The broker still performs final read-only file admission.

The selected source families are Fabric, Findings and Audit. Stable application-assigned project, root and source identifiers persist separately from ephemeral session and read capabilities. Application state stores physical identity digests and opaque identifiers, never raw source paths. Source names are displayed only in the local catalog.

## Isolation and storage

Before a browser session or window is created, the main process fixes private application locations for preferences, namespace identifiers, browser session data, cache, logs, crash dumps and temporary files under the operating system's application-data directory. Preferences accept only a schema version, theme and reduced-motion setting. Fixed state files use bounded reads and atomic replacement. Unsafe linked state paths are rejected. These destinations are excluded from admitted source roots by the broker.

The renderer has no Node.js, filesystem, process-spawning or generic IPC interface. Its context bridge contains only named state, native selection, close, cancellation and preference methods. Main authenticates the exact current window, main frame, document URL and browser session before decoding any request. Source requests use the maintained read-only consumer contract.

The document loads three packaged local assets. Its content security policy forbids inline scripts, evaluation, network connections and embedded documents. Session interception rejects other resource URLs. Navigation, redirects, new windows, downloads, browser permissions and webviews are denied. Unsupported launch switches that weaken these boundaries are rejected.

The session clears its dictionary-language list synchronously at creation and
the session and window explicitly disable spellchecking. Clearing the list
cancels queued Hunspell loads; the enable flag alone only updates renderer
behavior. Chromium's dictionary downloader operates outside page resource
interception, so page CSP alone does not establish process-wide offline operation. Linux native qualification uses
the pre-runtime environment described in [security qualification](security-qualification.md).

These controls are application boundaries. They do not constitute an operating-system sandbox for every main-process dependency. Native process-tree network and filesystem qualification remains part of platform release validation.

## Development and validation

The desktop package resides at `apps/fabric-explorer/desktop`. Use the repository's pinned local toolchain. `npm run build` builds the consumer contracts, checks TypeScript and produces the fixed compiled main, preload and renderer assets. `npm test` runs controller, state-storage and boundary tests. Run the compiled application using the pinned Electron executable with the desktop directory as its application argument.

The main and preload are separate CommonJS bundles. The renderer contains no main-only implementation. Native smoke verification runs from a separate test entry; production exposes no test API or debugging port. A finite operator check verifies the actual sandbox, context bridge, content policy, denied network/window behavior and lifecycle. Linux is the current native validation target; Windows and macOS execution must be recorded separately before those platforms are described as verified.

For a checkout-based native shell check, run `npm run build:native-smoke` from
the desktop package and ensure the pinned Electron binary is installed using
its checksum-verifying installer. Run `node node_modules/electron/cli.js
dist/native-shell.cjs`. The nine automatic steps use synthetic input and isolated
application state, print progress and have a 60-second total watchdog. The shell
and importer do not require a Python executable or reader configuration. Some
other development journey helpers use Python only to prepare synthetic fixtures
before opening the application. A successful build alone does not establish
native qualification; keep Electron sandboxing enabled.

Only compiled runnable application artifacts belong in an installed package. Source files, development tests, private evidence and planning documents are not installation payloads. Packaging and platform-signing qualification are completed by the release stages.

## Workspace commands and settings

The renderer exposes a keyboard-operable application menu and named icon
commands. The window removes Electron’s default menu so it cannot reveal a
second, unrelated command set. This adds no privileged IPC operation. Navigation
and inspector tabs present existing data and read-only actions. Pane separators
change session-local layout widths only; they do not change graph selection or
store new preference fields. The dedicated Preferences dialog uses the existing
theme/reduced-motion API and preserves its app-only persistence boundary.
