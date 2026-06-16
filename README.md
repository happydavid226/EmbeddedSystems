# 🌡️ HappyDavid - Temperature Monitoring System

A complete embedded systems project that reads temperature from a DHT11 sensor using Arduino Uno, displays it on an LCD, and publishes data to an MQTT broker with a real-time web dashboard.

## 📋 Table of Contents
- [System Architecture](#system-architecture)
- [Hardware Components](#hardware-components)
- [Software Components](#software-components)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Dashboard](#dashboard)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## 🏗️ System Architecture

🚀 Installation & Setup
1. Hardware Setup
Connect the DHT11 Sensor:

Left pin → 5V

Middle pin → Digital Pin 4

Right pin → GND

Connect the LCD Display:

VCC → 5V

GND → GND

SDA → A4

SCL → A5

2. Arduino Setup
Open Arduino IDE

Install required libraries:

LiquidCrystal_I2C

DHT sensor library

Upload the Arduino sketch (arduino_temperature.ino)

Verify LCD shows "HappyDavid" and temperature

3. PC Python Bridge Setup
Install Python packages:

bash
pip install pyserial paho-mqtt
Update COM_PORT in mqtt_bridge.py to match your Arduino port:

python
SERIAL_PORT = 'COM14'  # Change to your port
Run the bridge:

bash
python mqtt_bridge.py
4. VPS Dashboard Setup
SSH into your VPS:

bash
ssh user216@157.173.101.159
Create project directory:

bash
mkdir -p ~/embedded_exam
cd ~/embedded_exam
Install Node.js dependencies:

bash
npm init -y
npm install express ws mqtt
Create server.js and public/index.html (see code above)

Start the dashboard:

bash
node server.js
Access the dashboard at: http://157.173.101.159:9216

📱 Usage
Normal Operation
Power on the Arduino

LCD displays "HappyDavid" on first row

LCD displays temperature on second row

Temperature data sent via serial every second

Start the Python Bridge

Reads serial data from Arduino

Displays in console

Publishes to MQTT broker

View the Dashboard

Open browser

Navigate to http://157.173.101.159:9216

See real-time temperature updates

Testing MQTT Subscription
On VPS, test if data is arriving:

bash
mosquitto_sub -h 157.173.101.159 -t HappyDavid
🎨 Dashboard Features
Feature	Description
Current Temperature	Large display showing current reading
Real-time Updates	Updates automatically when new data arrives
Temperature History	Shows last 20 readings with timestamps
Live Chart	Visual temperature trend with Chart.js
Connection Status	Shows WebSocket connection state
Responsive Design	Works on desktop, tablet, and mobile
Modern UI	Gradient design with smooth animations
📂 Project Structure
text
Embedded_Exam/
├── arduino_temperature.ino          # Arduino sketch
├── mqtt_bridge.py                   # Python MQTT bridge
├── README.md                        # This file
└── VPS_Dashboard/                   # VPS dashboard files
    ├── server.js                    # Node.js server
    ├── package.json                 # NPM dependencies
    └── public/
        └── index.html               # Dashboard HTML/CSS/JS
🔍 Troubleshooting
Arduino Issues
Problem	Solution
LCD shows nothing	Check I2C address (0x27 or 0x3F)
Sensor Error on LCD	Check wiring, use internal pull-up
Serial not working	Check baud rate (9600)
Python Bridge Issues
Problem	Solution
COM port access denied	Close Serial Monitor, run as admin
MQTT connection failed	Check broker IP and port (1883)
No serial data	Verify Arduino is connected and running
Dashboard Issues
Problem	Solution
Port 9216 not accessible	Check firewall settings
No data on dashboard	Verify MQTT topic "HappyDavid"
WebSocket disconnects	Check VPS network connection
🛠️ Maintenance
Keep Dashboard Running Permanently
Using PM2 (recommended):

bash
sudo npm install -g pm2
cd ~/embedded_exam
pm2 start server.js --name dashboard
pm2 save
pm2 startup
Monitor Dashboard
bash
pm2 status
pm2 logs dashboard
pm2 restart dashboard
📊 Communication Protocols
Connection	Protocol	Details
Arduino ↔ LCD	I2C	SDA (A4), SCL (A5)
Arduino ↔ PC	UART/Serial	9600 baud, COM14
PC ↔ MQTT	MQTT	TCP/IP, Port 1883
Dashboard ↔ Client	WebSocket	Real-time bidirectional
Client ↔ Browser	HTTP/WebSocket	Port 9216
📝 License
This project is created for educational purposes as part of an embedded systems examination.

👨‍💻 Author
HappyDavid

Candidate Name: HappyDavid

Project: Temperature Monitoring System

Date: 2026

🙏 Acknowledgments
Arduino community for libraries

MQTT for IoT communication

Chart.js for beautiful charts

📞 Support
For issues or questions:

Check the troubleshooting section above

Verify all connections

Check console logs for errors

🌟 Happy Monitoring! 🌟

text

---

This README provides:
- ✅ Complete system architecture diagram
- ✅ Hardware connections with pin mapping
- ✅ Software installation steps
- ✅ Usage instructions
- ✅ Troubleshooting guide
- ✅ Project structure
- ✅ Communication protocols
- ✅ All technical details

Save this as `README.md` in your project folder. You can also upload it to a GitHub repository if needed!
