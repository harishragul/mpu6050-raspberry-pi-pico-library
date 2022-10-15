#angle.py is a sample code to measure tilt angle
# Author Harish Ragul

from imu import MPU6050
from machine import Pin, I2C
from Kalman import KalmanAngle
import time
import math

led = Pin(25, Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)


kalmanX = KalmanAngle()
kalmanY = KalmanAngle()

RestrictPitch = True
radToDeg = 57.2957786
kalAngleX = 0
kalAngleY = 0

#Read Accelerometer raw value
accX = imu.accel.x
accY = imu.accel.y
accZ = imu.accel.z

if (RestrictPitch):
    roll = math.atan2(accY,accZ) * radToDeg
    pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
else:
    roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
    pitch = math.atan2(-accX,accZ) * radToDeg

kalmanX.setAngle(roll)
kalmanY.setAngle(pitch)
gyroXAngle = roll;
gyroYAngle = pitch;
compAngleX = roll;
compAngleY = pitch;

timer = time.time()

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


    dt = time.time() - timer
    timer = time.time()

    if (RestrictPitch):
        roll = math.atan2(accY,accZ) * radToDeg
        pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
    else:
        roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
        pitch = math.atan2(-accX,accZ) * radToDeg

    gyroXRate = gyroX/131
    gyroYRate = gyroY/131

    if (RestrictPitch):
        if((roll < -90 and kalAngleX >90) or (roll > 90 and kalAngleX < -90)):
            kalmanX.setAngle(roll)
            complAngleX = roll
            kalAngleX   = roll
            gyroXAngle  = roll
        else:
            kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

        if(abs(kalAngleX)>90  or True):
            gyroYRate  = -gyroYRate
            kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
    else:

        if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
            kalmanY.setAngle(pitch)
            complAngleY = pitch
            kalAngleY   = pitch
            gyroYAngle  = pitch
        else:
            kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)

        if(abs(kalAngleY)>90):
            gyroXRate  = -gyroXRate
            kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

	#angle = (rate of change of angle) * change in time
    gyroXAngle = gyroXRate * dt
    gyroYAngle = gyroYAngle * dt

	#compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
    compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
    compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

    if ((gyroXAngle < -180) or (gyroXAngle > 180)):
        gyroXAngle = kalAngleX
    if ((gyroYAngle < -180) or (gyroYAngle > 180)):
        gyroYAngle = kalAngleY

    print("Angle X: " + str(kalAngleX)+"   " +"Angle Y: " + str(kalAngleY))
    #print(str(roll)+"  "+str(gyroXAngle)+"  "+str(compAngleX)+"  "+str(kalAngleX)+"  "+str(pitch)+"  "+str(gyroYAngle)+"  "+str(compAngleY)+"  "+str(kalAngleY))

    time.sleep(0.004)
