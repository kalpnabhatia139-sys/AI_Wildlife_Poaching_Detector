import smtplib
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from src.config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

# Fake GPS coordinates (Bandipur Tiger Reserve, Karnataka, India)
POACHER_LAT = "11.6667° N"
POACHER_LON = "76.6272° E"
LOCATION_NAME = "Bandipur Tiger Reserve, Karnataka, India"

def send_poacher_alert(image_path, confidence, class_name):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"⚠️ POACHER ALERT: {class_name} detected ({confidence:.1f}% confidence)"

        body = f"""
Wildlife Poaching Detection System

Alert Time: {time.ctime()}
Detected Object: {class_name}
Confidence: {confidence:.1f}%

📍 Location (Simulated):
   Reserve: {LOCATION_NAME}
   Coordinates: {POACHER_LAT}, {POACHER_LON}

Action Required: Please check the attached image and dispatch patrol.
"""
        msg.attach(MIMEText(body, 'plain'))

        with open(image_path, 'rb') as f:
            img_data = f.read()
            image = MIMEImage(img_data, name=image_path.split('/')[-1])
            msg.attach(image)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"[✓] Alert email sent to {RECEIVER_EMAIL} (GPS: {LOCATION_NAME})")
        return True
    except Exception as e:
        print(f"[✗] Failed to send email: {e}")
        return False