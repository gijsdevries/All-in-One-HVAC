#include <mqtt.h>

void connect_wifi(const char* ssid, const char* password)
{
    WiFi.begin(ssid, password);
    Serial.print("checking wifi...");

    while (WiFi.status() != WL_CONNECTED) {
	Serial.print(".");
	delay(1000);
    }

    Serial.println("\nconnected!");
    return;
}

void hello_world()
{
    Serial.println("hello world!");
}
