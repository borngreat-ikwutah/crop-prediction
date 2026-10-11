import os
import csv

DATA_DIR = './data/PlantVillage-Dataset/raw/color'
OUTPUT_CSV = 'dataset_manifest.csv'

def create_dataset_csv():
    if not os.path.exists(DATA_DIR):
        print(f"Directory {DATA_DIR} does not exist.")
        return

    with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['image_path', 'label'])
        
        # Iterate through the class folders
        for label in sorted(os.listdir(DATA_DIR)):
            class_dir = os.path.join(DATA_DIR, label)
            
            # Ensure it's a directory
            if os.path.isdir(class_dir):
                for image_file in os.listdir(class_dir):
                    # Only include standard image formats
                    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.JPG', '.JPEG')):
                        image_path = os.path.join(class_dir, image_file)
                        writer.writerow([image_path, label])

if __name__ == '__main__':
    create_dataset_csv()
    print(f"Successfully generated {OUTPUT_CSV}")
