#include "sensor.h"

QueueHandle_t dataQueue = NULL; //  Initialize dataQueue used for passing measurements to data uploader

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
