#include <mqtt.h>

WiFiClient net;
MQTTClient client;

void connect_wifi(const char* ssid, const char* password)
{
    WiFi.begin(ssid, password);
    Serial.print("checking wifi...");

    while (WiFi.status() != WL_CONNECTED)
    {
	Serial.print(".");
	delay(1000);
    }

    Serial.println("\nconnected to wifi. connecting to url now");
    return;
}

void connect_mqtt()
{
    client.begin("192.168.1.116", net);

    while (!client.connect("sensordev", "pi_mqtt", "M0squ!tt0"))
    {
      Serial.print(".");
      delay(1000);
    }

    Serial.println("\nconnected to mqtt broker");
    return;
}
