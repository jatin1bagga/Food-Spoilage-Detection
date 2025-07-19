from flask import Flask, jsonify, send_file
import torch
from torchvision import transforms
from PIL import Image
from picamera2 import Picamera2
import time
import os
import signal
import subprocess
import RPi.GPIO as GPIO

# 🔹 Flask setup
app = Flask(_name_)
IMAGE_PATH = "/home/jatin/Desktop/PROJECT/captured.jpg"

# 🔹 Load TorchScript model
model = torch.jit.load("resnet18_traced.pt", map_location='cpu')
model.eval()

# 🔹 Class labels
class_names = [
    'FreshApple', 'FreshBanana', 'FreshBellpepper', 'FreshBittergroud',
    'FreshCapsicum', 'FreshCarrot', 'FreshCucumber', 'FreshMango', 'FreshOkra',
    'FreshOrange', 'FreshPotato', 'FreshStrawberry', 'FreshTomato',
    'RottenApple', 'RottenBanana', 'RottenBellpepper', 'RottenBittergroud',
    'RottenCapsicum', 'RottenCarrot', 'RottenCucumber', 'RottenMango',
    'RottenOkra', 'RottenOrange', 'RottenPotato', 'RottenStrawberry', 'RottenTomato'
]

# 🔹 Image Transform
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])

# 🔹 GPIO Pins
MQ4_PIN = 17
MQ135_PIN = 27
MQ137_PIN = 22

# 🔹 Free port if stuck
def free_port(port):
    try:
        pid = subprocess.check_output(f"lsof -t -i:{port}", shell=True).decode().strip()
        if pid:
            os.kill(int(pid), signal.SIGKILL)
    except:
        pass

# 🔹 Capture Image
def capture_image():
    try:
        cam = Picamera2()
        cam.configure(cam.create_still_configuration())
        cam.start()
        time.sleep(2)
        cam.capture_file(IMAGE_PATH)
        cam.stop()
        del cam
    except Exception as e:
        print("❌ Camera Error:", e)

# 🔹 Predict Image
def predict_image():
    img = Image.open(IMAGE_PATH).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        _, pred = torch.max(output, 1)
    return class_names[pred.item()]

# 🔹 Read Gas Sensor
def read_gas_sensors():
    try:
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(MQ4_PIN, GPIO.IN)
        GPIO.setup(MQ135_PIN, GPIO.IN)
        GPIO.setup(MQ137_PIN, GPIO.IN)

        mq4 = GPIO.input(MQ4_PIN)
        mq135 = GPIO.input(MQ135_PIN)
        mq137 = GPIO.input(MQ137_PIN)

        return {
            "MQ4_Methane": mq4,
            "MQ135_AirQuality": mq135,
            "MQ137_Ammonia": mq137
        }

    except Exception as e:
        print("❌ Gas Sensor Error:", e)
        return {"error": "Gas sensor read failed"}

    finally:
        GPIO.cleanup()

# 🔹 Predict Route
@app.route('/predict', methods=['GET'])
def predict():
    capture_image()
    prediction = predict_image()
    gas_values = read_gas_sensors()

    return jsonify({
        "prediction": prediction,
        "gas_sensors": gas_values,
        "image_url": "http://<YOUR-PI-IP>:5001/image"
    })

# 🔹 Image Route
@app.route('/image', methods=['GET'])
def image():
    return send_file(IMAGE_PATH, mimetype='image/jpeg')

# 🔹 Run the app
if _name_ == '_main_':
    free_port(5001)
    app.run(host='0.0.0.0', port=5001)
