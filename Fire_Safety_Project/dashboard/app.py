#!/usr/bin/env python3
"""
Improved Fire Safety Dashboard
- Live video with real fire detection (OpenCV color filtering).
- Sensor simulation (temperature, smoke, gas).
- Fire alert comes from actual video detection + sensors.
- Chart with thresholds + larger layout for video and charts.
"""
from flask import Flask, render_template, Response, jsonify
import cv2, threading, time, random

app = Flask(__name__)

# -----------------------
# Video Fire Detection
# -----------------------
camera = cv2.VideoCapture(0)
fire_detected_global = False
fire_triggered_count = 0

def detect_fire_in_frame(frame):
    """Detect fire-like regions using HSV color range."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Fire-like colors (orange/red/yellow)
    lower = (18, 50, 50)
    upper = (35, 255, 255)
    mask = cv2.inRange(hsv, lower, upper)

    # Count how many pixels match fire color
    fire_pixels = cv2.countNonZero(mask)
    if fire_pixels > 5000:  # threshold (tune if needed)
        return True
    return False

def gen_frames():
    global fire_detected_global, fire_triggered_count
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Run fire detection
            fire_here = detect_fire_in_frame(frame)

            # Stability: require 3 consecutive detections
            if fire_here:
                fire_triggered_count += 1
            else:
                fire_triggered_count = max(0, fire_triggered_count - 1)

            fire_detected_global = fire_triggered_count >= 3

            # Overlay on frame
            status_text = "FIRE DETECTED!" if fire_detected_global else "Safe"
            color = (0, 0, 255) if fire_detected_global else (0, 255, 0)
            cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                        1.2, color, 3)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------------
# Sensor Simulation
# -----------------------
sensor_data = {"temperature_c": 25, "smoke_ppm": 100, "gas_mq2": 200}

def sensor_loop():
    global sensor_data
    while True:
        sensor_data = {
            "temperature_c": round(random.uniform(20, 120), 2),
            "smoke_ppm": round(random.uniform(50, 600), 1),
            "gas_mq2": round(random.uniform(100, 1000), 1),
            "timestamp": time.time()
        }
        time.sleep(2)

@app.route('/sensors')
def sensors():
    return jsonify(sensor_data)

@app.route('/status')
def status():
    return jsonify({"detected": fire_detected_global})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    t = threading.Thread(target=sensor_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=False)
