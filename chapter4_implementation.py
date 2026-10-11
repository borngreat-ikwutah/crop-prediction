import os
import csv
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from torch.utils.data import DataLoader, Subset
from art.estimators.classification import PyTorchClassifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent
from art.defences.preprocessor import JpegCompression, GaussianAugmentation
import numpy as np
from sklearn.model_selection import train_test_split

# ==========================================
# 1. Configuration and Hyperparameters
# ==========================================
DATA_DIR = './data/PlantVillage-Dataset/raw/color'
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 1e-4
NUM_CLASSES = 38 # PlantVillage has 38 classes
EPSILONS = [0.01, 0.03, 0.05]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
RESULTS_FILE = 'results.csv'

# ==========================================
# 2. Dataset Loading and Preprocessing
# ==========================================
def get_dataloaders(data_dir, batch_size):
    transform_train = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
    ])
    
    transform_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    
    full_dataset = datasets.ImageFolder(root=data_dir, transform=transform_test)
    train_idx, test_idx = train_test_split(list(range(len(full_dataset))), test_size=0.2, random_state=42)
    
    train_dataset = Subset(datasets.ImageFolder(root=data_dir, transform=transform_train), train_idx)
    test_dataset = Subset(datasets.ImageFolder(root=data_dir, transform=transform_test), test_idx)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    
    return train_loader, test_loader, full_dataset.classes

# ==========================================
# 3. Model Architectures
# ==========================================
def get_resnet50(num_classes):
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model.to(DEVICE)

def get_efficientnet_b0(num_classes):
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    return model.to(DEVICE)

# ==========================================
# 4. Training Loop (Clean Model)
# ==========================================
def train_model(model, train_loader, epochs, model_name):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
        epoch_loss = running_loss / total
        epoch_acc = 100. * correct / total
        print(f"[{model_name}] Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.4f} - Acc: {epoch_acc:.2f}%")
        
    torch.save(model.state_dict(), f'{model_name}_clean.pth')
    return model

# ==========================================
# 5. Evaluation, Attacks, and CSV Logging
# ==========================================
def evaluate_attacks_and_defenses(model, model_name, test_loader, epsilons, csv_writer):
    criterion = nn.CrossEntropyLoss()
    
    classifier = PyTorchClassifier(
        model=model,
        clip_values=(0.0, 1.0),
        loss=criterion,
        optimizer=optim.Adam(model.parameters(), lr=LEARNING_RATE),
        input_shape=(3, 224, 224),
        nb_classes=NUM_CLASSES,
        device_type='gpu' if torch.cuda.is_available() else 'cpu'
    )
    
    # Fetch a batch for evaluation (can loop through entire test_loader for full evaluation)
    x_test, y_test = next(iter(test_loader))
    x_test = x_test.numpy()
    y_test = y_test.numpy()
    
    # --- Clean Accuracy ---
    preds_clean = classifier.predict(x_test)
    acc_clean = np.sum(np.argmax(preds_clean, axis=1) == y_test) / len(y_test)
    print(f"[{model_name}] Clean Accuracy: {acc_clean * 100:.2f}%")
    
    # Log baseline clean accuracy to CSV
    csv_writer.writerow([model_name, "None", 0.0, "None", f"{acc_clean * 100:.2f}%", "N/A", "N/A", "N/A", "N/A"])
    
    # Preprocessing Defense Setup
    jpeg_defense = JpegCompression(clip_values=(0.0, 1.0), quality=75, apply_fit=False, apply_predict=True)
    defended_classifier = PyTorchClassifier(
        model=model, clip_values=(0.0, 1.0), loss=criterion, 
        optimizer=optim.Adam(model.parameters(), lr=LEARNING_RATE),
        input_shape=(3, 224, 224), nb_classes=NUM_CLASSES, 
        preprocessing_defences=[jpeg_defense], device_type='gpu' if torch.cuda.is_available() else 'cpu'
    )
    
    # Clean accuracy retention (Defended Model on Clean Data)
    preds_def_clean = defended_classifier.predict(x_test)
    acc_def_clean = np.sum(np.argmax(preds_def_clean, axis=1) == y_test) / len(y_test)
    
    # --- Attacks Loop ---
    for eps in epsilons:
        print(f"\n[{model_name}] --- Evaluating with Epsilon: {eps} ---")
        
        # 1. FGSM Attack
        attack_fgsm = FastGradientMethod(estimator=classifier, eps=eps)
        x_test_adv_fgsm = attack_fgsm.generate(x=x_test)
        
        preds_fgsm = classifier.predict(x_test_adv_fgsm)
        acc_fgsm = np.sum(np.argmax(preds_fgsm, axis=1) == y_test) / len(y_test)
        gap_fgsm = acc_clean - acc_fgsm
        
        preds_def_fgsm = defended_classifier.predict(x_test_adv_fgsm)
        acc_def_fgsm = np.sum(np.argmax(preds_def_fgsm, axis=1) == y_test) / len(y_test)
        
        print(f"FGSM Acc: {acc_fgsm * 100:.2f}% | Gap: {gap_fgsm * 100:.2f}% | Recovery (JPEG): {acc_def_fgsm * 100:.2f}%")
        csv_writer.writerow([
            model_name, "FGSM", eps, "JPEG Compression", 
            f"{acc_clean * 100:.2f}%", f"{acc_fgsm * 100:.2f}%", 
            f"{gap_fgsm * 100:.2f}%", f"{acc_def_fgsm * 100:.2f}%", 
            f"{acc_def_clean * 100:.2f}%"
        ])
        
        # 2. PGD Attack
        attack_pgd = ProjectedGradientDescent(estimator=classifier, eps=eps, eps_step=eps/4, max_iter=10)
        x_test_adv_pgd = attack_pgd.generate(x=x_test)
        
        preds_pgd = classifier.predict(x_test_adv_pgd)
        acc_pgd = np.sum(np.argmax(preds_pgd, axis=1) == y_test) / len(y_test)
        gap_pgd = acc_clean - acc_pgd
        
        preds_def_pgd = defended_classifier.predict(x_test_adv_pgd)
        acc_def_pgd = np.sum(np.argmax(preds_def_pgd, axis=1) == y_test) / len(y_test)
        
        print(f"PGD Acc: {acc_pgd * 100:.2f}% | Gap: {gap_pgd * 100:.2f}% | Recovery (JPEG): {acc_def_pgd * 100:.2f}%")
        csv_writer.writerow([
            model_name, "PGD", eps, "JPEG Compression", 
            f"{acc_clean * 100:.2f}%", f"{acc_pgd * 100:.2f}%", 
            f"{gap_pgd * 100:.2f}%", f"{acc_def_pgd * 100:.2f}%", 
            f"{acc_def_clean * 100:.2f}%"
        ])

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Dataset not found at {DATA_DIR}. Please ensure download is complete.")
    else:
        train_loader, test_loader, classes = get_dataloaders(DATA_DIR, BATCH_SIZE)
        
        print("=== Initializing Models ===")
        resnet_model = get_resnet50(NUM_CLASSES)
        efficientnet_model = get_efficientnet_b0(NUM_CLASSES)
        
        # Initialize CSV File
        with open(RESULTS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write Header
            writer.writerow([
                "Model", "Attack", "Epsilon", "Defense", 
                "Clean Accuracy", "Adversarial Accuracy", "Robustness Gap", 
                "Recovery (Defended Adv Acc)", "Clean-Accuracy Retention"
            ])
            
            print("=== Evaluating ResNet-50 ===")
            evaluate_attacks_and_defenses(resnet_model, "ResNet-50", test_loader, EPSILONS, writer)
            
            print("\n=== Evaluating EfficientNet-B0 ===")
            evaluate_attacks_and_defenses(efficientnet_model, "EfficientNet-B0", test_loader, EPSILONS, writer)
            
        print(f"\nAll evaluations complete. Results saved to {RESULTS_FILE}")
