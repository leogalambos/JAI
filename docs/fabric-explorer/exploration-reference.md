# Read-only exploration

## Source status

See [Importing local source journals](importing.md) for source selection, retry
and refresh. The viewer reads captured revisions and companion material.

The overview shows filtered snapshot counts and a small initial neighbourhood,
not the entire imported graph. **Snapshot provenance** exposes each captured
revision, digest/head, observation time, adapter and recorded verification
outcomes. **Source compatibility** identifies supported/unknown versions.
Import diagnostics retain available record pointers and sequences; the display
shows at most the first 20 diagnostics and states the total.

## Menus and panes

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

See [Arrange the workspace](exploring.md#arrange-the-workspace) for the
Preferences procedure.

## Graph scope and traversal

The graph header distinguishes **Snapshot totals** (all imported records),
**Filter matches** (indexed matches across the snapshot) and **Visible graph**
(the current bounded neighbourhood or path). A snapshot can contain hundreds
of records while its initial neighbourhood shows only two nodes. Select or
search a starting point and choose **Explore selected neighbourhood** to
investigate its links. Open **Traversal and path options** for direction,
hops, causal selection and path actions. **Query details** explains hidden
counts and omissions; query completeness never means the entire snapshot is
visible.

**Explore selected neighbourhood** uses the chosen forward/reverse/both
direction, relation filter, causal selector and finite hop/work/visible budgets.
Reverse exploration retains original arrows. Choose **Use selected as path
start**, select a destination, then **Find path to selected**. Query details
report whether the path search completed or stopped at its budget.

## Search and filters

Search matches admitted display labels, stable identities and recorded logical
or version identifiers. Label matching ignores case and can match text with collapsed
whitespace. Paste the complete version identifier to look up an exact recorded
version and its associated uses. Identical labels can match multiple versions.
Select the result to inspect its stable identity, attributes and provenance.
See [Inspect identity and evidence](exploring.md#inspect-identity-and-evidence).
**Next search page** advances the displayed query, even if the input contains an
unsubmitted draft. Findings have a separate bounded searchable list. Each page
shows the number remaining; earlier page records are not accumulated indefinitely.

The **Filters** control in Search or Findings exposes project, family, finding state and relation. They affect search,
findings, counts and the current bounded graph using the same indexed worker
rules. Nonapplicable family/state dimensions preserve surrounding context.
**Reset filters** restores the retained neighbourhood without reimporting it.
Overview groups are derived counts; they do not merge canonical identities or
infer ownership.

## Tables and inspector

Select a vertex or relation on the graph, or use **Elements → Table**. The list
has separate vertex/relation modes and 25 records per page. Every parallel
relation remains individually addressable. Its inspector shows both endpoints,
recorded arrow direction, relation type, evidence basis and causal membership.
Full labels remain available there when a canvas label cannot fit.
Canvas, table and inspector share readable names. See
[Graph canvas](canvas.md) for labels and material associations.

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

## Findings and captured evidence

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

## Keyboard and pointer

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
establish that conformance. See [Qualification envelope](qualification.md).

## Canvas recovery

Zoom, fit and focus also have named buttons. An inspector selection outside the
current projection remains inspectable; focus is available only when that
element is visible. If WebGL is unavailable or its context is lost, search,
findings, source evidence and semantic lists remain usable. Close/reopen the
source view to create a fresh canvas; automatic GPU recovery is not claimed.
