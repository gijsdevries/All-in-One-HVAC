## Installeren OS raspberry pi

Voor de aansturing gebruiken wij een raspberry pi 3. We hebben een SD kaart geflasht met Raspberry Pi Imager met Raspberry PI OS. Zorg ervoor dat je tijdens het installeren ook wifi van het energielab erop zet.

## Installeren python omgeving op de pi
  
In deze map staan de python bestanden die op de raspberry pi draaien. De raspberry pi ontvangt de MQTT data van Home Assistent en stuurt het door met UART naar de HOOM unit.
  
Voor het instellen van de python omgeving gebruiken wij een virtual environment (venv) in python 3.13.5. Om de python versie te controleren kan je `python3 --version` runnen.
Voor het maken van de virtual environment run je het volgende commando

`python3 -m venv /path/to/new/virtual/environment`

Je kan de environment activeren met het commando `source venv/bin/activate` (als de map van de environment venv heet)
Deactivaten kan met `deactivate`

Om het python script te kunnen draaien moeten er een paar dependencies aan de venv toegevoegd worden. Activeer de venv met het bovenstaande commando en installeer de dependencies:

`pip3 install -r requirements.txt`
  
Je zou nu alle python files moeten kunnen runnen met `python3 <naam python bestand>`

Om de pi MQTT data te laten ontvangen op het moment dat deze aanstaat kan je de volgende commandos toevoegen aan het bestand ~/.bashrc

```bash
# Check even of de directiories overeenkomen.

source /home/hvacpi/Documents/venv/bin/activate                                 # Activate the venv
python3 /home/hvacpi/Documents/All-in-One-HVAC/pythonFiles/MQTT_starter.py      # Start the python script
```

