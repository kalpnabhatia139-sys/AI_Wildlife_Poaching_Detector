import os

CONFIDENCE_THRESHOLD = 0.7
ALERT_COOLDOWN = 30
TARGET_CLASSES = ['person', 'car', 'truck', 'motorcycle']

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- Email Settings (now using environment variables for security) ---
# For local testing, you can set these in a .env file or directly in your terminal.
# For cloud (Render, Koyeb), set them as environment variables.
SENDER_EMAIL = os.environ.get('EMAIL_USER', "kalpnabhatia139@gmail.com")
SENDER_PASSWORD = os.environ.get('EMAIL_PASS', "fsjz umxv dvyw upqk")
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', "kalpnabhatia139@gmail.com")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
OUTPUTS_DIR = os.path.join(ROOT_DIR, 'outputs')

MODEL_FILENAME = "yolov8n.pt"
LOCAL_MODEL_PATH = os.path.join(MODELS_DIR, MODEL_FILENAME)
MODEL_PATH = LOCAL_MODEL_PATH if os.path.exists(LOCAL_MODEL_PATH) else os.path.join(ROOT_DIR, MODEL_FILENAME)
OUTPUT_IMAGE = os.path.join(OUTPUTS_DIR, "poacher_alert.jpg")
LOG_FILE = os.path.join(OUTPUTS_DIR, "alert_log.txt")
CAMERA_ID = 0

# ========== Weapon Detection Settings ==========
WEAPON_MODEL_PATH = os.path.join(MODELS_DIR, "threat_best.pt")   # Path to your downloaded weapon model
WEAPON_CONFIDENCE = 0.4                     # Lower threshold for high sensitivity
WEAPON_CLASSES = ['gun', 'explosive', 'grenade', 'knife']