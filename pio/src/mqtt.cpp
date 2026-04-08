#include <mqtt.h>

WiFiClient net;
MQTTClient client;

void connect_wifi(const char* ssid, const char* password, const char* topic)
{
    WiFi.begin(ssid, password);
    Serial.print("checking wifi...");

    while (WiFi.status() != WL_CONNECTED)
    {
	Serial.print(".");
	delay(1000);
    }

    Serial.println("\nconnected to wifi. connecting to url now");

    client.begin("192.168.1.116", net);

    while (!client.connect("sensordev", "pi_mqtt", "M0squ!tt0"))
    {
      Serial.print(".");
      delay(1000);
    }

    Serial.println("\nconnected to topic");

    client.subscribe(topic);
    return;
}
