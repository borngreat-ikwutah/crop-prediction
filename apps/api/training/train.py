"""
Crop Disease Model Training & TFLite Conversion Pipeline.
Focus crops: Cassava, Maize, Tomato (Enugu agricultural field application).
Architecture: MobileNetV2 Transfer Learning -> Quantized / Float32 TFLite.
"""

import os
import sys
import argparse
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

# Define constants
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
EPOCHS = 5
NUM_CLASSES = 4

CLASSES = [
    "Cassava_Mosaic",
    "Maize_Blight",
    "Tomato_Early_Blight",
    "Healthy",
]

# Paths relative to this training directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
DEFAULT_DATA_DIR = os.path.join(
    PROJECT_ROOT, "data", "raw", "New Plant Diseases Dataset(Augmented)", "train"
)
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed", "train")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
OUTPUT_H5_PATH = os.path.join(MODELS_DIR, "crop_model.h5")
OUTPUT_TFLITE_PATH = os.path.join(MODELS_DIR, "crop_model.tflite")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train CropDisease MobileNetV2 classifier and export to TFLite."
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="",
        help="Path to training image directory containing the 4 class folders.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=EPOCHS,
        help="Number of epochs to train (default: 5).",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=BATCH_SIZE,
        help="Batch size (default: 32).",
    )
    parser.add_argument(
        "--create_starter_model",
        action="store_true",
        help="Instantly build and export an initialized MobileNetV2 TFLite model without dataset for test setup.",
    )
    return parser.parse_args()


def get_data_directory(user_dir: str) -> str:
    """Find valid data directory."""
    if user_dir and os.path.isdir(user_dir):
        return os.path.abspath(user_dir)
    if os.path.isdir(DEFAULT_DATA_DIR):
        return DEFAULT_DATA_DIR
    if os.path.isdir(PROCESSED_DATA_DIR):
        return PROCESSED_DATA_DIR
    return ""


def build_model(num_classes: int = NUM_CLASSES) -> tf.keras.Model:
    """
    Build transfer learning model with MobileNetV2 backbone.
    """
    print("Loading MobileNetV2 backbone (pre-trained on ImageNet)...")
    base = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False

    model = models.Sequential([
        layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        layers.Rescaling(1.0 / 255.0),  # normalize if not pre-scaled
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax", name="predictions"),
    ])

    return model


def export_tflite(model: tf.keras.Model, output_tflite_path: str):
    """Convert Keras model to TensorFlow Lite and save."""
    print("Converting model to TFLite format...")
    os.makedirs(os.path.dirname(output_tflite_path), exist_ok=True)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    with open(output_tflite_path, "wb") as f:
        f.write(tflite_model)

    size_mb = os.path.getsize(output_tflite_path) / (1024 * 1024)
    print(f"Successfully saved TFLite model to: {output_tflite_path} ({size_mb:.2f} MB)")


def main():
    args = parse_args()
    os.makedirs(MODELS_DIR, exist_ok=True)

    if args.create_starter_model:
        print("Creating initialized starter MobileNetV2 TFLite model...")
        model = build_model()
        model.save(OUTPUT_H5_PATH)
        print(f"Saved initial H5 model to {OUTPUT_H5_PATH}")
        export_tflite(model, OUTPUT_TFLITE_PATH)
        print("Ready for local testing!")
        return

    data_dir = get_data_directory(args.data_dir)
    if not data_dir or not os.path.isdir(data_dir):
        print("=" * 70)
        print("⚠️  DATASET DIRECTORY NOT FOUND!")
        print(f"Looked at:\n - {DEFAULT_DATA_DIR}\n - {PROCESSED_DATA_DIR}")
        print("\nPlease follow these steps:")
        print("1. Download PlantVillage & Cassava datasets using Kaggle CLI:")
        print("   kaggle datasets download -d vipoooool/new-plant-diseases-dataset")
        print("2. Run python training/prepare_data.py to curate the 4 classes.")
        print("3. Alternatively, run:")
        print("   python training/train.py --create_starter_model")
        print("   to generate an immediate functional MobileNetV2 TFLite model.")
        print("=" * 70)
        sys.exit(1)

    print(f"Loading dataset from: {data_dir}")
    print(f"Target classes: {CLASSES}")

    # Load dataset with 80/20 train/validation split
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="int",
        class_names=CLASSES,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=args.batch_size,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="int",
        class_names=CLASSES,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=args.batch_size,
    )

    # Prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Build model
    model = build_model()
    model.summary()

    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    # Train model
    print(f"Starting transfer learning training for {args.epochs} epochs...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
    )

    # Save H5 model
    print(f"Saving Keras H5 model to: {OUTPUT_H5_PATH}...")
    model.save(OUTPUT_H5_PATH)
    print("H5 model saved successfully.")

    # Convert to TFLite
    export_tflite(model, OUTPUT_TFLITE_PATH)
    print("Training and TFLite conversion pipeline completed successfully.")


if __name__ == "__main__":
    main()
