#ifndef MPU_ADDED
#define MPU_ADDED

#define GYRO_SENSITIVITY 131
#define ACCEL_SENSITIVITY 16384
#define GRAVITY 9.81


int16_t ax, ay, az, gx, gy, gz; //collect raw values as global
float axp, ayp, azp, gxp, gyp, gzp; //collect processed m/s values as global

bool mpu_ready  = false;

void mpu_as_raw();
void mpu_as_ms();
void mpu_setup();

#endif
