# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Build authored SABSA narrative publication models without inventing architecture facts."""
import json
from pathlib import Path

PROFILE_ROOT = Path(__file__).resolve().parents[1] / 'sabsa/publication/profiles'


def narrative_issues(api, lib):
    """Validate authored chapter provenance and English-edition declarations.

    Args:
        api: SABSA module exposing parse and ids helpers.
        lib: Canonical library directory.
    Returns:
        Pair of error and warning lists; absent optional narrative trees are allowed.
    """
    errors, warnings = [], []
    for path in sorted((Path(lib) / 'narratives').glob('*/*.md')):
        if path.name == 'README.md': continue
        try:
            meta = api.parse(path)
        except api.SabsaError as exc:
            errors.append(str(exc)); continue
        if meta.get('basis') not in ('stated', 'inferred', 'assumed'):
            errors.append(f'{path}: narrative basis must be stated, inferred or assumed')
        if not meta.get('author'):
            warnings.append(f'{path}: narrative author is not recorded')
        if meta.get('language') != 'en':
            warnings.append(f'{path}: English edition needs author-reviewed English narrative (language: en); source text is not translated')
        if not meta.get('_body', '').strip():
            warnings.append(f'{path}: narrative is empty')
        if meta.get('basis') == 'assumed':
            warnings.append(f'{path}: narrative contains unconfirmed assumptions')
        if meta.get('basis') in ('stated', 'inferred') and not meta.get('source'):
            errors.append(f'{path}: stated/inferred narrative requires source provenance')
        for source in api.ids(meta.get('source')):
            relative = Path(source.split('#', 1)[0])
            if relative.is_absolute() or '..' in relative.parts or not (Path(lib) / relative).is_file():
                errors.append(f'{path}: narrative source does not resolve inside library: {source}')
    return errors, warnings


def scaffold_narratives(lib, layer):
    """Create missing authored chapter skeletons without overwriting existing prose.

    Args:
        lib: Existing canonical library directory.
        layer: Canonical SABSA layer key.
    Returns:
        Number of new chapter skeletons with explicit unconfirmed provenance.
    Raises:
        OSError: If a profile cannot be read or output cannot be written.
    """
    profile = json.loads((PROFILE_ROOT / (layer + '.json')).read_text(encoding='utf-8'))
    directory = Path(lib) / 'narratives' / layer
    directory.mkdir(parents=True, exist_ok=True)
    count = 0
    for chapter in profile['chapters']:
        path = directory / (chapter['key'] + '.md')
        if not path.exists():
            path.write_text('---\nbasis: assumed\nsource: \nauthor: \nlanguage: en\n---\n', encoding='utf-8')
            count += 1
    return count


def publication_model(api, lib, model, layer):
    """Enrich a layer model with authored chapters, complete entries and typed trace paths.

    Args:
        api: SABSA module providing metamodel, loading and business-parent functions.
        lib: Canonical library directory containing optional narratives/<layer>/*.md.
        model: Complete-library document model; copied before enrichment.
        layer: Canonical SABSA layer key, including service-management.
    Returns:
        Enriched model with explicit missing-narrative gaps and original source prose.
    Raises:
        ValueError: If an authored narrative is empty or contains NUL bytes.
        OSError: If a profile or authored narrative cannot be read.
    """
    profile = json.loads((PROFILE_ROOT / (layer + '.json')).read_text(encoding='utf-8'))
    entries, errors = api.load(lib)
    result = dict(model)
    result['publication_title'] = profile['title']
    result['publication_audience'] = profile['audience']
    result['publication_purpose'] = profile['purpose']
    result['publication_language'] = 'en'
    chapters, gaps = [], []
    for chapter in profile['chapters']:
        path = Path(lib) / 'narratives' / layer / (chapter['key'] + '.md')
        meta = api.parse(path) if path.is_file() else {}
        prose = meta.get('_body', '').strip()
        if '\x00' in prose:
            raise ValueError(f'{path}: narrative must contain UTF-8 Markdown without NUL')
        if not prose:
            gaps.append({'text': f"{chapter['heading']}: authored narrative not supplied ({path.relative_to(lib).as_posix()})."})
        chapters.append({**chapter, 'prose': prose, 'missing': not prose,
                         'path': path.relative_to(lib).as_posix(), 'basis': meta.get('basis') or 'Not recorded',
                         'source': meta.get('source') or 'Not recorded', 'author': meta.get('author') or 'Not recorded',
                         'language': meta.get('language') or 'Not declared', 'english_gap': bool(prose and meta.get('language') != 'en')})
    groups = []
    for group in profile['groups']:
        records = []
        for eid, entry in sorted(entries.items()):
            if entry['_dirtype'] not in group['types']:
                continue
            typ = entry['_dirtype']; spec = api.TYPES[typ]
            fields = [{'name': field.replace('_', ' ').capitalize(), 'value': ('Authoring gap — original source placeholder: ' + entry[field]) if entry.get(field) and api.PLACEHOLDER.search(entry[field]) else (entry.get(field) or 'Not recorded')}
                      for field in dict.fromkeys([*spec['fields'], 'aspect', 'status', *sorted(k for k in entry if not k.startswith('_'))]) if field not in ('id', 'title', 'type')]
            edges = []
            for field, (target_type, required) in spec['links'].items():
                for target in api.ids(entry.get(field)):
                    target_entry = entries.get(target, {})
                    edges.append({'field': field, 'target': target, 'target_type': target_type,
                                  'title': target_entry.get('title') or 'Unresolved reference',
                                  'business': field in api.BUSINESS_PARENT_FIELDS[typ]})
            paths = []
            limit = 128
            def visit(current, trail, text):
                if len(paths) >= limit:
                    return
                if current in trail:
                    paths.append({'text': text + ' [CYCLE — unresolved]'}); return
                current_entry = entries[current]
                label = f"{current} ({current_entry['_dirtype']}): {current_entry.get('title', '')}"
                text += label
                if current_entry['_dirtype'] == 'driver':
                    paths.append({'text': text + ' — Business outcome: ' + (current_entry.get('statement') or '[statement not recorded]')}); return
                parent_fields = api.BUSINESS_PARENT_FIELDS[current_entry['_dirtype']]
                followed = False
                for field in parent_fields:
                    target_type, required = api.TYPES[current_entry['_dirtype']]['links'][field]
                    targets = api.ids(current_entry.get(field))
                    if not targets and required:
                        paths.append({'text': text + f" —[{field} → {target_type}]→ [MISSING REQUIRED RELATIONSHIP]"})
                    for target in targets:
                        followed = True
                        hop = text + f" —[{field}]→ "
                        if target not in entries:
                            paths.append({'text': hop + target + ' [UNRESOLVED TARGET]'});
                        elif entries[target]['_dirtype'] != target_type:
                            paths.append({'text': hop + target + f" [TYPE MISMATCH: expected {target_type}]"})
                        else:
                            visit(target, trail + [current], hop)
                if not followed and not parent_fields:
                    paths.append({'text': text + ' [NO BUSINESS JUSTIFICATION RELATIONSHIP] '})
            visit(eid, [], '')
            if typ == 'driver':
                for candidate in sorted(entries):
                    if candidate == eid: continue
                    before = len(paths)
                    visit(candidate, [], '')
                    paths[before:] = [path for path in paths[before:] if f"{eid} (driver):" in path['text']]
                    if len(paths) >= limit: break
            if len(paths) >= limit:
                paths.append({'text': '[TRACE PRESENTATION LIMIT: 128 paths; inspect canonical typed dependencies for remaining paths.]'})
            records.append({'id': eid, 'title': entry.get('title', ''), 'type': typ,
                            'body': entry.get('_body', '').strip(), 'placeholder_gap': any(api.PLACEHOLDER.search(str(value)) for name, value in entry.items() if not name.startswith('_')), 'missing_body': not entry.get('_body', '').strip(),
                            'fields': fields, 'edges': edges, 'has_edges': bool(edges), 'paths': paths,
                            'external': bool(entry.get('_external')), 'origin': entry.get('_origin_library', ''), 'origin_id': entry.get('_origin_id', eid),
                            'path': entry.get('_path', ''), 'language': entry.get('language') or 'Not declared',
                            'english_gap': entry.get('language') not in (None, '', 'en')})
        groups.append({**group, 'records': records, 'empty': not records})
    result.update(publication_chapters=chapters, publication_groups=groups,
                  publication_gaps=gaps, has_publication_gaps=bool(gaps),
                  publication_sources=[{'file': source['file'], 'citations': [{'path': path} for path in source['cited_by'].split()]} for source in model['sources']])
    if gaps or any(chapter['english_gap'] for chapter in chapters) or any(record['missing_body'] or record['english_gap'] or record['placeholder_gap'] for group in groups for record in group['records']):
        result['draft'] = True
        result['approved'] = False
        result['approval_reason'] = 'Publication authoring gaps remain; architecture approval does not approve incomplete publication content.'
    return result
