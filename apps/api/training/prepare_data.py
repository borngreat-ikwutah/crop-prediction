"""
Data Preparation & Merging Pipeline for CropDisease Detection System.
Merges PlantVillage + Cassava leaf disease classification + data/local_enugu/
Standardizes into 4 target classes:
  1. Cassava_Mosaic
  2. Maize_Blight
  3. Tomato_Early_Blight
  4. Healthy
Resizes all images to 224x224 RGB and splits into train/val subsets in data/processed/.
"""

import os
import sys
import shutil
import random
from PIL import Image

# Directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
LOCAL_ENUGU_DIR = os.path.join(PROJECT_ROOT, "data", "local_enugu")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

TARGET_CLASSES = [
    "Cassava_Mosaic",
    "Maize_Blight",
    "Tomato_Early_Blight",
    "Healthy",
]

TARGET_SIZE = (224, 224)
VAL_SPLIT_RATIO = 0.2
ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Folder name mapping heuristics
CLASS_MAPPINGS = {
    # Cassava Mosaic
    "cassava mosaic disease (cmd)": "Cassava_Mosaic",
    "cassava_mosaic": "Cassava_Mosaic",
    "cmd": "Cassava_Mosaic",
    "cassava_cmd": "Cassava_Mosaic",
    # Maize Blight
    "corn_(maize)___northern_leaf_blight": "Maize_Blight",
    "corn_(maize)___cercospora_leaf_spot gray_leaf_spot": "Maize_Blight",
    "maize_blight": "Maize_Blight",
    "maize___northern_leaf_blight": "Maize_Blight",
    # Tomato Early Blight
    "tomato___early_blight": "Tomato_Early_Blight",
    "tomato_early_blight": "Tomato_Early_Blight",
    "early_blight": "Tomato_Early_Blight",
    # Healthy Crops (Tomato, Maize, Cassava healthy leaves)
    "tomato___healthy": "Healthy",
    "corn_(maize)___healthy": "Healthy",
    "cassava_healthy": "Healthy",
    "healthy": "Healthy",
}


def find_target_class(folder_name: str):
    """Map raw directory name to one of the 4 canonical classes."""
    name_clean = folder_name.lower().strip()
    if name_clean in CLASS_MAPPINGS:
        return CLASS_MAPPINGS[name_clean]
    for key, mapped in CLASS_MAPPINGS.items():
        if key in name_clean:
            return mapped
    return None


def process_image(src_path: str, dst_path: str) -> bool:
    """Resize to 224x224 RGB and save."""
    try:
        with Image.open(src_path) as img:
            img_rgb = img.convert("RGB")
            img_resized = img_rgb.resize(TARGET_SIZE, Image.Resampling.BILINEAR)
            img_resized.save(dst_path, "JPEG", quality=90)
            return True
    except Exception as e:
        print(f"Error processing {src_path}: {e}")
        return False


def collect_images_from_folder(dir_path: str):
    """Recursively collect valid image paths in a folder."""
    images = []
    if not os.path.exists(dir_path):
        return images
    for root, _, files in os.walk(dir_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ALLOWED_IMAGE_EXTS and not f.startswith("."):
                images.append(os.path.join(root, f))
    return images


def main():
    print("=" * 65)
    print("🌱 Preparing Crop Disease Dataset (Cassava, Maize, Tomato)")
    print("   Enugu Focus Field Pipeline")
    print("=" * 65)

    # Initialize processed folders
    for split in ["train", "val"]:
        for cls in TARGET_CLASSES:
            os.makedirs(os.path.join(PROCESSED_DIR, split, cls), exist_ok=True)

    class_images = {cls: [] for cls in TARGET_CLASSES}

    # 1. Search data/raw/
    print(f"\n1. Scanning raw dataset folders in: {RAW_DIR}")
    if os.path.exists(RAW_DIR):
        for root, dirs, _ in os.walk(RAW_DIR):
            for d in dirs:
                target_cls = find_target_class(d)
                if target_cls:
                    full_folder = os.path.join(root, d)
                    imgs = collect_images_from_folder(full_folder)
                    if imgs:
                        print(f"   [FOUND] '{d}' -> {target_cls} ({len(imgs)} images)")
                        class_images[target_cls].extend(imgs)

    # 2. Search data/local_enugu/
    print(f"\n2. Scanning local Enugu farm photos in: {LOCAL_ENUGU_DIR}")
    if os.path.exists(LOCAL_ENUGU_DIR):
        for entry in os.listdir(LOCAL_ENUGU_DIR):
            subpath = os.path.join(LOCAL_ENUGU_DIR, entry)
            if os.path.isdir(subpath):
                target_cls = find_target_class(entry)
                if target_cls:
                    imgs = collect_images_from_folder(subpath)
                    print(f"   [LOCAL ENUGU] '{entry}' -> {target_cls} ({len(imgs)} field images)")
                    class_images[target_cls].extend(imgs)

    # Summary
    print("\nImage counts collected per class:")
    total_found = 0
    for cls in TARGET_CLASSES:
        # Deduplicate
        class_images[cls] = list(set(class_images[cls]))
        count = len(class_images[cls])
        total_found += count
        print(f"   • {cls}: {count} images")

    if total_found == 0:
        print("\n⚠️ No images found in data/raw/ or data/local_enugu/.")
        print("To download the dataset, run:")
        print("  kaggle datasets download -d vipoooool/new-plant-diseases-dataset")
        print("  unzip new-plant-diseases-dataset.zip -d data/raw/")
        print("Or place your Enugu smartphone leaf images in:")
        print("  data/local_enugu/Cassava_Mosaic/")
        print("  data/local_enugu/Maize_Blight/")
        print("  data/local_enugu/Tomato_Early_Blight/")
        print("  data/local_enugu/Healthy/")
        return

    # Process and split
    print(f"\n3. Resizing to 224x224 and saving to {PROCESSED_DIR}...")
    for cls in TARGET_CLASSES:
        imgs = class_images[cls]
        random.seed(42)
        random.shuffle(imgs)

        val_count = int(len(imgs) * VAL_SPLIT_RATIO)
        val_imgs = imgs[:val_count]
        train_imgs = imgs[val_count:]

        for i, path in enumerate(train_imgs):
            dst = os.path.join(PROCESSED_DIR, "train", cls, f"{cls}_train_{i:05d}.jpg")
            process_image(path, dst)

        for i, path in enumerate(val_imgs):
            dst = os.path.join(PROCESSED_DIR, "val", cls, f"{cls}_val_{i:05d}.jpg")
            process_image(path, dst)

    print("\n✅ Dataset preparation complete! Data ready for training in data/processed/")


if __name__ == "__main__":
    main()
