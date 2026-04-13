#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
#include <MQTT.h>
#include <Wire.h>

#include <mqtt.h>
#include <sensor.h>

#define BLINK_GPIO (gpio_num_t)2

// task that sends mqtt data to home assistent
void mqtt_post(void *parameter)
{
    //topics
    const char topic_temp[] = "/sensor_kit/1/temp";
    const char topic_hum[] = "/sensor_kit/1/hum";

    client.subscribe(topic_temp);
    client.subscribe(topic_hum);

    data_struct data; //recieve the sensor data
    char buffer[6]; //used for snprintf

    while(true)
    {
	if (xQueueReceive(dataQueue, &data, portMAX_DELAY))
	{
	    //convert the float value to a string so it can be send over mqtt
	    snprintf(buffer, sizeof(buffer), "%.2f", data.temp);
	    client.publish(topic_temp, buffer);

	    snprintf(buffer, sizeof(buffer), "%.2f", data.hum);
	    client.publish(topic_hum, buffer);

	    printf("Send over mqtt: Temp: %.2f | Hum: %.2f\n", data.temp, data.hum);

	    gpio_set_level(BLINK_GPIO, 1);
	    vTaskDelay(100 / portTICK_PERIOD_MS);
	    digitalWrite(BLINK_GPIO, 0);
	}
    }
}

//start wifi and mqtt connection and keep it alive
void mqtt_connection(void *pvParameter)
{
    connect_wifi();
    connect_mqtt();

    xTaskCreate(mqtt_post, "mqtt_post", 8192, NULL, 5, NULL);

    while (1)
    {
	client.loop(); //this function should be called frequently to keep connection with broker alive
	vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void setup() {
    Serial.begin(115200);

    gpio_pad_select_gpio(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);

    xTaskCreate(SHT40Task, "SHT40Task", 8192, NULL, 5, NULL);
    xTaskCreate(&mqtt_connection, "mqtt_connection", 8192, NULL, 5, NULL);
}

void loop() 
{
    vTaskDelay(pdMS_TO_TICKS(1000));
}
