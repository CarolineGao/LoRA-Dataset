# VQA Integration Code
"""
# 0-5000 Images: Blender Background: Vqa_Background_L3_kitchen_Fruit_T1_v1.blend
# 5000-10000 Images: Blender Background: 
"""

import bpy
import mathutils
import random
import math
import sys
import csv
import os
import numpy as np
import pandas as pd
from random import randint
from random import randrange
from math import sqrt
from random import sample, choice, choices
import argparse
from contextlib import redirect_stdout

import argparse
parser = argparse.ArgumentParser()
args, unknown = parser.parse_known_args()

scene = bpy.context.scene

# Enable GPU rendering
bpy.context.scene.render.engine = 'CYCLES'

# Set compute device type
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA' 

# Enable GPU device(s)
for device_type in bpy.context.preferences.addons['cycles'].preferences.get_devices():
    for device in device_type:
        if device.type == 'CUDA':  
            device.use = True
        else:
            device.use = False

# Set the device to GPU in the scene
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.feature_set = "SUPPORTED"
for scene in bpy.data.scenes:
    print(scene.name)
    scene.cycles.device = 'GPU'

def place_object(names, empty_names):
    locs = get_empty_locs()
    for name, empty_name in zip(names, empty_names):
        if empty_name in locs: 
            print(f"{name} <{locs[empty_name]}>") 
            copy_new_object(name, locs[empty_name])

def copy_new_object(name, location):
    move = mathutils.Vector(location)
    obj = bpy.data.objects[name]
    cp_obj = obj.copy()
    cp_obj.location = move
    collection = bpy.data.collections["Collection"]
    collection.objects.link(cp_obj)

def render_image(name, save_path="path_to_save_imgs"):
    # scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = os.path.join(save_path, name)
    bpy.ops.render.render(write_still = 1)
    
# def unlink_object(names):
#     collection = bpy.data.collections["Collection"]
#     for obj in collection.objects:
#         if obj.name_full in names:
#             collection.objects.unlink(obj)

# Unlink/delete the initial objects from image.
def unlink_object(names):
    collection = bpy.data.collections["Collection"]
    unlink_objects = []
    for obj in collection.objects:
        if obj.name_full in names:
            unlink_objects.append(obj.name_full)

    for obj in bpy.data.objects:
        if obj.name_full in unlink_objects:
            collection.objects.unlink(obj)


def delete_object(names):
    #delete after save
    for name in names:
        collection = bpy.data.collections["Collection"]
        for obj in collection.objects:
            if name+'.' in obj.name_full and obj.name_full!=name:
                print(obj.name_full)
                collection.objects.unlink(obj)

def get_empty_locs():
    locs = {}
    for obj in bpy.data.objects:
        if 'Empty' in obj.name:
            locs[obj.name] = obj.location
    return locs

def generate_batch(start, end, file):
    datas_initial = pd.read_csv(file)
    datas = datas_initial[start:end]

    for i, (index, row) in enumerate(datas.iterrows(), start):
        print(row)
        
        right_objects = str(row['right_side_object']).split(', ')
        left_objects = str(row['left_side_object']).split(', ')
        middle_object = str(row['middle_object']).split(', ')

        unlink_object(right_objects + left_objects + middle_object)
        place_object(right_objects, ['Empty.001', 'Empty.002', 'Empty.003', 'Empty.004', 'Empty.005'])
        place_object(left_objects, ['Empty.006', 'Empty.007', 'Empty.008', 'Empty.009', 'Empty.010'])
        place_object(middle_object, ['Empty.011'])

        image_name = f'lora_logic3_{i}.png'
        print(f"ImgId: {image_name}")
        render_image(image_name)
        delete_object(right_objects + left_objects + middle_object)
        
    # Memory purge after each batch
    # bpy.ops.wm.memory_purge()


class ArgumentParserForBlender(argparse.ArgumentParser):   
    def _get_argv_after_doubledash(self):
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] 
        except ValueError as e: 
            return []

    def parse_args(self):
        return super().parse_args(args=self._get_argv_after_doubledash())


def main():
    parser = ArgumentParserForBlender() 
    parser.add_argument('start_index', type=int, help='Start index for batch processing')
    args = parser.parse_args()
    print(args.start_index)
    # return
    file = 'path_csv_file_to_generate_blend_img.csv'
    log_file_path = 'path_log.txt'
    total_images = 5000
    batch_size = 50
    start = args.start_index
    end = min(start + batch_size, total_images)

    with open(log_file_path, 'a') as f:
        with redirect_stdout(f):
            generate_batch(start, end, file)
            print(f"Batch {start} to {end} completed.")
            
if __name__ == '__main__':
    main()
    

