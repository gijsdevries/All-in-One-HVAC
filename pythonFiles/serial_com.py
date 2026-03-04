import serial
import time

# Configuratie van de seriële poort
port_name = '/dev/ttyACM0' 
baud_rate = 115200

try:
    # Open de poort met een timeout van 1 seconde
    with serial.Serial(port_name, baud_rate, timeout=1) as ser:
        print(f"Verbonden met {ser.name}")
        
        # Geef de hardware even tijd om te initialiseren (vooral bij Arduino)
        time.sleep(2)

        # 1. Data VERZENDEN
        # De data moet als bytes (b'...') verzonden worden
        ser.write(b"HELLO\r")
        print("Commando verzonden.")

        # 2. Data LEZEN
        # Wacht tot er data in de buffer staat
        if ser.in_waiting > 0:
            # Lees een volledige regel tot de newline (\n)
            response = ser.readline().decode('utf-8').strip()
            print(f"Antwoord ontvangen: {response}")
        else:
            print("Geen antwoord ontvangen binnen de timeout.")

except serial.SerialException as e:
    print(f"Fout bij openen poort: {e}")
