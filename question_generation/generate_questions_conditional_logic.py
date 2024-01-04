# Generate questions _ conditional _logic _ template 1. 

from ontology_v6 import graph, getOnto
from owlQuery import fill_template_with_relationships

from owlready2 import *
import random

from util import save_as_csv, replace_relations, identify_logical_operators

onto = getOnto()

#"Considering the unavailability of {food}, which {class} with a similar {nutrition} content would be ideal for making {recipe}?"
def generate_all_question_results(templates):
    with onto:
        all_classes = list(onto.classes())
        all_foods = list(onto.Food.instances())

        question_results = []
        for ont_class in all_classes:
            if onto.Food in ont_class.ancestors():
                for random_food in ont_class.instances():
                    for related_nutrition in random_food.has_nutrition:
                        for related_recipe in random_food.is_ingredient_of:
                            template = random.choice(templates)
                            
                            question_result = template.replace('{class}', ont_class.name)
                            question_result = question_result.replace('{food}', random_food.name)
                            question_result = question_result.replace('{nutrition}', related_nutrition.name)
                            question_result = question_result.replace('{recipe}', related_recipe.name)

                            is_class = [food.name for food in all_foods if isinstance(food, ont_class)]
                            has_nutrition = [food.name for food in all_foods if related_nutrition in food.has_nutrition]
                            fa = [food for food in is_class if food in has_nutrition and food is not random_food.name]

                            question_results.append((question_result, is_class, has_nutrition, fa))

    return question_results

template = "Considering the unavailability of {food}, which {class} with a similar {nutrition} content would be ideal for making {recipe}?"
templates = [
    "In the context of {recipe} preparation, if {food} is unavailable, what other {class} with comparable {nutrition} content would be suitable?",
    "For making {recipe}, what alternative {class} with similar {nutrition} content is recommended if {food} is not accessible?",
    "Propose another {class} with a similar {nutrition} profile if {food} is unavailable, suitable for preparing {recipe}.",
    "Considering the unavailability of {food}, which {class} with a similar {nutrition} content would be ideal for making {recipe}?"
]

results = generate_all_question_results(templates)

save_as_csv(results, "question_results_4.csv", ["Question", "is_class", "has_nutrition", "fa"])
