import serial
import time
import json
import smtplib
import sqlite3
import requests
from email.message import EmailMessage
from flask import Flask, render_template, jsonify
from threading import Thread

# ==== CONFIG ====
SERIAL_PORT = 'COM7'  # Change for your system
BAUD_RATE = 9600
FIREBASE_URL = "https://yourprojectID.firebaseio.com/"
EMAIL_COOLDOWN = 10  # seconds
last_email_time = 0

# Mailtrap SMTP credentials
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
EMAIL_USERNAME = "4b7ada0ea947b8"
EMAIL_PASSWORD = "80d3fecb4d88e5"
EMAIL_FROM = "Motion Sensor <motionarduinoproj@gmail.com>"
EMAIL_TO = "chvistopher@gmail.com"

# ==== SETUP ====
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

# SQLite DB setup
conn = sqlite3.connect('sensor_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS readings
                  (timestamp TEXT, S1 INTEGER, S2 INTEGER, S3 INTEGER)''')

# Flask app for dashboard
app = Flask(__name__)
latest_data = {}

def send_email(message):
    global last_email_time
    if time.time() - last_email_time < EMAIL_COOLDOWN:
        return
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "Motion Alert"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email sent:", message)
            last_email_time = time.time()
    except Exception as e:
        print("Failed to send email:", e)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    return jsonify(latest_data)

def serial_reader():
    global latest_data
    while True:
        try:
            line = ser.readline().decode().strip()
            if not line:
                continue
            if line == "EMAIL_TRIGGER":
                send_email("Alert: Person has been still for over 1 minute.")
                continue
            data = json.loads(line)
            latest_data = data
            print("Received:", data)

            # Log to SQLite
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO readings VALUES (?, ?, ?, ?)",
                           (timestamp, data['S1'], data['S2'], data['S3']))
            conn.commit()

            # Push to Firebase
            try:
                requests.post(FIREBASE_URL, json=data)
            except Exception as e:
                print("Firebase error:", e)

            # Check for close object alert
            if any(int(v) < 10 for v in data.values()):
                send_email("Alert:Person detected within 10 cm!")
        except Exception as err:
            print("Error:", err)
            time.sleep(1)

if __name__ == '__main__':
    Thread(target=serial_reader, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
