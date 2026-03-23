#AI code ;)

import serial
import paho.mqtt.client as mqtt

# --- SETTINGS ---
MQTT_HOST = "192.168.1.116" # IP of your HA/Mosquitto Broker
ETA_MQTT_TOPIC = "hoom/control/eta"
ODA_MQTT_TOPIC = "hoom/control/oda"
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

def on_connect(eta_client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {rc}")
    
    topics = [
        ("hoom/control/oda", 0),
        ("hoom/control/eta", 0),
    ]
    eta_client.subscribe(topics)


def on_message(eta_client, userdata, msg):
    print(f"DEBUG: topic={msg.topic}, payload={msg.payload}")

client = mqtt.Client()
client.username_pw_set("pi_mqtt", "M0squ!tt0")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, 1883, 60)
client.loop_forever()
