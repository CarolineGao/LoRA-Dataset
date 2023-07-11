# import libraries
import pandas as pd
from pprint import pprint
import numpy as np


def generate_questions(df):
    # Create the question template
    question_template = df.e1_classes.str.cat(sep=' ', others=[
        pd.Series(['in the image'] * len(df)).values,
        df.r1_relation_x, df.e2_entity_x, 
        pd.Series(['and'] * len(df)).values, 
        df.r1_relation_y, df.e2_entity_y, 
        pd.Series(['or'] * len(df)).values,  
        pd.Series(['not'] * len(df)).values,
        df.r1_relation, df.e2_entity 
    ])

    # Generate logic_3_questions
    logic_3_questions = 'Which ' + question_template

    # Create a new dataframe with the constructed question and other columns
    logic3_qa_full = pd.DataFrame({
        'question': logic_3_questions,
        'e1_classes': df['e1_classes'],
        'r1_relation_x': df['r1_relation_x'],
        'e2_entity_x': df['e2_entity_x'],
        'and_x': pd.Series(['and'] * len(df)).values,
        'r1_relation_y': df['r1_relation_y'],
        'e2_entity_y': df['e2_entity_y'],
        'or_x': pd.Series(['or'] * len(df)).values,
        'not_x': pd.Series(['not'] * len(df)).values,
        'r1_relation': df['r1_relation'],
        'e2_entity': df['e2_entity']
    })

    # Deduplicate based on 'question' and drop NaNs
    logic3_qa_full = logic3_qa_full.drop_duplicates(subset=['question']).dropna(subset=['question'])
    
    return logic3_qa_full


def main():
    # Read csv
    c3e = pd.read_csv("/home/jingying/LoRA/c3e.csv", dtype=str)
    c3e2 = c3e[1:10]
    print(c3e.shape)
    
    logic3_qa_full = generate_questions(c3e2)
    print(logic3_qa_full.shape)
    
    logic3_qa_full.to_csv("/home/jingying/LoRA/test.csv")
    print("File saved")


main()
print("done")