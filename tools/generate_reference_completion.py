#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Generate the authored 18-family reference extension and its integrity index.

Usage: python3 tools/generate_reference_completion.py [--check]. Existing
baseline Markdown remains byte-identical; only explicitly owned new cases are
generated. Successful generation is not professional qualification or approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from extended_reference_definitions import CONTEXTS, REFERENCE_CASES

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = Path('.ai/runtime/content/expert_references')
EXAMPLE_START = '<!-- JAI:PROFESSIONAL-EXAMPLE:START -->'
EXAMPLE_END = '<!-- JAI:PROFESSIONAL-EXAMPLE:END -->'


def render_reference(family, complexity):
    """Return one synthetic Markdown case with source-addressable information.

    Args:
        family: Exact key in the authored REFERENCE_CASES definitions.
        complexity: simple, medium or complex, selecting explicit case context.
    Returns:
        English Markdown with required DCS anchors, counterexample and rationale.
    Raises:
        KeyError: The family or complexity is not an authored selection.
    """
    _, fields, wrong, disposition = REFERENCE_CASES[family]
    name, boundary, population = CONTEXTS[complexity]
    lines = ['---', f'reference_id: example:{family}:{complexity}',
             "schema_version: '1.0.0'", 'document_kind: ' + family,
             'complexity: ' + complexity, 'language: en',
             'classification: public-synthetic', 'provenance: ai-authored-proposed',
             'fictional_context: true', 'applicable_dcs: kind/' + family,
             'approval_status: not-human-approved', 'content_revision: 1.0.0', '---', '',
             '# ' + family.replace('-', ' ').title() + ' — ' + name, '',
             '**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values '
             'and observations below are invented. Tests are not executed and no '
             'professional or human approval is established.', '',
             f'**Boundary:** {boundary}. **Illustrative evaluation population:** '
             f'{population} synthetic records or requests; this is a proposed scope, '
             'not a measured production sample.', '']
    complexity_rule = {
        'simple': 'Use one source revision and one receiving owner. Confirm the bounded '
                  'normal case and a meaningful failure before expanding scope.',
        'medium': 'Separate producer and consumer revisions. Test cross-service failure '
                  'and reconciliation; one team\'s success does not establish the next team\'s acceptance.',
        'complex': 'Partition evidence by jurisdiction, supplier and irreversible boundary. '
                   'Do not aggregate away a failed cohort; legal applicability and residual '
                   'risk decisions require their actual competent owners.'}[complexity]
    for field, (requirement, example) in fields.items():
        lines += [f'<a id="dcs-proposed-{family}.reference_{field}"></a>',
                  '## ' + field.replace('_', ' ').title(), '', example, '',
                  '**Acceptance question:** ' + requirement, '',
                  '**Context application:** ' + complexity_rule, '']
    lines += ['## Evidence and alternatives', '',
              '`SYN-INPUT-01` is the fictional requirements and source-revision record. '
              '`SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. '
              '`SYN-REVIEW-01` is a review request, not a completed review. In a real task, '
              'replace these with attributable permitted inputs and observed results.', '',
              'Compare the bounded baseline with the proposed change using the same '
              'business invariant. Retaining the baseline avoids transition exposure '
              'but leaves the stated problem unresolved; adopting the change before '
              'verification creates an unsupported confidence claim.', '',
              '## Plausible but incorrect conclusion', '', wrong, '',
              '**Why it fails:** the conclusion skips an evidence or semantic boundary '
              'identified in the information sections. A dated, polished artifact '
              'cannot repair the missing observation or change the meaning of an interface.', '',
              '## Reasoned disposition and downstream action', '', disposition, '',
              'The source owner supplies missing evidence; an independent competent '
              'reviewer assesses the exact revision. The receiving owner records '
              'acceptance or required rework. Human approval and release remain '
              'separate existing authority acts.', '',
              '## Professional basis and limitations', '',
              'Resolve the linked DCS foundation and its professional-source records. '
              'Record the source edition, applicability, interpretation, method and '
              'evidence for the real engagement. This case is a JAI-authored '
              'illustration, not a quotation from or certification against an external '
              'standard. Complexity changes the required evidence boundary, not '
              'the truth status of fictional facts.', '']
    return '\n'.join(lines)


def build(root=ROOT):
    """Return owned case bytes and an extended index without altering baseline cases.

    Args:
        root: Checkout containing the original trusted reference index.
    Returns:
        Mapping of absolute output paths to UTF-8 text; original index metadata
        and original 135 case digests remain unchanged.
    Raises:
        OSError, ValueError: Baseline data is missing, changed or escapes ownership.
    """
    base = Path(root) / DIRECTORY
    if base.is_symlink() or not base.resolve().is_relative_to(Path(root).resolve()):
        raise ValueError('Reference library escapes checkout ownership')
    manifest = json.loads((base / 'index.json').read_text())
    entries = [entry for entry in manifest['entries']
               if entry['document_kind'] not in REFERENCE_CASES]
    for entry in entries:
        path = base / entry['path']
        if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
            raise ValueError('Baseline reference path escapes owned library')
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('Baseline reference changed; independent source review required')
    result = {}
    for family in REFERENCE_CASES:
        for level in CONTEXTS:
            text = render_reference(family, level)
            raw = text.encode()
            path = family + '/' + level + '.md'
            result[base / path] = text
            fields = REFERENCE_CASES[family][1]
            entries.append({
                'reference_id': f'example:{family}:{level}', 'document_kind': family,
                'complexity': level, 'path': path, 'language': 'en',
                'provenance': 'ai-authored-proposed',
                'approval_status': 'not-human-approved',
                'dcs_binding_status': 'proposed-mapped',
                'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                'anchor_ids': [f'proposed-{family}.reference_{field}' for field in fields],
                'review_status': 'independent-review-pending', 'review_version': '1.0.0'})
    families = [family for family in manifest['families'] if family not in REFERENCE_CASES]
    manifest.update(version='2.4.0', baseline_version='2.3.0',
                    families=families + list(REFERENCE_CASES), entries=entries,
                    reference_count=len(entries))
    manifest['new_proposed_families'] = list(dict.fromkeys(
        manifest['new_proposed_families'] + list(REFERENCE_CASES)))
    manifest['coverage_extension'] = {
        'families': list(REFERENCE_CASES), 'reference_count': len(REFERENCE_CASES) * len(CONTEXTS),
        'review_status': 'independent-review-pending', 'human_approved': False,
        'basis': 'Concrete modality cases with reasoned counterexamples; not human-gold calibration.'}
    result[base / 'index.json'] = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    return result


def project_role_example(text, record, family, case_text):
    """Replace a generic response outline with a source-linked worked case.

    Args:
        text: Role Markdown containing the numbered worked-example section.
        record: Exact effective first-output guidance for the role.
        family: Selected registered reference-family identifier.
        case_text: Validated medium reference Markdown from the bundled library.
    Returns:
        Updated Markdown. Other numbered sections and substantive pre-existing
        examples are retained; only the owned example block is refreshed later.
    Raises:
        ValueError: The worked-example section or ownership markers are malformed.
    """
    match = re.search(r'^## 15\. [^\n]+\n', text, re.M)
    if not match:
        raise ValueError('Role lacks the worked-example section')
    end = re.search(r'^## \d+\. ', text[match.end():], re.M)
    stop = match.end() + end.start() if end else len(text)
    body = text[match.end():stop]
    retained_tail = ''
    if EXAMPLE_START in body or EXAMPLE_END in body:
        if body.count(EXAMPLE_START) != 1 or body.count(EXAMPLE_END) != 1:
            raise ValueError('Ambiguous worked-example ownership')
        retained = body[:body.index(EXAMPLE_START)].strip()
        retained_tail = body[body.index(EXAMPLE_END) + len(EXAMPLE_END):].strip()
    elif '**Expected shape of a good response:**' in body:
        request = re.search(r'^\*\*Request\.\*\*.*$', body, re.M)
        retained = request.group(0) if request else ''
    else:
        retained = body.strip()
    unheaded = re.sub(r'\A---\n.*?\n---\n', '', case_text, count=1, flags=re.S)
    anchor = re.search(r'<a id="dcs-[^"]+"></a>\s*\n#{1,6}[^\n]*\n', unheaded)
    if not anchor:
        raise ValueError('Reference has no source-addressable worked material')
    remainder = unheaded[anchor.end():]
    excerpt = re.split(r'\n(?:<a id="dcs-|## )', remainder, maxsplit=1)[0].strip()
    if not excerpt:
        raise ValueError('Reference worked material is empty')
    delivery = record['effective_deliverable']
    generated = [EXAMPLE_START, '', '**Synthetic worked case — no project facts or approval.**', '',
                 '**Assigned work product:** ' + delivery['name'] + '.', '',
                 '**Illustrative case material:**', '', excerpt, '',
                 '**Apply the role boundary:** resolve the actual section 3 inputs '
                 'and section 7 gates for this assignment. The shared case demonstrates '
                 'professional depth; replace its fictional subject and measurements '
                 'with permitted evidence for the actual request.', '',
                 '**Professional acceptance questions:**', '']
    generated += ['- ' + criterion for criterion in record['acceptance_criteria']]
    generated += ['', '**Reasoned decision:** distinguish the native work product '
                  'from its evidence wrapper. A described procedure, policy or '
                  'successful render cannot establish that an operation ran, a '
                  'business invariant held or an accountable owner accepted it.', '',
                  '**Counterexample:** a polished response that declares this output '
                  'complete while its required source version, observation or independent '
                  'review is missing must remain incomplete. Name the missing evidence '
                  'and responsible owner instead of filling the gap with an invented result.', '',
                  '**Full worked reference:** select `' + family + '` at `simple`, '
                  '`medium` or `complex` through the existing expert-reference resolver. '
                  'Its cases include alternatives, practical mechanics, evidence limits '
                  'and downstream actions; the reference supplies no execution rights '
                  'or human approval.', '', EXAMPLE_END, '']
    replacement = '\n' + retained + ('\n\n' if retained else '') + '\n'.join(generated)
    if retained_tail:
        replacement += '\n' + retained_tail + '\n'
    return text[:match.end()] + replacement + text[stop:]


def role_example_outputs(root=ROOT, role_slugs=None, reference_texts=None):
    """Return generated section-15 projections for selected canonical roles.

    Args:
        root: Checkout with generated effective guidance and reference bindings.
        role_slugs: Optional exact role slugs; None selects the complete catalogue.
        reference_texts: Candidate texts from build for same-generation projections;
            omitted paths use the validated existing reference files.
    Returns:
        Absolute role paths to complete Markdown, with all other sections retained.
    Raises:
        OSError, ValueError: A role, first output, path or selected reference is invalid.
    """
    root = Path(root).resolve()
    sys.path.insert(0, str(root / '.ai/runtime/tools'))
    from expert_references import ExpertReferences
    library = ExpertReferences(root)
    guidance = json.loads((root / '.ai/runtime/content/role-output-guidance.json').read_text())
    roles = json.loads((root / '.ai/runtime/roles.json').read_text())['roles']
    selected = {role['slug'] for role in roles} if role_slugs is None else set(role_slugs)
    if not selected or not selected <= {role['slug'] for role in roles}:
        raise ValueError('Unknown or empty role example selection')
    first = {record['role_slug']: record for record in guidance['outputs']
             if record['deliverable_number'] == 1}
    result = {}
    for role in roles:
        if role['slug'] not in selected:
            continue
        record = first[role['slug']]
        family = library.canonical_family(record['semantic_family'], contract_id=record['id'])
        reference = library.base / family / 'medium.md'
        if reference_texts is not None and reference in reference_texts:
            case_text = reference_texts[reference]
        else:
            library.validate(reference, family, 'medium', bundled=True)
            case_text = reference.read_text()
        path = root / '.ai' / role['path']
        if path.is_symlink() or not path.resolve().is_relative_to(root / '.ai/skills'):
            raise ValueError('Role example target escapes catalogue')
        result[path] = project_role_example(path.read_text(), record, family, case_text)
    return result


def main(argv=None):
    """Write the owned extension, or check reproducibility without mutation.

    Args:
        argv: Optional command arguments, otherwise process arguments.
    Returns:
        Zero on success/current output, one when --check finds drift.
    Raises:
        OSError, ValueError: Baseline integrity or a target ownership check fails.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--role-examples', action='store_true')
    args = parser.parse_args(argv)
    args.root = args.root.resolve()
    outputs = build(args.root)
    if args.role_examples:
        outputs.update(role_example_outputs(args.root, reference_texts=outputs))
    changed = [path for path, text in outputs.items()
               if not path.is_file() or path.read_text() != text]
    if args.check:
        print('Reference extension ' + ('differs' if changed else 'is reproducible'))
        return int(bool(changed))
    for path in changed:
        text = outputs[path]
        owned = [(args.root / DIRECTORY).resolve(), (args.root / '.ai/skills').resolve()]
        if path.is_symlink() or not any(path.resolve().is_relative_to(base) for base in owned):
            raise ValueError('Refusing a symlink reference target')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    role_count = sum(path.is_relative_to((args.root / '.ai/skills').resolve()) for path in outputs)
    print(f'Generated {len(REFERENCE_CASES) * len(CONTEXTS)} illustrative references and '
          f'{role_count} role examples; baseline reference bytes preserved')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
