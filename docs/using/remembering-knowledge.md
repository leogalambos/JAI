# Remember useful knowledge from your current task

Owner: JAI maintainers  
Last reviewed: 2026-10-20

Use experimental knowledge capture when something in your current conversation
is worth reusing: a successful approach, a failed attempt and its lesson, or a
procedure you have refined. Tell JAI what to remember in ordinary language.
You do not need to reconstruct the individual steps or prepare a technical
record yourself.

```text
/hint Remember the assessment approach we developed here, including how we
handled missing architecture evidence and verified the remediation findings.
```

In Codex, use `$workflow-hint` with the same request. In an active JAI
conversation you can also ask directly: “Remember this approach in our
knowledge library.” Identify the useful part if the conversation covers several
unrelated tasks. These are instructions to the active provider; capture does
not start a second model or read a hidden conversation archive.

**Experimental support:** the active provider interprets your selection and
prepares the record. Local validation and storage checks do not demonstrate
that a model always extracts an accurate or complete lesson.

Local knowledge capture requires POSIX descriptor, no-follow and file-locking
support. Recoverable deletion and restoration additionally require Linux
`renameat2` no-replace operations and fail closed without them. Do not assume
Windows support for this facility or equivalent delete/restore support on
macOS. These restrictions do not mean that every JAI feature has the same
platform requirements.

## What happens after you ask

JAI uses only the selected material available in its current conversation
context and any sources you explicitly permit. It prepares the English
knowledge record itself, separating observed actions and results from
interpretations, recommendations and untested proposals.

If essential information is missing, JAI asks a short, ordinary-language
question before saving. This can include the destination library,
confidentiality, reliability, or responsible role. Your operator role can be
used when it is already clear; JAI must not invent a person's identity or
assign responsibility to an unnamed stakeholder. Unknown reliability and
confidentiality must be clarified, not silently guessed.

Once you answer, JAI continues the original request to save. You do not need
to edit JSON, copy an internal identifier or issue a second save command.
It reports what it actually saved and where. A request only to **prepare or
show a draft** does not authorise saving it. If the selected knowledge or
destination changes materially or remains ambiguous, JAI clarifies that
change before proceeding.

## Example: remember an assessment lesson

The following conversations illustrate the intended interaction. They are
not transcripts of executed provider sessions.

**Operator:**

> Remember how we assessed ACME's monitoring architecture and separated
> missing evidence from confirmed control failures. Save it for our next
> assessment.

**JAI, when the destination and classifications are unknown:**

> Which local knowledge library should I use? What confidentiality and
> reliability should this lesson carry? I can record you as the responsible
> operator role unless another role owns it.

**Operator:**

> Use the engagement library we selected earlier. Mark it confidential and
> based on this engagement's observed results. I am the responsible operator.

JAI continues capture using that answer. Its completion message should name
the saved lesson and destination, explain that observed results apply to this
engagement, and identify any unresolved limitation. It must report a storage
failure rather than claim success when saving has not completed.

## Example: keep a proposal without turning it into evidence

**Operator:**

> Remember Alice's proposed monthly review cycle and Bob's escalation route.
> We have not tried them yet. Save them in the selected team library as an
> internal proposal; I own the record as the operator.

JAI should preserve the proposed status and lack of execution evidence. It
must not describe the monthly cycle as effective, independently reviewed or
human approved. If that request supplies all necessary information and the
library is already authorised, it can continue without asking you to restate
the steps or confirm a new technical save operation.

## Example: the earlier conversation is unavailable

**Operator:**

> Remember the successful migration procedure from the start of this chat.

**JAI, if that material is no longer available:**

> I cannot establish that earlier procedure from the context available now.
> Please provide the relevant excerpt or explicitly select a source containing
> it. I can then extract the procedure without asking you to rewrite it.

Long conversations can be shortened before they reach the model. JAI cannot
promise access to every earlier prompt, tool result or attachment. A summary
is not proof that every underlying step was executed. Missing details remain
unknown until an available source establishes them.

## Keep the library trustworthy

Capture is explicit, not automatic learning. A library chosen for one request
does not grant permission to inspect unrelated files or projects. Keep private
libraries outside the distributed JAI tree and installed runtime, and select
only sources you are entitled to use. Review sensitive material before asking
for it to be retained; confidentiality labels do not remove secrets from text.

A saved lesson does not replace project evidence, DCS obligations, expert
references, independent review or L0 authority. Storage does not establish
human approval; authority verification remains `NOT_VERIFIED`. Earlier
success also does not establish that the same procedure is suitable for a new
engagement.

Saved records can inform `/hint` only after explicit library selection and
permission to read and disclose the permitted content to the active provider.
They do not become runnable `/demo` scenarios automatically. Follow
[Build and reuse local know-how](reusing-knowledge.md) for selection,
maintenance and confidentiality boundaries. See
[experimental hint guidance](experimental-hint.md) for recommendation limits
and the [installed command guide](../reference/installed-cli-guide.md) for
the command overview.
