# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Manage explicitly selected local knowledge without implicit history or authority.

Usage: knowledge.py --help. Inputs are bounded JSON and explicit local roots.
Capture, prepare, save, export, delete and restore write only with explicit intent.
JSON diagnostics use exit 0 for success, 2 for invalid input or unavailable support.
No evidence contents, historical directories, providers or network are accessed.
"""
import argparse
from contextlib import contextmanager
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid

sys.dont_write_bytecode = True
MAX_BYTES = 256 * 1024
SCHEMA = Path(__file__).resolve().parent.parent / 'knowledge/record.schema.json'
_RUNTIME = Path(__file__).resolve().parent.parent
_COMMANDS = (_RUNTIME.parent if _RUNTIME.name == 'runtime' and _RUNTIME.parent.name == '.ai'
             else _RUNTIME) / 'commands'
_PROTECTED = {'.fabric', '.findings', '.git', '.npmrc', '.pypirc', 'id_rsa',
              'id_ed25519', 'settings-security.xml'}


def _parts(value):
    if (not isinstance(value, (str, Path)) or not str(value).strip() or '\\' in str(value)
            or '..' in str(value).split('/') or str(value).startswith('~')):
        raise ValueError('Unsafe path')
    path = Path(value)
    parts = path.parts
    if len(parts) > 64 or any(p in _PROTECTED or p == '.env' or p.startswith('.env.')
                              for p in parts):
        raise ValueError('Protected or excessive path')
    return path, parts


def _relative(value):
    path, parts = _parts(value)
    if path.is_absolute() or not parts or str(path) != str(value):
        raise ValueError('Require normalised root-relative path')
    return parts


@contextmanager
def _directory(value, *, library=False):
    if not all(hasattr(os, key) for key in ('O_NOFOLLOW', 'O_DIRECTORY', 'O_NONBLOCK')):
        raise ValueError('Safe POSIX directory primitives unavailable')
    if (not hasattr(os, 'getuid') or not {os.open, os.mkdir, os.stat, os.link, os.unlink}
            <= os.supports_dir_fd):
        raise ValueError('Safe POSIX descriptor-relative operations unavailable')
    path, _ = _parts(value)
    absolute = Path(os.path.abspath(path))
    if absolute == Path('/'):
        raise ValueError('Filesystem root is not a knowledge root')
    # Package trees and public release outputs cannot become personal libraries.
    runtime = Path(__file__).resolve().parent.parent
    if library:
        if runtime.name == 'runtime' and runtime.parent.name == '.ai':
            package = runtime.parent.parent
            private = package / 'INBOX'
            if (absolute == package or package in absolute.parents) and not (absolute == private or private in absolute.parents):
                raise ValueError('Package trees cannot persist private knowledge; choose an external or private excluded root')
        elif absolute == runtime or runtime in absolute.parents:
            raise ValueError('Installed runtime cannot persist private knowledge')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in absolute.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        if library:
            _owned(os.fstat(fd))
        yield fd, absolute
    finally:
        os.close(fd)


def _owned(info):
    if info.st_uid != os.getuid() or info.st_mode & 0o022:
        raise ValueError('Library entries require current ownership and no group/other write permission')


@contextmanager
def _child_dir(root_fd, parts, create=False, secure=False):
    fd = os.dup(root_fd)
    try:
        for part in parts:
            if create:
                try:
                    os.mkdir(part, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
            if secure:
                _owned(os.fstat(fd))
        yield fd
    finally:
        os.close(fd)


def _json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON property')
            result[key] = value
        return result
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))


def _read(fd, parts, secure=False):
    with _child_dir(fd, parts[:-1], secure=secure) as parent:
        item = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        try:
            info = os.fstat(item)
            if secure:
                _owned(info)
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise ValueError('Require bounded regular JSON file')
            data = b''
            while len(data) <= MAX_BYTES:
                chunk = os.read(item, min(65536, MAX_BYTES + 1 - len(data)))
                if not chunk:
                    break
                data += chunk
            if len(data) > MAX_BYTES:
                raise ValueError('JSON file exceeds byte limit')
            return data
        finally:
            os.close(item)


def _canonical(value):
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False) + '\n').encode('utf-8')
    if len(raw) > MAX_BYTES:
        raise ValueError('JSON envelope exceeds byte limit')
    return raw


def _identity(record_id, version, digest=None):
    if not isinstance(record_id, str) or not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', record_id) or len(record_id) > 80:
        raise ValueError('Invalid record id')
    if type(version) is not int or not 1 <= version <= 999999:
        raise ValueError('Invalid record version')
    if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest)):
        raise ValueError('Invalid draft digest')


def _validate_record(record):
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise ValueError('jsonschema is required for knowledge validation') from exc
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    if errors:
        raise ValueError('Invalid knowledge record: ' + errors[0].message)
    _identity(record['id'], record['version'])
    if date.fromisoformat(record['updated']) < date.fromisoformat(record['created']):
        raise ValueError('Updated date precedes created date')
    expected = None if record['version'] == 1 else record['version'] - 1
    if record['supersedes'] != expected or isinstance(record['supersedes'], bool):
        raise ValueError('Supersedes must name the preceding version')
    if record['scenario']:
        commands = {p.stem for p in _COMMANDS.glob('*.md')}
        if not commands:
            raise ValueError('Packaged command contracts unavailable')
        for step in record['scenario']['steps']:
            claude = re.fullmatch(r'/([a-z-]+)((?:[^\S\r\n][^\r\n]*)?)', step['claude'])
            codex = re.fullmatch(r'\$workflow-([a-z-]+)((?:[^\S\r\n][^\r\n]*)?)', step['codex'])
            if not claude or not codex or claude.groups() != codex.groups() or claude[1] not in commands:
                raise ValueError('Scenario commands must pair supported workflow contracts')
    for source in record['provenance']:
        _relative(source['path'])
    return record


def _scope(record, source_root, allowed):
    if len(allowed) > 32 or len(set(allowed)) != len(allowed):
        raise ValueError('Allowlist must be unique and bounded')
    for name in allowed:
        _relative(name)
    refs = record['provenance']
    if len({r['path'] for r in refs}) != len(refs) or {r['path'] for r in refs} != set(allowed):
        raise ValueError('Every provenance path requires an exact explicit allowlist entry')
    with _directory(source_root) as (fd, absolute):
        for source in refs:
            parts = _relative(source['path'])
            try:
                with _child_dir(fd, parts[:-1]) as parent:
                    info = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
                if not stat.S_ISREG(info.st_mode):
                    raise ValueError('Provenance must refer to a regular non-symlink file')
                exists = True
            except FileNotFoundError:
                exists = False
            if source['availability'] == 'AVAILABLE' and not exists:
                raise ValueError('Claimed available provenance is missing')
            if source['availability'] == 'UNAVAILABLE' and exists:
                raise ValueError('Claimed unavailable provenance exists')
    return str(absolute)


def validate(source_root, draft, allowed=()):
    """Read and validate one selected draft and its exact reference allowlist.

    Args:
        source_root: Explicit existing permitted directory, never a discovered root.
        draft: Normalised root-relative JSON draft path, at most 256 KiB.
        allowed: Exact provenance paths permitted for metadata-only existence checks.
    Returns:
        Validated record dictionary. No evidence contents are read or files written.
    Raises:
        ValueError, OSError: Invalid schema, scope, unsafe path or unavailable file.
    """
    parts = _relative(draft)
    if not str(draft).endswith('.json'):
        raise ValueError('Draft must be JSON')
    with _directory(source_root) as (fd, _):
        record = _validate_record(_json(_read(fd, parts)))
    _scope(record, source_root, allowed)
    return record


def _sequence(fd, record):
    if record['version'] == 1:
        return
    previous_parts = ('records', record['id'], f"v{record['version'] - 1}.json")
    previous = _validate_record(_json(_read(fd, previous_parts, secure=True)))
    if previous['version'] != record['version'] - 1:
        raise ValueError('Previous record version does not match its filename')
    for key in ('id', 'record_type', 'owner', 'created'):
        if previous[key] != record[key]:
            raise ValueError('Immutable identity metadata changed across versions')
    if record['updated'] < previous['updated']:
        raise ValueError('Updated date regressed across versions')


def _write(fd, parts, raw):
    with _child_dir(fd, parts[:-1], create=True, secure=True) as parent:
        temporary = '.pending-' + uuid.uuid4().hex
        item = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                       0o600, dir_fd=parent)
        try:
            with os.fdopen(item, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, parts[-1], src_dir_fd=parent, dst_dir_fd=parent,
                        follow_symlinks=False)
            except FileExistsError as exc:
                raise ValueError('Target already exists; no overwrite permitted') from exc
            os.fsync(parent)
        finally:
            os.unlink(temporary, dir_fd=parent)


def prepare(library, source_root, draft, allowed=(), *, capture_requested=False):
    """Stage an explicitly requested immutable candidate and return its full preview.

    Args:
        library: Explicit existing local personal/engagement library directory.
        source_root: Explicit existing directory containing selected draft and references.
        draft: Root-relative selected JSON draft, not a conversation history.
        allowed: Exact permitted provenance paths; contents are never copied.
        capture_requested: Caller-declared explicit capture intent, required true.
    Returns:
        Full envelope and SHA-256 digest for user review; no final record is saved.
    Raises:
        ValueError, OSError: Invalid intent, draft, sequence, destination or duplicate candidate.
    """
    if capture_requested is not True:
        raise ValueError('Explicit capture request required')
    record = validate(source_root, draft, allowed)
    with _directory(library, library=True) as (fd, absolute):
        _sequence(fd, record)
        envelope = dict(schema_version=1, record=record, library=str(absolute),
                        destination=str(absolute / 'records' / record['id'] / f"v{record['version']}.json"),
                        source_root=_scope(record, source_root, allowed),
                        allowed_sources=list(allowed), authority_verification='NOT_VERIFIED')
        raw = _canonical(envelope)
        digest = hashlib.sha256(raw).hexdigest()
        _write(fd, ('drafts', f"{record['id']}-v{record['version']}-{digest}.json"), raw)
    return dict(status='PREPARED_NOT_SAVED', digest=digest, envelope=envelope,
                review='Inspect full content, destination and confidentiality before explicitly requesting save.')


def _preview(fd, absolute, record_id, version, digest, source_root, allowed):
    _identity(record_id, version, digest)
    raw = _read(fd, ('drafts', f'{record_id}-v{version}-{digest}.json'), secure=True)
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('Prepared content changed; prepare and review again')
    envelope = _json(raw)
    keys = {'schema_version', 'record', 'library', 'destination', 'source_root',
            'allowed_sources', 'authority_verification'}
    if not isinstance(envelope, dict) or set(envelope) != keys or type(envelope['schema_version']) is not int or envelope['schema_version'] != 1:
        raise ValueError('Invalid prepared envelope')
    record = _validate_record(envelope['record'])
    if record['id'] != record_id or record['version'] != version:
        raise ValueError('Prepared identity mismatch')
    destination = str(absolute / 'records' / record_id / f'v{version}.json')
    if envelope['library'] != str(absolute) or envelope['destination'] != destination or envelope['authority_verification'] != 'NOT_VERIFIED':
        raise ValueError('Prepared destination or authority boundary mismatch')
    stored_allowed = envelope['allowed_sources']
    if not isinstance(stored_allowed, list) or any(not isinstance(p, str) for p in stored_allowed):
        raise ValueError('Invalid prepared allowlist')
    selected_path, _ = _parts(source_root)
    if (str(Path(os.path.abspath(selected_path))) != envelope['source_root']
            or list(allowed) != stored_allowed):
        raise ValueError('Prepared source scope differs from explicit caller selection')
    if _scope(record, envelope['source_root'], allowed) != envelope['source_root']:
        raise ValueError('Prepared source root must be absolute and stable')
    _sequence(fd, record)
    return dict(status='PREVIEW_NOT_APPROVAL', digest=digest, envelope=envelope)


def preview(library, record_id, version, draft_digest, *, source_root, allowed=()):
    """Return exactly one validated prepared candidate without writing or approving it.

    Args:
        library: Explicit existing library used during preparation.
        record_id: Stable lowercase record ID.
        version: Positive integer final record version.
        draft_digest: Explicit SHA-256 candidate selector, never implicit latest.
        source_root: Explicit selected source root; stored data cannot grant access.
        allowed: Exact explicitly selected provenance allowlist, matched before access.
    Returns:
        Full untrusted record envelope and its digest; evidence contents remain unread.
    Raises:
        ValueError, OSError: Tampered envelope, changed source availability, invalid path or absent candidate.
    """
    with _directory(library, library=True) as (fd, absolute):
        return _preview(fd, absolute, record_id, version, draft_digest, source_root, allowed)


def save(library, record_id, version, draft_digest, reviewed_digest, *, source_root, allowed=(), user_reviewed=False, save_requested=False):
    """Persist one revalidated reviewed candidate atomically without replacing a version.

    Args:
        library: Explicit original library destination.
        record_id: Stable record ID from the selected preview.
        version: Positive integer final version from the selected preview.
        draft_digest: Explicit candidate digest used for preview.
        reviewed_digest: Exact digest the caller declares was reviewed.
        source_root: Explicit selected source root, checked before provenance access.
        allowed: Exact caller-selected provenance paths, not inferred from staged data.
        user_reviewed: Legacy explicit review/save declaration, never authority proof.
        save_requested: Explicit persistent user save intent, without claiming review.
    Returns:
        Destination and unverified authority status. Existing bytes are never replaced.
    Raises:
        ValueError, OSError: Missing intent, changed digest/scope, invalid record or existing version.
    """
    if (user_reviewed is not True and save_requested is not True) or reviewed_digest != draft_digest:
        raise ValueError('Explicit reviewed digest and user save request required')
    with _directory(library, library=True) as (fd, absolute), _exclusive(fd):
        result = _preview(fd, absolute, record_id, version, draft_digest, source_root, allowed)
        _admit(fd, [result['envelope']['record']])
        _write(fd, ('records', record_id, f'v{version}.json'), _canonical(result['envelope']['record']))
    return dict(status='SAVED_NOT_APPROVAL', destination=result['envelope']['destination'],
                authority_verification='NOT_VERIFIED')


def _bounded_names(fd, maximum):
    names = []
    with os.scandir(fd) as entries:
        for entry in entries:
            if len(names) >= maximum:
                raise ValueError('Selected directory exceeds entry limit')
            names.append(entry.name)
    return names


def _validate_history(records):
    versions = sorted(records, key=lambda record: record['version'])
    if [r['version'] for r in versions] != list(range(1, len(versions) + 1)):
        raise ValueError('Knowledge history requires every consecutive version starting at one')
    first = versions[0]
    previous = first
    for record in versions:
        if any(record[key] != first[key] for key in ('id', 'record_type', 'owner', 'created')):
            raise ValueError('Immutable knowledge identity changed across versions')
        if record['updated'] < previous['updated']:
            raise ValueError('Knowledge history update date regressed')
        previous = record
    return versions


def _record_versions(fd, record_id):
    _identity(record_id, 1)
    with _child_dir(fd, ('records', record_id), secure=True) as directory:
        names = _bounded_names(directory, 128)
        if not names or len(names) > 128:
            raise ValueError('Record version count must be 1–128')
        versions = []
        for name in sorted(names):
            match = re.fullmatch(r'v([1-9][0-9]*)\.json', name)
            if not match:
                raise ValueError('Unexpected entry in selected record')
            try:
                record = _validate_record(_json(_read(directory, (name,), secure=True)))
            except (ValueError, UnicodeError):
                raise ValueError('Invalid selected knowledge record') from None
            if record['id'] != record_id or record['version'] != int(match[1]):
                raise ValueError('Record identity does not match selected filename')
            versions.append(record)
        return _validate_history(versions)


@contextmanager
def _exclusive(fd):
    import fcntl
    fcntl.flock(fd, fcntl.LOCK_EX)
    try:
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)


def _read_records_fd(fd):
    try:
        with _child_dir(fd, ('records',), secure=True) as directory:
            names = _bounded_names(directory, 256)
    except FileNotFoundError:
        return []
    if len(names) > 256:
        raise ValueError('Selected library exceeds 256 record identities')
    records = []
    total_bytes = 0
    for record_id in sorted(names):
        versions = _record_versions(fd, record_id)
        total_bytes += sum(len(_canonical(record)) for record in versions)
        if total_bytes > 8 * 1024 * 1024:
            raise ValueError('Selected library exceeds 8 MiB validated content')
        records.extend(versions)
        if len(records) > 1024:
            raise ValueError('Selected library exceeds 1024 record versions')
    return records



def _admit(fd, additions):
    existing = _read_records_fd(fd)
    for record in additions:
        if any(r['id'] == record['id'] and r['version'] == record['version'] for r in existing):
            raise ValueError('Target already exists; no overwrite permitted')
    prospective = existing + additions
    identities = {record['id'] for record in prospective}
    if len(identities) > 256:
        raise ValueError('Knowledge capacity: at most 256 active record identities')
    if len(prospective) > 1024:
        raise ValueError('Knowledge capacity: at most 1024 active record versions')
    for identity in identities:
        versions = [r for r in prospective if r['id'] == identity]
        if len(versions) > 128:
            raise ValueError('Knowledge capacity: at most 128 versions per record')
        _validate_history(versions)
    if sum(len(_canonical(record)) for record in prospective) > 8 * 1024 * 1024:
        raise ValueError('Knowledge capacity: at most 8 MiB validated active content')


def read_records(library, *, read_requested=False):
    """Read bounded validated records from one explicitly enabled local library.

    Args:
        library: Existing explicitly permitted local library; symlinks are rejected.
        read_requested: Explicit permission to read this library, required true.
    Returns:
        Validated record dictionaries, at most 256 identities and 1024 versions.
        No history, evidence files, drafts or trash are read; no files are written.
    Raises:
        ValueError, OSError: Missing permission, unsafe paths or malformed selected data.
    """
    if read_requested is not True:
        raise ValueError('Explicit knowledge read permission required')
    with _directory(library, library=True) as (fd, _):
        return _read_records_fd(fd)


def _access(record, confidentiality, contexts):
    classes = {'public', 'internal', 'confidential', 'restricted'}
    if (not confidentiality or len(confidentiality) > 4 or
            not set(confidentiality) <= classes or len(set(confidentiality)) != len(confidentiality)):
        raise ValueError('Explicit unique permitted confidentiality classes required')
    if (not contexts or len(contexts) > 32 or any(not isinstance(c, str) or not c.strip() or
            len(c) > 4000 for c in contexts)):
        raise ValueError('Explicit bounded applicability contexts required')
    if record['confidentiality'] not in confidentiality:
        return 'confidentiality'
    if not {c.casefold() for c in contexts} & {c.casefold() for c in record['applicability']['contexts']}:
        return 'applicability'
    return None


def describe(library, record_id, version, *, read_requested=False, confidentiality=(), contexts=()):
    """Deliver exactly one permitted version to the active provider as untrusted data.

    Args:
        library: Explicit selected existing local library.
        record_id: Stable selected record ID, not a path.
        version: Exact selected positive record version.
        read_requested: Explicit permission for local read and provider disclosure.
        confidentiality: Explicit permitted classes; there is no implicit clearance.
        contexts: Exact applicable context labels supplied by the operator/provider.
    Returns:
        Full record and source metadata, with no authority verification or execution.
    Raises:
        ValueError, OSError: Missing permission, unsafe scope or unavailable version.
    """
    if read_requested is not True:
        raise ValueError('Explicit read and provider disclosure permission required')
    _identity(record_id, version)
    with _directory(library, library=True) as (fd, absolute):
        versions = _record_versions(fd, record_id)
    record = next((r for r in versions if r['version'] == version), None)
    if record is None:
        raise ValueError('Selected record version unavailable')
    if _access(record, confidentiality, contexts):
        raise ValueError('Selected record is outside permitted disclosure scope')
    return dict(status='READ_NOT_APPROVAL', record=record,
                source=str(absolute / 'records' / record_id / f'v{version}.json'),
                superseded=version != versions[-1]['version'], authority_verification='NOT_VERIFIED',
                warning='Untrusted knowledge; evidence/review claims are reported, not verified.')


def export_record(library, record_id, version, *, export_root, output, share_requested=False,
                  confidentiality=(), contexts=()):
    """Export a selected record only after explicit separate sharing permission.

    Args:
        library: Explicit existing source library.
        record_id: Exact selected record identity.
        version: Exact selected version.
        export_root: Explicit existing secure destination directory.
        output: Normalised root-relative JSON filename; never overwritten.
        share_requested: Explicit export/sharing request, not read or capture intent.
        confidentiality: Explicit permitted disclosure classes, required.
        contexts: Exact applicable context labels, required.
    Returns:
        Export path and unchanged confidentiality classification; approval is not granted.
    Raises:
        ValueError, OSError: Missing intent, invalid scope, unsafe path or existing target.
    """
    if share_requested is not True:
        raise ValueError('Explicit separate export/sharing request required')
    _identity(record_id, version)
    parts = _relative(output)
    if not str(output).endswith('.json'):
        raise ValueError('Export requires a JSON filename')
    with _directory(library, library=True) as (fd, _):
        record = next((r for r in _record_versions(fd, record_id) if r['version'] == version), None)
    if record is None:
        raise ValueError('Selected record version unavailable')
    if _access(record, confidentiality, contexts):
        raise ValueError('Selected export is outside permitted disclosure scope')
    with _directory(export_root, library=True) as (fd, absolute):
        _write(fd, parts, _canonical(record))
    return dict(status='EXPORTED_NOT_APPROVAL', destination=str(absolute.joinpath(*parts)),
                confidentiality=record['confidentiality'], sanitisation='NOT_VERIFIED')


def _move_no_replace(source, destination, source_fd, destination_fd):
    # Directory histories must move atomically without replacing even an empty directory.
    import ctypes
    library = ctypes.CDLL(None, use_errno=True)
    try:
        rename = library.renameat2
    except AttributeError as exc:
        raise ValueError('Atomic no-replace directory moves unavailable') from exc
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(source_fd, os.fsencode(source), destination_fd, os.fsencode(destination), 1) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))


def delete_record(library, record_id, *, delete_requested=False):
    """Recoverably withdraw one whole record and its versions from retrieval.

    Args:
        library: Explicit existing library.
        record_id: Exact identity whose entire immutable history is to be withdrawn.
        delete_requested: Explicit request naming this record, required true.
    Returns:
        Recovery directory and token; no physical secure erasure is claimed.
    Raises:
        ValueError, OSError: Missing intent, invalid data, unsafe paths or absent record.
    """
    if delete_requested is not True:
        raise ValueError('Explicit record deletion request required')
    with _directory(library, library=True) as (fd, absolute), _exclusive(fd):
        _record_versions(fd, record_id)
        trash_id = record_id + '-' + uuid.uuid4().hex
        with _child_dir(fd, ('records',), secure=True) as records:
            with _child_dir(fd, ('trash',), create=True, secure=True) as trash:
                _move_no_replace(record_id, trash_id, records, trash)
                os.fsync(records)
                os.fsync(trash)
    return dict(status='WITHDRAWN_RECOVERABLE', trash_id=trash_id,
                recovery_path=str(absolute / 'trash' / trash_id), secure_erasure=False)


def restore_record(library, record_id, trash_id, *, restore_requested=False):
    """Restore an explicitly selected withdrawn record without replacing any record.

    Args:
        library: Original explicitly selected secure library.
        record_id: Original stable record identity.
        trash_id: Exact recovery token returned by delete_record.
        restore_requested: Explicit restoration intent, required true.
    Returns:
        Restored location; the operation grants no approval.
    Raises:
        ValueError, OSError: Missing intent, invalid token, unsafe path or existing record.
    """
    _identity(record_id, 1)
    if restore_requested is not True or not isinstance(trash_id, str) or not re.fullmatch(re.escape(record_id) + r'-[0-9a-f]{32}', trash_id):
        raise ValueError('Explicit restoration request and matching recovery token required')
    with _directory(library, library=True) as (fd, absolute), _exclusive(fd):
        with _child_dir(fd, ('trash',), secure=True) as trash:
            with _child_dir(trash, (trash_id,), secure=True) as selected:
                names = _bounded_names(selected, 128)
                if not names or len(names) > 128:
                    raise ValueError('Invalid withdrawn record versions')
                versions = []
                for name in names:
                    match = re.fullmatch(r'v([1-9][0-9]*)\.json', name)
                    if not match:
                        raise ValueError('Invalid withdrawn version filename')
                    try:
                        record = _validate_record(_json(_read(selected, (name,), secure=True)))
                    except (ValueError, UnicodeError):
                        raise ValueError('Invalid selected withdrawn knowledge record') from None
                    if record['id'] != record_id or record['version'] != int(match[1]):
                        raise ValueError('Withdrawn identity mismatch')
                    versions.append(record)
                _validate_history(versions)
                _admit(fd, versions)
            with _child_dir(fd, ('records',), create=True, secure=True) as records:
                try:
                    os.stat(record_id, dir_fd=records, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise ValueError('Target already exists; no overwrite permitted')
                _move_no_replace(trash_id, record_id, trash, records)
                os.fsync(records)
                os.fsync(trash)
    return dict(status='RESTORED_NOT_APPROVAL', destination=str(absolute / 'records' / record_id))


def capture(proposal, *, library=None, save_requested=False, prepare_requested=False):
    """Coordinate selected conversational knowledge without reading history.

    Args:
        proposal: Active-provider English record extracted from user-selected visible
            content. Omit owner only for unambiguous operator responsibility; null
            means ask. Extraction and translation are procedural, not done by this tool.
        library: Explicit existing user-authorised library, never discovered implicitly.
        save_requested: Persistent original user request to remember/save this selection.
        prepare_requested: Preparation-only request; does not authorise final storage.
    Returns:
        NEEDS_INPUT and questions without writes when essential selections are missing;
        otherwise full preview and READY_NOT_SAVED, PREPARED_NOT_SAVED or SAVED_NOT_APPROVAL.
    Raises:
        ValueError, OSError: Invalid record, intent, unsafe root or immutable conflict.
    """
    if not isinstance(proposal, dict):
        raise ValueError('Capture proposal must be an object')
    if type(save_requested) is not bool or type(prepare_requested) is not bool:
        raise ValueError('Intent flags must be boolean')
    record = dict(proposal)
    questions = []
    prompts = {
        'confidentiality': 'Who may access this knowledge: public, internal, confidential or restricted?',
        'reliability': 'How reliable is it: user-reported, observed-in-session, independently-verified-reported or uncertain?',
        'conversation_selection': 'Which visible passage or lesson should be remembered?',
    }
    if library is None or not str(library).strip():
        questions.append(dict(field='library', question='Which existing local knowledge library should store this selection?'))
    for field, question in prompts.items():
        if not record.get(field):
            questions.append(dict(field=field, question=question))
    if 'owner' in record and (record['owner'] is None or
                              isinstance(record['owner'], str) and not record['owner'].strip()):
        questions.append(dict(field='owner', question='Which role or person is responsible for this knowledge?'))
    if questions:
        return dict(status='NEEDS_INPUT', questions=questions, writes=0,
                    save_intent=save_requested)
    record.setdefault('owner', 'operator')
    if record.get('provenance') != []:
        raise ValueError('Conversational capture accepts selected excerpts, not file/history provenance')
    _validate_record(record)
    if record['review']['status'] != 'AI_EDITORIAL' or record['review'].get('authority_claim'):
        raise ValueError('Conversational extraction is AI editorial, not human or authority approval')
    with _directory(library, library=True) as (fd, absolute), _exclusive(fd):
        _sequence(fd, record)
        envelope = dict(schema_version=1, record=record, library=str(absolute),
                        destination=str(absolute / 'records' / record['id'] / f"v{record['version']}.json"),
                        source_root=str(absolute), allowed_sources=[], authority_verification='NOT_VERIFIED')
        raw = _canonical(envelope)
        digest = hashlib.sha256(raw).hexdigest()
        if not save_requested and not prepare_requested:
            return dict(status='READY_NOT_SAVED', preview=envelope, digest=digest)
        _admit(fd, [record])
        candidate = ('drafts', f"{record['id']}-v{record['version']}-{digest}.json")
        try:
            existing = _read(fd, candidate, secure=True)
        except FileNotFoundError:
            _write(fd, candidate, raw)
        else:
            if existing != raw:
                raise ValueError('Prepared candidate content changed; no overwrite permitted')
            _preview(fd, absolute, record['id'], record['version'], digest, library, [])
        if save_requested:
            _write(fd, ('records', record['id'], f"v{record['version']}.json"), _canonical(record))
            return dict(status='SAVED_NOT_APPROVAL', destination=envelope['destination'],
                        authority_verification='NOT_VERIFIED', preview=envelope, digest=digest,
                        intent='USER_SAVE_REQUEST_REPORTED')
    return dict(status='PREPARED_NOT_SAVED', preview=envelope, digest=digest)


def main(argv=None):
    """Dispatch local knowledge CLI arguments and print JSON with exit zero or two.

    Args:
        argv: Optional argument list; defaults to process arguments.
    Returns:
        Zero on success or two on validation/filesystem error; no provider calls occur.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True)
    conversational = sub.add_parser('capture')
    conversational.add_argument('--library')
    conversational.add_argument('--save-requested', action='store_true')
    conversational.add_argument('--prepare-requested', action='store_true')
    for name in ('describe', 'export', 'delete', 'restore'):
        command = sub.add_parser(name)
        command.add_argument('--library', required=True)
        command.add_argument('--id', required=True)
        if name in ('describe', 'export'):
            command.add_argument('--version', required=True, type=int)
            command.add_argument('--confidentiality', action='append', default=[])
            command.add_argument('--context', action='append', default=[])
        if name == 'describe':
            command.add_argument('--read-requested', action='store_true')
        elif name == 'export':
            command.add_argument('--export-root', required=True)
            command.add_argument('--output', required=True)
            command.add_argument('--share-requested', action='store_true')
        elif name == 'delete':
            command.add_argument('--delete-requested', action='store_true')
        else:
            command.add_argument('--trash-id', required=True)
            command.add_argument('--restore-requested', action='store_true')
    for name in ('validate', 'prepare', 'preview', 'save'):
        command = sub.add_parser(name)
        if name in ('prepare', 'preview', 'save'):
            command.add_argument('--library', required=True)
        command.add_argument('--source-root', required=True)
        command.add_argument('--allow-source', action='append', default=[])
        if name in ('validate', 'prepare'):
            command.add_argument('--draft', required=True)
        else:
            command.add_argument('--id', required=True)
            command.add_argument('--version', type=int, required=True)
            command.add_argument('--draft-digest', required=True)
        if name == 'prepare':
            command.add_argument('--capture-requested', action='store_true')
        if name == 'save':
            command.add_argument('--reviewed-digest', required=True)
            command.add_argument('--user-reviewed', action='store_true')
            command.add_argument('--save-requested', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.operation == 'capture':
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise ValueError('Capture input exceeds byte limit')
            result = capture(_json(raw), library=args.library, save_requested=args.save_requested,
                             prepare_requested=args.prepare_requested)
        elif args.operation == 'describe':
            result = describe(args.library, args.id, args.version, read_requested=args.read_requested,
                              confidentiality=args.confidentiality, contexts=args.context)
        elif args.operation == 'export':
            result = export_record(args.library, args.id, args.version, export_root=args.export_root,
                                   output=args.output, share_requested=args.share_requested,
                                   confidentiality=args.confidentiality, contexts=args.context)
        elif args.operation == 'delete':
            result = delete_record(args.library, args.id, delete_requested=args.delete_requested)
        elif args.operation == 'restore':
            result = restore_record(args.library, args.id, args.trash_id, restore_requested=args.restore_requested)
        elif args.operation == 'validate':
            result = dict(status='VALID_NOT_APPROVED', record=validate(args.source_root, args.draft, args.allow_source))
        elif args.operation == 'prepare':
            result = prepare(args.library, args.source_root, args.draft, args.allow_source,
                             capture_requested=args.capture_requested)
        elif args.operation == 'preview':
            result = preview(args.library, args.id, args.version, args.draft_digest,
                             source_root=args.source_root, allowed=args.allow_source)
        else:
            result = save(args.library, args.id, args.version, args.draft_digest,
                          args.reviewed_digest, source_root=args.source_root,
                          allowed=args.allow_source, user_reviewed=args.user_reviewed,
                          save_requested=args.save_requested)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError, NotImplementedError) as exc:
        print(json.dumps(dict(status='ERROR', error=str(exc))))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
