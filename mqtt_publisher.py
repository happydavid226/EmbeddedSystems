import serial
import paho.mqtt.client as mqtt
import time
import sys

# Configuration
SERIAL_PORT = 'COM14'  # Your Arduino's port
BAUD_RATE = 9600
MQTT_BROKER = '157.173.101.159'
MQTT_PORT = 1883  # Standard MQTT port
MQTT_TOPIC = 'HappyDavid'
MQTT_CLIENT_ID = 'arduino_monitor_windows'

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        print(f"📤 Publishing to topic: {MQTT_TOPIC}")
    else:
        print(f"❌ Failed to connect to MQTT broker, return code: {rc}")

def on_publish(client, userdata, mid, reason_code, properties=None):
    print(f"✅ Message published successfully (ID: {mid})")

# Setup MQTT Client with callback API version 2.0
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

# Connect to MQTT broker
try:
    print(f"🔌 Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"❌ Failed to connect to MQTT broker: {e}")
    sys.exit(1)

# Setup Serial connection
try:
    print(f"🔗 Opening serial port {SERIAL_PORT} at {BAUD_RATE} baud...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for serial to initialize
    print("✅ Serial port opened successfully!")
except Exception as e:
    print(f"❌ Failed to open serial port: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("🚀 STARTING MQTT BRIDGE")
print("="*50)
print(f"📡 Reading from: {SERIAL_PORT}")
print(f"📤 Publishing to: {MQTT_BROKER}:{MQTT_PORT}/{MQTT_TOPIC}")
print("Press Ctrl+C to stop")
print("="*50 + "\n")

try:
    while True:
        if ser.in_waiting > 0:
            # Read a line from serial
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                print(f"📥 Received from Arduino: {line}")
                
                # Check if it's a temperature value (not an error message)
                try:
                    temp_value = float(line)
                    # Publish to MQTT
                    result = mqtt_client.publish(MQTT_TOPIC, str(temp_value))
                    if result.rc == mqtt.MQTT_ERR_SUCCESS:
                        print(f"📤 Published to MQTT: {temp_value}°C")
                    else:
                        print(f"❌ Failed to publish: {result.rc}")
                except ValueError:
                    # It's an error message or non-numeric
                    print(f"⚠️ Skipping non-numeric value: {line}")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    ser.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("✅ Done!")