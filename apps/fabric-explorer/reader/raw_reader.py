# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""App-owned bounded capture/semantic transport; writer APIs are never exposed."""
import base64
import json
import os
from pathlib import Path
import sys
import uuid

sys.dont_write_bytecode = True
FRAME = 8 * 1024 * 1024
TOTAL = 1024 * 1024 * 1024
PAGE = 256 * 1024


class Reader:
    """Retain explicit local roots and leaf identities until capability release.

    Args:
        root_type: Canonical retained-directory implementation from trusted resources.
        write_paths: Existing app-owned directories excluded in both ancestry directions.
    """
    def __init__(self, root_type, write_paths):
        self.root_type = root_type
        self.writes = []
        self.groups = {}
        self.semantic = None
        try:
            for path in write_paths:
                self.writes.append(root_type(path))
        except BaseException:
            self.close()
            raise

    def _check(self, roots):
        """Revalidate mutable roots and deny overlap; observations grant no reads."""
        write_observations = [(root.identity, root.observe_ancestry()) for root in self.writes]
        for root in roots:
            ancestry = root.observe_ancestry()
            for identity, write_ancestry in write_observations:
                if root.identity in write_ancestry or identity in ancestry:
                    raise ValueError('source and application storage overlap')

    def admit(self, selections):
        """Admit explicit selected files transactionally; return identities, never source bytes.

        Args:
            selections: At most 128 main-only project/path/family dictionaries.
        Returns:
            Opaque group token and per-file native identities for app-owned namespace mapping.
        Raises:
            ValueError: Invalid selection, unsafe file, overlap, replacement or resource ceiling.
            OSError: Secure native acquisition fails.
        """
        if not isinstance(selections, list) or not 1 <= len(selections) <= 128:
            raise ValueError('bounded explicit selection required')
        roots = []; files = []; total = 0; seen = set()
        try:
            for item in selections:
                if not isinstance(item, dict) or set(item) != {'projectPath', 'path', 'family'}:
                    raise ValueError('selection shape denied')
                family = item['family']; path = Path(item['path']); project = Path(item['projectPath'])
                if family not in {'fabric', 'findings', 'audit'} or not path.is_absolute() or not project.is_absolute():
                    raise ValueError('explicit absolute selection required')
                if any(part == '..' for part in [*path.parts, *project.parts]):
                    raise ValueError('traversal denied')
                name = path.name
                if '\\' in name or not name or (family in {'fabric', 'findings'} and not name.endswith('.jsonl')) or (family == 'audit' and not name.endswith('.json')):
                    raise ValueError('selected family filename denied')
                anchor = self.root_type(project); roots.append(anchor)
                root = self.root_type(path.parent); roots.append(root)
                self._check([root]); anchor.observe_ancestry()
                limit = 100 * 1024 * 1024 if family == 'audit' else TOTAL
                with root.capture(name, maximum=limit) as captured:
                    identity = captured.info.identity; size = captured.info.size
                key = (anchor.identity, root.identity, name, family)
                if key in seen: raise ValueError('duplicate selected source')
                seen.add(key); total += size
                if total > TOTAL: raise ValueError('aggregate selection limit')
                files.append({'token': uuid.uuid4().hex, 'project': anchor.identity, 'root': root.identity,
                              'name': name, 'family': family, 'identity': identity, 'size': size,
                              '_root': root, '_anchor': anchor, '_limit': limit})
            self._check([entry['_root'] for entry in files])
            token = uuid.uuid4().hex; self.groups[token] = (roots, files)
            # Native device/inode/file IDs may exceed JavaScript's exact integer
            # range. Namespace transport is explicitly lossless text, while
            # expected leaf identities remain native tuples inside this helper.
            descriptors = []
            for entry in files:
                descriptors.append({'token': entry['token'], 'project': [str(part) for part in entry['project']],
                                    'root': [str(part) for part in entry['root']], 'name': entry['name'],
                                    'family': entry['family'], 'size': entry['size']})
            return {'token': token, 'sources': descriptors}
        except BaseException:
            for root in reversed(roots): root.close()
            raise

    def page(self, group, token, offset, length):
        """Read a bounded page pinned to the admitted leaf, allowing append between captures.

        Args:
            group: Previously admitted helper group token.
            token: Previously admitted file token within that group.
            offset: Unsigned decimal byte offset.
            length: Integer page size in 1..256 KiB.
        Returns:
            Base64 exact bytes, decoded length and finite-capture EOF.
        Raises:
            ValueError: Foreign/stale tokens, bounds, overlap or changed/unsafe source.
            OSError: Secure native acquisition/read fails.
        """
        if not isinstance(offset, str) or not offset.isascii() or not offset.isdigit() or len(offset) > 20 or (len(offset) > 1 and offset[0] == '0'):
            raise ValueError('unsigned offset required')
        if type(length) is not int or not 1 <= length <= PAGE: raise ValueError('page size limit')
        roots, files = self.groups[group]
        entry = next(item for item in files if item['token'] == token)
        self._check([item['_root'] for item in files])
        for item in files: item['_anchor'].observe_ancestry()
        # Recount fresh lengths before every action: legitimate appends cannot
        # turn an admitted bounded selection into unbounded aggregate work.
        total = 0; lengths = {}
        for item in files:
            with item['_root'].capture(item['name'], maximum=item['_limit'], expected_identity=item['identity']) as captured:
                total += captured.info.size; lengths[item['token']] = captured.info.size
        if total > TOTAL: raise ValueError('aggregate selection limit')
        with entry['_root'].capture(entry['name'], maximum=entry['_limit'], expected_identity=entry['identity']) as captured:
            if total - lengths[token] + captured.info.size > TOTAL:
                raise ValueError('aggregate selection limit')
            data = captured.read_page(int(offset), length)
            result = {'bytesBase64': base64.b64encode(data).decode('ascii'), 'byteLength': len(data),
                      'eof': int(offset) + len(data) == captured.info.size}
        self._check([item['_root'] for item in files])
        return result

    def release(self, token):
        """Close all native handles in one known group; repeated release is harmless.

        Args:
            token: Helper-issued group identifier; an unknown/released group is a no-op.
        """
        if self.semantic is not None: self.semantic.release_group(token)
        group = self.groups.pop(token, None)
        if group:
            for root in reversed(group[0]): root.close()

    def close(self):
        """Release all capabilities and write-root observations without modifying files."""
        for token in list(self.groups): self.release(token)
        for root in reversed(self.writes): root.close()
        self.writes.clear()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError('duplicate field')
        result[key] = value
    return result


def _encode_wire(value):
    """Encode inert JSON using UTF-8 while preserving isolated surrogate escapes."""
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8', 'backslashreplace')


def main():
    """Run bounded read-only transport without loading the canonical runtime.

    An absolute legacy development argument is accepted but never imported or
    added to the module search path. Frozen builds resolve bundled viewer modules.
    """
    if len(sys.argv) not in {1, 2}: return 2
    if len(sys.argv) == 2:
        if not Path(sys.argv[1]).is_absolute(): return 2
        # Retain the old launcher shape without granting a module search path.
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    elif not getattr(sys, 'frozen', False):
        return 2
    from readonly_files import ReadOnlyRoot
    reader = None
    try:
        while True:
            line = sys.stdin.buffer.readline(FRAME + 1)
            if not line: break
            if len(line) > FRAME or not line.endswith(b'\n'): return 2
            request_id = None
            try:
                request = json.loads(line, object_pairs_hook=_pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
                request_id = request['id']; operation = request['operation']; args = request['args']
                if type(request_id) is not int or set(request) != {'id', 'operation', 'args'}: raise ValueError()
                if operation == 'configure' and reader is None:
                    reader = Reader(ReadOnlyRoot, args['writeRoots']); result = True
                elif operation == 'admit' and reader is not None: result = reader.admit(args['selections'])
                elif operation.startswith('semantic.') and reader is not None:
                    if reader.semantic is None:
                        from semantic_reader import SemanticReader
                        reader.semantic = SemanticReader(reader)
                    semantic = reader.semantic
                    if operation == 'semantic.begin': result = semantic.begin(args['group'], args['sources'], args['limits'])
                    elif operation == 'semantic.chunk': result = semantic.chunk(args['group'], args['lease'], args['cursor'])
                    elif operation == 'semantic.page':
                        data, eof = semantic.page(args['group'], args['lease'], args['capture'], args['offset'], args['length'])
                        result = {'bytesBase64': base64.b64encode(data).decode('ascii'), 'byteLength': len(data), 'eof': eof}
                    elif operation == 'semantic.release': semantic.release(args['group'], args['lease']); result = True
                    else: raise ValueError()
                elif operation == 'page' and reader is not None: result = reader.page(args['group'], args['token'], args['offset'], args['length'])
                elif operation == 'release' and reader is not None: reader.release(args['group']); result = True
                else: raise ValueError()
                response = {'id': request_id, 'ok': True, 'result': result}
            except (ValueError, OSError, KeyError, TypeError, StopIteration, OverflowError, RecursionError, MemoryError) as error:
                diagnostic = getattr(error, 'diagnostic', None)
                response = {'id': request_id, 'ok': False, 'error': {'diagnostic': diagnostic, 'report': getattr(error, 'report', None), 'compatibility': getattr(error, 'compatibility', [])} if diagnostic is not None else 'secure read denied'}
            encoded = _encode_wire(response) + b'\n'
            if len(encoded) > FRAME: return 2
            sys.stdout.buffer.write(encoded); sys.stdout.buffer.flush()
    finally:
        if reader is not None: reader.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
