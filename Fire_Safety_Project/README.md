# 🔥 Fire Safety Dashboard 

This project integrates **real-time Fire Detection (OpenCV)** with an **IoT Sensor Simulator** and a **Flask Web Dashboard**.

---

## 🚀 Features
- Real-time **fire detection** using OpenCV (`detect_fire.py`).
- Simulated **IoT sensors**:
  - Temperature (°C)
  - Smoke (ppm)
  - Gas MQ-2 sensor values
- Flask **dashboard** (`app.py`) showing:
  - Live camera feed
  - Sensor charts
  - Fire detection alerts with thresholds

---

## 📂 Project Structure
FireSafety_Project/
│── app.py # Flask dashboard
│── detect_fire.py # OpenCV fire detection
│── requirements.txt # Dependencies
│── README.md # Documentation
│── .gitignore # Ignore unnecessary files
│── templates/
│ └── index.html # Dashboard UI
│── static/ # (Optional assets like CSS/JS)
