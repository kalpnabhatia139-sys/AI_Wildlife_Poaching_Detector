import cv2
import time
from ultralytics import YOLO
from src.config import (MODEL_PATH, CONFIDENCE_THRESHOLD, ALERT_COOLDOWN,
                        TARGET_CLASSES, CAMERA_ID, WEAPON_MODEL_PATH,
                        WEAPON_CONFIDENCE, WEAPON_CLASSES)
from src.alert import send_poacher_alert
from src.utils import save_alert_image, write_log, can_send_alert

def run_detector():
    print("Starting AI Poacher Detector with Weapon Detection...")
    print("Press 'q' to quit, 'p' to pause/resume.")

    # Load both models
    person_model = YOLO(MODEL_PATH)
    weapon_model = YOLO(WEAPON_MODEL_PATH)

    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_alert_time = 0
    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break

            # Run person/vehicle detection on full frame
            person_results = person_model(frame, stream=False)
            weapon_detected = False
            weapon_class_name = ""

            for r in person_results:
                if r.boxes is not None:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = person_model.names[cls_id]

                        if class_name in TARGET_CLASSES and conf > CONFIDENCE_THRESHOLD:
                            # Draw green box for person/vehicle
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            label = f"{class_name} {conf:.2f}"
                            cv2.putText(frame, label, (x1, y1-10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            # Crop the detected region for weapon analysis
                            roi = frame[y1:y2, x1:x2]
                            if roi.size != 0:
                                weapon_results = weapon_model(roi)
                                for wr in weapon_results:
                                    if wr.boxes is not None:
                                        for wbox in wr.boxes:
                                            wcls_id = int(wbox.cls[0])
                                            wconf = float(wbox.conf[0])
                                            wname = weapon_model.names[wcls_id]
                                            if wname in WEAPON_CLASSES and wconf > WEAPON_CONFIDENCE:
                                                weapon_detected = True
                                                weapon_class_name = wname
                                                # Draw yellow box for weapon (adjust coordinates to original frame)
                                                wx1, wy1, wx2, wy2 = map(int, wbox.xyxy[0])
                                                cv2.rectangle(frame, (x1+wx1, y1+wy1), (x1+wx2, y1+wy2), (0, 255, 255), 2)
                                                cv2.putText(frame, f"WEAPON: {wname}", (x1+wx1, y1+wy1-10),
                                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

            # Trigger critical alert if weapon found and cooldown passed
            current_time = time.time()
            if weapon_detected and can_send_alert(last_alert_time, ALERT_COOLDOWN):
                img_path = save_alert_image(frame)
                send_poacher_alert(img_path, 99.9, f"WEAPON ({weapon_class_name})")
                write_log(f"WEAPON_{weapon_class_name}", 99.9)
                last_alert_time = current_time
                print(f"⚠️ CRITICAL ALERT: {weapon_class_name} detected!")

            cv2.imshow("AI Poacher Detector - Press 'q' to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
            print("Paused" if paused else "Resumed")

    cap.release()
    cv2.destroyAllWindows()
    print("System stopped.")