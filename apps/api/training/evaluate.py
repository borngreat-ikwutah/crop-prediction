import os
import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Constants matching train.py
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
CLASSES = [
    "Cassava_Mosaic",
    "Maize_Blight",
    "Tomato_Early_Blight",
    "Healthy",
]

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate CropDisease Model")
    parser.add_argument("--model_path", type=str, default="../../models/crop_model.h5", help="Path to H5 model")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to validation/test dataset")
    return parser.parse_args()

def main():
    args = parse_args()
    
    if not os.path.exists(args.model_path):
        print(f"Model not found at {args.model_path}")
        return
        
    print(f"Loading model from {args.model_path}...")
    model = tf.keras.models.load_model(args.model_path)
    
    print(f"Loading dataset from {args.data_dir}...")
    val_ds = tf.keras.utils.image_dataset_from_directory(
        args.data_dir,
        labels="inferred",
        label_mode="int",
        class_names=CLASSES,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False  # Important for keeping order with predictions
    )
    
    print("Running evaluation...")
    loss, accuracy = model.evaluate(val_ds)
    print(f"\nOverall Validation Accuracy: {accuracy*100:.2f}%")
    print(f"Overall Validation Loss: {loss:.4f}\n")
    
    # Get predictions for detailed metrics
    print("Generating detailed predictions...")
    y_true = []
    for images, labels in val_ds:
        y_true.extend(labels.numpy())
    
    predictions = model.predict(val_ds)
    y_pred = np.argmax(predictions, axis=1)
    
    print("\nClassification Report:")
    report = classification_report(y_true, y_pred, target_names=CLASSES)
    print(report)
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASSES, yticklabels=CLASSES)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    os.makedirs("evaluation_results", exist_ok=True)
    cm_path = os.path.join("evaluation_results", "confusion_matrix.png")
    plt.savefig(cm_path)
    print(f"Saved confusion matrix plot to {cm_path}")
    
    # Save text report
    with open("evaluation_results/metrics_report.txt", "w") as f:
        f.write(f"Overall Validation Accuracy: {accuracy*100:.2f}%\n")
        f.write(f"Overall Validation Loss: {loss:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
    print("Saved metrics text report to evaluation_results/metrics_report.txt")

if __name__ == "__main__":
    main()
