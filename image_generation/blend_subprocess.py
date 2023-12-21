# Sub-process
import subprocess

def run_blender_script(blender_executable_path, blender_script_path, background_path, start_index):
    subprocess.call([blender_executable_path, '--background', background_path, '--python', blender_script_path, '--', str(start_index)])

def main():
    blender_executable_path = 'path/blender.blend'
    blender_script_path = 'path/blend_image_batch_generation.py'
    background_path = 'path_background.blend'
    
    total_images = 5000
    batch_size = 50
    num_batches = total_images // batch_size

    for batch_num in range(num_batches):
        start_index = (batch_num * batch_size) + 3000
        run_blender_script(blender_executable_path, blender_script_path, background_path, start_index)
        print(f"Blender batch {batch_num} completed and restarted.")

if __name__ == '__main__':
    main()


