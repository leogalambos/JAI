# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Private framed fact descriptors; callers serialize access and own references.

Files are created in the process-retained helper cwd, never a source directory.
Only one record is encoded or decoded at a time. No descriptor is reopened by
name, and independent consumers supply their own byte offsets.
"""
import errno
import json
import struct
import tempfile

PHYSICAL_DOMAIN = 539270912
PHYSICAL_TOTAL = 1617812736
DESCRIPTORS = 385
VERTICES = frozenset({'version', 'use', 'finding', 'audit'})
EDGES = frozenset({'reference', 'governing-dependency', 'decision-effect', 'participant', 'ownership', 'material'})


def _reject_constant(_value):
    raise ValueError('Non-finite private JSON value')


class _Budget:
    """Candidate counters shared by all its source writers; no decoded values."""
    def __init__(self, limits, error):
        self.limits = limits; self.error = error
        self.encoded = self.vertices = self.edges = self.count = 0

    def check(self, encoded, vertices, edges, count, source=None):
        """Reject proposed increments before allocation/write, without mutation."""
        if (self.encoded + encoded > self.limits['maxEncodedGraphBytes'] or
                self.vertices + vertices > self.limits['maxVertices'] or
                self.edges + edges > self.limits['maxEdges'] or
                self.count + count > 600000 or
                self.encoded + encoded + 4 * (self.count + count) > PHYSICAL_DOMAIN):
            raise self.error('resource-limit', source)

    def add(self, encoded, vertices, edges, count):
        """Commit previously checked scalar increments after a complete write."""
        self.encoded += encoded; self.vertices += vertices; self.edges += edges; self.count += count


class _Pool:
    """Count distinct live descriptors and physical bytes across reference owners."""
    def __init__(self, error):
        self.error = error; self.objects = set(); self.physical = 0

    def create(self, spool):
        """Allocate a retained-cwd descriptor or raise a redacted storage error."""
        if len(self.objects) >= DESCRIPTORS: raise self.error('resource-limit')
        # TemporaryFile retains its original descriptor, including named
        # delete-on-close platform fallbacks; no pathname cleanup is needed.
        try: handle = tempfile.TemporaryFile(mode='w+b', dir='.')
        except OSError as error:
            raise self.error('resource-limit' if error.errno in {errno.ENOSPC, errno.EDQUOT, errno.EMFILE, errno.ENFILE} else 'read-failed') from error
        try: self.objects.add(spool)
        except BaseException:
            handle.close()
            raise
        return handle

    def reserve(self, size):
        """Reserve physical framing bytes before writing; caller rolls back faults."""
        if self.physical + size > PHYSICAL_TOTAL: raise self.error('resource-limit')
        self.physical += size


class _Spool:
    """One source writer, then immutable frames with explicit shared ownership.

    The initial reference belongs to candidate construction. Sealed objects may
    acquire cache or lease references; the last release closes the descriptor.
    Reads are serialized by the helper and use caller-owned byte offsets.
    """
    def __init__(self, budget, encode, error, chunk, pool=None):
        self.budget = budget; self.encode = encode; self.error = error; self.chunk = chunk
        self.pool = pool or _Pool(error)
        self.encoded = self.vertices = self.edges = self.count = self.physical = 0
        self.refs = 1; self.sealed = False; self.closed = False; self.failed = False
        self.handle = self.pool.create(self)

    def append(self, fact):
        """Encode one fact and charge its complete frame; retain no decoded input.

        A failed append rejects construction. The caller must release the object
        rather than continue or publish a potentially partial private frame.
        """
        if self.sealed or self.closed or self.failed: raise self.error('read-failed')
        encoded = self.encode(fact); size = len(encoded); source = fact.get('sourceId')
        vertices = int(fact['kind'] in VERTICES); edges = int(fact['kind'] in EDGES)
        if not 0 < size <= self.chunk or vertices + edges != 1: raise self.error('resource-limit', source)
        self.budget.check(size, vertices, edges, 1, source)
        physical = size + 4
        prior_physical = self.physical
        next_physical = prior_physical + physical
        self.pool.reserve(physical)
        try:
            self.handle.seek(self.physical)
            if self.handle.write(struct.pack('>I', size)) != 4 or self.handle.write(encoded) != size:
                raise OSError('Incomplete private fact write')
            self.physical = next_physical; self.encoded += size
            self.vertices += vertices; self.edges += edges; self.count += 1
            self.budget.add(size, vertices, edges, 1)
        except BaseException as error:
            self.pool.physical -= physical
            self.physical = prior_physical
            self.failed = True
            if isinstance(error, (OSError, ValueError)):
                raise self.error('read-failed', source) from error
            raise

    def seal(self):
        """Flush a completed source and prohibit further append operations."""
        if self.closed or self.failed: raise self.error('read-failed')
        try: self.handle.flush()
        except BaseException as error:
            self.failed = True
            if isinstance(error, (OSError, ValueError)):
                raise self.error('read-failed') from error
            raise
        self.sealed = True
        # The finished immutable object does not retain the candidate budget.
        self.budget = None
        return self

    def acquire(self):
        """Add one owner of sealed immutable bytes and return this same object."""
        if self.closed or self.failed or not self.sealed: raise self.error('read-failed')
        self.refs += 1
        return self

    def release(self):
        """Drop one owner, retiring descriptor and counters at the last release.

        Releasing a closed object is harmless. Buffered I/O close errors are
        suppressed. Other failures propagate after retiring this ownership;
        callers must still release their remaining objects.
        """
        if self.closed: return
        self.refs -= 1
        if self.refs == 0:
            try: self.handle.close()
            except (OSError, ValueError):
                # Cleanup must release every owner even if buffered close reports
                # a prior write failure; no failed spool is ever published.
                pass
            finally:
                self.closed = True
                self.pool.physical -= self.physical
                self.pool.objects.remove(self)

    def read(self, offset):
        """Decode one bounded frame at offset; return fact, next offset and size.

        Invalid, zero, oversized or truncated framing raises the injected
        redacted error. No cursor or descriptor position is shared by callers.
        """
        if self.closed or type(offset) is not int or not 0 <= offset < self.physical:
            raise self.error('read-failed')
        try:
            self.handle.seek(offset)
            prefix = self.handle.read(4)
            if len(prefix) != 4: raise ValueError('Truncated frame')
            size = struct.unpack('>I', prefix)[0]
            if not 0 < size <= self.chunk or offset + 4 + size > self.physical: raise ValueError('Invalid frame')
            data = self.handle.read(size)
            if len(data) != size: raise ValueError('Truncated frame')
            fact = json.loads(data, parse_constant=_reject_constant)
            if not isinstance(fact, dict) or fact.get('kind') not in VERTICES | EDGES: raise ValueError('Invalid fact')
            return fact, offset + 4 + size, size
        except (OSError, ValueError, UnicodeError) as error:
            raise self.error('read-failed') from error
