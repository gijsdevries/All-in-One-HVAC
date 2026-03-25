import paho.mqtt.client as mqtt
import subprocess

import secrets

# MQTT host
MQTT_HOST = "192.168.1.116"
MQTT_PORT = 1883

def on_connect(eta_client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {rc}")
    
    eta_client.subscribe("hoom/control/enable_pi")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"Received message: {payload} on topic: {msg.topic}")

    if payload == "True":
        print("Starting the program...")
        subprocess.Popen(["python3", "/home/hvacpi/Documents/sensoren_klimaatkamer/pythonFiles/mqtt_receiver.py"])

# Setup the client
client = mqtt.Client()
client.username_pw_set(secrets.USERNAME, secrets.PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(MQTT_HOST, MQTT_PORT, 60)

print("Waiting for messages...")
client.loop_forever()
