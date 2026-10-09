# Licensing policy

AI IT House is distributed under the BSD 4-Clause License.

Copyright (c) 2026, Leo Galambos and the Egothor team. Project website:
https://www.egothor.org

The authoritative legal text is `LICENSE` in the package root. The
installed common runtime also carries a copy so the applicable license
remains available after installation.

## Source header policy

Executable and source files use only a compact notice where comments are
normal for that format:

```text
SPDX-License-Identifier: BSD-4-Clause
Copyright (c) 2026 Leo Galambos and the Egothor team
https://www.egothor.org
```

For executable scripts, a shebang stays on the first line. The compact
license notice follows it and must never make the script less directly
executable.

JSON and other machine formats that do not support comments receive no
synthetic header. Their licensing is inherited from the package-level
`LICENSE` file.

## AI context policy

Skills, role references, agent prompts, command material, workflow
knowledge, and similar AI-consumed assets do not repeat the full BSD
license text. Repeating legal boilerplate there would consume context
tokens without adding task-relevant semantic content.

Such assets remain covered by the package license. Where a short header
would reduce semantic signal or prompt efficiency, it may be omitted
entirely.

## Human-facing text

Human-facing prose is kept at a target width of 72 characters per line.
Code blocks, Markdown tables, and indivisible URLs may exceed the target
when wrapping would alter their meaning or usability.


## Explicit copyright/website separation (26.10.4 clarification)

The holder attribution, project web address, and reservation of rights
are distinct statements. Their canonical presentation in both
distributed `LICENSE` copies is:

```text
Copyright (c) 2026, Leo Galambos and the Egothor team
Website of the Egothor team: https://www.egothor.org
All rights reserved.
```

This is a formatting and attribution clarification only; all four BSD
clauses, permission conditions, disclaimers and retained legal
provisions remain unchanged.
