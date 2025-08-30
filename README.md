🚨 Fire Safety AI + IoT Project 🌐
🧩 Problem to Solve

Fire accidents 🔥 in hospitals 🏥, rural areas 🌾, and smart cities 🌆 often remain undetected until it’s too late.

Lack of real-time alerts ⏰ and integrated dashboards 📊 for monitoring increases risk.

Need for an affordable, AI + IoT powered system 💡 that can save lives 👨‍👩‍👧‍👦 and resources.

🌍 Domain

🤖 Artificial Intelligence (AI) → Real-time fire detection using computer vision.

📡 Internet of Things (IoT) → Sensor-based monitoring (temperature 🌡️, smoke ☁️, gas 🛢️).

🌐 Web Tech → Live dashboard 📊 + video feed 🎥 accessible anywhere.

🔄 Replicate → Modify → Innovate

Replicate:

Use basic OpenCV fire detection 🔥.

Build a simple Flask dashboard 💻.

Modify:

Add IoT sensor integration 📡 (temperature, smoke, gas).

Improve accuracy ✅ (combine multiple inputs → fewer false alarms).

Design visual dashboard 🎨 (real-time charts, thresholds in red 🟥).

Innovate:

Smart AI-driven alerts 🚨 (SMS/WhatsApp/Cloud integration).

Predictive analytics 📈 (detect risk before fire spreads).

Scalable deployment ☁️ (edge devices + cloud storage).

Community integration 🏘️ (fire station direct alerts 🚒).

🌟 Why This Matters

🏥 Hospitals: Protect vulnerable patients.

🌾 Rural Areas: Works even with limited infrastructure.

🌆 Smart Cities: Integrates into existing safety networks.

💡 Scalable + Affordable: A solution that anyone can deploy.

🎯 Vision

“An AI + IoT powered 🔥 fire safety network that saves lives, prevents disasters, and builds safer communities 🌍.”# 🔥 Fire Safety Dashboard 

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
