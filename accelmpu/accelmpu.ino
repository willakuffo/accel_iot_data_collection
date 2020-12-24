#include "ultrasonic_3d.h"
#include "mpu.h"

#include <I2Cdev.h>
#include "MPU6050.h"
#include <Wire.h>

//uncomment to read mpu as m/s
//comment to read as raw, sensitivity -> 2g
//#define MPU_AS_RAW



void setup() {
 // put your setup code here, to run once:
 Serial.begin(38400);
 mpu_setup();
 ultrasonic_3d_setup();
}

void loop() {
  // put your main code here, to run repeatedly:


SonarSensor(XTRIG, XECHO);
Serial.print("X: ");
Serial.print(distance);

SonarSensor(YTRIG, YECHO);
Serial.print("  Y: ");
Serial.print(distance);

SonarSensor(ZTRIG, ZECHO);
Serial.print("  Z: ");
Serial.print(distance);

#ifndef MPU_AS_RAW
mpu_as_ms();
Serial.print("  a/g:\t");
Serial.print(axp); Serial.print("\t"); 
Serial.print(ayp); Serial.print("\t");
Serial.print(azp); Serial.println("\t");
#endif

#ifdef MPU_AS_RAW
mpu_as_raw();
Serial.print("  a/g:\t");
Serial.print(ax); Serial.print("\t"); 
Serial.print(ay); Serial.print("\t");
Serial.print(az); Serial.println("\t");
#endif

}
