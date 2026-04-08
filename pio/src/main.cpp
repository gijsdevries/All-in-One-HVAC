#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
#include <MQTT.h>

#include <mqtt.h>

void setup() {
    const char ssid[] = "Energielab";
    const char pass[] = "Energie0238";
    const char topic[] = "/hello";

    Serial.begin(115200);
    connect_wifi(ssid, pass, topic);
}

void loop() {
    delay(1000);
}
