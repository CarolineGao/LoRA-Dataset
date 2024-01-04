import csv
import random
import re

def save_as_csv(results, filename, headers=None):
    csv_file_path = filename
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers or ['Question', 'fa'])
        csv_writer.writerows(results)

    print(f"Results saved to {csv_file_path}")

relation_dict = {
    "has_color": ["has a color of", "is colored", "shows the color"],
    "has_shape": ["has a shape like", "is shaped", "appears in shape"],
    "has_taste": ["has a taste of", "tastes like", "holds a flavor of"],
    "has_nutrition": ["has nutritional content of", "is nutritious with", "contains nutrition"],
    "original_from": ["originates from", "is originally from", "comes from"],
    "is_ingredient_of": ["is an ingredient of", "is used in", "can be found in"],
    "has_ingredient": ["has ingredient", "contains", "includes"],
    "is_category_of": ["belongs to the category", "is a type of", "is classified under"],
    "has_edible_part": ["has edible part", "has consumable"], #"you can eat its",
    "has_child_food": ["has a child food of", "derives"], # "gives birth to"
    "is_cousin_to": ["is a cousin to", "is related to", "has a connection with"],
    "has_seed_inside": ["has seeds inside", "contains seeds", "encloses seeds"],
    "has_dietary_method": ["follows the dietary method", "is consumed under a diet"],   
    "has_function": ["has function", "serves the purpose of", "fulfills the function"],
    "raw_and_cooked": ["raw and cooked"],
    "raw_or_cooked": ["raw or cooked"],
    "Vegetable": ["vegetable"],
    "Which fruit": ["Which fruit in the image", "Which fruit on the table", "Identify the fruit in the image that"],
    "Which dairy or poultry product": ["Which dairy or poultry product in the image", "Which dairy or poultry product on the table", "Identify the dairy or poultry product in the image that"],
    "not is": ["is not"],
    "not has": ["does not have"],
    "not you can eat its": ["does not have consumable"],
    "Food you can eat its": ["Food has edible"],
    "not tastes like": ["does not taste like"],
    "not holds": ["does not hold"],
    "not contains": ["does not contain"],
    "not appears": ["does not appear"],
    "not shows": ["does not show"]
}


def replace_relations(question):
    for relation, phrases in relation_dict.items():
        if relation in question:
            question = question.replace(relation, random.choice(phrases))
    return question

# Function to identify logical operators and their types
def identify_logical_operators(row):
    logical_operators = []
    logical_types = []

    if re.search(r'\band\b', row):
        logical_operators.append('and')
        logical_types.append('conjunction')
    if re.search(r'\bor\b', row):
        logical_operators.append('or')
        logical_types.append('disjunction')
    if re.search(r'\bnot\b', row):
        logical_operators.append('not')
        logical_types.append('negation')

    return ', '.join(logical_operators), 'level 3', ', '.join(logical_types)
