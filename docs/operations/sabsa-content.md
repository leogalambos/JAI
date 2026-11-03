# Governed SABSA content and views


## Select a bounded content profile

The [delivery profile](../reference/sabsa-delivery-profile.md) identifies the
adopted public sources and their limitations. The
[content architecture](../architecture/governed-sabsa-content.md) defines JAI's
original minimum catalogue. It supports a bounded SABSA-related deliverable;
neither a populated matrix nor a successful structural check establishes formal
SABSA conformity or certification.

An engagement selects an exact, immutable content-policy source through its
governing profile. That policy declares the intended claim, editions, scope,
audiences, required information units, relationships and publication views.
General processing without a content profile makes no SABSA-content claim. A
request for SABSA deliverables cannot be satisfied by silently selecting that
lighter mode.

Every included layer addresses What, Why, How, Who, Where and When at its own
abstraction level. The conceptual scope includes a tailored Business Attributes
Profile: business justification, target and unit, measurement method, accountable
owner and evaluation horizon. Missing client targets remain gaps. JAI must not
invent an appetite or assert that a proposed target has been achieved.

## Author, review and change content

Authors submit canonical structured content as immutable product material through
the [normal layer-local workflow](normal-layered-workflow.md). A unit has a stable
local key; its exact containing product identifies its version. References to
other units name the exact product and local key. A filesystem location or a
human-readable title cannot select a current version.

The containing product supplies ownership, inputs, evidence and provenance.
Relationships relied upon as justification also require the existing declared
causal bindings. A semantic link cannot make private material available, grant
authority or substitute for evidence. Each layer owns its own content; corrections
to another layer travel through the adjacent interface to that owner.

Independent professional review judges the substance against the exact assignment
and content obligations. Integration review assesses the combined answers and
their relationships. Receiving acceptance, human result acceptance and permission
to release remain separate acts. Structural completeness does not perform any of
these acts.

Changing an input or unit produces a new immutable version. Existing owner-led
selection and cancellation determine what applies. Historical reviews remain
truthful records of their original subjects; PASS does not transfer to a changed
product. A missing current basis remains a gap, with no fallback to an obsolete
predecessor.

Local work does not wait for future layers to finish. Registration validates the
owned payload and declared dependencies; local answer qualification checks its
owned requirements. A local bundle or handoff retains its stage-specific meaning.
The full-profile content gate applies to a verified final result and publication
of the whole declared claim. An incomplete whole-profile report on an intermediate
answer therefore does not prohibit authorized construction or its local review.

## Operational feedback

Management concerns span all five other perspectives. An activity definition
states its objective, actor, inputs, outputs, scope, trigger, timing, controls and
required evidence. A measure defines its target, method, source, frequency,
thresholds, action and owner. An actual observation identifies the measured
subject, measure, period, method, result and supporting evidence.

Defining an activity or measure does not prove execution or effectiveness.
Observations can support a new adjacent owner-change request. The owner then
creates a new architecture revision; the old architecture never acquires a
dependency on a future observation. This preserves an acyclic causal history.

## Assess and publish exact versions

Save the exact output UsePoint returned by the workflow in an operator-owned
file, for example `output-use.json`. It contains `ref` (the exact VersionRef) and
`use_scope`; it is not a name to resolve to the latest result. With the same
Store and host configuration used for ordinary work:

```sh
python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  content-status /operator/output-use.json --audience private

python3 .ai/runtime/tools/governed_workflow.py \
  --store /operator/engagement.jsonl --engagement engagement-id \
  --config /operator/host-config.json \
  content-views /operator/output-use.json --audience private
```

The first command reports current content status; the second returns the report
and deterministic JSON/Markdown views selected by the content profile. Use
`--audience public` for the constrained public projection. It does not switch
off confidentiality or grant release. Keep private results in operator-controlled
storage; they are not public build inputs.

Assess a specific output version in its use scope. Completeness concerns that
output's governing dependency closure, required content, business traces, current
reviews and evidence. Unrelated obsolete history does not block it. A required
missing, stale, conflicting or unreviewed item does block the relevant claim.
Exclusions need an explicit entitled decision, scope, rationale, consequences and
validity conditions; an empty cell is not an exclusion.

To exclude a requirement, first obtain an actual signed L0 `exclude_content`
decision naming the current `content_policy` VersionRef and exact obligation
keys. Then register a successor policy containing that decision reference and
select it through the existing owner-led transition. This order avoids future
references. The successor must retain the same obligation meanings; a reused key
with a different owner, group or relationship does not inherit the approval.
Expiry or revocation ends reliance on the exclusion. The ordinary external
signing and submission boundary applies; an agent cannot manufacture the act.

Documents are deterministic views of selected semantic versions. They do not
become a second editable architecture or an independent source of approval.
Correct the governed source and render again when a change affects meaning.
Current, target and transition views describe architectural horizons, separately
from lifecycle qualification, acceptance and release.

Public rendering must not disclose private content, paths, filenames, identifying
hashes or provenance through text, references, diagnostics or gap reports. An
omission for confidentiality does not satisfy a required obligation. If the public
claim needs information that cannot be disclosed, publication must remain blocked
or its claim must be changed by an entitled decision. A reproducible preview is
not permission to release it.
