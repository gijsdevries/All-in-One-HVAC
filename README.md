***All-in-One-HVAC***

**pio**
In deze folder staat een project voor een sensor kit die op een esp32 gedraaid kan worden. Uiteindelijk hebben wij er voor gekozen om testo sensoren te gebruiken. Er is weinig nuttigs in deze map de vinden.

**pythonFiles**
In deze folder staan alle python bestand die wij gebruiken.
[pythonFiles/MQTT_starter.py](https://github.com/gijsdevries/All-in-One-HVAC/blob/main/pythonFiles/MQTT_starter.py) als je dit script runt kan je ervoor zorgen dat de pi gaat luisteren naar MQTT data die ontvangen wordt van Home Assistent
[pythonFiles/mqtt_reciever.py](https://github.com/gijsdevries/All-in-One-HVAC/blob/main/pythonFiles/mqtt_receiver.py) dit is het script wat de MQTT data parsed en vervolgens doorstuurt naar de HOOM unit. In dit bestand moet je zelf bepaalde waardes aan variabele toekennen. Zie hiervoor het bestand zelf.

**testo_power**
In deze folder staat het kicad bestand voor de PCB die wij hebben gemaakt. De schematic is in KiCad v10.0 gemaakt. De schematic is op dit [forum](https://electronics.stackexchange.com/questions/418090/advice-for-this-p-channel-mosfet-power-source-selector) gebasseerd
