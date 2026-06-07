from flask import Flask, render_template, send_file
import os
import json
from src.db import get_recent_alerts, get_stats, get_anomaly_status
from src.config import OUTPUT_IMAGE

app = Flask(__name__)

@app.route('/')
def index():
    alerts = get_recent_alerts(10)
    stats = get_stats()
    
    # Safe unpacking – even if stats is malformed, we default to empty values
    if isinstance(stats, tuple) and len(stats) == 4:
        total, last_timestamp, daily, confidences = stats
    else:
        total, last_timestamp, daily, confidences = 0, None, [], []
    
    # Ensure lists are never None
    daily = daily or []
    confidences = confidences or []
    
    chart_dates = [row[0] for row in daily] if daily else []
    chart_counts = [row[1] for row in daily] if daily else []
    
    image_exists = os.path.exists(OUTPUT_IMAGE)
    
    # Get anomaly detection status
    is_anomaly, anomaly_message = get_anomaly_status()
    
    return render_template('dashboard.html',
                           alerts=alerts,
                           image_exists=image_exists,
                           chart_dates=json.dumps(chart_dates),
                           chart_counts=json.dumps(chart_counts),
                           confidences=json.dumps(confidences),
                           anomaly_message=anomaly_message)

@app.route('/image')
def serve_image():
    if os.path.exists(OUTPUT_IMAGE):
        return send_file(OUTPUT_IMAGE, mimetype='image/jpeg')
    return "No image yet", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Starting Poacher Detector Dashboard on port {port}...")
    app.run(host='0.0.0.0', port=port)