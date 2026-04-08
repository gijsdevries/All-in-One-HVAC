#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
//#include <MQTT.h>

#include <mqtt.h>

const char ssid[] = "Energielab";
const char pass[] = "Energie0238";

void setup() {
    Serial.begin(115200);
    hello_world();
    //connect_wifi(ssid, pass);
}

void loop() {
  delay(1000);
}
