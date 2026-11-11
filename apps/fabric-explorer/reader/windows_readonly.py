# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Read finite local Windows snapshots through non-following native handles.

Children are opened relative to retained directory handles, rather than by
re-resolving a checked pathname. No writer, lock file or authority operation is
provided. Native Windows qualification is separate from portable contract tests.
"""
from __future__ import annotations

import ctypes
from dataclasses import dataclass
import os
import re


_READ = 0x00100081
_SHARE_READ = 1
_SHARE_DELETE = 4
_DIRECTORY = 0x10
_REPARSE = 0x400
_OPEN_REPARSE = 0x00200000
_SYNCHRONOUS = 0x20
_DISK = 1
_CHUNK = 1024 * 1024
_INVALID_HANDLE = ctypes.c_void_p(-1).value
_U32 = ctypes.c_uint32
_HANDLE = ctypes.c_void_p


class _FileTime(ctypes.Structure):
    _fields_ = [('low', _U32), ('high', _U32)]


class _FileInfo(ctypes.Structure):
    _fields_ = [('attributes', _U32), ('creation', _FileTime),
                ('access', _FileTime), ('write', _FileTime), ('volume', _U32),
                ('size_high', _U32), ('size_low', _U32), ('links', _U32),
                ('index_high', _U32), ('index_low', _U32)]


class _UnicodeString(ctypes.Structure):
    _fields_ = [('length', ctypes.c_uint16), ('maximum', ctypes.c_uint16),
                ('buffer', ctypes.c_void_p)]


class _ObjectAttributes(ctypes.Structure):
    _fields_ = [('length', _U32), ('root', _HANDLE),
                ('name', ctypes.POINTER(_UnicodeString)), ('attributes', _U32),
                ('security', ctypes.c_void_p), ('quality', ctypes.c_void_p)]


class _Status(ctypes.Union):
    _fields_ = [('status', ctypes.c_int32), ('pointer', ctypes.c_void_p)]


class _IoStatus(ctypes.Structure):
    _fields_ = [('status', _Status), ('information', ctypes.c_size_t)]


@dataclass(frozen=True)
class _Info:
    attributes: int
    size: int
    links: int
    identity: tuple[int, int, int]
    modified: tuple[int, int]


def _parts(path):
    try:
        value = os.fspath(path)
    except TypeError as error:
        raise ValueError('absolute local-drive path required') from error
    if not isinstance(value, str) or not re.match(r'^[A-Za-z]:\\', value):
        raise ValueError('absolute local-drive path required')
    if '\x00' in value or '/' in value or ':' in value[2:]:
        raise ValueError('device, alternate stream or ambiguous path denied')
    components = value[3:].split('\\')
    if not components or any(not item or item in {'.', '..'} or item[-1] in ' .'
                             for item in components):
        raise ValueError('nontraversing unambiguous file path required')
    for item in components:
        if any(char in item for char in '<>"|?*') or any(ord(char) < 32 for char in item):
            raise ValueError('ambiguous Windows component denied')
        if re.fullmatch(r'(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|CLOCK\$|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?',
                        item, re.IGNORECASE):
            raise ValueError('DOS device name denied')
        try:
            encoded = item.encode('utf-16-le')
        except UnicodeError as error:
            raise ValueError('valid Windows Unicode component required') from error
        if len(encoded) > 510:
            raise ValueError('bounded Windows component required')
    return value[:3], components


class _WinAPI:
    def __init__(self):
        if os.name != 'nt':
            raise ValueError('native Windows read adapter unavailable on this OS')
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.ntdll = ctypes.WinDLL('ntdll', use_last_error=True)
        self.kernel.CreateFileW.argtypes = [ctypes.c_wchar_p, _U32, _U32,
                                           ctypes.c_void_p, _U32, _U32, _HANDLE]
        self.kernel.CreateFileW.restype = _HANDLE
        self.kernel.GetDriveTypeW.argtypes = [ctypes.c_wchar_p]
        self.kernel.GetDriveTypeW.restype = _U32
        self.kernel.GetFileType.argtypes = [_HANDLE]
        self.kernel.GetFileType.restype = _U32
        self.kernel.GetFileInformationByHandle.argtypes = [_HANDLE, ctypes.POINTER(_FileInfo)]
        self.kernel.GetFileInformationByHandle.restype = ctypes.c_int
        self.kernel.ReadFile.argtypes = [_HANDLE, ctypes.c_void_p, _U32,
                                        ctypes.POINTER(_U32), ctypes.c_void_p]
        self.kernel.ReadFile.restype = ctypes.c_int
        self.kernel.CloseHandle.argtypes = [_HANDLE]
        self.kernel.CloseHandle.restype = ctypes.c_int
        self.kernel.SetFilePointerEx.argtypes = [_HANDLE, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64), _U32]
        self.kernel.SetFilePointerEx.restype = ctypes.c_int
        self.ntdll.NtCreateFile.argtypes = [ctypes.POINTER(_HANDLE), _U32,
            ctypes.POINTER(_ObjectAttributes), ctypes.POINTER(_IoStatus),
            ctypes.c_void_p, _U32, _U32, _U32, _U32, ctypes.c_void_p, _U32]
        self.ntdll.NtCreateFile.restype = ctypes.c_int32
        self.ntdll.RtlNtStatusToDosError.argtypes = [ctypes.c_int32]
        self.ntdll.RtlNtStatusToDosError.restype = _U32

    def root(self, drive):
        if self.kernel.GetDriveTypeW(drive) not in {2, 3, 6}:
            raise ValueError('local disk drive required')
        handle = self.kernel.CreateFileW('\\\\?\\' + drive, _READ, _SHARE_READ,
            None, 3, _OPEN_REPARSE | 0x02000000, None)
        if handle == _INVALID_HANDLE:
            raise ctypes.WinError(ctypes.get_last_error())
        return handle

    def child(self, parent, component, directory):
        buffer = ctypes.create_unicode_buffer(component)
        length = len(component.encode('utf-16-le'))
        name = _UnicodeString(length, length + 2, ctypes.cast(buffer, ctypes.c_void_p))
        attributes = _ObjectAttributes(ctypes.sizeof(_ObjectAttributes), parent,
                                       ctypes.pointer(name), 0x40, None, None)
        result, status = _HANDLE(), _IoStatus()
        # Parent-relative opens prevent a drive-letter or checked-prefix swap.
        options = _OPEN_REPARSE | _SYNCHRONOUS | (1 if directory else 0x40)
        # Write-time updates may be deferred while a Windows writer stays open;
        # exclude ordinary writers instead of treating timestamp equality as proof.
        sharing = _SHARE_READ if directory else _SHARE_READ | _SHARE_DELETE
        code = self.ntdll.NtCreateFile(ctypes.byref(result), _READ,
            ctypes.byref(attributes), ctypes.byref(status), None, 0, sharing,
            1, options, None, 0)
        if code != 0:
            raise ctypes.WinError(self.ntdll.RtlNtStatusToDosError(code))
        return result.value

    def info(self, handle):
        value = _FileInfo()
        if self.kernel.GetFileType(handle) != _DISK:
            raise ValueError('regular local disk object required')
        if not self.kernel.GetFileInformationByHandle(handle, ctypes.byref(value)):
            raise ctypes.WinError(ctypes.get_last_error())
        return _Info(value.attributes, value.size_high << 32 | value.size_low,
                     value.links, (value.volume, value.index_high, value.index_low),
                     (value.write.high, value.write.low))

    def read(self, handle, length):
        buffer, received = ctypes.create_string_buffer(length), _U32()
        if not self.kernel.ReadFile(handle, buffer, length, ctypes.byref(received), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return buffer.raw[:received.value]

    def close(self, handle):
        self.kernel.CloseHandle(handle)

    def seek(self, handle, offset):
        if type(offset) is not int or not 0 <= offset < 2 ** 63:
            raise ValueError('nonnegative native file offset required')
        position = ctypes.c_int64()
        if not self.kernel.SetFilePointerEx(handle, offset, ctypes.byref(position), 0):
            raise ctypes.WinError(ctypes.get_last_error())
        if position.value != offset:
            raise ValueError('native file offset differs from requested page')


def read_snapshot(path, maximum=None):
    """Return a finite stable snapshot from a local Windows regular file.

    Args:
        path: Absolute drive-qualified file path; no UNC, device, ADS, traversal,
            reparse component or multiply linked final file is accepted.
        maximum: Optional nonnegative maximum byte count. None permits a finite
            journal of any captured size; this does not impose an application
            memory budget. Reads use at most one MiB native buffers per chunk.
    Returns:
        Exactly the captured file length as immutable bytes. Handles are closed
        on success and failure; source files and directory entries are untouched.
    Raises:
        ValueError: Unsafe path/type/link/size, changed snapshot, invalid bound or
            Windows API unavailable on this host.
        OSError: Native open, metadata or read operation fails.

    Directory handles deny write/delete sharing during acquisition. The final
    read handle denies write sharing and permits replacement through delete
    sharing. An existing ordinary writer therefore prevents acquisition, and
    new writers cannot open that file during the read. Changed descriptor
    size/write-time or short reads also reject the snapshot. No lock file or
    writer-lock operation is used. This is a finite descriptor observation, not
    a filesystem transaction or protection against direct-volume writes,
    pre-existing writable mappings or adversarial timestamp restoration.
    """
    if maximum is not None and (type(maximum) is not int or maximum < 0):
        raise ValueError('nonnegative maximum byte count required')
    drive, components = _parts(path)
    api, handles = _WinAPI(), []
    try:
        root = api.root(drive)
        handles.append(root)
        info = api.info(root)
        if info.attributes & _REPARSE or not info.attributes & _DIRECTORY:
            raise ValueError('nonreparse directory required')
        for index, component in enumerate(components):
            directory = index < len(components) - 1
            handle = api.child(handles[-1], component, directory)
            handles.append(handle)
            info = api.info(handle)
            if info.attributes & _REPARSE or bool(info.attributes & _DIRECTORY) != directory:
                raise ValueError('nonreparse regular file/directory required')
        before = info
        if before.links != 1 or maximum is not None and before.size > maximum:
            raise ValueError('bounded single-link regular file required')
        blocks, remaining = [], before.size
        while remaining:
            block = api.read(handle, min(remaining, _CHUNK))
            if not block or len(block) > remaining:
                raise ValueError('regular file changed while reading')
            blocks.append(block)
            remaining -= len(block)
        after = api.info(handle)
        if after.links > 1 or (after.identity, after.size, after.modified, after.attributes) != (
                before.identity, before.size, before.modified, before.attributes):
            raise ValueError('regular file changed while reading')
        return b''.join(blocks)
    finally:
        for handle in reversed(handles):
            api.close(handle)
