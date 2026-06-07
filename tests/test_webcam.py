import cv2
import pytest

def test_webcam_accessible_or_skip():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.release()
        pytest.skip("Webcam not available")
    assert cap.isOpened()
    cap.release()
