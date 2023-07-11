# Import Pandas, Numpy
from ontology import onto, graph
import pandas as pd
from pprint import pprint
import numpy as np
import re
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

import dask.dataframe as dd
from dask.dataframe import from_pandas
import dask.array as da
import vaex as vx
from itertools import chain
import warnings
warnings.filterwarnings("ignore")

# JY, - Import dictionaries
# Import OWLReady
import owlready2
from owlready2 import *
from itertools import chain
import rdflib
#import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
graph = default_world.as_rdflib_graph()
import time

# pd.set_option("display.max_rows", None, "display.max_columns", None)

print('ok - import dictionaries')

start_time = time.time()

# Time for Logic - Step 4 - Generate logic_2 answers and add 'a1', 'a2', 'fa' to Table: lde. 
# Answer Step4.1 - Dynamic query 'a1', 'a2' and add to Table: lde. 
def query_ontology(relation_name, entity_name):
    query = "PREFIX onto: <" + onto.base_iri + """> SELECT ?s
    WHERE {
        ?s rdf:type ?type. ?type rdfs:subClassOf+ onto:Food .
        """ + f"""
        ?s onto:{relation_name} onto:{entity_name} .
        """ + '}'
    r1 = list(graph.query_owlready(query))
    return r1    

def get_ontology_answer(relation_name, entity_name, not_modifier=False):
    if not_modifier == "not":
        query = "PREFIX onto: <" + onto.base_iri + """> SELECT ?s 
        WHERE {
            ?s rdf:type ?type. ?type rdfs:subClassOf+ onto:Food . 
            FILTER NOT EXISTS { """  + f""" ?s onto:{relation_name} onto:{entity_name} . """ + \
            """} FILTER NOT EXISTS {?s rdfs:subClassOf ?t . } }""" 
        r2 = list(graph.query_owlready(query)) 
        return r2 
    else:
        results:list = query_ontology(relation_name, entity_name)
        return results

# Define compute_logical_relation function, compute 'fa' answer and add to Table: lde. 
def compute_logical_relation(a1, a1_operator, a2, a2_operator, a3):
    result = []
    
    # a1,a2,a3 = [set() if a == 'not_answer' else set(a) for a in [a1,a2,a3]]
    a1, a2, a3 = set(str(x) for x in a1), set(str(x) for x in a2), set(str(x) for x in a3)
    
    if a1_operator == 'and':
        result1 = a1.intersection(a2)
    else:
        result1 = a1.union(a2)

    if a2_operator == 'and':
        result = result1.intersection(a3)
    else:
        result = result1.union(a3)

    return result


# def generate_answers(df1):
#     for idx, (modifier, relation, entity, col) in enumerate([
#         (df1.not_x, df1.r1_relation_x, df1.e2_entity_x, 'a1'),
#         (False, df1.r1_relation_y, df1.e2_entity_y, 'a2'),
#         (False, df1.r1_relation, df1.e2_entity, 'a3')
#     ]):
#         answers = df1.apply(lambda row: get_ontology_answer(row.e1_classes, relation, entity, modifier), axis=1)
#         filter_function = lambda item: item if isinstance(item, str) else ' '.join(item)
#         df1[col] = [filter_function(val) for val in answers]

#     fa_set = df1.apply(lambda row: compute_logical_relation(row.a1, row.combine_x,  row.a2, row.combine_y, row.a3), axis=1)
#     df1['fa'] = list(map(''.join, fa_set.apply(list)))
    
#     return df1


def generate_answers(df1):
    
    df1['a1'] = df1.apply(lambda row: get_ontology_answer(row.r1_relation_x, row.e2_entity_x, not_modifier=False), axis=1)
    df1['a2'] = df1.apply(lambda row: get_ontology_answer(row.r1_relation_y, row.e2_entity_y, not_modifier=False), axis=1)
    df1['a3'] = df1.apply(lambda row: get_ontology_answer(row.r1_relation, row.e2_entity, row.not_x), axis=1)
    fa_set = df1.apply(lambda row: compute_logical_relation(row.a1, row.and_x,  row.a2, row.or_x, row.a3), axis=1)
    df1['fa'] = list(map(''.join, fa_set.apply(list)))
    
    return df1


def main():
    # Read csv
    c3e = pd.read_csv("/home/jingying/LoRA/logic3_q_and_or_not.csv")
    print(c3e.shape)
    z = generate_answers(c3e) 
    z.to_csv("/home/jingying/LoRA/logic3_qa_and_or_not.csv")
    print(z.shape)
    return z

main()
end_time = time.time()
print("done", (end_time - start_time)/60, "mins")