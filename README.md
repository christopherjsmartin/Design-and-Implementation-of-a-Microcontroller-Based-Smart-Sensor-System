Smart Sensor System: IoT Occupancy & Movement Tracker

Overview
This project is an IoT-based smart sensor system designed to monitor room occupancy and movement patterns in real-time. By integrating hardware (Arduino) with a cloud-based data pipeline (Python & Firebase), the system provides non-invasive, privacy-safe monitoring for energy conservation and smart home automation.

Features
+ Real-Time Occupancy Tracking: Uses three ultrasonic sensors to estimate occupant location (e.g., "Front Left", "Back Center") with a ±1 cm measurement tolerance.
+ Live Web Dashboard: A Flask-based web interface utilizing Chart.js to visualize sensor data trends in real-time, updating every 2 seconds.
+ Cloud Synchronization: Automatically streams all sensor data to a Firebase Realtime Database for remote access and historical logging.
+ Automated Alerts: Integrated email notification system via Mailtrap SMTP that triggers alerts for stillness (over 1 minute) or when an object is detected within 10 cm.
+ LCD Feedback: Local display of raw distances and estimated quadrant positions for immediate system status.

Hardware Components
1. Microcontroller: Arduino Uno R3.
2. Sensors: 3 × HC-SR04 Ultrasonic Distance Sensors.
3. Display: 16x2 I2C LCD (address 0x27).
4. Communication: USB Serial for base station connection.

Software Stack
+ Embedded: C++/Arduino IDE for data collection and signal processing.
+ Backend: Python 3 with pySerial, Flask, and Requests for the base station .
+ Database: Firebase Realtime Database & local SQLite logging.
+ Frontend: HTML/JavaScript with Chart.js for data visualization.

Project Structure
* arduino_sketch.ino: Firmware for distance calculation, stillness logic, and LCD management.
* base_station.py: Python script handling serial-to-cloud bridge and automated alerts.
* templates/dashboard.html: Real-time web visualization code.

Installation & Usage

1. Hardware Setup: Connect the ultrasonic sensors and LCD to the Arduino according to the circuit diagram provided in the documentation.
2. Arduino: Upload arduino_sketch.ino to the Uno.
3. Python Environment: Install dependencies (flask, pyserial, requests) and update SERIAL_PORT and FIREBASE_URL in base_station.py .
4. Run: Execute the Python script to start the base station and web server. Access the dashboard at http://localhost:5000.

Demonstration
Video Demo: Physical Setup & Alerts- https://youtube.com/shorts/x8SwGRLb3hY?si=-mmMLU2UkmEQ4Jzh
Video Demo: Screen Recording & Dashboard- https://youtu.be/exmt4W3Wafk?si=jSYny5zBWcfrLDv1
