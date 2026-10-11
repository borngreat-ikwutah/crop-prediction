"""
Model Loader for CropDisease Detection System.
Loads crop_model.tflite ONCE globally at startup using tf.lite.Interpreter.
Tensors are allocated once to optimize inference latency on mobile/laptop edge hardware.
"""

import os
import sys
import logging
from typing import Optional, Tuple, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CropDisease.ModelLoader")

# Default search paths for model
CANDIDATE_PATHS = [
    os.environ.get("MODEL_PATH", ""),
    os.path.join(os.path.dirname(__file__), "..", "..", "models", "crop_model.tflite"),
    os.path.join(os.path.dirname(__file__), "models", "crop_model.tflite"),
    os.path.join(os.getcwd(), "models", "crop_model.tflite"),
]

GLOBAL_INTERPRETER: Optional[Any] = None
INPUT_DETAILS: Optional[list] = None
OUTPUT_DETAILS: Optional[list] = None
RESOLVED_MODEL_PATH: Optional[str] = None
IS_MOCK_MODEL: bool = False


def _find_model_file() -> Optional[str]:
    """Find the first existing crop_model.tflite from candidate paths."""
    for path in CANDIDATE_PATHS:
        if path and os.path.isfile(path):
            return os.path.abspath(path)
    return None


class MockInterpreter:
    """
    Fallback interpreter used only when crop_model.tflite has not yet been generated.
    Allows the Flask API to start and serve health checks and mock predictions.
    """
    def __init__(self):
        self._input_data = None
        self._output_data = None

    def allocate_tensors(self):
        pass

    def get_input_details(self):
        return [{"index": 0, "shape": [1, 224, 224, 3], "dtype": "float32"}]

    def get_output_details(self):
        return [{"index": 0, "shape": [1, 4], "dtype": "float32"}]

    def set_tensor(self, index, tensor):
        self._input_data = tensor

    def invoke(self):
        import numpy as np
        # Return a simulated distribution if real model not loaded
        # Uses green/yellow channel hints from input image to simulate output
        if self._input_data is not None:
            mean_vals = np.mean(self._input_data, axis=(1, 2))[0]
            # [R, G, B]
            r, g, b = mean_vals[0], mean_vals[1], mean_vals[2]
            if g > r and g > b:
                # Greenish -> likely Healthy or mild CMD
                probs = np.array([[0.10, 0.05, 0.05, 0.80]], dtype=np.float32)
            elif r > g and b < 0.4:
                # Brown/blight spot colors
                probs = np.array([[0.10, 0.70, 0.15, 0.05]], dtype=np.float32)
            else:
                probs = np.array([[0.65, 0.15, 0.15, 0.05]], dtype=np.float32)
        else:
            probs = np.array([[0.25, 0.25, 0.25, 0.25]], dtype=np.float32)
        self._output_data = probs

    def get_tensor(self, index):
        return self._output_data


def init_interpreter() -> Tuple[Any, Optional[list], Optional[list], bool]:
    """
    Load crop_model.tflite once globally.
    Returns: (interpreter, input_details, output_details, is_mock)
    """
    global GLOBAL_INTERPRETER, INPUT_DETAILS, OUTPUT_DETAILS, RESOLVED_MODEL_PATH, IS_MOCK_MODEL

    model_path = _find_model_file()

    # Try loading TensorFlow / TFLite interpreter
    tf_interpreter = None
    try:
        import tensorflow as tf
        InterpreterClass = tf.lite.Interpreter
    except ImportError:
        try:
            import tflite_runtime.interpreter as tflite
            InterpreterClass = tflite.Interpreter
        except ImportError:
            InterpreterClass = None

    if InterpreterClass is not None and model_path is not None:
        try:
            logger.info(f"Loading TFLite model from {model_path}...")
            tf_interpreter = InterpreterClass(model_path=model_path)
            tf_interpreter.allocate_tensors()
            INPUT_DETAILS = tf_interpreter.get_input_details()
            OUTPUT_DETAILS = tf_interpreter.get_output_details()
            GLOBAL_INTERPRETER = tf_interpreter
            RESOLVED_MODEL_PATH = model_path
            IS_MOCK_MODEL = False
            logger.info(
                f"Successfully loaded crop_model.tflite! "
                f"Input shape: {INPUT_DETAILS[0]['shape']}, Output shape: {OUTPUT_DETAILS[0]['shape']}"
            )
            return GLOBAL_INTERPRETER, INPUT_DETAILS, OUTPUT_DETAILS, False
        except Exception as e:
            logger.error(f"Failed to load TFLite model at {model_path}: {e}")

    # Fallback to mock interpreter
    logger.warning(
        "Real crop_model.tflite not found or TensorFlow runtime not ready. "
        "Using fallback mock interpreter for development/testing. "
        "Run `python training/train.py` to train and export the genuine TFLite model."
    )
    GLOBAL_INTERPRETER = MockInterpreter()
    GLOBAL_INTERPRETER.allocate_tensors()
    INPUT_DETAILS = GLOBAL_INTERPRETER.get_input_details()
    OUTPUT_DETAILS = GLOBAL_INTERPRETER.get_output_details()
    RESOLVED_MODEL_PATH = model_path
    IS_MOCK_MODEL = True
    return GLOBAL_INTERPRETER, INPUT_DETAILS, OUTPUT_DETAILS, True


def get_interpreter():
    """Retrieve the global interpreter, initializing if not done already."""
    global GLOBAL_INTERPRETER
    if GLOBAL_INTERPRETER is None:
        init_interpreter()
    return GLOBAL_INTERPRETER, INPUT_DETAILS, OUTPUT_DETAILS, IS_MOCK_MODEL


def get_model_status() -> dict:
    """Return runtime status of the ML model."""
    return {
        "model_loaded": GLOBAL_INTERPRETER is not None and not IS_MOCK_MODEL,
        "is_mock": IS_MOCK_MODEL,
        "model_path": RESOLVED_MODEL_PATH or "models/crop_model.tflite (pending training)",
        "input_shape": INPUT_DETAILS[0]["shape"] if INPUT_DETAILS else [1, 224, 224, 3],
        "output_shape": OUTPUT_DETAILS[0]["shape"] if OUTPUT_DETAILS else [1, 4],
    }


# Auto-initialize globally at module import
init_interpreter()
