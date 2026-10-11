# CHAPTER TWO: LITERATURE REVIEW
**Expanded review of crop disease detection, deep learning, adversarial attacks and defenses**

**Project focus:** Crop Disease Detection & Adversarial Attack Systems

This expanded chapter was prepared from the existing Chapter 2 and extended with additional literature located through scholarly web research. The review is organized around the conceptual path established in the original chapter: plant disease detection, datasets, CNN architectures, transfer learning, adversarial attacks, agricultural robustness, defenses, implementation tools, evaluation, and research gaps.

> **Important academic note:** The literature summaries below are written as a synthesis. The chapter uses reported-speech constructions such as “the study reported,” “the authors described,” and “the review identified.” Bibliographic details should be checked against the required citation style before final submission.

## 2.0 Literature Review Map

| Theme | Coverage in this expanded chapter |
|---|---|
| Plant disease diagnosis | Traditional image processing, spectral/thermal sensing, CNN classification and field imaging |
| Datasets | PlantVillage, PlantDoc, field datasets, rice datasets, PlantCLEF and dataset quality |
| CNNs | CNN foundations, ResNet, EfficientNet, VGG, Inception, DenseNet, MobileNet and SE blocks |
| Transfer learning | ImageNet pretraining, feature transfer, fine-tuning and limited-data learning |
| Generalization | Laboratory-to-field shift, domain adaptation, open-set recognition and deployment |
| Adversarial attacks | Adversarial examples, FGSM, PGD, white-box threat models and robustness evaluation |
| Defenses | Adversarial training, preprocessing, feature squeezing, robustness–accuracy trade-offs and evaluation pitfalls |
| Research gap | Why a comparative ResNet-50/EfficientNet-B0 study with attacks and defenses is justified |

## 2.1 Foundations of Computer Vision and Plant Disease Diagnosis

The literature evolved from handcrafted image descriptors and specialized sensors toward data-driven deep learning. Early studies established that colour, texture, spectral reflectance, and thermal information contain disease-related signals. Later CNN studies changed the workflow by allowing feature extraction and classification to be learned jointly.

### Key Handcrafted Features Extracted (Formatted for Dataset)

| Feature Category | Description | Representative Literature |
|---|---|---|
| **Colour** | Colour indices and histograms indicating chlorosis or necrosis. | Huang (2007) |
| **Texture** | Textural descriptors (e.g., GLCM) capturing surface irregularities caused by lesions. | Huang (2007) |
| **Spectral** | Hyperspectral reflectance capturing physiological changes before visible symptoms appear. | Rumpf et al. (2010); Lowe et al. (2017) |
| **Thermal** | Temperature gradients indicating transpiration changes and water stress from infection. | Raza et al. (2015) |
| **Shape** | Morphological features describing lesion boundaries and leaf deformations. | Sankaran et al. (2010) |

### Relevant Studies

- **Huang, K.-Y. (2007)** — Application of artificial neural network for detecting Phalaenopsis seedling diseases using color and texture features.
- **Sankaran, S., et al. (2010)** — A review of advanced techniques for detecting plant diseases.
- **Rumpf, T., et al. (2010)** — Early detection and classification of plant diseases with support vector machines based on hyperspectral reflectance.
- **Mahlein, A.-K., et al. (2012)** — Recent advances in sensing plant diseases for precision crop protection.
- **Wetterich, C. B., et al. (2013)** — A comparative study on application of computer vision and fluorescence imaging spectroscopy for detection of Huanglongbing citrus disease.
- **Hernández-Rabadán, D. L., et al. (2014)** — Integrating SOMs and a Bayesian classifier for segmenting diseased plants in uncontrolled environments.
- **Martinelli, F., et al. (2015)** — Advanced methods of plant disease detection: a review.
- **Raza, S.-e.-A., et al. (2015)** — Automatic detection of diseased tomato plants using thermal and stereo visible light images.
- **Mokhtar, U., et al. (2015)** — Identifying two of tomatoes leaf viruses using support vector machine.
- **Lowe, A., et al. (2017)** — Hyperspectral image analysis techniques for the detection and classification of the early onset of plant disease and stress.
- **Islam, M., et al. (2017)** — Detection of potato diseases using image segmentation and multiclass support vector machine.
- **Johannes, A., et al. (2017)** — Automatic plant disease diagnosis using mobile capture devices, applied on a wheat use case.

*Synthesis note: These earlier generation computer-vision approaches required explicit feature design and preprocessing, making performance dependent on imaging conditions. They establish the historical context before end-to-end deep learning became dominant, emphasizing the need to evaluate models across varied acquisition conditions.*

## 2.2 Public Datasets and Data Quality

Dataset design is a central methodological issue. The literature shows a recurring contrast between controlled datasets, which make learning and benchmarking easier, and field datasets, which better represent deployment conditions but contain greater variability and annotation difficulty.

### Major Datasets (Formatted for Dataset Review)

| Dataset | Characteristics | Impact on Generalization | Representative Literature |
|---|---|---|---|
| **PlantVillage** | Large, controlled, laboratory-style leaf images. | Excellent for benchmarking, but poor zero-shot transfer to field conditions. | Hughes & Salathé (2015) |
| **Field Maize Datasets** | Images annotated with disease symptoms in real agricultural fields. | Introduces background noise, varying illumination, and occlusion. | Wiesner-Hanks et al. (2018) |
| **PlantDoc** | Visual plant disease detection in non-laboratory settings. | Emphasizes real-field variability, complementing PlantVillage. | Singh et al. (2020) |
| **PlantCLEF** | Image-based plant identification at global scale. | Highlights issues of class balance, broad diversity, and large-scale data. | Goëau et al. (2022) |
| **Rice Leaf Datasets** | Field-acquired and aggregated rice disease images. | Explores specific crop diseases under real-world conditions. | Deng et al. (2021); Vbookshelf (2019) |

### Relevant Studies

- **Hughes, D. P., & Salathé, M. (2015)** — An open access repository of images on plant health to enable the development of mobile disease diagnostics.
- **Wiesner-Hanks, T., et al. (2018)** — Image set for deep learning: field images of maize annotated with disease symptoms.
- **Singh, D., et al. (2020)** — PlantDoc: A dataset for visual plant disease detection.
- **Goëau, H., et al. (2022)** — Overview of PlantCLEF 2022: image-based plant identification at global scale.
- **Deng, et al. (2021)** — Rice disease image dataset literature.
- **Vbookshelf (2019)** — Rice leaf diseases dataset.

## 2.3 Deep Learning and CNN-Based Plant Disease Detection

The literature on CNN-based disease recognition represents a progression from early demonstrations of feasibility to increasingly specialized classifiers, detectors, and severity-estimation systems.

### Relevant Studies

- **Mohanty, S. P., et al. (2016)** — Using deep learning for image-based plant disease detection.
- **Sladojevic, S., et al. (2016)** — Deep neural networks based recognition of plant diseases by leaf image classification.
- **Liu, B., et al. (2017)** — Identification of apple leaf diseases based on deep convolutional neural networks.
- **Ramcharan, A., et al. (2017)** — Deep learning for image-based cassava disease detection.
- **DeChant, C., et al. (2017)** — Automated identification of northern leaf blight-infected maize plants from field imagery using deep learning.
- **Oppenheim, D., & Shani, G. (2017)** — Potato disease classification using convolution neural networks.
- **Wang, G., et al. (2017)** — Automatic image-based plant disease severity estimation using deep learning.
- **Fuentes, A. F., et al. (2017)** — A robust deep-learning-based detector for real-time tomato plant diseases and pests recognition.
- **Brahimi, M., et al. (2017)** — Deep learning for tomato diseases: classification and visualisation.
- **Atabay, H. A. (2017)** — DeepPlant: Plant disease classification with very deep convolutional networks.
- **Cruz, A. C., et al. (2017)** — Automatic olive disease recognition using deep learning.
- **Ferentinos, K. P. (2018)** — Deep learning models for plant disease detection and diagnosis.
- **Fuentes, A. F., et al. (2018)** — High-performance deep neural network-based tomato plant diseases diagnosis system with refinement filter bank.
- **Brahimi, M., et al. (2018)** — Deep learning for plant disease recognition and localisation.
- **Zhang, X., et al. (2018)** — Identification of maize leaf diseases using improved deep convolutional neural networks.
- **Zhang, S., et al. (2018)** — Three-channel convolutional neural networks for vegetable leaf disease recognition.
- **Zhang, K., et al. (2018)** — Can deep learning identify tomato leaf disease?
- **Hang, J., et al. (2019)** — Classification of plant leaf diseases based on improved convolutional neural network.
- **Mishra, S., et al. (2020)** — Deep convolutional neural network based detection system for real-time corn plant disease recognition.

## 2.4 Transfer Learning, Architectures and Model Efficiency

This section establishes why ResNet-50 and EfficientNet-B0 are suitable choices for this study. The discussion includes VGG, Inception, DenseNet, MobileNet, and Squeeze-and-Excitation networks to explain design trade-offs between depth, capacity, efficiency, and transferability.

### Relevant Studies

- **Too, E. C., et al. (2018)** — A comparative study of fine-tuning deep learning models for plant disease identification.
- **Chen, J., et al. (2020)** — Using deep transfer learning for image-based plant disease identification.
- **Xu, M., et al. (2022)** — Transfer learning for versatile plant disease recognition with limited data.
- **LeCun, Y., et al. (1998 & 2015) / Bengio, Y., et al. (2013)** — Foundations of gradient-based representation learning.
- **Krizhevsky, A., et al. (2012)** — ImageNet classification with deep CNNs (AlexNet).
- **Simonyan, K., & Zisserman, A. (2014)** — Very deep convolutional networks (VGG).
- **Szegedy, C., et al. (2015 & 2016)** — Inception architectures.
- **He, K., et al. (2016)** — Deep residual learning (ResNet).
- **Huang, G., et al. (2017)** — Densely connected convolutional networks (DenseNet).
- **Howard, A. G., et al. (2017)** — Efficient convolutional neural networks (MobileNet).
- **Hu, J., et al. (2018)** — Squeeze-and-Excitation Networks.
- **Tan, M., & Le, Q. V. (2019)** — Rethinking model scaling for CNNs (EfficientNet).
- **Ioffe, S., & Szegedy, C. (2015) / Srivastava, N., et al. (2014) / Kingma & Ba (2014)** — Batch normalization, Dropout, and Adam optimizer methodologies.

## 2.5 Detection, Segmentation, Severity and Large-Scale Imaging

Classification alone does not describe every agricultural vision problem. Object detection, segmentation, severity estimation, and UAV-based imaging demonstrate that systems must locate disease evidence and operate at varied spatial scales.

### Relevant Studies

- **Lin, K., et al. (2019)** — Deep learning-based segmentation and quantification of cucumber powdery mildew.
- **Wang, Q., et al. (2019)** — Identification of tomato disease types and detection of infected areas based on deep CNNs and object detection techniques.
- **Stewart, E. L., et al. (2019)** — Quantitative phenotyping of northern leaf blight in UAV images.
- **Zhou, G., et al. (2019)** — Rapid detection of rice disease based on FCM-KM and Faster R-CNN fusion.
- **Xie, X., et al. (2020)** — A deep-learning-based real-time detector for grape leaf diseases.
- **Shoaib, M., et al. (2022)** — Segmentation and classification of leaf images for detection of tomato plant disease.
- **Ren, S., et al. (2015) / Girshick, R. (2015) / Liu, W., et al. (2016) / He, K., et al. (2017)** — Foundations of Faster R-CNN, Fast R-CNN, SSD, and Mask R-CNN architectures.

## 2.6 Surveys and the Evolution of the Research Area

Survey literature synthesizes the field, highlighting recurring weaknesses such as limited datasets, controlled acquisition conditions, and insufficient operational validation. They bridge benchmark results with real deployment requirements.

### Relevant Surveys

- **Boulent, J., et al. (2019)** / **Kaur, S., et al. (2019)** / **Saleem, M. H., et al. (2019)** / **Shruthi, U., et al. (2019)** / **Hasan, R. I., et al. (2020)** / **Nagaraju, M., et al. (2020)** / **Singh, V., et al. (2020)** / **Liu, J., & Wang, X. (2021)** / **Li, L., et al. (2021)** / **Tugrul, B., et al. (2022)** / **Jackulin, C., et al. (2022)** / **Katal, N., et al. (2022)** / **Salman, Z., et al. (2023)** / **Yao, J., et al. (2024)**

## 2.7 Generalization, Domain Shift and Deployment

A major theme across the literature is the gap between benchmark performance and real-world reliability. Domain shift, background complexity, illumination, camera variation, and unknown disease conditions are major deployment obstacles.

### Relevant Studies

- **Picon, A., et al. (2018)** — CNNs for mobile capture device-based crop disease classification in the wild.
- **Fuentes, A., et al. (2021)** — Open set self and across domain adaptation for tomato disease recognition.
- **Wu, X., et al. (2023)** — From laboratory to field: unsupervised domain adaptation for plant disease recognition.
- **Kochhar, A., et al. (2026)** — Frameworks with mobile application integration for multi-crop disease diagnosis.
- **Srivastava, A., et al. (2026)** — Robust multi-crop disease recognition in real-world conditions.

## 2.8 Adversarial Machine Learning: Foundations and Attacks

Adversarial machine learning provides the theoretical foundation for the project's security evaluation, establishing the existence of adversarial examples, gradient-based iterative attacks, and explicit threat models.

### Relevant Studies

- **Goodfellow, I. J., et al. (2014)** — Explaining and harnessing adversarial examples (introduced FGSM).
- **Szegedy, C., et al. (2014)** — Intriguing properties of neural networks.
- **Papernot, N., et al. (2016)** — The limitations of deep learning in adversarial settings.
- **Madry, A., et al. (2017)** — Towards deep learning models resistant to adversarial attacks (PGD and adversarial training).
- **Carlini, N., & Wagner, D. (2017)** — Towards evaluating the robustness of neural networks.
- **Ilyas, A., et al. (2019)** — Adversarial examples are not bugs, they are features.

## 2.9 Adversarial Defenses and Robustness Evaluation

Defense literature shows that claims must be tested against strong attacks. A recurring lesson is that higher robustness often involves a trade-off with natural accuracy, and apparent defense success can stem from obfuscated gradients.

### Relevant Studies

- **Tramèr, F., et al. (2018)** — Ensemble adversarial training: Attacks and defenses.
- **Xu, W., et al. (2018)** — Feature squeezing: Detecting adversarial examples in deep neural networks.
- **Athalye, A., et al. (2018)** — Obfuscated gradients give a false sense of security.
- **Zhang, H., et al. (2019)** — Theoretically principled trade-off between robustness and accuracy.
- **Shafahi, A., et al. (2019)** — Adversarial training for free!
- **Nicolae, M. I., et al. (2019)** — Adversarial Robustness Toolbox (ART).
- **Gao, J., et al. (2024)** — Adversarial robustness of plant disease classification models.
- **Powers, D. M. W. (2011)** — Evaluation metrics.

## 2.10 Interpretability and Emerging Directions

Visualization and attention mechanisms help determine what visual evidence a model relies on, ensuring it does not achieve benchmark performance through confounding background variables.

### Relevant Studies

- **Qin, Z., et al. (2018)** — Survey of CNN visualization methods.
- **Zeiler, M. D., & Fergus, R. (2014)** — Visualizing and understanding convolutional networks.
- **Vaswani, A., et al. (2017)** — Attention is all you need.

## 2.12 Thematic Synthesis of the Reviewed Literature

### 2.12.1 Development from handcrafted features to deep learning

Earlier systems relied on colour indices, texture descriptors, and spectral signatures, carrying a significant feature-engineering burden. CNNs changed this by learning hierarchical representations directly from images.

### 2.12.2 Dataset quality and the PlantVillage question

PlantVillage accelerated progress via reproducible benchmarking but does not capture all field variations. Field datasets (e.g., PlantDoc) are necessary counterpoints for measuring deployment reliability.

### 2.12.3 Why architecture comparison is necessary

CNN design involves trade-offs. ResNet relies on residual connections for deep optimization, while EfficientNet focuses on parameter-efficient scaling. This study contrasts these two distinct architectural philosophies.

### 2.12.4 Transfer learning as a practical strategy

Due to smaller agricultural datasets, initializing models from general-purpose (ImageNet) weights transfers low- and mid-level features that adapt well to plant disease tasks.

### 2.12.5 The laboratory-to-field gap

Differences in background, lighting, orientation, and image quality create a domain shift. Generalization is a separate and distinct problem from adversarial robustness.

### 2.12.6 Adversarial vulnerability as a second dimension of reliability

Models accurate on clean inputs remain vulnerable to perturbations. Evaluating with specified bounds using FGSM and iterative PGD provides a more informative robustness assessment.

### 2.12.7 Defense literature and the robustness–accuracy trade-off

Adversarial training is empirically strong but incurs computational and accuracy costs. Input transformations provide complementary defenses. Evaluation requires explicit experimental configurations rather than assuming universal effectiveness.

## 2.13 Comparative Literature Matrix

| Area | Representative literature | Main contribution reported | Main limitation/issue | Relevance to present study |
|---|---|---|---|---|
| **Early image processing** | Huang (2007); Sankaran et al. (2010); Rumpf et al. (2010); Raza et al. (2015) | Established colour, texture, spectral and thermal cues for disease recognition | Feature engineering and sensitivity to acquisition conditions | Provides historical basis for image-based plant disease analysis |
| **PlantVillage and benchmarks** | Hughes & Salathé (2015); Mohanty et al. (2016); Ferentinos (2018) | Large labelled datasets enabled high-performing CNN classification | Controlled images may not represent field variability | Primary dataset and benchmark context for the study |
| **Field datasets** | Singh et al. (2020); Wiesner-Hanks et al. (2018); Picon et al. (2018) | Introduced more realistic backgrounds and acquisition conditions | Smaller datasets and annotation complexity | Explains limits of controlled evaluation |
| **CNN architectures** | LeCun et al. (1998); Simonyan & Zisserman (2014); Szegedy et al. (2015); He et al. (2016); Tan & Le (2019) | Progressive improvements in representation, depth and efficiency | Architecture alone does not guarantee generalization or robustness | Justifies ResNet-50/EfficientNet-B0 comparison |
| **Transfer learning** | Yosinski et al. (2014); Too et al. (2018); Chen et al. (2020); Xu et al. (2022) | Pretrained representations can be adapted to plant disease tasks | Transferability depends on domain similarity | Supports ImageNet fine-tuning strategy |
| **Domain adaptation** | Fuentes et al. (2021); Wu et al. (2023) | Addresses distribution differences between laboratory and field images | Requires additional assumptions or target-domain data | Frames the limits of PlantVillage-only experiments |
| **Adversarial attacks** | Szegedy et al. (2014); Goodfellow et al. (2014); Madry et al. (2017); Carlini & Wagner (2017) | Established adversarial examples, FGSM/iterative attacks and robust evaluation | Attack strength and threat model must be specified | Direct foundation for FGSM and PGD |
| **Adversarial defenses** | Madry et al. (2017); Tramèr et al. (2018); Xu et al. (2018); Zhang et al. (2019) | Developed adversarial training, preprocessing and robust objectives | Defense can be costly and may reduce natural accuracy | Supports defense comparison |
| **Agricultural adversarial robustness** | Gao et al. (2024) | Connected adversarial vulnerability directly to plant disease classifiers | Agricultural evidence remains smaller than general computer vision literature | Directly motivates the project |

## 2.14 Research Gap and Positioning of the Present Study

The literature contains strong evidence that CNNs accurately classify plant diseases, that these models suffer under domain shift, and that neural networks are susceptible to adversarial perturbations. The gap is not the absence of plant-disease deep learning or adversarial theory; rather, it is their systematic integration. This study bridges this gap via a comparative robustness experiment contrasting ResNet-50 and EfficientNet-B0 on PlantVillage, evaluating clean data against FGSM and PGD attacks (ε = 0.01, 0.03, 0.05), and testing defenses like adversarial training and input preprocessing.

## 2.15 Summary of Chapter Two

This chapter traced the evolution from handcrafted image processing to deep CNNs, establishing the value of structured datasets like PlantVillage alongside the need for realistic field data. Architectural innovations and transfer learning provide robust baseline capabilities. However, real-world deployment faces domain shifts and adversarial vulnerabilities. By systematically exploring attacks (FGSM, PGD) and defenses (adversarial training, preprocessing), this chapter positions the upcoming comparative study between ResNet-50 and EfficientNet-B0 as a necessary step toward secure and reliable agricultural computer vision.
