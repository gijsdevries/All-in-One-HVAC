#TODO add serial port recognizer
import subprocess
import serial
import time
import subprocess
import sys

if len(sys.argv) < 2:
    print(f"Usage: python3 {sys.argv[0]} <serial_port>")
    sys.exit(1)

file_path = sys.argv[1]

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
