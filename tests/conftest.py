"""Shared pytest fixtures for AI Wildlife Poaching Detector tests."""
import os
import pytest
import numpy as np
import cv2
from pathlib import Path


@pytest.fixture
def sample_image_path(tmp_path):
    """Create a temporary sample image for testing."""
    image_path = tmp_path / "sample.jpg"
    dummy = np.ones((480, 640, 3), dtype=np.uint8) * 128
    cv2.putText(dummy, "SAMPLE", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite(str(image_path), dummy)
    return str(image_path)


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory for test outputs."""
    output_path = tmp_path / "outputs"
    output_path.mkdir(exist_ok=True)
    return str(output_path)


@pytest.fixture
def config_mock(monkeypatch, output_dir):
    """Mock the configuration with test paths."""
    from src import config
    monkeypatch.setattr(config, "LOG_FILE", os.path.join(output_dir, "test_log.txt"))
    monkeypatch.setattr(config, "OUTPUT_IMAGE", os.path.join(output_dir, "test_output.jpg"))
    return config


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def data_dir(project_root):
    """Get the data directory path."""
    return project_root / "data"


@pytest.fixture
def models_dir(project_root):
    """Get the models directory path."""
    return project_root / "models"
