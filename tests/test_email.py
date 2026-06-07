import os
import cv2
import numpy as np
from unittest.mock import patch
from src.alert import send_poacher_alert


def test_send_poacher_alert_with_mocked_smtp(tmp_path):
    image_path = tmp_path / "test.jpg"
    dummy = np.ones((480, 640, 3), dtype=np.uint8) * 255
    cv2.putText(dummy, "TEST", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imwrite(str(image_path), dummy)

    with patch('src.alert.smtplib.SMTP') as mock_smtp:
        smtp_instance = mock_smtp.return_value
        smtp_instance.starttls.return_value = None
        smtp_instance.login.return_value = None
        smtp_instance.send_message.return_value = None
        smtp_instance.quit.return_value = None

        result = send_poacher_alert(str(image_path), 90.0, "test")

    assert result is True
