from colorama import Fore, Back, Style
import serial
import paho.mqtt.client as mqtt
import os
import time

#user file
import secrets

highPowerOn = False

#TOPICS
ETA_TOPIC = "hoom/control/eta"
ODA_TOPIC = "hoom/control/oda"
TEC_TOPIC = "hoom/control/tec"
PELTIER_TOPIC = "hoom/control/peltier"
ENABLE_PI = "hoom/control/enable_pi"
VALVE_TOPIC = "hoom/control/valve"

#COM_PORTS
dirPathGijs = "/home/gijs"
dirPathPi = "/home/hvacpi"
    
if os.path.isdir(dirPathGijs):
    SERIAL_PORT_OCTO = "/dev/ttyS4" 
    SERIAL_PORT_TEC = "/dev/ttyS4"
elif os.path.isdir(dirPathPi):
    SERIAL_PORT_OCTO = "/dev/ttyACM0" 
    SERIAL_PORT_TEC = "/dev/ttyUSB0"

BAUD_RATE_OCTO = 115200 
BAUD_RATE_TEC = 9600 

#SETTINGS
MQTT_HOST = "192.168.1.116" # IP of your HA/Mosquitto Broker

# Initialize Serial
try:
    ser_octo = serial.Serial(SERIAL_PORT_OCTO, BAUD_RATE_OCTO, timeout=1)
    ser_tec = serial.Serial(SERIAL_PORT_TEC, BAUD_RATE_TEC, timeout=1)
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
        (VALVE_TOPIC, 0),
        (ENABLE_PI, 0),
    ]
    eta_client.subscribe(topics)

def on_message(eta_client, userdata, msg):

    if msg.topic == ETA_TOPIC:
        msg.payload = int(msg.payload)
        serial_buffer = f"M0 eta_fan D{msg.payload}\r" 
        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

        line = ser_octo.readline()
        print(Fore.CYAN + "OCTO: " + line.decode().strip())

    elif msg.topic == ODA_TOPIC:
        msg.payload = int(msg.payload)
        serial_buffer = f"M0 oda_fan D{msg.payload}\r" 
        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

        line = ser_octo.readline()
        print(Fore.CYAN + "OCTO: " + line.decode().strip())

    elif msg.topic == TEC_TOPIC:

        msg.payload = msg.payload.decode('utf-8')

        if msg.payload == 'False':
            serial_buffer = "set 2 0\r" 
        else:
            serial_buffer = "set 2 1\r" 

        ser_tec.write(serial_buffer.encode('utf-8'))
        print(Fore.GREEN + "SENT TEC: " + serial_buffer)

        line = ser_tec.readline()
        print(Fore.LIGHTGREEN_EX + "TEC : " + line.decode().strip())

    elif msg.topic == PELTIER_TOPIC:
        msg.payload = float(msg.payload)
        serial_buffer = f"set 1 {msg.payload}\r" 
        ser_tec.write(serial_buffer.encode('utf-8'))
        print(Fore.GREEN + "SENT TEC: " + serial_buffer)

        line = ser_tec.readline()
        print(Fore.LIGHTGREEN_EX + "TEC : " + line.decode().strip())

    elif msg.topic == VALVE_TOPIC:
        msg.payload = int(msg.payload)
        serial_buffer = f"M0 outdoor_air_valve D{msg.payload}\r" 

        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

        line = ser_octo.readline()
        print(Fore.CYAN + "OCTO: " + line.decode().strip())

    elif msg.topic == ENABLE_PI:
        if msg.payload.decode('utf-8') == "False":

            #turn eta off
            ser_octo.write(b"M0 eta_fan D0\r")
            time.sleep(0.1)

            #turn oda off
            ser_octo.write(b"M0 oda_fan D0\r")
            time.sleep(0.1)

            #close valve
            ser_octo.write(b"M0 outdoor_air_valve D0\r")
            time.sleep(0.1)

            #turn peltier off
            ser_tec.write(b"set 1 0.0\r")
            time.sleep(0.1)
            ser_tec.write(b"set 2 0\r")
            time.sleep(0.1)

            print(Back.RED + Fore.WHITE + "PI forwarder shutting down..." + Style.RESET_ALL)
            quit()

    print(Style.RESET_ALL)


client = mqtt.Client()
client.username_pw_set(secrets.USERNAME, secrets.PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, 1883, 60)
client.loop_forever()
