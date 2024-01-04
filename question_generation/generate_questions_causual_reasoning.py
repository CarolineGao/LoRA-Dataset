# Logic why questions generation. 

from ontology_v6 import graph, getOnto

from owlready2 import *
import random

from util import save_as_csv, replace_relations, identify_logical_operators

onto = getOnto()

# 11. Multi Fruit operators 
from util import replace_relations, identify_logical_operators

def generate_all_question_results(templates):
    with onto:
        all_fruits = list(onto.Fruit.instances())
        all_nutritions = [("has_nutrition", list(onto.Nutrition.instances()))]
        all_tastes = [("has_taste", list(onto.Taste.instances()))]
        all_colours = [("has_color", list(onto.Color.instances()))]
        all_shapes = [("has_shape", list(onto.Shape.instances()))]

        all_relations = all_tastes + all_colours + all_shapes + all_nutritions
        ops = ["and", "or", "and not", "or not"]

        question_results = []

        for rel_1, attributes_1 in all_relations:
            for attribute1 in attributes_1:
                for rel_2, attributes_2 in all_relations:
                    if rel_2 != rel_1:
                        for attribute2 in attributes_2:
                            for rel_3, attributes_3 in all_relations:
                                if rel_3 != rel_1 and rel_3 != rel_2:
                                    for attribute3 in attributes_3:

                                        template = random.choice(templates)
                                        op1 = random.choice(ops)
                                        op2 = random.choice(ops)
                                        
                                        question_result = template.replace('{rel_a}', rel_1)
                                        question_result = question_result.replace('{attr_a}', attribute1.name)
                                        question_result = question_result.replace('{rel_b}', rel_2)
                                        question_result = question_result.replace('{attr_b}', attribute2.name)
                                        question_result = question_result.replace('{rel_c}', rel_3)
                                        question_result = question_result.replace('{attr_c}', attribute3.name)
                                        question_result = question_result.replace('{op_a}', op1)
                                        question_result = question_result.replace('{op_b}', op2)

                                        def getMatches(rel, attr, op):
                                            if "not" in op:
                                                return [food.name for food in all_fruits if attr not in getattr(food, rel, [])]
                                            else:
                                                return [food.name for food in all_fruits if attr in getattr(food, rel, [])]

                                        def reduceAns(set1, set2, op):
                                            if "and" in op:
                                                return [item for item in set1 if item in set2]
                                            else:
                                                return list(set(set1) | set(set2))

                                        match1 = getMatches(rel_1, attribute1, "")
                                        match2 = getMatches(rel_2, attribute2, op1)
                                        match3 = getMatches(rel_3, attribute3, op2)

                                        step1 = reduceAns(match1, match2, op1)
                                        fa = reduceAns(step1, match3, op2)

                                        if not fa: 
                                            continue

                                        f = random.choice(fa)
                                        m1 = f"{rel_1} {attribute1.name}" if f in match1 else ""
                                        m2 = f"{rel_2} {attribute2.name}" if f in match2 else ""
                                        m2 = f"not {m2}" if "not" in op1 and m2 else m2
                                        m3 = f"{rel_3} {attribute3.name}" if f in match3 else ""
                                        m3 = f"not {m3}" if "not" in op2 and m3 else m3
                                        # ans = f"{f} {m1} {m2} {m3}"
                                        ans = f"{f} {' and '.join(part for part in [m1, m2, m3] if part)}"
                                        ans_nl = replace_relations(ans)

                                        question_result = question_result.replace('{food}', f)
                                        qnl = replace_relations(question_result)
                                        operators, level, types = identify_logical_operators(question_result)

                                        question_results.append((question_result, qnl, ans_nl, match1, match2, match3, fa, operators, level, types))
                    
    return question_results

templates = [
    # "Which fruit has taste {taste} and has shape {shape} or has colour {colour}",
    "Why is {food} a good choice when I want a fruit that {rel_a} {attr_a} {op_a} {rel_b} {attr_b} {op_b} {rel_c} {attr_c}?"
]

results = generate_all_question_results(templates)

save_as_csv(results, "question_results_why_meat.csv", [
    "Question",
    "questions_nlp",
    "answer",
    "a1",
    "a2",
    "a3",
    "fa",
    "logical_operator",
    "logical_level",
    "logical_types"
])
