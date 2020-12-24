#include <I2Cdev.h>
#include "MPU6050.h"
#include <Wire.h>
#include "mpu.h"

MPU6050 mpu;


void mpu_setup(){

 mpu.initialize();
 mpu.setSleepEnabled(false);
 mpu.setFullScaleAccelRange(0); // 0=> +-250deg/s ; 1=> +-500deg/s ; 2=> +-1000deg/s ; 3=> 2000deg/s
 mpu.setFullScaleGyroRange(0);  // 0=> +-2g ; 1=> +-4g ; 2=> +-8g ; 3=> +-16g

 mpu_ready = mpu.testConnection();
}

void mpu_as_raw(){
        ax = (int16_t)mpu.getAccelerationX();
        ay = (int16_t)mpu.getAccelerationY();
        az = (int16_t)mpu.getAccelerationZ();
}

void mpu_as_ms(){
  
        axp = mpu.getAccelerationX();
        ayp = mpu.getAccelerationY();
        azp = mpu.getAccelerationZ();
        
        axp = (axp/ACCEL_SENSITIVITY)*GRAVITY;
        ayp = (ayp/ACCEL_SENSITIVITY)*GRAVITY;
        azp = (azp/ACCEL_SENSITIVITY)*GRAVITY;
          
  }
