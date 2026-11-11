# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Development-only failure observer; never selected by normal helper startup."""
import functools
import json
import os
from pathlib import Path
import sys

NAME = 'semantic-cap-diagnostic.json'
SCALARS = ('total', 'encoded_total', 'size')
COUNTS = ('raw', 'facts', 'source_facts')


def observe(error, module):
    """Extract fixed frame coordinates and numeric counters without source values.

    Args:
        error: Original failed begin exception, including its bounded cause chain.
        module: Trusted shipped semantic_reader module; its imported facts helper
            also qualifies by exact module filename, never a directory prefix.
    Returns:
        Bounded JSON-safe record containing no native messages or source paths.
    """
    spool = sys.modules[module._Budget.__module__]
    trusted_files = {module.__file__, spool.__file__}
    chains = []; seen = set()
    while error is not None and id(error) not in seen and len(chains) < 4:
        seen.add(id(error)); frames = []; trace = error.__traceback__
        while trace is not None and len(frames) < 16:
            frame = trace.tb_frame
            if frame.f_code.co_filename in trusted_files:
                item = {'function': frame.f_code.co_name, 'line': trace.tb_lineno}
                values = frame.f_locals
                if frame.f_code.co_name in {'_begin', 'append', 'check'}:
                    for name in SCALARS:
                        value = values.get(name)
                        if type(value) is int and 0 <= value <= 2 ** 63 - 1: item[name] = value
                    for name in COUNTS:
                        value = values.get(name)
                        if type(value) in (bytes, list, tuple): item[name + 'Length'] = len(value)
                    owner = values.get('self')
                    if type(owner) is module._FactList:
                        for name in ('encoded', 'vertices', 'edges'):
                            value = owner.__dict__.get(name)
                            if type(value) is int and 0 <= value <= 2 ** 63 - 1: item[name] = value
                    limits = values.get('limits')
                    budget = owner if type(owner) is module._Budget else owner.__dict__.get('budget') if type(owner) is module._FactList else None
                    if type(budget) is module._Budget:
                        limits = budget.limits
                        for name in ('encoded', 'vertices', 'edges', 'count'):
                            committed = budget.__dict__.get(name)
                            increment = values.get(name) if frame.f_code.co_name == 'check' else None
                            if type(committed) is int and 0 <= committed <= 2 ** 63 - 1:
                                item['committed' + name.title()] = committed
                                if type(increment) is int and 0 <= increment <= 2 ** 63 - 1 - committed:
                                    item['proposed' + name.title()] = committed + increment
                    if type(limits) is dict:
                        item['limits'] = {key: limits[key] for key in ('maxVertices', 'maxEdges', 'maxEncodedGraphBytes') if type(limits.get(key)) is int and 0 <= limits[key] <= 2 ** 63 - 1}
                frames.append(item)
            trace = trace.tb_next
        kind = type(error).__name__
        chains.append({'type': kind if kind in {'SemanticReadError', 'MemoryError', 'ValueError', 'OSError', 'OverflowError', 'RecursionError'} else 'other', 'frames': frames})
        error = error.__cause__ if error.__cause__ is not None else error.__context__
    return {'format': 'jai.fabric-explorer.cap-diagnostic/1', 'exceptions': chains}


def install(module):
    """Wrap only begin, retaining its result, exception identity and traceback.

    Args:
        module: Trusted semantic_reader module imported before raw_reader.main.
    Returns:
        Original callable, available to bounded tests for restoration.
    """
    original = module.SemanticReader.begin
    @functools.wraps(original)
    def begin(self, *args, **kwargs):
        try:
            return original(self, *args, **kwargs)
        except Exception as error:
            try:
                data = json.dumps(observe(error, module), separators=(',', ':'), allow_nan=False).encode()
                if len(data) > 16384: raise ValueError('diagnostic bound')
                descriptor = os.open(NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
                with os.fdopen(descriptor, 'wb') as output: output.write(data + b'\n')
            except Exception:
                print('cap-diagnostic-write-failed', file=sys.stderr)
            raise
    module.SemanticReader.begin = begin
    return original


def main():
    """Invoke the original isolated helper with fixed trusted module locations.

    Returns:
        Original helper exit code; invalid development invocation returns 2.
    """
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_absolute(): return 2
    sys.path[:0] = [str(Path(__file__).resolve().parents[1]), sys.argv[1]]
    import semantic_reader
    import raw_reader
    install(semantic_reader)
    return raw_reader.main()


if __name__ == '__main__':
    raise SystemExit(main())
