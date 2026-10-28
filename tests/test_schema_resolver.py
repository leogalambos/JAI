# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Release-scope stdlib validation agrees with the maintained JSON Schema."""
import copy
import json
from pathlib import Path
import sys

import jsonschema
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
import schema_resolver


def resources(tmp_path, data, rules=None):
    schema=tmp_path/'schema';schema.mkdir(exist_ok=True)
    (schema/'release-scope.schema.json').write_text(json.dumps(rules if rules is not None else json.loads((ROOT/'.ai/runtime/schema/release-scope.schema.json').read_text())))
    (tmp_path/'RELEASE-SCOPE.json').write_text(json.dumps(data))


def test_release_scope_stdlib_matches_jsonschema_for_valid_and_invalid_values(tmp_path):
    canonical=json.loads((ROOT/'RELEASE-SCOPE.json').read_text())
    rules=json.loads((ROOT/'.ai/runtime/schema/release-scope.schema.json').read_text())
    cases=[canonical,dict(canonical,enabled=[]),dict(canonical,enabled=canonical['enabled'][:1]),dict(canonical,scope='GA_COMPATIBLE/19')]
    for key in canonical:
        missing=copy.deepcopy(canonical);del missing[key];cases.append(missing)
        for value in (None,True,False,0,1,{},[],['unknown'],'unknown'):
            cases.append(dict(canonical,**{key:value}))
    cases.extend([None,[],False,dict(canonical,extra=True),dict(canonical,schema_version=True),dict(canonical,schema_version=1.0),dict(canonical,enabled=canonical['enabled']*2),dict(canonical,scope='GA_COMPATIBLE/0'),dict(canonical,hardened_privileged={'enabled':0,'qualification':'NOT QUALIFIED'})])
    validator=jsonschema.Draft202012Validator(rules)
    for case in cases:
        resources(tmp_path,case,rules)
        expected=validator.is_valid(case)
        try:schema_resolver.release_scope(tmp_path);actual=True
        except ValueError:actual=False
        assert actual==expected,case


@pytest.mark.parametrize('mutation', ['unknown-keyword','unknown-nested-keyword','invalid-type','invalid-pattern','duplicate-enum','duplicate-required','additional-properties','missing-items','malformed-properties','boolean-schema'])
def test_release_scope_rejects_unsupported_or_malformed_schemas(tmp_path,mutation):
    rules=json.loads((ROOT/'.ai/runtime/schema/release-scope.schema.json').read_text())
    if mutation=='unknown-keyword':rules['allOf']=[]
    elif mutation=='unknown-nested-keyword':rules['properties']['enabled']['minItems']=1
    elif mutation=='invalid-type':rules['type']='unsupported'
    elif mutation=='invalid-pattern':rules['properties']['scope']['pattern']='['
    elif mutation=='duplicate-enum':rules['properties']['enabled']['items']['enum']=['same','same']
    elif mutation=='duplicate-required':rules['required'].append(rules['required'][0])
    elif mutation=='additional-properties':rules['additionalProperties']=True
    elif mutation=='missing-items':del rules['properties']['enabled']['items']
    elif mutation=='malformed-properties':rules['properties']=[]
    elif mutation=='boolean-schema':rules=True
    resources(tmp_path,json.loads((ROOT/'RELEASE-SCOPE.json').read_text()),rules)
    with pytest.raises(ValueError):schema_resolver.release_scope(tmp_path)


@pytest.mark.parametrize('resource',['RELEASE-SCOPE.json','schema/release-scope.schema.json'])
def test_release_scope_rejects_symlink_resources(tmp_path,resource):
    resources(tmp_path,json.loads((ROOT/'RELEASE-SCOPE.json').read_text()))
    source=tmp_path/resource;target=tmp_path/'target.json';source.rename(target);source.symlink_to(target)
    with pytest.raises(ValueError):schema_resolver.release_scope(tmp_path)


def test_release_scope_vocabulary_and_revision_are_read_from_schema(tmp_path):
    rules=json.loads((ROOT/'.ai/runtime/schema/release-scope.schema.json').read_text())
    data=json.loads((ROOT/'RELEASE-SCOPE.json').read_text())
    rules['properties']['enabled']['items']['enum']=['future-maintained-capability']
    rules['properties']['scope']['pattern']='^FUTURE/[1-9][0-9]*$'
    data['scope']='FUTURE/3';data['enabled']=['future-maintained-capability']
    resources(tmp_path,data,rules)
    assert schema_resolver.release_scope(tmp_path)==data


@pytest.mark.parametrize('resource',['RELEASE-SCOPE.json','schema/release-scope.schema.json'])
def test_release_scope_rejects_ambiguous_or_non_json_resource(tmp_path,resource):
    resources(tmp_path,json.loads((ROOT/'RELEASE-SCOPE.json').read_text()))
    for malformed in ('{"scope":1,"scope":2}','{"scope":NaN}','{'):
        (tmp_path/resource).write_text(malformed)
        with pytest.raises(ValueError):schema_resolver.release_scope(tmp_path)
