# mpu6050-raspberry-pi-pico-library
IMU Library for MPU 6050 with Raspberry Pi Pico - Micropython

## Credits
### Peter Hinch, Sebastian Plamauer
- imu.py, 
- vector3d.py
- https://github.com/micropython-IMU/micropython-mpu9150

### Roche Christopher
- kalman.py
- https://github.com/rocheparadox/Kalman-Filter-Python-for-mpu6050

## Connections:
- SDA - 1
- SCL - 2

From this library you can get the raw values of MPU6050 using imu.py and vector3d.py. The sample.py file demonstrate the process of getting raw values by uisng I2C communication. And you can measure the tilt angle of a system by using kalman.py as shown in angle.py.
