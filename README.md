# 🍅 Food Spoilage Detection System using Raspberry Pi, Camera & Gas Sensors

This project is an intelligent real-time system to detect **freshness or spoilage** of fruits and vegetables using a combination of **deep learning**, **gas sensor readings**, and **computer vision** on a **Raspberry Pi**.

---

## 🧠 What It Does

- 📸 Captures an image using Raspberry Pi Camera
- 🧪 Analyzes gases (Methane, Ammonia, etc.) using MQ4, MQ135, MQ137 sensors
- 🧠 Classifies the food item as **Fresh** or **Rotten** using a **ResNet18-based CNN**
- 🌐 Serves the result (prediction + gas sensor data + image) through a **Flask API**

---

## ⚙ Tech Stack

- **Hardware**: Raspberry Pi 4, PiCamera, MQ4, MQ135, MQ137 gas sensors
- **Software**: Python, Flask, TorchScript (PyTorch), OpenCV, PIL
- **Model**: ResNet18 trained on 26 food classes (Fresh/Rotten)
- **API Testing**: Postman

---

## 🧰 Requirements

- Raspberry Pi (3/4)
- PiCamera (enabled via `raspi-config`)
- MQ4 (Methane), MQ135 (CO2, NH3), MQ137 (Ammonia)
- Jumper Wires, Breadboard
- Python Libraries: `torch`, `torchvision`, `flask`, `PIL`, `RPi.GPIO`, `picamera2`

---

## 📦 Setup Instructions

```bash
# Clone repo
git clone https://github.com/yourusername/food-spoilage-detector.git
cd food-spoilage-detector

# Setup virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install torch torchvision flask pillow
