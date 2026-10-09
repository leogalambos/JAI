#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Resolve runtime schemas through explicit, versioned contract registry paths."""
from __future__ import annotations
import argparse, json
from pathlib import Path
RUNTIME=Path(__file__).resolve().parents[1]
RELEASE=(RUNTIME/'VERSION').read_text().strip()
REGISTRY=RUNTIME/'schema/schema-registry.json'

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))

def registry():
    r=load(REGISTRY)
    return r

def schema_path(name):
    matches=[x for x in registry().get('schemas',[]) if x.get('name')==name]
    if len(matches)!=1: raise KeyError(f"schema {name!r}: expected exactly one registry entry, got {len(matches)}")
    p=RUNTIME/matches[0]['path']
    if not p.is_file(): raise FileNotFoundError(p)
    if p.resolve() != (RUNTIME / matches[0]['path']).resolve() or not p.resolve().is_relative_to((RUNTIME/'schema').resolve()):
        raise ValueError(f"schema {name!r} escapes the trusted schema directory")
    return p

def schema(name): return load(schema_path(name))

def self_test():
    problems=[]
    try: r=registry()
    except Exception as e: print('FAIL registry',e); return 1
    for item in r.get('schemas',[]):
        try:
            p=schema_path(item['name']); doc=load(p)
            if doc.get('$id')!=f"https://ai-it-house.local/{item['path']}": problems.append(f"{item['name']}: $id drift")
        except Exception as e: problems.append(f"{item.get('name')}: {e}")
    if problems:
        for x in problems: print('FAIL',x)
        return 1
    print(f"PASS current schema resolver: {len(r.get('schemas',[]))} registered schemas (independent of product VERSION)")
    return 0

def main():
    p=argparse.ArgumentParser(); p.add_argument('cmd',choices=['self-test','path']); p.add_argument('name',nargs='?'); a=p.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    if not a.name: raise SystemExit('schema name required')
    print(schema_path(a.name))
if __name__=='__main__': main()
