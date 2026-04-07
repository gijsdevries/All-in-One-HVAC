#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include "sdkconfig.h"
#include <Arduino.h>

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

void setup() {
    Serial.begin(115200);
    xTaskCreate(&blink_task, "blink_task", configMINIMAL_STACK_SIZE, NULL, 5, NULL);
    pinMode(BLINK_GPIO, OUTPUT);
}

void loop() {
    Serial.println("Hello!");
    delay(1000);
}
