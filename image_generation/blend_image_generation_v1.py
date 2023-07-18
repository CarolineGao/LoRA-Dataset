# VQA Integration Code WIP
import bpy
import mathutils
import random
import math
import sys
import csv
import os
import numpy as np
#from random import random
from random import randint
from random import randrange
from math import sqrt
from random import sample, choice, choices
import pandas as pd
from contextlib import redirect_stdout

import argparse
parser = argparse.ArgumentParser()
args, unknown = parser.parse_known_args()
#args = parser.parse_args()

scene = bpy.context.scene

# Set the device_type
bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"

# Set the device and feature set
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.feature_set = "SUPPORTED"
for scene in bpy.data.scenes:
    # print(scene.name)
    scene.cycles.device = 'GPU'


#print("----------------------------------------------")
for devices in bpy.context.preferences.addons['cycles'].preferences.get_devices():
    for d in devices:
        d.use = True
        if d.type == 'CPU':
            d.use = False
        #print("Device '{}' type {} : {}" . format(d.name, d.type, d.use))
#print("----------------------------------------------")


#locs = [[0.53, -0.19, 0.0], [-0.25, 0.31, 0.0], [0.56, 0.24, 0.0], [0.29, 0.35, 0.0], [0.54, -0.48, 0.0], [-0.03, -0.68, 0.0], [-0.20, 0.12, 0.0], [0.30, 0.60, 0.0], [0.41, 0.14, 0.0], [-0.15, 0.50, 0.0], [-0.27, -0.52, 0.0]]


def generate_image(file='/home/jingying/LoRA/Images/logic2_blend_5850.csv'):
    # load base blender file
    datas = pd.read_csv(file, header=None, skiprows=0)

    i = 5851
    for _, row in datas.iterrows():
        # Considering that the names are in the first column of your data
        # Splitting the string into individual names
        names = str(row[1]).split(', ')
        print(row)
        # Stripping whitespace and removing quotes around each name
        names = [name.replace("'", "").replace('"', '').strip() for name in names]

        unlink_object(names)
        place_object(names)

        image_name = 'lora_logic2_{}.png'.format(i)
        render_image(image_name)
        delete_object(names)
        i += 1


def copy_new_object(name, location):
   move = mathutils.Vector(location)
   obj = bpy.data.objects[name]
   cp_obj = obj.copy()
   cp_obj.location = move
   collection = bpy.data.collections["Collection"]
   collection.objects.link(cp_obj)

def place_object(names):
    locs = get_empty_locs()
    num_objects = len(names)

    selected_indexes = np.random.choice(len(locs), num_objects, replace=False)

    for i, i_loc in enumerate(selected_indexes):
        copy_new_object(names[i], locs[i_loc])
        print(names[i], locs[i_loc])


# Code for generate an individual image.
#def render_image(save_path="/Users/jingying/Documents/PhD/Implementation/Paper_1/Blender/try.png"):
    #scene.render.image_settings.file_format = 'PNG'
    #scene.render.filepath = save_path
    #bpy.ops.render.render(write_still = 1)

def render_image(name, save_path="/home/jingying/LoRA/Images/Logic2"):
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = os.path.join(save_path, name)
    bpy.ops.render.render(write_still = 1)

# Unlink/delete the initial objects from image.
def unlink_object(names):
    collection = bpy.data.collections["Collection"]
    #sub_collection = bpy.data.scenes['Scene'].collection.all_objects
    unlink_objects = []
    #for obj in collection.objects:
    for obj in collection.objects:
        if obj.name_full in names:
            unlink_objects.append(obj.name_full)

    #for obj in bpy.data.objects:
    for obj in bpy.data.objects:
        if obj.name_full in unlink_objects:
            collection.objects.unlink(obj)
            # print('unlink {} ok'.format(obj.name_full))


def delete_object(names):
    #delete after save
    for name in names:
        collection = bpy.data.collections["Collection"]
        for obj in collection.objects:
            if name+'.' in obj.name_full and obj.name_full!=name:
                print(obj.name_full)
                collection.objects.unlink(obj)


def get_empty_locs():
    locs = []
    for obj in bpy.data.scenes['Scene'].collection.all_objects:
    #for obj in bpy.data.scollection.all_objects:
        if 'Empty.' in obj.name:
            locs.append(obj.location)
    return locs


# if __name__ == '__main__':
#     generate_image()
#     print('done')

if __name__ == '__main__':
    with open('output.txt', 'w') as f:
        with redirect_stdout(f):
            generate_image()  
            print('done')