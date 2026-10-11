"""
Flask Backend API for CropDisease Detection System.
Provides REST endpoints for edge disease classification, health status, and class metadata.
Binds to 0.0.0.0:5000 to enable LAN access from mobile phones (e.g., Tecno Android) in Enugu farm tests.
"""

import os
import socket
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from model_loader import get_model_status, init_interpreter
from predict import predict_image
from treatment_db import LABELS, TREATMENTS, get_treatment_record

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
)
logger = logging.getLogger("CropDisease.API")

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_local_ip() -> str:
    """Retrieve local LAN IP address for Wi-Fi mobile testing."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually connect to internet, just routes socket to find local interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


@app.route("/", methods=["GET"])
def index():
    """Root info endpoint."""
    return jsonify({
        "project": "CropDisease Detection System (Enugu Focus)",
        "crops": ["Cassava", "Maize", "Tomato"],
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "System health and model load status",
            "GET /classes": "Detectable disease categories and metadata",
            "POST /predict": "Upload leaf image (multipart/form-data) for classification",
        },
    })


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint:
    Returns {"status": "ok", "model_loaded": true/false}
    """
    status = get_model_status()
    return jsonify({
        "status": "ok",
        "model_loaded": status["model_loaded"],
        "is_mock": status["is_mock"],
        "classes_count": len(LABELS),
        "details": status,
    })


@app.route("/classes", methods=["GET"])
def get_classes():
    """
    Returns the target crop disease classes and their descriptive names.
    """
    classes_detail = [get_treatment_record(label) for label in LABELS]
    return jsonify({
        "classes": LABELS,
        "details": classes_detail,
    })


@app.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict
    Receives multipart/form-data file with key 'image' or 'file'.
    Returns:
    {
        "disease": "Cassava_Mosaic",
        "confidence": 98.4,
        "treatment": "...",
        ...
    }
    """
    # Check if file part is present
    file_key = None
    if "image" in request.files:
        file_key = "image"
    elif "file" in request.files:
        file_key = "file"

    if not file_key:
        return jsonify({
            "error": "No file uploaded. Please send a multipart file with key 'image' or 'file'."
        }), 400

    uploaded_file = request.files[file_key]

    if uploaded_file.filename == "":
        return jsonify({
            "error": "No file selected. Please select a valid leaf image."
        }), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({
            "error": f"Unsupported file type. Please upload one of: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    try:
        file_bytes = uploaded_file.read()
        if len(file_bytes) == 0:
            return jsonify({"error": "Uploaded file is empty."}), 400

        result = predict_image(file_bytes)
        return jsonify(result), 200

    except ValueError as ve:
        logger.warning(f"Validation error during prediction: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Inference error: {e}", exc_info=True)
        return jsonify({
            "error": f"An error occurred during prediction inference: {str(e)}"
        }), 500


if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    local_ip = get_local_ip()
    print("=" * 65)
    print("  🌿 CropDisease Detection System (Enugu Focus) - Flask API")
    print("=" * 65)
    print(f"  • Local Machine:   http://localhost:{port}")
    print(f"  • Tecno / Android: http://{local_ip}:{port} (Connect to same Wi-Fi)")
    print(f"  • Health Check:    http://{local_ip}:{port}/health")
    print(f"  • Predict API:     POST http://{local_ip}:{port}/predict")
    print("=" * 65)

    app.run(host=host, port=port, debug=debug)
