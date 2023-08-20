"""
Unroll Ontology Algorithm
This functions can be used to unroll an ontology into a table format. 
This is used for generating sentences from an ontology. 
It can be used for any ontology which uses OWL format. 
"""

from ontology import onto, graph
import numpy as np
import pandas as pd
from pprint import pprint
import re

# JY, - First part - Unroll ontology 
# --- First method set, recursive methods to turn objects and relations into some sort of consistent format ---
# --- Output: list of tuples to represent the entity and all its relationships including a depth tracker ---

# recursive method to get class hierarchy
def get_types_hierarchy(x):
    if issubclass(x, Thing):
        # to filter out Thing's, uncomment below
        # if x is not Thing:
        return [x, *get_types_hierarchy(x.__bases__[0])]
    return []

# gets a tuple representing a relationship (recursive with get_object_pairs)
def get_relation_pairs(o, depth=1):
    if depth >= 10:
        print('Warning, depth of 10 hit, check for cycles')
        return []
    return [('relation', p, get_object_pairs(getattr(o, p._name), depth=depth+1)) 
    for p in o.get_properties() if ObjectPropertyClass]

# gets a tuple representing a pair of objects (recursive with get_relation_pairs), [0, 1, 2, 3] = [entity, types, x, relation_pairs]
def get_object_pairs(objects, limit_domain=[], depth=1):
    return [(
        'entity',
        get_types_hierarchy(type(x)),
        x,
        get_relation_pairs(x, depth))
        for x in objects 
        if len(limit_domain)==0 or any([isinstance(x, y) for y in limit_domain])]


# --- JY - Get ready to build a table from unrolled ontology. 
# --- Second method set, recursive method sets to unroll the hierarchy, ---
# --- Output: collapsed list of dicts with each level of entity/relationship numbered as e1/r1, e2/r2 etc. ---

# works with dictify to flatten out the hierarchy to a one-dict per entity/relationship combination including recurse
def dict_collapse(e, depth=1):
    has_relationships = len(e[3])>0
    if has_relationships:
        return [{f'e{depth}': e[0:3], f'r{depth}': r[0:2], 'n': dictify(r[2], depth+1)} for r in e[3]]
    else:
        return [{f'e{depth}': e[0:3], f'r{depth}': None, 'n': []}]

# removes the "n" column which is used to indicate another level of recursion
def drop_n(d):
    return {k:v for k,v in d.items() if k!='n'}

# helper to flatten nested lists, put two sublists into a combined list. 
def flatten(l):
    return list(chain.from_iterable(l))

# Removes a single level of recursion then calls itself again
def flatten_dicts(dict_list):
    # handle case of no next level and case of having a next level then recurse
    recursed_set = [{**drop_n(e), **n} for e in dict_list for n in e['n']]
    if any(['n' in e for e in recursed_set]):
        recursed_set = flatten_dicts(recursed_set)
    return recursed_set + \
        [drop_n(e) for e in dict_list if len(e['n'])==0]

# controller method to orchestrate the other 2
def dictify(object_pairs, depth=1):
    if depth >= 10:
#         print('Warning, depth of 10 hit, check for cycles')
        return []
    collapsed_dicts = flatten([dict_collapse(e, depth) for e in object_pairs])
    return flatten_dicts(collapsed_dicts)

# --- JY Build the table 
# --- Third method set, no more recursion, these methods are just helpful to coerce to a table-like format, could easily write your own methods instead :) ---
# --- Output: dictionary with an entity or list of classes per column making it easier to filter and work with ---

# convert the whole ontology to a table format
from collections import ChainMap
def tablify(object_tuple_dict):
    def generate_entity_dict(k, v):
        if v is None:
            return {}
        elif v[0]=='entity':
            return {f'{k}_classes': v[1], f'{k}_entity': v[2]}
        else:
            return {f'{k}_relation': v[1]}
        
    return [dict(ChainMap(*[generate_entity_dict(k,v) for k,v in x.items()])) for x in object_tuple_dict]

# convert all the entities and classes to strings for easy sentence generation
def stringify_table(dict_table_format):
    return [{k: [x.name for x in v] if isinstance(v, list) else v._name for k,v in x.items()} for x in dict_table_format]

print('ok-Unroll Ontology Functions')
# --- Actually using the above methods! ---

# --- Time for logic - part1 ---
multi_space = re.compile('\\s+')
multi_space_v = np.vectorize(lambda x: multi_space.sub(' ', x))

def unique_concat(*args):
    return np.char.array(multi_space_v(np.unique(np.concatenate(args))))

# The below code is the print the unique indices of np.unique. 
# np.unique has a return which is the indices of the input array that give the unique values

# def unique_concat(*args):
#     print(f"{args}")
#     np_unique_index = np.unique(np.concatenate(args), return_index=True)
#     print(list(np_unique_index[1]))
#     return np.char.array(multi_space_v(np_unique_index[0]))

print('ok-Time for logic: run unique_concat function')


# these 2 do the main bulk of the work, you could happily write a function to process object_tuple_dict directly

# NOTE: HERE YOU NEED TO CHANGE onto.Vegetable or onto.Food or onto.Fruit!

object_pairs = get_object_pairs(onto.individuals(), [onto.Vegetable])
object_tuple_dict = dictify(object_pairs)

# or use these to get a table sort of format that we can do further processing on to generate questions!
dict_table_format = tablify(object_tuple_dict)
string_table = stringify_table(dict_table_format)

# can make an entity df with the individuals/classes if you want to access properties and inspect them, etc.
# entity_df = pd.DataFrame(dict_table_format)
# entity_df.explode('e2_classes').explode('e1_classes')
table_cols_threelevels = ['e1_classes', 'e1_entity', 'r1_relation', 'e2_classes', 'e2_entity', 'r2_relation', 'e3_classes', 'e3_entity']

# or can make a string df use the "string_table" for sentence generation purposes
string_df = pd.DataFrame(string_table)[table_cols_threelevels].fillna('').query("r1_relation!=''")
string_df

print('print ontology is unrolled to a table dataframe')

