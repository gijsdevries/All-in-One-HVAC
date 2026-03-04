import serial
import time

# Configuratie van de seriële poort
port_name = '/dev/ttyACM0' 
baud_rate = 115200

try:
    # Open de poort met een timeout van 1 seconde
    with serial.Serial(port_name, baud_rate, timeout=1) as ser:
        while 1:
            ser.write(b"M0 oda_fan D0\r")
            print("send command: M0 oda_fan D0")
            time.sleep(5)

            ser.write(b"M0 oda_fan D50\r")
            print("send command: M0 oda_fan D50")
            time.sleep(5)

            ser.write(b"M0 oda_fan D100\r")
            print("send command: M0 oda_fan D100")
            time.sleep(5)

            ser.write(b"M0 oda_fan D50\r")
            print("send command: M0 oda_fan D50")
            time.sleep(5)

except serial.SerialException as e:
    print(f"Fout bij openen poort: {e}")
