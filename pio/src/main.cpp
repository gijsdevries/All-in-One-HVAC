#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
#include <MQTT.h>

#include <mqtt.h>

const char topic[] = "/hello";

void mqtt_post(void *pvParameter)
{
    while(1)
    {
      client.publish(topic, "world");
      Serial.println("send string world to client");
      vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

void mqtt_connection(void *pvParameter)
{
    const char ssid[] = "Energielab";
    const char pass[] = "Energie0238";

    connect_wifi(ssid, pass);
    connect_mqtt();
    client.subscribe(topic);

    xTaskCreate(&mqtt_post, "mqtt_post", 8192, NULL, 5, NULL);

    while(1)
    {
      client.loop();
      vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void setup() {
    Serial.begin(115200);
    xTaskCreate(&mqtt_connection, "mqtt_connection", 8192, NULL, 5, NULL);
}

void loop() {
    delay(1000);
}
