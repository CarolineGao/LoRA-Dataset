# Import dictionaries
import pandas as pd
from pprint import pprint
import numpy as np
import re
import dask.dataframe as dd
from dask.dataframe import from_pandas
import dask.array as da
import vaex as vx
from itertools import chain
import warnings
warnings.filterwarnings("ignore")
multi_space = re.compile('\\s+')
multi_space_v = np.vectorize(lambda x: multi_space.sub(' ', x))

print('ok - import dictionaries')

# Read ontology and answers dataframe. 
logic2_fa = pd.read_csv("/home/jingying/LoRA/logic2_fa.csv")

# Convert all relevant columns to strings
columns = ['e1_classes', 'not_x', 'r1_relation_x', 'e2_entity_x', 'combine_x', 'r1_relation_y', 'e2_entity_y']
logic2_fa[columns] = logic2_fa[columns].applymap(str)

# Generate logic_2_questions
logic_2_questions = 'Which ' + logic2_fa.e1_classes.str.cat(sep=' ', others=[
    logic2_fa['not_x'], logic2_fa.r1_relation_x, 
    logic2_fa.e2_entity_x, logic2_fa['combine_x'], 
    logic2_fa.r1_relation_y, logic2_fa.e2_entity_y
])

# Create the logic_2 dataframe
logic2_qa_full = pd.DataFrame({
    'question': logic_2_questions,
    'not_x': logic2_fa['not_x'], 
    'r1_relation_x': logic2_fa['r1_relation_x'], 
    'e2_entity_x': logic2_fa['e2_entity_x'], 
    'combine_x': logic2_fa['combine_x'], 
    'r1_relation_y': logic2_fa['r1_relation_y'], 
    'e2_entity_y': logic2_fa['e2_entity_y'], 
    'a1': logic2_fa['a1'], 
    'a2': logic2_fa['a2'], 
    'fa': logic2_fa['fa']
})

# Deduplicate based on 'question' and drop NaNs
logic2_qa_full = logic2_qa_full.drop_duplicates(subset=['question'])
logic2_qa_full = logic2_qa_full.dropna(subset=['question'])

logic2_qa_full.to_csv("/home/jingying/LoRA/logic2_qa_full.csv")
print(logic2_qa_full.shape)

