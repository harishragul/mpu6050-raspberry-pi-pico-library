#sample.py is a sample code to find the raw values
# Author Harish Ragul

from imu import MPU6050
import time
from machine import Pin, I2C

led = Pin(25, Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

while True:
    led.value(1)

    #Read Accelerometer raw value
    accX = imu.accel.x
    accY = imu.accel.y
    accZ = imu.accel.z

    #Read Gyroscope raw value
    gyroX = imu.gyro.x
    gyroY = imu.gyro.y
    gyroZ = imu.gyro.z
