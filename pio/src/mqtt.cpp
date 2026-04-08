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

    Serial.println("\nconnected to wifi");

    client.begin("public.cloud.shiftr.io", net);

    while (!client.connect("arduino", "public", "public"))
    {
	Serial.print(".");
	delay(1000);
    }

    Serial.println("\nconnected to topic");

    client.subscribe(topic);
    return;
}
