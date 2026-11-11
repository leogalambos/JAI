# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Retained local directory and finite regular-file snapshots, with no writers.

An observed pathname or identity is not a read grant. Callers retain a directory
object, select a relative file, and pin its admitted leaf identity on later
captures. Snapshot bytes always come from the captured native handle.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import os
from pathlib import Path
import stat


@dataclass(frozen=True)
class FileInfo:
    """Immutable native identity, captured length and modification marker.

    Identity is platform-qualified and local to the filesystem, not a global
    content identity or canonical semantic hash. Size is measured in bytes.
    """
    identity: tuple
    size: int
    modified: tuple
    links: int
    directory: bool
    reparse: bool = False


def _bound(maximum):
    if maximum is not None and (type(maximum) is not int or maximum < 0):
        raise ValueError('nonnegative maximum byte count required')


def _relative(value):
    value = os.fspath(value)
    if not isinstance(value, str) or not value or '\x00' in value or value.startswith('/'):
        raise ValueError('bounded relative path required')
    components = value.split('/')
    if any(item in {'', '.', '..'} for item in components):
        raise ValueError('nontraversing relative path required')
    if os.name == 'nt':
        from windows_readonly import _parts
        _parts('C:\\' + '\\'.join(components))
    return components


def _posix_info(fd):
    info = os.fstat(fd)
    return FileInfo(('posix', info.st_dev, info.st_ino), info.st_size,
                    (info.st_mtime_ns,), info.st_nlink, stat.S_ISDIR(info.st_mode),
                    not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)))


class _PosixRoot:
    def __init__(self, path):
        if not hasattr(os, 'O_NOFOLLOW') or os.open not in os.supports_dir_fd:
            raise ValueError('secure local directory adapter unavailable')
        self.path = Path(path).absolute()
        if '..' in self.path.parts:
            raise ValueError('path traversal denied')
        self.handle, self.ancestry = self._open()

    def _open(self):
        directory = os.open(self.path.anchor, os.O_RDONLY | os.O_DIRECTORY)
        try:
            ancestry = [_posix_info(directory).identity]
            for part in self.path.parts[1:]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                os.close(directory); directory = child
                ancestry.append(_posix_info(directory).identity)
            return directory, tuple(ancestry)
        except BaseException:
            os.close(directory)
            raise

    def verify(self):
        current, ancestry = self._open()
        try:
            if _posix_info(current).identity != _posix_info(self.handle).identity:
                raise ValueError('retained root identity changed')
            return ancestry
        finally:
            os.close(current)

    def capture(self, components):
        directory = self.handle; owned = []
        try:
            for part in components[:-1]:
                directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                owned.append(directory)
            # Nonblocking open lets the subsequent type check reject FIFOs and
            # devices rather than waiting for another process before inspection.
            return os.open(components[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        finally:
            for handle in reversed(owned): os.close(handle)

    def info(self, handle): return _posix_info(handle)
    def read_page(self, handle, offset, length):
        blocks = []; remaining = length
        while remaining:
            block = os.pread(handle, min(remaining, 1024 * 1024), offset)
            if not block: break
            blocks.append(block); offset += len(block); remaining -= len(block)
        return b''.join(blocks)

    def read_all(self, handle, size):
        # Preserve the existing full-snapshot allocation behavior; bounded pages
        # use pread instead of materializing a complete large journal.
        os.lseek(handle, 0, os.SEEK_SET)
        with os.fdopen(handle, 'rb', closefd=False) as stream:
            return stream.read(size)

    def close_file(self, handle): os.close(handle)
    def close(self): os.close(self.handle)


class _WindowsRoot:
    def __init__(self, path):
        from windows_readonly import _WinAPI, _parts
        self.path = os.fspath(path)
        self.drive, self.components = _parts(self.path + ('' if self.path.endswith('\\') else '\\') + '__directory_probe__')
        self.components = self.components[:-1]
        self.api = _WinAPI()
        self.handles, self.ancestry = self._open()
        self.handle = self.handles[-1]

    def info(self, handle):
        from windows_readonly import _DIRECTORY, _REPARSE
        info = self.api.info(handle)
        return FileInfo(('windows', *info.identity), info.size, info.modified,
                        info.links, bool(info.attributes & _DIRECTORY), bool(info.attributes & _REPARSE))

    def _open(self):
        handles = []; ancestry = []
        try:
            handles.append(self.api.root(self.drive))
            for component in [None, *self.components]:
                if component is not None: handles.append(self.api.child(handles[-1], component, True))
                info = self.info(handles[-1])
                if info.reparse or not info.directory: raise ValueError('nonreparse directory required')
                ancestry.append(info.identity)
            return handles, tuple(ancestry)
        except BaseException:
            for handle in reversed(handles): self.api.close(handle)
            raise

    def verify(self):
        handles, ancestry = self._open()
        try:
            if self.info(handles[-1]).identity != self.info(self.handle).identity:
                raise ValueError('retained root identity changed')
            return ancestry
        finally:
            for handle in reversed(handles): self.api.close(handle)

    def capture(self, components):
        parent = self.handle; owned = []
        try:
            for component in components[:-1]:
                parent = self.api.child(parent, component, True); owned.append(parent)
                info = self.info(parent)
                if info.reparse or not info.directory: raise ValueError('nonreparse directory required')
            return self.api.child(parent, components[-1], False)
        finally:
            for handle in reversed(owned): self.api.close(handle)

    def read_page(self, handle, offset, length):
        self.api.seek(handle, offset)
        blocks = []; remaining = length
        while remaining:
            block = self.api.read(handle, min(remaining, 1024 * 1024))
            if not block: break
            blocks.append(block); remaining -= len(block)
        return b''.join(blocks)

    def read_all(self, handle, size): return self.read_page(handle, 0, size)
    def close_file(self, handle): self.api.close(handle)
    def close(self):
        for handle in reversed(self.handles): self.api.close(handle)


class CapturedFile:
    """Finite regular-file observation owned by a retained root; use as a context manager."""
    def __init__(self, root, handle, info, verify_root=True):
        """Bind an acquired native handle; construction belongs to ReadOnlyRoot.capture."""
        self._root, self._handle, self.info = root, handle, info
        self._verify_root, self._closed = verify_root, False

    def _check(self):
        if self._closed or self._root._closed: raise ValueError('captured file or root is closed')
        if self._verify_root: self._root.observe_ancestry()
        current = self._root._native.info(self._handle)
        # Atomic pathname replacement can unlink a coherent captured leaf.
        # Its descriptor still owns the original bytes; a newly added hardlink
        # is unsafe and a subsequent capture must match the admitted identity.
        if current.links not in {0, 1} or replace(current, links=self.info.links) != self.info:
            raise ValueError('regular file changed while reading')

    def read_page(self, offset, length):
        """Read one exact bounded page from the captured size without changing files.

        Args:
            offset: Nonnegative integer byte offset within the captured size.
            length: Nonnegative integer requested byte length; caller supplies its resource bound.
        Returns:
            At most length bytes, shortened only at the captured EOF.
        Raises:
            ValueError: Invalid bounds, closed/stale root, changed metadata or a short read.
            OSError: Native reading or descriptor verification fails.
        """
        if type(offset) is not int or type(length) is not int or offset < 0 or length < 0 or offset > self.info.size:
            raise ValueError('nonnegative captured page bounds required')
        self._check(); count = min(length, self.info.size - offset)
        data = self._root._native.read_page(self._handle, offset, count)
        self._check()
        if len(data) != count: raise ValueError('regular file changed while reading')
        return data

    def read_all(self):
        """Return exactly the captured finite file bytes.

        Returns:
            Immutable captured bytes; no size cap is invented beyond capture's maximum.
        Raises:
            ValueError: Closed/stale root, changed metadata or short read.
            OSError: Native reading fails.
        """
        self._check(); data = self._root._native.read_all(self._handle, self.info.size); self._check()
        if len(data) != self.info.size: raise ValueError('regular file changed while reading')
        return data

    def close(self):
        """Release this file handle idempotently; never delete or rewrite an input."""
        if not self._closed:
            self._closed = True; self._root._native.close_file(self._handle)

    def __enter__(self): return self
    def __exit__(self, *_args): self.close()


class ReadOnlyRoot:
    """Retained local directory identity with parent-relative, nonfollowing file capture."""
    def __init__(self, path):
        """Open a directory without following any link/reparse component.

        Args:
            path: Local directory pathname; Windows requires an absolute drive-qualified path.
        Raises:
            ValueError: Ambiguous, traversing, linked or unsupported input.
            OSError: Native acquisition fails.
        """
        self._native = _WindowsRoot(path) if os.name == 'nt' else _PosixRoot(path)
        self._closed = False
        try:
            self.identity = self._native.info(self._native.handle).identity
        except BaseException:
            self._closed = True
            self._native.close()
            raise

    def observe_ancestry(self):
        """Observe current directory ancestry without granting any pathname read access.

        Returns:
            Platform-qualified identities from filesystem root through this directory.
        Raises:
            ValueError: Closed root or a changed admitted directory identity.
            OSError: Current path verification fails.
        """
        if self._closed: raise ValueError('retained root is closed')
        return self._native.verify()

    def capture(self, relative, maximum=None, expected_identity=None):
        """Capture one regular file beneath the retained directory.

        Args:
            relative: Nonempty slash-separated path without empty/dot/traversal components.
            maximum: Optional nonnegative byte ceiling, applied before reading.
            expected_identity: Optional admitted leaf identity; later captures must provide it.
        Returns:
            A CapturedFile whose handle must be closed by the caller.
        Raises:
            ValueError: Changed root/leaf, type/link/size denial or invalid bound/path.
            OSError: Native acquisition fails.
        """
        return self._capture(relative, maximum, expected_identity, True)

    def _capture(self, relative, maximum, expected_identity, verify_root):
        _bound(maximum); components = _relative(relative)
        if self._closed: raise ValueError('retained root is closed')
        if verify_root: self.observe_ancestry()
        handle = self._native.capture(components)
        try:
            info = self._native.info(handle)
            if info.directory or info.reparse or info.links != 1 or maximum is not None and info.size > maximum:
                raise ValueError('bounded single-link regular file required')
            if expected_identity is not None and tuple(expected_identity) != info.identity:
                raise ValueError('admitted file identity changed')
            return CapturedFile(self, handle, info, verify_root)
        except BaseException:
            self._native.close_file(handle)
            raise

    def close(self):
        """Release retained directory handles idempotently; source state is untouched."""
        if not self._closed:
            self._closed = True; self._native.close()

    def __enter__(self): return self
    def __exit__(self, *_args): self.close()


def read_snapshot(path, maximum=None):
    """Capture one absolute-path-compatible regular file using the shared reader.

    Args:
        path: File pathname; POSIX relative paths retain their existing absolute resolution.
        maximum: Optional nonnegative maximum byte count; None permits a finite journal.
    Returns:
        Exact immutable snapshot bytes without locks, writers or initialization.
    Raises:
        ValueError: Invalid bounds, unsafe input or an unstable finite read.
        OSError: Secure acquisition or reading fails.
    """
    _bound(maximum)
    if os.name == 'nt':
        from windows_readonly import read_snapshot as native_snapshot
        return native_snapshot(path, maximum)
    resolved = Path(path).absolute()
    if '..' in resolved.parts: raise ValueError('path traversal denied')
    with ReadOnlyRoot(resolved.parent) as root:
        # The directory is freshly acquired for this legacy one-shot call, not
        # reused across admission events; its descriptor already pins that walk.
        with root._capture(resolved.name, maximum, None, False) as captured:
            return captured.read_all()
