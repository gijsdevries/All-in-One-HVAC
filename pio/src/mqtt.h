#include <WiFi.h>
#include <MQTT.h>

extern WiFiClient net;
extern MQTTClient client;

void connect_wifi(const char* ssid, const char* password, const char* topic);
