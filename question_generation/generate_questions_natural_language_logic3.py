# LoRA_Natural_Language_Generation
# logic3_qa_and_or_not.csv and logic3_qa_not_and_or.csv and 

import random
import pandas as pd

# Read the csv file
df = pd.read_csv("/home/jingying/LoRA/logic3_visible_full_and_or_not.csv")

# Rename columns
df = df.rename(columns={'question': 'question_template', 'visible_object': 'visual_features', 'limited_ans':'answers'})

# Add new columns with given values
# Add logical_operator column, remove NaN in not_x, add not_x + combine_x, if NaN, remove ,. 
df['not_x'] = df['not_x'].fillna('')
df['logical_operator'] = df['and_x'] + ', ' + df['not_x'] + ', ' + df['or_x']
df['logical_operator'] = df['logical_operator'].str.replace(", ,", ",")  # Remove ", ," caused by NaN
df['logical_operator'] = df['logical_operator'].str.lstrip(', ')

df['logical_level'] = 'level 3'

# Add'logical_type' column based on 'logical_operator'
def get_logical_type(val):
    if val == 'and, not, or':
        return 'conjunction, negation, disjunction'
    elif val == 'and, or':
        return 'conjunction, disjunction'
    else:
        return ''
    

df['logical_type'] = df['logical_operator'].apply(get_logical_type)

# Generate questionId and imageId. 
df['questionId'] = [f'{i:07d}' for i in range(3100000, 3100000 + df.shape[0])]
df['imageId'] = ['lora_logic3_{:07d}'.format(i) for i in range(3100000, 3100000 + df.shape[0])]

# Put questionID in the first column. 
# df = df[['questionId'] + [col for col in df.columns if col != 'questionId']]
df.reset_index(drop=True, inplace=True)

# Natural Language processing to both questions and answers.

# Define the relation dictionaries
relation_dict = {
    "has_color": ["has a color of", "is colored", "shows the color"],
    "has_shape": ["has a shape like", "is shaped", "appears in shape"],
    "has_taste": ["has a taste of", "tastes like", "holds a flavor of"],
    "has_nutrition": ["has nutritional content of", "is nutritious with", "contains nutrition"],
    "original_from": ["originates from", "is originally from", "comes from"],
    "is_ingredient_of": ["is an ingredient of", "is used in", "can be found in"],
    "has_ingredient": ["has ingredient", "contains", "includes"],
    "is_category_of": ["belongs to the category", "is a type of", "is classified under"],
    "has_edible_part": ["has edible part", "you can eat its", "has consumable"],
    "has_child_food": ["has a child food of", "derives", "gives birth to"],
    "is_cousin_to": ["is a cousin to", "is related to", "has a connection with"],
    "has_seed_inside": ["has seeds inside", "contains seeds", "encloses seeds"],
    "has_dietary_method": ["follows the dietary method", "is consumed under a diet"],
    "has_function": ["has function", "serves the purpose of", "fulfills the function"],
    "raw_and_cooked": ["raw and cooked"],
    "raw_or_cooked": ["raw or cooked"],
    "Vegetable": ["vegetable"]
}


def replace_relations(question):
    for relation, phrases in relation_dict.items():
        if relation in question:
            question = question.replace(relation, random.choice(phrases))
    return question

# question_nl column is use the dictionary to replace question template, but might have grammar errors. 
df['questions'] = df['question_template'].apply(replace_relations)

df['questions'] = df['questions'].replace(r'\bnan\b', '', regex=True)

# Save to csv file. 
df.to_csv('/home/jingying/LoRA/logic3_vqa_full_and_or_not.csv', index=False)
print("logic3_vqa_full shape", df.shape)

# Select columns
df1 = df[['questionId', 'questions', 'a1', 'a2', 'a3', 'answers', 'visual_features', 'logical_operator', 'logical_level', 'logical_type', 'imageId']]
df1.to_csv('/home/jingying/LoRA/Questions/logic3_vqa_and_or_not.csv', index=False)
print("logic3_vqa shape", df1.shape)

# Conver to json file
df1.to_json('/home/jingying/LoRA/Questions/questions_logic3_and_or_not.json', orient='records')


print("natural langauge questions generation logic 3 done")