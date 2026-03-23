#AI code ;)

import serial
import paho.mqtt.client as mqtt

# --- SETTINGS ---
MQTT_HOST = "192.168.1.116" # IP of your HA/Mosquitto Broker
MQTT_TOPIC = "hoom/commands/test"
SERIAL_PORT = "/dev/ttyACM0" 
BAUD_RATE = 115200 
# ----------------


# Initialize Serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Serial: {SERIAL_PORT}")
except Exception as e:
    print(f"Serial Error: {e}")
    exit()

def on_connect(client, userdata, flags, rc):
   print(f"Connected to MQTT with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"Received message on topic '{msg.topic}': {payload}")
    
    # Send to USB
    ser.write(f"{payload}\n".encode('utf-8'))

client = mqtt.Client()
client.username_pw_set("pi_mqtt", "M0squ!tt0")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, 1883, 60)
client.loop_forever()
