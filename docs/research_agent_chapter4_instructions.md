# Chapter 4 Implementation Instructions for Research Agent

**Role:** You are an AI Research Agent responsible for implementing the experimental methodology for Chapter 4 of a research project on "Crop Disease Detection & Adversarial Attack Systems."

## Objective
Implement a comparative robustness experiment contrasting two CNN architectures under clean and adversarial conditions, using the PlantVillage dataset. You must train the models, execute adversarial attacks, apply defenses, and record specific evaluation metrics.

## 1. Environment & Dataset
- **Frameworks:** PyTorch, Torchvision, and IBM Adversarial Robustness Toolbox (ART).
- **Dataset:** PlantVillage dataset (`data/PlantVillage-Dataset/raw/color`). The dataset contains 38 classes of crop leaves.
- **Data Splitting:** Use an 80/20 train/test split.
- **Data Augmentation:** Apply basic data augmentation (e.g., resizing to 224x224, random horizontal flips, and random rotation) for training.

## 2. Models to Implement
Initialize two distinct models using pre-trained ImageNet weights. Modify their final classification heads to output 38 classes:
1. **ResNet-50** (High-capacity baseline)
2. **EfficientNet-B0** (Parameter-efficient baseline)

## 3. Training Phase (Clean Models)
- Train both models on the clean training set for up to 10 epochs (or until convergence).
- Use Adam optimizer (`lr=1e-4`) and CrossEntropyLoss.
- Save the trained weights (e.g., `resnet50_clean.pth`, `efficientnet_b0_clean.pth`).

## 4. Adversarial Attack Implementations
Wrap the trained PyTorch models using IBM ART's `PyTorchClassifier`. Execute the following white-box evasion attacks on the test set for both models across three perturbation budgets ($\epsilon \in \{0.01, 0.03, 0.05\}$):
1. **FGSM (Fast Gradient Sign Method):** Single-step attack.
2. **PGD (Projected Gradient Descent):** Iterative attack (e.g., 10 iterations, step size $\epsilon/4$).

## 5. Defense Implementations
Apply the following defense mechanisms to evaluate model recovery:
1. **Adversarial Training:** Retrain or fine-tune the models on a mixture of clean and PGD-generated adversarial examples.
2. **Input Preprocessing (Feature Squeezing):** Apply non-differentiable transformations to the inputs before classification using ART's preprocessing wrappers:
   - JPEG Compression (Quality = 75)
   - Gaussian Smoothing

## 6. Evaluation Metrics to Record
For every combination of Model, Attack, $\epsilon$, and Defense, compute and log the following metrics into a CSV file or formatted Markdown table:
1. **Clean Accuracy ($Acc_{clean}$):** Accuracy on unperturbed test data.
2. **Adversarial Accuracy ($Acc_{adv}$):** Accuracy on adversarial examples.
3. **Robustness Gap:** $Acc_{clean} - Acc_{adv}$.
4. **Recovery:** Adversarial accuracy of the model *after* the defense is applied.
5. **Clean-Accuracy Retention:** Accuracy of the *defended* model on clean test data.

## 7. Deliverables Required from Agent
1. **`train_and_evaluate.py`:** The complete, modular Python script executing the pipeline above.
2. **`results.csv`:** The tabulated results of all experiments and metrics.
3. **`chapter_4_results_analysis.md`:** A written analysis synthesizing the metrics, comparing ResNet-50 vs. EfficientNet-B0, and evaluating the effectiveness of the defenses across the different $\epsilon$ budgets.
