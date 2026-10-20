# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Select advisory candidates from packaged metadata and opt-in local knowledge.

Usage: hint.py --goal 'assess architecture security' [--goal 'track remediation']
[--domain security] [--phase assessment] [--limit 3]. Inputs are structured
English phrases supplied by the active provider, not unrestricted translation.
JSON output exposes lexical ranking and gaps; no workflow or provider is run.
"""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

# Avoid import-cache writes even when invoked directly in an installed library.
sys.dont_write_bytecode = True
from scenario_demo import load_catalog

CATALOG = Path(__file__).with_name('scenarios.json')
_STOP = {'a', 'an', 'and', 'as', 'at', 'be', 'by', 'for', 'from', 'i', 'in',
         'is', 'it', 'my', 'need', 'of', 'on', 'or', 'our', 'please', 'the',
         'to', 'want', 'with', 'work', 'project'}
_FORMS = {'assessment': 'assess', 'assessing': 'assess', 'reviewing': 'review',
          'remediation': 'remediate', 'remediating': 'remediate', 'findings': 'finding',
          'controls': 'control', 'requirements': 'requirement', 'suppliers': 'supplier',
          'architectural': 'architecture', 'vulnerabilities': 'vulnerability'}


def _tokens(text):
    return {_FORMS.get(t, t) for t in re.findall(r'[a-z0-9]+', text.lower())
            if t not in _STOP}


def _validate_query(goals, domains, phases, limit, entries):
    for values, maximum, name in ((goals, 8, 'goals'), (domains, 8, 'domains'),
                                   (phases, 8, 'phases')):
        if (not isinstance(values, (list, tuple)) or len(values) > maximum
                or any(not isinstance(v, str) or not v.strip() or len(v) > 300 for v in values)
                or len(values) != len(set(values))):
            raise ValueError(f'Invalid {name}: supply unique bounded English strings')
    if not goals or type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError('Provide 1–8 goals and limit 1–10')
    for values, field in ((domains, 'domains'), (phases, 'phases')):
        available = {v for e in entries for v in e['discovery'][field]}
        if not set(values) <= available:
            raise ValueError(f'Unknown {field} filter')


def _rank(entries, goals, domains, phases, limit):
    candidates = []
    for entry in entries:
        discovery = entry['discovery']
        if domains and not set(domains).intersection(discovery['domains']):
            continue
        if phases and not set(phases).intersection(discovery['phases']):
            continue
        primary = _tokens(' '.join(discovery['goals']))
        secondary = _tokens(' '.join(discovery['output_kinds'] + discovery['domains']))
        matches = []
        score = 0
        for goal in goals:
            tokens = _tokens(goal)
            overlap = tokens & primary
            # At least two goal terms avoid broad domain words forcing unrelated matches.
            minimum = min(2, len(tokens))
            if not tokens or len(overlap) < minimum:
                continue
            points = 8 * len(overlap) + 2 * len(tokens & secondary)
            score += points
            matches.append({'goal': goal, 'matched_terms': sorted(overlap),
                            'field': 'discovery.goals', 'points': points})
        if not matches:
            continue
        candidates.append({'id': entry['id'], 'title': entry['title'], 'guide': entry['guide'],
                           'score': score, 'reasons': matches,
                           'prerequisites': discovery['prerequisites'],
                           'input_kinds': discovery['input_kinds'],
                           'output_kinds': discovery['output_kinds'],
                           'applicability_limits': discovery['applicability_limits']})
    return sorted(candidates, key=lambda c: (-c['score'], c['id']))[:limit]


def _knowledge_candidates(goals, libraries, allowed, scope, confidentiality, contexts, as_of):
    if (allowed is not True or scope not in {'personal', 'engagement', 'organisation'} or
            not isinstance(libraries, (list, tuple)) or not 1 <= len(libraries) <= 8):
        raise ValueError('Explicit bounded libraries, read/provider disclosure permission and scope required')
    roots = [str(Path(root).absolute()) for root in libraries]
    if len(set(roots)) != len(roots):
        raise ValueError('Duplicate selected knowledge library')
    if not isinstance(as_of, str):
        raise ValueError('Require an ISO as-of date')
    today = date.fromisoformat(as_of)
    # Load only the installed sibling tooling, never a user-provided module path.
    tools = str(Path(__file__).resolve().parent.parent / 'tools')
    if tools not in sys.path:
        sys.path.insert(0, tools)
    import knowledge
    knowledge._access({'confidentiality': 'public', 'applicability': {'contexts': []}}, confidentiality, contexts)
    excluded = dict(confidentiality=0, applicability=0, superseded=0, stale=0, no_lexical_match=0)
    candidates = []
    eligible = {}
    for index, root in enumerate(libraries):
        records = knowledge.read_records(root, read_requested=True)
        latest = {}
        for record in records:
            latest[record['id']] = max(latest.get(record['id'], 0), record['version'])
        for record in records:
            reason = knowledge._access(record, confidentiality, contexts)
            if reason:
                excluded[reason] += 1
                continue
            if record['version'] != latest[record['id']]:
                excluded['superseded'] += 1
                continue
            due = record.get('review_due')
            if ((today - date.fromisoformat(record['updated'])).days > 365 or
                    due is not None and date.fromisoformat(due) < today):
                excluded['stale'] += 1
                continue
            key = f"knowledge:{index}:{record['id']}:v{record['version']}"
            eligible.setdefault(record['id'], []).append(key)
            text = ' '.join(record['applicability']['contexts'] + record['observations'] +
                            record['interpretation'] + record['recommendations'])
            if record['scenario']:
                text += ' ' + ' '.join(step['purpose'] for step in record['scenario']['steps'])
            tokens = _tokens(text)
            reasons = []
            for goal in goals:
                query = _tokens(goal)
                overlap = query & tokens
                if query and len(overlap) >= min(2, len(query)):
                    reasons.append(dict(goal=goal, matched_terms=sorted(overlap),
                                        field='knowledge.content', points=8 * len(overlap)))
            if not reasons:
                excluded['no_lexical_match'] += 1
                continue
            warnings = [f"Evidence availability {record['evidence_availability']}; reported, not revalidated.",
                        f"Review {record['review']['status']}; authority NOT_VERIFIED."]
            if record.get('conflicts_with'):
                warnings.append('Declared conflicts require operator resolution; do not blend procedures.')
            candidates.append(dict(id=record['id'], title=record['id'].replace('-', ' '),
                source_type='knowledge', source_key=key, library_index=index,
                library=str(Path(root).absolute()), scope=scope, version=record['version'],
                record_type=record['record_type'], confidentiality=record['confidentiality'],
                reliability=record.get('reliability', 'NOT_RECORDED'), provenance=record['provenance'],
                evidence_availability=record['evidence_availability'], review=record['review'],
                conflicts_with=record.get('conflicts_with', []), warnings=warnings,
                score=sum(r['points'] for r in reasons), reasons=reasons,
                prerequisites=record['applicability']['preconditions'],
                applicability_limits=record['applicability']['exclusions'] + record['limitations']))
    conflicts = [dict(id=identity, sources=sources, reason='Duplicate identity across permitted libraries; no precedence implied.')
                 for identity, sources in sorted(eligible.items()) if len(sources) > 1]
    for candidate in candidates:
        if len(eligible[candidate['id']]) > 1:
            candidate['warnings'].append('Conflicting duplicate identity across selected libraries; keep sources distinct.')
    return candidates, dict(scope=scope, excluded=excluded, conflicts=conflicts,
        evidence='Availability and review declarations are not independently verified.',
        permissions='Explicit roots/classes/contexts permit active-provider disclosure, not sharing or approval.')


def select_candidates(goals, *, domains=(), phases=(), limit=3, knowledge_libraries=(),
                      allow_knowledge=False, knowledge_scope=None, confidentiality=(),
                      contexts=(), as_of=None):
    """Return bounded lexical candidates from the strictly validated packaged catalogue.

    Args:
        goals: One to eight unique structured English goal strings, up to 300 characters each.
        domains: Optional exact domain filters; any supplied domain may match.
        phases: Optional exact phase filters; any supplied phase may match.
        limit: Integer maximum result count, from one through ten.
        knowledge_libraries: Explicit existing local libraries; default none, never discovered.
        allow_knowledge: Explicit read and active-provider disclosure permission.
        knowledge_scope: Declared personal, engagement or organisation scope; not authority.
        confidentiality: Explicit permitted classes for selected knowledge.
        contexts: Exact applicability contexts, matched case-insensitively.
        as_of: Optional ISO date for stale assessment; defaults to local current date.
    Returns:
        JSON-compatible advisory dictionary with deterministic candidates, reasons and uncovered goals.
        Scores are lexical ranking points, never probabilities or approval judgments. No files are written.
    Raises:
        ValueError: Invalid query, metadata or packaged workflow registry; no fallback is attempted.
    """
    entries = load_catalog(CATALOG, require_discovery=True)
    _validate_query(goals, domains, phases, limit, entries)
    candidates = _rank(entries, goals, domains, phases, limit)
    knowledge_result = None
    if knowledge_libraries:
        if domains or phases:
            raise ValueError('Domain/phase filters are maintained-catalogue only; use explicit contexts for knowledge')
        additional, knowledge_result = _knowledge_candidates(goals, knowledge_libraries,
            allow_knowledge, knowledge_scope, confidentiality, contexts, as_of or date.today().isoformat())
        for candidate in candidates:
            candidate['source_type'] = 'maintained-scenario'
            candidate['source_key'] = 'maintained:' + candidate['id']
        candidates = sorted(candidates + additional, key=lambda c: (-c['score'], c.get('source_key', c['id'])))[:limit]
    elif allow_knowledge or knowledge_scope or confidentiality or contexts or as_of:
        raise ValueError('Knowledge options require explicitly selected libraries')
    covered = {r['goal'] for c in candidates for r in c['reasons']}
    unmatched = [g for g in goals if g not in covered]
    status = 'NO_MATCH' if not candidates else ('PARTIAL_MATCH' if unmatched else 'MATCH')
    result = {'schema_version': 1, 'status': status, 'experimental': True,
            'interpretation': 'Active provider supplies structured English goals; no translation executed.',
            'ranking': 'Lexical points; not confidence, semantic coverage or approval.',
            'candidates': candidates, 'unmatched_goals': unmatched,
            'limits': ['Candidate metadata is selected, not proof that procedure content was read.',
                       'Read selected instructions with demo.py describe ID before adapting steps.',
                       'No implicit project/history reads or provider/workflow execution occurred.']}
    if knowledge_result is not None:
        result['knowledge'] = knowledge_result
        result['limits'].append('Read exact selected knowledge with knowledge.py describe after permission; current project evidence takes precedence.')
    return result


def main(argv=None):
    """Print selection JSON for argv; return zero on a valid query or two on error.

    Args:
        argv: Optional CLI arguments; defaults to process arguments. No catalogue path option is exposed.
    Returns:
        Integer exit code. Valid queries, including no match, return zero. Invalid inputs return two.
        Explicit knowledge options additionally permit bounded library reads; no provider is invoked.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--goal', action='append', required=True)
    parser.add_argument('--domain', action='append', default=[])
    parser.add_argument('--phase', action='append', default=[])
    parser.add_argument('--limit', type=int, default=3)
    parser.add_argument('--knowledge-library', action='append', default=[])
    parser.add_argument('--allow-knowledge', action='store_true')
    parser.add_argument('--knowledge-scope', choices=['personal', 'engagement', 'organisation'])
    parser.add_argument('--confidentiality', action='append', default=[])
    parser.add_argument('--context', action='append', default=[])
    parser.add_argument('--as-of')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(select_candidates(args.goal, domains=args.domain, phases=args.phase,
                                           limit=args.limit, knowledge_libraries=args.knowledge_library,
                                           allow_knowledge=args.allow_knowledge, knowledge_scope=args.knowledge_scope,
                                           confidentiality=args.confidentiality, contexts=args.context,
                                           as_of=args.as_of), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'schema_version': 1, 'status': 'ERROR', 'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
