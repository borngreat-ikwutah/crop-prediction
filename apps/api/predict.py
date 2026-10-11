"""
Prediction service for CropDisease Detection System.
Processes uploaded leaf images, detects blurriness/clutter, executes TFLite inference,
and associates the prediction with FAO treatment guidelines.
"""

import io
import logging
from typing import Dict, Any, Tuple
from PIL import Image
import numpy as np

from model_loader import get_interpreter
from treatment_db import LABELS, TREATMENTS, get_treatment, get_treatment_record

logger = logging.getLogger("CropDisease.Predict")

BLUR_VARIANCE_THRESHOLD = 50.0  # Threshold below which an image is considered blurry
CONFIDENCE_WARNING_THRESHOLD = 0.45  # Probabilities below this trigger multi-leaf/clutter warning


def estimate_blur_and_quality(img_rgb: Image.Image) -> Tuple[float, bool]:
    """
    Estimate image sharpness using discrete Laplacian variance on grayscale leaf image.
    Returns: (sharpness_score, is_blurry)
    """
    try:
        # Convert to grayscale numpy array
        gray = np.array(img_rgb.convert("L"), dtype=np.float32)

        # Fast 2D discrete Laplacian filter without needing full OpenCV
        # kernel: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        laplacian = (
            np.roll(gray, 1, axis=0)
            + np.roll(gray, -1, axis=0)
            + np.roll(gray, 1, axis=1)
            + np.roll(gray, -1, axis=1)
            - 4.0 * gray
        )
        # Avoid boundary artifacts by slicing margins
        laplacian_interior = laplacian[1:-1, 1:-1]
        variance = float(np.var(laplacian_interior))
        is_blurry = variance < BLUR_VARIANCE_THRESHOLD
        return variance, is_blurry
    except Exception as e:
        logger.warning(f"Could not compute sharpness score: {e}")
        return 100.0, False


def predict_image(file_bytes: bytes) -> Dict[str, Any]:
    """
    Main prediction pipeline:
    1. Parse and validate image bytes
    2. Check blur and visual quality
    3. Resize to 224x224, normalize /255.0, expand_dims
    4. Invoke global TFLite interpreter
    5. Retrieve disease class and FAO treatment
    6. Attach quality warnings if image is blurry or has multiple leaves/clutter
    """
    if not file_bytes or len(file_bytes) == 0:
        raise ValueError("Empty image data received.")

    try:
        raw_img = Image.open(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Invalid or corrupted image format: {e}")

    # Ensure 3-channel RGB
    img_rgb = raw_img.convert("RGB")

    # Assess blurriness
    sharpness_score, is_blurry = estimate_blur_and_quality(img_rgb)

    # Preprocessing: resize to 224x224
    img_resized = img_rgb.resize((224, 224), Image.Resampling.BILINEAR)

    # Convert to float32 and normalize to [0.0, 1.0]
    img_array = np.array(img_resized, dtype=np.float32) / 255.0

    # Expand dimensions to shape (1, 224, 224, 3)
    input_tensor = np.expand_dims(img_array, axis=0)

    # Retrieve global interpreter
    interpreter, input_details, output_details, is_mock = get_interpreter()

    # Feed input tensor and invoke
    interpreter.set_tensor(input_details[0]["index"], input_tensor)
    interpreter.invoke()

    # Retrieve predictions
    raw_output = interpreter.get_tensor(output_details[0]["index"])[0]

    # Handle softmax normalization if logits are returned
    if np.sum(raw_output) <= 0.0 or not np.isclose(np.sum(raw_output), 1.0, atol=1e-2):
        exp_preds = np.exp(raw_output - np.max(raw_output))
        probabilities = exp_preds / np.sum(exp_preds)
    else:
        probabilities = raw_output

    predicted_index = int(np.argmax(probabilities))
    predicted_label = LABELS[predicted_index]
    confidence = float(probabilities[predicted_index])

    # Check for blur or multi-leaf low confidence warnings
    warnings = []
    if is_blurry:
        warnings.append(
            "Image appears blurry or out of focus. For higher diagnostic accuracy, hold the phone steady or tap to focus."
        )

    if confidence < CONFIDENCE_WARNING_THRESHOLD:
        warnings.append(
            "Low diagnostic confidence. The photo may contain multiple overlapping leaves, wide background field, or distant foliage. "
            "Please capture a close-up photo of a single symptomatic leaf in bright natural light."
        )

    # Treatment lookup
    treatment_text = get_treatment(predicted_label)
    disease_meta = get_treatment_record(predicted_label)

    # Build response payload
    # Confidence formatted as percentage float (e.g. 94.6%)
    confidence_pct = round(confidence * 100.0, 2)

    all_scores = {
        label: round(float(prob) * 100.0, 2)
        for label, prob in zip(LABELS, probabilities)
    }

    response_data = {
        "disease": predicted_label,
        "disease_name": disease_meta.get("disease_name", predicted_label),
        "crop": disease_meta.get("crop", "Unknown"),
        "confidence": confidence_pct,
        "treatment": treatment_text,
        "short_treatment": disease_meta.get("short_treatment", treatment_text),
        "severity": disease_meta.get("severity", "Medium"),
        "all_probabilities": all_scores,
        "sharpness_score": round(sharpness_score, 1),
        "is_blurry": is_blurry,
        "warnings": warnings,
        "is_mock_inference": is_mock,
        "status": "success",
    }

    return response_data
