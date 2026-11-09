# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Validate and render the explicit portable ArchiMate 3.2 implementation profile.

Pinned MIT implementation data supplies all 11,569 permitted relationship triples.
The bundled Open Group authored exchange XSD is version 3.1: language and exchange
editions are deliberately distinct. A pass is bounded implementation validation,
not certification, evidence of stakeholder completeness or human acceptance.
"""
from __future__ import annotations

import argparse
from collections import deque
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import unicodedata
import xml.etree.ElementTree as ET

from lxml import etree

DATA = Path(__file__).resolve().parent.parent / 'ea/vendor/archimate-3.2'
CODES = {'Access': 'a', 'Composition': 'c', 'Flow': 'f', 'Aggregation': 'g',
         'Assignment': 'i', 'Influence': 'n', 'Association': 'o',
         'Realization': 'r', 'Specialization': 's', 'Triggering': 't', 'Serving': 'v'}
VIEW_FIELDS = ('stakeholders', 'concerns', 'decision', 'boundary', 'included_types',
               'completeness_criteria', 'exclusions', 'review_status')
LABEL_FONT = 'Noto Sans Mono CJK JP, DejaVu Sans Mono, monospace'


@lru_cache(maxsize=1)
def _resources():
    source = json.loads((DATA / 'provenance.json').read_text())
    for name, record in source['files'].items():
        if hashlib.sha256((DATA / name).read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('ARCHIMATE_PROFILE_RESOURCE_CHANGED:' + name)
    return source


def metadata():
    """Return a detached provenance record; raise ValueError if pinned data changed."""
    return json.loads(json.dumps(_resources()))


@lru_cache(maxsize=1)
def _matrix():
    _resources()
    root = ET.parse(DATA / 'relationships.xml').getroot()
    if root.get('version') != '3.2':
        raise ValueError('ARCHIMATE_EDITION_MISMATCH')
    return {source.get('concept'): {target.get('concept'): target.get('relations')
                                  for target in source} for source in root}


def relationship_matrix():
    """Return a detached source/target permission matrix with pinned relation codes."""
    return {source: dict(targets) for source, targets in _matrix().items()}


def _concept(kind):
    return 'Junction' if kind in ('AndJunction', 'OrJunction') else kind if isinstance(kind, str) else None


def allowed(source_type, relationship_type, target_type):
    """Return whether the 3.2 implementation table permits this typed triple.

    source_type and target_type are exact exchange concept names and
    relationship_type names the relation. Unknown types return False. Junction
    alternatives share the Junction permission row. The source table includes
    direct and derived permissions without distinguishing their derivation proof.
    """
    return isinstance(relationship_type, str) and CODES.get(relationship_type, '?') in _matrix().get(
        _concept(source_type), {}).get(_concept(target_type), '')


def validate(repository, edition='3.2'):
    """Return metamodel findings for a canonical repository without mutating it.

    Rejects empty and ambiguous identifiers before indexing either concept kind.
    Checks all source/relation/target triples, Access/Influence attributes,
    specialization cycles, composition ownership and junction continuity.
    Missing facts stay errors; this function never waives findings or grants
    authority. Raises ValueError for an unimplemented language edition.
    """
    if edition != '3.2':
        raise ValueError('ARCHIMATE_EDITION_UNSUPPORTED:' + str(edition))
    errors = []
    seen = set()
    def index(key):
        records = {}
        for item in repository.get(key, []):
            ident = item.get('id') if isinstance(item, dict) else None
            if not isinstance(ident, str) or not ident.strip() or any(char.isspace() for char in ident):
                errors.append('IDENTIFIER_INVALID:' + key)
                continue
            if ident in seen:
                errors.append('IDENTIFIER_COLLISION:' + key + ':' + ident)
                continue
            seen.add(ident)
            records[ident] = item
        return records
    elements = index('elements')
    relations = index('relationships')
    types = {ident: item.get('type') for ident, item in elements.items()}
    types.update({ident: 'Relationship' for ident in relations})
    for ident, element in elements.items():
        if _concept(element.get('type')) not in _matrix() or element.get('type') == 'Relationship':
            errors.append('UNKNOWN_CONCEPT:' + str(ident) + ':' + str(element.get('type')))
    parents = {}
    specialization = {}
    for ident, relation in relations.items():
        source, target, kind = relation.get('source'), relation.get('target'), relation.get('type')
        if not isinstance(source, str) or not isinstance(target, str) or source not in types or target not in types:
            errors.append('MISSING_ENDPOINT:' + str(ident))
            continue
        if not allowed(types[source], kind, types[target]):
            errors.append(f'ILLEGAL_RELATIONSHIP:{ident}:{types[source]}->{kind}->{types[target]}')
        if kind == 'Access' and relation.get('access_type') not in (None, 'Access', 'Read', 'Write', 'ReadWrite'):
            errors.append('ACCESS_MODE:' + str(ident))
        if kind == 'Influence' and relation.get('influence_strength') is not None:
            strength = relation['influence_strength']
            if (isinstance(strength, bool) or not isinstance(strength, (str, int, float))
                    or isinstance(strength, float) and not math.isfinite(strength)):
                errors.append('INFLUENCE_MODIFIER:' + str(ident))
        if kind == 'Composition':
            if target in parents and parents[target] != source:
                errors.append('COMPOSITION_MULTIPLE_OWNERS:' + str(target))
            parents[target] = source
        if kind == 'Specialization':
            specialization.setdefault(source, []).append(target)
    for label, edges in [('SPECIALIZATION', specialization),
                         ('COMPOSITION', {part: [owner] for part, owner in parents.items()})]:
        indegrees = {node: 0 for node in edges}
        for targets in edges.values():
            for target in targets:
                indegrees[target] = indegrees.get(target, 0) + 1
        ready = deque(node for node, degree in indegrees.items() if not degree)
        visited = 0
        while ready:
            node = ready.popleft(); visited += 1
            for target in edges.get(node, []):
                indegrees[target] -= 1
                if not indegrees[target]:
                    ready.append(target)
        if visited != len(indegrees):
            errors.append(label + '_CYCLE:' + ','.join(sorted(str(node) for node, degree in indegrees.items() if degree)))
    for ident, element in elements.items():
        if _concept(element.get('type')) != 'Junction':
            continue
        incoming = [relation for relation in relations.values() if relation.get('target') == ident]
        outgoing = [relation for relation in relations.values() if relation.get('source') == ident]
        if not incoming or not outgoing or len({relation.get('type') for relation in incoming + outgoing}) != 1:
            errors.append('JUNCTION_CONTINUITY:' + str(ident))
    return {'profile': 'archimate-3.2-portable', 'language_edition': edition,
            'source_revision': _resources()['source_revision'], 'valid': not errors,
            'errors': sorted(set(errors)), 'checked_relationships': len(relations),
            'limits': ['Permitted-table check; no direct-versus-derived proof distinction.',
                       'Stakeholder completeness and professional approval remain separate.']}


@lru_cache(maxsize=1)
def _schema():
    _resources()
    class LocalResolver(etree.Resolver):
        def resolve(self, url, public_id, context):
            name = url.rsplit('/', 1)[-1]
            if name not in _resources()['files']:
                raise ValueError('UNREGISTERED_SCHEMA_IMPORT:' + name)
            return self.resolve_filename(str(DATA / name), context)
    parser = etree.XMLParser(no_network=True, resolve_entities=False)
    parser.resolvers.add(LocalResolver())
    return etree.XMLSchema(etree.parse(str(DATA / 'archimate3_Diagram.xsd'), parser))


def exchange_schema_errors(path):
    """Return offline official exchange-XSD errors for an XML path.

    Uses the pinned Open Group authored 3.1 exchange schemas, including diagram
    children, datatypes and references. Parse/schema failures return diagnostics;
    network and entity resolution are disabled. No external application is used.
    """
    try:
        document = etree.parse(str(path), etree.XMLParser(no_network=True, resolve_entities=False))
        schema = _schema()
        return [] if schema.validate(document) else [str(item) for item in schema.error_log]
    except (OSError, etree.Error, ValueError) as error:
        return [str(error)]


def validate_viewpoint(repository, view):
    """Check a view's explicit concern contract and source links without approving it.

    repository supplies canonical source objects; view selects their IDs.
    Required contract values describe stakeholders, concerns, decision, boundary,
    included concept types, completeness criteria, exclusions and review state.
    A structurally complete contract remains REVIEW_PENDING until an independent
    review outside this deterministic tool establishes its actual adequacy.
    """
    contract = view.get('viewpoint_contract', {})
    errors = []
    for field in VIEW_FIELDS:
        value = contract.get(field)
        if field == 'exclusions':
            valid = isinstance(value, list)
        elif field in ('stakeholders', 'concerns', 'included_types', 'completeness_criteria'):
            valid = isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)
        else:
            valid = isinstance(value, str) and bool(value.strip())
        if not valid:
            errors.append('VIEWPOINT_FIELD:' + field)
    errors.extend(_view_scope_errors(repository, view))
    known = {item.get('id'): item for item in repository.get('elements', [])}
    for ident in view.get('element_refs', []):
        if ident not in known:
            errors.append('VIEWPOINT_SOURCE_MISSING:' + str(ident))
        elif contract.get('included_types') and known[ident].get('type') not in contract['included_types']:
            errors.append('VIEWPOINT_TYPE_EXCLUDED:' + str(ident))
    return {'structurally_complete': not errors, 'errors': errors, 'status': 'REVIEW_PENDING',
            'review_claim': 'Independent semantic and visual review is required; a local status string is not approval.'}


def _view_scope_errors(repository, view):
    elements = {item.get('id') for item in repository.get('elements', [])}
    relations = {item.get('id'): item for item in repository.get('relationships', [])}
    selected_elements = set(view.get('element_refs', []))
    selected_relations = set(view.get('relationship_refs', []))
    selected = selected_elements | selected_relations
    errors = ['VIEWPOINT_SOURCE_MISSING:' + str(ident) for ident in selected_elements - elements]
    for ident in selected_relations:
        relation = relations.get(ident)
        if relation is None:
            errors.append('VIEWPOINT_RELATIONSHIP_MISSING:' + str(ident))
        elif relation.get('source') not in selected or relation.get('target') not in selected:
            errors.append('VIEWPOINT_RELATIONSHIP_ENDPOINT_OUTSIDE:' + str(ident))
    return errors


def _shape(kind, x, y, width, height):
    fill = '#fff4b5' if kind.startswith('Business') else '#cfefff' if kind.startswith('Application') else '#d5f5d1' if kind in ('Node', 'Device', 'SystemSoftware') or kind.startswith('Technology') else '#eee4ff'
    shape = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{12 if any(word in kind for word in ("Process", "Function", "Service", "Interaction", "Event")) else 0}" fill="{fill}" stroke="#24344b"/>'
    if kind in ('BusinessObject', 'DataObject', 'Artifact'):
        shape += f'<path d="M{x} {y+17}h{width}" stroke="#24344b"/>'
    if kind == 'ApplicationComponent':
        shape += f'<path d="M{x+width-26} {y+8}h18v22h-18z M{x+width-30} {y+12}h8v5h-8z M{x+width-30} {y+22}h8v5h-8z" fill="{fill}" stroke="#24344b"/>'
    if kind == 'BusinessActor':
        shape += f'<circle cx="{x+width-15}" cy="{y+11}" r="4" fill="none" stroke="#24344b"/><path d="M{x+width-15} {y+15}v11m-7 -7h14m-7 7l-6 7m6 -7l6 7" fill="none" stroke="#24344b"/>'
    return shape


def _wrap_label(text, width_cells):
    """Wrap losslessly at word/grapheme boundaries for conservative monospace cells."""
    clusters = []
    for char in str(text):
        if clusters and (unicodedata.combining(char) or char in ('\u200d', '\ufe0e', '\ufe0f') or clusters[-1].endswith('\u200d')):
            clusters[-1] += char
        else:
            clusters.append(char)
    def cells(cluster):
        return sum(0 if unicodedata.combining(char) or char in ('\u200d', '\ufe0e', '\ufe0f')
                   else 2 if unicodedata.east_asian_width(char) in ('W', 'F', 'A') else 1 for char in cluster)
    lines = []
    start = 0
    while start < len(clusters):
        end, used, word_break = start, 0, None
        while end < len(clusters):
            size = cells(clusters[end])
            if end > start and used + size > width_cells:
                break
            used += size
            end += 1
            if clusters[end-1].isspace():
                word_break = end
            if '\n' in clusters[end-1]:
                break
        if end < len(clusters) and word_break is not None:
            end = word_break
        lines.append(''.join(clusters[start:end]))
        start = end
    return lines or ['']


def render(repository, view, output):
    """Write a draft typed-box ArchiMate view with relationship-specific notation.

    repository supplies canonical objects, view selects their IDs, and output is
    a writable SVG path. The portable typed-box representation uses labels and
    aspect shapes; specialist concept-icon fidelity requires independent visual
    review. All eleven relationships have distinct standard marker/line semantics.
    Lossless word/grapheme wrapping bounds label width; node heights, row spacing
    and edge attachments adapt to line counts. Full names remain SVG titles.
    Raises ValueError for unknown concepts or illegal relationships, OSError if
    output cannot be written. Does not mutate the model or grant publication.
    """
    checked = validate(repository)
    if not checked['valid']:
        raise ValueError('NOTATION_MODEL_INVALID:' + ';'.join(checked['errors']))
    index = {element['id']: element for element in repository.get('elements', [])}
    refs = view.get('element_refs', [])
    scope_errors = _view_scope_errors(repository, view)
    if scope_errors:
        raise ValueError('NOTATION_VIEW_INVALID:' + ';'.join(scope_errors))
    columns = max(1, math.ceil(math.sqrt(len(refs))))
    width = max(840, columns * 340 + 60)
    heading = str(view.get('name', 'Architecture view'))
    heading_lines = _wrap_label(heading, int((width-60)/11.2))
    label_lines = {ref: _wrap_label(index[ref].get('name', ref), 24) for ref in refs}
    node_heights = {ref: max(80, 48+17*(len(lines)-1)+18+14) for ref, lines in label_lines.items()}
    positions = {}
    row_y = 30+22*len(heading_lines)+25
    for start in range(0, len(refs), columns):
        row = refs[start:start+columns]
        for column, ref in enumerate(row):
            positions[ref] = (40+column*340, row_y)
        row_y += max(node_heights[ref] for ref in row)+90
    content_bottom = max((y+node_heights[ref] for ref, (_, y) in positions.items()), default=row_y)
    height = content_bottom+150
    esc = lambda value: html.escape(str(value), quote=True)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(view.get("name", "Architecture view"))}">',
             '<title>ArchiMate 3.2 draft typed-box view</title><desc>Typed source elements and relationship notation; independent semantic and visual review pending.</desc>',
             '<defs><marker id="open" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto-start-reverse"><path d="M1 1L10 6L1 11" fill="none" stroke="#24344b"/></marker><marker id="filled" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto-start-reverse"><path d="M1 1L10 6L1 11z" fill="#24344b"/></marker><marker id="triangle" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M1 1L10 6L1 11z" fill="white" stroke="#24344b"/></marker><marker id="diamond" markerWidth="14" markerHeight="12" refX="1" refY="6" orient="auto"><path d="M1 6L6 1L12 6L6 11z" fill="#24344b" stroke="#24344b"/></marker><marker id="hollow" markerWidth="14" markerHeight="12" refX="1" refY="6" orient="auto"><path d="M1 6L6 1L12 6L6 11z" fill="white" stroke="#24344b"/></marker><marker id="ball" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><circle cx="5" cy="5" r="3" fill="#24344b"/></marker></defs>',
             '<defs><marker id="open-start" markerWidth="12" markerHeight="12" refX="2" refY="6" orient="auto"><path d="M11 1L2 6L11 11" fill="none" stroke="#24344b"/></marker></defs>',
             f'<rect width="{width}" height="{height}" fill="white"/>',
             f'<text class="view-name" font-family="{LABEL_FONT}" font-size="18" xml:space="preserve">'
             + ''.join(f'<tspan x="30" y="{30+22*i}">{esc(line)}</tspan>' for i, line in enumerate(heading_lines)) + '</text>']
    selected = set(view.get('relationship_refs', []))
    relations = {item['id']: item for item in repository.get('relationships', []) if item['id'] in selected}
    centers = {ident: (x+110, y+node_heights[ident]/2) for ident, (x, y) in positions.items()}
    dependants = {}
    dependencies = {}
    for ident, relation in relations.items():
        required = {relation['source'], relation['target']} & selected
        dependencies[ident] = len(required)
        for dependency in required:
            dependants.setdefault(dependency, []).append(ident)
    ready = deque(ident for ident, count in dependencies.items() if not count)
    drawn = set()
    def boundary(ident, toward):
        x, y = centers[ident]
        if ident not in positions:
            return x, y
        dx, dy = toward[0]-x, toward[1]-y
        factor = min(110/abs(dx) if dx else float('inf'), node_heights[ident]/2/abs(dy) if dy else float('inf'))
        return (x+dx*factor, y+dy*factor) if math.isfinite(factor) else (x+110, y)
    while ready:
        ident = ready.popleft()
        relation = relations[ident]
        source, target = relation['source'], relation['target']
        x1, y1 = boundary(source, centers[target])
        x2, y2 = boundary(target, centers[source])
        if source == target:
            cx, cy = centers[source]
            x1, y1, x2, y2 = cx+110, cy-15, cx+110, cy+15
            route = f'M{x1} {y1}C{x1+70} {y1-40} {x2+70} {y2+40} {x2} {y2}'
            anchor = (x1+52.5, cy)
        else:
            route = f'M{x1} {y1}L{x2} {y2}'
            anchor = ((x1+x2)/2, (y1+y2)/2)
        kind = relation['type']; attrs = ''
        if kind in ('Realization', 'Access', 'Influence'):
            attrs += ' stroke-dasharray="6 4"'
        start = 'diamond' if kind == 'Composition' else 'hollow' if kind == 'Aggregation' else 'ball' if kind == 'Assignment' else None
        end = 'triangle' if kind in ('Realization', 'Specialization') else 'filled' if kind in ('Assignment', 'Triggering', 'Flow') else 'open' if kind in ('Serving', 'Influence') else None
        if kind == 'Flow':
            attrs += ' stroke-dasharray="10 4"'
        if kind == 'Access':
            mode = relation.get('access_type', 'Access')
            start = 'open-start' if mode in ('Read', 'ReadWrite') else None
            end = 'open' if mode in ('Write', 'ReadWrite') else None
        if start:
            attrs += f' marker-start="url(#{start})"'
        if end:
            attrs += f' marker-end="url(#{end})"'
        parts += [f'<path data-relationship-id="{esc(ident)}" d="{route}" stroke="#24344b" fill="none"{attrs}/>',
                  f'<text x="{anchor[0]}" y="{anchor[1]-8}" text-anchor="middle" font-family="sans-serif" font-size="11">{esc(kind)}</text>']
        centers[ident] = anchor
        drawn.add(ident)
        for dependant in dependants.get(ident, []):
            dependencies[dependant] -= 1
            if not dependencies[dependant]:
                ready.append(dependant)
    if drawn != selected:
        raise ValueError('NOTATION_VIEW_UNRESOLVED_RELATIONSHIP_ANCHORS:' + ','.join(sorted(selected-drawn)))
    for ident, (x, y) in positions.items():
        element = index[ident]
        name = str(element.get('name', ident))
        lines = label_lines[ident]
        parts += [f'<g data-element-id="{esc(ident)}" role="group" aria-label="{esc(name)}"><title>{esc(name)}</title>',
                  _shape(element['type'], x, y, 220, node_heights[ident]),
                  f'<text class="element-name" font-family="{LABEL_FONT}" font-size="13" xml:space="preserve">'
                  + ''.join(f'<tspan x="{x+10}" y="{y+48+17*i}">{esc(line)}</tspan>' for i, line in enumerate(lines)) + '</text>',
                  f'<text x="{x+10}" y="{y+48+17*(len(lines)-1)+18}" font-family="{LABEL_FONT}" font-size="10">{esc(element["type"])}</text></g>']
    parts += [f'<text x="30" y="{height-65}" font-family="sans-serif" font-size="12">ArchiMate 3.2 typed-box draft; semantic and visual review pending.</text>',
              f'<text x="30" y="{height-40}" font-family="sans-serif" font-size="11">Concept labels identify types; specialist icon fidelity and viewpoint completeness require review.</text></svg>']
    Path(output).write_text(''.join(parts), encoding='utf-8')
    return {'status': 'DRAFT_NOTATION', 'language_edition': '3.2',
            'representation': 'typed-box', 'elements': len(refs), 'relationships': len(drawn), 'visual_review': 'pending',
            'viewpoint': validate_viewpoint(repository, view)}


def main(argv=None):
    """Run explicit profile validate/render commands and return their exit status.

    argv supplies optional CLI tokens; files are canonical JSON. Validation writes no
    source. Render requires a view ID and destination. Parse/file errors propagate.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('validate'); check.add_argument('repository')
    draw = sub.add_parser('render'); draw.add_argument('repository'); draw.add_argument('--view', required=True); draw.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    repository = json.loads(Path(args.repository).read_text())
    if args.command == 'validate':
        result = validate(repository)
    else:
        view = next(view for view in repository.get('views', []) if view['id'] == args.view)
        result = render(repository, view, args.out)
    print(json.dumps(result, indent=2))
    return 0 if result.get('valid', result.get('status') == 'DRAFT_NOTATION') else 1


if __name__ == '__main__':
    raise SystemExit(main())
