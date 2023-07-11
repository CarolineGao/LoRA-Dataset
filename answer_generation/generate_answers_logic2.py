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


# pd.set_option("display.max_rows", None, "display.max_columns", None)

print('ok - import dictionaries')

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
def compute_logical_relation(a1, a1_operator, a2):
    result = []
    
    a1 = set(str(x) for x in a1)
    a2 = set(str(x) for x in a2)
    
    if a1_operator == 'and':
        result = a1.intersection(a2)
    else:
        result = a1.union(a2)

    return result


def generate_answers(df1):
    df1['a1'] = df1.apply(lambda row: get_ontology_answer(row.r1_relation_x, row.e2_entity_x, row.not_x), axis=1)
    df1['a2'] = df1.apply(lambda row: get_ontology_answer(row.r1_relation_y, row.e2_entity_y, not_modifier=False), axis=1)
    fa_set = df1.apply(lambda row: compute_logical_relation(row.a1, row.combine_x,  row.a2), axis=1)
    fa_list = fa_set.apply(list)
    fa_string = list(map(''.join, fa_list))
    df1['fa'] = fa_string
    return df1

def main():
    # Read csv
    lde = pd.read_csv("/home/jingying/LoRA/lde.csv")
    print(lde.shape)
    z = generate_answers(lde) 
    z.to_csv("/home/jingying/LoRA/logic2_fa.csv")
    return z

main()