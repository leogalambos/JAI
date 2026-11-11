# Read-only exploration

Open the **Sources** tab, choose the source families, and use **Open
sources…** to select a project folder. Direct regular `.jsonl` files in its
`.fabric/` and `.findings/` directories are selected automatically for the chosen
families. Missing or unavailable project sources open a manual file dialog in
the selected project or its conventional family directory. Audit stays manual.
A successful selection immediately loads an observed revision set; no second
import action is needed. Progress and cancellation remain available while
loading. After a failed or cancelled load, **Retry import** is offered for an
admitted selection without a snapshot; **Close sources** lets you choose again.
Use **Refresh snapshot** for later source changes. The source files and
their companion material are read-only. This viewer never runs project code or
turns recorded decisions into current permission.

The overview shows filtered snapshot counts and a small initial neighbourhood,
not the entire imported graph. **Snapshot provenance** exposes each captured
revision, digest/head, observation time, adapter and recorded verification
outcomes. **Source compatibility** identifies supported/unknown versions.
Import diagnostics retain available record pointers and sequences; the display
shows at most the first 20 diagnostics and states the total.

The application menu groups commands under **File**, **View**, **Navigate** and
**Help**. Toolbar icons expose their complete command names in tooltips and have
labeled menu equivalents. **Sources**, **Search**, **Findings** and **Elements**
are separate navigation tabs; switching tabs retains their current content and
query drafts. **Elements** offers the semantic table and derived groups.

Drag either visible separator beside the graph to resize its neighbouring pane.
The graph keeps its selection and query scope. A focused separator also accepts
Left/Right arrows, larger Shift+Arrow steps, Home/End and Enter to reset; a
double-click resets its width too. **View → Reset pane widths** restores both
session defaults. Widths are not persisted across launches. At narrow windows,
the navigation and inspector use individually opened drawers; their toolbar
icons and View commands remain available. Content scrolls inside its active
section rather than hiding whole sections below unrelated controls.

**File → Preferences…** opens a dedicated dialog without scrolling the workspace.
Theme and Reduce motion remain the only stored settings. **Cancel** or Escape
discards an unsubmitted draft; **Save preferences** applies it. A save failure
keeps the dialog and draft open. Dismissal is temporarily disabled while an
already submitted save completes. **Help** opens keyboard and usage guidance.

The graph header distinguishes **Snapshot totals** (all imported records),
**Filter matches** (indexed matches across the snapshot) and **Visible graph**
(the current bounded neighbourhood or path). A snapshot can contain hundreds
of records while its initial neighbourhood shows only two nodes. Select or
search a starting point and choose **Explore selected neighbourhood** to
investigate its links. Open **Traversal and path options** for direction,
hops, causal selection and path actions. **Query details** explains hidden
counts and omissions; query completeness never means the entire snapshot is
visible.

Search literal labels or a complete stable identity. Select the exact result to
inspect its original identity and attributes; labels never replace identity.
**Next search page** advances the displayed query, even if the input contains an
unsubmitted draft. Findings have a separate bounded searchable list. Each page
shows the number remaining; earlier page records are not accumulated indefinitely.

The **Filters** control in Search or Findings exposes project, family, finding state and relation. They affect search,
findings, counts and the current bounded graph using the same indexed worker
rules. Nonapplicable family/state dimensions preserve surrounding context.
**Reset filters** restores the retained neighbourhood without reimporting it.
Overview groups are derived counts; they do not merge canonical identities or
infer ownership.

Select a vertex or relation on the graph, or use **Elements → Table**. The list
has separate vertex/relation modes and 25 records per page. Every parallel
relation remains individually addressable. Its inspector shows both endpoints,
recorded arrow direction, relation type, evidence basis and causal membership.
Full labels remain available there when a canvas label cannot fit.
Canvas, table and inspector share display-only readable names where supported
by the recorded attributes or material association. Exact IDs and original
source labels remain available in identity details; the display name does not
change query meaning or selection identity.

Semantic selection from a result, table row, endpoint or subject moves focus to
the inspector heading after the exact selection loads. The inspector exposes **Overview**, **Relations**, **Evidence** and **Raw** tabs.
Overview shows identifying fields; Relations shows endpoints, direction and
finding subjects; Evidence holds provenance and captured source pages. In Raw,
expand **Exact identity and original fields** for full canonical keys and raw
identity data; tagged attributes remain available in their own details. The
current inspector tab is retained when another applicable record is selected. Captured source and raw-value regions have names
and accept keyboard focus for scrolling. Skip links lead directly to the
workspace and inspector. See [Semantic graph tables](semantic-tables.md) for
the bounded table window and row metadata.

**Explore selected neighbourhood** uses the chosen forward/reverse/both
direction, relation filter, causal selector and finite hop/work/visible budgets.
Reverse exploration retains original arrows. Choose **Use selected as path
start**, select a destination, then **Find path to selected**. A bounded unknown
result is distinct from proved absence. Visible/global-hidden counts and
omissions explain what the current view contains; they do not invent the number
of unexplored reachable records.

A finding's display name starts with its complete ledger-local ID, followed by
its literal title. The inspector exposes **Finding ID** and **Ledger** directly;
the same finding ID in another ledger remains a different record. It also shows
the original state, severity and subject candidates. Follow a
single observed target or choose explicitly among multiple targets. Missing or
textual targets stay unresolved; the viewer does not guess a semantic match.
**Read captured source** displays a bounded byte page from the selected record's
captured revision. Previous/next offsets count bytes; UTF-8 display may show
replacement characters at page boundaries. Tagged attribute integers and
floating-point values remain lossless in the inspector.

**Back** and **Forward** restore up to 50 navigation intents without retaining
worker capabilities or copies of historical graphs. A successful refresh
publishes a new generation and invalidates the prior navigation/source pages.
A failed refresh keeps the accepted graph and captured evidence with an explicit
stale warning. Close/reselect sources if the admitted file identity has been
replaced; native source admission remains separate from refresh.

| Binding | Action |
| --- | --- |
| `Ctrl/Cmd+K` outside editable controls | Focus search |
| `Ctrl/Cmd+Shift+F` outside editable controls | Fit graph |
| `Ctrl/Cmd+,` outside editable controls | Open Preferences |
| `Alt+Left` / `Alt+Right` without extra modifiers, outside editable controls | Back / Forward |
| Unmodified `Escape` | Dismiss an active tooltip, menu or dialog first; otherwise cancel active work outside editable controls |
| Left/Right and Home/End on a tab strip | Select and focus a section |
| Arrows, Home/End and Enter on a separator | Resize or reset the adjacent pane |
| `Tab`, `Shift+Tab`, `Enter`, `Space` | Native controls and semantic selection |
| Pointer wheel / background drag | Zoom / pan |

Shortcuts ignore events already handled elsewhere, composition and key repeats.
They do not intercept Orca's `Alt+Shift+Arrow` table navigation. Theme preferences
offer light, dark and system appearance. System follows live operating-system
changes while retaining the stored system choice; controls and canvas use the
same resolved colors. Selection and partial/error states include text rather
than relying on color. Both shipped themes still require the recorded native
keyboard and 100/150/200% visual qualification; source tests alone do not
establish that conformance.

Zoom, fit and focus also have named buttons. An inspector selection outside the
current projection remains inspectable; focus is available only when that
element is visible. If WebGL is unavailable or its context is lost, search,
findings, source evidence and semantic lists remain usable. Close/reopen the
source view to create a fresh canvas; automatic GPU recovery is not claimed.

Development verification uses the finite Linux runner
`bash apps/fabric-explorer/desktop/tools/run-viewer-check.sh` with the pinned
installed toolchain and official Electron binary. It builds fixed assets, runs
bounded automatic production-DOM and canvas checks, and saves
synthetic screenshots/observations beneath ignored `build/`. Close its window
or press terminal Ctrl+C to stop. Test definitions alone are not evidence of
executed native or platform qualification. Detailed accessibility, performance,
packaging and cross-platform acceptance remain separate qualification stages.
