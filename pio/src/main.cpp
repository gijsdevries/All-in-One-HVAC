#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
#include <MQTT.h>
#include <Wire.h>
#include <mqtt.h>

#define SENSOR_ADDR 0x44    // SHT40 I2C address
#define QUEUE_SIZE 5    // Size of data queue
#define MEASUREMENT_INTERVAL 1000

QueueHandle_t dataQueue = NULL; //  Initialize dataQueue used for passing measurements to data uploader

struct data_struct //  Struct for measurements
{
    float temp;
    float hum;
};

/*
   SHT40Task
   This function is used as a freeRTOS task, it measures temperature and relative 
   humidity and adds these to the dataQueue
   */

void SHT40Task(void *parameter)
{
    Wire.begin();

    dataQueue = xQueueCreate(QUEUE_SIZE, sizeof(data_struct));
    if (dataQueue == NULL)
    {
	Serial.println("Failed to create dataQueue.");
	vTaskDelete(NULL);
    }    

    data_struct data;

    while(true)
    {
	Wire.beginTransmission(SENSOR_ADDR);    //  Initializes I2C communication
	Wire.write(0xFD);   //  Sends command for single high precision T & RH measurement

	int error = Wire.endTransmission();
	if (error != 0)
	{
	    Serial.println("Command sending failed！");
	    vTaskDelay(100 / portTICK_PERIOD_MS);             
	    continue;
	}

	vTaskDelay(60 / portTICK_PERIOD_MS);             

	Wire.requestFrom(SENSOR_ADDR, 6);
	if (Wire.available() == 6)
	{
	    // Read temperature data
	    uint16_t temp_raw = (Wire.read() << 8) | Wire.read();
	    Wire.read();         

	    // Read humidity data
	    uint16_t hum_raw = (Wire.read() << 8) | Wire.read();
	    Wire.read();          

	    data.temp = -45.0 + 175.0 * (temp_raw / 65535.0);
	    data.hum = -6 + 125 * (hum_raw / 65535.0);
	    if (data.hum > 100.0) data.hum = 100.0;
	    else if (data.hum < 0.0) data.hum = 0.0;

	    xQueueSend(dataQueue, &data, portMAX_DELAY);

	    vTaskDelay(MEASUREMENT_INTERVAL / portTICK_PERIOD_MS);
	} 
	else
	{
	    Serial.println("Data read failed！");
	    continue;
	}
    }
}

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
	    snprintf(buffer, sizeof(buffer), "%.2f", data.temp);
	    client.publish(topic_temp, buffer);

	    snprintf(buffer, sizeof(buffer), "%.2f", data.hum);
	    client.publish(topic_hum, buffer);

	    printf("Send over mqtt: Temp: %.2f | Hum: %.2f\n", data.temp, data.hum);
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
	vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void setup() {
    Serial.begin(115200);

    xTaskCreate(SHT40Task, "SHT40Task", 8192, NULL, 5, NULL);
    xTaskCreate(&mqtt_connection, "mqtt_connection", 8192, NULL, 5, NULL);
}

void loop() 
{
    vTaskDelay(pdMS_TO_TICKS(1000));
}
