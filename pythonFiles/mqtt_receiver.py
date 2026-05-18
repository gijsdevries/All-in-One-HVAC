from colorama import Fore, Back, Style
import serial
import paho.mqtt.client as mqtt
import os
import time

#user file
import secrets

highPowerOn = False # Variable that checks if hp is on. by default is should be off
highPowerAmp = 6.0 # Amp range to switch from lp to hp or vice versa

#TOPICS
ETA_TOPIC = "hoom/control/eta"
ODA_TOPIC = "hoom/control/oda"
TEC_TOPIC = "hoom/control/tec"
PELTIER_TOPIC = "hoom/control/peltier"
ENABLE_PI = "hoom/control/enable_pi"
VALVE_TOPIC = "hoom/control/valve"
CALIBRATE_VALVE_TOPIC = "hoom/control/calibrate_valve"
WATER_PUMP_TOPIC = "hoom/control/water_pump"

dirPathPi = "/home/hvacpi"

# COM_PORTS

# Configure these variables yourself. run the following command to see available COM ports
# ls -l /dev/serial/by-id/

if os.path.isdir(dirPathPi):
    SERIAL_PORT_OCTO = "/dev/ttyACM0" 
    SERIAL_PORT_TEC = "/dev/ttyUSB0"
else:
    SERIAL_PORT_OCTO = "/dev/ttyS4" 
    SERIAL_PORT_TEC = "/dev/ttyS4"

BAUD_RATE_OCTO = 115200 
BAUD_RATE_TEC = 9600 

#SETTINGS
MQTT_HOST = "192.168.1.116" # IP of your HA/Mosquitto Broker

POWER_CIRCUT_SWITCH_DELAY = 2 # Delay between commands when switching power circuits

# Initialize Serial
try:
    ser_octo = serial.Serial(SERIAL_PORT_OCTO, BAUD_RATE_OCTO, timeout=1)
    ser_tec = serial.Serial(SERIAL_PORT_TEC, BAUD_RATE_TEC, timeout=1)
except Exception as e:
    print(f"Serial Error: {e}")
    exit()

def on_connect(eta_client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {rc}")
    
    #TODO set topics in a struct and subscribe to all topics in the struct
    topics = [
        (ODA_TOPIC, 0),
        (ETA_TOPIC, 0),
        (TEC_TOPIC, 0),
        (PELTIER_TOPIC, 0),
        (VALVE_TOPIC, 0),
        (CALIBRATE_VALVE_TOPIC, 0),
        (WATER_PUMP_TOPIC, 0),
        (ENABLE_PI, 0),
    ]
    eta_client.subscribe(topics)

#TODO this code is very repetitive. write a function to reduce lines
def on_message(eta_client, userdata, msg):
    global highPowerOn

    if msg.topic == ETA_TOPIC:
        msg.payload = int(msg.payload)
        serial_buffer = f"M0 eta_fan D{msg.payload}\r" 
        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

    elif msg.topic == ODA_TOPIC:
        msg.payload = int(msg.payload)
        serial_buffer = f"M0 oda_fan D{msg.payload}\r" 
        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

    elif msg.topic == TEC_TOPIC:

        msg.payload = msg.payload.decode('utf-8')

        if msg.payload == 'False':
            serial_buffer = "set 2 0\r" 
        else:
            serial_buffer = "set 2 1\r" 

        ser_tec.write(serial_buffer.encode('utf-8'))
        print(Fore.GREEN + "SENT TEC: " + serial_buffer)

    elif msg.topic == PELTIER_TOPIC:
        msg.payload = float(msg.payload)

        # Check if the setpoint exceeds the amperage ranges
        if msg.payload > highPowerAmp or msg.payload < -highPowerAmp:
            # If hp is off
            if highPowerOn == False:
                highPowerOn = True

                # Turn hp on
                serial_buffer = f"set 2 0\r" 
                ser_tec.write(serial_buffer.encode('utf-8'))
                print(Fore.GREEN + "SENT TEC: " + serial_buffer)
                time.sleep(POWER_CIRCUT_SWITCH_DELAY)

                serial_buffer = f"relay_hp\r" 
                ser_tec.write(serial_buffer.encode('utf-8'))
                print(Fore.GREEN + "SENT TEC: " + serial_buffer)
                time.sleep(POWER_CIRCUT_SWITCH_DELAY)

                serial_buffer = f"set 2 1\r" 
                ser_tec.write(serial_buffer.encode('utf-8'))
                print(Fore.GREEN + "SENT TEC: " + serial_buffer)
                time.sleep(POWER_CIRCUT_SWITCH_DELAY)

        else:
            # Check if hp is on
            if highPowerOn == True:
                highPowerOn = False

                # Turn hp off
                serial_buffer = f"set 2 0\r" 
                ser_tec.write(serial_buffer.encode('utf-8'))
                print(Fore.GREEN + "SENT TEC: " + serial_buffer)
                time.sleep(POWER_CIRCUT_SWITCH_DELAY)

                serial_buffer = f"relay_lp\r" 
                ser_tec.write(serial_buffer.encode('utf-8'))
                print(Fore.GREEN + "SENT TEC: " + serial_buffer)
                time.sleep(POWER_CIRCUT_SWITCH_DELAY)

                serial_buffer = f"set 2 1\r" 
                ser_tec.write(serial_buffer.encode('utf-8'))
                print(Fore.GREEN + "SENT TEC: " + serial_buffer)
                time.sleep(POWER_CIRCUT_SWITCH_DELAY)


        serial_buffer = f"set 1 {msg.payload}\r" 
        ser_tec.write(serial_buffer.encode('utf-8'))
        print(Fore.GREEN + "SENT TEC: " + serial_buffer)

    elif msg.topic == VALVE_TOPIC:
        msg.payload = int(msg.payload)
        serial_buffer = f"M0 outdoor_air_valve D{msg.payload}\r" 

        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

    elif msg.topic == WATER_PUMP_TOPIC:
        payload = msg.payload.decode("utf-8").strip()
        data = [part.strip() for part in payload.split(";")]
        serial_buffer = f"M0 water_pump D{int(data[0])} S{float(data[1])}\r"

        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

    elif msg.topic == CALIBRATE_VALVE_TOPIC:
        serial_buffer = "M0 home_valves\r"

        ser_octo.write(serial_buffer.encode('utf-8'))
        print(Fore.BLUE + "SENT OCTO: " + serial_buffer)

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
