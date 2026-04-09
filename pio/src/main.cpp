#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
#include <MQTT.h>

#include <mqtt.h>

const char topic[] = "/hello";

void setup() {
    const char ssid[] = "Energielab";
    const char pass[] = "Energie0238";

    Serial.begin(115200);
    connect_wifi(ssid, pass);
    connect_mqtt();
    client.subscribe(topic);
}

void loop() {
    client.loop();

    client.publish(topic, "world");
    Serial.println("send string world to client");
    delay(1000);
}
