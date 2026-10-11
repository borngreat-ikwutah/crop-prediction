import os
import shutil
import random

DATA_DIR = './data/PlantVillage-Dataset'

def get_dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def trim_to_size():
    # 1. Remove grayscale and segmented to save space immediately
    for sub in ['raw/grayscale', 'raw/segmented', 'data_distribution_for_SVM']:
        path = os.path.join(DATA_DIR, sub)
        if os.path.exists(path):
            print(f"Removing {path}...")
            shutil.rmtree(path)
            
    # 2. Trim color dataset to ~490MB
    color_dir = os.path.join(DATA_DIR, 'raw/color')
    target_size = 490 * 1024 * 1024 # 490 MB
    
    current_size = get_dir_size(color_dir)
    print(f"Initial color dir size: {current_size / (1024*1024):.2f} MB")
    
    if current_size <= target_size:
        print("Dataset is already under target size.")
        return
        
    # Collect all image files
    all_files = []
    for root, dirs, files in os.walk(color_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
            
    random.shuffle(all_files)
    
    # Delete files until we are under the target size
    for file in all_files:
        if current_size <= target_size:
            break
        size = os.path.getsize(file)
        os.remove(file)
        current_size -= size
        
    print(f"Final color dir size: {get_dir_size(color_dir) / (1024*1024):.2f} MB")

if __name__ == '__main__':
    trim_to_size()
