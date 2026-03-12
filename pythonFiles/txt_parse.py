#TODO add serial port recognizer
import subprocess
import serial
import time
import subprocess

file_path = 'test.txt'
#file_path = '/home/hvacpi/Documents/sensoren_klimaatkamer/pythonFiles/test.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()

try:
    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
        for line in lines:
            command, delay = line.split(", ")

            ser.write(command.encode())
            ser.write(b"\r")
            print("--- send command:" + command + " ---")

            line = ser.readline()
            print(line.decode().strip() + "\n")

            time.sleep(int(delay))

except serial.SerialException as e:
    print(f"Fout: {e}")
