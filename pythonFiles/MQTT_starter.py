import paho.mqtt.client as mqtt
import subprocess

# User file, make this file yourself
import secrets

# Configure these variables yourself
MQTT_HOST = "192.168.1.116"
MQTT_PORT = 1883
pathToPythonfile = "/home/hvacpi/Documents/All-in-One-HVAC/pythonFiles/mqtt_receiver.py" 

def on_connect(eta_client, userdata, flags, rc):
    """
    Code to be run after connectiong to MQTT broker, subscribes to the relevant topic.
    """
    print(f"Connected to MQTT with result code {rc}")
    
    eta_client.subscribe("hoom/control/enable_pi")

def on_message(client, userdata, msg):
    """
    Code to be run after receiving a MQTT message, starts mqtt_receiver program.
    """
    payload = msg.payload.decode("utf-8")
    print(f"Received message: {payload} on topic: {msg.topic}")

    if payload == "True":
        print("Starting the program...")
        subprocess.Popen(["python3", pathToPythonfile])

# Setup the client
client = mqtt.Client()
client.username_pw_set(secrets.USERNAME, secrets.PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(MQTT_HOST, MQTT_PORT, 60)

print("Waiting for messages...")
client.loop_forever()
