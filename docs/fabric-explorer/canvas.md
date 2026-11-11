# Graph canvas behavior

The canvas displays a bounded projection of the accepted snapshot. It uses the
selected Sigma renderer and one directed Graphology multigraph for the lifetime
of the view. Replacing visible contents preserves that graph instance. Source
attributes, verification evidence and complete records remain in the inspector
and query model; the rendering graph stores compact labels, positions and style
values only.

Every vertex and relation keeps its exact identity. Parallel and opposing
relations follow independently selectable curved paths. Self-relations use loop
paths. Arrowheads follow the stored source-to-target direction. Findings use a
diamond and unresolved vertices a triangle, supplementing color. The canvas
never changes source relationships or treats position as a semantic fact.

Drag the background to pan and use zoom, fit and focus controls to navigate.
Node dragging and camera rotation are disabled. Fit resets the current bounded
view; focusing an element retains its exact identity. Selecting the background
clears the canvas highlight; the inspector selection remains available.
Semantic lists and the inspector provide the keyboard route
to the same elements without precise canvas picking.

Labels share one collision-placement policy across vertices and relations.
The selected element receives first priority, followed by a hovered relation,
then vertices in deterministic identity order. Placement avoids node bodies and
already placed label boxes. A selected relation therefore reserves its label
space before competing endpoint labels. Camera overview shows the selected and
hovered labels; intermediate zoom admits at most 24 ordinary vertex labels and
detail zoom at most 80. Crowded labels can be suppressed and long canvas text
abbreviated with an ellipsis. The inspector always provides the complete label.
Label text is drawn as inert text, never interpreted as HTML.

Container resizing and camera movement update label positions in CSS pixels.
The canvas enforces the existing 5,000-vertex and 20,000-edge view ceilings and
rejects mismatched generations or invalid layouts before replacing the current
view. If graphics initialization or the active WebGL context fails, the viewer
reports the canvas as unavailable; semantic controls and evidence remain the
alternative. Reopening the view creates a fresh graphics lifetime. Recovery is
not silently reported as successful.

Full high-DPI visual/accessibility and packaged performance qualification are
separate from these maintained interaction rules. The development canvas checks
exercise the actual adapter and SDK without adding a production test interface.

Canvas colors follow the resolved application theme. Changing between light and
dark appearance updates only presentation colors and label backgrounds; it
preserves the graph instance, selection, layout and camera. Label text/background
contrast and node/relation contrast are checked using the actual configured
renderer colors. Shapes and arrowheads remain unchanged, so color is not the
only way to distinguish findings, unresolved vertices or relation direction.

Both vertex and relation hover receive label priority after the selected
element. Loop label anchors and reserved node bounds read the SDK's active node
size, including selection enlargement, instead of guessing from the compact
base size. Labels are positioned in CSS pixels while the backing canvas follows
the display pixel ratio. Actual theme and scale qualification is recorded
separately from these implementation rules.

Wide layered ranks pack complete cycle-group footprints into compact shelves.
Rank bands stay ordered from source to target, while members of a cycle keep
circular placement. Layout coordinates remain derived view state. Node and
relation glyphs use CSS screen sizes as magnification increases, so zoom can
separate nearby centres without enlarging the glyphs at the same rate. Focus
chooses a local scale from nearby visible vertices; fit returns to the overview.

Primary display names can differ from stored source labels. A present authored
title or name takes precedence; otherwise a meaningful source label is retained.
A material can display its recorded neighbour and attachment field, explicitly
as an association, with a short digest. Without such context it displays a type
and short digest. These aliases are shared by the canvas and semantic view;
search still uses the existing source query rules. Exact identities and original
source labels remain available in the inspector. Aliases do not identify a new
record, rename source data or establish a causal relationship.
Loop label anchors also follow the renderer's minimum loop radius, so their
positions continue to match the configured curve geometry at deep magnification.
Actual high-magnification appearance remains part of native visual qualification.

While a replacement layout is pending, previous graphics are invisible and
noninteractive. The canvas retains its layout area so renderer resize work does
not encounter a collapsed host. A temporary zero-size observation defers owned
resize work until the real presentation area returns; a genuine renderer failure
uses the existing unavailable message and semantic alternative. Resizing does
not fit the graph or change the current camera.
