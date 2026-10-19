# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Apply explicit synthetic evaluation recipes without observing expected results."""
import copy


def apply_variant(reference, variant):
    """Return a mutated deep copy of reference using the variant recipe.

    reference is a synthetic case dictionary; variant identifies an operation
    and its arguments. The original remains unchanged. Raises ValueError for
    unknown operations or KeyError for a malformed authored recipe.
    """
    result=copy.deepcopy(reference);units=result['semantic_units'];op=variant['operation'];field=variant.get('field')
    if op=='headings_only':result['semantic_units']={k:'' for k in units}
    elif op=='append_irrelevant':result['irrelevant_annex']=variant['text']
    elif op=='remove':del units[field]
    elif op=='unsupported_claim':result['claims']=[{'text':variant['text'],'material':True,'evidence_refs':[]}]
    elif op=='repeat':result['repeated_content']=[copy.deepcopy(units[field]) for _ in range(variant['count'])]
    elif op=='mark_na':units[field]={'status':'not_applicable','reason':variant['reason']}
    elif op=='unknown_context':result['context'][field]=None
    elif op=='unauthorised_exception':
        result['context']['regulatory_requirement']=True
        units[field]={'status':'waived','reason':variant['text'],'authority_ref':None}
    elif op=='justified_conditional_na':
        result['context'].update(variant['context'])
        result['scenario']['privacy']=False
        result['scenario']['scope']='Anonymous stock-count service; no account, operator or transaction personal identifiers.'
        result['applicability_evidence']={'id':'SYN-NA','description':variant['justification'],'classification':'synthetic-scope-alternative'}
        units[field]={'status':'not_applicable','reason':variant['justification'],'evidence_refs':['SYN-NA']}
    else:raise ValueError(op)
    return result

