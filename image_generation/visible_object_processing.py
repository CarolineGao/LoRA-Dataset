# Processing fa: 
# 1. remove onto, [], and add , to each string. 2. limited fa to 6 answers to limited_ans. 
# 3. check visible in blend.onto add noise. 4. generate visible_objects for generating images. 

import warnings
warnings.filterwarnings("ignore", category=pd.core.common.SettingWithCopyWarning)
warnings.filterwarnings("default")


import pandas as pd
import random

blend_onto = set([
    'bottle', 'knife', 'plant', 'lemon', 'orange', 'grape', 'banana', 'pan', 'pot', 
    'cheese', 'onion', 'candy', 'tomato', 'carrot', 'eggplant', 'pumpkin', 'mushroom',
    'cucumber', 'pepper', 'garlic', 'watermelon', 'avocado', 'wine', 'potato', 'plum', 
    'lime', 'chocolate', 'yoghurt', 'milk', 'asparagus', 'broccoli', 'leek', 
    'capsicum', 'chilli', 'zucchini','cabbage', 'lettuce', 'springonion', 'parsley', 'pear'
])

def process_answer(val):
    if isinstance(val, str):
        val = val.replace('onto.', '').replace('][', ',').replace('[', '').replace(']', '')
        val_list = [v for v in val.split(',') if v in blend_onto]
        if len(val_list) > 6:
            limited_val_list = val_list[:6]
        else:
            limited_val_list = val_list
        
        limited_val = ', '.join(limited_val_list)
        noise_val_list = list(blend_onto - set(val_list))
        if len(noise_val_list) > 4:
            noise_val_list = random.sample(noise_val_list, 4)
        noise_val = ', '.join(noise_val_list)
        visible_val = ', '.join(limited_val_list + noise_val_list)
    else:
        limited_val = val
        noise_val = ''
        visible_val = ''
        
    return val, limited_val, noise_val, visible_val

qa = pd.read_csv("/home/jingying/LoRA/logic2_qa.csv")
df = qa.dropna(subset=['fa'])
df[['full_ans', 'limited_ans', 'noise_object', 'visible_object']] = df['fa'].apply(process_answer).apply(pd.Series)
# df.loc[:, ['full_ans', 'limited_ans', 'noise_object', 'visible_object']] = df['fa'].apply(process_answer).apply(pd.Series)
df.to_csv("/home/jingying/LoRA/logic2_visible_full.csv")
print("Done. logic2_visible_full.csv is saved.")


blend_visible = pd.read_csv("/home/jingying/LoRA/logic2_visible_full.csv", usecols=['visible_object'])
blend_visible.to_csv("/home/jingying/LoRA/logic2_blend.csv", index=False, header=False)
print("Done. logic2_blend.csv is saved.")


"""
The below is another way to write the function for processing fa. Studying purpose keeps here. 

"""

# def process_columns(df, blend_onto):
#     def format_answer(val):
#         if isinstance(val, str):
#             val = val.replace('onto.', '').replace('][', ',').replace('[', '').replace(']', '')
#             return val
#         else:
#             return val

    # def limit_answers(val):
    #     # Assuming the input will be a string of comma separated values
    #     if isinstance(val, str):
    #         val_list = val.split(',')
    #         if len(val_list) > 6:
    #             val_list = val_list[:6]
    #         return ','.join(val_list)
    #     else:
    #         return val

    # def find_noise_objects(val):
    #     if isinstance(val, str):
    #         val_list = val.split(',')
    #         noise_val_list = list(set(blend_onto) - set(val_list))
    #         if len(noise_val_list) > 4:
    #             noise_val_list = random.sample(noise_val_list, 4)
    #         return ','.join(noise_val_list)
    #     else:
#             return val

#     def visible_objects(row):
#         if isinstance(row['limited_ans'], str) and isinstance(row['noise_object'], str):
#             return ','.join([row['limited_ans'], row['noise_object']])
#         elif isinstance(row['limited_ans'], str):
#             return row['limited_ans']
#         elif isinstance(row['noise_object'], str):
#             return row['noise_object']
#         else:
#             return ''

#     df['full_ans'] = df['fa'].apply(format_answer)
#     df['limited_ans'] = df['full_ans'].apply(limit_answers)
#     df['noise_object'] = df['full_ans'].apply(find_noise_objects)
#     df['visible_object'] = df.apply(visible_objects, axis=1)
#     return df

# blend_onto = ['bottle', 'knife', 'plant', 'lemon', 'orange', 'grape', 'banana', 'pan', 'pot', 'cheese', 'onion', 'candy', 'tomato', 'carrot', 'eggplant', 'pumpkin', 'mushroom',
# 'cucumber', 'pepper', 'garlic', 'watermelon', 'avocado', 'wine', 'potato', 'plum', 'lime', 'chocolate', 'yoghurt', 'milk', 'asparagus', 'broccoli', 'leek', 
# 'mushroomnew', 'garlicnew', 'capsicum', 'chilli', 'tomatonew', 'zucchini', 'cabbage', 'greenpumpkin', 'yellowpumpkin', 
# 'lettuce', 'springonion', 'parsley', 'pear']

# df = process_columns(df, blend_onto)
# df.head(2)
