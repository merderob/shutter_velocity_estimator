#include <Arduino.h>
#include "imu.h"

Imu imu;


void setup() 
{
    Serial.begin(9600);
    imu.init();
}

void loop() 
{
    imu.execute();
    imu.log();
    delay(50);
}