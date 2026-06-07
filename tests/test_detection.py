import os
import pytest
from ultralytics import YOLO
from src.config import MODEL_PATH


def test_ultralytics_import():
    assert YOLO is not None


def test_model_path_exists_or_skip():
    if not os.path.exists(MODEL_PATH):
        pytest.skip(f"Model file not found: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    assert model is not None


def test_detection_sample_image_or_skip():
    sample_image = os.path.join('data', 'sample_poacher.jpg')
    if not os.path.exists(MODEL_PATH) or not os.path.exists(sample_image):
        pytest.skip("Sample image or model file not available")
    model = YOLO(MODEL_PATH)
    results = model(sample_image)
    assert isinstance(results, list)
