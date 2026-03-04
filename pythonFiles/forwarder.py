#chatgpt code 😉

import serial
import threading
import sys

BAUDRATE = 115200 

def read_from_serial(ser):
    """Continuously read from serial and print to terminal."""
    while True:
        try:
            line = ser.readline()
            if line:
                print("\nDEVICE:", line.decode(errors="ignore").strip())
                print("YOU: ", end="", flush=True)
        except serial.SerialException:
            break

def main():
    # Check if port argument was provided
    if len(sys.argv) < 2:
        print("Usage: python3 forwarder.py <serial_port> [baudrate]")
        print("Example: python3 forwarder.py /dev/ttyUSB0")
        print("Example (Windows): python3 forwarder.py COM3")
        sys.exit(1)

    port = sys.argv[1]

    # Optional baudrate argument
    baudrate = int(sys.argv[2]) if len(sys.argv) >= 3 else BAUDRATE

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud.")
    except Exception as e:
        print("Failed to open serial port:", e)
        sys.exit(1)

    # Start background reader thread
    thread = threading.Thread(target=read_from_serial, args=(ser,), daemon=True)
    thread.start()

    print("Type messages and press Enter to send. Ctrl+C to exit.\n")

    try:
        while True:
            msg = input("YOU: ")
            ser.write((msg + "\n").encode())
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
