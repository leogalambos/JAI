# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Explicit local knowledge authoring and immutable filesystem boundary regressions."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def tool():
    path = ROOT / '.ai/runtime/tools/knowledge.py'
    spec = importlib.util.spec_from_file_location('knowledge', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def record(kind='experience'):
    return dict(schema_version=1, id='acme-lesson', record_type=kind, version=1,
                owner='Alice', created='2026-10-20', updated='2026-10-20', language='en',
                confidentiality='internal', applicability=dict(contexts=['Architecture review'],
                preconditions=[], exclusions=['Not authority approval']), provenance=[],
                evidence_availability='NOT_CHECKED', review=dict(status='AI_EDITORIAL',
                reported_by='Alice', authority_claim='', authority_verification='NOT_VERIFIED'),
                limitations=['Fictional example; evidence not verified'], supersedes=None,
                observations=['The draft lacked ownership'], interpretation=['Ownership matters'],
                recommendations=['Name an owner'], scenario=None)


def setup(tmp_path):
    source = tmp_path / 'source'
    library = tmp_path / 'library'
    source.mkdir()
    library.mkdir()
    (source / 'draft.json').write_text(json.dumps(record()))
    return source, library


def test_explicit_prepare_preview_save_preserves_immutable_record(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    prepared = mod.prepare(library, source, 'draft.json', [], capture_requested=True)
    digest = prepared['digest']
    preview = mod.preview(library, 'acme-lesson', 1, digest, source_root=source)
    assert preview['envelope']['record']['observations'] == record()['observations']
    assert preview['envelope']['destination'] == str(library / 'records/acme-lesson/v1.json')
    saved = mod.save(library, 'acme-lesson', 1, digest, digest, source_root=source, user_reviewed=True)
    assert json.loads(Path(saved['destination']).read_text()) == record()
    with pytest.raises(ValueError, match='exists'):
        mod.save(library, 'acme-lesson', 1, digest, digest, source_root=source, user_reviewed=True)
    assert json.loads(Path(saved['destination']).read_text()) == record()


@pytest.mark.parametrize('change', [
    {'version': True}, {'version': 0}, {'version': 1000000}, {'id': '../escape'},
    {'extra': 'unknown'}, {'language': 'cs'}, {'created': '2026-02-30'},
    {'updated': '2025-01-01'}, {'supersedes': 1}, {'confidentiality': 'secret'},
])
def test_schema_and_semantic_errors_are_rejected_read_only(tmp_path, change):
    mod = tool()
    source, library = setup(tmp_path)
    value = record()
    value.update(change)
    (source / 'draft.json').write_text(json.dumps(value))
    with pytest.raises(ValueError):
        mod.validate(source, 'draft.json')
    assert list(library.iterdir()) == []


@pytest.mark.parametrize('kind', ['custom-scenario', 'organisational-procedure'])
def test_scenarios_require_supported_paired_commands(tmp_path, kind):
    mod = tool()
    source, _ = setup(tmp_path)
    value = record(kind)
    value['scenario'] = dict(inputs=['Architecture description'], steps=[dict(
        purpose='Understand scope', claude='/analyse .', codex='$workflow-analyse .',
        inspect='Identify missing evidence')])
    path = source / 'draft.json'
    path.write_text(json.dumps(value))
    assert mod.validate(source, 'draft.json')['record_type'] == kind
    for command, codex in [('/invented .', '$workflow-invented .'),
                            ('/analyse .', '$workflow-review .')]:
        value['scenario']['steps'][0].update(claude=command, codex=codex)
        path.write_text(json.dumps(value))
        with pytest.raises(ValueError, match='commands'):
            mod.validate(source, 'draft.json')


def test_provenance_requires_exact_allowlist_and_never_copies_contents(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    value = record()
    value['provenance'] = [dict(path='notes.md', availability='AVAILABLE', purpose='Reported lesson source')]
    evidence = 'Confidential contents must not be copied by capture.'
    (source / 'notes.md').write_text(evidence)
    (source / 'draft.json').write_text(json.dumps(value))
    for allowed in [[], ['other.md'], ['notes.md', 'notes.md']]:
        with pytest.raises(ValueError):
            mod.prepare(library, source, 'draft.json', allowed, capture_requested=True)
    prepared = mod.prepare(library, source, 'draft.json', ['notes.md'], capture_requested=True)
    assert evidence not in json.dumps(prepared)
    (source / 'notes.md').unlink()
    with pytest.raises(ValueError, match='missing'):
        mod.save(library, value['id'], 1, prepared['digest'], prepared['digest'], source_root=source, allowed=['notes.md'], user_reviewed=True)
    assert not (library / 'records').exists()


@pytest.mark.parametrize('path', ['../draft.json', '/tmp/draft.json',
                                  'inputs/../draft.json', 'draft\\file.json'])
def test_traversal_fails_before_writes(tmp_path, path):
    source, library = setup(tmp_path)
    with pytest.raises((ValueError, OSError)):
        tool().prepare(library, source, path, capture_requested=True)
    assert list(library.iterdir()) == []


def test_protected_components_are_rejected_as_data_without_creating_them(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    for component in sorted(mod._PROTECTED):
        with pytest.raises(ValueError, match='Protected'):
            mod.prepare(library, source, component + '/draft.json', capture_requested=True)
    assert list(library.iterdir()) == []


def test_symlink_sources_destinations_and_ancestor_components_fail(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    (source / 'linked.json').symlink_to(source / 'draft.json')
    with pytest.raises(OSError):
        mod.validate(source, 'linked.json')
    link = tmp_path / 'linked-root'
    link.symlink_to(library, target_is_directory=True)
    with pytest.raises(OSError):
        mod.prepare(link, source, 'draft.json', capture_requested=True)
    (library / 'drafts').symlink_to(source, target_is_directory=True)
    with pytest.raises(OSError):
        mod.prepare(library, source, 'draft.json', capture_requested=True)
    assert sorted(p.name for p in source.iterdir()) == ['draft.json', 'linked.json']


def test_fifo_and_oversized_files_fail_without_blocking(tmp_path):
    import os
    import subprocess
    source, _ = setup(tmp_path)
    os.mkfifo(source / 'fifo.json')
    for name in ['fifo.json', 'large.json']:
        if name == 'large.json':
            (source / name).write_bytes(b' ' * (256 * 1024 + 1))
        result = subprocess.run([sys.executable, str(ROOT / '.ai/runtime/tools/knowledge.py'),
                                 'validate', '--source-root', str(source), '--draft', name],
                                capture_output=True, text=True, timeout=5)
        assert result.returncode == 2 and 'regular JSON' in result.stdout


def test_capture_and_save_intent_and_digest_are_mandatory(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    with pytest.raises(ValueError, match='request'):
        mod.prepare(library, source, 'draft.json')
    assert list(library.iterdir()) == []
    prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
    digest = prepared['digest']
    for reviewed, flag in [(digest, False), ('0' * 64, True)]:
        with pytest.raises(ValueError, match='reviewed'):
            mod.save(library, 'acme-lesson', 1, digest, reviewed, source_root=source, user_reviewed=flag)
    assert not (library / 'records').exists()


def test_corrected_candidates_and_append_only_versions(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    first = mod.prepare(library, source, 'draft.json', capture_requested=True)
    value = record()
    value['recommendations'] = ['Use a named accountable owner and record evidence gaps']
    (source / 'draft.json').write_text(json.dumps(value))
    revised = mod.prepare(library, source, 'draft.json', capture_requested=True)
    assert first['digest'] != revised['digest']
    assert len(list((library / 'drafts').iterdir())) == 2
    destination = mod.save(library, value['id'], 1, revised['digest'], revised['digest'], source_root=source, user_reviewed=True)['destination']
    before = Path(destination).read_bytes()
    with pytest.raises(ValueError, match='exists'):
        mod.save(library, value['id'], 1, first['digest'], first['digest'], source_root=source, user_reviewed=True)
    value.update(version=2, supersedes=1, updated='2026-10-21')
    (source / 'draft.json').write_text(json.dumps(value))
    second = mod.prepare(library, source, 'draft.json', capture_requested=True)
    mod.save(library, value['id'], 2, second['digest'], second['digest'], source_root=source, user_reviewed=True)
    assert Path(destination).read_bytes() == before
    value.update(version=3, supersedes=2, owner='Bob')
    (source / 'draft.json').write_text(json.dumps(value))
    with pytest.raises(ValueError, match='identity metadata'):
        mod.prepare(library, source, 'draft.json', capture_requested=True)


def test_tampered_candidate_and_forged_destination_are_rejected(tmp_path):
    import hashlib
    mod = tool()
    source, library = setup(tmp_path)
    prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
    digest = prepared['digest']
    path = library / 'drafts' / f'acme-lesson-v1-{digest}.json'
    value = json.loads(path.read_text())
    value['record']['recommendations'] = ['Changed after preview']
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match='changed'):
        mod.save(library, 'acme-lesson', 1, digest, digest, source_root=source, user_reviewed=True)
    value['destination'] = str(tmp_path / 'outside.json')
    raw = mod._canonical(value)
    forged = hashlib.sha256(raw).hexdigest()
    (library / 'drafts' / f'acme-lesson-v1-{forged}.json').write_bytes(raw)
    with pytest.raises(ValueError, match='destination'):
        mod.preview(library, 'acme-lesson', 1, forged, source_root=source)
    assert not (tmp_path / 'outside.json').exists()


def test_concurrent_saves_publish_exactly_one_complete_record(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    mod = tool()
    source, library = setup(tmp_path)
    prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
    digest = prepared['digest']

    def attempt():
        try:
            return mod.save(library, 'acme-lesson', 1, digest, digest, source_root=source, user_reviewed=True)['status']
        except ValueError:
            return 'REFUSED'

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: attempt(), range(4)))
    assert results.count('SAVED_NOT_APPROVAL') == 1
    assert results.count('REFUSED') == 3
    assert json.loads((library / 'records/acme-lesson/v1.json').read_text()) == record()
    assert not list(library.rglob('.pending-*'))


def test_installed_cli_validate_prepare_preview_save_without_docs(tmp_path):
    import shutil
    import subprocess
    source, library = setup(tmp_path)
    house = tmp_path / 'house'
    (house / 'tools').mkdir(parents=True)
    shutil.copy2(ROOT / '.ai/runtime/tools/knowledge.py', house / 'tools/knowledge.py')
    shutil.copytree(ROOT / '.ai/runtime/knowledge', house / 'knowledge')
    shutil.copytree(ROOT / '.ai/commands', house / 'commands')
    script = house / 'tools/knowledge.py'

    def run(*args):
        result = subprocess.run([sys.executable, str(script), *args], cwd=tmp_path,
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
        return json.loads(result.stdout)

    value = record('custom-scenario')
    value['scenario'] = dict(inputs=['Requirements'], steps=[dict(purpose='Read inputs',
        claude='/analyse .', codex='$workflow-analyse .', inspect='Missing evidence')])
    (source / 'draft.json').write_text(json.dumps(value))
    assert run('validate', '--source-root', str(source), '--draft', 'draft.json')['status'] == 'VALID_NOT_APPROVED'
    prepared = run('prepare', '--library', str(library), '--source-root', str(source),
                   '--draft', 'draft.json', '--capture-requested')
    digest = prepared['digest']
    selected = ['--source-root', str(source), '--library', str(library), '--id', 'acme-lesson', '--version', '1', '--draft-digest', digest]
    assert run('preview', *selected)['status'] == 'PREVIEW_NOT_APPROVAL'
    assert run('save', *selected, '--reviewed-digest', digest, '--user-reviewed')['status'] == 'SAVED_NOT_APPROVAL'
    assert not (house / 'docs').exists()
    result = subprocess.run([sys.executable, str(script), 'prepare', '--library', str(house),
                             '--source-root', str(source), '--draft', 'draft.json', '--capture-requested'],
                            capture_output=True, text=True)
    assert result.returncode == 2 and 'Installed runtime' in result.stdout


def test_previous_version_filename_must_match_content(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    first = mod.prepare(library, source, 'draft.json', capture_requested=True)
    mod.save(library, 'acme-lesson', 1, first['digest'], first['digest'], source_root=source, user_reviewed=True)
    previous = library / 'records/acme-lesson/v1.json'
    value = record()
    value.update(version=5, supersedes=4)
    previous.write_text(json.dumps(value))
    value.update(version=2, supersedes=1)
    (source / 'draft.json').write_text(json.dumps(value))
    with pytest.raises(ValueError, match='filename'):
        mod.prepare(library, source, 'draft.json', capture_requested=True)


def test_package_library_and_publication_subtrees_are_rejected_before_writes(tmp_path):
    mod = tool()
    source, _ = setup(tmp_path)
    for path in [ROOT, ROOT / 'docs', ROOT / '.ai/runtime']:
        with pytest.raises(ValueError, match='Package trees'):
            mod.prepare(path, source, 'draft.json', capture_requested=True)


def test_revalidation_rejects_forged_authority_and_missing_sources(tmp_path):
    import hashlib
    mod = tool()
    source, library = setup(tmp_path)
    prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
    envelope = copy.deepcopy(prepared['envelope'])
    envelope['record']['review']['authority_verification'] = 'VERIFIED'
    raw = mod._canonical(envelope)
    digest = hashlib.sha256(raw).hexdigest()
    (library / 'drafts' / f'acme-lesson-v1-{digest}.json').write_bytes(raw)
    with pytest.raises(ValueError, match='record'):
        mod.save(library, 'acme-lesson', 1, digest, digest, source_root=source, user_reviewed=True)
    assert not (library / 'records').exists()


def test_validation_byte_boundary_and_duplicate_properties(tmp_path):
    mod = tool()
    source, _ = setup(tmp_path)
    value = json.dumps(record()).encode()
    (source / 'draft.json').write_bytes(value + b' ' * (mod.MAX_BYTES - len(value)))
    assert mod.validate(source, 'draft.json')['id'] == 'acme-lesson'
    (source / 'draft.json').write_text('{"id":"one","id":"two"}')
    with pytest.raises(ValueError, match='Duplicate'):
        mod.validate(source, 'draft.json')


def test_cli_errors_and_no_match_selector_do_not_implicitly_retrieve_records(tmp_path):
    import subprocess
    mod = tool()
    assert mod.main(['prepare', '--library', str(tmp_path), '--source-root', str(tmp_path),
                     '--draft', 'absent.json']) == 2
    source, library = setup(tmp_path)
    prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
    mod.save(library, 'acme-lesson', 1, prepared['digest'], prepared['digest'], source_root=source, user_reviewed=True)
    result = subprocess.run([sys.executable, str(ROOT / '.ai/runtime/demo/hint.py'),
                             '--goal', 'acme-lesson'], cwd=library, capture_output=True, text=True)
    assert result.returncode == 0 and json.loads(result.stdout)['status'] == 'NO_MATCH'


def test_empty_roots_are_not_implicit_current_directory(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    with pytest.raises(ValueError, match='Unsafe'):
        mod.validate('', 'draft.json')
    with pytest.raises(ValueError, match='Unsafe'):
        mod.prepare('', source, 'draft.json', capture_requested=True)
    assert list(library.iterdir()) == []


def test_unavailable_safe_platform_primitives_fail_closed(tmp_path, monkeypatch):
    mod = tool()
    source, library = setup(tmp_path)
    monkeypatch.setattr(mod.os, 'supports_dir_fd', set())
    with pytest.raises(ValueError, match='POSIX'):
        mod.prepare(library, source, 'draft.json', capture_requested=True)
    assert list(library.iterdir()) == []


def test_capture_contracts_preserve_explicit_intent_and_no_retrieval():
    for name in ['hint', 'guide']:
        text = (ROOT / '.ai/commands' / (name + '.md')).read_text()
        assert 'read-only' in text and 'preview' in text and 'save' in text
        assert 'explicit' in text and 'approval' in text
        assert 'visible' in text
        continuation = ('without a separate save instruction' if name == 'guide'
                        else 'without asking for another save command')
        assert continuation in text
    hint = (ROOT / '.ai/commands/hint.md').read_text()
    assert '--save-requested' in hint and '--prepare-requested' in hint and '--user-reviewed' in hint
    assert 'Stored records enter hint selection' in hint
    assert '--allow-knowledge' in hint and 'never enter demo setup automatically' in hint
    assert 'never ask for JSON' in hint and 'before writing' in hint


def test_forged_scope_never_inspects_nonselected_source_root(tmp_path, monkeypatch):
    import hashlib
    mod = tool()
    source, library = setup(tmp_path)
    prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
    envelope = copy.deepcopy(prepared['envelope'])
    envelope['source_root'] = str(tmp_path / 'not-authorized')
    raw = mod._canonical(envelope)
    digest = hashlib.sha256(raw).hexdigest()
    (library / 'drafts' / f'acme-lesson-v1-{digest}.json').write_bytes(raw)
    calls = []
    original = mod._scope

    def track_scope(*args):
        calls.append(args)
        return original(*args)

    monkeypatch.setattr(mod, '_scope', track_scope)
    with pytest.raises(ValueError, match='caller selection'):
        mod.preview(library, 'acme-lesson', 1, digest, source_root=source)
    with pytest.raises(ValueError, match='caller selection'):
        mod.save(library, 'acme-lesson', 1, digest, digest, source_root=source, user_reviewed=True)
    assert calls == []


@pytest.mark.parametrize('target', ['root', 'drafts', 'records'])
def test_group_writable_library_components_are_refused(tmp_path, target):
    mod = tool()
    source, library = setup(tmp_path)
    if target == 'root':
        library.chmod(0o777)
    elif target == 'drafts':
        (library / 'drafts').mkdir(mode=0o777)
        (library / 'drafts').chmod(0o777)
    else:
        prepared = mod.prepare(library, source, 'draft.json', capture_requested=True)
        (library / 'records').mkdir(mode=0o777)
        (library / 'records').chmod(0o777)
        with pytest.raises(ValueError, match='ownership'):
            mod.save(library, 'acme-lesson', 1, prepared['digest'], prepared['digest'],
                     source_root=source, user_reviewed=True)
        return
    with pytest.raises(ValueError, match='ownership'):
        mod.prepare(library, source, 'draft.json', capture_requested=True)


def test_prepared_source_allowlist_cannot_be_changed_implicitly(tmp_path):
    mod = tool()
    source, library = setup(tmp_path)
    value = record()
    value['provenance'] = [dict(path='missing.md', availability='UNAVAILABLE', purpose='Unavailable original')]
    (source / 'draft.json').write_text(json.dumps(value))
    prepared = mod.prepare(library, source, 'draft.json', ['missing.md'], capture_requested=True)
    with pytest.raises(ValueError, match='caller selection'):
        mod.preview(library, 'acme-lesson', 1, prepared['digest'], source_root=source)
    assert mod.preview(library, 'acme-lesson', 1, prepared['digest'], source_root=source,
                       allowed=['missing.md'])['status'] == 'PREVIEW_NOT_APPROVAL'
