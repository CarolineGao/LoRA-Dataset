# Generate questions _ conditional _logic _ template 2. 

from ontology_v6 import graph, getOnto
from owlQuery import fill_template_with_relationships

from owlready2 import *
import random

from util import save_as_csv, replace_relations, identify_logical_operators

onto = getOnto()

# "If {food} is not available, what other food with a similar taste to {taste} can be used for {cooking_method}?"
def generate_all_question_results(template):
    with onto:
        all_classes = list(onto.classes())
        all_foods = list(onto.Food.instances())
        distinct_is_growing_values = set(g for food in onto.Food.instances() for g in getattr(food, 'is_growing', []))


        question_results = []
        for ont_class in all_classes:
            if onto.Food in ont_class.ancestors():
                for random_food in ont_class.instances():
                    for related_taste in random_food.has_taste:
                        for is_growing in distinct_is_growing_values:
                            question_result = template.replace('{class}', ont_class.name)
                            question_result = question_result.replace('{food}', random_food.name)
                            question_result = question_result.replace('{taste}', related_taste.name)
                            question_result = question_result.replace('{is_growing}', is_growing.name)

                            is_class = [food.name for food in all_foods if isinstance(food, ont_class)]
                            has_taste = [food.name for food in all_foods if related_taste in food.has_taste]
                            has_growing_style = [food.name for food in all_foods if is_growing in food.is_growing]
                            fa = [food for food in is_class if food in has_taste and food in has_growing_style and food is not random_food.name]

                            # possible_answers = same_class_same_taste_foods if same_class_same_taste_foods else ['None']
                            question_results.append((question_result, is_class, has_taste, has_growing_style, fa))

    return question_results

template = "If {food} is not available, what other {class} with a similar {taste} taste can be used that grows {is_growing}?"
results = generate_all_question_results(template)

save_as_csv(results, "question_results_5.csv", ["Question", "is_class", "has_taste", "has_growing_style,", "fa"])
