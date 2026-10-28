#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Resolve runtime schemas through explicit, versioned contract registry paths."""
from __future__ import annotations
import argparse, json, re
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

def _release_json(path):
    """Reject ambiguous/non-JSON input rather than normalizing its constraints."""
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate JSON property: '+key)
            result[key]=value
        return result
    def invalid_constant(value):
        raise ValueError('non-JSON numeric constant: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=pairs,
                      parse_constant=invalid_constant)


def _release_schema(node, root=False):
    """Validate only the maintained release-scope schema dialect, fail closed."""
    if not isinstance(node,dict) or not node:raise ValueError('release scope schema must be a nonempty object')
    metadata={'$schema','title'} if root else set()
    if root and node.get('$schema')!='https://json-schema.org/draft/2020-12/schema':
        raise ValueError('unsupported release scope schema dialect')
    if 'title' in node and not isinstance(node['title'],str):raise ValueError('invalid schema title')
    keys=set(node)-metadata
    if keys=={'const'}:
        if type(node['const']) not in {str,int,bool}:raise ValueError('unsupported release scope constant')
        return
    if keys=={'enum'}:
        values=node['enum']
        if (not isinstance(values,list) or not values or any(type(item) is not str for item in values)
                or len(values)!=len(set(values))):raise ValueError('invalid release scope enum')
        return
    kind=node.get('type')
    if kind=='object' and keys=={'type','properties','required','additionalProperties'}:
        properties=node['properties'];required=node['required']
        if (not isinstance(properties,dict) or not properties or not isinstance(required,list)
                or any(type(key) is not str for key in required)
                or len(required)!=len(set(required)) or not set(required)<=set(properties)
                or node['additionalProperties'] is not False):
            raise ValueError('invalid or unsupported release scope object schema')
        for child in properties.values():_release_schema(child)
    elif kind=='array' and keys=={'type','items','uniqueItems'}:
        if node['uniqueItems'] is not True:raise ValueError('release scope arrays require unique items')
        _release_schema(node['items'])
    elif kind=='string' and keys=={'type','pattern'}:
        if not isinstance(node['pattern'],str):raise ValueError('invalid release scope pattern')
        try:re.compile(node['pattern'])
        except re.error as exc:raise ValueError('invalid release scope pattern') from exc
    else:
        raise ValueError('unsupported release scope schema shape or keyword')


def _release_value(value, node, location='$'):
    """Apply prevalidated release-scope constraints with JSON boolean semantics."""
    if 'const' in node:
        constant=node['const']
        if (isinstance(value,bool)!=isinstance(constant,bool)) or value!=constant:
            raise ValueError(location+': release scope constant mismatch')
    elif 'enum' in node:
        if value not in node['enum']:raise ValueError(location+': unknown release scope value')
    elif node['type']=='object':
        if not isinstance(value,dict):raise ValueError(location+': object required')
        if not set(node['required'])<=set(value) or not set(value)<=set(node['properties']):
            raise ValueError(location+': missing or unexpected release scope properties')
        for key,item in value.items():_release_value(item,node['properties'][key],location+'.'+key)
    elif node['type']=='array':
        if not isinstance(value,list):raise ValueError(location+': array required')
        for index,item in enumerate(value):
            _release_value(item,node['items'],location+'['+str(index)+']')
            if item in value[:index]:raise ValueError(location+': duplicate release scope item')
    elif not isinstance(value,str) or re.search(node['pattern'],value) is None:
        raise ValueError(location+': release scope string pattern mismatch')


def release_scope(root=None):
    """Read the sole release capability declaration using its required schema.

    Args:
        root: Trusted source-package or installed-runtime root; defaults to this
            module's runtime, never the current workspace or an environment flag.
    Returns:
        Fresh validated RELEASE-SCOPE.json data; schema vocabulary describes
        implemented features, not a second list of enabled capabilities.
    Raises:
        OSError, ValueError: Missing, malformed or symlinked manifest/schema.
        ValueError: Invalid declaration or malformed/unsupported schema. Only the
            maintained const/enum, closed object, unique array and patterned
            string dialect is supported; unknown schema shapes fail closed.
            Validation uses the standard library, without a jsonschema fallback.
    """
    base=Path(root) if root is not None else RUNTIME
    if base.name=='runtime' and base.parent.name=='.ai' and (base.parent/'setup/installer.py').is_file():
        base=base.parent.parent
    if (base/'.ai/runtime').is_dir():
        runtime=base/'.ai/runtime';manifest=base/'RELEASE-SCOPE.json'
    elif base.name=='runtime' and base.parent.name=='.ai' and (base/'RELEASE-SCOPE.json').exists() and (base.parent.parent/'RELEASE-SCOPE.json').exists():
        raise ValueError('ambiguous source and installed release scope roots')
    else:
        runtime=base;manifest=base/'RELEASE-SCOPE.json'
    spec=runtime/'schema/release-scope.schema.json'
    if manifest.is_symlink() or spec.is_symlink():
        raise ValueError('release scope and validation schema must be regular resources')
    data=_release_json(manifest);rules=_release_json(spec)
    _release_schema(rules,root=True)
    _release_value(data,rules)
    return data


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
