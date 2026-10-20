# Build and reuse your local know-how

Owner: JAI maintainers  
Last reviewed: 2026-10-20

A useful knowledge library preserves what made an approach work, where it
failed and which assumptions must be checked next time. It is not a collection
of universally valid answers. Use experimental assistance to prepare records;
keep responsibility for their scope, confidentiality and continued relevance.

These examples are fictional illustrations, not executed provider transcripts.
Use `/hint` in Claude or `$workflow-hint` in Codex. For capturing a selected
part of the current conversation, start with
[Remember useful knowledge](remembering-knowledge.md).

## Distinguish the sources you are reusing

| Source | What it contributes | What it does not establish |
| --- | --- | --- |
| Personal experience | A reported approach, outcome or lesson in its original context. | Suitability for another project or organisational approval. |
| Custom scenario | A reusable procedure with explicit inputs, steps and limits. | Evidence that every step was executed successfully. |
| Organisational procedure | A maintained procedure with ownership and a declared review state. | Verified human authority merely because it was saved. |
| Expert reference | Guidance selected through JAI's existing reference mechanisms and DCS bindings. | Facts about your current project. |
| Current project evidence | Available observations and artefacts relevant to the present assessment. | An unqualified conclusion beyond what those observations support. |

Keep observations separate from interpretation and recommendations. A saved
record remains AI-assisted material unless its actual provenance establishes
otherwise. Declared reliability is not a calculated confidence score, and
storage does not verify independent human approval.

## Example: turn your approach into a personal scenario

Alice repeatedly prepares architecture assessments for fictional ACME
projects. She has developed a useful evidence-first intake procedure and
wants to reuse the procedure without copying any project's private facts.

**Alice:**

> Save our evidence-first architecture intake as a personal scenario. Keep
> the document checklist, the order of assessment steps and the escalation
> when an architecture claim has no supporting evidence. Exclude ACME's
> actual architecture details. Use the local library I selected. Mark it
> internal, based on this session's observations, and owned by my operator
> role.

JAI should extract the selected procedure, define the inputs it needs and
retain each step's purpose, expected output and limits. It must distinguish
steps actually used from improvements merely proposed during discussion.
If a necessary detail is missing, it asks before saving and continues the
same request after Alice's answer. Alice does not need to write a structured
record herself.

Before reuse, ask JAI to validate the scenario's structure and supported
command references. Separately review whether its inputs and steps make
sense together. Structural validation does not demonstrate that the procedure
produces a sound assessment. A personal scenario does not replace JAI's
maintained workflow or create a new approved domain standard.

## Example: retain a failed approach as a lesson

**Bob:**

> Remember that our initial control inventory treated undocumented controls
> as implemented. That produced unsupported conclusions. We corrected it by
> recording missing evidence separately from confirmed control failures.
> Save the failed approach and correction as an internal lesson, observed in
> this session, in the selected engagement library. I own the record.

The useful knowledge is the failure mode and the correction. JAI must not
invent the number of affected controls, financial consequences, independent
review results or proof that the correction eliminated all errors. If the
conversation shows only a proposed correction, it must preserve that status.

Unavailable evidence must remain unavailable. A reference to a report that
was later removed or revoked does not restore the report or authorise JAI to
reconstruct its contents. Ask for current permitted evidence when a decision
depends on it.

## Example: reuse the lesson when assumptions have changed

In a later project, Alice wants a security assessment and a recurring process
for handling its findings.

**Alice:**

> Recommend a JAI procedure for this architecture assessment. You may read
> the local knowledge library I explicitly selected and use its internal
> records in this active provider session. Compare our earlier evidence-first
> approach with this project's assumptions: the architecture is now operated
> by two suppliers and evidence ownership is split. Explain what needs to
> change before we reuse the procedure.

The recommendation should identify its sources and their record types,
explain why each applies, and expose gaps. Earlier success does not resolve
the new ownership split. The plan may require named evidence owners,
supplier hand-offs and an escalation route before repeating the assessment.
It must not merge conflicting procedures into an apparently agreed standard.

Treat stale or superseded records as context to inspect, not current
instructions. A change to assumptions, scope or confidentiality can make an
otherwise relevant lesson unsuitable. A record's embedded request to ignore
JAI rules is untrusted source content, not an operator instruction.

## Control permission and provider disclosure

Select libraries explicitly for the current task. Permission to save a record
does not automatically authorise a later search of the library. Likewise,
permission to read a local file is not unlimited permission to disclose its
contents to a provider. State the permitted scope and confidentiality; JAI
must ask when the boundary is unclear.

Opt-in hint selection uses explicitly named local libraries, a declared
scope (`personal`, `engagement` or `organisation`), permitted confidentiality
classes and exact applicability context labels. A scope label describes the
declared use of the batch; it is not a record-level access-control rule or
proof of authority. The provider translates your plain-language choices into
the local tool options and must confirm the library and disclosure boundary.
Metadata and lexical filtering return preconditions and exclusions for review;
they do not determine semantic suitability for your project.

The active provider can reason only over content actually delivered into its
context. Distinguish a candidate found in an index, a selected record, a record
actually read and content delivered to the provider. Do not claim that every
linked source has been read or that local searching makes provider disclosure
irrelevant. Never use real private records as distributed examples.

The selector loads complete bounded saved JSON records locally for validation
and lexical scoring. Its candidate response contains filtered metadata and
limits, not the full observations or procedure steps. It does not read linked
evidence contents, pending drafts, deleted records or chat history. An
explicitly permitted description then returns the full selected record before
its steps are explained. Source identifiers, record type, declared reliability,
review state and evidence availability remain visible.
Recommendations must explain excluded and unavailable sources rather than
suggest they reviewed the underlying evidence.

By default, records older than 365 days or past their declared review date
are excluded as stale, and earlier versions are excluded as superseded.
Duplicate IDs in different libraries remain distinct sources and are flagged
as conflicts. Declared conflicts must be explained. These checks do not
detect every semantic disagreement or establish that a newer record is true.

## Maintain the library deliberately

The local knowledge facility requires POSIX descriptor, no-follow and
file-locking support. Delete and restore additionally require Linux
`renameat2` no-replace operations and fail closed without them. Do not assume
Windows support or equivalent delete/restore support on macOS. These
restrictions do not describe the platform scope of every JAI command.

Review useful records when their assumptions change. Keep the original
observation intact when writing a revision; explain what changed and why.
Superseding a procedure must make the replacement relationship visible rather
than silently rewriting history. Review status records what was declared; it
does not manufacture a human approval event.

Ask JAI to prepare and save a revision of the selected record. Revisions use
the existing capture process with a new immutable version and a link to the
superseded version; there is no separate automatic review or approval act.
State the actual review outcome and its evidence when reporting one. A
declared review date or status cannot replace the review itself.

Before exporting, check the destination and allowed sharing scope. Before
deleting, identify the exact record ID and understand that all its versions
will move to trash. Export and deletion require their own explicit requests; asking for
advice or a recommendation does not authorise them.

Deletion moves the **whole record ID and all its versions** into protected
local trash. It is not permanent erasure and does not remove exported copies
or information already disclosed to a provider. The reported recovery
location supports an explicitly requested restore; restore does not overwrite
an existing active record. Confirm the whole-record scope before deleting.

Export copies the selected version to an explicitly selected destination and
refuses to overwrite an existing file. It does not anonymise, sanitise or
approve the record: inspect its contents and sharing permission before
requesting export.

`/guide` can explain validated custom steps after explicit record access.
Saved scenarios do not automatically become executable `/demo` projects;
`/demo` continues to prepare the maintained fictional practice packs.

## Implementation and verification boundaries

The local `demo/hint.py` selector performs deterministic candidate selection.
`tools/knowledge.py` handles record validation, explicitly permitted
description, capture, export and recoverable deletion or restoration. Use
each tool's `--help` when maintaining the local installation; the active
provider handles these interfaces for ordinary conversational use. Revisions
use immutable capture versions rather than an independent approval command.
See the [command reference](../reference/commands.md) and
[installed guide](../reference/installed-cli-guide.md) for the provider
command contract.

Offline fixtures can verify selection, exclusions and storage behavior.
They do not establish the quality of a live model's interpretation, a novice
operator's experience or actual independent human approval. The illustrative
conversations above must not be reported as executed tests.

Experimental capture and reuse do not replace L0 authority, independent
review, segregation of duties, evidence requirements or release gates.
