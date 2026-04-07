#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>

#include <Wire.h>

struct CTH832X_data {
    float celcius;
    float relative_humidity;
};

#define SENSOR_ADDR 0x44  

#define BLINK_GPIO (gpio_num_t)CONFIG_BLINK_GPIO

void blink_task(void *pvParameter)
{
    gpio_pad_select_gpio(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);

    while(1)
    {
	/* Blink off (output low) */
	gpio_set_level(BLINK_GPIO, 0);
	vTaskDelay(1000 / portTICK_PERIOD_MS);
	/* Blink on (output high) */
	digitalWrite(BLINK_GPIO, !digitalRead(BLINK_GPIO));
	vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

CTH832X_data get_temp(void)
{
    Wire.beginTransmission(SENSOR_ADDR);
    Wire.write(0x24);       
    Wire.write(0x00);       
    int error = Wire.endTransmission();
    
    if (error != 0) {
        Serial.println("Command sending failed！");
        CTH832X_data temp_hum;
        temp_hum.celcius = 0;
        temp_hum.relative_humidity = 0;
        return temp_hum;
    }

    delay(60);              

    
    Wire.requestFrom(SENSOR_ADDR, 6);
    if (Wire.available() == 6) {
        // Read temperature data
        uint16_t temp_raw = (Wire.read() << 8) | Wire.read();
        Wire.read();         
        
        // Read humidity data
        uint16_t humi_raw = (Wire.read() << 8) | Wire.read();
        Wire.read();          

        CTH832X_data temp_hum;
        temp_hum.celcius = -45.0 + 175.0 * (temp_raw / 65535.0);
        temp_hum.relative_humidity = 100.0 * (humi_raw / 65535.0);


        Serial.print("temperature: ");
        Serial.print(temp_hum.celcius, 2);
        Serial.print("°C \thumidity: ");
        Serial.print(temp_hum.relative_humidity, 2);
        Serial.println(" %RH");

        return temp_hum;
    } 
    else {
        Serial.println("Data read failed！");
        CTH832X_data temp_hum;
        temp_hum.celcius = 0;
        temp_hum.relative_humidity = 0;
        return temp_hum;
    }
}

void setup() {
    Serial.begin(115200);

    Wire.begin();

    xTaskCreate(&blink_task, "blink_task", configMINIMAL_STACK_SIZE, NULL, 5, NULL);
    pinMode(BLINK_GPIO, OUTPUT);
}

void loop() {
    CTH832X_data test = get_temp();    

    delay(500);   
}
