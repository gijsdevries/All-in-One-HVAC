#include <mqtt.h>
#include <secrets.h>

WiFiClient net;
MQTTClient client;

//connect to wifi
void connect_wifi()
{
    WiFi.begin(secret_ssid, secret_password);
    Serial.print("checking wifi...");

    while (WiFi.status() != WL_CONNECTED)
    {
	Serial.print(".");
	delay(1000);
    }

    Serial.println("\nconnected to wifi. connecting to url now");
    return;
}

//connect to mqtt broker
void connect_mqtt()
{
    client.begin("192.168.1.116", net);

    while (!client.connect("sensordev", secret_username_broker, secret_password_broker))
    {
      Serial.print(".");
      delay(1000);
    }

    Serial.println("\nconnected to mqtt broker");
    return;
}
