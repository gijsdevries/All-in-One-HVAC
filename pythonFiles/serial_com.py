import serial
import time

try:
    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:

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
    print(f"Fout: {e}")
