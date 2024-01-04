# 13. Multi Fruit operators, "at least"

from ontology_v6 import graph, getOnto
from owlQuery import fill_template_with_relationships

from owlready2 import *
import random

from util import save_as_csv, replace_relations, identify_logical_operators

onto = getOnto()


def generate_all_question_results(templates):
    with onto:
        all_fruits = list(onto.Fruit.instances())
        all_nutritions = [("has_nutrition", list(onto.Nutrition.instances()))]
        all_tastes = [("has_taste", list(onto.Taste.instances()))]
        all_colours = [("has_color", list(onto.Color.instances()))]
        all_shapes = [("has_shape", list(onto.Shape.instances()))]

        all_relations = all_tastes + all_colours + all_shapes + all_nutritions
        ops = ["and", "or", "and not", "or not"]
        ops_not = ["", "not "]

        question_results = []

        for rel_1, attributes_1 in all_relations:
            for attribute1 in attributes_1:
                for rel_2, attributes_2 in all_relations:
                    if rel_2 != rel_1:
                        for attribute2 in attributes_2:

                            template = random.choice(templates)
                            not_or_blank = random.choice(ops_not)
                            op1 = random.choice(ops)
                            op2 = random.choice(ops)
                            
                            question_result = template.replace('{maybe_not}', not_or_blank)
                            question_result = question_result.replace('{rel_a}', rel_1)
                            question_result = question_result.replace('{attr_a}', attribute1.name)
                            question_result = question_result.replace('{rel_b}', rel_2)
                            question_result = question_result.replace('{attr_b}', attribute2.name)
                            question_result = question_result.replace('{op_a}', op1)
                            question_result = question_result.replace('{op_b}', op2)

                            def getMatches(rel, attr, op):
                                if "not" in op:
                                    return [food.name for food in all_fruits if attr not in getattr(food, rel, [])]
                                else:
                                    return [food.name for food in all_fruits if attr in getattr(food, rel, [])]

                            def getMatchesNum(rel, op):
                                if "not" in op:
                                    return [food.name for food in all_fruits if not len(getattr(food, rel, [])) >= 3]
                                else:
                                    return [food.name for food in all_fruits if len(getattr(food, rel, [])) >= 3]

                            def reduceAns(set1, set2, op):
                                if "and" in op:
                                    return [item for item in set1 if item in set2]
                                else:
                                    return list(set(set1) | set(set2))

                            match1 = getMatches(rel_1, attribute1, not_or_blank)
                            match2 = getMatches(rel_2, attribute2, op1)
                            match3 = getMatchesNum("has_taste", op2)
                            
                            step1 = reduceAns(match1, match2, op1)
                            # fa = reduceAns(step1, has_num_taste, op2) !!BUG fixed
                            fa = reduceAns(step1, match3, op2)

                            qnl = replace_relations(question_result)
                            operators, level, types = identify_logical_operators(question_result)

                            question_results.append((question_result, qnl, match1, match2, match3, fa, operators, level, types ))
                
    return question_results

templates = [
    # "Which fruit has taste {taste} and has shape {shape} or has colour {colour}",
    "Which fruit {maybe_not}{rel_a} {attr_a} {op_a} {rel_b} {attr_b} {op_b} has at least three tastes?"
]

results = generate_all_question_results(templates)

save_as_csv(results, "question_results_fruit_3_revised.csv", [
    "Question",
    "questions_nlp",
    "a1",
    "a2",
    "a3",
    "fa",
    "logical_operator",
    "logical_level",
    "logical_types"
])

