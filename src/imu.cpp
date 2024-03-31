// Copyright © 2024 Robert Takacs
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
// files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy,
// modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
// is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
// WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
// COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
// ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include "imu.h"
#include <Arduino.h>

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

void Imu::init()
{
    Serial.println("Initializing IMU");
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    sensor_.initialize();

    // verify connection
    initialized_ = sensor_.testConnection();
    Serial.println(initialized_ ? "IMU initialization successful" : "IMU initialization failed");
    Serial.println("Time,Ax,Ay,Az");
}

void Imu::execute()
{
    // read raw accel/gyro measurements from device
    sensor_.getMotion6(&ax_, &ay_, &az_, &gx_, &gy_, &gz_);
    execution_time_ = static_cast<double>(millis()) / 1000.0;

}

void Imu::log()
{
    Serial.print(execution_time_);
    Serial.print(",");
    Serial.print(ax_/accelerometer_sensitivity_); Serial.print(",");
    Serial.print(ay_/accelerometer_sensitivity_); Serial.print(",");
    Serial.println(az_/accelerometer_sensitivity_);
}
