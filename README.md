# 🌿 CropDisease Detection System (Enugu Focus)

> **Final Year Project**: Automated foliar disease diagnosis for smallholder farmers in **Enugu State, Nigeria**, targeting **Cassava**, **Maize**, and **Tomato** crops. Built as an optimized Turborepo monorepo with TanStack Router frontend and Flask + TensorFlow Lite edge backend.

---

## 📁 Monorepo Structure

```text
crop-prediction/
├── apps/
│   ├── web/                     # TanStack Router + Vite + React + Tailwind CSS
│   │   ├── src/
│   │   │   ├── components/      # ImageUploader, Preview, ResultCard
│   │   │   ├── routes/          # File-based routes: /, /about, /history
│   │   │   ├── lib/api.ts       # Axios client + LocalStorage history
│   │   │   ├── routeTree.gen.ts # TanStack generated route tree
│   │   │   └── main.tsx         # Application entry
│   │   └── vite.config.ts       # Host on 0.0.0.0:3000 for LAN testing
│   └── api/                     # Flask REST API + TFLite inference
│       ├── app.py               # Flask server (host=0.0.0.0, port=5000, CORS enabled)
│       ├── model_loader.py      # Global TFLite interpreter loader
│       ├── predict.py           # Preprocessing, quality & blur check, inference
│       ├── treatment_db.py      # FAO & IITA recommendation database
│       ├── requirements.txt     # Python dependencies
│       └── training/
│           ├── train.py         # MobileNetV2 transfer learning & TFLite conversion
│           └── prepare_data.py  # Dataset merger & 224x224 preprocessor
├── packages/
│   ├── ui/                      # Shared reusable UI primitives (Button, Card, Badge, Spinner)
│   └── config/                  # Shared TypeScript configs & crop constants
├── data/
│   ├── raw/                     # PlantVillage + Cassava leaf disease datasets
│   ├── processed/               # Standardized 224x224 RGB train/val splits
│   └── local_enugu/             # Phone-captured Enugu farm images (Nsukka, Udi, Agbani)
├── models/
│   ├── crop_model.h5            # Keras saved model
│   └── crop_model.tflite        # Quantized edge model
├── turbo.json                   # Turborepo task pipeline configuration
├── pnpm-workspace.yaml          # PNPM workspaces configuration
├── package.json                 # Monorepo root scripts (dev:web, dev:api, dev:all)
└── .env.example                 # Environment variables template
```

---

## 🎯 Target Crops & Diagnostic Classes

| Class Key | Crop | Common Name | Pathogen / Vector |
| :--- | :--- | :--- | :--- |
| **`Cassava_Mosaic`** | Cassava | African Cassava Mosaic Disease (CMD) | *Begomovirus* transmitted by *Bemisia tabaci* whiteflies |
| **`Maize_Blight`** | Maize | Northern / Southern Corn Leaf Blight | *Exserohilum turcicum* / *Bipolaris maydis* fungi |
| **`Tomato_Early_Blight`** | Tomato | Early Blight | *Alternaria solani* fungus |
| **`Healthy`** | Any | Healthy Foliage Baseline | Normal vegetative growth |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Node.js**: v18+ or v20+ (v24 supported)
- **pnpm**: v9+ or v10+
- **Python**: 3.10+

### 2. Install Monorepo Dependencies
From the repository root:
```bash
pnpm install
```

### 3. Setup Python Backend Environment
```bash
# Navigate to the Flask API directory
cd apps/api

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Running the Development Servers
From the repository root, you can run any of the following:

```bash
# Run both Frontend & Backend concurrently via Turborepo
pnpm dev:all

# Run Frontend only (http://localhost:3000)
pnpm dev:web

# Run Backend only (http://0.0.0.0:5000)
pnpm dev:api
```

---

## 📱 Testing on Tecno Android Phone (Same Wi-Fi in Enugu)

Both the Flask API and Vite development server are configured with `host: 0.0.0.0` so you can test leaf disease detection live from your Android smartphone (e.g., Tecno, Infinix, Samsung) using the phone camera on the farm:

1. Connect your laptop and Android phone to the **same Wi-Fi network** (or turn on your phone's Wi-Fi hotspot and connect your laptop to it).
2. Find your laptop's local IP address:
   ```bash
   hostname -I
   # Example output: 192.168.1.105
   ```
3. Update `apps/web/.env` (or set `VITE_API_URL`):
   ```env
   VITE_API_URL=http://192.168.1.105:5000
   ```
4. Start the servers:
   ```bash
   pnpm dev:all
   ```
5. Open Chrome on your Tecno Android phone and navigate to:
   ```text
   http://192.168.1.105:3000
   ```
6. Tap **"Take Photo (Phone)"** to capture a fresh leaf photo directly with your phone's camera in the field!

---

## 📊 Dataset Preparation & Download

### Download PlantVillage Dataset (Kaggle)
To download the primary dataset:
```bash
# Ensure Kaggle CLI is configured (~/.kaggle/kaggle.json)
kaggle datasets download -d vipoooool/new-plant-diseases-dataset

# Unzip into data/raw/
unzip new-plant-diseases-dataset.zip -d data/raw/
```

### Add Phone-Captured Enugu Farm Images
Place your local field photos taken in Enugu farms into:
```text
data/local_enugu/
├── Cassava_Mosaic/
├── Maize_Blight/
├── Tomato_Early_Blight/
└── Healthy/
```

### Run Data Preprocessing
Standardizes images to 224×224 RGB and creates train/val splits:
```bash
python apps/api/training/prepare_data.py
```

---

## 🧠 Training & TFLite Model Export

Run the full MobileNetV2 transfer learning script:
```bash
# Train on curated dataset and export crop_model.tflite
python apps/api/training/train.py --epochs 5 --batch_size 32

# Or generate a starter MobileNetV2 TFLite model instantly for testing:
python apps/api/training/train.py --create_starter_model
```

The script:
1. Loads ImageNet pre-trained `MobileNetV2` (frozen base)
2. Adds `GlobalAveragePooling2D` + `Dropout(0.2)` + `Dense(4, softmax)`
3. Compiles with Adam optimizer and `SparseCategoricalCrossentropy`
4. Saves Keras model to `models/crop_model.h5`
5. Quantizes and converts to `models/crop_model.tflite` for edge mobile inference

---

## 🔌 API Documentation

| Endpoint | Method | Description | Sample Output |
| :--- | :--- | :--- | :--- |
| **`/health`** | `GET` | Health check & model status | `{"status": "ok", "model_loaded": true}` |
| **`/classes`** | `GET` | Supported diseases & metadata | `{"classes": ["Cassava_Mosaic", ...], ...}` |
| **`/predict`** | `POST` | Upload multipart leaf image | `{ "disease": "Cassava_Mosaic", "confidence": 98.4, "treatment": "..." }` |

### POST /predict Example
```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@/path/to/cassava_leaf.jpg"
```

Response format:
```json
{
  "disease": "Cassava_Mosaic",
  "disease_name": "African Cassava Mosaic Disease (CMD)",
  "crop": "Cassava",
  "confidence": 98.4,
  "treatment": "1. Roguing: Uproot and burn infected plants...\n2. Clean Planting Material: Use certified TMS 30572 cuttings...",
  "severity": "High",
  "status": "success"
}
```

---

## 🏛️ System Features
- **Global TFLite Interpreter**: Loaded once at startup to minimize CPU and RAM consumption.
- **Blur & Image Quality Check**: Evaluates Laplacian variance and flags blurry or distant multi-leaf shots.
- **LocalStorage History**: Past diagnoses and timestamps are saved locally on the client.
- **CORS Enabled**: `allow_origins=["*"]` allows mobile connections without preflight issues.
