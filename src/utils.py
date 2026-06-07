import os
import time
import cv2
from src.config import LOG_FILE, OUTPUT_IMAGE
from src.db import save_alert

def save_alert_image(frame, path=OUTPUT_IMAGE):
    """Save the current frame as the alert image."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, frame)
    print(f"[✓] Image saved: {path}")
    return path

def write_log(class_name, confidence):
    """Log detection to file AND save to SQLite database."""
    # Write to text log file
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time.ctime()} | {class_name} | {confidence:.1f}%\n")
    print(f"[✓] Logged to {LOG_FILE}")
    
    # Also save to SQLite database
    save_alert(class_name, confidence, OUTPUT_IMAGE)
    print(f"[✓] Saved to database")

def can_send_alert(last_alert_time, cooldown_seconds):
    """Return True if cooldown period has passed."""
    return (time.time() - last_alert_time) >= cooldown_seconds