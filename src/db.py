import sqlite3
import os
from datetime import datetime
import statistics
import re

DB_PATH = "outputs/alerts.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            object_class TEXT,
            confidence REAL,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_alert(object_class, confidence, image_path):
    # Store timestamps in ISO format (YYYY-MM-DD HH:MM:SS) for easier grouping
    iso_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Also keep a human-readable version if needed, but we'll just use ISO
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO alerts (timestamp, object_class, confidence, image_path)
        VALUES (?, ?, ?, ?)
    ''', (iso_timestamp, object_class, confidence, image_path))
    conn.commit()
    conn.close()

def get_recent_alerts(limit=10):
    if not os.path.exists(DB_PATH):
        return ["No alerts yet. Run 'python run.py' and trigger detection."]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT timestamp, object_class, confidence FROM alerts ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return ["No alerts yet. Run 'python run.py' and trigger detection."]
    # Convert ISO timestamps to readable format for display
    display_rows = []
    for r in rows:
        try:
            dt = datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S")
            readable = dt.strftime("%a %b %d %H:%M:%S %Y")
        except:
            readable = r[0]
        display_rows.append(f"{readable} | {r[1]} | {r[2]}%")
    return display_rows

def get_stats():
    if not os.path.exists(DB_PATH):
        return (0, None, [], [])
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM alerts')
        total = c.fetchone()[0]
        if total == 0:
            conn.close()
            return (0, None, [], [])
        
        # Get last alert timestamp (display in readable format)
        c.execute('SELECT timestamp FROM alerts ORDER BY id DESC LIMIT 1')
        last_ts = c.fetchone()[0]
        try:
            dt = datetime.strptime(last_ts, "%Y-%m-%d %H:%M:%S")
            last_timestamp = dt.strftime("%a %b %d %H:%M:%S %Y")
        except:
            last_timestamp = last_ts
        
        # Daily counts: group by date using ISO date part
        c.execute("SELECT DATE(timestamp) as day, COUNT(*) FROM alerts GROUP BY day ORDER BY day")
        daily = c.fetchall()   # each row: ('2026-05-21', 5)
        
        # Confidence list
        c.execute("SELECT confidence FROM alerts")
        confidences = [row[0] for row in c.fetchall()]
        conn.close()
        return (total, last_timestamp, daily, confidences)
    except Exception as e:
        print(f"Database error in get_stats: {e}")
        return (0, None, [], [])

def get_anomaly_status():
    """
    Returns (is_anomaly, message) using daily counts from properly parsed dates.
    """
    if not os.path.exists(DB_PATH):
        return (False, "No data yet – run the detector to create alerts.")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Use DATE(timestamp) assuming ISO format (works for new alerts; old ones may be parsed differently)
    # But old timestamps are in non-ISO format, so we need to handle gracefully.
    # Safer: fetch all timestamps and count in Python.
    c.execute("SELECT timestamp FROM alerts")
    rows = c.fetchall()
    conn.close()
    
    if len(rows) < 2:
        return (False, "Insufficient data (need at least 2 alerts).")
    
    # Parse timestamps to get dates
    from collections import defaultdict
    day_counts = defaultdict(int)
    for (ts,) in rows:
        try:
            # Try ISO first
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except:
            # Try custom format like "Thu May 21 14:20:14 2026"
            try:
                dt = datetime.strptime(ts, "%a %b %d %H:%M:%S %Y")
            except:
                continue
        day_counts[dt.date()] += 1
    
    # Sort dates
    sorted_dates = sorted(day_counts.keys())
    if len(sorted_dates) < 2:
        return (False, "Need at least 2 days of data for anomaly detection.")
    
    # Last day (today) and previous days
    today = sorted_dates[-1]
    today_count = day_counts[today]
    prev_counts = [day_counts[d] for d in sorted_dates[:-1]]
    
    if len(prev_counts) < 2:
        return (False, "Need more historical data (at least 2 previous days).")
    
    mean = statistics.mean(prev_counts)
    stdev = statistics.stdev(prev_counts)
    threshold = mean + (1.5 * stdev)
    
    if today_count > threshold:
        message = f"⚠️ Anomaly detected! Today's alerts ({today_count}) exceed average ({mean:.1f}) + 1.5σ. Possible poaching activity."
        return (True, message)
    else:
        message = f"✅ Normal activity. Average alerts over last {len(prev_counts)} days: {mean:.1f}. Today: {today_count}."
        return (False, message)