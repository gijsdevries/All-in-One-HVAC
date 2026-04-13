#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>
#include <MQTT.h>

#include <Wire.h>

struct data_struct {    //  Struct for measurements
    float temp;
    float hum;
};

#define SENSOR_ADDR 0x44    // SHT40 I2C address
#define QUEUE_SIZE 5    // Size of data queue
#define MEASUREMENT_INTERVAL 1000

// #define BLINK_GPIO (gpio_num_t)CONFIG_BLINK_GPIO

QueueHandle_t dataQueue = NULL; //  Initialize dataQueue used for passing measurements to data uploader

/*
    SHT40Task
    This function is used as a freeRTOS task, it measures temperature and relative 
    humidity and adds these to the dataQueue
*/
void SHT40Task(void *parameter)
{
    while(true)
    {
        Wire.beginTransmission(SENSOR_ADDR);    //  Initializes I2C communication
        Wire.write(0xFD);   //  Sends command for single high precision T & RH measurement
#include <mqtt.h>

const char topic[] = "/hello";

//post data to certain topic
//TODO recieve data from queue that has sensor struct inside
void mqtt_post(void *pvParameter)
{
    while(1)
    {
      client.publish(topic, "world");
      Serial.println("send string world to client");
      vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

//start wifi and mqtt connection and keep it alive
void mqtt_connection(void *pvParameter)
{
    const char ssid[] = "Energielab";
    const char pass[] = "Energie0238";

    connect_wifi(ssid, pass);
    connect_mqtt();
    client.subscribe(topic);

    xTaskCreate(&mqtt_post, "mqtt_post", 8192, NULL, 5, NULL);

        int error = Wire.endTransmission();
        if (error != 0) {
            Serial.println("Command sending failed！");
            continue;
        }

        vTaskDelay(60 / portTICK_PERIOD_MS);             

        
        Wire.requestFrom(SENSOR_ADDR, 6);
        if (Wire.available() == 6) {
            // Read temperature data
            uint16_t temp_raw = (Wire.read() << 8) | Wire.read();
            Wire.read();         
            
            // Read humidity data
            uint16_t hum_raw = (Wire.read() << 8) | Wire.read();
            Wire.read();          
            
            data_struct data;

            data.temp = -45.0 + 175.0 * (temp_raw / 65535.0);
            data.hum = -6 + 125 * (hum_raw / 65535.0);
            if (data.hum > 100.0) data.hum = 100.0;
            else if (data.hum < 0.0) data.hum = 0.0;

            xQueueSend(dataQueue, &data, portMAX_DELAY);
            
            vTaskDelay(MEASUREMENT_INTERVAL / portTICK_PERIOD_MS);
        } 
        else {
            Serial.println("Data read failed！");
            continue;
        }
    }
}

void PrintTask(void *parameter)
{
    while(true)
    {
        data_struct data;
        if (xQueueReceive(dataQueue, &data, portMAX_DELAY))
        {
            Serial.printf("From queue: Temp: %.2f | Hum: %.2f\n", data.temp, data.hum);
        }
      client.loop(); //this function should be called frequently to keep connection with broker alive
      vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void setup() {
    Serial.begin(115200);

    Wire.begin();

    dataQueue = xQueueCreate(QUEUE_SIZE, sizeof(data_struct));
    if (dataQueue == NULL)
    {
        Serial.println("Failed to create dataQueue.");
        while(true);
    }    

    xTaskCreatePinnedToCore(
        SHT40Task,
        "SHT40Task",
        3000,
        NULL,
        1,
        NULL,
        1
    );

    xTaskCreatePinnedToCore(
        PrintTask,
        "PrintTask",
        3000,
        NULL,
        1,
        NULL,
        1
    );
}

void loop() 
{
    vTaskDelay(pdMS_TO_TICKS(1000));
    xTaskCreate(&mqtt_connection, "mqtt_connection", 8192, NULL, 5, NULL);
}

void loop() {
    delay(1000);
}
