#include <WiFi.h>
#include <MQTT.h>

extern WiFiClient net;
extern MQTTClient client;

void connect_mqtt();
void connect_wifi();
