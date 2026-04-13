#include "Wire.h"
#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <Arduino.h>

#define SENSOR_ADDR 0x44    // SHT40 I2C address
#define QUEUE_SIZE 2    // Size of data queue
#define MEASUREMENT_INTERVAL 1000

extern QueueHandle_t dataQueue; //  Initialize dataQueue used for passing measurements to data uploader

struct data_struct //  Struct for measurements
{
    float temp;
    float hum;
};

void SHT40Task(void *parameter);
