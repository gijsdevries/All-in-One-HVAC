import serial
import paho.mqtt.client as mqtt

#TOPICS
ETA_TOPIC = "hoom/control/eta"
ODA_TOPIC = "hoom/control/oda"
TEC_TOPIC = "hoom/control/tec"
PELTIER_TOPIC = "hoom/control/peltier"
ABORT_TOPIC = "hoom/control/abort"

#COM_PORTS
SERIAL_PORT_OCTO = "/dev/ttyACM0" 
SERIAL_PORT_TEC = "/dev/ttyUSB0"
BAUD_RATE = 115200 

#SETTINGS
MQTT_HOST = "192.168.1.116" # IP of your HA/Mosquitto Broker

#LOGIN
username = "pi_mqtt"
password = "M0squ!tt0"

# Initialize Serial
try:
    ser_octo = serial.Serial(SERIAL_PORT_OCTO, BAUD_RATE, timeout=1)
    print(f"Connected to Serial: {SERIAL_PORT_OCTO}")
    ser_tec = serial.Serial(SERIAL_PORT_TEC, BAUD_RATE, timeout=1)
    print(f"Connected to Serial: {SERIAL_PORT_TEC}")
except Exception as e:
    print(f"Serial Error: {e}")
    exit()

def on_connect(eta_client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {rc}")
    
    topics = [
        (ODA_TOPIC, 0),
        (ETA_TOPIC, 0),
        (TEC_TOPIC, 0),
        (PELTIER_TOPIC, 0),
        (ABORT_TOPIC, 0),
    ]
    eta_client.subscribe(topics)

def on_message(eta_client, userdata, msg):
    print(f"DEBUG: topic={msg.topic}, payload={msg.payload}")

    if msg.topic == ETA_TOPIC:
        msg.payload = int(msg.payload)
        ser_octo.write(f"M0 eta_fan D{msg.payload}\r".encode('utf-8'))
    elif msg.topic == ODA_TOPIC:
        msg.payload = int(msg.payload)
        ser_octo.write(f"M0 oda_fan D{msg.payload}\r".encode('utf-8'))
    elif msg.topic == TEC_TOPIC:
        msg.payload = bool(msg.payload)
        ser_tec.write(f"set 2 {msg.payload}\r".encode('utf-8'))
    elif msg.topic == PELTIER_TOPIC:
        msg.payload = float(msg.payload)
        ser_tec.write(f"set 1 {msg.payload}\r".encode('utf-8'))
    elif msg.topic == ABORT_TOPIC:
        #TODO stop all commands??
        quit()

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, 1883, 60)
client.loop_forever()
