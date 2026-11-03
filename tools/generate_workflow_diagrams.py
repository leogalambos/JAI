#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate complete workflow figures and maintained Gen2 explanatory diagrams.

Usage: python3 tools/generate_workflow_diagrams.py [--root CHECKOUT] [--check].
Canonical workflow JSON supplies every role and activity; wrapping never truncates
words. Marker-owned Markdown figures and SVG assets are refreshed together.
Check mode reports drift without writes. Exit zero means current/successful;
nonzero means stale output or invalid source. No workflow or approval is executed.
"""
from __future__ import annotations

import argparse
from html import escape
import json
import re
from pathlib import Path
import textwrap

START = '<!-- JAI:WORKFLOW-DIAGRAM:START -->'
END = '<!-- JAI:WORKFLOW-DIAGRAM:END -->'
FONT = 'Arial,Helvetica,sans-serif'
INK = '#102d43'
BLUE = '#145776'
ACCENT = '#147eaa'
WIDTH = 996


def _wrap(text, width):
    # Slashes separate professional domains but must remain visible when wrapped.
    spaced = re.sub(r'/(?=\S)', '/ ', text)
    return textwrap.wrap(spaced, width=width, break_long_words=False,
                         break_on_hyphens=False)


def _text(x, y, label, size=17, fill=INK, bold=False, anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(label)}</text>'


def _lines(x, y, text, width=38, fill=INK, size=17, bold=False):
    lines = _wrap(text, width)
    return [_text(x, y + index * 24, line, size, fill, bold) for index, line in enumerate(lines)]


def _start(title, description, height, ident):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" class="ai-inline-diagram-svg" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="{ident}-title {ident}-description">',
            '<!-- SPDX-License-Identifier: BSD-4-Clause; Copyright (c) 2026 Leo Galambos and the Egothor team; https://www.egothor.org -->',
            f'<title id="{ident}-title">{escape(title)}</title>',
            f'<desc id="{ident}-description">{escape(description)}</desc>',
            f'<defs><marker id="{ident}-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="{ACCENT}"/></marker></defs>',
            '<rect width="100%" height="100%" rx="16" fill="#f6fafc" stroke="#cbdde8"/>',
            *_lines(30, 38, title, 67, size=23, bold=True)]


def _arrow(ident, points):
    return f'<path d="{points}" fill="none" stroke="{ACCENT}" stroke-width="3" marker-end="url(#{ident}-arrow)"/>'


def _box(x, y, width, height, heading, body, chars=35, tint='#e8f2f8'):
    result = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{tint}" stroke="#a9c6d8"/>']
    title = _wrap(heading, chars)
    result += [_text(x + 16, y + 29 + i * 24, line, bold=True) for i, line in enumerate(title)]
    result += _lines(x + 16, y + 38 + len(title) * 24, body, chars)
    return result


def render_workflow(workflow):
    """Render a serpentine workflow with complete canonical role/activity text.

    Args:
        workflow: Canonical workflow dictionary with key, title, outcome and steps.
    Returns:
        Deterministic SVG text with adaptive node/row heights and a text description.
    Raises:
        ValueError: No steps are supplied or canonical numbering is not consecutive.
        KeyError: A required canonical field is absent.
    """
    steps = workflow['steps']
    if not steps or [step['step'] for step in steps] != list(range(1, len(steps) + 1)):
        raise ValueError('Workflow steps must be nonempty and consecutively numbered')
    ident = 'workflow-' + workflow['key']
    nodes = []
    y = 100
    for row_start in range(0, len(steps), 3):
        batch = steps[row_start:row_start + 3]
        height = max((len(_wrap(f"{step['step']}. {step['role']}", 28))
                      + len(_wrap(step['does'], 30))) * 24 + 44 for step in batch)
        for col, step in enumerate(batch):
            position = col if (row_start // 3) % 2 == 0 else 2 - col
            nodes.append((step, 30 + position * 324, y, height))
        y += height + 58
    result = _start(workflow['title'], workflow['outcome'] + ' Arrows follow the numbered stages. The table below supplies handoffs and acceptance gates.', y + 10, ident)
    for previous, current in zip(nodes, nodes[1:]):
        _, px, py, ph = previous
        _, cx, cy, ch = current
        if py == cy:
            if cx > px:
                points = f'M{px + 288},{py + ph // 2} L{cx - 8},{cy + ch // 2}'
            else:
                points = f'M{px},{py + ph // 2} L{cx + 296},{cy + ch // 2}'
        else:
            points = f'M{px + 144},{py + ph} L{cx + 144},{cy - 10}'
        result.append(_arrow(ident, points))
    for step, x, y, height in nodes:
        result.append(f'<g data-step="{step["step"]}"><rect x="{x}" y="{y}" width="288" height="{height}" rx="12" fill="{BLUE}"/>')
        role_lines = _wrap(f"{step['step']}. {step['role']}", 28)
        for index, line in enumerate(role_lines):
            result.append(_text(x + 16, y + 29 + index * 24, line, 16, '#ffffff', True))
        result += _lines(x + 16, y + 42 + len(role_lines) * 24, step['does'], 30, '#ffffff', 16)
        result.append('</g>')
    return '\n'.join([*result, '</svg>']) + '\n'


def concept_diagrams():
    """Return four authored SVG explanations of the implemented Gen2 model.

    Returns:
        Mapping of maintained SVG asset filenames to complete accessible SVG text.
        Management is shown as a content perspective with crosscutting concerns;
        ordinary local review is distinguished from reserved human decisions.
    """
    result = {}
    ident = 'gen2-layers'
    svg = _start('Gen2 layers, local work and neighbouring handoffs', 'L0 is external human authority. Work descends through six SABSA content perspectives. Findings and handoffs return through adjacent ownership. Management is crosscutting across the lifecycle.', 940, ident)
    svg += _box(260, 90, 476, 100, 'L0: external human authority', 'Reserved decisions and changes to human requirements.', 48)
    svg.append(_arrow(ident, 'M498,190 L498,215'))
    labels = [('L1 Contextual', 'Business purpose, scope and required qualities'), ('L2 Conceptual', 'Principles, domains and control objectives'), ('L3 Logical', 'Services, information and control behaviour'), ('L4 Physical', 'Concrete technical and organisational mechanisms'), ('L5 Component', 'Components, configuration and implementation'), ('L6 Management', 'Operation, assurance and lifecycle improvement')]
    for index, (heading, body) in enumerate(labels):
        y = 225 + index * 98
        svg += _box(260, y, 476, 82, heading, body, 49)
        if index < 5:
            svg.append(_arrow(ident, f'M498,{y + 82} L498,{y + 96}'))
    svg.append(_arrow(ident, 'M160,230 L160,810'))
    svg += _lines(30, 345, 'Requirements and agreed inputs descend', 14)
    svg.append(_arrow(ident, 'M840,810 L840,230'))
    svg += _lines(855, 345, 'Findings and reviewed handoffs return', 13)
    svg += [_text(32, 872, 'Each layer addresses What, Why, How, Who, Where and When.', bold=True), _text(32, 900, 'Management concerns inform every perspective; no lower layer rewrites its neighbour’s inputs.')]
    result['layered-runtime-cycle.svg'] = '\n'.join([*svg, '</svg>']) + '\n'
    ident = 'gen2-triad'
    svg = _start('One local triad within the six-perspective matrix', 'Each SABSA content perspective addresses six questions. Local setter, author and independent reviewer choose suitable professional roles. Cross-question integration and the neighbouring receiver are separate acceptance boundaries.', 700, ident)
    svg += _box(30, 90, 936, 110, 'Six perspectives × six questions', 'Contextual · Conceptual · Logical · Physical · Component · Management; What · Why · How · Who · Where · When.', 98)
    svg += _box(30, 270, 280, 150, 'Setter', 'Frames the local question, criteria and required inputs.', 26)
    svg += _box(358, 270, 280, 150, 'Author', 'Supplies a candidate, evidence and explicit uncertainty.', 26)
    svg += _box(686, 270, 280, 150, 'Independent reviewer', 'Assesses this candidate; reports findings without repairing it.', 26)
    svg += [_arrow(ident, 'M310,345 L348,345'), _arrow(ident, 'M638,345 L676,345'), _arrow(ident, 'M826,425 L826,470 L498,470 L498,425'), _text(510, 462, 'Findings → local rework')]
    svg += _box(30, 520, 936, 140, 'Integration and neighbouring handoff', 'Integrate the layer’s questions before the receiving neighbour assesses the exact handoff. Aggregate unresolved conflicts and escalate through ownership. Each local entity selects its own professions from the complete catalogue.', 98)
    result['gen2-local-triad.svg'] = '\n'.join([*svg, '</svg>']) + '\n'
    ident = 'gen2-applicability'
    svg = _start('Changed inputs preserve history and change current applicability', 'Evidence for input version A remains truthful history. An explicit scoped transition to B cancels affected reliance and permissions atomically. New verification and output-specific acceptance are required; permission to continue is separate from release.', 800, ident)
    svg += _box(30, 100, 280, 210, 'Version A: historical basis', 'Evidence records what ran against A. Preserve the exact input identity, result and historical decision.', 27)
    svg += _box(358, 100, 280, 210, 'Explicit scoped transition', 'Select B. Cancel affected uses and dependent permissions together. Unrelated scopes retain their own valid basis.', 27)
    svg += _box(686, 100, 280, 210, 'Version B: new basis', 'New records coexist with A. Missing evidence remains pending; no inherited PASS or silent fallback.', 27)
    svg += [_arrow(ident, 'M310,205 L348,205'), _arrow(ident, 'M638,205 L676,205')]
    svg += _box(30, 400, 280, 190, 'Continue work', 'Applicable authority permits revised inputs and verification. This does not accept the result.', 27)
    svg += _box(358, 400, 280, 190, 'Accept this output', 'Assess its exact version, governing inputs, applicable decisions and required evidence.', 27)
    svg += _box(686, 400, 280, 190, 'Permit release', 'Apply the separate release requirements and reserved human decision where required.', 27)
    svg += [_arrow(ident, 'M310,495 L348,495'), _arrow(ident, 'M638,495 L676,495'), _text(32, 665, 'A valid historical record is not automatically applicable to the current output.', bold=True)]
    svg += _lines(32, 710, 'Changed dependencies cancel only the affected justification closure. Reinstatement requires an explicit traceable decision and the applicable verification.', 102)
    result['gen2-input-applicability.svg'] = '\n'.join([*svg, '</svg>']) + '\n'
    ident = 'gen2-contract'
    svg = _start('The effective output contract comes from explicit composition', 'The selected role output and its shared foundations and overlays define the effective contract. A true condition requires content, a false condition permits justified non-applicability, and an unknown condition stays unresolved. Review and receiving acceptance remain separate.', 840, ident)
    svg += _box(30, 95, 280, 170, 'Exact role output', 'Purpose, required inputs and specialist obligations; select by registered contract identity.', 27)
    svg += _box(358, 95, 280, 170, 'Shared foundations', 'Common required information, evidence duties and prohibited content.', 27)
    svg += _box(686, 95, 280, 170, 'Bound overlays and context', 'Applicable specialisations and explicit conditional requirements.', 27)
    svg += [_arrow(ident, 'M170,265 L170,315 L498,315 L498,350'), _arrow(ident, 'M498,265 L498,350'), _arrow(ident, 'M826,265 L826,315 L498,315')]
    svg += _box(260, 360, 476, 120, 'Effective contract for this output', 'Read all linked obligations together. Optional content does not replace required content.', 48)
    svg += _box(30, 550, 280, 160, 'Condition = true', 'The conditional information is required and needs supporting evidence.', 27)
    svg += _box(358, 550, 280, 160, 'Condition = false', 'Document the justified non-applicability where required by the contract.', 27)
    svg += _box(686, 550, 280, 160, 'Condition = unknown', 'Resolve the missing context or record a gap; do not treat unknown as false.', 27)
    svg += [_text(32, 777, 'Author → independent review → exact workflow handoff; human acceptance remains separate.', bold=True)]
    result['gen2-effective-output-contract.svg'] = '\n'.join([*svg, '</svg>']) + '\n'
    return result


def replace_figure(text, content):
    """Replace one generated figure while preserving surrounding manual text.

    Args:
        text: Existing Markdown containing one ordered ownership marker pair.
        content: Newly rendered figure block without markers.
    Returns:
        Updated Markdown with the original manual prefix and suffix.
    Raises:
        ValueError: Markers are absent, duplicated or reversed.
    """
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
        raise ValueError('Expected one ordered workflow diagram marker pair')
    return text[:text.index(START)] + START + '\n' + content.rstrip() + '\n' + text[text.index(END):]


def generate(root, check=False):
    """Refresh SVG assets and responsive numbered overviews, or report drift.

    Args:
        root: Checkout containing canonical workflow JSON and Markdown pages.
        check: When true, inspect generated output without writing files.
    Returns:
        Zero when generation succeeds/current; one when check detects drift.
    Raises:
        OSError, ValueError, KeyError: Required input, ownership or output is invalid.
    """
    root = Path(root)
    workflows = json.loads((root / '.ai/runtime/workflows.json').read_text())['workflows']
    outputs = {}
    for workflow in workflows:
        svg = render_workflow(workflow)
        name = 'workflow-' + workflow['key'] + '.svg'
        outputs[root / 'docs/assets/diagrams' / name] = svg
        items = '\n'.join(
            f'<li data-step="{step["step"]}"><span class="ai-workflow-step-number" aria-hidden="true">{step["step"]}</span>'
            f'<div><strong>{escape(step["role"])}</strong><p>{escape(step["does"])}</p></div></li>'
            for step in workflow['steps'])
        content = (f'<div class="ai-workflow-overview">\n'
                   f'<ol class="ai-workflow-steps" role="list" aria-label="{escape(workflow["title"], quote=True)} workflow steps">\n'
                   f'{items}\n</ol>\n</div>\n\n'
                   f'[Open the full-size workflow diagram](../assets/diagrams/{name}). '
                   'Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.')
        path = root / 'docs/workflow-library' / (workflow['key'] + '.md')
        outputs[path] = replace_figure(path.read_text(), content)
    outputs.update({root / 'docs/assets/diagrams' / name: svg for name, svg in concept_diagrams().items()})
    if any(path.is_symlink() for path in outputs):
        raise ValueError('Generated diagram targets must not be symbolic links')
    stale = [str(path.relative_to(root)) for path, content in outputs.items() if not path.exists() or path.read_text() != content]
    if check:
        print('PASS: workflow and Gen2 diagram sources match' if not stale else 'Diagram drift: ' + ', '.join(stale))
        return int(bool(stale))
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    print(f'Generated {len(workflows)} complete workflow figures and four Gen2 explanations')
    return 0


def main(argv=None):
    """Parse diagram generation options and return its non-publishing status.

    Args:
        argv: Optional argument sequence; None uses process arguments.
    Returns:
        Generation/check status; malformed arguments raise SystemExit.
    Raises:
        OSError, ValueError, KeyError: Canonical input or output ownership is invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    return generate(args.root, args.check)


if __name__ == '__main__':
    raise SystemExit(main())
