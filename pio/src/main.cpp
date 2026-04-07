#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
//#include <MQTT.h>

#include <mqtt.h>

#define BLINK_GPIO (gpio_num_t)CONFIG_BLINK_GPIO

const char ssid[] = "Energielab";
const char pass[] = "Energie0238";

WiFiClient net;
//MQTTClient client;

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, pass);
}

void loop() {
  Serial.print("checking wifi...");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("\nconnected!");
  delay(1000);
}
